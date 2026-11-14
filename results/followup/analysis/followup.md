# Rate-use follow-up: results

Plan: `prereg/rate_use_followup.md`. 170400 rows, 12 critic runs, 10000 whole-problem resamples, 200000 randomization draws where needed. ρ is [c(10%) − c(90%)] × d′(ref) / ln 81; intervals are descriptive.

## Labels and ceiling

Errors per 200 at `neutral`. At 4 or fewer, ρ is reported but not interpreted (marked \*).

| critic | original | contested left out | contested flipped |
|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 21.3 | 13.6 | 18.0 |
| gemma4:12b-think-bf16-t1 | 11.8 | 1.8\* | 5.7 |
| gpt-6-luna-think | 21.7 | 9.7 | 10.3 |
| gpt-6.1-sol-think | 27.0 | 15.1 | 15.0 |
| haiku-5.5-think | 17.7 | 5.4 | 6.3 |
| opus-5.5-think | 16.0 | 3.8\* | 5.0 |
| qwen3.5:4b-nothink-bf16-t1 | 52.7 | 43.7 | 42.7 |
| qwen3.5:4b-think-bf16-t1 | 15.3 | 3.6\* | 5.3 |
| qwen3.5:9b-nothink-bf16-t1 | 47.4 | 36.3 | 34.1 |
| qwen3.5:9b-think-bf16-t1 | 16.0 | 3.9\* | 5.3 |
| qwen3.5:27b-nothink-bf16-t1 | 29.3 | 17.9 | 18.0 |
| qwen3.5:27b-think-bf16-t1 | 19.5 | 6.5 | 6.7 |

## original labels

### ρ by arm (d′ reference in brackets)

| critic | br | bayes | exp | paper_self | paper_other | paper_methods | paper_true |
|---|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.07 [0.02, 0.14] (neutral) | 0.08 [0.04, 0.14] (neutral) | 0.03 [-0.04, 0.10] (exp50) | – | – | – | – |
| gemma4:12b-think-bf16-t1 | 0.07 [-0.13, 0.23] (neutral) | – | – | – | – | – | – |
| gpt-6-luna-think | 0.07 [-0.01, 0.19] (neutral) | 0.03 [-0.02, 0.07] (neutral) | 0.01 [-0.02, 0.04] (exp50) | – | – | – | – |
| gpt-6.1-sol-think | 0.17 [0.00, 0.32] (neutral) | 0.17 [0.00, 0.32] (neutral) | 0.03 [0.00, 0.08] (exp50) | – | – | – | – |
| haiku-5.5-think | 0.02 [-0.01, 0.05] (neutral) | 0.13 [-0.05, 0.27] (neutral) | -0.10 [-0.22, 0.06] (exp50) | – | – | – | – |
| opus-5.5-think | 0.29 [0.09, 0.43] (neutral) | 0.11 [0.04, 0.21] (neutral) | -0.12 [-0.25, 0.07] (exp50) | 0.05 [0.01, 0.12] (neutral) | 0.21 [0.01, 0.35] (neutral) | 0.08 [0.03, 0.17] (neutral) | 0.07 [0.00, 0.16] (neutral) |
| qwen3.5:4b-nothink-bf16-t1 | 0.14 [0.10, 0.21] (neutral) | 0.09 [0.06, 0.15] (neutral) | 0.09 [0.05, 0.15] (exp50) | – | – | – | – |
| qwen3.5:4b-think-bf16-t1 | 0.14 [0.07, 0.22] (neutral) | – | – | – | – | – | – |
| qwen3.5:9b-nothink-bf16-t1 | 0.08 [0.05, 0.13] (neutral) | 0.08 [0.05, 0.12] (neutral) | 0.04 [-0.00, 0.10] (exp50) | – | – | – | – |
| qwen3.5:9b-think-bf16-t1 | 0.20 [0.08, 0.33] (neutral) | – | – | – | – | – | – |
| qwen3.5:27b-nothink-bf16-t1 | 0.07 [0.04, 0.11] (neutral) | 0.11 [0.07, 0.16] (neutral) | 0.07 [0.02, 0.13] (exp50) | – | – | – | – |
| qwen3.5:27b-think-bf16-t1 | 0.36 [0.23, 0.50] (neutral) | 0.35 [0.22, 0.49] (neutral) | 0.22 [0.10, 0.33] (exp50) | – | – | – | – |

### Family A, attribution (exact within-item tests, Holm over the family)

