#!/usr/bin/env python3
"""arXiv query plan for the claim-test addendum (claims P1-P5), run 2026-11-10.

Usage: python3 -I premise_arxiv_queries.py <out_dir>
Writes <out_dir>/queries_premise.jsonl (targeted, 2023-01-01 to 2026-11-10) and
<out_dir>/queries_premise_recency.jsonl (every submission in seven cs categories from
2026-10-01 to 2026-11-10 that mentions an evaluator or a premise/sycophancy term).

Harvest with the existing runner:
  ARXIV_MIN_GAP=6 python3 -I scripts/arxiv_harvest.py run raw/premise/arxiv/queries_premise.jsonl raw/premise/arxiv

The arXiv API stems every term (see arxiv_queries.py), so hits are re-matched literally by
premise_arxiv_screen.py before any title is read.
"""
import json
import os
import sys

DATE = "submittedDate:[202301010000 TO 202611102359]"
DATE_RECENT = "submittedDate:[202610010000 TO 202611102359]"

# Wider than the Nov 6 LLM block, which missed abstracts that say only "foundation models",
# "reasoning models" or "VLMs".
LLMQ = ('(abs:LLM OR abs:"language model" OR abs:"foundation model" OR abs:"reasoning model" OR '
        'abs:VLM OR abs:GPT OR abs:"AI agent" OR abs:"AI agents")')
EVAL = ('(abs:judge OR abs:verifier OR abs:critic OR abs:reviewer OR abs:grader OR abs:evaluator OR '
        'abs:monitor OR abs:auditor OR abs:overseer OR abs:"code review" OR abs:"peer review" OR '
        'abs:"error detection" OR abs:"process reward")')

