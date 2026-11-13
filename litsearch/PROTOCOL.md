# Literature search and novelty check: protocol

Set up Nov 6, 2026. Nothing below has been run yet. The search follows this protocol so it can be reported in the paper (PRISMA-style counts) and repeated before submission.

## Goal

Decide, before committing HPC time, whether each claim below is new, and which journals or venues fit. A claim counts as **covered** if any paper (peer-reviewed or preprint) reports the same manipulation and the same measurement on LLM critics, verifiers or judges. **Partly covered** means the same idea with a different measurement, domain or a single condition.

## Claims to test

| ID | Claim | Prior status (Nov 2 check) |
|---|---|---|
| C1 | A stated error base rate moves an LLM critic's criterion far less than the SDT ideal observer predicts (ρ ≪ 1), measured against c* = ln((1−p)/p)/d′ | No paper found |
| C2 | Telling the critic to use the base rate as a prior does not raise ρ | No paper found |
| C3 | Stated payoffs (numeric or verbal) don't move the criterion in the right direction; models react to the presence of a scoring rule, not its content | No paper found |
| C4 | One line of tone (harsh, lenient, presupposed error, persona) moves c as far as or further than the whole base-rate manipulation, and no framing changes d′ or AUC | Partly: "prompts move c, not d′" shown for other manipulations (2608.16003, 2609.18204, 2610.22631) |
| C5 | Within one model family, smaller models use the stated prior more | No paper found |
| C6 | Models state the right lean when asked but don't act on it (manipulation check vs behavior) | Not searched |
| C7 | ROC / z-ROC curves for critics from verdict-token logprobs | No paper found |
| C8 | (Planned) Thinking on vs off changes ρ or payoff use | Not searched |

## Databases (tab group "Claude" in Chrome)

| Source | Access | Covers | Notes |
|---|---|---|---|
| NYU Libraries search (Primo) | NYU sign-in | Journals, books, psych and cog-sci databases | Use for the human SDT background and journal-side coverage |
| Google Scholar | Open | Everything, incl. citations | Best for forward citations ("Cited by"). Optional: set Settings → Library links → NYU for full-text links |
| Semantic Scholar | Open | CS preprints, citation graph | Forward/backward citations; API was rate-limited last time, so use the website |
| arXiv advanced search | Open | Preprints (cs.CL, cs.AI, cs.LG, cs.HC, q-bio.NC) | Primary source: most close work is arXiv-only |
| OpenReview | Open | ICLR, NeurIPS, COLM, TMLR, workshops, incl. rejected and withdrawn papers | Search under-review submissions too |
| ACL Anthology | Open | ACL, EMNLP, NAACL, Findings, TACL, workshops | |
| Scopus | NYU (confirmed working) | Peer-reviewed journals and conferences, citation counts | Use for systematic counts and journal coverage |
| ACM Digital Library | NYU proxy (needs a consent click by you) | FAccT, CHI, CSCW, RecSys, SIGIR | |
| Web of Science | Failed to load through the NYU proxy on Nov 6 | | Optional; Scopus covers most of it |

Also outside the browser: DBLP for author lists of the closest groups; arXiv alerts (see the end of this file).

## Search strings

Three concept blocks. A hit must match block A and at least one of B or C.

- **A, the system:** (critic OR verifier OR "LLM judge" OR "LLM-as-a-judge" OR "process reward model" OR "self-correction" OR "self-critique" OR "error detection" OR reviewer OR overseer OR monitor) AND ("language model" OR LLM)
- **B, the measurement:** ("signal detection" OR "d-prime" OR "d'" OR sensitivity OR "response bias" OR "decision criterion" OR "decision threshold" OR "operating point" OR "false alarm" OR "false positive rate" OR ROC OR "base rate" OR prior OR payoff OR "asymmetric cost" OR "ideal observer" OR conservatism)
- **C, the manipulation:** (strict OR lenient OR harsh OR skeptical OR "devil's advocate" OR adversarial OR presuppos* OR persona OR stakes OR framing OR "prompt sensitivity" OR sycophan* OR "over-critical" OR "false rejection")

Per-database forms:

