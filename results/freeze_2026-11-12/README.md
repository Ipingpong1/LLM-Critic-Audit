# Saved-response freeze — 2026-11-12

Status: Saved-response freeze conditional on original labels. Human audit: pending.
This directory supports a human-authored manuscript; it contains technical evidence, not replacement manuscript prose.

## Entry points

- `claim_ledger.json`: usable conclusions and mandatory limits.
- `arms.csv`, `conditions.csv`: publication-number ledger, label variant and ceiling flag on every row. H/F in the original fields use the historical correction; `raw_hit_rate` / `raw_fa_rate` are observed fractions.
- `claim_tests.csv`: corrected exact/randomization tests; Holm families 18 and 9. Original-label predicted-direction support: 16/18 and 4/9.
- `wording_tests.csv`: studentized interaction tests, 60-slot Holm family per labeling. Sparse/degenerate cases are descriptive and keep p=1 in the family. rho intervals are descriptive.
- `threshold_policies.csv`: five-fold problem-held-out risk, matched reply coverage, selected thresholds and full-refit bootstrap intervals. These are retrospective analyses, not fresh confirmatory experiments.
- `reasoning_contrasts.csv`: paired changes in d-prime, observed criterion shift, and rho.
- `hard.json`, `premise.json`, `easy.json`: full numerical results, missing-verdict sensitivities, all contested-label assignments, fixed folds and detailed test provenance.
- `reconciliation.json`: old/new point-estimate agreement and corrected claim inference.
- `validation.json`: finite simulation checks, including rho undercoverage near ceiling; not a proof of calibration.
- `figures/`: PNG and editable SVG figures generated solely from these results.
- `manifest.json`: input/source/output checksums and runtime settings; written last. A directory without it is incomplete.

## Interpretation and pending work

Original, drop, flip and damaged-text exclusions are sensitivity variants, not estimates of correct labels. Drop/flip were selected using model disagreements. A completed human audit must be archived using `scripts/check_audit.py` and supplied as `--audit-receipt` to a NEW output directory. Report both gap readings and explicit uncertainty. Never replace this version in place. Two reviewers require separate first-pass files and a separate adjudication record.

Bootstrap intervals are descriptive and are not inversions of the randomization tests. Whole problems are resampled within split and exact label-composition strata, with paired conditions and common critic resamples; singleton strata contribute no resampling uncertainty. No latent-evidence, internal-belief, universal reasoning, or isolated attribution/reliability causal claim is supported by these calculations alone.

Raw outputs and manuscript files are untouched. No new model calls were made. Source baseline: `.local/results-freeze-baseline-2026-11-12/`. Historical scripts remain legacy paths; use this freeze's CSV/JSON for revised inference.

## Reproduction

Use the same environment in `uv.lock`, then run `scripts/validate_freeze.py --simulations 500 --bootstrap 999 --out <validation.json>` and `scripts/freeze_results.py --validation <validation.json> --out-dir <new-directory>`. Defaults match this run unless the manifest settings say otherwise. Run `python -m unittest discover -s tests -v` first. Hashes establish integrity of these saved inputs, not provider revision identity or experimental randomization.

## Final packaging and checks

`source_snapshot.tar.gz` contains the exact analysis sources and small inputs named in the numerical manifest, plus this packaging script and the pre-packaging manifest. Raw responses remain in the repository and are covered by the 97-file checksum manifest. Reproduce the numerical run first, then run `scripts/package_freeze.py <new-directory>` for this final presentation.

The threshold figure includes the best constant-verdict baseline. At 10% error prevalence, Qwen-27B and Sol choose the all-correct policy under the bare claim: zero hits and zero false alarms. Their low weighted risk at that prevalence is not evidence of recovered error detection. All corresponding hit/false-alarm rates are in `threshold_policies.csv`.

`claim_ledger.json` also records the support counts and wording-test eligibility for every label variant. The retained revised wording inference does not establish equivalence for non-significant or sparse comparisons.
