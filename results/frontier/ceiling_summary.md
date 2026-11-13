# Stage A ceiling check: Claude Sonnet 5.5

Neutral prompt, 40 items per set (10 per split x class), one sample each. Decision rule: hard set usable if misses and false alarms are each about 10% or more.

| set | thinking | misses | false alarms | d′ [95% CI] | AUC (p_error) | trials with thinking block | median output tokens | cost |
|---|---|---|---|---|---|---|---|---|
| easy | off | 0/20 | 1/20 | 3.45 [2.95, 3.96] | 1.000 | 0/40 | 137 | $0.117 |
| easy | on | 0/20 | 0/20 | 3.96 [3.96, 3.96] | 1.000 | 5/40 | 186 | $0.138 |
| hard | off | 2/20 | 2/20 | 2.36 [1.60, 3.45] | 0.975 | 0/40 | 230 | $0.216 |
| hard | on | 2/20 | 2/20 | 2.36 [1.60, 3.45] | 0.975 | 15/40 | 270 | $0.229 |

Open models on the same 40 easy items (Torch, neutral, T = 1):

| model | thinking | misses | false alarms | d′ [95% CI] |
|---|---|---|---|---|
| qwen 4b | off | 1/20 | 6/20 | 1.96 [1.21, 2.95] |
| qwen 4b | on | 2/20 | 0/20 | 3.16 [2.62, 3.96] |
| qwen 9b | off | 4/20 | 0/20 | 2.77 [2.22, 3.45] |
| qwen 9b | on | 1/19 | 0/20 | 3.42 [2.92, 3.94] |
| qwen 27b | off | 5/20 | 0/20 | 2.62 [2.10, 3.45] |
| qwen 27b | on | 1/19 | 0/20 | 3.42 [2.92, 3.94] |
| gemma 12b | off | 3/20 | 3/20 | 1.93 [1.21, 3.16] |
| gemma 12b | on | 1/19 | 0/20 | 3.42 [2.92, 3.94] |

Sonnet's wrong verdicts on the hard set (the same four items in both settings):

- miss `olympiadbench-674`: p_error 20 off / 22 on; first error step 2; final answer correct: True
- false alarm `olympiadbench-690`: p_error 70 off / 70 on; first error step -1; final answer correct: True
- miss `omnimath-543`: p_error 3 off / 3 on; first error step 0; final answer correct: True
- false alarm `omnimath-979`: p_error 50 off / 62 on; first error step -1; final answer correct: True