| critic | test | contrast | predicted | difference in c [95%] | Holm p | outcome |
|---|---|---|---|---|---|---|
| gpt-6.1-sol-think | A1 | note_bare − neutral | negative | -0.01 [-0.05, 0.00] | 1.0000 | not shown |
| gpt-6.1-sol-think | A2 | claim_bare − note_bare | negative | -1.58 [-1.71, -1.45] | 0.0000 | held |
| gpt-6.1-sol-think | A3 | note_bare − claim_random | none | -0.01 [-0.05, 0.00] | 1.0000 | no shift |
| opus-5.5-think | A1 | note_bare − neutral | negative | -0.36 [-0.59, -0.09] | 0.0002 | held |
| opus-5.5-think | A2 | claim_bare − note_bare | negative | -0.95 [-1.17, -0.79] | 0.0000 | held |
| opus-5.5-think | A3 | note_bare − claim_random | none | -0.23 [-0.37, -0.12] | 0.0020 | held |
| qwen3.5:27b-think-bf16-t1 | A1 | note_bare − neutral | negative | -0.45 [-0.57, -0.35] | 0.0000 | held |
| qwen3.5:27b-think-bf16-t1 | A2 | claim_bare − note_bare | negative | +0.06 [-0.01, 0.14] | 0.3010 | not shown |
| qwen3.5:27b-think-bf16-t1 | A3 | note_bare − claim_random | none | -0.38 [-0.50, -0.28] | 0.0000 | held |

False alarms per 100 correct solutions:

| critic | neutral | note_bare | claim_bare | claim_random | claim_reviewer |
|---|---|---|---|---|---|
| gpt-6.1-sol-think | 27 | 28 | 100 | 27 | 28 |
| opus-5.5-think | 15 | 24 | 89 | 12 | 22 |
| qwen3.5:27b-think-bf16-t1 | 19 | 52 | 47 | 23 | 50 |

Reading: **opus-5.5-think**: the reliability statement does the work (A3 held and negative, A1 held); **qwen3.5:27b-think-bf16-t1**: the reliability statement does the work (A3 held and negative, A1 held); **gpt-6.1-sol-think**: attribution alone discounts (A2 held, A3 no shift)

### Family B, the posterior rule spelled out (studentized interaction test on c, Holm over the critics)

| critic | ρ, bayes | ρ, br | difference | Holm p | B1 raises use | B2 near ideal | stated P shift, bayes / br (log-odds) | verdict follows own posterior rule |
|---|---|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.08 [0.04, 0.14] | 0.07 [0.02, 0.14] | +0.01 [-0.06, 0.08] | 1.0000 (descriptive) | no | no | -0.09 / 0.19 | 100% / 100% |
| gpt-6-luna-think | 0.03 [-0.02, 0.07] | 0.07 [-0.01, 0.19] | -0.04 [-0.18, 0.03] | 1.0000 (descriptive) | no | no | 0.05 / 0.04 | 100% / 100% |
| gpt-6.1-sol-think | 0.17 [0.00, 0.32] | 0.17 [0.00, 0.32] | -0.00 [-0.03, 0.03] | 1.0000 (descriptive) | no | no | 0.16 / 0.13 | 100% / 100% |
| haiku-5.5-think | 0.13 [-0.05, 0.27] | 0.02 [-0.01, 0.05] | +0.11 [-0.08, 0.26] | 1.0000 (descriptive) | no | no | 0.04 / 0.18 | 100% / 100% |
| opus-5.5-think | 0.11 [0.04, 0.21] | 0.29 [0.09, 0.43] | -0.18 [-0.31, 0.01] | 1.0000 (descriptive) | no | no | 0.53 / 0.55 | 100% / 100% |
| qwen3.5:4b-nothink-bf16-t1 | 0.09 [0.06, 0.15] | 0.14 [0.10, 0.21] | -0.05 [-0.12, 0.01] | 0.6591 | no | no | 0.93 / 1.10 | 100% / 100% |
| qwen3.5:9b-nothink-bf16-t1 | 0.08 [0.05, 0.12] | 0.08 [0.05, 0.13] | -0.00 [-0.05, 0.04] | 1.0000 | no | no | 0.55 / 0.58 | 100% / 100% |
| qwen3.5:27b-nothink-bf16-t1 | 0.11 [0.07, 0.16] | 0.07 [0.04, 0.11] | +0.04 [-0.00, 0.09] | 0.5939 | no | no | 0.58 / 0.35 | 100% / 100% |
| qwen3.5:27b-think-bf16-t1 | 0.35 [0.22, 0.49] | 0.36 [0.23, 0.50] | -0.01 [-0.07, 0.04] | 1.0000 | no | no | 1.00 / 1.06 | 100% / 100% |

### Family C, the rate shown in examples (studentized interaction test on c, Holm over the critics)

