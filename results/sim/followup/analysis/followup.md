# Rate-use follow-up: results

Plan: `prereg/rate_use_followup.md`. 25200 rows, 2 critic runs, 2000 whole-problem resamples, 20000 randomization draws where needed. ρ is [c(10%) − c(90%)] × d′(ref) / ln 81; intervals are descriptive.

## Labels and ceiling

Errors per 200 at `neutral`. At 4 or fewer, ρ is reported but not interpreted (marked \*).

| critic | original |
|---|---|
| sim-plain | 51.8 |
| sim-raised | 54.0 |

## original labels

### ρ by arm (d′ reference in brackets)

| critic | br | bayes | exp | paper_self | paper_other | paper_methods | paper_true |
|---|---|---|---|---|---|---|---|
| sim-plain | 0.50 [0.41, 0.62] (neutral) | 0.46 [0.37, 0.57] (neutral) | 0.45 [0.37, 0.55] (exp50) | 0.47 [0.38, 0.58] (neutral) | 0.49 [0.39, 0.60] (neutral) | 0.44 [0.36, 0.56] (neutral) | 0.57 [0.46, 0.73] (neutral) |
| sim-raised | 0.46 [0.37, 0.57] (neutral) | 0.80 [0.65, 0.99] (neutral) | 0.87 [0.73, 1.06] (exp50) | 0.78 [0.64, 0.95] (neutral) | 0.75 [0.62, 0.92] (neutral) | 0.48 [0.38, 0.61] (neutral) | 0.03 [-0.02, 0.08] (neutral) |

### Family A, attribution (exact within-item tests, Holm over the family)

| critic | test | contrast | predicted | difference in c [95%] | Holm p | outcome |
|---|---|---|---|---|---|---|
| sim-plain | A1 | note_bare − neutral | negative | -0.06 [-0.20, 0.07] | 0.6855 | not shown |
| sim-plain | A2 | claim_bare − note_bare | negative | -0.71 [-0.86, -0.56] | 0.0003 | held |
| sim-plain | A3 | note_bare − claim_random | none | -0.07 [-0.20, 0.07] | 0.6855 | no shift |
| sim-raised | A1 | note_bare − neutral | negative | -0.36 [-0.50, -0.23] | 0.0003 | held |
| sim-raised | A2 | claim_bare − note_bare | negative | -0.36 [-0.48, -0.24] | 0.0003 | held |
| sim-raised | A3 | note_bare − claim_random | none | -0.40 [-0.55, -0.26] | 0.0003 | held |

False alarms per 100 correct solutions:

| critic | neutral | note_bare | claim_bare | claim_random | claim_reviewer |
|---|---|---|---|---|---|
| sim-plain | 15 | 19 | 44 | 15 | 25 |
| sim-raised | 18 | 30 | 38 | 14 | 20 |

Reading: **sim-plain**: attribution alone discounts (A2 held, A3 no shift); **sim-raised**: the reliability statement does the work (A3 held and negative, A1 held)

### Family B, the posterior rule spelled out (studentized interaction test on c, Holm over the critics)

| critic | ρ, bayes | ρ, br | difference | Holm p | B1 raises use | B2 near ideal | stated P shift, bayes / br (log-odds) | verdict follows own posterior rule |
|---|---|---|---|---|---|---|---|---|
| sim-plain | 0.46 [0.37, 0.57] | 0.50 [0.41, 0.62] | -0.05 [-0.12, 0.03] | 0.2349 | no | no | 2.90 / 2.95 | 100% / 100% |
| sim-raised | 0.80 [0.65, 0.99] | 0.46 [0.37, 0.57] | +0.35 [0.24, 0.47] | 0.0010 | yes | yes | 4.95 / 2.97 | 100% / 100% |

### Family C, the rate shown in examples (studentized interaction test on c, Holm over the critics)

| critic | ρ, exp (d′ at exp50) | ρ, br | difference | Holm p | C1 raises use | C2 near ideal | d′(exp50) − d′(neutral) | c(exp50) − c(neutral) | C3 |
|---|---|---|---|---|---|---|---|---|---|
| sim-plain | 0.45 [0.37, 0.55] | 0.50 [0.41, 0.62] | -0.05 [-0.17, 0.06] | 0.5987 | no | no | -0.09 [-0.39, 0.19] | -0.07 [-0.21, 0.08] | no |
| sim-raised | 0.87 [0.73, 1.06] | 0.46 [0.37, 0.57] | +0.41 [0.25, 0.60] | 0.0010 | yes | yes | +0.10 [-0.18, 0.38] | +0.13 [-0.01, 0.27] | no |

### Family D, the paper (Opus only, exploratory)

