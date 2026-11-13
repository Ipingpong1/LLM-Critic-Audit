# Adjacent stream: notes

Run on Nov 6, 2026. Scope: the literatures that are *not* about LLM critics but decide how new and how interpretable C1–C8 are:
1. base-rate, prior and payoff use by LLMs;
2. model-size trends in using in-context information;
3. says-vs-does gaps;
4. thinking modes and judge or verifier behaviour;
5. SDT analyses of LLMs in any task;
6. the human SDT background.

Files:
- `adjacent_query_log.csv`: 95 rows. 85 search queries, of which 80 ran: 71 web searches and 9 OpenAlex queries. 5 failed (2 Semantic Scholar, 3 OpenAlex). The remaining rows are logged lookups (arXiv `id_list`, Crossref and OpenAlex DOI lookups).
- `adjacent_screening.csv`: 96 LLM papers rated background or above. 0 close, 18 related, 78 background.
- `adjacent_background_refs.md`: 76 human-SDT references verified in Crossref by DOI, plus one reply verified inline. Three items aren't in Crossref (Green & Swets 1966, Egan 1975, the Edwards 1968 original), and the source of the term "sluggish beta" is unconfirmed.

**No paper in this stream is close.** None of them tests C1–C8 on an LLM critic, verifier, judge or monitor of artifacts. The closest are payoff and threshold studies in clinical classification and triage, plus SDT studies of LLMs in non-critic tasks.

How I read papers. "Full text" (`full_text_read = yes`) means I fetched the arXiv HTML and asked the fetch tool for methods, models, manipulations and numbers. The tool returns a model-written digest of roughly the first 100k characters. That covers methods and results, but sometimes not late appendices; I note this where it matters. Everything else was read at abstract or search-snippet level, as the screening file says. No fetched page contained instructions aimed at LLM readers that I noticed.

---

## Related papers: what they do and how they bear on each claim

Coverage legend: **covers** = same manipulation and same measurement on LLM critics. **partly** = same idea with a different task, measurement or single condition. **contra** = evidence pointing the other way. **–** = doesn't touch.

### Payoff and cost statements (C3 and the threshold-vs-optimal question)

**Liu, Ding, Barrett, Santamaría-Pang, Dobbins & Lehmann (2026)**, *Misaligned clinical risk classification and cost asymmetry in open-weight LLMs*. arXiv 2609.23999, v3 Oct 2026, submitted to ML4H 2026. https://arxiv.org/abs/2609.23999. Full text read.
- Setup: binary HIGH/LOW diabetes-risk classification (Pima data) with Qwen-2.5-7B/32B and Llama-3.1-8B/70B at temperature 0. The FN:FP cost ratio is stated in the prompt: 11 ratios from 1:20 to 20:1, in 3 phrasings, with and without an "err towards" hint.
- Measurement: operating points (TPR/FPR) from next-token P(HIGH), per-patient log-odds shifts, mirror and coherence tests, and linear probes for risk and cost direction.
- Results: only 2 of 12 model × phrasing combinations move correctly in both cost directions (the two large models, baseline phrasing only). Most shifts are common-mode, i.e. the same direction whichever error is said to be costly. A neutral 1:1 cost line still shifts every model toward LOW. Cost direction is linearly decodable from activations but isn't used downstream.
- Claims: **C3 partly**, and the closest prior result to "models react to the presence of a scoring rule, not its content", in a classifier rather than a critic. C6 partly: it "knows" the cost internally but doesn't act on it, a representation-level analogue rather than a stated manipulation check. C5: – for base rates; for payoffs the larger models do better, the opposite of the pilot's base-rate size trend. C7 partly: operating points from token probabilities, but no ROC or z-ROC. C1, C2, C4, C8: –.