- **Scopus:** `TITLE-ABS-KEY((critic OR verifier OR "LLM judge" OR "LLM-as-a-judge" OR "process reward model" OR "self-correction" OR "error detection") AND ("language model" OR LLM) AND ("signal detection" OR "response bias" OR "decision criterion" OR "false alarm" OR "base rate" OR payoff OR "ideal observer" OR ROC)) AND PUBYEAR > 2021`
- **arXiv (abstract field, one query per pair):** run each B and C term with each of: critic, verifier, judge, "self-correction", "process reward". Keep the query log below.
- **Google Scholar:** short phrase queries, e.g. `"signal detection" "LLM judge"`, `"base rate" LLM verifier criterion`, `"lenient" "strict" LLM critic false alarm`, `"ideal observer" "language model"`. Read the first 50 results each.
- **OpenReview / ACL Anthology:** title and abstract search for "signal detection", "judge bias", "verifier calibration", "over-critical", "base rate".

Base-rate and payoff use by LLMs outside critics (for C1–C3 context): ("base rate neglect" OR "Bayesian updating" OR "prior" OR "expected value" OR "asymmetric payoff") AND (LLM OR "language model").

Human background (no date limit): SDT criterion placement under base rates and payoffs ("conservative criterion", "sluggish beta", "optimal criterion placement"). Find the canonical reviews and verify every citation before use.

## Date range and inclusion

- LLM work: Jan 2022 to the search date. Human SDT background: any date.
- Include: any paper that manipulates a critic's, verifier's or judge's prompt or context and reports both error types, or any SDT treatment of LLM judgments.
- Exclude: pure human-agreement judge benchmarks with no correct/flawed ground truth, unless they vary strictness or framing.
- Peer-reviewed and preprints both count for novelty.

## Snowballing

1. Backward: read the reference lists of every paper rated "close".
2. Forward: "Cited by" in Google Scholar and Semantic Scholar for the seed papers in `known_papers.csv` marked `seed`.
3. Authors: list other recent papers by the authors of the five closest papers (DBLP, Google Scholar profiles). The overseer-paper group (2609.18204) said criterion-calibration prompts were their next step.
4. Stop when a full round adds no new "close" paper.

## Screening

Two passes: title/abstract, then full text for anything rated "maybe" or above. Log every query in `query_log.csv` and every screened paper in `screening_log.csv` (relevance: close / related / background / exclude, plus which claims it touches). Final output: a claim-by-claim novelty table with the closest paper for each, and PRISMA-style counts.

## Journal and venue targets

Evaluate the candidates in `venues.csv` on scope fit, whether they publish this kind of empirical LLM-behavior work, review time, page limits, open-access cost, and 2027 deadlines. Check each venue's own pages; fill in only what was verified, with the date checked.

## Execution notes and deviations

- **Nov 6, 2026, search started.** It runs as parallel streams, each writing its own logs in `streams/` (shared rules in `streams/README.md`); the logs are merged into `query_log.csv` and `screening_log.csv` at the end.
- Open sources (arXiv, OpenReview, ACL Anthology, ACM and AAAI proceedings, Semantic Scholar, OpenAlex, DBLP, Crossref) are searched through their public APIs rather than the browser: same indexes, exact query strings logged, and faster. NYU-only sources (Scopus, NYU Libraries, PsycINFO) and Google Scholar run in the browser.
- Web of Science was unavailable (error page through the NYU proxy). PsycINFO through NYU was added to cover psychology journals.
- Google Scholar was skipped: it showed a CAPTCHA on the first query, and the author chose to skip it rather than clear it. Forward citations therefore rely on Semantic Scholar and OpenAlex (the `citations` stream); before submission, re-run "Cited by" for the closest papers in Google Scholar by hand.
- NYU Libraries (Primo) returned 1,380 mostly engineering hits for the first query; Scopus and PsycINFO stand in for its journal coverage.

| Stream | Covers |
|---|---|
| `arxiv` | arXiv API sweep of block A × (B or C), plus every judge/verifier/critic paper submitted Oct 15–Nov 6, 2026 |
| `peer` | OpenReview (incl. ICLR 2027 submissions and 2026 workshops), ACL Anthology, ACM, AAAI and other proceedings via Crossref, DBLP and OpenAlex |
| `citations` | Forward and backward citations of the seed papers and ProcessBench; other recent papers by the closest authors |
| `adjacent` | LLM base-rate and payoff use outside critics, model-size trends, says-vs-does gaps, thinking modes and verification, SDT of LLMs in psychology venues, and the human SDT background |
| `venues` | Journal and venue facts for `venues.csv` from each venue's own pages |
| `chrome` | Scopus, Google Scholar (incl. "Cited by"), NYU Libraries and PsycINFO, run in the browser by the main session |

## Ongoing alerts (set up after the search)

arXiv and Google Scholar alerts for "signal detection" or "decision criterion" combined with judge, verifier or critic, and for the authors of the closest papers.
