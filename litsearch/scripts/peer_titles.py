"""Print compact title lists of not-yet-seen candidates and mark them as seen.

Usage: python3 -I peer_titles.py SRC MIN_SCORE MAX_SCORE [--mark]
SRC: or | cr | oa (reads <src>_dedup.jsonl written by peer_triage.py)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import peer_lib as L  # noqa: E402

src, lo, hi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
mark = "--mark" in sys.argv
seen_path = os.path.join(L.SCRATCH, f"seen_{src}.txt")
seen = set(x.strip() for x in open(seen_path)) if os.path.exists(seen_path) else set()
rows = []
for line in open(os.path.join(L.SCRATCH, f"{src}_dedup.jsonl")):
    r = json.loads(line)
    k = r["key"]
    if k in seen:
        continue
    yr = r.get("year") or 0
    if yr and yr < 2022:
        continue
    cl = r["cl"]
    ok = (cl["LLM"] and bool(cl["A"] or cl["B"] or cl["C"])) if src == "cr" else cl["hit"]
    if not ok or not (lo <= cl["score"] <= hi):
        continue
    rows.append((cl["score"], k, r))
rows.sort(key=lambda x: (-x[0], x[1]))
for s, k, r in rows:
    if src == "or":
        v = (r.get("venueid") or "").replace("/Conference", "/C").replace("/Workshop", "/W")[:38]
    elif src == "cr":
        v = (r.get("venue") or "")[:38]
    else:
        v = (r.get("primary_source") or "")[:30]
    kk = k.split("/")[-1]
    print(f"{s}|{kk}|{r.get('year')}|{v}|{(r.get('title') or '')[:120]}")
print(f"# {len(rows)} new rows (score {lo}-{hi})", file=sys.stderr)
if mark:
    with open(seen_path, "a") as f:
        for _, k, _ in rows:
            f.write(k + "\n")
