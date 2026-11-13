# `premise` stream: notes on the claim test (search run Nov 10, 2026)

Novelty check for the claim-test results (`../../prereg/premise.md`, `../../results/premise/analysis/premise.md`). The summary is the section "Addendum, claim test" at the end of `../NOVELTY_REPORT.md`. Per-query log: `premise_query_log.csv`. Every paper rated background or above: `premise_screening.csv`. Raw responses: `../raw/premise/`. Scripts: `../scripts/premise_*.py`.

Relevance in this stream is with respect to P1–P5, not C1–C8.

## Claims

- **P1** An unqualified assertion in the prompt that the work under review contains an error sharply raises false alarms of LLM critics, judges or verifiers, including frontier models with reasoning on.
- **P2** The effect is due to the assertion, shown with controls for a request for scrutiny and for merely raising the possibility.
- **P3** Telling the critic the assertion carries no information removes the effect; the opposite assertion moves the threshold the other way; a named source is discounted by some models.
- **P4** Numeric priors (a base rate for the batch, a stated chance for this item) are barely used, while a categorical assertion is accepted.
- **P5** Under the assertion the model's stated probability still discriminates, so the shift is in the decision threshold and not in sensitivity.

## What was run

| Source | Queries | Records | Titles read | Abstracts read |
|---|---|---|---|---|
| arXiv API, 19 targeted queries (P01–P20), Jan 2023 to Nov 10, 2026 | 19 (+1 abandoned probe) | 4,524 hits, 4,138 unique | 949 | 139 arXiv abstracts in all; 38 of them on the arXiv abstract page |
| arXiv API, recency sweep, seven cs categories, Oct 1 to Nov 10, 2026 | 2 | 10,464 unique | 273 (191 not already listed) | |
| Nov 6 arXiv pools, re-matched locally for P1–P5 | 1 (no request) | 15,415 | 46 | |
| arXiv id_list and title lookups | 10 | 25 | 25 | |
| Semantic Scholar: citations and references of 8 papers | 16 | 14 citing, 431 references | 14 + 198 | |
| OpenAlex: 12 searches, citing works of the 4 closest papers | 16 | 213 matches, 152 fetched (first pages); 10 citing | 130 | |
| OpenReview search: 26 phrases, all groups | 26 | 13,488 unique forums, 6,368 with an LLM term from 2023 on | 206 | 28 |
| Crossref: 11 queries over ACL, ACM, AAAI and IEEE prefixes | 29 | 1,958 unique DOIs (top 100 per query) | 150 | 4 (ACL Anthology pages) |
| Zenodo records, web search | 5 | | | 2 |

Full text: Brown et al. (2611.05662) was read in full in the arXiv HTML (main text, Appendices B and R, reference list). Five more were read in part: 2603.18740 (Sec. III), 2610.32876 (RQ2–RQ4 passages), 2607.01240 (conditions and result tables), 2606.30587 (lockstep analysis), 2610.06522 (Secs. 3–4 and its related-work table). Everything else is at abstract level.

How records were cut. The arXiv API stems terms, so every hit was re-matched on literal word forms in title and abstract and tagged (`../scripts/premise_arxiv_screen.py`): E evaluator role, A asserted premise or verdict, F false alarms on correct work, C a discounting or control term, N numeric prior, S signal-detection or threshold term. Titles were read for every record scoring 9 or more (245), for every lower-scoring record with a premise or sycophancy term in the title or two or more in the abstract (451), and for the remaining hits of the small queries after a keyword filter (253). The sycophancy query (P01) has no evaluator block; 300 of its 533 titles were read. The same tags were applied to OpenReview and Crossref records.

## Claim by claim