**Yamin, Kelly, Wilder & Horvitz (2026)**, *High-stakes decisions with language models: insights from emergency triage*. arXiv 2608.01361, Aug 2026. https://arxiv.org/abs/2608.01361. Full text read.
- Setup: 576/1,248 triage vignettes with six models, each at three reasoning settings. Models: GPT-5-mini, GPT-5.4, Claude Fable 5, Claude Sonnet 5, DeepSeek V4 Pro/Flash.
- Manipulation: stated FN:FP cost ratios of 1:100 to 100:1, or a stated probability threshold.
- Measurement: sensitivity and false-referral rates, AUROC, and a threshold recovered by a discrete-choice fit on separately elicited probabilities. Compared with the best fixed threshold per ratio.
- Results: errors come from the threshold, not from discrimination (AUROC 0.86–0.99). Small non-reasoning models stay flat whatever cost ratio is stated. Claude models move the right way but compressed. GPT-5.4 tracks the stated ratio. Reasoning effort is the main factor in steerability.
- Claims: **C3 partly** (stated costs are ignored by small non-reasoning models but used by frontier/reasoning ones). C4 partly (the prompt moves the threshold, not AUROC). **C8 partly**: the strongest prior evidence that thinking raises payoff use, though outside critics and without ρ. C1, C2, C5, C6, C7: –.

**Yamin, Tang, Horvitz & Wilder (2026)**, *Can revealed preferences clarify LLM alignment and steering?* arXiv 2605.08556, v2 Sep 2026, with a NeurIPS checklist. https://arxiv.org/abs/2605.08556. Full text read: first 100k of 129k characters, covering methods and main results.
- Setup: four diagnose-or-defer medical tasks with GPT-5 (High/Minimal reasoning), DeepSeek-R1 and Llama-4 Scout. Costs are recovered from elicited P(condition) and choices with a multinomial logit.
- Manipulation: steering by stated FN/FP/defer losses.
- Results: the recovered FN/FP ratio moves the wrong way in 12.5–27% of settings and undershoots in 15–48%. Self-reported cost ratios explain decisions worse than revealed ones: ILFC 24–60% for self-reports vs 61–82% revealed. Reasoning models use probabilities better.
- Claims: **C3 partly**. **C6 partly**: the closest "states one cost, acts on another" result, with costs rather than base rates. C8 partly. C1, C2, C4, C5, C7: –. No FP/FN rates are reported.

**Wang, Zhou, Devic & Fu (2026)**, *Are LLM decisions faithful to verbal confidence?* (RiskEval). arXiv 2601.07767. OpenAlex lists an EMNLP 2026 main DOI, 10.18653/2026.emnlp-main.759, which I didn't confirm on the ACL Anthology. https://arxiv.org/abs/2601.07767. Full text read.
- Setup: answer-or-abstain on HLE, GPQA-Diamond and GSM8K. The system prompt states +1 correct / −λ wrong / 0 abstain, with λ from 0.1 to 100. Ten models, including two thinking variants.
- Comparison: decisions against the Bayes-optimal rule, answer iff confidence ≥ λ/(1+λ).
- Results: abstention stays near zero at high λ and verbal confidence is flat across λ. Policy consistency with the optimal rule on HLE at λ ≥ 10 is 0.12–0.62. Applying the optimal rule to the model's own confidence recovers +0.35 to +0.69 normalized utility. An added instruction to use the confidence when deciding changes almost nothing.
- Claims: **C3 partly**: stated penalty content barely moves the decision threshold. **C2 partly** by analogy: telling the model to use its information doesn't help. **C6 partly**: the stated confidence is informative, but decisions ignore it. C8: thinking variants are only somewhat better, not a controlled comparison. C1, C4, C5, C7: –.

