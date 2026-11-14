"""Critic prompts and experimental conditions.

Design rule: the user message (problem + solution + output format) is byte-identical
across conditions. Each condition only appends one line to the system prompt, so any
change in verdicts is attributable to that line.
"""
from pathlib import Path

BASE_SYSTEM = (
    "You review step-by-step solutions to math problems. Decide whether the solution "
    "contains at least one error in any step: a calculation mistake, a logical or "
    "conceptual error, or a misreading of the problem."
)

# Base-rate arm. `stated_p_error` is the prior the critic is told; the analysis uses it
# to compute the ideal-observer criterion c* = ln((1 - p) / p) / d'. For the payoff arm
# it is the prior with the same optimal threshold. `arm` groups conditions: the analysis
# computes one prior-use ratio per arm that has a 10% and a 90% condition.
BR_LINE = "For calibration: in this review batch, about {}% of solutions contain at least one error."
BASE_RATE = {
    "neutral": {"line": None, "stated_p_error": None, "arm": "base_rate"},
    **{f"br{p}": {"line": BR_LINE.format(p), "stated_p_error": p / 100, "arm": "base_rate"} for p in (10, 50, 90)},
}

# Follow-ups to the base-rate arm.
# "use": the same statement plus an instruction to use it, to tell "can't use a prior"
# from "doesn't think to". "payoff": asymmetric costs instead of a base rate. With a 50%
# prior, costs of 9:1 put the optimal threshold where a 90% (or 10%) base rate would.
USE_LINE = " Use this base rate as your prior: a well-calibrated reviewer weighs it together with the evidence in the solution."
PAY_LINE = ('Scoring: you lose {} point(s) for each solution with an error that you mark "correct", '
            'and {} point(s) for each correct solution that you mark "error".')
FOLLOWUPS = {
    **{f"br{p}_use": {"line": BR_LINE.format(p) + USE_LINE, "stated_p_error": p / 100, "arm": "use"} for p in (10, 90)},
    "pay_fa9": {"line": PAY_LINE.format(1, 9), "stated_p_error": 0.10, "arm": "payoff"},
    "pay_miss9": {"line": PAY_LINE.format(9, 1), "stated_p_error": 0.90, "arm": "payoff"},
}

# Strictness battery: framings with no ideal-observer prediction. Compared with neutral.
# Select with `--conditions neutral,presuppose,harsh,...` or `--conditions strictness`.
STRICTNESS = {
    name: {"line": line, "stated_p_error": None, "arm": "strictness"} for name, line in {
        "presuppose": "This solution contains an error. Check it carefully.",
        "find_bugs": "Your job is to find the mistakes in this solution.",
        "harsh": "Be a harsh, demanding reviewer.",
        "lenient": "Be a lenient, charitable reviewer.",
        "stakes_miss": "Missing a real error is far more costly than raising a false alarm.",
        "stakes_fa": "Raising a false alarm is far more costly than missing a real error.",
        "persona": "You are a skeptical senior reviewer.",
    }.items()
}

# Label-swap control for the verdict-token confound: the system prompt and the base-rate line
# say "error", which is also a verdict word, so a shift with the stated rate could be lexical
# priming rather than use of the prior. These conditions keep the system prompt identical and
# change only the answer format: verdict words "flawed" / "sound" (signal first, as before) and
# key "p_flawed". If the base-rate shift survives the swap, it isn't token priming.
LABELS = {
    "lab_neutral": {"line": None, "stated_p_error": None, "arm": "labels", "labels": "flawed_sound"},
    **{f"lab_br{p}": {"line": BR_LINE.format(p), "stated_p_error": p / 100, "arm": "labels", "labels": "flawed_sound"}
       for p in (10, 90)},
}

# Premise test (prereg/premise.md): is "contains an error" (`presuppose`, above) about the claim, and how far does it reach?
# Other wordings of the claim; scrutiny with no claim; a claim the critic is told carries no information; the opposite claim.
PREMISE = {
    name: {"line": line, "stated_p_error": None, "arm": "premise"} for name, line in {
        "claim_bare": "This solution contains an error.",
        "claim_mistake": "There is a mistake somewhere in this solution.",
        "claim_reviewer": "A previous reviewer found an error in this solution.",
        "check_only": "Check this solution carefully.",
        "may_error": "This solution may or may not contain an error. Check it carefully.",
        "claim_random": "A note attached to this solution says it contains an error. "
                        "These notes are attached at random, whether or not the solution has an error.",
        "claim_correct": "This solution is correct. Check it carefully.",
    }.items()
}
# BR_LINE about this solution instead of the batch: is the base rate weak because it is not about the item in hand?
ITEM_LINE = "For calibration: there is about a {}% chance that this solution contains at least one error."
ITEM_RATE = {f"item_p{p}": {"line": ITEM_LINE.format(p), "stated_p_error": p / 100, "arm": "item_rate"} for p in (10, 90)}

