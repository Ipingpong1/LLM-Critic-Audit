#!/usr/bin/env python3
"""Write streams/citations_screening.csv (python3 -I). Rows are maintained by hand below."""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "streams", "citations_screening.csv")
COLS = ["id", "title", "authors", "year", "venue_or_status", "source_database", "found_via",
        "relevance", "claims_touched", "manipulation", "measurement", "domain_models",
        "full_text_read", "notes"]

R = []


def add(id, title, authors, year, venue, src, via, rel, claims, manip, meas, dom, ft, notes):
    R.append(dict(zip(COLS, [id, title, authors, year, venue, src, via, rel, claims, manip, meas, dom, ft, notes])))


# ---------------------------------------------------------------- close
add("2606.30587",
    "Words Speak Louder Than Code: Investigating Cognitive Heuristics in LLM-Based Code Vulnerability Detection",
    "Asif Shahriar; Hongyu Cai; Hadjer Benkraouda; Gang Wang; Z. Berkay Celik", "2026", "Accepted at IEEE S&P 2027 (arXiv v2 comment)",
    "Semantic Scholar (citations of 2601.13537); full text via arXiv HTML",
    "forward: cites 2601.13537 (Hwang et al.)", "close", "C3 C4",
    "One context line per condition, two polarities each, vs a neutral instruction: author persona (halo); gain-loss consequence line (benefit of avoiding false alarms vs cost of a missed vulnerability); goal framing (verify adherence vs identify violations); prior-verdict anchor (marked SAFE/VULNERABLE; passed/did not pass pre-merge checks)",
    "Recall and FPR per condition; recall gap and FPR gap between polarities; utility index (recall gain minus FPR gain over neutral); precision, F1; McNemar tests; 3 reruns; regression of FPR gap on recall gap",
    "Binary safe/vulnerable verdict on code: PrimeVul paired test split (435 vulnerable + 435 patched C/C++ functions) and CleanVul (vulnerable-only Java and Python, recall only); 8 models (LLaMA 4 Maverick, LLaMA 3.3 70B, DeepSeek V3.1, Qwen3 Coder Next, Mistral Small 3 24B, GPT-5.2, Claude Sonnet 4.6, Gemini 2.5 Pro); temperature 0.2, ablation at 0",
    "yes",
    "Closest new paper. Every manipulation moves recall and FPR in lockstep (slope 0.994, r=0.965; precision stays 0.49-0.55): the authors call it a volume knob. The gain frame that mentions avoiding false alarms cuts recall about 25 points below neutral, while the loss frame stays near neutral. No d-prime/c, ROC, base-rate arm, ideal observer or thinking manipulation. Detectors are near chance on PrimeVul (recall close to FPR even at neutral), so the lockstep partly reflects near-zero discrimination.")
add("2610.32876", "Trusting the Tool: Asymmetric Deference of LLM Vulnerability Auditors to Static-Analysis Evidence",
    "Zhi-Hong Liu; Shu-Yao Gao", "2026", "Submitted to IEEE Access (arXiv comment)",
    "Semantic Scholar (citations of 2606.30587); full text via arXiv HTML", "second hop: cites 2606.30587", "close", "C4 C6 C8",
    "Static-analysis notes shown with the code under six conditions: none; all true notes; true notes on the patched operations; true notes elsewhere; fabricated assurances that a check exists (vulnerable versions); fabricated alarms that a check is missing (patched versions). Presentation strategies (e.g., instruction to treat notes as unverified and quote the code; separate verification call). Reasoning on vs off for one DeepSeek model",
    "Accuracy on vulnerable versions (recall) and patched versions (specificity); paired outcomes; direction-aware assurance shift, alarm shift and their asymmetry; exact McNemar, bootstrap CIs; LLM-annotated reasons",
    "PrimeVul vulnerable/patched C/C++ function pairs (916 pairs in four disjoint sets, 16,572 audits); 11 configurations from 4 vendors (DeepSeek chat/flash/v4-pro, qwen-plus; registered replication on GLM-5.2, Kimi K2.6/K3, Qwen3.7-plus/max, others)",
    "yes",
    "Second-hop close paper. False alarms (a presupposed specific flaw) did not raise flagging: models checked them and cleared the function more often; false assurances lowered detection by up to 19 points. Asymmetry replicated (mean +0.16 on 7 new models). Models differ mainly in bias, not discrimination; reasoning moved deepseek-flash toward flagging (69% vs 36% flagged without reasoning). In-prompt instructions did not reliably help; the best one failed to replicate. Can-vs-does gap: when asked to verify claims separately the model refutes false assurances (0.76) about as often as false alarms (0.79). No SDT d-prime/c, base rate, payoff or tone.")
add("2603.18740", "When AI Agrees Too Much: Manipulating Automated Code Review via Bias Injection",
    "Georgios Alexopoulos; Nikolaos Alexopoulos; Diomidis Spinellis; Dimitris Mitropoulos", "2026", "To appear at ICSE 2027 (arXiv v5 comment); cited by 2610.32876 under an earlier title",
    "arXiv HTML reference list of 2610.32876; full text via arXiv HTML", "third hop: ref of 2610.32876", "close", "C4",
    "Five one-condition framings of the detection prompt: neutral; weak bug-present (vulnerabilities may exist); strong bug-present (asserts the specific vulnerability type); weak and strong bug-free (code is secure / specific vulnerability types absent). Then crafted PR metadata attacks on real review pipelines",
    "Detection rate on vulnerable files and true-negative rate on patched files per framing; two-proportion z-tests; manual validation of justifications and false-positive root causes; attack success",
    "CrossVul file pairs (247 vulnerable, 250 patched; PHP, JavaScript, C); GPT-4o-mini, Claude 3.5 Haiku, Gemini 2.0 Flash, DeepSeek V3, Claude Sonnet 4.5, Claude Opus 4.5; Claude Code and CodeRabbit pipelines (33 CVEs)",
    "yes",
    "Read the exploratory study (Sec. III) and the attack study (Sec. IV): blunt template attacks on Claude Code and CodeRabbit are ineffective or backfire, iteratively refined PR metadata gets 32 of 33 reintroduced CVEs accepted, and redacting the description restores much detection. Bug-free framing collapses detection (GPT-4o-mini 97.2% to 3.6% under strong bug-free; others -16 to -60 points, Opus -6.9) while raising true negatives; bug-present framing barely moves models already flagging 88%+ of patched files at neutral. A presupposition moves the operating point; no SDT, base rate or ideal observer; detectors near chance at neutral.")

add("2610.35942", "Counting the Bandages: On measuring the time that AI saves", "Solomon Shalom Lijo", "2026", "arXiv preprint (Oct 23 2026)",
    "Semantic Scholar (citations of 2603.18740); full text via arXiv HTML", "third hop: cites 2603.18740", "close", "C1 C3 C6",
    "Stated error rate of the drafter told to an AI reviewer (truthful at several levels from 2% up; and told 3% when the true rate is 30%); prompt states costs (3 min per lookup, 10 h per escaped error, so checking pays above 4.5%); one-line instruction to treat track-record claims as unverified; lookup budget fixed in a calibration experiment",
    "Checking effort (lookups of statement lines, 0-9), escapes of seeded wrong figures, corrections; comparison with an optimal-search model and its break-even error rate; cluster-bootstrap CIs, Holm-corrected pre-specified tests",
    "One reviewer (claude-sonnet-5-5 in Claude Code with a lookup tool) checking claude-haiku-5-5 drafts of revenue, net income and margin from 10-Q filings with one seeded wrong figure or none; 540 sessions",
    "partial",
    "Read Section 7 (the LLM-reviewer experiment), the introduction and limits; the rest is an economics argument about time saved. Effort rises with the stated rate (+2.2 lookups per unit of ln q) but is all-or-nothing (96% of reviews make 0 or 9 lookups), switching between 2% and 5%, next to the 4.5% break-even its prompt implies; reviews at 2% wrote the cost comparison out. Told 3% when the truth was 30%, 29/40 reviews checked nothing (0/40 when told the truth) and 22.5% of briefs shipped an error. The unverified-claims instruction did not help. Effort allocation with explicit costs, not a verdict criterion; one frontier model; no false-alarm measure; small study.")


