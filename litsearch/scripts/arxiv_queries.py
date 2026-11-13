#!/usr/bin/env python3
"""Build the arXiv API query plan for the `arxiv` stream (PROTOCOL.md blocks A, B, C).

Usage: python3 -I arxiv_queries.py <out_dir>
Writes <out_dir>/queries_main.jsonl (abstract and title queries plus targeted queries)
and <out_dir>/queries_recency.jsonl (Oct 15 - Nov 6, 2026 sweep).

Notes on the arXiv API (verified with count probes on 2026-11-06):
- abs:/ti: terms are stemmed (Porter-like): verifier = verifiers = verify; critic = critical;
  reviewer = review; monitor = monitoring; judge = judges; "language model" = "language models".
  So plural forms need no expansion, but different stems do (lenient vs leniency, sycophancy vs
  sycophantic, presuppose vs presupposition, skeptical vs sceptical).
- max_results=0 returns HTTP 500, so count probes use max_results=1.
"""
import json
import os
import sys

DATE = "submittedDate:[202201010000 TO 202611062359]"
DATE_RECENT = "submittedDate:[202610150000 TO 202611062359]"

# Block A as an OR list: PROTOCOL.md block A plus `judge` and "process reward" from the
# protocol's arXiv-specific form ("critic, verifier, judge, self-correction, process reward").
A_TERMS = ['critic', 'verifier', 'judge', '"LLM judge"', '"LLM-as-a-judge"', '"process reward"',
           '"self-correction"', '"self-critique"', '"error detection"', 'reviewer', 'overseer', 'monitor']
LLM_TERMS = ['"language model"', 'LLM', 'LLMs']

# Block B (measurement) and C (manipulation) with word-form expansions (different stems only).
B_TERMS = [
    ("B01", '"signal detection"'),
    ("B02a", '"d-prime"'),
    ("B02b", '"d prime"'),
    ("B03", 'sensitivity'),
    ("B04", '"response bias"'),
    ("B05a", '"decision criterion"'),
    ("B05b", '"decision criteria"'),
    ("B06", '"decision threshold"'),
    ("B07", '"operating point"'),
    ("B08", '"false alarm"'),
    ("B09a", '"false positive rate"'),
    ("B09b", '"false positive"'),          # addition: counterpart wording of "false positive rate"
    ("B10a", 'ROC'),
    ("B10b", 'AUROC'),                     # word form of ROC (area under ROC)
    ("B11", '"base rate"'),
    ("B12", 'prior'),
    ("B13", 'payoff'),
    ("B14", '"asymmetric cost"'),
    ("B15", '"ideal observer"'),
    ("B16a", 'conservatism'),
    ("B16b", 'conservative'),              # word form of conservatism
    ("B17", 'specificity'),                # addition: counterpart of sensitivity (both error types)
]
C_TERMS = [
    ("C01a", 'strict'),
    ("C01b", 'stricter'),
    ("C02a", 'lenient'),
    ("C02b", 'leniency'),
    ("C03a", 'harsh'),
    ("C03b", 'harsher'),
    ("C04a", 'skeptical'),
    ("C04b", 'sceptical'),
    ("C04c", 'scepticism'),
    ("C05", '"devil\'s advocate"'),
    ("C06", 'adversarial'),
    ("C07a", 'presuppose'),
    ("C07b", 'presupposition'),
    ("C08", 'persona'),
    ("C09", 'stakes'),
    ("C10", 'framing'),
    ("C11", '"prompt sensitivity"'),
    ("C12a", 'sycophancy'),
    ("C12b", 'sycophantic'),
    ("C13a", '"over-critical"'),
    ("C13b", 'overcritical'),
    ("C13c", '"overly critical"'),
    ("C14", '"false rejection"'),
]

