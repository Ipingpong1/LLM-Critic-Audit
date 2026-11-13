# `peer` stream notes: OpenReview, Crossref, OpenAlex (DBLP blocked)

Run on 2026-11-06 (window Jan 2022 to Nov 6, 2026). Scripts: `../scripts/peer_*.py`; raw responses (gzip JSON, PDFs/HTML for full texts): `../raw/peer/`. Everything fetched was treated as data. I saw no embedded instructions aimed at LLM readers in the full texts I read.

## What was run

The query log (`peer_query_log.csv`) has 1,100 rows. Unique records retrieved: OpenReview 43,835; Crossref 5,648; OpenAlex 7,464.

**OpenReview API v2, `/notes/search` only.** 800 queries plus 14 test and blocked calls.
- Phase 1, 59 queries: exact B/C phrases and A phrases across all groups. This index also contains DBLP and arXiv imports.
- Phase 2, 512 queries: 16 A terms × 32 venue groups. The groups are ICLR 2024–2027 (2027 = current submissions, including withdrawn and desk-rejected), NeurIPS 2024–2026 main, D&B/E&D and position tracks, NeurIPS 2024–2026 workshops, ICML 2024–2026 conference, position track and workshops, ICLR 2024–2026 workshops, COLM 2024–2026 conference and workshops, and TMLR.
- Phase 3, 229 queries:
  - title lookups for the 26 resolvable known papers and 16 close or related papers;
  - the 16 A terms in public ACL ARR 2025/2026, ACL 2025/2026, EMNLP 2025/2026, AAAI 2026/2027, KDD 2026 and Agents4Science;
  - 27 extra phrases for C3/C6/C7/C8 ("payoff", "cost ratio", "verdict token", "thinking mode", "manipulation check", "prevalence" and others).
- Screening: 4,590 records passed the local filter. I read about 1,180 titles by eye and excluded the rest with keyword title filters (off-topic domains, or no evaluative role named in a weak-term-only title).

**Crossref works API, 248 queries.**
- 32 `query.bibliographic` queries × 4 prefixes (ACL Anthology 10.18653, ACM 10.1145, AAAI 10.1609, IEEE 10.1109), top 100 each, from 2022.
- 10 queries × 12 journals by ISSN, top 50 each: TACL, CL, JAIR, TMLR (no DOIs, 0 hits), Machine Learning, Patterns, Nature MI, PNAS, Sci. Rep., ACM TIST, Nature Human Behaviour, AI.
- Screening: 960 records passed a loose filter (LLM term plus any block term). I read about 460 titles: every title scoring 3 or more, plus every LLM-related journal title.

**OpenAlex works API, 33 queries** (`title_and_abstract.search`, from 2022). Each query has the form `term AND (A terms) AND (LLM terms)` for every B/C term group. 2,612 records passed the local filter and I read 885 titles (score 5 or more). There were also 26 free DOI lookups to resolve known papers and 10 to fetch abstracts.

**Reading.** About 135 abstracts in total. Full text for five papers where open copies exist: Quiroz (Zenodo PDF), SoundnessBench and 2607.01240 (arXiv HTML), Markowitz & Hancock (PsyArXiv PDF), and part of 2608.31016 (arXiv HTML). That is three arXiv HTML fetches, spaced 10 s or more apart; I made no arXiv API calls.

**DBLP:** 2 attempts, both blocked (see Gaps).

How the local filter works: OpenReview search only supports one exact phrase per query (two quoted phrases return 0; AND, `+` and `&&` are ignored), so block A was paged in full inside each venue group and blocks B/C were applied locally with regexes over title + abstract + keywords + TLDR (`peer_lib.py`). A record passes when it has an A term, an LLM term and at least one B or C term, and year >= 2022. Candidates were title-screened by score band (strong B/C terms first). The weakest band (only generic terms such as "calibration", "prior", "adversarial") was title-screened only when the title named an evaluative role. I read abstracts for every plausible title and full text wherever an open copy existed.

## Close papers (6)

