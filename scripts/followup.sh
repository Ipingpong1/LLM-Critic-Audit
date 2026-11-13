#!/bin/sh
# Rate-use follow-up, API part (prereg/rate_use_followup.md): the held-out items, Claude as Message Batches and OpenAI at the
# Flex rate (both half price). The open-model part runs on the cluster: scripts/torch_submit.sh (FOLLOWUP=1).
# Re-running a step resumes it, and nothing is paid for twice.
#
#   DRY=1 STEP=1 scripts/followup.sh   # Claude: build every batch and print its estimate; nothing is sent, no key needed
#   STEP=smoke scripts/followup.sh     # 4 already-used items x every new condition, every API critic, real time: parse check only
#   STEP=1 scripts/followup.sh         # one step
#
#   step   what                                                                   expected   cap
#   1      Opus 5.5, reasoning on (high), 1 sample of the 6 conditions           $13        $17   (exact token counts, 2026-11-13)
#   2      Haiku 5.5, reasoning on (high), 3 samples of the 6 conditions         $1.5       $3
#   3      GPT-6.1 Sol, effort high, 1 sample of the 6 conditions                $3.5       $8
#   4      GPT-6 Luna, effort high, 3 samples of the 6 conditions                $1         $3
#   5      Opus 5.5, the paper arm: 8 conditions, 1 sample                      $40 uncached, less with caching   PAPER_CAP (default $48)
# A step stopped by its cap is not raised automatically: report and ask.
set -eu
cd "$(dirname "$0")/.."
STEP=${STEP:?set STEP to smoke, 1, 2, 3, 4 or 5}
DRY=${DRY:-}
D=results/followup
ITEMS=data/items_premise.jsonl
PY=.venv/bin/python
mkdir -p "$D/smoke"

# --cache-system: the example blocks and the paper are the same text in every request of a condition, so they are
# billed as cache reads after the first request (run log of the plan). The model's input is unchanged.
claude() {
  if [ -n "$DRY" ]; then $PY -m pilot.run --backend anthropic --items "$ITEMS" --batch --dry-run --cache-system "$@"
  else scripts/with_key.sh $PY -m pilot.run --backend anthropic --items "$ITEMS" --batch --poll 20 --cache-system "$@"; fi
}
claude_rt() { scripts/with_key.sh $PY -m pilot.run --backend anthropic --concurrency 4 --cache-system "$@"; }
# OpenAI reasoning models through Chat Completions at the Flex rate; refused requests (no capacity, not charged) are repeated.
openai() {
  n=0
  while [ $n -lt 6 ]; do
    n=$((n + 1))
    scripts/with_openai_key.sh $PY -m pilot.run --base-url https://api.openai.com/v1 --api-key-env OPENAI_API_KEY \
        --flex --max-tokens 32000 --timeout 300 --retries 4 --log-every 200 "$@" | tee "$D/last_run_$STEP.log"
    grep -q " 0 to run" "$D/last_run_$STEP.log" && break
    grep -q "stopped on a request error\|stopped at the cost cap" "$D/last_run_$STEP.log" && break
  done
}

case "$STEP" in
smoke)
  # 4 items already used elsewhere (2 flawed, 2 correct), every new condition, one reply each. Read for parse rates only.
  S=data/items_hard_a40.jsonl
  echo "== smoke: Opus 5.5 (14 conditions x 4 items, cap 1.50 USD)"
  claude_rt --model claude-opus-5-5 --thinking on --effort high --label opus-5.5-think --items $S --limit 4 \
      --conditions followup_smoke --samples 1 --max-tokens 64000 --max-usd 1.50 --out "$D/smoke/opus-5.5-think.jsonl"
  echo "== smoke: Haiku 5.5 (6 conditions x 4 items, cap 0.20 USD)"
  claude_rt --model claude-haiku-5-5 --thinking on --effort high --label haiku-5.5-think --items $S --limit 4 \
      --conditions followup_api --samples 1 --max-tokens 64000 --max-usd 0.20 --out "$D/smoke/haiku-5.5-think.jsonl"
  echo "== smoke: GPT-6.1 Sol (6 conditions x 4 items, cap 0.50 USD)"
  openai --model gpt-6.1-sol --effort high --label gpt-6.1-sol-think --items $S --limit 4 --conditions followup_api \
      --samples 1 --concurrency 8 --max-usd 0.50 --out "$D/smoke/gpt-6.1-sol-think.jsonl"
  echo "== smoke: GPT-6 Luna (6 conditions x 4 items, cap 0.10 USD)"
  openai --model gpt-6-luna --effort high --label gpt-6-luna-think --items $S --limit 4 --conditions followup_api \
      --samples 1 --concurrency 8 --max-usd 0.10 --out "$D/smoke/gpt-6-luna-think.jsonl" ;;
1)
  echo "== 1. Opus 5.5, reasoning on (adaptive, effort high): 6 conditions, 1 sample"
  claude --model claude-opus-5-5 --thinking on --effort high --label opus-5.5-think --conditions followup_api --samples 1 \
      --max-tokens 64000 --est-output-tokens 330 --batch-chunk 600 --max-usd 17 --out "$D/opus-5.5-think.jsonl" ;;
2)
  echo "== 2. Haiku 5.5, reasoning on (adaptive, effort high): 6 conditions, 3 samples"
  claude --model claude-haiku-5-5 --thinking on --effort high --label haiku-5.5-think --conditions followup_api --samples 3 \
      --max-tokens 64000 --est-output-tokens 900 --batch-chunk 1800 --max-usd 3 --out "$D/haiku-5.5-think.jsonl" ;;
3)
  echo "== 3. GPT-6.1 Sol, effort high: 6 conditions, 1 sample"
  openai --model gpt-6.1-sol --effort high --label gpt-6.1-sol-think --items "$ITEMS" --conditions followup_api --samples 1 \
      --concurrency "${CONC:-24}" --max-usd 8 --out "$D/gpt-6.1-sol-think.jsonl" ;;
4)
  echo "== 4. GPT-6 Luna, effort high: 6 conditions, 3 samples"
  openai --model gpt-6-luna --effort high --label gpt-6-luna-think --items "$ITEMS" --conditions followup_api --samples 3 \
      --concurrency "${CONC:-32}" --max-usd 3 --out "$D/gpt-6-luna-think.jsonl" ;;
5)
  echo "== 5. Opus 5.5, the paper arm: 8 conditions, 1 sample (cap ${PAPER_CAP:-48} USD)"
  claude --model claude-opus-5-5 --thinking on --effort high --label opus-5.5-think --conditions followup_paper --samples 1 \
      --max-tokens 64000 --est-output-tokens 330 --batch-chunk 400 --max-usd "${PAPER_CAP:-48}" --out "$D/opus-5.5-think-paper.jsonl" ;;
*) echo "unknown STEP $STEP" >&2; exit 1 ;;
esac