**Mohamadi, Wang & Li (2025)**, *Honesty over accuracy: trustworthy language models through reinforced hesitation*. arXiv 2511.11500. https://arxiv.org/abs/2511.11500. Partly read: the section 2 prompting experiments and the training summary.
- Setup: 11 frontier models on GSM8K, MedQA and GPQA, with a prompt that states +1 / 0 / −λ, λ ∈ {1, 5, 25, 100}.
- Results: abstention stays below 1% and errors above 10%, flat across λ, even though the implied optimal thresholds are 0.5–0.99. Reasoning-tuned models are no better. Training with the ternary reward (Qwen3-1.7B) does move the threshold.
- Claims: **C3 partly**. **C8 partly (contra to Yamin 2608.01361)**: here reasoning doesn't help.

**Zong, Li, Long, Chang, Wu & Hadfield (2026)**, *I-CALM*. arXiv 2604.03904. https://arxiv.org/abs/2604.03904. Abstract only.
- Announced answer/abstain payoffs, bundled with confidence elicitation and normative guidance, lower false answers and route error-prone items to abstention.
- Claims: **C3 contra (weak)**. Prompted payoffs can work as part of a bundle; the payoff line isn't isolated.

### Stated base rates and priors (C1, C2)

**Gupta, Corona, Ge, Wang, Klein, Darrell & Chan (2025)**, *Enough coin flips can make LLMs act Bayesian*. ACL 2025 main, arXiv 2503.04722. https://arxiv.org/abs/2503.04722. Full text read.
- Manipulation: the prompt states a coin bias ("they land on heads X% of the time"), compared with in-context flip demonstrations. Base and instruct models (Gemma-2, Phi, Llama-3.1-8B, Mistral-7B, OLMoE) plus Pythia 70M–12B.
- Measurement: token-probability P(heads), as total variation distance from the stated bias.
- Results: base models mostly ignore the stated bias (P(heads) stays around 0.6–0.8 whatever X is). Instruct models do somewhat better but stay pulled toward their own prior. A few in-context flips outweigh the explicit statement. Pythia scale doesn't improve use of the stated bias.
- Claims: **C1 partly**: the cleanest outside-critic evidence that a *stated* rate is under-used compared with *experienced* evidence, with no SDT or ideal-observer ratio. C5 partly: no size trend. C2: –.

**Li & Rui (2024)**, *Dual traits in probabilistic reasoning of LLMs*. arXiv 2412.11009. https://arxiv.org/abs/2412.11009. Full text read.
- Manipulation: the Jason vignette (CS vs humanities professor) with stated base rates of 75% vs 25%, so the normative posterior-odds ratio is 9. Models: GPT-4o, GPT-4, Claude-3-Opus, Gemini-1.5-Pro, Mistral-Large and Llama-3-70B.
- Results: with representative descriptions the observed odds ratio is 1.0–2.6 instead of 9. On a log scale that is 0–0.43 of the normative shift, roughly ρ-like base-rate neglect. With an uninformative description the ratio is about 9. Rewording the question to "compute" the "posterior probability" lifts GPT-4o to 8.5–11.7.
- Claims: **C1 partly**: under-use of a stated base rate relative to Bayes, in judgment rather than detection. **C2 contra**: an explicit computation framing restored base-rate use here, while "use this as your prior" did nothing for critics. This contrast should be discussed in the paper.

### Model-size trends in using in-context information (C5)

**Wei et al. (2023)**, *Larger language models do in-context learning differently*. arXiv 2303.03846. https://arxiv.org/abs/2303.03846. Abstract only.
- Larger models override semantic priors with flipped in-context labels; small models stick to their priors. Instruction tuning *increases* reliance on priors.
- Claims: **C5 contra** in direction, since there larger models use contrary in-context evidence more. The manipulation differs (demonstrations rather than a stated rate). The instruction-tuning point fits instruct critics ignoring stated rates.

**Yu, Merullo & Pavlick (2023)**, *Characterizing mechanisms for factual recall in language models*. EMNLP 2023, arXiv 2310.15910. https://arxiv.org/abs/2310.15910. Abstract only.
- Larger Pythia/GPT-2 models (up to 2.8B) use in-context counterfactuals less and prefer memorized answers.
- Claims: **C5 partly** (same direction: larger models trust their priors more).

