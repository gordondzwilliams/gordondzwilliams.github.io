#!/usr/bin/env python3
# scripts/fetch_orcid.py (fixed: safe handling for missing fields)
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

def safe_filename(s):
    s = re.sub(r"[^\w\s-]", "", s or "").strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:200]

def parse_work_summary(ws):
    # ws may be None or missing many fields; handle safely
    if not isinstance(ws, dict):
        ws = {}

    # title
    title = ""
    try:
        title = (
            (ws.get("work-title") or {}).get("title", {}).get("value")
            or ws.get("title")
            or ws.get("short-title")
            or ""
        )
    except Exception:
        title = ""

    # publication date -> produce YYYY-MM-DD string if possible
    pubdate = ws.get("publication-date") or {}
    year = None
    if isinstance(pubdate, dict) and pubdate:
        y = (pubdate.get("year") or {}).get("value")
        m = (pubdate.get("month") or {}).get("value")
        d = (pubdate.get("day") or {}).get("value")
        if y:
            year = f"{y}-{m or '01'}-{d or '01'}"

    # external ids
    doi = None
    url = None
    ext_ids = ws.get("external-ids", {}).get("external-id", []) or []
    # normalize to list
    if isinstance(ext_ids, dict):
        ext_ids = [ext_ids]
    for e in ext_ids:
        if not isinstance(e, dict):
            continue
        id_type = (e.get("external-id-type") or "").lower()
        if id_type == "doi" and not doi:
            doi = e.get("external-id-value")
        elif id_type in ("url", "uri") and not url:
            url = (e.get("external-id-url") or {}).get("value") or e.get("external-id-value")

    # authors/contributors
    authors = []
    contribs = ws.get("contributors", {}).get("contributor", []) or []
    if isinstance(contribs, dict):
        contribs = [contribs]
    for c in contribs:
        if not isinstance(c, dict):
            continue
        name = None
        if c.get("credit-name"):
            name = (c.get("credit-name") or {}).get("value")
        # fallback to contributor name structure if present
        if not name:
            given = (c.get("given-names") or {}).get("value") if c.get("given-names") else None
            family = (c.get("family-name") or {}).get("value") if c.get("family-name") else None
            if given or family:
                name = " ".join([p for p in [given, family] if p])
        if name:
            authors.append(name)

    # abstract/description
    abstract = ws.get("short-description") or ws.get("description") or ""
    if abstract is None:
        abstract = ""

    return {
        "title": title or "Untitled",
        "year": year,
        "doi": doi,
        "url": url,
        "authors": authors,
        "abstract": (abstract or "").strip()
    }

def mk_markdown(item, idx):
    summaries = item.get("work-summary", []) or []
    if isinstance(summaries, dict):
        summaries = [summaries]
    summary = summaries[0] if summaries else item if isinstance(item, dict) else {}
    parsed = parse_work_summary(summary)
    slug = safe_filename(parsed["title"]) or f"publication-{idx}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
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
