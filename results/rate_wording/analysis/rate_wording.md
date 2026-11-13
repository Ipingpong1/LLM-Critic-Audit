# Rate wording run: results

Plan: `prereg/rate_wording.md`. 141200 rows, 12 critic runs, 10000 resamples. ρ is [c(10%) − c(90%)] × d′(neutral) / ln 81. Intervals are 95%, from an item bootstrap.

## Labels and ceiling

Errors per 200 at `neutral`. At 4 or fewer, ρ is reported but not interpreted under that labelling (marked \*).

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

## W1, under-use in every wording

Holds when the interval for ρ lies below 1 in every arm the critic has.

| critic | original | contested left out | contested flipped | all below 0.5 (original labels) |
|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | holds (largest upper limit 0.21, freq) | holds (largest upper limit 0.28, item) | holds (largest upper limit 0.23, freq) | yes |
| gemma4:12b-think-bf16-t1 | holds (largest upper limit 0.40, item) | holds (largest upper limit 0.69, item)\* | holds (largest upper limit 0.45, item) | yes |
| gpt-6-luna-think | holds (largest upper limit 0.29, item) | holds (largest upper limit 0.40, item) | holds (largest upper limit 0.36, item) | yes |
| gpt-6.1-sol-think | holds (largest upper limit 0.34, item) | holds (largest upper limit 0.43, item) | holds (largest upper limit 0.39, item) | yes |
| haiku-5.5-think | holds (largest upper limit 0.37, user) | holds (largest upper limit 0.53, user) | holds (largest upper limit 0.45, user) | yes |
| opus-5.5-think | holds (largest upper limit 0.44, br) | holds (largest upper limit 0.80, br)\* | fails in br (largest upper limit 1.01, br) | yes |
| qwen3.5:4b-nothink-bf16-t1 | holds (largest upper limit 0.34, user) | holds (largest upper limit 0.39, user) | holds (largest upper limit 0.35, user) | yes |
| qwen3.5:4b-think-bf16-t1 | holds (largest upper limit 0.47, item) | holds (largest upper limit 0.95, item)\* | holds (largest upper limit 0.99, user) | yes |
| qwen3.5:9b-nothink-bf16-t1 | holds (largest upper limit 0.14, user) | holds (largest upper limit 0.17, user) | holds (largest upper limit 0.17, user) | yes |
| qwen3.5:9b-think-bf16-t1 | holds (largest upper limit 0.39, comp) | holds (largest upper limit 0.62, freq)\* | holds (largest upper limit 0.75, hist) | yes |
| qwen3.5:27b-nothink-bf16-t1 | holds (largest upper limit 0.16, item) | holds (largest upper limit 0.21, item) | holds (largest upper limit 0.22, item) | yes |
| qwen3.5:27b-think-bf16-t1 | holds (largest upper limit 0.65, item) | fails in item (largest upper limit 1.16, item) | fails in item (largest upper limit 1.12, item) | no |

### ρ by arm, original (100 flawed, 100 correct)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.07 [0.02, 0.15] | 0.12 [0.06, 0.21] | 0.02 [0.00, 0.05] | 0.05 [0.00, 0.12] | 0.05 [0.02, 0.12] | 0.11 [0.06, 0.21] |
| gemma4:12b-think-bf16-t1 | 0.07 [-0.12, 0.22] | -0.04 [-0.21, 0.07] | -0.02 [-0.17, 0.11] | -0.11 [-0.26, 0.07] | 0.23 [0.11, 0.35] | 0.21 [0.09, 0.40] |
| gpt-6-luna-think | 0.07 [-0.02, 0.20] | 0.03 [-0.00, 0.08] | 0.07 [0.00, 0.14] | 0.07 [-0.01, 0.22] | 0.10 [-0.01, 0.23] | 0.16 [0.06, 0.29] |
| gpt-6.1-sol-think | 0.17 [0.00, 0.32] | 0.17 [0.00, 0.32] | 0.17 [0.00, 0.32] | 0.16 [0.00, 0.31] | 0.17 [0.00, 0.32] | 0.19 [0.01, 0.34] |
| haiku-5.5-think | 0.02 [-0.01, 0.05] | 0.09 [-0.02, 0.20] | 0.10 [-0.01, 0.21] | 0.11 [0.01, 0.23] | 0.20 [0.01, 0.37] | 0.04 [0.00, 0.08] |
| opus-5.5-think | 0.29 [0.09, 0.44] | 0.09 [0.03, 0.18] | 0.14 [0.07, 0.26] | 0.22 [0.03, 0.35] | 0.08 [0.03, 0.17] | 0.19 [0.01, 0.31] |
| qwen3.5:4b-nothink-bf16-t1 | 0.14 [0.10, 0.21] | 0.11 [0.07, 0.17] | 0.08 [0.05, 0.13] | 0.05 [0.03, 0.08] | 0.23 [0.17, 0.34] | 0.13 [0.09, 0.20] |
| qwen3.5:4b-think-bf16-t1 | 0.14 [0.07, 0.22] | 0.30 [0.13, 0.43] | 0.18 [0.01, 0.29] | 0.16 [0.01, 0.29] | 0.26 [0.13, 0.39] | 0.32 [0.15, 0.47] |
| qwen3.5:9b-nothink-bf16-t1 | 0.08 [0.05, 0.13] | 0.06 [0.03, 0.09] | 0.02 [0.01, 0.04] | 0.06 [0.03, 0.12] | 0.08 [0.05, 0.14] | 0.08 [0.05, 0.13] |
| qwen3.5:9b-think-bf16-t1 | 0.20 [0.08, 0.33] | 0.24 [0.12, 0.37] | 0.21 [0.01, 0.39] | 0.20 [0.12, 0.29] | 0.11 [0.06, 0.18] | 0.16 [0.09, 0.25] |
| qwen3.5:27b-nothink-bf16-t1 | 0.07 [0.04, 0.11] | 0.09 [0.05, 0.13] | 0.06 [0.03, 0.10] | 0.06 [0.03, 0.10] | 0.08 [0.05, 0.13] | 0.10 [0.06, 0.16] |
| qwen3.5:27b-think-bf16-t1 | 0.36 [0.23, 0.51] | 0.29 [0.21, 0.39] | 0.34 [0.15, 0.50] | 0.25 [0.12, 0.38] | 0.28 [0.16, 0.42] | 0.47 [0.26, 0.65] |

