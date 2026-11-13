#!/usr/bin/env python3
"""Verify human-SDT background citations against Crossref (adjacent stream).
Input: TSV (key<TAB>doi_or_empty<TAB>bibliographic query). Output: JSONL summary to argv[2].
Raw Crossref responses saved under ../raw/adjacent/crossref/. <= ~1.6 requests/s, no mailto."""
import json, os, re, sys, time, urllib.parse, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "adjacent", "crossref")
os.makedirs(RAW, exist_ok=True)
UA = "critic-sdt-litsearch/0.1 (academic literature search; no contact)"

def get(url):
    for attempt in range(6):
        time.sleep(0.65)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 429:
                time.sleep(60); continue
            raise
    return None

def summarize(m):
    yr = None
    for k in ("published-print", "published-online", "issued", "created"):
        if m.get(k, {}).get("date-parts") and m[k]["date-parts"][0][0]:
            yr = m[k]["date-parts"][0][0]; break
    return {
        "doi": m.get("DOI"), "title": (m.get("title") or [""])[0],
        "authors": "; ".join(f"{a.get('family','')}, {a.get('given','')}".strip(", ") for a in m.get("author", [])),
        "year": yr, "journal": (m.get("container-title") or [""])[0], "volume": m.get("volume"),
        "issue": m.get("issue"), "pages": m.get("page"), "type": m.get("type"), "publisher": m.get("publisher"),
        "abstract": re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", m.get("abstract", ""))).strip(),
    }

inp, outp = sys.argv[1], sys.argv[2]
with open(inp) as f, open(outp, "a") as out:
    for line in f:
        if not line.strip() or line.startswith("#"):
            continue
        key, doi, q = (line.rstrip("\n").split("\t") + ["", ""])[:3]
        rec = {"key": key, "query_doi": doi, "query": q}
        if doi:
            t = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
            if t:
                open(os.path.join(RAW, re.sub(r"[^A-Za-z0-9]+", "_", doi) + ".json"), "w").write(t)
                rec["status"] = "found"; rec.update(summarize(json.loads(t)["message"]))
            else:
                rec["status"] = "doi_not_found"
        if q and rec.get("status") != "found":
            t = get("https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": q, "rows": "3"}))
            if t:
                open(os.path.join(RAW, "q_" + re.sub(r"[^A-Za-z0-9]+", "_", q)[:80] + ".json"), "w").write(t)
                items = json.loads(t)["message"]["items"]
                rec["status"] = rec.get("status", "") + "|query_candidates"
                rec["candidates"] = [summarize(m) for m in items]
        out.write(json.dumps(rec) + "\n"); out.flush()
print("done")
