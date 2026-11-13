#!/bin/sh
# Stage C (prereg/stage_c.md): the full run on the 200 hard items, plus the Claude model ladder
# (Haiku 5.5, Sonnet 5.5, Opus 5.5). Stage B trials are copied in first and reused (step 0);
# re-running any step resumes it, and nothing is paid for twice.
#
#   scripts/stage_c.sh            # every step in order
#   STEP=4 scripts/stage_c.sh     # one step only
#   DRY=1 scripts/stage_c.sh      # build every batch and print its estimate; nothing is sent
#
# Spending. Steps 2-6 and 8 are Message Batches (half price), sent in chunks: the whole step's
# estimate must fit its cap before anything is sent, and the cap is re-checked with the measured
# cost per call before each later chunk. Steps 1 and 7 are real time with hard caps.
#   step  what                                         expected  cap
#   1     smoke test, Haiku + Opus, 6 calls            $0.05     $0.80
#   2     Sonnet, thinking off, 18 conditions          $8.5      $12
#   3     Sonnet, thinking on (high), 6 core           $3.0      $5
#   4     Sonnet, max effort, 6 core                   $14       $20
#   5     Haiku, thinking off, 18 conditions           $0.8      $3
#   6     Haiku, thinking on (high), 18 conditions     $2        $5
#   7     Opus probe: 40 items, neutral, high          $0.5-2    $2.50
#   8     Opus, high, 6 core (gate on the probe)       $7-20     $20
#   9     analysis (free)
# Step 4 stopped at its cap on the first pass; it was resumed with CAP4=20 EST4=4700 (prereg/stage_c.md, Deviations).
set -eu
cd "$(dirname "$0")/.."
STEP=${STEP:-all}
DRY=${DRY:-}
D=results/frontier/stage_c
ITEMS=data/items_hard.jsonl
PY=.venv/bin/python
mkdir -p "$D"

want() { [ "$STEP" = all ] || [ "$STEP" = "$1" ]; }
# Batch step: a dry run needs no key and sends nothing.
batch() {
  if [ -n "$DRY" ]; then $PY -m pilot.run --backend anthropic --items "$ITEMS" --batch --dry-run "$@"
  else scripts/with_key.sh $PY -m pilot.run --backend anthropic --items "$ITEMS" --batch --poll 20 "$@"; fi
}
realtime() {
  if [ -n "$DRY" ]; then echo "  (dry run: real-time step skipped)"
  else scripts/with_key.sh $PY -m pilot.run --backend anthropic "$@"; fi
}

if want 0; then
  echo "== 0. reuse Stage B trials (free)"
  $PY scripts/seed_rows.py results/frontier/hard_sonnet-5.5-nothink.jsonl "$D/sonnet-5.5-nothink.jsonl" --conditions full
  $PY scripts/seed_rows.py results/frontier/hard_sonnet-5.5-think.jsonl "$D/sonnet-5.5-think.jsonl" --conditions core
  $PY scripts/seed_rows.py results/frontier/hard_sonnet-5.5-think-max.jsonl "$D/sonnet-5.5-think-max.jsonl" --conditions core
