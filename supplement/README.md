# Supplementary material (anonymized copies, prepared 2026-11-12)

Anonymized copies of the documents the paper points to as "supplementary material". The originals in `prereg/`, `litsearch/` and `pilot/` are unchanged; regenerate this folder from them if they change.

| folder or file | contents | pointer in the paper |
|---|---|---|
| `plans/1_stage_b.md` … `6_rate_wording.md` | the six written plans, in the order they were fixed, each with its predictions, decision rules, deviations and recorded outcomes appended below the plan | Method, "Preregistration"; Section 4.5 |
| `plans/7_results_freeze_amendment.json` | the retrospective methodological amendment of 2026-11-12 (exact tests, studentized wording tests, audit rules); not a preregistration | Method, "Inference" |
| `literature_search/PROTOCOL.md` | the search protocol | Related Work, "Stated rates and costs" |
| `literature_search/query_log.csv`, `screening_log.csv` | every query (1,816 rows) and every kept paper (560 rows) | same |
| `literature_search/NOVELTY_REPORT.md` | the claim-by-claim novelty check of 2026-11-06 and its 2026-11-10 addendum | same |
| `prompts.py` | the system prompt, user template and every condition line, byte-for-byte as sent | Appendix A |
| `code/` | the anonymized source, item sets, audit sheet and tests, with its own README on verification and reproduction; the raw replies and saved analyses travel in the companion archive | Method; "Compute and budgets" |

## What was changed for anonymity

Only these substitutions were made; no number, date or outcome was altered.

- The institution's name was replaced by "the institution" or "the university library" (search protocol, two query-log rows, novelty report).
- The cluster's name was replaced by "the cluster" or "the HPC cluster" in prose. Directory and script names that contain it (`results/torch_hard/`, `scripts/torch_submit.sh`) are left as they are, since they are file paths in the code release.
- A credential-store entry name and the mention of a personal billing account were removed or made generic.

Left in on purpose: commit hashes and dates (they document when each plan was fixed, and the dated history will accompany the code release), cluster job numbers, API spend, and the statements that the AI assistant drafted plans and scripts. Those statements are the record behind the paper's AI-use disclosure and should match it.

## Before uploading

- `code/` carries the same substitutions (done 2026-11-12; see its README). Build the companion archive with `scripts/release_data.py pack` from the working copy and record its hash here.
- Check `screening_log.csv` once more by eye: author names in it are third-party authors, and repository links in the notes are theirs.
- Nothing in this folder names an author, an e-mail address, a local path or the repository.
