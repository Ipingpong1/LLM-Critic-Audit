"""Build a blind label-audit sheet for the items most critics disagree with the label on.

Why. With no added line, several critics flag the same "correct" solutions again and again: 12 of the 100
correct premise items are flagged by at least 5 of the 6 thinking-on critics, and 73 by none. That pattern
points at the labels, or at a rigor standard stricter than the annotators', and not at noise in the critics.
A person has to decide which, without knowing which items are in doubt: telling the auditor "six critics
found an error here" is the manipulation the premise test measured.

Rule, fixed in this file:
  - Critics: every thinking-on critic that ran the neutral condition on the set (SETS below).
  - A critic disagrees with an item's label if its verdict contradicts the label in more than half of its
    parsed neutral replies.
  - An item is contested if at least half of the critics with a parsed reply disagree with its label.
  - Controls: correct items that no critic flagged in any neutral reply, and flawed items that every critic
    caught in every neutral reply. Flawed controls are solutions that still reach the right final answer,
    the closest match to the contested ones. Drawn at random (--seed), half from each set.
  - Contested items and controls are shuffled together and numbered A01, A02, ...

Writes, under audit/:
  audit_sheet.html  the blind sheet: problem, solution and an answer form. No labels, verdicts or item ids.
  audit_key.csv     audit id -> item id, set, group, label, and what each critic did.
  audit_key.html    the same, with each critic's reasoning. Open it only after the blind pass.

Usage:
    python3 scripts/build_audit_sheet.py
"""
import argparse
import collections
import csv
import hashlib
import html
import json
import random
import re
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SETS = {
    "premise": {
        "items": "data/items_premise.jsonl",
        "critics": {
            "opus-5.5": "results/premise/opus-5.5-think.jsonl",
            "haiku-5.5": "results/premise/haiku-5.5-think.jsonl",
            "qwen3.5:4b": "results/premise/qwen3.5_4b-think-bf16-t1.jsonl",
            "qwen3.5:9b": "results/premise/qwen3.5_9b-think-bf16-t1.jsonl",
            "gemma4:12b": "results/premise/gemma4_12b-think-bf16-t1.jsonl",
            "qwen3.5:27b": "results/premise/qwen3.5_27b-think-bf16-t1.jsonl",
        },
    },
    "hard": {
        "items": "data/items_hard.jsonl",
        "critics": {
            "opus-5.5": "results/frontier/stage_c/opus-5.5-think.jsonl",
            "sonnet-5.5": "results/frontier/stage_c/sonnet-5.5-think.jsonl",
            "haiku-5.5": "results/frontier/stage_c/haiku-5.5-think.jsonl",
            "qwen3.5:4b": "results/torch_hard/qwen3.5_4b-think-bf16-t1.jsonl",
            "qwen3.5:9b": "results/torch_hard/qwen3.5_9b-think-bf16-t1.jsonl",
            "gemma4:12b": "results/torch_hard/gemma4_12b-think-bf16-t1.jsonl",
            "qwen3.5:27b": "results/torch_hard/qwen3.5_27b-think-bf16-t1.jsonl",
        },
    },
}
CRITIC_ORDER = ["opus-5.5", "sonnet-5.5", "haiku-5.5", "qwen3.5:27b", "gemma4:12b", "qwen3.5:9b", "qwen3.5:4b"]
CLAUDE = ("opus", "sonnet", "haiku")  # these return a short thinking summary, the open models their full reasoning
STEP = re.compile(r"\bstep\s*(\d{1,2})\b", re.I)


def neutral_rows(path):
    """Parsed neutral replies of one critic. The substring test skips the long reasoning of other conditions."""
    with open(path) as f:
        for line in f:
            if '"condition": "neutral"' not in line:
                continue
            r = json.loads(line)
            if r.get("condition") == "neutral" and r.get("verdict") in ("error", "correct"):
                yield r


def prose(raw):
    """The visible reply without its JSON verdict."""
    return re.sub(r"```(?:json)?|\{[^{}]*\}", "", raw or "").strip()


def tail(s, n):
    if len(s) <= n:
        return s
    cut = s[-n:]
    return "… " + cut[cut.find(" ") + 1:]


def repair(text):
    """Undo a JSON escape that ate a LaTeX command upstream: a form feed for "\\f" (\\frac), a backspace for "\\b".

    7 of the 2,000 OlympiadBench and Omni-MATH rows in ProcessBench have this, all in the problem statement.
    The critics saw the damaged text. The sheet shows the repaired text, and the key marks those items.
    """
    return text.replace("\x0c", "\\f").replace("\x08", "\\b")