| rule | contrast | ρ, first | ρ, second | difference | Holm p | outcome |
|---|---|---|---|---|---|---|
| D1 | self − br | 0.78 [0.64, 0.95] | 0.46 [0.37, 0.57] | +0.32 [0.21, 0.44] | 0.0015 | held |
| D2 | self − other | 0.78 [0.64, 0.95] | 0.75 [0.62, 0.92] | +0.03 [-0.06, 0.12] | 0.5677 | not shown |
| D3 | self − methods | 0.78 [0.64, 0.95] | 0.48 [0.38, 0.61] | +0.30 [0.21, 0.40] | 0.0015 | held |
| D4 | true − self | 0.03 [-0.02, 0.08] | 0.78 [0.64, 0.95] | -0.75 [-0.92, -0.61] | 0.0005 | held |

D5, overshoot: ρ_self 0.78 [0.64, 0.95]; no overshoot.

## Pipeline rules (original labels)

- **Unparsed:** sim-plain, neutral: 2.2% (over 2%). c with those trials counted as error: +0.27; correct: +0.35.
- **Unparsed:** sim-plain, br10: 2.0% (over 2%). Shift from neutral with those trials counted as error: +0.67; correct: +0.80.
- **Unparsed:** sim-plain, claim_reviewer: 2.8% (over 2%). Shift from neutral with those trials counted as error: -0.36; correct: -0.27.
- **Unparsed:** sim-plain, claim_random: 2.8% (over 2%). Shift from neutral with those trials counted as error: -0.06; correct: +0.04.
- **Unparsed:** sim-plain, note_bare: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.10; correct: -0.03.
- **Unparsed:** sim-plain, bayes10: 2.8% (over 2%). Shift from neutral with those trials counted as error: +0.56; correct: +0.72.
- **Unparsed:** sim-plain, exp50: 2.3% (over 2%). Shift from neutral with those trials counted as error: -0.10; correct: -0.03.
- **Unparsed:** sim-plain, exp90: 2.7% (over 2%). Shift from neutral with those trials counted as error: -0.89; correct: -0.79.
- **Unparsed:** sim-plain, paper_self10: 3.3% (over 2%). Shift from neutral with those trials counted as error: +0.57; correct: +0.75.
- **Unparsed:** sim-plain, paper_self90: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.82; correct: -0.74.
- **Unparsed:** sim-plain, paper_other90: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.76; correct: -0.69.
- **Unparsed:** sim-plain, paper_methods90: 2.5% (over 2%). Shift from neutral with those trials counted as error: -0.78; correct: -0.68.
- **Unparsed:** sim-plain, paper_true10: 2.3% (over 2%). Shift from neutral with those trials counted as error: +0.75; correct: +0.90.
- **Unparsed:** sim-raised, neutral: 2.5% (over 2%). c with those trials counted as error: +0.23; correct: +0.31.
- **Unparsed:** sim-raised, br10: 2.8% (over 2%). Shift from neutral with those trials counted as error: +0.74; correct: +0.94.
- **Unparsed:** sim-raised, br50: 4.5% (over 2%). Shift from neutral with those trials counted as error: +0.00; correct: +0.15.
- **Unparsed:** sim-raised, br90: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.69; correct: -0.63.
- **Unparsed:** sim-raised, claim_reviewer: 2.5% (over 2%). Shift from neutral with those trials counted as error: -0.19; correct: -0.12.
- **Unparsed:** sim-raised, claim_random: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.01; correct: +0.06.
- **Unparsed:** sim-raised, note_bare: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.40; correct: -0.34.
- **Unparsed:** sim-raised, bayes10: 2.3% (over 2%). Shift from neutral with those trials counted as error: +1.06; correct: +1.39.
- **Unparsed:** sim-raised, exp10: 2.3% (over 2%). Shift from neutral with those trials counted as error: +1.15; correct: +1.45.
- **Unparsed:** sim-raised, exp50: 2.2% (over 2%). Shift from neutral with those trials counted as error: +0.09; correct: +0.16.
- **Unparsed:** sim-raised, exp90: 2.2% (over 2%). Shift from neutral with those trials counted as error: -1.38; correct: -1.21.
- **Unparsed:** sim-raised, paper_self10: 2.3% (over 2%). Shift from neutral with those trials counted as error: +1.15; correct: +1.37.
- **Unparsed:** sim-raised, paper_other10: 3.5% (over 2%). Shift from neutral with those trials counted as error: +1.01; correct: +1.35.
- **Unparsed:** sim-raised, paper_other90: 2.0% (over 2%). Shift from neutral with those trials counted as error: -1.28; correct: -1.18.
- **Unparsed:** sim-raised, paper_methods10: 2.2% (over 2%). Shift from neutral with those trials counted as error: +0.76; correct: +0.93.
- **Unparsed:** sim-raised, paper_methods90: 2.7% (over 2%). Shift from neutral with those trials counted as error: -0.77; correct: -0.67.
- **Unparsed:** sim-raised, paper_true90: 2.5% (over 2%). Shift from neutral with those trials counted as error: -0.06; correct: +0.03.

