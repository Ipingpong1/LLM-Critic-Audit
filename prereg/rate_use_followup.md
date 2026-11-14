# Rate-use follow-up: attribution, instruction, experience. What is fixed before the data

**Status: drafted 2026-11-12 by the assistant at the PI's request; the paper arm (Q4, Family D) was added and the plan approved by the PI on 2026-11-13, with the runs in the table below. Committed at that point, before any code for it existed and before any model had seen a new line.** Everything above "Deviations" is fixed; later changes go under "Deviations".

## Why

The review of 2026-11-12 named three readings of the results that the paper cannot yet rule out.

1. **Attribution and reliability are confounded in the claim test.** The line that removed the claim effect ("A note attached to this solution says it contains an error. These notes are attached at random ...") changes two things at once: the claim becomes a note's claim instead of the system prompt's own, and the note is declared uninformative. The paper currently says that stating a note's reliability is a cheap remedy. That may be true of the attribution alone.
2. **Under-use of a stated rate may be a default, not an inability.** "Use this base rate as your prior" did not help, but it did not say how. If an instruction that spells out the posterior rule brings ρ near 1, the critics can use the rate and choose not to by default. If it does not, they cannot. Either answer sharpens the paper; Li and Rui found that asking for the posterior restores base-rate use in vignettes.
3. **A told rate may be discounted because it cannot be checked.** The critic sees one solution per request. Every rate so far was described, never shown. People shift more under an experienced rate than a described one (Estes and Maddox). A rate the critic can see in labelled examples is the test of the "rational discounting" reading: if critics use a shown rate and not a told one, the under-use is about trust, not about priors.

Already known, and part of why these are the three: Opus discounted both a named reviewer (22 false alarms per 100) and the random note (12) against 89 for the bare claim; GPT-6.1 Sol ignored both (28, 27); Qwen3.5-27B discounted the random note (23) but not the reviewer (50). The stated P(error) shifts by at most 1.98 log-odds between told 10% and told 90%, against 4.39 for a believer, so the critics do not form the belief and then decline to act on it. Nothing in this plan looks at any held-out verdict again before the new replies are in.

## Questions

- **Q1.** Does attributing the claim to a note, with nothing said about its reliability, already discount it?
- **Q2.** Does spelling out the posterior rule raise ρ, and to what?
- **Q3.** Is a shown rate used more than a told one, and does seeing labelled examples change sensitivity?
- **Q4 (exploratory, Opus only).** Does reading this paper change the critic's use of the rate, and if so, is it the rule the paper states, the finding that the critic under-uses it, the critic's own name, or the disclosure that the stated rate is false?

## Items

- **Test items:** `data/items_premise.jsonl`, the 200 held-out items (100 flawed, 100 correct). Every critic below already has `neutral`, the eight claim lines, `br10`, `br50` and `br90` on them.
- **Example pool for Q3:** `data/examples_experienced.jsonl`, to be built once by `pilot/data.py --examples` from `data/items_hard.jsonl`: the 10 shortest flawed and the 10 shortest correct solutions (all under 1,300 characters; the 20 together are about 5,000 tokens), from the same two splits as the held-out items. The hard set shares no problem with the held-out set. The critics have seen these solutions in earlier runs, but no call carries memory of another; this is noted under limits.

## Conditions (six new)

Each line is appended to the system prompt; the user message stays byte-identical to every earlier run. Exact strings go into `pilot/prompts.py` before any call.

| name | added to the system prompt | role |
|---|---|---|
| `note_bare` | A note attached to this solution says it contains an error. | the claim from a note, nothing said about reliability (Q1) |
| `bayes10`, `bayes90` | the original rate line, then: Treat this rate as your prior. Combine it with the evidence in the solution to obtain the posterior probability that the solution contains an error, report that posterior as p_error, and answer "error" only if it is above 50%. | the posterior rule spelled out (Q2) |
| `exp10`, `exp50`, `exp90` | The ten solutions below were reviewed just before this one, from the same batch, and their verdicts have been audited. Then ten examples from the pool, each as problem, numbered steps and "Audited verdict: error" or "correct", with 1, 5 or 9 of the ten flawed. No rate is stated in words. | a shown rate (Q3); `exp50` is the control for having examples at all |

The example sets are drawn once with seed 0 and fixed in the pool file with their order: `exp50` takes 5 flawed and 5 correct; `exp90` adds 4 flawed from the remaining 5 and keeps 1 of the correct ones; `exp10` the reverse. Order within the ten is shuffled once per condition and then fixed, so every critic sees the same block.

Comparators that already exist: `neutral`, `claim_bare`, `claim_random`, `claim_reviewer` (Q1); `br10`, `br50`, `br90` (Q2, Q3 and Q4).

**Paper arm (Q4), Opus only, eight conditions.** Each is the original rate line at 10% or 90%, preceded in the system prompt by a document and one framing sentence. The document is the body of the manuscript as of 2026-11-12 (abstract to Limitations; no references, tables, figures or appendices), converted to plain text by `scripts/build_followup_blocks.py` and fixed by hash in the run log.

