#!/usr/bin/env python3
"""Pre-rank arXiv candidates by how many search blocks they match (literal word forms).

Usage: python3 -I arxiv_rank.py <candidates.jsonl> <out_dir> [--known known_papers.csv]

The arXiv API stems terms (critic = critical, reviewer = review, monitor = monitoring,
verifier = verify), so API hits are re-matched here on title + abstract with literal word-form
regexes for PROTOCOL.md blocks A (system), B (measurement) and C (manipulation), plus an LLM block.

Writes <out_dir>/ranked.jsonl (all candidates with match details, sorted) and
<out_dir>/ranked_titles.tsv (rank, tier, score, id, matched terms, title).

Tiers:
  1  A and strong-B and strong-C
  2  A and (strong-B or strong-C)
  3  A and only weak B/C terms (prior, sensitivity, adversarial, persona, stakes, framing, ...)
  4  no literal A term, but a strong B or C term (safety net; A_ext records extended system terms such
     as verify, evaluator, grader, reward model, classifier, detector for ranking only)
  5  everything else: API stemming over-reach only (e.g. critical, review, monitoring, sensitive,
     frame, 'based rating'), or a literal A term with no literal B/C term
"""
import csv
import json
import os
import re
import sys

def rx(p):
    return re.compile(p, re.I)

A = {
    "critic": rx(r"\bcritics?\b"),
    "critique": rx(r"\bcritiqu(?:e|es|ed|ing)\b"),
    "verifier": rx(r"\bverifiers?\b"),
    "judge": rx(r"\bjudges?\b|\bLLMs?[- ]as[- ](?:an?[- ])?judges?\b"),
    "process reward": rx(r"\bprocess[- ]reward|\bPRMs?\b"),
    "self-correction": rx(r"\bself[- ]?correct(?:ion|ions|ing|ive|s)?\b"),
    "self-critique": rx(r"\bself[- ]?critiqu\w*|\bself[- ]critic\w*"),
    "error detection": rx(r"\berror[- ]detect\w*|\bdetect(?:ing|s)? (?:the )?errors?\b|\berror detectors?\b"),
    "reviewer": rx(r"\breviewers?\b"),
    "overseer": rx(r"\boverseers?\b"),
    "monitor": rx(r"\bmonitor(?:s|ed|ing)?\b"),
}
A_ACTOR_CRITIC = rx(r"\bactor[- ]critic\b")
A_EXT = {  # extended system terms (safety net only)
    "verify": rx(r"\bverif(?:y|ies|ied|ying|ication|ications)\b|\bself[- ]verif\w*"),
    "evaluator": rx(r"\bevaluators?\b|\bLLM[- ]based evaluat\w*|\bauto[- ]?raters?\b|\bautoraters?\b"),
    "grader": rx(r"\bgraders?\b|\bgrading\b"),
    "reward model": rx(r"\breward models?\b|\bORMs?\b"),
    "classifier": rx(r"\bclassifiers?\b|\bguard(?:rail)? models?\b"),
    "detector": rx(r"\bdetectors?\b"),
    "assessor": rx(r"\bassessors?\b|\bscorers?\b"),
    "oversight": rx(r"\boversight\b"),
}
LLM = rx(r"\blanguage models?\b|\bLLMs?\b|\bGPT|\bChatGPT\b|\bfoundation models?\b|\bLM\b|\bVLMs?\b|\bMLLMs?\b")

B_STRONG = {
    "signal detection": rx(r"\bsignal[- ]detection\b|\bSDT\b"),
    "d-prime": rx(r"\bd[- ]prime\b|(?<![A-Za-z])d\s?['′’](?=[\s,;:.)\]]|$)"),
    "response bias": rx(r"\bresponse[- ]bias(?:es)?\b"),
    "decision criterion": rx(r"\bdecision[- ]criteri(?:on|a)\b"),
    "decision threshold": rx(r"\bdecision[- ]thresholds?\b"),
    "operating point": rx(r"\boperating[- ]points?\b"),
    "false alarm": rx(r"\bfalse[- ]alarms?\b"),
    "false positive rate": rx(r"\bfalse[- ]positive[- ]rates?\b|\bFPRs?\b"),
    "base rate": rx(r"\bbase[- ]rates?\b"),
    "payoff": rx(r"\bpay[- ]?offs?\b"),
    "asymmetric cost": rx(r"\basymmetric (?:error )?costs?\b|\bcost[- ]sensitive\b|\bunequal costs?\b"),
    "ideal observer": rx(r"\bideal[- ]observers?\b"),
    "conservatism": rx(r"\bconservatism\b|\bconservative (?:criterion|bias|threshold)\b"),
    "criterion": rx(r"\bcriterion shift|\bcriterion placement\b|\bresponse criterion\b"),
}
B_WEAK = {
    "sensitivity": rx(r"\bsensitivity\b"),
    "specificity": rx(r"\bspecificity\b"),
    "ROC": rx(r"\bROC\b|\bAUROC\b|\bAU-ROC\b"),
    "prior": rx(r"\bpriors?\b"),
    "conservative": rx(r"\bconservative\b"),
    "false positive": rx(r"\bfalse[- ]positives?\b"),
    "false negative": rx(r"\bfalse[- ]negatives?\b"),
    "calibration": rx(r"\bcalibrat\w*"),
    "threshold": rx(r"\bthresholds?\b"),
    "bayes": rx(r"\bBayes\w*"),
    "type I/II": rx(r"\btype[- ]I{1,2}\b"),
}
C_STRONG = {
    "strict": rx(r"\bstrict(?:er|est|ness)?\b"),
    "lenient": rx(r"\blenien(?:t|cy|ce)\b"),
    "harsh": rx(r"\bharsh(?:er|ly|ness)?\b"),
    "skeptical": rx(r"\bs[ck]eptic(?:al|ism|s)?\b"),
    "devil's advocate": rx(r"\bdevil'?s?\s+advocate\b"),
    "presuppos": rx(r"\bpresuppos\w*"),
    "sycophancy": rx(r"\bsycophan\w*"),
    "over-critical": rx(r"\bover[- ]?critic\w*|\boverly critical\b|\bhypercritical\b"),
    "false rejection": rx(r"\bfalse(?:ly)?[- ]reject\w*"),
}
C_WEAK = {
    "adversarial": rx(r"\badversarial\w*"),
    "persona": rx(r"\bpersonas?\b"),
    "stakes": rx(r"\bstakes\b|\bat stake\b"),
    "framing": rx(r"\bfram(?:ing|ings|ed)\b"),
    "prompt sensitivity": rx(r"\bprompt[- ]sensitiv\w*|\bsensitiv\w* to (?:the )?prompt"),
}