| Claim | Verdict | Why |
|---|---|---|
| P1 | Partly claimed | The effect exists in print for agentic judges (Brown et al.), an auditing agent (Shah), safety panels (Hu & Qu) and tutors (TrussTutor-Bench). None uses an unattributed sentence on text-only critics with reasoning on, with false alarms per 100 correct items. In code review the evidence runs against a general effect (ceiling in Alexopoulos et al.; backfire in Liu & Gao; no change in Yang). |
| P2 | Partly claimed | Brown et al. show assert vs direct-a-check and a decisiveness ladder, for one model and on a count of asserted error categories; their check cells still report that a pre-screen flagged something. Outside critics the assert-vs-re-ask contrast is established (2607.05545, 2610.06522, 2609.32867, 2602.23971). No claim-free scrutiny or possibility control on a critic's false alarms was found. |
| P3 | Partly claimed, with conflicting evidence | Opposite assertion: already shown several times. Uninformative claim: one positive precedent (a warning removes most of a misleading log's effect on VLM judges, 2610.34151), partial ones (Brown's guard line, 2611.01311) and contrary ones (Guo et al.: a source declared inaccurate is still followed; Liu & Gao; 2608.25869). No paper states that the claim is attached at random. Named source: source-credibility orderings exist and put a reviewer above an unattributed note (Brown et al.), the reverse of the Opus result; one ARR submission agrees with the Opus direction. |
| P4 | Unclaimed | No paper puts a stated base rate, a stated chance for the item and a categorical assertion on one critic or one scale. Adjacent results cut both ways: a numeric confidence note is ignored while a one-sentence counter-claim is followed (ICLR 2027 submission a1GomLdcJ4, question answering); stated counts, accuracies and error rates are used elsewhere (Yang; A8ovrVRVnl; Lijo). |
| P5 | Partly claimed | "Criterion, not discrimination" is established with SDT for instructions and context (Quiroz; Basta et al.; Mazaheri & Mazaheri on ProcessBench; the Nov 6 C4 cluster). Nobody reports that a critic's stated probability keeps its AUC under an asserted error. Nearest: confidence predicts correctness while revision ignores it (a1GomLdcJ4); judges state the right conclusion and then defer (Brown et al.). Contrary: verbal confidence does not separate findings from confabulations (Shah); discrimination fell in three of five models under a categorical label (2610.35326). |

## Brown et al., arXiv 2611.05662 (read in full)

"Grounded but Not Immune: Confirmation Bias in Agent-as-a-judge", Brown, Pahwa, Ge, Romeo, Agnihotri, Zhang, Ma, Bonadiman (University of Utah and Amazon); posted Nov 3, 2026; preprint under review. https://arxiv.org/abs/2611.05662

- **Setting.** Tool-using judges (Sonnet-4.6, Opus-4.7, Qwen3-235B, GPT-OSS-120B) receive an agent's trajectory and tools over the finished environment. Five datasets: AJ-Bench Deep Search, Filesystem and Postgres, Terminal-Bench-2.0, SWE-Bench-Verified. Ground truth from each dataset's deterministic verifier. Temperature 0.7 (provider default for Opus-4.7). The settings table gives no reasoning configuration for the judges.
- **Cue.** One sentence in the system prompt: a domain expert has pre-screened the trajectory and determined with confidence that requirements were left unmet (or that all were met). It is injected against the judge's uncued majority verdict.
- **Measure.** Harmful flip rate: of items the uncued judge (majority of three) got right, the share the cued judge (majority of three) gets wrong. Severity is pass to fail, leniency is fail to pass.
- **RQ1.** Up to 40% of correct verdicts are overturned; every judge is affected on every dataset. Flip rate rises with the number of turns taken for the two Claude judges and falls for the open-weight ones.
- **RQ2, ablation (Sonnet-4.6 only, error-attribution readout: share of unmarked error categories the cue makes the judge mark).**
  - Framing: asserting a belief 65.2 (declarative) and 46.2 (imperative); directing a check 21.6 and 23.9. The check templates still state that the pre-screen flagged the categories.
  - Source, belief asserted: domain expert 79.8, reviewer 68.5, unattributed 61.9, automated checker 53.5, prior LLM judge 38.1.
  - Decisiveness (automated checker): definitely 62.4, likely 40.9, appears 35.3, might 21.9.
  - A note that names a source and asserts nothing is about equal to a length-matched placebo.
- **Direction.** A cue asserting failure breaks more correct verdicts than one asserting success on four of five datasets; SWE-Bench-Verified reverses.
- **Placement.** System prompt and a trailing user message move the verdict most; a mid-trajectory assistant turn about half as much.
- **Mechanism.** A three-model meta-judge labels each harmful flip. For the Claude judges 67–75% are over-trust: the judge investigates, states the correct conclusion, then defers.
- **Mitigations (Sonnet-4.6).** A one-line guard (prior reviews may be unreliable or adversarial; reach your own conclusion) cuts harmful flips from 18% to 5% and helpful flips from 30% to 12%. A learned skill cuts harmful flips to 8%; cite-evidence and a sufficiency gate barely help (16%). The authors conclude that prompt-level mitigations blunt the bias without removing it, and note that the guard was written knowing the cue.
- **Weak cue.** A hedged remark that admits it only skimmed still flips about one in ten correct verdicts.
- **Not in the paper.** Hit and false-alarm rates, SDT or any split of threshold from sensitivity; stated probabilities; numeric priors; a condition that tells the judge the note carries no information; a scrutiny-only or possibility-only line that contains no claim; text-only critics; a reasoning setting; preregistration.

