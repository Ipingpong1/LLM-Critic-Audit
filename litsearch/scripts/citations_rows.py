#!/usr/bin/env python3
"""Print rows (1-based, in file order) of an S2 citations/references file with abstract and contexts.
usage: citations_rows.py FILE.json ROWSPEC [abs_chars] [ctx_chars]   ROWSPEC like 1,5,9-12 or 'match:REGEX'"""
import json, re, sys
js = json.load(open(sys.argv[1]))
spec = sys.argv[2]
na = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
nc = int(sys.argv[4]) if len(sys.argv) > 4 else 300
rows = js["data"]
sel = []
if spec.startswith("match:"):
    rx = re.compile(spec[6:], re.I)
    for i, r in enumerate(rows, 1):
        p = r.get("citingPaper") or r.get("citedPaper") or {}
        blob = " ".join([p.get("title") or "", p.get("abstract") or "", " ".join(r.get("contexts") or [])])
        if rx.search(blob):
            sel.append(i)
else:
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-"); sel.extend(range(int(a), int(b) + 1))
        else:
            sel.append(int(part))
for i in sel:
    r = rows[i - 1]
    p = r.get("citingPaper") or r.get("citedPaper") or {}
    ex = p.get("externalIds") or {}
    pid = ex.get("ArXiv") or ex.get("DOI") or "S2:" + str(p.get("paperId"))
    au = ", ".join(a.get("name", "") for a in (p.get("authors") or [])[:5])
    print(f"#{i} {pid} | {p.get('publicationDate') or p.get('year')} | {p.get('title')} | {p.get('venue') or ''} | {au}")
    for c in (r.get("contexts") or [])[:3]:
        print("   ctx:", re.sub(r"\s+", " ", c)[:nc])
    ab = p.get("abstract") or ""
    if ab and na:
        print("   abs:", re.sub(r"\s+", " ", ab)[:na])