| name | document | framing sentence |
|---|---|---|
| `paper_self10/90` | the paper, with the passages that reveal that the stated rate is never the true rate removed (listed below) | "The following paper reports measurements of how reviewers like you, including Claude Opus 5.5, use a stated error rate." |
| `paper_other10/90` | the same text with every mention of Opus replaced by the name "Model M", so the paper is about another critic | the same sentence with "Model M" in place of the name |
| `paper_methods10/90` | Section 3 only (the audit, the ideal observer, Eq. 1 and Eq. 2), with the same passages removed; no results and no model names | "The following describes how a reviewer's use of a stated error rate is scored." |
| `paper_true10/90` | the paper as in `paper_self`, with the revealing passages kept | the `paper_self` sentence |

Removed from the first three variants, and only these: the two sentences in Method ("The true error rate is therefore always 50%. The stated rate is the manipulation."), the sentence after Eq. 2 ("Because ρ compares criteria on the same items, it does not require the stated rate to be true."), and the Limitations paragraph that begins "The stated rate is never the true rate." `paper_true` keeps them, so it asks whether a critic told that the rate is false stops using it. The `paper_other` text still names the Claude family in the critic list; this is a known limit.

## Runs

| critic | samples | new requests | expected cost or time | cap |
|---|---|---|---|---|
| Opus 5.5, reasoning on, effort high (batch) | 1 | 1,200 | about $10.5: 600 short calls at the measured $0.0054, 600 example calls with about 2,500 more input tokens each | $14 |
| Haiku 5.5, reasoning on, effort high (batch) | 3 | 3,600 | about $1.5 | $3 |
| GPT-6.1 Sol, effort high (Flex) | 1 | 1,200 | about $3.5 | $8 |
| GPT-6 Luna, effort high (Flex) | 3 | 3,600 | about $1 | $3 |
| qwen3.5:4b, 9b, 27b and gemma4:12b, thinking off (cluster) | 3 | 3,600 each | 15–30 minutes each | – |
| qwen3.5:27b, thinking on (cluster) | 3 | 3,600 | 14–18 hours (the 5,400-request rate-wording job took 21 hours; the example prompts add prefill) | – |
| Opus 5.5, paper arm, reasoning on, effort high (batch) | 1 | 1,600 | about $26: the paper is about 8,000 input tokens per call for six of the eight conditions, 1,200 for the two methods-only ones | $32 |

- **Claude credit:** $81.94 of $100 was used by 2026-11-11, and the PI added $50 on 2026-11-13, so about $68 is available. The three Claude runs are expected at about $38 and capped at $49 in all. If anything has to go, `paper_true` goes first (400 calls, about $7), then Haiku.
- **OpenAI:** billed to the account used before; at most $11.
- **Settings** as in the rate-wording run. For the example conditions, the open models' thinking runs raise the vLLM model length from 36,864 to 40,960 tokens, because a 4,000-token prompt plus 32,768 output tokens would not fit; nothing else changes. This is fixed now so that it is not a post hoc choice.
- **Order:** approve and commit this plan; build the conditions, pool, scripts and analysis; run the analysis on simulated replies with known ρ; smoke-test on 40 already-used items (parse rates only); dry-run the Claude batches for the estimate; then launch everything on the same day. The cluster's thinking-on job is the long pole.
- **The three smaller open models with thinking on are not run** (5–20 hours each for little added information on these questions).

## Measures and tests

Inference follows the results freeze (`pilot/inference.py`): exact within-item randomization tests for paired verdict contrasts, Holm within each family; ρ and differences in ρ with the whole-problem bootstrap, intervals descriptive. Labels: original as primary, contested items dropped and flipped as bounds, the audit if it exists by then. The ceiling rule stays (four or fewer errors per 200 at `neutral`: reported, not interpreted).

**Family A, attribution** (Q1), for Opus, GPT-6.1 Sol and Qwen3.5-27B with reasoning on; 9 tests, Holm across them.

| test | contrast in c | predicted |
|---|---|---|
| A1 | `note_bare` − `neutral` | negative |
| A2 | `claim_bare` − `note_bare` | negative (the system prompt's own claim moves more than a note's) |
| A3 | `note_bare` − `claim_random` | no direction; the quantity of interest |

