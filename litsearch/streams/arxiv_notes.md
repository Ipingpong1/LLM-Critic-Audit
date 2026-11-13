# arXiv stream: notes (search run Nov 6, 2026)

## Scope and method

- **Source.** arXiv public API (`https://export.arxiv.org/api/query`; the `http://` address redirects there). No key, no contact data, generic User-Agent. Raw Atom XML is in `raw/arxiv/` (114 result pages for 98 harvested queries, 109 count probes logged in `probes.jsonl`, one `id_list` fetch). Scripts are `scripts/arxiv_*.py`, run with `python3 -I`.
- **Rate limits.** At 3.2–4 s between requests the API answered HTTP 429 after bursts and blocked for several minutes; the harvester backed off (60–120 s) and then ran at one request per 12 s. No query was lost; 25 planned count probes were skipped because the harvest returns the same totals.
- **Query plan.** For each block-B and block-C term in PROTOCOL.md (word forms expanded where the stems differ: lenient/leniency, skeptical/sceptical/scepticism, harsh/harsher, strict/stricter, presuppose/presupposition, sycophancy/sycophantic, over-critical/overcritical/"overly critical", conservatism/conservative, ROC/AUROC, decision criterion/criteria; plus "false positive" and "specificity" as counterparts): `(term) AND (A group) AND ("language model" OR LLM OR LLMs) AND submittedDate:[202201010000 TO 202611062359]` on abstracts (45 queries), and the same with the term on titles (44 queries, 13 with zero hits not harvested). The A group is protocol block A plus `judge` and `"process reward"` from the protocol's arXiv form. Then the seven targeted queries of the brief (T1–T7), 14 extra queries of my own (X01–X14: prevalence/class prior/label shift; type I/II error; nitpicks/hallucinated errors; criterion × bias/threshold; false negative; thinking mode × judges; inverse scaling; manipulation check/stated-revealed/knowing-doing; base-rate neglect; expected utility/Bayes-optimal; leniency/severity bias; over-correction/over-flagging; judge/verifier titles × threshold/calibration; metacognitive sensitivity), and one query without the LLM block (X15, malformed, rerun as X15b; see Gaps). Recency sweep: `(cat:cs.CL OR cs.AI OR cs.LG OR cs.SE OR cs.HC OR cs.CY) AND (title or abstract: judge, verifier, critic, critique, "reward model", self-correct*, self-refine*, reviewer, overseer, monitor, grader) AND submittedDate:[202610150000 TO 202611062359]`.
- **What the API does to these terms (count probes, logged).** `abs:` and `ti:` terms are Porter-stemmed, even inside quotes: verifier = verify (73,128 hits), critic = critical (200,918), reviewer = review (86,119), monitor = monitoring, judge = judges, "language model" = "language models"; "base rate" also matches "based rating", specificity matches specific, utility matches utilize. "d'" cannot be searched (the apostrophe is dropped). `max_results=0` returns HTTP 500.
- **Literal re-match and cut.** Because of the stemming, every hit was re-matched on title + abstract with literal word-form regexes (`scripts/arxiv_rank.py`): tier 1 = A + strong B + strong C; tier 2 = A + strong B or C; tier 3 = A + only weak B/C terms (prior, sensitivity, specificity, ROC, adversarial, persona, stakes, framing, ...); tier 4 (safety net) = a strong B/C term without a literal A term; tier 5 = stemming over-reach only, or A without any literal B/C term. All titles in tiers 1–4 were read; tier 5 was not title-screened. Targeted and extra queries were re-matched on their own AND-groups (`scripts/arxiv_tfilter.py`) and every literal match read. The literal A∧(B∨C) set (2,997) exceeds ~1,500, so, per the brief, every title was read and abstracts only for titles that could plausibly be relevant. The cut is stated per query in `arxiv_query_log.csv`.

## Counts (arXiv only)

- Queries: 98 harvested, 17 count-only probes (zero-hit title queries, B17 specificity, recency denominator), 36 stemming probes, 1 id_list recall check: 152 rows in the query log.
- Records: 24,701 hits summed over harvested queries; 18,580 unique arXiv ids (versions ignored).
- Main sweep (block, targeted and extra queries, 13,454 unique ids): tiers 1–3 = 2,997; tier 4 = 967; tier 5 (not screened) = 9,489.
- Recency sweep: 2,343 API hits in the window (8,885 submissions in the six categories in all), 1,063 literal term matches (914 new titles read, 149 already read), 1,280 stemming-only hits not read.
- Screening: 5,567 unique titles read; 237 abstracts read (17 excluded at abstract level); full text read for 14 papers (methods and results) and partly for 30.
- Kept in `arxiv_screening.csv`: 9 close, 56 related, 155 background (including 8 rows on known papers with new information or a first screening).
- Recall check against `known_papers.csv`: 21 of 27 known papers came back from the block queries. The other six (fetched by id_list) lack any block-B/C term (2412.19513, 2412.06559 ProcessBench, 2603.12123, 2603.00539) or lack "LLM"/"language model" in the abstract (2605.20745 VerifySteer; 2608.10729 says "foundation models").

## Claim by claim (what arXiv shows)

