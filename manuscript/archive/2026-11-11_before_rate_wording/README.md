# Manuscript: "Told the Odds, Moved by a Claim: An Ideal-Observer Audit of LLM Critics"

Full rewrite of 2026-11-11, for the AAAI-27 workshop "Effective and Efficient Evaluation for AI Scientists" (full papers 6–8 pages excluding references, double-blind, AAAI-27 two-column kit, OpenReview; due Nov 20, 2026, 06:00 UTC, which is Thursday Nov 19 at 1:00 am New York time). The first draft (2026-11-10) is kept unchanged in `archive/2026-11-10_first_draft/`.

| file | what |
|---|---|
| `main.tex` | the paper (one file; the AAAI kit forbids `\input`) |
| `main.pdf` | the compiled paper, 13 pages |
| `refs.bib` | 71 entries, 68 cited; the 50 arXiv ones were generated from the arXiv API on 2026-11-10 |
| `aaai2027.sty`, `aaai2027.bst` | from the official AAAI-27 kit (`AuthorKit27.zip`, aaai.org/authorkit27, sha256 9406a545…780c960). Do not modify |
| `build.sh` | builds `main.pdf`; intermediate files go to `build/` (git-ignored) |
| `figures/make_figures.py` | rebuilds all six figures and prints every number quoted in the text and tables |
| `figures/*.pdf` | the figures (fonts embedded, no Type 3); the `.png` copies are for a quick look |

## What changed from the first draft

- **Text.** Every section was rewritten: shorter paragraphs, fewer numbers in running prose (they moved into figures), and results stated as plain findings.
- **The table comparing this paper with Brown, Mazaheri and Quiroz is gone**, and so is the paragraph reporting the size of the literature search. What is new is now said where it comes up, in a clause or a sentence (see the map at the end).
- **Figures: six instead of one.**

  | figure | shows | where |
  |---|---|---|
  | 1 | the signal-detection model, the ideal-observer curve c\*(p) with all 14 critics, and the same comparison in ROC space | page 2 |
  | 2 | d′, observed against ideal shift, ρ with intervals and relabelling ranges, and output tokens, per critic | page 5 |
  | 3 | effective probability of stated rates and of the claim (was Figure 1a); the preregistered claim test (was Figure 1b) | page 6 |
  | 4 | stated P(error) for correct and flawed solutions, with and without the claim, Opus and Qwen3.5-27B | page 7 |
  | 5 (Appendix C) | each critic against its own ideal-observer curve, with intervals | page 13 |
  | 6 (Appendix D) | false alarms for all ten held-out critic runs and all lines | page 13 |

- **The hard-set numbers table moved to Appendix B** (Table 2), because Figures 2 and 3a show the same values. Its rows are now grouped by model. The budget column the workshop asks for is panel (d) of Figure 2.
- **One analysis is new and post hoc**, and the text says so: a cut-off of 80 on Opus's stated probability, instead of its verdict, gives 10 false alarms and 98 hits per 100 under the bare claim (verdicts: 89 and 100). For Qwen3.5-27B no cut-off brings false alarms under that claim below 28. `make_figures.py --only numbers` prints both.
- **Two numbers are worded differently** after re-checking them against the saved analyses: the tone line reaches 80% of the whole 10%→90% shift in eight of 14 configurations (the first draft said "half"), and the own-confidence Bayesian moves "roughly 70–100%" as far as the equal-variance ideal (exact range 0.73–1.02; the first draft said 72–101%). Every other number is unchanged.
- **Two terms changed.** The "premise set" is now the "held-out set", and "thinking" is "reasoning" throughout.

## Is the ideal-observer curve new?

The curve c\*(p) = ln((1 − p)/p)/d′ is textbook signal-detection theory, and comparing observed with optimal criteria is standard in the human literature (the paper cites Green & Swets for it). For LLMs, `litsearch/NOVELTY_REPORT.md` (C1) and the stream notes record no paper that compares a model's criterion with c\* in any task, so no earlier paper can have plotted LLM behaviour against it. The closest are Lijo (checking effort against a break-even point, not a verdict criterion) and Servajean & Servajean (criterion shifts under a risk line, no optimum). The search has the gaps listed in the novelty report (no Google Scholar, abstract-only reads), so repeat the check before submitting.

## Build

```bash
manuscript/build.sh
```