### ρ by arm, contested left out (100 flawed, 86 correct)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.09 [0.03, 0.18] | 0.14 [0.07, 0.24] | 0.03 [0.01, 0.07] | 0.05 [-0.00, 0.14] | 0.06 [0.02, 0.15] | 0.15 [0.07, 0.28] |
| gemma4:12b-think-bf16-t1\* | 0.19 [-0.07, 0.43] | 0.03 [-0.28, 0.24] | 0.00 [-0.25, 0.27] | -0.07 [-0.26, 0.19] | 0.32 [0.00, 0.57] | 0.45 [0.21, 0.69] |
| gpt-6-luna-think | 0.09 [-0.03, 0.24] | 0.07 [0.00, 0.16] | 0.11 [0.00, 0.22] | 0.09 [-0.03, 0.27] | 0.12 [-0.04, 0.28] | 0.23 [0.10, 0.40] |
| gpt-6.1-sol-think | 0.20 [0.00, 0.39] | 0.20 [0.00, 0.39] | 0.20 [0.00, 0.38] | 0.18 [0.00, 0.35] | 0.20 [0.00, 0.38] | 0.24 [0.03, 0.43] |
| haiku-5.5-think | 0.06 [-0.04, 0.20] | 0.16 [-0.04, 0.36] | 0.22 [0.05, 0.39] | 0.18 [0.04, 0.33] | 0.29 [0.02, 0.53] | 0.10 [0.00, 0.22] |
| opus-5.5-think\* | 0.49 [0.15, 0.80] | 0.31 [0.10, 0.61] | 0.40 [0.19, 0.73] | 0.32 [0.04, 0.63] | 0.17 [0.04, 0.46] | 0.27 [0.00, 0.48] |
| qwen3.5:4b-nothink-bf16-t1 | 0.16 [0.11, 0.24] | 0.12 [0.08, 0.19] | 0.10 [0.07, 0.15] | 0.06 [0.03, 0.09] | 0.27 [0.19, 0.39] | 0.15 [0.11, 0.23] |
| qwen3.5:4b-think-bf16-t1\* | 0.32 [0.21, 0.46] | 0.62 [0.39, 0.82] | 0.27 [-0.02, 0.51] | 0.29 [0.02, 0.55] | 0.68 [0.48, 0.89] | 0.72 [0.47, 0.95] |
| qwen3.5:9b-nothink-bf16-t1 | 0.09 [0.05, 0.16] | 0.07 [0.04, 0.11] | 0.02 [0.01, 0.05] | 0.08 [0.04, 0.13] | 0.10 [0.06, 0.17] | 0.10 [0.06, 0.16] |
| qwen3.5:9b-think-bf16-t1\* | 0.32 [0.15, 0.48] | 0.45 [0.28, 0.62] | 0.33 [0.05, 0.59] | 0.41 [0.28, 0.60] | 0.24 [0.12, 0.40] | 0.33 [0.21, 0.49] |
| qwen3.5:27b-nothink-bf16-t1 | 0.09 [0.05, 0.14] | 0.12 [0.07, 0.18] | 0.08 [0.04, 0.13] | 0.08 [0.04, 0.14] | 0.10 [0.06, 0.16] | 0.13 [0.07, 0.21] |
| qwen3.5:27b-think-bf16-t1 | 0.61 [0.43, 0.83] | 0.48 [0.36, 0.65] | 0.59 [0.35, 0.79] | 0.41 [0.24, 0.60] | 0.45 [0.28, 0.64] | 0.85 [0.58, 1.16] |

### ρ by arm, contested flipped (114 flawed, 86 correct)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0.07 [0.03, 0.14] | 0.14 [0.08, 0.23] | 0.03 [0.00, 0.06] | 0.06 [0.01, 0.12] | 0.05 [0.02, 0.10] | 0.13 [0.06, 0.23] |
| gemma4:12b-think-bf16-t1 | 0.12 [-0.03, 0.29] | 0.11 [-0.11, 0.29] | -0.09 [-0.30, 0.11] | -0.04 [-0.16, 0.09] | 0.17 [-0.06, 0.41] | 0.27 [0.07, 0.45] |
| gpt-6-luna-think | 0.04 [-0.06, 0.17] | 0.05 [-0.02, 0.14] | 0.09 [0.00, 0.20] | 0.08 [-0.02, 0.26] | 0.10 [-0.02, 0.23] | 0.17 [0.07, 0.36] |
| gpt-6.1-sol-think | 0.11 [0.00, 0.34] | 0.11 [0.00, 0.34] | 0.11 [0.00, 0.34] | 0.09 [0.00, 0.32] | 0.11 [0.00, 0.34] | 0.15 [0.03, 0.39] |
| haiku-5.5-think | 0.06 [-0.09, 0.19] | 0.06 [-0.13, 0.29] | 0.09 [-0.09, 0.27] | 0.16 [-0.01, 0.40] | 0.21 [0.05, 0.45] | 0.11 [0.00, 0.24] |
| opus-5.5-think | 0.56 [0.29, 1.01] | 0.38 [0.14, 0.76] | 0.49 [0.25, 0.93] | 0.33 [0.11, 0.71] | 0.27 [0.09, 0.65] | 0.23 [0.04, 0.52] |
| qwen3.5:4b-nothink-bf16-t1 | 0.15 [0.11, 0.22] | 0.13 [0.09, 0.19] | 0.09 [0.06, 0.13] | 0.05 [0.03, 0.09] | 0.25 [0.19, 0.35] | 0.14 [0.10, 0.20] |
| qwen3.5:4b-think-bf16-t1 | 0.47 [0.22, 0.69] | 0.72 [0.53, 0.90] | 0.11 [-0.11, 0.37] | 0.21 [-0.04, 0.48] | 0.76 [0.53, 0.99] | 0.62 [0.43, 0.87] |
| qwen3.5:9b-nothink-bf16-t1 | 0.10 [0.06, 0.17] | 0.07 [0.04, 0.11] | 0.03 [0.01, 0.05] | 0.09 [0.05, 0.15] | 0.11 [0.07, 0.17] | 0.11 [0.07, 0.17] |
| qwen3.5:9b-think-bf16-t1 | 0.37 [0.23, 0.54] | 0.58 [0.43, 0.71] | 0.20 [-0.03, 0.45] | 0.57 [0.39, 0.75] | 0.29 [0.10, 0.49] | 0.35 [0.10, 0.64] |
| qwen3.5:27b-nothink-bf16-t1 | 0.10 [0.06, 0.16] | 0.13 [0.09, 0.20] | 0.09 [0.05, 0.14] | 0.09 [0.05, 0.14] | 0.10 [0.06, 0.16] | 0.14 [0.08, 0.22] |
| qwen3.5:27b-think-bf16-t1 | 0.55 [0.40, 0.77] | 0.66 [0.46, 0.85] | 0.53 [0.37, 0.77] | 0.38 [0.25, 0.58] | 0.40 [0.19, 0.65] | 0.78 [0.55, 1.12] |