| critic | ρ, exp (d′ at exp50) | ρ, br | difference | Holm p | C1 raises use | C2 near ideal | d′(exp50) − d′(neutral) | c(exp50) − c(neutral) | C3 |
|---|---|---|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.03 [-0.04, 0.10] | 0.07 [0.02, 0.14] | -0.04 [-0.14, 0.03] | 1.0000 (descriptive) | no | no | -0.17 [-0.51, 0.09] | -0.03 [-0.17, 0.14] | no |
| gpt-6-luna-think | 0.01 [-0.02, 0.04] | 0.07 [-0.01, 0.19] | -0.06 [-0.19, 0.03] | 1.0000 (descriptive) | no | no | +0.13 [-0.31, 0.64] | -0.06 [-0.32, 0.15] | no |
| gpt-6.1-sol-think | 0.03 [0.00, 0.08] | 0.17 [0.00, 0.32] | -0.14 [-0.29, 0.04] | 1.0000 (descriptive) | no | no | +0.06 [0.00, 0.16] | +0.03 [0.00, 0.08] | no |
| haiku-5.5-think | -0.10 [-0.22, 0.06] | 0.02 [-0.01, 0.05] | -0.11 [-0.25, 0.05] | 1.0000 (descriptive) | no | no | -0.29 [-0.61, 0.19] | +0.34 [0.10, 0.50] | no |
| opus-5.5-think | -0.12 [-0.25, 0.07] | 0.29 [0.09, 0.43] | -0.41 [-0.65, -0.06] | 1.0000 (descriptive) | no | no | +0.04 [-0.12, 0.22] | +0.02 [-0.06, 0.11] | no |
| qwen3.5:4b-nothink-bf16-t1 | 0.09 [0.05, 0.15] | 0.14 [0.10, 0.21] | -0.05 [-0.11, 0.01] | 1.0000 | no | no | -0.16 [-0.46, 0.14] | -0.29 [-0.44, -0.14] | no |
| qwen3.5:9b-nothink-bf16-t1 | 0.04 [-0.00, 0.10] | 0.08 [0.05, 0.13] | -0.04 [-0.11, 0.02] | 1.0000 | no | no | -0.11 [-0.44, 0.22] | -0.19 [-0.35, -0.03] | no |
| qwen3.5:27b-nothink-bf16-t1 | 0.07 [0.02, 0.13] | 0.07 [0.04, 0.11] | +0.00 [-0.06, 0.07] | 1.0000 | no | no | -0.17 [-0.48, 0.11] | -0.18 [-0.33, -0.03] | no |
| qwen3.5:27b-think-bf16-t1 | 0.22 [0.10, 0.33] | 0.36 [0.23, 0.50] | -0.15 [-0.32, 0.02] | 1.0000 | no | no | -0.09 [-0.21, 0.02] | -0.05 [-0.11, 0.00] | no |

### Family D, the paper (Opus only, exploratory)

| rule | contrast | ρ, first | ρ, second | difference | Holm p | outcome |
|---|---|---|---|---|---|---|
| D1 | self − br | 0.05 [0.01, 0.12] | 0.29 [0.09, 0.43] | -0.24 [-0.38, -0.04] | 1.0000 (descriptive) | not shown |
| D2 | self − other | 0.05 [0.01, 0.12] | 0.21 [0.01, 0.35] | -0.16 [-0.30, 0.05] | 1.0000 (descriptive) | not shown |
| D3 | self − methods | 0.05 [0.01, 0.12] | 0.08 [0.03, 0.17] | -0.03 [-0.11, 0.03] | 1.0000 (descriptive) | not shown |
| D4 | true − self | 0.07 [0.00, 0.16] | 0.05 [0.01, 0.12] | +0.02 [-0.08, 0.11] | 1.0000 (descriptive) | not shown |

D5, overshoot: ρ_self 0.05 [0.01, 0.12]; no overshoot.

## contested left out labels

### ρ by arm (d′ reference in brackets)

