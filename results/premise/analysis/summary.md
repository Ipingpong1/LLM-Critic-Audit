### gemma4:12b-nothink-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 300 / 300 | 0 | 0.94 | 0.16 | 2.54 [2.16, 3.09] | -0.28 [-0.53, -0.06] | 0.00 [0.00, 0.00] | – | 0.96 [0.93, 0.98] |
| br10 | 0.10 | 300 / 299 | 1 | 0.93 | 0.16 | 2.49 [2.12, 2.97] | -0.25 [-0.51, -0.04] | 0.03 [-0.05, 0.12] | 0.86 | 0.96 [0.93, 0.98] |
| br90 | 0.90 | 300 / 299 | 1 | 0.95 | 0.18 | 2.53 [2.16, 3.11] | -0.37 [-0.64, -0.14] | -0.09 [-0.18, -0.01] | -0.86 | 0.96 [0.93, 0.98] |
| presuppose | – | 300 / 300 | 0 | 0.96 | 0.26 | 2.41 [2.02, 2.97] | -0.57 [-0.83, -0.35] | -0.29 [-0.44, -0.16] | – | 0.95 [0.92, 0.98] |
| claim_bare | – | 300 / 300 | 0 | 0.96 | 0.25 | 2.45 [2.08, 2.98] | -0.55 [-0.81, -0.35] | -0.27 [-0.42, -0.14] | – | 0.95 [0.92, 0.98] |
| claim_mistake | – | 300 / 300 | 0 | 0.97 | 0.33 | 2.31 [1.91, 3.10] | -0.70 [-1.05, -0.49] | -0.43 [-0.68, -0.27] | – | 0.95 [0.92, 0.98] |
| claim_reviewer | – | 300 / 300 | 0 | 0.96 | 0.30 | 2.26 [1.91, 2.77] | -0.60 [-0.83, -0.40] | -0.33 [-0.46, -0.20] | – | 0.95 [0.92, 0.98] |
| check_only | – | 300 / 300 | 0 | 0.95 | 0.18 | 2.52 [2.15, 3.01] | -0.34 [-0.60, -0.13] | -0.07 [-0.15, 0.01] | – | 0.95 [0.92, 0.98] |
| may_error | – | 300 / 299 | 1 | 0.94 | 0.17 | 2.50 [2.12, 3.03] | -0.30 [-0.55, -0.08] | -0.02 [-0.13, 0.09] | – | 0.96 [0.93, 0.98] |
| claim_random | – | 299 / 299 | 2 | 0.96 | 0.26 | 2.35 [1.99, 2.86] | -0.52 [-0.77, -0.33] | -0.25 [-0.36, -0.13] | – | 0.96 [0.93, 0.98] |
| claim_correct | – | 299 / 300 | 1 | 0.91 | 0.14 | 2.39 [2.04, 2.88] | -0.12 [-0.35, 0.09] | 0.16 [0.06, 0.30] | – | 0.96 [0.93, 0.98] |
| item_p10 | 0.10 | 300 / 300 | 0 | 0.94 | 0.18 | 2.47 [2.10, 3.01] | -0.31 [-0.57, -0.09] | -0.03 [-0.11, 0.04] | 0.86 | 0.96 [0.93, 0.98] |
| item_p90 | 0.90 | 300 / 300 | 0 | 0.96 | 0.22 | 2.54 [2.15, 3.14] | -0.51 [-0.79, -0.30] | -0.23 [-0.35, -0.12] | -0.86 | 0.95 [0.92, 0.98] |

- **Prior-use ratio ρ = 0.07 [0.02, 0.15]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.12 [0.04, 0.23]; ideal = ln 81 / d′(neutral) = 1.73.
- ρ for stated chance for this solution (item_p10 vs item_p90) = **0.11 [0.06, 0.21]**; minus base-rate ρ = 0.05 [-0.01, 0.12] (paired).
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 4 distinct values.
- z-ROC slope in neutral: 1.50 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 74/81; wrong answer 209/219.