# ---------------------------------------------------------------- related
add("2610.15415", "Sensitivity or Criterion? Measuring and Moving When Language Models Act",
    "Sixun Dong; Yebowen Hu; Ming Yin; Yi-Ran Chen; Fei Liu; Chen Chen", "2026", "arXiv preprint (Oct 11 2026)",
    "Semantic Scholar; full text via arXiv HTML", "forward: cites 2603.14893 (Cacioli)", "related", "C5 C7 C8",
    "No prompt manipulation beyond five rephrasings and reversed question polarity; criterion moved by activation steering and by distillation from a steered copy; reasoning mode on vs off",
    "SDT on a rule-computed evidence scale: slope of fitted Yes-rate curve (sensitivity) and its crossing (criterion); external d-prime and c on four when-to-act benchmarks; criterion-free AUC",
    "When-to-act decisions about tool use in physical states (FlipAct quads); 44 open models up to 70B incl. Qwen3, Qwen3.5 0.8B-35B, Gemma generations, Mistral-Small",
    "partial",
    "Not a critic task. Within a family sensitivity rises with size (Qwen3.5 peaks at 9B) and the criterion drifts toward zero; criterion is a per-model setting, not set by size. Qwen3.5-9B and -27B answer No under both question polarities (answer-token preference inside the criterion). Reasoning mode raises sensitivity only in models of 4B and below and moves the criterion toward acting in larger ones (Table 19). Read sections 1-5, App. B.7, C, G.")
add("2608.23941", "More Rejective, Not More Discriminative: The Unit of Verification in Pre-Execution LLM Oversight",
    "Yu-Chen Han; Cheng Yan; Wu-Yang Zhang", "2026", "arXiv preprint (Aug 25 2026)",
    "Semantic Scholar", "forward: cites 2605.20745 (VerifySteer)", "related", "C4",
    "Number of planned actions one monitor call reviews (five nested window lengths); twin prefixes with one injected error vs a clean twin",
    "Catch (hit) and false rejection; pre-registered informedness = catch minus false rejection",
    "Pre-execution LLM monitors of agent plans, two domains, six zero-shot judges",
    "no",
    "Abstract only. Longer review raises catch and false rejection in lockstep; informedness peaks at one or two actions. Same SDT-style conclusion as the seed cluster (context moves rejection, not discrimination) with a different manipulation.")
add("2609.27756", "Reporting Under Pressure: Separating Factual and Tonal Sycophancy in LLM Statistical Analysis",
    "P. Balani; Subhrakanta Panda", "2026", "arXiv preprint (Aug 15 2026)",
    "Semantic Scholar; full text via arXiv HTML", "forward: cites 2601.13537 (Hwang et al.)", "related", "C4",
    "Four instruction framings (neutral; honesty; brutally critical, extreme skepticism; significance-seeking) crossed with four ground-truth data patterns (clear effect, confounded, informative null, underpowered null)",
    "LLM-judged factual claim shift and tone-only shift vs a ground-truth interpretation; hedge-word counts; 30 runs per cell (480 responses)",
    "Interpretation of fixed statistical result summaries; one model (not named in the sections read)",
    "yes",
    "Borderline close: tone framing with ground truth. Harsh framing turned a genuine effect into unwarranted skepticism in 29/30 runs vs 0/30 neutral (a false alarm in SDT terms); significance-seeking framing made 30/30 overclaim an underpowered null. Not a correct/flawed verdict task; no hit/false-alarm rates, no SDT, single model.")
add("2606.15610", "LLM Judges Have Dark Current: Stratified Null and Utility Tests for LLM Judge Reliability",
    "Hiroyasu Usami; K. Hara; Ayato Tsuboi; Naohiko Matsuda", "2026", "arXiv preprint (v2 substantially revised; v1 titled ...A Psychometric Datasheet for LLM-as-a-Judge Evaluation)",
    "Semantic Scholar; full text via arXiv HTML", "forward: cites 2603.14893 (Cacioli)", "related", "C4",
    "Neutral vs strict criterion prompt (strict: choose a response only for a material quality advantage, otherwise tie); exact-clone null pairs vs signal pairs",
    "Non-tie preference on exact duplicates (null false preference), target-selection utility, ties, wrong choices; Clopper-Pearson gates",
    "Pairwise judging of RewardBench 2 rows and finite-domain code; Qwen2.5-32B, Qwen3.6-35B, Llama-3.1-8B, Qwen-14B/32B, qwen3.8-flash-next, gpt-oss-120b, nemotron-3-super",
    "partial",
    "Borderline close: a strictness instruction with both error types reported. Strict prompt removes false preferences but also costs utility (Qwen-32B sensitivity at the smallest quality gap .94 to .50, misses become ties). Authors state the design cannot separate threshold movement from resolution change. Pairwise preference with ties, not error detection; strict arm sparse and nonrandomized in the controlled study.")
add("2609.00038", "trajectory-judge: What Outcome-Only LLM Judges Miss on Agent Trajectories",
    "Hadi Mohammadi", "2026", "NeurIPS 2026 workshop Who Verifies the Agents? (poster; arXiv v4 comment)",
    "Semantic Scholar; full text via arXiv HTML", "forward: cites 2412.06559 (ProcessBench)", "related", "C4",
    "Judge view (request and reply only vs full trajectory) crossed with task instruction (judge the reply vs check each step)",
    "Sensitivity and specificity (false-alarm rate on clean runs); paired discrimination = flag rate on faults minus flag rate on their clean parents",
    "Deterministic support-desk agent testbed, 400 trajectories with one injected fault; qwen2.5:14b, llama3.1:8b, self-consistency ensemble",
    "partial",
    "Recall without the clean-parent control credits a judge with detection it lacks; told to check each step, the 14B judge flags every reply-unchanged fault and 0/100 clean runs. Instruction is procedural, not tone or strictness.")
add("2601.14691", "Gaming the Judge: Unfaithful Chain-of-Thought Can Undermine Agent Evaluation",
    "Muhammad Khalifa; Lajanugen Logeswaran; Jaekyeom Kim; Sungryull Sohn; Yunxiang Zhang; Moontae Lee; Hao Peng; Lu Wang; Honglak Lee",
    "2026", "Findings of EMNLP 2026 (OpenAlex DOI 10.18653/2026.findings-emnlp.1636); arXiv Jan 21 2026",
    "Semantic Scholar; OpenAlex", "forward: cites 2412.06559 (ProcessBench)", "related", "C4",
    "Rewriting agent chain-of-thought (style-based and content-based) with actions and observations fixed; manipulation-aware prompting and judge-time scaling as mitigations",
    "False positive rate of judges (up to +117% relative in the venue abstract)",
    "800 web-agent trajectories; VLM judges",
    "no", "Abstract only. Manipulates the evaluated artifact, not the judge prompt; mitigating prompts reduce but do not remove the effect.")
add("2610.06668", "Language models can notice an impossible engineering problem yet still report it as solved",
    "Shao-Liang Yang; Jun Wang", "2026", "arXiv preprint (Oct 5 2026)",
    "Semantic Scholar", "forward: cites 2412.06559 (ProcessBench)", "related", "C6 C4",
    "Reply status options (solved / cannot solve vs flawed plus naming the defect); no warning that problems may be flawed",
    "Rejection of impossible problems and solving of their valid twins scored separately; stated flaw vs reported status",
    "30 pairs of mechanics problems (valid vs made impossible); 14 models",
    "no",
    "Abstract only. In 11 of 12 failures the model stated the flaw yet reported the original as solved (a says/does gap). Offering a flawed status raised rejection in 3 of 4 models but lowered valid-problem solving in 3: both error types move.")
add("2508.07805", "Can You Trick the Grader? Adversarial Persuasion of LLM Judges",
    "Yerin Hwang; Dongryeol Lee; Taegwan Kang; Yongil Kim; Kyomin Jung", "2025", "Findings of EMNLP 2025",
    "arXiv API; OpenAlex", "backward: ref of 2610.22631; authors: Hwang group", "related", "C4 C5",
    "Seven persuasion techniques (majority, consistency, flattery, reciprocity, pity, authority, identity) embedded in otherwise identical math solutions; counter-prompting",
    "Scores assigned to incorrect solutions (inflation up to 8% on average)",
    "Six math benchmarks; several judges of different sizes",
    "no", "Abstract only. Increasing model size does not substantially mitigate; counter-prompting does not remove the effect. Manipulates the artifact, scores only.")
