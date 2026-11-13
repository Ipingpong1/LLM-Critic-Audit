# Novelty check: LLM critics as signal detectors

Search run Nov 6, 2026, following [PROTOCOL.md](PROTOCOL.md). Every query is in [query_log.csv](query_log.csv) and every kept paper in [screening_log.csv](screening_log.csv) (merged from [streams/](streams/)).

## Bottom line

**The core of the study is still new; most of its secondary claims are not.**

- **Still unclaimed:**
  - No paper, in any task, states a base rate to a model and scores its criterion shift against the ideal-observer shift (the prior-use ratio ρ).
  - No paper compares information (a stated base rate or payoff) against tone on the same critic, on one SDT scale.
  - No paper crosses thinking mode with prior or payoff use in a critic.
- **Now covered or partly covered by 2026 work:**
  - "One line of framing moves the critic's threshold, not its skill" (C4) appears in at least 15 papers, several peer reviewed (ACL 2026, ICSE 2027, IEEE S&P 2027, RecSys 2026).
  - Logprob ROC curves for LLM verifiers (C7) are already done.
  - "Stated costs move models the same way whichever error is costly" (C3) has a close precedent in clinical classification.
  - The says-vs-does gap (C6) is well documented in other forms.
- **The biggest risk is generality, not novelty.** In other tasks, frontier and reasoning models do use stated costs, rates and counts:
  - emergency triage;
  - a GPT-5 SDT study with a one-line risk statement;
  - a Claude reviewer whose checking effort tracks a stated error rate;
  - GPT and Claude following stated error counts.

  The pilot's ρ ≪ 1 and payoff-blindness hold for four small open models with thinking off. Whether they hold for frontier models and with thinking on decides whether the headline is general or a small-model finding.
- **Recommendation: commit the HPC time, but re-scope the study.**
  - Make the headline an ideal-observer test of whether critics use decision-relevant information, across model scale and thinking mode.
  - Keep tone as the comparison condition, not the headline.
  - Spend compute on thinking on/off, more sizes and a second family. Add one or two frontier models through APIs.
  - Drop further tone variants.

## What was searched

| Stream | Sources | Queries | Records screened (with overlap) | Papers kept (close) |
|---|---|---|---|---|
| Browser, main session | Scopus documents and preprints (institutional access), APA PsycInfo (institutional access), the university library, Semantic Scholar web | 26 | 829 | 62 (1) |
| arXiv | arXiv API: block A × (B or C) grid, targeted queries, every judge/verifier/critic paper from Oct 15 to Nov 6, 2026 | 152 | 8,714 | 220 (9) |
| Proceedings | OpenReview API (incl. ICLR 2027 submissions, ARR Oct 2026, NeurIPS 2026 workshops), Crossref (ACL, ACM, AAAI, IEEE prefixes), OpenAlex | 1,100 | 10,184 (5,019 unique titles) | 81 (6) |
| Citations | Forward and backward citations of the seed papers and ProcessBench, second and third hops, author tracking | 140 | 1,722 | 135 (4) |
| Adjacent fields | LLM base-rate and payoff use, size trends, says-vs-does, thinking modes, SDT of LLMs, human SDT (verified by DOI) | 95 | 1,079 | 96 (0) plus 76 human-SDT references |
| Venues | Official venue pages | 171 | n/a | 27 venues |
| **Merged** | | **1,684** | **≈ 23,000** | **501 unique: 17 close, 120 related, 364 background** |

All close papers were read in full, except 4 that are abstract-only (two NeurIPS 2026 JUDGe workshop posters, two ARR Oct 2026 submissions). The main session re-read the decisive ones on arXiv and OpenReview: Liu et al., Servajean & Servajean, Yamin et al., Yang, PmiVQwR4Xv, NzRJ3C97oF and the RecSys tone paper.

**Gaps:**
- Google Scholar is missing (CAPTCHA, skipped by choice).
- Web of Science is missing (proxy error).
- DBLP is missing (bot check).
- Semantic Scholar and OpenAlex throttled requests. Forward citations of the newest preprints therefore rest on OpenAlex and arXiv lookups.
- NeurIPS 2026 main-track papers are not public yet.
- ARR submissions are visible only when authors opted in.

These gaps are listed again under *Residual risk*.

