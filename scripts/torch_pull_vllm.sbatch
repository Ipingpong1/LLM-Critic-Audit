#!/bin/bash
#SBATCH --job-name=pull-vllm
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=01:30:00
#SBATCH --output=logs/%x-%j.out
# Build the vLLM Apptainer image on a compute node (submitted by scripts/torch_setup.sh).
# On a Torch login node the squashfs step gets killed, and on /scratch unpacking fails
# (its NFS ACLs reject xattr changes), so this builds on the node's local disk.
set -euo pipefail
SIF=${VLLM_SIF:-/scratch/$USER/images/vllm-openai_v0.32.0.sif}
export APPTAINER_CACHEDIR=/scratch/$USER/.apptainer-cache
export APPTAINER_TMPDIR=${TMPDIR:-/tmp}/$USER-apptainer
mkdir -p "$APPTAINER_TMPDIR" "$(dirname "$SIF")"
apptainer pull --force "$SIF" docker://vllm/vllm-openai:v0.32.0
rm -rf "$APPTAINER_TMPDIR"
ls -la "$SIF"
