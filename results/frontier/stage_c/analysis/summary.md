### haiku-5.5-nothink

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.97 | 0.54 | 1.72 [1.28, 2.48] | -0.96 [-1.34, -0.75] | 0.00 [0.00, 0.00] | – | 0.77 [0.73, 0.82] |
| br10 | 0.10 | 100 / 100 | 0 | 0.94 | 0.40 | 1.77 [1.41, 2.31] | -0.63 [-0.90, -0.43] | 0.32 [0.09, 0.64] | 1.45 | 0.82 [0.76, 0.87] |
| br50 | 0.50 | 100 / 100 | 0 | 0.94 | 0.50 | 1.52 [1.13, 2.06] | -0.76 [-1.04, -0.56] | 0.20 [0.02, 0.47] | 0.00 | 0.79 [0.73, 0.84] |
| br90 | 0.90 | 100 / 100 | 0 | 0.95 | 0.45 | 1.73 [1.34, 2.30] | -0.74 [-1.04, -0.54] | 0.22 [-0.01, 0.53] | -1.45 | 0.81 [0.75, 0.86] |
| br10_use | 0.10 | 100 / 100 | 0 | 0.98 | 0.36 | 2.32 [1.90, 3.07] | -0.80 [-1.18, -0.58] | 0.15 [-0.18, 0.47] | 1.45 | 0.88 [0.83, 0.92] |
| br90_use | 0.90 | 100 / 100 | 0 | 0.97 | 0.36 | 2.17 [1.75, 2.93] | -0.73 [-1.13, -0.51] | 0.23 [-0.12, 0.59] | -1.45 | 0.87 [0.82, 0.91] |
| pay_fa9 | 0.10 | 100 / 100 | 0 | 0.96 | 0.38 | 2.00 [1.60, 2.64] | -0.70 [-1.02, -0.48] | 0.26 [0.01, 0.55] | 1.45 | 0.83 [0.77, 0.88] |
| pay_miss9 | 0.90 | 100 / 100 | 0 | 0.97 | 0.42 | 2.02 [1.59, 2.80] | -0.81 [-1.20, -0.61] | 0.15 [-0.10, 0.39] | -1.45 | 0.84 [0.79, 0.89] |
| presuppose | – | 100 / 100 | 0 | 0.98 | 0.62 | 1.66 [1.21, 2.38] | -1.13 [-1.49, -0.91] | -0.18 [-0.50, 0.14] | – | 0.69 [0.64, 0.75] |
| find_bugs | – | 100 / 100 | 0 | 0.99 | 0.52 | 2.12 [1.66, 2.70] | -1.11 [-1.40, -0.87] | -0.15 [-0.50, 0.25] | – | 0.77 [0.72, 0.82] |
| harsh | – | 100 / 100 | 0 | 0.96 | 0.51 | 1.68 [1.27, 2.30] | -0.86 [-1.17, -0.65] | 0.10 [-0.02, 0.29] | – | 0.76 [0.71, 0.81] |
| lenient | – | 100 / 100 | 0 | 0.97 | 0.36 | 2.17 [1.77, 2.91] | -0.73 [-1.11, -0.51] | 0.23 [-0.03, 0.49] | – | 0.90 [0.85, 0.94] |
| stakes_miss | – | 100 / 100 | 0 | 0.95 | 0.42 | 1.80 [1.43, 2.40] | -0.70 [-0.98, -0.50] | 0.26 [0.02, 0.54] | – | 0.81 [0.75, 0.86] |
| stakes_fa | – | 100 / 100 | 0 | 0.98 | 0.32 | 2.43 [2.00, 3.16] | -0.75 [-1.11, -0.53] | 0.21 [-0.04, 0.37] | – | 0.88 [0.83, 0.92] |
| persona | – | 100 / 100 | 0 | 0.98 | 0.45 | 2.09 [1.68, 2.83] | -0.92 [-1.29, -0.69] | 0.04 [-0.31, 0.35] | – | 0.79 [0.74, 0.84] |
| lab_neutral | – | 100 / 100 | 0 | 0.99 | 0.50 | 2.17 [1.70, 2.78] | -1.09 [-1.38, -0.86] | -0.13 [-0.40, 0.09] | – | 0.81 [0.77, 0.86] |
| lab_br10 | 0.10 | 100 / 100 | 0 | 0.96 | 0.42 | 1.90 [1.50, 2.50] | -0.75 [-1.05, -0.55] | 0.21 [-0.02, 0.49] | 1.45 | 0.82 [0.76, 0.87] |
| lab_br90 | 0.90 | 100 / 100 | 0 | 0.92 | 0.43 | 1.55 [1.21, 2.04] | -0.60 [-0.85, -0.41] | 0.36 [0.17, 0.65] | -1.45 | 0.80 [0.74, 0.85] |

