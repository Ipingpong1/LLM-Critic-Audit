# Does under-use of a stated rate depend on how the rate is stated? What is fixed before the data

Drafted 2026-11-10, and revised the same day to add two OpenAI critics. **Status: approved by the PI on 2026-11-10, with every run in the table below. This file was committed at that point, before any code for it existed and before any model had seen a new line.** Everything above "Deviations" is as approved. Later changes go under "Deviations".

## Why

The base-rate result rests on one sentence in one place: "For calibration: in this review batch, about N% of solutions contain at least one error", appended to the system prompt. The review of 2026-11-10 listed five weaknesses this run addresses, and one it cannot:

1. **One wording.** The under-use may belong to that sentence.
2. **One placement.** The line always sits in the system prompt.
3. **Scope on open models only.** A chance "for this solution" was run on the open models, not on Claude.
4. **Never replicated for Claude on new items.** Claude's base-rate numbers come from the hard set alone.
5. **Three model families.** Every critic so far is a Qwen, Gemma or Claude model.
6. **The stated rate is never the true rate** (always 50%). No new condition fixes this. A critic sees one solution per request, so it cannot check the rate. What can be shown, from the same replies, is what under-use would cost if the stated rate were true (see "Secondary measures").

## Questions

1. Does under-use hold in every wording, placement and scope?
2. Does any of them raise use, compared with the original line?
3. When the rate is stated as a share of correct solutions, does the critic still follow the information, or the number?
4. Do the base-rate result and the claim effect appear in a fourth model family?

## What was already known when this was written

- Every result in `README.md`, including the original and per-solution arms on these items for the open models.
- The label re-analysis (`prereg/label_sensitivity.md`): with the contested items left out or flipped, ρ for thinking-on critics rises, one interval reaches above 1 (qwen3.5:27b, thinking on, per-solution chance), and most thinking-on critics come close to the ceiling. Nobody has audited the items.
- While drafting, Claude computed two label-free measures on the arms that already exist (flag-rate shift and stated-confidence shift). No new wording was involved.
- The literature refresh of 2026-11-10 (`litsearch/NOVELTY_REPORT.md`, addendum): the claim effect is partly published (Brown et al., arXiv 2611.05662), and no paper compares a stated rate with a flat assertion on the same critic.
- No OpenAI model has seen any item or prompt of this project. Their names and prices were read from OpenAI's documentation on 2026-11-10.

## Items

`data/items_premise.jsonl`, the 200 held-out items of the premise test (100 flawed, 100 correct).

- The open models already have `neutral`, the original line and the per-solution line on them, with 3 samples each. Claude has `neutral` and the claim conditions, and no rate condition. The OpenAI critics have nothing.
- The label audit covers this set's 14 contested items, so the audit will settle its labels.
- Every new line makes a new prompt, so no open-model reply can repeat an old one.

## Conditions

Each arm has a 10% and a 90% version. Unless marked, the line is appended to the system prompt and the user message is byte-identical to every earlier run.

| arm | line (90% version) | what changes from the original |
|---|---|---|
| `br` (exists for open models) | For calibration: in this review batch, about 90% of solutions contain at least one error. | – |
| `freq` | For calibration: in this review batch, about 9 in every 10 solutions contain at least one error. | number format |
| `comp` | For calibration: in this review batch, about 10% of solutions are fully correct. | same information, stated as the share correct; no "error" |
| `hist` | Past audits of solutions from this source found at least one error in about 90% of them. | where the rate comes from; no "For calibration" |
| `user` | the original sentence, as its own paragraph in the user message between the solution and the question; the system prompt is the neutral one | placement |
| `item` (exists for open models) | For calibration: there is about a 90% chance that this solution contains at least one error. | scope |

Also `br50` (the original line at 50%), which the own-confidence benchmark needs.

The 10% versions swap the number: "about 1 in every 10 solutions contains", "about 90% of solutions are fully correct", "in about 10% of them".

**The OpenAI critics also get `neutral` and the eight claim conditions of `prereg/premise.md`**, byte-identical to the premise test. They have nothing on these items, and a rate result without the claim result would leave the paper's main contrast untested in their family.

## Runs

The open models and Claude run with the settings of the premise test, so the existing rows can be reused.

