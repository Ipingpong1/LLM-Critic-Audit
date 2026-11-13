#!/usr/bin/env python3
"""Count results in raw files of the citations stream (python3 -I).
Prints one line per raw result file: path, n_results, completeness/notes."""
import glob
import json
import os
import re
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "citations")


def main():
    for f in sorted(glob.glob(os.path.join(RAW, "**", "*"), recursive=True)):
        if os.path.isdir(f) or "/req/" in f or "/derived/" in f:
            continue
        rel = os.path.relpath(f, RAW)
        if rel.endswith(".json"):
            try:
                js = json.load(open(f))
            except Exception as e:
                print(rel, "BADJSON", e)
                continue
            if isinstance(js, dict) and "data" in js and "pages" in js:
                n = js["n"]
                print(f"{rel}\t{n}\tcomplete={js['complete']}")
            elif isinstance(js, dict) and "meta" in js:
                print(f"{rel}\t{js['meta'].get('count')}\treturned={len(js.get('results', []))}")
            elif isinstance(js, list):
                print(f"{rel}\t{len(js)}\tbatch")
            else:
                print(f"{rel}\t1\trecord")
        elif rel.endswith(".xml"):
            try:
                root = ET.parse(f).getroot()
                ns = {"a": "http://www.w3.org/2005/Atom", "os": "http://a9.com/-/spec/opensearch/1.1/"}
                tot = root.find("os:totalResults", ns)
                n = len(root.findall("a:entry", ns))
                print(f"{rel}\t{tot.text if tot is not None else '?'}\treturned={n}")
            except Exception as e:
                print(rel, "BADXML", e)
        elif rel.endswith(".err") or rel.endswith(".partial"):
            head = open(f, "rb").read(60).decode("utf-8", "replace").split("\n")[0]
            print(f"{rel}\tERR\t{head}")
        elif rel.endswith(".html"):
            print(f"{rel}\t-\thtml {os.path.getsize(f)} bytes")


if __name__ == "__main__":
    main()
