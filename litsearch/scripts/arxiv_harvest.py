#!/usr/bin/env python3
"""arXiv API harvester for the litsearch `arxiv` stream (standard library only).

Usage:
  python3 -I arxiv_harvest.py run   <queries.jsonl> <raw_dir> [--page 1000] [--only qid1,qid2]
  python3 -I arxiv_harvest.py count <raw_dir> "<search_query>" ["<search_query>" ...]

queries.jsonl: one JSON object per line, {"qid": "...", "query": "<search_query>", ...}.

`run` pages through every query (sortBy=submittedDate, descending; `--page` results per call,
at most 1000), saves each raw Atom page to <raw_dir>/<qid>__s<start>.xml and appends one record
per page to <raw_dir>/manifest.jsonl. It is resumable: pages already saved are skipped.
`count` only asks for totalResults (max_results=1; max_results=0 returns HTTP 500) and logs the probe to <raw_dir>/probes.jsonl.

Etiquette: at least ARXIV_MIN_GAP (default 4 s) between request starts; on HTTP 429/5xx or network
errors it waits (Retry-After if given, else 15 s, or 60 s after a 429, doubling to 600 s) and retries
up to 8 times. No contact or
personal data is sent; the User-Agent is generic.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API = "https://export.arxiv.org/api/query"
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "os": "http://a9.com/-/spec/opensearch/1.1/",
    "ax": "http://arxiv.org/schemas/atom",
}
UA = "litsearch-systematic-review/1.0 (python-urllib; 1 request per 3 s)"
MIN_GAP = float(os.environ.get("ARXIV_MIN_GAP", "4.0"))  # seconds between request starts (>= 3)
_last = [0.0]


def _wait_gap():
    dt = time.time() - _last[0]
    if dt < MIN_GAP:
        time.sleep(MIN_GAP - dt)
    _last[0] = time.time()


def fetch(params, tries=8):
    url = API + "?" + urllib.parse.urlencode(params)
    delay = 15
    last_err = None
    for attempt in range(tries):
        _wait_gap()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                return url, r.status, r.read()
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504):
                ra = e.headers.get("Retry-After") if e.headers else None
                if e.code == 429:
                    delay = max(delay, 60)  # rate limited: back off for at least a minute
                w = int(ra) if (ra and ra.isdigit() and int(ra) > 0) else delay
                print(f"    HTTP {e.code}; waiting {w}s (attempt {attempt + 1})", file=sys.stderr, flush=True)
                time.sleep(w)
                delay = min(delay * 2, 600)
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            last_err = e
            print(f"    network error {e!r}; waiting {delay}s (attempt {attempt + 1})", file=sys.stderr, flush=True)
            time.sleep(delay)
            delay = min(delay * 2, 600)
    raise RuntimeError(f"giving up after {tries} tries: {url} ({last_err!r})")


def parse_page(body):
    root = ET.fromstring(body)
    tot = root.find("os:totalResults", NS)
    total = int(tot.text) if tot is not None and tot.text else -1
    entries = root.findall("a:entry", NS)
    err = None
    for e in entries:
        eid = (e.findtext("a:id", default="", namespaces=NS) or "")
        if "api/errors" in eid:
            err = (e.findtext("a:summary", default="", namespaces=NS) or "").strip()
    n = 0 if err else len(entries)
    return total, n, err


def safe_qid(qid):
    return "".join(ch if (ch.isalnum() or ch in "-_.") else "_" for ch in qid)


def run(qfile, raw_dir, page=1000, only=None):
    os.makedirs(raw_dir, exist_ok=True)
    manifest = os.path.join(raw_dir, "manifest.jsonl")
    queries = [json.loads(l) for l in open(qfile, encoding="utf-8") if l.strip()]
    if only:
        queries = [q for q in queries if q["qid"] in only]
    for q in queries:
        qid, sq = q["qid"], q["query"]
        start, total, got = 0, None, 0
        while True:
            fn = os.path.join(raw_dir, f"{safe_qid(qid)}__s{start:05d}.xml")
            if os.path.exists(fn):
                with open(fn, "rb") as fh:
                    total, n, err = parse_page(fh.read())
            else:
                n, err, empty_retries = 0, None, 0
                while True:
                    params = {"search_query": sq, "start": start, "max_results": page,
                              "sortBy": "submittedDate", "sortOrder": "descending"}
                    url, status, body = fetch(params)
                    total, n, err = parse_page(body)
                    # arXiv occasionally returns an empty page inside the result range: retry it
                    if n == 0 and not err and total > start and empty_retries < 3:
                        empty_retries += 1
                        print(f"    empty page at start={start} of {total}; retry {empty_retries}", file=sys.stderr, flush=True)
                        time.sleep(10)
                        continue
                    break
                with open(fn, "wb") as fh:
                    fh.write(body)
                rec = {"qid": qid, "query": sq, "start": start, "max_results": page, "total": total,
                       "n_entries": n, "error": err, "http": status, "url": url, "file": os.path.basename(fn),
                       "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                with open(manifest, "a", encoding="utf-8") as mf:
                    mf.write(json.dumps(rec) + "\n")
            got += n
            print(f"{qid}: start={start} total={total} page_entries={n} cum={got}" + (f" ERROR={err}" if err else ""), flush=True)
            if err or n == 0:
                break
            start += page
            if start >= total:
                break


def count(raw_dir, queries, qids=None, tag="probe"):
    os.makedirs(raw_dir, exist_ok=True)
    out = os.path.join(raw_dir, "probes.jsonl")
    for i, sq in enumerate(queries):
        url, status, body = fetch({"search_query": sq, "start": 0, "max_results": 1})
        total, n, err = parse_page(body)
        rec = {"qid": qids[i] if qids else None, "tag": tag, "query": sq, "total": total, "error": err,
               "url": url, "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
        label = qids[i] if qids else sq
        print(f"{total}\t{label}" + (f"\tERROR={err}" if err else ""), flush=True)


def probe(qfile, raw_dir):
    qs = [json.loads(l) for l in open(qfile, encoding="utf-8") if l.strip()]
    count(raw_dir, [q["query"] for q in qs], qids=[q["qid"] for q in qs], tag="plan-probe")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "run":
        args = sys.argv[2:]
        page, only = 1000, None
        if "--page" in args:
            i = args.index("--page"); page = min(int(args[i + 1]), 1000); del args[i:i + 2]
        if "--only" in args:
            i = args.index("--only"); only = set(args[i + 1].split(",")); del args[i:i + 2]
        run(args[0], args[1], page=page, only=only)
    elif cmd == "count":
        count(sys.argv[2], sys.argv[3:], tag="stemming-probe")
    elif cmd == "probe":
        probe(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        sys.exit(1)