| critic | new conditions | samples | requests | expected |
|---|---|---|---|---|
| qwen3.5:4b, 9b, 27b and gemma4:12b, thinking off (cluster) | 9 | 3 | 5,400 each | under 20 minutes each, free |
| qwen3.5:4b, thinking on (cluster) | 9 | 3 | 5,400 | about 5 hours, free |
| qwen3.5:9b, thinking on (cluster) | 9 | 3 | 5,400 | about 10 hours, free |
| gemma4:12b, thinking on (cluster) | 9 | 3 | 5,400 | about 19 hours, free |
| qwen3.5:27b, thinking on (cluster) | 9 | 3 | 5,400 | about 21 hours, free |
| Opus 5.5, thinking on (batch) | 13 | 1 | 2,600 | about $14, cap $17 |
| Haiku 5.5, thinking on (batch) | 13 | 3 | 7,800 | about $2.1, cap $3 |
| GPT-6.1 Sol, reasoning on (OpenAI) | 22 | 1 | 4,400 | set by the probe, cap $30 |
| GPT-6 Luna, reasoning on (OpenAI) | 22 | 3 | 13,200 | set by the probe, cap $8 |

- The open models get `br50` and the four new arms. Claude also gets `br` and `item`, which it has never had on these items. The OpenAI critics get all 13 rate conditions, `neutral` and the 8 claim conditions.
- Times scale the premise jobs by request count and leave out queueing. Claude costs use the cost per call measured on these items ($0.0054 for Opus, $0.00027 for Haiku).
- **Claude API credit:** $66.25 of $100 is spent. This run is expected to take about $16 and can take at most $20.
- **OpenAI:** billed to a personal OpenAI account. At most $40: the two caps above and $2 for the probe.
- **Not in this plan:** Sonnet 5.5, GPT-6 Astra (five times the price of GPT-6.1 Sol per token) and any Google critic.

### The OpenAI critics

- **Models.** `gpt-6.1-sol`, which OpenAI describes as near its most capable model at a lower cost, with one sample, as for Opus. `gpt-6-luna`, its cheapest current model, with three samples, as for Haiku.
- **Prices** per million tokens at the half-price rate (Flex or Batch): $1 in and $5 out for Sol, $0.05 in and $0.25 out for Luna. A request is about 1,300 tokens in. Reply length with reasoning is not known, so the cost is not known: for Sol's 4,400 requests it is about $17 at 500 tokens out, $28 at 1,000 and $50 at 2,000.
- **Settings.** The same system and user messages as every other critic. Default sampling: no temperature is sent, as for Claude. Reasoning effort is set by the probe, below. The reasoning text is not available through the endpoint the runner uses, so only the verdict and the stated P(error) are stored.
- **Probe, before any held-out item is sent.** 40 items already used elsewhere (`data/items_hard_a40.jsonl`), `neutral` only, at effort `high` and at `medium`, for both models: 160 requests. It is read for cost per request, reply length and parse rate. Its verdicts decide nothing.
- **Effort rule, fixed now, applied per model.** The projected cost is the probe's cost per request × the number of requests × 1.2.
  1. Effort `high` with all 22 conditions, if that is within the cap.
  2. Otherwise effort `medium` with all 22.
  3. Otherwise effort `medium` with the 14 rate conditions only, and no claim tests for that critic.
  4. Otherwise nothing is run for that critic, and the PI is asked.
- **Key.** Read from a local credential store by a wrapper script, as for Claude. It is never printed or written to a file.

**To build before any data:** the new conditions and the user-message placement in `pilot/prompts.py`, a mode for them in `scripts/torch_submit.sh`, `scripts/rate_wording.sh` for the Claude batches and the OpenAI runs, and `scripts/rate_wording_analysis.py`. For OpenAI, the runner needs their request format for reasoning models, the half-price rate, a price table, the spending cap and the spend log it already has for Claude. Then, in order: the analysis on simulated replies with known ρ; a smoke test on 40 items already used elsewhere, read for parse rates only; a dry run of the Claude batches for the cost estimate; the OpenAI probe.

## Measure

ρ per critic and arm, exactly as before: [c(10%) − c(90%)] × d′(`neutral`) / ln 81, with the log-linear correction per pass over the items. The reference d′ is the one at `neutral`, as in the premise analysis, so the existing numbers for `br` and `item` do not change. 10,000 item-bootstrap resamples, flawed and correct resampled separately, the same resamples for every critic and arm.

## Reading rules

