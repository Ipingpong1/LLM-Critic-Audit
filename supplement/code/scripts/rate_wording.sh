#!/bin/sh
# Rate wording run, API part (prereg/rate_wording.md): the held-out items, Claude as Message Batches and OpenAI at the Flex
# rate (both half price). The open-model part runs on the cluster: see scripts/torch_submit.sh (RATEWORD=1).
# Re-running a step resumes it, and nothing is paid for twice.
#
#   DRY=1 STEP=1 scripts/rate_wording.sh   # Claude: build every batch and print its estimate; nothing is sent, no key needed
#   STEP=1 scripts/rate_wording.sh         # one step
#
#   step   what                                                               expected       cap
#   1      Opus 5.5, thinking on, 1 sample of the 13 rate conditions          $14            $17
#   2      Haiku 5.5, thinking on, 3 samples of the 13 rate conditions        $2.1           $3
#   probe  GPT-6.1 Sol and GPT-6 Luna: 40 used items, neutral, effort high    under $2       $1.50 + $0.50
#          and medium. Read for cost, reply length and parse rate only.
#   3      GPT-6.1 Sol, 1 sample.  EFFORT and CONDS come from the probe by    set by probe   $30
#   4      GPT-6 Luna, 3 samples.  the effort rule of the plan.               set by probe   $8
# A step stopped by its cap is not raised automatically: report and ask.
set -eu
cd "$(dirname "$0")/.."
STEP=${STEP:?set STEP to 1, 2, probe, 3 or 4}
DRY=${DRY:-}
D=results/rate_wording
ITEMS=data/items_premise.jsonl
PY=.venv/bin/python
mkdir -p "$D/probe"

claude() {
  if [ -n "$DRY" ]; then $PY -m pilot.run --backend anthropic --items "$ITEMS" --batch --dry-run "$@"
  else scripts/with_key.sh $PY -m pilot.run --backend anthropic --items "$ITEMS" --batch --poll 20 "$@"; fi
}
# OpenAI reasoning models through Chat Completions. Flex requests can be refused for lack of capacity (not charged);
# those trials stay unfinished, so the command is repeated until none is left, at most 6 times.
openai() {
  n=0
  while [ $n -lt 6 ]; do
    n=$((n + 1))
    scripts/with_openai_key.sh $PY -m pilot.run --base-url https://api.openai.com/v1 --api-key-env OPENAI_API_KEY \
        --flex --max-tokens 32000 --timeout 300 --retries 4 --log-every 200 "$@" | tee "$D/.last_run_$STEP.log"
    grep -q " 0 to run" "$D/.last_run_$STEP.log" && break
    grep -q "stopped on a request error\|stopped at the cost cap" "$D/.last_run_$STEP.log" && break
  done
}

case "$STEP" in
1)
  echo "== 1. Opus 5.5, thinking on (adaptive, effort high): 13 rate conditions, 1 sample"
  claude --model claude-opus-5-5 --thinking on --effort high --label opus-5.5-think --conditions rate_wording --samples 1 \
      --max-tokens 64000 --est-output-tokens 330 --batch-chunk 650 --max-usd 17 --out "$D/opus-5.5-think.jsonl" ;;
2)
  echo "== 2. Haiku 5.5, thinking on (adaptive, effort high): 13 rate conditions, 3 samples"
  claude --model claude-haiku-5-5 --thinking on --effort high --label haiku-5.5-think --conditions rate_wording --samples 3 \
      --max-tokens 64000 --est-output-tokens 900 --batch-chunk 2600 --max-usd 3 --out "$D/haiku-5.5-think.jsonl" ;;
probe)
  for effort in high medium; do
    echo "== probe: GPT-6.1 Sol, effort $effort"
    ITEMS=data/items_hard_a40.jsonl
    openai --model gpt-6.1-sol --effort $effort --label gpt-6.1-sol-$effort --items $ITEMS --conditions neutral --samples 1 \
        --concurrency 8 --max-usd 0.75 --out "$D/probe/gpt-6.1-sol-$effort.jsonl"
    echo "== probe: GPT-6 Luna, effort $effort"
    openai --model gpt-6-luna --effort $effort --label gpt-6-luna-$effort --items $ITEMS --conditions neutral --samples 1 \
        --concurrency 8 --max-usd 0.25 --out "$D/probe/gpt-6-luna-$effort.jsonl"
  done ;;
3)
  echo "== 3. GPT-6.1 Sol, reasoning effort ${EFFORT:?from the probe}, conditions ${CONDS:?from the probe}, 1 sample"
  openai --model gpt-6.1-sol --effort "$EFFORT" --label gpt-6.1-sol-think --items "$ITEMS" --conditions "$CONDS" --samples 1 \
      --concurrency "${CONC:-24}" --max-usd 30 --out "$D/gpt-6.1-sol-think.jsonl" ;;
4)
  echo "== 4. GPT-6 Luna, reasoning effort ${EFFORT:?from the probe}, conditions ${CONDS:?from the probe}, 3 samples"
  openai --model gpt-6-luna --effort "$EFFORT" --label gpt-6-luna-think --items "$ITEMS" --conditions "$CONDS" --samples 3 \
      --concurrency "${CONC:-32}" --max-usd 8 --out "$D/gpt-6-luna-think.jsonl" ;;
*) echo "unknown STEP $STEP" >&2; exit 1 ;;
esac
