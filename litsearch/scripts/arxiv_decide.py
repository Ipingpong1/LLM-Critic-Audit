#!/usr/bin/env python3
"""Append screening decisions to raw/arxiv/derived/decisions.jsonl.

Usage: python3 -I arxiv_decide.py <decisions.jsonl> <stage> < lines
Each input line: id | relevance | claims | manipulation | measurement | domain_models | full_text_read | notes
(trailing fields may be omitted; relevance is close / related / background / exclude / maybe).
Later lines for the same id override earlier ones when the outputs are written.
"""
import json
import sys
import time

FIELDS = ["id", "relevance", "claims", "manipulation", "measurement", "domain_models", "full_text_read", "notes"]


def main(path, stage):
    n = 0
    with open(path, "a", encoding="utf-8") as fh:
        for line in sys.stdin:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            while len(parts) > len(FIELDS) and parts[-1] == "":
                parts.pop()
            if len(parts) > len(FIELDS):
                parts = parts[:len(FIELDS) - 1] + [" | ".join(x for x in parts[len(FIELDS) - 1:] if x)]
            rec = dict(zip(FIELDS, parts))
            if rec.get("relevance") not in ("close", "related", "background", "exclude", "maybe"):
                print("BAD RELEVANCE:", line, file=sys.stderr)
                continue
            rec["stage"] = stage
            rec["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    print(f"appended {n} decisions ({stage})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