fi
if want 1; then
  echo "== 1. smoke test: 2 items, neutral, Haiku off / Haiku high / Opus high (real time)"
  S=results/frontier_smoke/stage_c
  realtime --model claude-haiku-5-5 --thinking off --effort high --label haiku-5.5-nothink --items "$ITEMS" \
      --conditions neutral --limit 2 --max-tokens 4096 --max-usd 0.05 --out "$S/haiku-5.5-nothink.jsonl"
  realtime --model claude-haiku-5-5 --thinking on --effort high --label haiku-5.5-think --items "$ITEMS" \
      --conditions neutral --limit 2 --max-tokens 16000 --max-usd 0.10 --out "$S/haiku-5.5-think.jsonl"
  realtime --model claude-opus-5-5 --thinking on --effort high --label opus-5.5-think --items "$ITEMS" \
      --conditions neutral --limit 2 --max-tokens 16000 --max-usd 0.65 --concurrency 1 --out "$S/opus-5.5-think.jsonl"
  [ -n "$DRY" ] || $PY scripts/stage_b_check.py "$S"/*.jsonl
fi
if want 2; then
  echo "== 2. Sonnet 5.5, thinking off, all 18 conditions"
  batch --model claude-sonnet-5-5 --thinking off --label sonnet-5.5-nothink --conditions full \
      --max-tokens 2048 --est-output-tokens 300 --batch-chunk 1000 --max-usd 12 --out "$D/sonnet-5.5-nothink.jsonl"
fi
if want 3; then
  echo "== 3. Sonnet 5.5, thinking on (adaptive, default effort = high), 6 core conditions"
  batch --model claude-sonnet-5-5 --thinking on --label sonnet-5.5-think --conditions core \
      --max-tokens 32000 --est-output-tokens 420 --batch-chunk 500 --max-usd 5 --out "$D/sonnet-5.5-think.jsonl"
fi
if want 4; then
  echo "== 4. Sonnet 5.5, thinking on at max effort, 6 core conditions"
  batch --model claude-sonnet-5-5 --thinking on --effort max --label sonnet-5.5-think-max --conditions core \
      --max-tokens 64000 --est-output-tokens "${EST4:-2600}" --batch-chunk 300 --max-usd "${CAP4:-20}" --out "$D/sonnet-5.5-think-max.jsonl"
fi
if want 5; then
  echo "== 5. Haiku 5.5, thinking off (effort high), all 18 conditions"
  batch --model claude-haiku-5-5 --thinking off --effort high --label haiku-5.5-nothink --conditions full \
      --max-tokens 4096 --est-output-tokens 600 --batch-chunk 1800 --max-usd 3 --out "$D/haiku-5.5-nothink.jsonl"
fi
if want 6; then
  echo "== 6. Haiku 5.5, thinking on (adaptive, effort high), all 18 conditions"
  batch --model claude-haiku-5-5 --thinking on --effort high --label haiku-5.5-think --conditions full \
      --max-tokens 64000 --est-output-tokens 2000 --batch-chunk 1200 --max-usd 5 --out "$D/haiku-5.5-think.jsonl"
fi
if want 7; then
  echo "== 7. Opus 5.5 probe: the 40 Stage B items, neutral, adaptive thinking at effort high (real time)"
  realtime --model claude-opus-5-5 --thinking on --effort high --label opus-5.5-think --items data/items_hard_a40.jsonl \
      --conditions neutral --max-tokens 64000 --concurrency 8 --log-every 10 --max-usd 2.50 --out "$D/opus-5.5-think.jsonl"
fi
if want 8; then
  echo "== 8. Opus 5.5, adaptive thinking at effort high: 6 core conditions if the probe says they fit \$20"
  set -- $($PY scripts/stage_c_gate.py "$D/opus-5.5-think.jsonl" --cap 20)
  if [ "$1" = stop ]; then
    echo "Opus gate: even the base-rate arm is projected over \$20; stopping here (see prereg/stage_c.md)"
  else
    batch --model claude-opus-5-5 --thinking on --effort high --label opus-5.5-think --conditions "$1" \
        --max-tokens 64000 --est-output-tokens "$2" --batch-chunk 300 --max-usd 20 --out "$D/opus-5.5-think.jsonl"
  fi
fi
if want 9; then
  echo "== 9. analysis"
  files=$(ls "$D"/*.jsonl)
  $PY scripts/stage_b_check.py $files
  $PY -m pilot.analyze $files --items "$ITEMS" --out-dir "$D/analysis"
  echo "== 9b. replication: Sonnet, thinking off, on the 160 items Stage B never saw"
  $PY -m pilot.analyze "$D/sonnet-5.5-nothink.jsonl" --items data/items_hard_new160.jsonl --subset \
      --out-dir "$D/analysis_new160"
fi
