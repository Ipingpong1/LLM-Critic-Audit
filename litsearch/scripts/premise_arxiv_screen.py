#!/usr/bin/env python3
"""Literal re-match and ranking of arXiv records for the claim-test addendum (P1-P5).

Usage:
  python3 -I premise_arxiv_screen.py rank <candidates.jsonl> <out.tsv> [--since YYYY-MM-DD] [--min N]
  python3 -I premise_arxiv_screen.py show <out.tsv> [--min N] [--max N] [--skip ids.txt] [--limit K]
  python3 -I premise_arxiv_screen.py abs  <candidates.jsonl> <id> [...]

The arXiv API stems terms, so API hits are re-matched here on literal word forms in title + abstract.
Each record gets tags and a score:
  E  evaluator role (judge, verifier, critic, reviewer, grader, monitor, auditor, code review, error detection, ...)
  A  an asserted premise, verdict or hint in the prompt or context (sycophancy, presupposition, false premise,
     prior verdict, pre-screening, anchoring, confirmation bias, deference, accusation, told that, ...)
  F  false alarms on correct work (false positive, false alarm, false rejection, specificity, correct-to-incorrect, ...)
  C  a control that separates assertion from scrutiny or possibility, or discounts it (uninformative, random,
     unreliable source, source credibility, hedged, decisiveness, both directions, ...)
  N  numeric priors (base rate, prior probability, Bayesian, stated probability, likelihood ratio, ...)
  S  signal detection or threshold language (signal detection, criterion, response bias, d-prime, threshold,
     discrimination, AUROC, calibration, ...)
  L  an LLM term
score = 3*[E and A] + 2*[A and F] + 2*[A and C] + 2*[A and N] + 2*[A and S] + 2*[E and N] + 1 per tag present.
Titles are read from the top of the ranking down to the stated cut (logged per query in the stream log).
"""
import json
import re
import sys

RX = {
    "E": r"\bjudg(?:e|es|ing)\b|\bverifiers?\b|\bcritics?\b|\bcritiqu\w+|\breviewers?\b|\bgraders?\b|\bgrading\b|"
         r"\bevaluators?\b|\bmonitors?\b|\bauditors?\b|\bauditing\b|\boverseers?\b|\bcode[- ]review\w*|\bpeer[- ]review\w*|"
         r"\b(?:error|bug|mistake|vulnerability|defect|flaw)[- ](?:detection|identification|finding|localization)\b|"
         r"\bproof[- ](?:check\w*|verif\w*|grad\w*)|\bverification\b|\bverify(?:ing)?\b|\bfact[- ]check\w*|"
         r"\bself[- ]?(?:correct\w*|verif\w*|critiqu\w*|refin\w*|review\w*)|\breward models?\b|\bassessors?\b",
    "A": r"\bsycophan\w+|\bpresuppos\w+|\bfalse[- ]premises?\b|\b(?:flawed|misleading|incorrect|wrong|faulty) premises?\b|"
         r"\bmisleading (?:hints?|cues?|context|feedback|notes?|claims?|evidence|comments?)\b|\btold that\b|\bbeing told\b|"
         r"\bassert(?:s|ed|ing|ion|ions)\b|\bhints?\b|\bcues?\b|\banchoring\b|\banchor(?:s|ed)? (?:the |its |their )?(?:judg|verdict|score|rating)\w*|"
         r"\bconfirmation bias\b|\bprior (?:verdicts?|reviews?|labels?|scores?|judg\w+|decisions?|assessments?|ratings?)\b|"
         r"\bprevious (?:verdicts?|reviews?|reviewers?|judg\w+|scores?)\b|\bpre-?screen\w*|\bdefer(?:s|red|ring|ence|ential)?\b|"
         r"\bover-?trust\w*|\bauthority (?:bias|cue|cues)\b|\bappeal to authority\b|\b(?:false|falsely) accus\w+|\baccusations?\b|"
         r"\bgullib\w+|\bcredul\w+|\bleading questions?\b|\bloaded questions?\b|\bbias injection\b|\bsuggestib\w+|"
         r"\bcontains? (?:an? )?(?:error|bug|mistake|flaw|vulnerabilit)\w*|\bthere is (?:an? )?(?:error|bug|mistake|flaw)\b|"
         r"\b(?:false|fabricated|misleading|incorrect) (?:feedback|assurances?|alarms?|notes?|claims?|labels?|hints?)\b|"
         r"\bframing (?:effect|bias)\b|\bsocial pressure\b|\bpushback\b|\bpersuasi\w+|\bconformity\b|\bcapitulat\w+",
    "F": r"\bfalse[- ]positives?\b|\bfalse[- ]alarms?\b|\bfalse[- ]reject\w*|\bspecificity\b|\bover-?(?:flag\w*|correct\w*|critical)\b|"
         r"\bcorrect[- ]to[- ]incorrect\b|\bhallucinated (?:bugs?|errors?|vulnerabilit\w+|findings?)\b|"
         r"\b(?:non-?existent|spurious|phantom|fabricated) (?:bugs?|errors?|vulnerabilit\w+|findings?|flaws?|issues?)\b|"
         r"\bcorrect (?:solutions?|answers?|code|work|verdicts?|proofs?)\b|\btrue[- ]negatives?\b",
    "C": r"\buninformative\b|\b(?:at )?random(?:ly)?\b|\bunreliable\b|\bsource (?:reliab\w+|credib\w+|trust\w*)|\bprovenance\b|"
         r"\bdiscount(?:s|ed|ing)?\b|\bhedg(?:e|ed|ing)\b|\bdecisiveness\b|\bboth directions\b|\bbidirectional\w*|"
         r"\bepistemic (?:vigilance|markers?)\b|\bplacebo\b|\battribut(?:ed|ion) to\b|\bnon-?informative\b|\bno information\b|"
         r"\bmay be (?:inaccurate|wrong|unreliable|incorrect)\b|\bunverified\b|\bcontrols? (?:for|condition)\b|\bablat\w+",
    "N": r"\bbase[- ]rates?\b|\bprior probabilit\w+|\bBayes\w*|\bstated (?:probabilit\w+|chance|rate|prior)s?\b|"
         r"\blikelihood ratios?\b|\bnumeric(?:al)? (?:prior|probabilit|anchor|cue|hint)\w*|\bprevalence\b|\bprobability estimates?\b|"
         r"\bposterior\b|\bbelief updat\w+",
    "S": r"\bsignal[- ]detection\b|\bcriterion\b|\bresponse bias\b|\bd[- ]?prime\b|\bd['′]|\bdecision thresholds?\b|\bthresholds?\b|"
         r"\bdiscriminat\w+|\bAUROC\b|\bAUC\b|\bROC\b|\bcalibrat\w+|\bsensitivity\b|\boperating points?\b",
    "L": r"\blanguage models?\b|\bLLMs?\b|\bGPT\b|\bGPT-|\bChatGPT\b|\bfoundation models?\b|\bVLMs?\b|\bMLLMs?\b|"
         r"\breasoning models?\b|\bAI agents?\b|\bagents?\b|\bClaude\b|\bGemini\b|\bQwen\b|\bLlama\b|\bAI (?:reviewers?|judges?|systems?)\b",
}
CRX = {k: re.compile(v, re.I) for k, v in RX.items()}