# Targeted queries from the task brief (abstract field).
TARGETED = [
    ("T1", '(abs:"signal detection") AND (abs:LLM OR abs:"language model")'),
    ("T2", '(abs:"ideal observer") AND (abs:LLM OR abs:"language model")'),
    ("T3", '(abs:"base rate" OR abs:"base-rate" OR abs:"prior probability") AND (abs:judge OR abs:verifier OR '
           'abs:critic OR abs:grader OR abs:"reward model" OR abs:classifier) AND (abs:LLM OR abs:"language model")'),
    ("T4", '(abs:payoff OR abs:"asymmetric cost" OR abs:"cost-sensitive" OR abs:utility) AND (abs:judge OR '
           'abs:verifier OR abs:critic) AND (abs:LLM OR abs:"language model")'),
    ("T5", '(abs:"d prime" OR abs:"criterion shift" OR abs:"response bias" OR abs:"decision criterion" OR '
           'abs:"decision threshold") AND (abs:LLM OR abs:"language model")'),
    ("T6", '(abs:ROC OR abs:AUROC OR abs:"operating point") AND (abs:judge OR abs:verifier OR abs:critic OR '
           'abs:"process reward") AND (abs:logprob OR abs:"token probability" OR abs:confidence)'),
    ("T7", '(abs:ProcessBench) AND (abs:"false positive" OR abs:"false alarm" OR abs:"over-critical" OR '
           'abs:specificity)'),
]

# Extra targeted queries added by the arxiv stream (not in the brief): synonyms that the protocol's
# terms miss, and the claims C5, C6 and C8. Abstract field unless stated.
SYS = ('(abs:judge OR abs:verifier OR abs:critic OR abs:grader OR abs:"reward model" OR abs:monitor OR '
       'abs:evaluator OR abs:"self-correction" OR abs:"self-verification")')
LLMQ = '(abs:LLM OR abs:"language model")'
EXTRA = [
    ("X01", f'(abs:prevalence OR abs:"class prior" OR abs:"label shift" OR abs:"prior shift") AND {SYS} AND {LLMQ}'),
    ("X02", f'(abs:"type I error" OR abs:"type II error" OR abs:"type I and type II") AND {SYS} AND {LLMQ}'),
    ("X03", f'(abs:nitpick OR abs:nitpicks OR abs:"hallucinated errors" OR abs:"hallucinated bugs" OR '
            f'abs:"nonexistent errors" OR abs:"non-existent errors" OR abs:"spurious errors") AND {LLMQ}'),
    ("X04", f'(abs:criterion) AND (abs:judge OR abs:verifier OR abs:critic OR abs:grader OR abs:monitor) AND '
            f'(abs:bias OR abs:threshold OR abs:shift) AND {LLMQ}'),
    ("X05", f'(abs:"false negative") AND (abs:judge OR abs:verifier OR abs:critic OR abs:grader OR abs:monitor OR '
            f'abs:"process reward") AND {LLMQ}'),
    ("X06", f'(abs:"thinking mode" OR abs:"non-thinking" OR abs:"reasoning mode" OR abs:"extended thinking" OR '
            f'abs:"thinking budget" OR abs:"reasoning effort") AND (abs:judge OR abs:verifier OR abs:critic OR '
            f'abs:"reward model" OR abs:grader OR abs:monitor OR abs:"self-correction")'),
    ("X07", f'(abs:"inverse scaling") AND (abs:prior OR abs:"base rate" OR abs:"in-context" OR abs:sycophancy OR '
            f'abs:judge OR abs:verifier OR abs:critic)'),
    ("X08", f'(abs:"manipulation check" OR abs:"says and does" OR abs:"stated and revealed" OR '
            f'abs:"stated preferences" OR abs:"knowing-doing" OR abs:"knowing and doing") AND {LLMQ}'),
    ("X09", f'(abs:"base rate neglect" OR abs:"base-rate neglect" OR abs:"base rates") AND {LLMQ}'),
    ("X10", f'(abs:"expected utility" OR abs:"expected cost" OR abs:"Bayes optimal" OR abs:"Bayes-optimal") AND '
            f'(abs:judge OR abs:verifier OR abs:critic OR abs:grader OR abs:monitor OR abs:classifier) AND {LLMQ}'),
    ("X11", f'(abs:"leniency bias" OR abs:"severity bias" OR abs:"strictness bias" OR abs:"harshness" OR '
            f'abs:"overly strict" OR abs:"too strict" OR abs:"too lenient" OR abs:"overly lenient") AND {LLMQ}'),
    ("X12", f'(abs:"over-correction" OR abs:overcorrection OR abs:"over-flagging" OR abs:"over-refusal" OR '
            f'abs:"false error") AND (abs:verifier OR abs:critic OR abs:judge OR abs:"self-correction" OR '
            f'abs:"self-verification" OR abs:"process reward") AND {LLMQ}'),
    ("X13", f'(ti:judge OR ti:judges OR ti:verifier OR ti:critic OR ti:grader OR ti:"reward model" OR ti:monitor) '
            f'AND (ti:threshold OR ti:criterion OR ti:calibration OR ti:calibrated OR ti:"decision") AND {LLMQ}'),
    ("X14", f'(abs:"metacognitive sensitivity" OR abs:"meta-d" OR abs:"type 2 sensitivity" OR '
            f'abs:"metacognitive efficiency") AND {LLMQ}'),
]

