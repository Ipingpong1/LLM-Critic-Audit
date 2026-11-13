#!/bin/bash
# Submit the thinking on/off study on the HPC cluster: four models x {nothink, think} in bf16,
# every condition (base-rate arm, follow-ups, strictness battery: 15 x 200 = 3000 requests per job).
# Run from the project root on a cluster login node, after scripts/torch_setup.sh:
#
#   SMOKE=1 scripts/torch_submit.sh    # 20 items x 4 base-rate conditions -> results/torch_smoke/
#   scripts/torch_submit.sh            # full runs -> results/torch/
#   HARD=1 NOTHINK_SAMPLING=card THINK_SAMPLING=card scripts/torch_submit.sh
#                                      # hard item pool, Stage B conditions, T = 1 -> results/torch_hard/
#   PREMISE=1 NOTHINK_SAMPLING=card THINK_SAMPLING=card NOTHINK_SAMPLES=3 THINK_SAMPLES=3 scripts/torch_submit.sh
#                                      # held-out items, premise conditions, 3 samples -> results/premise/ (prereg/premise.md)
#   PREMISE=smoke NOTHINK_SAMPLING=card ONLY='4b-nothink' scripts/torch_submit.sh
#                                      # the new prompts on 40 items already used elsewhere -> results/torch_smoke/premise/
#   RATEWORD=1 NOTHINK_SAMPLING=card THINK_SAMPLING=card NOTHINK_SAMPLES=3 THINK_SAMPLES=3 scripts/torch_submit.sh
#                                      # held-out items, the new rate wordings, 3 samples -> results/rate_wording/ (prereg/rate_wording.md)
#   RATEWORD=smoke NOTHINK_SAMPLING=card ONLY='4b-nothink' scripts/torch_submit.sh
#                                      # those wordings on 40 items already used elsewhere -> results/torch_smoke/rate_wording/
#
# Optional: ACCOUNT (Slurm account), ONLY (regex on the label, e.g. ONLY='9b|27b-think'), DRY=1 (print only),
# THINK_LOGPROBS=1 (also record verdict-token logprobs when thinking; large replies),
# THINK_SAMPLING=card (thinking runs use the sampling each model card recommends, labels end in -t1;
# greedy decoding sends Qwen3.5's thinking into repetition loops on ~6% of items), THINK_SAMPLES (default 1),
# NOTHINK_SAMPLING=card (thinking-off runs use that same sampling, labels end in -t1), NOTHINK_SAMPLES (default 1; needs card).
# Example, only the T=1.0 thinking-off runs: NOTHINK_SAMPLING=card ONLY='nothink-bf16-t1' scripts/torch_submit.sh
set -euo pipefail
cd "$(dirname "$0")/.."

# Supply the allocation for the cluster on which this job will run.
: "${ACCOUNT:?Set ACCOUNT to your Slurm allocation before submitting jobs}"
export VLLM_SIF=${VLLM_SIF:-/scratch/$USER/images/vllm-openai_v0.32.0.sif}
export PYTHON=${PYTHON:-$PWD/.venv/bin/python}
export HF_HOME=${HF_HOME:-/scratch/$USER/.huggingface}
export CACHE=${CACHE:-/scratch/$USER/.cache}

export ITEMS=
THINK_MAX_TOKENS=16384; THINK_TIMEOUT=3600; THINK_HOURS=12
if [ -n "${RATEWORD:-}" ]; then
  # Rate wording run (prereg/rate_wording.md): the 9 conditions the open models lack on the held-out items,
  # 9 x 200 = 1800 per sample. Same items, labels, sampling and reply limits as PREMISE, so the rows join by label.
  DIR=results/rate_wording; export CONDITIONS=rate_wording_new LIMIT= ITEMS=data/items_premise.jsonl
  if [ "$RATEWORD" = smoke ]; then DIR=results/torch_smoke/rate_wording; ITEMS=data/items_hard_a40.jsonl; fi
  THINK_MAX_TOKENS=32768; THINK_TIMEOUT=7200; THINK_HOURS=24; export MAX_MODEL_LEN=36864
elif [ -n "${PREMISE:-}" ]; then
  # Premise test: 13 x 200 = 2600 per sample. Same reply limits as HARD, so the two are comparable.
  DIR=results/premise; export CONDITIONS=premise LIMIT= ITEMS=data/items_premise.jsonl
  if [ "$PREMISE" = smoke ]; then DIR=results/torch_smoke/premise; ITEMS=data/items_hard_a40.jsonl; fi
  THINK_MAX_TOKENS=32768; THINK_TIMEOUT=7200; THINK_HOURS=24; export MAX_MODEL_LEN=36864
