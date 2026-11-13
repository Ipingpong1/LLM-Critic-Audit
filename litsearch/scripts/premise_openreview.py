#!/usr/bin/env python3
"""OpenReview API v2 search for the claim-test addendum (2026-11-10).

Usage:
  python3 -I premise_openreview.py run  "<phrase>" ["<phrase>" ...]   # one exact phrase per query
  python3 -I premise_openreview.py rank [--since-year 2023]           # literal re-match over everything fetched
  python3 -I premise_openreview.py show <forum_id> [...]              # print title, venue and abstract

/notes/search takes one phrase per query (AND and several quoted phrases are not supported; see
streams/peer_notes.md), so each phrase is paged in full (limit 1000, at most 3 pages) and the claim
terms are matched locally with the same regexes as premise_arxiv_screen.py. Raw pages go to
raw/premise/openreview/ as gzip JSON; one line per query to raw/premise/openreview/queries.tsv.
At most 2 requests per second; no login.
"""
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import premise_arxiv_screen as S  # noqa: E402  (tags_score)

RAW = os.path.join(os.path.dirname(HERE), "raw", "premise", "openreview")
BASE = "https://api2.openreview.net/notes/search"
UA = "litsearch-systematic-review/1.0 (python-urllib; academic literature search; no key)"


def val(c, k):
    v = c.get(k)
    if isinstance(v, dict):
        v = v.get("value")
    if isinstance(v, list):
        v = "; ".join(str(x) for x in v)
    return "" if v is None else str(v)


def get(url):
    for attempt in range(4):
        time.sleep(0.7)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(30)
                continue
            return e.code, b""
        except Exception:
            time.sleep(10)
    return 0, b""


def run(phrases):
    os.makedirs(RAW, exist_ok=True)
    for ph in phrases:
        slug = re.sub(r"[^a-z0-9]+", "_", ph.lower()).strip("_")
        total, got = None, 0
        for page in range(3):
            fn = os.path.join(RAW, f"{slug}__o{page * 1000:05d}.json.gz")
            if os.path.exists(fn):
                d = json.loads(gzip.open(fn).read())
            else:
                q = urllib.parse.urlencode({"term": f'"{ph}"', "content": "all", "source": "forum",
                                            "limit": 1000, "offset": page * 1000})
                st, body = get(BASE + "?" + q)
                if st != 200:
                    print(f"{ph}: HTTP {st} at offset {page * 1000}")
                    break
                with gzip.open(fn, "wb") as fh:
                    fh.write(body)
                d = json.loads(body)
            notes = d.get("notes", [])
            total = d.get("count", total)
            got += len(notes)
            if len(notes) < 1000:
                break
        with open(os.path.join(RAW, "queries.tsv"), "a") as fh:
            fh.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')}\t{ph}\t{total}\t{got}\n")
        print(f"{ph}: count={total} fetched={got}", flush=True)


def load():
    recs = {}
    for fn in sorted(os.listdir(RAW)):
        if not fn.endswith(".json.gz"):
            continue
        phrase = fn.split("__")[0]
        for n in json.loads(gzip.open(os.path.join(RAW, fn)).read()).get("notes", []):
            c = n.get("content", {})
            fid = n.get("forum") or n.get("id")
            r = recs.setdefault(fid, {"id": fid, "title": val(c, "title"), "abstract": val(c, "abstract"),
                                      "venue": val(c, "venue"), "venueid": val(c, "venueid"),
                                      "authors": val(c, "authors"), "tldr": val(c, "TLDR") or val(c, "TL;DR"),
                                      "keywords": val(c, "keywords"), "cdate": n.get("cdate") or n.get("tcdate"),
                                      "via": []})
            if phrase not in r["via"]:
                r["via"].append(phrase)
    return recs


def year(r):
    m = re.search(r"\b(20[12]\d)\b", r["venue"] + " " + r["venueid"])
    if m:
        return int(m.group(1))
    if r["cdate"]:
        return time.gmtime(r["cdate"] / 1000).tm_year
    return 0


def rank(since_year=2023):
    recs = load()
    rows = []
    for r in recs.values():
        if year(r) < since_year:
            continue
        t, s = S.tags_score(" \n ".join([r["title"], r["abstract"], r["tldr"], r["keywords"]]))
        if "L" not in t:
            continue
        rows.append((s, "".join(sorted(t - {"L"})), year(r), r["id"], r["venue"][:40], r["title"]))
    rows.sort(key=lambda x: (-x[0], x[3]))
    with open(os.path.join(RAW, "ranked.tsv"), "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write("\t".join(str(x) for x in row) + "\n")
    print(f"unique forums={len(recs)} with an LLM term and year>={since_year}: {len(rows)}")


def show(ids):
    recs = load()
    for i in ids:
        r = recs.get(i)
        if not r:
            print(f"=== {i}: not in the fetched pages")
            continue
        print(f"=== {i} | {r['venue']} | {r['title']}\n    authors: {r['authors'][:200]}\n    {r['abstract']}\n")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "run":
        run(a[1:])
    elif a[0] == "rank":
        rank(int(a[a.index("--since-year") + 1]) if "--since-year" in a else 2023)
    elif a[0] == "show":
        show(a[1:])
