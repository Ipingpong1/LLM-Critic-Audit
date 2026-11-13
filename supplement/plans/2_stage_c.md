# Stage C pre-registration: the full run and the Claude model ladder

Written 2026-11-07, after Stage B and before any Stage C call. Changes made after the data
come in are listed under "Deviations" at the end, with the reason.

## Purpose

1. **Headline estimate.** ρ for Claude Sonnet 5.5 on all 200 hard items, as Stage B's decision rules set out.
2. **Model ladder.** Does the response to a stated base rate change with capability within one model family? The family is Claude Haiku 5.5, Sonnet 5.5 and Opus 5.5, run on the same items and prompts.
3. **Confidence as the explanation.** Stage B found that Sonnet barely moves, but its stated confidence is so extreme that a Bayesian with the same confidence would barely move either. One model can't tell "ignores the prior" apart from "is sure of itself". Models of different capability give different confidence on the same items, so comparing ρ (equal-variance ideal) with ρ_Bayes (the critic's own confidence) across the ladder separates the two.
4. **Thinking depth.** Max effort on the core conditions, as Stage B's thinking rule requires.

## Models and settings

| label | model | thinking | effort | conditions | `max_tokens` |
|---|---|---|---|---|---|
| sonnet-5.5-nothink | `claude-sonnet-5-5` | off (`between_tools`) | default = high | full (18) | 2,048 |
| sonnet-5.5-think | `claude-sonnet-5-5` | adaptive, summarized | default = high | core (6) | 32,000 |
| sonnet-5.5-think-max | `claude-sonnet-5-5` | adaptive, summarized | max | core (6) | 64,000 |
| haiku-5.5-nothink | `claude-haiku-5-5` | off (`disabled`) | high | full (18) | 4,096 |
| haiku-5.5-think | `claude-haiku-5-5` | adaptive, summarized | high | full (18) | 64,000 |
| opus-5.5-think | `claude-opus-5-5` | adaptive, summarized | high | core (6), subject to the gate | 64,000 |

- **Effort is matched at "high".** The models' default effort differs (Haiku medium, Sonnet high, Opus medium, per the Claude models overview, checked 2026-11-07). So Haiku and Opus are set to high explicitly. Sonnet keeps its default (high), which keeps its requests byte-identical to the Stage B trials that are reused.
- **Opus 5.5 can't turn thinking off.** It appears only in the thinking-on rung. The matched comparison across all three models is therefore the thinking-on rung; the thinking-off rung compares Haiku and Sonnet.
- **`max_tokens`** only bounds reply length; it is set from the reply lengths seen in Stage B, with room to spare. Replies that hit it are counted as cut off.
- **Sampling.** No temperature is sent (the API rejects it), so trials use API-default sampling. One sample per item and condition.
- **Prompts.** Byte-identical to Stage B and to the open-model runs (`pilot/prompts.py`). The label-swap conditions change only the answer format.
- **Batches.** All main runs use the Message Batches API (half price), in chunks (`--batch-chunk`). Stage B's thinking-on trials were real time. The model and request are the same, and batch processing is not documented to change outputs.
- **Prices** were checked against the pricing page on 2026-11-07, per million tokens, input / output, standard rate:

| model | price | batch |
|---|---|---|
| Haiku 5.5 | $0.10 / $0.50 | half price |
| Sonnet 5.5 | $2 / $10 | half price |
| Opus 5.5 | $4 / $20 | half price |

## Items

`data/items_hard.jsonl`: 200 items from ProcessBench OlympiadBench and Omni-MATH, 100 flawed and 100 correct. 30 of the flawed solutions reach the right final answer. The 40 Stage B items are a subset. `data/items_hard_new160.jsonl` lists the other 160.

## Reused trials

Stage B trials made with the same model, prompt and settings are copied into the Stage C files with `scripts/seed_rows.py`. Copied rows carry `"reused_from"`, and the Stage A/B files are not changed.

