# Code and item sets: "Where LLM Critics Draw the Line, and What Moves It"

Anonymized source for the paper. Raw model replies are not in this folder: they are distributed as a companion archive (`critic-responses.tar.gz`) whose files are listed, with checksums, in `data/RESPONSE_FILES.sha256`. Restore the archive at this folder's root, then:

```sh
python3 scripts/release_data.py verify          # checks every reply file against the manifest
uv sync --locked
uv run python manuscript/figures/make_figures.py --only numbers   # prints every number quoted in the paper
uv run python -m unittest discover -s tests -v
```

None of these makes a model call.

| folder | contents |
|---|---|
| `pilot/` | item sampling from ProcessBench (`data.py`), prompts and conditions (`prompts.py`), the runner for OpenAI-compatible, Anthropic and OpenAI endpoints (`run.py`), signal-detection analysis with item bootstrap (`analyze.py`), the exact and studentized tests of the results freeze (`inference.py`, `thresholds.py`), and a simulated critic (`simulate.py`) |
| `scripts/` | stage-specific analyses and figures, the collection wrappers for the API runs and the Slurm cluster, the label re-analysis, the results freeze, and data packaging |
| `tests/` | unit tests for the freeze inference, threshold policies and the audit receipt |
| `data/` | the sampled item sets (easy, hard, held-out, and the 40-item subsets) and the reply-file manifest |
| `audit/` | the blind label-audit sheet and its key; the key must be kept from auditors until they have finished |
| `manuscript/figures/make_figures.py`, `manuscript/build.sh` | figure generation from saved analyses, and the LaTeX build |

Saved analyses (`results/*/analysis/`, `results/label_sensitivity/`, `results/freeze_2026-11-12/`) are part of the companion archive together with the raw replies.

## New model runs

Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in the environment; the wrappers `scripts/with_key.sh` and `scripts/with_openai_key.sh` also accept a local credential-store entry. Every API run requires a spending cap (`--max-usd`). The cluster scripts (`scripts/torch_*.sh`, `scripts/*.sbatch`) are written for a Slurm cluster with L40S or H200 GPUs and an Apptainer image of vLLM; set `ACCOUNT` to your allocation and review the partition settings before submitting. Model revisions used for the paper are recorded in the plans (supplementary material) where known.

## Anonymization

Refreshed 2026-11-13 with the rate-use follow-up (`pilot/prompts.py`, `pilot/run.py`, `scripts/build_followup_blocks.py`, `scripts/followup.sh`, `scripts/followup_analysis.py`, `scripts/torch_submit.sh`, `data/condition_blocks/`, `data/examples_experienced.jsonl`, the figure script), with the same substitutions; the condition blocks are verbatim, since their hashes are recorded in the plan.

Relative to the working copy, only the cluster's name was replaced by "the cluster" in comments and figure labels, and a user-specific credential-entry name was made generic. File and directory names containing the cluster's name (`results/torch_hard/`, `scripts/torch_*.sh`) are unchanged.
