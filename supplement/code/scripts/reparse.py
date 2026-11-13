"""Re-apply the current reply parser to stored raw replies, rewriting verdict and p_error in place.

Use after a parser fix, and never on a file a run is still appending to:
    .venv/bin/python scripts/reparse.py results/pilot/qwen3.5_4b-nothink.jsonl
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pilot.run import parse_response  # noqa: E402

for path in map(Path, sys.argv[1:]):
    rows = [json.loads(line) for line in path.open()]
    changed = 0
    for r in rows:
        if r.get("retryable") or r.get("raw") is None:
            continue
        verdict, p = parse_response(r["raw"])
        if (verdict, p) != (r["verdict"], r["p_error"]):
            r["verdict"], r["p_error"] = verdict, p
            changed += 1
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))
    print(f"{path}: {changed} of {len(rows)} rows re-parsed, {sum(r['verdict'] is None for r in rows)} still unparsed")
