# `citations` stream: notes (Nov 6, 2026)

Citation chasing around the seed papers and ProcessBench, plus author tracking for the five closest papers. Raw responses are in `../raw/citations/` (every HTTP attempt is in `fetch_log.tsv`). Scripts are `../scripts/citations_*.py`, the per-query log is `citations_query_log.csv`, and every paper rated background or above is in `citations_screening.csv`.

**Headline.** Chasing citations out of the Hwang framing paper turned up a cluster of 2026 software-security papers that this project hadn't seen. They test one-line framings, presupposed verdicts and stated error rates on LLM code reviewers and report both error types. Four are close: 2606.30587, 2610.32876, 2603.18740 and 2610.35942. None uses SDT d′/c, ROC or an ideal-observer criterion for verdicts. One (2610.35942) is the first paper I found that tells an LLM reviewer a stated error rate. Its reviewer used the rate, together with the costs in its prompt, almost optimally when deciding how much to check.

## What each source returned

| Source | Used for | What happened |
|---|---|---|
| Semantic Scholar Graph API (no key) | Forward citations of all 10 seeds and ProcessBench; reference lists of the five papers; later hops; title matches | Worked in short windows only: 27 HTTP 200 vs 91 HTTP 429 over 15:15-16:31 (60 s wait after each 429, at most 5 retries per request; `fetch_log.tsv`). Forward lists obtained for 10 of 11 (2604.15224 failed in both passes). References obtained for 4 of 5 (2610.22631 failed; its arXiv HTML list was used). The author-paper endpoint was reached last: 3 of 18 queries returned (Zihan Chen, Di Zhu, Lei Zheng); the rest were not run in time. |
| OpenAlex (no key, no mailto) | Fallback forward citations (`filter=cites:`), author works, reference title lookups | 10 of 11 seed records found (2609.28564 returns 404). Counts far below S2 (ProcessBench 79 vs 362; the 2026 seeds have 0 except Hwang 3 and Jin & Chen 7). Reference lists are empty for most 2026 preprints. At 15:31 the free daily budget for this IP ran out (HTTP 429, resets at midnight UTC), so 12 reference lookups and every later fallback were not run. |
| arXiv API (`export.arxiv.org`) | `au:` queries for all 18 authors (2025-01-01 to today); four `id_list` metadata calls; one abstract search | All returned, spaced at least 12 s apart, with 13 back-offs of 60 s on HTTP 429. |
| arXiv HTML (`arxiv.org/html`) | Reference lists; full texts of candidates | 17 pages. The HTML of 2601.13537 has no rendered bibliography (citation keys only). |
| DBLP search API | Author lists | Returned an Anubis proof-of-work "Making sure you're not a bot" page (HTTP 202) and 429s on the first 12 requests (15:17-15:19). Stopped: solving bot checks is not allowed. |

Instruction found in fetched content: OpenAlex's 429 body tells "an AI agent" it can get a key for its user by POSTing the user's email to an OpenAlex endpoint. Not acted on (no sign-ups, no personal data).

## New close papers

### 1. 2606.30587, Shahriar, Cai, Benkraouda, Wang & Celik, "Words Speak Louder Than Code: Investigating Cognitive Heuristics in LLM-Based Code Vulnerability Detection"

https://arxiv.org/abs/2606.30587 (v2 Oct 15, 2026; accepted at IEEE S&P 2027 per the arXiv comment). Found as a citer of Hwang et al. (2601.13537). Full text read (arXiv HTML v2: methods, results, appendix tables).

- **Critic and data.** Eight LLMs give a binary safe/vulnerable verdict on code (LLaMA 4 Maverick, LLaMA 3.3 70B, DeepSeek V3.1, Qwen3 Coder Next, Mistral Small 3 24B, GPT-5.2, Claude Sonnet 4.6, Gemini 2.5 Pro), at temperature 0.2 with a temperature-0 ablation. The system prompt is a security-reviewer role and answers are JSON only. PrimeVul's paired test split (435 vulnerable functions and their 435 patched versions) gives both error types; CleanVul (vulnerable Java and Python only) gives recall only.
- **Manipulation.** One line of context per condition, each with a pro-safe and a pro-vulnerable polarity, against a neutral instruction:
  - author persona (principal security engineer vs new junior developer; long-time vs first-time contributor);
  - gain-loss consequence framing (a line about avoiding false alarms and pipeline delays vs a line about the damage of a missed vulnerability);
  - goal framing (verify that the code follows secure-coding guidelines vs identify violations);
  - a prior-verdict anchor (marked SAFE/VULNERABLE by an automated analysis; passed/did not pass pre-merge checks).