def tags_score(text):
    t = {k for k, rx in CRX.items() if rx.search(text)}
    s = len(t)
    if "E" in t and "A" in t:
        s += 3
    for k in "FCNS":
        if "A" in t and k in t:
            s += 2
    if "E" in t and "N" in t:
        s += 2
    return t, s


def rank(cand, out, since=None, minscore=0):
    rows = []
    n = 0
    for line in open(cand, encoding="utf-8"):
        r = json.loads(line)
        n += 1
        pub = (r.get("published") or "")[:10]
        if since and pub < since:
            continue
        t, s = tags_score(r["title"] + " \n " + r["abstract"])
        if "L" not in t or s < minscore:
            continue
        rows.append((s, "".join(sorted(t - {"L"})), pub, r["id"], ",".join(r.get("found_via", [])), r["title"]))
    rows.sort(key=lambda x: (-x[0], x[3]), reverse=False)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("score\ttags\tpublished\tid\tfound_via\ttitle\n")
        for row in rows:
            fh.write("\t".join(str(x) for x in row) + "\n")
    hist = {}
    for row in rows:
        hist[row[0]] = hist.get(row[0], 0) + 1
    print(f"records={n} kept={len(rows)} score histogram: " + " ".join(f"{k}:{hist[k]}" for k in sorted(hist, reverse=True)))


def show(tsv, lo=0, hi=99, skip=None, limit=10 ** 6):
    skipset = set()
    if skip:
        skipset = {l.strip() for l in open(skip, encoding="utf-8") if l.strip()}
    k = 0
    for i, line in enumerate(open(tsv, encoding="utf-8")):
        if i == 0:
            continue
        s, tags, pub, aid, via, title = line.rstrip("\n").split("\t", 5)
        if not (lo <= int(s) <= hi) or aid in skipset:
            continue
        k += 1
        if k > limit:
            break
        print(f"{s}\t{tags}\t{pub}\t{aid}\t{title[:140]}")
    print(f"[{min(k, limit)} titles shown]")


def abstracts(cand, ids):
    want = set(ids)
    for line in open(cand, encoding="utf-8"):
        r = json.loads(line)
        if r["id"] in want:
            print(f"=== {r['id']} ({r['published'][:10]}; {r.get('primary_category')}) {r['title']}\n    {'; '.join(r['authors'][:6])}"
                  f"{' et al.' if len(r['authors']) > 6 else ''} | {r.get('comment', '')[:120]}\n    {r['abstract']}\n")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(1)

    def opt(name, default=None):
        if name in a:
            i = a.index(name)
            v = a[i + 1]
            del a[i:i + 2]
            return v
        return default

    if a[0] == "rank":
        since = opt("--since")
        mn = int(opt("--min", "0"))
        rank(a[1], a[2], since, mn)
    elif a[0] == "show":
        lo = int(opt("--min", "0"))
        hi = int(opt("--max", "99"))
        skip = opt("--skip")
        limit = int(opt("--limit", str(10 ** 6)))
        show(a[1], lo, hi, skip, limit)
    elif a[0] == "abs":
        abstracts(a[1], a[2:])
