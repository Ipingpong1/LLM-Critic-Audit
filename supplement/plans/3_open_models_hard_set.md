# Open models on the hard items: what was fixed before the data

Written 2026-11-08, right after submitting the jobs and before any result came back. Changes made after the data come in are listed under "Deviations".

## Purpose

Run the four open models on the same 200 hard items and prompts as the Claude runs in Stage C, so the two sets can be compared item by item. Two questions:

1. Do the Stage C results hold outside Claude: small ρ, and ρ_Bayes well below 1?
2. Does "contains an error" move open models with thinking on as it moved Opus 5.5? That Opus result came from a pre-registered measure, but its explanation (deference to the claim) was exploratory, so this run is a first check, not a confirmation.

## Runs

`HARD=1 NOTHINK_SAMPLING=card THINK_SAMPLING=card scripts/torch_submit.sh`, Slurm jobs 22283432–22283439, output in `results/torch_hard/`.

- **Models:** qwen3.5:4b, qwen3.5:9b, gemma4:12b and qwen3.5:27b in bf16, each with thinking off and on (8 jobs).
- **Items:** `data/items_hard.jsonl`, 100 flawed and 100 correct.
- **Conditions:** `stage_b`, 13 in all: neutral, br10, br50, br90, br10_use, br90_use, pay_fa9, pay_miss9, presuppose, lenient, lab_neutral, lab_br10, lab_br90. So 2,600 requests per job, with one sample per item and condition.
- **Sampling:** each model card's, at temperature 1.0, in both modes. These are the settings of the earlier `-t1` cluster runs on the easy items.
- **Reply limits:**
  - thinking off: 1,024 tokens, as before (the easy-item runs reached at most 3 cut-offs in 3,000);
  - thinking on: **32,768 tokens, up from 16,384**, with a 2-hour request timeout, a 24-hour job limit and a 36,864-token model length.
  - The longer limit was set before the run. On the easy items the 99th percentile already reached about 16k, and the Claude runs on these items allowed 32k–64k, so the old cap would have dropped mostly the hardest replies.
- **Prompts:** byte-identical to Stage C, and to the earlier cluster runs for the conditions they share.

## Analysis

`pilot/analyze.py` with the same settings as Stage C: 2,000 paired item-bootstrap resamples, reference d′ at br50, and the Bayes check.

**Primary measures, per model and setting:**

1. ρ (base rate), with its 95% interval.
2. ρ_Bayes and the Bayes-check counts.
3. c(presuppose) − c(neutral) and c(lenient) − c(neutral).
4. d′ at br50, and the share of replies with 10 < p_error ≤ 90.

**Secondary measures:**

- ρ for the use, payoff and label-swap arms, each minus the base-rate ρ.
- Paired comparisons with Claude's matching setting, using `sonnet-5.5-nothink` and `sonnet-5.5-think` as the reference. These are paired only if the analysis is run with the Stage C files, which share the items. Claude's sampling is API-default and the open models' is the model card's, so this compares critics rather than isolating one setting.
- Exploratory, with `scripts/stage_c_explore.py` or an equivalent: how the stated P(error) changes under "contains an error", and whether replies say they found nothing or cite the claim.

## Rules

- **Pipeline.** Unparsed replies plus refusals should stay at or under 2% per condition. A condition above 2% is also reported with those trials counted as "error" and as "correct". A model over 5% in a condition stays in, flagged.
- **Failed trials** are not re-sampled, except API errors, which the runner retries on the next pass. Jobs preempted or requeued resume where they stopped.
- **Ceiling.** A critic with 4 or fewer errors out of 200 at br50 has its ρ reported but not interpreted.

## Expectations

- **ρ.** 0–0.35 for every model and setting, with most upper bounds below 0.6. The easy-item runs gave 0.04–0.24 with thinking off and 0.13–0.30 with it on.
- **d′.** Lower than on the easy items, and with thinking on clearly above thinking off, as on the easy items.
- **ρ_Bayes.** Below 1 for every model whose confidence is usable, and the told-10% shortfall larger than the told-90% one.
- **"Contains an error".** Thinking on: qwen3.5:27b strongly negative (at or below −0.4), as on the easy items (−0.82). The other three weaker (above −0.5). Stated P(error) on correct solutions rises in the critics whose false alarms rise, as for Opus.
- **"Lenient".** Positive for every model.

## Deviations