| critic | br | bayes | exp | paper_self | paper_other | paper_methods | paper_true |
|---|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.09 [0.03, 0.18] (neutral) | 0.11 [0.06, 0.19] (neutral) | 0.05 [-0.05, 0.17] (exp50) | – | – | – | – |
| gemma4:12b-think-bf16-t1\* | 0.19 [-0.07, 0.43] (neutral) | – | – | – | – | – | – |
| gpt-6-luna-think | 0.09 [-0.03, 0.24] (neutral) | 0.03 [-0.06, 0.12] (neutral) | 0.01 [-0.08, 0.11] (exp50) | – | – | – | – |
| gpt-6.1-sol-think | 0.20 [0.00, 0.39] (neutral) | 0.20 [0.00, 0.38] (neutral) | 0.06 [0.00, 0.15] (exp50) | – | – | – | – |
| haiku-5.5-think | 0.06 [-0.04, 0.20] (neutral) | 0.04 [-0.24, 0.29] (neutral) | -0.15 [-0.37, 0.14] (exp50) | – | – | – | – |
| opus-5.5-think\* | 0.49 [0.18, 0.80] (neutral) | 0.31 [0.10, 0.61] (neutral) | -0.13 [-0.31, 0.18] (exp50) | 0.15 [0.03, 0.37] (neutral) | 0.29 [-0.04, 0.56] (neutral) | 0.21 [0.06, 0.51] (neutral) | 0.12 [-0.05, 0.38] (neutral) |
| qwen3.5:4b-nothink-bf16-t1 | 0.16 [0.11, 0.24] (neutral) | 0.10 [0.06, 0.17] (neutral) | 0.11 [0.06, 0.17] (exp50) | – | – | – | – |
| qwen3.5:4b-think-bf16-t1\* | 0.32 [0.20, 0.46] (neutral) | – | – | – | – | – | – |
| qwen3.5:9b-nothink-bf16-t1 | 0.09 [0.05, 0.15] (neutral) | 0.09 [0.06, 0.14] (neutral) | 0.05 [-0.00, 0.12] (exp50) | – | – | – | – |
| qwen3.5:9b-think-bf16-t1\* | 0.32 [0.15, 0.48] (neutral) | – | – | – | – | – | – |
| qwen3.5:27b-nothink-bf16-t1 | 0.09 [0.05, 0.14] (neutral) | 0.16 [0.10, 0.23] (neutral) | 0.10 [0.04, 0.18] (exp50) | – | – | – | – |
| qwen3.5:27b-think-bf16-t1 | 0.61 [0.44, 0.83] (neutral) | 0.62 [0.46, 0.82] (neutral) | 0.41 [0.24, 0.59] (exp50) | – | – | – | – |

### Family A, attribution (exact within-item tests, Holm over the family)

| critic | test | contrast | predicted | difference in c [95%] | Holm p | outcome |
|---|---|---|---|---|---|---|
| gpt-6.1-sol-think | A1 | note_bare − neutral | negative | -0.02 [-0.08, 0.00] | 1.0000 | not shown |
| gpt-6.1-sol-think | A2 | claim_bare − note_bare | negative | -1.72 [-1.91, -1.59] | 0.0000 | held |
| gpt-6.1-sol-think | A3 | note_bare − claim_random | none | -0.02 [-0.08, 0.00] | 1.0000 | no shift |
| opus-5.5-think | A1 | note_bare − neutral | negative | -0.55 [-0.89, -0.23] | 0.0003 | held |
| opus-5.5-think | A2 | claim_bare − note_bare | negative | -1.12 [-1.37, -0.92] | 0.0000 | held |
| opus-5.5-think | A3 | note_bare − claim_random | none | -0.50 [-0.80, -0.28] | 0.0078 | held |
| qwen3.5:27b-think-bf16-t1 | A1 | note_bare − neutral | negative | -0.65 [-0.82, -0.52] | 0.0000 | held |
| qwen3.5:27b-think-bf16-t1 | A2 | claim_bare − note_bare | negative | +0.07 [-0.01, 0.16] | 0.3172 | not shown |
| qwen3.5:27b-think-bf16-t1 | A3 | note_bare − claim_random | none | -0.52 [-0.68, -0.40] | 0.0000 | held |

False alarms per 100 correct solutions:

| critic | neutral | note_bare | claim_bare | claim_random | claim_reviewer |
|---|---|---|---|---|---|
| gpt-6.1-sol-think | 16 | 17 | 100 | 16 | 17 |
| opus-5.5-think | 3 | 13 | 87 | 1 | 10 |
| qwen3.5:27b-think-bf16-t1 | 7 | 44 | 38 | 11 | 42 |

Reading: **opus-5.5-think**: the reliability statement does the work (A3 held and negative, A1 held); **qwen3.5:27b-think-bf16-t1**: the reliability statement does the work (A3 held and negative, A1 held); **gpt-6.1-sol-think**: attribution alone discounts (A2 held, A3 no shift)

### Family B, the posterior rule spelled out (studentized interaction test on c, Holm over the critics)