- **Measurement.** Recall and FPR per condition, the recall gap and FPR gap between polarities, a utility index (recall gain minus FPR gain over neutral), precision, McNemar tests, three reruns. No d′, c, ROC, logprobs or ideal-observer comparison.
- **Findings.**
  - All three manipulations move recall and FPR together. Regressing the FPR gap on the recall gap over the 48 model-heuristic-variant points gives slope 0.994 (r = 0.965); precision stays at 0.49-0.55. The authors call this a "volume knob".
  - Every model moves in the expected direction under framing.
  - The gain frame, which mentions avoiding false alarms, cuts recall by about 25 points below neutral (FPR falls with it); the loss frame stays near neutral (−0.23 points).
  - "Identify violations" raises recall about 16 points above neutral.
  - Only 14 of 48 combinations give a useful shift, none for the three commercial models.
- **Caveat.** At neutral the detectors are close to chance on PrimeVul (LLaMA 4: recall 91.3%, FPR 90.8%; Claude: 73.1% vs 63.5%), so the lockstep partly reflects near-zero discrimination. Our ProcessBench critics have d′ ≈ 2.

### 2. 2610.32876, Liu & Gao, "Trusting the Tool: Asymmetric Deference of LLM Vulnerability Auditors to Static-Analysis Evidence"

https://arxiv.org/abs/2610.32876 (Oct 23, 2026; submitted to IEEE Access). The only S2 citer of 2606.30587 (second hop). Full text read (methods, results RQ1-RQ4, discussion, conclusion).

- **Critic and data.** LLM auditors judge PrimeVul vulnerable/patched C/C++ pairs (916 pairs in four disjoint sets, 16,572 audits). Eleven configurations from four vendors: DeepSeek chat (no reasoning), flash (reasoning) and v4-pro, qwen-plus, plus a registered replication on seven more (GLM-5.2, Kimi K2.6/K3, Qwen3.7-plus/max and others). Temperature 0.
- **Manipulation.** Static-analysis notes beside the code under six conditions:
  - none; all true notes; true notes on the patched operations; true notes elsewhere;
  - fabricated assurances that a check exists, on vulnerable versions;
  - fabricated alarms that a check is missing, on patched versions. This is a presupposed specific flaw.
  - Presentation strategies were also tested, including an instruction to treat notes as unverified and quote the code, and a separate verification call.
- **Measurement.** Recall on vulnerable versions and specificity on patched versions, paired outcomes, and direction-aware assurance and alarm shifts plus their asymmetry, with McNemar tests and bootstrap CIs.
- **Findings.**
  - Models differ mainly in bias, not discrimination.
  - Reasoning shifts the operating point toward suspicion: deepseek-flash flags 69% of functions vs 36% for deepseek-chat without reasoning.
  - True evidence barely helps (+0.02).
  - False assurances lower detection by up to 19 points.
  - False alarms never significantly lower accuracy. Models check them, find the guard and clear the function more often (backfire).
  - The asymmetry replicated on seven new models (mean +0.16, CI +0.10 to +0.24).
  - In-prompt instructions did not reliably help; the best one failed to replicate on held-out pairs.
  - When asked to verify claims in a separate call, the model refutes false assurances about as often as false alarms (0.76 vs 0.79). The model can check claims but doesn't do it in the audit.

### 3. 2603.18740, Alexopoulos, Alexopoulos, Spinellis & Mitropoulos, "When AI Agrees Too Much: Manipulating Automated Code Review via Bias Injection"

https://arxiv.org/abs/2603.18740 (v5 Oct 27, 2026; to appear at ICSE 2027; earlier title "Measuring and exploiting contextual bias in LLM-assisted security code review"). Reference of 2610.32876 (third hop). Read the exploratory study (Sec. III) and parts of the attack study (Sec. IV).

