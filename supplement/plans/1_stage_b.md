# Stage B pre-registration: Claude Sonnet 5.5 on the hard items

Written 2026-11-07, after Stage A and before any Stage B call. Changes made after the data
come in are listed under "Deviations" at the end, with the reason.

## Purpose

A pilot of the study's manipulations on a frontier critic. It should:

1. check that every condition runs cleanly: parsing, refusals, very long replies, batch mode;
2. give coarse effect sizes for the base-rate, payoff and tone manipulations;
3. test the verdict-token confound with the label swap;
4. choose the "thinking on" setting for the full run.

It is **not** powered to pin down ρ. A simulation at Sonnet's Stage A d′ (≈ 2.4), with the
analysis in `pilot/analyze.py`, gives:

| items | true prior use | ρ estimate, 95% range |
|---|---|---|
| 40 | 0 | −0.39 to 0.31 |
| 40 | 0.3 | −0.05 to 0.65 |
| 200 | 0 | −0.16 to 0.17 |
| 200 | 0.3 | 0.12 to 0.49 |

So Stage B can detect large effects (ρ ≳ 0.4, tone shifts ≳ 0.6); the 200-item full run is needed for the
headline estimate.

## Model and settings

- `claude-sonnet-5-5` through the Claude API, official `anthropic` SDK (`pilot/run.py --backend anthropic`).
- Thinking off: `thinking: {type: "between_tools"}`, default effort.
- Thinking on: `thinking: {type: "adaptive", display: "summarized"}`, default effort (high).
- Effort probe: adaptive thinking at `effort: max`, neutral condition only.
- No temperature is sent (the API rejects it), so trials use the API's default sampling.
- One sample per item and condition. Prompts are byte-identical to the open-model runs except the
  label-swap answer format.

## Items

`data/items_hard_a40.jsonl`: the 40 Stage A items, 10 per (split × class) from ProcessBench
OlympiadBench and Omni-MATH. The Stage A neutral trials are reused; they were made with the same
prompt, model and settings.

## Conditions (13; 12 new per setting)

Exact wording is in `pilot/prompts.py` (set `stage_b`).

| arm | conditions | what changes |
|---|---|---|
| base rate | neutral, br10, br50, br90 | system line: "about p% of solutions contain at least one error" |
| use | br10_use, br90_use | the same line, plus "use this base rate as your prior …" |
| payoff | pay_fa9, pay_miss9 | 1:9 and 9:1 costs for misses vs false alarms (same c* as 10% / 90%) |
| tone | presuppose, lenient | "This solution contains an error. Check it carefully." / "Be a lenient, charitable reviewer." |
| labels | lab_neutral, lab_br10, lab_br90 | answer format uses "flawed" / "sound" and `p_flawed` instead of "error" / "correct" and `p_error`; system prompt unchanged |

## Analysis

`pilot/analyze.py`:

- log-linear corrected H and F;
- d′ = z(H) − z(F), c = −(z(H) + z(F))/2;
- the reference d′ is br50;
- 2,000 paired item-bootstrap resamples (flawed and correct items resampled separately);
- unparsed replies and refusals are excluded from rates and counted per condition.

**Primary measures**

1. ρ for the base-rate arm: Δc(br10 → br90) ÷ (ln 81 / d′(br50)).
2. Verdict-token confound: ρ(labels) − ρ(base rate), paired.
3. Tone: c(presuppose) − c(neutral) and c(lenient) − c(neutral), paired.

**Secondary measures**

- ρ for the use and payoff arms, and each minus the base-rate ρ (paired).
- c(br50) − c(neutral) and c(lab_neutral) − c(neutral).
- d′ per condition.
- Thinking on minus off for each primary measure.
- Unparsed and refusal rates, and output tokens per condition (especially presuppose).
- Effort probe: d′, misses, false alarms and output tokens vs default effort on the same items.

## Expectations (written before the data)