## W2, a wording changes use

ρ(arm) − ρ(`br`), paired, Holm across all tests of a labelling. "No difference" needs the whole interval within ±0.15.

### original: 60 tests; 3 differ, 27 no difference, 30 inconclusive

| critic | freq | comp | hist | user | item |
|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | +0.06 [-0.00, 0.11], no difference | -0.05 [-0.13, 0.00], no difference | -0.02 [-0.08, 0.03], no difference | -0.01 [-0.06, 0.03], no difference | +0.05 [-0.01, 0.12], no difference |
| gemma4:12b-think-bf16-t1 | -0.10 [-0.34, 0.05], inconclusive | -0.09 [-0.36, 0.19], inconclusive | -0.18 [-0.38, 0.11], inconclusive | +0.17 [-0.03, 0.36], inconclusive | +0.15 [-0.06, 0.45], inconclusive |
| gpt-6-luna-think | -0.04 [-0.18, 0.04], inconclusive | -0.00 [-0.15, 0.05], inconclusive | +0.00 [-0.13, 0.12], no difference | +0.03 [-0.18, 0.11], inconclusive | +0.09 [-0.01, 0.18], inconclusive |
| gpt-6.1-sol-think | +0.00 [0.00, 0.00], no difference | -0.00 [-0.03, 0.03], no difference | -0.01 [-0.05, 0.03], no difference | -0.00 [-0.03, 0.03], no difference | +0.02 [-0.02, 0.07], no difference |
| haiku-5.5-think | +0.07 [-0.05, 0.19], inconclusive | +0.08 [-0.03, 0.20], inconclusive | +0.10 [-0.00, 0.21], inconclusive | +0.19 [-0.01, 0.36], inconclusive | +0.02 [-0.01, 0.06], no difference |
| opus-5.5-think | -0.20 [-0.33, -0.00], inconclusive | -0.15 [-0.28, 0.06], inconclusive | -0.07 [-0.17, 0.00], inconclusive | -0.21 [-0.34, -0.02], inconclusive | -0.10 [-0.21, -0.03], inconclusive |
| qwen3.5:4b-nothink-bf16-t1 | -0.03 [-0.08, 0.02], no difference | -0.06 [-0.11, -0.02], no difference | -0.09 [-0.14, -0.06], differs (Holm p 0.006) | +0.09 [0.05, 0.15], differs (Holm p 0.006) | -0.01 [-0.05, 0.03], no difference |
| qwen3.5:4b-think-bf16-t1 | +0.16 [-0.01, 0.29], inconclusive | +0.05 [-0.14, 0.16], inconclusive | +0.02 [-0.15, 0.16], inconclusive | +0.12 [0.01, 0.23], inconclusive | +0.19 [0.01, 0.32], inconclusive |
| qwen3.5:9b-nothink-bf16-t1 | -0.02 [-0.09, 0.03], no difference | -0.06 [-0.11, -0.02], no difference | -0.02 [-0.05, 0.02], no difference | +0.00 [-0.04, 0.05], no difference | +0.00 [-0.04, 0.04], no difference |
| qwen3.5:9b-think-bf16-t1 | +0.04 [-0.12, 0.20], inconclusive | +0.01 [-0.13, 0.10], no difference | -0.01 [-0.13, 0.12], no difference | -0.09 [-0.21, 0.02], inconclusive | -0.05 [-0.17, 0.08], inconclusive |
| qwen3.5:27b-nothink-bf16-t1 | +0.02 [-0.03, 0.07], no difference | -0.01 [-0.05, 0.03], no difference | -0.01 [-0.03, 0.02], no difference | +0.02 [-0.02, 0.06], no difference | +0.03 [-0.00, 0.07], no difference |
| qwen3.5:27b-think-bf16-t1 | -0.08 [-0.19, 0.03], inconclusive | -0.02 [-0.16, 0.13], inconclusive | -0.12 [-0.20, -0.05], differs (Holm p 0.029) | -0.08 [-0.25, 0.08], inconclusive | +0.11 [-0.02, 0.26], inconclusive |

### contested left out: 60 tests; 2 differ, 22 no difference, 36 inconclusive

