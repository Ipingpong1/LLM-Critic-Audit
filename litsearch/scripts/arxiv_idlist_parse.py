#!/usr/bin/env python3
"""Convert an id_list Atom response into a ranked.jsonl-style file (metadata only).
Usage: python3 -I arxiv_idlist_parse.py <xml> <out_dir> <known_papers.csv>"""
import csv, json, os, re, sys
import xml.etree.ElementTree as ET
NS = {"a": "http://www.w3.org/2005/Atom", "ax": "http://arxiv.org/schemas/atom"}
xml, out_dir, known_csv = sys.argv[1:4]
known = {r["id"].strip() for r in csv.DictReader(open(known_csv, newline="", encoding="utf-8"))}
os.makedirs(out_dir, exist_ok=True)
sp = lambda s: re.sub(r"\s+", " ", s or "").strip()
with open(os.path.join(out_dir, "ranked.jsonl"), "w", encoding="utf-8") as fh:
    for e in ET.parse(xml).getroot().findall("a:entry", NS):
        m = re.search(r"abs/(.+?)(v\d+)?$", e.findtext("a:id", namespaces=NS))
        aid, ver = m.group(1), m.group(2) or ""
        rec = {"id": aid, "versions": [ver] if ver else [], "title": sp(e.findtext("a:title", namespaces=NS)),
               "abstract": sp(e.findtext("a:summary", namespaces=NS)),
               "authors": [sp(a.findtext("a:name", namespaces=NS)) for a in e.findall("a:author", NS)],
               "published": e.findtext("a:published", namespaces=NS) or "", "comment": sp(e.findtext("ax:comment", default="", namespaces=NS)),
               "journal_ref": sp(e.findtext("ax:journal_ref", default="", namespaces=NS)), "found_via": ["id_list recall check"],
               "tier": None, "known": aid in known}
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
print("ok")