add("2604.06756", "How Long Reasoning Chains Influence LLMs' Judgment of Answer Factuality",
    "M. Tu; S. Ni; K. Bi", "2026", "ACL 2026 Main (arXiv v2 comment)",
    "OpenAlex", "backward: ref of 2610.22631", "related", "C4 C5",
    "Presence vs absence of the answer's reasoning chain; reasoning fluency and factuality",
    "Acceptance of incorrect answers; judgment accuracy by judge strength",
    "Factual QA and math datasets; judges of different capability",
    "no", "Abstract only. Weaker judges accept more incorrect answers when reasoning is shown; stronger judges become more selective.")
add("2603.25112", "Do LLMs Know What They Know? Measuring Metacognitive Efficiency with Signal Detection Theory",
    "Jon-Paul Cacioli", "2026", "arXiv preprint (v3)",
    "Semantic Scholar; arXiv API; OpenAlex", "forward: cites 2603.14893; authors: Cacioli", "related", "C7",
    "Temperature; four models",
    "Type-2 ROC and z-ROC of token-level normalised log-probability; unequal-variance slopes 0.78-1.18; meta-I",
    "Factual QA (TriviaQA, Natural Questions), 224,000 trials, four LLMs", "no",
    "Abstract only (S2 record; v3 recomputed all analyses after a scorer correction, so numbers may differ). Same logprob-ROC machinery as C7 but for answer confidence, not critic verdicts.")
add("2610.34151", "Execution Logs Sway VLM Judges of Robot Progress", "Wei-Yan Zhao; Sunny Yang", "2026", "SPAIS workshop at CoRL 2026 (arXiv comment)",
    "Semantic Scholar; full text via arXiv HTML", "forward: cites 2609.28564 (Xu)", "related", "C4",
    "One appended execution-log sentence (progress claim, regression claim, matched neutral sentence, fake completion claims) beside fixed frames; prompt variants: observe, verify, a one-line warning that the log may be inaccurate",
    "Rate at which correct verdicts flip, minus the neutral-sentence rate, on reversal-consistent intervals; accuracy with agreeing vs contradicting logs",
    "Robot-progress judging on 240 intervals; Gemini 3.8 Flash, Qwen3.7 Flash (reasoning off), GPT-6.1 Sol", "yes",
    "Short paper read in full. A progress line flips correct Falling verdicts 10-35 points more than a neutral line; a regression line has the mirror effect. The one-line warning removes most of the effect but also cuts the gain from logs that agree with the label.")
add("2607.10411", "Mitigating LLM Sycophancy in Code Smell Detection Using Evidence-Guided Reasoning Prompts",
    "I. A. Fahad; K. Asif; Md. N. A. Tawhid", "2026", "arXiv preprint", "arXiv HTML reference list of 2610.32876; arXiv API abstract",
    "third hop: ref of 2610.32876", "related", "C4",
    "Prompt framings: confirmation-bias hints, contradictory hints, false premises; evidence-first debiasing prompt (EGDP)",
    "Decision flip rate (up to 72%), false alignment rate (over 90%)", "Code smell detection, MLCQ dataset", "no", "Abstract only.")

add("2611.01311", "What Do LLM Judges Actually Verify? Matched Controls and Record Gaps for Document Currency",
    "Unnati Shah; Samruddhi Kakade; Aum Patel", "2026", "arXiv preprint (Oct 31 2026)", "Semantic Scholar; arXiv HTML (partly read)",
    "third hop: cites 2610.32876", "related", "C4 C5",
    "Amendment record given to the judge (none, correct, links removed) and its presentation: in force, no replacement recorded, unverified note, warning that the record is incomplete, conflict code; worked examples in the prompt",
    "Right-reason catches of replaced-document citations and false alarms on matched controls (current documents, date controls, decoys); discrimination = catch minus matched false alarm; recall, specificity, precision",
    "IETF RFC index (48 replacements); Gemini 3.1 Pro, GPT-5.5, Claude Opus 4.5, Gemma 4 26B, qwen2.5 at several sizes", "partial",
    "Borderline close. Record gaps cut catches; presenting the record as unverified or warning it is incomplete restored most catches for three judges, but false alarms returned with them (a criterion shift). Within qwen2.5 the largest model did not review better than the 14B one.")
add("2608.25869", "Anchoring Bias in LLM-as-a-Judge Systems: Prior Scores Compromise Evaluation Independence",
    "Ante Kapetanovic; Kemal Altwlkany; Andro Mercep; Tomislav Duricic; Emanuel Lacic", "2026", "CIKM 2026 (arXiv comment)",
    "arXiv API (abstract); found in the reference list of 2610.35942", "third hop: ref of 2610.35942", "related", "C3 C4",
    "No metadata vs revision framing vs anchored metadata with a prior score", "Score shifts toward the anchor; token-level score probabilities; on labelled categorical data, blocked corrections and flipped correct judgments",
    "Eight judges; 20 fixed texts (192,000 evaluations) plus categorical industry data", "no",
    "Abstract only. Adding anchored metadata moves scores in a threshold-like way while the anchor value itself adds little: the presence of the cue matters more than its content, as in our payoff result. A disregard warning did not remove it (per 2610.35942).")
add("2606.13757", "SEVRA-BENCH: Social Engineering of Vulnerabilities in Review Agents",
    "Rui Melo; Riccardo Fogliato; Sean Zhou; Pratiksha Thaker; Zhiwei Steven Wu", "2026", "arXiv preprint (v2)", "Semantic Scholar",
    "third hop: cites 2603.18740", "related", "C4",
    "15 social-engineering PR framings (supporting evidence, urgency, prior approval, authority) around reintroduced vulnerable code",
    "Approval rate of adversarial PRs (misses only)", "About 1,000 adversarial PRs; 8 review agents", "no", "Abstract only.")
add("2605.29586", "FinVerBench: Benchmark Validity and Calibration in Large Language Model Financial Statement Verification", "Silu Panda", "2026",
    "arXiv preprint", "arXiv API (abstract); found in the reference list of 2610.35942", "third hop: ref of 2610.35942", "background", "C4",
    "Prompt (guided checklist) and rendering (rounded vs unrounded statements)", "False positives on clean statements, recall on error-injected ones",
    "SEC 10-K XBRL statements, 14 LLM runs", "no", "Abstract only. Nine of 14 runs flag 95-100% of clean statements under the checklist prompt.")
add("2606.15689", "Bigger Isn't Always Better: A Comparative Evaluation of LLMs for Automated Code Review", "Shivam Pankaj Kumar; Swati Bararia; Kislay Raj",
    "2026", "arXiv preprint", "arXiv API (abstract); found in the reference list of 2610.35942", "third hop: ref of 2610.35942", "background", "C5",
    "", "F1, recall of review comments", "150 code-review samples; Claude Sonnet 4.6 vs Haiku 4.5 and three others", "no", "Abstract only. The smaller Haiku beats Sonnet on recall.")
add("2605.23243", "Are Frontier LLMs Ready for Cybersecurity? Evidence for Vertical Foundation Models from Dual-Mode Vulnerability Benchmarks",
    "Vivek Dahiya; Sunny Nehra; Vipul Dholariya; Bhavik Shangari; Chandra Khatri", "2026", "arXiv preprint (v5)", "Semantic Scholar",
    "third hop: cites 2603.18740", "background", "", "", "False positive rates in white-box detection (10-50%)", "Six frontier and two specialized models", "no",
    "Abstract and citation context only. Its text cites a He et al. (2026) paper on confirmation bias in LLM vulnerability detection that is missing from its reference list; not located (gap).")
add("2610.33509", "Can Agentic Code Review Catch Vulnerabilities Before They Are Merged?", "Yihan Yang; Chenyuan Yang; Zijie Zhao; et al.", "2026",
    "arXiv preprint (v2)", "Semantic Scholar", "third hop: cites 2603.18740", "background", "", "Security harnesses (Codex Security, Defending Code)",
    "Recall on real bug-introducing commits; abstention", "SecPRBench, 265 tasks, eight frontier models", "no", "Abstract only.")
add("2610.05399", "Adaptive Code Revision Attacks on AI Pull Request Reviewers", "Jingzhi Gong; Jie M. Zhang; Gunel Jahangirova; Meng Wang", "2026",
    "arXiv preprint", "Semantic Scholar", "third hop: cites 2603.18740", "background", "", "Feedback-guided code revision by an attacker",
    "Attack success", "159 vulnerabilities; Sonnet 5 and GPT-5.5 reviewers", "no", "Abstract only.")
add("2603.02961", "Delegation and Verification Under AI", "Lingxiao Huang; Wenyang Xiao; Nisheeth K. Vishnoi", "2026", "ICML 2026 (arXiv comment)",
    "arXiv API (metadata); found in the reference list of 2610.35942", "third hop: ref of 2610.35942", "background", "", "", "", "Theory", "no", "Title and metadata only.")