1. **Runs, rules and pre-registered measures:** none. All 8 jobs finished on the first pass.
2. **Scoring note.** "Whose confidence is usable" was not defined in advance. It is not defined now either: the ρ_Bayes expectation is scored on every critic with a defined ρ_Bayes.
3. **Text search replaced.** The rough search for replies citing the claim hits nearly every reply, because open models return their full reasoning. The 42 flips from qwen3.5:27b with thinking on were read and coded by hand instead, by one reader who knew the results.
4. **Exploratory checks added after seeing the data** (`scripts/torch_hard_explore.py`): whether critics flip the same items, which way the base rate moves verdicts, whether reasoning names the rate, calibration, and ρ split into Δc and its benchmark.

## Results (2026-11-08)

20,800 replies, no API spend. Job times were 5–13 minutes with thinking off and 2.5–9.5 hours with it on. Output is in `results/torch_hard/analysis/`: `summary.md`, `explore.md`, `flips_27b_coded.csv` and the figure `torch_hard.png`.

**Rules.** No trigger. No condition is above 2% unparsed (the worst is 4 of 200, all cut off at the 32,768-token limit), and no critic is near the ceiling.

| critic | ρ [95% CI] | ρ_Bayes [95% CI] | d′ at 50% (easier items) | mid-confidence items | "contains an error" | "lenient" |
|---|---|---|---|---|---|---|
| qwen3.5:4b off | 0.18 [0.11, 0.28] | 2.49 [1.34, 5.29] | 1.41 (1.71) | 7% | −0.41 [−0.69, −0.19] | +0.32 [0.11, 0.54] |
| qwen3.5:9b off | 0.08 [0.04, 0.17] | undefined | 1.64 (1.74) | 0% | −0.24 [−0.43, −0.06] | +0.10 [−0.08, 0.29] |
| gemma4:12b off | 0.05 [0.01, 0.12] | undefined | 2.01 (2.26) | 0% | −0.34 [−0.52, −0.20] | +0.12 [−0.03, 0.28] |
| qwen3.5:27b off | 0.08 [0.04, 0.14] | undefined | 1.74 (2.46) | 0% | +0.02 [−0.14, 0.18] | +0.16 [0.00, 0.33] |
| qwen3.5:4b on | 0.36 [0.20, 0.60] | 1.66 [0.73, 3.81] | 2.72 (3.66) | 6% | −0.48 [−0.78, −0.23] | +0.20 [−0.04, 0.49] |
| qwen3.5:9b on | 0.25 [0.11, 0.52] | 2.47 [0.86, 8.32] | 3.03 (3.40) | 4% | +0.26 [−0.01, 0.59] | +0.46 [0.22, 0.78] |
| gemma4:12b on | 0.06 [−0.14, 0.29] | 0.29 [−0.86, 1.66] | 3.20 (4.13) | 4% | −0.40 [−0.74, −0.14] | −0.04 [−0.32, 0.23] |
| qwen3.5:27b on | 0.35 [0.15, 0.51] | 2.10 [0.63, 7.31] | 2.62 (3.68) | 4% | −0.90 [−1.16, −0.52] | +0.22 [0.03, 0.50] |

**Expectations**

| expectation | outcome |
|---|---|
| ρ 0–0.35 for every model, most upper bounds below 0.6 | **Narrowly missed.** The range is 0.05–0.36: qwen3.5:4b on (0.362) and qwen3.5:27b on (0.352) are just over. Upper bounds are 0.12–0.60 |
| d′ lower than on the easy items | Held in all 8 (not paired: different items) |
| d′ with thinking on clearly above off | Held in all 4 (+0.88 to +1.39). For qwen3.5:27b the intervals just touch |
| ρ_Bayes below 1 | **Failed.** Only gemma4:12b on is below 1. The three qwen models with thinking on are at 1.66–2.47, with intervals that include 1. qwen3.5:4b off is above 1. The rest are undefined |
| Told-10% shortfall larger than told-90% | Not testable: all 8 critics have zero predicted additions |
| "Contains an error", qwen3.5:27b on ≤ −0.4 | Held: −0.90 |
| "Contains an error", the other three above −0.5 | Held, narrowly for qwen3.5:4b: −0.48, +0.26, −0.40 |
| Stated P(error) on correct solutions rises where false alarms rise | Held on means: 27b 16→56, 4b 16→34, gemma 4→12, and 9b flat (16→18). The median moves only for 27b (0→90) |
| "Lenient" positive for every model | 7 of 8 in direction. gemma4:12b on is −0.04, with false alarms already at 4 of 100. Five of the eight intervals reach 0 |