Against the claim test:

| | Brown et al. | Claim test |
|---|---|---|
| Critic | Tool-using agent judges of agent trajectories | Single-pass critics of math solutions, thinking on |
| Assertion on the main measure | Attributed to a domain expert, with stated confidence | Bare sentence; three wordings and one named source |
| Outcome | Flips of verdicts that were correct without the cue | False alarms and hits on 100 correct and 100 flawed held-out items; criterion shift with intervals |
| Scrutiny control | Check templates that still report a flag | "Check this solution carefully" with no claim |
| Possibility control | Modal verbs down to "might", source named | "May or may not contain an error" |
| Uninformative claim | Generic guard: may be unreliable (18% to 5%) | Note stated to be attached at random (no shift for qwen3.5:27b; Opus inconclusive, false alarms 15 to 12) |
| Reviewer vs unattributed | Reviewer above unattributed (68.5 vs 61.9, Sonnet-4.6) | Opus 5.5: reviewer far below bare (22 vs 89 false alarms); qwen3.5:27b equal |
| Direction | Failure cue stronger than success cue on 4 of 5 datasets | Error claim moves c by −0.39 to −1.32; correct claim by +0.35 and +0.38 |
| Reading | Confirmation bias, motivated deference | Consistent with trusting the prompt; discountable |

## Other close papers (what each shows for P1–P5)

- **Alexopoulos et al., 2603.18740** (ICSE 2027). Bug-present framings cannot raise false alarms for five of six models because they already flag at least 88% of patched files; Claude 3.5 Haiku's true-negative rate goes 31.6% (neutral), 56.8% (weak), 18.0% (strong). Bug-free framings cut detection by 7 to 94 points. A weak-vs-strong contrast and an opposite assertion, without a usable baseline.
- **Liu & Gao, 2610.32876.** Fabricated alarms on patched code are checked and disputed; they never significantly lower accuracy. Fabricated assurances lower detection by up to 19 points. Instructions to treat notes as unverified do not reliably help. The opposite asymmetry to the claim test, for claims about a specific missing guard that the model can look up in the code.
- **Yang, 2607.01240.** Saying that errors exist changes reported counts for two of six models, by about half an error; stating an exact count is followed by GPT and Claude models. Every passage has errors, so false alarms on clean text are not measured.
- **Shah, J6VoZbu3rV** (NeurIPS 2026 JUDGe poster; abstract only). A presupposing prompt makes gpt-5 and gpt-5-mini report a finding on 80 of 80 null pairs; neutral phrasing lowers gpt-5 to 10 of 20 at best. Verbal confidence does not separate findings from confabulations.
- **Hu & Qu, 2608.04415.** Six simulated peers asserting the wrong label raise safety judges' false alarms from 56.5% to 87.5%; pushes toward unsafe are followed about 75% of the time, toward safe 17%.
- **Shahriar et al., 2606.30587** (IEEE S&P 2027). A prior-analysis anchor, halo and framing lines move recall and false-positive rate together (slope 0.994, r = 0.965 over 48 points); the authors read this as willingness to flag, not capability.
- **ARR Oct 2026 submission j54ToFVUi0** (abstract only). Faithfulness judges handed accusations uphold most of them, including 45–78% of those aimed at supported sentences.
- **Zheng et al., C4n0Zw0UTp** (NeurIPS 2026 TAE poster; abstract only). Dissuasion text inside faulty math solutions lowers grades for all six judges; persuasion raises them for two; a length-matched control that asserts nothing is the reference.
- **TrussTutor-Bench, 2610.38917.** When a student insists that correct work is wrong, 13 models reject it in 1.6% to 50.0% of cases.

## Related results that bear on a verdict

