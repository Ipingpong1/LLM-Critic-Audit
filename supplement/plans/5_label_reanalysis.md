# Label re-analysis: what was fixed before running it

Written 2026-11-10, after the first commit of this repository (`8b4a2cc`) and before the re-analysis script existed. No one had judged an audit item. **Status: run on 2026-11-10; results at the end, under "Results". The audit variant has not been run, because no audit answers exist yet.** Everything above "Deviations" is as it was committed in `99d53ee`, apart from this status line. Changes made after the numbers came in are listed under "Deviations".

This is a re-analysis of saved replies. It costs nothing and collects no new data.

## Why

Every analysis so far takes ProcessBench's labels as the truth. On the hard set and the premise set, most thinking-on critics contradict the label on a small group of items, and they do so with no added line in the prompt. If those labels are wrong, the false-alarm rates, d′ and the ideal shift ln 81 / d′ are wrong with them, and ρ divides by that ideal shift.

A human audit of those items is prepared (`audit/audit_sheet.html`, sheet `b5c684be`), but it is several hours of work. This re-analysis asks a question that does not need the audit: **could any outcome of the audit change a headline claim?** It also fixes how the audit's answers will be used once they exist.

## What was already known when this was written

- Every original result in `README.md` and `results/*/analysis/`.
- How many items are contested and by how many critics.
- Claude, who wrote this plan and the script, has read the critics' objections to the contested items and believes at least one "correct" label is wrong. The PI has not been shown which items are contested or what the objections are.
- From the review on 2026-11-10: on the premise set, the neutral false-alarm rate of each thinking-on critic with the 12 most contested "correct" items left out. It fell for every critic.
- Not known: ρ, any threshold shift or any test under any relabelling.

## Items

- **Hard set:** `data/items_hard.jsonl`, 200 items. 14 critic runs: `results/torch_hard/*.jsonl` and `results/frontier/stage_c/*.jsonl`.
- **Premise set:** `data/items_premise.jsonl`, 200 items. 10 critic runs: `results/premise/*.jsonl`.
- **Contested items:** the items with group `contested_correct` or `contested_flawed` in `audit/audit_key.csv`. The rule that made them is in `scripts/build_audit_sheet.py`: at least half of the thinking-on critics contradict the label in most of their neutral replies. That gives 14 items on the premise set (all labelled correct) and 13 on the hard set (11 labelled correct, 2 labelled flawed). The key file is read as it is; the rule is not re-run.
- **Damaged text:** 3 items (1 hard, 2 premise) have a form-feed character where `\frac` should start in the problem statement, an upstream fault. The critics saw the damaged text.

## Label variants

| variant | what changes |
|---|---|
| `original` | nothing |
| `drop` | contested items are left out |
| `flip` | contested items take the opposite label |
| `no_damaged` | the 3 damaged-text items are left out; labels as original |
| `audit` | labels from an exported audit file (see "When the audit exists") |

`drop` and `flip` both favour the critics. The contested items were chosen because the critics disagree with their labels, so removing or reversing them raises d′ by construction. They are bounds, not estimates. For each contested item the truth is either the original label or its opposite, so an audit that judges every item lands between `original` and `flip`.

**Every assignment.** Because the audit could confirm some labels and reverse others, the point estimate of each quantity below is also computed under every one of the 2^k ways to keep or flip the k contested items of a set (2^13 on the hard set, 2^14 on the premise set), and the smallest and largest values are reported. This covers every audit outcome with no "can't tell" answers. It gives no intervals.

## What is recomputed

The same code as the original analyses, on relabelled rows: `analyze_model` in `pilot/analyze.py`, and `Critic` and `primary_tests` in `scripts/premise_analysis.py`. Same seeds (0) and the same number of resamples. Items are resampled within the classes of the variant in hand. Under `original` the script must reproduce the saved `summary.json` and `premise.json` exactly, and it says whether it did.

**Hard set** (reference d′ at `br50`, 2,000 resamples), per critic run:

1. ρ for the stated base rate (`br10` against `br90`).
2. ρ for the three other arms: the instruction to use the rate, the stated payoffs, and the "flawed"/"sound" verdict words.
3. c(`presuppose`) − c(`neutral`) and c(`lenient`) − c(`neutral`).

**Premise set:**

4. The 18 primary tests (T1–T9 for qwen3.5:27b and Opus 5.5, both thinking on), 10,000 resamples, Holm across the 18.
5. ρ for the stated base rate and ρ for a stated chance for this solution (reference d′ at `neutral`, 2,000 resamples), for the critics that ran them.

**Described, not judged** (these are expected to move): d′ at the reference condition, false alarms and hits at neutral, ρ_Bayes, and the AUC of the stated P(error) at neutral and under the claim conditions for the two primary critics.

## Reading rules

Each rule compares a variant with `original`. A claim **survives a variant** when its rule holds there.

- **R1, the stated rate is under-used.** For every critic run and arm in 1, 2 and 5 whose 95% interval for ρ lies below 1 under the original labels, the interval still lies below 1. The largest upper limit in each variant is reported.
- **R2, "contains an error" moves the threshold on the hard set.** For every critic run, c(`presuppose`) − c(`neutral`) keeps its sign and keeps whether its 95% interval excludes 0.
- **R3, the premise tests.** Each of the 18 tests keeps its outcome (held, moved, not shown, or against) under the same Holm procedure.
- **R4, every assignment.** Over all keep-or-flip assignments, the largest base-rate ρ of any critic run stays below 1, and each primary test that held under the original labels keeps the sign of its point estimate.

How the result will be used:

- **R1 to R4 all survive `drop`, `flip` and `no_damaged`:** the label question is reported as a robustness check. The audit is still worth doing, but the manuscript does not wait for it. The paper reports the original-label numbers as primary and these as the check.
- **Any rule fails:** that claim is reported with the failure next to it, and the audit blocks that claim.

Changes in d′, in false-alarm and hit rates, and in the size of ρ within its interval are not failures. They are reported so a reader can see how far the labels matter.

**Expectation, stated in advance:** R1 survives everywhere, since ρ compares thresholds on the same items and the ideal shift only shrinks as d′ rises. R2 and R3 probably survive. Neutral false-alarm rates fall a good deal.

## What this cannot show

- The contested rule finds only label faults that the critics notice. A "correct" label on a solution with an error that no critic catches is invisible to it. The 15 control items in the audit sheet are the only check on that, and they are too few to bound it tightly.
- Items flagged by one or two critics are in neither group and are not audited.
- `drop` and `flip` are chosen using the neutral replies, which also enter the estimates. That is why they are bounds.

## When the audit exists

`scripts/label_sensitivity.py --audit audit/<file>.csv` adds the audit variant. Fixed now:

- The file's sheet id must match the key, or the script stops.
- An item judged **error** is flawed. **No error** is correct. **Can't tell** leaves the item out. An item not yet judged keeps its original label, and the report says how many there were.
- **Gap only** has two readings, and both are reported: correct (primary, since ProcessBench marks erroneous steps, not unjustified ones) and flawed (secondary).
- The audit covers all 42 sheet items, controls included, so a control's label can change too.
- The report gives, per group of the sheet (contested correct, contested flawed, control correct, control flawed), how many items the auditor called error, gap, no error and can't tell. For items labelled flawed it also says how often the auditor's earliest step matches the label's.
- R1 to R3 are then read on the audit variant in the same way. With more than one auditor file, each is reported separately.

## Outputs

`results/label_sensitivity/report.md` and `report.json`. No item is named in either.

## Deviations

- **Two counts were added after the first run.** The rules ask whether an interval for ρ stays below 1. The first run showed two things they do not cover: the estimate itself can move a long way while the interval stays below 1, and relabelling can leave a critic with almost no errors. The report now also counts the ρ estimates that leave their original 95% interval, and the critic runs that fall under the ceiling rule of `prereg/premise.md` (4 or fewer errors per 200 at neutral). Both are marked in the report as added. Nothing else in the script changed, and every number of the first run is identical in the second.
- **Smoke tests came first.** The script was run twice with 100 and 200 resamples before the planned run, writing to a temporary folder. That showed rough versions of the results early.
- **The audit path was tested on made-up answers.** A file of random verdicts, in a temporary folder. No real audit answer exists.