| critic | freq | comp | hist | user | item |
|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | +0.05 [-0.02, 0.13], no difference | -0.05 [-0.15, 0.01], no difference | -0.03 [-0.11, 0.01], no difference | -0.02 [-0.08, 0.03], no difference | +0.06 [-0.02, 0.16], inconclusive |
| gemma4:12b-think-bf16-t1 | -0.16 [-0.51, 0.13], inconclusive | -0.19 [-0.63, 0.28], inconclusive | -0.26 [-0.57, 0.15], inconclusive | +0.13 [-0.20, 0.40], inconclusive | +0.26 [-0.08, 0.66], inconclusive |
| gpt-6-luna-think | -0.02 [-0.19, 0.12], inconclusive | +0.02 [-0.15, 0.11], inconclusive | +0.00 [-0.17, 0.15], inconclusive | +0.03 [-0.22, 0.15], inconclusive | +0.14 [0.00, 0.29], inconclusive |
| gpt-6.1-sol-think | +0.00 [0.00, 0.00], no difference | -0.00 [-0.06, 0.06], no difference | -0.02 [-0.10, 0.05], no difference | -0.00 [-0.06, 0.06], no difference | +0.04 [-0.04, 0.13], no difference |
| haiku-5.5-think | +0.09 [-0.18, 0.35], inconclusive | +0.15 [-0.09, 0.38], inconclusive | +0.12 [-0.05, 0.28], inconclusive | +0.23 [-0.10, 0.50], inconclusive | +0.03 [-0.10, 0.17], inconclusive |
| opus-5.5-think | -0.18 [-0.38, 0.10], inconclusive | -0.09 [-0.27, 0.23], inconclusive | -0.17 [-0.45, 0.07], inconclusive | -0.32 [-0.58, 0.00], inconclusive | -0.22 [-0.52, -0.02], inconclusive |
| qwen3.5:4b-nothink-bf16-t1 | -0.04 [-0.10, 0.02], no difference | -0.06 [-0.12, -0.01], no difference | -0.10 [-0.16, -0.07], differs (Holm p 0.006) | +0.11 [0.06, 0.18], differs (Holm p 0.006) | -0.01 [-0.06, 0.04], no difference |
| qwen3.5:4b-think-bf16-t1 | +0.30 [0.04, 0.50], inconclusive | -0.05 [-0.37, 0.21], inconclusive | -0.03 [-0.34, 0.24], inconclusive | +0.36 [0.14, 0.57], inconclusive | +0.40 [0.13, 0.63], inconclusive |
| qwen3.5:9b-nothink-bf16-t1 | -0.03 [-0.10, 0.03], no difference | -0.07 [-0.13, -0.03], no difference | -0.02 [-0.06, 0.02], no difference | +0.01 [-0.04, 0.06], no difference | +0.01 [-0.04, 0.05], no difference |
| qwen3.5:9b-think-bf16-t1 | +0.13 [-0.08, 0.35], inconclusive | +0.02 [-0.20, 0.18], inconclusive | +0.10 [-0.11, 0.34], inconclusive | -0.08 [-0.25, 0.13], inconclusive | +0.01 [-0.16, 0.22], inconclusive |
| qwen3.5:27b-nothink-bf16-t1 | +0.03 [-0.03, 0.10], no difference | -0.01 [-0.07, 0.05], no difference | -0.01 [-0.04, 0.03], no difference | +0.01 [-0.03, 0.07], no difference | +0.04 [-0.01, 0.11], no difference |
| qwen3.5:27b-think-bf16-t1 | -0.13 [-0.29, 0.04], inconclusive | -0.02 [-0.23, 0.17], inconclusive | -0.20 [-0.37, -0.05], inconclusive | -0.16 [-0.39, 0.06], inconclusive | +0.23 [0.02, 0.51], inconclusive |

### contested flipped: 60 tests; 2 differ, 25 no difference, 33 inconclusive

| critic | freq | comp | hist | user | item |
|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | +0.07 [0.00, 0.14], no difference | -0.05 [-0.12, 0.00], no difference | -0.02 [-0.07, 0.03], no difference | -0.03 [-0.08, 0.02], no difference | +0.05 [-0.00, 0.13], no difference |
| gemma4:12b-think-bf16-t1 | -0.01 [-0.23, 0.20], inconclusive | -0.21 [-0.54, 0.08], inconclusive | -0.16 [-0.37, 0.04], inconclusive | +0.05 [-0.16, 0.23], inconclusive | +0.15 [-0.07, 0.37], inconclusive |
| gpt-6-luna-think | +0.00 [-0.12, 0.14], no difference | +0.04 [-0.06, 0.15], no difference | +0.03 [-0.08, 0.19], inconclusive | +0.05 [-0.10, 0.17], inconclusive | +0.13 [0.02, 0.30], inconclusive |
| gpt-6.1-sol-think | +0.00 [0.00, 0.00], no difference | -0.00 [-0.06, 0.05], no difference | -0.02 [-0.09, 0.05], no difference | -0.00 [-0.06, 0.05], no difference | +0.03 [-0.04, 0.12], no difference |
| haiku-5.5-think | +0.01 [-0.28, 0.34], inconclusive | +0.03 [-0.21, 0.28], inconclusive | +0.10 [-0.06, 0.33], inconclusive | +0.15 [-0.05, 0.46], inconclusive | +0.06 [-0.07, 0.22], inconclusive |
| opus-5.5-think | -0.19 [-0.49, 0.00], inconclusive | -0.07 [-0.33, 0.14], inconclusive | -0.23 [-0.55, 0.00], inconclusive | -0.29 [-0.62, -0.06], inconclusive | -0.33 [-0.71, -0.12], inconclusive |
| qwen3.5:4b-nothink-bf16-t1 | -0.02 [-0.08, 0.03], no difference | -0.06 [-0.12, -0.02], no difference | -0.10 [-0.15, -0.06], differs (Holm p 0.006) | +0.10 [0.06, 0.16], differs (Holm p 0.006) | -0.01 [-0.05, 0.03], no difference |
| qwen3.5:4b-think-bf16-t1 | +0.24 [0.01, 0.50], inconclusive | -0.36 [-0.66, 0.01], inconclusive | -0.26 [-0.51, 0.03], inconclusive | +0.28 [0.07, 0.51], inconclusive | +0.14 [-0.15, 0.53], inconclusive |
| qwen3.5:9b-nothink-bf16-t1 | -0.03 [-0.10, 0.02], no difference | -0.08 [-0.14, -0.03], no difference | -0.02 [-0.05, 0.02], no difference | +0.00 [-0.05, 0.05], no difference | +0.01 [-0.04, 0.05], no difference |
| qwen3.5:9b-think-bf16-t1 | +0.20 [-0.01, 0.37], inconclusive | -0.17 [-0.36, 0.03], inconclusive | +0.19 [-0.05, 0.40], inconclusive | -0.09 [-0.23, 0.07], inconclusive | -0.02 [-0.22, 0.20], inconclusive |
| qwen3.5:27b-nothink-bf16-t1 | +0.04 [-0.03, 0.10], no difference | -0.01 [-0.07, 0.05], no difference | -0.01 [-0.04, 0.02], no difference | +0.01 [-0.04, 0.05], no difference | +0.04 [-0.01, 0.10], no difference |
| qwen3.5:27b-think-bf16-t1 | +0.11 [-0.16, 0.29], inconclusive | -0.02 [-0.19, 0.18], inconclusive | -0.17 [-0.34, 0.01], inconclusive | -0.15 [-0.38, 0.07], inconclusive | +0.23 [0.04, 0.49], inconclusive |

## W3, information or number

Under `comp`, c(told 10% have errors) − c(told 90% have errors). Above 0: follows the information. Below 0: the number or the word.

