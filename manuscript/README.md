# Manuscript: "Where LLM Critics Draw the Line, and What Moves It: An Ideal-Observer Audit"

Full rewrite of 2026-11-11, with the rate-wording results added the same afternoon, for the AAAI-27 workshop "Effective and Efficient Evaluation for AI Scientists" (full papers 6–8 pages excluding references, double-blind, AAAI-27 two-column kit, OpenReview; due Nov 20, 2026, 06:00 UTC, which is Friday Nov 20 at 1:00 am New York time). The first draft (2026-11-10) is kept unchanged in `archive/2026-11-10_first_draft/`, and the rewrite as it stood before the rate-wording results in `archive/2026-11-11_before_rate_wording/`.

| file | what |
|---|---|
| `main.tex` | the paper (one file; the AAAI kit forbids `\input`) |
| `main.pdf` | the compiled paper, 15 pages |
| `refs.bib` | 71 entries, 68 cited; the 50 arXiv ones were generated from the arXiv API on 2026-11-10 |
| `aaai2027.sty`, `aaai2027.bst` | from the official AAAI-27 kit (`AuthorKit27.zip`, aaai.org/authorkit27, sha256 9406a545…780c960). Do not modify |
| `build.sh` | builds `main.pdf`; intermediate files go to `build/` (git-ignored) |
| `figures/make_figures.py` | rebuilds all seven figures and prints every number quoted in the text and tables |
| `figures/*.pdf` | the figures (fonts embedded, no Type 3); the `.png` copies are for a quick look |

## Corrections from the results freeze, applied 2026-11-12

Source: `results/freeze_2026-11-12/` (`claim_tests.csv`, `wording_tests.csv`, `validation.json`), which re-tests the preregistered contrasts with an exact within-item randomization test and the wording comparisons with a studentized problem-cluster bootstrap. Point estimates are unchanged; the freeze's whole-problem intervals differ from the paper's item-bootstrap intervals by at most 0.01, so the paper keeps the latter. `make_figures.py --only numbers` now prints the freeze outcomes used below at the end of its output.

| where | what changed |
|---|---|
| Table 4 and Section 4.3 | GPT-6.1 Sol holds **4 of 9** contrasts (T2, T3, T8, T9), not 7 of 9. T1, T5 and T6 are the same six verdicts moving one way (exact Holm p = .16); their marks are now "not shown" and the text says so. T7's zero-width interval is explained in the caption |
| Table 1 caption | marks come from the exact test; "all such p ≤ .002" became "p ≤ .01" (largest Holm p among held tests is .0095) |
| Section 4.5 and Appendix E, W2 | **one** wording comparison differs (Qwen3.5-4B off, audit wording, Holm p = .006), not three; Appendix E names the two next-largest (Qwen3.5-4B off user message, p = .12; Qwen3.5-27B on audit wording, p = .17) as not surviving correction; 30 comparisons are descriptive only (fewer than 20 problems changed). The "no difference within ±0.15" count is no longer stated: the freeze does not carry equivalence claims forward (the descriptive intervals lie within ±0.15 in 28 of 60; `make_figures.py --only numbers` prints it) |
| Method, "Inference" | names the exact test and gives the simulated coverage of ρ's intervals (95% at d′ 1.5, 91% at 3.2, 80% at 4.5, where the mean estimate is 0.35 for a true 0.5): ρ is biased toward zero near ceiling. The whole-problem resampling note (nine hard-set problems contribute two solutions; intervals move by at most 0.01) did not fit and is recorded here instead |
| Section 4.5 | the ceiling bias is named where the drop/flip variants are discussed |

**Page budget.** The corrections added about four lines and the body had no slack (the note below about seven spare lines was stale: the 2026-11-11 build ended at the foot of page 8). To stay within eight pages these were trimmed, none of them a finding: the one-line pointer to Section 4.5 at the end of Section 4.1; the Appendix C pointer, folded into the preceding parenthesis; the Table 1 caption's list of line names (the rows and Appendix A carry them); one sentence each from the Figure 2 and Figure 3 captions that restated the text ("Reasoning raises d′ ..."; "Critics stay near 50% ..."); and, in the Discussion and Limitations, the "audit is cheap" item, the first two sentences and the clause "reasoning settings are not commensurable across vendors" (already in "Compute and budgets") compressed. The build after the corrections is 14 pages with the body ending at the foot of page 8 and no spare lines, so the audit results will still need a cut elsewhere (shorten Related Work, or move Table 1 to the appendix).

The historical plans in `prereg/` keep the legacy bootstrap outcomes (7 of 9, 3 of 60) as a record of what was first reported.

## Attribution, instruction and experience results, added 2026-11-13