## Results (2026-11-10)

Tables: `results/label_sensitivity/report.md`. Under the original labels the script reproduces all 323 saved numbers it compares, exactly.

**Read by the rules**

| rule | contested left out | contested flipped | damaged text left out |
|---|---|---|---|
| R1, intervals for ρ stay below 1 (63 cases) | fails in 1 | fails in 1 | survives |
| R2, "contains an error" on the hard set (14 critic runs) | survives | survives | survives |
| R3, the 18 premise tests | survives | survives | survives |

- **R4 survives.** Over every keep-or-flip assignment, the largest base-rate ρ of any critic run is 0.68 (qwen3.5:4b, thinking on, hard set). None of the 16 tests that held can change sign.
- **R3:** all 18 tests keep their outcome, 16 held and 2 not shown. Every shift that held is larger with the contested items left out or flipped.
- **R1 fails in the same case under both variants:** qwen3.5:27b with thinking on, told a chance for this solution. Its ρ goes from 0.47 [0.26, 0.65] to 0.85 [0.56, 1.16] with the contested items left out and 0.78 [0.55, 1.11] with them flipped. By the rule fixed above, the audit blocks the under-use claim for that critic and arm. The expectation stated in advance, that R1 would survive everywhere, was wrong here.
- **The 3 damaged-text items change nothing.**

**Beyond the rules: the size of ρ for thinking-on critics depends on the contested labels**

- With the contested items left out, 13 of 63 estimates leave their original 95% interval; with them flipped, 10 of 63. All move up except one payoff estimate. All but three are thinking-on runs, and those three are Sonnet 5.5 with thinking off.
- On the hard set, Opus 5.5 goes from 0.21 [0.05, 0.44] to 0.55 [0.18, 0.96] (left out) and 0.45 [0.17, 0.91] (flipped). Sonnet 5.5 with thinking on goes from 0.13 to 0.44 and 0.39. On the premise set, qwen3.5:27b with thinking on goes from 0.36 to 0.61 and 0.55.
- The other thinking-off runs barely move: their base-rate ρ is at most 0.20 in every variant.
- Both parts of ρ move. For Opus on the hard set with the contested items left out, d′ rises from 3.12 to 4.49, so the ideal shift falls from 1.41 to 0.98, and the observed shift rises from 0.29 to 0.54. The contested items are flagged whatever rate is stated, so they hold the false-alarm rate up in every condition and hide the few verdicts that do change.
- **Ceiling.** With the contested items left out, Opus and all three Sonnet runs make 4 or fewer errors per 200 at neutral on the hard set, and so do Opus and three open thinking-on runs on the premise set. The project's own rule says shifts of such critics are reported but not interpreted. If the audit sides with the critics, the hard set is no longer hard for the frontier critics, and their ρ is poorly measured as well as larger.

**Described**

- Neutral false alarms of the thinking-on critics fall from 4–19 per 100 correct solutions to 0–9.
- Opus's stated P(error) keeps an AUC of 0.98 or more under every claim in every variant. For qwen3.5:27b it is 0.85–0.89 under the claims with the original labels and 0.89–0.94 with the contested items left out or flipped.

**What follows**

- **The claim tests do not depend on the contested labels.** They can be written up as they stand, with this as the robustness check.
- **Under-use holds in direction.** 62 of 63 intervals stay below 1, and no assignment takes a base-rate point estimate above 0.68.
- **How much the thinking-on critics under-use the rate is not settled.** "About a fifth of the ideal" for Opus and Sonnet holds only if the contested labels are right. If they are wrong it is about a half, measured near the ceiling. The audit decides which, so the audit is needed before the manuscript states a size for those critics. It is not needed for the thinking-off critics or for the claim tests.