| critic | original | contested left out | contested flipped |
|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | +0.03 [0.00, 0.07], unclear | +0.05 [0.01, 0.10], information | +0.04 [0.00, 0.10], unclear |
| gemma4:12b-think-bf16-t1 | -0.02 [-0.20, 0.13], unclear | +0.00 [-0.25, 0.26], unclear | -0.11 [-0.34, 0.12], unclear |
| gpt-6-luna-think | +0.10 [0.01, 0.22], information | +0.14 [0.00, 0.29], unclear | +0.12 [0.00, 0.26], unclear |
| gpt-6.1-sol-think | +0.23 [0.00, 0.44], unclear | +0.25 [0.00, 0.46], unclear | +0.15 [0.00, 0.41], unclear |
| haiku-5.5-think | +0.12 [-0.01, 0.26], unclear | +0.23 [0.05, 0.41], information | +0.11 [-0.10, 0.29], unclear |
| opus-5.5-think | +0.20 [0.09, 0.33], information | +0.44 [0.23, 0.73], information | +0.57 [0.30, 0.96], information |
| qwen3.5:4b-nothink-bf16-t1 | +0.24 [0.16, 0.33], information | +0.26 [0.18, 0.35], information | +0.24 [0.17, 0.33], information |
| qwen3.5:4b-think-bf16-t1 | +0.25 [0.01, 0.41], information | +0.30 [-0.02, 0.56], unclear | +0.13 [-0.13, 0.42], unclear |
| qwen3.5:9b-nothink-bf16-t1 | +0.05 [0.02, 0.10], information | +0.06 [0.02, 0.11], information | +0.06 [0.02, 0.11], information |
| qwen3.5:9b-think-bf16-t1 | +0.26 [0.01, 0.48], information | +0.35 [0.05, 0.59], information | +0.23 [-0.03, 0.47], unclear |
| qwen3.5:27b-nothink-bf16-t1 | +0.12 [0.07, 0.19], information | +0.13 [0.06, 0.20], information | +0.15 [0.08, 0.22], information |
| qwen3.5:27b-think-bf16-t1 | +0.44 [0.19, 0.62], information | +0.64 [0.39, 0.84], information | +0.62 [0.43, 0.86], information |

## W4, Opus on new items

- **original:** ρ for `br` 0.29 [0.09, 0.44]; holds; inside the Stage C interval [0.05, 0.44].
- **contested left out:** ρ for `br` 0.49 [0.15, 0.80]; holds; outside the Stage C interval [0.05, 0.44].
- **contested flipped:** ρ for `br` 0.56 [0.29, 1.01]; fails; outside the Stage C interval [0.05, 0.44].

## W5, the claim tests on GPT-6.1 Sol

| test | contrast | original | contested left out | contested flipped |
|---|---|---|---|---|
| T1 | `presuppose` − `neutral` | -0.09 [-0.16, -0.03], held | -0.12 [-0.23, -0.04], held | -0.12 [-0.23, -0.04], held |
| T2 | `claim_bare` − `neutral` | -1.59 [-1.72, -1.47], held | -1.75 [-1.91, -1.61], held | -1.95 [-2.20, -1.64], held |
| T3 | `claim_mistake` − `neutral` | -0.16 [-0.26, -0.08], held | -0.21 [-0.35, -0.10], held | -0.41 [-0.64, -0.13], held |
| T4 | `claim_reviewer` − `neutral` | -0.01 [-0.05, 0.00], not shown | -0.02 [-0.08, 0.00], not shown | -0.02 [-0.08, 0.00], not shown |
| T5 | `presuppose` − `check_only` | -0.09 [-0.16, -0.03], held | -0.12 [-0.23, -0.04], held | -0.12 [-0.23, -0.04], held |
| T6 | `presuppose` − `may_error` | -0.09 [-0.16, -0.03], held | -0.12 [-0.23, -0.04], held | -0.12 [-0.23, -0.04], held |
| T7 | `claim_random` − `neutral` | +0.00 [0.00, 0.00], no shift | +0.00 [0.00, 0.00], no shift | +0.00 [0.00, 0.00], no shift |
| T8 | `claim_random` − `claim_bare` | +1.59 [1.47, 1.72], held | +1.75 [1.61, 1.91], held | +1.95 [1.64, 2.20], held |
| T9 | `claim_correct` − `neutral` | +0.35 [0.08, 0.58], held | +0.48 [0.17, 0.77], held | +0.38 [0.16, 0.71], held |

## Secondary measures

Planned, uncorrected, not primary. The first three use no label.

### Flag-rate shift: share of all solutions flagged when told 90%, minus when told 10% (points)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | +2.0 [0.7, 3.5] | +4.0 [2.2, 6.3] | +0.7 [-0.2, 1.5] | +1.7 [0.3, 3.3] | +1.3 [0.5, 2.3] | +3.5 [1.7, 5.7] |
| gemma4:12b-think-bf16-t1 | +0.7 [-1.0, 2.5] | +0.5 [-1.0, 2.2] | -1.0 [-2.7, 0.5] | -1.0 [-2.3, 0.3] | +2.2 [0.5, 4.0] | +2.0 [0.2, 4.0] |
| gpt-6-luna-think | +0.5 [-0.7, 2.0] | +0.8 [-0.3, 2.2] | +1.5 [-0.2, 3.2] | +0.8 [-0.7, 2.5] | +0.8 [-0.7, 2.5] | +2.3 [0.8, 4.2] |
| gpt-6.1-sol-think | +1.5 [0.0, 3.5] | +1.5 [0.0, 3.5] | +1.5 [0.0, 3.5] | +1.0 [0.0, 2.5] | +1.5 [0.0, 3.5] | +2.5 [0.5, 5.0] |
| haiku-5.5-think | +0.5 [-0.3, 1.5] | +0.7 [-0.7, 2.2] | +1.0 [-0.2, 2.5] | +1.5 [0.2, 3.0] | +1.8 [0.5, 3.5] | +1.2 [0.0, 2.5] |
| opus-5.5-think | +5.0 [2.0, 8.0] | +3.0 [1.0, 5.5] | +5.0 [2.0, 8.0] | +3.0 [1.0, 5.5] | +3.0 [1.0, 5.5] | +2.0 [0.5, 4.0] |
| qwen3.5:4b-nothink-bf16-t1 | +10.7 [8.0, 13.5] | +8.0 [5.7, 10.5] | +6.3 [4.3, 8.3] | +3.7 [2.2, 5.3] | +16.7 [13.2, 20.2] | +9.2 [6.8, 11.7] |
| qwen3.5:4b-think-bf16-t1 | +5.2 [2.7, 7.8] | +6.0 [3.3, 8.8] | +0.8 [-0.7, 2.7] | +1.8 [-0.0, 3.8] | +7.2 [4.3, 10.3] | +7.3 [4.3, 10.7] |
| qwen3.5:9b-nothink-bf16-t1 | +5.0 [3.0, 7.0] | +4.2 [2.3, 6.3] | +1.7 [0.5, 3.0] | +4.3 [2.5, 6.3] | +5.7 [3.7, 7.8] | +5.7 [3.8, 7.7] |
| qwen3.5:9b-think-bf16-t1 | +5.0 [2.7, 7.7] | +6.2 [3.8, 8.8] | +2.2 [0.2, 4.3] | +7.3 [4.3, 10.5] | +4.0 [2.0, 6.2] | +5.8 [3.0, 8.8] |
| qwen3.5:27b-nothink-bf16-t1 | +3.3 [2.0, 4.7] | +4.7 [3.0, 6.5] | +3.2 [1.7, 4.8] | +3.0 [1.7, 4.3] | +3.8 [2.3, 5.5] | +4.7 [2.7, 6.8] |
| qwen3.5:27b-think-bf16-t1 | +13.0 [9.4, 17.0] | +12.7 [9.2, 16.5] | +7.5 [4.8, 10.3] | +7.5 [4.7, 10.7] | +9.5 [6.2, 13.2] | +13.5 [9.5, 17.7] |