**Reading**

1. **Small ρ holds outside Claude.** Thinking on raises ρ for the qwen models (4b +0.19 [0.01, 0.43], 9b +0.16 [−0.01, 0.44], 27b +0.28 [0.07, 0.44]) but not for gemma4:12b (0.00 [−0.24, 0.21] as off − on). Part of that is the benchmark: a higher d′ shrinks the ideal shift. For qwen3.5:4b, Δc barely moves (0.55→0.59), so its higher ρ comes almost entirely from d′. For qwen3.5:27b, Δc does rise (0.19→0.59). Against Sonnet at the same setting, most differences include 0. The exceptions are gemma4:12b off (−0.17 [−0.41, −0.02]) and qwen3.5:4b on (+0.24 [0.04, 0.47]).
2. **The Stage C reading of ρ_Bayes does not carry over.** Open models state nearly binary confidence: 0–7% of items in the middle, against 14–22% for Claude with thinking on. Their stated passes are accurate (1–4% of p ≤ 10 are flawed), but their flags are overconfident (83–96% of p > 90 are flawed, against 99% for Claude). So the benchmark predicts few changes, and no additions at all. They then change more verdicts than it predicts, mostly on items where their confidence predicts no change: qwen3.5:27b made 3 of 8 predicted changes plus 22 others. ρ_Bayes above 1 therefore does not mean better than Bayesian. What holds in both families is weaker: stated confidence does not set the size of the shift.
3. **The base rate mostly adds false alarms when told 90%** (exploratory). From 50% to 90%, false alarms go 25→43, 19→33, 18→27 and 6→8 (27b, 9b, 4b, gemma). From 50% to 10%, they go 25→23, 19→17, 18→11 and 6→4. Hits are near ceiling, so they have little room to show a shift. The qwen reasoning names the rate in nearly every reply, flipped or not. gemma4:12b names it in all 3 flips but only 3 of 92 passes, and has the lowest ρ, though those counts are small.
4. **"Contains an error" is not specific to Claude.** qwen3.5:27b with thinking on matches Opus in size (−0.90 vs −0.99; difference +0.09 [−0.10, 0.28]), going from 16 of 100 to 57 of 98 false alarms while hits stay near ceiling (96 of 98, then 99 of 99). It also repeats its easy-item result (−0.82), as does qwen3.5:4b (−0.47, now −0.48). Model size does not order the effect (4b −0.48, 9b +0.26, gemma −0.40, 27b −0.90). Nor does thinking have one direction: on − off is −0.92 [−1.22, −0.54] for 27b, +0.50 [0.16, 0.90] for 9b, and −0.06 for 4b and gemma.
5. **How the flips are argued** (exploratory; qwen3.5:27b, thinking on). Of 42 flips, 22 clearly use the claim as a reason, 9 do so in softer terms, and 11 do not in the excerpts read. A common pattern is to confirm the mathematics and then call a detail of wording or notation an error. Some treat the sentence as a dataset label: "is likely the ground truth label for this sample"; "Probability: 100 (because of the prompt)". This shows how the verdict is argued, not why these items flipped: a text search finds the claim in 39 of the 41 correct solutions it still passed. The causal evidence is the experiment itself: same items, one added sentence. Flips carry a median stated P(error) of 95, so under a claim the stated number is not a reading of the evidence. qwen3.5:27b and Opus flip 27 of the same items where chance gives 19.8 (p = .001, uncorrected). Why those items is unknown.
6. **Other arms.** Stated payoffs do little: ρ is −0.01 to +0.02 with thinking off, below the base-rate ρ in all four. With thinking on it is −0.08 to +0.10, clearly below for qwen3.5:4b (−0.44 [−0.75, −0.25]) and 27b (−0.25 [−0.40, −0.03]). "Use it as your prior" adds nothing (differences −0.20 to +0.03, all intervals include 0). The label swap changes ρ by at most 0.12, with all intervals including 0.

**Limits.** One sample per item and condition, on one family of math items, with many comparisons and no correction. With thinking on, open-model z-ROC slopes are far from 1 (0.56–2.33), because stated confidence is nearly binary, so the equal-variance ρ is shakier for them than for Claude. Claude and the open models differ in sampling and in how thinking works, so comparisons between them compare critics, not one setting. The coding of flips is by one unblinded reader.
