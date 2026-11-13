#!/usr/bin/env python3
"""Fetch specific arXiv records by id_list (recall check for known papers).

Usage: python3 -I arxiv_idlist.py <raw_dir> <out_name> <id> [<id> ...]
Saves the raw Atom XML to <raw_dir>/<out_name>.xml and logs the call in <raw_dir>/idlist_calls.jsonl.
Uses the same polite fetch (rate limit, retries) as arxiv_harvest.py.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arxiv_harvest as h  # noqa: E402

raw_dir, name, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
url, status, body = h.fetch({"id_list": ",".join(ids), "max_results": len(ids)})
total, n, err = h.parse_page(body)
with open(os.path.join(raw_dir, name + ".xml"), "wb") as fh:
    fh.write(body)
with open(os.path.join(raw_dir, "idlist_calls.jsonl"), "a", encoding="utf-8") as fh:
    fh.write(json.dumps({"name": name, "ids": ids, "url": url, "total": total, "n_entries": n, "error": err,
                         "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n")
print(f"{name}: total={total} entries={n} err={err}")