### gemma4:12b-think-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 295 / 300 | 5 | 0.98 | 0.11 | 3.39 [2.97, 3.95] | -0.47 [-0.74, -0.24] | 0.00 [0.00, 0.00] | – | 0.95 [0.92, 0.98] |
| br10 | 0.10 | 295 / 300 | 5 | 0.96 | 0.10 | 3.11 [2.70, 3.77] | -0.26 [-0.56, -0.02] | 0.22 [0.07, 0.40] | 0.65 | 0.96 [0.93, 0.98] |
| br90 | 0.90 | 298 / 300 | 2 | 0.98 | 0.10 | 3.24 [2.88, 3.76] | -0.34 [-0.58, -0.13] | 0.13 [-0.02, 0.32] | -0.65 | 0.96 [0.94, 0.98] |
| presuppose | – | 294 / 298 | 8 | 0.98 | 0.13 | 3.19 [2.81, 3.73] | -0.49 [-0.74, -0.28] | -0.02 [-0.16, 0.13] | – | 0.94 [0.91, 0.96] |
| claim_bare | – | 294 / 300 | 6 | 0.98 | 0.13 | 3.16 [2.78, 3.67] | -0.44 [-0.69, -0.22] | 0.03 [-0.13, 0.25] | – | 0.94 [0.91, 0.97] |
| claim_mistake | – | 298 / 298 | 4 | 0.99 | 0.19 | 3.26 [2.93, 3.63] | -0.77 [-0.93, -0.59] | -0.29 [-0.55, -0.01] | – | 0.95 [0.92, 0.97] |
| claim_reviewer | – | 299 / 300 | 1 | 0.99 | 0.11 | 3.62 [3.26, 4.06] | -0.59 [-0.77, -0.39] | -0.11 [-0.22, 0.03] | – | 0.96 [0.93, 0.98] |
| check_only | – | 296 / 299 | 5 | 0.98 | 0.11 | 3.33 [2.88, 3.99] | -0.42 [-0.74, -0.18] | 0.05 [-0.14, 0.17] | – | 0.95 [0.92, 0.97] |
| may_error | – | 293 / 300 | 7 | 0.97 | 0.09 | 3.24 [2.86, 3.78] | -0.28 [-0.52, -0.06] | 0.19 [0.08, 0.35] | – | 0.96 [0.93, 0.98] |
| claim_random | – | 296 / 300 | 4 | 0.98 | 0.12 | 3.24 [2.82, 3.87] | -0.47 [-0.77, -0.24] | 0.01 [-0.19, 0.21] | – | 0.95 [0.92, 0.97] |
| claim_correct | – | 290 / 300 | 10 | 0.98 | 0.10 | 3.44 [2.94, 4.09] | -0.44 [-0.75, -0.17] | 0.03 [-0.17, 0.12] | – | 0.96 [0.93, 0.98] |
| item_p10 | 0.10 | 298 / 299 | 3 | 0.97 | 0.10 | 3.11 [2.71, 3.71] | -0.26 [-0.52, -0.03] | 0.21 [0.10, 0.38] | 0.65 | 0.96 [0.93, 0.98] |
| item_p90 | 0.90 | 294 / 300 | 6 | 0.99 | 0.12 | 3.45 [3.00, 4.01] | -0.54 [-0.79, -0.31] | -0.07 [-0.22, 0.04] | -0.65 | 0.97 [0.94, 0.99] |

- **Prior-use ratio ρ = 0.07 [-0.12, 0.23]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.09 [-0.15, 0.29]; ideal = ln 81 / d′(neutral) = 1.30.
- ρ for stated chance for this solution (item_p10 vs item_p90) = **0.21 [0.09, 0.39]**; minus base-rate ρ = 0.15 [-0.06, 0.44] (paired).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 10 distinct values.
- z-ROC slope in neutral: 1.14 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 77/80; wrong answer 215/215.

### haiku-5.5-think

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 300 / 300 | 0 | 1.00 | 0.18 | 3.50 [3.25, 3.79] | -0.83 [-0.96, -0.69] | 0.00 [0.00, 0.00] | – | 0.98 [0.97, 0.99] |
| presuppose | – | 300 / 300 | 0 | 1.00 | 0.17 | 3.52 [3.26, 3.82] | -0.82 [-0.95, -0.67] | 0.01 [-0.03, 0.05] | – | 0.99 [0.98, 1.00] |
| claim_bare | – | 300 / 300 | 0 | 1.00 | 0.19 | 3.46 [3.21, 3.75] | -0.85 [-0.98, -0.70] | -0.02 [-0.07, 0.03] | – | 0.99 [0.98, 1.00] |
| claim_mistake | – | 300 / 300 | 0 | 1.00 | 0.18 | 3.50 [3.23, 3.79] | -0.83 [-0.97, -0.69] | 0.00 [-0.04, 0.03] | – | 0.99 [0.98, 1.00] |
| claim_reviewer | – | 300 / 300 | 0 | 1.00 | 0.20 | 3.42 [3.18, 3.72] | -0.87 [-0.99, -0.72] | -0.04 [-0.09, -0.01] | – | 0.99 [0.98, 1.00] |
| check_only | – | 300 / 300 | 0 | 1.00 | 0.17 | 3.53 [3.27, 3.84] | -0.81 [-0.95, -0.66] | 0.02 [-0.02, 0.07] | – | 0.99 [0.98, 1.00] |
| may_error | – | 300 / 300 | 0 | 1.00 | 0.17 | 3.55 [3.28, 3.86] | -0.81 [-0.94, -0.65] | 0.03 [-0.01, 0.06] | – | 0.99 [0.97, 1.00] |
| claim_random | – | 300 / 300 | 0 | 1.00 | 0.17 | 3.52 [3.26, 3.82] | -0.82 [-0.95, -0.67] | 0.01 [-0.03, 0.07] | – | 0.99 [0.98, 1.00] |
| claim_correct | – | 300 / 300 | 0 | 0.99 | 0.13 | 3.51 [3.14, 3.92] | -0.64 [-0.84, -0.45] | 0.19 [0.06, 0.33] | – | 0.99 [0.98, 1.00] |

- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 49 distinct values.
- z-ROC slope in neutral: 1.13 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 81/81; wrong answer 219/219.

### opus-5.5-think

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 200 / 200 | 0 | 0.99 | 0.15 | 3.20 [2.70, 3.81] | -0.58 [-0.89, -0.32] | 0.00 [0.00, 0.00] | – | 0.99 [0.98, 1.00] |
| presuppose | – | 200 / 200 | 0 | 1.00 | 0.57 | 2.39 [2.16, 2.62] | -1.38 [-1.50, -1.27] | -0.81 [-1.07, -0.50] | – | 0.99 [0.97, 1.00] |
| claim_bare | – | 100 / 100 | 0 | 1.00 | 0.89 | 1.37 [1.06, 1.64] | -1.89 [-2.05, -1.76] | -1.32 [-1.62, -0.98] | – | 0.99 [0.98, 1.00] |
| claim_mistake | – | 100 / 100 | 0 | 1.00 | 0.61 | 2.30 [2.06, 2.53] | -1.43 [-1.55, -1.31] | -0.85 [-1.12, -0.54] | – | 0.98 [0.96, 1.00] |
| claim_reviewer | – | 100 / 100 | 0 | 1.00 | 0.22 | 3.34 [3.07, 3.64] | -0.91 [-1.04, -0.76] | -0.33 [-0.56, -0.06] | – | 0.99 [0.98, 1.00] |
| check_only | – | 100 / 100 | 0 | 1.00 | 0.17 | 3.52 [3.25, 3.84] | -0.82 [-0.96, -0.66] | -0.24 [-0.46, 0.01] | – | 0.99 [0.99, 1.00] |
| may_error | – | 100 / 100 | 0 | 1.00 | 0.16 | 3.56 [3.28, 3.90] | -0.80 [-0.94, -0.63] | -0.22 [-0.44, 0.04] | – | 0.99 [0.99, 1.00] |
| claim_random | – | 100 / 100 | 0 | 1.00 | 0.12 | 3.74 [3.45, 4.10] | -0.71 [-0.86, -0.53] | -0.14 [-0.35, 0.13] | – | 0.99 [0.98, 1.00] |
| claim_correct | – | 100 / 100 | 0 | 0.96 | 0.09 | 3.02 [2.58, 3.66] | -0.19 [-0.51, 0.07] | 0.38 [0.14, 0.71] | – | 0.99 [0.98, 1.00] |

- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 45 distinct values.
- z-ROC slope in neutral: 1.08 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 52/54; wrong answer 146/146.

### qwen3.5:4b-nothink-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 300 / 300 | 0 | 0.92 | 0.45 | 1.52 [1.20, 1.87] | -0.64 [-0.81, -0.49] | 0.00 [0.00, 0.00] | – | 0.90 [0.86, 0.94] |
| br10 | 0.10 | 300 / 300 | 0 | 0.89 | 0.48 | 1.25 [0.95, 1.59] | -0.58 [-0.75, -0.43] | 0.06 [-0.04, 0.16] | 1.44 | 0.90 [0.86, 0.94] |
| br90 | 0.90 | 300 / 300 | 0 | 0.95 | 0.63 | 1.30 [0.93, 1.75] | -0.99 [-1.20, -0.81] | -0.35 [-0.51, -0.21] | -1.44 | 0.90 [0.85, 0.94] |
| presuppose | – | 300 / 300 | 0 | 0.96 | 0.60 | 1.49 [1.17, 1.87] | -0.99 [-1.19, -0.83] | -0.36 [-0.53, -0.21] | – | 0.90 [0.85, 0.94] |
| claim_bare | – | 300 / 300 | 0 | 0.95 | 0.58 | 1.43 [1.11, 1.79] | -0.92 [-1.10, -0.77] | -0.28 [-0.44, -0.15] | – | 0.90 [0.85, 0.94] |
| claim_mistake | – | 298 / 299 | 3 | 0.97 | 0.66 | 1.48 [1.11, 1.95] | -1.17 [-1.40, -0.99] | -0.53 [-0.72, -0.38] | – | 0.89 [0.84, 0.93] |
| claim_reviewer | – | 300 / 299 | 1 | 0.95 | 0.56 | 1.48 [1.16, 1.85] | -0.89 [-1.08, -0.74] | -0.26 [-0.39, -0.14] | – | 0.90 [0.85, 0.94] |
| check_only | – | 299 / 300 | 1 | 0.92 | 0.46 | 1.51 [1.21, 1.88] | -0.66 [-0.84, -0.52] | -0.03 [-0.15, 0.09] | – | 0.90 [0.86, 0.94] |
| may_error | – | 300 / 300 | 0 | 0.92 | 0.44 | 1.56 [1.24, 1.93] | -0.62 [-0.81, -0.46] | 0.02 [-0.10, 0.14] | – | 0.90 [0.86, 0.94] |
| claim_random | – | 300 / 299 | 1 | 0.95 | 0.55 | 1.54 [1.22, 1.97] | -0.90 [-1.10, -0.74] | -0.26 [-0.40, -0.13] | – | 0.90 [0.85, 0.94] |
| claim_correct | – | 300 / 300 | 0 | 0.85 | 0.26 | 1.66 [1.35, 2.00] | -0.19 [-0.36, -0.04] | 0.44 [0.32, 0.58] | – | 0.90 [0.86, 0.94] |
| item_p10 | 0.10 | 300 / 300 | 0 | 0.92 | 0.54 | 1.31 [0.98, 1.70] | -0.75 [-0.95, -0.59] | -0.11 [-0.23, 0.00] | 1.44 | 0.90 [0.85, 0.94] |
| item_p90 | 0.90 | 300 / 300 | 0 | 0.97 | 0.67 | 1.37 [1.00, 1.85] | -1.13 [-1.36, -0.96] | -0.49 [-0.69, -0.34] | -1.44 | 0.90 [0.85, 0.94] |