- **Critic and data.** Six LLMs judge CrossVul files (247 vulnerable, 250 patched; PHP, JavaScript, C): GPT-4o-mini, Claude 3.5 Haiku, Gemini 2.0 Flash, DeepSeek V3, Claude Sonnet 4.5 and Opus 4.5, at default temperatures. A second part attacks Claude Code and CodeRabbit review pipelines with crafted PR metadata (33 CVEs).
- **Manipulation.** Five framings of the detection prompt: neutral, weak bug-present ("vulnerabilities may exist"), strong bug-present (asserts the specific vulnerability type), weak bug-free and strong bug-free.
- **Measurement.** Detection rate on vulnerable files and true-negative rate on patched files per framing, two-proportion z-tests, manual validation of justifications and false-positive root causes.
- **Findings.**
  - Bug-free framing collapses detection while raising true negatives (GPT-4o-mini 97.2% to 3.6% under strong bug-free; others −16 to −60 points; Opus −6.9).
  - Bug-present framing barely moves models that already flag 88%+ of patched files at neutral (Claude 3.5 Haiku, the least flag-happy, moves both ways).
  - Blunt template attacks on real pipelines can backfire (they raise suspicion); iteratively refined ones succeed in 32 of 33 cases.
  - As with 2606.30587, the detectors are near chance at neutral.

### 4. 2610.35942, Lijo, "Counting the Bandages: On measuring the time that AI saves"

https://arxiv.org/abs/2610.35942 (Oct 23, 2026; single author). A citer of 2603.18740 (fourth hop). Read Section 7 (the LLM-reviewer experiment), the introduction and the limits; the rest is an economics argument about measuring time saved.

- **Critic and data.** One reviewer (claude-sonnet-5-5 in Claude Code with a single lookup tool) checks claude-haiku-5-5 drafts of three financial figures from 10-Q filings, each with one seeded wrong figure or none. 540 sessions; hypotheses frozen in a repository commit before the main run.
- **Manipulation.** The prompt states the drafter's error rate q, told truthfully at levels from 2% up, or told 3% when the truth is 30%. It also states costs (3 min per lookup, 10 h per escaped error), so checking every line pays above q = 4.5%. One arm adds an instruction to treat track-record claims as unverified.
- **Measurement.** Lookups (0-9) as checking effort, escapes, corrections, and comparison with an optimal-search model and its break-even rate.
- **Findings.**
  - Effort rises with the stated rate (+2.2 lookups per unit of ln q) but is all-or-nothing: 96% of reviews make 0 or 9 lookups.
  - The switch falls between 2% and 5%, next to the 4.5% break-even its prompt implies. Every review at 2% that made at most one lookup wrote the cost comparison out (20 of 20).
  - Told 3% when the truth was 30%, 29 of 40 reviews checked nothing (0 of 40 when told the truth) and 22.5% of briefs shipped a wrong figure.
  - The unverified-claims instruction did not help: 26 of 40 reviews called the 3% figure unverified and then checked nothing.
- **Limits.** One frontier model, explicit cost arithmetic in the prompt, an effort decision rather than a correct/flawed verdict, no false-alarm measure, a small study. It cites Wolfe et al. (2005) on the human low-prevalence effect.

### What the four close papers cover

