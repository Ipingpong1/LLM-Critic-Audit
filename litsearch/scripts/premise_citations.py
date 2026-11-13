#!/usr/bin/env python3
"""Forward and backward citations for the claim-test addendum (2026-11-10).

Usage:
  python3 -I premise_citations.py s2 <arxiv_id> [...]        # Semantic Scholar citations + references
  python3 -I premise_citations.py openalex <arxiv_id> [...]  # OpenAlex record + citing works
  python3 -I premise_citations.py show                       # print what was retrieved

Raw JSON goes to raw/premise/s2/ and raw/premise/openalex/; one line per call is appended to
raw/premise/citations_calls.tsv (time, source, kind, id, HTTP status, rows).

Etiquette (streams/README.md): Semantic Scholar one request per 3 s, on HTTP 429 wait 60 s and retry at
most 5 times; OpenAlex at most 1 request per second. No API keys, no mailto, no personal data.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "premise")
CALLS = os.path.join(RAW, "citations_calls.tsv")
UA = "litsearch-systematic-review/1.0 (python-urllib; academic literature search; no key)"
S2F = "title,externalIds,year,venue,publicationDate,abstract,authors"


def log(*f):
    with open(CALLS, "a") as fh:
        fh.write("\t".join(str(x) for x in f) + "\n")


def get(url, gap, tries_429=5):
    n429 = 0
    while True:
        time.sleep(gap)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and n429 < tries_429:
                n429 += 1
                time.sleep(60)
                continue
            return e.code, b""
        except Exception:
            return 0, b""


def s2(ids):
    os.makedirs(os.path.join(RAW, "s2"), exist_ok=True)
    for aid in ids:
        for kind in ("citations", "references"):
            out = os.path.join(RAW, "s2", f"{kind}_{aid}.json")
            if os.path.exists(out):
                continue
            url = (f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{aid}/{kind}"
                   f"?fields={S2F}&limit=1000")
            st, body = get(url, 3.0)
            rows = -1
            if st == 200:
                with open(out, "wb") as fh:
                    fh.write(body)
                rows = len(json.loads(body).get("data", []))
            log(time.strftime("%Y-%m-%dT%H:%M:%S"), "s2", kind, aid, st, rows)
            print(f"s2 {kind} {aid}: HTTP {st}, rows {rows}", flush=True)


def openalex(ids):
    os.makedirs(os.path.join(RAW, "openalex"), exist_ok=True)
    for aid in ids:
        rec = os.path.join(RAW, "openalex", f"work_{aid}.json")
        if not os.path.exists(rec):
            url = "https://api.openalex.org/works/https://doi.org/10.48550/arXiv." + aid
            st, body = get(url, 1.0, tries_429=0)
            log(time.strftime("%Y-%m-%dT%H:%M:%S"), "openalex", "work", aid, st, 1 if st == 200 else 0)
            print(f"openalex work {aid}: HTTP {st}", flush=True)
            if st != 200:
                continue
            with open(rec, "wb") as fh:
                fh.write(body)
        wid = json.load(open(rec)).get("id", "").rsplit("/", 1)[-1]
        out = os.path.join(RAW, "openalex", f"citing_{aid}.json")
        if wid and not os.path.exists(out):
            url = f"https://api.openalex.org/works?filter=cites:{wid}&per_page=200"
            st, body = get(url, 1.0, tries_429=0)
            rows = -1
            if st == 200:
                with open(out, "wb") as fh:
                    fh.write(body)
                rows = len(json.loads(body).get("results", []))
            log(time.strftime("%Y-%m-%dT%H:%M:%S"), "openalex", "citing", aid, st, rows)
            print(f"openalex citing {aid} ({wid}): HTTP {st}, rows {rows}", flush=True)


def show():
    d = os.path.join(RAW, "s2")
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if not fn.endswith(".json") or fn.startswith("_"):
            continue
        kind = fn.split("_")[0]
        key = "citingPaper" if kind == "citations" else "citedPaper"
        data = json.load(open(os.path.join(d, fn))).get("data", [])
        print(f"## {fn}: {len(data)} rows")
        for row in data:
            p = row.get(key) or {}
            ext = p.get("externalIds") or {}
            pid = ext.get("ArXiv") or ext.get("DOI") or ext.get("CorpusId")
            print(f"{pid}\t{p.get('year')}\t{(p.get('title') or '')[:150]}")
    d = os.path.join(RAW, "openalex")
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if not fn.startswith("citing_"):
            continue
        data = json.load(open(os.path.join(d, fn))).get("results", [])
        print(f"## {fn}: {len(data)} rows")
        for w in data:
            print(f"{w.get('doi')}\t{w.get('publication_year')}\t{(w.get('title') or '')[:150]}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(1)
    if a[0] == "s2":
        s2(a[1:])
    elif a[0] == "openalex":
        openalex(a[1:])
    elif a[0] == "show":
        show()
