#!/usr/bin/env python3
# scripts/fetch_orcid.py (aggressive author extraction + diagnostics)
# Requires: python3, requests

import os, sys, requests, json, re
from pathlib import Path
from datetime import datetime

ORCID = "0000-0002-9076-9635"
CLIENT_ID = os.environ.get("ORCID_CLIENT_ID")
CLIENT_SECRET = os.environ.get("ORCID_CLIENT_SECRET")
OUT_DIR = Path("_publications")
ORCID_TOKEN_URL = "https://orcid.org/oauth/token"
ORCID_RECORD_URL_TEMPLATE = "https://pub.orcid.org/v3.0/{orcid}/record"

def fail(msg, code=1):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(code)

if not CLIENT_ID or not CLIENT_SECRET:
    fail("Missing ORCID_CLIENT_ID or ORCID_CLIENT_SECRET environment variables. Check repository secrets.")

OUT_DIR.mkdir(parents=True, exist_ok=True)

def get_token():
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "/read-public"
    }
    headers = {"Accept": "application/json"}
    r = requests.post(ORCID_TOKEN_URL, data=data, headers=headers, timeout=30)
    if r.status_code != 200:
        print("Token response:", r.status_code, r.text)
        fail("Failed to obtain token from ORCID.")
    body = r.json()
    token = body.get("access_token")
    if not token:
        print("Token JSON:", json.dumps(body, indent=2))
        fail("No access_token in ORCID response.")
    print("Successfully obtained ORCID token (expires_in: {})".format(body.get("expires_in")))
    return token

def normalize_to_string(x):
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    if isinstance(x, (int, float)):
        return str(x)
    if isinstance(x, dict):
        # common nested patterns
        if "value" in x and isinstance(x["value"], str):
            return x["value"]
        for k in ("title", "short-title", "translated-title", "credit-name", "given-names", "family-name"):
            v = x.get(k)
            if isinstance(v, str):
                return v
            if isinstance(v, dict) and isinstance(v.get("value"), str):
                return v.get("value")
        # try nested title.title.value
        t = x.get("title") or {}
        if isinstance(t, dict):
            inner = t.get("title") or t.get("value") or {}
            if isinstance(inner, dict) and isinstance(inner.get("value"), str):
                return inner.get("value")
        # fallback: return first string child
        for val in x.values():
            if isinstance(val, str):
                return val
            if isinstance(val, dict) and isinstance(val.get("value"), str):
                return val.get("value")
        return ""
    try:
        return str(x)
    except Exception:
        return ""

def safe_filename(s):
    s = normalize_to_string(s) or ""
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:200] or ""

def ensure_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]

def extract_contrib_name(c):
    # c is a dict contributor entry in many possible shapes
    if not isinstance(c, dict):
        return None
    # Try credit-name
    if c.get("credit-name"):
        name = normalize_to_string(c.get("credit-name"))
        if name:
            return name
    # Try contributor-name
    if c.get("contributor-name"):
        name = normalize_to_string(c.get("contributor-name"))
        if name:
            return name
    # Try given/family
    given = None
    family = None
    if c.get("given-names"):
        given = normalize_to_string((c.get("given-names") or {}).get("value") if isinstance(c.get("given-names"), dict) else c.get("given-names"))
    if c.get("family-name"):
        family = normalize_to_string((c.get("family-name") or {}).get("value") if isinstance(c.get("family-name"), dict) else c.get("family-name"))
    if given or family:
        return " ".join([p for p in [given, family] if p])
    # Try contributor-orcid name, sometimes stored differently
    if c.get("contributor-orcid"):
        # contributor-orcid rarely contains names; skip
        pass
    # last: try any 'name' or 'value' subfields
    for k in ("name","value"):
        if k in c and isinstance(c[k], str):
            return c[k]
    # None found
    return None

def find_authors_in_summary(summary):
    # look in summary->contributors
    if not summary or not isinstance(summary, dict):
        return []
    cont_block = summary.get("contributors")
    if not cont_block:
        return []
    # cont_block may be {'contributor': [...] } or list or dict
    if isinstance(cont_block, dict) and "contributor" in cont_block:
        entries = ensure_list(cont_block["contributor"])
    else:
        entries = ensure_list(cont_block)
    authors = []
    for c in entries:
        name = extract_contrib_name(c) or extract_contrib_name(c.get("contributor") if isinstance(c.get("contributor"), dict) else c)
        if name:
            authors.append(name)
    return authors

def find_authors_in_item(item):
    # item is the group-level object from activities-summary. Works can place contributors in many locations.
    authors = []
    if not item or not isinstance(item, dict):
        return authors

    # 1) item['work'] -> 'work' object sometimes exists
    work_obj = item.get("work") or {}
    if work_obj:
        # contributors at work_obj['contributors'] or work_obj['contributors']['contributor']
        cont = work_obj.get("contributors") or {}
        if cont:
            if isinstance(cont, dict) and "contributor" in cont:
                entries = ensure_list(cont["contributor"])
            else:
                entries = ensure_list(cont)
            for c in entries:
                name = extract_contrib_name(c)
                if name:
                    authors.append(name)
    # 2) top-level item['contributors']
    topc = item.get("contributors")
    if topc:
        if isinstance(topc, dict) and "contributor" in topc:
            entries = ensure_list(topc["contributor"])
        else:
            entries = ensure_list(topc)
        for c in entries:
            name = extract_contrib_name(c)
            if name and name not in authors:
                authors.append(name)

    # 3) some records put contributors under item['work-summary'][*]['contributors'] (we handle in summary pass)
    # 4) some records have 'creator' or 'authors' fields - scan whole item for obvious lists
    for key in ("contributors", "creator", "authors", "author"):
        if key in item and isinstance(item[key], (list, dict)):
            entries = ensure_list(item[key])
            for c in entries:
                name = extract_contrib_name(c)
                if name and name not in authors:
                    authors.append(name)

    return authors

