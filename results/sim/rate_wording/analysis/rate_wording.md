# Rate wording run: results

Plan: `prereg/rate_wording.md`. 48400 rows, 5 critic runs, 2000 resamples. ρ is [c(10%) − c(90%)] × d′(neutral) / ln 81. Intervals are 95%, from an item bootstrap.

## Labels and ceiling

Errors per 200 at `neutral`. At 4 or fewer, ρ is reported but not interpreted under that labelling (marked \*).

| critic | original | contested left out | contested flipped |
|---|---|---|---|
| gpt-6.1-sol-think | 51.0 | 52.7 | 61.2 |
| opus-5.5-think | 53.8 | 55.7 | 64.0 |
| sim-nothink-a | 58.8 | 60.6 | 67.7 |
| sim-plain | 54.0 | 54.9 | 62.2 |
| sim-think-a | 49.9 | 50.7 | 58.4 |

## W1, under-use in every wording

Holds when the interval for ρ lies below 1 in every arm the critic has.

| critic | original | contested left out | contested flipped | all below 0.5 (original labels) |
|---|---|---|---|---|
| gpt-6.1-sol-think | fails in user (largest upper limit 1.03, user) | fails in user (largest upper limit 1.03, user) | holds (largest upper limit 0.91, user) | no |
| opus-5.5-think | holds (largest upper limit 0.72, freq) | holds (largest upper limit 0.76, freq) | holds (largest upper limit 0.62, freq) | no |
| sim-nothink-a | holds (largest upper limit 0.53, br) | holds (largest upper limit 0.54, br) | holds (largest upper limit 0.46, br) | no |
| sim-plain | holds (largest upper limit 0.64, comp) | holds (largest upper limit 0.64, comp) | holds (largest upper limit 0.56, comp) | no |
| sim-think-a | holds (largest upper limit 0.99, item) | holds (largest upper limit 0.99, item) | holds (largest upper limit 0.84, item) | no |

### ρ by arm, original (100 flawed, 100 correct)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gpt-6.1-sol-think | 0.49 [0.34, 0.71] | 0.59 [0.43, 0.83] | 0.55 [0.39, 0.78] | 0.47 [0.33, 0.66] | 0.75 [0.54, 1.03] | 0.42 [0.28, 0.60] |
| opus-5.5-think | 0.46 [0.31, 0.67] | 0.50 [0.34, 0.72] | -0.20 [-0.31, -0.12] | 0.39 [0.25, 0.57] | 0.45 [0.31, 0.65] | 0.45 [0.31, 0.64] |
| sim-nothink-a | 0.42 [0.33, 0.53] | 0.41 [0.31, 0.51] | 0.41 [0.32, 0.51] | 0.38 [0.30, 0.48] | 0.39 [0.31, 0.50] | 0.39 [0.31, 0.49] |
| sim-plain | 0.44 [0.36, 0.55] | 0.43 [0.34, 0.54] | 0.51 [0.40, 0.64] | 0.46 [0.37, 0.57] | 0.48 [0.38, 0.60] | 0.49 [0.40, 0.60] |
| sim-think-a | 0.49 [0.40, 0.61] | 0.54 [0.43, 0.67] | 0.50 [0.40, 0.62] | 0.49 [0.40, 0.60] | 0.51 [0.41, 0.64] | 0.80 [0.65, 0.99] |