**Fouilhé, Asher & Muller (2026)**, *Memory vs. context?* BlackboxNLP 2026 reproducibility track, arXiv 2609.24238. https://arxiv.org/abs/2609.24238. Abstract only.
- Replicates Yu et al. across 31 models (Pythia, GPT-2, Qwen3, Ministral): larger models favour memory, with large family-level variance. Phrasing alone shifts reliance on memory by up to 80%.
- Claims: **C5 partly**. It also warns that a three-size, one-family trend may not generalize.

**Wei, Huang, Lu, Zhou & Le (2023)**, *Simple synthetic data reduces sycophancy in large language models*. arXiv 2308.03958. https://arxiv.org/abs/2308.03958. Abstract and search summaries.
- Following a user's stated opinion rises with scale (+19.8% from 8B to 62B, +10% from 62B to 540B) and with instruction tuning.
- Claims: **C5 contra**: larger models move *more* with this kind of in-context cue, which is social rather than statistical.

**McKenzie et al. (2023)**, *Inverse scaling: when bigger isn't better*. TMLR, arXiv 2306.09479. https://arxiv.org/abs/2306.09479. Abstract only.
- One named cause of inverse scaling is a preference for memorized sequences over in-context instructions. The task set includes hindsight neglect, i.e. judging a bet by expected value rather than outcome.
- Claims: C5 partly (mechanism), C3 partly (EV judgment). Wei, Kim, Tay & Le (2022, arXiv 2211.02011, background) show most of these trends turn U-shaped at 540B, a caution for C5.

### Says vs does (C6)

**Schmied, Bornschein, Grau-Moya, Wulfmeier & Pascanu (2025)**, *LLMs are greedy agents*. ICLR 2026, arXiv 2504.16078. https://arxiv.org/abs/2504.16078. Abstract and summaries.
- In bandits, models state the correct UCB rationale (about 87%) yet act greedily (about 58%). These figures come from summaries.
- Claims: **C6 partly**: a knowing-doing gap outside critics.

Also bearing on C6, entered above: Yamin et al. 2605.08556 (self-reported vs revealed costs), RiskEval 2601.07767 (confidence vs decisions) and Liu et al. 2609.23999 (cost encoded but unused).

### Thinking and reasoning modes and judge or criterion behaviour (C8)

**Barkett, Long & Thakur (2025)**, *Reasoning isn't enough: examining truth-bias and sycophancy in LLMs*. ICML 2025 listing, arXiv 2506.21561. https://arxiv.org/abs/2506.21561. Abstract and summaries.
- On 4,800 veracity judgments by 8 LLMs, reasoning models show less truth-bias than non-reasoning ones (59% vs 71%). Truth vs deception accuracy is asymmetric for o4-mini, GPT-4.1 and R1.
- Claims: **C8 partly**: reasoning shifts a response bias. Both error types are reported, but there is no prior or payoff manipulation.

**Jayarao, Gupta, Varshney & Dwivedi (2025/2026)**, *Explicit reasoning makes better judges*. arXiv 2509.13332, v2 May 2026. https://arxiv.org/abs/2509.13332. Full text read.
- Qwen3 0.6B/1.7B/4B with thinking on vs off as pairwise RewardBench judges, under position, bandwagon, identity, distraction and verbosity perturbations.
- Results for 4B: thinking raises Chat-Hard accuracy from 60 to 79, Reasoning from 77 to 96, and bias consistency by about 6 points. The gains grow with size.
- Claims: **C8 partly**: same model family as the pilot, but pairwise accuracy only, with no hits or false alarms.