Q = [
    # P1: sycophancy and false-presupposition acceptance (no evaluator block: read the whole field)
    ("P01", "sycophancy, all",
     '(abs:sycophancy OR abs:sycophantic OR ti:sycophancy OR ti:sycophantic)'),
    ("P02", "false premise / presupposition",
     '(abs:"false premise" OR abs:"false presupposition" OR abs:"false assumption" OR abs:presupposition OR '
     'abs:"loaded question" OR abs:"misleading premise" OR abs:"flawed premise" OR abs:"false-premise") AND ' + LLMQ),
    # P1/P3: anchoring of judges and reviewers by prior verdicts, hints, authority
    ("P03", "confirmation / anchoring / authority bias x evaluators",
     '(abs:"confirmation bias" OR abs:anchoring OR abs:"authority bias" OR abs:"bandwagon") AND ' + EVAL + ' AND ' + LLMQ),
    ("P04", "prior verdicts and reviews",
     '(abs:"prior verdict" OR abs:"prior judgment" OR abs:"previous review" OR abs:"prior review" OR '
     'abs:"previous reviewer" OR abs:"pre-screening" OR abs:"prior label" OR abs:"prior assessment" OR '
     'abs:"suggested verdict" OR abs:"prior decision" OR abs:"earlier verdict" OR abs:"first-pass") AND '
     + EVAL + ' AND ' + LLMQ),
    # P1/P2: "there is a bug" style prompts
    # (A phrase query for "contains an error", "there is a bug", ... returned 15,156 hits on the probe: the
    # API drops the stop words and stems the rest. Replaced by this AND form; the phrases are matched
    # literally in premise_arxiv_screen.py instead.)
    ("P05", "evaluator told / asserted that an error exists, with false positives",
     '(abs:told OR abs:asserted OR abs:asserting OR abs:presupposed OR abs:informed OR abs:"pre-labeled" OR '
     'abs:claimed) AND (abs:error OR abs:bug OR abs:mistake OR abs:flaw OR abs:vulnerability) AND ' + EVAL +
     ' AND (abs:"false positive" OR abs:"false alarm" OR abs:"false rejection" OR abs:specificity OR '
     'abs:"over-flagging" OR abs:hallucinated OR abs:"correct solutions" OR abs:"correct code") AND ' + LLMQ),
    ("P06", "false positives in error / bug / proof checking",
     '(abs:"false positive" OR abs:"false alarm" OR abs:"false rejection" OR abs:"hallucinated bug" OR '
     'abs:"hallucinated error" OR abs:"nonexistent bug" OR abs:"nonexistent error" OR abs:"phantom") AND '
     '(abs:"error detection" OR abs:"bug detection" OR abs:"mistake detection" OR abs:"code review" OR '
     'abs:"proof verification" OR abs:"proof checking" OR abs:"error identification" OR '
     'abs:"vulnerability detection" OR abs:"fault localization" OR abs:"proof grading") AND ' + LLMQ),
    ("P07", "code review x bias terms",
     '(abs:"code review" OR abs:"vulnerability detection" OR abs:"bug detection" OR abs:"program repair" OR '
     'abs:"code audit" OR abs:"security audit") AND (abs:sycophancy OR abs:framing OR abs:"confirmation bias" OR '
     'abs:anchoring OR abs:deference OR abs:"false premise" OR abs:misleading OR abs:presupposition OR '
     'abs:"cognitive bias") AND ' + LLMQ),
    ("P08", "proof / math checking x premise terms",
     '(abs:proof OR abs:theorem OR abs:mathematical OR abs:math) AND (abs:verifier OR abs:verification OR '
     'abs:grading OR abs:grader OR abs:"error detection" OR abs:critic OR abs:judge) AND (abs:sycophancy OR '
     'abs:"false premise" OR abs:presupposition OR abs:misleading OR abs:hint OR abs:framing OR abs:deference OR '
     'abs:"false claim") AND ' + LLMQ),
    # P4: numeric priors vs categorical assertions
    ("P09", "Bayesian updating x assertion / testimony",
     '(abs:"base rate" OR abs:prior OR abs:likelihood OR abs:probability) AND (abs:assertion OR abs:testimony OR '
     'abs:verbal OR abs:categorical OR abs:"stated") AND (abs:Bayesian OR abs:"belief updating" OR '
     'abs:"belief revision" OR abs:"belief update") AND ' + LLMQ),
    ("P18", "verbal probability and epistemic markers in prompts",
     '(abs:"verbal probability" OR abs:"estimative probability" OR abs:"linguistic uncertainty" OR '
     'abs:"epistemic markers" OR abs:"uncertainty expressions" OR abs:"probability phrases" OR '
     'abs:"expressions of uncertainty" OR abs:"certainty markers") AND ' + LLMQ),
    # P5: signal-detection readings of sycophancy / deference
    ("P10", "SDT x sycophancy / deference / persuasion",
     '(abs:"signal detection" OR abs:"decision criterion" OR abs:"response bias" OR abs:"criterion shift" OR '
     'abs:"d-prime" OR abs:"decision threshold" OR abs:"response criterion") AND (abs:sycophancy OR '
     'abs:sycophantic OR abs:"false premise" OR abs:deference OR abs:"social pressure" OR abs:persuasion OR '
     'abs:conformity OR abs:suggestion OR abs:suggestibility OR abs:assertion) AND ' + LLMQ),
    # P3: source reliability, discounting, uninformative claims
    ("P12", "source reliability x deference",
     '(abs:"source reliability" OR abs:"source credibility" OR abs:"unreliable source" OR '
     'abs:"epistemic vigilance" OR abs:uninformative OR abs:"source attribution" OR abs:provenance OR '
     'abs:"source trust") AND (abs:deference OR abs:sycophancy OR abs:hint OR abs:assertion OR '
     'abs:"false claim" OR abs:misleading OR abs:conformity OR abs:"false information") AND ' + LLMQ),
    ("P13", "deference / over-trust x evaluators",
     '(abs:deference OR abs:defer OR abs:"over-trust" OR abs:overtrust OR abs:overreliance OR abs:gullible OR '
     'abs:gullibility OR abs:credulous OR abs:credulity) AND ' + EVAL + ' AND ' + LLMQ),
    ("P14", "hints and cues x reasoning models",
     '(abs:hint OR abs:hints OR abs:cue) AND (abs:"reasoning model" OR abs:"extended thinking" OR '
     'abs:"thinking mode" OR abs:"reasoning models") AND (abs:faithfulness OR abs:sycophancy OR abs:bias OR '
     'abs:deference)'),
    ("P15", "system-prompt authority x false claims",
     '(abs:"system prompt" OR abs:"system message" OR abs:"instruction hierarchy" OR abs:"developer message") '
     'AND (abs:"false claim" OR abs:"false information" OR abs:misinformation OR abs:"incorrect claim" OR '
     'abs:assertion OR abs:"false premise" OR abs:sycophancy OR abs:deference) AND ' + LLMQ),
    ("P16", "self-correction x presupposed error",
     '(abs:"self-correction" OR abs:"self-refine" OR abs:"self-refinement" OR abs:"self-verification" OR '
     'abs:"self-critique" OR abs:"self-review") AND (abs:"correct to incorrect" OR '
     'abs:"correct answers to incorrect" OR abs:"false positive" OR abs:"over-correction" OR '
     'abs:"feedback prompt" OR abs:"find problems" OR abs:"find the mistake" OR abs:sycophancy) AND ' + LLMQ),
    ("P19", "LLM-judge bias suites",
     '(abs:"LLM-as-a-judge" OR abs:"LLM judge" OR abs:"LLM judges" OR abs:"agent-as-a-judge" OR '
     'abs:"LLM evaluators" OR abs:"LLM evaluator") AND (abs:"authority bias" OR abs:sycophancy OR '
     'abs:bandwagon OR abs:anchoring OR abs:"confirmation bias" OR abs:hint OR abs:deference OR '
     'abs:"false premise" OR abs:presupposition)'),
    ("P20", "accusations / asserted failure in agents",
     '(abs:"false accusation" OR abs:"false accusations" OR abs:"falsely accused" OR abs:"false feedback" OR '
     'abs:"misleading feedback" OR abs:"incorrect feedback" OR abs:"false error report" OR abs:"false bug report") '
     'AND ' + LLMQ),
]

