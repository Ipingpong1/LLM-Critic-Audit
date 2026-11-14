"""Build the fixed text blocks of the rate-use follow-up (prereg/rate_use_followup.md), once, before any call.

    .venv/bin/python scripts/build_followup_blocks.py

Writes data/examples_experienced.jsonl (the example pool: the 10 shortest flawed and 10 shortest correct hard-set
solutions), data/condition_blocks/exp{10,50,90}.txt (the example blocks), data/condition_blocks/paper_{self,other,
methods,true}.txt (the manuscript body as plain text, in the four variants the plan fixes) and
data/condition_blocks/blocks.sha256. pilot/prompts.py reads the blocks at import. Deterministic: seed 0.
"""
import hashlib
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "condition_blocks"
POOL = ROOT / "data" / "examples_experienced.jsonl"
HARD = ROOT / "data" / "items_hard.jsonl"
PREMISE = ROOT / "data" / "items_premise.jsonl"
# The manuscript as it stood when the blocks were built (2026-11-12 build, archived 2026-11-13 before the follow-up's
# results were written in). The live main.tex has since changed, and the REVEAL passages below no longer occur in it.
TEX = ROOT / "manuscript" / "archive" / "2026-11-13_before_followup" / "main.tex"
TITLE = "Told the Odds, Moved by a Claim: An Ideal-Observer Audit of LLM Critics"
INTRO_EXP = ("The ten solutions below were reviewed just before this one, from the same batch, "
             "and their verdicts have been audited.")
# The passages that reveal that the stated rate is never the true rate. Removed from paper_self, paper_other and
# paper_methods; kept in paper_true. Each must occur exactly once in the manuscript.
REVEAL = [
    " The true error rate is therefore always 50\\%. The stated rate is the manipulation.",
    " Because $\\rho$ compares criteria on the same items, it does not require the stated rate to be true.",
    "The stated rate is never the true rate. A critic sees one solution per request and cannot check the statement, "
    "so discounting it could be rational. Against this reading, the instruction to use the rate did not help, "
    "and the critics did act on a statement about a note's reliability.\n\n",
]


def length(it):
    return len(it["problem"]) + sum(map(len, it["steps"]))


def build_pool():
    hard = [json.loads(l) for l in HARD.open()]
    held = {json.loads(l)["problem"] for l in PREMISE.open()}
    assert not any(it["problem"] in held for it in hard), "the hard set shares a problem with the held-out set"
    pool = []
    for flag in (True, False):
        pool += sorted([it for it in hard if it["has_error"] == flag], key=length)[:10]
    with POOL.open("w") as f:
        for it in pool:
            f.write(json.dumps(it) + "\n")
    return pool


def example_blocks(pool):
    rng = random.Random(0)
    fl = [it for it in pool if it["has_error"]]
    co = [it for it in pool if not it["has_error"]]
    rng.shuffle(fl)
    rng.shuffle(co)
    sets = {"exp50": fl[:5] + co[:5], "exp90": fl[:9] + co[:1], "exp10": fl[:1] + co[:9]}
    out = {}
    for name in ("exp10", "exp50", "exp90"):
        ex = list(sets[name])
        rng.shuffle(ex)
        parts = [INTRO_EXP]
        for k, it in enumerate(ex, 1):
            steps = "\n".join(f"Step {i + 1}: {s}" for i, s in enumerate(it["steps"]))
            parts.append(f"Example {k}\nProblem: {it['problem']}\nSolution:\n{steps}\n"
                         f"Audited verdict: {'error' if it['has_error'] else 'correct'}")
        out[name] = "\n\n".join(parts)
        assert sum(it["has_error"] for it in ex) == {"exp10": 1, "exp50": 5, "exp90": 9}[name]
    return out


def _name(key):
    m = re.match(r"([a-z]+)(\d{4})", key.strip())
    return f"{m.group(1).capitalize()} et al. ({m.group(2)})" if m else key


