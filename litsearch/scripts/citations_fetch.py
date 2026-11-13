#!/usr/bin/env python3
"""Rate-limited fetcher for the `citations` stream.

Usage:
  python3 -I citations_fetch.py JOBS.tsv

JOBS.tsv lines (tab-separated, '#' comments allowed):
  source  url  out_relpath  [paginate:0/1]  [post_body_file]

source is one of s2, openalex, dblp, arxiv, web. Raw responses are written to
raw/citations/<out_relpath> (pages of a paginated S2 call are merged into one
JSON file with all `data` rows). Every attempt is appended to
raw/citations/fetch_log.tsv.

Etiquette (streams/README.md): S2 >= 2 s between requests (we use 3 s), on
HTTP 429 wait 60 s and retry at most 5 times; OpenAlex/DBLP <= 2 req/s (we use
1 s); arXiv >= 10 s apart (we use 12 s). No API keys, no mailto.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "citations")
LOG = os.path.join(RAW, "fetch_log.tsv")
MIN_GAP = {"s2": 3.0, "openalex": 1.0, "dblp": 1.0, "arxiv": 12.0, "web": 2.0}
UA = "litsearch-citations-stream/0.1 (academic literature search; no key)"
_last = {}


def log(*fields):
    with open(LOG, "a") as fh:
        fh.write("\t".join(str(f) for f in fields) + "\n")


def wait_gap(source):
    """Per-source spacing shared across processes via a locked stamp file."""
    import fcntl
    gap = MIN_GAP.get(source, 2.0)
    stamp = os.path.join(RAW, f".last_{source}")
    with open(stamp, "a+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.seek(0)
        txt = fh.read().strip()
        last = float(txt) if txt else _last.get(source, 0.0)
        now = time.time()
        if now - last < gap:
            time.sleep(gap - (now - last))
        fh.seek(0)
        fh.truncate()
        fh.write(str(time.time()))
        fh.flush()
        fcntl.flock(fh, fcntl.LOCK_UN)
    _last[source] = time.time()


def fetch(source, url, body=None):
    """Return (status, bytes). Retries 429 up to 5 times with 60 s waits;
    retries 5xx/timeouts up to 2 times with 15 s waits."""
    retries_429 = 0
    retries_other = 0
    while True:
        wait_gap(source)
        data = None
        headers = {"User-Agent": UA}
        if body is not None:
            data = body
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers)
        t0 = time.strftime("%Y-%m-%dT%H:%M:%S")
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                content = resp.read()
                log(t0, source, resp.status, len(content), url)
                return resp.status, content
        except urllib.error.HTTPError as e:
            content = e.read() if hasattr(e, "read") else b""
            log(t0, source, e.code, len(content), url)
            if e.code == 429 and retries_429 < 5:
                retries_429 += 1
                time.sleep(60)
                continue
            if e.code >= 500 and retries_other < 2:
                retries_other += 1
                time.sleep(15)
                continue
            return e.code, content
        except Exception as e:  # timeouts, connection errors
            log(t0, source, "ERR:" + type(e).__name__, 0, url)
            if retries_other < 2:
                retries_other += 1
                time.sleep(15)
                continue
            return -1, str(e).encode()


def run_job(source, url, out_rel, paginate=False, body_file=None):
    out = os.path.join(RAW, out_rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    body = None
    if body_file:
        with open(os.path.join(RAW, body_file), "rb") as fh:
            body = fh.read()
    if not paginate:
        status, content = fetch(source, url, body)
        if status == 200:
            with open(out, "wb") as fh:
                fh.write(content)
        else:
            with open(out + ".err", "wb") as fh:
                fh.write(str(status).encode() + b"\n" + content[:5000])
        return status
    # S2-style pagination: {"offset":..,"next":..,"data":[..]}
    rows = []
    offset = 0
    pages = 0
    status = None
    while True:
        sep = "&" if "?" in url else "?"
        page_url = f"{url}{sep}offset={offset}"
        status, content = fetch(source, page_url, body)
        if status != 200:
            with open(out + ".err", "wb") as fh:
                fh.write(f"{status} at offset {offset}\n".encode() + content[:5000])
            break
        js = json.loads(content)
        pages += 1
        rows.extend(js.get("data") or [])
        nxt = js.get("next")
        if nxt is None or nxt <= offset:
            break
        offset = nxt
    merged = {"source_url": url, "pages": pages, "n": len(rows),
              "complete": status == 200, "data": rows}
    # only a complete result counts as done; partial pages go to .partial
    with open(out if status == 200 else out + ".partial", "w") as fh:
        json.dump(merged, fh)
    return status


def main():
    jobs = sys.argv[1]
    with open(jobs) as fh:
        lines = [l.rstrip("\n") for l in fh if l.strip() and not l.startswith("#")]
    for line in lines:
        parts = line.split("\t")
        source, url, out_rel = parts[0], parts[1], parts[2]
        paginate = len(parts) > 3 and parts[3] == "1"
        body_file = parts[4] if len(parts) > 4 and parts[4] else None
        out = os.path.join(RAW, out_rel)
        if os.path.exists(out):
            print("skip (exists)", out_rel, flush=True)
            continue
        st = run_job(source, url, out_rel, paginate, body_file)
        print(st, out_rel, flush=True)


if __name__ == "__main__":
    main()
