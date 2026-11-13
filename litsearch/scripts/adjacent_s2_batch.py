#!/usr/bin/env python3
"""One Semantic Scholar /paper/batch call for metadata of screened arXiv ids (adjacent stream).
argv[1]: file with one id per line (e.g. ARXIV:2601.07767); argv[2]: output JSON. 60 s wait on 429, max 5 retries."""
import json, os, sys, time, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.dirname(HERE), "raw", "adjacent")
ids = [l.strip() for l in open(sys.argv[1]) if l.strip()]
url = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year,venue,publicationVenue,journal,authors,externalIds,publicationDate"
body = json.dumps({"ids": ids}).encode()
for attempt in range(6):
    try:
        req = urllib.request.Request(url, data=body, headers={"User-Agent": "critic-sdt-litsearch/0.1", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=90) as r:
            text = r.read().decode()
        open(sys.argv[2], "w").write(text)
        open(os.path.join(RAW, "s2_batch_metadata.json"), "w").write(text)
        print("ok", len(json.loads(text)))
        break
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, "attempt", attempt + 1, flush=True)
        if e.code == 429 and attempt < 5:
            time.sleep(60); continue
        raise
