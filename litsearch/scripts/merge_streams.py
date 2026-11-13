"""Merge the per-stream logs in streams/ into query_log.csv and screening_log.csv.

Papers are deduplicated by arXiv id, then DOI, then normalized title. When a paper was
kept by several streams, the merged row keeps the highest relevance, the union of claims,
sources and routes, and the deepest reading level. Prints PRISMA-style counts.

    python3 -I scripts/merge_streams.py
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STREAMS = ROOT / "streams"
RANK = {"close": 3, "related": 2, "background": 1, "exclude": 0}
READ = {"yes": 2, "full": 2, "partial": 1, "no": 0}
QCOLS = ["date", "database", "query", "filters", "n_results", "n_screened", "n_kept", "notes"]
SCOLS = ["id", "title", "authors", "year", "venue_or_status", "source_database", "found_via", "relevance",
         "claims_touched", "manipulation", "measurement", "domain_models", "full_text_read", "notes"]

csv.field_size_limit(sys.maxsize)


def arxiv_id(*texts):
    for t in texts:
        m = re.search(r"\b(\d{4}\.\d{4,5})(v\d+)?\b", t or "")
        if m:
            return m.group(1)
    return None


def doi(*texts):
    for t in texts:
        m = re.search(r"10\.\d{4,9}/[^\s,;\"]+", t or "")
        if m:
            return m.group(0).rstrip(").").lower()
    return None


def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())[:120]


def key(row):
    a = arxiv_id(row.get("id"))
    if a:
        return "arxiv:" + a
    d = doi(row.get("id"))
    if d:
        return "doi:" + d
    return "title:" + norm_title(row.get("title"))


def union(*vals, sep="; "):
    out = []
    for v in vals:
        for part in re.split(r"\s*;\s*", v or ""):
            if part and part not in out:
                out.append(part)
    return sep.join(out)


def main():
    queries, papers, aliases = [], {}, {}
    for f in sorted(STREAMS.glob("*_query_log.csv")):
        stream = f.name.replace("_query_log.csv", "")
        for r in csv.DictReader(f.open()):
            r = {c: r.get(c, "") for c in QCOLS}
            r["notes"] = union(f"stream={stream}", r["notes"])
            queries.append(r)
    for f in sorted(STREAMS.glob("*_screening.csv")):
        stream = f.name.replace("_screening.csv", "")
        for r in csv.DictReader(f.open()):
            r = {c: (r.get(c) or "").strip() for c in SCOLS}
            if not r["title"]:
                continue
            k = key(r)
            # a title seen before under another key (e.g. arXiv id vs. title) maps to the same paper
            k = aliases.get("title:" + norm_title(r["title"]), k)
            aliases["title:" + norm_title(r["title"])] = k
            r["found_via"] = union(f"{stream}:{r['found_via']}" if r["found_via"] else stream)
            if k not in papers:
                papers[k] = r
                continue
            p = papers[k]
            if RANK.get(r["relevance"], 0) > RANK.get(p["relevance"], 0):
                p["relevance"] = r["relevance"]
            if READ.get(r["full_text_read"], 0) > READ.get(p["full_text_read"], 0):
                p["full_text_read"] = r["full_text_read"]
            for c in ["source_database", "found_via", "claims_touched", "notes"]:
                p[c] = union(p[c], r[c])
            for c in ["id", "authors", "year", "venue_or_status", "manipulation", "measurement", "domain_models"]:
                if not p[c] or (c == "id" and not arxiv_id(p[c]) and arxiv_id(r[c])):
                    p[c] = r[c] or p[c]
    rows = sorted(papers.values(), key=lambda p: (-RANK.get(p["relevance"], 0), p["title"].lower()))
    with (ROOT / "query_log.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, QCOLS)
        w.writeheader()
        w.writerows(queries)
    with (ROOT / "screening_log.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, SCOLS)
        w.writeheader()
        w.writerows(rows)

    def num(x):
        try:
            return int(str(x).replace(",", ""))
        except ValueError:
            return 0
    print(f"queries logged: {len(queries)}")
    print(f"records returned (sum over queries, with overlap): {sum(num(q['n_results']) for q in queries)}")
    print(f"records screened (sum over queries, with overlap): {sum(num(q['n_screened']) for q in queries)}")
    print(f"unique papers kept: {len(rows)}")
    for rel in ["close", "related", "background"]:
        print(f"  {rel}: {sum(p['relevance'] == rel for p in rows)}")
    print(f"  full text read: {sum(READ.get(p['full_text_read'], 0) == 2 for p in rows)}")


if __name__ == "__main__":
    main()