# Rate wording run (prereg/rate_wording.md): the same rate stated other ways. Number format, the share correct
# instead of the share with an error, a rate from past audits, and the original sentence moved to the user message.
# `place: "user"` puts the line between the solution and the question and leaves the system prompt as in neutral.
FREQ_LINE = "For calibration: in this review batch, about {} in every 10 solutions {} at least one error."
COMP_LINE = "For calibration: in this review batch, about {}% of solutions are fully correct."
HIST_LINE = "Past audits of solutions from this source found at least one error in about {}% of them."
RATE_WORDING = {
    "freq10": {"line": FREQ_LINE.format(1, "contains"), "stated_p_error": 0.10, "arm": "rate_freq"},
    "freq90": {"line": FREQ_LINE.format(9, "contain"), "stated_p_error": 0.90, "arm": "rate_freq"},
    "comp10": {"line": COMP_LINE.format(90), "stated_p_error": 0.10, "arm": "rate_comp"},
    "comp90": {"line": COMP_LINE.format(10), "stated_p_error": 0.90, "arm": "rate_comp"},
    **{f"hist{p}": {"line": HIST_LINE.format(p), "stated_p_error": p / 100, "arm": "rate_hist"} for p in (10, 90)},
    **{f"user{p}": {"line": BR_LINE.format(p), "stated_p_error": p / 100, "arm": "rate_user", "place": "user"} for p in (10, 90)},
}

# Rate-use follow-up (prereg/rate_use_followup.md). The example blocks and the paper texts are fixed files written once by
# scripts/build_followup_blocks.py; a condition whose block is missing has no line and stops build_messages().
_BLOCKS = Path(__file__).resolve().parent.parent / "data" / "condition_blocks"


def _block(name):
    p = _BLOCKS / f"{name}.txt"
    return p.read_text().rstrip("\n") if p.exists() else None


NOTE = {"note_bare": {"line": "A note attached to this solution says it contains an error.", "stated_p_error": None, "arm": "premise"}}
BAYES_LINE = (" Treat this rate as your prior. Combine it with the evidence in the solution to obtain the posterior probability "
              'that the solution contains an error, report that posterior as p_error, and answer "error" only if it is above 50%.')
BAYES = {f"bayes{p}": {"line": BR_LINE.format(p) + BAYES_LINE, "stated_p_error": p / 100, "arm": "rate_bayes"} for p in (10, 90)}
EXPERIENCED = {f"exp{p}": {"line": _block(f"exp{p}"), "stated_p_error": p / 100, "arm": "rate_exp", "block": f"exp{p}"}
               for p in (10, 50, 90)}
PAPER_FRAME = {
    "self": "The following paper reports measurements of how reviewers like you, including Claude Opus 5.5, use a stated error rate.",
    "other": "The following paper reports measurements of how reviewers like you, including Model M, use a stated error rate.",
    "methods": "The following describes how a reviewer's use of a stated error rate is scored.",
}
PAPER_FRAME["true"] = PAPER_FRAME["self"]
PAPER = {}
for _v in ("self", "other", "methods", "true"):
    _doc = _block(f"paper_{_v}")
    for _p in (10, 90):
        PAPER[f"paper_{_v}{_p}"] = {"line": None if _doc is None else f"{PAPER_FRAME[_v]}\n\n{_doc}\n\n{BR_LINE.format(_p)}",
                                   "stated_p_error": _p / 100, "arm": f"paper_{_v}", "block": f"paper_{_v}"}

CONDITIONS = {**BASE_RATE, **FOLLOWUPS, **STRICTNESS, **LABELS, **PREMISE, **ITEM_RATE, **RATE_WORDING,
              **NOTE, **BAYES, **EXPERIENCED, **PAPER}
