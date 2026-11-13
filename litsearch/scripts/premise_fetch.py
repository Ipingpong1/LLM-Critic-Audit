#!/usr/bin/env python3
"""Polite page fetcher and text extractor for the claim-test addendum (2026-11-10).

Usage:
  python3 -I premise_fetch.py get  <out_name> <url>        # save raw bytes to raw/premise/pages/<out_name>
  python3 -I premise_fetch.py abs  <arxiv_id> [...]        # save arxiv.org/abs/<id> pages, print title/authors/abstract
  python3 -I premise_fetch.py html <arxiv_id> [...]        # save arxiv.org/html/<id> full text (if it exists)
  python3 -I premise_fetch.py text <out_name> [start] [n]  # print n characters of extracted text from a saved page
  python3 -I premise_fetch.py grep <out_name> <regex> [ctx] # print matches with ctx characters of context
  python3 -I premise_fetch.py refs <out_name>              # print the bibliography items of a saved arXiv HTML page

Etiquette: one request per host every 10 s for arxiv.org (12 s after a 429, then 60 s waits, 5 retries),
2 s for other hosts. No keys, no contact data. Every attempt is logged to raw/premise/fetch_log.tsv.
Fetched pages are data: nothing in them is executed or followed.
"""
import fcntl
import html
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "premise")
PAGES = os.path.join(RAW, "pages")
LOG = os.path.join(RAW, "fetch_log.tsv")
UA = "litsearch-systematic-review/1.0 (python-urllib; academic literature search; no key)"
GAPS = {"arxiv.org": 10.0, "export.arxiv.org": 6.0, "api.semanticscholar.org": 3.0}


