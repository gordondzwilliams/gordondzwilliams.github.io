#!/usr/bin/env python3
# scripts/fetch_orcid.py (fixed: handle dict-type titles safely)
# Requires: python3, requests, python-dateutil

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
    try:
        r = requests.post(ORCID_TOKEN_URL, data=data, headers=headers, timeout=30)
    except Exception as e:
        fail(f"Token request failed to connect: {e}")
    if r.status_code != 200:
        print("Token request returned status", r.status_code)
        print("Token response body:", r.text)
        fail("Failed to obtain token from ORCID. Check client id/secret and that they are valid for the Public API.")
    try:
        body = r.json()
    except Exception:
        print("Token response (non-json):", r.text)
        fail("Token response was not JSON.")
    token = body.get("access_token")
    if not token:
        print("Token response JSON:", json.dumps(body, indent=2))
        fail("No access_token in ORCID response.")
    print("Successfully obtained ORCID token (expires_in: {})".format(body.get("expires_in")))
    return token

def normalize_to_string(x):
    """
    Robustly coerce various ORCID fields to a plain string.
    - If x is a string, return it.
    - If x is a dict, try common subkeys (value, title/title/value, etc).
    - Otherwise return empty string.
    """
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    if isinstance(x, (int, float)):
        return str(x)
    if isinstance(x, dict):
        # common places ORCID stores textual value
        # Try nested patterns in order of common occurrence.
        candidates = []
        # direct common keys
        for k in ("value", "title", "short-title", "subtitle", "translated-title"):
            v = x.get(k) if isinstance(x.get(k), (str, dict)) else None
            if isinstance(v, str):
                candidates.append(v)
            elif isinstance(v, dict):
                # dive one level to look for 'value'
                vv = v.get("value")
                if isinstance(vv, str):
                    candidates.append(vv)
        # also check for deeper nested title.title.value pattern
        try:
            t = x.get("title", {})
            if isinstance(t, dict):
                inner = t.get("title", {})
                if isinstance(inner, dict):
                    vv = inner.get("value")
                    if isinstance(vv, str):
                        candidates.append(vv)
        except Exception:
            pass
        # Last resort, join any string-like fields
        for key, val in x.items():
            if isinstance(val, str):
                candidates.append(val)
            elif isinstance(val, dict) and isinstance(val.get("value"), str):
                candidates.append(val.get("value"))
        if candidates:
            return candidates[0]
        return ""
    # fallback: try str()
    try:
        return str(x)
    except Exception:
        return ""

def safe_filename(s):
    # ensure s is a string first
    s = normalize_to_string(s) or ""
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:200] or ""

def parse_work_summary(ws):
    # ws may be None or missing many fields; handle safely
    if not isinstance(ws, dict):
        ws = {}

    # title: robust extraction using normalize_to_string
    title_raw = None
    # try multiple places commonly used in ORCID payloads
    title_raw = (ws.get("work-title") or {}).get("title") if ws.get("work-title") else None
    if not title_raw:
        title_raw = ws.get("title") or ws.get("short-title") or ws.get("title", None)
    title = normalize_to_string(title_raw) or "Untitled"

    # publication date -> produce YYYY-MM-DD string if possible
    pubdate = ws.get("publication-date") or {}
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
    ext_ids = ws.get("external-ids", {}).get("external-id", []) or []
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

    # authors/contributors
    authors = []
    contribs = ws.get("contributors", {}).get("contributor", []) or []
    if isinstance(contribs, dict):
        contribs = [contribs]
    for c in contribs:
        if not isinstance(c, dict):
            continue
        name = ""
        if c.get("credit-name"):
            name = normalize_to_string((c.get("credit-name") or {}).get("value") if isinstance(c.get("credit-name"), dict) else c.get("credit-name"))
        if not name:
            # fallback to given/family structure
            given = normalize_to_string((c.get("given-names") or {}).get("value") if c.get("given-names") else None)
            family = normalize_to_string((c.get("family-name") or {}).get("value") if c.get("family-name") else None)
            if given or family:
                name = " ".join([p for p in [given, family] if p])
        if name:
            authors.append(name)

    # abstract/description
    abstract = normalize_to_string(ws.get("short-description") or ws.get("description") or "")

    return {
        "title": title,
        "year": year,
        "doi": doi,
        "url": url,
        "authors": authors,
        "abstract": abstract.strip()
    }

def mk_markdown(item, idx):
    summaries = item.get("work-summary", []) or []
    if isinstance(summaries, dict):
        summaries = [summaries]
    summary = summaries[0] if summaries else item if isinstance(item, dict) else {}
    parsed = parse_work_summary(summary)
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
    headers = {"Accept":"application/json", "Authorization": f"Bearer {token}"}
    url = ORCID_RECORD_URL_TEMPLATE.format(orcid=ORCID)
    try:
        r = requests.get(url, headers=headers, timeout=30)
    except Exception as e:
        fail(f"Failed to GET ORCID record: {e}")
    if r.status_code != 200:
        print("Record request returned status", r.status_code)
        print("Record response body:", r.text[:4000])
        fail("Failed to fetch ORCID record. Check ORCID API availability and token.")
    try:
        data = r.json()
    except Exception:
        print("Record response (non-json):", r.text[:4000])
        fail("ORCID record response was not JSON.")
    print("ORCID record top-level keys:", list(data.keys()))
    works_group = data.get("activities-summary", {}).get("works", {}).get("group", []) or []
    if not works_group:
        print("No works found in activities-summary. Dumping activities-summary snippet (for debugging):")
        print(json.dumps(data.get("activities-summary", {}) , indent=2)[:8000])
        fail("No works found in ORCID record; nothing to write.")
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