- **Prior-use ratio ρ = 0.14 [0.10, 0.21]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.40 [0.29, 0.55]; ideal = ln 81 / d′(neutral) = 2.88.
- ρ for stated chance for this solution (item_p10 vs item_p90) = **0.13 [0.09, 0.20]**; minus base-rate ρ = -0.01 [-0.05, 0.03] (paired).
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 20 distinct values.
- z-ROC slope in neutral: 0.97 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 74/81; wrong answer 203/219.

### qwen3.5:4b-think-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 300 / 300 | 0 | 0.99 | 0.15 | 3.22 [2.86, 3.67] | -0.56 [-0.79, -0.38] | 0.00 [0.00, 0.00] | – | 0.94 [0.91, 0.97] |
| br10 | 0.10 | 300 / 300 | 0 | 1.00 | 0.15 | 3.61 [3.36, 3.90] | -0.77 [-0.90, -0.63] | -0.21 [-0.35, -0.02] | 0.68 | 0.95 [0.93, 0.98] |
| br90 | 0.90 | 300 / 300 | 0 | 1.00 | 0.25 | 3.25 [3.02, 3.51] | -0.96 [-1.07, -0.83] | -0.39 [-0.55, -0.19] | -0.68 | 0.93 [0.90, 0.95] |
| presuppose | – | 300 / 300 | 0 | 1.00 | 0.28 | 3.18 [2.98, 3.39] | -0.99 [-1.09, -0.89] | -0.43 [-0.58, -0.23] | – | 0.89 [0.85, 0.92] |
| claim_bare | – | 300 / 299 | 1 | 0.99 | 0.24 | 3.09 [2.75, 3.47] | -0.85 [-1.03, -0.68] | -0.29 [-0.50, -0.06] | – | 0.90 [0.87, 0.94] |
| claim_mistake | – | 300 / 300 | 0 | 1.00 | 0.52 | 2.53 [2.34, 2.72] | -1.31 [-1.41, -1.22] | -0.75 [-0.93, -0.54] | – | 0.81 [0.77, 0.85] |
| claim_reviewer | – | 300 / 300 | 0 | 1.00 | 0.32 | 3.05 [2.84, 3.30] | -1.05 [-1.16, -0.93] | -0.49 [-0.66, -0.29] | – | 0.88 [0.85, 0.92] |
| check_only | – | 300 / 300 | 0 | 1.00 | 0.15 | 3.61 [3.36, 3.92] | -0.77 [-0.90, -0.62] | -0.21 [-0.34, -0.01] | – | 0.95 [0.92, 0.97] |
| may_error | – | 300 / 300 | 0 | 0.99 | 0.16 | 3.28 [2.92, 3.73] | -0.63 [-0.85, -0.44] | -0.07 [-0.20, 0.03] | – | 0.94 [0.91, 0.96] |
| claim_random | – | 300 / 300 | 0 | 1.00 | 0.19 | 3.45 [3.21, 3.70] | -0.86 [-0.98, -0.73] | -0.29 [-0.43, -0.10] | – | 0.93 [0.89, 0.96] |
| claim_correct | – | 300 / 300 | 0 | 0.98 | 0.11 | 3.30 [2.83, 3.94] | -0.44 [-0.76, -0.20] | 0.12 [-0.14, 0.30] | – | 0.96 [0.93, 0.98] |
| item_p10 | 0.10 | 300 / 300 | 0 | 0.99 | 0.14 | 3.24 [2.81, 3.79] | -0.55 [-0.82, -0.33] | 0.01 [-0.16, 0.11] | 0.68 | 0.93 [0.89, 0.96] |
| item_p90 | 0.90 | 300 / 300 | 0 | 1.00 | 0.28 | 3.17 [2.94, 3.41] | -1.00 [-1.11, -0.87] | -0.43 [-0.59, -0.23] | -0.68 | 0.91 [0.88, 0.95] |

