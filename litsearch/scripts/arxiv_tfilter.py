#!/usr/bin/env python3
"""Literal re-match of the targeted (T) and extra (X) queries' own term groups.

Usage: python3 -I arxiv_tfilter.py <ranked.jsonl> <query_hits.json> <screened_ids.txt> <out_tsv> [qid ...]

The API stems terms (utility = utilize, critic = critical, ...). For each targeted query this keeps the
records returned by that query whose title+abstract literally match every AND-group of the query, and
writes them (with a flag for whether their title was already read) so every such title can be read.
"""
import json
import re
import sys

LLM = r"\blanguage models?\b|\bLLMs?\b|\bGPT|\bChatGPT\b|\bfoundation models?\b|\bVLMs?\b|\bMLLMs?\b"
SYS = r"\bjudg(?:e|es)\b|\bverifiers?\b|\bcritics?\b|\bgraders?\b|\breward models?\b|\bmonitors?\b|\bevaluators?\b|\bself[- ]correct\w*|\bself[- ]verif\w*|\bclassifiers?\b|\bprocess[- ]reward"
GROUPS = {
    "T1": [r"\bsignal[- ]detection\b", LLM],
    "T2": [r"\bideal[- ]observers?\b", LLM],
    "T3": [r"\bbase[- ]rates?\b|\bprior probabilit\w*", r"\bjudg(?:e|es)\b|\bverifiers?\b|\bcritics?\b|\bgraders?\b|\breward models?\b|\bclassifiers?\b", LLM],
    "T4": [r"\bpay[- ]?offs?\b|\basymmetric costs?\b|\bcost[- ]sensitive\b|\butilit(?:y|ies)\b", r"\bjudg(?:e|es)\b|\bverifiers?\b|\bcritics?\b", LLM],
    "T5": [r"\bd[- ]prime\b|\bcriterion shifts?\b|\bresponse bias\w*|\bdecision criteri\w*|\bdecision thresholds?\b", LLM],
    "T6": [r"\bROC\b|\bAUROC\b|\boperating points?\b", r"\bjudg(?:e|es)\b|\bverifiers?\b|\bcritics?\b|\bprocess[- ]reward", r"\blog[- ]?probs?\b|\btoken probabilit\w*|\bconfidence\b"],
    "T7": [r"\bProcessBench\b", r"\bfalse[- ]positives?\b|\bfalse[- ]alarms?\b|\bover[- ]?critical\b|\bspecificity\b"],
    "X01": [r"\bprevalence\b|\bclass priors?\b|\blabel shift\b|\bprior shift\b", SYS, LLM],
    "X02": [r"\btype[- ]I\b|\btype[- ]II\b", SYS, LLM],
    "X03": [r"\bnitpick\w*|\bhallucinated (?:errors|bugs)\b|\bnon-?existent errors\b|\bspurious errors\b", LLM],
    "X04": [r"\bcriterion\b", r"\bjudg(?:e|es)\b|\bverifiers?\b|\bcritics?\b|\bgraders?\b|\bmonitors?\b", r"\bbias\w*|\bthresholds?\b|\bshift\w*", LLM],
    "X05": [r"\bfalse[- ]negatives?\b", r"\bjudg(?:e|es)\b|\bverifiers?\b|\bcritics?\b|\bgraders?\b|\bmonitors?\b|\bprocess[- ]reward", LLM],
    "X06": [r"\bthinking mode\b|\bnon-thinking\b|\breasoning mode\b|\bextended thinking\b|\bthinking budget\b|\breasoning effort\b", r"\bjudg(?:e|es)\b|\bverifiers?\b|\bcritics?\b|\breward models?\b|\bgraders?\b|\bmonitors?\b|\bself[- ]correct\w*"],
    "X07": [r"\binverse scaling\b", r"\bpriors?\b|\bbase[- ]rates?\b|\bin-context\b|\bsycophan\w*|\bjudg(?:e|es)\b|\bverifiers?\b|\bcritics?\b"],
    "X08": [r"\bmanipulation checks?\b|\bsays? and does\b|\bstated and revealed\b|\bstated preferences?\b|\bknowing[- ](?:and[- ])?doing\b", LLM],
    "X09": [r"\bbase[- ]rate neglect\b|\bbase[- ]rates\b", LLM],
    "X10": [r"\bexpected (?:utility|cost)\b|\bBayes[- ]optimal\b", r"\bjudg(?:e|es)\b|\bverifiers?\b|\bcritics?\b|\bgraders?\b|\bmonitors?\b|\bclassifiers?\b", LLM],
    "X11": [r"\bleniency bias\b|\bseverity bias\b|\bstrictness bias\b|\bharshness\b|\boverly strict\b|\btoo strict\b|\btoo lenient\b|\boverly lenient\b", LLM],
    "X12": [r"\bover-?correction\b|\bover-?flagging\b|\bover-?refusal\b|\bfalse errors?\b", SYS, LLM],
    "X13": [r"\bjudg(?:e|es)\b|\bverifiers?\b|\bcritics?\b|\bgraders?\b|\breward models?\b|\bmonitors?\b", r"\bthresholds?\b|\bcriterion\b|\bcalibrat\w*|\bdecision\w*", LLM],
    "X14": [r"\bmetacognitive (?:sensitivity|efficiency)\b|\bmeta-d\b|\btype[- ]2 sensitivity\b", LLM],
}


def main(ranked, hits_file, screened_file, out, qids):
    by = {}
    for l in open(ranked, encoding="utf-8"):
        r = json.loads(l)
        by[r["id"]] = r
    hits = json.load(open(hits_file, encoding="utf-8"))["hits"]
    screened = {l.strip() for l in open(screened_file, encoding="utf-8") if l.strip()}
    rows = []
    for q in qids or sorted(GROUPS):
        if q not in hits:
            continue
        rx = [re.compile(g, re.I) for g in GROUPS[q]]
        n_lit = 0
        for aid in hits[q]:
            r = by.get(aid)
            if not r:
                continue
            text = r["title"] + " \n " + r["abstract"]
            if all(x.search(text) for x in rx):
                n_lit += 1
                rows.append((q, aid, "screened" if aid in screened else "new", r["title"]))
        print(f"{q}: api={len(hits[q])} literal={n_lit} new={sum(1 for x in rows if x[0] == q and x[2] == 'new')}")
    with open(out, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write("\t".join(row) + "\n")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], a[2], a[3], a[4:])