### Own-confidence benchmark: verdict changes made, of those the critic's stated P(error) at `br50` predicts (sample 0)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 0 of 0 (+4 unpredicted, 0 wrong way) | 0 of 0 (+13 unpredicted, 5 wrong way) | 0 of 0 (+8 unpredicted, 7 wrong way) | 0 of 0 (+3 unpredicted, 1 wrong way) | 0 of 0 (+7 unpredicted, 5 wrong way) | 0 of 0 (+11 unpredicted, 1 wrong way) |
| gemma4:12b-think-bf16-t1 | 2 of 6 (+5 unpredicted, 6 wrong way) | 2 of 6 (+4 unpredicted, 5 wrong way) | 1 of 6 (+2 unpredicted, 8 wrong way) | 3 of 6 (+1 unpredicted, 7 wrong way) | 2 of 6 (+7 unpredicted, 7 wrong way) | 2 of 6 (+7 unpredicted, 4 wrong way) |
| gpt-6-luna-think | 1 of 1 (+5 unpredicted, 7 wrong way) | 1 of 1 (+8 unpredicted, 7 wrong way) | 1 of 1 (+7 unpredicted, 4 wrong way) | 1 of 1 (+7 unpredicted, 4 wrong way) | 0 of 1 (+6 unpredicted, 6 wrong way) | 1 of 1 (+7 unpredicted, 5 wrong way) |
| gpt-6.1-sol-think | 3 of 8 (+1 unpredicted, 1 wrong way) | 3 of 8 (+1 unpredicted, 1 wrong way) | 3 of 8 (+0 unpredicted, 0 wrong way) | 3 of 8 (+0 unpredicted, 1 wrong way) | 3 of 8 (+0 unpredicted, 0 wrong way) | 5 of 8 (+0 unpredicted, 0 wrong way) |
| haiku-5.5-think | 2 of 27 (+2 unpredicted, 2 wrong way) | 5 of 27 (+1 unpredicted, 4 wrong way) | 5 of 27 (+1 unpredicted, 5 wrong way) | 4 of 27 (+0 unpredicted, 1 wrong way) | 6 of 27 (+1 unpredicted, 1 wrong way) | 4 of 27 (+1 unpredicted, 5 wrong way) |
| opus-5.5-think | 10 of 37 (+0 unpredicted, 0 wrong way) | 7 of 37 (+0 unpredicted, 1 wrong way) | 12 of 37 (+0 unpredicted, 2 wrong way) | 8 of 37 (+0 unpredicted, 2 wrong way) | 9 of 37 (+0 unpredicted, 3 wrong way) | 7 of 37 (+0 unpredicted, 3 wrong way) |
| qwen3.5:4b-nothink-bf16-t1 | 2 of 16 (+25 unpredicted, 1 wrong way) | 3 of 16 (+41 unpredicted, 27 wrong way) | 3 of 16 (+41 unpredicted, 31 wrong way) | 0 of 16 (+18 unpredicted, 5 wrong way) | 1 of 16 (+38 unpredicted, 1 wrong way) | 0 of 16 (+33 unpredicted, 3 wrong way) |
| qwen3.5:4b-think-bf16-t1 | 1 of 6 (+15 unpredicted, 5 wrong way) | 3 of 6 (+14 unpredicted, 2 wrong way) | 1 of 6 (+8 unpredicted, 7 wrong way) | 2 of 6 (+7 unpredicted, 6 wrong way) | 1 of 6 (+17 unpredicted, 2 wrong way) | 3 of 6 (+16 unpredicted, 4 wrong way) |
| qwen3.5:9b-nothink-bf16-t1 | 0 of 0 (+9 unpredicted, 0 wrong way) | 0 of 0 (+32 unpredicted, 21 wrong way) | 0 of 0 (+30 unpredicted, 27 wrong way) | 0 of 0 (+11 unpredicted, 5 wrong way) | 0 of 0 (+13 unpredicted, 4 wrong way) | 0 of 0 (+12 unpredicted, 2 wrong way) |
| qwen3.5:9b-think-bf16-t1 | 1 of 4 (+14 unpredicted, 4 wrong way) | 1 of 4 (+13 unpredicted, 3 wrong way) | 1 of 4 (+9 unpredicted, 4 wrong way) | 1 of 4 (+16 unpredicted, 4 wrong way) | 0 of 4 (+11 unpredicted, 5 wrong way) | 1 of 4 (+14 unpredicted, 6 wrong way) |
| qwen3.5:27b-nothink-bf16-t1 | 0 of 0 (+9 unpredicted, 1 wrong way) | 0 of 0 (+32 unpredicted, 20 wrong way) | 0 of 0 (+30 unpredicted, 23 wrong way) | 0 of 0 (+9 unpredicted, 2 wrong way) | 0 of 0 (+12 unpredicted, 1 wrong way) | 0 of 0 (+10 unpredicted, 1 wrong way) |
| qwen3.5:27b-think-bf16-t1 | 8 of 10 (+20 unpredicted, 2 wrong way) | 6 of 10 (+22 unpredicted, 3 wrong way) | 7 of 10 (+10 unpredicted, 3 wrong way) | 5 of 10 (+12 unpredicted, 4 wrong way) | 7 of 10 (+14 unpredicted, 3 wrong way) | 8 of 10 (+23 unpredicted, 3 wrong way) |