RECENCY_CATS = ["cs.CL", "cs.AI", "cs.LG", "cs.SE", "cs.HC", "cs.CY"]
RECENCY_TERMS = ['judge', 'verifier', 'critic', 'critique', '"reward model"', '"self-correct"',
                 '"self-correction"', '"self-correcting"', '"self-refine"', '"self-refinement"',
                 'reviewer', 'overseer', 'monitor', 'grader']


def orlist(prefix, terms):
    return "(" + " OR ".join(f"{prefix}:{t}" for t in terms) + ")"


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    A_abs, L_abs = orlist("abs", A_TERMS), orlist("abs", LLM_TERMS)
    A_any = "(" + " OR ".join([f"abs:{t}" for t in A_TERMS] + [f"ti:{t}" for t in A_TERMS]) + ")"
    L_any = "(" + " OR ".join([f"abs:{t}" for t in LLM_TERMS] + [f"ti:{t}" for t in LLM_TERMS]) + ")"
    rows = []
    for block, terms in (("B", B_TERMS), ("C", C_TERMS)):
        for code, t in terms:
            rows.append({"qid": f"{code}_abs", "block": block, "term": t, "field": "abs",
                         "query": f"(abs:{t}) AND {A_abs} AND {L_abs} AND {DATE}"})
    for block, terms in (("B", B_TERMS), ("C", C_TERMS)):
        for code, t in terms:
            rows.append({"qid": f"{code}_ti", "block": block, "term": t, "field": "ti",
                         "query": f"(ti:{t}) AND {A_any} AND {L_any} AND {DATE}"})
    for code, q in TARGETED:
        rows.append({"qid": code, "block": "T", "term": code, "field": "abs", "query": f"{q} AND {DATE}"})
    with open(os.path.join(out_dir, "queries_main.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    with open(os.path.join(out_dir, "queries_extra.jsonl"), "w", encoding="utf-8") as fh:
        for code, q in EXTRA:
            fh.write(json.dumps({"qid": code, "block": "X", "term": code, "field": "abs/ti",
                                 "query": f"{q} AND {DATE}"}) + "\n")
    cats = "(" + " OR ".join(f"cat:{c}" for c in RECENCY_CATS) + ")"
    terms = "(" + " OR ".join([f"ti:{t}" for t in RECENCY_TERMS] + [f"abs:{t}" for t in RECENCY_TERMS]) + ")"
    rec = [{"qid": "R1_recency", "block": "R", "term": "recency", "field": "ti+abs",
            "query": f"{cats} AND {terms} AND {DATE_RECENT}"},
           {"qid": "R0_recency_all", "block": "R", "term": "all submissions in categories", "field": "cat",
            "query": f"{cats} AND {DATE_RECENT}"}]
    with open(os.path.join(out_dir, "queries_recency.jsonl"), "w", encoding="utf-8") as fh:
        for r in rec:
            fh.write(json.dumps(r) + "\n")
    print(f"{len(rows)} main queries, {len(rec)} recency queries written to {out_dir}")


if __name__ == "__main__":
    main(sys.argv[1])