- **Prior-use ratio ρ = 0.14 [0.07, 0.21]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.18 [0.10, 0.27]; ideal = ln 81 / d′(neutral) = 1.36.
- ρ for stated chance for this solution (item_p10 vs item_p90) = **0.32 [0.15, 0.47]**; minus base-rate ρ = 0.19 [0.01, 0.32] (paired).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 16 distinct values.
- z-ROC slope in neutral: 3.98 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 79/81; wrong answer 218/219.

### qwen3.5:9b-nothink-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 300 / 299 | 1 | 0.91 | 0.39 | 1.63 [1.31, 2.01] | -0.54 [-0.72, -0.37] | 0.00 [0.00, 0.00] | – | 0.91 [0.86, 0.94] |
| br10 | 0.10 | 300 / 300 | 0 | 0.93 | 0.38 | 1.74 [1.41, 2.11] | -0.58 [-0.77, -0.41] | -0.03 [-0.16, 0.09] | 1.35 | 0.90 [0.86, 0.94] |
| br90 | 0.90 | 299 / 300 | 1 | 0.96 | 0.45 | 1.81 [1.45, 2.28] | -0.79 [-1.02, -0.62] | -0.25 [-0.42, -0.11] | -1.35 | 0.90 [0.86, 0.94] |
| presuppose | – | 300 / 300 | 0 | 0.93 | 0.47 | 1.52 [1.21, 1.91] | -0.69 [-0.88, -0.52] | -0.14 [-0.26, -0.04] | – | 0.90 [0.86, 0.94] |
| claim_bare | – | 300 / 300 | 0 | 0.96 | 0.49 | 1.72 [1.39, 2.16] | -0.84 [-1.05, -0.67] | -0.30 [-0.44, -0.17] | – | 0.90 [0.86, 0.94] |
| claim_mistake | – | 300 / 299 | 1 | 0.95 | 0.53 | 1.55 [1.21, 2.00] | -0.86 [-1.09, -0.69] | -0.31 [-0.49, -0.16] | – | 0.90 [0.86, 0.94] |
| claim_reviewer | – | 300 / 300 | 0 | 0.95 | 0.54 | 1.53 [1.22, 1.92] | -0.87 [-1.05, -0.71] | -0.32 [-0.45, -0.20] | – | 0.90 [0.85, 0.94] |
| check_only | – | 300 / 300 | 0 | 0.90 | 0.37 | 1.61 [1.29, 2.02] | -0.47 [-0.66, -0.30] | 0.07 [-0.07, 0.21] | – | 0.90 [0.86, 0.94] |
| may_error | – | 300 / 300 | 0 | 0.91 | 0.36 | 1.67 [1.35, 2.06] | -0.48 [-0.68, -0.31] | 0.06 [-0.07, 0.19] | – | 0.90 [0.86, 0.94] |
| claim_random | – | 300 / 300 | 0 | 0.91 | 0.37 | 1.69 [1.35, 2.07] | -0.51 [-0.71, -0.34] | 0.03 [-0.09, 0.14] | – | 0.90 [0.85, 0.94] |
| claim_correct | – | 299 / 299 | 2 | 0.86 | 0.26 | 1.70 [1.40, 2.05] | -0.21 [-0.38, -0.05] | 0.33 [0.22, 0.46] | – | 0.91 [0.86, 0.94] |
| item_p10 | 0.10 | 299 / 300 | 1 | 0.92 | 0.33 | 1.81 [1.49, 2.19] | -0.47 [-0.65, -0.31] | 0.07 [-0.03, 0.18] | 1.35 | 0.90 [0.86, 0.94] |
| item_p90 | 0.90 | 299 / 300 | 1 | 0.95 | 0.41 | 1.82 [1.47, 2.24] | -0.69 [-0.91, -0.53] | -0.15 [-0.30, -0.02] | -1.35 | 0.90 [0.86, 0.94] |

- **Prior-use ratio ρ = 0.08 [0.04, 0.13]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.22 [0.12, 0.34]; ideal = ln 81 / d′(neutral) = 2.70.
- ρ for stated chance for this solution (item_p10 vs item_p90) = **0.08 [0.05, 0.13]**; minus base-rate ρ = 0.00 [-0.04, 0.04] (paired).
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 10 distinct values.
- z-ROC slope in neutral: 1.13 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 74/81; wrong answer 201/219.

