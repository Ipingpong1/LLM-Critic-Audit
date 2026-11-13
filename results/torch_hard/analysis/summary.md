### gemma4:12b-nothink-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.88 | 0.20 | 1.99 [1.61, 2.43] | -0.16 [-0.39, 0.04] | 0.00 [0.00, 0.00] | – | 0.92 [0.88, 0.95] |
| br10 | 0.10 | 100 / 100 | 0 | 0.86 | 0.19 | 1.93 [1.55, 2.39] | -0.10 [-0.31, 0.11] | 0.06 [-0.08, 0.21] | 1.09 | 0.92 [0.88, 0.95] |
| br50 | 0.50 | 100 / 100 | 0 | 0.87 | 0.18 | 2.01 [1.63, 2.47] | -0.10 [-0.32, 0.10] | 0.06 [-0.10, 0.22] | 0.00 | 0.92 [0.88, 0.96] |
| br90 | 0.90 | 100 / 100 | 0 | 0.88 | 0.23 | 1.89 [1.51, 2.35] | -0.21 [-0.43, -0.00] | -0.05 [-0.20, 0.10] | -1.09 | 0.92 [0.88, 0.96] |
| br10_use | 0.10 | 100 / 100 | 0 | 0.84 | 0.17 | 1.92 [1.55, 2.36] | -0.02 [-0.23, 0.18] | 0.14 [0.01, 0.29] | 1.09 | 0.92 [0.88, 0.95] |
| br90_use | 0.90 | 100 / 100 | 0 | 0.87 | 0.24 | 1.81 [1.46, 2.24] | -0.21 [-0.41, -0.00] | -0.04 [-0.21, 0.13] | -1.09 | 0.92 [0.88, 0.95] |
| pay_fa9 | 0.10 | 100 / 100 | 0 | 0.90 | 0.21 | 2.06 [1.66, 2.51] | -0.23 [-0.47, -0.02] | -0.07 [-0.23, 0.08] | 1.09 | 0.92 [0.87, 0.95] |
| pay_miss9 | 0.90 | 100 / 100 | 0 | 0.90 | 0.21 | 2.06 [1.67, 2.51] | -0.23 [-0.47, -0.02] | -0.07 [-0.23, 0.09] | -1.09 | 0.92 [0.88, 0.96] |
| presuppose | – | 100 / 100 | 0 | 0.93 | 0.33 | 1.88 [1.48, 2.42] | -0.50 [-0.75, -0.30] | -0.34 [-0.52, -0.20] | – | 0.92 [0.88, 0.95] |
| lenient | – | 100 / 100 | 0 | 0.86 | 0.16 | 2.05 [1.66, 2.51] | -0.04 [-0.26, 0.17] | 0.12 [-0.03, 0.28] | – | 0.92 [0.88, 0.96] |
| lab_neutral | – | 100 / 100 | 0 | 0.89 | 0.31 | 1.70 [1.32, 2.14] | -0.36 [-0.58, -0.16] | -0.20 [-0.34, -0.06] | – | 0.91 [0.87, 0.95] |
| lab_br10 | 0.10 | 100 / 100 | 0 | 0.88 | 0.24 | 1.85 [1.46, 2.32] | -0.23 [-0.45, -0.02] | -0.07 [-0.21, 0.08] | 1.09 | 0.91 [0.87, 0.95] |
| lab_br90 | 0.90 | 100 / 100 | 0 | 0.92 | 0.33 | 1.81 [1.41, 2.30] | -0.47 [-0.71, -0.27] | -0.31 [-0.48, -0.17] | -1.09 | 0.91 [0.87, 0.95] |

