"""Per-condition health check for Stage B files: parsed, refusals, cut-offs, output length, hits and false alarms.

    .venv/bin/python scripts/stage_b_check.py results/frontier/hard_sonnet-5.5-nothink.jsonl [...]
"""
import json
import sys
from collections import defaultdict

sys.path.insert(0, ".")
from pilot.prompts import CONDITIONS  # noqa: E402

for path in sys.argv[1:]:
    rows = [json.loads(l) for l in open(path)]
    by = defaultdict(list)
    for r in rows:
        by[r["condition"]].append(r)
    print(f"\n{path}: {len(rows)} rows, ${sum(r.get('cost_usd') or 0 for r in rows):.2f}")
    print(f"{'condition':12s} {'n':>3s} {'unparsed':>8s} {'refused':>7s} {'cut':>4s} {'tok med':>7s} {'tok max':>7s} "
          f">2k  {'misses':>6s} {'FAs':>5s}  verdict words")
    for c in [c for c in CONDITIONS if c in by]:
        rs = by[c]
        toks = sorted(r.get("completion_tokens") or 0 for r in rs)
        fl = [r for r in rs if r["has_error"] and r["verdict"]]
        co = [r for r in rs if not r["has_error"] and r["verdict"]]
        words = defaultdict(int)
        for r in rs:
            raw = (r.get("raw") or "")
            for w in ("\"error\"", "\"correct\"", "\"flawed\"", "\"sound\""):
                if f'"verdict": {w}' in raw.replace('":"', '": "').replace('" :', '":'):
                    words[w.strip('"')] += 1
        print(f"{c:12s} {len(rs):3d} {sum(r['verdict'] is None for r in rs):8d} "
              f"{sum(r.get('finish_reason') == 'refusal' for r in rs):7d} "
              f"{sum(r.get('finish_reason') in ('max_tokens', 'length') for r in rs):4d} "
              f"{toks[len(toks) // 2]:7d} {toks[-1]:7d} {sum(t > 2000 for t in toks):3d}  "
              f"{sum(r['verdict'] == 'correct' for r in fl):3d}/{len(fl):<3d} {sum(r['verdict'] == 'error' for r in co):2d}/{len(co):<3d} "
              + " ".join(f"{k}={v}" for k, v in sorted(words.items())))