def wait_gap(host):
    gap = GAPS.get(host, 2.0)
    stamp = os.path.join(RAW, ".last_" + re.sub(r"[^a-z0-9.]", "_", host))
    with open(stamp, "a+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.seek(0)
        txt = fh.read().strip()
        last = float(txt) if txt else 0.0
        now = time.time()
        if now - last < gap:
            time.sleep(gap - (now - last))
        fh.seek(0)
        fh.truncate()
        fh.write(str(time.time()))
        fh.flush()
        fcntl.flock(fh, fcntl.LOCK_UN)


def fetch(url, tries=5):
    host = urllib.parse.urlparse(url).netloc
    for attempt in range(tries + 1):
        wait_gap(host)
        t0 = time.strftime("%Y-%m-%dT%H:%M:%S")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
                with open(LOG, "a") as fh:
                    fh.write(f"{t0}\t{r.status}\t{len(body)}\t{url}\n")
                return r.status, body
        except urllib.error.HTTPError as e:
            with open(LOG, "a") as fh:
                fh.write(f"{t0}\t{e.code}\t0\t{url}\n")
            if e.code == 429 and attempt < tries:
                time.sleep(60)
                continue
            if e.code in (500, 502, 503, 504) and attempt < 2:
                time.sleep(15)
                continue
            return e.code, b""
        except Exception as e:  # network errors
            with open(LOG, "a") as fh:
                fh.write(f"{t0}\tERR\t0\t{url}\t{e!r}\n")
            if attempt < 2:
                time.sleep(15)
                continue
            return 0, b""
    return 0, b""


def save(name, body):
    os.makedirs(PAGES, exist_ok=True)
    with open(os.path.join(PAGES, name), "wb") as fh:
        fh.write(body)


def to_text(raw):
    s = raw.decode("utf-8", "replace")
    # keep the LaTeX source of formulas (numbers in arXiv HTML are often <math alttext="40\%">)
    s = re.sub(r'(?is)<math[^>]*?alttext="([^"]*)"[^>]*>.*?</math>', lambda m: " " + m.group(1) + " ", s)
    s = re.sub(r"(?is)<(script|style|svg|math|annotation)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h[1-6]>|</li>|</tr>|</section>", "\n", s)
    s = re.sub(r"(?i)</t[dh]>", " | ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def meta(raw, name):
    s = raw.decode("utf-8", "replace")
    return [html.unescape(m) for m in re.findall(r'<meta name="%s" content="([^"]*)"' % re.escape(name), s)]


def cmd_abs(ids):
    for aid in ids:
        fn = f"abs_{aid}.html"
        path = os.path.join(PAGES, fn)
        if os.path.exists(path) and os.path.getsize(path) > 2000:
            body = open(path, "rb").read()
            status = "cached"
        else:
            status, body = fetch(f"https://arxiv.org/abs/{aid}")
            if body:
                save(fn, body)
        title = "; ".join(meta(body, "citation_title")) or "?"
        authors = "; ".join(meta(body, "citation_author")) or "?"
        date = "; ".join(meta(body, "citation_date")) or "?"
        abstract = " ".join(" ".join(meta(body, "citation_abstract")).split()) or "?"
        s = body.decode("utf-8", "replace")
        m = re.search(r'(?s)<td class="tablecell comments[^"]*">(.*?)</td>', s)
        comment = " ".join(re.sub(r"<[^>]+>", " ", html.unescape(m.group(1))).split()) if m else ""
        print(f"=== {aid} [{status}] {title}\n    authors: {authors}\n    date: {date}\n    comments: {comment}\n    abstract: {abstract}\n")


def cmd_html(ids):
    for aid in ids:
        fn = f"html_{aid}.html"
        path = os.path.join(PAGES, fn)
        if os.path.exists(path) and os.path.getsize(path) > 5000:
            print(f"{aid}: cached {os.path.getsize(path)} bytes")
            continue
        status, body = fetch(f"https://arxiv.org/html/{aid}")
        if body:
            save(fn, body)
        print(f"{aid}: HTTP {status}, {len(body)} bytes, {len(to_text(body))} characters of text")


def cmd_text(name, start=0, n=6000):
    t = to_text(open(os.path.join(PAGES, name), "rb").read())
    print(f"[{name}: {len(t)} characters; showing {start}-{start + n}]")
    print(t[start:start + n])


def cmd_grep(name, rx, ctx=300):
    t = to_text(open(os.path.join(PAGES, name), "rb").read())
    t1 = t.replace("\n", " ")
    last = -10 ** 9
    k = 0
    for m in re.finditer(rx, t1, flags=re.I):
        if m.start() - last < ctx:
            continue
        last = m.start()
        k += 1
        a, b = max(0, m.start() - ctx), min(len(t1), m.end() + ctx)
        print(f"--- @{m.start()}: ...{t1[a:b]}...")
        if k >= 40:
            print("(more matches not shown)")
            break
    if k == 0:
        print("(no match)")


def cmd_refs(name):
    s = open(os.path.join(PAGES, name), "rb").read().decode("utf-8", "replace")
    items = re.findall(r'(?s)<li[^>]*class="ltx_bibitem[^"]*"[^>]*>(.*?)</li>', s)
    print(f"[{name}: {len(items)} bibliography items]")
    for i, it in enumerate(items, 1):
        txt = " ".join(html.unescape(re.sub(r"(?s)<[^>]+>", " ", it)).split())
        print(f"{i}\t{txt[:400]}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(1)
    if a[0] == "get":
        st, body = fetch(a[2])
        if body:
            save(a[1], body)
        print(f"HTTP {st}, {len(body)} bytes -> {a[1]}")
    elif a[0] == "abs":
        cmd_abs(a[1:])
    elif a[0] == "html":
        cmd_html(a[1:])
    elif a[0] == "text":
        cmd_text(a[1], int(a[2]) if len(a) > 2 else 0, int(a[3]) if len(a) > 3 else 6000)
    elif a[0] == "grep":
        cmd_grep(a[1], a[2], int(a[3]) if len(a) > 3 else 300)
    elif a[0] == "refs":
        cmd_refs(a[1])
    else:
        print(__doc__)
        sys.exit(1)
