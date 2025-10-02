#!/usr/bin/env python3
# scripts/fetch_orcid.py
# Aggressive extraction + detailed-work fetch for contributors
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
ORCID_WORK_URL_TEMPLATE = "https://pub.orcid.org/v3.0/{orcid}/work/{put_code}"

def fail(msg, code=1):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(code)

if not CLIENT_ID or not CLIENT_SECRET:
    fail("Missing ORCID_CLIENT_ID or ORCID_CLIENT_SECRET environment variables. Check repository secrets.")

OUT_DIR.mkdir(parents=True, exist_ok=True)

# --- helpers (normalize, filename, heuristics) --------------------------------
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
        if "value" in x and isinstance(x["value"], str):
            return x["value"]
        for k in ("title", "short-title", "translated-title", "credit-name", "given-names", "family-name", "contributor-name", "name"):
            v = x.get(k)
            if isinstance(v, str):
                return v
            if isinstance(v, dict) and isinstance(v.get("value"), str):
                return v.get("value")
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

def looks_like_name(s):
    if not s or not isinstance(s, str):
        return False
    s = s.strip()
    if len(s) > 80:
        return False
    if "http" in s or "doi.org" in s or "@" in s:
        return False
    if " " in s and re.search(r"[A-Za-z]", s):
        if re.search(r"\b(dept|department|univ|university|institute|school|college|laboratory|lab)\b", s.lower()):
            return False
        if len(s.split()) > 6:
            return False
        return True
    if "," in s and re.search(r"[A-Za-z]", s) and len(s) < 80:
        return True
    return False

def deep_collect_strings(obj, max_found=50):
    found = []
    stack = [obj]
    while stack and len(found) < max_found:
        cur = stack.pop()
        if isinstance(cur, dict):
            for k, v in cur.items():
                if isinstance(v, str):
                    if looks_like_name(v):
                        found.append(v.strip())
                elif isinstance(v, (dict, list)):
                    stack.append(v)
                if isinstance(k, str) and looks_like_name(k):
                    found.append(k.strip())
        elif isinstance(cur, list):
            for item in cur:
                if isinstance(item, str):
                    if looks_like_name(item):
                        found.append(item.strip())
                else:
                    stack.append(item)
        elif isinstance(cur, str):
            if looks_like_name(cur):
                found.append(cur.strip())
    seen = set(); out = []
    for s in found:
        if s not in seen:
            out.append(s); seen.add(s)
    return out

# --- contributor extraction helpers ------------------------------------------
def extract_contrib_name(c):
    if not isinstance(c, dict):
        return None
    if c.get("credit-name"):
        v = c.get("credit-name")
        if isinstance(v, dict):
            v = v.get("value")
        if looks_like_name(normalize_to_string(v)):
            return normalize_to_string(v)
    if c.get("contributor-name"):
        v = c.get("contributor-name")
        if looks_like_name(normalize_to_string(v)):
            return normalize_to_string(v)
    given = None; family = None
    if c.get("given-names"):
        given = normalize_to_string((c.get("given-names") or {}).get("value") if isinstance(c.get("given-names"), dict) else c.get("given-names"))
    if c.get("family-name"):
        family = normalize_to_string((c.get("family-name") or {}).get("value") if isinstance(c.get("family-name"), dict) else c.get("family-name"))
    if given or family:
        cand = " ".join([p for p in [given, family] if p])
        if looks_like_name(cand):
            return cand
    for k in ("name","value"):
        if k in c and isinstance(c[k], str) and looks_like_name(c[k]):
            return c[k]
    return None

def find_authors_targets(summary, item):
    authors = []
    if summary and isinstance(summary, dict) and summary.get("contributors"):
        cont = summary.get("contributors")
        entries = ensure_list(cont.get("contributor") if isinstance(cont, dict) and "contributor" in cont else cont)
        for e in entries:
            n = extract_contrib_name(e) or (extract_contrib_name(e.get("contributor")) if isinstance(e, dict) and e.get("contributor") else None)
            if n:
                authors.append(n)
    if not authors:
        work_obj = item.get("work") if isinstance(item, dict) else None
        if work_obj and isinstance(work_obj, dict) and work_obj.get("contributors"):
            cont = work_obj.get("contributors")
            entries = ensure_list(cont.get("contributor") if isinstance(cont, dict) and "contributor" in cont else cont)
            for e in entries:
                n = extract_contrib_name(e)
                if n:
                    authors.append(n)
    if not authors:
        if item and isinstance(item, dict) and item.get("contributors"):
            cont = item.get("contributors")
            entries = ensure_list(cont.get("contributor") if isinstance(cont, dict) and "contributor" in cont else cont)
            for e in entries:
                n = extract_contrib_name(e)
                if n:
                    authors.append(n)
    seen = set(); out=[]
    for a in authors:
        if a not in seen:
            out.append(a); seen.add(a)
    return out