### ρ by arm, contested left out (100 flawed, 86 correct)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gpt-6.1-sol-think | 0.53 [0.36, 0.74] | 0.57 [0.40, 0.81] | 0.54 [0.37, 0.76] | 0.46 [0.31, 0.67] | 0.74 [0.52, 1.03] | 0.45 [0.30, 0.64] |
| opus-5.5-think | 0.46 [0.30, 0.70] | 0.51 [0.34, 0.76] | -0.19 [-0.31, -0.11] | 0.36 [0.24, 0.56] | 0.44 [0.30, 0.66] | 0.43 [0.29, 0.63] |
| sim-nothink-a | 0.43 [0.33, 0.54] | 0.40 [0.31, 0.52] | 0.40 [0.31, 0.50] | 0.39 [0.30, 0.50] | 0.39 [0.30, 0.50] | 0.40 [0.32, 0.50] |
| sim-plain | 0.45 [0.35, 0.56] | 0.44 [0.35, 0.55] | 0.51 [0.41, 0.64] | 0.47 [0.38, 0.58] | 0.48 [0.39, 0.60] | 0.50 [0.41, 0.61] |
| sim-think-a | 0.50 [0.40, 0.62] | 0.56 [0.45, 0.70] | 0.50 [0.39, 0.62] | 0.49 [0.40, 0.61] | 0.54 [0.43, 0.67] | 0.80 [0.65, 0.99] |

### ρ by arm, contested flipped (114 flawed, 86 correct)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gpt-6.1-sol-think | 0.43 [0.30, 0.63] | 0.50 [0.35, 0.72] | 0.47 [0.32, 0.69] | 0.38 [0.25, 0.57] | 0.63 [0.44, 0.91] | 0.37 [0.24, 0.55] |
| opus-5.5-think | 0.38 [0.23, 0.59] | 0.41 [0.26, 0.62] | -0.16 [-0.26, -0.09] | 0.31 [0.19, 0.48] | 0.37 [0.24, 0.57] | 0.37 [0.23, 0.54] |
| sim-nothink-a | 0.35 [0.27, 0.46] | 0.33 [0.25, 0.43] | 0.33 [0.25, 0.43] | 0.31 [0.23, 0.42] | 0.33 [0.25, 0.43] | 0.33 [0.25, 0.42] |
| sim-plain | 0.39 [0.30, 0.49] | 0.38 [0.30, 0.48] | 0.44 [0.34, 0.56] | 0.41 [0.32, 0.51] | 0.42 [0.34, 0.53] | 0.44 [0.36, 0.53] |
| sim-think-a | 0.43 [0.33, 0.54] | 0.47 [0.37, 0.60] | 0.43 [0.33, 0.54] | 0.42 [0.33, 0.53] | 0.45 [0.35, 0.57] | 0.68 [0.53, 0.84] |

## W2, a wording changes use

ρ(arm) − ρ(`br`), paired, Holm across all tests of a labelling. "No difference" needs the whole interval within ±0.15.

### original: 25 tests; 3 differ, 16 no difference, 6 inconclusive

| critic | freq | comp | hist | user | item |
|---|---|---|---|---|---|
| gpt-6.1-sol-think | +0.10 [-0.04, 0.27], inconclusive | +0.06 [-0.08, 0.21], inconclusive | -0.03 [-0.16, 0.10], inconclusive | +0.26 [0.10, 0.46], differs (Holm p 0.034) | -0.07 [-0.20, 0.05], inconclusive |
| opus-5.5-think | +0.04 [-0.10, 0.18], inconclusive | -0.66 [-0.94, -0.45], differs (Holm p 0.012) | -0.07 [-0.23, 0.05], inconclusive | -0.01 [-0.14, 0.13], no difference | -0.01 [-0.14, 0.11], no difference |
| sim-nothink-a | -0.02 [-0.09, 0.05], no difference | -0.01 [-0.09, 0.05], no difference | -0.04 [-0.11, 0.03], no difference | -0.03 [-0.10, 0.04], no difference | -0.03 [-0.11, 0.04], no difference |
| sim-plain | -0.01 [-0.08, 0.05], no difference | +0.06 [-0.02, 0.14], no difference | +0.01 [-0.07, 0.10], no difference | +0.03 [-0.05, 0.11], no difference | +0.05 [-0.03, 0.13], no difference |
| sim-think-a | +0.04 [-0.03, 0.12], no difference | +0.01 [-0.07, 0.08], no difference | -0.00 [-0.09, 0.07], no difference | +0.01 [-0.06, 0.09], no difference | +0.30 [0.21, 0.43], differs (Holm p 0.012) |