# ---------------------------------------------------------------- background (forward)
add("2610.06522", "Anatomy of LLM Sycophancy: What a Flip Rate Hides", "Hao-Nan Huang", "2026", "arXiv preprint (Oct 5 2026)",
    "Semantic Scholar", "forward: cites 2603.14893", "background", "C4",
    "Pushback wording, committed text, answer format, boundary distance, ground truth", "Flip rates; correction vs capitulation",
    "11 frontier models, about 760,000 replays", "no", "Abstract only. Yes/no readout shows a pressure-induced shift toward no.")
add("2605.06673", "Domain-level metacognitive monitoring in frontier LLMs: A 33-model atlas", "Jon-Paul Cacioli", "2026", "arXiv preprint",
    "Semantic Scholar; arXiv API", "forward: cites 2603.14893; authors: Cacioli", "background", "",
    "", "Type-2 AUROC from verbalized confidence by domain", "MMLU, 33 models", "no", "Abstract only.")
add("2607.11881", "Metacognition in LLMs: Foundations, Progress, and Opportunities",
    "Gabrielle Kaili-May Liu; Areeb Gani; Jacqueline Lu; Thomas; M. Steyvers; Arman Cohan", "2026", "arXiv preprint (survey)",
    "Semantic Scholar", "forward: cites 2603.14893", "background", "", "", "", "Survey", "no", "Abstract only.")
add("2605.28188", "Framing Matters: Addressing Framing Sensitivity in Decision-Making through Behaviorally-Grounded Value Alignment",
    "Seojin Hwang; Minju Kim; Junhyuk Choi; Jeonghyun Park; Hwanhee Lee", "2026", "arXiv preprint",
    "Semantic Scholar", "forward: cites 2601.13537", "background", "C4",
    "Fact-preserving framing (value-tinted narration, temporal slice, vividness)", "Decision flip rate (28.6% average)", "Legal decision-making benchmark (Fragile)", "no",
    "Abstract only. Prompt- and activation-level interventions amplified framing sensitivity.")
add("10.1145/3773078.3841257", "Intent-Description Anchoring Bias in LLM-as-a-Judge Evaluation of Recommender Systems",
    "Himan Abdollahpouri; Kyle Kretschman; Mounia Lalmas", "2026", "ACM RecSys 2026", "OpenAlex", "forward: cites 2601.13537",
    "background", "C4", "Description of the algorithm's optimization objective in the judge prompt", "Diversity scores for identical recommendations",
    "Four frontier LLMs", "no", "Abstract only.")
add("S2:20a3ac71cbb36362a9db33991a00dbfa7c678e33", "Surface or Substance? A Controlled Experiment on How Contextual Signals Sway LLM Peer Review Judgements in CS",
    "(not listed in S2)", "", "Bachelor thesis (no venue or date in S2)", "Semantic Scholar", "forward: cites 2601.13537", "background", "C4",
    "Contextual signals around evaluated papers", "", "LLM peer review", "no", "Title and citation contexts only; no abstract in S2.")
add("2610.38917", "TrussTutor-Bench: Benchmarking large language models on solution accuracy, sycophancy, and error detection in statics",
    "Evangelos Apostolakis; Erfan Hamdi; Sara Jahedazad; Emma Lejeune", "2026", "arXiv preprint (Oct 28 2026)",
    "Semantic Scholar", "forward: cites 2412.06559", "background", "C4",
    "Student insists correct work is wrong (sycophancy pressure)", "Rejection of correct solutions (1.6-50%); detection of injected errors (90-100%)",
    "200 truss problems; 13 LLMs", "no", "Abstract only.")
add("2604.02450", "Do We Need Frontier Models to Verify Mathematical Proofs?", "Aaditya Naik; Guruprerana Shabadi; Rajeev Alur; Mayur Naik",
    "2026", "arXiv preprint", "Semantic Scholar", "forward: cites 2412.06559", "background", "C5",
    "Judging prompt choice; LLM-guided prompt search", "Verifier accuracy and self-consistency", "Human-graded competition proofs; 4 open and 2 frontier models", "no",
    "Abstract only. Accuracy is prompt-sensitive for all models; smaller models more inconsistent.")
add("2609.32622", "Does CoT-Pass@k Really Check the CoT? A Multilingual Mathematical Audit", "Tarik Tuna Tasalti; Burcu Hudaverdi; David Semedo",
    "2026", "MRL workshop at EMNLP 2026 (arXiv comment)", "Semantic Scholar", "forward: cites 2412.06559", "background", "",
    "Deterministic corruptions of chains vs answers", "Acceptance of corrupted chains", "Five multilingual math benchmarks; three judges", "no", "Abstract only.")
add("2606.01462", "An Enigma of Artificial Reason: Investigating the Production-Evaluation Gap in Large Reasoning Models",
    "Ming Sun; Teresa Yeo; Armando Solar-Lezama; Tan Zhi-Xuan", "2026", "arXiv preprint", "Semantic Scholar", "forward: cites 2412.06559",
    "background", "", "", "Grading vs solving accuracy", "VAIR dataset; LRMs and humans", "no", "Abstract only.")
add("2603.25633", "Is Mathematical Problem-Solving Expertise in Large Language Models Associated with Assessment Performance?",
    "Liang Zhang; Yu-Qian Fu; Xin Jin", "2026", "arXiv preprint", "Semantic Scholar", "forward: cites 2412.06559", "background", "C5",
    "", "Solving vs step-level assessment", "ProcessBench GSM8K and MATH; GPT-4, GPT-5", "no", "Abstract only.")
add("2606.09078", "The Hidden Bias of Process Reward Models: PRISM for Rewarding the Right Reasoning",
    "Aakriti Agrawal; Souradip Chakraborty; Armin Saghafian; Nihal Sharma; Rizal Fathony; et al.", "2026", "arXiv preprint",
    "Semantic Scholar", "forward: cites 2412.06559", "background", "", "Training-data imbalance", "PRM false-positive rates and their downstream effect",
    "Math PRMs", "no", "Abstract only.")
add("2512.03109", "E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing",
    "Shuvom Sadhuka; Drew Prinster; Clara Fannjiang; G. Scalia; Bonnie Berger; Aviv Regev; Han-Chen Wang", "2025", "arXiv preprint",
    "Semantic Scholar", "forward: cites 2412.06559", "background", "", "Decision rule on verifier scores", "False alarm rate control", "Agent trajectories", "no", "Abstract only.")
add("2502.06217", "Examining False Positives under Inference Scaling for Mathematical Reasoning",
    "Yu Wang; Nan Yang; Liangying Wang; Furu Wei; Fuli Feng", "2025", "EMNLP 2025", "Semantic Scholar", "forward: cites 2412.06559",
    "background", "", "", "False-positive solutions (right answer, flawed process)", "Math", "no", "Abstract only.")
add("2503.19877", "Scaling Evaluation-Time Compute with Reasoning Models as Evaluators",
    "Seungone Kim; Ian Wu; Jinu Lee; Xiang Yue; Seongyun Lee; et al.", "2025", "Findings of ACL 2026 (arXiv v3 comment)", "Semantic Scholar", "forward: cites 2412.06559",
    "background", "C8", "Reasoning vs non-reasoning evaluators; outcome vs process evaluation", "Evaluator performance", "", "no", "Abstract only.")
add("2510.13744", "Hard2Verify: A Step-Level Verification Benchmark for Open-Ended Frontier Math",
    "Shrey Pandit; Austin Xu; Xuan-Phi Nguyen; Yifei Ming; Caiming Xiong; Shafiq Joty", "2025", "ACL 2026 (per S2 venue)", "Semantic Scholar",
    "forward: cites 2412.06559", "background", "", "", "Step-level verification", "29 critics and PRMs", "no", "Abstract only.")
add("2502.19361", "Can Large Language Models Detect Errors in Long Chain-of-Thought Reasoning?", "Yancheng He; Shilong Li; Jiaheng Liu; et al.",
    "2025", "ACL 2025", "Semantic Scholar", "forward: cites 2412.06559", "background", "", "", "Error detection in long CoT (DeltaBench)", "PRMs and critic models", "no", "Abstract only.")
