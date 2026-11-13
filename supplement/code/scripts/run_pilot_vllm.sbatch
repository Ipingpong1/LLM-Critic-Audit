#!/bin/bash
#SBATCH --job-name=critic-sdt-pilot
#SBATCH --gres=gpu:1
#SBATCH --constraint="l40s|h200"
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=03:00:00
#SBATCH --requeue
#SBATCH --open-mode=append
#SBATCH --output=logs/%x-%j.out
#
# Serve one open model with vLLM on a GPU node and run the pilot against it.
# Run from the project root, after downloading the weights on a login node
# (compute nodes often have no internet). On the HPC cluster, scripts/torch_submit.sh sets
# everything below and submits the whole study; this script also works on its own:
#
#   hf download Qwen/Qwen3.5-9B          # once, on the login node
#   MODEL=Qwen/Qwen3.5-9B LABEL=qwen3.5:9b-nothink-bf16 \
#     EXTRA_BODY='{"chat_template_kwargs": {"enable_thinking": false}}' sbatch --account=<account> scripts/run_pilot_vllm.sbatch
#
# Optional variables: CONDITIONS (default base_rate), SAMPLES (default 1), TEMPERATURE (default 0), LABEL (name in results),
# OUT (output JSONL), ITEMS (items JSONL; default data/items.jsonl), LIMIT (first N items, for smoke tests), MAX_TOKENS (default 1024),
# MAX_MODEL_LEN (default 20480), TIMEOUT (seconds per request, default 600), CONCURRENCY (default 64),
# LOGPROBS (default 1), EXTRA_BODY (JSON passed to every request, e.g. to turn thinking on or off),
# REASONING_PARSER (vLLM parser that splits thinking from the answer, e.g. qwen3), TP (GPUs per model),
# VLLM_SIF (Apptainer image of vllm/vllm-openai; empty = `vllm` on PATH),
# PYTHON (interpreter for the client; default `uv run python`), CACHE (where vLLM, Triton etc. cache).
# The #SBATCH lines are cluster defaults; sbatch command-line options override them.
# --requeue: if the job is preempted it restarts, and the runner skips finished trials.
set -euo pipefail

MODEL=${MODEL:?set MODEL, e.g. MODEL=Qwen/Qwen3.5-9B}
PORT=${PORT:-$((8000 + SLURM_JOB_ID % 1000))}
CONDITIONS=${CONDITIONS:-base_rate}
SAMPLES=${SAMPLES:-1}
EXTRA_BODY=${EXTRA_BODY:-}
VLLM_SIF=${VLLM_SIF:-}
TP=${TP:-1}
REASONING_PARSER=${REASONING_PARSER:-}
export HF_HOME=${HF_HOME:-${SCRATCH:-$HOME}/hf}
export HF_HUB_OFFLINE=1
# Keep every cache off $HOME, which has small quotas on most clusters.
CACHE=${CACHE:-${SCRATCH:-$HOME}/.cache}
export XDG_CACHE_HOME=$CACHE VLLM_CACHE_ROOT=$CACHE/vllm TRITON_CACHE_DIR=$CACHE/triton \
  TORCHINDUCTOR_CACHE_DIR=$CACHE/inductor FLASHINFER_WORKSPACE_BASE=$CACHE PIP_NO_CACHE_DIR=1 \
  VLLM_NO_USAGE_STATS=1 DO_NOT_TRACK=1

mkdir -p logs "$CACHE/home"
echo "$(date '+%F %T') job $SLURM_JOB_ID on $(hostname): $MODEL, label ${LABEL:-}, TP $TP, restart ${SLURM_RESTART_COUNT:-0}"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

if [ -n "$VLLM_SIF" ]; then
  # --home: the container gets a writable home on $CACHE instead of the real (quota-limited) one.
  SERVE=(apptainer exec --nv --home "$CACHE/home" --bind "$HF_HOME,$CACHE" "$VLLM_SIF" vllm serve)
else
  SERVE=(vllm serve)
fi
SERVE_ARGS=(--port "$PORT" --max-model-len "${MAX_MODEL_LEN:-20480}" --gpu-memory-utilization 0.90
            --tensor-parallel-size "$TP")
if [ -n "$REASONING_PARSER" ]; then SERVE_ARGS+=(--reasoning-parser "$REASONING_PARSER"); fi
"${SERVE[@]}" "$MODEL" "${SERVE_ARGS[@]}" >> "logs/vllm-$SLURM_JOB_ID.log" 2>&1 &
VLLM_PID=$!
trap 'kill $VLLM_PID 2>/dev/null || true' EXIT

echo "waiting for vLLM ($MODEL) on port $PORT ..."
for _ in $(seq 1 180); do
  if curl -sf "http://localhost:$PORT/health" > /dev/null; then break; fi
  if ! kill -0 "$VLLM_PID" 2>/dev/null; then echo "vLLM exited early; see logs/vllm-$SLURM_JOB_ID.log"; exit 1; fi
  sleep 10
done
echo "$(date '+%F %T') vLLM is up"

PY=(${PYTHON:-uv run python})
ARGS=(--model "$MODEL" --base-url "http://localhost:$PORT/v1" --conditions "$CONDITIONS"
      --samples "$SAMPLES" --temperature "${TEMPERATURE:-0}" --concurrency "${CONCURRENCY:-64}"
      --max-tokens "${MAX_TOKENS:-1024}" --timeout "${TIMEOUT:-600}")
if [ -n "${LABEL:-}" ]; then ARGS+=(--label "$LABEL"); fi
if [ -n "${OUT:-}" ]; then ARGS+=(--out "$OUT"); fi
if [ -n "${LIMIT:-}" ]; then ARGS+=(--limit "$LIMIT"); fi
if [ -n "${ITEMS:-}" ]; then ARGS+=(--items "$ITEMS"); fi
if [ -n "$EXTRA_BODY" ]; then ARGS+=(--extra-body "$EXTRA_BODY"); fi
# Verdict-token logprobs give the graded score for ROC curves.
if [ "${LOGPROBS:-1}" = "1" ]; then ARGS+=(--logprobs); fi
"${PY[@]}" -m pilot.run "${ARGS[@]}"
echo "$(date '+%F %T') done"