elif [ "${HARD:-0}" = 1 ]; then
  # Frontier comparison: the 200-item OlympiadBench + Omni-MATH pool, Stage B conditions (13 x 200 = 2600 per job).
  DIR=results/torch_hard; export CONDITIONS=stage_b LIMIT= ITEMS=data/items_hard.jsonl
  # Thinking runs longer here: on the easy items p99 already reached 16k, and the Claude runs on these items
  # allowed 32k-64k. A low cap would drop the hardest replies. Prompts reach about 3.1k tokens.
  THINK_MAX_TOKENS=32768; THINK_TIMEOUT=7200; THINK_HOURS=24; export MAX_MODEL_LEN=36864
elif [ "${SMOKE:-0}" = 1 ]; then
  DIR=results/torch_smoke; export CONDITIONS=base_rate LIMIT=20
else
  DIR=results/torch; export CONDITIONS=base_rate,followups,strictness LIMIT=
fi
mkdir -p "$DIR" logs

# model id | name | vLLM reasoning parser | GPUs (bf16 weights: 9, 19, 24, 56 GB; an L40S has 48 GB) |
# sampling the model card recommends for thinking (with temperature 1.0)
MODELS=(
  'Qwen/Qwen3.5-4B|qwen3.5:4b|qwen3|1|"top_p": 0.95, "top_k": 20, "presence_penalty": 1.5'
  'Qwen/Qwen3.5-9B|qwen3.5:9b|qwen3|1|"top_p": 0.95, "top_k": 20, "presence_penalty": 1.5'
  'google/gemma-4-12B-it|gemma4:12b|gemma4|1|"top_p": 0.95, "top_k": 64'
  'Qwen/Qwen3.5-27B|qwen3.5:27b|qwen3|2|"top_p": 0.95, "top_k": 20, "presence_penalty": 1.5'
)

for row in "${MODELS[@]}"; do
  IFS='|' read -r model name parser gpus sampling <<< "$row"
  for mode in nothink think; do
    label="$name-$mode-bf16"
    temp=0; samples=1; body="\"chat_template_kwargs\": {\"enable_thinking\": false}"
    if [ "$mode" = think ]; then
      # Thinking: replies of ~1-12k tokens (smoke test), so long timeouts and no per-token logprobs.
      max_tokens=$THINK_MAX_TOKENS; logprobs=${THINK_LOGPROBS:-0}; conc=128; timeout=$THINK_TIMEOUT
      body="\"chat_template_kwargs\": {\"enable_thinking\": true}"
      if [ "${THINK_SAMPLING:-greedy}" = card ]; then
        temp=1.0; samples=${THINK_SAMPLES:-1}; body="$body, $sampling"; label="$label-t1"
      fi
      hours=$((THINK_HOURS * samples)); if [ $hours -gt 47 ]; then hours=47; fi; time=$hours:00:00
    else
      max_tokens=1024; logprobs=1; conc=64; timeout=600; time=03:00:00
      # Same sampling as the thinking runs, to separate thinking from temperature.
      if [ "${NOTHINK_SAMPLING:-greedy}" = card ]; then
        temp=1.0; samples=${NOTHINK_SAMPLES:-1}; body="$body, $sampling"; label="$label-t1"
      fi
    fi
    if [ -n "${ONLY:-}" ] && ! [[ $label =~ $ONLY ]]; then continue; fi
    if [ -n "$LIMIT" ]; then time=01:00:00; fi
    cmd=(sbatch --parsable --account="$ACCOUNT" --job-name="critic-${label//:/-}" --time="$time"
         --gres="gpu:$gpus" --constraint=l40s scripts/run_pilot_vllm.sbatch)
    echo "$label: ${cmd[*]}"
    if [ "${DRY:-0}" = 1 ]; then continue; fi
    MODEL=$model LABEL=$label OUT="$DIR/${label//:/_}.jsonl" TP=$gpus REASONING_PARSER=$parser \
      EXTRA_BODY="{$body}" TEMPERATURE=$temp SAMPLES=$samples \
      MAX_TOKENS=$max_tokens LOGPROBS=$logprobs CONCURRENCY=$conc TIMEOUT=$timeout \
      "${cmd[@]}"
  done
done
