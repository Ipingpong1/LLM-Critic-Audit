#!/usr/bin/env python3
"""Fetch arXiv HTML full texts and convert them to plain text (standard library only).

Usage:
  python3 -I arxiv_fulltext.py fetch <out_dir> <id> [<id> ...]   # saves <out_dir>/<id>.html and <id>.txt
  python3 -I arxiv_fulltext.py text  <html_file> <txt_file>        # re-convert a saved page
  python3 -I arxiv_fulltext.py grep  <txt_file> <regex> [context_lines]

Fetches https://arxiv.org/html/<id> (latest version) with at least 10 s between requests and a
generic User-Agent. Pages are data: nothing in them is executed. The text conversion keeps headings
(prefixed with '#'), paragraphs, list items, table cells and figure captions, and drops scripts,
styles and MathML annotations. Hidden-text tricks (display:none, white-on-white) are flagged when
an element's inline style hides it: such text is kept but prefixed with [HIDDEN] so it can be noted.
"""
import html.parser
import os
import re
import sys
import time
import urllib.error
import urllib.request

UA = "litsearch-systematic-review/1.0 (python-urllib; full-text reading)"
GAP = 10.0
_last = [0.0]

BLOCK = {"p", "div", "section", "li", "tr", "figcaption", "caption", "h1", "h2", "h3", "h4", "h5", "h6",
         "table", "blockquote", "br", "dt", "dd", "article", "header", "footer"}
SKIP = {"script", "style", "annotation", "annotation-xml", "noscript", "svg", "head", "button", "nav"}
HIDE_RE = re.compile(r"display\s*:\s*none|visibility\s*:\s*hidden|font-size\s*:\s*0|color\s*:\s*(#fff\b|#ffffff|white)", re.I)


class Text(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.hidden, self.stack = [], 0, 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        hid = bool(HIDE_RE.search(a.get("style", "") or "")) or ("hidden" in a and tag not in ("input",))
        self.stack.append((tag, hid))
        if tag in SKIP:
            self.skip += 1
        if hid:
            self.hidden += 1
        if tag in BLOCK:
            self.out.append("\n")
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.out.append("# ")
        if tag in ("td", "th"):
            self.out.append(" | ")
        if tag == "math":
            alt = a.get("alttext")
            if alt:
                self.out.append(" " + alt + " ")
                self.skip += 1
                self.stack[-1] = (tag, hid, "mathskip")

    def handle_endtag(self, tag):
        while self.stack:
            item = self.stack.pop()
            t, hid = item[0], item[1]
            if t in SKIP:
                self.skip -= 1
            if len(item) > 2:
                self.skip -= 1
            if hid:
                self.hidden -= 1
            if t == tag:
                break
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip > 0:
            return
        if self.hidden > 0 and data.strip():
            self.out.append(" [HIDDEN] ")
        self.out.append(data)


def to_text(raw):
    p = Text()
    p.feed(raw)
    s = "".join(p.out)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip() + "\n"


def fetch(out_dir, aid):
    os.makedirs(out_dir, exist_ok=True)
    dt = time.time() - _last[0]
    if dt < GAP:
        time.sleep(GAP - dt)
    _last[0] = time.time()
    url = f"https://arxiv.org/html/{aid}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
            final = r.geturl()
    except urllib.error.HTTPError as e:
        print(f"{aid}: HTTP {e.code} for {url}")
        return False
    except Exception as e:  # network errors
        print(f"{aid}: error {e!r}")
        return False
    html_path = os.path.join(out_dir, f"{aid}.html")
    with open(html_path, "wb") as fh:
        fh.write(raw)
    txt = to_text(raw.decode("utf-8", errors="replace"))
    with open(os.path.join(out_dir, f"{aid}.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"SOURCE: {final}\n\n" + txt)
    n_hidden = txt.count("[HIDDEN]")
    print(f"{aid}: ok {len(raw)} bytes -> {len(txt.split())} words; final={final}; hidden_spans={n_hidden}")
    return True


def grep(txt_file, pattern, ctx=2):
    lines = open(txt_file, encoding="utf-8").read().split("\n")
    rx = re.compile(pattern, re.I)
    shown = set()
    for i, l in enumerate(lines):
        if rx.search(l):
            for j in range(max(0, i - ctx), min(len(lines), i + ctx + 1)):
                if j not in shown:
                    print(f"{j}: {lines[j][:600]}")
                    shown.add(j)
            print("--")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        for aid in sys.argv[3:]:
            fetch(sys.argv[2], aid)
    elif cmd == "text":
        raw = open(sys.argv[2], encoding="utf-8", errors="replace").read()
        open(sys.argv[3], "w", encoding="utf-8").write(to_text(raw))
    elif cmd == "grep":
        grep(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 2)
    else:
        print(__doc__)