### contested left out: 25 tests; 2 differ, 14 no difference, 9 inconclusive

| critic | freq | comp | hist | user | item |
|---|---|---|---|---|---|
| gpt-6.1-sol-think | +0.05 [-0.12, 0.20], inconclusive | +0.01 [-0.14, 0.16], inconclusive | -0.07 [-0.21, 0.06], inconclusive | +0.21 [0.05, 0.42], inconclusive | -0.08 [-0.23, 0.05], inconclusive |
| opus-5.5-think | +0.04 [-0.10, 0.18], inconclusive | -0.65 [-0.97, -0.44], differs (Holm p 0.012) | -0.10 [-0.25, 0.02], inconclusive | -0.02 [-0.17, 0.11], inconclusive | -0.03 [-0.18, 0.09], inconclusive |
| sim-nothink-a | -0.02 [-0.09, 0.04], no difference | -0.03 [-0.10, 0.04], no difference | -0.04 [-0.12, 0.04], no difference | -0.04 [-0.11, 0.03], no difference | -0.03 [-0.10, 0.05], no difference |
| sim-plain | -0.01 [-0.08, 0.06], no difference | +0.06 [-0.02, 0.15], no difference | +0.02 [-0.07, 0.11], no difference | +0.03 [-0.05, 0.11], no difference | +0.05 [-0.03, 0.13], no difference |
| sim-think-a | +0.06 [-0.03, 0.15], no difference | -0.00 [-0.08, 0.07], no difference | -0.01 [-0.09, 0.07], no difference | +0.04 [-0.04, 0.11], no difference | +0.30 [0.20, 0.42], differs (Holm p 0.012) |

### contested flipped: 25 tests; 2 differ, 17 no difference, 6 inconclusive

| critic | freq | comp | hist | user | item |
|---|---|---|---|---|---|
| gpt-6.1-sol-think | +0.07 [-0.07, 0.21], inconclusive | +0.03 [-0.10, 0.17], inconclusive | -0.05 [-0.17, 0.06], inconclusive | +0.20 [0.06, 0.37], inconclusive | -0.06 [-0.19, 0.05], inconclusive |
| opus-5.5-think | +0.03 [-0.08, 0.15], no difference | -0.54 [-0.81, -0.34], differs (Holm p 0.012) | -0.07 [-0.21, 0.04], inconclusive | -0.00 [-0.13, 0.11], no difference | -0.01 [-0.14, 0.09], no difference |
| sim-nothink-a | -0.02 [-0.08, 0.04], no difference | -0.02 [-0.08, 0.04], no difference | -0.04 [-0.11, 0.02], no difference | -0.03 [-0.09, 0.03], no difference | -0.03 [-0.10, 0.03], no difference |
| sim-plain | -0.01 [-0.07, 0.05], no difference | +0.05 [-0.02, 0.12], no difference | +0.02 [-0.06, 0.09], no difference | +0.03 [-0.04, 0.11], no difference | +0.05 [-0.02, 0.12], no difference |
| sim-think-a | +0.04 [-0.02, 0.12], no difference | -0.00 [-0.07, 0.06], no difference | -0.01 [-0.07, 0.06], no difference | +0.02 [-0.04, 0.08], no difference | +0.25 [0.16, 0.35], differs (Holm p 0.012) |

## W3, information or number

Under `comp`, c(told 10% have errors) − c(told 90% have errors). Above 0: follows the information. Below 0: the number or the word.

| critic | original | contested left out | contested flipped |
|---|---|---|---|
| gpt-6.1-sol-think | +1.78 [1.47, 2.17], information | +1.74 [1.45, 2.12], information | +1.71 [1.42, 2.09], information |
| opus-5.5-think | -0.69 [-0.99, -0.46], number | -0.69 [-1.00, -0.45], number | -0.67 [-0.95, -0.43], number |
| sim-nothink-a | +1.59 [1.45, 1.76], information | +1.58 [1.43, 1.75], information | +1.49 [1.34, 1.65], information |
| sim-plain | +1.76 [1.57, 2.00], information | +1.73 [1.54, 1.98], information | +1.66 [1.47, 1.90], information |
| sim-think-a | +1.60 [1.44, 1.78], information | +1.58 [1.41, 1.78], information | +1.52 [1.36, 1.72], information |

