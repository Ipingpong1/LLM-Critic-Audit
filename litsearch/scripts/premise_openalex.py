#!/usr/bin/env python3
"""OpenAlex title+abstract search for the claim-test addendum (no key, no mailto; one request per second).

Usage: python3 -I premise_openalex.py
Runs the queries below (title_and_abstract.search, per_page=50, first page only because the keyless daily
budget is small), saves raw JSON to raw/premise/openalex/ and prints one line per hit not seen before.
"""
import json
import os
import re
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "premise", "openalex")
UA = "litsearch-systematic-review/1.0 (python-urllib; academic literature search; no key)"
Q = [
    ("sycophancy judge verifier", "2026-10-01"),
    ("sycophancy language model", "2026-10-01"),
    ("false premise language model", "2026-10-01"),
    ("LLM judge anchoring prior verdict", "2026-10-01"),
    ("language model error detection false positive prompt", "2026-10-01"),
    ("code review language model bias framing", "2026-10-01"),
    ("language model base rate Bayesian", "2026-10-01"),
    ("signal detection language model criterion", "2026-10-01"),
    ("signal detection sycophancy", "2023-01-01"),
    ("presupposition error detection language model verifier", "2023-01-01"),
    ("LLM critic told solution contains error false alarm", "2023-01-01"),
    ("confirmation bias LLM judge pre-screening note", "2023-01-01"),
]


def inv(ix):
    if not ix:
        return ""
    pos = {}
    for w, ps in ix.items():
        for p in ps:
            pos[p] = w
    return " ".join(pos[k] for k in sorted(pos))


def main():
    os.makedirs(RAW, exist_ok=True)
    seen = set()
    for q, since in Q:
        fn = os.path.join(RAW, "q_" + re.sub(r"[^a-z0-9]+", "_", q.lower())[:60] + "_" + since + ".json")
        if not os.path.exists(fn):
            url = "https://api.openalex.org/works?" + urllib.parse.urlencode({
                "filter": f"title_and_abstract.search:{q},from_publication_date:{since}",
                "per_page": 50, "sort": "relevance_score:desc"})
            time.sleep(1.0)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=90) as r:
                    body = r.read()
            except Exception as e:
                print(f"## {q} [{since}]: failed {e!r}")
                continue
            with open(fn, "wb") as fh:
                fh.write(body)
        d = json.load(open(fn))
        res = d.get("results", [])
        print(f"## {q} [from {since}]: count={d.get('meta', {}).get('count')} fetched={len(res)}")
        for w in res:
            wid = w.get("id")
            if wid in seen:
                continue
            seen.add(wid)
            loc = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
            print(f"{w.get('publication_date')}|{(w.get('doi') or '').replace('https://doi.org/', '')}|{loc[:22]}|{(w.get('title') or '')[:115]}")


if __name__ == "__main__":
    main()