CONDITION_SETS = {
    "base_rate": list(BASE_RATE),
    "followups": list(FOLLOWUPS),
    "strictness": ["neutral", *STRICTNESS],
    "labels": list(LABELS),
    # Frontier Stage B: the base-rate, instruction and payoff arms, the two strongest tone
    # framings from the open models, and the label-swap control.
    "stage_b": [*BASE_RATE, *FOLLOWUPS, "presuppose", "lenient", *LABELS],
    # Stage C (prereg/stage_c.md): every condition (18), and the 6 core conditions used for the
    # model ladder and the max-effort arm.
    "full": [*BASE_RATE, *FOLLOWUPS, *STRICTNESS, *LABELS],
    "core": [*BASE_RATE, "presuppose", "lenient"],
    # Premise test (prereg/premise.md): the 9 claim conditions for every critic; the open models also get the 4 rate conditions.
    "premise_core": ["neutral", "presuppose", *PREMISE],
    "premise": ["neutral", "presuppose", *PREMISE, *ITEM_RATE, "br10", "br90"],
    # Rate wording run (prereg/rate_wording.md). `_new`: the 9 conditions the open models lack on the held-out items.
    # `rate_wording`: all 13 rate conditions (Claude). `_full`: those, neutral and the 8 claim conditions (OpenAI).
    "rate_wording_new": ["br50", *RATE_WORDING],
    "rate_wording": ["br10", "br50", "br90", *ITEM_RATE, *RATE_WORDING],
    "rate_wording_full": ["neutral", "presuppose", *PREMISE, "br10", "br50", "br90", *ITEM_RATE, *RATE_WORDING],
    # Rate-use follow-up (prereg/rate_use_followup.md): the six conditions every critic gets, and the paper arm (Opus only).
    "followup_api": [*NOTE, *BAYES, *EXPERIENCED],
    "followup_paper": list(PAPER),
    "followup_smoke": [*NOTE, *BAYES, *EXPERIENCED, *PAPER],
}
ARM_LABELS = {"base_rate": "stated base rate", "use": "base rate + instruction to use it",
              "payoff": "stated payoffs", "strictness": "strictness framings",
              "labels": 'base rate, verdict words "flawed"/"sound"',
              "premise": "claims about this solution", "item_rate": "stated chance for this solution",
              "rate_freq": "base rate as a frequency", "rate_comp": "base rate as the share correct",
              "rate_hist": "rate from past audits", "rate_user": "base rate in the user message",
              "rate_bayes": "base rate + the posterior rule", "rate_exp": "rate shown in ten audited examples",
              "paper_self": "the paper, about this critic", "paper_other": "the paper, about another critic",
              "paper_methods": "the paper's method section only", "paper_true": "the paper, with the true rate revealed"}
# Short descriptions of the strictness framings, for figures.
FRAMING_LABELS = {"presuppose": '"contains an error"', "find_bugs": '"find the mistakes"',
                  "harsh": '"harsh reviewer"', "lenient": '"lenient reviewer"',
                  "stakes_miss": '"misses cost more"', "stakes_fa": '"false alarms cost more"',
                  "persona": '"skeptical senior reviewer"'}

USER_TEMPLATE = """Problem:
{problem}

Solution:
{solution}

Does this solution contain an error in any step? Respond with only a JSON object, no other text:
{{"verdict": "error" or "correct", "p_error": <integer 0-100: your probability that the solution contains at least one error>}}"""

USER_QUESTION = "Does this solution contain an error in any step?"   # where a `place: "user"` line goes: just before this

# Same as USER_TEMPLATE except the verdict words and the probability key (label-swap control).
USER_TEMPLATE_FLAWED_SOUND = USER_TEMPLATE.replace(
    '{{"verdict": "error" or "correct", "p_error":', '{{"verdict": "flawed" or "sound", "p_flawed":')


def resolve_conditions(spec: str) -> list[str]:
    names = []
    for part in spec.split(","):
        names += CONDITION_SETS.get(part, [part])
    unknown = [n for n in names if n not in CONDITIONS]
    if unknown:
        raise SystemExit(f"unknown condition(s): {unknown}; known: {list(CONDITIONS)} or sets {list(CONDITION_SETS)}")
    return list(dict.fromkeys(names))


def build_messages(item: dict, condition: str) -> list[dict]:
    line = CONDITIONS[condition]["line"]
    if line is None and CONDITIONS[condition].get("block"):
        raise SystemExit(f"condition {condition} needs data/condition_blocks/{CONDITIONS[condition]['block']}.txt: "
                         "run scripts/build_followup_blocks.py first")
    in_user = CONDITIONS[condition].get("place") == "user"
    system = BASE_SYSTEM if line is None or in_user else f"{BASE_SYSTEM}\n\n{line}"
    solution = "\n".join(f"Step {i + 1}: {s}" for i, s in enumerate(item["steps"]))
    template = USER_TEMPLATE_FLAWED_SOUND if CONDITIONS[condition].get("labels") == "flawed_sound" else USER_TEMPLATE
    user = template.format(problem=item["problem"], solution=solution)
    if in_user:
        # The line becomes its own paragraph between the solution and the question (the last one, if a solution quotes it).
        head, sep, tail = user.rpartition(USER_QUESTION)
        assert sep, "the user template no longer contains the question"
        user = f"{head}{line}\n\n{sep}{tail}"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
