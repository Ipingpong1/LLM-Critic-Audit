# Manuscript: "Told the Odds, Moved by a Claim: An Ideal-Observer Audit of LLM Critics"

First draft, 2026-11-10, for the AAAI-27 workshop "Effective and Efficient Evaluation for AI Scientists" (full papers 6–8 pages excluding references, double-blind, AAAI-27 two-column kit, OpenReview; due Nov 20, 2026, 06:00 UTC, which is Thursday Nov 19 at 1:00 am New York time).

| file | what |
|---|---|
| `main.tex` | the paper (one file; the AAAI kit forbids `\input`) |
| `main.pdf` | the compiled paper, 10 pages |
| `refs.bib` | 71 entries; the 50 arXiv ones were generated from the arXiv API on 2026-11-10 |
| `aaai2027.sty`, `aaai2027.bst` | from the official AAAI-27 kit (`AuthorKit27.zip`, aaai.org/authorkit27, sha256 9406a545…780c960). Do not modify |
| `build.sh` | builds `main.pdf`; intermediate files go to `build/` (git-ignored) |
| `figures/make_figures.py` | rebuilds Figure 1 and prints the numbers in Tables 2–3 from saved results |
| `figures/fig_numbers_vs_claims.pdf` | Figure 1 (fonts embedded, no Type 3) |

## Build

```bash
manuscript/build.sh
```

- **Engine.** `aaai2027.sty` requires pdfLaTeX and stops under XeLaTeX, LuaLaTeX or Tectonic. `build.sh` uses `pdflatex` from your PATH, or else TinyTeX.
- **TinyTeX.** It lives in `~/Library/TinyTeX` (installed 2026-11-10, TeX Live 2026, about 250 MB, no admin rights). Packages added with `tlmgr`: newtx, fontaxes, placeins, caption, xstring, kastrup, courier, xpatch, carlisle, tex-gyre.
- **Last build (2026-11-10).** 10 pages, no LaTeX warnings, no overfull lines, all fonts Type 1.
- **Layout of that build.**
  - Body: pages 1–7 (about 6.6 pages; References begin partway down page 7).
  - Figure 1: top of page 2. Table 2: page 5. Table 3: page 6.
  - Appendix: page 10.
- **Overleaf instead.** Upload `main.tex`, `refs.bib`, `aaai2027.sty`, `aaai2027.bst` and `figures/fig_numbers_vs_claims.pdf`, keeping the `figures/` folder. Set the compiler to pdfLaTeX.
- **Figure.** Rebuild it with `.venv/bin/python manuscript/figures/make_figures.py` from the project root. It reads only finished analyses and never `results/rate_wording/`.

## Before submission

1. **Rate-wording results.** Replace the `\pending{}` paragraph in "How the rate is stated" once `scripts/rate_wording_analysis.py` has run (after the last Torch job, about 13:00 on Nov 11). Rules W1–W5 decide the wording: whether under-use holds in every wording, whether any wording helps, and whether the claim effect holds in a fourth family (GPT-6.1 Sol). If W5 holds, add OpenAI to the abstract and the family count ("three" appears in the intro, the contributions and the limitations).
2. **Label audit.** Replace the second `\pending{}` once blind judgments exist (`scripts/label_sensitivity.py --audit <csv>`). Until then the paper states ρ sizes for reasoning-on critics as label-dependent.
3. **Length.** The body runs about 6.6 pages; the limit is 6–8, references excluded. Filling in the rate-wording results (perhaps with a small table) leaves room to spare. Rebuild and check where "References" starts.
4. **Check the workshop's rules:** whether the appendix may follow the references or must go to supplementary material, any abstract word limit, and the policy on AI-assisted writing.
5. **Supplementary material** (cited in the text): the plans in `prereg/`, `litsearch/PROTOCOL.md` with the query and screening logs, prompts, and code. Anonymize first: no names, no repository history, no cluster name.
6. **Search for new papers** in the week before submitting. The area moves fast: five of the close papers appeared in the two weeks before Nov 6.

## Novelty claims and where they rest

| claim in the paper | evidence | closest prior work, and the difference |
|---|---|---|
| No earlier study, in any task, scores an LLM's threshold shift under a stated base rate against the ideal observer | ρ for 14 configurations, Table 1; search: `litsearch/NOVELTY_REPORT.md`, C1 | Gupta et al. 2025 and Li & Rui 2024 show under-use of stated priors with no ideal observer. Lijo 2026 compares checking *effort* with a break-even point, not a verdict threshold |
| First same-critic, same-scale comparison of numbers (base rate, item chance, payoffs) with tone and a claim | Table 1, Figure 1a; held-out comparison in "Numbers versus claims" | Novelty report C4 and addendum P4: no paper puts a stated rate and an assertion on one critic or one scale |
| Claim test with no-claim scrutiny and possibility controls, an assertion declared uninformative, and the opposite claim | Table 2; `prereg/premise.md` | Brown et al. 2026 (closest; read in full): assertion outweighs a directed check, but their check cues still report a flag, they use a generic guard line rather than an uninformative note, and they report flips rather than hit and false-alarm rates |
| The stated probability keeps its AUC under the claim (Opus) | AUC 0.983–0.991 vs 0.992; `results/label_sensitivity/report.md` | Addendum P5: not reported anywhere. Contrary signs: Shah's poster; Rosenblum et al. 2026 |
| Payoffs mapped to the same c* as the base rate | Table 1, payoff column | Liu et al. 2026: direction-agnostic cost responses, but not scored against c* |
| Thinking crossed with prior use | Table 1, the thinking-on rows | Novelty report C8: open for prior and payoff use |

**Claims kept out on purpose**

- "Threshold, not skill" as a finding. It is established, and the paper cites it.
- Logprob ROC as a method contribution. It is covered (C7).
- "Confirmation bias" or "deference" for our critics. The preregistered test of unjustified deference was not met.
- Any size of ρ for reasoning-on critics beyond "label-dependent".
- Any claim about OpenAI critics before the rate-wording analysis.

**Points that run against the paper.** It discusses each of them:

- Frontier models use stated costs and counts in other tasks (Yamin; Servajean; Lijo; Yang).
- A declared-inaccurate source is still followed (Guo et al.).
- Brown et al.'s source ordering is the reverse of Opus's.
- The open models treat a bare claim about like a stated 90% chance. Only the strongest wording beats every number for them.