**Servajean & Servajean (2026)**, *Measuring (some aspects of) the metacognition of AI*. arXiv 2603.29693, v4 Sep 2026. https://arxiv.org/abs/2603.29693. Full text read.
- Setup: SST-2 sentiment, oral vs written sentences, and detection of a deleted "the". Models: GPT-5 (reasoning Medium), DeepSeek-V3.2-Exp (non-thinking) and Mistral-Medium.
- Manipulation: one verbal stakes line saying that responding S1 (or S2) is high risk. No magnitudes and no abstention option.
- Measurement: d′, c and c/d′, plus meta-d′.
- Results: GPT-5 moves c the right way in every task (|c| > 0.6). DeepSeek and Mistral are often non-significant. Some d′ changes occur.
- Claims: **C3 contra** for a reasoning frontier model: verbal stakes *do* move c. C4 partly (one line moves c). C8 partly, though not a controlled thinking on/off comparison. Borderline for "close": task C is error detection in text scored with SDT under a stakes line, but the model isn't critiquing generated work.

**Cacioli (2026)**, *LLMs as signal detectors*. arXiv 2603.14893. Already in `known_papers.csv`; added because the full text has new details. https://arxiv.org/abs/2603.14893. Full text read.
- Setup: factual QA with Llama-3-8B (base and instruct) and Mistral-7B. Scores are length-normalised answer log-probabilities.
- Results: liberal vs conservative system prompts produced no graded criterion shift. The conservative prompt caused refusals, a small c shift and lower sensitivity. z-ROC slopes were 0.52–0.84 (instruct 0.52–0.65, base 0.77–0.87), and the unequal-variance model fit best. Instruction tuning shifted c, not sensitivity.
- Claims: **C7 partly** (logprob z-ROC below 1 in LLMs, not critics). The pilot's 0.76–0.92 is close to Cacioli's base-model range and above his instruct range. **C4 contra (weak)**: a strictness line didn't move c gradedly in factual QA, whereas tone moved critics' c strongly.

---

## Strongest prior result per area, and what it means for the claims

### 1. LLMs using stated base rates, priors and payoffs (C1–C3)

**Strongest prior results.**
- Payoffs: Liu et al. 2609.23999. A stated FN:FP cost changes the operating point in the same direction whichever error is said to be costly; only 2 of 12 model-phrasing cells respond correctly. Stated-penalty null results point the same way for answer/abstain decisions: RiskEval 2601.07767 and Mohamadi et al. 2511.11500. So do Yamin et al. 2605.08556 (undershoot or wrong direction) and Huynh et al. 2601.19082 (cooperation depends on payoff scale, which is strategically irrelevant).
- Base rates: Gupta et al. (ACL 2025) find a stated rate largely ignored in favour of the model's prior and in-context evidence. Li & Rui 2412.11009 find posterior-odds shifts of 1–2.6 against a normative 9 when the description is representative.
- Threshold vs Bayes-optimal: only RiskEval tests decisions against an explicit Bayes rule (λ/(1+λ)). Yamin 2608.01361 uses an empirical best threshold. Liu et al. give the p* formula but no per-ratio comparison.
- I found no study, in any task, that states a base rate and scores the LLM's criterion shift against the ideal-observer shift ln(81)/d′. ICL label-prior work (Zhao et al. 2021, Fei et al. 2023, batch calibration, majority-label robustness 2312.16549) concerns *demonstrated*, not stated, label distributions and corrects them post hoc.

**What it means.**
- C1 is novel as stated: critics, SDT, ρ against c*. The broad finding "stated rates are under-used" has partial precedents in vignette judgments and coin flips, which should be cited.
- C3's headline, "react to the presence of a scoring rule, not its content", has a close precedent in Liu et al. in clinical classification with open-weight models. Cite it prominently and frame C3 as extending that pattern to critics, and to base rate vs payoff within the same SDT metric.
- C3 must be scoped. Frontier or reasoning models do follow stated costs and risk: Yamin 2608.01361 (GPT-5.4, reasoning settings) and Servajean (GPT-5). So "payoffs don't work" holds for small open models with thinking off, not in general.
- C2 sits against a contrast: explicit computation wording ("compute the posterior") restored base-rate use for GPT-4o (Li & Rui), and explicit update equations work for large models (Cheng et al. 2606.17657). RiskEval's "use your confidence" line, like the pilot's "use this as your prior", did nothing. So the pilot's C2 null is consistent with exhortation lines failing, not with all instruction failing.