### qwen3.5:9b-think-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 299 / 300 | 1 | 1.00 | 0.16 | 3.56 [3.31, 3.86] | -0.80 [-0.92, -0.65] | 0.00 [0.00, 0.00] | – | 0.95 [0.93, 0.98] |
| br10 | 0.10 | 300 / 300 | 0 | 0.99 | 0.18 | 3.31 [2.96, 3.69] | -0.74 [-0.91, -0.56] | 0.06 [-0.08, 0.20] | 0.62 | 0.95 [0.92, 0.97] |
| br90 | 0.90 | 300 / 300 | 0 | 1.00 | 0.28 | 3.18 [2.97, 3.41] | -0.99 [-1.09, -0.87] | -0.19 [-0.29, -0.11] | -0.62 | 0.95 [0.92, 0.97] |
| presuppose | – | 300 / 300 | 0 | 1.00 | 0.23 | 3.31 [3.09, 3.56] | -0.92 [-1.03, -0.80] | -0.13 [-0.21, -0.06] | – | 0.94 [0.91, 0.96] |
| claim_bare | – | 299 / 300 | 1 | 1.00 | 0.30 | 3.11 [2.91, 3.33] | -1.02 [-1.12, -0.91] | -0.23 [-0.33, -0.14] | – | 0.93 [0.89, 0.95] |
| claim_mistake | – | 299 / 293 | 8 | 1.00 | 0.49 | 2.61 [2.40, 2.83] | -1.27 [-1.38, -1.16] | -0.48 [-0.60, -0.36] | – | 0.88 [0.84, 0.91] |
| claim_reviewer | – | 299 / 300 | 1 | 1.00 | 0.37 | 2.90 [2.69, 3.13] | -1.13 [-1.23, -1.02] | -0.33 [-0.45, -0.23] | – | 0.91 [0.88, 0.93] |
| check_only | – | 298 / 300 | 2 | 1.00 | 0.16 | 3.57 [3.32, 3.85] | -0.79 [-0.92, -0.65] | 0.01 [-0.05, 0.06] | – | 0.96 [0.93, 0.98] |
| may_error | – | 300 / 300 | 0 | 0.99 | 0.15 | 3.45 [3.09, 3.86] | -0.67 [-0.86, -0.48] | 0.12 [-0.01, 0.27] | – | 0.94 [0.91, 0.97] |
| claim_random | – | 300 / 300 | 0 | 1.00 | 0.21 | 3.40 [3.18, 3.66] | -0.88 [-0.99, -0.75] | -0.08 [-0.15, -0.03] | – | 0.94 [0.91, 0.96] |
| claim_correct | – | 299 / 300 | 1 | 0.98 | 0.13 | 3.22 [2.75, 3.84] | -0.48 [-0.79, -0.24] | 0.31 [0.05, 0.52] | – | 0.95 [0.92, 0.97] |
| item_p10 | 0.10 | 299 / 300 | 1 | 1.00 | 0.17 | 3.53 [3.29, 3.82] | -0.81 [-0.93, -0.67] | -0.01 [-0.08, 0.05] | 0.62 | 0.97 [0.95, 0.98] |
| item_p90 | 0.90 | 300 / 300 | 0 | 1.00 | 0.29 | 3.15 [2.92, 3.39] | -1.01 [-1.12, -0.89] | -0.21 [-0.30, -0.13] | -0.62 | 0.93 [0.91, 0.96] |

- **Prior-use ratio ρ = 0.20 [0.08, 0.33]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.25 [0.10, 0.40]; ideal = ln 81 / d′(neutral) = 1.23.
- ρ for stated chance for this solution (item_p10 vs item_p90) = **0.16 [0.08, 0.25]**; minus base-rate ρ = -0.05 [-0.17, 0.08] (paired).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 14 distinct values.
- z-ROC slope in neutral: 2.26 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 81/81; wrong answer 218/218.

