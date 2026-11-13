"""Print abstracts for Crossref DOIs; for ACL Anthology DOIs without an abstract, read the anthology page.
Usage: python3 -I peer_acl_abs.py DOI1,DOI2,...   (pages saved under ../raw/peer/acl_pages/)"""
import html, json, os, re, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import peer_lib as L  # noqa: E402
want = [d.lower() for d in sys.argv[1].split(",")]
recs = {}
for line in open(os.path.join(L.SCRATCH, "cr_dedup.jsonl")):
    r = json.loads(line)
    if r["key"] in want:
        recs[r["key"]] = r
for d in want:
    r = recs.get(d, {})
    ab = r.get("abstract") or ""
    src = "crossref"
    if not ab and d.startswith("10.18653/"):
        aid = d.split("/")[-1]
        url = f"https://aclanthology.org/{aid}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": L.UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                t = resp.read().decode("utf-8", "replace")
            os.makedirs(os.path.join(L.RAW, "acl_pages"), exist_ok=True)
            open(os.path.join(L.RAW, "acl_pages", aid + ".html"), "w").write(t)
            m = re.search(r'<div class="card-body acl-abstract">(.*?)</div>', t, re.S)
            ab = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))).strip() if m else "(no abstract on page)"
            au = re.findall(r'<meta content="([^"]+)" name="citation_author"', t)
            r["authors"] = r.get("authors") or "; ".join(au)
            src = "aclanthology"
        except Exception as e:
            ab = f"(fetch failed: {e})"
        time.sleep(1.0)
    print(f"== {d} | {r.get('year')} | {r.get('venue','')[:80]}\n   T: {r.get('title')}\n   AU: {(r.get('authors') or '')[:160]}\n   ABS[{src}]: {ab[:1400]}")