## Claim by claim

| Claim | Verdict | Closest prior work | What to do |
|---|---|---|---|
| **C1** Stated base rate moves the critic's criterion far less than the ideal observer (ρ ≪ 1) | **New** for critics, and as an ideal-observer test in any task. Under-use of stated rates is shown elsewhere without ρ or c* | Gupta et al., ACL 2025 ([2503.04722](https://arxiv.org/abs/2503.04722)): a stated coin bias is mostly ignored. Li & Rui 2024 ([2412.11009](https://arxiv.org/abs/2412.11009)): posterior odds shift 1–2.6 where Bayes gives 9. Markowitz & Hancock 2023: a stated 50% lie rate cuts LLM truth-bias from 97–99% to 67%. PRM operating points set by the training prior (ICLR 2027 submission [NzRJ3C97oF](https://openreview.net/forum?id=NzRJ3C97oF)). **Against, for frontier models:** a Claude Sonnet 5.5 reviewer's checking effort tracks a stated error rate and switches near the break-even its prompt implies ([2610.35942](https://arxiv.org/abs/2610.35942)); GPT and Claude follow stated error counts at 82–94% ([2607.01240](https://arxiv.org/abs/2607.01240)) | Keep as the headline. Test frontier and thinking models before claiming generality. Add an *experienced* base-rate arm (labelled examples at 10% / 90%) to match the human described-vs-experienced literature |
| **C2** Telling the critic to use the base rate doesn't raise ρ | **New** for critics; mixed context | Consistent: RiskEval ([2601.07767](https://arxiv.org/abs/2601.07767)), where "use your confidence" changes nothing. Against: asking to *compute* the posterior restores base-rate use (Li & Rui), and instructed abstention thresholds are followed (Kumaran et al., *Nature Machine Intelligence* 2026) | Frame as "exhortation doesn't help". Add a cheap arm that states the optimal threshold or asks for the posterior |
| **C3** Payoffs don't move the criterion the right way; presence, not content | **Partly covered** outside critics; contradicted for frontier models | Liu et al. ([2609.23999](https://arxiv.org/abs/2609.23999), ML4H 2026 submission): Qwen-2.5 and Llama-3.1 cost responses are "predominantly direction-agnostic", with 2 of 12 model-phrasings correct. Stated penalties ignored in answer/abstain decisions (RiskEval; [2511.11500](https://arxiv.org/abs/2511.11500)). Consequence lines move recall and FPR together in code vulnerability detection (IEEE S&P 2027, [2606.30587](https://arxiv.org/abs/2606.30587)). **Against:** frontier models follow stated cost ratios in triage ([2608.01361](https://arxiv.org/abs/2608.01361)); GPT-5 shifts c past ±0.6 under a one-line risk statement ([2603.29693](https://arxiv.org/abs/2603.29693)) | Cite Liu et al. prominently. Claim the critic version with numeric payoffs mapped to the same c* as the base rates, scoped to the models tested. Thinking and frontier arms decide generality |
| **C4** One line of tone moves c as far as the whole base-rate effect; skill unchanged | **"Moves the threshold, not the skill" is covered.** The comparison with an information manipulation on the same critic is not | Preregistered SDT study: a contrarian line moves the criterion by 2.2–2.6 with d′ almost unchanged (Quiroz, Zenodo 2026). SoundnessBench ([2605.30329](https://arxiv.org/abs/2605.30329), ICLR 2027 submission): FPR 74% → 20%. DialDefer (ACL 2026). Bias injection in code review (ICSE 2027, [2603.18740](https://arxiv.org/abs/2603.18740)). IEEE S&P 2027 paper above. Visual Sanad ([2610.22009](https://arxiv.org/abs/2610.22009)). Confirmation bias in agent judges ([2611.05662](https://arxiv.org/abs/2611.05662)). Two NeurIPS 2026 JUDGe posters. Known: [2608.16003](https://arxiv.org/abs/2608.16003), [2609.18204](https://arxiv.org/abs/2609.18204), [2610.22631](https://arxiv.org/abs/2610.22631), and the RecSys 2026 tone paper ("Tone as a Severity Operating-Point Shift"). One counterexample: self-attribution lowers AUROC (2603.04582) | Treat as established and cite it. Claim only "tone outweighs information". Stop adding tone variants |
| **C5** Within a family, smaller models use the stated prior more | **New but thin**; prior size trends conflict | Larger models trust memory over context (Yu et al. 2023; 31-model replication 2609.24238). Larger models override priors with flipped labels and are more sycophantic (Wei et al. 2023). Smaller open models shift more under framing (DialDefer, SoundnessBench) | Needs more sizes and a second family before it is a claim |
| **C6** States the right lean but doesn't act on it | **Partly covered** as a general gap | Stated vs revealed costs ([2605.08556](https://arxiv.org/abs/2605.08556)). RiskEval. "Knows but defers" in agent judges (2611.05662). "Seeing is not judging" in monitors ([2611.00407](https://arxiv.org/abs/2611.00407)). Can-vs-does in vulnerability auditors ([2610.32876](https://arxiv.org/abs/2610.32876)) | Supporting evidence only |
| **C7** ROC / z-ROC for critics from verdict-token logprobs | **Covered** | ARR Oct 2026 submission [PmiVQwR4Xv](https://openreview.net/forum?id=PmiVQwR4Xv): d′, bias and ROC from the two verdict-token logits for 0.5–14B verifiers. Reasoning's Razor ([2510.21049](https://arxiv.org/abs/2510.21049)): token-score ROC. Cacioli ([2603.14893](https://arxiv.org/abs/2603.14893)): logprob z-ROC slopes 0.52–0.84 | Use it as method and cite it |
| **C8** Thinking on vs off changes ρ or payoff use | **Open** for prior and payoff use; partly covered for operating points | Reasoning's Razor: thinking raises accuracy but lowers TPR at 1% FPR. Reasoning effort raises cost steerability (2608.01361). The reasoning variant is more suspicious (2610.32876). Against: reasoning-tuned models no more penalty-responsive (2511.11500); thinking budget rarely changes small judges' verdicts (SLMJury, ARR Aug 2026) | **The most valuable experiment.** Pre-register both directions |

## The 17 close papers

All are from Oct 2025 to Nov 2026. Twelve appeared from June 2026 on, five of them in the last two weeks. The status column marks the papers read only as abstracts or in part; the rest were read in full.

| Paper | Status | What it does | Overlap |
|---|---|---|---|
| Quiroz, *Criterion, Not Discrimination* (Zenodo 10.5281/zenodo.23671078) | Preprint, preregistered | Approval, accuracy, neutral and contrarian system prompts; probit SDT on false-premise challenges | C4, C3 (verbal incentive) |
| SoundnessBench ([2605.30329](https://arxiv.org/abs/2605.30329)) | ICLR 2027 submission | "Default to low soundness" line; 12 LLMs judging 1,099 research proposals | C4 |
| [PmiVQwR4Xv](https://openreview.net/forum?id=PmiVQwR4Xv) | ARR Oct 2026 (abstract only) | SDT and ROC from verdict-token logits for logic-puzzle verifiers, 0.5–14B | C7 |
| *Leniency Is Not Damage* (OpenReview LRJsAUYRLr) | ARR Oct 2026 (abstract only) | One consequence-framing sentence; 12 judges; accuracy vs ground truth | C3 (verbal stakes), C4 |
| *When the Grader Is Fooled* (rtYX2czR3H) | NeurIPS 2026 JUDGe poster (abstract only) | Strict rubric trades false accepts for up to 16 points of false rejects | C4 |
| *An Auditing Agent Asserts at Ceiling* (J6VoZbu3rV) | NeurIPS 2026 JUDGe poster (abstract only) | Presupposing prompt: 80/80 false findings | C4, C6 |
| DialDefer ([2601.10896](https://arxiv.org/abs/2601.10896)) | ACL 2026 | Speaker attribution shifts verdicts, accuracy within 2 pp; smaller open models shift most | C4, C5 |
| Reasoning's Razor ([2510.21049](https://arxiv.org/abs/2510.21049)) | Preprint | Think on/off; token-score ROC; certainty prompts move operating points | C7, C8 |
| *Prompt Framing Distorts Count-Based Evaluation* ([2607.01240](https://arxiv.org/abs/2607.01240)) | Preprint | Presupposed and stated error counts in proofreading | C1 (over-use by frontier models), C4 |
| Visual Sanad ([2610.22009](https://arxiv.org/abs/2610.22009)) | Preprint, accepted workshop poster | De-bias line moves VLM thresholds, not discrimination | C4, C5 |
| *Trusting the Tool* ([2610.32876](https://arxiv.org/abs/2610.32876)) | Submitted to IEEE Access | False assurances vs false alarms for vulnerability auditors; reasoning variant more suspicious | C4, C6, C8 |
| *Hacking or Just Failing?* ([2611.00407](https://arxiv.org/abs/2611.00407)) | Preprint, preregistered | Monitor prompt variants move the operating point; describes the exploit but doesn't flag it | C4, C6 |
| *What Do LLM Judges Actually Verify?* ([2611.01311](https://arxiv.org/abs/2611.01311)) | Preprint | Skeptical framing restores catches and false alarms together | C4 |
| *Grounded but Not Immune* ([2611.05662](https://arxiv.org/abs/2611.05662)) | Preprint | A false pre-screening note overturns up to 40% of correct verdicts; knows but defers | C4, C6 |
| *Words Speak Louder Than Code* ([2606.30587](https://arxiv.org/abs/2606.30587)) | IEEE S&P 2027 | Persona, gain/loss consequence and goal lines; recall and FPR move in lockstep | C3, C4 |
| *When AI Agrees Too Much* ([2603.18740](https://arxiv.org/abs/2603.18740)) | ICSE 2027 | Bug-free / bug-present framing of code review | C4 |
| *Counting the Bandages* ([2610.35942](https://arxiv.org/abs/2610.35942)) | Preprint (partial read) | Stated drafter error rate and costs; frontier reviewer's checking effort tracks them | C1, C3 (against, for frontier) |

The most decisive related papers are Liu et al. (cost asymmetry), Yamin et al. (triage), Servajean & Servajean (GPT-5 SDT under risk statements), RiskEval, Gupta et al. (coin flips) and Li & Rui (vignettes). Details for every paper are in `screening_log.csv` and the stream notes.

## What this means for the paper

1. **Headline:**
   - Do LLM critics use decision-relevant information? Test with the SDT ideal observer (ρ for base rates, the same c* for payoffs), across model scale and thinking mode.
   - The SDT pairing of base rate and payoff, both mapped to the same optimal threshold, has no precedent.
   - Tone is the foil: it moves the criterion more than information does.
2. **Claim less on C4 and C7:**
   - Cite the 2026 framing cluster as established and state the specific gap: none compares framing with an information manipulation, or with the ideal observer.
   - Cite PmiVQwR4Xv and Cacioli for the logprob ROC method.
3. **Expect these reviewer questions:**
   - "Isn't this Liu et al. / RiskEval for critics?"
   - "Frontier models follow stated costs (Yamin; Servajean)."
   - "Asking for the posterior fixes base-rate neglect (Li & Rui)."
   - "Threshold gaps and logit adjustment are known." This is what the public ICLR 2027 reviews of the PRM operating-point paper say.

   Each needs an experiment or a scoped claim.
4. **Check a verdict-token confound before the full study.** Dong et al. ([2610.15415](https://arxiv.org/abs/2610.15415)) apply SDT to 44 open models, including Qwen3.5 0.8B–35B. They find that Qwen3.5-9B and -27B partly owe their conservative criterion to a preference for the answer token "No". Our critics answer "error" or "correct", so a token preference could pass for a criterion. Add a reversed-label control: swap which word means flawed, or use neutral labels.
5. **The human comparison is a real asset.**
   - People also shift too little, and use payoffs worse than base rates (Maddox and colleagues; verified references in [streams/adjacent_background_refs.md](streams/adjacent_background_refs.md)).
   - What's new in LLMs is that payoffs move the criterion the *wrong* way, and that ρ is far below human levels.
   - The closest human condition is a stated rate without feedback (Estes & Maddox 1995), which argues for an experienced-rate arm.

## Should you commit HPC time? Yes, for these runs, in this order

1. **Thinking on vs off** for the four pilot models on the base-rate and payoff arms (C8; HPC). This is the open question, and it determines whether C1 and C3 generalize.
2. **One or two frontier models** through APIs on the same arms. They are the direct test of the counter-evidence (Yamin, Servajean, Counting the Bandages). They are cheap: about 9M output tokens per model with thinking on.
3. **Two cheap prompt arms** (no new models needed):
   - state the optimal threshold, or ask for the posterior (C2);
   - show the base rate through labelled examples rather than stating it (C1, the described-vs-experienced contrast).
4. **More sizes and a second family** (C5), for example the Qwen 3.5 ladder plus Gemma 4 or Llama.
5. **Don't spend compute on more tone framings.** C4 is saturated, and the one missing piece (tone vs information) is already in the pilot.

## Venues (details in [streams/venues_notes.md](streams/venues_notes.md) and [venues.csv](venues.csv))

The facts below were checked by the venues stream on official pages. The main session re-read the time-critical ones in the browser.

- **AAAI-27 workshop "Effective and Efficient Evaluation for AI Scientists":**
  - Deadline Nov 20, 2026, 06:00 UTC.
  - Non-archival and double-blind; 6–8 pages; in-person in Montréal on Feb 22, 2027.
  - It requires matched compute and token budgets when comparing systems.
  - Fastest feedback, and blocks nothing later. The pilot alone is enough.
- **ACL 2027 via ARR:**
  - Deadline Jan 4, 2027.
  - Since Oct 2026, a submission gets guaranteed review only if it names a qualified reviewer; the rest go into a lottery.
  - No de-anonymized preprint in the month before submission, so post arXiv by Dec 3 or after Jan 4.
  - Findings is the fallback. Best fit for the LLM-judge audience.
- **TMLR:** rolling and free. It judges correctness and evidence rather than novelty, which suits a crowded topic. It is the alternative if ARR's reviewer rule can't be met.
- **COLM 2027** (deadline probably late March) and **CogSci 2027** (probably early February; the human-comparison audience) are the other two in the top five.

**Timing matters.** Twelve of the 17 close papers appeared from June 2026 on, five of them in the last two weeks. A preprint with the C1 and C3 results, posted by early December, would establish priority on the ideal-observer test.

## Residual risk

No search can make this certain. These are the known holes:

- **Unseen work in review:**
  - Most ARR submissions aren't public.
  - NeurIPS 2026 papers aren't public yet.
  - Three close papers were read only as abstracts.
- **Sources not run:** Google Scholar and its "Cited by" lists (CAPTCHA), Web of Science, DBLP. Semantic Scholar was mostly unavailable, so forward citations of the newest preprints are incomplete.
- **arXiv query limits:**
  - The arXiv API stems every term, even inside quotes, so "critic" also matches "critical". The sweep re-matched hits on the literal words and screened that set (5,567 titles, 237 abstracts, 44 full texts). The 10,769 hits that matched only through stemming were not screened. Papers that say "verification" or "review" but never "verifier" or "reviewer" may sit there.
  - Abstracts that say only "foundation models" or "reasoning models" were missed. Two known papers were lost this way (2605.20745, 2608.10729).
  - The last days of the recency window may not be fully indexed yet.
- **C7 nuance:** ROC curves from verdict-token probabilities exist for verifiers and detectors. z-ROC slopes have been reported only for factual QA (Cacioli), not for critics, which is a small methodological addition at most.
- **Mitigations:**
  - Set arXiv and Google Scholar alerts for "signal detection" and "decision criterion" combined with judge, verifier or critic, and for the authors of the close papers.
  - Re-run the arXiv recency sweep and Scholar "Cited by" by hand before submitting.
  - Re-check ICLR 2027 decisions in January.

## Addendum, claim test (Nov 10, 2026)

Search run Nov 10, 2026. It checks whether the claim-test results (`prereg/premise.md`, `results/premise/analysis/premise.md`), which came after the Nov 6 search, are already published. Details and the full comparison with Brown et al. are in [streams/premise_notes.md](streams/premise_notes.md). New log rows carry `stream=premise` in [query_log.csv](query_log.csv) and a `premise:` prefix in the `found_via` column of [screening_log.csv](screening_log.csv).

### Bottom line

**The claim test is not published as a whole, but its first two findings are no longer new on their own.**

- **Brown et al. ([2611.05662](https://arxiv.org/abs/2611.05662), posted Nov 3)** already show that one false assertion in the system prompt overturns correct verdicts of frontier judges, and that asserting moves a judge more than asking it to check. The paper was in the Nov 6 corpus under C4 and predates `prereg/premise.md` by five days.
- **Still unclaimed:**
  - No paper tells a critic that the assertion carries no information (a note attached at random).
  - No paper compares a stated base rate, a stated chance for the item and a categorical assertion on one critic.
  - No paper shows that a critic's stated probability of error keeps separating flawed from correct work while the verdict follows the assertion.
- **Two of our results run against published ones**, so they need care rather than a novelty claim:
  - Our critics discount a claim once told it is uninformative. Guo et al. find that a source declared inaccurate is still followed, and Brown et al. find that a guard line reduces the effect without removing it.
  - Opus 5.5 discounts "a previous reviewer". In Brown et al., a reviewer's note moves Sonnet-4.6 more than an unattributed one.

### What was searched

| Source | Queries | Records | Titles read |
|---|---|---|---|
| arXiv API: 19 targeted queries, Jan 2023 to Nov 10, 2026 | 19 | 4,138 unique | 949 |
| arXiv API: every submission in seven cs categories from Oct 1 to Nov 10, 2026 that names an evaluator or a premise term | 2 | 10,464 unique | 273 |
| The Nov 6 arXiv pools, re-matched for P1–P5 | none sent | 15,415 | 46 |
| OpenReview search: 26 phrases, all groups (incl. ICLR 2027 and ARR Oct 2026) | 26 | 13,488 unique | 206 |
| Crossref: ACL Anthology, ACM, AAAI and IEEE prefixes | 29 | 1,958 unique | 150 |
| OpenAlex: 12 searches, 8 of them limited to Oct 1 on | 12 | 213 matches, first pages only | 120 |
| Semantic Scholar and OpenAlex: citations and references of the four closest papers and four others | 20 | 24 citing, 431 references | 222 |
| Web search, Zenodo records, ACL Anthology pages | 9 | | |

127 query rows were logged in all; the rest are id and title lookups and page fetches.

- 59 papers were kept: 10 close, 36 related, 13 background. 35 are new to the log and 24 re-screen papers already in it.
- The abstract page of every arXiv paper cited below was opened on Nov 10 (38 pages). Brown et al. was read in full. Alexopoulos et al., Liu & Gao, Yang, Shahriar et al. and Huang & Zhang were read in part. Everything else is at abstract level.
- Forward citations: Semantic Scholar and OpenAlex list no paper citing Brown et al., ten citing Alexopoulos et al., one citing Liu & Gao and one citing Yang. By title or abstract, none of them tests an asserted error on a critic beyond the papers below.

### Claim by claim

Each closest paper has one line on what it shows and one on what it does not.

| Claim | Verdict | Closest papers |
|---|---|---|
| **P1** An unqualified assertion that the work contains an error sharply raises false alarms, also for frontier models with reasoning on | **Partly claimed** | **Brown et al. ([2611.05662](https://arxiv.org/abs/2611.05662)).** Shows: a note that an expert found requirements unmet overturns up to 40% of correct verdicts of four tool-using judges (Opus-4.7, Sonnet-4.6, Qwen3-235B, GPT-OSS-120B), more toward failing than passing. Does not: use an unattributed sentence on its main measure, report false-alarm rates, or state a reasoning setting. **Shah, JUDGe poster ([J6VoZbu3rV](https://openreview.net/forum?id=J6VoZbu3rV), abstract only).** Shows: a presupposing prompt makes gpt-5 and gpt-5-mini report a finding in 80 of 80 runs on pairs with nothing to find, against 10 of 20 at best under neutral wording. Does not: go beyond one small auditing task, or add controls. **Hu & Qu ([2608.04415](https://arxiv.org/abs/2608.04415)).** Shows: six simulated peers asserting the wrong label raise safety judges' false alarms from 56.5% to 87.5%. Does not: use one prompt line, frontier reasoning models or solution checking. **Against a general effect in code review:** five of six models have no room to rise in Alexopoulos et al. ([2603.18740](https://arxiv.org/abs/2603.18740)); asserted alarms are disputed and backfire in Liu & Gao ([2610.32876](https://arxiv.org/abs/2610.32876)); saying that errors exist barely changes counts in Yang ([2607.01240](https://arxiv.org/abs/2607.01240)) |
| **P2** The effect is due to the assertion, not to a request for scrutiny or to raising the possibility | **Partly claimed** | **Brown et al.** Shows: asserting closes 46–65% of the room left for marking error categories, directing a check 22–24%; wording from "definitely" to "might" scales it from 62% to 22%. Does not: test more than one model (Sonnet-4.6), measure verdicts on correct work, or include a control with no claim in it (its check wording still reports that a pre-screen flagged something). **Alexopoulos et al.** Shows: a weak ("may exist") against a strong (asserted) bug framing. Does not: have a usable baseline; only Claude 3.5 Haiku moves, with true negatives 31.6% neutral, 56.8% weak, 18.0% strong. **Hu & Qu ([2607.05545](https://arxiv.org/abs/2607.05545)) and Huang & Zhang ([2610.06522](https://arxiv.org/abs/2610.06522)).** Show: for a model's own answers, an asserted answer causes harmful revision in 66.5% of cases against 10.3% for a plain re-ask, and lines that assert a verdict rank models almost unrelatedly to lines that only dispute. Do not: study critics |
| **P3** Saying the assertion carries no information removes the effect; the opposite assertion moves the threshold the other way; a named source is discounted by some models | **Partly claimed, with conflicting evidence** | **Opposite assertion: already shown** (success cue in Brown et al.; bug-free framing in Alexopoulos et al.; both polarities in Shahriar et al., [2606.30587](https://arxiv.org/abs/2606.30587)). **No information: not tested anywhere as "attached at random".** Zhao & Yang ([2610.34151](https://arxiv.org/abs/2610.34151)) show that a one-line warning removes most of a misleading log's effect on VLM judges, in the accepting direction. Brown et al.'s guard line cuts harmful flips from 18% to 5% and helpful ones from 30% to 12%. Against: Guo et al. ([2610.32055](https://arxiv.org/abs/2610.32055), abstract only) find the shift from a hint persists when its source is declared inaccurate (open models, multiple choice), and instructions to distrust notes fail in Liu & Gao. **Named source: not claimed, and at odds with Brown et al.**, where a reviewer's note (68.5) outweighs an unattributed one (61.9) for Sonnet-4.6. An ARR Oct 2026 submission ([A8ovrVRVnl](https://openreview.net/forum?id=A8ovrVRVnl), abstract only) agrees with our direction: an answer with no source moves correct answers more often than one attributed to another AI model (6.6% vs 2.3%) |
| **P4** Numeric priors are barely used while a categorical assertion is accepted | **Unclaimed** | **Yang.** Shows the reverse pattern in proofreading: saying errors exist changes counts for two of six models by about half an error, while an exact count is followed by GPT and Claude models. Does not: include error-free texts or a base rate. **ICLR 2027 submission ([a1GomLdcJ4](https://openreview.net/forum?id=a1GomLdcJ4), abstract only).** Shows: a perfect numeric confidence note changes accuracy after a challenge by at most 0.01, while one sentence citing another source takes Qwen2.5-7B from 0.855 to 0.233. Does not: study critics or priors; it concerns a model revising its own answers. **Lijo ([2610.35942](https://arxiv.org/abs/2610.35942)) and A8ovrVRVnl.** Show: stated error rates and accuracies are used elsewhere (a reviewer's checking effort; deference to a peer). Do not: compare them with an assertion. The Nov 6 result for C1 stands: nobody else scores a stated rate against the ideal observer |
| **P5** Under the assertion the stated probability still discriminates, so the threshold moves, not sensitivity | **Partly claimed** | **Quiroz (Zenodo [10.5281/zenodo.23671078](https://doi.org/10.5281/zenodo.23671078), preregistered).** Shows with SDT: a contrarian instruction shifts the criterion in three models while d′ changes little. Does not: use an assertion about the item, a critic task or reasoning models. **Basta et al. ([2610.36453](https://arxiv.org/abs/2610.36453)).** Shows with SDT: an evidence-gating instruction shifts the propensity to concede rather than discrimination, and cited sources lower discrimination in four of seven models. Does not: study verdicts on someone else's work. **Mazaheri & Mazaheri ([2608.16003](https://arxiv.org/abs/2608.16003)).** Shows on ProcessBench: prior audit context moves the criterion and not d′, also with reasoning on. Does not: assert anything about the solution under review, and its effect lowers false alarms. **Not found anywhere:** a critic's stated probability keeping its AUC under an asserted error. Contrary signs: verbal confidence does not separate findings from confabulations in Shah's poster, and a diagnosis in the record lowered discrimination in three of five frontier models (Rosenblum et al., [2610.35326](https://arxiv.org/abs/2610.35326)) |

### Positioning against Brown et al.

Cite Brown et al. as the first public demonstration, in tool-using agent judges, that a false assertion about the work under review overturns correct verdicts and that asserting matters more than asking for a check. Present the claim test as an independent, preregistered test of the same family of effect in text-only critics with reasoning on, and claim only what their paper lacks. First, measurement: false alarms and hits on held-out correct and flawed items, and a criterion shift with intervals, where they report flips of verdicts that were correct without the cue. Second, controls that contain no claim: their check wording still says that something was flagged. Third, the uninformative-claim test, which they do not run; say that it differs from their generic guard line rather than that it contradicts them. Fourth, the comparison with numeric priors and the stated-probability evidence, which are ours alone. Report the reviewer result as a discrepancy with their source ordering, for one model on each side. Avoid their terms "confirmation bias" and "motivated deference" for our critics: the preregistered test of unjustified deference was not shown for either.

### Other points for the manuscript

- **P5 rests on the stated probability, not on d′.** In `results/premise/analysis/premise.md`, d′ from binary verdicts falls under the bare claim (by 1.82 for Opus 5.5 and 0.77 for qwen3.5:27b) while hits sit at 100%. The "threshold, not sensitivity" papers above report little change in d′, so the manuscript should say which measure carries the claim.
- **Channel.** Every claim-test line sits in the system prompt. Ni ([2610.34809](https://arxiv.org/abs/2610.34809)) finds for Qwen3.5-27B on multiple-choice items that moving a claim between system and user message changes error by a few points, and Brown et al. find that their cue moves the verdict most from the system prompt or a trailing user message. Both bear on the limit noted in `prereg/premise.md`.
- **Rational-updating reading.** Shapira et al. ([2610.28325](https://arxiv.org/abs/2610.28325)) argue that deference to an assertion is in-context updating with too much weight on the assertion. This is close to the reading the claim test supports.
- **Three anonymous ARR Oct 2026 submissions** are under review on neighbouring questions: "Evidence or Assertion?" ([oH7RUqaXuu](https://openreview.net/forum?id=oH7RUqaXuu)), A8ovrVRVnl above, and an accusation-acceptance study of faithfulness judges ([j54ToFVUi0](https://openreview.net/forum?id=j54ToFVUi0)).

### What could not be checked

- **Twelve OpenReview records were read only as abstracts**, three of them rated close (Shah's poster, a NeurIPS 2026 TAE poster on math grading, and j54ToFVUi0). Their PDFs are behind a challenge page, and a title search found no arXiv copy for the nine that were looked up.
- **Guo et al. was read only as an abstract.** It has no HTML version, and the PDF was not downloaded.
- **Numbers taken from abstracts** were not checked against full texts, except for the six papers read in HTML.
- **Google Scholar was not run.** It showed a CAPTCHA on Nov 6 and was not retried. "Cited by" for the four closest papers rests on Semantic Scholar and OpenAlex. Brown et al. is a week old and has no indexed citers yet, so this check should be repeated before submission.
- **Scopus, PsycINFO, Web of Science and DBLP were not run** in this pass.
- **arXiv titles were read selectively**: 949 of 4,138 targeted records and 273 of 10,464 recent ones, chosen by literal term tags. A paper that asserts an error to a critic without words such as assert, told, hint, premise, presuppose, sycophancy, anchoring, deference, accusation or framing would not have been read.
- **The last days before Nov 10 may not be fully indexed** on arXiv (newest record: Nov 9). NeurIPS 2026 main-track papers are not public. ARR submissions are visible only when authors opted in.
- **Crossref and OpenAlex were shallow**: the top 100 per Crossref query, and first pages only on OpenAlex because of its keyless budget. ACM and IEEE full texts were not opened.
- **The project's own numbers were taken from the two premise files as written.** Nothing in `audit/` was opened.
