# Supplementary material (anonymized copies, prepared 2026-11-12, plan 8 added 2026-11-13)

Anonymized copies of the documents the paper points to as "supplementary material". The originals in `prereg/`, `litsearch/` and `pilot/` are unchanged; regenerate this folder from them if they change.

| folder or file | contents | pointer in the paper |
|---|---|---|
| `plans/1_stage_b.md` … `6_rate_wording.md` | the six written plans, in the order they were fixed, each with its predictions, decision rules, deviations and recorded outcomes appended below the plan | Method, "Preregistration"; Section 4.5 |
| `plans/7_results_freeze_amendment.json` | the retrospective methodological amendment of 2026-11-12 (exact tests, studentized wording tests, audit rules); not a preregistration | Method, "Inference" |
| `plans/8_rate_use_followup.md` | the seventh plan (attribution, instruction, experience, and the exploratory paper arm), approved 2026-11-13 before any code or data, with its run log, deviations and recorded outcomes | Section 4.1 (Attention, Trust), Section 4.3, Discussion, Limitations, Appendix F |
| `literature_search/PROTOCOL.md` | the search protocol | Related Work, "Stated rates and costs" |
| `literature_search/query_log.csv`, `screening_log.csv` | every query (1,816 rows) and every kept paper (560 rows) | same |
| `literature_search/NOVELTY_REPORT.md` | the claim-by-claim novelty check of 2026-11-06 and its 2026-11-10 addendum | same |
| `prompts.py` | the system prompt, user template and every condition line, byte-for-byte as sent | Appendix A |
| `code/` | the anonymized source, item sets, audit sheet and tests, with its own README on verification and reproduction; the raw replies and saved analyses travel in the companion archive | Method; "Compute and budgets" |

## What was changed for anonymity

Only these substitutions were made; no number, date or outcome was altered.

- The institution's name was replaced by "the institution" or "the university library" (search protocol, two query-log rows, novelty report).
- The cluster's name was replaced by "the cluster" or "the HPC cluster" in prose, and the name of its allocation by "the cluster's allocation" (plan 8). Directory and script names that contain it (`results/torch_hard/`, `scripts/torch_submit.sh`) are left as they are, since they are file paths in the code release.
- A credential-store entry name and the mention of a personal billing account were removed or made generic.

Left in on purpose: commit hashes and dates (they document when each plan was fixed, and the dated history will accompany the code release), cluster job numbers, API spend, and the statements that the AI assistant drafted plans and scripts. Those statements are the record behind the paper's AI-use disclosure and should match it.

## Before uploading

- `code/` carries the same substitutions (done 2026-11-12; see its README). The companion archive was built with `scripts/release_data.py pack --output .local/releases/critic-responses-2026-11-13.tar.gz` on 2026-11-13 after the rate-use follow-up: 372,249,988 bytes, the 114 files listed in `data/RESPONSE_FILES.sha256`, SHA-256 `6812b198c351db210449d1c337398061e652640ad7c161c5bdb3939c13ec4d38` (the archive of 2026-11-11, 353,504,704 bytes, predates the follow-up). Rebuild it and update this line if any listed file changes.
- Check `screening_log.csv` once more by eye: author names in it are third-party authors, and repository links in the notes are theirs.
- Nothing in this folder names an author, an e-mail address, a local path or the repository.