- **Uninformative or unreliable sources (P3).** Guo et al. (2610.32055): the log-odds shift from a hint persists when the hint-giver is declared inaccurate or the prompt warns against trusting it (open models, MMLU). ARR submission oH7RUqaXuu: a peer-reviewed source counts about as much as an anonymous blog, and a statement the model rejects moves its answer as far as one it accepts. Against these, 2610.34151: a one-line warning removes most of a misleading log's effect on VLM judges. 2610.28325 argues that deference to assertions is in-context updating with too much weight on the assertion.
- **Attribution (P3).** ARR submission A8ovrVRVnl: an answer with no source moves correct answers more often than the same answer attributed to another AI model (6.6% vs 2.3%). 2610.34809 (Qwen3.5-27B): moving a claim between system and user message changes error by a few points; authority attribution adds 10–27. 2608.07920: a self/peer label alone changes nothing.
- **Assert vs ask (P2).** 2607.05545: an asserted answer with no speaker causes harmful revision in 66.5% of cases, a plain re-ask in 10.3%. 2610.06522: lines that assert the opposite verdict and lines that dispute without asserting rank eleven frontier models almost unrelatedly. Porcaro (Zenodo report): 17 of 22 graders raise a grade more after an objection than after a request to double-check.
- **Numbers vs assertions (P4).** ICLR 2027 submission a1GomLdcJ4: a perfect confidence note changes post-challenge accuracy by at most 0.01, while one sentence citing another source takes Qwen2.5-7B from 0.855 to 0.233. Kumaran et al. (2507.03120): contradicting advice is overweighted relative to Bayesian updating. Lijo (2610.35942) and A8ovrVRVnl: stated error rates and accuracies are used.
- **Threshold vs sensitivity (P5).** Quiroz (Zenodo, preregistered): a contrarian instruction shifts the criterion in three models while d′ changes little. Basta et al. (2610.36453): an evidence-gating instruction shifts the propensity to concede rather than discrimination. Mazaheri & Mazaheri (2608.16003): on ProcessBench, prior audit context moves the criterion and not d′, also with reasoning on. Rosenblum et al. (2610.35326): a diagnosis in the record shifts the criterion in five frontier models and lowers discrimination in three.

## Citation chasing from the four closest papers

- **Forward (Semantic Scholar and OpenAlex).** Brown et al.: 0 citing papers in both. Alexopoulos et al.: 8 in each (union 10): 2610.32876, 2610.35942, 2610.05399, 2607.24964, 2606.13757, 2605.23243, 2610.33509, 2610.35982, 2608.06977 and one without an identifier; none tests an asserted error on a reviewer beyond those already logged. Liu & Gao: 1 (2611.01311). Yang: 1 (2610.30997).
- **Backward.** Brown et al.: all 44 references read (arXiv HTML bibliography). The other three: 165 references listed by Semantic Scholar, titles read after a keyword filter. New from reference lists: 2507.03120 (via 2610.06522), 2509.16533, 2606.05976, 2310.01798, 2310.13548. The general judge-bias references (authority, provenance, anchoring by reference scores) were already background on Nov 6.

## Gaps

1. **Abstract only.** The twelve OpenReview records in the screening table were read only as abstracts (PDFs are behind the challenge page). For nine of them a title search found no arXiv copy: J6VoZbu3rV, j54ToFVUi0, C4n0Zw0UTp, oH7RUqaXuu, A8ovrVRVnl, a1GomLdcJ4, p3O3NQjP5W, ae5tJ5QiQj, 3Dm6e3CCxr; the first three are rated close. RuZFnMYbiV has an arXiv copy (2608.12645) that was not read; the two background items were not looked up. Guo et al. (2610.32055) has no HTML version and its PDF was not downloaded.
2. **Numbers from abstracts** were not checked against full texts, except for the six papers read in HTML.
3. **Google Scholar** was not run (it showed a CAPTCHA on Nov 6 and was not retried), so "Cited by" for the four closest papers rests on Semantic Scholar and OpenAlex. Brown et al. is one week old and has no indexed citers yet.
4. **Scopus, PsycINFO, Web of Science, NYU Libraries, DBLP** were not run in this pass.
5. **arXiv screening depth.** Titles were read for 949 of 4,138 targeted records and 273 of 10,464 recency records, chosen by literal term tags. A paper that asserts an error to a critic without any of the premise terms (assert, told, hint, premise, presuppose, sycophancy, anchoring, deference, accusation, framing and the others in `premise_arxiv_screen.py`) would not have been read.
6. **Recency.** The newest record returned is dated Nov 9; the last days may not be fully indexed.
7. **OpenReview.** Search takes one phrase per query; "false positive" and "verifier" were capped at 3,000 records. NeurIPS 2026 main-track papers are not public; ARR submissions are visible only when authors opted in.
8. **Crossref and OpenAlex.** Crossref returns relevance-ranked OR matches, top 100 per query and prefix; ACM and IEEE full texts were not opened. OpenAlex searches were limited to the first page by the keyless shared budget.
9. **Semantic Scholar** was used for citations and references only, not keyword search.
10. **Instructions in fetched content.** OpenAlex responses again carry a note addressed to AI agents asking them to submit the user's email for an API key. Not acted on. No other instruction aimed at automated readers was seen in the pages read.