add("2504.15253", "Evaluating Judges as Evaluators: The JETTS Benchmark of LLM-as-Judges as Test-Time Scaling Evaluators",
    "Yilun Zhou; Austin Xu; Peifeng Wang; Caiming Xiong; Shafiq Joty", "2025", "ICML 2025", "Semantic Scholar", "forward: cites 2412.06559",
    "background", "", "", "Judge performance in reranking, beam search, refinement", "10 judges, 8 generators", "no", "Abstract only.")
add("2610.21244", "System1-Arena: Which Decisions Can Be Left to System 1?", "Tian-Yu Chen; Xin-Yang Liu; Ru-Yi An; Zhen-Dong Wang; Ming-Yuan Zhou",
    "2026", "arXiv preprint", "Semantic Scholar", "forward: cites 2412.06559", "background", "C7 C8",
    "System-1 (single-pass probabilities) vs reasoning models", "Accuracy and calibration of option probabilities (open LLMs read at the answer token)",
    "92k decision questions, 105 tasks; 30 models", "no", "Abstract only.")
add("10.1609/aaai.v40i39.40609", "Rectify Evaluation Preference: Improving LLMs' Critique on Math Reasoning via Perplexity-aware Reinforcement Learning",
    "Changyuan Tian; Zhicong Lu; Shuang Qian; Nayu Liu; Peiguang Li; Li Jin", "2026", "AAAI 2026", "OpenAlex", "forward: cites 2412.06559",
    "background", "", "", "Critic verdicts vs solution perplexity (low-perplexity solutions judged correct)", "Math critique", "no", "Abstract only.")
add("10.1609/aaai.v40i44.41123", "FindTheFlaws: Annotated Errors for Detecting Flawed Reasoning and Scalable Oversight Research",
    "Gabriel L. Recchia; Chatrik Singh Mangat; Issac Yuk-fai Li; G Krishnakumar", "2026", "AAAI 2026", "OpenAlex", "forward: cites 2412.06559",
    "background", "", "", "Critique accuracy", "Five datasets with expert-annotated correct and flawed long-form solutions", "no", "Abstract only.")
add("10.3390/ai7100416", "Understanding Regression in Code Self-Refinement: A Study of Refinement Protocols Without Execution Feedback",
    "Jindae Kim", "2026", "AI (MDPI) 7(10):416", "OpenAlex", "forward: cites 2603.00539 (Jin and Chen)", "background", "",
    "Refinement protocol (direct revision, critique, planning, decision filtering)", "Repairs vs regressions of already-correct code", "Six open-weight models; three Python benchmarks", "no",
    "Abstract only. Critique stages raise repairs but cause many more regressions.")
add("10.18653/2026.findings-emnlp.1634", "Learning to Code by Learning to Verify: Execution-Grounded Co-Evolution of Code Generation and Self-Verification for Reliable Code LLMs",
    "Juyong Jiang; Chansung Park; Jiasi Shen; Sunghun Kim", "2026", "Findings of EMNLP 2026", "OpenAlex", "forward: cites 2603.00539", "background", "C5",
    "", "Generation-verification gap", "Code LLMs", "no", "Abstract only.")
add("2610.30882", "Inherited, Not Invented: Tracing the Provenance of Wait in Reasoning Models",
    "Zhi-Zhuo Kou; Si-Zai Hou; Long Chen; Jian Yang; Junyu Luo; Jing-Shu Peng", "2026", "arXiv preprint (Oct 22 2026)",
    "Semantic Scholar", "forward: cites 2609.18204 (the only S2 citer)", "background", "",
    "Training recipe (RL-Zero, GRPO, SFT) and injected errors", "Frequency and use of the wait marker read as an error alarm (sensitivity and liberalness)",
    "Open reasoning models (OLMo-3, MiMo, others); MATH-500", "no",
    "Abstract only. Cites 2609.18204 for overseers shifting criterion rather than sensitivity; not a critic study.")

add("2610.36010", "CIVER: Causal Intervention Verification for Reliable Code Review",
    "Xin-Yuan Song; H. Haque; Jay Somasundaram; Ryan Turner; Bo-Wen Zhu; Liang Zhao", "2026", "arXiv preprint (Oct 26 2026)",
    "Semantic Scholar", "forward: cites 2603.00539 (Jin and Chen)", "background", "",
    "Repair-oriented perturbations to test review findings", "Share of genuine defects identified; false-positive findings",
    "LLM code-review agents, SWE-Review-Bench", "no", "Abstract only. Motivated by false positives of LLM reviewers.")
add("2607.21656", "Cross-Model LLM Code Review: Should you use Claude to review Codex or vice versa?",
    "Zuo-Dong Xiang; Yi-Ke Zhang; Yue-Ming Zhang; Hai-Lu Xu", "2026", "arXiv preprint (Jul 22 2026)",
    "Semantic Scholar", "forward: cites 2603.00539", "background", "",
    "Writer/reviewer pairing and order (Claude, Codex)", "Pass rate after review without test execution",
    "116 LiveCodeBench tasks", "no", "Abstract only. Codex reviewing Claude drafts lowers pass rate 91.4% to 82.8%: over-correction of correct code.")


# ---------------------------------------------------------------- author tracking (background)
add("2505.16222", "Don't Judge Code by Its Cover: Exploring Biases in LLM Judges for Code Evaluation",
    "Jiwon Moon; Yerin Hwang; Dongryeol Lee; Taegwan Kang; Yongil Kim; Kyomin Jung", "2025", "Findings of EACL 2026 (arXiv comment; OpenAlex)",
    "arXiv API; OpenAlex", "authors: Hwang group", "background", "C4", "Superficial code variations (names, comments, formatting)",
    "Inflated or deflated correctness scores", "Five programming languages; several judges", "no", "Abstract only. Bias persists when told to write tests first.")
add("2601.07506", "Judging Against the Reference: Uncovering Knowledge-Driven Failures in LLM-Judges on QA Evaluation",
    "Dongryeol Lee; Yerin Hwang; Taegwan Kang; Minwoo Lee; et al.", "2026", "arXiv preprint (v2)", "arXiv API; OpenAlex", "authors: Hwang group",
    "background", "", "Swapped (incorrect) reference answers", "Grading reliability", "Reference-based QA judging", "no", "Abstract only.")
add("2505.15249", "Fooling the LVLM Judges: Visual Biases in LVLM-Based Evaluation", "Yerin Hwang; Dongryeol Lee; Kyungmin Min; Taegwan Kang; et al.",
    "2025", "EMNLP 2025 Main (arXiv comment)", "arXiv API; OpenAlex", "authors: Hwang group", "background", "", "Adversarial image manipulations", "Score inflation",
    "Text-image alignment judging (FRAME)", "no", "Abstract only.")
add("10.5281/zenodo.20394748", "Thinking Mode Induces Confidence Compression in Reasoning LLMs: A Pre-Registered Type-2 SDT Analysis",
    "Jon-Paul Cacioli", "2026", "Zenodo report (pre-registered, OSF osf.io/2jwub)", "OpenAlex", "authors: Cacioli", "background", "C8",
    "Thinking vs non-thinking mode", "Type-2 AUROC of logprob confidence", "TriviaQA, three 7-8B reasoning models", "no",
    "Abstract only. Thinking raised accuracy but lowered confidence discrimination; answer confidence, not critic criterion.")
add("10.17605/osf.io/jvtpe", "Do open-weight LLM faithfulness judges have valid confidence?", "Jon-Paul Cacioli", "2026", "OSF registration (Jul 2026)",
    "OpenAlex", "authors: Cacioli", "background", "C5", "Judge scale", "Validity screen of judges' confidence", "RAG faithfulness judges", "no",
    "One-sentence OSF summary only.")
add("10.5281/zenodo.21237442", "Repairing the Know-Say Gap: A No-Finetuning Probe-to-Logit Confidence Controller", "Jon-Paul Cacioli", "2026",
    "Zenodo report (Jul 2026)", "OpenAlex", "authors: Cacioli", "background", "C6", "Probe-to-logit controller", "Verbal vs probe confidence discrimination",
    "TriviaQA, five base models", "no", "Abstract only. A says-vs-knows gap for confidence, not for criterion use.")
add("2604.15702", "The Metacognitive Monitoring Battery: A Cross-Domain Benchmark for LLM Self-Monitoring", "Jon-Paul Cacioli", "2026", "Submitted to NeurIPS 2026 Evaluations and Datasets Track (arXiv comment)",
    "arXiv API; OpenAlex", "authors: Cacioli", "background", "", "", "Withdraw/bet probes; withdraw delta", "524 items, 20 frontier LLMs", "no", "Abstract only.")

