"""Opus gate for Stage C (prereg/stage_c.md, decision rule "Opus"): which conditions fit the cap.

    .venv/bin/python scripts/stage_c_gate.py results/frontier/stage_c/opus-5.5-think.jsonl --cap 20

Projects the batch cost of the 200-item Opus run from the 40-item probe (mean input tokens,
and mean output tokens + 25%), then prints one line for the run script:
    "<condition set> <est output tokens>"   core if it fits the cap, else base_rate if that fits,
                                            else "stop".
Explanations go to stderr. Without probe data it assumes 1,000 output tokens (dry runs only).
"""
import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pilot.prompts import resolve_conditions  # noqa: E402
from pilot.run import PRICES  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("probe")
ap.add_argument("--cap", type=float, required=True)
ap.add_argument("--items", type=int, default=200)
ap.add_argument("--model", default="claude-opus-5-5")
args = ap.parse_args()

p = Path(args.probe)
rows = [json.loads(l) for l in p.open()] if p.exists() else []
rows = [r for r in rows if r.get("completion_tokens") is not None]
if rows:
    tin = sum(r["prompt_tokens"] for r in rows) / len(rows)
    tout = sum(r["completion_tokens"] for r in rows) / len(rows)
    basis = f"probe: {len(rows)} calls, mean {tin:.0f} in / {tout:.0f} out tokens"
else:
    tin, tout = 1500, 1000
    basis = "no probe data: assuming 1500 in / 1000 out tokens"
est_out = math.ceil(1.25 * tout)
pin, pout = PRICES[args.model]
per_call = (tin * pin + est_out * pout) / 1e6 * 0.5
choice = "stop"
for name in ("core", "base_rate"):
    conds = resolve_conditions(name)
    n = len(conds) * args.items - sum(r["condition"] in conds for r in rows)  # probe trials are reused
    cost = n * per_call
    print(f"gate: {name}: {n} new calls x ${per_call:.4f} = ${cost:.2f} (cap ${args.cap:.2f}; {basis}, "
          f"output +25%)", file=sys.stderr)
    if cost <= args.cap:
        choice = name
        break
print(f"{choice} {est_out}")
