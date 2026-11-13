# Premise test: expected precision (simulation, no model called)

## Calibration: agreement between neutral and told-50% on correct solutions (hard set)

| critic | flagged at neutral | flagged at told 50% | phi |
|---|---|---|---|
| qwen3.5:27b on | 0.16 | 0.25 | 0.76 |
| qwen3.5:4b on | 0.16 | 0.18 | 0.65 |
| opus on | 0.13 | 0.12 | 0.96 |
| sonnet on | 0.08 | 0.06 | 0.55 |

| item spread sigma (logit) | implied phi at a 16% flag rate |
|---|---|
| 1 | 0.12 |
| 2 | 0.33 |
| 3 | 0.48 |
| 4 | 0.59 |
| 6 | 0.71 |
| 8 | 0.78 |

Mean phi across these critics is 0.73, so the simulation uses sigma = 6. The two prompts are not identical, so this is if anything a lower bound on how stable a verdict is.

## Designs

Half-width of the 95% CI on c(claim) − c(neutral), and the share of runs whose CI excludes 0. 300 simulated runs, 400 bootstrap resamples each.

| items per class | samples | requests per condition | logit shift | false alarms | mean c shift | CI half-width | CI excludes 0 |
|---|---|---|---|---|---|---|---|
| 100 | 1 | 200 | 0.0 | 16 → 16 | +0.00 | 0.23 | 0.07 |
| 100 | 1 | 200 | 0.5 | 16 → 18 | -0.09 | 0.23 | 0.14 |
| 100 | 1 | 200 | 1.0 | 16 → 20 | -0.16 | 0.24 | 0.32 |
| 100 | 1 | 200 | 2.0 | 16 → 25 | -0.30 | 0.25 | 0.76 |
| 100 | 1 | 200 | 4.0 | 16 → 37 | -0.56 | 0.28 | 0.98 |
| 100 | 3 | 600 | 0.0 | 16 → 16 | +0.00 | 0.13 | 0.09 |
| 100 | 3 | 600 | 0.5 | 16 → 18 | -0.08 | 0.14 | 0.24 |
| 100 | 3 | 600 | 1.0 | 16 → 20 | -0.16 | 0.15 | 0.61 |
| 100 | 3 | 600 | 2.0 | 16 → 25 | -0.30 | 0.17 | 0.95 |
| 100 | 3 | 600 | 4.0 | 16 → 37 | -0.55 | 0.21 | 1.00 |
| 100 | 5 | 1000 | 0.0 | 16 → 16 | -0.00 | 0.10 | 0.08 |
| 100 | 5 | 1000 | 0.5 | 16 → 18 | -0.07 | 0.11 | 0.34 |
| 100 | 5 | 1000 | 1.0 | 16 → 20 | -0.15 | 0.12 | 0.80 |
| 100 | 5 | 1000 | 2.0 | 16 → 25 | -0.29 | 0.14 | 0.97 |
| 100 | 5 | 1000 | 4.0 | 16 → 37 | -0.55 | 0.19 | 1.00 |
| 150 | 2 | 600 | 0.0 | 16 → 16 | +0.00 | 0.14 | 0.07 |
| 150 | 2 | 600 | 0.5 | 16 → 18 | -0.08 | 0.14 | 0.27 |
| 150 | 2 | 600 | 1.0 | 16 → 20 | -0.15 | 0.15 | 0.57 |
| 150 | 2 | 600 | 2.0 | 16 → 25 | -0.30 | 0.17 | 0.96 |
| 150 | 2 | 600 | 4.0 | 16 → 37 | -0.57 | 0.21 | 1.00 |
| 300 | 1 | 600 | 0.0 | 16 → 16 | +0.00 | 0.14 | 0.08 |
| 300 | 1 | 600 | 0.5 | 16 → 18 | -0.08 | 0.15 | 0.20 |
| 300 | 1 | 600 | 1.0 | 16 → 20 | -0.16 | 0.15 | 0.59 |
| 300 | 1 | 600 | 2.0 | 16 → 25 | -0.31 | 0.18 | 0.98 |
| 300 | 1 | 600 | 4.0 | 16 → 37 | -0.59 | 0.21 | 1.00 |