- **W1, under-use in every wording.** For a critic run, the 95% interval for ρ lies below 1 in every arm it has. No correction is applied, because every arm has to pass. The largest upper limit per critic is reported, and so is whether every interval lies below 0.5.
- **W2, a wording changes use.** ρ(arm) − ρ(`br`), paired over items, for the five other arms. Two-sided p from the bootstrap, **Holm across all 60 tests** (12 critic runs × 5 arms). "Differs" means Holm p < .05. "No difference" is claimed only when the whole 95% interval lies within ±0.15. Anything else is "inconclusive".
- **W3, information or number.** Under `comp`, c(told 10% have errors) − c(told 90% have errors). Its 95% interval above 0: the critic follows the information. Below 0: it follows the number or the word. Otherwise unclear.
- **W4, Claude on new items.** Opus's ρ for `br` on these items has a 95% interval below 1. Whether the estimate falls inside the Stage C interval, 0.21 [0.05, 0.44], is reported.
- **W5, the claim tests in another family.** T1–T9 of `prereg/premise.md` on GPT-6.1 Sol, with that plan's definitions of "held", "no shift" and "inconclusive", and Holm across its 9 tests. GPT-6 Luna is described, not tested. These critics were not chosen for a large effect, so this asks whether the claim effect generalizes, not whether its size replicates.

**Labels.** Every rule is read under the original labels, with the contested items left out, and with them flipped, as defined in `prereg/label_sensitivity.md`. If audit answers exist when the analysis is run, the audited labels are added and become the primary reading. Until then the original labels are primary and the other two are bounds. The contested items were picked from the replies of the open models and Claude, so for the OpenAI critics they are not picked from their own replies.

**Ceiling.** A critic with 4 or fewer errors per 200 at `neutral` under a label variant has its ρ reported but not interpreted in that variant. From the replies that already exist, this is known now:

| errors per 200 at `neutral` | original | left out | flipped |
|---|---|---|---|
| four open models, thinking off | 21–53 | 14–44 | 18–43 |
| qwen3.5:27b, thinking on | 19.5 | 6.5 | 6.7 |
| Haiku 5.5, thinking on | 17.7 | 5.4 | 6.3 |
| Opus 5.5, thinking on | 16.0 | 3.8 | 5.0 |
| qwen3.5:4b, 9b and gemma4:12b, thinking on | 12–16 | 1.8–3.9 | 5.3–5.7 |
| GPT-6.1 Sol, GPT-6 Luna | not known until their replies exist | | |

So with the contested items left out, four of the six thinking-on runs cannot be interpreted, and the other two are close. This run does not fix that, and the OpenAI critics may be in the same position. **The part of this run that can be firm whatever the audit says is the thinking-off part.**

**How the result will be used**

- **W1 holds for a critic under all three label readings:** the manuscript says its under-use does not depend on wording, placement or scope.
- **W1 holds under the original labels only:** the manuscript says so, and the size waits for the audit, as it already does.
- **W1 fails in some arm under the original labels:** for that critic the claim becomes "use of a stated rate depends on how it is stated", with the arm named.
- **W2 and W3** decide what the manuscript says about remedies: whether rewording, moving the line, or stating it per solution helps.
- **W5** decides whether the manuscript says the claim effect holds in four families or in three.

## Precision

From the two arms that already exist on these items, so these are measured, not simulated.

| | half-width of the 95% interval for ρ | for a difference between two arms |
|---|---|---|
| open models, thinking off, 3 samples | 0.04–0.08 | 0.04–0.07 |
| open models, thinking on, 3 samples | 0.07–0.20 | 0.13–0.25 |
| Claude, 1 sample (hard set) | about 0.2; about 0.4 with contested items left out | 0.1–0.3 |

- Thinking off, a difference of 0.1 between wordings is detectable, and "no difference" within ±0.15 is reachable.
- Thinking on, only differences of about 0.25 or more are detectable, so W2 will mostly read "inconclusive".
- For Opus, W1 can hold under the original labels. With the contested items left out, an estimate near 0.5 would have an interval reaching about 0.9, so W1 is at risk there.
- GPT-6.1 Sol has one sample, so its precision should be like Opus's, if it makes about as many errors. For the claim tests with one sample, `prereg/premise.md` gives a half-width of 0.23–0.28 on a shift in c.

## Secondary measures

Planned in advance, not corrected, and not counted as primary.