Source: `prereg/rate_use_followup.md` (Results) and `results/followup/analysis/`. `make_figures.py --only numbers` prints every number used (block "rate-use follow-up"). The manuscript as it stood before these changes is in `archive/2026-11-13_before_followup/` (it is also the text the paper arm's blocks were built from).

| where | what changed |
|---|---|
| Abstract | "restating the rate five other ways changed little" now also names spelling out how to use the rate and showing it in audited examples |
| Section 4.1, "Attention" | the spelled-out Bayesian rule: nine critic runs changed ρ by −0.18 to +0.11, no interval above 0; reported posteriors moved by at most 1.1 log-odds for an 81-fold change in the odds |
| Section 4.1, new item "Trust" | the rate shown in ten audited verdicts was used no more than the told rate (differences −0.41 to 0.00; Opus's interval below 0); d′ unchanged |
| Section 4.3, "It can be discounted" | the bare note without the reliability declaration: 24 vs 89 false alarms (Opus), 28 vs 100 (GPT-6.1 Sol), 52 vs 47 (Qwen3.5-27B) |
| Method, "Preregistration" | the follow-up added to the list of plans |
| Discussion, "What critics do with context" | the Estes analogy now says it only half fits: a shown rate was used no better than a told one |
| Discussion, new paragraph "A critic handed this paper" | the exploratory paper arm (Opus): ρ 0.29 → 0.05 with the manuscript in the prompt; 0.08 Method only, 0.07 with the statements that the rate is false, 0.21 about "Model M"; the after-the-fact limit that every version states the item composition |
| Discussion, "Compute and budgets" | about 253,000 replies; API fees US$103 and US$12 |
| Limitations | the normative-premise paragraph now cites the two checks: told how, and shown, the critics used the rate no more |
| Appendix E | **Table 1 moved here** from Section 4.3 (its caption points back to Section 4.3; the text's references to it are unchanged) |
| Appendix F (new) | "Attribution, Instruction and Experience": the three families, the paper arm's four ρ values, the label variants and the 2% rule; a two-column table of ρ told / rule / shown and Δd′ for the nine runs |

**Page budget.** The additions came to about 21 lines of one column and moving Table 1 freed about the same, but the body still ran 17 lines onto page 9, so these were trimmed, none of them a finding: the new Discussion paragraph and the Section 4.3 addition compressed; in Related Work, the sentence likening critics to an observer told rather than shown the rate (no longer accurate), the three-element description of the claim test, the Lijo et al. comparison and the ProcessBench sentence shortened; "Nor is it uniform conservatism" and "This is why we add the own-confidence benchmark" dropped; the human-payoffs sentence in "Payoffs do even less" dropped (Related Work says the same); the two tone sentences merged; "The audit is cheap" and "Compute and budgets" compressed; the Figure 4 caption's two explanatory sentences shortened; and the Introduction's description of the third contribution shortened to pay for the abstract clause. The build is 15 pages with the body ending at the foot of page 8 (no spare lines); Appendix F's table floats to page 15.

## Rate-wording results, added 2026-11-11

Source: `prereg/rate_wording.md` (Results) and `results/rate_wording/analysis/`. `make_figures.py --only numbers` prints every number used.

| where | what changed |
|---|---|
| Section 4.5, "How the rate is stated" | the pending marker is replaced by the results: under-use in all 72 critic-by-wording cells, no wording a remedy, the rate read as information, Opus replicated on new items |
| Section 4.3 | a new item on GPT-6.1 Sol and GPT-6 Luna (7 of 9 contrasts held; all 200 solutions flagged under the bare claim); "Numbers against claims" now compares rate and claim for Opus on the same items (0.71 against 0.99) and for GPT-6.1 Sol |
| Section 4.4 | **the subsection title changed** to "The Claim Moves the Decision, Not Always the Evidence", with a paragraph on GPT-6.1 Sol, whose stated probability stops discriminating under the claim (AUC 0.52) |
| Section 4.5, "Disputed labels" | one sentence: both OpenAI critics flag 13 of the 14 disputed held-out items |
| Abstract, Introduction, Method | the follow-up and the two OpenAI critics are mentioned; "three families" became four, the fourth on held-out items only |
| Discussion, Limitations | GPT-6.1 Sol added to the two profiles; the advice to threshold the stated probability now says to check it per critic; replies (about 224,000) and API cost (US$82 Claude, US$8 OpenAI) updated; placement is no longer untested |
| Appendix A | the four new wordings |
| Appendix D, Figure 6 | the grid has twelve rows (the two OpenAI critics added) and Haiku's and Opus's stated-rate cells are filled |
| Appendix E (new) | the five preregistered rules W1–W5, Figure 7 (ρ under the six statements) and Table 4 (the nine claim contrasts for GPT-6.1 Sol) |

Statements outside the preregistered plan are marked in the text: GPT-6.1 Sol's stated probability under the claim, and the count of disputed items the OpenAI critics flag.

## What changed from the first draft

- **Text.** Every section was rewritten: shorter paragraphs, fewer numbers in running prose (they moved into figures), and results stated as plain findings.
- **The table comparing this paper with Brown, Mazaheri and Quiroz is gone**, and so is the paragraph reporting the size of the literature search. What is new is now said where it comes up, in a clause or a sentence (see the map at the end).
- **Figures: seven instead of one.**

  | figure | shows | where |
  |---|---|---|
  | 1 | the signal-detection model, the ideal-observer curve c\*(p) with all 14 critics, and the same comparison in ROC space | page 2 |
  | 2 | d′, observed against ideal shift, ρ with intervals and relabelling ranges, and output tokens, per critic | page 5 |
  | 3 | effective probability of stated rates and of the claim (was Figure 1a); the preregistered claim test (was Figure 1b) | page 6 |
  | 4 | stated P(error) for correct and flawed solutions, with and without the claim, Opus and Qwen3.5-27B | page 7 |
  | 5 (Appendix C) | each critic against its own ideal-observer curve, with intervals | page 13 |
  | 6 (Appendix D) | false alarms for all twelve held-out critic runs and all lines | page 13 |
  | 7 (Appendix E) | ρ under six statements of the rate, twelve held-out critic runs, with the range over label readings | page 14 |

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
- **Last build (2026-11-11, with the rate-wording results).** 14 pages, no LaTeX warnings, no overfull lines.
- **Layout of that build.** Body: pages 1–8, ending about seven lines above the foot of page 8, so it is at the 8-page limit. References: pages 9–11. Appendix: pages 12–14.
- **Figures.** Rebuild with `.venv/bin/python manuscript/figures/make_figures.py` from the project root (`--only 1`, `2`, `3`, `4`, `A1`, `A2`, `A3` or `numbers` for one part). It reads only finished analyses and the saved replies, and never `audit/`. It stops if the criteria it recomputes from the replies differ from the saved analysis.
- **Colour.** Blue with a left-pointing triangle is "told 10%" and orange with a right-pointing triangle is "told 90%" in every figure; everything else is black or grey, and open markers mean reasoning off. The figures stay readable in greyscale.
- **Overleaf instead.** Upload `main.tex`, `refs.bib`, `aaai2027.sty`, `aaai2027.bst` and the seven `figures/*.pdf`, keeping the `figures/` folder. Set the compiler to pdfLaTeX.

## Before submission

1. **Rate-wording results.** Done on 2026-11-11 (see the section above).
2. **Label audit.** Replace the second `\pending{}` once blind judgments exist (`scripts/label_sensitivity.py --audit <csv>`). Until then the paper states ρ for reasoning-on critics as label-dependent.
3. **Length.** The body now ends about seven lines above the foot of page 8. The audit results will replace a three-line marker, so anything longer needs a cut elsewhere: shorten Related Work, or move Table 1 (the preregistered contrasts) to the appendix.
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
| Section 4.4 | The stated probability keeps its ranking under the claim for Opus, and loses it for GPT-6.1 Sol | AUC 0.983–0.991 against 0.992 (Opus); 0.52 against 0.92 (GPT-6.1 Sol); Figure 4 | Addendum P5: not reported elsewhere; contrary signs in Shah's poster and Rosenblum et al. |

**Kept out on purpose**

- "Threshold, not skill" as a finding. It is established, and the paper says it builds on it.
- Any "first" or "to our knowledge, no study in any task".
- "Confirmation bias" or "deference" for our critics. The preregistered test of unjustified deference was not met.
- Any size of ρ for reasoning-on critics beyond "label-dependent".
- Any general claim that the stated probability survives a claim. It does for Opus and not for GPT-6.1 Sol.

**Points that run against the paper.** It discusses each of them:

- Frontier models use stated costs and counts in other tasks (Yamin; Servajean; Lijo; Yang).
- A declared-inaccurate source is still followed (Guo et al.).
- Brown et al.'s source ordering is the reverse of Opus's.
- The open models treat a bare claim about like a stated 90% chance. Only the strongest wording beats every number for them.
- GPT-6.1 Sol's stated probability is 99 or 100 for every solution under the bare claim, so the "decision, not evidence" finding is Opus's alone.
- For GPT-6.1 Sol the claim effect nearly disappears when "Check it carefully." follows the claim, so the effect depends on the exact sentence.