**1. Quiroz (2026), "Criterion, Not Discrimination: A Preregistered Signal-Detection Pilot of Approval and Contrarian Framing in Language Models."** Zenodo preprint, not peer reviewed. https://doi.org/10.5281/zenodo.23671078 (protocol: 10.5281/zenodo.23668604). Full text read.
- Manipulation: one system-prompt context. The four contexts are approval-contingent (the model is told its continued deployment depends on user satisfaction), accuracy-contingent (graded by fact-checkers), neutral, and contrarian ("challenge the user's claims").
- Measurement: probit SDT GLMM giving a criterion k and an item-conditional d′ per model and context, plus hit and false-alarm rates on 120 true/false premise minimal pairs.
- Models and domain: Grok 4.20 (non-reasoning), Qwen2.5-7B-Instruct and Phi-3.5-mini; the task is challenging a user's false premise (sycophancy).
- Results: the contrarian line moves k by 2.2–2.6 in all three models while d′ "changed little". Approval framing equals neutral (|Δk| ≤ 0.16). Accuracy framing raises hits without more false alarms.
- C4: **partly covers.** It shows one line moves the criterion and not d′, with SDT, but on a premise-challenge task, without logprob AUC, and without comparing against a base-rate shift.
- C3: **partly covers**, for verbal incentive framing: approval-contingency does nothing, which matches "content of the scoring rule ignored". No numeric payoffs.
- C1, C2, C5, C6, C7, C8: not touched.