| Claim | Status | Closest arXiv papers (new ones in bold) |
|---|---|---|
| **C1** stated base rate moves c far less than the ideal observer (ρ ≪ 1) | **Not covered.** No arXiv paper states an error base rate to an LLM critic, verifier or judge and compares the criterion shift with c* or any ideal observer. | Context only: **2610.35326** (a stated prior diagnosis shifts the SDT criterion of clinical LLM decisions by −0.49 to −1.04; categorical prior, no ideal observer, not a critic), **2412.11009** (base-rate neglect in Bayesian word problems), **2610.41391** (LLM reviewers' accept threshold vs the acceptance base rate, recalibrated post hoc, never stated to the model), **2606.07874**, **2606.00467**, **2607.02575** (judges/VLMs under-use definitions or criteria given in context), **2607.13618** (agents scored against an exact Bayes-filter oracle) |
| **C2** "use this base rate as your prior" does not raise ρ | **Not covered.** | Context: **2610.32876** (audit instructions do not reliably reduce deference to fabricated notes), **2608.25869** (a "disregard prior scores" warning does not remove anchoring), **2606.07834** (a detailed instruction leaves 21–48% overcommitment). Counterpoints where one line does work: **2610.34151** (a "the log may be inaccurate" warning removes most of a misleading log's effect), **2611.05662** (a guard line cuts harmful flips 18% → 5%, and helpful flips too), **2412.11009** (rewording to "compute the posterior probability" fixes GPT-4o's base-rate neglect outside critics) |
| **C3** stated payoffs don't move c in the right direction; reaction to presence, not content | **Not covered for critics.** | Context: **2604.03904** (announced abstain payoffs move abstention mostly as expected, an extreme wrong-answer penalty does not), **2603.29693** (GPT-5 shifts its SDT criterion toward the safer answer under a stated risk, other models inconsistent; no magnitudes or optimum), **2606.22974** (high-utility incentives do nothing while exhortation works), **2601.19082** (multiplying all payoffs changes cooperation although theory predicts no change), **2608.25869** (the presence of a prior-score anchor matters, its value hardly), **2510.17880**, **2610.06191** (stated costs and stopping rules under-used) |
| **C4** one line of tone moves c as far as the whole base-rate change, and no framing changes d′ or AUC | **Partly covered, more broadly than on Nov 2.** Several judge papers show a strictness, skepticism, de-biasing, speaker-framing or presupposition line moving false alarms and hits (or false acceptances and rejections) together with little change in overall discrimination. None compares such a line with a base-rate manipulation in the same critic, and only the known papers report d′ and c for it. | **2605.30329** (aggressive "default to low" prompt), **2610.22009** (a de-bias line moves the threshold, J flat), **2601.10896** (speaker framing shifts per-class accuracy, overall accuracy flat), **2611.01311** (skeptical framing of evidence raises catches and false alarms together), **2611.00407** (monitor prompt variants trade misses for false alarms at similar AUC), **2611.05662**, **2610.32876** (presupposition-type notes), **2607.01240** (presupposed error counts); related **2610.05094**, **2608.31016** (one instruction slightly improves discrimination), **2608.04415**, **2608.23941**, **2610.36453**; known 2608.16003, 2609.18204, 2610.22631 |
| **C5** within a family, smaller models use the stated prior more | **Not covered** (no paper measures prior use by size). | Context on size and context sensitivity, mixed in direction: **2608.10385** (smaller Llama and Qwen models more persona-sensitive), **2606.06306**, **2608.04415** (Qwen 7B far more pliable than 32B); **2605.30329** (larger Qwen3.5 more lenient by default); **2610.22009** (larger models accept fewer invalid items); **2607.02575** (7B → 32B barely changes criterion sensitivity) |
| **C6** models state the right lean but don't act on it | **Not covered** for a critic's stated lean about a base rate or payoff. The closest judge-side results are knowing-but-deferring. | **2611.05662** (judges reach the correct conclusion, then defer to a false note), **2606.07834** (judges recognise the conflict when asked afterwards on 62–66% of their own overcommitted claims), **2611.00407** (the monitor describes the exploit, never flags it); context: 2602.07996, 2610.38096, 2604.00228, 2610.36453 and the general says-vs-does work (2503.07003, 2605.05957, 2605.14038, 2606.09843, 2606.11016, 2606.12730, 2604.28031, 2607.13618, 2610.06191, 2610.34488) |
| **C7** ROC / z-ROC for critics from verdict-token logprobs | **Partly covered for ROC** (verdict-token probabilities used for ROC and low-FPR operating points of LLM detectors and classifiers); no z-ROC for critics of reasoning found beyond the known papers. | **2510.21049** (token scores vs verbal confidence, TPR at 1% FPR, safety and hallucination detectors), **2610.23988** (renormalised yes/no probabilities, AUROC, adjustable thresholds); context **2603.25112** (type-2 ROC and z-ROC from token logprobs for QA confidence); known 2608.16003, 2603.14893 |
| **C8** (planned) thinking on vs off changes ρ or payoff use | **Not covered** (no paper tests prior or payoff use by thinking mode). Thinking does shift operating points of detectors and judges. | **2510.21049** (thinking raises accuracy but lowers TPR at low FPR), **2605.26174** (reasoning on lowers c and raises d′ in one model), **2608.31016** (a reasoning budget raises discrimination), **2610.05094** (reasoning effort changes neither leniency nor accuracy), **2610.32876** (a reasoning variant is more suspicious), **2506.21561**, **2605.29087** |

## Close papers (full text read)

Each entry: what it manipulates and measures; models and domain; then each claim.

### 2605.30329 — SoundnessBench (Ho et al., May 2026). https://arxiv.org/abs/2605.30329
- Manipulation: standard reviewer prompt vs an "aggressive" prompt (a strict area chair applying an aggressive rigor filter; default to "low" unless rigor is clearly shown; prefer "low" when information is incomplete); also a retrieval-augmented evaluator. No base rate, payoff or stakes in any prompt.
- Measurement: confusion matrices for low- vs high-soundness proposals (false approvals, false rejections), per-class recall, Macro-F1. No d′, c or AUC.
- Models and domain: 12 LLMs (GPT-4o, GPT-5.4, Claude-Opus-4.6, Gemini-3.1-Pro, Qwen-3.5 2B–122B, ...); 1,099 results-masked ICLR proposals (reviewer-score labels; 327 expert-labeled).
- Results: false approvals 74.0% → 19.9%, false rejections about 8% → 63.8%; Macro-F1 54.9 → 51.1 (ICLR labels) or 48.9 → 56.5 (expert labels).
- Claims: C4 partly covered (one strictness line moves the criterion of LLM judges, both error types reported; no SDT, no base-rate comparison). C5 not touched (it reports larger Qwen3.5 models being more lenient by default, which concerns the default criterion, not prior use). C1–C3, C6–C8 not touched.

### 2611.01311 — What Do LLM Judges Actually Verify? (Shah et al., Oct 31, 2026). https://arxiv.org/abs/2611.01311
- Manipulation: complete vs gapped amendment record; the gapped line framed as an authoritative lookup, reworded ("no replacement recorded"), presented as an unverified note from an automated tagger, or with a warning that it may omit replacements.
- Measurement: catches of replaced citations (hits), validity false alarms on decoys and date controls, catch minus decoy false alarm; McNemar with Holm. No d′ or c.
- Models and domain: Gemini 3.1 Pro, GPT-5.5, Claude Opus 4.5, Gemma 4 26B; 48 IETF RFC replacement links × 4 item types (faults a fixed 25% of items, never stated).
- Results: the authoritative record suppresses catches; skeptical framing restores catches for Gemini and GPT-5.5 while decoy false alarms return too (GPT-5.5 decoy flags 0 → 10 and 8). The authors read this as a return to text-only behaviour: more flagging, not better use of the record.
- Claims: C4 partly covered (a skepticism framing moves catches and false alarms together; no SDT, no base-rate comparison). Others not touched.

### 2610.32876 — Trusting the Tool (Liu & Gao, Oct 23, 2026). https://arxiv.org/abs/2610.32876
- Manipulation: six evidence-note conditions in the audit context (none; true notes; relevant or irrelevant true notes; fabricated assurances on vulnerable code; fabricated alarms on patched code); eight audit-instruction variants.
- Measurement: recall on vulnerable and specificity on patched functions; direction-aware deference and its asymmetry. No d′ or c.
- Models and domain: deepseek-chat/flash/v4-pro, qwen-plus and 7 replication models; PrimeVul C/C++ vulnerable/patched pairs, 16,572 audits.
- Results: false assurances cut recall by 11–19 points; false alarms never lowered accuracy (specificity rose); asymmetry +0.16 [0.10, 0.24]; no instruction reliably reduced deference (a separate verification call helped, +0.12); default flag rates 36–79%; the reasoning variant of DeepSeek leaned to suspicion.
- Claims: C4 partly covered (presupposition-type context moves a code critic's verdicts, asymmetrically). C2 not covered (the instructions concern evidence, not a prior) but parallel. C8 touched (a reasoning variant is more suspicious; not ρ). Others not touched.

### 2601.10896 — DialDefer (Rabbani et al., ACL 2026). https://arxiv.org/abs/2601.10896
- Manipulation: the same claim judged as a statement ("Is this statement correct?") vs attributed to a speaker ("Is Speaker 2 correct?"); human vs LLM speaker labels; mitigations ("Be Honest", "Dehumanizing", SFT, DPO).
- Measurement: Dialogic Deference Score = change in accuracy on correct claims minus change on incorrect claims (both error types); overall accuracy. No d′ or c.
- Models and domain: GPT-4o, GPT-4o-mini, GPT-5-mini, Gemma-3-12B, Qwen-2.5-7B; 9 balanced datasets and r/AIO (3,244 items).
- Results: DDS +33.8 (Qwen-7B), +29.5 (Gemma-12B), +9.0, +8.3 and −1.1 (GPT-4o) while overall accuracy changes by under 2 pp; "Be Honest" over-corrects into skepticism.
- Claims: C4 partly covered (framing moves the judge's lean, not accuracy; not tone vs base rate). Others not touched (sizes differ only across families).

### 2607.01240 — Prompt Framing Distorts Count-Based Evaluation of LLM Error Detection (Yang, May 2026). https://arxiv.org/abs/2607.01240
- Manipulation: Blind ("Does this text have any grammatical errors?"), Informed ("This text contains grammatical errors"), Anchored ("contains exactly N errors", true N), Mislead-Over (N+2), Mislead-Under (N−2).
- Measurement: count-F1 vs span-level F0.5 (M2-style and ERRANT, two references).
- Models and domain: GPT-4o, GPT-5.4, Claude Haiku 4.5, Claude Sonnet 4.6, Gemini 2.5 Flash, Gemini 3.1 Pro; 123 CoNLL-2014 passages with 3–7 errors.
- Results: presupposing errors barely changes counts; GPT and Claude follow a stated count closely (82–94% of a 4-error difference), Gemini hardly (4–5%); span F0.5 rises +0.04 vs count-F1 +0.22.
- Claims: C4 partly covered (presupposed errors and counts move how much is flagged, not detection). C1 touched only by contrast (a stated per-text count is followed almost fully by two families, unlike a stated prevalence in the pilot). Others not touched. Every passage has errors, so no item-level false alarms.

### 2510.21049 — Reasoning's Razor (Chegini et al., Oct 2025). https://arxiv.org/abs/2510.21049
- Manipulation: Think On vs Think Off on the same model; fine-tuned vs zero-shot; certainty-level prompts ("at least X% certain").
- Measurement: token-based scores (normalised label-token logits) vs verbalised confidence; ROC; TPR at fixed low FPR; accuracy.
- Models and domain: safety detection (8 benchmarks) and RAG hallucination detection (HaluBench); Llama-3 1B/8B, Qwen2.5 7B–32B, QwQ-32B, R1-distill-Qwen-32B, K2-Think, fine-tuned guards.
- Results: thinking raises accuracy but lowers TPR at 1% FPR (fine-tuned safety model 40.0% Off vs 13.8% On); token scores beat verbal ones at strict operating points (QwQ-32B 30.6% vs 10.0%); certainty prompts move operating points.
- Claims: C7 partly covered (ROC and operating points from verdict-token probabilities for LLM detectors, not critics of reasoning; no z-ROC). C8 partly covered (thinking changes operating characteristics; no prior or payoff). C4 touched (certainty prompts). Others not touched.

### 2610.22009 — Visual Sanad (Abtahi et al., Oct 15, 2026). https://arxiv.org/abs/2610.22009
- Manipulation: natural prompt vs a de-biased prompt telling the model not to treat decorative design, religious-looking borders or verification headers as evidence; six visual framings.
- Measurement: false acceptance, false rejection, discrimination = 100 − FA − FR (Youden's J).
- Models and domain: GPT-4o/4.1/5.5/5.6-Terra and 8 open VLMs (Qwen2.5-VL, Qwen3-VL, InternVL3.5, MiniCPM-V, Gemma 4); 2,400 rendered quote–reference pairs, 25% valid (not stated to the model).
- Results: in weaker models the de-bias line moves the threshold rather than discrimination (InternVL3.5-38B FA 81.6 → 48.1, FR 10.8 → 42.8, J 7.6 → 9.1); within a family, larger models accept fewer invalid citations.
- Claims: C4 partly covered (one prompt line shifts the criterion with little change in J). C5 not touched (size raises discrimination; prior use not measured). Others not touched.

### 2611.00407 — Hacking or Just Failing? (Kezendirane, Oct 30, 2026). https://arxiv.org/abs/2611.00407
- Manipulation: five monitor prompt variants (definition of manipulation, event-ID checklist, 1–10 rating, two separately scored questions); monitor capability.
- Measurement: exploits caught, false alarms on honest and gap-matched failures, AUC from verbal suspicion scores.
- Models and domain: Llama 3.2 3B and 3.1 8B monitors vs Gemini 3.1 Flash-Lite; sandboxed order-reconciliation task, 60 episodes (14 exploits).
- Results: prompt changes move the 8B monitor's operating point (4/14 caught at 0/35 false alarms, AUC 0.64, vs 13/14 at 20/35, AUC 0.70); Gemini AUC 0.80; Gemini described an exploit no prompt named in 16 of 20 explanations but flagged none (0/5, then 0/25).
- Claims: C4 partly covered (prompt variants trade misses for false alarms). C6 partly covered (describes but does not act; not a stated lean about a prior). Others not touched. Very small samples.

### 2611.05662 — Grounded but Not Immune: Confirmation Bias in Agent-as-a-Judge (Brown et al., Nov 3, 2026). https://arxiv.org/abs/2611.05662
- Manipulation: a false pre-screening note in the system prompt, attributed to a domain expert, asserting that requirements were unmet (or met); a weak hedged cue; ablations of framing, source, decisiveness and placement; four mitigations including a one-line guard instruction.
- Measurement: harmful flips of correct verdicts, split into severity (pass → fail) and leniency (fail → pass); helpful flips; failure modes.
- Models and domain: Sonnet-4.6, Opus-4.7, Qwen3-235B, GPT-OSS-120B as tool-using judges on AJ-Bench, Terminal-Bench-2.0 and SWE-Bench-Verified.
- Results: up to 40% of correct verdicts overturned; assertions move judges more than instructions to check; over-trust (gather the evidence, state the correct conclusion, then defer) is 67–75% of harmful flips for the Claude judges; the guard line cuts harmful flips 18% → 5% and helpful flips 30% → 12%.
- Claims: C4 partly covered (a presupposed verdict moves the judge; no SDT). C6 partly covered (the correct conclusion is stated and then not acted on). C2 touched by contrast (one guard line does change behaviour, by changing reliance rather than skill). Others not touched.

## Related papers

Generated from `arxiv_screening.csv`. "partly" = the same idea on an LLM critic, judge, verifier or monitor with a different measurement or manipulation; "context" = outside critic tasks, or a different manipulation that bears on the claim. Claims not listed are not touched.

- **2412.11009** Dual Traits in Probabilistic Reasoning of Large Language Models (2024). https://arxiv.org/abs/2412.11009
  - Manipulation: Bayesian problems with all inputs stated; stated base rate with omitted diagnosticity (75% vs 25%, normative odds ratio 9); base rates recalled from memory; prompt rewording ('compute', 'posterior probability') and Bayes-focused prompts. Measurement: Posterior-odds ratios vs normative; prior-posterior and similarity correlations.
  - Domain/models: Probabilistic reasoning tasks; up to 15 LLMs incl. GPT-4o, GPT-4, Claude-3-Opus, Gemini-1.5-Pro, Mistral-Large, Llama-3-70B; human comparison. Read: partial.
  - Claims: C1 context: base-rate neglect in Bayesian word problems, not critics; C2 context (counterpoint): rewording to 'compute the posterior probability' fixed GPT-4o; all other claims not touched.

- **2503.07003** Large Language Models Often Say One Thing and Do Another (2025). https://arxiv.org/abs/2503.07003
  - Manipulation: Word-based vs deed-based question pairs (opinion, values, theory vs action); chain-of-thought explanations. Measurement: Words-deeds consistency.
  - Domain/models: 1,225 items; 12 models incl. GPT-4-Turbo, GPT-3.5, Llama-2/3, Mistral-7B (ICLR 2025). Read: partial.
  - Claims: C6 context: general words-vs-deeds gap, no judging task; all other claims not touched.

- **2506.21561** Reasoning Isn't Enough: Examining Truth-Bias and Sycophancy in LLMs (2025). https://arxiv.org/abs/2506.21561
  - Manipulation: Reasoning vs non-reasoning models; prompts. Measurement: Truth-bias, truth accuracy vs deception accuracy.
  - Domain/models: Veracity detection, 4,800 judgments; 8 LLMs. Read: abstract only.
  - Claims: C8 context: reasoning models show less truth-bias in veracity judgments (criterion-like), no prior or payoff; all other claims not touched.

- **2509.13332** Explicit Reasoning Makes Better Judges: A Systematic Study on Accuracy, Efficiency, and Robustness (2025). https://arxiv.org/abs/2509.13332
  - Manipulation: Thinking vs non-thinking judges; ICL, rubrics, references, n-best. Measurement: Judge accuracy, FLOPs, bias and robustness.
  - Domain/models: RewardBench; Qwen3 0.6B/1.7B/4B. Read: abstract only.
  - Claims: C5 context: small Qwen3 sizes compared on accuracy; C8 context: thinking vs non-thinking judges (accuracy only); all other claims not touched.

- **2510.17880** Outraged AI: Large language models prioritise emotion over cost in fairness enforcement (2025). https://arxiv.org/abs/2510.17880
  - Manipulation: Unfairness of allocation, stated cost of punishment, emotion self-report prompts. Measurement: Punishment rates, cost sensitivity (GLMMs), emotion-mediation by cost.
  - Domain/models: Third-party punishment; 4,068 LLM agents (GPT-3.5-turbo, o3-mini, DeepSeek-V3, DeepSeek-R1) vs 1,017 humans. Read: partial.
  - Claims: C3 context: stated punishment cost under-used outside critics; C8 context: reasoning models more cost-sensitive; all other claims not touched.

- **2511.10871** From Fact to Judgment: Investigating the Impact of Task Framing on LLM Conviction in Dialogue Systems (2025). https://arxiv.org/abs/2511.10871
  - Manipulation: Factual query vs speaker-correctness framing; rebuttal pressure. Measurement: Accuracy change, sycophantic vs overly critical shifts.
  - Domain/models: Dialogue judging; several LLMs. Read: abstract only.
  - Claims: C4 partly: framing (fact vs speaker correctness) and rebuttals shift judge verdicts; accuracy only; all other claims not touched.

- **2601.05376** The Persona Paradox: Medical Personas as Behavioral Priors in Clinical Language Models (2026). https://arxiv.org/abs/2601.05376
  - Manipulation: Professional persona (ED physician, nurse) and interaction style (bold vs cautious). Measurement: Accuracy, calibration, risk propensity and sensitivity.
  - Domain/models: Clinical triage and patient-safety tasks; several LLMs. Read: abstract only.
  - Claims: C4 context: persona and bold/cautious style shift clinical risk propensity; not a critic; all other claims not touched.

- **2601.19082** Payoff scaling shapes cooperation in LLM agents across languages (2026). https://arxiv.org/abs/2601.19082
  - Manipulation: Payoff scale multiplier (0.01-1000, 10 levels), 5 languages, cooperative vs selfish persona lines. Measurement: Cooperation rates.
  - Domain/models: Iterated prisoner's dilemma; Claude Haiku 4.5, GPT-5.4 Nano, Gemini 3.5 Flash-Lite, Qwen3 235B, Grok 4.20; 200,000 decisions. Read: partial.
  - Claims: C3 context: payoff scale changes cooperation although theory predicts no change; C4 context: persona effect reverses with scale; all other claims not touched.

- **2602.07996** The Judge Who Never Admits: Hidden Shortcuts in LLM-based Evaluation (2026). https://arxiv.org/abs/2602.07996
  - Manipulation: Synthetic metadata cues (source, temporal, age, gender, ethnicity, education) appended to candidate responses. Measurement: Verdict shift rate (VSR) and cue acknowledgment rate (CAR).
  - Domain/models: ELI5 and LitBench pairwise items; GPT-4o, Gemini-2.0-Flash, Gemma-3-27B, Qwen3-235B, Claude-3-Haiku, Llama-3.3-70B. Read: partial.
  - Claims: C6 context: judges' rationales omit the cues that drive verdicts (reverse direction of C6); all other claims not touched.

- **2603.16244** More Rounds, More Noise: Why Multi-Turn Review Fails to Improve Cross-Context Verification (2026). https://arxiv.org/abs/2603.16244
  - Manipulation: Single-pass vs multi-turn cross-context review. Measurement: Recall, false positives, precision, F1.
  - Domain/models: 30 artifacts with 150 injected errors. Read: abstract only.
  - Claims: C4 partly: extra review rounds raise recall and false positives (criterion shift), different manipulation; all other claims not touched.

- **2603.25112** Do LLMs Know What They Know? Measuring Metacognitive Efficiency with Signal Detection Theory (2026). https://arxiv.org/abs/2603.25112
  - Manipulation: Model, temperature, domain. Measurement: Type-2 ROC and z-ROC of token log-probability confidence, meta-I.
  - Domain/models: Factual QA, 224,000 trials; 4 LLMs. Read: abstract only.
  - Claims: C7 context: type-2 ROC and z-ROC from token log-probabilities for QA confidence, not critics; all other claims not touched.

- **2603.29693** Measuring (some aspects of) the metacognition of AI (2026). https://arxiv.org/abs/2603.29693
  - Manipulation: Prompts stating high risk for answering S1, high risk for S2, or no risk (no payoff magnitudes). Measurement: d', c, normalized c', meta-d', M-ratio.
  - Domain/models: Binary sentiment (SST-2), oral vs written, word-depletion detection; GPT-5 (medium reasoning), DeepSeek-V3.2-Exp (non-thinking), Mistral-Medium. Read: partial.
  - Claims: C3 context (counterpoint): GPT-5 shifts SDT c toward the safer answer under stated risk; no magnitudes or optimum; C7 context: meta-d' for LLMs; all other claims not touched.

- **2604.00228** Do Language Models Know When They'll Refuse? Probing Introspective Awareness of Safety Boundaries (2026). https://arxiv.org/abs/2604.00228
  - Manipulation: Phase 1 self-prediction of refusal (yes/no, confidence); Phase 2 actual response in fresh context; strict vs lenient refusal definitions. Measurement: SDT d' and c of self-prediction vs behavior; mismatch rates.
  - Domain/models: 300 requests x paraphrases; Claude Sonnet 4, Sonnet 4.5, GPT-5.2, Llama 3.1 405B. Read: partial.
  - Claims: C6 context: refusal self-prediction vs behaviour with SDT; all other claims not touched.

- **2604.03904** I-CALM: Incentivizing Confidence-Aware Abstention for LLM Selective Answering (2026). https://arxiv.org/abs/2604.03904
  - Manipulation: Announced payoffs r(correct)=+a, r(wrong)=-b, r(abstain)=+g with b in {0,1}, g in {0.2..0.8} and extreme values; ablation without payoffs; confidence elicitation; normative guidance. Measurement: Coverage, false-answer rate, error capture, correct-answer retention, abstention informedness, ECE, Brier.
  - Domain/models: Factual QA (PopQA, TriviaQA, SimpleQA-Verified); GPT-5 mini, Gemini-3.1-Flash-Lite, Llama-3-8B, GPT-4o mini, Qwen3-4B. Read: partial.
  - Claims: C3 context (partial counterpoint): announced abstain payoffs move abstention as expected, an extreme wrong-answer penalty does not; all other claims not touched.

- **2604.16790** Bias in the Loop: Auditing LLM-as-a-Judge for Software Engineering (2026). https://arxiv.org/abs/2604.16790
  - Manipulation: Controlled prompt interventions isolating one presentation cue at a time; repeated runs. Measurement: Judge consistency, sensitivity to bias, accuracy when cue aligns or not.
  - Domain/models: LLM-as-judge for code generation, repair and test generation. Read: abstract only.
  - Claims: C4 partly: prompt cues shift code-judge verdicts toward the cued option; all other claims not touched.

- **2604.24074** How Sensitive Are Safety Benchmarks to Judge Configuration Choices? (2026). https://arxiv.org/abs/2604.24074
  - Manipulation: 12 judge-prompt variants (evaluation structure x instruction framing), one judge. Measurement: Harmful-response rates (no ground truth), ranking stability.
  - Domain/models: HarmBench, 6 targets; Claude Sonnet 4-6 judge. Read: abstract only.
  - Claims: C4 partly: judge-prompt framing shifts harmful-response rates by up to 24 pp; no ground truth; all other claims not touched.

- **2604.28031** Models Recall What They Violate: Constraint Adherence in Multi-Turn LLM Ideation (2026). https://arxiv.org/abs/2604.28031
  - Manipulation: Iterative pressure; restatement probe in forked call; structured checkpointing. Measurement: Knows-but-violates (KBV) rate.
  - Domain/models: DriftBench scientific ideation; 7 models. Read: partial.
  - Claims: C6 context: models restate constraints they violate (8-99%); all other claims not touched.

- **2605.05957** Knowing but Not Correcting: Routine Task Requests Suppress Factual Correction in LLMs (2026). https://arxiv.org/abs/2605.05957
  - Manipulation: Same false claim alone vs embedded in a task request. Measurement: Correction suppression rate.
  - Domain/models: 300 false premises; 8 models (Qwen3.5-Plus to GPT-5.1; Qwen3.5-9B, Llama3.1-8B). Read: partial.
  - Claims: C6 context: knowing but not correcting false premises; all other claims not touched.

- **2605.06161** Are LLM Safety Judges Policy-Invariant? A Three-Principle Stress-Test (2026). https://arxiv.org/abs/2605.06161
  - Manipulation: Certified-equivalent rubric rewrites; strict vs lenient policy wording ('must not' vs 'should avoid'; 'any violation' vs 'clear and significant violations'). Measurement: Verdict flip rates, agreement; no ground-truth error split, no d'.
  - Domain/models: ASSEBench, R-Judge, ATBench; GPT-5.4-mini, Claude-Haiku-4.5, DeepSeek-V3.2, Gemini-3-Flash, GPT-5.6-sol (NeurIPS 2026). Read: partial.
  - Claims: C4 partly: strict vs lenient policy wording flips 32-70% of safety-judge verdicts; flips only; all other claims not touched.

- **2605.14038** Model-Adaptive Tool Necessity Reveals the Knowing-Doing Gap in LLM Tool Use (2026). https://arxiv.org/abs/2605.14038
  - Manipulation: none. Measurement: Hidden-state probes for believed tool necessity vs actual tool calls; verbal yes/no self-reports.
  - Domain/models: Arithmetic and TruthfulQA; Qwen3-8B/4B, Llama-3.1-8B, Llama-3.2-3B (NeurIPS 2026). Read: partial.
  - Claims: C6 context: probe-decoded tool necessity vs tool calls; all other claims not touched.

- **2605.26174** A Universal Cliff and a Design Fingerprint: Cross-Section Defect Detection Under LLM Orchestration (2026). https://arxiv.org/abs/2605.26174
  - Manipulation: Single agent vs invisible 5-worker orchestration; 10 systems incl. 5 Anthropic generations and Opus 4.7 reasoning off vs on; documents and defects fixed. Measurement: Hit rate on defect runs, false-alarm rate on clean catch runs, d', c (log-linear correction, post hoc).
  - Domain/models: 16 cross-section contradictions in 4 long documents; Sonnet 4.5, Opus 4.6, Sonnet 4.6, Opus 4.7 (off/on), GPT-5, Grok-4, Gemini 2.5 Pro, DeepSeek-R1, Llama 3.3 70B. Read: partial.
  - Claims: C4 partly: SDT d'/c of a defect-detecting critic under orchestration (not tone); C5 context: c falls across model generations within one developer (not prior use); C8 partly: reasoning on vs off in one model lowers c (1.29 to 0.96) and raises d' (0.42 to 0.66); no prior or payoff; all other claims not touched.

- **2605.29087** The Chain Holds, the Answer Folds: Trace-Answer Dissociation in Reasoning Models Under Adversarial Pressure (2026). https://arxiv.org/abs/2605.29087
  - Manipulation: Same Qwen3-32B in think vs no_think mode; sustained adversarial pushback. Measurement: Latent-correct rate at behavioural flip; answer-slot token probe.
  - Domain/models: MT-Consistency, MMLU-Pro, GSM8K; Qwen3-32B, GPT-OSS-20B, Gemma-4-31B-it. Read: partial.
  - Claims: C6 context: latent-correct answers not emitted; C7 context: answer-slot token probe; C8 context: think mode widens a trace-answer gap under pushback; all other claims not touched.

- **2606.00467** On the Limits of LLM Adaptability: Impact of Model-Internalized Priors on Annotation Task Performance (2026). https://arxiv.org/abs/2606.00467
  - Manipulation: Aligned definitions, few-shot examples, both, DSPy prompts after zero-shot errors; misaligned definitions from other datasets. Measurement: Rescue/corruption rates, accuracy, AUC, prediction bias (predicted minus true positive rate), verbal confidence.
  - Domain/models: Toxicity/hate detection as zero-shot annotation/LLM-judge; 9 LLMs (Llama 8B/70B, Mistral, Mixtral, DeepSeek-V3, GPT-4o-mini, Qwen-2.5-72B); 5 datasets. Read: partial.
  - Claims: C1 context: added definitions/examples rescue only 34.8% of judge errors (in-context information under-used); C2 context: added instructions have limited corrective power; all other claims not touched.

- **2606.06306** Decomposing Factual Sycophancy in Language Models: How Size and Instruction Tuning Shape Robustness (2026). https://arxiv.org/abs/2606.06306
  - Manipulation: 13 manipulation types; model size and instruction tuning. Measurement: Truth margin vs manipulation sensitivity.
  - Domain/models: Factual sycophancy; 56 open models 0.3B-32B. Read: abstract only.
  - Claims: C5 context: small instruction-tuned models are more manipulation-sensitive (sycophancy); all other claims not touched.

- **2606.07834** Cherry-pick Override: LLM Judges Under-use the Non-Directional Verdicts Their Contract Authorizes (2026). https://arxiv.org/abs/2606.07834
  - Manipulation: Detailed contract specifying Conflicting / Not Enough Evidence vs neutral label wording; fresh-context probe asking whether evidence contains material support and refutation. Measurement: Cherry-pick override (directional overcommitment) rates; probe recognition rates.
  - Domain/models: AVeriTeC (N=285) and VitaminC-Mixed (N=250); GPT-5.6 Terra, Claude Sonnet 5, gpt-oss-120b, Mistral Small 4 + historical panel. Read: partial.
  - Claims: C2 context: a detailed instruction leaves 21-48% overcommitment; C6 partly: judges recognise the conflict when asked afterwards but did not act on it (not a stated lean); all other claims not touched.

- **2606.07874** Safety is Contextual, LLM-Judges Are Not: Navigating the Rigid Priors of Evaluators (2026). https://arxiv.org/abs/2606.07874
  - Manipulation: Added explanations of unfamiliar terms (context) vs irrelevant context; altered safety definitions (s_a swaps categories, s_b stricter, absurd control); reframing as arbitrary classes. Measurement: Prediction flip rates (sensitivity/steerability), accuracy, F1 vs human labels.
  - Domain/models: Binary SAFE/UNSAFE prompt classification; 13 judges incl. 3 safety-specific; MultilingualPrompts (779), NovelPrompts (194), 1,000 Sorry-BENCH. Read: partial.
  - Claims: C1 context: safety judges change ~5% of verdicts where new definitions require >15%; C2 context: definitions stated in context barely steer judges; all other claims not touched.

- **2606.09843** An LLM-Native Psychometric Instrument Reveals a Self-Report--Behavior Gap Across 25 Models (2026). https://arxiv.org/abs/2606.09843
  - Manipulation: none. Measurement: 100-item LLM self-report vs human- and judge-rated behaviour.
  - Domain/models: 25 LLMs, 17 developers. Read: partial.
  - Claims: C6 context: self-report barely tracks behaviour (r = .09); all other claims not touched.

- **2606.11016** Superficial Beliefs in LLM Decision-Making (2026). https://arxiv.org/abs/2606.11016
  - Manipulation: Thinking vs non-thinking modes. Measurement: Stated most-important attribute vs behaviourally inferred driver.
  - Domain/models: Binary profile choices; GPT-5-mini, GPT-5-nano, Qwen3-14B, Ministral-3-14B (COLM 2026). Read: partial.
  - Claims: C6 context: stated decision driver matches behavioural driver 61%; C8 context: thinking changes that agreement; all other claims not touched.

- **2606.12730** Rethinking Psychometric Evaluation of LLMs: When and Why Self-Reports Predict Behavior (2026). https://arxiv.org/abs/2606.12730
  - Manipulation: Session context, identity induction, persona prompting. Measurement: Self-report (TPB vs Big Five) vs behaviour coherence.
  - Domain/models: Risk-taking, sycophancy, honesty, implicit bias; 11 frontier LLMs. Read: partial.
  - Claims: C6 context: self-report/behaviour coherence collapses for context-primed behaviour; all other claims not touched.

- **2606.22974** When Preferences Fail to Become Incentives: A Utility-Behavior Gap in Large Language Models (2026). https://arxiv.org/abs/2606.22974
  - Manipulation: Direct 'max-effort' exhortation; 'world-class' vs 'skilled' role; sponsor-funded outcomes the model rated high vs low utility; harmful causes. Measurement: Pairwise output quality by blind 3-model panel.
  - Domain/models: Essays, grant abstracts, postmortems, translation; 7 models incl. DeepSeek V3.2, GPT-5.4 mini, Qwen3.5 9B; 8,400 judged pairs. Read: partial.
  - Claims: C3 context: offering high-utility incentives does nothing while exhortation works (generation, not judging); C4 context: exhortation and role lines move quality; all other claims not touched.

- **2607.02575** Criterion-Conditional In-Context Learning: Evaluating Criterion-Shift Adaptation in Vision-Language Models (2026). https://arxiv.org/abs/2607.02575
  - Manipulation: Latent binary criterion (zero-tolerance vs significant-only) conveyed only through support-example labels; shots; multi-criterion training. Measurement: Criterion invariance and sensitivity.
  - Domain/models: CC-Bench (3,580 test); GPT-4o, Gemini 2.5 Pro, Qwen2.5-VL 7B/32B, Qwen3-VL-8B, InternVL3.5-8B, LLaVA-OV-1.5-8B. Read: partial.
  - Claims: C1 context: context-specified decision criteria under-used ('rigid boundary bias'); C5 context: 7B to 32B barely changes criterion sensitivity; all other claims not touched.

- **2607.05904** More Convincing, Not More Correct: Self-Play Reward Hacking of Reference-Free LLM Judges (2026). https://arxiv.org/abs/2607.05904
  - Manipulation: Judge commits own answer first vs not; blind solving; self-play training. Measurement: False-positive rate, discrimination (AUROC-like).
  - Domain/models: GSM8K, code, competition math; Qwen3, Llama, Gemma judges. Read: abstract only.
  - Claims: C4 context: judge protocol (commit own answer first) cuts false positives; all other claims not touched.

- **2607.10411** Mitigating LLM Sycophancy in Code Smell Detection Using Evidence-Guided Reasoning Prompts (2026). https://arxiv.org/abs/2607.10411
  - Manipulation: Prompt framings: confirmation bias, contradictory hints, false premises; evidence-guided prompting. Measurement: Decision flip rate, false alignment rate.
  - Domain/models: Code smell detection (MLCQ); LLMs. Read: abstract only.
  - Claims: C4 partly: false-premise framings flip code-smell critic decisions (flip rates); all other claims not touched.

- **2607.13618** STOCKTAKE: Measuring the Gap Between Perception and Action in LLM Agents with a Fair Oracle (2026). https://arxiv.org/abs/2607.13618
  - Manipulation: none. Measurement: Skill score vs exact Bayes-filter oracle on identical observations; graded stated beliefs; knowing-doing rate.
  - Domain/models: 26-week supply-chain POMDP; Claude Sonnet 5, GPT-5.4, DeepSeek-V4-Pro, Grok 4.5. Read: partial.
  - Claims: C1 context: agents scored against an exact Bayes-filter (ideal) oracle; C6 context: knowing-doing gap in a POMDP; all other claims not touched.

- **2608.04415** Social Pressure Breaks Majority Voting in LLM Safety Panels (2026). https://arxiv.org/abs/2608.04415
  - Manipulation: Six simulated peers assert the wrong label (toward unsafe or safe) vs abstain; single 'senior reviewer' authority; wording variants; repair preambles. Measurement: Reviewer and panel false-alarm and harmful-miss rates; no d' or c.
  - Domain/models: Six safety datasets (200 items each); Qwen2.5-7B/32B, Llama-3.1-8B, gemma-2-9B, Mistral-7B, OLMo-2-7B + OpenAI probe. Read: yes.
  - Claims: C4 partly: peer-asserted labels raise safety-judge false alarms 56% to 88% with misses nearly flat; C5 context: Qwen 7B far more pliable than 32B; all other claims not touched.

- **2608.08975** How Can Rhetoric Reward-Hack AI Reviewers? Dissecting Rhetorical Sensitivity in AI-Based Peer Review (2026). https://arxiv.org/abs/2608.08975
  - Manipulation: Rhetorical rewriting in six dimensions; standard vs strict review protocol. Measurement: Overall assessment scores.
  - Domain/models: 4,200 manuscripts from ICLR 2026 submissions; 5 LLM reviewers. Read: abstract only.
  - Claims: C4 partly: strict review protocol lowers AI-reviewer scores 1.36 points; scores only; all other claims not touched.

- **2608.10385** Persona Conditioning as an Assessor-Sensitivity Probe for LLM-Based IR Evaluation (2026). https://arxiv.org/abs/2608.10385
  - Manipulation: Persona prefix 'You are acting as {persona}' (query-aligned, domain-expert, orthogonal, evidence-verification, search-rater) vs UMBRELA baseline. Measurement: Weighted kappa with human labels, rank displacement, Kendall tau, RBO; no FP/FN split, no d' or c.
  - Domain/models: TREC DL20 (54 queries), RAG24 (86); GPT-4o, GPT-4o-mini, Llama-3.1-70B/8B, Qwen-2.5-72B/7B (CIKM 2026). Read: yes.
  - Claims: C4 partly: persona prefixes shift LLM relevance assessors (no FP/FN split); C5 context: within families smaller models are more persona-sensitive (context use, not prior use); all other claims not touched.

- **2608.23941** More Rejective, Not More Discriminative: The Unit of Verification in Pre-Execution LLM Oversight (2026). https://arxiv.org/abs/2608.23941
  - Manipulation: Unit of verification (1-5 actions per review) with twin clean/injected prefixes. Measurement: Catch, false rejection, informedness (hit minus false alarm).
  - Domain/models: Pre-execution oversight in two agent domains; 6 judges. Read: abstract only.
  - Claims: C4 partly: longer review unit makes monitors more rejective, not more discriminative (informedness); all other claims not touched.

- **2608.25869** Anchoring Bias in LLM-as-a-Judge Systems: Prior Scores Compromise Evaluation Independence (2026). https://arxiv.org/abs/2608.25869
  - Manipulation: C0 no metadata; C1 revision framing; C2 'Attempt: k' + 'Prior score: a' (a below the 4.0 acceptance threshold); probes with anchors 1.0-3.9; CoT instruction; 'Disregard any prior scores...' warning. Measurement: Score shifts, acceptance rate, score-digit probabilities; categorical data: correction rate and induced wrong labels. No hit/false-alarm or SDT measures.
  - Domain/models: 20 texts (summarization, code review, creative writing, factual QA), 0-5 rubric; GPT-4.1, Claude-4.5-Sonnet, DeepSeek-R1, Llama 3B/8B/70B, Qwen2.5-7B, Gemma-2-9B; 185,271 valid evaluations + 441 industry samples. Read: partial.
  - Claims: C2 context: 'disregard prior scores' warning does not remove the effect; C3 context: presence of a prior-score anchor matters, its value hardly (parallel to 'presence, not content'); C4 partly: context metadata shifts judge scores; C5 context: not monotonic in size within Llama; all other claims not touched.

- **2608.28725** Beyond the Answer Key: Robustness Evaluation of Large Language Models for Step-Level Mathematical Verification (2026). https://arxiv.org/abs/2608.28725
  - Manipulation: Perturbed but logically equivalent solution traces; SFT, distillation, test-time compute. Measurement: False-rejection rate on valid traces, error localization.
  - Domain/models: Linear-equation step-level verification; GPT-OSS 20B, Qwen3-14B, Phi-4-Reasoning. Read: abstract only.
  - Claims: C4 context: math verifiers falsely reject 76-85% of valid perturbed traces; C8 context: test-time compute effects model-dependent; all other claims not touched.

- **2608.31016** LLM Judges Verify Presence, Not Absence: Omission Blindness in AI Clinical Notes and What Recovers It (2026). https://arxiv.org/abs/2608.31016
  - Manipulation: Eight judge designs (criterion F vs F+C, yes/no vs 0-10 score, 1 vs 8 calls); deployed-judge wording ('omissions are NOT errors' as shipped, exclusion deleted, affirmative instruction to report omissions); GEPA optimisation; reasoning budget; task restructuring. Measurement: Paired discrimination (AUC-like, flawed vs clean twin), single-note detection and false-alarm rates at the design's own rule, Youden J, threshold sweeps.
  - Domain/models: 495 note pairs (293 omissions, 202 commissions, 112 clean twins) + 151-pair held-out set + 261 vendor notes; GPT-family judge, Gemini-family replication. Read: yes.
  - Claims: C4 partly: wording, voting, format and optimisation mostly move the operating point; one affirmative instruction slightly improves discrimination; C7 context: AUC-like paired discrimination; C8 partly: a reasoning budget raises discrimination (0.546 to 0.669); no prior or payoff; all other claims not touched.

- **2609.04270** Reviewer Capability Governs Rejection Targeting, Not Repair Skill: Evidence from LLM Execute-Review-Revise Pipelines (2026). https://arxiv.org/abs/2609.04270
  - Manipulation: Reviewer identity and capability tier (self vs cross-family vs weak). Measurement: Recall, false rejection of correct answers, repair rate.
  - Domain/models: 100 olympiad math problems. Read: abstract only.
  - Claims: C4 context: self-review falsely rejects 35% of own correct answers vs 2% cross-family; C5 context: reviewer capability tiers; all other claims not touched.

- **2609.12439** Debiasing as a Measurement Intervention: Calibrated Ties and Resolution Loss in LLM-as-a-Judge Evaluation (2026). https://arxiv.org/abs/2609.12439
  - Manipulation: (not re-screened). Measurement: n/a.
  - Domain/models: n/a. Read: abstract only.
  - Claims: C4 known paper (not re-screened); all other claims not touched.

- **2609.32616** "You're Right, Let Me Fix It": How LLM Agents Damage Correct Work When Falsely Accused (2026). https://arxiv.org/abs/2609.32616
  - Manipulation: False accusations of failure (5 risk factors) after verified correct work. Measurement: Accusation acceptance, damage to correct work, evidence use.
  - Domain/models: CAVE-Bench, 365 agentic tasks; 14 models. Read: abstract only.
  - Claims: C4 partly: false accusations (presupposed error) drive agents to damage correct work; all other claims not touched.

- **2610.05094** How Much Do LLM-as-a-Judge Design Choices Matter? A Systematic Comparison of Prompt Designs, Rating Scales, and Models (2026). https://arxiv.org/abs/2610.05094
  - Manipulation: Prompt detail (base, short in-context, long in-context), 10 reasoning models, reasoning effort low vs medium. Measurement: Accuracy, leniency (share of errors that are false acceptances), switch rate.
  - Domain/models: 600 Humanity's Last Exam QA pairs (binary correctness); gpt-oss 120b, GPT-5.5, GPT-5.6 Terra, Gemini 3.7 Flash, DeepSeek V4 Pro, Claude Haiku 4.5, Claude Sonnet 5, Kimi K3, Qwen 3.8 27B, GLM-5.3. Read: yes.
  - Claims: C4 partly: detailed judge prompts cut leniency 81% to 52% with accuracy unchanged; C8 partly: reasoning effort (low vs medium) changes neither leniency nor accuracy; no prior or payoff; all other claims not touched.

- **2610.06191** Judged Useless, Queried Anyway: Tool-Using Agents Rarely Turn Their Own Evidence Judgments into Stopping Decisions (2026). https://arxiv.org/abs/2610.06191
  - Manipulation: Stated budget, stated stopping rule, call cost, permission to answer from memory, reasoning mode, running count; harness-enforced integration step. Measurement: Agents' one-word usefulness judgments vs stopping actions.
  - Domain/models: Retrieval with controlled source failures; 7 agents incl. Llama-3.1-8B, Qwen3-32B. Read: partial.
  - Claims: C3 context: stated stopping rule/call cost followed only partly; C6 context: agents judge results useless yet keep querying; C8 context: reasoning mode causes early stops; all other claims not touched.

- **2610.11986** FearCaut-Qwen: Affective Steering in a Vision-Language Model Shifts the Decision Criterion for Hazard Assessment (2026). https://arxiv.org/abs/2610.11986
  - Manipulation: Activation steering along a fear direction. Measurement: SDT d' and c of hazard flags (c=+1.354, d'=1.521 at baseline).
  - Domain/models: Post-earthquake building assessment; Qwen2.5-VL-7B. Read: abstract only.
  - Claims: C4 context: activation steering moves SDT c of a VLM hazard assessor (not a prompt); all other claims not touched.

- **2610.23988** Single-Pass Decision Scores Enable Rapid Classification with Adjustable Thresholds in Medical Multimodal Large Language Models (2026). https://arxiv.org/abs/2610.23988
  - Manipulation: Decision threshold on renormalized yes/no token probabilities. Measurement: AUROC, sensitivity/specificity at chosen operating points.
  - Domain/models: 6 medical imaging datasets; MedGemma, Gemma-3 4B/27B. Read: abstract only.
  - Claims: C7 context: renormalised yes/no token probabilities give AUROC and adjustable thresholds (MLLM clinical classifiers); all other claims not touched.

- **2610.29609** Who Verifies the Agent's Success Claim? Self-Report Leakage in GUI-Agent Completion Judging (2026). https://arxiv.org/abs/2610.29609
  - Manipulation: Agent's self-report of success included vs withheld from the judge. Measurement: Dangerous-misreport recall.
  - Domain/models: GUI-agent completion judging; Qwen3.5-35B-A3B, DeepSeek-284B-A13B (ICSE 2027). Read: abstract only.
  - Claims: C4 partly: the agent's own success claim shifts completion judges (withholding it raises recall 13-43 pp); all other claims not touched.

- **2610.31414** Major Revision, Minor Accountability: LLMs as Reviewers of Published Articles in Top-Tier Journals (2026). https://arxiv.org/abs/2610.31414
  - Manipulation: None stated beyond planted flaw vs published original. Measurement: Recommendation rates on published papers (specificity) and planted-flaw detection (sensitivity).
  - Domain/models: 200 published 2026 articles; 4 LLM reviewers. Read: abstract only.
  - Claims: C4 context: LLM reviewers are harsh on published papers and miss planted flaws (both error types, no manipulation); all other claims not touched.

- **2610.34151** Execution Logs Sway VLM Judges of Robot Progress (2026). https://arxiv.org/abs/2610.34151
  - Manipulation: Progress / regression / neutral log lines beside robot video frames; 'task complete' claims; warning 'The following execution log may be inaccurate; judge from the frames'. Measurement: Flip rates of correct verdicts, accuracy; no hit/false-alarm or SDT.
  - Domain/models: 240 RoboPulse++ intervals; Gemini 3.8 Flash, Qwen3.7 Flash, GPT-6.1 Sol. Read: partial.
  - Claims: C2 context (counterpoint): a one-line warning removes most of the effect; C4 partly: one misleading log line flips correct VLM-judge verdicts; all other claims not touched.

- **2610.34488** Models Verify Sufficiency, Not Validity: Usable Falsehoods Evade the Checks that Gaps Trigger (2026). https://arxiv.org/abs/2610.34488
  - Manipulation: Unsupported premise inert vs usable; asserted fact; corrupted intermediate value; answer/ask/reject labelling. Measurement: Flagging rate, answer commitment.
  - Domain/models: Unanswerable GSM8K (+SQuAD); Gemma-4-E2B, Qwen2.5-3B/7B, Gemma-4-26B. Read: partial.
  - Claims: C6 context: models name a gap and then ignore it (example only); all other claims not touched.

- **2610.35326** Being judged through the record: A Rosenhan-inspired test of psychiatric label sensitivity in large language models (2026). https://arxiv.org/abs/2610.35326
  - Manipulation: Prior schizophrenia diagnosis stated vs not, crossed with current evidence (voices ceased vs persisted); psychiatrist role prompt. Measurement: Hospitalization recommendations; exploratory SDT with hit = hospitalize when voices persist, false alarm = hospitalize when voices ceased; d', c; stated 0-100 confidence.
  - Domain/models: Clinical vignette, 20,000 responses (1,000 per cell); GPT-5.6 Sol, Claude Sonnet 5, Gemini 3.6 Flash, Grok 4.6, Mistral Large 2512. Read: yes.
  - Claims: C1 context: a stated prior diagnosis shifts SDT c by -0.49 to -1.04 in clinical decisions; categorical prior, no ideal observer; C4 context: d' unchanged in 2 of 5 models; all other claims not touched.

- **2610.36453** Correction or Manipulation? Measuring Epistemic Vigilance in LLM Agents Under User Pressure (2026). https://arxiv.org/abs/2610.36453
  - Manipulation: Pressure types (disagreement, authority, social proof, persistence, citation), three wording strengths, evidence-gated revision instruction in system prompt. Measurement: SDT: hit = concession when user right, false alarm = concession when user wrong; d' and c.
  - Domain/models: MMLU-Pro, GPQA-diamond, MATH-500 (~23,000 conversations) + 10,080 account-recovery agent conversations; GPT-6 Luna/Luna Pro, DeepSeek-V3.2, Llama 3.3 70B, Ministral 3B/8B/14B. Read: partial.
  - Claims: C4 partly: an evidence-gating instruction raises c without raising d' (concession judgments); C5 context: no simple size trend (Ministral 3B/8B/14B); C6 context: an agent reports changes it did not make; all other claims not touched.

- **2610.38096** Calculation and rejection diverge in language models tested at known mechanical limits (2026). https://arxiv.org/abs/2610.38096
  - Manipulation: Feasibility-only vs full-answer requests; margins from 0.03% to 30% beyond limits; decline-rule wording; answer format; confidence target; tool; reference sheet. Measurement: Rejection of flawed designs, false alarms on valid designs, statements of violation in accepted replies.
  - Domain/models: Beam collapse and disk burst problems; 12 models, 4,860 calls (+800 stated-limit calls). Read: partial.
  - Claims: C4 context: decline wording helps on original items only; C6 context: models reject infeasible designs when asked only about feasibility but accept them in full answers; all other claims not touched.

- **2610.41391** Comparative Evaluation of LLM-Based Review Paradigms for Academic Paper Quality Assessment (2026). https://arxiv.org/abs/2610.41391
  - Manipulation: Review paradigm (Direct, Anchor, Group, Elo, Swiss), input representation, model; post-hoc threshold set so predicted reject rate equals true 59.5% (not stated to the LLM). Measurement: Score inflation, reject recall, kappa, AUC-ROC, F1.
  - Domain/models: 232 stratified ICLR 2025 submissions (+11,513 replication); GPT-4o-mini, Llama 3.3-70B, GPT-oss-120B. Read: partial.
  - Claims: C1 context: LLM reviewers' accept threshold far above the acceptance base rate; base rate never stated, recalibrated post hoc; all other claims not touched.

## Known papers: new information

- 2609.12439: arXiv comment says accepted at EMNLP 2026.
- 2608.18167 (Adversarial Review): accepted to the ICML 2026 DL4C workshop; screened here as background.
- 2507.11662 (Andrade et al.): v3 (Mar 8, 2026) lists ICLR 2026.
- 2603.12123 (Cross-Context Review): v2 revises the comparisons (no longer significantly ahead of subagent or single same-session review); background.
- First screening of papers listed as unscreened: 2604.16790 Bias in the Loop (related, C4); 2607.23002, 2604.19049, 2608.10729 (background).
- 2605.20745 (VerifySteer) and 2608.10729 cannot be retrieved with the protocol's LLM block: their abstracts never say "LLM" or "language model".

## Gaps and caveats

1. **Stemming cut.** 9,489 main-sweep and 1,280 recency hits were not title-screened because they contain no literal block-A term, or no literal B/C term; they matched through stemming (critical, review, monitoring, verify, sensitive, frame, ...). A paper that uses only unlisted forms (for example "verification" without "verifier", or "evaluator" or "grader" without another A term) reaches screening only through the tier-4 safety net (strong B/C terms) or the targeted and extra queries.
2. **LLM block.** The protocol's `("language model" OR LLM OR LLMs)` misses abstracts that say only "foundation models", "reasoning models", "VLMs" or "PRMs" (two known papers). X15b (block A + strong B/C, no LLM terms, cs.CL/AI/LG) compensates only partly; its first version X15 was malformed (ANDNOT absorbed the date and category filters, so it returned pre-2022 and non-CS records). X15's literal matches were all read anyway, and the corrected X15b added nothing new.
3. **Terms that cannot be searched as intended.** d′ (apostrophe dropped; covered by "signal detection", "d-prime" and a local regex), "specificity" (stems to specific; not harvested, covered by "sensitivity" and T7), "utility" (stems to utilize; T4 re-matched literally).
4. **Title-level screening.** Abstracts were read only for plausible titles (237 of 5,567). Papers with uninformative titles may have been missed.
5. **How full texts were read.** Through the WebFetch tool, i.e. a model's extraction from the arXiv HTML (usually the first 100,000 characters: methods and main results, not always appendices), and by local text extraction from the PDF for two papers without HTML (2610.35326, 2510.17880). Numbers quoted here come from those extractions; check them against the papers before citing. No text aimed at AI readers or reviewers was reported in any fetched page (pages longer than 100,000 characters were not checked past that point).
6. **Recency window.** Only six categories and v1 dates Oct 15 – Nov 6, 2026; the last day or two may not be fully indexed yet (the newest ids seen are 2611.08xxx).
7. **Rate limiting.** HTTP 429 blocks forced long pauses; no query was lost.
8. **Coverage.** arXiv only (peer-reviewed venues and citation chasing are other streams). The API returns metadata for the latest version only.
