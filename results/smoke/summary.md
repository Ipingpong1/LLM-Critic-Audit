### gemma4:12b-nothink

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 10 / 10 | 0 | 0.68 | 0.14 | 1.57 [0.62, 2.79] | 0.31 [-0.30, 0.85] | – | 0.92 [0.78, 1.00] |
| br10 | 0.10 | 10 / 10 | 0 | 0.68 | 0.14 | 1.57 [0.62, 2.79] | 0.31 [-0.30, 0.85] | 1.40 | 0.87 [0.70, 0.99] |
| br50 | 0.50 | 10 / 10 | 0 | 0.68 | 0.14 | 1.57 [0.62, 2.79] | 0.31 [-0.30, 0.85] | 0.00 | 0.87 [0.70, 0.99] |
| br90 | 0.90 | 10 / 10 | 0 | 0.68 | 0.14 | 1.57 [0.62, 2.79] | 0.31 [-0.30, 0.85] | -1.40 | 0.90 [0.76, 1.00] |

- **Prior-use ratio ρ = 0.00 [0.00, 0.00]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.00 [0.00, 0.00]; ideal = ln 81 / d′(br50) = 2.80.
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.00 [0.00, 0.00].
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 2 distinct values.
- z-ROC slope in br50: 0.86 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: wrong answer 7/10.

### qwen3.5:27b-nothink

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 10 / 10 | 0 | 0.86 | 0.05 | 2.79 [2.16, 3.38] | 0.30 [-0.00, 0.61] | – | 1.00 [1.00, 1.00] |
| br10 | 0.10 | 10 / 10 | 0 | 0.77 | 0.05 | 2.44 [1.69, 3.38] | 0.47 [-0.00, 0.85] | 0.90 | 1.00 [1.00, 1.00] |
| br50 | 0.50 | 10 / 10 | 0 | 0.77 | 0.05 | 2.44 [1.69, 3.38] | 0.47 [-0.00, 0.85] | 0.00 | 1.00 [1.00, 1.00] |
| br90 | 0.90 | 10 / 10 | 0 | 0.86 | 0.05 | 2.79 [2.16, 3.38] | 0.30 [-0.00, 0.61] | -0.90 | 1.00 [1.00, 1.00] |

- **Prior-use ratio ρ = 0.10 [0.00, 0.30]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.17 [0.00, 0.61]; ideal = ln 81 / d′(br50) = 1.80.
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.17 [0.00, 0.61].
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 4 distinct values.
- z-ROC slope in br50: – (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: wrong answer 9/10.

### qwen3.5:9b-nothink

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 10 / 10 | 0 | 0.77 | 0.14 | 1.84 [0.95, 3.38] | 0.17 [-0.43, 0.73] | – | 0.92 [0.79, 1.00] |
| br10 | 0.10 | 10 / 10 | 0 | 0.68 | 0.05 | 2.16 [1.46, 2.79] | 0.61 [0.30, 0.96] | 1.40 | 0.93 [0.81, 1.00] |
| br50 | 0.50 | 10 / 10 | 0 | 0.68 | 0.14 | 1.57 [0.70, 2.79] | 0.31 [-0.26, 0.85] | 0.00 | 0.91 [0.79, 1.00] |
| br90 | 0.90 | 10 / 10 | 0 | 0.77 | 0.23 | 1.50 [0.52, 2.79] | -0.00 [-0.61, 0.61] | -1.40 | 0.90 [0.75, 1.00] |

- **Prior-use ratio ρ = 0.22 [0.00, 0.45]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.61 [0.00, 1.08]; ideal = ln 81 / d′(br50) = 2.80.
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.14 [0.00, 0.47].
- ROC, AUC and z-ROC use verdict-token logprobs. Verbalized p_error took 3 distinct values.
- z-ROC slope in br50: 0.52 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: wrong answer 8/10.

### qwen3.5:9b-think

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 9 / 9 | 2 | 0.95 | 0.05 | 3.29 [3.13, 3.38] | 0.00 [-0.06, 0.08] | – | 1.00 [1.00, 1.00] |
| br10 | 0.10 | 9 / 10 | 1 | 0.95 | 0.05 | 3.34 [3.22, 3.38] | 0.02 [-0.00, 0.08] | 0.67 | 1.00 [1.00, 1.00] |
| br50 | 0.50 | 9 / 9 | 2 | 0.95 | 0.05 | 3.29 [3.13, 3.38] | 0.00 [-0.06, 0.08] | 0.00 | 1.00 [1.00, 1.00] |
| br90 | 0.90 | 9 / 10 | 1 | 0.95 | 0.05 | 3.34 [3.22, 3.38] | 0.02 [-0.00, 0.08] | -0.67 | 1.00 [1.00, 1.00] |

- **Prior-use ratio ρ = 0.00 [0.00, 0.00]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 0.00 [0.00, 0.00]; ideal = ln 81 / d′(br50) = 1.34.
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.00 [0.00, 0.00].
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 2 distinct values (too coarse for a useful ROC; rerun with --logprobs).
- z-ROC slope in br50: – (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: wrong answer 9/9.

### Model comparison (paired over the same items)

- ρ(gemma4:12b-nothink) − ρ(qwen3.5:27b-nothink) = -0.10 [-0.30, 0.00]
- ρ(gemma4:12b-nothink) − ρ(qwen3.5:9b-nothink) = -0.22 [-0.45, 0.00]
- ρ(gemma4:12b-nothink) − ρ(qwen3.5:9b-think) = 0.00 [0.00, 0.00]
- ρ(qwen3.5:27b-nothink) − ρ(qwen3.5:9b-nothink) = -0.12 [-0.43, 0.15]
- ρ(qwen3.5:27b-nothink) − ρ(qwen3.5:9b-think) = 0.10 [0.00, 0.30]
- ρ(qwen3.5:9b-nothink) − ρ(qwen3.5:9b-think) = 0.22 [0.00, 0.45]