## W4, Opus on new items

- **original:** ρ for `br` 0.46 [0.31, 0.67]; holds; outside the Stage C interval [0.05, 0.44].
- **contested left out:** ρ for `br` 0.46 [0.30, 0.70]; holds; outside the Stage C interval [0.05, 0.44].
- **contested flipped:** ρ for `br` 0.38 [0.23, 0.59]; holds; inside the Stage C interval [0.05, 0.44].

## W5, the claim tests on GPT-6.1 Sol

| test | contrast | original | contested left out | contested flipped |
|---|---|---|---|---|
| T1 | `presuppose` − `neutral` | -0.94 [-1.25, -0.68], held | -0.94 [-1.26, -0.68], held | -0.83 [-1.11, -0.59], held |
| T2 | `claim_bare` − `neutral` | -1.02 [-1.33, -0.77], held | -0.98 [-1.30, -0.72], held | -0.96 [-1.22, -0.70], held |
| T3 | `claim_mistake` − `neutral` | -0.88 [-1.18, -0.63], held | -0.87 [-1.18, -0.60], held | -0.83 [-1.10, -0.57], held |
| T4 | `claim_reviewer` − `neutral` | -0.30 [-0.55, -0.07], held | -0.28 [-0.54, -0.02], not shown | -0.27 [-0.51, -0.02], not shown |
| T5 | `presuppose` − `check_only` | -1.07 [-1.38, -0.82], held | -1.03 [-1.35, -0.77], held | -0.93 [-1.21, -0.69], held |
| T6 | `presuppose` − `may_error` | -0.82 [-1.10, -0.57], held | -0.83 [-1.13, -0.57], held | -0.70 [-0.96, -0.47], held |
| T7 | `claim_random` − `neutral` | -0.07 [-0.33, 0.21], inconclusive | -0.07 [-0.36, 0.20], inconclusive | -0.07 [-0.33, 0.19], inconclusive |
| T8 | `claim_random` − `claim_bare` | +0.95 [0.69, 1.28], held | +0.91 [0.63, 1.23], held | +0.89 [0.63, 1.17], held |
| T9 | `claim_correct` − `neutral` | +0.35 [0.07, 0.65], held | +0.31 [0.02, 0.60], not shown | +0.30 [0.05, 0.59], not shown |

## Secondary measures

Planned, uncorrected, not primary. The first three use no label.

### Flag-rate shift: share of all solutions flagged when told 90%, minus when told 10% (points)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gpt-6.1-sol-think | +50.0 [42.3, 57.2] | +52.4 [45.3, 59.7] | +48.7 [41.4, 56.1] | +45.7 [37.9, 53.1] | +68.9 [62.2, 75.7] | +40.9 [32.8, 49.5] |
| opus-5.5-think | +48.4 [40.6, 55.9] | +52.1 [43.9, 59.7] | -21.4 [-28.6, -14.0] | +41.8 [33.5, 50.5] | +49.2 [41.8, 56.6] | +49.5 [41.7, 56.9] |
| sim-nothink-a | +48.1 [43.4, 52.6] | +46.8 [42.2, 51.2] | +47.5 [42.9, 51.8] | +45.5 [40.8, 50.2] | +47.9 [43.0, 52.9] | +45.3 [40.4, 50.3] |
| sim-plain | +45.9 [41.3, 50.6] | +47.5 [42.8, 52.2] | +50.3 [45.5, 54.8] | +47.2 [42.7, 51.8] | +48.9 [44.3, 53.5] | +50.8 [46.2, 54.9] |
| sim-think-a | +50.2 [45.8, 55.5] | +51.8 [47.3, 56.3] | +49.1 [44.6, 54.1] | +47.3 [42.5, 52.2] | +47.7 [43.1, 52.3] | +70.7 [66.7, 74.5] |