| critic | ρ, bayes | ρ, br | difference | Holm p | B1 raises use | B2 near ideal | stated P shift, bayes / br (log-odds) | verdict follows own posterior rule |
|---|---|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.11 [0.06, 0.19] | 0.09 [0.03, 0.18] | +0.02 [-0.08, 0.12] | 1.0000 (descriptive) | no | no | -0.09 / 0.17 | 100% / 100% |
| gpt-6-luna-think | 0.03 [-0.06, 0.12] | 0.09 [-0.03, 0.24] | -0.06 [-0.23, 0.07] | 1.0000 (descriptive) | no | no | 0.04 / 0.06 | 100% / 100% |
| gpt-6.1-sol-think | 0.20 [0.00, 0.38] | 0.20 [0.00, 0.39] | -0.00 [-0.06, 0.06] | 1.0000 (descriptive) | no | no | 0.16 / 0.14 | 100% / 100% |
| haiku-5.5-think | 0.04 [-0.24, 0.29] | 0.06 [-0.04, 0.20] | -0.03 [-0.29, 0.23] | 1.0000 (descriptive) | no | no | 0.05 / 0.16 | 100% / 100% |
| opus-5.5-think\* | 0.31 [0.10, 0.61] | 0.49 [0.18, 0.80] | -0.18 [-0.38, 0.10] | 1.0000 (descriptive) | no | no | 0.50 / 0.50 | 100% / 100% |
| qwen3.5:4b-nothink-bf16-t1 | 0.10 [0.06, 0.17] | 0.16 [0.11, 0.24] | -0.06 [-0.13, 0.01] | 0.4880 | no | no | 0.93 / 1.12 | 100% / 99% |
| qwen3.5:9b-nothink-bf16-t1 | 0.09 [0.06, 0.14] | 0.09 [0.05, 0.15] | -0.00 [-0.06, 0.05] | 1.0000 | no | no | 0.54 / 0.56 | 100% / 100% |
| qwen3.5:27b-nothink-bf16-t1 | 0.16 [0.10, 0.23] | 0.09 [0.05, 0.14] | +0.07 [0.01, 0.14] | 0.2448 | no | no | 0.60 / 0.32 | 100% / 100% |
| qwen3.5:27b-think-bf16-t1 | 0.62 [0.46, 0.82] | 0.61 [0.44, 0.83] | +0.01 [-0.12, 0.13] | 1.0000 | no | no | 1.02 / 1.10 | 100% / 100% |

### Family C, the rate shown in examples (studentized interaction test on c, Holm over the critics)

| critic | ρ, exp (d′ at exp50) | ρ, br | difference | Holm p | C1 raises use | C2 near ideal | d′(exp50) − d′(neutral) | c(exp50) − c(neutral) | C3 |
|---|---|---|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.05 [-0.05, 0.17] | 0.09 [0.03, 0.18] | -0.03 [-0.16, 0.08] | 1.0000 (descriptive) | no | no | -0.21 [-0.59, 0.11] | -0.05 [-0.21, 0.14] | no |
| gpt-6-luna-think | 0.01 [-0.08, 0.11] | 0.09 [-0.03, 0.24] | -0.08 [-0.24, 0.05] | 1.0000 (descriptive) | no | no | +0.13 [-0.33, 0.67] | -0.06 [-0.33, 0.17] | no |
| gpt-6.1-sol-think | 0.06 [0.00, 0.15] | 0.20 [0.00, 0.39] | -0.14 [-0.32, 0.08] | 1.0000 (descriptive) | no | no | +0.10 [0.00, 0.26] | +0.05 [0.00, 0.13] | no |
| haiku-5.5-think | -0.15 [-0.37, 0.14] | 0.06 [-0.04, 0.20] | -0.21 [-0.53, 0.16] | 1.0000 (descriptive) | no | no | +0.10 [-0.32, 0.69] | +0.54 [0.27, 0.78] | no |
| opus-5.5-think\* | -0.13 [-0.31, 0.18] | 0.49 [0.18, 0.80] | -0.62 [-1.05, -0.08] | 1.0000 (descriptive) | no | no | -0.07 [-0.53, 0.42] | -0.04 [-0.26, 0.21] | no |
| qwen3.5:4b-nothink-bf16-t1 | 0.11 [0.06, 0.17] | 0.16 [0.11, 0.24] | -0.05 [-0.13, 0.01] | 1.0000 | no | no | -0.23 [-0.54, 0.08] | -0.32 [-0.48, -0.17] | no |
| qwen3.5:9b-nothink-bf16-t1 | 0.05 [-0.00, 0.12] | 0.09 [0.05, 0.15] | -0.04 [-0.12, 0.03] | 1.0000 | no | no | -0.18 [-0.54, 0.17] | -0.22 [-0.40, -0.05] | no |
| qwen3.5:27b-nothink-bf16-t1 | 0.10 [0.04, 0.18] | 0.09 [0.05, 0.14] | +0.02 [-0.07, 0.10] | 1.0000 | no | no | -0.42 [-0.80, -0.09] | -0.31 [-0.49, -0.13] | no |
| qwen3.5:27b-think-bf16-t1 | 0.41 [0.24, 0.59] | 0.61 [0.44, 0.83] | -0.20 [-0.45, 0.02] | 1.0000 | no | no | -0.16 [-0.42, 0.05] | -0.09 [-0.22, 0.02] | no |