| Claim | 2606.30587 | 2610.32876 | 2603.18740 | 2610.35942 |
|---|---|---|---|---|
| C1 stated base rate vs ideal observer | Doesn't touch | Doesn't touch | Doesn't touch | **Partly covers, opposite result in a different decision.** A stated error rate drives checking effort to switch near the payoff-implied optimum, for one frontier model. No verdict criterion, d′ or c, and no correct/flawed artifacts judged at a fixed effort. |
| C2 "use the prior" instruction | Doesn't touch | Doesn't touch | Doesn't touch | Doesn't touch (its extra instruction is "treat claims as unverified", which also did nothing) |
| C3 payoffs don't move c the right way | **Partly covers, partly cuts against.** A verbal line stressing the cost of false alarms made every model flag less; the miss-cost line didn't move them. Our pilot found no model became more lenient when told false alarms are costly. | Doesn't touch | Doesn't touch | **Partly cuts against.** With base rate and costs both stated, the reviewer does the expected-cost arithmetic. Payoff content is not varied on its own. |
| C4 one line of tone moves c as far as the base rate; no framing changes skill | **Partly covers the second half.** Framings and anchors move flag rate, not discrimination, for 8 models. No base-rate comparison; no harsh/lenient tone or critic persona. | **Partly covers, with a twist.** A presupposed specific flaw (false alarm) is checked and backfires, while a presupposed absence (false assurance) is followed. Instructions don't fix it. | **Partly covers.** Presupposed-secure framing collapses detection and raises true negatives; presupposed-bug framing hits a ceiling. Both error types, 6 models, no SDT. | Doesn't touch |
| C5 smaller models use the prior more | Doesn't touch | Doesn't touch | Doesn't touch | Doesn't touch |
| C6 says vs does | Doesn't touch (flips cite non-existent bugs) | **Partly related.** Can refute claims when asked, does not check them in the audit. | Doesn't touch | **Contrasts.** Its reviewer states the cost comparison and acts on it. |
| C7 ROC from logprobs | Doesn't touch | Doesn't touch | Doesn't touch | Doesn't touch |
| C8 thinking on/off | Doesn't touch | **Partly covers the idea.** Reasoning moves one auditor's operating point toward flagging without separating versions; not ρ or payoff use. | Doesn't touch | Doesn't touch |

Second and later hops:
- 2606.30587: 85 references screened by title; 1 S2 citer (2610.32876).
- 2610.32876: 71 references; 1 citer (2611.01311, related).
- 2603.18740: 62 references; 8 citers (2610.35942 close; SEVRA-BENCH related; others background).
- 2610.35942: 47 references (Kapetanovic et al. related; FinVerBench background; Sorkin & Woods 1985 and Wolfe et al. 2005 as human background); 0 S2 citers.

The last round (2610.35942) added no new close paper, so I stopped. 2611.01311 (related) was not chased further.

## Related papers