| file | trials copied |
|---|---|
| sonnet-5.5-nothink | 520 (13 conditions × 40 items) |
| sonnet-5.5-think | 240 (6 core × 40) |
| sonnet-5.5-think-max | 40 (neutral × 40) |

The Opus probe's 40 neutral trials are reused in the Opus run. So the 200-item estimates include the Stage B items, and the replication check below uses only the 160 new ones.

## Conditions

Exact wording is in `pilot/prompts.py`.

- **full (18):**
  - base rate: neutral, br10, br50, br90;
  - use: br10_use, br90_use;
  - payoff: pay_fa9, pay_miss9;
  - strictness: presuppose, find_bugs, harsh, lenient, stakes_miss, stakes_fa, persona;
  - labels: lab_neutral, lab_br10, lab_br90.
- **core (6):** neutral, br10, br50, br90, presuppose, lenient.

## Analysis

`pilot/analyze.py`, unchanged from Stage B apart from these additions:

- **The Bayes check** below, now part of the analysis.
- **`--subset`**, for the replication check.
- **Settings:** all 200 items; 2,000 paired item-bootstrap resamples (flawed and correct items resampled separately); the reference d′ is br50.
- **Models share resamples,** so differences between models are paired over items.
- **Unparsed replies and refusals** are excluded from rates and counted per condition.

**The Bayes check** (`bayes_check` in `pilot/analyze.py`):

- **The rule.** The stated P(error) at br50, p, is read as a posterior under a 50% prior, so its likelihood ratio is p / (1 − p).
  - Told 10%, a Bayesian says "error" iff p > 90.
  - Told 90%, it says "error" iff p > 10.
  - A posterior of exactly ½ counts as "correct".
- **Items used:** sample 0, on the items whose br50 verdict and p and br10 and br90 verdicts all parsed.
- **Counts:**
  - told 10%: flags at 50% that a Bayesian drops, and how many of those the critic dropped;
  - told 90%: passes at 50% that a Bayesian flags, and how many the critic flagged;
  - changes against the stated rate.
- **ρ_Bayes** = observed c(br10) − c(br90) ÷ the same shift computed from the Bayesian verdicts.
  - 1 means the critic moves as far as its own stated confidence implies.
  - Resamples with no predicted shift are dropped from its interval, and their number is reported.

**Primary measures**

1. ρ (base rate) for sonnet-5.5-nothink on 200 items.
2. The ladder at matched effort: ρ for haiku-5.5-think, sonnet-5.5-think and opus-5.5-think. Also the paired differences Haiku − Sonnet and Sonnet − Opus.
3. ρ_Bayes and the Bayes-check counts for every model and setting.
4. The confidence test: the paired difference in ρ_Bayes between Haiku and Opus (thinking on) next to their difference in ρ. If confidence explains the ladder, the ρ_Bayes gap is smaller than the ρ gap.

**Secondary measures**

1. **Thinking-off ladder:** ρ and ρ_Bayes for haiku-5.5-nothink vs sonnet-5.5-nothink.
2. **Thinking depth (Sonnet):**
   - max − high and high − off, for ρ, ρ_Bayes, d′ and the tone shifts;
   - verdicts changed between max and high in the core conditions;
   - output tokens.
3. **Tone, per model:** c(presuppose) − c(neutral) and c(lenient) − c(neutral).
4. **The other arms (use, payoff, labels) and the strictness battery,** for the models that ran all 18 conditions:
   - ρ per arm, and each minus the base-rate ρ;
   - c − c(neutral) for each framing.
