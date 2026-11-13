# Release preparation

This directory is the development and release base assembled on 2026-11-11.
The migration preserves the scientific inputs, model replies, saved analyses,
analysis plans, and current manuscript. It does not implement the scientific
revisions identified in the manuscript review.

## What belongs in Git

Track source, dependency declarations and lockfile, sampled item sets, saved
analysis summaries and figures, manuscript sources and current PDF, analysis
plans, literature-search protocols/logs, and the response-data manifest.

Raw replies remain at their original paths for analysis, but are excluded from
Git. Supply the companion archive with the release. Downloaded literature and
original benchmark caches remain local; do not package the entire working
directory as a release.

## Verify and package response data

From the project root:

```sh
python3 scripts/release_data.py verify
python3 scripts/release_data.py pack
```

The second command creates `.local/releases/critic-responses.tar.gz` and refuses
to overwrite an existing archive. It packages only the sampled item sets, saved
JSONL files under `results/`, and `data/RESPONSE_FILES.sha256`. After obtaining a
source checkout and the matching companion archive, restore it at the root:

```sh
tar -xzf /path/to/critic-responses.tar.gz
python3 scripts/release_data.py verify
```

Archive hashes and the matching source commit should accompany an eventual
published release. No remote repository or download URL has been created yet.

## Reproduce the current manuscript's numerical report

```sh
uv sync --locked
uv run python manuscript/figures/make_figures.py --only numbers
```

This uses saved responses and saved analyses, and makes no inference calls.
It is a consistency check for the current paper, not a rerun of every bootstrap.
The historical research log and individual analysis plans document the full
analysis commands. To regenerate figures, run the same figure script without
`--only numbers`. To compile the manuscript, run `manuscript/build.sh` with
pdfLaTeX and BibTeX installed; build intermediates are ignored.

## Preserved provenance

`.local/provenance/` is intentionally excluded from Git. It contains the source
snapshot manifest, original modified files, the original untracked-file
manifest, source working-tree status/diff, and a verified Git bundle retaining
the old history. The source manifest records the exact files copied before
cleanup; subsequent edits are listed in `migration-report.json`.

The earlier prospective plans remain unchanged. Their dates and registration
status require the qualifications discussed in the review. The migrated
lockfile describes the reproduction environment; it does not reconstruct all
historical collection environments. Unknown model revisions remain unknown.

Existing credential-bearing HPC notes were preserved outside this project in
the private sibling directory `LLM-critics-private`. No credentials are needed
to verify the data or reproduce the numerical report.

## Remaining publication work

- Resolve the targeted human label audit and near-ceiling interpretations.
- Qualify the ideal-observer reference, reasoning, and reported-probability claims.
- Isolate attribution from reliability, or remove the causal remedy claim.
- Complete the planned statistical validation and final numerical reconciliation.
- Finalize model/environment provenance and preregistration wording.
- Select the code/data licensing and attribution appropriate for distribution.
- Prepare the anonymous manuscript and supplement; historical documents still
  include collection-environment details and are not an anonymized submission.
- Confirm appendix and disclosure rules, then inspect the final rendered PDF.

The recorded workshop deadline is 2026-11-20 06:00 UTC, which is Friday,
November 20 at 01:00 Eastern. The submission package should be finalized earlier.
