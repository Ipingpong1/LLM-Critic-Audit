#!/usr/bin/env python3
"""Parse saved arXiv Atom pages and deduplicate by arXiv id (versions ignored).

Usage: python3 -I arxiv_parse.py <raw_dir> <out_dir> [qid_prefix_filter ...]

Reads <raw_dir>/manifest.jsonl (written by arxiv_harvest.py), parses every page it lists and writes
  <out_dir>/candidates.jsonl : one record per unique arXiv id with title, abstract, authors, dates,
                               categories, comment, journal_ref and found_via (list of qids)
  <out_dir>/query_hits.json  : {qid: [ids...]} and {qid: total} for the query log
Optional prefix filters restrict which qids are parsed (e.g. R for the recency sweep).
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom", "os": "http://a9.com/-/spec/opensearch/1.1/",
      "ax": "http://arxiv.org/schemas/atom"}


def norm_space(s):
    return re.sub(r"\s+", " ", s or "").strip()


def base_id(url):
    # http://arxiv.org/abs/2608.16003v2 -> 2608.16003 ; old-style ids keep their archive prefix
    m = re.search(r"arxiv\.org/abs/(.+?)(v\d+)?$", url.strip())
    if not m:
        return None, None
    return m.group(1), (m.group(2) or "")


def main(raw_dir, out_dir, prefixes):
    os.makedirs(out_dir, exist_ok=True)
    recs = [json.loads(l) for l in open(os.path.join(raw_dir, "manifest.jsonl"), encoding="utf-8") if l.strip()]
    if prefixes:
        recs = [r for r in recs if any(r["qid"].startswith(p) for p in prefixes)]
    cands, hits, totals = {}, {}, {}
    seen_files = set()
    for r in recs:
        fn = os.path.join(raw_dir, r["file"])
        if fn in seen_files or not os.path.exists(fn):
            continue
        seen_files.add(fn)
        root = ET.parse(fn).getroot()
        tot = root.find("os:totalResults", NS)
        totals[r["qid"]] = int(tot.text) if tot is not None and tot.text else r.get("total")
        hits.setdefault(r["qid"], [])
        for e in root.findall("a:entry", NS):
            aid, ver = base_id(e.findtext("a:id", default="", namespaces=NS))
            if not aid or "api/errors" in aid:
                continue
            hits[r["qid"]].append(aid)
            if aid in cands:
                c = cands[aid]
                if r["qid"] not in c["found_via"]:
                    c["found_via"].append(r["qid"])
                if ver and ver not in c["versions"]:
                    c["versions"].append(ver)
                continue
            pc = e.find("ax:primary_category", NS)
            cands[aid] = {
                "id": aid,
                "versions": [ver] if ver else [],
                "title": norm_space(e.findtext("a:title", default="", namespaces=NS)),
                "abstract": norm_space(e.findtext("a:summary", default="", namespaces=NS)),
                "authors": [norm_space(a.findtext("a:name", default="", namespaces=NS)) for a in e.findall("a:author", NS)],
                "published": e.findtext("a:published", default="", namespaces=NS),
                "updated": e.findtext("a:updated", default="", namespaces=NS),
                "primary_category": pc.get("term") if pc is not None else "",
                "categories": [c.get("term") for c in e.findall("a:category", NS)],
                "comment": norm_space(e.findtext("ax:comment", default="", namespaces=NS)),
                "journal_ref": norm_space(e.findtext("ax:journal_ref", default="", namespaces=NS)),
                "found_via": [r["qid"]],
            }
    with open(os.path.join(out_dir, "candidates.jsonl"), "w", encoding="utf-8") as fh:
        for c in sorted(cands.values(), key=lambda x: x["id"], reverse=True):
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(os.path.join(out_dir, "query_hits.json"), "w", encoding="utf-8") as fh:
        json.dump({"totals": totals, "hits": {k: sorted(set(v)) for k, v in hits.items()}}, fh)
    n_hits = sum(len(set(v)) for v in hits.values())
    print(f"pages={len(seen_files)} queries={len(hits)} hit-records={n_hits} unique ids={len(cands)}")
    for q in sorted(hits):
        got = len(set(hits[q]))
        flag = "" if got >= (totals.get(q) or 0) else f"  (retrieved {got} < total {totals.get(q)})"
        print(f"  {q}: total={totals.get(q)} unique_retrieved={got}{flag}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