### 2. Model-size trends in in-context information vs priors (C5)

**Strongest prior results.** They conflict.
- Larger models trust memorized priors more and in-context counterfactuals less: Yu et al. 2023, replicated across 31 models with family variance by Fouilhé et al. 2026.
- But larger models override semantic priors with flipped demonstrations more (Wei et al. 2023), follow user opinions more (Wei et al. 2023, sycophancy), and handle payoff direction better (Liu et al. 2609.23999).
- Use of a stated coin bias doesn't change with Pythia scale (Gupta et al. 2025).
- Inverse-scaling trends often turn U-shaped at larger scale (Wei et al. 2022).

**What it means.** C5 (smaller qwen models use the stated prior more) is not predicted by one established law. It agrees with the memory-over-context line and disagrees with the flipped-label and sycophancy lines. It is novel for critics and stated base rates, but evidentially thin (three sizes, one family). The paper should present it as a within-family observation, test a second family, and cite both lines. One plausible bridge: post-training (instruction tuning) increases reliance on priors (Wei et al. 2023), and larger instruct models have stronger default verdict priors.

### 3. Stated vs revealed behaviour (C6)

**Strongest prior results.**
- Yamin et al. 2605.08556: self-reported cost ratios are exaggerated and explain decisions far worse than revealed ratios (ILFC 24–60% vs 61–82%).
- RiskEval: verbal confidence is informative but abstention decisions don't follow it.
- Liu et al.: cost direction is decodable but not used.
- Schmied et al.: a knowing-doing gap in bandits.
- Background: value-action gap (Shen et al., EMNLP 2025), stated vs revealed preferences (Gu et al. 2025), generator-validator inconsistency (Li et al., ICLR 2024).

**What it means.** C6 is a new instance of a well-documented gap, not a new phenomenon. Its novelty is narrow: a manipulation check on critics for base-rate and payoff lean, where one model states the right lean and doesn't act on it while another acts without stating it. Frame it as consistent with this literature and cite Yamin 2605.08556 and RiskEval as the closest.

### 4. Thinking and reasoning modes and judge or verifier behaviour (C8, planned)

**Strongest prior results.**
- For "thinking increases use of stated costs": Yamin et al. 2608.01361. Reasoning effort is the main driver of cost-ratio steerability, and small non-reasoning models stay flat.
- Consistent with it: Servajean 2026 (GPT-5 reasoning moves c with a verbal risk line), Barkett et al. 2025 (reasoning lowers truth-bias), and Jayarao et al. (Qwen3 thinking improves pairwise judge accuracy and robustness).
- Against: Mohamadi et al. 2511.11500 (reasoning-tuned models no more penalty-responsive), MathIF (Fu et al., ACL 2026: longer reasoning lowers instruction adherence, which could dilute a one-line base-rate or payoff instruction), Gema et al. (inverse scaling in test-time compute), and VeriThinker (reasoning models often flag their own correct solutions as wrong, i.e. false alarms in self-verification).
- No study measured base-rate use, ρ or payoff use with thinking on vs off in a critic. No study reported verification false-positive rates by thinking mode with a controlled toggle; only accuracy or bias consistency.

**What it means.** C8 is open. The literature supports a two-sided prediction: thinking may raise payoff and prior use (frontier triage, GPT-5 SDT) or erode adherence and increase over-flagging (MathIF, VeriThinker). Pre-register both.

### 5. SDT analyses of LLMs, including psychology venues

