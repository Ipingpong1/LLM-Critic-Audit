"""OpenReview API v2 /notes/search runner for the `peer` stream.

Usage: python3 -I peer_openreview.py TASKS.json
TASKS.json: list of {"term": ..., "group": ..., "max_pages": N, "tag": ...}

Each task pages /notes/search (content=all, source=forum, limit=1000) up to max_pages,
saves raw pages (gzip) under raw/peer/openreview/, appends notes to the scratch corpus,
and logs one query-log row.  The /notes listing endpoint is behind a challenge page,
so search is the only route used.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import peer_lib as L  # noqa: E402

BASE = "https://api2.openreview.net/notes/search"
CORPUS = os.path.join(L.SCRATCH, "or_corpus.jsonl")
DONE = os.path.join(L.SCRATCH, "or_done.txt")


def val(c, k):
    v = c.get(k)
    if isinstance(v, dict):
        v = v.get("value")
    if isinstance(v, list):
        v = "; ".join(str(x) for x in v)
    return "" if v is None else str(v)


def year_of(rec):
    m = re.search(r"\b(20[0-2]\d)\b", rec.get("venue") or "")
    if m:
        return int(m.group(1))
    for k in ("pdate", "odate", "cdate"):
        t = rec.get(k)
        if t:
            import datetime
            return datetime.datetime.utcfromtimestamp(t / 1000).year
    return None


def to_rec(n):
    c = n.get("content", {})
    authors = c.get("authors")
    if isinstance(authors, dict):
        authors = authors.get("value")
    if isinstance(authors, list):
        authors = "; ".join(a.get("fullname", "") if isinstance(a, dict) else str(a) for a in authors)
    rec = {
        "id": n.get("id"),
        "forum": n.get("forum"),
        "number": n.get("number"),
        "domain": n.get("domain"),
        "title": val(c, "title"),
        "abstract": val(c, "abstract"),
        "keywords": val(c, "keywords"),
        "tldr": val(c, "TLDR") or val(c, "TL;DR"),
        "venue": val(c, "venue"),
        "venueid": val(c, "venueid"),
        "authors": authors or "",
        "pdf": val(c, "pdf"),
        "html": val(c, "html"),
        "bibtex": val(c, "_bibtex")[:600],
        "primary_area": val(c, "primary_area"),
        "cdate": n.get("cdate"),
        "pdate": n.get("pdate"),
        "odate": n.get("odate"),
    }
    rec["year"] = year_of(rec)
    return rec


def run_task(t):
    term, group = t["term"], t["group"]
    max_pages = t.get("max_pages", 3)
    tag = t.get("tag", "")
    key = f"{term}||{group}"
    got, count, pages = [], None, 0
    offset = 0
    while True:
        params = {"term": term, "content": "all", "group": group, "source": "forum",
                  "limit": 1000, "offset": offset}
        name = f"{L.slug(group,40)}__{L.slug(term,40)}__o{offset}"
        d = L.get_json(BASE, params, source="openreview", raw_name=name)
        notes = d.get("notes", [])
        count = d.get("count")
        pages += 1
        got.extend(notes)
        offset += 1000
        if not notes or offset >= (count or 0) or pages >= max_pages:
            break
    recs = [to_rec(n) for n in got]
    hits = 0
    with open(CORPUS, "a") as f:
        for r in recs:
            r["found_via"] = key
            cl = L.classify(" ".join([r["title"], r["abstract"], r["keywords"], r["tldr"]]))
            r["cl"] = cl
            if cl["hit"] and (r["year"] or 0) >= 2022:
                hits += 1
            f.write(json.dumps(r) + "\n")
    capped = " (API count capped at 10000)" if count == 10000 else ""
    note = (f"retrieved {len(recs)} of {count}{capped} in {pages} page(s); "
            f"{hits} pass local A&LLM&(B|C) filter with year>=2022")
    if tag:
        note = tag + "; " + note
    L.log_query("OpenReview API v2 (/notes/search)", term,
                f"group={group}; content=all; source=forum; limit=1000; max_pages={max_pages}",
                count, notes=note)
    with open(DONE, "a") as f:
        f.write(key + "\n")
    print(f"{term!r:40} {group:45} count={count} got={len(recs)} hits={hits}", flush=True)


def main():
    tasks = json.load(open(sys.argv[1]))
    done = set()
    if os.path.exists(DONE):
        done = set(x.strip() for x in open(DONE))
    for t in tasks:
        if f"{t['term']}||{t['group']}" in done:
            continue
        try:
            run_task(t)
        except Exception as e:  # keep going; record the failure
            print("FAILED", t, e, flush=True)
            L.log_query("OpenReview API v2 (/notes/search)", t["term"], f"group={t['group']}",
                        "", notes=f"FAILED: {str(e)[:200]}")


if __name__ == "__main__":
    main()