- **Flag-rate shift (needs no labels).** Share of all 200 solutions flagged when told 90%, minus when told 10%, per arm.
- **Own-confidence benchmark (needs no labels).** As pre-registered in `prereg/stage_c.md`: the verdict changes a Bayesian would make from the critic's own stated P(error) at `br50`, and how many of them the critic makes, per arm. On the hard set this benchmark moved far less under relabelling than ρ did for the Claude critics (Opus 0.20, 0.33 and 0.26 under the three readings, against 0.21, 0.55 and 0.45 for ρ). It does not work for the qwen models, whose stated confidence is nearly binary.
- **Stated P(error) shift**, in log-odds, 90% minus 10%, per arm.
- **A rate against a claim, on the same critic.** c(`neutral`) − c(`br`, 90%) and c(`neutral`) − c(`item`, 90%) beside c(`neutral`) − c(`claim_bare`), with intervals, for all 12 critic runs. Described, not tested.
- **What under-use costs if the rate were true.** Accuracy at the stated rate p, p × hits + (1 − p) × correct rejections, from the replies under that condition. It is set beside the same critic's neutral verdicts reweighted the same way, and beside the ideal observer with the critic's d′. This addresses weakness 6 without new data.
- **Thinking on − off** in ρ per arm for the open models, paired.
- **Verdicts that flip** between the 10% and 90% versions, per arm, and their direction.

## Rules

Carried over from `prereg/premise.md` unchanged: the 2% rule for unparsed replies and refusals, failed trials not re-sampled, caps not raised without asking, unfinished jobs reported and not extended.

**No peeking.** Verdict rates are not looked at until every approved job has finished. While jobs run, checks use row counts and unparsed counts only.

## Expectations

- **Thinking off.** Every arm of every open model has ρ at or below 0.25. W1 holds under all three label readings. No arm differs from `br` by more than 0.1.
- **Thinking on, original labels.** ρ between 0.05 and 0.6 in every arm, and W1 holds for every critic.
- **Thinking on, contested items left out or flipped.** W1 fails for qwen3.5:27b in at least one arm besides `item`.
- **`freq`** about equal to `br`.
- **`comp`** follows the information for every critic whose `br` interval excludes 0, with ρ at or below that of `br`.
- **`hist`** at or below `br`.
- **`user`** above `br` by point estimate for most thinking-on critics. This is the least certain expectation about the wordings.
- **Opus.** ρ for `br` between 0.1 and 0.4, and W4 holds. `item` above `br` by point estimate.
- **Haiku.** ρ within ±0.15 of 0 in every arm, as on the hard set.
- **GPT-6.1 Sol.** ρ at or below 0.5 in every arm under the original labels, and W1 holds there. T1–T3, T5, T6 and T9 held. T7 no shift or inconclusive. No prediction on whether it discounts a named reviewer as Opus does.
- **GPT-6 Luna.** ρ below 0.3 in every arm. No prediction on the claims: the two small critics so far went opposite ways (qwen3.5:4b moved, Haiku did not).

## Limits, known in advance

- Still one family of items, and still a stated rate that is not the true one.
- The open models' `neutral`, `br` and `item` replies come from the premise jobs of Nov 8–10, not from the same jobs as the new arms. Model, weights, image and sampling are the same.
- Opus and GPT-6.1 Sol have one sample per condition.
- An unbiased ideal observer with d′ = 4 gives different verdicts on about 14 of 200 solutions between 10% and 90%. So for thinking-on critics the intervals are wide however many wordings are run.
- Three rewordings and one other placement are a sample of the ways to state a rate, not all of them.
- This run does not settle the contested labels. The audit does.
- Reasoning effort has no common scale across vendors, so "reasoning on" for OpenAI, "thinking on" for Claude and thinking mode for the open models are three settings, not one. Comparisons between families compare critics as run.
- For the OpenAI critics there is no reasoning text, so nothing can be said about how they argue.

## Analysis

```
.venv/bin/python scripts/rate_wording_analysis.py     # reads results/premise/ and results/rate_wording/, writes results/rate_wording/analysis/
```

New replies go to `results/rate_wording/<critic>.jsonl`. The analysis joins them with the existing rows in `results/premise/` by critic.

## Run log

Written 2026-11-10 while the jobs ran. No verdict rate of any new reply had been looked at.

