"""Build a balanced sample of correct and flawed solutions from ProcessBench.

ProcessBench labels each step-by-step solution with the index of its earliest
erroneous step, or -1 if every step is correct. We only need the binary
"contains an error" label, so `has_error = label >= 0`.

Usage:
    uv run python -m pilot.data --n-per-class 100
"""
import argparse
import json
import random
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
HF_URL = "https://huggingface.co/datasets/Qwen/ProcessBench/resolve/main/{split}.json"


def load_split(split: str) -> list[dict]:
    path = RAW / f"{split}.json"
    if not path.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        print(f"downloading {split} -> {path}")
        urllib.request.urlretrieve(HF_URL.format(split=split), path)
    return json.loads(path.read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--splits", default="gsm8k,math",
                    help="comma-separated ProcessBench splits (gsm8k, math, olympiadbench, omnimath)")
    ap.add_argument("--n-per-class", type=int, default=100,
                    help="items per class (correct / flawed), divided evenly across splits")
    ap.add_argument("--max-chars", type=int, default=6000,
                    help="skip solutions longer than this (keeps local runs fast)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--fresh-from", default=None,
                    help="items file: draw only from problems it does not use, with one solution per problem (held-out items)")
    ap.add_argument("--out", default=str(ROOT / "data" / "items.jsonl"))
    args = ap.parse_args()

    rng = random.Random(args.seed)
    splits = args.splits.split(",")
    per_split = args.n_per_class // len(splits)
    items = []
    # Problems can have several solutions in ProcessBench. Held-out items share none with the earlier set or with each other.
    used = {json.loads(l)["problem"] for l in open(args.fresh_from)} if args.fresh_from else None
    for split in splits:
        rows = [r for r in load_split(split) if sum(map(len, r["steps"])) <= args.max_chars]
        if used is not None:
            rows = [r for r in rows if r["problem"] not in used]
        for has_error in (False, True):
            pool = [r for r in rows if (r["label"] >= 0) == has_error]
            if used is not None:
                rng.shuffle(pool)
                picked = []
                for r in pool:
                    if r["problem"] not in used and len(picked) < per_split:
                        used.add(r["problem"])
                        picked.append(r)
                pool = picked
            if len(pool) < per_split:
                raise SystemExit(f"{split}: only {len(pool)} items with has_error={has_error}, need {per_split}")
            for r in rng.sample(pool, per_split):
                items.append({
                    "id": r["id"],
                    "split": split,
                    "problem": r["problem"],
                    "steps": r["steps"],
                    "has_error": has_error,
                    "first_error_step": r["label"],
                    # Flawed solutions that still reach the right answer are the hard cases.
                    "final_answer_correct": r["final_answer_correct"],
                    "generator": r["generator"],
                })
    rng.shuffle(items)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
    n_err = sum(it["has_error"] for it in items)
    n_hard = sum(it["has_error"] and it["final_answer_correct"] for it in items)
    print(f"wrote {len(items)} items ({n_err} flawed, {len(items) - n_err} correct; "
          f"{n_hard} flawed-but-right-answer) to {out}")


if __name__ == "__main__":
    main()