# ---------------------------------------------------------------- background (backward references)
def bref(id, title, authors, year, venue, via, notes, claims=""):
    add(id, title, authors, year, venue, "arXiv HTML reference list; Semantic Scholar references where available", via,
        "background", claims, "", "", "", "no", notes)

bref("2604.23478", "JudgeSense: A Benchmark for Prompt Sensitivity in LLM-as-a-Judge Systems", "Rohith Reddy Bellibatlu; Edward Raff; Wenbin Zhang",
     "2026", "arXiv preprint", "backward: ref of 2608.16003",
     "Abstract via OpenAlex. Meaning-preserving rewordings cost judge agreement on 4 tasks, 25 judges; parameter count does not predict stability within a family.", "C4 C5")
bref("10.18653/v1/2025.findings-emnlp.805", "Curse of Knowledge: Your Guidance and Provided Knowledge are biasing LLM Judges in Complex Evaluation",
     "Weiyuan Li; Xintao Wang; Siyu Yuan; et al.", "2025", "Findings of EMNLP 2025", "backward: ref of 2608.16003", "Abstract via OpenAlex.")
bref("2402.13764", "CriticEval: Evaluating Large Language Model as Critic", "Tian Lan; Wenwei Zhang; et al.", "2024", "arXiv preprint",
     "backward: ref of 2608.16003", "Abstract via OpenAlex.")
bref("2402.14809", "CriticBench: Benchmarking LLMs for Critique-Correct Reasoning", "Zicheng Lin; Zhibin Gou; et al.", "2024", "Findings of ACL 2024",
     "backward: ref of 2608.16003", "Abstract via OpenAlex.")
bref("2310.01798", "Large Language Models Cannot Self-Correct Reasoning Yet", "Jie Huang; Xinyun Chen; et al.", "2024", "ICLR 2024",
     "backward: ref of 2608.16003", "Abstract via OpenAlex.")
bref("2306.09896", "Is Self-Repair a Silver Bullet for Code Generation?", "Theo X. Olausson; Jeevana Priya Inala; et al.", "2024", "ICLR 2024",
     "backward: ref of 2608.16003", "Abstract via OpenAlex.")
bref("2404.13076", "LLM Evaluators Recognize and Favor Their Own Generations", "Arjun Panickssery; Samuel R. Bowman; Shi Feng", "2024", "NeurIPS 2024",
     "backward: ref of 2608.16003", "Abstract via OpenAlex.")
bref("2310.13548", "Towards Understanding Sycophancy in Language Models", "Mrinank Sharma; Meg Tong; et al.", "2024", "ICLR 2024",
     "backward: ref of 2608.16003, 2609.18204, 2610.22631", "Abstract via OpenAlex.")
bref("2411.15594", "A Survey on LLM-as-a-Judge", "Jiawei Gu; Xuhui Jiang; et al.", "2024", "arXiv preprint (journal version 2026)",
     "backward: ref of 2608.16003", "Abstract via OpenAlex.")
bref("2306.05685", "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", "Lianmin Zheng; Wei-Lin Chiang; et al.", "2023", "NeurIPS 2023",
     "backward: ref of 2608.16003, 2609.18204, 2610.22631", "Abstract via OpenAlex.")
bref("2305.17926", "Large Language Models are not Fair Evaluators", "Peiyi Wang; Lei Li; et al.", "2024", "ACL 2024",
     "backward: ref of 2609.18204, 2610.22631", "Title and S2 record.")
bref("2305.04388", "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting",
     "Miles Turpin; Julian Michael; Ethan Perez; Samuel Bowman", "2023", "NeurIPS 2023", "backward: ref of 2609.18204, 2610.22631", "Title and S2 record.", "C6")
bref("2410.21819", "Self-Preference Bias in LLM-as-a-Judge", "Koki Wataoka; Tsubasa Takahashi; Ryokan Ri", "2024", "NeurIPS 2024 SafeGenAI workshop",
     "backward: ref of 2609.18204", "Abstract via OpenAlex.")
bref("2212.06823", "Explanations Can Reduce Overreliance on AI Systems During Decision-Making", "Helena Vasconcelos; Matthew Joerke; et al.", "2023",
     "PACM HCI (CSCW 2023)", "backward: ref of 2609.18204", "Abstract via OpenAlex. Human-AI reliance background.")
bref("2006.14779", "Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance", "Gagan Bansal; Tongshuang Wu; et al.",
     "2021", "CHI 2021", "backward: ref of 2609.18204", "Abstract via OpenAlex. Human-AI reliance background (human study).")
bref("10.1177/0018720810376055", "Complacency and Bias in Human Use of Automation: An Attentional Integration", "Raja Parasuraman; Dietrich H. Manzey",
     "2010", "Human Factors 52(3)", "backward: ref of 2609.18204", "Abstract via OpenAlex. Human automation-bias background.")
bref("10.1006/ijhc.1999.0252", "Does automation bias decision-making?", "Linda J. Skitka; Kathleen L. Mosier; Mark Burdick", "1999",
     "Int. J. Human-Computer Studies 51(5)", "backward: ref of 2609.18204", "Title only (no abstract in OpenAlex). Human automation-bias background.")
bref("10.1518/hfes.46.1.50_30392", "Trust in Automation: Designing for Appropriate Reliance", "John D. Lee; Katrina A. See", "2004", "Human Factors 46(1)",
     "backward: ref of 2609.18204", "Title only. Human background.")
bref("10.3758/BF03203619", "Corrections for extreme proportions and their biasing effects on estimated values of d'", "Michael J. Hautus", "1995",
     "Behavior Research Methods, Instruments, & Computers 27(1)", "backward: ref of 2609.18204, 2603.14893", "Title only. SDT method (log-linear correction).")
bref("Macmillan&Creelman-DetectionTheory", "Detection Theory: A User's Guide (2nd ed.; 3rd ed. Hautus, Macmillan & Creelman 2021)",
     "Neil A. Macmillan; C. Douglas Creelman", "2005", "Lawrence Erlbaum (book)", "backward: ref of 2608.16003, 2609.18204, 2603.14893",
     "Title only. Standard SDT text; no DOI recorded.")
bref("GreenSwets1966", "Signal Detection Theory and Psychophysics", "David M. Green; John A. Swets", "1966", "Wiley (book)",
     "backward: ref of 2609.18204, 2603.14893", "Title only.")
bref("10.18653/v1/2025.findings-emnlp.1222", "Challenging the Evaluator: LLM Sycophancy Under User Rebuttal", "S. W. Kim; D. Khashabi", "2025",
     "Findings of EMNLP 2025", "backward: ref of 2610.22631", "Abstract via OpenAlex. Conversational framing of rebuttals shifts evaluators.", "C4")
bref("2509.26072", "The Silent Judge: Unacknowledged Shortcut Bias in LLM-as-a-Judge", "Arash Marioriyad; Mohammad Hossein Rohban; Mahdieh Soleymani Baghshah",
     "2025", "NeurIPS 2025 workshop Reliable ML from Unreliable Data (arXiv journal-ref)", "backward: ref of 2610.22631", "Abstract via OpenAlex. Provenance and recency cues shift pairwise verdicts; justifications never mention them.", "C6")
bref("2606.02578", "Mitigating Perceptual Judgment Bias in Multimodal LLM-as-a-Judge via Perceptual Perturbation and Reward Modeling",
     "S. Park; J. Choi; J. Kang; S. Lee; J. Shin; H. Shim", "2026", "ICML 2026", "backward: ref of 2610.22631", "Abstract via OpenAlex.")
bref("10.18653/v1/2026.acl-long.703", "When Vision-Language Models Judge Without Seeing: Exposing Informativeness Bias",
     "X. Zou; R. Sridhar; M. Safarzadeh; D. Roth", "2026", "ACL 2026", "backward: ref of 2610.22631", "Abstract via OpenAlex.")
bref("2410.02736", "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge", "Jiayi Ye; Yanbo Wang; et al.", "2025", "ICLR 2025",
     "backward: ref of 2610.22631; also ref of 2606.30587", "Abstract via OpenAlex.")
bref("10.18653/v1/2024.emnlp-main.427", "Is LLM-as-a-Judge Robust? Investigating Universal Adversarial Attacks on Zero-shot LLM Assessment",
     "V. Raina; A. Liusie; M. Gales", "2024", "EMNLP 2024", "backward: ref of 2610.22631", "Abstract via OpenAlex.")