- **Prior-use ratio ρ = 0.05 [0.01, 0.12]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.11 [0.02, 0.23]; ideal = ln 81 / d′(br50) = 2.18.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.09 [0.04, 0.15]**; minus base-rate ρ = 0.03 [-0.03, 0.09] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **0.00 [-0.03, 0.03]**; minus base-rate ρ = -0.05 [-0.12, -0.00] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.11 [0.06, 0.19]**; minus base-rate ρ = 0.06 [-0.01, 0.14] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.06 [-0.10, 0.22].
- **Bayes check** (own stated confidence at 50% as the posterior; 200 items, 0% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 0 of 105 flags, the critic dropped 0 of those (+1 others); told 90%, a Bayesian adds 0 of 95 passes as flags, the critic added 0 (+7 others); 2 changes against the stated rate. c(10%) − c(90%): observed 0.11 [0.02, 0.23], Bayesian 0.00 [0.00, 0.00]; **ρ_Bayes = – [–, –]** (1 = moves as far as its own confidence implies; 2000 resamples with no predicted shift dropped).
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 6 distinct values.
- z-ROC slope in br50: 0.94 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 23/30; wrong answer 65/70.

### gemma4:12b-think-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 97 / 100 | 3 | 0.92 | 0.04 | 3.13 [2.67, 3.78] | 0.14 [-0.15, 0.44] | 0.00 [0.00, 0.00] | – | 0.94 [0.91, 0.97] |
| br10 | 0.10 | 98 / 99 | 3 | 0.94 | 0.04 | 3.29 [2.81, 4.02] | 0.05 [-0.28, 0.37] | -0.08 [-0.31, 0.11] | 0.69 | 0.96 [0.93, 0.98] |
| br50 | 0.50 | 96 / 100 | 4 | 0.95 | 0.06 | 3.20 [2.73, 3.97] | -0.08 [-0.39, 0.20] | -0.22 [-0.54, 0.03] | 0.00 | 0.96 [0.93, 0.98] |
| br90 | 0.90 | 97 / 100 | 3 | 0.92 | 0.08 | 2.81 [2.40, 3.40] | -0.03 [-0.30, 0.23] | -0.16 [-0.43, 0.07] | -0.69 | 0.95 [0.92, 0.97] |
| br10_use | 0.10 | 97 / 99 | 4 | 0.93 | 0.04 | 3.32 [2.82, 4.12] | 0.15 [-0.14, 0.49] | 0.02 [-0.19, 0.26] | 0.69 | 0.96 [0.93, 0.98] |
| br90_use | 0.90 | 97 / 100 | 3 | 0.93 | 0.05 | 3.11 [2.67, 3.77] | 0.05 [-0.24, 0.34] | -0.09 [-0.40, 0.23] | -0.69 | 0.95 [0.92, 0.98] |
| pay_fa9 | 0.10 | 96 / 100 | 4 | 0.92 | 0.05 | 3.03 [2.58, 3.66] | 0.09 [-0.19, 0.38] | -0.05 [-0.24, 0.12] | 0.69 | 0.94 [0.91, 0.97] |
| pay_miss9 | 0.90 | 100 / 100 | 0 | 0.95 | 0.05 | 3.21 [2.76, 3.87] | 0.00 [-0.29, 0.29] | -0.14 [-0.46, 0.17] | -0.69 | 0.96 [0.93, 0.98] |
| presuppose | – | 97 / 100 | 3 | 0.95 | 0.12 | 2.84 [2.41, 3.49] | -0.26 [-0.58, -0.02] | -0.40 [-0.74, -0.14] | – | 0.93 [0.90, 0.96] |
| lenient | – | 99 / 100 | 1 | 0.94 | 0.04 | 3.21 [2.76, 3.96] | 0.09 [-0.19, 0.40] | -0.04 [-0.32, 0.23] | – | 0.95 [0.92, 0.97] |
| lab_neutral | – | 97 / 100 | 3 | 0.96 | 0.07 | 3.25 [2.79, 4.01] | -0.18 [-0.56, 0.11] | -0.31 [-0.68, -0.07] | – | 0.96 [0.94, 0.98] |
| lab_br10 | 0.10 | 98 / 99 | 3 | 0.94 | 0.04 | 3.29 [2.81, 3.99] | 0.05 [-0.27, 0.36] | -0.08 [-0.33, 0.14] | 0.69 | 0.96 [0.94, 0.99] |
| lab_br90 | 0.90 | 99 / 100 | 1 | 0.96 | 0.07 | 3.26 [2.78, 4.02] | -0.18 [-0.57, 0.11] | -0.32 [-0.65, -0.08] | -0.69 | 0.97 [0.95, 0.99] |

- **Prior-use ratio ρ = 0.06 [-0.14, 0.29]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.08 [-0.19, 0.36]; ideal = ln 81 / d′(br50) = 1.37.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.08 [-0.13, 0.32]**; minus base-rate ρ = 0.02 [-0.26, 0.30] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **0.07 [-0.13, 0.30]**; minus base-rate ρ = 0.01 [-0.26, 0.26] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.17 [-0.01, 0.44]**; minus base-rate ρ = 0.12 [-0.16, 0.43] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = -0.22 [-0.54, 0.03].
- **Bayes check** (own stated confidence at 50% as the posterior; 194 items, 4% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 7 of 97 flags, the critic dropped 2 of those (+3 others); told 90%, a Bayesian adds 0 of 97 passes as flags, the critic added 0 (+3 others); 6 changes against the stated rate. c(10%) − c(90%): observed 0.08 [-0.19, 0.36], Bayesian 0.28 [0.11, 0.56]; **ρ_Bayes = 0.29 [-0.86, 1.66]** (1 = moves as far as its own confidence implies; 1 resamples with no predicted shift dropped).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 8 distinct values.
- z-ROC slope in br50: 1.89 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 22/29; wrong answer 68/68.

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

### qwen3.5:4b-nothink-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.89 | 0.48 | 1.26 [0.89, 1.71] | -0.58 [-0.81, -0.40] | 0.00 [0.00, 0.00] | – | 0.85 [0.79, 0.90] |
| br10 | 0.10 | 99 / 100 | 1 | 0.86 | 0.34 | 1.51 [1.15, 1.94] | -0.35 [-0.55, -0.16] | 0.23 [0.05, 0.43] | 1.56 | 0.85 [0.79, 0.89] |
| br50 | 0.50 | 99 / 100 | 1 | 0.86 | 0.38 | 1.41 [1.04, 1.84] | -0.40 [-0.60, -0.22] | 0.18 [-0.01, 0.38] | 0.00 | 0.84 [0.79, 0.89] |
| br90 | 0.90 | 99 / 100 | 1 | 0.94 | 0.61 | 1.24 [0.84, 1.77] | -0.90 [-1.17, -0.70] | -0.32 [-0.55, -0.13] | -1.56 | 0.84 [0.78, 0.89] |
| br10_use | 0.10 | 100 / 100 | 0 | 0.87 | 0.40 | 1.36 [0.99, 1.77] | -0.43 [-0.65, -0.23] | 0.15 [-0.06, 0.37] | 1.56 | 0.85 [0.79, 0.90] |
| br90_use | 0.90 | 100 / 100 | 0 | 0.94 | 0.52 | 1.47 [1.09, 1.99] | -0.78 [-1.05, -0.58] | -0.21 [-0.44, -0.01] | -1.56 | 0.84 [0.78, 0.89] |
| pay_fa9 | 0.10 | 100 / 100 | 0 | 0.83 | 0.41 | 1.17 [0.83, 1.57] | -0.36 [-0.55, -0.18] | 0.22 [0.04, 0.42] | 1.56 | 0.85 [0.79, 0.90] |
| pay_miss9 | 0.90 | 100 / 100 | 0 | 0.86 | 0.42 | 1.26 [0.90, 1.68] | -0.43 [-0.64, -0.25] | 0.15 [-0.06, 0.36] | -1.56 | 0.85 [0.80, 0.90] |
| presuppose | – | 100 / 100 | 0 | 0.95 | 0.65 | 1.22 [0.82, 1.82] | -0.99 [-1.29, -0.78] | -0.41 [-0.69, -0.19] | – | 0.84 [0.78, 0.89] |
| lenient | – | 100 / 100 | 0 | 0.84 | 0.32 | 1.44 [1.09, 1.84] | -0.26 [-0.46, -0.07] | 0.32 [0.11, 0.54] | – | 0.85 [0.80, 0.90] |
| lab_neutral | – | 100 / 100 | 0 | 0.93 | 0.70 | 0.93 [0.55, 1.42] | -0.98 [-1.24, -0.79] | -0.40 [-0.61, -0.22] | – | 0.85 [0.79, 0.90] |
| lab_br10 | 0.10 | 100 / 100 | 0 | 0.92 | 0.56 | 1.23 [0.83, 1.68] | -0.76 [-1.01, -0.57] | -0.19 [-0.41, 0.02] | 1.56 | 0.85 [0.79, 0.90] |
| lab_br90 | 0.90 | 100 / 100 | 0 | 0.99 | 0.76 | 1.48 [0.99, 2.09] | -1.44 [-1.74, -1.21] | -0.86 [-1.20, -0.62] | -1.56 | 0.84 [0.78, 0.89] |

- **Prior-use ratio ρ = 0.18 [0.11, 0.28]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.55 [0.38, 0.78]; ideal = ln 81 / d′(br50) = 3.13.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.11 [0.06, 0.20]**; minus base-rate ρ = -0.06 [-0.15, 0.01] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **0.02 [0.00, 0.06]**; minus base-rate ρ = -0.15 [-0.26, -0.09] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.22 [0.13, 0.34]**; minus base-rate ρ = 0.04 [-0.06, 0.15] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.18 [-0.01, 0.38].
- **Bayes check** (own stated confidence at 50% as the posterior; 199 items, 7% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 13 of 124 flags, the critic dropped 1 of those (+3 others); told 90%, a Bayesian adds 0 of 75 passes as flags, the critic added 0 (+30 others); 0 changes against the stated rate. c(10%) − c(90%): observed 0.55 [0.38, 0.78], Bayesian 0.22 [0.12, 0.35]; **ρ_Bayes = 2.49 [1.34, 5.29]** (1 = moves as far as its own confidence implies).
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 21 distinct values.
- z-ROC slope in br50: 0.95 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 27/30; wrong answer 62/70.

### qwen3.5:4b-think-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.97 | 0.16 | 2.80 [2.37, 3.56] | -0.42 [-0.80, -0.18] | 0.00 [0.00, 0.00] | – | 0.93 [0.89, 0.96] |
| br10 | 0.10 | 100 / 100 | 0 | 0.95 | 0.11 | 2.81 [2.40, 3.43] | -0.20 [-0.49, 0.04] | 0.22 [-0.03, 0.53] | 0.81 | 0.93 [0.89, 0.97] |
| br50 | 0.50 | 100 / 100 | 0 | 0.97 | 0.18 | 2.72 [2.28, 3.45] | -0.46 [-0.86, -0.22] | -0.04 [-0.29, 0.23] | 0.00 | 0.93 [0.89, 0.96] |
| br90 | 0.90 | 100 / 100 | 0 | 0.99 | 0.27 | 2.78 [2.33, 3.41] | -0.78 [-1.09, -0.54] | -0.37 [-0.66, -0.13] | -0.81 | 0.92 [0.87, 0.95] |
| br10_use | 0.10 | 100 / 100 | 0 | 0.97 | 0.11 | 3.02 [2.58, 3.78] | -0.31 [-0.69, -0.05] | 0.11 [-0.13, 0.38] | 0.81 | 0.95 [0.91, 0.97] |
| br90_use | 0.90 | 100 / 100 | 0 | 0.98 | 0.20 | 2.80 [2.34, 3.52] | -0.57 [-0.94, -0.32] | -0.15 [-0.39, 0.02] | -0.81 | 0.95 [0.91, 0.98] |
| pay_fa9 | 0.10 | 100 / 100 | 0 | 0.97 | 0.16 | 2.80 [2.35, 3.52] | -0.42 [-0.80, -0.17] | 0.00 [-0.25, 0.26] | 0.81 | 0.92 [0.88, 0.96] |
| pay_miss9 | 0.90 | 100 / 100 | 0 | 0.96 | 0.13 | 2.81 [2.39, 3.49] | -0.30 [-0.62, -0.04] | 0.12 [-0.13, 0.42] | -0.81 | 0.94 [0.91, 0.97] |
| presuppose | – | 100 / 100 | 0 | 0.99 | 0.35 | 2.56 [2.09, 3.16] | -0.90 [-1.20, -0.66] | -0.48 [-0.78, -0.23] | – | 0.85 [0.80, 0.90] |
| lenient | – | 100 / 100 | 0 | 0.97 | 0.08 | 3.19 [2.76, 3.99] | -0.22 [-0.60, 0.06] | 0.20 [-0.04, 0.49] | – | 0.97 [0.94, 0.99] |
| lab_neutral | – | 100 / 100 | 0 | 0.99 | 0.17 | 3.12 [2.63, 3.79] | -0.62 [-0.92, -0.38] | -0.20 [-0.49, 0.04] | – | 0.94 [0.91, 0.97] |
| lab_br10 | 0.10 | 100 / 100 | 0 | 0.97 | 0.13 | 2.93 [2.47, 3.69] | -0.35 [-0.74, -0.10] | 0.06 [-0.18, 0.33] | 0.81 | 0.95 [0.92, 0.98] |
| lab_br90 | 0.90 | 100 / 100 | 0 | 0.98 | 0.33 | 2.40 [1.95, 3.13] | -0.76 [-1.13, -0.54] | -0.35 [-0.68, -0.04] | -0.81 | 0.91 [0.87, 0.95] |

- **Prior-use ratio ρ = 0.36 [0.20, 0.60]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.59 [0.32, 0.92]; ideal = ln 81 / d′(br50) = 1.62.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.16 [0.05, 0.36]**; minus base-rate ρ = -0.20 [-0.44, 0.01] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **-0.08 [-0.23, 0.01]**; minus base-rate ρ = -0.44 [-0.75, -0.25] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.25 [0.06, 0.47]**; minus base-rate ρ = -0.11 [-0.39, 0.05] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = -0.04 [-0.29, 0.23].
- **Bayes check** (own stated confidence at 50% as the posterior; 200 items, 6% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 11 of 115 flags, the critic dropped 5 of those (+7 others); told 90%, a Bayesian adds 0 of 85 passes as flags, the critic added 0 (+14 others); 6 changes against the stated rate. c(10%) − c(90%): observed 0.59 [0.32, 0.92], Bayesian 0.35 [0.17, 0.66]; **ρ_Bayes = 1.66 [0.73, 3.81]** (1 = moves as far as its own confidence implies).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 16 distinct values.
- z-ROC slope in br50: 2.33 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 28/30; wrong answer 69/70.

### qwen3.5:9b-nothink-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.86 | 0.35 | 1.45 [1.09, 1.87] | -0.34 [-0.57, -0.16] | 0.00 [0.00, 0.00] | – | 0.88 [0.82, 0.92] |
| br10 | 0.10 | 100 / 100 | 0 | 0.87 | 0.34 | 1.52 [1.15, 1.95] | -0.35 [-0.56, -0.16] | -0.01 [-0.20, 0.18] | 1.34 | 0.88 [0.83, 0.92] |
| br50 | 0.50 | 100 / 100 | 0 | 0.90 | 0.35 | 1.64 [1.27, 2.11] | -0.44 [-0.66, -0.24] | -0.10 [-0.30, 0.09] | 0.00 | 0.88 [0.83, 0.92] |
| br90 | 0.90 | 100 / 100 | 0 | 0.92 | 0.41 | 1.60 [1.23, 2.08] | -0.58 [-0.82, -0.38] | -0.23 [-0.45, -0.05] | -1.34 | 0.87 [0.82, 0.92] |
| br10_use | 0.10 | 100 / 100 | 0 | 0.87 | 0.33 | 1.54 [1.19, 1.99] | -0.34 [-0.55, -0.15] | 0.00 [-0.17, 0.17] | 1.34 | 0.87 [0.82, 0.91] |
| br90_use | 0.90 | 100 / 100 | 0 | 0.88 | 0.42 | 1.36 [1.01, 1.79] | -0.48 [-0.70, -0.29] | -0.14 [-0.32, 0.05] | -1.34 | 0.87 [0.82, 0.91] |
| pay_fa9 | 0.10 | 100 / 100 | 0 | 0.88 | 0.34 | 1.56 [1.22, 1.98] | -0.37 [-0.60, -0.19] | -0.03 [-0.23, 0.16] | 1.34 | 0.88 [0.84, 0.93] |
| pay_miss9 | 0.90 | 100 / 100 | 0 | 0.87 | 0.34 | 1.52 [1.17, 1.94] | -0.35 [-0.56, -0.16] | -0.01 [-0.21, 0.19] | -1.34 | 0.88 [0.84, 0.92] |
| presuppose | – | 100 / 100 | 0 | 0.90 | 0.46 | 1.36 [0.98, 1.83] | -0.58 [-0.80, -0.39] | -0.24 [-0.43, -0.06] | – | 0.87 [0.82, 0.92] |
| lenient | – | 100 / 100 | 0 | 0.87 | 0.26 | 1.75 [1.38, 2.19] | -0.24 [-0.45, -0.04] | 0.10 [-0.08, 0.29] | – | 0.88 [0.83, 0.92] |
| lab_neutral | – | 100 / 100 | 0 | 0.93 | 0.62 | 1.14 [0.75, 1.68] | -0.87 [-1.13, -0.68] | -0.53 [-0.73, -0.36] | – | 0.87 [0.82, 0.92] |
| lab_br10 | 0.10 | 100 / 100 | 0 | 0.94 | 0.55 | 1.39 [1.01, 1.94] | -0.82 [-1.09, -0.63] | -0.48 [-0.73, -0.27] | 1.34 | 0.87 [0.82, 0.92] |
| lab_br90 | 0.90 | 100 / 100 | 0 | 0.95 | 0.60 | 1.35 [0.93, 1.92] | -0.93 [-1.20, -0.73] | -0.59 [-0.85, -0.37] | -1.34 | 0.87 [0.82, 0.91] |

- **Prior-use ratio ρ = 0.08 [0.04, 0.17]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.23 [0.11, 0.40]; ideal = ln 81 / d′(br50) = 2.68.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.05 [0.02, 0.09]**; minus base-rate ρ = -0.03 [-0.10, 0.01] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **-0.01 [-0.04, 0.01]**; minus base-rate ρ = -0.09 [-0.18, -0.04] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.04 [0.01, 0.09]**; minus base-rate ρ = -0.04 [-0.13, 0.02] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = -0.10 [-0.30, 0.09].
- **Bayes check** (own stated confidence at 50% as the posterior; 200 items, 0% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 1 of 125 flags, the critic dropped 0 of those (+4 others); told 90%, a Bayesian adds 0 of 75 passes as flags, the critic added 0 (+8 others); 0 changes against the stated rate. c(10%) − c(90%): observed 0.23 [0.11, 0.40], Bayesian 0.00 [0.00, 0.00]; **ρ_Bayes = – [–, –]** (1 = moves as far as its own confidence implies; 2000 resamples with no predicted shift dropped).
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 10 distinct values.
- z-ROC slope in br50: 0.88 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 25/30; wrong answer 61/70.

### qwen3.5:9b-think-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 99 / 100 | 1 | 0.98 | 0.17 | 3.11 [2.64, 3.74] | -0.61 [-0.92, -0.36] | 0.00 [0.00, 0.00] | – | 0.94 [0.90, 0.97] |
| br10 | 0.10 | 99 / 100 | 1 | 0.97 | 0.17 | 2.90 [2.45, 3.64] | -0.51 [-0.87, -0.26] | 0.11 [-0.07, 0.38] | 0.72 | 0.97 [0.94, 0.99] |
| br50 | 0.50 | 98 / 100 | 2 | 0.98 | 0.19 | 3.03 [2.57, 3.67] | -0.65 [-0.95, -0.40] | -0.04 [-0.16, 0.08] | 0.00 | 0.95 [0.92, 0.98] |
| br90 | 0.90 | 99 / 100 | 1 | 0.98 | 0.33 | 2.61 [2.14, 3.21] | -0.87 [-1.17, -0.63] | -0.25 [-0.39, -0.14] | -0.72 | 0.90 [0.85, 0.94] |
| br10_use | 0.10 | 99 / 100 | 1 | 0.98 | 0.15 | 3.19 [2.72, 3.84] | -0.57 [-0.89, -0.32] | 0.04 [-0.07, 0.16] | 0.72 | 0.97 [0.94, 0.99] |
| br90_use | 0.90 | 99 / 100 | 1 | 0.98 | 0.28 | 2.75 [2.29, 3.34] | -0.80 [-1.10, -0.55] | -0.18 [-0.32, -0.05] | -0.72 | 0.96 [0.93, 0.98] |
| pay_fa9 | 0.10 | 100 / 99 | 1 | 0.95 | 0.10 | 2.91 [2.48, 3.56] | -0.15 [-0.44, 0.13] | 0.47 [0.21, 0.80] | 0.72 | 0.96 [0.93, 0.98] |
| pay_miss9 | 0.90 | 99 / 100 | 1 | 0.94 | 0.15 | 2.62 [2.20, 3.22] | -0.29 [-0.58, -0.05] | 0.33 [0.07, 0.64] | -0.72 | 0.93 [0.90, 0.97] |
| presuppose | – | 100 / 100 | 0 | 0.95 | 0.18 | 2.51 [2.09, 3.08] | -0.35 [-0.65, -0.13] | 0.26 [-0.01, 0.59] | – | 0.92 [0.87, 0.96] |
| lenient | – | 100 / 100 | 0 | 0.94 | 0.11 | 2.73 [2.32, 3.30] | -0.16 [-0.44, 0.09] | 0.46 [0.22, 0.78] | – | 0.96 [0.93, 0.98] |
| lab_neutral | – | 99 / 100 | 1 | 0.95 | 0.18 | 2.60 [2.17, 3.22] | -0.40 [-0.72, -0.17] | 0.22 [-0.03, 0.52] | – | 0.92 [0.88, 0.96] |
| lab_br10 | 0.10 | 99 / 100 | 1 | 0.97 | 0.21 | 2.76 [2.31, 3.48] | -0.58 [-0.95, -0.34] | 0.03 [-0.17, 0.31] | 0.72 | 0.94 [0.90, 0.97] |
| lab_br90 | 0.90 | 100 / 100 | 0 | 0.99 | 0.32 | 2.64 [2.17, 3.22] | -0.86 [-1.16, -0.62] | -0.24 [-0.36, -0.14] | -0.72 | 0.94 [0.91, 0.97] |

- **Prior-use ratio ρ = 0.25 [0.11, 0.52]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.36 [0.16, 0.66]; ideal = ln 81 / d′(br50) = 1.45.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.15 [0.05, 0.28]**; minus base-rate ρ = -0.09 [-0.34, 0.07] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **0.10 [-0.07, 0.30]**; minus base-rate ρ = -0.15 [-0.41, 0.04] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.19 [0.06, 0.44]**; minus base-rate ρ = -0.06 [-0.17, 0.05] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = -0.04 [-0.16, 0.08].
- **Bayes check** (own stated confidence at 50% as the posterior; 198 items, 4% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 7 of 116 flags, the critic dropped 1 of those (+6 others); told 90%, a Bayesian adds 0 of 82 passes as flags, the critic added 0 (+17 others); 7 changes against the stated rate. c(10%) − c(90%): observed 0.36 [0.16, 0.66], Bayesian 0.14 [0.05, 0.26]; **ρ_Bayes = 2.47 [0.86, 8.32]** (1 = moves as far as its own confidence implies; 2 resamples with no predicted shift dropped).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 13 distinct values.
- z-ROC slope in br50: 1.90 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 29/30; wrong answer 69/69.

### qwen3.5:27b-nothink-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 100 / 100 | 0 | 0.82 | 0.24 | 1.60 [1.24, 2.01] | -0.10 [-0.30, 0.08] | 0.00 [0.00, 0.00] | – | 0.92 [0.88, 0.95] |
| br10 | 0.10 | 100 / 100 | 0 | 0.83 | 0.17 | 1.88 [1.51, 2.34] | 0.00 [-0.21, 0.21] | 0.10 [-0.07, 0.29] | 1.26 | 0.92 [0.88, 0.95] |
| br50 | 0.50 | 100 / 100 | 0 | 0.83 | 0.21 | 1.74 [1.40, 2.18] | -0.07 [-0.28, 0.13] | 0.03 [-0.15, 0.21] | 0.00 | 0.92 [0.89, 0.95] |
| br90 | 0.90 | 100 / 100 | 0 | 0.85 | 0.26 | 1.66 [1.31, 2.08] | -0.19 [-0.41, 0.00] | -0.09 [-0.25, 0.06] | -1.26 | 0.92 [0.88, 0.95] |
| br10_use | 0.10 | 100 / 100 | 0 | 0.85 | 0.21 | 1.82 [1.46, 2.26] | -0.11 [-0.32, 0.10] | -0.01 [-0.20, 0.19] | 1.26 | 0.92 [0.88, 0.95] |
| br90_use | 0.90 | 100 / 100 | 0 | 0.87 | 0.26 | 1.75 [1.38, 2.19] | -0.24 [-0.46, -0.04] | -0.13 [-0.32, 0.05] | -1.26 | 0.92 [0.88, 0.95] |
| pay_fa9 | 0.10 | 100 / 100 | 0 | 0.87 | 0.22 | 1.87 [1.51, 2.35] | -0.17 [-0.40, 0.03] | -0.07 [-0.24, 0.09] | 1.26 | 0.92 [0.87, 0.95] |
| pay_miss9 | 0.90 | 100 / 100 | 0 | 0.87 | 0.21 | 1.91 [1.54, 2.39] | -0.16 [-0.39, 0.04] | -0.05 [-0.22, 0.10] | -1.26 | 0.92 [0.88, 0.95] |
| presuppose | – | 100 / 100 | 0 | 0.86 | 0.18 | 1.97 [1.57, 2.43] | -0.08 [-0.30, 0.12] | 0.02 [-0.14, 0.18] | – | 0.92 [0.89, 0.95] |
| lenient | – | 100 / 100 | 0 | 0.81 | 0.16 | 1.85 [1.49, 2.30] | 0.06 [-0.16, 0.27] | 0.16 [0.00, 0.33] | – | 0.92 [0.88, 0.95] |
| lab_neutral | – | 100 / 100 | 0 | 0.88 | 0.29 | 1.70 [1.32, 2.13] | -0.30 [-0.52, -0.11] | -0.20 [-0.39, -0.02] | – | 0.92 [0.88, 0.95] |
| lab_br10 | 0.10 | 100 / 100 | 0 | 0.88 | 0.32 | 1.62 [1.25, 2.08] | -0.35 [-0.56, -0.14] | -0.24 [-0.44, -0.06] | 1.26 | 0.92 [0.88, 0.95] |
| lab_br90 | 0.90 | 100 / 100 | 0 | 0.94 | 0.36 | 1.87 [1.48, 2.43] | -0.58 [-0.83, -0.37] | -0.48 [-0.70, -0.30] | -1.26 | 0.92 [0.88, 0.95] |

- **Prior-use ratio ρ = 0.08 [0.04, 0.14]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.19 [0.09, 0.32]; ideal = ln 81 / d′(br50) = 2.53.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.05 [0.02, 0.10]**; minus base-rate ρ = -0.03 [-0.10, 0.04] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **-0.01 [-0.02, 0.00]**; minus base-rate ρ = -0.08 [-0.15, -0.04] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.09 [0.04, 0.17]**; minus base-rate ρ = 0.02 [-0.05, 0.09] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.03 [-0.15, 0.21].
- **Bayes check** (own stated confidence at 50% as the posterior; 200 items, 0% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 0 of 104 flags, the critic dropped 0 of those (+5 others); told 90%, a Bayesian adds 0 of 96 passes as flags, the critic added 0 (+7 others); 1 changes against the stated rate. c(10%) − c(90%): observed 0.19 [0.09, 0.32], Bayesian 0.00 [0.00, 0.00]; **ρ_Bayes = – [–, –]** (1 = moves as far as its own confidence implies; 2000 resamples with no predicted shift dropped).
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 13 distinct values.
- z-ROC slope in br50: 0.93 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 23/30; wrong answer 59/70.

### qwen3.5:27b-think-bf16-t1

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 98 / 100 | 2 | 0.97 | 0.16 | 2.94 [2.49, 3.69] | -0.49 [-0.85, -0.22] | 0.00 [0.00, 0.00] | – | 0.94 [0.90, 0.97] |
| br10 | 0.10 | 98 / 100 | 2 | 0.97 | 0.23 | 2.69 [2.23, 3.44] | -0.61 [-0.98, -0.38] | -0.13 [-0.23, -0.05] | 0.84 | 0.95 [0.92, 0.98] |
| br50 | 0.50 | 98 / 100 | 2 | 0.97 | 0.25 | 2.62 [2.17, 3.38] | -0.64 [-1.01, -0.41] | -0.16 [-0.49, 0.15] | 0.00 | 0.94 [0.91, 0.97] |
| br90 | 0.90 | 97 / 99 | 4 | 0.99 | 0.43 | 2.73 [2.49, 2.97] | -1.20 [-1.33, -1.08] | -0.72 [-0.97, -0.35] | -0.84 | 0.93 [0.89, 0.96] |
| br10_use | 0.10 | 99 / 100 | 1 | 0.97 | 0.22 | 2.72 [2.30, 3.45] | -0.60 [-0.95, -0.35] | -0.11 [-0.22, -0.02] | 0.84 | 0.95 [0.92, 0.98] |
| br90_use | 0.90 | 99 / 100 | 1 | 0.98 | 0.45 | 2.29 [1.83, 2.87] | -1.02 [-1.33, -0.79] | -0.54 [-0.85, -0.33] | -0.84 | 0.92 [0.88, 0.95] |
| pay_fa9 | 0.10 | 99 / 100 | 1 | 0.97 | 0.13 | 3.07 [2.60, 3.84] | -0.43 [-0.80, -0.17] | 0.06 [-0.02, 0.16] | 0.84 | 0.96 [0.93, 0.98] |
| pay_miss9 | 0.90 | 100 / 100 | 0 | 0.98 | 0.22 | 2.73 [2.30, 3.45] | -0.60 [-0.97, -0.36] | -0.11 [-0.43, 0.19] | -0.84 | 0.95 [0.91, 0.97] |
| presuppose | – | 99 / 98 | 3 | 0.99 | 0.58 | 2.37 [2.11, 2.61] | -1.39 [-1.52, -1.27] | -0.90 [-1.16, -0.52] | – | 0.90 [0.86, 0.94] |
| lenient | – | 100 / 100 | 0 | 0.96 | 0.12 | 2.86 [2.42, 3.56] | -0.27 [-0.60, -0.00] | 0.22 [0.03, 0.50] | – | 0.97 [0.95, 0.99] |
| lab_neutral | – | 99 / 100 | 1 | 0.97 | 0.23 | 2.69 [2.25, 3.44] | -0.61 [-0.98, -0.36] | -0.13 [-0.24, -0.05] | – | 0.93 [0.89, 0.96] |
| lab_br10 | 0.10 | 99 / 100 | 1 | 0.97 | 0.18 | 2.86 [2.42, 3.60] | -0.53 [-0.89, -0.27] | -0.04 [-0.17, 0.08] | 0.84 | 0.96 [0.94, 0.99] |
| lab_br90 | 0.90 | 99 / 100 | 1 | 0.99 | 0.45 | 2.70 [2.45, 2.96] | -1.23 [-1.35, -1.10] | -0.74 [-0.99, -0.37] | -0.84 | 0.95 [0.92, 0.98] |

- **Prior-use ratio ρ = 0.35 [0.15, 0.51]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.59 [0.23, 0.81]; ideal = ln 81 / d′(br50) = 1.68.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.25 [0.14, 0.50]**; minus base-rate ρ = -0.10 [-0.22, 0.09] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **0.10 [-0.09, 0.33]**; minus base-rate ρ = -0.25 [-0.40, -0.03] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.42 [0.22, 0.59]**; minus base-rate ρ = 0.06 [-0.03, 0.17] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = -0.16 [-0.49, 0.15].
- **Bayes check** (own stated confidence at 50% as the posterior; 195 items, 4% with 10 < p_error ≤ 90): told 10%, a Bayesian drops 8 of 120 flags, the critic dropped 3 of those (+3 others); told 90%, a Bayesian adds 0 of 75 passes as flags, the critic added 0 (+19 others); 3 changes against the stated rate. c(10%) − c(90%): observed 0.59 [0.22, 0.81], Bayesian 0.28 [0.06, 0.58]; **ρ_Bayes = 2.10 [0.63, 7.31]** (1 = moves as far as its own confidence implies).
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 13 distinct values.
- z-ROC slope in br50: 0.56 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 27/29; wrong answer 69/69.

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

- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(gemma4:12b-think-bf16-t1) = -0.00 [-0.24, 0.21]
- base rate + instruction to use it: ρ(gemma4:12b-nothink-bf16-t1) − ρ(gemma4:12b-think-bf16-t1) = 0.01 [-0.23, 0.23]
- stated payoffs: ρ(gemma4:12b-nothink-bf16-t1) − ρ(gemma4:12b-think-bf16-t1) = -0.07 [-0.30, 0.14]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-nothink-bf16-t1) − ρ(gemma4:12b-think-bf16-t1) = -0.06 [-0.34, 0.15]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(gemma4:12b-think-bf16-t1) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(haiku-5.5-nothink) = 0.02 [-0.05, 0.08]
- base rate + instruction to use it: ρ(gemma4:12b-nothink-bf16-t1) − ρ(haiku-5.5-nothink) = 0.11 [0.04, 0.23]
- stated payoffs: ρ(gemma4:12b-nothink-bf16-t1) − ρ(haiku-5.5-nothink) = -0.04 [-0.16, 0.05]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-nothink-bf16-t1) − ρ(haiku-5.5-nothink) = 0.16 [0.09, 0.27]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(haiku-5.5-nothink) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(haiku-5.5-think) = 0.05 [-0.19, 0.30]
- base rate + instruction to use it: ρ(gemma4:12b-nothink-bf16-t1) − ρ(haiku-5.5-think) = 0.24 [0.11, 0.51]
- stated payoffs: ρ(gemma4:12b-nothink-bf16-t1) − ρ(haiku-5.5-think) = 0.08 [-0.02, 0.28]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-nothink-bf16-t1) − ρ(haiku-5.5-think) = -0.00 [-0.22, 0.13]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(haiku-5.5-think) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(opus-5.5-think) = -0.15 [-0.38, -0.00]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(opus-5.5-think) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.12 [-0.24, -0.04]
- base rate + instruction to use it: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.03 [-0.12, 0.05]
- stated payoffs: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.02 [-0.07, 0.02]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.10 [-0.24, -0.00]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.31 [-0.55, -0.15]
- base rate + instruction to use it: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.08 [-0.29, 0.05]
- stated payoffs: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = 0.08 [-0.02, 0.23]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.14 [-0.36, 0.05]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:4b-think-bf16-t1) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.03 [-0.12, 0.04]
- base rate + instruction to use it: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.03 [-0.03, 0.10]
- stated payoffs: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.01 [-0.03, 0.05]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.07 [-0.00, 0.17]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.19 [-0.47, -0.04]
- base rate + instruction to use it: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.07 [-0.20, 0.04]
- stated payoffs: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.10 [-0.31, 0.08]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.08 [-0.33, 0.07]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:9b-think-bf16-t1) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.02 [-0.10, 0.05]
- base rate + instruction to use it: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.04 [-0.03, 0.11]
- stated payoffs: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.01 [-0.03, 0.04]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.02 [-0.08, 0.12]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.30 [-0.46, -0.09]
- base rate + instruction to use it: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.17 [-0.41, -0.04]
- stated payoffs: ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.10 [-0.33, 0.09]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.31 [-0.48, -0.09]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:27b-think-bf16-t1) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.17 [-0.41, -0.02]
- base rate + instruction to use it: ρ(gemma4:12b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.13 [-0.35, -0.00]
- stated payoffs: ρ(gemma4:12b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.04 [-0.14, 0.04]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.05 [-0.24, 0.09]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-nothink) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(sonnet-5.5-think) = -0.07 [-0.27, 0.07]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-think) = – [–, –]
- stated base rate: ρ(gemma4:12b-nothink-bf16-t1) − ρ(sonnet-5.5-think-max) = -0.15 [-0.42, -0.01]
- Bayes check: ρ_Bayes(gemma4:12b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-think-max) = – [–, –]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(haiku-5.5-nothink) = 0.02 [-0.20, 0.25]
- base rate + instruction to use it: ρ(gemma4:12b-think-bf16-t1) − ρ(haiku-5.5-nothink) = 0.10 [-0.12, 0.36]
- stated payoffs: ρ(gemma4:12b-think-bf16-t1) − ρ(haiku-5.5-nothink) = 0.03 [-0.20, 0.25]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-think-bf16-t1) − ρ(haiku-5.5-nothink) = 0.22 [0.03, 0.51]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(haiku-5.5-nothink) = -0.14 [-1.44, 1.20]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(haiku-5.5-think) = 0.06 [-0.26, 0.41]
- base rate + instruction to use it: ρ(gemma4:12b-think-bf16-t1) − ρ(haiku-5.5-think) = 0.23 [-0.01, 0.61]
- stated payoffs: ρ(gemma4:12b-think-bf16-t1) − ρ(haiku-5.5-think) = 0.14 [-0.07, 0.42]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-think-bf16-t1) − ρ(haiku-5.5-think) = 0.06 [-0.24, 0.35]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(haiku-5.5-think) = 0.29 [-0.94, 1.68]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(opus-5.5-think) = -0.15 [-0.47, 0.12]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(opus-5.5-think) = 0.08 [-1.10, 1.42]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.12 [-0.36, 0.12]
- base rate + instruction to use it: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.04 [-0.26, 0.21]
- stated payoffs: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = 0.04 [-0.16, 0.28]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.04 [-0.28, 0.23]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) = -2.21 [-5.22, -0.34]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.31 [-0.67, -0.04]
- base rate + instruction to use it: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.09 [-0.35, 0.19]
- stated payoffs: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = 0.14 [-0.07, 0.42]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.08 [-0.39, 0.25]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(qwen3.5:4b-think-bf16-t1) = -1.37 [-3.88, 0.17]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.03 [-0.24, 0.21]
- base rate + instruction to use it: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.02 [-0.19, 0.26]
- stated payoffs: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.07 [-0.13, 0.31]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.13 [-0.06, 0.40]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.19 [-0.51, 0.07]
- base rate + instruction to use it: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.08 [-0.32, 0.17]
- stated payoffs: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.03 [-0.35, 0.29]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.02 [-0.34, 0.29]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(qwen3.5:9b-think-bf16-t1) = -2.19 [-8.30, -0.20]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.02 [-0.23, 0.21]
- base rate + instruction to use it: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.03 [-0.19, 0.27]
- stated payoffs: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.07 [-0.13, 0.31]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.08 [-0.13, 0.35]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.30 [-0.51, 0.02]
- base rate + instruction to use it: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.18 [-0.45, 0.06]
- stated payoffs: ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.04 [-0.35, 0.29]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.25 [-0.51, 0.15]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(qwen3.5:27b-think-bf16-t1) = -1.81 [-6.97, 0.17]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.17 [-0.43, 0.06]
- base rate + instruction to use it: ρ(gemma4:12b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.14 [-0.41, 0.10]
- stated payoffs: ρ(gemma4:12b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.03 [-0.21, 0.29]
- base rate, verdict words "flawed"/"sound": ρ(gemma4:12b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.01 [-0.26, 0.31]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-nothink) = -0.02 [-1.15, 1.35]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(sonnet-5.5-think) = -0.07 [-0.36, 0.18]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-think) = 0.14 [-1.07, 1.52]
- stated base rate: ρ(gemma4:12b-think-bf16-t1) − ρ(sonnet-5.5-think-max) = -0.15 [-0.45, 0.12]
- Bayes check: ρ_Bayes(gemma4:12b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-think-max) = 0.04 [-1.10, 1.36]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(haiku-5.5-think) = 0.04 [-0.20, 0.29]
- base rate + instruction to use it: ρ(haiku-5.5-nothink) − ρ(haiku-5.5-think) = 0.13 [0.01, 0.38]
- stated payoffs: ρ(haiku-5.5-nothink) − ρ(haiku-5.5-think) = 0.11 [0.00, 0.33]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-nothink) − ρ(haiku-5.5-think) = -0.17 [-0.41, -0.04]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(haiku-5.5-think) = 0.42 [-0.01, 1.19]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(opus-5.5-think) = -0.17 [-0.38, -0.03]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(opus-5.5-think) = 0.22 [-0.23, 1.03]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.14 [-0.24, -0.06]
- base rate + instruction to use it: ρ(haiku-5.5-nothink) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.14 [-0.28, -0.07]
- stated payoffs: ρ(haiku-5.5-nothink) − ρ(qwen3.5:4b-nothink-bf16-t1) = 0.01 [-0.08, 0.13]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-nothink) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.27 [-0.40, -0.19]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) = -2.07 [-4.67, -0.67]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(qwen3.5:4b-think-bf16-t1) = -0.33 [-0.57, -0.17]
- base rate + instruction to use it: ρ(haiku-5.5-nothink) − ρ(qwen3.5:4b-think-bf16-t1) = -0.19 [-0.43, -0.06]
- stated payoffs: ρ(haiku-5.5-nothink) − ρ(qwen3.5:4b-think-bf16-t1) = 0.11 [-0.01, 0.31]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-nothink) − ρ(qwen3.5:4b-think-bf16-t1) = -0.31 [-0.55, -0.12]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(qwen3.5:4b-think-bf16-t1) = -1.23 [-3.30, -0.15]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.05 [-0.13, 0.03]
- base rate + instruction to use it: ρ(haiku-5.5-nothink) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.08 [-0.19, -0.02]
- stated payoffs: ρ(haiku-5.5-nothink) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.05 [-0.04, 0.16]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-nothink) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.09 [-0.19, -0.02]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(qwen3.5:9b-think-bf16-t1) = -0.21 [-0.48, -0.06]
- base rate + instruction to use it: ρ(haiku-5.5-nothink) − ρ(qwen3.5:9b-think-bf16-t1) = -0.18 [-0.36, -0.06]
- stated payoffs: ρ(haiku-5.5-nothink) − ρ(qwen3.5:9b-think-bf16-t1) = -0.06 [-0.28, 0.14]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-nothink) − ρ(qwen3.5:9b-think-bf16-t1) = -0.24 [-0.52, -0.10]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(qwen3.5:9b-think-bf16-t1) = -2.05 [-7.93, -0.29]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.04 [-0.11, 0.04]
- base rate + instruction to use it: ρ(haiku-5.5-nothink) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.07 [-0.19, -0.02]
- stated payoffs: ρ(haiku-5.5-nothink) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.04 [-0.04, 0.16]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-nothink) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.14 [-0.25, -0.08]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(haiku-5.5-nothink) − ρ(qwen3.5:27b-think-bf16-t1) = -0.32 [-0.48, -0.09]
- base rate + instruction to use it: ρ(haiku-5.5-nothink) − ρ(qwen3.5:27b-think-bf16-t1) = -0.28 [-0.56, -0.15]
- stated payoffs: ρ(haiku-5.5-nothink) − ρ(qwen3.5:27b-think-bf16-t1) = -0.07 [-0.30, 0.16]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-nothink) − ρ(qwen3.5:27b-think-bf16-t1) = -0.47 [-0.65, -0.27]
- Bayes check: ρ_Bayes(haiku-5.5-nothink) − ρ_Bayes(qwen3.5:27b-think-bf16-t1) = -1.68 [-7.16, 0.26]
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
- stated base rate: ρ(haiku-5.5-think) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.18 [-0.45, 0.09]
- base rate + instruction to use it: ρ(haiku-5.5-think) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.27 [-0.55, -0.14]
- stated payoffs: ρ(haiku-5.5-think) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.10 [-0.31, -0.01]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-think) − ρ(qwen3.5:4b-nothink-bf16-t1) = -0.10 [-0.29, 0.13]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) = -2.49 [-5.24, -1.32]
- stated base rate: ρ(haiku-5.5-think) − ρ(qwen3.5:4b-think-bf16-t1) = -0.36 [-0.76, -0.15]
- base rate + instruction to use it: ρ(haiku-5.5-think) − ρ(qwen3.5:4b-think-bf16-t1) = -0.32 [-0.72, -0.14]
- stated payoffs: ρ(haiku-5.5-think) − ρ(qwen3.5:4b-think-bf16-t1) = -0.00 [-0.20, 0.16]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-think) − ρ(qwen3.5:4b-think-bf16-t1) = -0.14 [-0.36, 0.08]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(qwen3.5:4b-think-bf16-t1) = -1.66 [-3.78, -0.78]
- stated base rate: ρ(haiku-5.5-think) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.08 [-0.35, 0.18]
- base rate + instruction to use it: ρ(haiku-5.5-think) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.21 [-0.48, -0.08]
- stated payoffs: ρ(haiku-5.5-think) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.07 [-0.27, 0.02]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-think) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.08 [-0.05, 0.31]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(haiku-5.5-think) − ρ(qwen3.5:9b-think-bf16-t1) = -0.25 [-0.65, 0.01]
- base rate + instruction to use it: ρ(haiku-5.5-think) − ρ(qwen3.5:9b-think-bf16-t1) = -0.31 [-0.62, -0.14]
- stated payoffs: ρ(haiku-5.5-think) − ρ(qwen3.5:9b-think-bf16-t1) = -0.17 [-0.49, 0.02]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-think) − ρ(qwen3.5:9b-think-bf16-t1) = -0.07 [-0.35, 0.17]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(qwen3.5:9b-think-bf16-t1) = -2.47 [-8.35, -0.86]
- stated base rate: ρ(haiku-5.5-think) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.08 [-0.34, 0.19]
- base rate + instruction to use it: ρ(haiku-5.5-think) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.21 [-0.48, -0.07]
- stated payoffs: ρ(haiku-5.5-think) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.07 [-0.28, 0.01]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-think) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.02 [-0.13, 0.27]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(haiku-5.5-think) − ρ(qwen3.5:27b-think-bf16-t1) = -0.35 [-0.63, 0.01]
- base rate + instruction to use it: ρ(haiku-5.5-think) − ρ(qwen3.5:27b-think-bf16-t1) = -0.41 [-0.80, -0.23]
- stated payoffs: ρ(haiku-5.5-think) − ρ(qwen3.5:27b-think-bf16-t1) = -0.18 [-0.53, 0.03]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-think) − ρ(qwen3.5:27b-think-bf16-t1) = -0.30 [-0.52, 0.04]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(qwen3.5:27b-think-bf16-t1) = -2.10 [-7.45, -0.54]
- stated base rate: ρ(haiku-5.5-think) − ρ(sonnet-5.5-nothink) = -0.22 [-0.66, 0.07]
- base rate + instruction to use it: ρ(haiku-5.5-think) − ρ(sonnet-5.5-nothink) = -0.38 [-0.77, -0.19]
- stated payoffs: ρ(haiku-5.5-think) − ρ(sonnet-5.5-nothink) = -0.11 [-0.35, 0.01]
- base rate, verdict words "flawed"/"sound": ρ(haiku-5.5-think) − ρ(sonnet-5.5-nothink) = -0.05 [-0.30, 0.21]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(sonnet-5.5-nothink) = -0.31 [-0.65, -0.01]
- stated base rate: ρ(haiku-5.5-think) − ρ(sonnet-5.5-think) = -0.13 [-0.48, 0.16]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(sonnet-5.5-think) = -0.15 [-0.46, 0.14]
- stated base rate: ρ(haiku-5.5-think) − ρ(sonnet-5.5-think-max) = -0.21 [-0.65, 0.09]
- Bayes check: ρ_Bayes(haiku-5.5-think) − ρ_Bayes(sonnet-5.5-think-max) = -0.24 [-0.60, 0.07]
- stated base rate: ρ(opus-5.5-think) − ρ(qwen3.5:4b-nothink-bf16-t1) = 0.03 [-0.15, 0.27]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) = -2.29 [-5.01, -1.13]
- stated base rate: ρ(opus-5.5-think) − ρ(qwen3.5:4b-think-bf16-t1) = -0.16 [-0.39, -0.01]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(qwen3.5:4b-think-bf16-t1) = -1.45 [-3.57, -0.63]
- stated base rate: ρ(opus-5.5-think) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.12 [-0.05, 0.36]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(opus-5.5-think) − ρ(qwen3.5:9b-think-bf16-t1) = -0.04 [-0.19, 0.18]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(qwen3.5:9b-think-bf16-t1) = -2.27 [-8.05, -0.71]
- stated base rate: ρ(opus-5.5-think) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.13 [-0.03, 0.37]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(opus-5.5-think) − ρ(qwen3.5:27b-think-bf16-t1) = -0.14 [-0.30, 0.17]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(qwen3.5:27b-think-bf16-t1) = -1.90 [-7.23, -0.38]
- stated base rate: ρ(opus-5.5-think) − ρ(sonnet-5.5-nothink) = -0.01 [-0.28, 0.24]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(sonnet-5.5-nothink) = -0.10 [-0.34, 0.10]
- stated base rate: ρ(opus-5.5-think) − ρ(sonnet-5.5-think) = 0.08 [-0.17, 0.34]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(sonnet-5.5-think) = 0.06 [-0.18, 0.28]
- stated base rate: ρ(opus-5.5-think) − ρ(sonnet-5.5-think-max) = 0.00 [-0.28, 0.25]
- Bayes check: ρ_Bayes(opus-5.5-think) − ρ_Bayes(sonnet-5.5-think-max) = -0.04 [-0.26, 0.17]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.19 [-0.43, -0.01]
- base rate + instruction to use it: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.05 [-0.25, 0.10]
- stated payoffs: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = 0.10 [0.01, 0.26]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:4b-think-bf16-t1) = -0.04 [-0.27, 0.19]
- Bayes check: ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:4b-think-bf16-t1) = 0.83 [-1.46, 3.58]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.09 [0.01, 0.19]
- base rate + instruction to use it: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.06 [-0.00, 0.15]
- stated payoffs: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.03 [0.00, 0.08]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.18 [0.08, 0.31]
- Bayes check: ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.07 [-0.34, 0.10]
- base rate + instruction to use it: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.04 [-0.17, 0.09]
- stated payoffs: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.07 [-0.28, 0.11]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = 0.03 [-0.23, 0.22]
- Bayes check: ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:9b-think-bf16-t1) = 0.02 [-5.64, 2.99]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.10 [0.02, 0.21]
- base rate + instruction to use it: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.06 [-0.00, 0.15]
- stated payoffs: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.03 [0.00, 0.07]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.12 [0.01, 0.25]
- Bayes check: ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.18 [-0.34, 0.04]
- base rate + instruction to use it: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.14 [-0.39, 0.01]
- stated payoffs: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.08 [-0.30, 0.12]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.20 [-0.39, 0.04]
- Bayes check: ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:27b-think-bf16-t1) = 0.39 [-5.11, 3.59]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.05 [-0.28, 0.11]
- base rate + instruction to use it: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.11 [-0.33, 0.06]
- stated payoffs: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.01 [-0.11, 0.07]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.05 [-0.15, 0.23]
- Bayes check: ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-nothink) = 2.19 [1.02, 4.94]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(sonnet-5.5-think) = 0.05 [-0.15, 0.20]
- Bayes check: ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-think) = 2.35 [1.19, 5.11]
- stated base rate: ρ(qwen3.5:4b-nothink-bf16-t1) − ρ(sonnet-5.5-think-max) = -0.03 [-0.29, 0.13]
- Bayes check: ρ_Bayes(qwen3.5:4b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-think-max) = 2.25 [1.08, 4.94]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.28 [0.10, 0.53]
- base rate + instruction to use it: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.11 [-0.01, 0.31]
- stated payoffs: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = -0.07 [-0.22, 0.03]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-nothink-bf16-t1) = 0.22 [0.02, 0.44]
- Bayes check: ρ_Bayes(qwen3.5:4b-think-bf16-t1) − ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = 0.12 [-0.06, 0.36]
- base rate + instruction to use it: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = 0.01 [-0.15, 0.21]
- stated payoffs: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.17 [-0.44, 0.04]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = 0.07 [-0.17, 0.25]
- Bayes check: ρ_Bayes(qwen3.5:4b-think-bf16-t1) − ρ_Bayes(qwen3.5:9b-think-bf16-t1) = -0.81 [-6.34, 1.37]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.29 [0.12, 0.53]
- base rate + instruction to use it: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.11 [-0.01, 0.32]
- stated payoffs: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.07 [-0.23, 0.02]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.16 [-0.04, 0.38]
- Bayes check: ρ_Bayes(qwen3.5:4b-think-bf16-t1) − ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = 0.01 [-0.19, 0.37]
- base rate + instruction to use it: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.09 [-0.38, 0.15]
- stated payoffs: ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.18 [-0.44, 0.04]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.16 [-0.35, 0.12]
- Bayes check: ρ_Bayes(qwen3.5:4b-think-bf16-t1) − ρ_Bayes(qwen3.5:27b-think-bf16-t1) = -0.44 [-6.39, 2.38]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.14 [-0.05, 0.36]
- base rate + instruction to use it: ρ(qwen3.5:4b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.06 [-0.24, 0.12]
- stated payoffs: ρ(qwen3.5:4b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.11 [-0.30, 0.01]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:4b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.09 [-0.15, 0.31]
- Bayes check: ρ_Bayes(qwen3.5:4b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-nothink) = 1.35 [0.41, 3.56]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(sonnet-5.5-think) = 0.24 [0.04, 0.47]
- Bayes check: ρ_Bayes(qwen3.5:4b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-think) = 1.51 [0.57, 3.71]
- stated base rate: ρ(qwen3.5:4b-think-bf16-t1) − ρ(sonnet-5.5-think-max) = 0.16 [-0.07, 0.40]
- Bayes check: ρ_Bayes(qwen3.5:4b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-think-max) = 1.42 [0.49, 3.54]
- stated base rate: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.16 [-0.44, 0.01]
- base rate + instruction to use it: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.10 [-0.23, 0.00]
- stated payoffs: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.11 [-0.32, 0.07]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:9b-think-bf16-t1) = -0.15 [-0.40, -0.01]
- Bayes check: ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:9b-think-bf16-t1) = – [–, –]
- stated base rate: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.01 [-0.05, 0.08]
- base rate + instruction to use it: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.00 [-0.05, 0.05]
- stated payoffs: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.00 [-0.03, 0.02]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = -0.05 [-0.14, 0.02]
- Bayes check: ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.27 [-0.43, -0.04]
- base rate + instruction to use it: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.20 [-0.45, -0.08]
- stated payoffs: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.11 [-0.33, 0.08]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.38 [-0.55, -0.17]
- Bayes check: ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:27b-think-bf16-t1) = – [–, –]
- stated base rate: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.14 [-0.36, 0.00]
- base rate + instruction to use it: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.17 [-0.38, -0.04]
- stated payoffs: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.05 [-0.14, 0.03]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.12 [-0.31, -0.01]
- Bayes check: ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-nothink) = – [–, –]
- stated base rate: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(sonnet-5.5-think) = -0.04 [-0.23, 0.10]
- Bayes check: ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-think) = – [–, –]
- stated base rate: ρ(qwen3.5:9b-nothink-bf16-t1) − ρ(sonnet-5.5-think-max) = -0.12 [-0.38, 0.03]
- Bayes check: ρ_Bayes(qwen3.5:9b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-think-max) = – [–, –]
- stated base rate: ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.17 [0.01, 0.45]
- base rate + instruction to use it: ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.10 [-0.00, 0.23]
- stated payoffs: ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.10 [-0.07, 0.31]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-nothink-bf16-t1) = 0.10 [-0.05, 0.34]
- Bayes check: ρ_Bayes(qwen3.5:9b-think-bf16-t1) − ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) = – [–, –]
- stated base rate: ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.10 [-0.25, 0.13]
- base rate + instruction to use it: ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.10 [-0.33, 0.06]
- stated payoffs: ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.01 [-0.20, 0.20]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:9b-think-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.23 [-0.38, 0.01]
- Bayes check: ρ_Bayes(qwen3.5:9b-think-bf16-t1) − ρ_Bayes(qwen3.5:27b-think-bf16-t1) = 0.37 [-5.28, 6.27]
- stated base rate: ρ(qwen3.5:9b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.03 [-0.20, 0.24]
- base rate + instruction to use it: ρ(qwen3.5:9b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.07 [-0.27, 0.09]
- stated payoffs: ρ(qwen3.5:9b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.06 [-0.12, 0.29]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:9b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.03 [-0.15, 0.24]
- Bayes check: ρ_Bayes(qwen3.5:9b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-nothink) = 2.17 [0.60, 7.97]
- stated base rate: ρ(qwen3.5:9b-think-bf16-t1) − ρ(sonnet-5.5-think) = 0.12 [-0.10, 0.40]
- Bayes check: ρ_Bayes(qwen3.5:9b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-think) = 2.33 [0.72, 8.15]
- stated base rate: ρ(qwen3.5:9b-think-bf16-t1) − ρ(sonnet-5.5-think-max) = 0.04 [-0.19, 0.25]
- Bayes check: ρ_Bayes(qwen3.5:9b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-think-max) = 2.23 [0.64, 8.03]
- stated base rate: ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.28 [-0.44, -0.07]
- base rate + instruction to use it: ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.20 [-0.44, -0.08]
- stated payoffs: ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.11 [-0.34, 0.09]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(qwen3.5:27b-think-bf16-t1) = -0.32 [-0.50, -0.11]
- Bayes check: ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) − ρ_Bayes(qwen3.5:27b-think-bf16-t1) = – [–, –]
- stated base rate: ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.15 [-0.38, 0.00]
- base rate + instruction to use it: ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.17 [-0.38, -0.04]
- stated payoffs: ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.04 [-0.14, 0.03]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(sonnet-5.5-nothink) = -0.07 [-0.26, 0.05]
- Bayes check: ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-nothink) = – [–, –]
- stated base rate: ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(sonnet-5.5-think) = -0.05 [-0.24, 0.08]
- Bayes check: ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-think) = – [–, –]
- stated base rate: ρ(qwen3.5:27b-nothink-bf16-t1) − ρ(sonnet-5.5-think-max) = -0.13 [-0.39, 0.02]
- Bayes check: ρ_Bayes(qwen3.5:27b-nothink-bf16-t1) − ρ_Bayes(sonnet-5.5-think-max) = – [–, –]
- stated base rate: ρ(qwen3.5:27b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.13 [-0.19, 0.30]
- base rate + instruction to use it: ρ(qwen3.5:27b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.03 [-0.17, 0.26]
- stated payoffs: ρ(qwen3.5:27b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.07 [-0.15, 0.30]
- base rate, verdict words "flawed"/"sound": ρ(qwen3.5:27b-think-bf16-t1) − ρ(sonnet-5.5-nothink) = 0.25 [0.00, 0.41]
- Bayes check: ρ_Bayes(qwen3.5:27b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-nothink) = 1.79 [0.38, 7.04]
- stated base rate: ρ(qwen3.5:27b-think-bf16-t1) − ρ(sonnet-5.5-think) = 0.23 [-0.08, 0.43]
- Bayes check: ρ_Bayes(qwen3.5:27b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-think) = 1.95 [0.48, 7.16]
- stated base rate: ρ(qwen3.5:27b-think-bf16-t1) − ρ(sonnet-5.5-think-max) = 0.15 [-0.18, 0.31]
- Bayes check: ρ_Bayes(qwen3.5:27b-think-bf16-t1) − ρ_Bayes(sonnet-5.5-think-max) = 1.86 [0.44, 7.21]
- stated base rate: ρ(sonnet-5.5-nothink) − ρ(sonnet-5.5-think) = 0.10 [-0.09, 0.31]
- Bayes check: ρ_Bayes(sonnet-5.5-nothink) − ρ_Bayes(sonnet-5.5-think) = 0.16 [-0.07, 0.39]
- stated base rate: ρ(sonnet-5.5-nothink) − ρ(sonnet-5.5-think-max) = 0.01 [-0.12, 0.18]
- Bayes check: ρ_Bayes(sonnet-5.5-nothink) − ρ_Bayes(sonnet-5.5-think-max) = 0.07 [-0.09, 0.24]
- stated base rate: ρ(sonnet-5.5-think) − ρ(sonnet-5.5-think-max) = -0.08 [-0.32, 0.14]
- Bayes check: ρ_Bayes(sonnet-5.5-think) − ρ_Bayes(sonnet-5.5-think-max) = -0.09 [-0.34, 0.17]
