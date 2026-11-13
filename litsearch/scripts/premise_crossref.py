#!/usr/bin/env python3
"""Crossref title search for the claim-test addendum (ACL Anthology, ACM, AAAI, IEEE prefixes).

Usage: python3 -I premise_crossref.py run     # runs the query grid below, saves raw JSON, prints counts
       python3 -I premise_crossref.py rank    # literal re-match on titles (+ abstracts where Crossref has them)

query.bibliographic is a relevance-ranked OR match, so the top 100 per query and prefix are taken and
re-matched locally. Raw responses: raw/premise/crossref/. One request per second, no mailto.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import premise_arxiv_screen as S  # noqa: E402

RAW = os.path.join(os.path.dirname(HERE), "raw", "premise", "crossref")
UA = "litsearch-systematic-review/1.0 (python-urllib; academic literature search; no key)"
PREFIXES = {"acl": "10.18653", "acm": "10.1145", "aaai": "10.1609", "ieee": "10.1109"}
QUERIES = [
    ("sycophancy language model", ["acl", "acm", "aaai", "ieee"]),
    ("false premise presupposition language model", ["acl", "aaai"]),
    ("LLM judge authority anchoring confirmation bias", ["acl", "acm", "aaai", "ieee"]),
    ("LLM evaluator misleading hint prior verdict deference", ["acl", "acm", "aaai"]),
    ("error detection language model false positive correct solutions", ["acl", "aaai"]),
    ("code review language model framing bias false positive", ["acm", "ieee"]),
    ("self-correction language model correct answers become incorrect", ["acl", "aaai"]),
    ("language model base rate Bayesian belief updating assertion", ["acl", "aaai", "acm"]),
    ("signal detection sycophancy language model criterion", ["acl", "acm", "aaai"]),
    ("language model source reliability testimony epistemic vigilance", ["acl", "aaai"]),
    ("verifier mathematical proof grading language model sycophancy", ["acl", "aaai"]),
]


def run():
    os.makedirs(RAW, exist_ok=True)
    for q, prefs in QUERIES:
        for p in prefs:
            slug = re.sub(r"[^a-z0-9]+", "_", q.lower())[:60] + "__" + p
            fn = os.path.join(RAW, slug + ".json")
            if not os.path.exists(fn):
                url = "https://api.crossref.org/works?" + urllib.parse.urlencode({
                    "query.bibliographic": q, "filter": f"prefix:{PREFIXES[p]},from-pub-date:2023-01-01",
                    "rows": 100, "select": "DOI,title,author,issued,container-title,abstract"})
                time.sleep(1.0)
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": UA})
                    with urllib.request.urlopen(req, timeout=90) as r:
                        body = r.read()
                except Exception as e:
                    print(f"{q} [{p}]: failed {e!r}")
                    continue
                with open(fn, "wb") as fh:
                    fh.write(body)
            d = json.load(open(fn))["message"]
            print(f"{q} [{p}]: total={d.get('total-results')} fetched={len(d.get('items', []))}", flush=True)


def rank():
    seen, rows = set(), []
    for fn in sorted(os.listdir(RAW)):
        if not fn.endswith(".json"):
            continue
        for it in json.load(open(os.path.join(RAW, fn)))["message"].get("items", []):
            doi = it.get("DOI", "").lower()
            if doi in seen:
                continue
            seen.add(doi)
            title = " ".join(it.get("title") or [""])
            abst = re.sub(r"<[^>]+>", " ", it.get("abstract") or "")
            t, s = S.tags_score(title + " \n " + abst)
            yr = ((it.get("issued") or {}).get("date-parts") or [[0]])[0][0]
            venue = " ".join(it.get("container-title") or [""])[:50]
            rows.append((s, "".join(sorted(t)), yr, doi, venue, title))
    rows.sort(key=lambda x: (-x[0], x[3]))
    with open(os.path.join(RAW, "ranked.tsv"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    print(f"unique DOIs: {len(rows)}")


if __name__ == "__main__":
    {"run": run, "rank": rank}[sys.argv[1]]()