**Strongest prior results.**
- All SDT treatments of LLMs as observers that I found are 2026 arXiv preprints: Cacioli 2603.14893 (temperature as criterion, z-ROC 0.52–0.84) and 2603.25112 (meta-d′); Servajean & Servajean 2603.29693 (c under verbal risk); Ranjan et al. 2607.23927 (reality monitoring, d′ and c).
- In psychology and science journals I found response-bias findings but no formal d′/c analysis of LLMs: Dentella et al. (PNAS 2023, yes-bias in grammaticality judgments) and Hu et al. (PNAS 2024 reply: the bias vanishes with the human prompt). The rest is either SDT applied to *humans* judging LLM output or AI content (Kovesdi et al., HFES 2025; 2605.23426; 2606.28510) or psychophysics of VLMs (contrast sensitivity, *Neural Networks* 2026).
- No hit in *Behavior Research Methods*, *Cognition*, *Cognitive Science*, *Psychological Review*, *Nature Human Behaviour*, *Computational Brain & Behavior*, *Open Mind* or *PB&R* applies SDT to LLM judgments. The coverage caveat is in the gaps below.

**What it means.** An SDT paper on LLM critics with an ideal-observer benchmark would be among the first in a psychology venue. C7 is partly anticipated: logprob-based z-ROC slopes below 1 in factual QA (Cacioli). The critic-specific ROC from verdict logprobs is not. Servajean's GPT-5 result is the main counterpoint to C3.

### 6. Human SDT background (details in `adjacent_background_refs.md`)

**Strongest prior results.**
- Humans shift the criterion in the right direction but not far enough (conservatism). Payoffs are used less well than base rates even when the optimal criterion is identical (Maddox & Bohil 1998; Bohil & Maddox 2001; Maddox & Dodd 2001; Maddox 2002). This is explained by flat maxima and competition between reward and accuracy (COBRA).
- In recognition memory, prior and payoff manipulations moved the cutoff by similar amounts (Healy & Kubovy 1978).
- Without feedback, old/new base rates barely moved hits or false alarms (Estes & Maddox 1995). Awareness and feedback drive base-rate shifts (Rhodes & Jacoby 2007).
- Experienced low prevalence produces large criterion shifts (Wolfe et al. 2007; Levari et al. 2018).
- Recognition z-ROC slopes are about 0.8 (Ratcliff et al. 1992).

**What it means.**
- ρ ≪ 1 is the LLM analogue of conservatism but far more extreme. In feedback-trained categorization, human criteria under unequal base rates are near-optimal (Maddox 2002) or even over-shifted (Maddox 1995). The pilot's 0.04–0.31 is closer to the human *no-feedback, stated or implicit* case (Estes & Maddox 1995). The paper should make this described-vs-experienced distinction explicit, perhaps with an arm that gives feedback or demonstrates the base rate in context.
- The human payoff < base-rate asymmetry parallels C3, so C3 isn't surprising in direction. What's new is that payoffs move LLM criteria in the *wrong* direction.
- The pilot's z-ROC slopes (0.76–0.92) are in the human range, so the equal-variance c* is an approximation and should be flagged. Van Zandt (2000) shows ROC shape can change with how bias is induced, which matters for pooling logprob ROCs across conditions.

---

## Claim-by-claim summary (adjacent literatures only)