- **2611.01311, Shah, Kakade & Patel, "What Do LLM Judges Actually Verify? Matched Controls and Record Gaps for Document Currency"** (https://arxiv.org/abs/2611.01311, Oct 31; cites 2610.32876). Partly read. Judges check whether cited RFCs are still in force, with matched controls, catches and false alarms, and discrimination (catch minus matched false alarm). Presenting an incomplete record as unverified, or warning it is incomplete, restored most lost catches for Gemini 3.1 Pro, GPT-5.5 and Claude Opus 4.5, but false alarms came back with them. That is a criterion shift from one line of framing. Within qwen2.5 the largest model was no better than the 14B. C4: borderline close; C5: adjacent.
- **2608.25869, Kapetanovic et al., "Anchoring Bias in LLM-as-a-Judge Systems: Prior Scores Compromise Evaluation Independence"** (CIKM 2026; reference of 2610.35942). Abstract only. Prior-score metadata shifts ratings in eight judges. Its threshold-like response means adding the anchor matters more than its value, which parallels our result that payoff lines act by presence, not content (C3). On labelled categorical data it blocks 48% of error corrections and flips 10% of correct judgments.
- **2610.15415, Dong et al., "Sensitivity or Criterion? Measuring and Moving When Language Models Act"** (cites Cacioli). Full text partly read (sections 1-5, App. B.7, C, G).
  - SDT for when-to-act decisions on tool use (FlipAct) across 44 open models up to 70B, including Qwen3.5 0.8B-35B.
  - Within a family sensitivity rises with size (Qwen3 0.34 at 4B to 0.58 at 32B; Qwen3.5 peaks at 9B) and the criterion drifts toward zero; the criterion is a per-model setting, not set by size.
  - Reversed-polarity wordings show Qwen3.5-9B and -27B partly owe their conservative criterion to a preference for the answer token "No". That is worth checking for our Qwen3.5 verdict tokens.
  - Reasoning mode raises sensitivity only in models of 4B and below and moves the criterion toward acting in larger ones; the criterion is moved by steering and distillation, not prompts.
  - Not a critic task. C5/C7/C8: adjacent.
- **2608.23941, Han, Yan & Zhang, "More Rejective, Not More Discriminative: The Unit of Verification in Pre-Execution LLM Oversight"** (cites VerifySteer). Abstract only. With longer review windows, catch and false rejection rise in lockstep; informedness peaks at 1-2 actions (six judges, two domains). Same result as the seed cluster, with a different manipulation (C4 adjacent).
- **2609.27756, Balani & Panda, "Reporting Under Pressure"** (cites Hwang). Full text read. "Brutally critical" framing made one model reject a genuine statistical effect in 29/30 runs (0/30 neutral). Significance-seeking framing overclaimed an underpowered null in 30/30. Borderline close for C4: tone with ground truth, but not a verdict task and no SDT.
- **2606.15610, Usami et al., "LLM Judges Have Dark Current"** (v2; cites Cacioli). Partly read. Pairwise judges under a neutral vs a strict criterion prompt: the strict prompt removes false preferences on exact clones but costs utility (misses become ties). The authors say they cannot separate threshold from resolution. Borderline close for C4.
- **2610.34151, Zhao & Yang, "Execution Logs Sway VLM Judges of Robot Progress"** (CoRL 2026 workshop; cites Xu). Read in full (short). One log line flips correct verdicts 10-35 points more than a matched neutral line, in both directions. A one-line warning removes most of the effect but also the benefit of agreeing logs (C4).
- **2609.00038, Mohammadi, "trajectory-judge"** (NeurIPS 2026 workshop; cites ProcessBench). Partly read. Sensitivity, specificity and paired discrimination for 14B/8B judges under view × instruction ("check each step"); a procedural instruction, not tone (C4 method).
- **2601.14691, Khalifa et al., "Gaming the Judge"** (Findings of EMNLP 2026). Abstract only. Rewritten agent chain-of-thought raises VLM judges' false-positive rates (up to +117% relative); mitigation prompts only reduce it (C4, artifact manipulation).
- **2610.06668, Yang & Wang, "Language models can notice an impossible engineering problem yet still report it as solved."** Abstract only. 11 of 12 failures named the flaw yet reported "solved" (C6-like). A "flawed" status option raised rejection but lowered valid-problem solving (both error types move).
- **2607.10411, Fahad, Asif & Tawhid, "Mitigating LLM Sycophancy in Code Smell Detection..."** (reference of 2610.32876). Abstract only. Confirmation hints and false premises flip up to 72% of decisions; an evidence-first prompt reduces this (C4).
- **2606.13757, Melo et al., "SEVRA-BENCH"** (cites 2603.18740). Abstract only. 15 social-engineering PR framings get vulnerable code approved by 8 review agents (misses only; C4).
- **2508.07805, Hwang et al., "Can You Trick the Grader?"** (Findings of EMNLP 2025) and **2604.06756, Tu, Ni & Bi** (ACL 2026), both references of 2610.22631, abstract only. Persuasive text or reasoning chains raise acceptance of incorrect answers. Larger or stronger judges are not reliably more robust (C4/C5 adjacent).
- **2603.25112, Cacioli** (v3). Abstract only. Logprob type-2 ROC/z-ROC for QA confidence; same machinery as C7, not critics.

Background papers (116) are in the CSV with how far each was read; most were reached from reference lists and read at abstract level or title only.

## Author tracking (2025-2026)

Sources: arXiv `au:` queries (all 18 authors), OpenAlex author works (all 18), DBLP (failed), S2 author API (3 of 18: the 2609.18204 group's Chen, Zhu and Zheng, which confirm the arXiv list).

- **2609.18204 group (Zihan Chen and Di Zhu, Stevens; Lei Nico Zheng, UMass Boston; Weiling Li, Stony Brook).**
  - Since the HICSS paper (Sep 16), Chen, Zheng and Zhu have posted seven more arXiv papers: 2610.27610, 2610.30763, 2610.36422, 2610.38113, 2610.40324, 2611.02623 (Nov 2) and 2611.06696 (Nov 4). Earlier in 2026 they posted 2603.22677, 2605.27864, 2607.26348 and 2609.09321.
  - **None tests criterion-calibration prompts on LLM overseers**, the next step they named. The new papers are about human ratings, prediction markets, prompt-injection reuse, AI art, stated vs revealed preferences in PRISM, and the evidence behind recursive self-improvement claims.
  - 2611.02623 ("Ask More, Hear Less") applies SDT sensitivity/criterion to human online reviews, so they still use SDT framing.
  - The only S2 citer of the overseer paper is 2610.30882 (background).
  - Weiling Li's other papers are on LVLM referential communication.
  - At about one paper a week, a follow-up could appear at any time.
- **2608.16003 (Parsa and Kasra Mazaheri).** Other 2025-26 papers: 2608.15022 (interpretability), 2605.30052 (program-of-thought repair), 2605.20530 (AgentAtlas), 2511.11571 (attention kernels), and the Apple foundation-model report. Nothing on critic criteria. (The Nov 2 check noted an unreported "repairgym" module in their code repository; I did not re-check it.)
- **2610.22631 (Cai, Wang, Yang, Lin, Lee, Yang; Dongwon Lee's group at Penn State).** Anglin Cai, Xiaozhi Yang and Yurun Lin have no other 2025-26 arXiv papers. Zhiqi Wang, Dongwon Lee and Yuchen Yang publish on security, fact-checking, unlearning and refusal steering (e.g., 2602.07013, 2606.21147), but nothing on judge framing or SDT.
- **2603.14893 (Jon-Paul Cacioli).** 21 arXiv papers between Mar 14 and Apr 30, 2026, then OSF/Zenodo pre-registrations and reports. Most are SDT/metacognition of LLM confidence (type-2 AUROC, validity screens, thinking mode compressing confidence, faithfulness-judge confidence, sandbagging). The rest are psychophysics of LLM representations and child-scale language learning. None manipulates a stated base rate, payoff or framing for a critic.
- **2601.13537 (Hwang, Lee, Kang, Lee, Jung; SNU / LG AI Research).** Judge-bias line: 2508.07805, 2505.16222, 2505.15249, 2601.07506, 2410.20774. Later papers move to instruction hierarchy (2607.23545; EMNLP 2026) and survey personas. No SDT or error-type follow-up to the framing paper.

## Gaps

- Semantic Scholar: forward citations of 2604.15224 (Gupta et al.) failed in both passes (OpenAlex also lists 0 citers); references of 2610.22631 failed (its arXiv HTML bibliography was used instead); the keyword search for the He et al. paper and title matches for Koo et al. 2024 and Thornton 2026 failed; 15 of 18 author-paper queries were not run.
- OpenAlex's daily budget for this IP ran out at 15:31 (resets at midnight UTC), so there was no OpenAlex fallback after that, including for all later hops and 12 reference abstracts.
- DBLP was unusable (bot-check page). Author coverage relies on arXiv `au:` queries, which match exact names and miss non-arXiv venues, and on OpenAlex. OpenAlex's 2026 profiles for the 2609.18204 and 2610.22631 authors are new single-paper IDs.
- 2601.13537's arXiv HTML has no bibliography; its reference list comes from S2 (32 entries, some fragments).
- A "He et al. (2026)" paper is cited in 2605.23243 for a confirmation-bias study of LLM vulnerability detection that reportedly measures false-negative vs false-positive bias under benign framing. It is missing from that paper's reference list. An S2 keyword search failed (429), and an arXiv abstract search ("confirmation bias" AND vulnerability, 2025-26) did not find it. If it exists, it is probably close for C4.
- Google Scholar "Cited by" was left to the main session. S2 and OpenAlex index few citations of Aug-Oct 2026 preprints (0-1 citing papers each), so forward coverage of the newest seeds is probably incomplete.
- The security cluster was followed to four hops along citation links only. A keyword search of arXiv cs.CR/cs.SE for "framing", "bias injection", "deference" and "stated error rate" with reviewer, auditor or code review would probably find more.
- Common names (Zihan Chen, Di Zhu, Lei Zheng, Yuchen Yang, Dongwon Lee, Minwoo Lee) return many namesakes; authorship was judged from co-authors and topic.