- **Analysis on simulated replies** (`results/sim/rate_wording/`): five simulated critics with a true ρ of 0.5. Unshifted arms were estimated at 0.38–0.59. Two arms built to be higher (true 0.68 and 0.80) came out at 0.75 and 0.80 and read "differs". A `comp` arm built to follow the number read "number". The built-in claim shifts were recovered within their intervals.
- **Smoke test** (Slurm 22608295, qwen3.5:4b thinking off, 40 used items × the 9 new conditions): 360 of 360 replies parsed. Verdicts not looked at.
- **Cluster:** 8 jobs submitted at about 19:27, Slurm 22608876–22608883.
- **Claude:** dry-run estimates $13.53 (Opus) and $2.13 (Haiku). Batches sent at 19:28.
- **OpenAI probe** (160 requests, $0.12, all parsed, all served at the Flex rate):

  | | cost per request | reply tokens, median | reasoning tokens, median | projected for the full run (× 1.2) | cap |
  |---|---|---|---|---|---|
  | GPT-6.1 Sol, effort `high` | $0.00143 | 48 | 28 (none in 8 of 40) | $7.54 | $30 |
  | GPT-6.1 Sol, effort `medium` | $0.00119 | 14 | 0 (none in 28 of 40) | $6.27 | $30 |
  | GPT-6 Luna, effort `high` | $0.00018 | 224 | 204 | $2.85 | $8 |
  | GPT-6 Luna, effort `medium` | $0.00015 | 198 | 178 | $2.40 | $8 |

  By rule 1 both run at effort `high` with all 22 conditions. Started at 19:38.
- **GPT-6.1 Sol reasons very little on these items even at effort `high`.** Its label stays `gpt-6.1-sol-think`, but "reasoning on" means the setting, not that it reasoned at length. Reasoning tokens per reply are stored, so this can be reported.
- **State at 22:12 on 2026-11-10.** Checked by row counts, unparsed counts and cost only; still no verdict rate looked at.

  | run | replies | unparsed | cost | cap |
  |---|---|---|---|---|
  | Opus 5.5 | 2,600 of 2,600 | 0 | $13.65 | $17 |
  | Haiku 5.5 | 7,800 of 7,800 | 0 | $2.04 | $3 |
  | GPT-6.1 Sol | 4,400 of 4,400 | 0 | $5.84 | $30 |
  | GPT-6 Luna | 13,200 of 13,200 | 0 | $1.62 | $8 |
  | qwen3.5:4b, thinking off | 5,400 of 5,400 | 2 | – | – |
  | qwen3.5:9b, thinking off | 5,400 of 5,400 | 3 | – | – |
  | gemma4:12b, thinking off | 5,400 of 5,400 | 2 | – | – |
  | qwen3.5:27b, thinking off | 5,400 of 5,400 | 0 | – | – |
  | qwen3.5:4b, thinking on | 3,088 of 5,400 | not checked | – | – |
  | qwen3.5:9b, thinking on | 1,596 of 5,400 | not checked | – | – |
  | gemma4:12b, thinking on | 836 of 5,400 | not checked | – | – |
  | qwen3.5:27b, thinking on | 460 of 5,400 | not checked | – | – |

  Claude credit used: $81.94 of $100. OpenAI: $7.58 in all, the probe included. Every OpenAI reply in the results was served at the Flex rate. One GPT-6 Luna request was refused for lack of Flex capacity (not charged) and succeeded when repeated; the refused row stays in the file and the loader drops it. The four thinking-off result files were copied back from the cluster. The thinking-on jobs started earlier than Slurm had estimated (19:48, 19:48, 19:49 and 20:50); at their pace so far they end at about midnight (4b), 04:00 (9b), 11:00 (gemma4:12b) and 13:00 (27b) on 2026-11-11.
- **State at 16:30 on 2026-11-11: every job has finished.** The four thinking-on jobs ended with exit code 0 at 00:00 (qwen3.5:4b), 04:03 (qwen3.5:9b), 12:44 (gemma4:12b) and 13:17 (qwen3.5:27b), each with 5,400 of 5,400 replies; unparsed 0, 4, 49 and 17. Their files were copied back. All 12 result files hold each trial once and the same number of replies in every condition: 71,200 replies, 77 unparsed. The raw replies were committed at this point (the four thinking-on files by hash, in `UNTRACKED.sha256`), before the analysis was run and with no verdict rate looked at.

## Deviations

- **Test requests before the probe.** The plan lists the probe as the first contact with OpenAI. Before it, six requests checked the request format: two "Say OK" requests, and one already-used item under `neutral` sent four times to GPT-6 Luna (twice by hand, at the standard and the Flex rate, and twice through the runner). Under a cent in all. Only whether a reply parsed was looked at.
- **A stalled test.** The first runner test (two requests at the Flex rate) had no reply after about nine minutes and was stopped. Whether OpenAI charged for it is not known; it would be under a cent. The request timeout was then set to 300 seconds, with retries. The probe and the runs so far show no stall.