- **Base rate:** ρ will be higher than the open models' (0.05–0.30), roughly 0.2–0.6. Prior work finds that frontier models respond to stated rates.
- **Payoffs:** payoff ρ will be lower than base-rate ρ, as in every open model.
- **Label swap:** no large change (|ρ difference| < 0.2).
- **Tone:**
  - "presuppose" will make Sonnet more flag-happy (c − c(neutral) < 0). The new false alarms should fall on rigor-borderline correct solutions, such as `olympiadbench-690` and `omnimath-979` from Stage A.
  - "lenient" will move c the other way.
- **Thinking:** on vs off will differ little at default effort, because adaptive thinking barely engaged in Stage A (15/40 items).

## Decision rules for the full run (200 hard items, batch API)

- **Pipeline:**
  - Go ahead only if unparsed replies plus refusals are under 2% in every condition, and the batch returns a result for every request.
  - Otherwise fix the cause and re-run the affected cells first.
- **Item set:**
  - Use all 200 hard items (`data/items_hard.jsonl`).
  - Exception: if misses and false alarms both fall to ≤ 1/20 in neutral, br50 and lab_neutral, enrich the set with flawed-but-right-answer items before the full run.
- **Labels:**
  - If the paired ρ(labels) − ρ(base rate) CI excludes 0, or |difference| ≥ 0.25, run the full base-rate arm in both answer formats.
  - Otherwise the label swap stays a 3-condition control.
- **Thinking:**
  - Use max effort for the full run's "thinking on" arm if the probe meets any of these, compared with default effort on the same items:
    - d′ rises by ≥ 0.5;
    - ≥ 4/40 verdicts change;
    - it uses ≥ 3× the output tokens.
  - That choice depends on the cost, which is estimated first.
  - Otherwise keep default effort and report "thinking on" as "adaptive, default effort".
- **Reply length:** if more than 10% of replies in any condition exceed 2,000 output tokens, keep `--max-tokens` high in the full run and budget for it.
- **Strictness battery:** the full run adds the remaining framings (find_bugs, harsh, stakes_miss, stakes_fa, persona).

## Cost (from Stage A per-call costs: $0.0054 thinking off, $0.0057 thinking on, real time)

| step | calls | expected | limit |
|---|---|---|---|
| 1. thinking off, one batch (half price) | 480 | $1.2 | estimate gate $3.00; at most $5.41 if every reply used all 2,048 tokens |
| 2. thinking on, real time | 480 | $2.7 | hard cap $4.00 |
| 3. effort probe, real time | 40 | unknown ($1–3) | hard cap $2.50; stops early if reached |
| **total** | 1,000 | **≈ $5** | at most $11.91 |

Spent before Stage B: $0.73 (Stage A).

## What stays fixed

The items, conditions, prompts, analysis code and decision rules above. Bug fixes in the code are
allowed and are logged below.

## Deviations

1. **Pipeline rule at n = 40.** One thinking-off reply in br90 (`omnimath-484`, a flawed item) had no
   JSON. Sonnet reasoned that the solution was wrong and ended its turn (`end_turn`) without writing
   the answer object. That is 1/40 = 2.5%, over the "< 2% per condition" rule as written. At 40 items
   the rule allows no failures at all. The rule was meant to catch pipeline faults, and this is a
   model format slip. The trial stays unparsed and is **not re-run**: re-sampling only the
   failures would bias the sample. The full run keeps the 2% rule, which at 200 items allows up to 3
   failures per condition.
2. **Exploratory, not pre-registered:** the paired change in stated P(error) from br10 to br90, per
   item. Verdicts barely move, so this shows whether the stated rate moves confidence below the
   verdict threshold.

## Results (2026-11-07)

Spent **$5.26** (thinking-off batch $1.32, thinking on $2.96, effort probe $0.97); $5.98 in all so far.
Figure: `results/frontier/stage_b/stage_b.png`. Tables: `results/frontier/stage_b/summary.md`.