### Family D, the paper (Opus only, exploratory) \*ceiling

| rule | contrast | ρ, first | ρ, second | difference | Holm p | outcome |
|---|---|---|---|---|---|---|
| D1 | self − br | 0.15 [0.03, 0.37] | 0.49 [0.18, 0.80] | -0.34 [-0.63, -0.00] | 1.0000 (descriptive) | not shown |
| D2 | self − other | 0.15 [0.03, 0.37] | 0.29 [-0.04, 0.56] | -0.14 [-0.42, 0.26] | 1.0000 (descriptive) | not shown |
| D3 | self − methods | 0.15 [0.03, 0.37] | 0.21 [0.06, 0.51] | -0.05 [-0.34, 0.18] | 1.0000 (descriptive) | not shown |
| D4 | true − self | 0.12 [-0.05, 0.38] | 0.15 [0.03, 0.37] | -0.03 [-0.35, 0.25] | 1.0000 (descriptive) | not shown |

D5, overshoot: ρ_self 0.15 [0.03, 0.37]; no overshoot.

## contested flipped labels

### ρ by arm (d′ reference in brackets)

| critic | br | bayes | exp | paper_self | paper_other | paper_methods | paper_true |
|---|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.07 [0.03, 0.14] (neutral) | 0.10 [0.05, 0.17] (neutral) | 0.04 [-0.04, 0.13] (exp50) | – | – | – | – |
| gemma4:12b-think-bf16-t1 | 0.12 [-0.03, 0.29] (neutral) | – | – | – | – | – | – |
| gpt-6-luna-think | 0.04 [-0.06, 0.18] (neutral) | 0.04 [-0.04, 0.15] (neutral) | 0.03 [-0.06, 0.13] (exp50) | – | – | – | – |
| gpt-6.1-sol-think | 0.11 [0.00, 0.35] (neutral) | 0.11 [0.00, 0.34] (neutral) | 0.06 [0.00, 0.14] (exp50) | – | – | – | – |
| haiku-5.5-think | 0.06 [-0.10, 0.19] (neutral) | -0.08 [-0.27, 0.17] (neutral) | 0.02 [-0.25, 0.27] (exp50) | – | – | – | – |
| opus-5.5-think | 0.56 [0.29, 1.01] (neutral) | 0.40 [0.16, 0.81] (neutral) | 0.05 [-0.21, 0.32] (exp50) | 0.14 [0.03, 0.36] (neutral) | 0.30 [0.05, 0.66] (neutral) | 0.28 [0.08, 0.67] (neutral) | 0.26 [0.03, 0.63] (neutral) |
| qwen3.5:4b-nothink-bf16-t1 | 0.15 [0.11, 0.22] (neutral) | 0.12 [0.07, 0.19] (neutral) | 0.10 [0.05, 0.15] (exp50) | – | – | – | – |
| qwen3.5:4b-think-bf16-t1 | 0.47 [0.22, 0.68] (neutral) | – | – | – | – | – | – |
| qwen3.5:9b-nothink-bf16-t1 | 0.10 [0.06, 0.17] (neutral) | 0.10 [0.07, 0.15] (neutral) | 0.05 [0.00, 0.11] (exp50) | – | – | – | – |
| qwen3.5:9b-think-bf16-t1 | 0.37 [0.23, 0.55] (neutral) | – | – | – | – | – | – |
| qwen3.5:27b-nothink-bf16-t1 | 0.10 [0.06, 0.15] (neutral) | 0.16 [0.10, 0.23] (neutral) | 0.08 [0.02, 0.16] (exp50) | – | – | – | – |
| qwen3.5:27b-think-bf16-t1 | 0.55 [0.41, 0.77] (neutral) | 0.63 [0.49, 0.83] (neutral) | 0.52 [0.32, 0.70] (exp50) | – | – | – | – |

### Family A, attribution (exact within-item tests, Holm over the family)