- **The four thinking-on result files are pinned by hash, not tracked.** They are 77–98 MB each. The plan did not say how raw replies would be stored. The other eight files are tracked.
- **One description outside the plan**, marked as such under Results: what GPT-6.1 Sol does under the flat assertion, and its stated P(error) there.

## Results

Analysed on 2026-11-11, after every job had finished and the raw replies had been committed (`95db3be`). Full tables: `results/rate_wording/analysis/rate_wording.md`. Nobody has audited the contested items yet, so the original labels are the primary reading and the other two are bounds.

### Checks

- 141,200 replies, 12 critic runs, 22 conditions each. No trial is missing or doubled.
- **2% rule.** No new condition is over 2% unparsed; the largest is 1.7% (gemma4:12b, thinking on, `freq` at 90%). The two conditions over 2% are old ones of qwen3.5:27b with thinking on (`presuppose` 2.0%, `claim_mistake` 3.7%), already reported in `prereg/premise.md`.
- Eight values of ρ, recomputed from the raw replies by separate code, match the report to two decimals.
- For the OpenAI critics, the number of prompt tokens differs between conditions as the added lines require, so each condition did reach the model.

### W1, under-use in every wording

| reading | holds for | fails for |
|---|---|---|
| original labels | all 12 critic runs; the largest upper limit is 0.65 | – |
| contested left out | 11 (4 of them at the ceiling, so not interpreted) | qwen3.5:27b thinking on, `item`: 0.85 [0.58, 1.16] |
| contested flipped | 10 | qwen3.5:27b thinking on, `item`: 0.78 [0.55, 1.12]; Opus, `br`: 0.56 [0.29, 1.01] |

- **Holds under all three readings, none at the ceiling (7 runs):** the four thinking-off open models, GPT-6.1 Sol, GPT-6 Luna and Haiku.
  - Thinking off: ρ is 0.02–0.23 under the original labels and at most 0.27 under any reading; no upper limit is above 0.39.
  - GPT-6.1 Sol: 0.16–0.19 (0.09–0.24 across readings; upper limits at most 0.43). Its intervals start at 0.00 in five of six arms: the stated rate changed 2 to 5 of its 200 verdicts.
  - GPT-6 Luna: 0.03–0.16 (at most 0.23 across readings; upper limits at most 0.40).
  - Haiku: 0.02–0.20 (at most 0.29; upper limits at most 0.53).
- **Holds where it can be read (3 runs):** gemma4:12b, qwen3.5:4b and qwen3.5:9b with thinking on. They are at the ceiling with the contested items left out.
- **Holds under the original labels only (2 runs):** Opus and qwen3.5:27b with thinking on. Under the original labels every interval of 11 runs lies below 0.5; the exception is qwen3.5:27b with thinking on (`item` 0.47 [0.26, 0.65], `br` 0.36 [0.23, 0.51]).
- **The OpenAI critics are not at the ceiling under any reading** (10 to 27 errors per 200 at `neutral`). They are the first reasoning-on critics whose under-use can be stated without waiting for the audit.

### W2, a wording changes use

60 tests under the original labels: 3 differ, 27 show no difference, 30 are inconclusive.

- **Differs:** qwen3.5:4b thinking off, `hist` −0.09 [−0.14, −0.06] and `user` +0.09 [0.05, 0.15], under all three readings. qwen3.5:27b thinking on, `hist` −0.12 [−0.20, −0.05], under the original labels only.
- **No difference (within ±0.15):** 18 of the 20 thinking-off tests, all 5 for GPT-6.1 Sol, and 4 others.
- **Inconclusive:** nearly every thinking-on test, as the plan predicted. The largest are Opus `user` −0.21 [−0.34, −0.02] and `freq` −0.20 [−0.33, −0.00] (the original line gave Opus its highest ρ), and Haiku `user` +0.19 [−0.01, 0.36].
- **No wording brought any critic near full use.** The highest ρ in any arm under the original labels is 0.47.

### W3, information or number

Under `comp`, no critic followed the number, under any reading. Under the original labels 8 follow the information (Opus, GPT-6 Luna, all six qwen runs) and 4 are unclear (both gemma runs, GPT-6.1 Sol, Haiku). Five follow the information under all three readings: Opus, qwen3.5:27b on and off, and qwen3.5:4b and 9b off.

