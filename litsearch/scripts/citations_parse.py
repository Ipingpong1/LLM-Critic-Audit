#!/usr/bin/env python3
"""Parsers for raw files of the `citations` stream (run with python3 -I).

  citations_parse.py bib  FILE.html      -> one line per bibliography item (LaTeXML arXiv HTML)
  citations_parse.py text FILE.html [start_regex] [n_chars]  -> visible text (optionally from a heading)
  citations_parse.py atom FILE.xml       -> arXiv Atom feed as TSV (id, published, updated, title, authors, comment, journal_ref, categories)
"""
import html
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


class TextGrab(HTMLParser):
    """Collect visible text; mark bibliography items."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0
        self.bib = []
        self.in_bib = 0
        self.cur = []
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "math"):
            # keep alt text for math
            if tag == "math" and a.get("alttext"):
                self.parts.append(" " + a["alttext"] + " ")
                if self.in_bib:
                    self.cur.append(" " + a["alttext"] + " ")
            self.skip += 1
            return
        cls = a.get("class", "") or ""
        if tag == "li" and "ltx_bibitem" in cls:
            self.in_bib = 1
            self.depth = 0
            self.cur = []
        elif self.in_bib and tag == "li":
            self.depth += 1
        if tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "br", "section"):
            self.parts.append("\n")
        if tag in ("td", "th"):
            self.parts.append(" | ")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "math"):
            self.skip = max(0, self.skip - 1)
            return
        if self.in_bib and tag == "li":
            if self.depth == 0:
                self.bib.append(re.sub(r"\s+", " ", "".join(self.cur)).strip())
                self.in_bib = 0
            else:
                self.depth -= 1

    def handle_data(self, data):
        if self.skip:
            return
        self.parts.append(data)
        if self.in_bib:
            self.cur.append(data)


def load(path):
    with open(path, "rb") as fh:
        raw = fh.read().decode("utf-8", "replace")
    p = TextGrab()
    p.feed(raw)
    return p


def main():
    mode, path = sys.argv[1], sys.argv[2]
    if mode == "bib":
        p = load(path)
        for i, b in enumerate(p.bib, 1):
            print(f"[{i}] {b}")
    elif mode == "text":
        p = load(path)
        txt = "".join(p.parts)
        txt = re.sub(r"[ \t]+", " ", txt)
        txt = re.sub(r"\n\s*\n+", "\n\n", txt)
        if len(sys.argv) > 3 and sys.argv[3]:
            m = re.search(sys.argv[3], txt)
            if m:
                txt = txt[m.start():]
        n = int(sys.argv[4]) if len(sys.argv) > 4 else len(txt)
        print(txt[:n])
    elif mode == "atom":
        ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
        root = ET.parse(path).getroot()
        for e in root.findall("a:entry", ns):
            def g(tag):
                el = e.find(tag, ns)
                return re.sub(r"\s+", " ", el.text).strip() if el is not None and el.text else ""
            authors = "; ".join(re.sub(r"\s+", " ", a.find("a:name", ns).text).strip() for a in e.findall("a:author", ns))
            cats = ",".join(c.get("term") for c in e.findall("a:category", ns))
            print("\t".join([g("a:id").replace("http://arxiv.org/abs/", ""), g("a:published")[:10], g("a:updated")[:10],
                             g("a:title"), authors, g("arxiv:comment"), g("arxiv:journal_ref"), cats]))
    elif mode == "atom_abs":
        ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
        root = ET.parse(path).getroot()
        for e in root.findall("a:entry", ns):
            def g(tag):
                el = e.find(tag, ns)
                return re.sub(r"\s+", " ", el.text).strip() if el is not None and el.text else ""
            print(g("a:id").replace("http://arxiv.org/abs/", ""), "|", g("a:title"))
            print("   ", g("a:summary"))
            print()


if __name__ == "__main__":
    main()
