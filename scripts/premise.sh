#!/bin/sh
# Premise test, Claude part (prereg/premise.md): the 9 claim conditions on the held-out items, as Message Batches (half price).
# The open-model part runs on Torch: see scripts/torch_submit.sh. Re-running a step resumes it, and nothing is paid for twice.
#
#   scripts/premise.sh            # steps 1 and 2
#   STEP=3 scripts/premise.sh     # one step only
#   DRY=1 scripts/premise.sh      # build every batch and print its estimate; nothing is sent, no key needed
#
#   step  what                                                  expected  cap
#   1     Opus 5.5, thinking on, 1 sample of all 9 conditions   $10       $14
#   1b    Opus 5.5, a second sample of neutral and presuppose   $2.5      $4
#   2     Haiku 5.5, thinking on, 3 samples of all 9            $1.6      $3
#   3     Sonnet 5.5, thinking on, as step 1 + 1b (optional)    $7        $10
# A step stopped by its cap is not raised automatically: report and ask.
set -eu
cd "$(dirname "$0")/.."
STEP=${STEP:-all}
DRY=${DRY:-}
D=results/premise
ITEMS=data/items_premise.jsonl
PY=.venv/bin/python
mkdir -p "$D"

want() { [ "$STEP" = all ] || [ "$STEP" = "$1" ]; }
batch() {
  if [ -n "$DRY" ]; then $PY -m pilot.run --backend anthropic --items "$ITEMS" --batch --dry-run "$@"
  else scripts/with_key.sh $PY -m pilot.run --backend anthropic --items "$ITEMS" --batch --poll 20 "$@"; fi
}

if want 1; then
  echo "== 1. Opus 5.5, thinking on (adaptive, effort high): 9 conditions, 1 sample"
  batch --model claude-opus-5-5 --thinking on --effort high --label opus-5.5-think --conditions premise_core --samples 1 \
      --max-tokens 64000 --est-output-tokens 330 --batch-chunk 300 --max-usd 14 --out "$D/opus-5.5-think.jsonl"
  echo "== 1b. Opus 5.5: second sample of neutral and presuppose, for the retest check"
  # A dry run has no step 1 rows, so it would count sample 0 again: 800 calls, not the real 400.
  if [ -n "$DRY" ]; then echo "  (dry run: skipped; 400 calls, about \$2.3 at the cost per call measured in Stage C, cap \$4)"
  else batch --model claude-opus-5-5 --thinking on --effort high --label opus-5.5-think --conditions neutral,presuppose --samples 2 \
      --max-tokens 64000 --est-output-tokens 330 --batch-chunk 200 --max-usd 4 --out "$D/opus-5.5-think.jsonl"; fi
fi
if want 2; then
  echo "== 2. Haiku 5.5, thinking on (adaptive, effort high): 9 conditions, 3 samples"
  batch --model claude-haiku-5-5 --thinking on --effort high --label haiku-5.5-think --conditions premise_core --samples 3 \
      --max-tokens 64000 --est-output-tokens 900 --batch-chunk 1800 --max-usd 3 --out "$D/haiku-5.5-think.jsonl"
fi
# Optional, so `all` leaves it out: run it with STEP=3 once approved.
if [ "$STEP" = 3 ]; then
  echo "== 3. Sonnet 5.5, thinking on (adaptive, default effort): 9 conditions, 1 sample, then a second sample of neutral and presuppose"
  batch --model claude-sonnet-5-5 --thinking on --label sonnet-5.5-think --conditions premise_core --samples 1 \
      --max-tokens 32000 --est-output-tokens 380 --batch-chunk 500 --max-usd 8 --out "$D/sonnet-5.5-think.jsonl"
  if [ -n "$DRY" ]; then echo "  (dry run: second sample skipped; 400 calls, about \$1.3, cap \$2)"
  else batch --model claude-sonnet-5-5 --thinking on --label sonnet-5.5-think --conditions neutral,presuppose --samples 2 \
      --max-tokens 32000 --est-output-tokens 380 --batch-chunk 200 --max-usd 2 --out "$D/sonnet-5.5-think.jsonl"; fi
fi