# Cross-reference numbers of the 2026-11-12 build (from the .aux), so the text reads as the PDF does.
REFS = {"fig:ideal": "1", "fig:rho": "2", "fig:claims": "3", "fig:evidence": "4", "fig:curves": "5", "fig:grid": "6",
        "fig:wording": "7", "tab:premise": "1", "tab:hard": "2", "tab:easy": "3", "tab:sol": "4", "sec:related": "2",
        "sec:method": "3", "sec:rates": "4.1", "sec:reasoning": "4.2", "sec:claims": "4.3", "sec:evidence": "4.4",
        "sec:robust": "4.5", "eq:cstar": "1", "eq:rho": "2", "eq:peff": "3"}


def detex(tex):
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    tex = re.sub(r"\\begin\{(figure\*?|table\*?)\}.*?\\end\{\1\}", "", tex, flags=re.S)
    tex = re.sub(r"\\pending\{[^}]*\}", "", tex)
    tex = re.sub(r"\\label\{[^}]*\}", "", tex)
    tex = re.sub(r"~?\\ref\{([^}]*)\}", lambda m: " " + REFS.get(m.group(1), "?"), tex)
    tex = re.sub(r"\\citet\{([^}]*)\}", lambda m: " and ".join(_name(k) for k in m.group(1).split(",")), tex)
    tex = re.sub(r"\s*\\citep\{[^}]*\}", "", tex)
    for _ in range(3):
        tex = re.sub(r"\\(emph|textbf|textit|texttt)\{([^{}]*)\}", r"\2", tex)
    tex = re.sub(r"\\section\{([^}]*)\}", r"\n\n\1\n", tex)
    tex = re.sub(r"\\subsection\{([^}]*)\}", r"\n\n\1\n", tex)
    tex = re.sub(r"\\paragraph\{([^}]*)\}", r"\n\n\1 ", tex)
    tex = re.sub(r"\\(begin|end)\{(abstract|itemize|equation)\}", "", tex)
    tex = tex.replace("\\item", "-").replace("\\dprime", "d'").replace("\\peff", "p_eff")
    tex = tex.replace("``", '"').replace("''", '"').replace("\\%", "%").replace("\\&", "&").replace("\\ldots", "...")
    tex = tex.replace("\\,", " ").replace("---", " - ").replace("--", "-").replace("~", " ").replace("\\ ", " ")
    tex = re.sub(r"\\(centering|maketitle|noindent)", "", tex)
    tex = re.sub(r"[ \t]+\n", "\n", tex)
    tex = re.sub(r"\n{3,}", "\n\n", tex)
    return tex.strip()


def paper_texts():
    src = TEX.read_text()
    body = src[src.index("\\begin{abstract}"): src.index("\\bibliography{refs}")]
    for s in REVEAL:
        assert body.count(s) == 1, f"revealing passage not found exactly once: {s[:50]!r}"
    stripped = body
    for s in REVEAL:
        stripped = stripped.replace(s, "")
    methods = stripped[stripped.index("\\section{The Ideal-Observer Audit}"): stripped.index("\\section{Results}")]
    full = lambda b: f"{TITLE}\n\nAbstract\n{detex(b)}"
    out = {"paper_true": full(body), "paper_self": full(stripped), "paper_methods": detex(methods)}
    other = out["paper_self"]
    for a, b in (("Claude Opus 5.5", "Model M"), ("Opus 5.5", "Model M"), ("Opus's", "Model M's")):
        other = other.replace(a, b)
    other = re.sub(r"\bOpus\b", "Model M", other)
    assert "Opus" not in other
    out["paper_other"] = other
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    blocks = example_blocks(build_pool())
    blocks.update(paper_texts())
    lines = []
    for name, text in blocks.items():
        (OUT / f"{name}.txt").write_text(text + "\n")
        h = hashlib.sha256((text + "\n").encode()).hexdigest()
        lines.append(f"{h}  {name}.txt")
        print(f"{name:14s} {len(text):7,} chars  ~{len(text) / 3.6:6,.0f} tokens  sha256 {h[:12]}")
    (OUT / "blocks.sha256").write_text("\n".join(lines) + "\n")
    print(f"wrote {POOL.relative_to(ROOT)} and {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