def parse_item(item, idx):
    # item is group-level; prefer summary metadata but fallback to group-level fields
    summaries = item.get("work-summary") or []
    summaries = ensure_list(summaries)
    summary = summaries[0] if summaries else item if isinstance(item, dict) else {}
    # title
    title_raw = None
    if summary.get("work-title"):
        title_raw = (summary.get("work-title") or {}).get("title") or summary.get("work-title")
    title_raw = title_raw or summary.get("title") or item.get("title") or ""
    title = normalize_to_string(title_raw) or "Untitled"

    # date
    pubdate = (summary.get("publication-date") or {}) or (item.get("publication-date") or {})
    year = None
    if isinstance(pubdate, dict) and pubdate:
        y = normalize_to_string((pubdate.get("year") or {}).get("value") if pubdate.get("year") else (pubdate.get("year") or {}).get("value") )
        m = normalize_to_string((pubdate.get("month") or {}).get("value") if pubdate.get("month") else None)
        d = normalize_to_string((pubdate.get("day") or {}).get("value") if pubdate.get("day") else None)
        if y:
            year = f"{y}-{m or '01'}-{d or '01'}"

    # external ids (doi/url)
    doi = None
    url = None
    ext_ids = (summary.get("external-ids") or {}).get("external-id", []) or (item.get("external-ids") or {}).get("external-id", []) or []
    ext_ids = ensure_list(ext_ids)
    for e in ext_ids:
        if not isinstance(e, dict):
            continue
        id_type = normalize_to_string(e.get("external-id-type")).lower()
        if id_type == "doi" and not doi:
            doi = normalize_to_string(e.get("external-id-value"))
        elif id_type in ("url","uri") and not url:
            url = normalize_to_string((e.get("external-id-url") or {}).get("value") or e.get("external-id-value"))

    # authors: try summary contributors, then item-level places, then work_obj
    authors = []
    authors += find_authors_in_summary(summary)
    # fallback to item-level
    if not authors:
        authors += find_authors_in_item(item)
    # dedupe preserving order
    seen = set()
    authors = [a for a in authors if a and not (a in seen or seen.add(a))]

    # diagnostics: what contributor locations exist
    diag = {
        "summary_contributors_present": bool(summary.get("contributors")),
        "item_contributors_present": bool(item.get("contributors")),
        "work_object_present": bool(item.get("work")),
        "authors_found_count": len(authors)
    }
    return {
        "title": title,
        "year": year,
        "doi": doi,
        "url": url,
        "authors": authors,
        "abstract": normalize_to_string(summary.get("short-description") or summary.get("description") or item.get("short-description") or ""),
        "diag": diag
    }

def mk_markdown(parsed, idx):
    # parsed is the metadata dict returned from parse_item
    slug = safe_filename(parsed.get("title")) or f"publication-{idx}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    fname_prefix = (parsed.get('year') or '')[:4] or 'nodate'
    filename = OUT_DIR / f"{fname_prefix}-{slug}.md"
    front = {
        "layout": "publication",
        "title": parsed["title"],
        "authors": parsed["authors"],
        "year": (parsed["year"][:4] if parsed["year"] else None),
        "doi": parsed["doi"],
        "url": parsed["url"],
    }
    fm = "---\n"
    for k,v in front.items():
        if v is None:
            continue
        if isinstance(v, list):
            fm += f"{k}:\n"
            for elem in v:
                fm += f"  - \"{elem}\"\n"
        else:
            fm += f"{k}: \"{v}\"\n"
    fm += "---\n\n"
    body = parsed["abstract"] + "\n" if parsed["abstract"] else ""
    return filename, fm + body

def main():
    print("Starting ORCID fetch for", ORCID)
    token = get_token()
    headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
    url = ORCID_RECORD_URL_TEMPLATE.format(orcid=ORCID)
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code != 200:
        print("Record response:", r.status_code, r.text[:2000])
        fail("Failed to fetch ORCID record.")
    data = r.json()
    works_group = data.get("activities-summary", {}).get("works", {}).get("group", []) or []
    if not works_group:
        print("activities-summary snippet:", json.dumps(data.get("activities-summary", {}), indent=2)[:2000])
        fail("No works found in ORCID record.")
    written = []
    # Optional: save raw JSON for first group for debugging (committed)
    try:
        debug_file = OUT_DIR / f"orcid-debug-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
        with open(debug_file, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(works_group[:3], indent=2))
        print("WROTE debug file:", debug_file)
    except Exception as e:
        print("Could not write debug JSON:", e)
    # process each group item
    for i, item in enumerate(works_group):
        parsed = parse_item(item, i)
        # print quick diagnostic to logs so you can inspect contributor detection
        print(f"[{i}] title='{parsed['title'][:80]}' authors_found={len(parsed['authors'])} diag={parsed['diag']}")
        if parsed['authors']:
            print(f"    authors: {parsed['authors']}")
        else:
            print("    authors: (none found by script)")
        filename, content = mk_markdown(parsed, i)
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(str(filename))
        print("WROTE", filename)
    print(f"Wrote {len(written)} publication files to {OUT_DIR}")

if __name__ == "__main__":
    main()
