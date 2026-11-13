### sim-critic

| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | ideal c* | AUC [95% CI] |
|---|---|---|---|---|---|---|---|---|---|
| neutral | – | 99 / 96 | 5 | 0.65 | 0.21 | 1.17 [0.80, 1.56] | 0.21 [0.02, 0.41] | – | 0.82 [0.76, 0.88] |
| br10 | 0.10 | 98 / 98 | 4 | 0.35 | 0.05 | 1.30 [0.87, 1.98] | 1.04 [0.83, 1.35] | 1.57 | 0.82 [0.76, 0.87] |
| br50 | 0.50 | 99 / 97 | 4 | 0.69 | 0.18 | 1.40 [1.03, 1.81] | 0.22 [0.03, 0.42] | 0.00 | 0.83 [0.78, 0.89] |
| br90 | 0.90 | 98 / 99 | 3 | 0.90 | 0.40 | 1.57 [1.19, 2.05] | -0.52 [-0.76, -0.32] | -1.57 | 0.85 [0.78, 0.90] |

- **Prior-use ratio ρ = 0.50 [0.35, 0.70]** (0 = ignores the stated base rate, 1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = 1.56 [1.29, 1.95]; ideal = ln 81 / d′(br50) = 3.13.
- Saying "50%" vs saying nothing: c(br50) − c(neutral) = 0.00 [-0.23, 0.26].
- ROC, AUC and z-ROC use verbalized p_error. Verbalized p_error took 101 distinct values.
- z-ROC slope in br50: 0.95 (≈1 supports the equal-variance model behind d′ and c*).
- Hits on flawed solutions in neutral, by final answer: right answer 4/9; wrong answer 60/90.