# --- parse group item and attempt detailed work fetch when needed -------------
def parse_group_item_with_details(item, i, headers):
    summaries = ensure_list(item.get("work-summary") or [])
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
        y = normalize_to_string((pubdate.get("year") or {}).get("value") if pubdate.get("year") else None)
        m = normalize_to_string((pubdate.get("month") or {}).get("value") if pubdate.get("month") else None)
        d = normalize_to_string((pubdate.get("day") or {}).get("value") if pubdate.get("day") else None)
        if y:
            year = f"{y}-{m or '01'}-{d or '01'}"

    # external ids
    doi = None; url = None
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

    # targeted extraction
    authors = find_authors_targets(summary, item)
    used_deep = False
    used_detailed = False

    # If no authors found, try fetching detailed work records by put-code
    if not authors and summaries:
        for s in summaries:
            put = s.get("put-code") or s.get("put_code") or None
            if not put:
                continue
            work_url = ORCID_WORK_URL_TEMPLATE.format(orcid=ORCID, put_code=put)
            try:
                r = requests.get(work_url, headers=headers, timeout=20)
            except Exception as e:
                print(f"Could not fetch detailed work {put}: {e}")
                continue
            if r.status_code != 200:
                # skip non-200 details
                # print short debug
                print(f"Detailed work {put} returned {r.status_code}")
                continue
            try:
                work_json = r.json()
            except Exception:
                print(f"Detailed work {put} response not JSON")
                continue
            # The detailed work JSON often contains 'contributors' (object with contributor list)
            cont_block = work_json.get("contributors") or {}
            entries = []
            if isinstance(cont_block, dict) and "contributor" in cont_block:
                entries = ensure_list(cont_block.get("contributor"))
            elif cont_block:
                entries = ensure_list(cont_block)
            # try to extract names
            for c in entries:
                name = extract_contrib_name(c)
                if name and name not in authors:
                    authors.append(name)
            if authors:
                used_detailed = True
                print(f"Detailed work {put} provided authors: {authors}")
                break

    # aggressive fallback: deep scan
    if not authors:
        candidates = deep_collect_strings(item)
        if candidates:
            used_deep = True
            authors = candidates[:6]

    diag = {
        "summary_contributors_present": bool(summary.get("contributors")),
        "item_contributors_present": bool(item.get("contributors")),
        "work_object_present": bool(item.get("work")),
        "authors_found_count": len(authors),
        "used_deep_scan": used_deep,
        "used_detailed_fetch": used_detailed
    }

    abstract = normalize_to_string(summary.get("short-description") or summary.get("description") or item.get("short-description") or "")
    return {
        "title": title,
        "year": year,
        "doi": doi,
        "url": url,
        "authors": authors,
        "abstract": abstract.strip(),
        "diag": diag
    }

def mk_markdown(parsed, idx):
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
    # write debug snippet (first few groups)
    try:
        debug_file = OUT_DIR / f"orcid-debug-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
        with open(debug_file, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(works_group[:6], indent=2))
        written.append(str(debug_file))
        print("WROTE debug file:", debug_file)
    except Exception as e:
        print("Could not write debug JSON:", e)

    for i, item in enumerate(works_group):
        parsed = parse_group_item_with_details(item, i, headers)
        print(f"[{i}] title='{parsed['title'][:120]}' authors_found={len(parsed['authors'])} diag={parsed['diag']}")
        if parsed['authors']:
            print(f"    authors: {parsed['authors']}")
        else:
            print("    authors: (none found by script)")
        filename, content = mk_markdown(parsed, i)
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(str(filename))
        print("WROTE", filename)

    # timestamp file so commit always occurs
    try:
        ts_file = OUT_DIR / ".fetched_at"
        with open(ts_file, "w", encoding="utf-8") as fh:
            fh.write(datetime.utcnow().isoformat() + "Z\n")
        if str(ts_file) not in written:
            written.append(str(ts_file))
        print("WROTE timestamp file:", ts_file)
    except Exception as e:
        print("Could not write timestamp file:", e)

    print(f"Wrote {len(written)} publication files to {OUT_DIR}")

if __name__ == "__main__":
    main()
