#!/usr/bin/env python3
"""Fetch arXiv metadata by id (one id_list call per 40 ids) for the claim-test addendum.

Usage: python3 -I premise_arxiv_ids.py <name> <max_abstract_chars> <id> [...]
Saves the Atom response to raw/premise/arxiv/idlist_<name>_<k>.xml and prints id, date, title, authors,
comment and abstract (cut at max_abstract_chars; 0 = whole abstract). Six seconds between calls.
"""
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "premise", "arxiv")
NS = {"a": "http://www.w3.org/2005/Atom", "ax": "http://arxiv.org/schemas/atom"}
UA = "litsearch-systematic-review/1.0 (python-urllib; 1 request per 3 s)"


def main(name, cut, ids):
    for k in range(0, len(ids), 40):
        chunk = ids[k:k + 40]
        fn = os.path.join(RAW, f"idlist_{name}_{k // 40}.xml")
        if not os.path.exists(fn):
            url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
                {"id_list": ",".join(chunk), "max_results": len(chunk)})
            time.sleep(6)
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
            with open(fn, "wb") as fh:
                fh.write(body)
        root = ET.parse(fn).getroot()
        for e in root.findall("a:entry", NS):
            aid = (e.findtext("a:id", default="", namespaces=NS)).rsplit("/abs/", 1)[-1]
            title = " ".join((e.findtext("a:title", default="", namespaces=NS)).split())
            abst = " ".join((e.findtext("a:summary", default="", namespaces=NS)).split())
            auth = [a.findtext("a:name", default="", namespaces=NS) for a in e.findall("a:author", NS)]
            com = " ".join((e.findtext("ax:comment", default="", namespaces=NS) or "").split())
            jr = " ".join((e.findtext("ax:journal_ref", default="", namespaces=NS) or "").split())
            pub = e.findtext("a:published", default="", namespaces=NS)[:10]
            a = abst if not cut or len(abst) <= cut else abst[:cut] + "…"
            print(f"=== {aid} ({pub}) {title}\n    {'; '.join(auth[:5])}{' et al.' if len(auth) > 5 else ''} | {com[:110]} {jr[:80]}\n    {a}\n")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3:])
