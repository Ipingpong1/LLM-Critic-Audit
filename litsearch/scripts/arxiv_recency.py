#!/usr/bin/env python3
"""Recency sweep filter (submissions 2026-10-15 to 2026-11-06).

Usage: python3 -I arxiv_recency.py <recency_candidates.jsonl> <screened_ids.txt> <out_tsv>

Keeps candidates whose title or abstract literally mentions one of the recency terms (the API stems,
e.g. critic = critical, reviewer = review, monitor = monitoring, verifier = verify), restricted to
primary or cross-list categories cs.CL, cs.AI, cs.LG, cs.SE, cs.HC, cs.CY and v1 submission dates in
the window. Writes all kept ids with a flag for whether their title was already read in the main sweep.
"""
import json
import re
import sys

TERMS = {
    "judge": r"\bjudg(?:e|es|ing)\b|\bLLMs?[- ]as[- ](?:an?[- ])?judges?\b",
    "verifier": r"\bverifiers?\b",
    "critic": r"\bcritics?\b",
    "critique": r"\bcritiqu(?:e|es|ed|ing)\b",
    "reward model": r"\breward[- ]models?\b",
    "self-correct": r"\bself[- ]?correct\w*",
    "self-refine": r"\bself[- ]?refin\w*",
    "reviewer": r"\breviewers?\b",
    "overseer": r"\boverseers?\b",
    "monitor": r"\bmonitor(?:s|ed|ing)?\b",
    "grader": r"\bgraders?\b",
}
RX = {k: re.compile(v, re.I) for k, v in TERMS.items()}
CATS = {"cs.CL", "cs.AI", "cs.LG", "cs.SE", "cs.HC", "cs.CY"}


def main(cand, screened_file, out):
    screened = {l.strip() for l in open(screened_file, encoding="utf-8") if l.strip()}
    rows, n_all, n_cat, n_date = [], 0, 0, 0
    for line in open(cand, encoding="utf-8"):
        r = json.loads(line)
        n_all += 1
        if not (set(r["categories"]) & CATS):
            continue
        n_cat += 1
        pub = r["published"][:10]
        if not ("2026-10-15" <= pub <= "2026-11-06"):
            continue
        n_date += 1
        text = r["title"] + " \n " + r["abstract"]
        hits = [k for k, rx in RX.items() if rx.search(text)]
        if not hits:
            continue
        rows.append((pub, r["id"], ",".join(hits), "screened" if r["id"] in screened else "new", r["title"]))
    rows.sort()
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("published\tid\tterms\tstatus\ttitle\n")
        for row in rows:
            fh.write("\t".join(row) + "\n")
    new = sum(1 for r in rows if r[3] == "new")
    print(f"recency candidates={n_all} in_categories={n_cat} in_window(v1)={n_date} literal_term_match={len(rows)} "
          f"already_screened={len(rows) - new} new_to_read={new}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
