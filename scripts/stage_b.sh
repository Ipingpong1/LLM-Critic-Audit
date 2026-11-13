#!/bin/sh
# Stage B on Claude Sonnet 5.5: the 40 hard items from Stage A x the Stage B conditions
# (see prereg/stage_b.md). The neutral trials from Stage A are reused: same output files,
# and the runner skips trials that are already there. Re-running resumes; nothing is paid twice.
#
#   scripts/stage_b.sh          # steps 1-4 in order
#   STEP=2 scripts/stage_b.sh   # one step only
#
# Spending: step 1 is one Message Batch (half price). A batch can't be stopped part-way,
# so it is gated by its estimate (~$1.2) and bounded by --max-tokens (at most $5.41 even if
# every reply used all 2,048 tokens). Steps 2 and 3 are real-time with hard caps.
set -eu
cd "$(dirname "$0")/.."
STEP=${STEP:-all}
run() { scripts/with_key.sh .venv/bin/python -m pilot.run --backend anthropic --model claude-sonnet-5-5 \
          --items data/items_hard_a40.jsonl "$@"; }

if [ "$STEP" = all ] || [ "$STEP" = 1 ]; then
  echo "== 1. thinking off, all Stage B conditions, as one batch"
  run --conditions stage_b --thinking off --label sonnet-5.5-nothink --max-tokens 2048 \
      --batch --est-output-tokens 300 --max-usd 3.00 --out results/frontier/hard_sonnet-5.5-nothink.jsonl
fi
if [ "$STEP" = all ] || [ "$STEP" = 2 ]; then
  echo "== 2. thinking on (adaptive, default effort), all Stage B conditions, real time"
  run --conditions stage_b --thinking on --label sonnet-5.5-think --max-tokens 32000 --concurrency 8 \
      --max-usd 4.00 --log-every 60 --out results/frontier/hard_sonnet-5.5-think.jsonl
fi
if [ "$STEP" = all ] || [ "$STEP" = 3 ]; then
  echo "== 3. effort probe: neutral only, adaptive thinking at max effort, real time"
  run --conditions neutral --thinking on --effort max --label sonnet-5.5-think-max --max-tokens 64000 \
      --concurrency 8 --max-usd 2.50 --log-every 10 --out results/frontier/hard_sonnet-5.5-think-max.jsonl
fi
if [ "$STEP" = all ] || [ "$STEP" = 4 ]; then
  echo "== 4. analysis"
  .venv/bin/python -m pilot.analyze results/frontier/hard_sonnet-5.5-nothink.jsonl \
      results/frontier/hard_sonnet-5.5-think.jsonl results/frontier/hard_sonnet-5.5-think-max.jsonl \
      --items data/items_hard_a40.jsonl --out-dir results/frontier/stage_b
fi