bref("10.1109/cvpr52734.2025.00366", "Words or Vision: Do Vision-Language Models Have Blind Faith in Text?", "A. Deng; T. Cao; Z. Chen; B. Hooi",
     "2025", "CVPR 2025", "backward: ref of 2610.22631", "Abstract via OpenAlex.")
bref("10.18653/v1/2025.findings-emnlp.121", "Measuring Sycophancy of Language Models in Multi-turn Dialogues", "J. Hong; G. Byun; S. Kim; K. Shu",
     "2025", "Findings of EMNLP 2025", "backward: ref of 2610.22631", "Abstract via OpenAlex.")
bref("2402.04788", "MLLM-as-a-Judge: Assessing Multimodal LLM-as-a-Judge with Vision-Language Benchmark", "Dongping Chen; Ruoxi Chen; et al.", "2024",
     "ICML 2024", "backward: ref of 2610.22631", "Abstract via OpenAlex.")
bref("StanislawTodorov1999", "Calculation of signal detection theory measures", "H. Stanislaw; N. Todorov", "1999",
     "Behavior Research Methods, Instruments, & Computers 31(1)", "backward: ref of 2610.22631", "Title only. SDT method.")
bref("BartlettMcCarley2017", "Benchmarking aided decision making in a signal detection framework", "M. L. Bartlett; J. S. McCarley", "2017",
     "Human Factors 59(6)", "backward: ref of 2603.14893", "Title only. Human SDT background on aided decisions.")
bref("2207.05221", "Language Models (Mostly) Know What They Know", "Saurav Kadavath; et al.", "2022", "arXiv preprint", "backward: ref of 2603.14893",
     "Title only (reference list).")
bref("10.1016/j.concog.2011.09.021", "A signal detection theoretic approach for estimating metacognitive sensitivity from confidence ratings",
     "B. Maniscalco; H. Lau", "2012", "Consciousness and Cognition 21", "backward: ref of 2603.14893", "Title only. Human SDT background.")
bref("10.3758/BF03194112", "A direct test of the unequal-variance signal detection model of recognition memory", "L. Mickes; J. T. Wixted; P. E. Wais",
     "2007", "Psychonomic Bulletin & Review 14", "backward: ref of 2603.14893", "Title only. Human z-ROC background (C7).", "C7")
bref("2508.10367", "Contrast sensitivity in multimodal large language models: a psychophysics-inspired evaluation", "P. Hernandez-Camara; et al.", "2025",
     "Neural Networks (per S2 venue)", "backward: ref of 2603.14893", "Title only (reference list).")

bref("2504.14045", "Metacognition and uncertainty communication in humans and large language models", "M. Steyvers; M. A. K. Peters", "2025",
     "Current Directions in Psychological Science", "backward: ref of 2603.14893", "Title only (reference list).")
bref("2401.13835", "What large language models know and what people think they know", "M. Steyvers; H. Tejeda; A. Kumar; C. Belem; S. Karny; X. Hu; L. W. Mayer; P. Smyth",
     "2025", "Nature Machine Intelligence 7(2)", "backward: ref of 2603.14893", "Title only (reference list).")
bref("Swets1996", "Signal detection theory and ROC analysis in psychology and diagnostics", "J. A. Swets", "1996", "Lawrence Erlbaum (book)",
     "backward: ref of 2603.14893", "Title only. Human SDT/ROC background (C7).", "C7")
bref("2305.14975", "Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback",
     "K. Tian; et al.", "2023", "EMNLP 2023", "backward: ref of 2603.14893", "Title only (reference list).")

# references of 2601.13537 (from Semantic Scholar; its arXiv HTML has no bibliography)
def href(id, title, authors, year, venue, notes, claims=""):
    add(id, title, authors, year, venue, "Semantic Scholar references (arXiv HTML lacks bibliography)",
        "backward: ref of 2601.13537", "background", claims, "", "", "", "no", notes)

href("2410.20774", "Are LLM-Judges Robust to Expressions of Uncertainty? Investigating the effect of Epistemic Markers on LLM-based Evaluation",
     "Dongryeol Lee; Yerin Hwang; Yongil Kim; Joonsuk Park; Kyomin Jung", "2025", "NAACL 2025",
     "Abstract via S2. Judges penalize outputs carrying uncertainty markers regardless of correctness (EMBER). Hwang group.", "C4")
href("2506.03923", "More or Less Wrong: A Benchmark for Directional Bias in LLM Comparative Reasoning", "Mohammadamin Shafiei; Hamidreza Saffari; N. Moosavi",
     "2025", "arXiv preprint", "Abstract via S2. Framing words steer answers toward the framing term; also cited by 2606.30587.")
href("2412.05579", "LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods", "Haitao Li; Qian Dong; Junjie Chen; et al.", "2024",
     "arXiv preprint", "Abstract via S2. Survey.")
href("2406.18403", "LLMs instead of Human Judges? A Large Scale Empirical Study across 20 NLP Evaluation Tasks", "Anna Bavaresco; Raffaella Bernardi; et al.",
     "2025", "ACL 2025", "Abstract via S2.")
href("2401.06766", "Mind Your Format: Towards Consistent Evaluation of In-Context Learning Improvements", "Anton Voronov; Lena Wolf; Max Ryabinin", "2024",
     "Findings of ACL 2024", "Title and S2 record only.")
href("2401.00595", "State of What Art? A Call for Multi-Prompt LLM Evaluation", "Moran Mizrahi; Guy Kaplan; Dan Malkin; Rotem Dror; Dafna Shahaf; Gabriel Stanovsky",
     "2024", "TACL", "Title and S2 record only; also cited by 2606.30587.")
href("2310.11324", "Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design", "Melanie Sclar; Yejin Choi; Yulia Tsvetkov; Alane Suhr",
     "2024", "ICLR 2024", "Title and S2 record only; also cited by 2606.30587.")
href("2311.09410", "When Large Language Models contradict humans? Large Language Models' Sycophantic Behaviour", "Leonardo Ranaldi; Giulia Pucci", "2023",
     "arXiv preprint", "Title and S2 record only.")
href("Zhou2024-Nature-LessReliable", "Larger and more instructable language models become less reliable", "(authors not given in the S2 reference record)", "2024",
     "Nature", "Title only (S2 reference fragment).", "C5")
href("Brucks2025-PLOSOne", "Prompt architecture induces methodological artifacts in large language models", "(authors not given in the S2 reference record)", "2025",
     "PLoS One", "Title only (S2 reference fragment).")
href("Cheung2025-PNAS", "Large language models show amplified cognitive biases in moral decision-making", "V. Cheung; M. Maier; F. Lieder", "2025",
     "PNAS", "Title only (S2 reference fragment; authors from the 2606.30587 reference list).")
href("Cheng2025-SocialSycophancy", "Social sycophancy: A broader understanding of LLM sycophancy", "(authors not given in the S2 reference record)", "2025",
     "arXiv preprint", "Title only (S2 reference fragment). Published as ELEPHANT (ICLR 2026) per the 2606.30587 reference list.")

# second hop: references of the close paper 2606.30587 (titles from its arXiv HTML bibliography)
def h2(id, title, authors, year, venue, notes, claims=""):
    add(id, title, authors, year, venue, "arXiv HTML reference list of 2606.30587", "second hop: ref of 2606.30587",
        "background", claims, "", "", "", "no", notes)

h2("Koo2024-CoBBLEr", "Benchmarking cognitive biases in large language models as evaluators", "R. Koo; M. Lee; V. Raheja; J. I. Park; Z. M. Kim; D. Kang",
   "2024", "Findings of ACL 2024", "Title only (reference list).", "C4")
h2("2409.16022", "AI Can Be Cognitively Biased: An Exploratory Study on Threshold Priming in LLM-Based Batch Relevance Assessment",
   "N. Chen; J. Liu; X. Dong; Q. Liu; T. Sakai; X. Wu", "2024", "SIGIR-AP 2024", "Abstract via S2 title match. Judges score later documents lower after highly relevant earlier ones and vice versa (GPT-3.5, GPT-4, LLaMa2-13B/70B; TREC DL 2019).", "C4")
h2("2508.17361", "Trust Me, I Know This Function: Hijacking LLM Static Analysis using Bias", "S. Bernstein; D. Beste; D. Ayzenshteyn; L. Schonherr; Y. Mirsky",
   "2026", "NDSS 2026", "Abstract via S2 title match. Familiar-pattern edits make code LLMs overlook small bugs, even when warned in the system prompt.")
