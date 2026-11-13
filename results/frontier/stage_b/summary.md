### sonnet-5.5-nothink

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | – | 0.97 [0.93, 1.00] |
| br10 | 0.10 | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | 0.93 | 0.97 [0.93, 1.00] |
| br50 | 0.50 | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | 0.00 | 0.96 [0.90, 1.00] |
| br90 | 0.90 | 19 / 20 | 1 | 0.93 | 0.12 | 2.62 [1.90, 3.94] | -0.13 [-0.59, 0.40] | -0.13 [-0.49, 0.03] | -0.93 | 0.98 [0.95, 1.00] |
| br10_use | 0.10 | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | 0.93 | 0.96 [0.90, 1.00] |
| br90_use | 0.90 | 20 / 20 | 0 | 0.93 | 0.12 | 2.64 [1.93, 3.96] | -0.14 [-0.59, 0.40] | -0.14 [-0.51, 0.00] | -0.93 | 0.98 [0.93, 1.00] |
| pay_fa9 | 0.10 | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | 0.93 | 0.96 [0.91, 1.00] |
| pay_miss9 | 0.90 | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | -0.93 | 0.96 [0.91, 1.00] |
| presuppose | – | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | – | 0.98 [0.93, 1.00] |
| lenient | – | 20 / 20 | 0 | 0.88 | 0.02 | 3.16 [2.62, 3.96] | 0.40 [-0.00, 0.67] | 0.40 [0.00, 0.67] | – | 0.97 [0.93, 1.00] |
| lab_neutral | – | 20 / 20 | 0 | 0.93 | 0.12 | 2.64 [1.93, 3.96] | -0.14 [-0.59, 0.40] | -0.14 [-0.51, 0.00] | – | 0.98 [0.95, 1.00] |
| lab_br10 | 0.10 | 20 / 20 | 0 | 0.88 | 0.07 | 2.64 [1.93, 3.96] | 0.14 [-0.40, 0.59] | 0.14 [0.00, 0.51] | 0.93 | 0.98 [0.94, 1.00] |
| lab_br90 | 0.90 | 20 / 20 | 0 | 0.93 | 0.12 | 2.64 [1.93, 3.96] | -0.14 [-0.59, 0.40] | -0.14 [-0.51, 0.00] | -0.93 | 0.98 [0.93, 1.00] |

- **Prior-use ratio ρ = 0.07 [-0.02, 0.25]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.13 [-0.03, 0.49]; ideal = ln 81 / d′(br50) = 1.86.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.08 [0.00, 0.27]**; minus base-rate ρ = 0.01 [0.00, 0.03] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **0.00 [0.00, 0.00]**; minus base-rate ρ = -0.07 [-0.25, 0.02] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.15 [0.00, 0.40]**; minus base-rate ρ = 0.08 [0.00, 0.26] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.00 [0.00, 0.00].
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 35 distinct values.
- z-ROC slope in br50: 0.94 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 4/6; wrong answer 14/14.

### sonnet-5.5-think

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | – | 0.97 [0.92, 1.00] |
| br10 | 0.10 | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | 0.83 | 0.96 [0.90, 1.00] |
| br50 | 0.50 | 20 / 20 | 0 | 0.88 | 0.07 | 2.64 [1.93, 3.96] | 0.14 [-0.40, 0.59] | 0.14 [0.00, 0.51] | 0.00 | 0.98 [0.93, 1.00] |
| br90 | 0.90 | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | -0.83 | 0.96 [0.89, 1.00] |
| br10_use | 0.10 | 20 / 20 | 0 | 0.88 | 0.07 | 2.64 [1.93, 3.96] | 0.14 [-0.40, 0.59] | 0.14 [0.00, 0.51] | 0.83 | 0.97 [0.93, 1.00] |
| br90_use | 0.90 | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | -0.83 | 0.97 [0.90, 1.00] |
| pay_fa9 | 0.10 | 20 / 20 | 0 | 0.83 | 0.02 | 2.95 [2.48, 3.96] | 0.51 [-0.00, 0.74] | 0.51 [0.00, 0.91] | 0.83 | 0.97 [0.93, 1.00] |
| pay_miss9 | 0.90 | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | -0.83 | 0.96 [0.89, 1.00] |
| presuppose | – | 20 / 20 | 0 | 0.93 | 0.12 | 2.64 [1.93, 3.96] | -0.14 [-0.59, 0.40] | -0.14 [-0.51, 0.00] | – | 0.96 [0.89, 1.00] |
| lenient | – | 20 / 20 | 0 | 0.88 | 0.07 | 2.64 [1.93, 3.96] | 0.14 [-0.40, 0.59] | 0.14 [0.00, 0.51] | – | 0.98 [0.94, 1.00] |
| lab_neutral | – | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | – | 0.97 [0.93, 1.00] |
| lab_br10 | 0.10 | 20 / 20 | 0 | 0.88 | 0.07 | 2.64 [1.93, 3.96] | 0.14 [-0.40, 0.59] | 0.14 [0.00, 0.51] | 0.83 | 0.98 [0.93, 1.00] |
| lab_br90 | 0.90 | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | -0.83 | 0.98 [0.93, 1.00] |

- **Prior-use ratio ρ = 0.00 [0.00, 0.00]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.00 [0.00, 0.00]; ideal = ln 81 / d′(br50) = 1.66.
- ρ for base rate + instruction to use it (br10_use vs br90_use) = **0.09 [0.00, 0.36]**; minus base-rate ρ = 0.09 [0.00, 0.36] (paired).
- ρ for stated payoffs (pay_fa9 vs pay_miss9) = **0.30 [0.00, 0.63]**; minus base-rate ρ = 0.30 [0.00, 0.63] (paired).
- ρ for base rate, verdict words "flawed"/"sound" (lab_br10 vs lab_br90) = **0.09 [0.00, 0.36]**; minus base-rate ρ = 0.09 [0.00, 0.36] (paired).
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.14 [0.00, 0.51].
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 34 distinct values.
- z-ROC slope in br50: 0.45 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 4/6; wrong answer 14/14.

### sonnet-5.5-think-max

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 20 / 20 | 0 | 0.88 | 0.12 | 2.36 [1.60, 3.45] | -0.00 [-0.51, 0.51] | 0.00 [0.00, 0.00] | – | 0.97 [0.93, 1.00] |

- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 14 distinct values.
- z-ROC slope in neutral: 0.33 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 4/6; wrong answer 14/14.

### Model comparison (paired over the same items)

- stated base rate: ρ(sonnet-5.5-nothink) − ρ(sonnet-5.5-think) = 0.07 [-0.02, 0.25]
- base rate + instruction to use it: ρ(sonnet-5.5-nothink) − ρ(sonnet-5.5-think) = -0.01 [-0.31, 0.24]
- stated payoffs: ρ(sonnet-5.5-nothink) − ρ(sonnet-5.5-think) = -0.30 [-0.63, 0.00]
- base rate, verdict words "flawed"/"sound": ρ(sonnet-5.5-nothink) − ρ(sonnet-5.5-think) = 0.07 [-0.07, 0.25]
