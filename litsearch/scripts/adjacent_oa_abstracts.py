#!/usr/bin/env python3
"""Fetch OpenAlex abstracts (inverted index) by DOI for the adjacent stream's background refs.
argv[1]: JSONL with 'key' and 'doi' fields (Crossref verify output); argv[2]: output JSONL.
Raw responses under ../raw/adjacent/openalex_abs/. ~1.5 req/s, 60 s backoff on 429, no mailto."""
import json, os, re, sys, time, urllib.parse, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "adjacent", "openalex_abs")
os.makedirs(RAW, exist_ok=True)
UA = "critic-sdt-litsearch/0.1 (academic literature search; no contact)"
def get(url):
    for _ in range(4):
        time.sleep(0.7)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            if e.code == 429: time.sleep(60); continue
            raise
    return None
def deinv(inv):
    if not inv: return ""
    pos = sorted((i, w) for w, idx in inv.items() for i in idx)
    return " ".join(w for _, w in pos)
with open(sys.argv[2], "a") as out:
    for line in open(sys.argv[1]):
        r = json.loads(line)
        doi = r.get("doi") or r.get("query_doi")
        if not doi or r.get("status") != "found":
            continue
        t = get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi, safe="/:()") + "?select=id,doi,title,publication_year,cited_by_count,abstract_inverted_index")
        rec = {"key": r["key"], "doi": doi}
        if t:
            open(os.path.join(RAW, re.sub(r"[^A-Za-z0-9]+", "_", doi) + ".json"), "w").write(t)
            d = json.loads(t)
            rec.update({"oa_id": d.get("id"), "oa_title": d.get("title"), "cited_by": d.get("cited_by_count"), "abstract": deinv(d.get("abstract_inverted_index"))})
        else:
            rec["oa"] = "not found"
        out.write(json.dumps(rec) + "\n"); out.flush()
print("done")