### W4, Opus on new items

ρ for `br` is 0.29 [0.09, 0.44]: it holds and lies inside the Stage C interval (0.21 [0.05, 0.44]). With the contested items left out it is 0.49 [0.15, 0.80], at the ceiling. With them flipped it is 0.56 [0.29, 1.01], and W4 fails by 0.01. So Opus's under-use replicates on new items under the original labels, and its size still waits for the audit.

### W5, the claim tests on GPT-6.1 Sol

Seven of nine tests held, with the same outcome under all three readings.

| test | contrast | shift in c [95% CI], original labels | outcome |
|---|---|---|---|
| T1 | `presuppose` − `neutral` | −0.09 [−0.16, −0.03] | held |
| T2 | `claim_bare` − `neutral` | −1.59 [−1.72, −1.47] | held |
| T3 | `claim_mistake` − `neutral` | −0.16 [−0.26, −0.08] | held |
| T4 | `claim_reviewer` − `neutral` | −0.01 [−0.05, 0.00] | not shown |
| T5 | `presuppose` − `check_only` | −0.09 [−0.16, −0.03] | held |
| T6 | `presuppose` − `may_error` | −0.09 [−0.16, −0.03] | held |
| T7 | `claim_random` − `neutral` | 0.00 [0.00, 0.00] | no shift |
| T8 | `claim_random` − `claim_bare` | +1.59 [1.47, 1.72] | held |
| T9 | `claim_correct` − `neutral` | +0.35 [0.08, 0.58] | held |

- The claim effect is in a fourth family. Its size depends heavily on the sentence: the flat assertion moved everything, and the other wordings moved a few verdicts (false alarms 27% at `neutral`, 33% under `presuppose`, 39% under `claim_mistake`, 28% under `claim_reviewer`).
- The T2 and T8 sizes are the largest the measure can show here, because every solution was flagged (see "Outside the plan").
- GPT-6.1 Sol ignores a named reviewer's finding (T4: one verdict of 200 changed) and a claim said to be attached at random (T7, T8: none changed).
- **GPT-6 Luna, described:** small shifts toward flagging. `claim_mistake` −0.32 [−0.49, −0.08], `claim_bare` −0.19 [−0.44, 0.03], `claim_reviewer` −0.16 [−0.42, −0.03], `presuppose` −0.13 [−0.39, 0.01]; `claim_random` −0.04 and `claim_correct` 0.00. False alarms go from 20% to at most 27%.

### Expectations

| expectation | outcome |
|---|---|
| Thinking off: every ρ at or below 0.25; W1 under all readings; no arm more than 0.1 from `br` | held under the original labels (largest ρ 0.23, largest difference 0.09). With contested items left out one arm reaches 0.27 and two differences reach 0.10–0.11 |
| Thinking on, original labels: ρ between 0.05 and 0.6 in every arm; W1 holds | W1 held for all. The range did not: 6 arms are below 0.05 (gemma4:12b, Haiku, GPT-6 Luna) |
| Thinking on, other readings: W1 fails for qwen3.5:27b in an arm besides `item` | wrong: it fails in `item` only. Not expected: Opus fails in `br` with the contested items flipped |
| `freq` about equal to `br` | held where it can be told (thinking off, GPT-6.1 Sol); inconclusive elsewhere |
| `comp` follows the information wherever the `br` interval excludes 0, with ρ at or below `br` | held for 7 of 8 such critics (gemma4:12b thinking off is unclear); ρ is above `br` for 2 of them |
| `hist` at or below `br` | held for 10 of 12 by point estimate; above for Haiku and qwen3.5:4b with thinking on |
| `user` above `br` for most thinking-on critics | not held: above for 4 of 8, below for 3, equal for 1 |
| Opus: ρ for `br` between 0.1 and 0.4, W4 holds, `item` above `br` | first two held; `item` is below `br` (0.19 against 0.29) |
| Haiku: ρ within ±0.15 of 0 in every arm | held in 5 of 6 arms; `user` is 0.20 [0.01, 0.37] |
| GPT-6.1 Sol: ρ at or below 0.5, W1 holds, T1–T3, T5, T6, T9 held, T7 no shift | all held |
| GPT-6 Luna: ρ below 0.3 in every arm | held (largest 0.16) |

### Secondary measures