### Stated P(error) shift in log-odds, 90% minus 10% (a calibrated Bayesian: 4.39 before clipping at 1 and 99)

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | +0.19 [0.08, 0.34] | +0.38 [0.21, 0.59] | +0.06 [-0.01, 0.14] | +0.14 [0.03, 0.28] | +0.14 [0.06, 0.24] | +0.31 [0.15, 0.50] |
| gemma4:12b-think-bf16-t1 | +0.06 [-0.08, 0.22] | +0.04 [-0.09, 0.17] | -0.08 [-0.22, 0.05] | -0.05 [-0.16, 0.07] | +0.19 [0.05, 0.35] | +0.17 [0.02, 0.33] |
| gpt-6-luna-think | +0.04 [-0.06, 0.16] | +0.08 [-0.01, 0.20] | +0.11 [-0.01, 0.24] | +0.04 [-0.07, 0.16] | +0.06 [-0.06, 0.17] | +0.17 [0.06, 0.31] |
| gpt-6.1-sol-think | +0.13 [0.06, 0.23] | +0.10 [0.03, 0.19] | +0.09 [0.02, 0.17] | +0.07 [0.02, 0.12] | +0.11 [0.05, 0.20] | +0.15 [0.07, 0.26] |
| haiku-5.5-think | +0.18 [0.12, 0.24] | +0.15 [0.09, 0.21] | +0.06 [0.01, 0.12] | +0.22 [0.17, 0.28] | +0.24 [0.19, 0.30] | +0.24 [0.17, 0.31] |
| opus-5.5-think | +0.55 [0.47, 0.63] | +0.48 [0.41, 0.56] | +0.44 [0.36, 0.52] | +0.42 [0.35, 0.49] | +0.37 [0.29, 0.44] | +0.41 [0.33, 0.49] |
| qwen3.5:4b-nothink-bf16-t1 | +1.10 [0.87, 1.34] | +0.83 [0.63, 1.05] | +0.62 [0.45, 0.80] | +0.37 [0.24, 0.51] | +1.98 [1.69, 2.28] | +1.14 [0.95, 1.36] |
| qwen3.5:4b-think-bf16-t1 | +0.50 [0.30, 0.73] | +0.56 [0.35, 0.78] | +0.06 [-0.08, 0.22] | +0.16 [0.00, 0.32] | +0.65 [0.43, 0.90] | +0.58 [0.34, 0.86] |
| qwen3.5:9b-nothink-bf16-t1 | +0.58 [0.41, 0.76] | +0.49 [0.32, 0.69] | +0.10 [-0.01, 0.23] | +0.50 [0.34, 0.67] | +0.62 [0.46, 0.81] | +0.55 [0.38, 0.72] |
| qwen3.5:9b-think-bf16-t1 | +0.41 [0.22, 0.60] | +0.50 [0.31, 0.72] | +0.15 [-0.00, 0.33] | +0.63 [0.40, 0.87] | +0.37 [0.21, 0.55] | +0.56 [0.34, 0.80] |
| qwen3.5:27b-nothink-bf16-t1 | +0.35 [0.24, 0.47] | +0.49 [0.35, 0.64] | +0.28 [0.17, 0.41] | +0.44 [0.33, 0.55] | +0.53 [0.40, 0.67] | +0.69 [0.53, 0.83] |
| qwen3.5:27b-think-bf16-t1 | +1.05 [0.79, 1.32] | +1.01 [0.77, 1.27] | +0.60 [0.42, 0.81] | +0.69 [0.49, 0.92] | +0.85 [0.63, 1.08] | +1.12 [0.87, 1.40] |

### Verdicts that flip between the 10% and the 90% version (sample 0): toward "error" at 90% / toward "correct" at 90%

| critic | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 4 / 0 of 199 | 9 / 0 of 200 | 3 / 1 of 200 | 4 / 1 of 200 | 2 / 0 of 200 | 10 / 0 of 200 |
| gemma4:12b-think-bf16-t1 | 4 / 3 of 199 | 4 / 3 of 194 | 2 / 7 of 197 | 0 / 3 of 196 | 5 / 3 of 196 | 6 / 1 of 193 |
| gpt-6-luna-think | 2 / 3 of 200 | 4 / 2 of 200 | 4 / 0 of 200 | 6 / 2 of 200 | 2 / 2 of 200 | 3 / 0 of 200 |
| gpt-6.1-sol-think | 3 / 0 of 200 | 3 / 0 of 200 | 3 / 0 of 200 | 2 / 0 of 200 | 3 / 0 of 200 | 5 / 0 of 200 |
| haiku-5.5-think | 3 / 1 of 200 | 3 / 1 of 200 | 2 / 1 of 200 | 3 / 0 of 200 | 6 / 0 of 200 | 2 / 2 of 200 |
| opus-5.5-think | 10 / 0 of 200 | 6 / 0 of 200 | 10 / 0 of 200 | 6 / 0 of 200 | 6 / 0 of 200 | 4 / 0 of 200 |
| qwen3.5:4b-nothink-bf16-t1 | 26 / 0 of 200 | 17 / 0 of 200 | 13 / 0 of 200 | 13 / 0 of 200 | 38 / 0 of 200 | 30 / 0 of 200 |
| qwen3.5:4b-think-bf16-t1 | 12 / 1 of 200 | 15 / 0 of 200 | 4 / 2 of 200 | 4 / 1 of 200 | 16 / 0 of 200 | 16 / 1 of 200 |
| qwen3.5:9b-nothink-bf16-t1 | 9 / 0 of 200 | 11 / 0 of 199 | 4 / 1 of 200 | 6 / 0 of 200 | 10 / 1 of 200 | 10 / 0 of 200 |
| qwen3.5:9b-think-bf16-t1 | 13 / 2 of 200 | 11 / 0 of 200 | 8 / 2 of 200 | 13 / 0 of 200 | 10 / 4 of 199 | 13 / 4 of 200 |
| qwen3.5:27b-nothink-bf16-t1 | 8 / 0 of 200 | 12 / 0 of 200 | 8 / 1 of 200 | 7 / 0 of 200 | 11 / 0 of 200 | 9 / 0 of 200 |
| qwen3.5:27b-think-bf16-t1 | 26 / 0 of 197 | 25 / 0 of 198 | 15 / 1 of 200 | 14 / 1 of 199 | 19 / 1 of 195 | 29 / 1 of 198 |

