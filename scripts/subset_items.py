"""Take a split- and class-balanced subset of an items file, keeping file order.

    .venv/bin/python scripts/subset_items.py data/items_hard.jsonl data/items_hard_a40.jsonl --per-cell 10
"""
import argparse
import json
from collections import defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--per-cell", type=int, default=10, help="items per (split, has_error) cell")
args = ap.parse_args()

cells = defaultdict(list)
out = []
for line in open(args.src):
    it = json.loads(line)
    key = (it["split"], it["has_error"])
    if len(cells[key]) < args.per_cell:
        cells[key].append(it["id"])
        out.append(it)
with open(args.dst, "w") as f:
    for it in out:
        f.write(json.dumps(it) + "\n")
chars = sorted(sum(map(len, it["steps"])) for it in out)
print(f"wrote {len(out)} items to {args.dst}: " + ", ".join(f"{k[0]}/{'flawed' if k[1] else 'correct'}={len(v)}" for k, v in sorted(cells.items()))
      + f"; solution chars median {chars[len(chars)//2]}, max {chars[-1]}; "
      f"{sum(it['has_error'] and it['final_answer_correct'] for it in out)} flawed-but-right-answer")