| Claim | Status from this stream | Closest prior work |
|---|---|---|
| C1 | Not covered for critics. Partly covered elsewhere: stated rates under-used in coin flips and vignettes, with no ρ or c* | Gupta et al. ACL 2025 (2503.04722); Li & Rui 2412.11009 |
| C2 | Not covered. Contra evidence: explicit computation wording helps in word problems. Consistent: "use your confidence" does nothing | Li & Rui 2412.11009 (contra); RiskEval 2601.07767 (consistent); Cheng et al. 2606.17657 |
| C3 | Partly covered outside critics; scope limits needed | Liu et al. 2609.23999 (direction-agnostic cost response); RiskEval; Mohamadi et al. 2511.11500; Yamin 2605.08556. Contra: Servajean 2603.29693 (GPT-5), Yamin 2608.01361 (frontier/reasoning models), I-CALM |
| C4 | Not covered here (other streams). Adjacent hints only | Cacioli 2603.14893 (strictness prompt, no graded c shift); Servajean 2603.29693 (one line moves c); Yamin 2608.01361 (threshold not AUROC) |
| C5 | Not covered; prior trends conflict | Yu et al. 2023 / Fouilhé et al. 2026 (same direction); Wei et al. 2023 ICL and sycophancy (opposite); Gupta et al. 2025 (no trend) |
| C6 | Partly covered as a general says-vs-does gap; not for critics | Yamin 2605.08556; RiskEval; Liu et al. 2609.23999; Schmied et al. 2504.16078 |
| C7 | Partly covered: logprob z-ROC below 1 in factual QA, not critics | Cacioli 2603.14893; Liu et al. 2609.23999 (operating points only) |
| C8 | Not covered; two-sided prior evidence | Yamin 2608.01361 (reasoning raises steerability); Barkett 2506.21561; Jayarao 2509.13332; contra Mohamadi 2511.11500, MathIF 2505.14810 |

## Leads for other streams

- 2610.23223 (*BayesianPRM: reliability- and conservatism-aware Bayesian belief for PRMs*, Oct 2026). A verifier paper with no prompt manipulation; for the arxiv and peer streams to check.
- Kovesdi et al. (HFES 2025, 10.1177/10711813251368829) proposes SDT for trust in LLM output, which bears on venue fit for a human-factors outlet.
- RiskEval's EMNLP 2026 status (from the OpenAlex DOI) should be confirmed by the peer stream.

## Gaps: what I couldn't search and why

- **Semantic Scholar**: the search API returned HTTP 429 on all attempts (2 queries × 6 tries with 60 s waits, plus one batch-metadata call), so I stopped using it. No S2 relevance search or citation graph from this stream.
- **OpenAlex**: 9 title/abstract queries and 74 DOI abstract lookups ran early on. After that it returned persistent 429s. The 8 planned SDT-of-LLM queries and the 8 queries restricted by ISSN to the psychology venues (BRM, *Cognition*, *Cognitive Science*, *Psych Review*, PNAS, NHB, CBB, *Open Mind*, PB&R, JEP:G, *Communications Psychology*, *Psych Science*, CogSci proceedings) did **not** run. Psychology-venue coverage therefore rests on general web search plus 3 searches restricted to publisher domains. **Recommendation: the chrome stream should run PsycINFO and Scopus for ("language model" OR LLM) AND ("signal detection" OR "response bias" OR "base rate" OR "decision criterion").**
- **arXiv API**: one `id_list` lookup succeeded; the second returned 429. I ran no arXiv searches and left them to the arxiv stream.
- **Web search** returns at most about 10 summarized results per query, so recall per query is limited. No Google Scholar or "cited by" from this stream.
- **Full-text depth**: digests came from arXiv HTML. For 2605.08556, 2609.23999, 2511.11500, 2509.13332 and 2603.29693 only the first 100k characters were covered, so some appendix tables weren't seen. The 2601.14264 HTML returned 404 (abstract only). I couldn't find a full text for the ICLR 2026 poker paper (Ilanyan & Jain); its numbers come from a blog summary and are unverified.
- **Human SDT papers**: no full texts (paywalled). The one-liners rest on abstracts (41 via OpenAlex, a few via web search) or secondary descriptions, marked per entry. Not in Crossref and so not verified: Green & Swets (1966), Egan (1975), the Edwards (1968) original, and the source of the term "sluggish beta".
- **Metadata**: 27 screened rows lack full author lists because the OpenAlex and S2 metadata calls were throttled. Their arXiv ids are given.
- **Not covered**: economics working-paper series (NBER/SSRN) beyond what surfaced, non-English venues, and the Jia et al. (2024) risk-preference framework, which I searched for but didn't find.