5. **Capability and confidence on these items, per model:**
   - d′ (br50);
   - the share of br50 replies with 10 < p_error ≤ 90 (the range where a stated rate should flip a Bayesian's verdict);
   - the z-ROC slope (a check on the equal-variance model behind ρ).
6. **Replication:** ρ for sonnet-5.5-nothink on the 160 items Stage B never saw.
7. **Health per condition:** unparsed replies, refusals (with category), cut-offs and output tokens.

**Sensitivity:** if any condition has more than 2% unparsed replies plus refusals, ρ and ρ_Bayes are also reported with those trials counted as "error" and as "correct".

## Precision

From the simulation in `prereg/stage_b.md` and an end-to-end simulated run of this analysis, at 200 items:

- one model's ρ has a 95% range of about ±0.17 at d′ ≈ 2.4;
- a paired difference in ρ between two models, about ±0.25.

That is enough to detect a ladder gap of about 0.3 or more, but not a small one.

## Expectations (written before the data)

- **Sonnet, thinking off:** ρ about 0–0.2 (Stage B: 0.07), with the upper CI bound below 0.35. The 160-item replication agrees within its CI.
- **Capability order on these items:** d′ for Opus ≥ Sonnet ≥ Haiku. The ladder assumes this; if it fails, the ladder is described by measured d′ rather than by model name.
- **Ladder:**
  - ρ for Haiku > Sonnet ≥ Opus, because a weaker critic is less confident, so more of its verdicts sit near the threshold.
  - Haiku's ρ is about 0.1–0.4.
- **Bayes check:**
  - ρ_Bayes < 1 for every model: critics move less than their own confidence implies.
  - The shortfall is mostly when told 10% (they keep flags).
  - The Haiku − Opus gap is smaller in ρ_Bayes than in ρ.
- **Thinking depth:** max vs high on Sonnet: |Δρ| < 0.15, and ≤ 5% of verdicts change.
- **Tone:**
  - Sonnet as in Stage B: presuppose ≈ 0, lenient > 0.
  - Haiku: presuppose < 0 (like the open models), with larger tone shifts than Sonnet.
- **Labels:** the label swap changes ρ by less than 0.2 for every model that runs it.

## Order of steps and decision rules

`scripts/stage_c.sh`; `DRY=1` builds every batch and prints its estimate without sending anything.

| step | what | new calls | expected | cap |
|---|---|---|---|---|
| 0 | copy the Stage B trials | – | free | – |
| 1 | smoke test: 2 items, neutral; Haiku off, Haiku high, Opus high (real time) | 6 | $0.05 | $0.80 |
| 2 | Sonnet, thinking off, full | 3,080 | $7.7–8.5 | $12 |
| 3 | Sonnet, thinking on (high), core | 960 | $3.0 | $5 |
| 4 | Sonnet, max effort, core | 1,160 | $14–16 | $20 |
| 5 | Haiku, thinking off, full | 3,600 | $0.7 | $3 |
| 6 | Haiku, thinking on (high), full | 3,600 | $2.0 | $5 |
| 7 | Opus probe: 40 Stage B items, neutral (real time) | 40 | $0.5–2 | $2.50 |
| 8 | Opus, high, core (gate below) | 1,160 | $7–19 | $20 |
| 9 | analysis and replication check | – | free | – |
| **total** | | **13,606** | **≈ $35–51** | $68.30 |

Spent before Stage C: $5.98 of $100 in credit.

- **Smoke test (step 1).**
  - Go on only if all 6 replies parse and none is refused.
  - If a model refuses or doesn't answer in the format, stop before that model's main run and report. Prompts are not changed for one model.
- **Caps.**
  - Real-time steps stop starting calls at their cap.
  - Batch steps must fit their cap on the estimate before anything is sent, and are re-checked with the measured cost per call before each later chunk (at most 300–1,800 calls per chunk).
  - A step stopped by its cap is not raised automatically: report and ask.
- **Opus gate (step 8).** The probe gives mean input tokens and mean output tokens; add 25% to the output. Then project the batch cost of the remaining calls (`scripts/stage_c_gate.py`):
  - if the core conditions fit $20, run core;
  - else, if the base-rate arm (neutral, br10, br50, br90) fits $20, run only that;
  - else stop and ask.
- **Pipeline.**
  - Unparsed replies plus refusals should stay under 2% per condition (≤ 3 of 200).
  - A model over 5% in a condition stays in the analysis, flagged, with the sensitivity analysis above.
  - Failed trials are not re-sampled, except API errors (`retryable`), which the runner retries on the next pass.
- **Ceiling.** If a model makes 4 or fewer errors (misses + false alarms) out of 200 in br50, its ρ is reported but not interpreted: d′ is past what 200 items measure. Its Bayes-check counts are still reported.

## What stays fixed

The items, conditions, prompts, settings, analysis code and decision rules above. Bug fixes in the code are allowed and are logged below.

## Deviations

1. **Step 4 (Sonnet, max effort) stopped at its $20 cap and was resumed with a higher cap** (2026-11-08).
   - **What happened.** After 2 of 4 chunks (600 calls, $13.78), the measured cost was $0.023 per call. With the 20% margin, the next chunk was estimated at $8.27, which would have gone past the cap, so the runner stopped with 560 trials not sent (`logs/stage_c_step4.log`).
     - Done at that point: neutral, br10, br50 on all 200 items, and br90 on 40.
     - Not sent: br90 on 160, presuppose and lenient on 200 each.
   - **Why the estimate was off.** The median reply was close to Stage B's (about 1,300–1,400 tokens on the new items, against about 1,100). The mean was about 4,400–4,800 tokens, though, against an estimate of 2,600. That came from a heavy tail: the 90th percentile was about 10,000–13,000 tokens, and 6 replies used all 64,000 tokens without answering.
   - **Decision.** Following the cap rule, this was reported to the user, who approved finishing the step. It was resumed with `STEP=4 CAP4=20 EST4=4700 scripts/stage_c.sh`. That is a new $20 cap for the 560 remaining calls (estimated $13.71), so the step's cap is $33.78 in all.
   - **Unchanged.** Items, conditions, prompts and settings. The resumed calls use the same requests as the first pass.
   - **Outcome.** The resume finished under its cap: $13.33 for 560 calls, or $27.11 for the 1,160 calls of step 4. Replies cut off at 64,000 tokens with no answer: br10 3, br50 2, br90 2, presuppose 1, lenient 1, neutral 0. That is at most 1.5% in any condition, within the 2% pipeline rule. Nothing was refused.
2. **The Haiku chain stopped between steps 5 and 6** (2026-11-08). `scripts/stage_c.sh` was edited (for Deviation 1) while the chain was running it, so `sh` lost its place after step 5 and exited on a stray fragment. Step 5 had already saved all its rows. Step 6 was started by hand with the same settings. No effect on the data or the spend.
3. **Exploratory checks added after seeing the data** (`scripts/stage_c_explore.py`, output `results/frontier/stage_c/analysis/explore.md`): thinking summaries returned, mentions of the stated rate, the "contains an error" false alarms, paired differences in that shift, and calibration of the stated P(error). None of these was pre-registered, and they are marked as exploratory below. Panel f of the figure also gained the share of replies with a thinking summary.

## Results (2026-11-08)

**Spend.** $46.90 for 13,606 new calls, inside the expected $35–51. All API spend to date: $52.88.

| step | what | calls | spent | cap |
|---|---|---|---|---|
| 1 | smoke test | 6 | $0.03 | $0.80 |
| 2 | Sonnet, thinking off | 3,080 | $8.62 | $12 |
| 3 | Sonnet, thinking on (high) | 960 | $3.01 | $5 |
| 4 | Sonnet, max effort | 1,160 | $27.11 | $20, then $20 more (Deviation 1) |
| 5 | Haiku, thinking off | 3,600 | $0.31 | $3 |
| 6 | Haiku, thinking on (high) | 3,600 | $1.04 | $5 |
| 7 | Opus probe | 40 | $0.40 | $2.50 |
| 8 | Opus, high, core | 1,160 | $6.38 | $20 |

**Decision rules.**
- Smoke test: passed (6 of 6 parsed, none refused).
- Opus gate: projected $6.52, so core ran.
- Pipeline: at most 3 of 200 unparsed in any condition (1.5%), none refused, no API errors left. The 2% sensitivity analysis was not triggered.
- Ceiling: 11–56 errors in br50, so no critic is at the ceiling.

**Primary measures.**

| critic | ρ [95% CI] | ρ_Bayes [95% CI] | Δc: observed / Bayesian / ideal | told 10%: dropped / predicted | told 90%: added / predicted | wrong way |
|---|---|---|---|---|---|---|
| Haiku, off | 0.04 [−0.00, 0.10] | 0.42 [−0.04, 1.27] | 0.11 / 0.25 / 2.89 | 4 / 16 (+9) | 0 / 0 (+3) | 10 |
| Sonnet, off | **0.22 [0.09, 0.45]** | 0.31 [0.14, 0.50] | 0.35 / 1.13 / 1.56 | 6 / 25 | 8 / 11 | 5 |
| Haiku, high | 0.00 [−0.26, 0.25] | 0.00 [−0.25, 0.24] | 0.00 / 1.16 / 1.32 | 2 / 21 | 1 / 8 | 3 |
| Sonnet, high | 0.13 [0.01, 0.31] | 0.15 [0.01, 0.31] | 0.18 / 1.20 / 1.41 | 2 / 20 | 6 / 15 (+1) | 4 |
| Opus, high | 0.21 [0.05, 0.44] | 0.20 [0.05, 0.37] | 0.29 / 1.43 / 1.41 | 2 / 26 | 5 / 18 | 0 |
| Sonnet, max | 0.21 [0.08, 0.46] | 0.24 [0.06, 0.45] | 0.31 (0.26 on Bayes items) / 1.09 / 1.48 | 5 / 20 | 1 / 9 | 0 |

"+n" counts changes a Bayesian would not make. Sonnet max's Bayes check uses 196 items and Sonnet off's uses 199; the others use 200.

- **Ladder, paired differences in ρ (thinking on):** Haiku − Sonnet −0.13 [−0.48, 0.16]; Sonnet − Opus −0.08 [−0.34, 0.17]; Haiku − Opus −0.21 [−0.53, −0.03].
- **Confidence test (thinking on, Haiku − Opus):** ρ gap −0.21 [−0.53, −0.03]; ρ_Bayes gap −0.20 [−0.46, −0.00]. The gap does not shrink, so confidence does not explain it.

**Secondary measures.**

1. **Thinking-off ladder:** Haiku − Sonnet in ρ −0.19 [−0.43, −0.03]; in ρ_Bayes +0.12 [−0.39, 0.98].
2. **Thinking depth (Sonnet):**
   - ρ: max − high +0.08 [−0.14, 0.32]; high − off −0.10 [−0.31, 0.09].
   - ρ_Bayes: max − high +0.09 [−0.17, 0.34]; high − off −0.16 [−0.39, 0.07].
   - d′ (br50): off 2.81, high 3.12, max 2.96.
   - Verdicts changed in the core conditions: max vs high 37 of 1,191 (3.1%); high vs off 42 of 1,199 (3.5%).
   - Median output tokens: off 247, high 302, max 1,360.
3. **Tone, c − c(neutral):**

   | critic | "contains an error" | "lenient" |
   |---|---|---|
   | Haiku, off | −0.18 [−0.50, 0.14] | +0.23 [−0.03, 0.49] |
   | Sonnet, off | −0.03 [−0.24, 0.20] | +0.22 [0.06, 0.46] |
   | Haiku, high | −0.18 [−0.47, 0.03] | +0.11 [−0.14, 0.36] |
   | Sonnet, high | −0.42 [−0.72, −0.21] | +0.20 [−0.03, 0.48] |
   | Opus, high | **−0.99 [−1.24, −0.60]** | +0.24 [0.08, 0.50] |
   | Sonnet, max | −0.20 [−0.44, −0.06] | +0.30 [0.11, 0.59] |

4. **Other arms, ρ (minus base-rate ρ, paired):**

   | critic | + "use it" | payoffs | label swap |
   |---|---|---|---|
   | Haiku, off | −0.03 [−0.12, 0.02] (−0.06 [−0.19, −0.00]) | 0.04 [−0.05, 0.15] (0.00 [−0.10, 0.11]) | −0.05 [−0.13, 0.01] (−0.09 [−0.18, −0.03]) |
   | Sonnet, off | 0.22 [0.10, 0.43] (−0.00 [−0.22, 0.18]) | 0.04 [−0.04, 0.13] (−0.18 [−0.43, −0.03]) | 0.16 [0.06, 0.35] (−0.06 [−0.26, 0.11]) |
   | Haiku, high | −0.16 [−0.43, −0.02] (−0.16 [−0.46, 0.01]) | −0.08 [−0.29, 0.00] (−0.08 [−0.38, 0.17]) | 0.11 [0.00, 0.35] (+0.11 [−0.04, 0.37]) |

   **Strictness battery, c − c(neutral):**

   | framing | Haiku, off | Sonnet, off | Haiku, high |
   |---|---|---|---|
   | find the mistakes | −0.15 [−0.50, 0.25] | −0.11 [−0.31, 0.00] | −0.07 [−0.31, 0.17] |
   | harsh | +0.10 [−0.02, 0.29] | −0.13 [−0.35, 0.00] | −0.12 [−0.36, 0.02] |
   | a miss costs more | +0.26 [0.02, 0.54] | −0.16 [−0.44, 0.03] | −0.18 [−0.47, 0.03] |
   | a false alarm costs more | +0.21 [−0.04, 0.37] | +0.35 [0.15, 0.67] | +0.05 [0.00, 0.13] |
   | persona | +0.04 [−0.31, 0.35] | −0.08 [−0.27, 0.12] | 0.00 [−0.22, 0.24] |

5. **Capability and confidence (br50):**

   | critic | d′ [95% CI] | misses + false alarms | 10 < p ≤ 90 | z-ROC slope |
   |---|---|---|---|---|
   | Haiku, off | 1.52 [1.13, 2.06] | 6 + 50 | 8% | 1.23 |
   | Sonnet, off | 2.81 [2.39, 3.42] | 5 + 11 | 18% | 0.86 |
   | Haiku, high | 3.33 [2.88, 3.96] | 1 + 12 | 14% | 0.69 |
   | Sonnet, high | 3.12 [2.69, 3.78] | 5 + 6 | 18% | 0.80 |
   | Opus, high | 3.12 [2.65, 3.90] | 2 + 12 | 22% | 0.79 |
   | Sonnet, max | 2.96 [2.51, 3.73] | 3 + 12 | 15% | 0.77 |

6. **Replication:** ρ for sonnet-5.5-nothink on the 160 items Stage B never saw is 0.26 [0.09, 0.53], which agrees with the 200-item 0.22. Stage B's 0.07 [−0.02, 0.25] on the other 40 items sits just below that interval.
7. **Health:** see the decision rules above and `logs/stage_c_step9.log`.

**Expectations, against what happened.**

| expectation | outcome |
|---|---|
| Sonnet off: ρ about 0–0.2, upper bound below 0.35 | **Missed, slightly:** 0.22, upper bound 0.45 |
| Replication agrees within its CI | Held |
| d′ Opus ≥ Sonnet ≥ Haiku | **Failed with thinking on** (3.12, 3.12, 3.33, tied within noise). Held with thinking off (Sonnet 2.81, Haiku 1.52) |
| ρ Haiku > Sonnet ≥ Opus; Haiku about 0.1–0.4 | **Failed, in the opposite order:** 0.00, 0.13, 0.21 |
| ρ_Bayes < 1 for every model | Held for 5 of 6; Haiku off's interval includes 1 |
| The shortfall is mostly when told 10% | Held, descriptively: critics made 21 of 128 predicted drops (16%) and 21 of 61 predicted additions (34%), pooled over critics |
| Haiku − Opus gap smaller in ρ_Bayes than in ρ | **Failed:** −0.20 vs −0.21 |
| Max vs high: \|Δρ\| < 0.15, ≤ 5% of verdicts change | Held: 0.08, 3.1% |
| Sonnet: presuppose ≈ 0, lenient > 0 | Presuppose ≈ 0 only with thinking off. Lenient held in direction at all three settings; the CI includes 0 at high |
| Haiku: presuppose < 0, tone shifts larger than Sonnet's | **Failed:** −0.18 at both settings (CIs include 0). With thinking on, the shift grows up the ladder instead |
| Label swap changes ρ by less than 0.2 | Held: −0.09, −0.06, +0.11 |

**Exploratory (not pre-registered; `analysis/explore.md`).**

- **Calibration when told 50%.** The Bayes check takes the stated P(error) as a posterior. With thinking on, and for Sonnet off, the extreme bins are close to right (p ≤ 10: 3–4 stated vs 1–2% flawed; p > 90: 97–98 vs 98–99%). The middle bins lean high and are small (n = 9–26): for 50 < p ≤ 90, stated 73–78 vs 50–83% flawed. Haiku off is badly miscalibrated (stated 88 vs 12% flawed; stated 96 vs 72% flawed), so its ρ_Bayes should not be interpreted.
  - What this does to the two counts: the told-10% shortfall survives. Flags at 50 < p ≤ 90 were flawed only 50–83% of the time, so a Bayesian told 10% should still drop them even using the true rates. The told-90% predictions are less safe for the critics that overstate most: replies at 10 < p ≤ 50 were flawed only 0–6% of the time for Haiku high and Opus, so some of those predicted flags would not be justified.
- **"Contains an error" (Opus).** Median stated P(error) on correct solutions goes from 3 to 60, and false alarms from 13 to 60 of 100. A rough text search finds that 23 of the 46 newly flagged replies with text say they found nothing or cite the prompt's claim; one says it "could not find a mistake, but the prompt says an error exists". So this looks like deference to the claim at modest confidence, more than errors the model believes it found. The shift is larger than Sonnet's at the same setting: −0.56 [−0.86, −0.12] paired; Haiku's: −0.81 [−1.18, −0.25] paired. Sonnet's own shift is larger with thinking on than off (−0.40 [−0.78, −0.10]) and smaller at max than at high (+0.22 [0.04, 0.47]). These differences were chosen after seeing the data, and no correction was applied.
- **"Thinking on" isn't the same treatment across models.** Adaptive thinking lets the model decide. A thinking summary came back on 97% of Haiku's replies, 26% of Sonnet's at high, 64% of Opus's, and 97% of Sonnet's at max. When Sonnet doesn't think, it usually writes its reasoning in the visible reply, and Haiku with thinking off answers with almost nothing else (median 19 tokens). So the thinking-on rung is matched on the setting, not on how much reasoning happened.
- **The stated rate is rarely named.** Told 10% or 90%, replies name the rate (or "base rate" or "calibration") in 0–8 of 200 replies, except at max effort (28–32, against 11 at neutral). Summaries may leave things out and many replies are bare JSON, so this does not show the rate went unused.

**Reading.**

1. Every Claude critic moves far less than the ideal, at most 0.22 of the way, and Sonnet's estimate replicates on new items.
2. Confidence is not the explanation. This reverses the reading from Stage B's 40 items, which had almost no mid-confidence replies. Across 200 items, a Bayesian with the critic's own stated confidence would move 72–101% as far as the equal-variance ideal (except Haiku off), but the critics make only 3–14 of the 29–44 verdict changes it predicts.
3. There is no capability ladder at matched effort on these items: Haiku with thinking is as accurate as Sonnet and Opus. So the ladder can't test what capability does. What it does show is that thinking took Haiku's d′ from 1.52 to 3.33, at about $0.0003 per call.
4. Max effort added 4.5× the tokens and changed 3.1% of verdicts, with no clear change in ρ, ρ_Bayes or d′.
5. The largest effect in this stage is the asserted premise: "contains an error" moves Opus by about one full unit of c, while stated base rates move any critic by at most 0.35.

**Limits.** One sample per item and condition, on one family of math items. ρ assumes equal variance (z-ROC slopes 0.69–0.86 apart from Haiku off). ρ_Bayes assumes the stated P(error) is a real posterior. Many comparisons were made without correction, so a single interval that barely excludes 0, such as Haiku − Opus in ρ, is suggestive only. The Stage B items are part of the 200.
