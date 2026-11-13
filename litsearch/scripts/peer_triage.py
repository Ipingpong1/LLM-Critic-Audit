"""Dedupe the peer-stream corpora and print candidates for title/abstract screening.

Usage:
  python3 -I peer_triage.py or  [min_score] [--abstracts] [--ids id1,id2]
  python3 -I peer_triage.py cr  [min_score]
  python3 -I peer_triage.py oa  [min_score]
Writes <src>_dedup.jsonl in the scratchpad (one record per paper, found_via aggregated).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import peer_lib as L  # noqa: E402

SRC = {"or": "or_corpus.jsonl", "cr": "cr_corpus.jsonl", "oa": "oa_corpus.jsonl"}


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def load(src):
    path = os.path.join(L.SCRATCH, SRC[src])
    recs = {}
    for line in open(path):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if src == "or":
            k = r["forum"] or r["id"]
        elif src == "cr":
            k = (r.get("doi") or "").lower()
        else:
            k = r.get("openalex")
        if not k:
            continue
        if k in recs:
            recs[k]["found_via"].add(r["found_via"])
        else:
            r["found_via"] = {r["found_via"]}
            # re-classify (classifier may have been refined after the run)
            text = " ".join([r.get("title") or "", r.get("abstract") or "", r.get("keywords") or "",
                             r.get("tldr") or ""])
            r["cl"] = L.classify(text)
            recs[k] = r
    out = os.path.join(L.SCRATCH, f"{src}_dedup.jsonl")
    with open(out, "w") as f:
        for k, r in recs.items():
            r2 = dict(r)
            r2["key"] = k
            r2["found_via"] = sorted(r["found_via"])
            f.write(json.dumps(r2) + "\n")
    return recs


def main():
    src = sys.argv[1]
    min_score = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 0
    show_abs = "--abstracts" in sys.argv
    only = None
    if "--ids" in sys.argv:
        only = set(sys.argv[sys.argv.index("--ids") + 1].split(","))
    recs = load(src)
    rows = []
    for k, r in recs.items():
        if only is not None:
            if k in only:
                rows.append((99, k, r))
            continue
        yr = r.get("year") or 0
        if yr and yr < 2022:
            continue
        cl = r["cl"]
        if src == "cr":
            ok = cl["LLM"] and bool(cl["A"] or cl["B"] or cl["C"])
        else:
            ok = cl["hit"]
        if ok and cl["score"] >= min_score:
            rows.append((cl["score"], k, r))
    rows.sort(key=lambda x: (-x[0], x[1]))
    print(f"# {src}: {len(recs)} unique records; {len(rows)} candidates (min_score={min_score})")
    for s, k, r in rows:
        venue = r.get("venue") or r.get("primary_source") or ""
        if src == "or":
            venue = f"{r.get('venue')} [{r.get('venueid')}]"
        print(f"{s:2d} | {k} | {r.get('year')} | {venue[:70]} | {r.get('title')[:150]} | "
              f"S={','.join(r['cl']['strong'])}")
        if show_abs:
            print("     ABS:", (r.get("abstract") or "")[:1800].replace("\n", " "))
            if r.get("keywords"):
                print("     KW:", r["keywords"][:200])


if __name__ == "__main__":
    main()