h2("2602.16741", "Can adversarial code comments fool AI security reviewers - large-scale empirical study of comment-based attacks and defenses against LLM code analysis",
   "S. Thornton", "2026", "arXiv preprint", "Title only (reference list).")
h2("2509.13400", "Justice in Judgment: Unveiling (Hidden) Bias in LLM-assisted Peer Reviews", "S. S. M. Vasu; I. Sheth; H. Wang; R. Binkyte; M. Fritz",
   "2025", "NeurIPS 2025 workshop (as cited); S2 lists ACL", "Abstract via S2 title match. Author-metadata interventions; strong affiliation bias in LLM reviews.")
h2("2202.12299", "Capturing Failures of Large Language Models via Human Cognitive Biases", "E. Jones; J. Steinhardt", "2022", "NeurIPS 2022",
   "Abstract via S2 title match. Cognitive-bias-inspired failure probes (framing, anchoring) in code generation.")
h2("2308.00225", "Instructed to Bias: Instruction-Tuned Language Models Exhibit Emergent Cognitive Bias", "I. Itzhak; G. Stanovsky; N. Rosenfeld; Y. Belinkov",
   "2024", "TACL", "Abstract via S2 title match. Instruction tuning and RLHF increase decoy, certainty and belief biases.")
h2("Echterhoff2024-FindingsEMNLP", "Cognitive bias in decision-making with LLMs", "J. M. Echterhoff; Y. Liu; A. Alessa; J. McAuley; Z. He", "2024",
   "Findings of EMNLP 2024", "Title only (reference list).")
h2("2402.09193", "(Ir)rationality and cognitive biases in large language models", "O. Macmillan-Scott; M. Musolesi", "2024", "arXiv preprint",
   "Title only (reference list).")
h2("2402.08113", "Addressing cognitive bias in medical language models", "S. Schmidgall; et al.", "2024", "arXiv preprint", "Title only (reference list).")
h2("Ding2025-PrimeVul", "Vulnerability detection with code language models: how far are we?", "Y. Ding; Y. Fu; O. Ibrahim; C. Sitawarin; X. Chen; B. Alomair; D. Wagner; B. Ray; Y. Chen",
   "2025", "ICSE 2025", "Title only (reference list). PrimeVul paired benchmark used by 2606.30587.")
h2("Fanous2025-SycEval", "SycEval: evaluating LLM sycophancy", "A. Fanous; J. Goldberg; A. Agarwal; J. Lin; A. Zhou; S. Xu; V. Bikia; R. Daneshjou; S. Koyejo",
   "2025", "AIES 2025", "Title only (reference list).")

# second/third hop: references of 2610.32876 and 2603.18740
def h3(id, title, authors, year, venue, via, notes, claims=""):
    add(id, title, authors, year, venue, "arXiv HTML reference lists (second/third hop)", via, "background", claims, "", "", "", "no", notes)

h3("2607.24964", "ALIBI: Adaptive Agentic Attacks on LLM-Based Vulnerability Detectors via Adversarial Code Comments", "Z. Wu; C. Nita-Rotaru", "2026",
   "arXiv preprint", "ref of 2610.32876", "Abstract via arXiv API. Prompt-level defenses give limited robustness; isolating comments works better.")
h3("2610.06366", "Correct Verdicts, Flawed Reasoning: Structured Auditing of LLM-based Vulnerability Reasoning", "B. C. Hu; K. Ahir; R. Ni; L. Jia", "2026",
   "arXiv preprint", "ref of 2610.32876", "Abstract via arXiv API. About 60% of correct verdicts come with fabricated claims.", "C6")
h3("2601.22952", "Sifting the Noise: A Comparative Study of LLM Agents in Vulnerability False Positive Filtering", "Y. Xiong; T. Zhang", "2026",
   "arXiv preprint", "ref of 2610.32876", "Abstract via arXiv API. Aggressive false-positive reduction suppresses true vulnerabilities.")
h3("2404.10198", "ClashEval: Quantifying the tug-of-war between an LLM's internal prior and external evidence", "K. Wu; E. Wu; J. Zou", "2024",
   "NeurIPS 2024 Datasets and Benchmarks", "ref of 2610.32876", "Title only (reference list). Prior vs context use.")
h3("Parasuraman&Riley1997", "Humans and automation: use, misuse, disuse, abuse", "R. Parasuraman; V. Riley", "1997", "Human Factors 39(2)",
   "ref of 2610.32876", "Title only. Human automation background.")
h3("Bucinca2021-CognitiveForcing", "To trust or to think: cognitive forcing functions can reduce overreliance on AI in AI-assisted decision-making",
   "Z. Bucinca; M. B. Malaya; K. Z. Gajos", "2021", "PACM HCI (CSCW 2021)", "ref of 2610.32876", "Title only. Human-AI background.")
h3("2403.17218", "To err is machine: vulnerability detection challenges LLM reasoning", "B. Steenhoek; et al.", "2024", "arXiv preprint",
   "ref of 2610.32876", "Title only (reference list).")
h3("Germani&Spitale2025", "Source framing triggers systematic bias in large language models", "F. Germani; G. Spitale", "2025", "Science Advances 11(45)",
   "ref of 2603.18740", "Title only (reference list).", "C4")
h3("Yu2025-SecurityCodeReview", "An insight into security code review with LLMs: capabilities, obstacles, and influential factors", "J. Yu; et al.", "2025",
   "arXiv preprint", "ref of 2603.18740", "Title only (reference list).")
h3("Lou&Sun2025-Anchoring", "Anchoring bias in large language models: an experimental study", "J. Lou; Y. Sun", "2025", "Journal of Computational Social Science",
   "ref of 2603.18740", "Title only (reference list).")
h3("Perez2023-ModelWrittenEvals", "Discovering language model behaviors with model-written evaluations", "E. Perez; et al.", "2023", "Findings of ACL 2023",
   "ref of 2610.32876 and 2603.18740", "Title only (reference list); sycophancy evaluations.")

h3("SorkinWoods1985", "Systems with human monitors: A signal detection analysis", "R. D. Sorkin; D. D. Woods", "1985", "Human-Computer Interaction 1(1)",
   "ref of 2610.35942", "Title only. Human SDT background on monitors.", "C1")
h3("10.1038/435439a", "Rare items often missed in visual searches", "J. M. Wolfe; T. S. Horowitz; N. M. Kenner", "2005", "Nature 435",
   "ref of 2610.35942", "Title only. Human low-prevalence effect: background for C1.", "C1")


def arxiv_meta():
    """Authors and version info from the arXiv API responses saved for this stream."""
    import re
    import xml.etree.ElementTree as ET
    ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    meta = {}
    raw = os.path.join(os.path.dirname(HERE), "raw", "citations", "arxiv")
    for fn in ("screened_idlist.xml", "screened_idlist2.xml", "screened_idlist3.xml"):
        p = os.path.join(raw, fn)
        if not os.path.exists(p):
            continue
        for e in ET.parse(p).getroot().findall("a:entry", ns):
            full = e.find("a:id", ns).text.rsplit("/", 1)[1]
            m = re.match(r"(\d{4}\.\d{4,5})(v\d+)$", full)
            if not m:
                continue
            names = [re.sub(r"\s+", " ", a.find("a:name", ns).text).strip() for a in e.findall("a:author", ns)]
            au = "; ".join(names[:8]) + ("; et al." if len(names) > 8 else "")
            def g(tag):
                el = e.find(tag, ns)
                return re.sub(r"\s+", " ", el.text).strip() if el is not None and el.text else ""
            meta[m.group(1)] = dict(authors=au, version=m.group(2), published=g("a:published")[:10],
                                    updated=g("a:updated")[:10], comment=g("arxiv:comment"),
                                    jref=g("arxiv:journal_ref"))
    return meta


def main():
    seen = set()
    rows = []
    meta = arxiv_meta()
    for r in R:
        if r["id"] in seen:
            raise SystemExit("duplicate id " + r["id"])
        seen.add(r["id"])
        m = meta.get(r["id"])
        if m:
            r["authors"] = m["authors"]
            ver = f"arXiv {m['version']} (v1 {m['published']}; latest {m['updated']})"
            v = r["venue_or_status"]
            if v.startswith("arXiv preprint (") and v.endswith(" 2026)") and "v" not in v[16:18]:
                v = "arXiv preprint"
            if ver not in v:
                v = v + "; " + ver
            r["venue_or_status"] = v
        rows.append(r)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    from collections import Counter
    print(len(rows), "rows", Counter(r["relevance"] for r in rows))


if __name__ == "__main__":
    main()
