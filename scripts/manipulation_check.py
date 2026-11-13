"""Manipulation check: does the critic understand which way a condition line should push it?

For each condition, the system prompt is exactly the one the critic saw in the pilot, and the
user asks (before any solution) which way to lean when unsure, and for payoffs, which mistake
costs more. A model that answers correctly here but doesn't shift in the pilot understands the
instruction and fails to apply it. Temperature 0, thinking off, one reply per question and option order.

    .venv/bin/python scripts/manipulation_check.py qwen3.5:4b qwen3.5:27b
    .venv/bin/python scripts/manipulation_check.py --rescore   # re-score stored replies
"""
import json
import re
import sys
from pathlib import Path

from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pilot.prompts import BASE_SYSTEM, CONDITIONS  # noqa: E402

# Each question is asked twice, with the two options in both orders, to separate an answer
# from a preference for whichever option is named first.
LEAN_Q = ('Before you review any solutions: given these instructions, when you are unsure whether a solution '
          'contains an error, should you lean toward answering "{}" or "{}"? '
          'Start your reply with one word, {} or {}, then give one sentence of explanation.')
LEAN_OPTS = ("error", "correct")
COST_Q = ('Before you review any solutions: under this scoring, which mistake costs you more points, '
          '{}? Start your reply with "{}" or "{}", then give one sentence of explanation.')
COST_OPTS = ("flawed marked correct", "correct marked error")
COST_DESC = {"flawed marked correct": 'marking a flawed solution "correct"',
             "correct marked error": 'marking a correct solution "error"'}


def question(kind: str, order: int) -> tuple[str, tuple[str, str]]:
    a, b = (LEAN_OPTS if kind == "lean" else COST_OPTS)[::1 if order == 0 else -1]
    if kind == "lean":
        return LEAN_Q.format(a, b, a, b), (a, b)
    return COST_Q.format(f"{COST_DESC[a]} or {COST_DESC[b]}", a, b), (a, b)


# Fallback when the reply doesn't start with an option: "I should lean toward answering "error" ...".
LEAN_RE = re.compile(r'lean toward (?:answering |marking )?(?:it |a solution |the solution )?(?:as )?["\']?(error|correct)\b', re.I)


def extract(kind: str, reply: str, opts: tuple[str, str]) -> str | None:
    head = reply.lower().lstrip('*"\' ')
    answer = next((o for o in opts if head.startswith(o)), None)
    if answer is None and kind == "lean" and (m := LEAN_RE.search(reply)):
        answer = m.group(1).lower()
    return answer


# condition: (questions to ask, the answers an ideal reader gives)
CHECKS = {
    "neutral": {"lean": None},
    "br10": {"lean": "correct"},
    "br90": {"lean": "error"},
    "pay_fa9": {"lean": "correct", "cost": "correct marked error"},
    "pay_miss9": {"lean": "error", "cost": "flawed marked correct"},
}

OUT = Path("results/checks/manipulation_check.jsonl")


def rescore():
    recs = [json.loads(line) for line in OUT.open()]
    for r in recs:
        opts = LEAN_OPTS if r["question"] == "lean" else COST_OPTS
        r["answer"] = extract(r["question"], r["reply"], opts)
        r["ok"] = None if r["expected"] is None else r["answer"] == r["expected"]
    OUT.write_text("".join(json.dumps(r) + "\n" for r in recs))
    print(f"re-scored {len(recs)} replies, {sum(r['answer'] is None for r in recs)} without an answer")


def run(models):
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="EMPTY")
    with OUT.open("a") as f:
        for model in models:
            for cond, expected in CHECKS.items():
                line = CONDITIONS[cond]["line"]
                system = BASE_SYSTEM if line is None else f"{BASE_SYSTEM}\n\n{line}"
                for kind in ("lean", "cost"):
                    if kind not in expected:
                        continue
                    for order in (0, 1):
                        q, opts = question(kind, order)
                        reply = client.chat.completions.create(
                            model=model, temperature=0, max_tokens=120,
                            messages=[{"role": "system", "content": system}, {"role": "user", "content": q}],
                            extra_body={"reasoning_effort": "none"},
                        ).choices[0].message.content.strip()
                        answer = extract(kind, reply, opts)
                        ok = None if expected[kind] is None else answer == expected[kind]
                        rec = dict(model=model, condition=cond, question=kind, first_option=opts[0],
                                   expected=expected[kind], answer=answer, ok=ok, reply=reply)
                        f.write(json.dumps(rec) + "\n")
                        print(f"{model:13} {cond:9} {kind:4} first={opts[0]:21} expected={expected[kind]!s:21} "
                              f"got={answer!s:21} | {reply[:70]!r}")


if __name__ == "__main__":
    rescore() if sys.argv[1:] == ["--rescore"] else run(sys.argv[1:])
