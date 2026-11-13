#!/usr/bin/env python3
"""Screening helper for the `arxiv` stream.

  python3 -I arxiv_screen.py titles <ranked.jsonl> <tiers e.g. 1,2,3> <start> <n> [--exclude-ids file]
      prints "pos id title" for candidates in the given tiers (in ranked order), skipping known papers
      and ids listed in --exclude-ids (one id per line, first tab-separated field)
  python3 -I arxiv_screen.py abstracts <ranked.jsonl> <idfile>
      prints id, date, first authors, categories, matched terms, title and abstract for each id in idfile
      (first tab-separated field per line; lines starting with # ignored)
  python3 -I arxiv_screen.py count <ranked.jsonl> <tiers>
"""
import json
import sys


def load(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def read_ids(p):
    out = []
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if l and not l.startswith("#"):
            out.append(l.split("\t")[0].strip())
    return out


def main():
    cmd = sys.argv[1]
    rows = load(sys.argv[2])
    if cmd in ("titles", "count"):
        tiers = {int(t) for t in sys.argv[3].split(",")}
        excl = set()
        if "--exclude-ids" in sys.argv:
            excl = set(read_ids(sys.argv[sys.argv.index("--exclude-ids") + 1]))
        sel = [r for r in rows if r["tier"] in tiers and not r["known"] and r["id"] not in excl]
        if cmd == "count":
            print(len(sel))
            return
        start, n = int(sys.argv[4]), int(sys.argv[5])
        for i, r in enumerate(sel[start:start + n], start):
            t = r["title"]
            print(f"{i} {r['id']} {t[:150]}")
    elif cmd == "abstracts":
        ids = read_ids(sys.argv[3])
        by = {r["id"]: r for r in rows}
        for aid in ids:
            r = by.get(aid)
            if not r:
                print(f"## {aid}: NOT IN CANDIDATES\n")
                continue
            au = ", ".join(r["authors"][:4]) + (" et al." if len(r["authors"]) > 4 else "")
            print(f"## {aid} | {r['published'][:10]} | {au} | {r['primary_category']}"
                  + (f" | {r['journal_ref']}" if r['journal_ref'] else "") + (f" | c: {r['comment'][:120]}" if r['comment'] else ""))
            print(f"T: {r['title']}")
            print(f"A: {r['abstract']}\n")


if __name__ == "__main__":
    main()