### Own-confidence benchmark: verdict changes made, of those the critic's stated P(error) at `br50` predicts (sample 0)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gpt-6.1-sol-think | 85 of 128 (+34 unpredicted, 22 wrong way) | 93 of 126 (+33 unpredicted, 26 wrong way) | 84 of 127 (+35 unpredicted, 24 wrong way) | 92 of 131 (+28 unpredicted, 31 wrong way) | 105 of 126 (+42 unpredicted, 16 wrong way) | 80 of 126 (+34 unpredicted, 35 wrong way) |
| opus-5.5-think | 75 of 114 (+34 unpredicted, 22 wrong way) | 79 of 116 (+38 unpredicted, 20 wrong way) | 31 of 119 (+13 unpredicted, 85 wrong way) | 77 of 115 (+30 unpredicted, 29 wrong way) | 80 of 120 (+38 unpredicted, 23 wrong way) | 86 of 119 (+30 unpredicted, 22 wrong way) |
| sim-nothink-a | 71 of 123 (+33 unpredicted, 21 wrong way) | 81 of 125 (+27 unpredicted, 24 wrong way) | 88 of 126 (+29 unpredicted, 22 wrong way) | 79 of 125 (+31 unpredicted, 23 wrong way) | 86 of 126 (+32 unpredicted, 24 wrong way) | 77 of 126 (+35 unpredicted, 26 wrong way) |
| sim-plain | 81 of 125 (+28 unpredicted, 21 wrong way) | 80 of 126 (+32 unpredicted, 19 wrong way) | 85 of 124 (+30 unpredicted, 20 wrong way) | 77 of 127 (+26 unpredicted, 19 wrong way) | 83 of 127 (+29 unpredicted, 19 wrong way) | 78 of 124 (+28 unpredicted, 23 wrong way) |
| sim-think-a | 86 of 125 (+33 unpredicted, 24 wrong way) | 89 of 122 (+35 unpredicted, 23 wrong way) | 71 of 128 (+34 unpredicted, 20 wrong way) | 79 of 124 (+36 unpredicted, 24 wrong way) | 88 of 128 (+31 unpredicted, 22 wrong way) | 111 of 130 (+48 unpredicted, 5 wrong way) |

### Stated P(error) shift in log-odds, 90% minus 10% (a calibrated Bayesian: 4.39 before clipping at 1 and 99)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gpt-6.1-sol-think | +2.80 [2.49, 3.11] | +3.16 [2.85, 3.48] | +3.24 [2.91, 3.56] | +2.92 [2.60, 3.26] | +4.20 [3.89, 4.49] | +2.64 [2.31, 2.95] |
| opus-5.5-think | +2.93 [2.60, 3.27] | +3.10 [2.78, 3.41] | -1.16 [-1.49, -0.85] | +2.84 [2.53, 3.15] | +2.81 [2.49, 3.13] | +2.93 [2.59, 3.27] |
| sim-nothink-a | +2.77 [2.60, 2.95] | +2.93 [2.76, 3.11] | +3.03 [2.85, 3.21] | +2.77 [2.57, 2.97] | +2.85 [2.66, 3.04] | +2.78 [2.61, 2.96] |
| sim-plain | +2.77 [2.58, 2.94] | +2.94 [2.76, 3.13] | +3.09 [2.92, 3.25] | +2.93 [2.76, 3.09] | +2.89 [2.72, 3.07] | +3.11 [2.93, 3.28] |
| sim-think-a | +2.97 [2.81, 3.15] | +2.96 [2.79, 3.12] | +2.89 [2.70, 3.09] | +2.97 [2.76, 3.15] | +2.91 [2.74, 3.10] | +4.49 [4.29, 4.69] |

