# LLM critics: context, decisions, and signal detection

Research code and saved experiments for **Where LLM Critics Draw the Line, and What Moves It**.
The project compares mathematical critics' responses to stated error rates,
error costs, tone, and assertions using ProcessBench solution labels and
signal-detection analyses.

This is the release-base copy of the research project as of **2026-11-11**.
The current manuscript and results are preserved; the scientific revisions
from the pre-submission review remain outstanding. The ideal-observer
comparison is conditional on its assumptions, and some magnitudes depend on
the pending targeted label audit.

## Start here

- [Current manuscript](manuscript/main.pdf) and [manuscript/build notes](manuscript/README.md)
- [Historical research log](RESEARCH_HISTORY.md): full experiment chronology,
  tables, caveats, commands, and collection details
- [Release preparation](RELEASE.md): data archive, provenance, reproduction, and
  remaining publication work
- [Analysis plans](prereg/): the original plans and appended results

## Verify the saved data and numerical report

Run from this directory:

```sh
python3 scripts/release_data.py verify
uv sync --locked
uv run python manuscript/figures/make_figures.py --only numbers
```

These commands do not make model calls. The local copy contains every saved
response. A future Git checkout will also need the matching companion data
archive described in [RELEASE.md](RELEASE.md); large response files are excluded
from ordinary Git commits. The manifest identifies the exact item and response
files used by this snapshot.

## Project layout

| Directory | Contents |
|---|---|
| `pilot/` | Item preparation, prompts, inference runner, simulation, SDT analysis |
| `scripts/` | Stage-specific analyses, figures, collection wrappers, data packaging |
| `data/` | Sampled item sets and the response-file checksum manifest |
| `results/` | Raw replies, saved analyses, and figures across all experiment stages |
| `prereg/` | Prospective written plans, deviations, and recorded outcomes |
| `audit/` | Blind audit sheet and separate identifying key; keep the key from auditors |
| `manuscript/` | Current paper, figure source, author-kit files, and earlier drafts |
| `litsearch/` | Literature search protocols, screening/query logs, and local caches |
| `.local/` | Private migration provenance, original history, and built data archives |

## New model runs

Saved-data analysis needs no API keys. For new hosted runs, provide
`ANTHROPIC_API_KEY` or `OPENAI_API_KEY` through the environment; the existing
wrappers also support macOS Keychain fallback. Do not store keys in this project.
The historical run scripts retain their spending caps and settings.

The Slurm scripts are templates for the original cluster configuration. Set
`ACCOUNT` to your allocation, review GPU/partition/container settings, and record
exact model revisions before starting new jobs. No cluster or API jobs are
launched by the verification or packaging commands above.

## Manuscript build

```sh
uv run python manuscript/figures/make_figures.py
manuscript/build.sh
```

Figure regeneration uses saved data. PDF compilation additionally requires
pdfLaTeX and BibTeX. The included PDF can be read without either.

The legacy `summary_mobile.html` is an early pilot summary, not the current paper.