| critic | test | contrast | predicted | difference in c [95%] | Holm p | outcome |
|---|---|---|---|---|---|---|
| gpt-6.1-sol-think | A1 | note_bare − neutral | negative | -0.02 [-0.08, 0.00] | 1.0000 | not shown |
| gpt-6.1-sol-think | A2 | claim_bare − note_bare | negative | -1.92 [-2.18, -1.62] | 0.0000 | held |
| gpt-6.1-sol-think | A3 | note_bare − claim_random | none | -0.02 [-0.08, 0.00] | 1.0000 | no shift |
| opus-5.5-think | A1 | note_bare − neutral | negative | -0.49 [-0.87, -0.25] | 0.0002 | held |
| opus-5.5-think | A2 | claim_bare − note_bare | negative | -1.32 [-1.63, -0.97] | 0.0000 | held |
| opus-5.5-think | A3 | note_bare − claim_random | none | -0.67 [-1.10, -0.36] | 0.0020 | held |
| qwen3.5:27b-think-bf16-t1 | A1 | note_bare − neutral | negative | -0.71 [-0.92, -0.54] | 0.0000 | held |
| qwen3.5:27b-think-bf16-t1 | A2 | claim_bare − note_bare | negative | +0.07 [-0.01, 0.16] | 0.3172 | not shown |
| qwen3.5:27b-think-bf16-t1 | A3 | note_bare − claim_random | none | -0.52 [-0.68, -0.40] | 0.0000 | held |

False alarms per 100 correct solutions:

| critic | neutral | note_bare | claim_bare | claim_random | claim_reviewer |
|---|---|---|---|---|---|
| gpt-6.1-sol-think | 16 | 17 | 100 | 16 | 17 |
| opus-5.5-think | 3 | 13 | 87 | 1 | 10 |
| qwen3.5:27b-think-bf16-t1 | 7 | 44 | 38 | 11 | 42 |

Reading: **opus-5.5-think**: the reliability statement does the work (A3 held and negative, A1 held); **qwen3.5:27b-think-bf16-t1**: the reliability statement does the work (A3 held and negative, A1 held); **gpt-6.1-sol-think**: attribution alone discounts (A2 held, A3 no shift)

### Family B, the posterior rule spelled out (studentized interaction test on c, Holm over the critics)

| critic | ρ, bayes | ρ, br | difference | Holm p | B1 raises use | B2 near ideal | stated P shift, bayes / br (log-odds) | verdict follows own posterior rule |
|---|---|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.10 [0.05, 0.17] | 0.07 [0.03, 0.14] | +0.02 [-0.05, 0.10] | 1.0000 (descriptive) | no | no | -0.09 / 0.19 | 100% / 100% |
| gpt-6-luna-think | 0.04 [-0.04, 0.15] | 0.04 [-0.06, 0.18] | -0.01 [-0.14, 0.14] | 1.0000 (descriptive) | no | no | 0.05 / 0.04 | 100% / 100% |
| gpt-6.1-sol-think | 0.11 [0.00, 0.34] | 0.11 [0.00, 0.35] | -0.00 [-0.06, 0.05] | 1.0000 (descriptive) | no | no | 0.16 / 0.13 | 100% / 100% |
| haiku-5.5-think | -0.08 [-0.27, 0.17] | 0.06 [-0.10, 0.19] | -0.14 [-0.34, 0.15] | 1.0000 (descriptive) | no | no | 0.04 / 0.18 | 100% / 100% |
| opus-5.5-think | 0.40 [0.16, 0.81] | 0.56 [0.29, 1.01] | -0.16 [-0.44, 0.04] | 1.0000 (descriptive) | no | no | 0.53 / 0.55 | 100% / 100% |
| qwen3.5:4b-nothink-bf16-t1 | 0.12 [0.07, 0.19] | 0.15 [0.11, 0.22] | -0.04 [-0.11, 0.04] | 1.0000 | no | no | 0.93 / 1.10 | 100% / 100% |
| qwen3.5:9b-nothink-bf16-t1 | 0.10 [0.07, 0.15] | 0.10 [0.06, 0.17] | +0.00 [-0.06, 0.05] | 1.0000 | no | no | 0.55 / 0.58 | 100% / 100% |
| qwen3.5:27b-nothink-bf16-t1 | 0.16 [0.10, 0.23] | 0.10 [0.06, 0.15] | +0.06 [-0.00, 0.12] | 0.4941 | no | no | 0.58 / 0.35 | 100% / 100% |
| qwen3.5:27b-think-bf16-t1 | 0.63 [0.49, 0.83] | 0.55 [0.41, 0.77] | +0.08 [-0.07, 0.22] | 1.0000 | no | no | 1.00 / 1.06 | 100% / 100% |