### Verdicts that flip between the 10% and the 90% version (sample 0): toward "error" at 90% / toward "correct" at 90%

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gpt-6.1-sol-think | 103 / 5 of 196 | 100 / 1 of 189 | 99 / 4 of 195 | 94 / 4 of 197 | 133 / 2 of 190 | 87 / 8 of 193 |
| opus-5.5-think | 91 / 2 of 184 | 103 / 4 of 190 | 11 / 52 of 192 | 89 / 10 of 189 | 99 / 2 of 197 | 98 / 4 of 190 |
| sim-nothink-a | 89 / 4 of 188 | 89 / 3 of 191 | 99 / 3 of 191 | 95 / 7 of 193 | 100 / 5 of 193 | 90 / 3 of 195 |
| sim-plain | 93 / 4 of 191 | 96 / 1 of 192 | 100 / 4 of 193 | 93 / 6 of 194 | 100 / 3 of 190 | 86 / 2 of 185 |
| sim-think-a | 99 / 3 of 190 | 105 / 3 of 188 | 90 / 5 of 193 | 99 / 7 of 191 | 99 / 1 of 193 | 154 / 0 of 196 |

### A rate against a claim: shift from `neutral` toward flagging, original labels

| critic | told 90% of the batch | told 90% for this solution | "This solution contains an error." |
|---|---|---|---|
| gpt-6.1-sol-think | +0.87 [0.62, 1.16] | +0.68 [0.43, 0.95] | +1.02 [0.77, 1.33] |
| opus-5.5-think | +0.71 [0.46, 0.99] | +0.75 [0.50, 1.03] | +0.99 [0.69, 1.33] |
| sim-nothink-a | +0.84 [0.70, 0.99] | +0.76 [0.61, 0.92] | +0.83 [0.68, 0.98] |
| sim-plain | +0.68 [0.54, 0.83] | +0.79 [0.65, 0.93] | +0.82 [0.66, 0.98] |
| sim-think-a | +0.75 [0.60, 0.89] | +1.25 [1.08, 1.44] | +0.87 [0.72, 1.04] |

### What under-use costs if the stated rate were true: accuracy (%) for `br`, original labels

Critic's verdicts under that line / its neutral verdicts / ideal observer with its d′.

| critic | true rate 10% | true rate 90% |
|---|---|---|
| gpt-6.1-sol-think | 88.5 / 82.8 / 90.8 | 83.2 / 66.0 / 90.8 |
| opus-5.5-think | 90.1 / 79.4 / 90.5 | 85.0 / 66.6 / 90.5 |
| sim-nothink-a | 91.0 / 79.1 / 90.3 | 85.3 / 62.1 / 90.3 |
| sim-plain | 90.4 / 80.5 / 90.5 | 82.3 / 65.6 / 90.5 |
| sim-think-a | 87.8 / 81.1 / 90.8 | 83.7 / 69.0 / 90.8 |

### Thinking on − off in ρ, paired, original labels

| critic (thinking on) | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| sim-think-a | +0.07 [-0.07, 0.22] | +0.13 [-0.00, 0.28] | +0.09 [-0.05, 0.24] | +0.11 [-0.03, 0.25] | +0.11 [-0.03, 0.25] | +0.41 [0.24, 0.60] |

## Pipeline rules (original labels)

