"""Shared helpers for the `peer` literature-search stream.

- Polite HTTP GET with per-host spacing, retries on 429/5xx (60 s wait), honest User-Agent,
  no API keys, no mailto/email parameters.
- Raw responses saved gzip-compressed under ../raw/peer/<source>/ (data only).
- Query log rows appended to a JSONL in the scratchpad (converted to CSV at the end).
- Block A / B / C regex classifiers from PROTOCOL.md, applied locally to title+abstract+keywords.
"""
import gzip
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

LS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(LS, "raw", "peer")
SCRATCH = os.environ.get("PEER_SCRATCH", "/tmp")
QLOG = os.path.join(SCRATCH, "peer_qlog.jsonl")
UA = "litsearch-peer/1.0 (academic literature search script; python urllib)"

# minimum spacing between requests, per host (seconds)
SPACING = {
    "api2.openreview.net": 3.1,
    "api.crossref.org": 1.0,
    "api.openalex.org": 2.0,
}
_last = {}


def _wait(host):
    gap = SPACING.get(host, 1.0)
    t = _last.get(host, 0)
    dt = time.time() - t
    if dt < gap:
        time.sleep(gap - dt)
    _last[host] = time.time()


def get_json(url, params=None, source="misc", raw_name=None, timeout=180, max_retries=5):
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
    host = urllib.parse.urlparse(url).netloc
    for attempt in range(max_retries + 1):
        _wait(host)
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
            data = json.loads(raw)
            break
        except urllib.error.HTTPError as e:
            body = e.read()[:500]
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries:
                print(f"  HTTP {e.code} on {host}; waiting 60 s (attempt {attempt+1})", flush=True)
                time.sleep(60)
                continue
            raise RuntimeError(f"HTTP {e.code} for {url}: {body!r}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < max_retries:
                print(f"  network error {e}; waiting 30 s", flush=True)
                time.sleep(30)
                continue
            raise
    if raw_name is None:
        raw_name = hashlib.sha1(url.encode()).hexdigest()[:16]
    d = os.path.join(RAW, source)
    os.makedirs(d, exist_ok=True)
    with gzip.open(os.path.join(d, raw_name + ".json.gz"), "wb") as f:
        f.write(json.dumps({"url": url, "fetched": time.strftime("%Y-%m-%dT%H:%M:%S"), "response": data}).encode())
    return data


def log_query(database, query, filters, n_results, notes="", n_screened="", n_kept=""):
    row = {
        "date": "2026-11-06",
        "database": database,
        "query": query,
        "filters": filters,
        "n_results": n_results,
        "n_screened": n_screened,
        "n_kept": n_kept,
        "notes": notes,
    }
    with open(QLOG, "a") as f:
        f.write(json.dumps(row) + "\n")


def slug(s, n=60):
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s[:n]


# ----------------------------------------------------------------------------------------
# Block classifiers (PROTOCOL.md), applied to title + abstract + keywords (+ TLDR)
# ----------------------------------------------------------------------------------------
A_RE = re.compile(
    r"\b(critic|critics|critique[sd]?|critiquing|verifiers?|judges?|judging|judged|"
    r"llm[- ]as[- ]an?[- ]judges?|llms?[- ]as[- ]judges?|evaluators?|graders?|grading|"
    r"reward[- ]models?|process[- ]reward|prms?|orms?|self[- ]correct\w*|self[- ]critique\w*|"
    r"self[- ]critic\w*|self[- ]verif\w*|self[- ]refine\w*|self[- ]evaluat\w*|error[- ]detection|"
    r"error identification|detect\w* (?:the )?(?:errors?|mistakes?|flaws?|bugs?)|"
    r"reviewers?|overseers?|oversight|monitors?|monitoring|auditors?|verification)\b",
    re.I,
)
LLM_RE = re.compile(
    r"\b(language models?|llms?|large language|gpt[- ]?\d*\w*|chatgpt|foundation models?|vlms?|mllms?|"
    r"vision[- ]language|chatbots?|qwen\w*|llama\w*|claude|gemini|gemma|mistral|deepseek\w*|lms)\b",
    re.I,
)
B_TERMS = {
    "signal detection": r"signal[- ]detection",
    "d-prime": r"\bd[- ]?prime\b|\bd['′’](?=\s|\)|,|\.|$)",
    "sensitivity": r"\bsensitivity\b",
    "response bias": r"response[- ]bias",
    "decision criterion": r"decision[- ]criteri(?:on|a)",
    "decision threshold": r"decision[- ]thresholds?",
    "operating point": r"operating[- ]points?",
    "false alarm": r"false[- ]alarms?",
    "false positive rate": r"false[- ]positive[- ]rates?|\bfpr\b",
    "false positive/negative": r"false[- ](?:positives?|negatives?)",
    "specificity": r"\bspecificity\b",
    "ROC": r"\broc\b|receiver operating",
    "base rate": r"base[- ]rates?",
    "prior": r"\bpriors?\b|prior (?:probability|belief)",
    "payoff": r"\bpay[- ]?offs?\b",
    "asymmetric cost": r"asymmetric (?:costs?|payoffs?|loss|risks?|rewards?)|cost[- ]sensitive|unequal costs?",
    "ideal observer": r"ideal[- ]observer|bayes[- ]optimal|bayesian (?:observer|decision)",
    "conservatism": r"conservatism|\bconservative\b",
    "calibration": r"calibrat\w+",
    "criterion": r"\bcriterion shift|\bresponse criterion|\bcriterion placement|threshold shift",
}
C_TERMS = {
    "strict": r"\bstrict(?:ness|er|est|ly)?\b",
    "lenient": r"\blenien(?:t|cy|ce)\b",
    "harsh": r"\bharsh\w*",
    "skeptical": r"\bs[ck]eptic\w*",
    "devil's advocate": r"devil'?s advocate",
    "adversarial": r"\badversarial\w*",
    "presuppos": r"presuppos\w*|presum\w* (?:an )?errors?",
    "persona": r"\bpersonas?\b",
    "stakes": r"\b(?:high|low)?[- ]?stakes\b",
    "framing": r"\bfram(?:ing|ed|e)\b",
    "prompt sensitivity": r"prompt[- ]sensitiv\w*|prompt (?:wording|phrasing|variation)s?",
    "sycophancy": r"sycophan\w*",
    "over-critical": r"over[- ]?critical|overly critical|hyper[- ]?critical|nitpick\w*",
    "false rejection": r"false[- ]rejections?|over[- ]?rejection|over[- ]?refusal",
    "tone/politeness": r"\btone\b|politeness|\bpolite\b",
    "confirmation/anchoring": r"confirmation bias|anchoring",
    "leniency bias": r"leniency bias|severity bias|harshness",
}
B_RE = {k: re.compile(v, re.I) for k, v in B_TERMS.items()}
C_RE = {k: re.compile(v, re.I) for k, v in C_TERMS.items()}
STRONG_B = {"signal detection", "d-prime", "response bias", "decision criterion", "decision threshold",
            "operating point", "false alarm", "false positive rate", "ROC", "base rate", "payoff",
            "asymmetric cost", "ideal observer", "criterion", "specificity", "false positive/negative"}
STRONG_C = {"strict", "lenient", "harsh", "skeptical", "devil's advocate", "presuppos", "persona",
            "stakes", "framing", "prompt sensitivity", "sycophancy", "over-critical", "false rejection",
            "tone/politeness", "leniency bias"}


def classify(text):
    text = text or ""
    a = sorted({m.group(0).lower() for m in A_RE.finditer(text)})
    llm = bool(LLM_RE.search(text))
    b = sorted(k for k, r in B_RE.items() if r.search(text))
    c = sorted(k for k, r in C_RE.items() if r.search(text))
    strong = sorted((set(b) & STRONG_B) | (set(c) & STRONG_C))
    return {
        "A": a,
        "LLM": llm,
        "B": b,
        "C": c,
        "strong": strong,
        "hit": bool(a) and llm and bool(b or c),
        "score": len(strong) * 2 + len(b) + len(c),
    }