# Bayesian and base-rate reasoning since 2026-10-01 (the Nov 6 `adjacent` stream covers earlier work).
Q_RECENT = [
    ("P17", "Bayesian / base-rate reasoning, Oct 1 on",
     '(abs:"base rate" OR abs:"Bayesian reasoning" OR abs:"Bayesian inference" OR abs:"belief updating" OR '
     'abs:"prior probability" OR abs:"Bayes rule" OR abs:"probabilistic reasoning") AND ' + LLMQ),
]

RECENCY_CATS = ["cs.CL", "cs.AI", "cs.LG", "cs.SE", "cs.HC", "cs.CY", "cs.CR"]
RECENCY_TERMS = [
    # the Nov 6 evaluator terms
    'judge', 'verifier', 'critic', 'critique', '"reward model"', '"self-correct"', '"self-correction"',
    '"self-correcting"', '"self-refine"', '"self-refinement"', 'reviewer', 'overseer', 'monitor', 'grader',
    # added for the claim test
    'evaluator', 'auditor', '"error detection"', '"code review"', '"bug detection"', '"vulnerability detection"',
    'sycophancy', 'sycophantic', 'presupposition', '"false premise"', 'deference', 'anchoring',
    '"confirmation bias"', '"base rate"', 'gullible', '"false positive"', '"false alarm"',
]


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "queries_premise.jsonl"), "w", encoding="utf-8") as fh:
        for qid, label, q in Q:
            fh.write(json.dumps({"qid": qid, "label": label, "query": f"{q} AND {DATE}"}) + "\n")
        for qid, label, q in Q_RECENT:
            fh.write(json.dumps({"qid": qid, "label": label, "query": f"{q} AND {DATE_RECENT}"}) + "\n")
    cats = "(" + " OR ".join(f"cat:{c}" for c in RECENCY_CATS) + ")"
    terms = "(" + " OR ".join([f"ti:{t}" for t in RECENCY_TERMS] + [f"abs:{t}" for t in RECENCY_TERMS]) + ")"
    with open(os.path.join(out_dir, "queries_premise_recency.jsonl"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"qid": "PR1_recency", "label": "recency sweep, Oct 1 - Nov 10, 2026",
                             "query": f"{cats} AND {terms} AND {DATE_RECENT}"}) + "\n")
    print(f"{len(Q) + len(Q_RECENT)} targeted queries and 1 recency query written to {out_dir}")


if __name__ == "__main__":
    main(sys.argv[1])