- **Unparsed:** gpt-6.1-sol-think, neutral: 2.0% (over 2%). c with those trials counted as error: +0.30; correct: +0.36.
- **Unparsed:** gpt-6.1-sol-think, check_only: 2.5% (over 2%). Shift from neutral with those trials counted as error: +0.10; correct: +0.17.
- **Unparsed:** gpt-6.1-sol-think, may_error: 3.0% (over 2%). Shift from neutral with those trials counted as error: -0.17; correct: -0.08.
- **Unparsed:** gpt-6.1-sol-think, claim_random: 2.5% (over 2%). Shift from neutral with those trials counted as error: -0.12; correct: -0.04.
- **Unparsed:** gpt-6.1-sol-think, item_p10: 2.5% (over 2%). Shift from neutral with those trials counted as error: +0.57; correct: +0.70.
- **Unparsed:** gpt-6.1-sol-think, freq10: 2.5% (over 2%). Shift from neutral with those trials counted as error: +0.63; correct: +0.96.
- **Unparsed:** gpt-6.1-sol-think, freq90: 3.0% (over 2%). Shift from neutral with those trials counted as error: -0.99; correct: -0.88.
- **Unparsed:** gpt-6.1-sol-think, user10: 3.0% (over 2%). Shift from neutral with those trials counted as error: +0.90; correct: +1.23.
- **Unparsed:** gpt-6.1-sol-think, user90: 2.0% (over 2%). Shift from neutral with those trials counted as error: -1.22; correct: -1.15.
- **Unparsed:** opus-5.5-think, br10: 6.0% (over 5%, flagged). Shift from neutral with those trials counted as error: +0.62; correct: +0.95.
- **Unparsed:** opus-5.5-think, br90: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.73; correct: -0.67.
- **Unparsed:** opus-5.5-think, claim_bare: 2.0% (over 2%). Shift from neutral with those trials counted as error: -1.00; correct: -0.91.
- **Unparsed:** opus-5.5-think, claim_reviewer: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.40; correct: -0.34.
- **Unparsed:** opus-5.5-think, may_error: 2.0% (over 2%). Shift from neutral with those trials counted as error: +0.13; correct: +0.20.
- **Unparsed:** opus-5.5-think, claim_correct: 4.0% (over 2%). Shift from neutral with those trials counted as error: +0.34; correct: +0.57.
- **Unparsed:** opus-5.5-think, item_p10: 2.0% (over 2%). Shift from neutral with those trials counted as error: +0.76; correct: +0.85.
- **Unparsed:** opus-5.5-think, item_p90: 3.0% (over 2%). Shift from neutral with those trials counted as error: -0.78; correct: -0.69.
- **Unparsed:** opus-5.5-think, freq10: 2.5% (over 2%). Shift from neutral with those trials counted as error: +0.73; correct: +0.91.
- **Unparsed:** opus-5.5-think, freq90: 2.5% (over 2%). Shift from neutral with those trials counted as error: -0.89; correct: -0.78.
- **Unparsed:** opus-5.5-think, comp90: 3.0% (over 2%). Shift from neutral with those trials counted as error: +0.31; correct: +0.43.
- **Unparsed:** opus-5.5-think, hist10: 4.0% (over 2%). Shift from neutral with those trials counted as error: +0.50; correct: +0.67.
- **Unparsed:** opus-5.5-think, hist90: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.74; correct: -0.66.
- **Unparsed:** sim-nothink-a, neutral: 2.0% (over 2%). c with those trials counted as error: +0.27; correct: +0.33.
- **Unparsed:** sim-nothink-a, br10: 2.3% (over 2%). Shift from neutral with those trials counted as error: +0.64; correct: +0.82.
- **Unparsed:** sim-nothink-a, br90: 2.8% (over 2%). Shift from neutral with those trials counted as error: -0.87; correct: -0.76.
- **Unparsed:** sim-nothink-a, claim_mistake: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.91; correct: -0.83.
- **Unparsed:** sim-nothink-a, claim_reviewer: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.51; correct: -0.45.
- **Unparsed:** sim-nothink-a, check_only: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.02; correct: +0.05.
- **Unparsed:** sim-nothink-a, item_p90: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.78; correct: -0.69.
- **Unparsed:** sim-nothink-a, freq10: 2.2% (over 2%). Shift from neutral with those trials counted as error: +0.62; correct: +0.76.
- **Unparsed:** sim-nothink-a, freq90: 2.3% (over 2%). Shift from neutral with those trials counted as error: -0.86; correct: -0.77.
- **Unparsed:** sim-nothink-a, comp10: 2.2% (over 2%). Shift from neutral with those trials counted as error: +0.64; correct: +0.78.
- **Unparsed:** sim-nothink-a, comp90: 2.3% (over 2%). Shift from neutral with those trials counted as error: -0.85; correct: -0.76.
- **Unparsed:** sim-nothink-a, hist90: 2.3% (over 2%). Shift from neutral with those trials counted as error: -0.82; correct: -0.74.
- **Unparsed:** sim-nothink-a, user90: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.82; correct: -0.75.
- **Unparsed:** sim-plain, neutral: 2.5% (over 2%). c with those trials counted as error: +0.23; correct: +0.31.
- **Unparsed:** sim-plain, br50: 2.3% (over 2%). Shift from neutral with those trials counted as error: +0.02; correct: +0.09.
- **Unparsed:** sim-plain, br90: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.70; correct: -0.63.
- **Unparsed:** sim-plain, presuppose: 2.8% (over 2%). Shift from neutral with those trials counted as error: -0.83; correct: -0.73.
- **Unparsed:** sim-plain, claim_bare: 4.5% (over 2%). Shift from neutral with those trials counted as error: -0.86; correct: -0.72.
- **Unparsed:** sim-plain, claim_mistake: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.77; correct: -0.71.
- **Unparsed:** sim-plain, check_only: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.01; correct: +0.06.
- **Unparsed:** sim-plain, may_error: 2.5% (over 2%). Shift from neutral with those trials counted as error: +0.09; correct: +0.18.
- **Unparsed:** sim-plain, claim_random: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.10; correct: -0.04.
- **Unparsed:** sim-plain, claim_correct: 2.3% (over 2%). Shift from neutral with those trials counted as error: +0.29; correct: +0.38.
- **Unparsed:** sim-plain, item_p10: 2.2% (over 2%). Shift from neutral with those trials counted as error: +0.83; correct: +0.94.
- **Unparsed:** sim-plain, item_p90: 2.3% (over 2%). Shift from neutral with those trials counted as error: -0.81; correct: -0.72.
- **Unparsed:** sim-plain, freq90: 3.5% (over 2%). Shift from neutral with those trials counted as error: -0.84; correct: -0.71.
- **Unparsed:** sim-plain, comp10: 2.0% (over 2%). Shift from neutral with those trials counted as error: +0.81; correct: +0.98.
- **Unparsed:** sim-plain, comp90: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.81; correct: -0.74.
- **Unparsed:** sim-plain, hist10: 2.7% (over 2%). Shift from neutral with those trials counted as error: +0.73; correct: +0.86.
- **Unparsed:** sim-plain, user10: 2.5% (over 2%). Shift from neutral with those trials counted as error: +0.65; correct: +0.83.
- **Unparsed:** sim-plain, user90: 2.3% (over 2%). Shift from neutral with those trials counted as error: -0.86; correct: -0.78.
- **Unparsed:** sim-think-a, br10: 2.7% (over 2%). Shift from neutral with those trials counted as error: +0.71; correct: +0.85.
- **Unparsed:** sim-think-a, br50: 2.7% (over 2%). Shift from neutral with those trials counted as error: +0.07; correct: +0.16.
- **Unparsed:** sim-think-a, br90: 2.8% (over 2%). Shift from neutral with those trials counted as error: -0.78; correct: -0.68.
- **Unparsed:** sim-think-a, claim_bare: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.89; correct: -0.81.
- **Unparsed:** sim-think-a, claim_mistake: 2.3% (over 2%). Shift from neutral with those trials counted as error: -0.87; correct: -0.79.
- **Unparsed:** sim-think-a, freq10: 2.7% (over 2%). Shift from neutral with those trials counted as error: +0.81; correct: +0.95.
- **Unparsed:** sim-think-a, comp10: 2.0% (over 2%). Shift from neutral with those trials counted as error: +0.73; correct: +0.85.
- **Unparsed:** sim-think-a, comp90: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.78; correct: -0.71.
- **Unparsed:** sim-think-a, hist90: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.77; correct: -0.70.
- **Unparsed:** sim-think-a, user90: 2.2% (over 2%). Shift from neutral with those trials counted as error: -0.80; correct: -0.72.

