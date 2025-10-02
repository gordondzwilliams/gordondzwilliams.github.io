#!/usr/bin/env python3
# scripts/fetch_orcid.py
# Requires: python3, requests, python-dateutil

import os, sys, requests, json, re
from pathlib import Path

ORCID = "0000-0002-9076-9635"  # <- your ORCID iD hardcoded here
CLIENT_ID = os.environ.get("ORCID_CLIENT_ID")
CLIENT_SECRET = os.environ.get("ORCID_CLIENT_SECRET")
OUT_DIR = Path("_publications")
ORCID_TOKEN_URL = "https://orcid.org/oauth/token"
ORCID_RECORD_URL_TEMPLATE = "https://pub.orcid.org/v3.0/{orcid}/record"

if not CLIENT_ID or not CLIENT_SECRET:
    print("Missing ORCID_CLIENT_ID or ORCID_CLIENT_SECRET environment variables.", file=sys.stderr)
    sys.exit(2)

OUT_DIR.mkdir(parents=True, exist_ok=True)

def get_token():
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "/read-public"
    }
    r = requests.post(ORCID_TOKEN_URL, data=data, headers={"Accept":"application/json"})
    r.raise_for_status()
    return r.json()["access_token"]

def safe_filename(s):
    s = re.sub(r"[^\w\s-]", "", s).strip().lower()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:200]

def parse_work_summary(ws):
    title = ws.get("work-title", {}).get("title", {}).get("value", "")
    year = None
    pubdate = ws.get("publication-date", {})
    if pubdate:
        y = pubdate.get("year", {}).get("value")
        m = pubdate.get("month", {}).get("value")
        d = pubdate.get("day", {}).get("value")
        if y:
            year = f"{y}-{m or '01'}-{d or '01'}"
    doi = None
    url = None
    ext_ids = ws.get("external-ids", {}).get("external-id", [])
    for e in ext_ids:
        id_type = e.get("external-id-type","").lower()
        if id_type == "doi":
            doi = e.get("external-id-value")
        elif id_type in ("url","uri"):
            url = e.get("external-id-url", {}).get("value") or e.get("external-id-value")
    authors = []
    contribs = ws.get("contributors", {}).get("contributor", [])
    for c in contribs:
        name = c.get("credit-name", {}).get("value")
        if name:
            authors.append(name)
    abstract = ws.get("short-description") or ws.get("description") or ""
    return {
        "title": title or "Untitled",
        "year": year,
        "doi": doi,
        "url": url,
        "authors": authors,
        "abstract": abstract.strip()
    }

def mk_markdown(item, idx):
    summaries = item.get("work-summary", [])
    summary = summaries[0] if summaries else {}
    parsed = parse_work_summary(summary)
    slug = safe_filename(parsed["title"]) or f"publication-{idx}"
    filename = OUT_DIR / f"{parsed['year'][:4] if parsed['year'] else 'nodate'}-{slug}.md"
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
    token = get_token()
    headers = {"Accept":"application/json", "Authorization": f"Bearer {token}"}
    url = ORCID_RECORD_URL_TEMPLATE.format(orcid=ORCID)
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    works_group = data.get("activities-summary", {}).get("works", {}).get("group", [])
    if not works_group:
        print("No works found.", file=sys.stderr)
        return
    for i, item in enumerate(works_group):
        filename, content = mk_markdown(item, i)
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write(content)
        print("Wrote", filename)

if __name__ == "__main__":
    main()