- **Prior-use ratio ρ = 0.04 [-0.00, 0.10]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.11 [-0.01, 0.26]; ideal = ln 81 / d′(br50) = 2.89.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **-0.03 [-0.12, 0.02]**; minus base-rate ρ = -0.06 [-0.19, -0.00] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **0.04 [-0.05, 0.15]**; minus base-rate ρ = 0.00 [-0.10, 0.11] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **-0.05 [-0.13, 0.01]**; minus base-rate ρ = -0.09 [-0.18, -0.03] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.20 [0.02, 0.47].
- **Bayes check** (own stated confidence at 50% as the posterior; 200 items, 8% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 16 of 144 flags, the critic dropped 4 of those (+9 others); told 90%, a Bayesian adds 0 of 56 passes as flags, the critic added 0 (+3 others); 10 changes against the stated rate. c(10%) − c(90%): observed 0.11 [-0.01, 0.26], Bayesian 0.25 [0.13, 0.41]; **ρ_Bayes = 0.42 [-0.04, 1.27]** (1 = moves as far as its own confidence implies).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 25 distinct values.
- z-ROC slope in br50: 1.23 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 29/30; wrong answer 68/70.

### haiku-5.5-think

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.97 | 0.12 | 2.97 [2.54, 3.74] | -0.33 [-0.71, -0.08] | 0.00 [0.00, 0.00] | – | 0.97 [0.95, 0.99] |
| br10 | 0.10 | 100 / 100 | 0 | 0.98 | 0.12 | 3.12 [2.68, 3.84] | -0.40 [-0.78, -0.14] | -0.07 [-0.31, 0.08] | 0.66 | 0.98 [0.97, 1.00] |
| br50 | 0.50 | 100 / 100 | 0 | 0.99 | 0.12 | 3.33 [2.88, 3.96] | -0.51 [-0.82, -0.22] | -0.18 [-0.47, 0.03] | 0.00 | 0.99 [0.97, 1.00] |
| br90 | 0.90 | 100 / 100 | 0 | 0.98 | 0.12 | 3.12 [2.68, 3.90] | -0.40 [-0.78, -0.13] | -0.07 [-0.31, 0.00] | -0.66 | 0.98 [0.97, 1.00] |
| br10_use | 0.10 | 100 / 100 | 0 | 0.98 | 0.10 | 3.22 [2.76, 3.99] | -0.35 [-0.74, -0.09] | -0.02 [-0.26, 0.11] | 0.66 | 0.99 [0.97, 1.00] |
| br90_use | 0.90 | 100 / 100 | 0 | 0.95 | 0.09 | 2.92 [2.51, 3.57] | -0.14 [-0.44, 0.11] | 0.19 [0.04, 0.43] | -0.66 | 0.97 [0.95, 0.99] |
| pay_fa9 | 0.10 | 100 / 100 | 0 | 0.98 | 0.11 | 3.17 [2.72, 3.90] | -0.38 [-0.76, -0.11] | -0.05 [-0.29, 0.06] | 0.66 | 0.98 [0.96, 0.99] |
| pay_miss9 | 0.90 | 100 / 100 | 0 | 0.97 | 0.10 | 3.08 [2.65, 3.84] | -0.28 [-0.66, -0.00] | 0.05 [-0.18, 0.29] | -0.66 | 0.98 [0.96, 1.00] |
| presuppose | – | 100 / 100 | 0 | 0.99 | 0.12 | 3.33 [2.88, 3.96] | -0.51 [-0.82, -0.22] | -0.18 [-0.47, 0.03] | – | 0.98 [0.96, 1.00] |
| find_bugs | – | 100 / 100 | 0 | 0.97 | 0.15 | 2.84 [2.42, 3.56] | -0.40 [-0.78, -0.16] | -0.07 [-0.31, 0.17] | – | 0.98 [0.96, 0.99] |
| harsh | – | 100 / 100 | 0 | 0.98 | 0.14 | 3.03 [2.60, 3.79] | -0.45 [-0.82, -0.19] | -0.12 [-0.36, 0.02] | – | 0.98 [0.96, 0.99] |
| lenient | – | 100 / 100 | 0 | 0.97 | 0.08 | 3.19 [2.76, 4.02] | -0.22 [-0.60, 0.05] | 0.11 [-0.14, 0.36] | – | 0.98 [0.96, 1.00] |
| stakes_miss | – | 100 / 100 | 0 | 0.99 | 0.12 | 3.33 [2.88, 3.96] | -0.51 [-0.82, -0.22] | -0.18 [-0.47, 0.03] | – | 0.98 [0.96, 1.00] |
| stakes_fa | – | 100 / 100 | 0 | 0.97 | 0.10 | 3.08 [2.63, 3.84] | -0.28 [-0.66, 0.00] | 0.05 [0.00, 0.13] | – | 0.98 [0.96, 1.00] |
| persona | – | 100 / 100 | 0 | 0.97 | 0.12 | 2.97 [2.54, 3.74] | -0.33 [-0.69, -0.08] | 0.00 [-0.22, 0.24] | – | 0.98 [0.96, 0.99] |
| lab_neutral | – | 100 / 100 | 0 | 0.99 | 0.14 | 3.24 [2.80, 3.90] | -0.55 [-0.87, -0.29] | -0.22 [-0.51, -0.02] | – | 0.98 [0.96, 0.99] |
| lab_br10 | 0.10 | 100 / 100 | 0 | 0.98 | 0.12 | 3.12 [2.68, 3.90] | -0.40 [-0.78, -0.15] | -0.07 [-0.31, 0.00] | 0.66 | 0.99 [0.97, 1.00] |
| lab_br90 | 0.90 | 100 / 100 | 0 | 0.99 | 0.14 | 3.24 [2.80, 3.90] | -0.55 [-0.87, -0.29] | -0.22 [-0.51, -0.02] | -0.66 | 0.98 [0.97, 1.00] |

- **Prior-use ratio ρ = 0.00 [-0.26, 0.25]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.00 [-0.31, 0.31]; ideal = ln 81 / d′(br50) = 1.32.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **-0.16 [-0.43, -0.02]**; minus base-rate ρ = -0.16 [-0.46, 0.01] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **-0.08 [-0.29, 0.00]**; minus base-rate ρ = -0.08 [-0.38, 0.17] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.11 [0.00, 0.35]**; minus base-rate ρ = 0.11 [-0.04, 0.37] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = -0.18 [-0.47, 0.03].
- **Bayes check** (own stated confidence at 50% as the posterior; 200 items, 14% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 21 of 111 flags, the critic dropped 2 of those (+0 others); told 90%, a Bayesian adds 8 of 89 passes as flags, the critic added 1 (+0 others); 3 changes against the stated rate. c(10%) − c(90%): observed 0.00 [-0.31, 0.31], Bayesian 1.16 [0.87, 1.63]; **ρ_Bayes = 0.00 [-0.25, 0.24]** (1 = moves as far as its own confidence implies).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 48 distinct values.
- z-ROC slope in br50: 0.69 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 27/30; wrong answer 70/70.

### opus-5.5-think

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.98 | 0.13 | 3.07 [2.60, 3.79] | -0.43 [-0.80, -0.17] | 0.00 [0.00, 0.00] | – | 0.99 [0.97, 1.00] |
| br10 | 0.10 | 100 / 100 | 0 | 0.97 | 0.11 | 3.02 [2.55, 3.78] | -0.31 [-0.69, -0.04] | 0.12 [0.00, 0.36] | 0.70 | 0.99 [0.97, 1.00] |
| br50 | 0.50 | 100 / 100 | 0 | 0.98 | 0.12 | 3.12 [2.65, 3.90] | -0.40 [-0.78, -0.13] | 0.02 [0.00, 0.09] | 0.00 | 0.99 [0.98, 1.00] |
| br90 | 0.90 | 100 / 100 | 0 | 0.99 | 0.16 | 3.15 [2.69, 3.79] | -0.60 [-0.91, -0.33] | -0.17 [-0.46, 0.00] | -0.70 | 0.99 [0.97, 1.00] |
| presuppose | – | 100 / 100 | 0 | 1.00 | 0.60 | 2.33 [2.09, 2.58] | -1.42 [-1.53, -1.29] | -0.99 [-1.24, -0.60] | – | 0.99 [0.98, 1.00] |
| lenient | – | 100 / 100 | 0 | 0.97 | 0.07 | 3.26 [2.81, 4.02] | -0.19 [-0.60, 0.11] | 0.24 [0.08, 0.50] | – | 0.99 [0.97, 1.00] |

- **Prior-use ratio ρ = 0.21 [0.05, 0.44]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.29 [0.07, 0.60]; ideal = ln 81 / d′(br50) = 1.41.
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.02 [0.00, 0.09].
- **Bayes check** (own stated confidence at 50% as the posterior; 200 items, 22% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 26 of 110 flags, the critic dropped 2 of those (+0 others); told 90%, a Bayesian adds 18 of 90 passes as flags, the critic added 5 (+0 others); 0 changes against the stated rate. c(10%) − c(90%): observed 0.29 [0.07, 0.60], Bayesian 1.43 [1.13, 1.90]; **ρ_Bayes = 0.20 [0.05, 0.37]** (1 = moves as far as its own confidence implies).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 43 distinct values.
- z-ROC slope in br50: 0.79 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 28/30; wrong answer 70/70.

### sonnet-5.5-nothink

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.96 | 0.10 | 2.96 [2.51, 3.66] | -0.22 [-0.57, 0.05] | 0.00 [0.00, 0.00] | – | 0.98 [0.97, 1.00] |
| br10 | 0.10 | 100 / 100 | 0 | 0.94 | 0.09 | 2.84 [2.42, 3.42] | -0.10 [-0.38, 0.16] | 0.12 [-0.09, 0.39] | 0.78 | 0.98 [0.96, 0.99] |
| br50 | 0.50 | 100 / 100 | 0 | 0.95 | 0.11 | 2.81 [2.39, 3.42] | -0.20 [-0.49, 0.04] | 0.02 [-0.19, 0.26] | 0.00 | 0.98 [0.96, 0.99] |
| br90 | 0.90 | 99 / 100 | 1 | 0.97 | 0.14 | 3.02 [2.55, 3.78] | -0.45 [-0.82, -0.19] | -0.23 [-0.51, -0.06] | -0.78 | 0.98 [0.97, 1.00] |
| br10_use | 0.10 | 98 / 100 | 2 | 0.93 | 0.07 | 2.95 [2.52, 3.61] | -0.03 [-0.32, 0.23] | 0.19 [0.01, 0.42] | 0.78 | 0.98 [0.96, 0.99] |
| br90_use | 0.90 | 100 / 100 | 0 | 0.97 | 0.14 | 2.88 [2.46, 3.62] | -0.38 [-0.74, -0.13] | -0.16 [-0.44, 0.11] | -0.78 | 0.99 [0.97, 1.00] |
| pay_fa9 | 0.10 | 100 / 100 | 0 | 0.95 | 0.08 | 2.98 [2.53, 3.66] | -0.11 [-0.40, 0.15] | 0.11 [-0.11, 0.36] | 0.78 | 0.98 [0.96, 0.99] |
| pay_miss9 | 0.90 | 100 / 100 | 0 | 0.95 | 0.10 | 2.86 [2.43, 3.49] | -0.17 [-0.47, 0.08] | 0.05 [-0.13, 0.29] | -0.78 | 0.98 [0.96, 0.99] |
| presuppose | – | 100 / 100 | 0 | 0.96 | 0.11 | 2.91 [2.47, 3.57] | -0.25 [-0.58, 0.00] | -0.03 [-0.24, 0.20] | – | 0.98 [0.96, 0.99] |
| find_bugs | – | 100 / 100 | 0 | 0.97 | 0.12 | 2.97 [2.51, 3.74] | -0.33 [-0.71, -0.07] | -0.11 [-0.31, 0.00] | – | 0.98 [0.97, 1.00] |
| harsh | – | 100 / 100 | 0 | 0.97 | 0.13 | 2.93 [2.47, 3.69] | -0.35 [-0.74, -0.09] | -0.13 [-0.35, 0.00] | – | 0.98 [0.96, 0.99] |
| lenient | – | 100 / 100 | 0 | 0.94 | 0.06 | 3.04 [2.58, 3.69] | -0.00 [-0.29, 0.29] | 0.22 [0.06, 0.46] | – | 0.98 [0.97, 1.00] |
| stakes_miss | – | 100 / 100 | 0 | 0.98 | 0.11 | 3.17 [2.72, 3.96] | -0.38 [-0.76, -0.11] | -0.16 [-0.44, 0.03] | – | 0.98 [0.97, 1.00] |
| stakes_fa | – | 100 / 100 | 0 | 0.93 | 0.04 | 3.14 [2.68, 3.87] | 0.13 [-0.15, 0.44] | 0.35 [0.15, 0.67] | – | 0.98 [0.96, 1.00] |
| persona | – | 100 / 100 | 0 | 0.96 | 0.13 | 2.81 [2.36, 3.43] | -0.30 [-0.62, -0.06] | -0.08 [-0.27, 0.12] | – | 0.98 [0.97, 1.00] |
| lab_neutral | – | 100 / 100 | 0 | 0.98 | 0.12 | 3.12 [2.67, 3.87] | -0.40 [-0.78, -0.14] | -0.18 [-0.46, -0.02] | – | 0.99 [0.97, 1.00] |
| lab_br10 | 0.10 | 99 / 100 | 1 | 0.94 | 0.09 | 2.91 [2.46, 3.55] | -0.14 [-0.45, 0.13] | 0.08 [-0.07, 0.28] | 0.78 | 0.99 [0.97, 1.00] |
| lab_br90 | 0.90 | 100 / 100 | 0 | 0.97 | 0.15 | 2.84 [2.42, 3.57] | -0.40 [-0.76, -0.16] | -0.18 [-0.45, 0.07] | -0.78 | 0.98 [0.96, 0.99] |

- **Prior-use ratio ρ = 0.22 [0.09, 0.45]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.35 [0.15, 0.67]; ideal = ln 81 / d′(br50) = 1.56.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.22 [0.10, 0.43]**; minus base-rate ρ = -0.00 [-0.22, 0.18] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **0.04 [-0.04, 0.13]**; minus base-rate ρ = -0.18 [-0.43, -0.03] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.16 [0.06, 0.35]**; minus base-rate ρ = -0.06 [-0.26, 0.11] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.02 [-0.19, 0.26].
- **Bayes check** (own stated confidence at 50% as the posterior; 199 items, 18% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 25 of 105 flags, the critic dropped 6 of those (+0 others); told 90%, a Bayesian adds 11 of 94 passes as flags, the critic added 8 (+0 others); 5 changes against the stated rate. c(10%) − c(90%): observed 0.35 [0.15, 0.67], Bayesian 1.13 [0.86, 1.58]; **ρ_Bayes = 0.31 [0.14, 0.50]** (1 = moves as far as its own confidence implies).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 42 distinct values.
- z-ROC slope in br50: 0.86 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 26/30; wrong answer 70/70.

### sonnet-5.5-think

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.96 | 0.08 | 3.08 [2.64, 3.78] | -0.16 [-0.48, 0.11] | 0.00 [0.00, 0.00] | – | 0.99 [0.97, 1.00] |
| br10 | 0.10 | 100 / 100 | 0 | 0.94 | 0.08 | 2.90 [2.47, 3.52] | -0.07 [-0.36, 0.20] | 0.09 [-0.09, 0.30] | 0.70 | 0.98 [0.96, 0.99] |
| br50 | 0.50 | 100 / 100 | 0 | 0.95 | 0.06 | 3.12 [2.69, 3.78] | -0.04 [-0.35, 0.26] | 0.12 [-0.07, 0.37] | 0.00 | 0.98 [0.97, 1.00] |
| br90 | 0.90 | 100 / 100 | 0 | 0.96 | 0.11 | 2.91 [2.47, 3.55] | -0.25 [-0.57, 0.00] | -0.09 [-0.20, 0.00] | -0.70 | 0.98 [0.96, 0.99] |
| presuppose | – | 100 / 100 | 0 | 0.98 | 0.21 | 2.76 [2.31, 3.48] | -0.58 [-0.96, -0.35] | -0.42 [-0.72, -0.21] | – | 0.98 [0.95, 0.99] |
| lenient | – | 100 / 100 | 0 | 0.93 | 0.06 | 2.96 [2.53, 3.62] | 0.04 [-0.22, 0.33] | 0.20 [-0.03, 0.48] | – | 0.98 [0.96, 0.99] |

- **Prior-use ratio ρ = 0.13 [0.01, 0.31]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.18 [0.01, 0.40]; ideal = ln 81 / d′(br50) = 1.41.
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.12 [-0.07, 0.37].
- **Bayes check** (own stated confidence at 50% as the posterior; 200 items, 18% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 20 of 101 flags, the critic dropped 2 of those (+0 others); told 90%, a Bayesian adds 15 of 99 passes as flags, the critic added 6 (+1 others); 4 changes against the stated rate. c(10%) − c(90%): observed 0.18 [0.01, 0.40], Bayesian 1.20 [0.90, 1.68]; **ρ_Bayes = 0.15 [0.01, 0.31]** (1 = moves as far as its own confidence implies).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 40 distinct values.
- z-ROC slope in br50: 0.80 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 26/30; wrong answer 70/70.

### sonnet-5.5-think-max

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.97 | 0.12 | 2.97 [2.51, 3.74] | -0.33 [-0.71, -0.08] | 0.00 [0.00, 0.00] | – | 0.99 [0.97, 1.00] |
| br10 | 0.10 | 99 / 98 | 3 | 0.95 | 0.07 | 3.20 [2.74, 3.96] | -0.09 [-0.43, 0.21] | 0.24 [0.09, 0.49] | 0.74 | 0.99 [0.97, 1.00] |
| br50 | 0.50 | 98 / 100 | 2 | 0.96 | 0.12 | 2.96 [2.51, 3.73] | -0.33 [-0.71, -0.07] | 0.00 [0.00, 0.01] | 0.00 | 0.99 [0.98, 1.00] |
| br90 | 0.90 | 98 / 100 | 2 | 0.97 | 0.12 | 3.11 [2.68, 3.84] | -0.40 [-0.78, -0.14] | -0.07 [-0.30, 0.01] | -0.74 | 0.99 [0.97, 1.00] |
| presuppose | – | 99 / 100 | 1 | 0.97 | 0.18 | 2.86 [2.42, 3.60] | -0.53 [-0.89, -0.29] | -0.20 [-0.44, -0.06] | – | 0.99 [0.98, 1.00] |
| lenient | – | 99 / 100 | 1 | 0.94 | 0.07 | 2.96 [2.52, 3.61] | -0.03 [-0.32, 0.23] | 0.30 [0.11, 0.59] | – | 0.98 [0.96, 0.99] |

- **Prior-use ratio ρ = 0.21 [0.08, 0.46]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.31 [0.11, 0.63]; ideal = ln 81 / d′(br50) = 1.48.
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.00 [0.00, 0.01].
- **Bayes check** (own stated confidence at 50% as the posterior; 196 items, 15% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 20 of 105 flags, the critic dropped 5 of those (+0 others); told 90%, a Bayesian adds 9 of 91 passes as flags, the critic added 1 (+0 others); 0 changes against the stated rate. c(10%) − c(90%): observed 0.26 [0.06, 0.57], Bayesian 1.09 [0.81, 1.56]; **ρ_Bayes = 0.24 [0.06, 0.45]** (1 = moves as far as its own confidence implies).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 52 distinct values.
- z-ROC slope in br50: 0.77 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 27/30; wrong answer 70/70.

### Model comparison (paired over the same items)

- stated base rate: ρ(haiku-5.5-nothink) − ρ(haiku-5.5-think) = 0.04 [-0.20, 0.29]
- base rate + instruction to use it: ρ(haiku-5.5-nothink) − ρ(haiku-5.5-think) = 0.13 [0.01, 0.38]
- stated payoffs: ρ(haiku-5.5-nothink) − ρ(haiku-5.5-think) = 0.11 [0.00, 0.33]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-nothink) − ρ(haiku-5.5-think) = -0.17 [-0.41, -0.04]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(haiku-5.5-think) = 0.42 [-0.01, 1.19]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(opus-5.5-think) = -0.17 [-0.38, -0.03]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(opus-5.5-think) = 0.22 [-0.23, 1.03]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(sonnet-5.5-nothink) = -0.19 [-0.43, -0.03]
- base rate + instruction to use it: ρ(haiku-5.5-nothink) − ρ(sonnet-5.5-nothink) = -0.25 [-0.45, -0.13]
- stated payoffs: ρ(haiku-5.5-nothink) − ρ(sonnet-5.5-nothink) = -0.00 [-0.13, 0.13]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-nothink) − ρ(sonnet-5.5-nothink) = -0.22 [-0.42, -0.10]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(sonnet-5.5-nothink) = 0.12 [-0.39, 0.98]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(sonnet-5.5-think) = -0.09 [-0.29, 0.05]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(sonnet-5.5-think) = 0.28 [-0.21, 1.14]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(sonnet-5.5-think-max) = -0.17 [-0.43, -0.02]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(sonnet-5.5-think-max) = 0.18 [-0.35, 1.04]
- stated base rate: ρ(haiku-5.5-think) − ρ(opus-5.5-think) = -0.21 [-0.53, -0.03]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(opus-5.5-think) = -0.20 [-0.46, -0.00]
- stated base rate: ρ(haiku-5.5-think) − ρ(sonnet-5.5-nothink) = -0.22 [-0.66, 0.07]
- base rate + instruction to use it: ρ(haiku-5.5-think) − ρ(sonnet-5.5-nothink) = -0.38 [-0.77, -0.19]
- stated payoffs: ρ(haiku-5.5-think) − ρ(sonnet-5.5-nothink) = -0.11 [-0.35, 0.01]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-think) − ρ(sonnet-5.5-nothink) = -0.05 [-0.30, 0.21]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(sonnet-5.5-nothink) = -0.31 [-0.65, -0.01]
- stated base rate: ρ(haiku-5.5-think) − ρ(sonnet-5.5-think) = -0.13 [-0.48, 0.16]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(sonnet-5.5-think) = -0.15 [-0.46, 0.14]
- stated base rate: ρ(haiku-5.5-think) − ρ(sonnet-5.5-think-max) = -0.21 [-0.65, 0.09]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(sonnet-5.5-think-max) = -0.24 [-0.60, 0.07]
- stated base rate: ρ(opus-5.5-think) − ρ(sonnet-5.5-nothink) = -0.01 [-0.28, 0.24]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(sonnet-5.5-nothink) = -0.10 [-0.34, 0.10]
- stated base rate: ρ(opus-5.5-think) − ρ(sonnet-5.5-think) = 0.08 [-0.17, 0.34]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(sonnet-5.5-think) = 0.06 [-0.18, 0.28]
- stated base rate: ρ(opus-5.5-think) − ρ(sonnet-5.5-think-max) = 0.00 [-0.28, 0.25]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(sonnet-5.5-think-max) = -0.04 [-0.26, 0.17]
- stated base rate: ρ(sonnet-5.5-nothink) − ρ(sonnet-5.5-think) = 0.10 [-0.09, 0.31]
- Bayes check: ρ_Bayes(sonnet-5.5-nothink) − ρ_Bayes(sonnet-5.5-think) = 0.16 [-0.07, 0.39]
- stated base rate: ρ(sonnet-5.5-nothink) − ρ(sonnet-5.5-think-max) = 0.01 [-0.12, 0.18]
- Bayes check: ρ_Bayes(sonnet-5.5-nothink) − ρ_Bayes(sonnet-5.5-think-max) = 0.07 [-0.09, 0.24]
- stated base rate: ρ(sonnet-5.5-think) − ρ(sonnet-5.5-think-max) = -0.08 [-0.32, 0.14]
- Bayes check: ρ_Bayes(sonnet-5.5-think) − ρ_Bayes(sonnet-5.5-think-max) = -0.09 [-0.34, 0.17]