def collect(cfg):
    """items by id, and per item and critic: parsed replies, replies against the label, stated P(error), longest such reply."""
    items = {}
    for line in open(ROOT / cfg["items"]):
        it = json.loads(line)
        shown = {"problem": repair(it["problem"]), "steps": [repair(s) for s in it["steps"]]}
        it["text_repaired"] = shown["problem"] != it["problem"] or shown["steps"] != it["steps"]
        it.update(shown)
        items[it["id"]] = it
    seen = {i: {} for i in items}
    for critic, path in cfg["critics"].items():
        for r in neutral_rows(ROOT / path):
            it = items.get(r["item_id"])
            if it is None:
                continue
            s = seen[it["id"]].setdefault(critic, {"n": 0, "against": 0, "p": [], "best": None})
            s["n"] += 1
            if r.get("p_error") is not None:
                s["p"].append(r["p_error"])
            if (r["verdict"] == "error") != it["has_error"]:
                s["against"] += 1
                size = len(r.get("reasoning") or "") + len(r.get("raw") or "")
                if s["best"] is None or size > s["best"]["size"]:
                    s["best"] = {"reasoning": r.get("reasoning") or "", "raw": r.get("raw") or "",
                                 "p_error": r.get("p_error"), "size": size}
    return items, seen


def classify(items, seen, n_critics):
    """item id -> (group, critics with a parsed reply, critics that disagree with the label)."""
    out = {}
    for iid in items:
        cs = seen[iid]
        voters = [c for c in cs if cs[c]["n"]]
        against = [c for c in voters if cs[c]["against"] * 2 > cs[c]["n"]]
        if voters and len(against) * 2 >= len(voters):
            group = "contested"
        elif len(voters) == n_critics and not any(cs[c]["against"] for c in voters):
            group = "clean"
        else:
            group = "other"
        out[iid] = (group, voters, against)
    return out


def named_step(best, n_steps):
    """The step a critic names most often at the end of its reasoning (rough: a text search)."""
    text = (best["reasoning"][-1200:] + " " + prose(best["raw"]))
    hits = [int(m) for m in STEP.findall(text) if 1 <= int(m) <= n_steps]
    return collections.Counter(hits).most_common(1)[0][0] if hits else None


def excerpt(critic, best):
    reasoning, reply = best["reasoning"].strip(), prose(best["raw"])
    parts = []
    if reasoning:
        parts.append(tail(reasoning, 3000 if critic.startswith(CLAUDE) else 1500))
    if len(reply) > 40:
        parts.append("[visible reply] " + tail(reply, 1000))
    return "\n\n".join(parts) or "(no reasoning came back: the reply was the verdict alone)"


def build(n_clean, n_flawed, seed):
    rng = random.Random(seed)
    entries, pools = [], {"control_correct": {}, "control_flawed": {}}
    for set_name, cfg in SETS.items():
        items, seen = collect(cfg)
        groups = classify(items, seen, len(cfg["critics"]))
        for iid, (group, voters, against) in groups.items():
            it = items[iid]
            e = {"set": set_name, "item": it, "seen": seen[iid], "voters": voters, "against": against}
            if group == "contested":
                entries.append({**e, "group": "contested_flawed" if it["has_error"] else "contested_correct"})
            elif group == "clean" and not it["has_error"]:
                pools["control_correct"].setdefault(set_name, []).append(e)
            elif group == "clean" and it["final_answer_correct"]:
                pools["control_flawed"].setdefault(set_name, []).append(e)
    for group, n in (("control_correct", n_clean), ("control_flawed", n_flawed)):
        names = list(SETS)
        for k, set_name in enumerate(names):
            share = n // len(names) + (1 if k < n % len(names) else 0)
            pool = sorted(pools[group].get(set_name, []), key=lambda e: e["item"]["id"])
            for e in rng.sample(pool, min(share, len(pool))):
                entries.append({**e, "group": group})
    entries.sort(key=lambda e: (e["set"], e["item"]["id"]))
    rng.shuffle(entries)
    for k, e in enumerate(entries):
        e["aid"] = f"A{k + 1:02d}"
    ident = "|".join(f'{e["set"]}:{e["item"]["id"]}' for e in entries)
    return entries, hashlib.sha1(ident.encode()).hexdigest()[:8]