### Family C, the rate shown in examples (studentized interaction test on c, Holm over the critics)

| critic | ρ, exp (d′ at exp50) | ρ, br | difference | Holm p | C1 raises use | C2 near ideal | d′(exp50) − d′(neutral) | c(exp50) − c(neutral) | C3 |
|---|---|---|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.04 [-0.04, 0.13] | 0.07 [0.03, 0.14] | -0.04 [-0.13, 0.06] | 1.0000 (descriptive) | no | no | -0.15 [-0.45, 0.12] | -0.08 [-0.22, 0.07] | no |
| gpt-6-luna-think | 0.03 [-0.06, 0.13] | 0.04 [-0.06, 0.18] | -0.02 [-0.15, 0.12] | 1.0000 (descriptive) | no | no | +0.08 [-0.24, 0.50] | -0.04 [-0.24, 0.13] | no |
| gpt-6.1-sol-think | 0.06 [0.00, 0.14] | 0.11 [0.00, 0.35] | -0.06 [-0.29, 0.07] | 1.0000 (descriptive) | no | no | +0.10 [0.00, 0.26] | +0.05 [0.00, 0.13] | no |
| haiku-5.5-think | 0.02 [-0.25, 0.27] | 0.06 [-0.10, 0.19] | -0.04 [-0.35, 0.29] | 1.0000 (descriptive) | no | no | +0.27 [-0.22, 0.71] | +0.45 [0.26, 0.72] | no |
| opus-5.5-think | 0.05 [-0.21, 0.32] | 0.56 [0.29, 1.01] | -0.51 [-1.05, -0.21] | 1.0000 (descriptive) | no | no | -0.25 [-0.82, 0.33] | +0.06 [-0.20, 0.36] | no |
| qwen3.5:4b-nothink-bf16-t1 | 0.10 [0.05, 0.15] | 0.15 [0.11, 0.22] | -0.06 [-0.13, 0.00] | 1.0000 | no | no | -0.30 [-0.61, 0.02] | -0.29 [-0.45, -0.14] | no |
| qwen3.5:9b-nothink-bf16-t1 | 0.05 [0.00, 0.11] | 0.10 [0.06, 0.17] | -0.05 [-0.13, 0.02] | 1.0000 | no | no | -0.22 [-0.56, 0.11] | -0.21 [-0.37, -0.04] | no |
| qwen3.5:27b-nothink-bf16-t1 | 0.08 [0.02, 0.16] | 0.10 [0.06, 0.15] | -0.01 [-0.10, 0.06] | 1.0000 | no | no | -0.50 [-0.88, -0.18] | -0.27 [-0.45, -0.09] | no |
| qwen3.5:27b-think-bf16-t1 | 0.52 [0.32, 0.70] | 0.55 [0.41, 0.77] | -0.03 [-0.33, 0.18] | 1.0000 | no | no | -0.04 [-0.36, 0.28] | -0.15 [-0.33, -0.00] | no |

### Family D, the paper (Opus only, exploratory)

| rule | contrast | ρ, first | ρ, second | difference | Holm p | outcome |
|---|---|---|---|---|---|---|
| D1 | self − br | 0.14 [0.03, 0.36] | 0.56 [0.29, 1.01] | -0.42 [-0.83, -0.16] | 1.0000 (descriptive) | not shown |
| D2 | self − other | 0.14 [0.03, 0.36] | 0.30 [0.05, 0.66] | -0.16 [-0.51, 0.14] | 1.0000 (descriptive) | not shown |
| D3 | self − methods | 0.14 [0.03, 0.36] | 0.28 [0.08, 0.67] | -0.14 [-0.50, 0.12] | 1.0000 (descriptive) | not shown |
| D4 | true − self | 0.26 [0.03, 0.63] | 0.14 [0.03, 0.36] | +0.12 [-0.22, 0.50] | 1.0000 (descriptive) | not shown |

D5, overshoot: ρ_self 0.14 [0.03, 0.36]; no overshoot.

## Pipeline rules (original labels)

- **Unparsed:** qwen3.5:9b-nothink-bf16-t1, exp10: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.15; correct: -0.06.
- **Unparsed:** qwen3.5:9b-nothink-bf16-t1, exp90: 3.7% (over 2%). Shift from neutral with those trials counted as error: -0.28; correct: -0.10.
- **Unparsed:** qwen3.5:27b-think-bf16-t1, presuppose: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.47; correct: -0.28.
- **Unparsed:** qwen3.5:27b-think-bf16-t1, claim_mistake: 3.7% (over 2%). Shift from neutral with those trials counted as error: -0.62; correct: -0.38.