### A rate against a claim: shift from `neutral` toward flagging, original labels

| critic | told 90% of the batch | told 90% for this solution | "This solution contains an error." |
|---|---|---|---|
| gemma4:12b-nothink-bf16-t1 | +0.09 [0.01, 0.17] | +0.23 [0.12, 0.36] | +0.27 [0.14, 0.42] |
| gemma4:12b-think-bf16-t1 | -0.13 [-0.31, 0.02] | +0.07 [-0.04, 0.22] | -0.03 [-0.25, 0.13] |
| gpt-6-luna-think | +0.07 [-0.02, 0.18] | +0.19 [0.02, 0.41] | +0.19 [-0.03, 0.44] |
| gpt-6.1-sol-think | -0.02 [-0.05, 0.00] | +0.01 [0.00, 0.05] | +1.59 [1.47, 1.72] |
| haiku-5.5-think | -0.04 [-0.08, 0.00] | +0.01 [-0.03, 0.06] | +0.02 [-0.03, 0.07] |
| opus-5.5-think | +0.28 [0.03, 0.50] | +0.28 [0.03, 0.50] | +1.32 [0.98, 1.62] |
| qwen3.5:4b-nothink-bf16-t1 | +0.35 [0.21, 0.52] | +0.49 [0.34, 0.69] | +0.28 [0.14, 0.43] |
| qwen3.5:4b-think-bf16-t1 | +0.39 [0.19, 0.55] | +0.43 [0.23, 0.60] | +0.29 [0.06, 0.50] |
| qwen3.5:9b-nothink-bf16-t1 | +0.25 [0.10, 0.43] | +0.15 [0.02, 0.31] | +0.30 [0.17, 0.44] |
| qwen3.5:9b-think-bf16-t1 | +0.19 [0.12, 0.29] | +0.21 [0.13, 0.30] | +0.23 [0.14, 0.33] |
| qwen3.5:27b-nothink-bf16-t1 | +0.15 [0.03, 0.27] | +0.14 [0.00, 0.28] | +0.14 [0.02, 0.27] |
| qwen3.5:27b-think-bf16-t1 | +0.36 [0.26, 0.46] | +0.32 [0.23, 0.43] | +0.39 [0.29, 0.50] |

### What under-use costs if the stated rate were true: accuracy (%) for `br`, original labels

Critic's verdicts under that line / its neutral verdicts / ideal observer with its d′.

| critic | true rate 10% | true rate 90% |
|---|---|---|
| gemma4:12b-nothink-bf16-t1 | 85.2 / 85.3 / 95.1 | 94.0 / 93.3 / 95.1 |
| gemma4:12b-think-bf16-t1 | 91.3 / 90.3 / 97.7 | 97.2 / 98.0 / 97.7 |
| gpt-6-luna-think | 81.4 / 82.1 / 96.0 | 96.8 / 96.2 / 96.0 |
| gpt-6.1-sol-think | 78.3 / 75.7 / 97.2 | 97.4 / 97.3 / 97.2 |
| haiku-5.5-think | 86.8 / 84.1 / 97.9 | 98.4 / 98.2 / 97.9 |
| opus-5.5-think | 90.9 / 86.4 / 97.2 | 98.1 / 97.6 / 97.2 |
| qwen3.5:4b-nothink-bf16-t1 | 55.4 / 58.7 / 91.2 | 89.5 / 88.6 / 91.2 |
| qwen3.5:4b-think-bf16-t1 | 86.8 / 87.0 / 97.3 | 97.5 / 97.7 / 97.3 |
| qwen3.5:9b-nothink-bf16-t1 | 64.8 / 63.9 / 91.6 | 91.9 / 88.6 / 91.6 |
| qwen3.5:9b-think-bf16-t1 | 84.1 / 85.6 / 98.0 | 97.3 / 98.4 / 98.0 |
| qwen3.5:27b-nothink-bf16-t1 | 79.8 / 81.3 / 93.5 | 90.2 / 89.3 / 93.5 |
| qwen3.5:27b-think-bf16-t1 | 83.4 / 82.6 / 97.8 | 95.6 / 98.1 / 97.8 |

### Thinking on − off in ρ, paired, original labels

| critic (thinking on) | br | freq | comp | hist | user | item |
|---|---|---|---|---|---|---|
| gemma4:12b-think-bf16-t1 | -0.00 [-0.20, 0.16] | -0.16 [-0.35, -0.04] | -0.04 [-0.19, 0.09] | -0.16 [-0.33, 0.03] | +0.18 [0.04, 0.30] | +0.10 [-0.05, 0.29] |
| qwen3.5:4b-think-bf16-t1 | -0.00 [-0.09, 0.08] | +0.19 [0.00, 0.32] | +0.10 [-0.08, 0.21] | +0.11 [-0.05, 0.24] | +0.02 [-0.16, 0.17] | +0.19 [0.00, 0.33] |
| qwen3.5:9b-think-bf16-t1 | +0.12 [-0.01, 0.25] | +0.18 [0.06, 0.31] | +0.19 [-0.01, 0.37] | +0.13 [0.05, 0.23] | +0.03 [-0.05, 0.10] | +0.08 [-0.01, 0.16] |
| qwen3.5:27b-think-bf16-t1 | +0.29 [0.16, 0.44] | +0.20 [0.12, 0.30] | +0.28 [0.08, 0.44] | +0.18 [0.05, 0.32] | +0.20 [0.07, 0.33] | +0.37 [0.16, 0.55] |

## Pipeline rules (original labels)

- **Unparsed:** qwen3.5:27b-think-bf16-t1, presuppose: 2.0% (over 2%). Shift from neutral with those trials counted as error: -0.47; correct: -0.28.
- **Unparsed:** qwen3.5:27b-think-bf16-t1, claim_mistake: 3.7% (over 2%). Shift from neutral with those trials counted as error: -0.62; correct: -0.38.