Planned, uncorrected. Tables are in the report.

- **Flag-rate shift (no labels).** Between "10%" and "90%", the share of solutions flagged changes by −1 to +5 points for Opus, Haiku, both OpenAI critics and gemma4:12b with thinking on, and by at most 17 points for any critic (qwen3.5:4b thinking off, `user`).
- **Own-confidence benchmark (no labels).** Opus makes 7 to 12 of the 37 verdict changes its own stated P(error) predicts, depending on the arm (10 for `br`). Haiku makes 2 to 6 of 27. GPT-6.1 Sol makes 3 of 8 (5 of 8 for `item`). The benchmark does not work for the open models or GPT-6 Luna: few or no changes are predicted, and most changes made are not predicted.
- **Stated P(error) shift.** At most 1.98 log-odds (qwen3.5:4b thinking off, `user`), against 4.39 for a calibrated Bayesian. Under 0.7 for every critic except that one and qwen3.5:27b with thinking on.
- **A rate against a claim, same critic.** GPT-6.1 Sol: told 90% of the batch has errors, its criterion moves by 0.02 [0.00, 0.05] away from flagging; told this solution contains an error, by 1.59 toward it. Opus: 0.28 [0.03, 0.50] for either rate, 1.32 [0.98, 1.62] for the claim. For the qwen models a 90% rate and the claim move the criterion about equally (0.14–0.49 and 0.14–0.39). Haiku and gemma4:12b with thinking on move for neither.
- **What under-use costs if the rate were true.** At a true rate of 10%, the critics would be 55–91% accurate, against 91–98% for an ideal observer with the same d′. Stating the rate changes that by −3.3 to +4.5 points from their neutral verdicts. At a true rate of 90% every critic is within 3.5 points of the ideal observer, because all of them already lean toward flagging.
- **Thinking on − off.** qwen3.5:27b uses the rate more with thinking on in every arm (+0.18 to +0.37, every interval above 0). The smaller models show no consistent difference.
- **Flips.** For Opus, GPT-6.1 Sol and the thinking-off models, nearly every flipped verdict goes toward "error" at 90%. For gemma4:12b with thinking on and GPT-6 Luna the flips go both ways, so their small ρ is hard to tell from noise.

### Outside the plan

Described after the planned analysis; nothing here was a rule.

- **Under "This solution contains an error.", GPT-6.1 Sol flagged all 200 solutions and stated a P(error) of 99 or 100 for every one.** Its stated P(error) then carries no information (AUC 0.52, against 0.92 at `neutral`). Opus under the same sentence flags 89% of the correct solutions, but its stated P(error) still separates them (AUC 0.99; mean 60 on correct solutions, 97 on flawed ones). So "the stated probability keeps discriminating while the verdict follows the claim" is a finding about Opus, not about reasoning critics in general.
- **GPT-6.1 Sol is nearly deterministic.** Its 200 verdicts are identical under `neutral`, `check_only`, `may_error`, `claim_random`, `br50`, `comp` at 90% and `user` at 90%. One sample therefore loses little for this critic, and its intervals reflect the choice of items only.
- **GPT-6.1 Sol flags 27% of the correct-labelled solutions at `neutral`**, with a median of 27 reasoning tokens.
- **Both OpenAI critics flag 13 of the 14 contested items at `neutral`.** Those items were picked from the other critics' replies, so this is independent of how they were chosen. On the other 86 correct-labelled items GPT-6.1 Sol flags 16% and GPT-6 Luna 8%.

### What the manuscript can say

By the rules under "How the result will be used":

- **Under-use does not depend on wording, placement or scope** for the four thinking-off open models, GPT-6.1 Sol, GPT-6 Luna and Haiku, under every label reading; and for the three smaller open models with thinking on, where they can be read.
- **For Opus and qwen3.5:27b with thinking on, under-use holds in every wording under the original labels, and the size waits for the audit.** No critic's claim becomes "depends on how it is stated".
- **No remedy among those tried.** Rewording, moving the line to the user message and stating the chance per solution left ρ at or below 0.47 under the original labels. Two small, reliable differences exist, both in qwen3.5:4b with thinking off.
- **Critics read the rate as information:** stated as a share correct, it moves the criterion the right way wherever it moves at all.
- **The claim effect holds in four families**, with a size that depends on the sentence. For GPT-6.1 Sol it falls from every solution flagged to 6 more false alarms in 100 when "Check it carefully." follows the claim.