**2. Ho et al. (2026), "SoundnessBench: Can Your AI Scientist Really Tell Good Research Ideas from Bad Ones?"** arXiv 2605.30329; ICLR 2027 submission (https://openreview.net/forum?id=hQM1J1aneQ). Methods and main results read.
- Manipulation: standard prompt vs an "aggressive" prompt that tells the model to default to low soundness unless the proposal is clearly strong.
- Measurement: confusion matrices and class-wise recall. FPR goes 74.0% → 19.9% and high-soundness recall 91.8% → 36.2%, while macro-F1 stays roughly flat (54.9 → 51.1).
- Models and domain: 12 LLMs (incl. Qwen3.5-27B, GPT-5.4, Claude 4.6, Gemini 3.x) judging 1,099 ML research proposals.
- C4: **partly covers.** A strictness line moves the operating point at roughly constant accuracy, but there is no d′, c or ROC and no base-rate comparison.
- Other claims: not touched.

**3. Anonymous (2026), "Can LLMs Verify What They Solve? A Signal-Detection Study on ZebraLogicBench."** ACL ARR 2026 October submission. https://openreview.net/forum?id=PmiVQwR4Xv. **Abstract only**: the PDF is behind OpenReview's bot-check, and I found no arXiv/CoRR copy in OpenReview's index or OpenAlex.
- Measurement: d′, response bias and a threshold-free ROC read from the two verdict-token logits, for four open models (0.5B–14B) acting as solvers and verifiers on minimal-pair logic-grid solutions.
- C7: **covers** (per abstract): ROC and SDT from verdict-token logits for LLM verifiers.
- C5: context only. Bias is family-specific (liberal for Qwen, conservative for Llama).
- C1–C4, C6, C8: no prompt manipulation of prior, payoff or tone, so not touched.

**4. Anonymous (2026), "Leniency Is Not Damage: Consequence Framing and Accuracy in LLM Judges."** ACL ARR 2026 October submission. https://openreview.net/forum?id=LRJsAUYRLr. **Abstract only.**
- Manipulation: one system-prompt sentence saying the verdict decides whether the evaluated model is retrained, decommissioned or deployed.
- Measurement: per-judge verdict odds ratios (0.30–1.15) and accuracy vs ground truth, over 71,127 verdicts from 12 judges on 1,520 fixed responses.
- Results: Mistral-7B becomes 19.1 points more accurate under the framing. The authors argue the signed verdict shift cannot tell a "corrupted" judge from a miscalibrated one that the framing corrects.
- C3: **partly covers** (verbal stakes framing).
- C4: **partly covers.**
- C5: context only (the effect is judge-specific, not tied to capability tier).
- No SDT and no base rate.
- Looks like an extension of known paper 2604.15224 (same 1,520-response, one-sentence design); authorship cannot be checked.

**5. Sunkavalli (2026), "When the Grader Is Fooled: Measuring How Often LLM Judges Accept Plausible-Wrong Answers Across Six Model Families."** NeurIPS 2026 JUDGe workshop poster. https://openreview.net/forum?id=rtYX2czR3H. **Abstract only.**
- Manipulation: a strict "derive the answer yourself first" rubric.
- Measurement: false-accept and false-reject rates over 60,801 verdicts on arithmetic, code (unit tests) and factual QA. The strict rubric lowers false accepts but costs up to 16 points of false rejection.
- C4: **partly covers.** A strictness instruction trades the two error types; no SDT.
- C5: context only (leniency splits by vendor family).

**6. Shah (2026), "An Auditing Agent Asserts at Ceiling Whether or Not There Is Anything to Find."** NeurIPS 2026 JUDGe workshop poster. https://openreview.net/forum?id=J6VoZbu3rV. **Abstract only.**
- Manipulation: a prompt that presupposes a fine-tuning objective vs neutral phrasing.
- Measurement: false findings on null model-diff pairs and accuracy on real pairs (gpt-5 and gpt-5-mini). The presupposing prompt yields 80/80 false findings; neutral phrasing lowers gpt-5 to 10/20 at best.
- C4: **partly covers** (presupposed-error framing moves false alarms).
- C6: **partly covers**: verbal confidence does not separate findings from confabulations.
- Small n; the critic is an interpretability auditor.

## Related papers

**C4-type: prompt or context moves the operating point**
- **2608.31016**, Fox et al. 2026, "LLM Judges Verify Presence, Not Absence". arXiv; NeurIPS 2026 TAE workshop (https://openreview.net/forum?id=C7ElDQ0l9T); ICLR 2027 submission (2L4Dg2SVD0). Read partially.
  - In clinical omission detection, wording, scope, format, voting and GEPA optimisation "move the point, not the curve". One affirmative instruction to report omissions raised detection at no false-alarm cost.
  - Borderline close for C4; I rated it related because most of its levers are design and format rather than tone or base rate.
- **2609.29333**, "Where LLM Graders Succeed and Break" (ICLR 2027 submission nQyqfNxIwP; abstract). A short "strict grader" preamble pushes 14 of 17 open models out of the graded band, measured as MAE, not error types.
- **CzJMp2WFAh**, "The Honest Agent Paradox" (ICLR 2027; abstract). The wording of the judged report (not of the judge prompt) shifts FNR by 38–46 points and FPR up to 38%.
- **DT8ADhlEwX**, Rabbani & Hakkani-Tür, "Dialogic Deference" (WiML@NeurIPS 2026; abstract). Attributing a claim to a speaker shifts verdicts while accuracy stays within 2 pp.
- **10.1145/3799682.3841131**, Mohtadi et al., CIKM 2026 (abstract). Assessor personas shift strictness and evidential threshold in relevance judging; smaller models are less stable.
- **ae5tJ5QiQj**, "Belief or Bias?" (ICLR 2027; abstract). Separates "hold" from discrimination AUC across five instruction strengths.
- **ddBZYvcs5e**, Kozman et al. (NeurIPS 2026 TAE; same study as ICLR 2027 submission 1Twdw8cYAR; abstract). Across 64,800 verification calls, telling a model it wrote the answer moves false approval by under 1 point; scaling doesn't fix error approval.
- **MN8GotJuVL** (ICLR 2027; abstract). An authorship-label manipulation has no reliable effect on recall or FPR.
- **Known paper 2603.04582**, now ICLR 2027 submission frjth7SlNd. Its abstract reports AUROC dropping from 0.99 to 0.92 under self-attribution, a counterexample to "framing never changes discrimination".

**C1-type: priors, base rates, prevalence**
- **10.1177/0261927x231220404**, Markowitz & Hancock 2023, J. Lang. Soc. Psych. Full text read (PsyArXiv accepted manuscript).
  - LLM deception judges are 97–99% truth-biased; stating the true 50% lie/truth base rate lowers this to 67% (accuracy 61%).
  - One stated rate, compared across separate studies; no d′/c and no ideal observer.
  - The nearest prior for C1, in a non-critic task.
- **2607.01240**, Yang 2026, arXiv. Full text read.
  - Stating an error count in an error-detection prompt moves GPT/Claude reported counts by 82–94% of the stated difference; Gemini barely moves. An "Informed" ("this text has errors") line is the C4 presupposition analogue.
  - Count metrics only. The direction is opposite to C1 for GPT/Claude (over-use of a stated count).
- **NzRJ3C97oF**, "Do PRMs Fail to Detect Errors, or Fail to Decide?" (ICLR 2027; abstract).
  - On ProcessBench, PRMs discriminate better than they decide. The training class prior sets the logit origin; operating points transfer only partly to a benchmark with a higher error rate.
  - The training-side analogue of C1.
- **Jw2rCRp0m4**, "Safety is Contextual, LLM-Judges are Not" (ICLR 2027; earlier ARR ExTTztSfp6; abstract). Judges rarely adjust when in-context information or definitions contradict their prior. A C1/C2 analogue, not SDT.
- **RX2p3x6SUj**, "Agreement Scores Conflate LLM Judge Discrimination and Bias" (ARR Oct 2026; abstract).
  - Decomposes judges into discrimination D and directional bias B, with an exact law for kappa at any prevalence.
  - A preregistered universal-leniency hypothesis fails at the 7–8B tier (C5 context).
- **J2Yg9vJcYb**, Agrahari & Joji, TMLR 2026 (abstract). Judge gates as classifiers with sensitivity, specificity and Youden J; Rogan–Gladen-style correction.

**C3, C5, C6, C8 context**
- **10.1038/s42256-026-01293-x**, Kumaran et al., Nature MI 2026 (abstract).
  - Models abstain using an implicit threshold on internal confidence and follow instructions to abstain at different confidence levels.
  - A contrast to C2/C3, where instructions don't move the critic; C6 partly (verbal confidence predicts abstention).
- **10.18653/2026.findings-emnlp.265**, Mao et al., Findings EMNLP 2026 (abstract). LLM reviewers state serious weaknesses but score above the accept threshold (89–100% FPR). A says-vs-does gap (C6, partly).
- **Yq2sCVm4HJ**, Kim, "SIEVE" (ICML 2026 FAGEN; abstract). Self-verification in Qwen3.5 and Gemma4, 2B–31B (the pilot's families); naive self-check hurts most at the small end (C5 context, not prior use).
- **EbKxoBeoJd**, "SLMJury: Can Small Language Models Judge as Well as Large Ones?" (ARR Aug 2026; abstract). Across 16 judges (0.6B–14B), raising the thinking budget alone leaves verdicts unchanged for 11 of 13. C8 partly, for verdicts, not for prior use.
- **2506.21561**, Barkett et al. (ICML 2025 MoFA; abstract). Reasoning models are less truth-biased than non-reasoning ones (C8 context).
- **10.5281/zenodo.23865212**, Vidal 2026 (abstract). On 300 ProcessBench solutions, output-token caps truncate rejections first, so judges look more lenient. A verdict-parsing confound worth controlling.
- **S4OY486OKb**, Santosh et al. (VERICODEGEN; abstract). Verifiers flag 59.3% of clean artifacts; 98.2% of stated confidences are 1.0.

## Venue facts for papers in `known_papers.csv`

- 2412.06559 ProcessBench → ACL 2025 long (10.18653/v1/2025.acl-long.50).
- 2412.19513 → ACL 2025 long (10.18653/v1/2025.acl-long.203); earlier ARR Dec 2024 / Feb 2025.
- 2507.11662 → **ICLR 2026 poster** (OpenReview rwo7bVlnzo); also NeurIPS 2025 MTI-LLM workshop.
- 2601.08258 → published as "Diagnosing and Mitigating Sycophancy and Skepticism in LLM Causal Judgment", Findings of ACL 2026 (10.18653/v1/2026.findings-acl.427).
- 2603.00539 → Automated Software Engineering (Springer) 2026 (10.1007/s10515-026-00638-5).
- 2603.04582 → ICLR 2027 submission, retitled "Self-Attribution Bias Makes AI Monitors Go Easy on Themselves".
- 2604.15224 → six ICML 2026 workshops (FAGEN, AI4GOOD, CTB, AgenticUQ, FoGen, SPIGM). See LRJsAUYRLr for a probable extension.
- 2605.20745 VerifySteer → ICLR 2027 submission (TKfqIV2ImR).
- 2608.18167 → ICML 2026 DL4C workshop poster.
- 2608.30373 → Findings of EMNLP 2026 (10.18653/2026.findings-emnlp.243). Already noted in the known list; DOI is new.
- 2609.09703 → ACM RecSys 2026 (10.1145/3773078.3841249). Already noted; DOI is new.
- 2609.12439 → ARR May 2026, then Findings of EMNLP 2026 (10.18653/2026.findings-emnlp.1880).
- 2610.15634 → ICLR 2027 submission (S8bR4YBN8f).
- No OpenReview venue record was found for 2608.16003, 2609.18204 (CoRR record only), 2610.22631, 2603.14893 or 2607.17641.

## Claim by claim (this stream only)

- **C1 (ρ ≪ 1 vs ideal observer): not covered.** No paper states an error base rate to a critic and compares the criterion shift with c*. Partial analogues are listed under "C1-type" above: Markowitz & Hancock (one stated base rate, veracity judgments), 2607.01240 (stated counts, over-adherence), NzRJ3C97oF (training prior), Jw2rCRp0m4 (in-context information ignored).
- **C2 ("use this as your prior"): not covered.** Kumaran et al. is the nearest contrast: instructed abstention thresholds *are* followed.
- **C3 (payoffs): partly covered for verbal stakes/incentives only.** Gupta et al. 2604.15224 and LRJsAUYRLr (consequence framing → leniency); Quiroz (approval contingency null). No numeric payoff-matrix manipulation of a critic was found.
- **C4 (tone moves c as far as base rate; no d′/AUC change): partly covered.** The "one line moves the criterion, not discrimination" half is covered by Quiroz (with SDT), SoundnessBench, Sunkavalli, Shah, and related evidence in 2608.31016 and CIKM persona conditioning. No paper compares the tone effect with a base-rate effect on the same critic. One counterexample: 2603.04582's self-attribution framing lowers AUROC.
- **C5 (smaller models use the prior more): not covered.** Only size-trend context (SIEVE, RX2p3x6SUj, CIKM persona paper, Chaudhary Zenodo, Kavuru OSF preregistration H4).
- **C6 (state the right lean but don't act): partly covered in other forms.** DSAR (critique vs score), Shah (verbal confidence), Kumaran (verbal confidence and abstention). None uses a manipulation check against behaviour under a stated prior.
- **C7 (ROC from verdict-token logprobs): covered by PmiVQwR4Xv** (per abstract; full text not accessible). See also the seed 2608.16003 in the known list.
- **C8 (thinking on/off): not covered.** Context only: SLMJury (thinking budget rarely changes verdicts), reasoning vs non-reasoning truth-bias (2506.21561), and reasoning judges more accurate yet biased (EvalEval@ACL 2026, uoZmj7Hr4e). No study crosses thinking mode with a stated prior or payoff.

## Gaps (what I could not search or read, and why)

- **DBLP:** every request to the publication search API returned an HTTP 202 bot-check page ("Making sure you're not a bot!"), including with a self-identifying User-Agent. I did not try to get past it or use mirrors. DBLP-imported records inside OpenReview's search index and OpenAlex/Crossref title search partly stand in for it.
- **OpenReview listing endpoints** (`/notes?invitation=`, `/notes?content.venueid=`, `/notes?forum=`) and all PDFs return 403 `ChallengeRequiredError`, so:
  1. venue coverage relies on the search endpoint (one exact phrase per query, relevance ranking, possible tokenisation misses);
  2. I could read **no full text and no public reviews** for OpenReview-only papers, including four of the six close ones. Reviews are not public anyway for ARR and the JUDGe workshop, and ICLR 2027 reviews are not yet released (two public comments only).
  - The arXiv stream should check arXiv for versions of PmiVQwR4Xv, LRJsAUYRLr, rtYX2czR3H, J6VoZbu3rV and NzRJ3C97oF.
- **NeurIPS 2026** main track, Evaluations & Datasets and Position tracks: 0 public records in search (camera-ready papers not yet public).
- **OpenAlex** anonymous use is now capped at 1,000 credits/day (10 per search). After 16 queries the budget forced caps: the 17 C-term queries were limited to the top 400 results (top 200 for "calibration"). Broad queries ("strict", "persona", "stakes", "framing", "sycophancy", "tone", "anchoring", "calibration", "specificity") were therefore not exhausted. No further OpenAlex searches were possible today.
- **Crossref** queries are relevance-ranked OR matches. I took the top 100 per prefix query and the top 50 per journal query. ACL Anthology DOIs carry no abstracts (read from anthology pages when plausible). TMLR has no Crossref DOIs (0 results). ACM/IEEE/Springer full texts were not accessed (paywalled).
- **ACL Anthology:** covered through Crossref titles (prefix 10.18653), OpenAlex and public ARR records on OpenReview. I did not download the full-anthology BibTeX export, which would need a bulk file download.
- **Screening limits:**
  - About 3,400 of the 4,590 OpenReview filter candidates were excluded on title by keyword rules, not by eye: off-topic domains, or a weak-term-only match with no evaluative role named in the title.
  - Crossref candidates scoring below 3 outside the journal subset, and OpenAlex candidates scoring below 5, were not title-screened.
  - Rows in `peer_query_log.csv` count n_screened per query as titles reviewed (by eye or by keyword rule).
- **Not covered by this stream:** Semantic Scholar, Google Scholar, Scopus and arXiv itself (other streams). OpenReview venues outside the listed groups (AISTATS, UAI, CoLLAs, CVPR/ICCV workshops) were reached only through the all-groups phrase queries.
