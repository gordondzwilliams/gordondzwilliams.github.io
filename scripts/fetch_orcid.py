#!/usr/bin/env python3
# scripts/fetch_orcid.py (improved author extraction)
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
        # try direct 'value'
        if "value" in x and isinstance(x["value"], str):
            return x["value"]
        # try title.title.value pattern
        t = x.get("title") or x.get("translated-title") or x.get("short-title")
        if isinstance(t, dict) and isinstance(t.get("value"), str):
            return t.get("value")
        # try flattening common subkeys
        for k in ("title", "short-title", "translated-title", "subtitle"):
            v = x.get(k)
            if isinstance(v, str):
                return v
            if isinstance(v, dict) and isinstance(v.get("value"), str):
                return v.get("value")
        # fallback: find first string child value
        for val in x.values():
            if isinstance(val, str):
                return val
            if isinstance(val, dict) and isinstance(val.get("value"), str):
                return val.get("value")
        return ""
    # otherwise
    try:
        return str(x)
    except Exception:
        return ""

def safe_filename(s):
    s = normalize_to_string(s) or ""
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:200] or ""

def extract_authors_from_contribs(contribs):
    """Normalize contributors block (which may be list or dict)."""
    authors = []
    if not contribs:
        return authors
    if isinstance(contribs, dict):
        contribs = [contribs]
    for c in contribs:
        if not isinstance(c, dict):
            continue
        # credit-name
        name = ""
        if c.get("credit-name"):
            name = normalize_to_string(c.get("credit-name"))
        # ORCID sometimes nests credit-name as {"value": "..."}
        if not name and isinstance(c.get("credit-name"), dict):
            name = normalize_to_string(c.get("credit-name").get("value") if isinstance(c.get("credit-name"), dict) else None)
        # given/family fallback
        if not name:
            given = normalize_to_string((c.get("given-names") or {}).get("value") if c.get("given-names") else None)
            family = normalize_to_string((c.get("family-name") or {}).get("value") if c.get("family-name") else None)
            if given or family:
                name = " ".join([p for p in [given, family] if p])
        # contributor name key sometimes different
        if not name and c.get("contributor-name"):
            name = normalize_to_string(c.get("contributor-name"))
        if name:
            authors.append(name)
    return authors

def parse_work_summary(summary, item_fallback=None):
    """
    summary: the work-summary dictionary (or fallback)
    item_fallback: the group-level item (the parent) to search for contributors if needed
    """
    if not isinstance(summary, dict):
        summary = {}

    # title
    title_raw = None
    if summary.get("work-title"):
        title_raw = (summary.get("work-title") or {}).get("title") or summary.get("work-title")
    title_raw = title_raw or summary.get("title") or summary.get("short-title") or ""
    title = normalize_to_string(title_raw) or "Untitled"

    # publication date
    pubdate = summary.get("publication-date") or {}
    year = None
    if isinstance(pubdate, dict) and pubdate:
        y = normalize_to_string((pubdate.get("year") or {}).get("value") if pubdate.get("year") else None)
        m = normalize_to_string((pubdate.get("month") or {}).get("value") if pubdate.get("month") else None)
        d = normalize_to_string((pubdate.get("day") or {}).get("value") if pubdate.get("day") else None)
        if y:
            year = f"{y}-{m or '01'}-{d or '01'}"

    # external ids
    doi = None
    url = None
    ext_ids = (summary.get("external-ids") or {}).get("external-id", []) or []
    if isinstance(ext_ids, dict):
        ext_ids = [ext_ids]
    for e in ext_ids:
        if not isinstance(e, dict):
            continue
        id_type = normalize_to_string(e.get("external-id-type")).lower()
        if id_type == "doi" and not doi:
            doi = normalize_to_string(e.get("external-id-value"))
        elif id_type in ("url", "uri") and not url:
            url = normalize_to_string((e.get("external-id-url") or {}).get("value") or e.get("external-id-value"))

    # authors: try summary->contributors, then fallback to item-level contributors, then to other fields
    authors = []
    # typical path in summary:
    if summary.get("contributors"):
        contributors = (summary.get("contributors") or {}).get("contributor") or summary.get("contributors")
        authors = extract_authors_from_contribs(contributors)

    # fallback: group-level contributors (item_fallback might contain them)
    if not authors and item_fallback:
        # item_fallback can be the group object that sometimes contains 'contributors'
        # Try several likely places:
        if item_fallback.get("contributors"):
            authors = extract_authors_from_contribs(item_fallback.get("contributors").get("contributor") or item_fallback.get("contributors"))
        # sometimes contributors live under item_fallback['work'] or item_fallback['work']['contributors']
        if not authors and item_fallback.get("work", {}).get("contributors"):
            authors = extract_authors_from_contribs(item_fallback.get("work", {}).get("contributors").get("contributor") or item_fallback.get("work", {}).get("contributors"))

    # last resort: try top-level person info? (not likely per-work)
    # keep authors possibly empty

    # abstract/description
    abstract = normalize_to_string(summary.get("short-description") or summary.get("description") or "")

    return {
        "title": title,
        "year": year,
        "doi": doi,
        "url": url,
        "authors": authors,
        "abstract": abstract.strip()
    }

def mk_markdown(item, idx):
    # item is a group entry; prefer the first work-summary for metadata
    summaries = item.get("work-summary", []) or []
    if isinstance(summaries, dict):
        summaries = [summaries]
    summary = summaries[0] if summaries else item if isinstance(item, dict) else {}
    parsed = parse_work_summary(summary, item_fallback=item)
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
        if v is None: continue
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
    print("ORCID record top-level keys:", list(data.keys()))
    works_group = data.get("activities-summary", {}).get("works", {}).get("group", []) or []
    if not works_group:
        print("activities-summary snippet:", json.dumps(data.get("activities-summary", {}), indent=2)[:2000])
        fail("No works found in ORCID record.")
    written = []
    for i, item in enumerate(works_group):
        filename, content = mk_markdown(item, i)
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(str(filename))
        print("WROTE", filename)
    print(f"Wrote {len(written)} publication files to {OUT_DIR}")

if __name__ == "__main__":
    main()