def critic_rows(e):
    """One row per critic: name, replies against the label, parsed replies, median stated P(error)."""
    rows = []
    for c in CRITIC_ORDER:
        s = e["seen"].get(c)
        if s and s["n"]:
            rows.append((c, s["against"], s["n"], st.median(s["p"]) if s["p"] else None))
    return rows


def steps_named(e):
    if e["item"]["has_error"]:
        return ""
    tally = collections.Counter()
    for c in e["against"]:
        k = named_step(e["seen"][c]["best"], len(e["item"]["steps"]))
        if k:
            tally[k] += 1
    return "; ".join(f"Step {k} ({n})" for k, n in tally.most_common())


def label_text(it):
    # ProcessBench counts steps from 0; the critics and the sheet count from 1.
    return f'flawed, first wrong step: Step {it["first_error_step"] + 1}' if it["has_error"] else "correct"


def write_key_csv(entries, path):
    critics = [c for c in CRITIC_ORDER if any(c in e["seen"] for e in entries)]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["audit_id", "set", "item_id", "group", "label_has_error", "label_first_error_step",
                    "final_answer_correct", "generator", "n_critics", "n_against_label", "steps_named_by_critics",
                    "text_repaired"]
                   + [f"{c} against/replies" for c in critics] + [f"{c} median P(error)" for c in critics])
        for e in entries:
            it, rows = e["item"], {r[0]: r for r in critic_rows(e)}
            w.writerow([e["aid"], e["set"], it["id"], e["group"], int(it["has_error"]),
                        it["first_error_step"] + 1 if it["has_error"] else "", int(it["final_answer_correct"]),
                        it["generator"], len(e["voters"]), len(e["against"]), steps_named(e), int(it["text_repaired"])]
                       + [f"{rows[c][1]}/{rows[c][2]}" if c in rows else "" for c in critics]
                       + [("" if rows[c][3] is None else f"{rows[c][3]:g}") if c in rows else "" for c in critics])


GROUP_TEXT = {
    "contested_correct": "Contested: labelled correct, flagged by {a} of {n} critics",
    "contested_flawed": "Contested: labelled flawed, passed by {a} of {n} critics",
    "control_correct": "Control: labelled correct, flagged by no critic",
    "control_flawed": "Control: labelled flawed, caught by every critic",
}


def write_key_html(entries, sheet_id, path):
    esc = html.escape
    out = []
    for e in entries:
        it = e["item"]
        head = GROUP_TEXT[e["group"]].format(a=len(e["against"]), n=len(e["voters"]))
        out.append(f'<section class="item {e["group"].split("_")[0]}"><h2>{e["aid"]} <span class="tag">{esc(head)}</span></h2>')
        out.append(f'<p class="meta">Label: {esc(label_text(it))} · final answer '
                   f'{"right" if it["final_answer_correct"] else "wrong"} · {e["set"]} set · {esc(it["id"])} · '
                   f'solution written by {esc(it["generator"])}'
                   + (' · the critics saw a damaged LaTeX command in the problem (repaired here)' if it["text_repaired"] else '')
                   + '</p>')
        out.append('<table><tr><th>critic</th><th>replies against the label</th><th>median stated P(error)</th></tr>')
        for c, against, n, p in critic_rows(e):
            out.append(f'<tr><td>{esc(c)}</td><td>{against} of {n}</td><td>{"–" if p is None else f"{p:g}"}</td></tr>')
        out.append('</table>')
        named = steps_named(e)
        if named:
            out.append(f'<p>Step named most at the end of each critic\'s reasoning (rough text search; number of critics): {esc(named)}</p>')
        out.append('<details><summary>Problem and solution</summary><h3>Problem</h3>'
                   f'<div class="text">{esc(it["problem"])}</div><h3>Solution</h3>')
        for k, s in enumerate(it["steps"]):
            out.append(f'<div class="step"><div class="stepno">Step {k + 1}</div><div class="text">{esc(s)}</div></div>')
        out.append('</details>')
        if e["against"]:
            out.append('<h3>What the disagreeing critics wrote</h3>')
            for c in CRITIC_ORDER:
                if c not in e["against"]:
                    continue
                best = e["seen"][c]["best"]
                kind = "thinking summary" if c.startswith(CLAUDE) else "end of its reasoning"
                p = "" if best["p_error"] is None else f' · stated P(error) {best["p_error"]:g}'
                out.append(f'<details{" open" if c.startswith(CLAUDE) else ""}><summary>{esc(c)}{p} · {kind}</summary>'
                           f'<div class="text quote">{esc(excerpt(c, best))}</div></details>')
        out.append('</section>')
    page = KEY_HTML.replace("@@SHEET_ID@@", sheet_id).replace("@@BODY@@", "\n".join(out))
    Path(path).write_text(page, encoding="utf-8")