- **Engine.** `aaai2027.sty` requires pdfLaTeX and stops under XeLaTeX, LuaLaTeX or Tectonic. `build.sh` uses `pdflatex` from your PATH, or else TinyTeX in `~/Library/TinyTeX`.
- **Last build (2026-11-11).** 13 pages, no LaTeX warnings, no overfull lines, no Type 3 fonts.
- **Layout of that build.** Body: pages 1–8, about 7.7 pages (References begin partway down the right column of page 8). References: pages 8–10. Appendix: pages 11–13.
- **Figures.** Rebuild with `.venv/bin/python manuscript/figures/make_figures.py` from the project root (`--only 1`, `2`, `3`, `4`, `A1`, `A2` or `numbers` for one part). It reads only finished analyses and the saved replies, never `results/rate_wording/` and never `audit/`. It stops if the criteria it recomputes from the replies differ from the saved analysis.
- **Colour.** Blue with a left-pointing triangle is "told 10%" and orange with a right-pointing triangle is "told 90%" in every figure; everything else is black or grey, and open markers mean reasoning off. The figures stay readable in greyscale.
- **Overleaf instead.** Upload `main.tex`, `refs.bib`, `aaai2027.sty`, `aaai2027.bst` and the six `figures/*.pdf`, keeping the `figures/` folder. Set the compiler to pdfLaTeX.

## Before submission

1. **Rate-wording results.** Replace the `\pending{}` paragraph in "How the rate is stated" once `scripts/rate_wording_analysis.py` has run (after the last Torch job, about 13:00 on Nov 11). If the claim effect holds on GPT-6.1 Sol (rule W5), add OpenAI to the abstract and change the family count ("three families" appears in the introduction and the limitations). Add the run's replies and cost to "Compute and budgets".
2. **Label audit.** Replace the second `\pending{}` once blind judgments exist (`scripts/label_sensitivity.py --audit <csv>`). Until then the paper states ρ for reasoning-on critics as label-dependent.
3. **Length.** The body has about a third of a page to spare under the 8-page limit. If the rate-wording paragraph needs a table, shorten Related Work or move Table 1 (the preregistered contrasts) to the appendix.
4. **Check the workshop's rules:** whether an appendix may follow the references or must go to supplementary material, any abstract word limit, and the policy on AI-assisted writing. If no appendix is allowed, Table 2 (exact hard-set values) and Figures 5–6 go to the supplement, and the text's pointers to Appendices A–D need changing.
5. **Supplementary material** (cited in the text): the plans in `prereg/`, `litsearch/PROTOCOL.md` with the query and screening logs, prompts, and code. Anonymize first: no names, no repository history, no cluster name.
6. **Search for new papers** in the week before submitting. The area moves fast: five of the close papers appeared in the two weeks before Nov 6.

## Where the paper says what is new

Each statement is one clause or sentence in the running text.

| where | what it says | evidence | closest prior work |
|---|---|---|---|
| Introduction, third paragraph | Earlier studies measure how far a judge moves and leave open how far it should | ρ for 14 configurations (Figure 2c, Table 2) | Quiroz; Mazaheri & Mazaheri; Brown et al. |
| Related Work, "Stated rates and costs" | "we know of no study that scores [a verdict threshold] against the ideal observer's; a structured literature search found none" | `litsearch/NOVELTY_REPORT.md`, C1 | Gupta et al. and Li & Rui (under-use, no ideal observer); Lijo (checking effort against a break-even point) |
| Related Work, end of "Context moves thresholds" | The claim test combines hit and false-alarm rates on held-out items, control lines with no claim in them, and a claim declared random | Table 1, `prereg/premise.md` | Brown et al.: their check cues still report a flag, they use a generic guard line, and they report flips |
| Introduction, last paragraph | Numbers, tone and a claim on one scale and the same critics | Figure 3a | Novelty report C4 and addendum P4 |
| Section 4.4 | The stated probability keeps its ranking under the claim (Opus) | AUC 0.983–0.991 against 0.992; Figure 4 | Addendum P5: not reported elsewhere; contrary signs in Shah's poster and Rosenblum et al. |

**Kept out on purpose**

- "Threshold, not skill" as a finding. It is established, and the paper says it builds on it.
- Any "first" or "to our knowledge, no study in any task".
- "Confirmation bias" or "deference" for our critics. The preregistered test of unjustified deference was not met.
- Any size of ρ for reasoning-on critics beyond "label-dependent".
- Any claim about OpenAI critics before the rate-wording analysis.

**Points that run against the paper.** It discusses each of them:

- Frontier models use stated costs and counts in other tasks (Yamin; Servajean; Lijo; Yang).
- A declared-inaccurate source is still followed (Guo et al.).
- Brown et al.'s source ordering is the reverse of Opus's.
- The open models treat a bare claim about like a stated 90% chance. Only the strongest wording beats every number for them.
