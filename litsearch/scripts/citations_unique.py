#!/usr/bin/env python3
"""Count unique records screened by the citations stream across all saved lists (python3 -I).
Dedup key: arXiv id, else DOI (lower case), else normalized title prefix."""
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "citations")
sys.path.insert(0, HERE)


def norm(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())[:60]


keys = {}
title_of = {}


def add(src, arx=None, doi=None, title=None):
    k = None
    if arx:
        k = "arxiv:" + re.sub(r"v\d+$", "", arx)
    elif doi:
        m = re.search(r"arxiv\.(\d{4}\.\d{4,5})", doi, re.I)
        k = ("arxiv:" + m.group(1)) if m else "doi:" + doi.lower()
    elif title and norm(title):
        k = "t:" + norm(title)
    if not k:
        return
    # merge title-keyed duplicates
    if title and norm(title):
        tk = "t:" + norm(title)
        if tk in title_of and title_of[tk] != k and not k.startswith("t:"):
            pass
        if k.startswith("t:") and tk in title_of:
            k = title_of[tk]
        title_of.setdefault(tk, k)
    keys.setdefault(k, set()).add(src)


for f in glob.glob(os.path.join(RAW, "s2", "*.json")):
    js = json.load(open(f))
    rows = js if isinstance(js, list) else js.get("data", [])
    if os.path.basename(f).startswith(("known_batch", "match_")):
        continue
    for r in rows:
        p = r.get("citingPaper") or r.get("citedPaper") or r
        ex = p.get("externalIds") or {}
        add("s2:" + os.path.basename(f), ex.get("ArXiv"), ex.get("DOI"), p.get("title"))
for f in glob.glob(os.path.join(RAW, "openalex", "*.json")):
    b = os.path.basename(f)
    if not (b.startswith("cites_") or b.startswith("authorworks_")):
        continue
    for w in json.load(open(f)).get("results", []):
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        add("oa:" + b, None, doi or None, w.get("title"))
ns = {"a": "http://www.w3.org/2005/Atom"}
for f in glob.glob(os.path.join(RAW, "arxiv", "au_*.xml")):
    for e in ET.parse(f).getroot().findall("a:entry", ns):
        aid = e.find("a:id", ns).text.rsplit("/", 1)[1]
        add("arxiv:" + os.path.basename(f), aid, None, e.find("a:title", ns).text)
for f in glob.glob(os.path.join(RAW, "derived", "bib_*.txt")):
    seed = os.path.basename(f)[4:-4]
    if os.path.exists(os.path.join(RAW, "s2", f"ref_{seed}.json")):
        continue  # same list already counted from S2 references
    for line in open(f):
        m = re.search(r"arXiv[: ]+(?:preprint )?(?:arXiv:)?(\d{4}\.\d{4,5})", line)
        add("bib:" + os.path.basename(f), m.group(1) if m else None, None, line[:200])
# ProcessBench etc. counted above; report
by = {}
for k, srcs in keys.items():
    for s_ in srcs:
        by.setdefault(s_.split(":")[0], set()).add(k)
print("unique records:", len(keys))
for s_, ks in sorted(by.items()):
    print(f"  {s_}: {len(ks)}")