def write_sheet_html(entries, sheet_id, path):
    data = {"sheet_id": sheet_id,
            "items": [{"aid": e["aid"], "problem": e["item"]["problem"], "steps": e["item"]["steps"]} for e in entries]}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    Path(path).write_text(SHEET_HTML.replace("@@SHEET_ID@@", sheet_id).replace("@@DATA@@", blob), encoding="utf-8")


CSS = r"""
:root{--bg:#f6f6f3;--card:#fff;--ink:#1c1c1a;--muted:#66665f;--line:#dcdcd4;--accent:#2f5fd0;--done:#2e7d4f;--warn:#a8480a;--soft:#efefe9}
@media (prefers-color-scheme: dark){:root{--bg:#151514;--card:#1e1e1c;--ink:#ecece7;--muted:#a3a39b;--line:#383833;--accent:#8fb0ff;--done:#6fcf97;--warn:#f0b35a;--soft:#262623}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1120px;margin:0 auto;padding:16px}
h1{font-size:20px;margin:0}h2{font-size:18px;margin:0}h3{font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin:18px 0 6px}
.muted{color:var(--muted)}.warn{color:var(--warn);font-weight:600}
button,.filebtn{font:inherit;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 12px;cursor:pointer}
button:hover,.filebtn:hover{border-color:var(--accent)}
input[type=text],select,textarea{font:inherit;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:8px;padding:6px 8px}
.text{white-space:pre-wrap;overflow-wrap:anywhere;min-width:0}
.step{display:grid;grid-template-columns:64px minmax(0,1fr);gap:10px;padding:10px 0;border-top:1px solid var(--line)}
.stepno{color:var(--muted);font-size:13px;font-weight:600;padding-top:2px}
mjx-container{max-width:100%;overflow-x:auto;overflow-y:hidden}
mjx-container[display="true"]{display:block;padding:2px 0}
details>summary{cursor:pointer}
@media (max-width:640px){.step{grid-template-columns:1fr;gap:2px}}
"""

MATHJAX = r"""<script>
window.MathJax = {
  tex: {inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']], processEscapes: true},
  options: {ignoreHtmlClass: 'no-math'},
  svg: {fontCache: 'global'}
};
</script>
<script async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.min.js"></script>"""

