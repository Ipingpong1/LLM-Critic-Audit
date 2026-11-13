"""Copy finished trials from an earlier results file into a new one, so the runner reuses them.

    .venv/bin/python scripts/seed_rows.py SRC DST --conditions core

Stage C reuses the Stage B trials made with the same model, prompt and settings (see
prereg/stage_c.md); the Stage A/B files stay as they are. Does nothing if DST already exists.
Copied rows keep every field and gain "reused_from": the source file name.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pilot.prompts import resolve_conditions  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("dst")
ap.add_argument("--conditions", required=True)
ap.add_argument("--items", default=None, help="only copy items listed in this JSONL file")
args = ap.parse_args()

src, dst = Path(args.src), Path(args.dst)
if dst.exists():
    print(f"seed: {dst} exists, leaving it alone")
    sys.exit(0)
keep = set(resolve_conditions(args.conditions))
ids = {json.loads(l)["id"] for l in Path(args.items).open()} if args.items else None
rows = []
for line in src.open():
    r = json.loads(line)
    finished = r.get("verdict") is not None or not r.get("retryable", False)
    if finished and r["condition"] in keep and (ids is None or r["item_id"] in ids):
        rows.append({**r, "reused_from": src.name})
dst.parent.mkdir(parents=True, exist_ok=True)
with dst.open("w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
conds = sorted({r["condition"] for r in rows})
print(f"seed: {len(rows)} trials from {src.name} -> {dst} ({len(conds)} conditions: {', '.join(conds)})")