Reading, per critic: **attribution alone discounts** when A2 held and A3 shows no shift (whole interval within ±0.3, the premise test's rule). **The reliability statement does the work** when A3 held and negative (the note still flags more than the random note). **Neither** when A1 is not shown. Anything else is reported as mixed.

**Family B, instruction** (Q2), for every critic run: ρ_instr = [c(`bayes10`) − c(`bayes90`)] × d′(`neutral`) / ln 81, exactly as ρ for `br`; and the paired difference ρ_instr − ρ(`br`). Holm over the ten critic runs on the difference.

| rule | reads |
|---|---|
| B1 | the difference's interval lies above 0: the instruction raises use |
| B2 | ρ_instr ≥ 0.8 with its lower limit above 0.5: near-ideal use when told how |
| B3 | the reported p_error's log-odds shift between `bayes10` and `bayes90` (secondary, no labels needed), against 4.39; and the share of replies whose verdict matches their own reported posterior rule (p_error > 50 if and only if "error") |

**Family C, experience** (Q3), for every critic run: ρ_exp = [c(`exp10`) − c(`exp90`)] × d′(`exp50`) / ln 81, with `exp50` as the reference because the examples may change sensitivity; the paired difference ρ_exp − ρ(`br`); d′(`exp50`) − d′(`neutral`); c(`exp50`) − c(`neutral`). Holm over the ten runs on the difference.

| rule | reads |
|---|---|
| C1 | ρ_exp − ρ(`br`) has its interval above 0: a shown rate is used more than a told one |
| C2 | ρ_exp ≥ 0.8 with its lower limit above 0.5: near-ideal use of a shown rate |
| C3 | d′(`exp50`) − d′(`neutral`) has its interval above +0.5: the examples taught the labelling standard, and C1 is then read with that in mind |

**Family D, the paper** (Q4), Opus only, exploratory. ρ for each document variant, computed as for `br` with d′(`neutral`) as the reference, and paired differences with the whole-problem bootstrap; Holm over D1–D3.

| rule | contrast | reads |
|---|---|---|
| D1 | ρ_self − ρ(`br`) | reading the paper changes use of the rate (either direction) |
| D2 | ρ_self − ρ_other | the critic's own name does work beyond the content |
| D3 | ρ_self − ρ_methods | the reported failure does work beyond the rule |
| D4 | ρ_true − ρ_self | told the rate is false, the critic stops using it (predicted negative); a ρ_true near 0 with ρ_self well above it is the clean outcome |
| D5 | ρ_self ≥ 1 with its lower limit above 1 | overshoot: the critic obeys rather than calibrates |

Family D is exploratory. It goes into the paper as at most one paragraph of the Discussion, never into the abstract, and is dated to the model version, since the paper may later enter training data.

## Precision

From the half-widths measured on these items in the rate-wording run: ρ, about ±0.05 for the open models with thinking off, ±0.07–0.20 with thinking on, about ±0.2 for Opus and GPT-6.1 Sol with one sample; a difference between two arms, ±0.05–0.25. A contrast in c with one sample, ±0.23–0.28; with three samples, ±0.13–0.21. So A3's "no shift" rule is reachable for Qwen3.5-27B and will often read "inconclusive" for Opus and Sol; B2 and C2 can show a jump to above 0.6 for the one-sample critics but cannot tell 0.3 from 0.5.

## Expectations (written before the data)

- **A.** Opus: `note_bare` gives 25–45 false alarms per 100, so A1 and A2 hold and A3 is negative: the reliability statement does part of the work. GPT-6.1 Sol: no change from 27, A1 not shown. Qwen3.5-27B: about 50, like the reviewer's note; A3 held negative.
- **B.** Opus, Sol and Haiku: ρ_instr between 0.4 and 0.8, B1 held, B2 not met; the reported p_error shift rises above 3 log-odds. Open models with thinking off: ρ_instr within 0.15 of ρ(`br`). Qwen3.5-27B with thinking on: 0.5–0.9. This is the expectation I hold most firmly: the instruction will help and will not reach the ideal.
- **C.** ρ_exp above ρ(`br`) by 0.1–0.3 for Opus, Haiku, Sol and Qwen3.5-27B with reasoning; C1 held for at least three of those four; C2 met for none. d′(`exp50`) within ±0.5 of d′(`neutral`). The open models with thinking off change little. This is the least certain expectation.
- **D.** ρ_self between 0.6 and 1.3 (D1 held, a large rise from 0.29); ρ_other within 0.2 of ρ_self (D2 not shown); ρ_methods between ρ(`br`) and ρ_self (D3 held); ρ_true below ρ_self and below 0.3 (D4 held). Overshoot (D5) is possible and would not surprise me.

## Rules

Carried over unchanged from `prereg/premise.md` and `prereg/rate_wording.md`: unparsed replies plus refusals at or under 2% per condition, with the sensitivity analysis above that; failed trials not re-sampled except API errors; caps not raised without asking; unfinished jobs reported, not extended; no verdict rate looked at until every approved job has finished.

## How the result will be used

- **A** decides what the paper says about remedies: "stating a note's reliability" stays only if the reliability statement does the work; it becomes "attributing the claim to a note" if attribution alone discounts; it is dropped if neither.
- **B** decides whether the paper may say that under-use is a default the critic can abandon when told how. If B1 holds, that goes into Section 4.1 and the Discussion's remedies; if not, "the critics cannot use the rate even when told how" goes into the Discussion.
- **C** answers the normative-premise objection in the Discussion: if C1 holds, critics use a rate they can see and discount one they are only told, which is the human told-versus-shown pattern; if not, the under-use is not about trust.
- **D** gives at most one Discussion paragraph: either "a critic handed the paper corrects, or over-corrects, its threshold" or "it does not", with D4 saying whether the critic reasons about the truth of the rate at all.
- Any of these adds text to a body that already ends at the foot of page 8, so Table 1 moves to the appendix or Related Work is shortened before the results are written in.

## Limits, known in advance

- The examples are solutions the critics have already judged in other runs; no call remembers another, but familiarity with the solutions cannot be excluded.
- The example block adds about 2,500 tokens to the system prompt. `exp50` controls for that, not for anchoring on the particular examples.
- The instruction in `bayes10`/`bayes90` changes the verdict rule as well as the prior, so ρ_instr measures the two together; B3 separates them in part.
- Opus and GPT-6.1 Sol have one sample per condition.
- Still one family of items, and in the told conditions still a rate that is not the true one.
- The paper arm is one model, one reply per item, and a document that is itself part of this project; it is a demonstration, not a test of self-knowledge, since no call remembers another.

## To build before any data

The fourteen conditions in `pilot/prompts.py`, reading the example blocks and paper texts from `data/condition_blocks/`; `scripts/build_followup_blocks.py` for the pool (`data/examples_experienced.jsonl`), the three example blocks and the four paper texts, recording a hash of each; a `FOLLOWUP=1` mode in `scripts/torch_submit.sh` with the raised model length; `scripts/followup.sh` for the Claude batches and the OpenAI runs; `scripts/followup_analysis.py` on `pilot/inference.py` for families A to D under each label variant; the simulated check; the smoke test. The cluster jobs are submitted by the PI; the assistant has no cluster access.

## Run log

Written 2026-11-13 while building, before any held-out item was sent. No verdict rate of any new reply has been looked at.

- **Blocks fixed.** `scripts/build_followup_blocks.py` wrote the pool and the seven blocks; hashes in `data/condition_blocks/blocks.sha256`. The example blocks run 9,300–11,500 characters, the paper 34,000 (the methods-only text 6,400).
- **Exact token counts** (count-tokens endpoint, free, mean over three items, Opus tokenizer): note 1,286; bayes 1,365; examples 5,751–6,617; paper 13,330–13,492; methods only 3,718. The plan's estimates (2,500 and 8,000) were low: LaTeX and mathematics tokenize at about 2.5 characters per token. At batch prices with 330 output tokens per call, step 1 is $13.1 and the paper arm $40.4, against $10.5 and $26 expected.
- **Analysis on simulated replies** (`results/sim/followup/`, 2,000 resamples): two simulated critics with true ρ = 0.5 on the told rate, three samples each. The plain one, built with no instruction or example effect and a note that moves it by 0.05, read B1 "no", C1 "no", D not run, and "attribution alone discounts" for family A. The raised one, built with ρ ≈ 0.9 under the instruction, the examples and the paper, a true-rate paper that cancels the shift, and a note that moves it by 0.4, read B1 and C1 "yes" (ρ 0.80 and 0.87), D1 and D3 held, D2 not shown (self and other built equal), D4 held with ρ_true 0.03, and "the reliability statement does the work" for family A. Every built-in value sat inside its interval.

- **Smoke test** (2026-11-13, 01:39–01:41; `results/followup/smoke/`): 4 items already used elsewhere (`data/items_hard_a40.jsonl`, 2 flawed, 2 correct), one reply each, real time: Opus on all 14 new conditions (56 replies), Haiku, GPT-6.1 Sol and GPT-6 Luna on the 6 shared ones (24 each). 128 of 128 parsed, no refusal, no reply cut off. Cached prompt tokens were billed as cache reads (Opus: 229,000 of 446,000 input tokens; Haiku 46,000 of 93,000). Opus wrote a median of 308 output tokens (largest 726), so the 330 used in the estimates stands. Cost $1.44 (Opus), $0.02 (Haiku), $0.08 (Sol), $0.01 (Luna). Verdicts were not looked at. The code was committed at this point, before any held-out item was sent.

- **Launch** (2026-11-13, 08:03 UTC). All five API steps of `scripts/followup.sh` were started at once, from this Mac, and the cluster part from the project's copy on the cluster (an rsync mirror, last synced 2026-11-10; `pilot/`, `scripts/` and `data/` were synced again before anything was submitted, and the block hashes verified there). The longest held-out prompt (`exp90`) is 5,855 tokens under the Qwen3.5-27B tokenizer with its chat template, 38,623 with the 32,768-token reply budget, against the 40,960 model length. No verdict has been looked at; the checks below are parse counts.
  - Step 1, Opus 5.5: batches `msgbatch_013gxWTbTK5xAsHzpDcYbhkj` (600) and `msgbatch_01NqqgfK1piiYY2rCeYKsmhK` (600), done 08:09 UTC. 1,200 of 1,200 parsed, 200 per condition, no refusal, none cut off. $6.53 (cap $17): the second batch's 3.77M input tokens were almost all cache reads.
  - Step 3, GPT-6.1 Sol (Flex): 1,200 calls, done 08:06 UTC, all parsed, none cut off, $3.86 (cap $8).
  - Step 2, Haiku 5.5: batches `msgbatch_01V41m1hYwNU7WUyZbuWoSPG` and `msgbatch_01Gvy5zFZatYRy3F13JxLzmw` (1,800 each), done 08:16 UTC. 3,600 of 3,600 parsed, three samples of every condition and item, no refusal, none cut off. $1.01 (cap $3).
  - Step 4, GPT-6 Luna (Flex): 3,600 calls, done 08:25 UTC, all parsed, three samples of every condition and item, none cut off, $0.79 (cap $3).
  - The API part is complete: 11,200 replies, 11,200 parsed, no refusal, none cut off, $23.87 in all (Claude $19.22 of the $68 in caps; OpenAI $4.65). Verdicts remain unread until the cluster jobs are in.
  - Step 5, Opus 5.5, the paper arm: batches `msgbatch_01Sy85x3DYhRd5gpM8UutvgF`, `msgbatch_014FpEgvw8a75EFpCzU49xs7`, `msgbatch_01Vz7KfJJfMaB1RCx6decHfB` and `msgbatch_019QbUruQu9WVjp6r5wYrAer` (400 each), done 08:14 UTC. 1,600 of 1,600 parsed, 200 per condition, no refusal, none cut off; median reply 227 output tokens. $11.68 (cap $48, $40 estimated uncached): the paper was a cache read in nearly every request.
  - Cluster smoke job 22965848 (Qwen3.5-4B, thinking off, the six conditions on the 40 already-used items, `results/torch_smoke/followup/`), submitted 08:06 UTC on the Courant allocation: completed in 2 min 48 s, 240 of 240 parsed.
  - Cluster, the five full jobs, submitted 08:12 UTC on the Courant allocation, `results/followup/` on the cluster: 22966591 (Qwen3.5-4B, thinking off), 22966592 (9B, off), 22966593 (Gemma 4 12B, off), 22966594 (27B, off), each three samples with a 3-hour limit; 22966595 (Qwen3.5-27B, thinking on, three samples, 47-hour limit, 32,768-token reply budget, model length 40,960).
  - Cluster, thinking off, three of four done by 08:27 UTC and copied to `results/followup/` here with their job logs (`results/followup/cluster_logs/`): Qwen3.5-4B (22966591, 4 min 58 s) 3,600 rows, 1 without a verdict (a 22-token reply that stopped without one); Qwen3.5-9B (22966592, 7 min 45 s) 3,600 rows, 43 without a verdict, every one cut off at the 1,024-token reply limit the thinking-off runs have had throughout (22 in `exp90`, 13 in `exp10`, 6 in `exp50`, 1 each in `bayes10` and `bayes90`); Gemma 4 12B (22966593, 8 min 5 s) 3,600 rows, 5 without a verdict, all at that limit. The limit is part of the fixed protocol, so these rows stay as they are and the analysis treats them as it treats every reply without a verdict. Every condition has its three samples of all 200 items. The two 27B jobs (22966594, 22966595) were waiting for two-GPU nodes, with Slurm's estimated starts at 09:40 and 09:55 UTC. The connection to the cluster dropped before either could be observed (noticed 10:37 UTC); the jobs run independently of it, and their results and logs are to be pulled on the next login.
  - Cluster, Qwen3.5-27B thinking off (22966594): started 08:46 UTC, 15 min 27 s; 3,600 rows pulled 16:44 UTC, 10 without a verdict, all at the 1,024-token limit (7 in `exp10`, 2 in `exp50`, 1 in `exp90`); three samples of every condition and item. The thinking-on job (22966595) started 08:55 UTC on a two-GPU node and was running at 16:44 UTC.
  - Cluster, Qwen3.5-27B thinking on (22966595): 13 h 58 min, ended 22:53 UTC; 3,600 rows pulled 22:55 UTC with the job and vLLM logs. 13 without a verdict, all cut off at the 32,768-token reply budget (9 in `note_bare`, 2 each in `bayes10` and `bayes90`; none in the example conditions); three samples of every condition and item; median reply 5,081 output tokens, 90th percentile 10,719.
  - **Every approved job has finished** (2026-11-13, 22:55 UTC): 29,200 new replies, 72 without a verdict (0.25%). The no-peeking rule ends here; the analysis follows.
- **Analysis** (2026-11-13, 22:58 UTC): `scripts/followup_analysis.py` with its defaults, nine seconds; outputs in `results/followup/analysis/`. Read below under Results.

## Deviations

1. **Caps raised before launch, and prompt caching turned on** (2026-11-13, before any call). With the exact token counts, the plan's caps would stall both Opus steps: the runner re-checks each later batch at the measured cost plus 20%, so a run expected at $13 needs a cap of about $17, and one expected at $40 about $48. Caps are now $17 (step 1) and $48 (the paper arm), $68 for the three Claude runs together, equal to the credit. To bring the real spend well under that, the Claude requests mark the system prompt for prompt caching (`--cache-system` in `pilot/run.py`): the example block or the paper is identical across the 200 requests of a condition, and cached reads are billed at a tenth of the input price. The model's input is unchanged; what changes is the request's billing. The runner now counts cached tokens in the spend ledger. `paper_true` is kept; it would be the first to go only if the smoke test shows replies far longer than 330 tokens.

## Results

Written 2026-11-13, 23:00–23:40 UTC, after every approved job had finished (run log). Analysis: `scripts/followup_analysis.py` with its defaults, seed 0: the held-out rows of the premise test, the rate-wording run and this follow-up (170,400 rows, twelve critic runs, nine with the new conditions); 10,000 whole-problem resamples; 200,000 randomization draws; the label variants original, contested left out and contested flipped; no audit, since none exists. Nine seconds; `results/followup/analysis/followup.md` and `followup.json`. Numbers are under the original labels unless said otherwise; the other two variants are read at the end. The ten-critic Holm families of the plan have nine members, because Gemma 4 12B with thinking on was not run (as the Runs section says).

### Pipeline rules

- **2% rule.** Two new conditions, both Qwen3.5-9B with thinking off: `exp10` 2.2% (13 of 600) and `exp90` 3.7% (22 of 600) without a verdict, every one cut off at the 1,024-token reply limit. Shift from `neutral` with those trials counted as "error", then as "correct": `exp10` −0.15 / −0.06; `exp90` −0.28 / −0.10. ρ_exp is 0.041 as analysed, 0.044 and 0.013 under the two fills, so C1 and C2 read the same either way. No condition reached 5%. The two older conditions over 2% (Qwen3.5-27B with thinking on, `presuppose` and `claim_mistake`) are as reported in `prereg/premise.md`. Over the whole follow-up, 72 of 29,200 replies (0.25%) had no verdict.
- **Ceiling.** No critic is at the ceiling under the original labels. With the contested items left out, Opus is (3.8 errors per 200), so its ρ under that variant is reported, not interpreted.
- **Eligibility of the interaction test.** The studentized problem-cluster bootstrap needs enough problems whose verdicts change across the four conditions. It was eligible for the four open runs with thinking off and for Qwen3.5-27B with thinking on; for Opus, Haiku, GPT-6.1 Sol, GPT-6 Luna and Gemma 4 12B with thinking off it was descriptive only (too few informative problems), and the bootstrap interval of the ρ difference is the only reading there. Family A uses the exact within-item tests throughout (the paired problem-vector swap for Qwen3.5-27B's three samples).

### Family A, attribution (Q1): the readings the plan allowed, one per critic

| critic | A1 `note_bare` − `neutral` (predicted −) | A2 `claim_bare` − `note_bare` (predicted −) | A3 `note_bare` − `claim_random` | reading |
|---|---|---|---|---|
| Opus 5.5 | −0.36 [−0.59, −0.09], Holm p = .0002, held | −0.95 [−1.17, −0.79], p < .0001, held | −0.23 [−0.37, −0.12], p = .002, held, negative | the reliability statement does the work |
| Qwen3.5-27B, thinking on | −0.45 [−0.57, −0.35], p < .0001, held | +0.06 [−0.01, 0.14], p = .30, not shown | −0.38 [−0.50, −0.28], p < .0001, held, negative | the reliability statement does the work |
| GPT-6.1 Sol | −0.01 [−0.05, 0.00], p = 1, not shown | −1.58 [−1.71, −1.45], p < .0001, held | −0.01 [−0.05, 0.00], no shift | attribution alone discounts |

False alarms per 100 correct solutions, `neutral` / `note_bare` / `claim_bare` / `claim_random` / `claim_reviewer`: Opus 15 / 24 / 89 / 12 / 22; Qwen3.5-27B 19 / 52 / 47 / 23 / 50; GPT-6.1 Sol 27 / 28 / 100 / 27 / 28. Hits stayed at or near 100 throughout.

The three critics differ in what the attribution does. For GPT-6.1 Sol the bare note changed one verdict: attributing the claim to a note removes its whole effect. For Qwen3.5-27B the bare note moved the criterion as far as the system prompt's own claim (52 against 47 false alarms), so attribution does nothing and the declaration that notes are random does everything. For Opus the attribution removed about three quarters of the claim's effect on c (the claim moved c by −1.32 from `neutral` in the premise test, the note by −0.36) and the declaration removed most of the rest (12 false alarms against 15 with no line). The readings are the same under all three label variants.

Against the expectations: as written for all three critics (Opus's 24 false alarms sit at the edge of the predicted 25–45).

### Family B, the posterior rule spelled out (Q2): no critic used the rate more when told how

| critic | ρ(`br`) | ρ_instr | ρ_instr − ρ(`br`) | test | B1 | B2 | B3: posterior shift, `bayes` / `br` (log-odds; ideal 4.39) | verdict follows own posterior |
|---|---|---|---|---|---|---|---|---|
| Gemma 4 12B, off | 0.07 [0.02, 0.14] | 0.08 [0.04, 0.14] | +0.01 [−0.06, 0.08] | descriptive | no | no | −0.09 / 0.19 | 100% |
| GPT-6 Luna | 0.07 [−0.01, 0.19] | 0.03 [−0.02, 0.07] | −0.04 [−0.18, 0.03] | descriptive | no | no | 0.05 / 0.04 | 100% |
| GPT-6.1 Sol | 0.17 [0.00, 0.32] | 0.17 [0.00, 0.32] | −0.00 [−0.03, 0.03] | descriptive | no | no | 0.16 / 0.13 | 100% |
| Haiku 5.5 | 0.02 [−0.01, 0.05] | 0.13 [−0.05, 0.27] | +0.11 [−0.08, 0.26] | descriptive | no | no | 0.04 / 0.18 | 100% |
| Opus 5.5 | 0.29 [0.09, 0.43] | 0.11 [0.04, 0.21] | −0.18 [−0.31, 0.01] | descriptive | no | no | 0.53 / 0.55 | 100% |
| Qwen3.5-4B, off | 0.14 [0.10, 0.21] | 0.09 [0.06, 0.15] | −0.05 [−0.12, 0.01] | Holm p = .66 | no | no | 0.93 / 1.10 | 100% |
| Qwen3.5-9B, off | 0.08 [0.05, 0.13] | 0.08 [0.05, 0.12] | −0.00 [−0.05, 0.04] | Holm p = 1 | no | no | 0.55 / 0.58 | 100% |
| Qwen3.5-27B, off | 0.07 [0.04, 0.11] | 0.11 [0.07, 0.16] | +0.04 [−0.00, 0.09] | Holm p = .59 | no | no | 0.58 / 0.35 | 100% |
| Qwen3.5-27B, on | 0.36 [0.23, 0.50] | 0.35 [0.22, 0.49] | −0.01 [−0.07, 0.04] | Holm p = 1 | no | no | 1.00 / 1.06 | 100% |

B1 held for no run: the differences run from −0.18 (Opus) to +0.11 (Haiku), every interval includes 0, and the four eligible tests have Holm p ≥ .59. B2 was met by none: ρ_instr runs from 0.03 to 0.35, and the largest, Qwen3.5-27B with thinking on, equals that critic's ρ(`br`). B3 says why: told to treat the rate as a prior, combine it with the evidence and report the posterior, the critics reported posteriors that moved by −0.09 to 1.00 log-odds between the 10% and the 90% rate, against the 4.39 the rule prescribes, and within 0.3 of the shift of the probability they report under the plain line; in 99–100% of replies the verdict was on the side of 50% that the reported posterior said. The critics apply the rule they are given to a posterior that hardly moves with the prior. For Opus the instruction went with less use of the rate (0.11 against 0.29; the interval of the difference reaches 0.01).

Against the expectations: the expectation held most firmly, that the instruction would help without reaching the ideal, failed in its first half. Not one critic used the rate more when told how to use it.

### Family C, the rate shown in examples (Q3): a shown rate was used no more than a told one

| critic | ρ(`br`) | ρ_exp (d′ at `exp50`) | ρ_exp − ρ(`br`) | test | C1 | C2 | d′(`exp50`) − d′(`neutral`) | c(`exp50`) − c(`neutral`) | C3 |
|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 12B, off | 0.07 [0.02, 0.14] | 0.03 [−0.04, 0.10] | −0.04 [−0.14, 0.03] | descriptive | no | no | −0.17 [−0.51, 0.09] | −0.03 [−0.17, 0.14] | no |
| GPT-6 Luna | 0.07 [−0.01, 0.19] | 0.01 [−0.02, 0.04] | −0.06 [−0.19, 0.03] | descriptive | no | no | +0.13 [−0.31, 0.64] | −0.06 [−0.32, 0.15] | no |
| GPT-6.1 Sol | 0.17 [0.00, 0.32] | 0.03 [0.00, 0.08] | −0.14 [−0.29, 0.04] | descriptive | no | no | +0.06 [0.00, 0.16] | +0.03 [0.00, 0.08] | no |
| Haiku 5.5 | 0.02 [−0.01, 0.05] | −0.10 [−0.22, 0.06] | −0.11 [−0.25, 0.05] | descriptive | no | no | −0.29 [−0.61, 0.19] | +0.34 [0.10, 0.50] | no |
| Opus 5.5 | 0.29 [0.09, 0.43] | −0.12 [−0.25, 0.07] | −0.41 [−0.65, −0.06] | descriptive | no | no | +0.04 [−0.12, 0.22] | +0.02 [−0.06, 0.11] | no |
| Qwen3.5-4B, off | 0.14 [0.10, 0.21] | 0.09 [0.05, 0.15] | −0.05 [−0.11, 0.01] | Holm p = 1 | no | no | −0.16 [−0.46, 0.14] | −0.29 [−0.44, −0.14] | no |
| Qwen3.5-9B, off | 0.08 [0.05, 0.13] | 0.04 [−0.00, 0.10] | −0.04 [−0.11, 0.02] | Holm p = 1 | no | no | −0.11 [−0.44, 0.22] | −0.19 [−0.35, −0.03] | no |
| Qwen3.5-27B, off | 0.07 [0.04, 0.11] | 0.07 [0.02, 0.13] | +0.00 [−0.06, 0.07] | Holm p = 1 | no | no | −0.17 [−0.48, 0.11] | −0.18 [−0.33, −0.03] | no |
| Qwen3.5-27B, on | 0.36 [0.23, 0.50] | 0.22 [0.10, 0.33] | −0.15 [−0.32, 0.02] | Holm p = 1 | no | no | −0.09 [−0.21, 0.02] | −0.05 [−0.11, 0.00] | no |

C1 held for no run: the differences run from −0.41 (Opus) to +0.00 (Qwen3.5-27B with thinking off), and no interval lies above 0. Opus's lies below it: shown ten audited verdicts with one or nine errors among them, it moved its criterion less than when told 10% or 90%, and in the wrong direction as a point estimate (ρ_exp −0.12 [−0.25, 0.07]). C2 was met by none: ρ_exp runs from −0.12 to 0.22. C3 was met by none: d′(`exp50`) − d′(`neutral`) runs from −0.29 to +0.13 with every interval including 0, so the ten examples did not change what the critics detect. They did move criteria: with the balanced block present, the three Qwen runs with thinking off flagged more (c down by 0.18–0.29, intervals below 0) and Haiku flagged less (+0.34 [0.10, 0.50]); the other five runs were within ±0.06.

Against the expectations: the least certain expectation failed. A rate the critic could see in audited verdicts was used no more than a rate it was told, and by Opus less.

### Family D, the paper (Q4): Opus, exploratory, every test descriptive only

| ρ (d′ at `neutral`) | value |
|---|---|
| `br` (the plain line) | 0.29 [0.09, 0.43] |
| `paper_self` | 0.05 [0.01, 0.12] |
| `paper_other` ("Model M") | 0.21 [0.01, 0.35] |
| `paper_methods` | 0.08 [0.03, 0.17] |
| `paper_true` | 0.07 [0.00, 0.16] |

| rule | difference in ρ | outcome |
|---|---|---|
| D1 self − `br` | −0.24 [−0.38, −0.04] | not shown by the rule (8 informative problems, descriptive); the interval lies below 0 |
| D2 self − other | −0.16 [−0.30, 0.05] | not shown |
| D3 self − methods | −0.03 [−0.11, 0.03] | not shown |
| D4 true − self | +0.02 [−0.08, 0.11] | not shown |
| D5 overshoot | ρ_self 0.05 [0.01, 0.12] | none |

Handed a description of this study, Opus used the stated rate less, not more: ρ fell from 0.29 to 0.05, and the methods-only text (0.08) and the text with the revealing passages kept (0.07) did the same. The paper about "Model M" left use nearer the plain line (0.21); the difference from `paper_self`, −0.16 [−0.30, 0.05], is not shown. The expectation of a rise to 0.6–1.3 was wrong in direction.

A limit found after the fact: every variant kept the Items paragraph, "three balanced sets of 200 solutions (100 flawed, 100 correct)", so each lets a reader infer that the true rate is 50% and the stated rate false; removing the three passages did not hide that. D4 therefore compares two texts that both imply the truth, which fits ρ_true ≈ ρ_self, and the drop in D1 is consistent with the critic inferring that the rate is false rather than with it correcting toward the ideal. The arm cannot tell the two apart; the paper gets one dated, exploratory paragraph, as the plan says, and no more.

### Labels

Every reading is the same under the three variants. The Family A readings are identical; B1 and C1 held for no run under any variant; D1's interval lies below 0 under all three (self 0.15 against `br` 0.49 with the contested items left out, 0.14 against 0.56 flipped). As in the earlier plans, ρ(`br`) rises for the thinking-on critics when the contested items are left out or flipped (Opus 0.49 and 0.56; Qwen3.5-27B 0.61 and 0.55), and ρ_instr and ρ_exp rise with it (Qwen3.5-27B 0.62 and 0.63; 0.41 and 0.52), leaving the differences where they were. Opus is at the ceiling in the left-out variant, so its ρ there is not interpreted.

### Expectations against outcomes

- **A** held as written for all three critics.
- **B** failed: no critic used the rate more when told how; the reported posteriors barely moved with the prior.
- **C** failed: no critic used a shown rate more than a told one; Opus used it less.
- **D** failed in direction: the paper lowered Opus's use of the rate; the arm cannot separate "told it is false" from "read about itself".

### Decisions for the manuscript (the plan's "How the result will be used")

- **A.** "Stating a note's reliability is a cheap remedy" stays, with the attribution result beside it: attributing the claim to a note removed its whole effect for GPT-6.1 Sol, about three quarters of it for Opus, and none of it for Qwen3.5-27B, and the declaration that notes are random removed the rest for the two that still moved.
- **B.** "The critics cannot use the rate even when told how" goes into Section 4.1 (beside the attention control) and the Discussion, with the posterior-shift numbers: told to compute a posterior, they report one that moves by at most 1.1 log-odds for an 81-fold change in the stated odds.
- **C.** The Limitations paragraph on the normative premise is rewritten: a critic shown the rate in ten audited verdicts used it no more than one told the rate, so the under-use is not discounting of an unverifiable statement.
- **D.** One Discussion paragraph, dated to the model version, exploratory, with the after-the-fact limit stated.
- Method, Preregistration: this plan is added to the list. Discussion, Compute: about 253,000 replies; API fees US$103 and US$12.
- A table of Families A–C goes into the appendix, and the body is kept at the foot of page 8 by moving Table 1 to the appendix or shortening Related Work, as the plan foresaw.