### qwen3.5:27b-nothink-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 300 / 300 | 0 | 0.90 | 0.20 | 2.12 [1.77, 2.54] | -0.22 [-0.42, -0.03] | 0.00 [0.00, 0.00] | – | 0.94 [0.90, 0.97] |
| br10 | 0.10 | 300 / 300 | 0 | 0.89 | 0.22 | 2.03 [1.72, 2.39] | -0.23 [-0.41, -0.06] | -0.01 [-0.13, 0.11] | 1.04 | 0.93 [0.90, 0.96] |
| br90 | 0.90 | 300 / 300 | 0 | 0.92 | 0.26 | 2.02 [1.70, 2.41] | -0.37 [-0.56, -0.20] | -0.15 [-0.27, -0.03] | -1.04 | 0.93 [0.90, 0.96] |
| presuppose | – | 300 / 300 | 0 | 0.91 | 0.28 | 1.91 [1.60, 2.27] | -0.38 [-0.57, -0.22] | -0.16 [-0.28, -0.05] | – | 0.94 [0.90, 0.97] |
| claim_bare | – | 300 / 300 | 0 | 0.91 | 0.27 | 1.95 [1.62, 2.35] | -0.36 [-0.56, -0.18] | -0.14 [-0.26, -0.02] | – | 0.94 [0.90, 0.97] |
| claim_mistake | – | 300 / 300 | 0 | 0.94 | 0.29 | 2.07 [1.73, 2.49] | -0.49 [-0.70, -0.31] | -0.27 [-0.42, -0.13] | – | 0.94 [0.90, 0.97] |
| claim_reviewer | – | 300 / 300 | 0 | 0.92 | 0.30 | 1.91 [1.58, 2.28] | -0.42 [-0.62, -0.26] | -0.21 [-0.33, -0.08] | – | 0.94 [0.90, 0.97] |
| check_only | – | 300 / 300 | 0 | 0.87 | 0.22 | 1.93 [1.60, 2.30] | -0.18 [-0.35, -0.01] | 0.04 [-0.07, 0.16] | – | 0.94 [0.90, 0.96] |
| may_error | – | 300 / 300 | 0 | 0.87 | 0.19 | 1.99 [1.66, 2.39] | -0.13 [-0.32, 0.06] | 0.09 [-0.03, 0.23] | – | 0.94 [0.90, 0.97] |
| claim_random | – | 300 / 300 | 0 | 0.88 | 0.22 | 1.95 [1.61, 2.32] | -0.21 [-0.40, -0.03] | 0.00 [-0.10, 0.11] | – | 0.94 [0.90, 0.97] |
| claim_correct | – | 300 / 300 | 0 | 0.88 | 0.20 | 2.02 [1.70, 2.41] | -0.18 [-0.37, 0.01] | 0.04 [-0.07, 0.16] | – | 0.94 [0.90, 0.97] |
| item_p10 | 0.10 | 300 / 300 | 0 | 0.88 | 0.19 | 2.04 [1.73, 2.41] | -0.15 [-0.33, 0.02] | 0.06 [-0.06, 0.20] | 1.04 | 0.93 [0.90, 0.97] |
| item_p90 | 0.90 | 300 / 300 | 0 | 0.92 | 0.25 | 2.09 [1.75, 2.49] | -0.36 [-0.55, -0.18] | -0.14 [-0.28, -0.01] | -1.04 | 0.93 [0.90, 0.96] |

- **Prior-use ratio ρ = 0.07 [0.04, 0.11]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.14 [0.08, 0.21]; ideal = ln 81 / d′(neutral) = 2.07.
- ρ for stated chance for this solution (item_p10 vs item_p90) = **0.10 [0.06, 0.16]**; minus base-rate ρ = 0.03 [-0.00, 0.07] (paired).
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 13 distinct values.
- z-ROC slope in neutral: 1.06 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 72/81; wrong answer 199/219.

### qwen3.5:27b-think-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 296 / 300 | 4 | 0.99 | 0.20 | 3.43 [3.20, 3.70] | -0.86 [-0.98, -0.72] | 0.00 [0.00, 0.00] | – | 0.94 [0.91, 0.97] |
| br10 | 0.10 | 296 / 299 | 5 | 0.99 | 0.19 | 3.28 [2.92, 3.67] | -0.75 [-0.93, -0.57] | 0.11 [-0.02, 0.25] | 0.64 | 0.96 [0.94, 0.98] |
| br90 | 0.90 | 297 / 299 | 4 | 0.99 | 0.44 | 2.72 [2.50, 2.95] | -1.22 [-1.32, -1.10] | -0.36 [-0.47, -0.26] | -0.64 | 0.93 [0.90, 0.96] |
| presuppose | – | 298 / 290 | 12 | 1.00 | 0.52 | 2.53 [2.31, 2.75] | -1.31 [-1.42, -1.20] | -0.45 [-0.57, -0.35] | – | 0.85 [0.81, 0.89] |
| claim_bare | – | 300 / 300 | 0 | 1.00 | 0.47 | 2.66 [2.47, 2.86] | -1.25 [-1.34, -1.15] | -0.39 [-0.51, -0.29] | – | 0.85 [0.82, 0.89] |
| claim_mistake | – | 298 / 280 | 22 | 1.00 | 0.63 | 2.25 [2.02, 2.47] | -1.45 [-1.56, -1.34] | -0.59 [-0.73, -0.47] | – | 0.85 [0.81, 0.89] |
| claim_reviewer | – | 298 / 295 | 7 | 1.00 | 0.50 | 2.57 [2.36, 2.79] | -1.29 [-1.39, -1.18] | -0.43 [-0.56, -0.33] | – | 0.88 [0.85, 0.92] |
| check_only | – | 295 / 300 | 5 | 0.99 | 0.18 | 3.29 [2.96, 3.69] | -0.74 [-0.93, -0.55] | 0.12 [-0.01, 0.25] | – | 0.94 [0.91, 0.97] |
| may_error | – | 295 / 300 | 5 | 0.99 | 0.19 | 3.44 [3.21, 3.70] | -0.85 [-0.97, -0.72] | 0.01 [-0.03, 0.05] | – | 0.95 [0.93, 0.98] |
| claim_random | – | 296 / 300 | 4 | 0.99 | 0.24 | 3.29 [3.06, 3.55] | -0.93 [-1.04, -0.80] | -0.07 [-0.15, 0.01] | – | 0.94 [0.91, 0.96] |
| claim_correct | – | 297 / 300 | 3 | 0.98 | 0.16 | 3.03 [2.64, 3.63] | -0.51 [-0.78, -0.28] | 0.35 [0.08, 0.53] | – | 0.95 [0.92, 0.97] |
| item_p10 | 0.10 | 298 / 300 | 2 | 0.99 | 0.16 | 3.18 [2.78, 3.74] | -0.58 [-0.84, -0.37] | 0.28 [0.04, 0.45] | 0.64 | 0.97 [0.94, 0.99] |
| item_p90 | 0.90 | 299 / 299 | 2 | 1.00 | 0.42 | 2.79 [2.58, 3.02] | -1.18 [-1.29, -1.07] | -0.32 [-0.43, -0.23] | -0.64 | 0.93 [0.90, 0.96] |

