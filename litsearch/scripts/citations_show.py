#!/usr/bin/env python3
"""Print S2 citation/reference lists or OpenAlex lists for screening (python3 -I).

  citations_show.py s2 FILE.json [--abs N] [--ctx N] [--grep REGEX]
  citations_show.py oa FILE.json [--abs N] [--grep REGEX]
  citations_show.py s2batch FILE.json [--abs N]

--grep keeps only rows whose title/abstract/contexts match REGEX (case-insensitive).
"""
import json
import re
import sys


def ident(p):
    ex = p.get("externalIds") or {}
    if ex.get("ArXiv"):
        return ex["ArXiv"]
    if ex.get("DOI"):
        return ex["DOI"]
    return "S2:" + str(p.get("paperId"))


def oa_abstract(inv):
    if not inv:
        return ""
    pos = []
    for w, idxs in inv.items():
        for i in idxs:
            pos.append((i, w))
    return " ".join(w for _, w in sorted(pos))


def main():
    mode, path = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    nabs = int(args[args.index("--abs") + 1]) if "--abs" in args else 0
    nctx = int(args[args.index("--ctx") + 1]) if "--ctx" in args else 0
    rx = re.compile(args[args.index("--grep") + 1], re.I) if "--grep" in args else None
    js = json.load(open(path))
    if mode in ("s2", "s2batch"):
        rows = js if mode == "s2batch" else js.get("data", [])
        for r in rows:
            if r is None:
                print("NULL")
                continue
            p = r if mode == "s2batch" else (r.get("citingPaper") or r.get("citedPaper") or {})
            ctxs = r.get("contexts") or [] if mode == "s2" else []
            intents = r.get("intents") or [] if mode == "s2" else []
            title = p.get("title") or ""
            abstract = p.get("abstract") or ""
            blob = " ".join([title, abstract, " ".join(ctxs)])
            if rx and not rx.search(blob):
                continue
            authors = ", ".join(a.get("name", "") for a in (p.get("authors") or [])[:6])
            print(f"{ident(p)} | {p.get('publicationDate') or p.get('year')} | {title} | {p.get('venue') or ''} | {authors}")
            if nctx and ctxs:
                for c in ctxs[:4]:
                    print("    ctx:", re.sub(r"\s+", " ", c)[:nctx])
                if intents:
                    print("    intents:", ",".join(intents))
            if nabs and abstract:
                print("    abs:", re.sub(r"\s+", " ", abstract)[:nabs])
    elif mode == "oa":
        for w in js.get("results", []):
            ids = w.get("ids") or {}
            doi = (w.get("doi") or "").replace("https://doi.org/", "")
            arx = ""
            m = re.search(r"arxiv\.(\d{4}\.\d{4,5})", doi, re.I)
            if m:
                arx = m.group(1)
            title = w.get("title") or ""
            abstract = oa_abstract(w.get("abstract_inverted_index"))
            if rx and not rx.search(title + " " + abstract):
                continue
            loc = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
            authors = ", ".join(a["author"]["display_name"] for a in (w.get("authorships") or [])[:6])
            print(f"{arx or doi or w.get('id')} | {w.get('publication_date')} | {title} | {loc} | {authors}")
            if nabs and abstract:
                print("    abs:", abstract[:nabs])


if __name__ == "__main__":
    main()