def hits(d, text):
    return [k for k, r in d.items() if r.search(text)]


def main(cand_file, out_dir, known_file=None):
    known = set()
    if known_file and os.path.exists(known_file):
        with open(known_file, newline="", encoding="utf-8") as fh:
            known = {row["id"].strip() for row in csv.DictReader(fh)}
    rows = []
    for line in open(cand_file, encoding="utf-8"):
        c = json.loads(line)
        text = c["title"] + " \n " + c["abstract"]
        a = hits(A, text)
        actor_only = bool(a == ["critic"] and A_ACTOR_CRITIC.search(text)
                          and not re.search(r"\bcritics?\b(?<!actor-critic)", A_ACTOR_CRITIC.sub("", text), re.I))
        aext = hits(A_EXT, text)
        bs, bw = hits(B_STRONG, text), hits(B_WEAK, text)
        cs, cw = hits(C_STRONG, text), hits(C_WEAK, text)
        llm = bool(LLM.search(text))
        hasA = bool(a)
        if hasA and bs and cs:
            tier = 1
        elif hasA and (bs or cs):
            tier = 2
        elif hasA and (bw or cw):
            tier = 3
        elif bs or cs:
            tier = 4
        else:
            tier = 5
        nblocks = int(hasA) + int(bool(bs or bw)) + int(bool(cs or cw)) + int(llm)
        score = 10 * nblocks + 3 * len(bs) + 3 * len(cs) + len(bw) + len(cw) + len(a)
        # title hits weigh more
        t = c["title"]
        score += 4 * (len(hits(B_STRONG, t)) + len(hits(C_STRONG, t))) + 2 * len(hits(A, t))
        c.update({"A": a, "actor_critic_only": actor_only, "A_ext": aext, "B_strong": bs, "B_weak": bw,
                  "C_strong": cs, "C_weak": cw, "LLM": llm, "tier": tier, "n_blocks": nblocks, "score": score,
                  "known": c["id"] in known})
        rows.append(c)
    rows.sort(key=lambda r: (r["tier"], -r["score"], r["id"]))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "ranked.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(os.path.join(out_dir, "ranked_titles.tsv"), "w", encoding="utf-8") as fh:
        fh.write("rank\ttier\tscore\tid\tknown\tA\tB\tC\ttitle\n")
        for i, r in enumerate(rows, 1):
            fh.write("\t".join([str(i), str(r["tier"]), str(r["score"]), r["id"], "K" if r["known"] else "",
                                ",".join(r["A"]) + ("(AC)" if r["actor_critic_only"] else ""),
                                ",".join(r["B_strong"] + [x.lower() for x in r["B_weak"]]),
                                ",".join(r["C_strong"] + [x.lower() for x in r["C_weak"]]),
                                r["title"]]) + "\n")
    from collections import Counter
    tc = Counter(r["tier"] for r in rows)
    print("candidates:", len(rows), "by tier:", dict(sorted(tc.items())))
    print("A and (B or C) [tiers 1-3]:", sum(tc[t] for t in (1, 2, 3)),
          "| of which actor-critic-only:", sum(1 for r in rows if r["tier"] <= 3 and r["actor_critic_only"]))
    print("known papers present:", sorted(r["id"] for r in rows if r["known"]))


if __name__ == "__main__":
    args = sys.argv[1:]
    known = None
    if "--known" in args:
        i = args.index("--known"); known = args[i + 1]; del args[i:i + 2]
    main(args[0], args[1], known)