- **Prior-use ratio ρ = 0.36 [0.22, 0.52]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.46 [0.30, 0.64]; ideal = ln 81 / d′(neutral) = 1.28.
- ρ for stated chance for this solution (item_p10 vs item_p90) = **0.47 [0.26, 0.65]**; minus base-rate ρ = 0.11 [-0.02, 0.26] (paired).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 14 distinct values.
- z-ROC slope in neutral: – (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 80/80; wrong answer 216/216.

### Model comparison (paired over the same items)

- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(gemma4:12b-think-bf16-t1) = 0.00 [-0.16, 0.19]
- stated chance for this solution: ρ(gemma4:12b-nothink-bf16-t1) − ρ(gemma4:12b-think-bf16-t1) = -0.10 [-0.29, 0.05]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.07 [-0.15, 0.02]
- stated chance for this solution: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.02 [-0.11, 0.09]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.07 [-0.15, 0.03]
- stated chance for this solution: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.21 [-0.35, -0.02]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.01 [-0.08, 0.07]
- stated chance for this solution: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.03 [-0.04, 0.13]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.14 [-0.26, 0.01]
- stated chance for this solution: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.04 [-0.14, 0.07]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.00 [-0.06, 0.07]
- stated chance for this solution: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.02 [-0.07, 0.12]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.29 [-0.45, -0.14]
- stated chance for this solution: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.35 [-0.53, -0.14]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.07 [-0.27, 0.10]
- stated chance for this solution: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = 0.08 [-0.05, 0.26]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.07 [-0.28, 0.10]
- stated chance for this solution: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.11 [-0.25, 0.10]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.01 [-0.22, 0.15]
- stated chance for this solution: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.13 [0.01, 0.31]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.14 [-0.35, 0.09]
- stated chance for this solution: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = 0.06 [-0.08, 0.24]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.00 [-0.19, 0.16]
- stated chance for this solution: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.12 [-0.03, 0.31]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.30 [-0.52, -0.07]
- stated chance for this solution: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.25 [-0.47, 0.03]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = 0.00 [-0.08, 0.09]
- stated chance for this solution: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.19 [-0.33, -0.00]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.06 [0.00, 0.13]
- stated chance for this solution: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.05 [-0.00, 0.11]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.06 [-0.19, 0.08]
- stated chance for this solution: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.02 [-0.12, 0.07]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.07 [0.01, 0.15]
- stated chance for this solution: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.04 [-0.04, 0.11]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.22 [-0.37, -0.07]
- stated chance for this solution: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.34 [-0.51, -0.12]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.06 [-0.02, 0.13]
- stated chance for this solution: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.24 [0.06, 0.38]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.07 [-0.19, 0.06]
- stated chance for this solution: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = 0.17 [-0.00, 0.30]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.07 [-0.00, 0.15]
- stated chance for this solution: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.23 [0.05, 0.37]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.23 [-0.37, -0.08]
- stated chance for this solution: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.14 [-0.32, 0.01]
- stated base rate: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.12 [-0.25, 0.01]
- stated chance for this solution: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.08 [-0.16, 0.01]
- stated base rate: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.01 [-0.03, 0.07]
- stated chance for this solution: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.02 [-0.08, 0.04]
- stated base rate: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.28 [-0.43, -0.14]
- stated chance for this solution: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.39 [-0.56, -0.18]
- stated base rate: ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.14 [0.01, 0.26]
- stated chance for this solution: ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.06 [-0.03, 0.15]
- stated base rate: ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.16 [-0.27, -0.08]
- stated chance for this solution: ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.31 [-0.47, -0.11]
- stated base rate: ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.29 [-0.44, -0.16]
- stated chance for this solution: ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.37 [-0.54, -0.16]