SHEET_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Label audit sheet</title>
<style>""" + CSS + r"""
.bar{display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px}
.bar .grow{flex:1}
#howto{margin:12px 0 0;padding:10px 14px;background:var(--card);border:1px solid var(--line);border-radius:10px}
#howto ul{margin:8px 0 0;padding-left:20px}#howto li{margin:4px 0}
.layout{display:grid;grid-template-columns:150px minmax(0,1fr);gap:16px;margin-top:16px;align-items:start}
#index{position:sticky;top:12px;display:grid;grid-template-columns:repeat(3,1fr);gap:4px}
#index button{padding:4px 0;font-size:13px;border-radius:6px}
#index button.done{border-color:var(--done);color:var(--done)}
#index button.current{background:var(--accent);border-color:var(--accent);color:#fff}
article,form{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px}
form{margin-top:14px}
.itemhead{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.opts{display:flex;flex-wrap:wrap;gap:8px}
.opts label{flex:1 1 170px;display:flex;gap:8px;align-items:flex-start;border:1px solid var(--line);border-radius:8px;padding:8px 10px;cursor:pointer}
.opts label:has(input:checked){border-color:var(--accent);box-shadow:0 0 0 1px var(--accent) inset}
.opts small{display:block;color:var(--muted);line-height:1.35}
.opts.small label{flex:0 0 auto}
.row{display:flex;flex-wrap:wrap;gap:8px 24px;align-items:flex-end;margin-top:4px}
textarea{width:100%;min-height:72px;resize:vertical}
.nav{display:flex;gap:8px;justify-content:space-between;margin:14px 0 40px;flex-wrap:wrap}
#fallback{margin:0 0 30px}#csvout{width:100%;font:12px/1.4 ui-monospace,Menlo,monospace}
@media (max-width:800px){.layout{grid-template-columns:1fr}#index{position:static;grid-template-columns:repeat(auto-fill,minmax(48px,1fr))}}
</style>
""" + MATHJAX + r"""
</head>
<body>
<div class="wrap">
<header>
  <div class="bar">
    <h1>Label audit</h1>
    <span id="progress" class="muted"></span>
    <span class="grow"></span>
    <label>Auditor <input type="text" id="auditor" size="8" placeholder="initials" autocomplete="off"></label>
    <button type="button" id="export">Export CSV</button>
    <label class="filebtn">Import CSV<input type="file" id="import" accept=".csv,text/csv" hidden></label>
  </div>
  <div id="status" class="muted" role="status"></div>
  <details id="howto" open>
    <summary>How to judge</summary>
    <ul>
      <li>The task is the one the critics had: decide whether the solution contains at least one error in any step: a calculation mistake, a logical or conceptual error, or a misreading of the problem.</li>
      <li><b>No error:</b> every step is right.</li>
      <li><b>Gap only:</b> nothing stated is false, but a step is asserted without enough justification, or is loosely worded.</li>
      <li><b>Error:</b> a step states something false, makes an invalid inference, miscalculates or misreads the problem. It counts even when the final answer comes out right.</li>
      <li>For "gap only" and "error", give the earliest step where it happens.</li>
      <li>This sheet holds no labels and no model verdicts, and it does not say how many solutions contain an error.</li>
      <li>Complete all 42 items before the first-pass results are analyzed. You can take breaks and export partial work. This is a selected audit set, not a random sample of the benchmark.</li>
      <li>Work independently before viewing benchmark labels, model answers, or another reviewer's judgments. Record a short mathematical reason and your confidence. Use "Can't tell" when needed; do not guess.</li>
      <li>For a difficult item, save your first judgment before requesting AI help. Keep that assistance and any revised judgment in a separate record. Do not overwrite the independent first-pass CSV.</li>
      <li>Different reviewers must use separate browser profiles and separate CSV files. Enter your initials before starting. A calculator or symbolic check is fine if you record the tool and what it checked in your note.</li>
      <li>Answers are saved in this browser only. Export the CSV when you stop and keep the file in <code>audit/</code>. Import it to continue in another browser.</li>
      <li>If the mathematics looks broken, tick "Show unrendered text" to see the characters the critics saw.</li>
    </ul>
  </details>
</header>
<div class="layout">
  <nav id="index" aria-label="Items"></nav>
  <main>
    <article id="item">
      <div class="itemhead"><h2 id="aid"></h2><label class="muted"><input type="checkbox" id="raw"> Show unrendered text</label></div>
      <h3>Problem</h3>
      <div id="problem" class="text"></div>
      <h3>Solution</h3>
      <div id="steps"></div>
    </article>
    <form id="form" autocomplete="off">
      <h3 style="margin-top:0">Your verdict</h3>
      <div class="opts">
        <label><input type="radio" name="verdict" value="none"><span>No error<small>Every step is right.</small></span></label>
        <label><input type="radio" name="verdict" value="gap"><span>Gap only<small>Nothing false, but a step is not justified.</small></span></label>
        <label><input type="radio" name="verdict" value="error"><span>Error<small>A step is false or invalid.</small></span></label>
        <label><input type="radio" name="verdict" value="unsure"><span>Can't tell<small>Not without more work.</small></span></label>
      </div>
      <div class="row">
        <div><h3>Earliest step with the gap or error</h3><select id="step"></select></div>
        <div><h3>Confidence</h3>
          <div class="opts small">
            <label><input type="radio" name="confidence" value="low">Low</label>
            <label><input type="radio" name="confidence" value="medium">Medium</label>
            <label><input type="radio" name="confidence" value="high">High</label>
          </div>
        </div>
      </div>
      <h3>Note</h3>
      <textarea id="note" placeholder="What is wrong, or why it is fine"></textarea>
      <div style="margin-top:8px"><button type="button" id="clear">Clear this answer</button></div>
    </form>
    <div class="nav">
      <button type="button" id="prev">← Previous</button>
      <button type="button" id="nextopen">Next unjudged</button>
      <button type="button" id="next">Next →</button>
    </div>
    <details id="fallback" hidden><summary>No download? Copy the CSV from here</summary><textarea id="csvout" rows="8" readonly></textarea></details>
  </main>
</div>
</div>
<script id="data" type="application/json">@@DATA@@</script>
<script>
(function () {
  var DATA = JSON.parse(document.getElementById('data').textContent);
  var ITEMS = DATA.items, SHEET = DATA.sheet_id, KEY = 'label-audit:' + SHEET;
  var VERDICTS = {none: 1, gap: 1, error: 1, unsure: 1}, LEVELS = {low: 1, medium: 1, high: 1};
  function $(id) { return document.getElementById(id); }
  var state = {auditor: '', pos: 0, answers: {}};
  var storageOK = true;
  try {
    var saved = localStorage.getItem(KEY);
    if (saved) {
      var o = JSON.parse(saved);
      if (o && typeof o === 'object' && o.answers && typeof o.answers === 'object') {
        state.auditor = typeof o.auditor === 'string' ? o.auditor : '';
        state.answers = o.answers;
        state.pos = Math.min(Math.max(parseInt(o.pos, 10) || 0, 0), ITEMS.length - 1);
      }
    }
  } catch (e) { storageOK = false; }

  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); storageOK = true; } catch (e) { storageOK = false; }
    paintStatus();
  }
  function judged(aid) { var a = state.answers[aid]; return !!(a && a.verdict && ((a.verdict !== 'error' && a.verdict !== 'gap') || a.step)); }
  function paintStatus() {
    var n = ITEMS.filter(function (it) { return judged(it.aid); }).length;
    $('progress').textContent = n + ' of ' + ITEMS.length + ' judged · sheet ' + SHEET;
    $('status').textContent = storageOK ? 'Answers are saved in this browser as you go.' : 'This browser is not saving answers. Export the CSV before you close the page.';
    $('status').className = storageOK ? 'muted' : 'warn';
  }
  function paintIndex() {
    var nav = $('index');
    nav.textContent = '';
    ITEMS.forEach(function (it, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.textContent = it.aid;
      b.className = (judged(it.aid) ? 'done ' : '') + (i === state.pos ? 'current' : '');
      b.title = judged(it.aid) ? 'judged' : 'not judged yet';
      b.addEventListener('click', function () { show(i); });
      nav.appendChild(b);
    });
  }
  var queue = Promise.resolve();
  function typeset() {
    if ($('raw').checked) return;
    // One typeset at a time: moving quickly between items must not start two on the same element.
    queue = queue.then(function () {
      if (window.MathJax && MathJax.typesetPromise) return MathJax.typesetPromise([$('item')]);
    }).catch(function () {});
  }
  function radio(name) { var el = document.querySelector('input[name="' + name + '"]:checked'); return el ? el.value : ''; }
  function setRadio(name, value) {
    document.querySelectorAll('input[name="' + name + '"]').forEach(function (el) { el.checked = (el.value === value); });
  }
  function syncStep() {
    var v = radio('verdict'), on = (v === 'gap' || v === 'error');
    $('step').disabled = !on;
    if (!on) $('step').value = '';
  }
  function show(i) {
    state.pos = i;
    var it = ITEMS[i], box = $('item');
    if (window.MathJax && MathJax.typesetClear) MathJax.typesetClear([box]);
    box.classList.toggle('no-math', $('raw').checked);
    $('aid').textContent = it.aid + ' · item ' + (i + 1) + ' of ' + ITEMS.length;
    $('problem').textContent = it.problem;
    var steps = $('steps');
    steps.textContent = '';
    it.steps.forEach(function (t, k) {
      var d = document.createElement('div'), n = document.createElement('div'), x = document.createElement('div');
      d.className = 'step'; n.className = 'stepno'; x.className = 'text';
      n.textContent = 'Step ' + (k + 1); x.textContent = t;
      d.appendChild(n); d.appendChild(x); steps.appendChild(d);
    });
    var sel = $('step');
    sel.textContent = '';
    var none = document.createElement('option');
    none.value = ''; none.textContent = '—';
    sel.appendChild(none);
    for (var k = 1; k <= it.steps.length; k++) {
      var op = document.createElement('option');
      op.value = String(k); op.textContent = 'Step ' + k;
      sel.appendChild(op);
    }
    var a = state.answers[it.aid] || {};
    setRadio('verdict', a.verdict || '');
    setRadio('confidence', a.confidence || '');
    syncStep();
    sel.value = sel.disabled ? '' : (a.step || '');
    $('note').value = a.note || '';
    paintIndex(); paintStatus(); typeset();
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
    window.scrollTo(0, 0);
  }
  function record() {
    syncStep();
    var it = ITEMS[state.pos];
    var a = {verdict: radio('verdict'), step: $('step').disabled ? '' : $('step').value,
             confidence: radio('confidence'), note: $('note').value, saved_at: new Date().toISOString()};
    if (!a.verdict && !a.step && !a.confidence && !a.note.trim()) delete state.answers[it.aid];
    else state.answers[it.aid] = a;
    save(); paintIndex();
  }
  $('form').addEventListener('change', record);
  $('note').addEventListener('input', record);
  $('form').addEventListener('submit', function (ev) { ev.preventDefault(); });
  $('clear').addEventListener('click', function () {
    setRadio('verdict', ''); setRadio('confidence', ''); $('step').value = ''; $('note').value = '';
    record();
  });
  $('auditor').value = state.auditor;
  $('auditor').addEventListener('input', function () { state.auditor = $('auditor').value.trim(); save(); });
  $('raw').addEventListener('change', function () { show(state.pos); });
  $('prev').addEventListener('click', function () { if (state.pos > 0) show(state.pos - 1); });
  $('next').addEventListener('click', function () { if (state.pos < ITEMS.length - 1) show(state.pos + 1); });
  $('nextopen').addEventListener('click', function () {
    for (var k = 1; k <= ITEMS.length; k++) {
      var j = (state.pos + k) % ITEMS.length;
      if (!judged(ITEMS[j].aid)) { show(j); return; }
    }
    $('status').textContent = 'Every item is judged. Export the CSV.';
  });
  document.addEventListener('keydown', function (ev) {
    var t = ev.target.tagName;
    if (t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT' || ev.metaKey || ev.ctrlKey || ev.altKey) return;
    if (ev.key === 'ArrowLeft') $('prev').click();
    if (ev.key === 'ArrowRight') $('next').click();
  });

  function cell(v) {
    v = (v === null || v === undefined) ? '' : String(v);
    return /[",\r\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
  }
  function toCSV() {
    var rows = [['sheet_id', 'audit_id', 'auditor', 'verdict', 'step', 'confidence', 'note', 'saved_at']];
    ITEMS.forEach(function (it) {
      var a = state.answers[it.aid] || {};
      rows.push([SHEET, it.aid, state.auditor, a.verdict || '', a.step || '', a.confidence || '', a.note || '', a.saved_at || '']);
    });
    return rows.map(function (r) { return r.map(cell).join(','); }).join('\n') + '\n';
  }
  function parseCSV(text) {
    var rows = [], row = [], cur = '', quoted = false;
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (quoted) {
        if (ch === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else quoted = false; }
        else cur += ch;
      } else if (ch === '"') quoted = true;
      else if (ch === ',') { row.push(cur); cur = ''; }
      else if (ch === '\n') { row.push(cur); rows.push(row); row = []; cur = ''; }
      else if (ch !== '\r') cur += ch;
    }
    if (cur !== '' || row.length) { row.push(cur); rows.push(row); }
    return rows;
  }
  $('export').addEventListener('click', function () {
    var text = toCSV();
    $('csvout').value = text;
    $('fallback').hidden = false;
    try {
      var url = URL.createObjectURL(new Blob([text], {type: 'text/csv;charset=utf-8'}));
      var a = document.createElement('a');
      a.href = url;
      a.download = 'audit_responses_' + (state.auditor.replace(/[^A-Za-z0-9_-]/g, '') || 'anon') + '_' + SHEET + '.csv';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    } catch (e) {}
  });
  $('import').addEventListener('change', function (ev) {
    var file = ev.target.files && ev.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function () {
      ev.target.value = '';
      var rows = parseCSV(String(reader.result)), ix = {};
      if (!rows.length) return;
      rows[0].forEach(function (name, j) { ix[name.trim()] = j; });
      var required = ['sheet_id', 'audit_id', 'auditor', 'verdict', 'step'];
      if (required.some(function (k) { return !(k in ix); })) { alert('Missing required CSV columns.'); return; }
      var known = {}, seen = {}, imported = {}, reviewers = {}, n = 0, problem = '';
      ITEMS.forEach(function (it) { known[it.aid] = it.steps.length; });
      rows.slice(1).filter(function (r) { return r.some(function (v) { return v !== ''; }); }).forEach(function (r) {
        function get(k) { return (k in ix && r[ix[k]] !== undefined) ? r[ix[k]] : ''; }
        var aid = get('audit_id'), verdict = get('verdict'), auditor = get('auditor').trim();
        if (get('sheet_id') !== SHEET) problem = 'Sheet ID mismatch. No answers were imported.';
        if (!known[aid] || seen[aid]) problem = 'Unknown or duplicate audit ID. No answers were imported.';
        if (verdict && !VERDICTS[verdict]) problem = 'Unknown verdict. No answers were imported.';
        if (!auditor) problem = 'Each row needs a reviewer identifier. No answers were imported.';
        seen[aid] = true; reviewers[auditor] = true;
        var step = Number(get('step'));
        if (get('step') && (!Number.isInteger(step) || step < 1 || step > known[aid])) problem = 'Invalid step. No answers were imported.';
        var a = {verdict: verdict, step: get('step'),
                 confidence: LEVELS[get('confidence')] ? get('confidence') : '',
                 note: get('note'), saved_at: get('saved_at')};
        if (a.verdict || a.step || a.confidence || a.note) { imported[aid] = a; n++; }
      });
      var names = Object.keys(reviewers);
      if (names.length !== 1) problem = 'Use one reviewer per CSV. No answers were imported.';
      if (problem) { alert(problem); return; }
      if (Object.keys(state.answers).length && state.auditor && state.auditor !== names[0]) {
        alert('Another reviewer has answers in this browser. Use a separate browser profile. No answers were imported.'); return;
      }
      if (Object.keys(state.answers).length && !confirm('Import replaces the current answers. Export your current work first. Continue?')) return;
      state.answers = imported;
      state.auditor = names[0];
      $('auditor').value = state.auditor;
      save(); show(state.pos);
      $('status').textContent = 'Imported ' + n + ' answers.';
    };
    reader.readAsText(file);
  });

  show(state.pos);
})();
</script>
</body>
</html>
"""

KEY_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Label audit key</title>
<style>""" + CSS + r"""
.banner{background:var(--card);border:2px solid var(--warn);border-radius:10px;padding:12px 16px;margin:12px 0 20px}
.item{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:0 0 16px}
.item.contested{border-left:4px solid var(--warn)}
.tag{font-size:13px;font-weight:600;color:var(--muted);margin-left:6px}
.meta{color:var(--muted);margin:4px 0 10px;font-size:14px}
table{border-collapse:collapse;font-size:14px;margin:6px 0 10px}
th,td{text-align:left;padding:3px 16px 3px 0;border-bottom:1px solid var(--line)}
th{color:var(--muted);font-weight:600}
td:nth-child(n+2),th:nth-child(n+2){font-variant-numeric:tabular-nums}
.item details{margin:6px 0}
.quote{background:var(--soft);border-radius:8px;padding:10px 12px;margin-top:6px;font-size:14.5px}
</style>
""" + MATHJAX + r"""
</head>
<body>
<div class="wrap">
<h1>Label audit key · sheet @@SHEET_ID@@</h1>
<div class="banner"><b>Answer key.</b> It shows each item's label and what the critics did at the neutral condition. Open it only after you have exported your blind judgments: knowing that critics found an error is the claim the premise test showed moves a reviewer.</div>
@@BODY@@
</div>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n-clean", type=int, default=10, help="control items labelled correct that no critic flagged")
    ap.add_argument("--n-flawed", type=int, default=5, help="control items labelled flawed that every critic caught")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out-dir", default=str(ROOT / "audit"))
    args = ap.parse_args()

    entries, sheet_id = build(args.n_clean, args.n_flawed, args.seed)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_sheet_html(entries, sheet_id, out / "audit_sheet.html")
    write_key_csv(entries, out / "audit_key.csv")
    write_key_html(entries, sheet_id, out / "audit_key.html")

    tally = collections.Counter((e["group"], e["set"]) for e in entries)
    print(f"sheet {sheet_id}: {len(entries)} items")
    for group in GROUP_TEXT:
        print(f"  {group:18s} " + ", ".join(f"{s} {tally[(group, s)]}" for s in SETS))
    for name in ("audit_sheet.html", "audit_key.csv", "audit_key.html"):
        print(f"wrote {out / name}")


if __name__ == "__main__":
    main()
