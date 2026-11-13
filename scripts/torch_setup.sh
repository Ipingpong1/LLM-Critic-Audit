#!/bin/bash
# One-time setup on an NYU Torch login node, from the project root (keep the project on /scratch:
# $HOME has a 30k-file quota). Creates .venv, downloads the four models into $HF_HOME (~10 min)
# and submits a CPU job that builds the vLLM image (~10 min once it starts).
# Safe to rerun: downloads resume and finished steps are skipped. ACCOUNT sets the Slurm account.
set -euo pipefail
cd "$(dirname "$0")/.."
: "${ACCOUNT:?Set ACCOUNT to your Slurm allocation before setting up cluster jobs}"

export HF_HOME=${HF_HOME:-/scratch/$USER/.huggingface}
SIF=${VLLM_SIF:-/scratch/$USER/images/vllm-openai_v0.32.0.sif}
mkdir -p "$HF_HOME" logs

if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
  .venv/bin/pip install --no-cache-dir -q --upgrade pip
  .venv/bin/pip install --no-cache-dir -q "huggingface_hub>=0.34" "openai>=1.50" "numpy>=1.26" "scipy>=1.11" "matplotlib>=3.8"
fi

for m in Qwen/Qwen3.5-4B Qwen/Qwen3.5-9B google/gemma-4-12B-it Qwen/Qwen3.5-27B; do
  echo "$(date +%T) downloading $m"
  .venv/bin/hf download "$m" --max-workers 8 > /dev/null
done

if [ ! -f "$SIF" ]; then
  echo "submitting the image build: job $(VLLM_SIF=$SIF sbatch --parsable --account="$ACCOUNT" scripts/torch_pull_vllm.sbatch)"
fi
echo "$(date +%T) setup done (check the image with: ls -la $SIF)"