| | thinking off | thinking on |
|---|---|---|
| ρ, stated base rate | 0.07 [−0.02, 0.25] | 0.00 (same verdict on every item) |
| ρ, base rate + "use it" | 0.08 [0.00, 0.27] | 0.09 [0.00, 0.36] |
| ρ, payoffs | 0.00 | 0.30 [0.00, 0.63] |
| ρ(labels) − ρ(base rate), paired | +0.08 [0.00, 0.26] | +0.09 [0.00, 0.36] |
| c(presuppose) − c(neutral) | 0.00 | −0.14 [−0.51, 0.00] |
| c(lenient) − c(neutral) | +0.40 [0.00, 0.67] | +0.14 [0.00, 0.51] |
| items with the same verdict in all 13 conditions | 37/40 | 36/40 |
| unparsed / refused / cut off | 1 / 0 / 0 (of 520) | 0 / 0 / 0 |

- **Against expectations:**
  - Base-rate ρ is about 0, not 0.2–0.6: at or below every open model.
  - "Contains an error" does not make Sonnet flag more: 0.00 and −0.14, against −0.82 for qwen 27b with thinking.
- **As expected:**
  - Payoffs ≤ base rate with thinking off.
  - The label swap changes little.
  - "Lenient" moves c up.
  - Thinking on vs off differs little.
- **Wrong verdicts:** the same 4 items as in Stage A in almost every cell.
- **Max effort** (neutral): 4.7× the median output tokens of default effort, 0/40 verdicts changed, same 4 wrong items.
- **Exploratory Bayes check:**
  - A Bayesian that takes Sonnet's stated P(error) at br50 as its posterior would change 4 (off) / 3 (on) verdicts when told 10%, and 1 / 2 when told 90%.
  - Sonnet changed 0 / 1 and 1 / 1. *Correction (written before Stage C):* the "1" with thinking on, told 10%, was a flag added, not dropped. Counting only changes toward the stated rate, Sonnet changed 0 / 1 (thinking off) and 0 / 1 (thinking on), plus that one change the other way. `pilot/analyze.py` now counts the two directions separately; the figure is updated.
  - So most of the small ρ is what its extreme confidence implies. The deviation is one-sided: told errors are rare, it keeps flags it held at 55–85% confidence.
  - Because of this, ρ against the equal-variance ideal (ln 81 / d′) overstates how far a confident critic *should* move. The full run should report both benchmarks.

## Decision rules applied

| rule | outcome |
|---|---|
| Pipeline | Passes. One unparsed reply (deviation 1); the batch returned 480/480. |
| Item set | Not triggered (2/20 misses, 2/20 false alarms in neutral): use all 200 hard items. |
| Labels | Not triggered: paired CIs include 0 and |difference| < 0.25. The label swap stays a 3-condition control. |
| Thinking | **Triggered** by the token criterion (4.7× ≥ 3×). It was not triggered by d′ (+0.00) or by changed verdicts (0/40). The full run's "thinking on" arm uses max effort, subject to cost (below). |
| Reply length | Not triggered at default effort (no condition has replies > 2,000 tokens). Triggered for max effort (15/40 > 2,000): keep `--max-tokens 64000` there. |
| Strictness | Add find_bugs, harsh, stakes_miss, stakes_fa and persona. |

**Full-run cost** (batch prices measured here; 200 items × 18 conditions; Stage B trials reused):

| arm | cost |
|---|---|
| thinking off, 18 conditions | ≈ $8.5 |
| thinking on, default effort, 18 conditions | ≈ $9.5 |
| thinking on, max effort, 18 conditions | ≈ $43 (over the remaining $44 once thinking off is added) |
| thinking on, max effort, 6 core conditions (neutral, br10, br50, br90, presuppose, lenient) | ≈ $14 |

Max effort on all 18 conditions does not fit the $50 budget. Following the thinking rule within budget means:
- thinking off on all 18 conditions;
- max effort on the 6 core conditions;
- about $23 in all.
