"""Label re-analysis: could wrong ProcessBench labels change a headline claim? Free; reads saved rows only.

Plan and reading rules: prereg/label_sensitivity.md. The contested items come from audit/audit_key.csv.

    .venv/bin/python scripts/label_sensitivity.py
    .venv/bin/python scripts/label_sensitivity.py --audit audit/audit_responses_<name>_<sheet>.csv

Writes results/label_sensitivity/report.md and report.json. No item is named in either, so the report can be read
before the audit is done. The estimates come from the same code as the original analyses (pilot/analyze.py and
scripts/premise_analysis.py), run on relabelled rows.
"""
import argparse
import csv
import datetime
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm, rankdata

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from pilot.analyze import LN81, analyze_model, model_sort_key  # noqa: E402
from pilot.prompts import ARM_LABELS  # noqa: E402
import premise_analysis as pa  # noqa: E402

SETS = {
    "hard": {"items": "data/items_hard.jsonl", "globs": ["results/torch_hard/*.jsonl", "results/frontier/stage_c/*.jsonl"],
             "ref": "br50", "saved": "results/torch_hard/analysis/summary.json"},
    "premise": {"items": "data/items_premise.jsonl", "globs": ["results/premise/*.jsonl"],
                "ref": "neutral", "saved": "results/premise/analysis/summary.json",
                "saved_tests": "results/premise/analysis/premise.json"},
}
SHIFTS = ("presuppose", "lenient")                       # threshold shifts from neutral that R2 and the tables use
AUC_CONDS = ("neutral", "presuppose", "claim_bare", "claim_mistake", "claim_reviewer")
VARIANT_TEXT = {"original": "original", "drop": "contested left out", "flip": "contested flipped",
                "no_damaged": "damaged text left out"}


def load(globs):
    """Result rows without the reply text, which nothing here reads and which is most of the file size."""
    rows = []
    for g in globs:
        for p in sorted(ROOT.glob(g)):
            with p.open() as f:
                for line in f:
                    r = json.loads(line)
                    if r.get("retryable"):
                        continue
                    r.pop("reasoning", None)
                    r.pop("raw", None)
                    rows.append(r)
    return rows


def read_key():
    with (ROOT / "audit" / "audit_key.csv").open(newline="") as f:
        rows = sorted(csv.DictReader(f), key=lambda r: r["audit_id"])
    sheet = hashlib.sha1("|".join(f'{r["set"]}:{r["item_id"]}' for r in rows).encode()).hexdigest()[:8]
    return rows, sheet


def relabel(rows, items, labels):
    """labels: item id -> True (flawed), False (correct) or None (left out)."""
    keep = {i for i, v in labels.items() if v is not None}
    items2 = {i: {**it, "has_error": labels[i]} for i, it in items.items() if i in keep}
    rows2 = [{**r, "has_error": labels[r["item_id"]]} for r in rows if r["item_id"] in keep]
    return rows2, items2


def stated_auc(rows, cond):
    """AUC of the stated P(error), every sample pooled."""
    s = [r["p_error"] for r in rows if r["condition"] == cond and r["has_error"] and r.get("p_error") is not None]
    n = [r["p_error"] for r in rows if r["condition"] == cond and not r["has_error"] and r.get("p_error") is not None]
    if not s or not n:
        return None
    rk = rankdata(np.array(s + n, float))
    return float((rk[: len(s)].sum() - len(s) * (len(s) + 1) / 2) / (len(s) * len(n)))


def digest(res, rows):
    md, col = res["_md"], res["_col"]
    by = {c["condition"]: c for c in res["conditions"]}
    k0 = col["neutral"]
    raw = lambda idx: float(md.E[idx, k0].sum() / md.V[idx, k0].sum())
    wrong = (md.V[md.fl_idx, k0] - md.E[md.fl_idx, k0]).sum() + md.E[md.co_idx, k0].sum()
    return {
        "ref": res["ref"], "d_ref": by[res["ref"]]["d_prime"],
        "fa_neutral": raw(md.co_idx), "hit_neutral": raw(md.fl_idx),
        "errors_per_200": float(200 * wrong / md.V[:, k0].sum()),
        "arms": {a: {"low": v["low"], "high": v["high"], "rho": v["rho"], "ci": list(v["rho_ci"])} for a, v in res["arms"].items()},
        "shifts": {c: {"est": by[c]["c_minus_neutral"], "ci": list(by[c]["c_minus_neutral_ci"])} for c in SHIFTS if c in by},
        "rho_bayes": (res.get("bayes") or {}).get("rho_bayes"),
        "auc_stated": {c: stated_auc(rows, c) for c in AUC_CONDS if c in by},
    }


def outcome(r):
    return "held" if r["held"] and r["sign"] else ("moved" if r["held"] else ("against" if r["against"] else "not shown"))


def premise_tests(rows, items, n_boot, seed):
    """The 18 primary tests, built the way scripts/premise_analysis.py builds them."""
    has_error = {i: it["has_error"] for i, it in items.items()}
    ids = sorted(has_error)
    fl = np.array([k for k, i in enumerate(ids) if has_error[i]])
    co = np.array([k for k, i in enumerate(ids) if not has_error[i]])
    rng = np.random.default_rng(seed)
    fl_boot = rng.choice(fl, size=(n_boot, len(fl)))
    co_boot = rng.choice(co, size=(n_boot, len(co)))
    critics = {}
    for name in pa.PRIMARY:
        r = [x for x in rows if x["model"] == name]
        if sorted({x["item_id"] for x in r}) != ids:
            raise SystemExit(f"{name}: rows do not cover the items of this variant")
        critics[name] = pa.Critic(name, r, fl_boot, co_boot)
    return [{"critic": r["critic"], "test": r["test"], "a": r["a"], "b": r["b"], "sign": r["sign"], "est": r["est"],
             "ci": list(r["ci"]), "p_holm": r["p_holm"], "outcome": outcome(r)} for r in pa.primary_tests(critics)]


def run_variant(name, cfg, rows, items, labels, args, keep_models=False):
    rows2, items2 = relabel(rows, items, labels)
    out = {"n_flawed": sum(it["has_error"] for it in items2.values()),
           "n_correct": sum(not it["has_error"] for it in items2.values()), "critics": {}}
    models = {}
    for m in sorted({r["model"] for r in rows2}, key=model_sort_key):
        mine = [r for r in rows2 if r["model"] == m]
        res = analyze_model(m, mine, items2, args.bootstrap, cfg["ref"], np.random.default_rng(args.seed))
        out["critics"][m] = digest(res, mine)
        if keep_models:
            models[m] = res
    if name == "premise":
        out["tests"] = premise_tests(rows2, items2, args.bootstrap_tests, args.seed)
    return out, models


def assignment_stats(md, cidx):
    """d' and c per condition under every keep-or-flip assignment of the contested items.
    Row 0 keeps every label, the last row flips them all. Same formula as ModelData.rates."""
    k = len(cidx)
    masks = ((np.arange(2 ** k)[:, None] >> np.arange(k)) & 1).astype(float)
    base = md.flawed.astype(float)
    w = np.repeat(base[None], len(masks), 0)
    w[:, cidx] = np.abs(base[cidx][None] - masks)
    E, V = md.E / md._k, md.V / md._k
    h, ns, f, nn = w @ E, w @ V, (1 - w) @ E, (1 - w) @ V
    zH, zF = norm.ppf((h + 0.5) / (ns + 1)), norm.ppf((f + 0.5) / (nn + 1))
    return zH - zF, -(zH + zF) / 2


def assignment_ranges(name, models, contested, tests):
    """Smallest and largest point estimate of each quantity over all assignments, per critic."""
    out = {"critics": {}, "tests": []}
    for m, res in models.items():
        md, col = res["_md"], res["_col"]
        cidx = np.array([md.ids.index(i) for i in sorted(contested)])
        d, c = assignment_stats(md, cidx)
        span = lambda x: {"min": float(x.min()), "max": float(x.max()), "keep_all": float(x[0]), "flip_all": float(x[-1])}
        entry = {"arms": {a: span((c[:, col[v["low"]]] - c[:, col[v["high"]]]) * d[:, col[res["ref"]]] / LN81)
                          for a, v in res["arms"].items()},
                 "shifts": {s: span(c[:, col[s]] - c[:, col["neutral"]]) for s in SHIFTS if s in col}}
        out["critics"][m] = entry
        if name == "premise" and m in pa.PRIMARY:
            for t in tests:
                if t["critic"] == m:
                    out["tests"].append({"critic": m, "test": t["test"], **span(c[:, col[t["a"]]] - c[:, col[t["b"]]])})
    return out


def close(a, b):
    return a is None and b is None or (a is not None and b is not None and abs(a - b) < 1e-9)


def check_reproduction(name, cfg, orig):
    """Largest difference between this run under the original labels and the saved analysis files."""
    worst, n = 0.0, 0
    saved = {s["model"]: s for s in json.load((ROOT / cfg["saved"]).open())}
    for m, d in orig["critics"].items():
        s = saved[m]
        pairs = [(d["arms"][a]["rho"], s["arms"][a]["rho"]) for a in d["arms"]]
        pairs += [(x, y) for a in d["arms"] for x, y in zip(d["arms"][a]["ci"], s["arms"][a]["rho_ci"])]
        by = {c["condition"]: c for c in s["conditions"]}
        pairs += [(d["d_ref"], by[d["ref"]]["d_prime"])]
        pairs += [(v["est"], by[c]["c_minus_neutral"]) for c, v in d["shifts"].items()]
        for x, y in pairs:
            worst, n = max(worst, abs(x - y)), n + 1
    if "saved_tests" in cfg:
        st = {(t["critic"], t["test"]): t for t in json.load((ROOT / cfg["saved_tests"]).open())["primary_tests"]}
        for t in orig["tests"]:
            s = st[t["critic"], t["test"]]
            for x, y in [(t["est"], s["est"]), (t["p_holm"], s["p_holm"]), *zip(t["ci"], s["ci"])]:
                worst, n = max(worst, abs(x - y)), n + 1
    return worst, n


# ---- reading rules (prereg/label_sensitivity.md) -------------------------------------------------------------------

def excludes_zero(lo_hi):
    return lo_hi[0] > 0 or lo_hi[1] < 0


def rule_r1(results, variant):
    fails, n, top = [], 0, (-math.inf, "")
    for s, by_variant in results.items():
        for m, d in by_variant["original"]["critics"].items():
            for a, v in d["arms"].items():
                if not v["ci"][1] < 1:
                    continue
                n += 1
                hi = by_variant[variant]["critics"][m]["arms"][a]["ci"][1]
                if hi > top[0]:
                    top = (hi, f"{m}, {ARM_LABELS.get(a, a)}, {s} set")
                if not hi < 1:
                    fails.append(f"{m}, {ARM_LABELS.get(a, a)}, {s} set: upper limit {hi:.2f}")
    return {"n": n, "fails": fails, "largest_upper": top[0], "largest_upper_at": top[1]}


def rule_r2(results, variant):
    fails, n = [], 0
    o, v = results["hard"]["original"]["critics"], results["hard"][variant]["critics"]
    for m in o:
        a, b = o[m]["shifts"]["presuppose"], v[m]["shifts"]["presuppose"]
        n += 1
        if np.sign(a["est"]) != np.sign(b["est"]) or excludes_zero(a["ci"]) != excludes_zero(b["ci"]):
            fails.append(f"{m}: {cell(a)} under the original labels, {cell(b)} here")
    return {"n": n, "fails": fails}


def rule_r3(results, variant):
    fails = []
    o, v = results["premise"]["original"]["tests"], results["premise"][variant]["tests"]
    for a, b in zip(o, v):
        if a["outcome"] != b["outcome"]:
            fails.append(f"{a['critic']} {a['test']}: {a['outcome']} under the original labels, {b['outcome']} here "
                         f"({cell(b)}, Holm p {b['p_holm']:.4f})")
    return {"n": len(o), "fails": fails}


def rule_r4(ranges, results):
    top = max(((e["arms"]["base_rate"]["max"], f"{m}, {s} set") for s, r in ranges.items()
               for m, e in r["critics"].items() if "base_rate" in e["arms"]))
    held = {(t["critic"], t["test"]) for t in results["premise"]["original"]["tests"] if t["outcome"] == "held"}
    flips = [f"{t['critic']} {t['test']}: {t['min']:+.2f} to {t['max']:+.2f}" for t in ranges["premise"]["tests"]
             if (t["critic"], t["test"]) in held and np.sign(t["min"]) != np.sign(t["max"])]
    return {"largest_rho": top[0], "largest_rho_at": top[1], "n_held": len(held), "sign_changes": flips,
            "fails": ([f"largest base-rate ρ {top[0]:.2f} ({top[1]})"] if not top[0] < 1 else []) + flips}


# ---- audit ---------------------------------------------------------------------------------------------------------

def read_audit(path, key, sheet, allow_partial=False):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    required = {'sheet_id', 'audit_id', 'auditor', 'verdict', 'step'}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f'{path}: empty audit or missing required columns {sorted(required)}')
    ids = [r['audit_id'] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError(f'{path}: duplicate audit IDs')
    sheets = {r["sheet_id"] for r in rows}
    if sheets != {sheet}:
        raise SystemExit(f"{path}: sheet id {sorted(sheets)} does not match the key ({sheet}).")
    known = {k["audit_id"] for k in key}
    if not allow_partial and set(ids) != known:
        raise ValueError(f'{path}: incomplete audit; missing {len(known - set(ids))} IDs')
    bad = [r["audit_id"] for r in rows if r["audit_id"] not in known or r["verdict"] not in ("", "none", "gap", "error", "unsure")]
    if bad:
        raise SystemExit(f"{path}: unknown audit ids or verdicts at {bad[:5]}")
    if not allow_partial and any(not r['verdict'] for r in rows):
        raise ValueError(f'{path}: blank judgments cannot be treated as a completed audit')
    reviewers = {r['auditor'].strip() for r in rows}
    if len(reviewers) != 1 or '' in reviewers:
        raise ValueError(f'{path}: require one consistent, nonblank reviewer identifier')
    item_sets = {s: {it['id']: it for it in map(json.loads, (ROOT / cfg['items']).read_text().splitlines())} for s, cfg in SETS.items()}
    lookup = {k['audit_id']: k for k in key}
    for r in rows:
        if r['verdict'] in ('error', 'gap'):
            k = lookup[r['audit_id']]
            n = len(item_sets[k['set']][k['item_id']]['steps'])
            try:
                step = int(r['step'])
            except (TypeError, ValueError):
                raise ValueError(f"{path}: {r['audit_id']} requires an earliest affected step") from None
            if not 1 <= step <= n:
                raise ValueError(f"{path}: {r['audit_id']} step outside 1..{n}")
    auditor = next(iter(reviewers))
    return auditor, {r["audit_id"]: r for r in rows}


def audit_labels(items, key, answers, gap_is_error):
    labels = {s: {i: bool(it["has_error"]) for i, it in its.items()} for s, its in items.items()}
    for k in key:
        v = answers.get(k["audit_id"], {}).get("verdict", "")
        if v:
            labels[k["set"]][k["item_id"]] = {"error": True, "none": False, "gap": gap_is_error, "unsure": None}[v]
    return labels


def audit_table(key, answers):
    groups = ["contested_correct", "contested_flawed", "control_correct", "control_flawed"]
    out = {}
    for g in groups:
        ks = [k for k in key if k["group"] == g]
        vs = [answers.get(k["audit_id"], {}).get("verdict", "") for k in ks]
        entry = {"items": len(ks), **{name: vs.count(v) for name, v in
                                      (("error", "error"), ("gap", "gap"), ("none", "none"), ("unsure", "unsure"), ("unjudged", ""))}}
        if g.endswith("flawed"):
            found = [k for k, v in zip(ks, vs) if v == "error"]
            entry["same_step"] = sum(answers[k["audit_id"]].get("step", "").strip() == k["label_first_error_step"].strip() for k in found)
        out[g] = entry
    return out


# ---- added after the first run (prereg/label_sensitivity.md, "Deviations") -------------------------------------------

CEILING = 4   # errors per 200 at neutral at or under which prereg/premise.md stops interpreting a critic's shifts


def post_hoc(results, variants):
    """How far the size of rho moves, and which critics the relabelled sets leave with almost no errors."""
    moved, ceiling = {}, {}
    for v in variants[1:]:
        moved[v], n = [], 0
        for s, by_variant in results.items():
            for m, d in by_variant["original"]["critics"].items():
                for a, o in d["arms"].items():
                    n += 1
                    x = by_variant[v]["critics"][m]["arms"][a]["rho"]
                    if not o["ci"][0] <= x <= o["ci"][1]:
                        moved[v].append({"critic": m, "arm": a, "set": s, "original": o["rho"], "original_ci": o["ci"], "here": x})
        moved[v] = {"n": n, "cases": moved[v]}
    for v in variants:
        ceiling[v] = {s: [m for m, d in results[s][v]["critics"].items() if d["errors_per_200"] <= CEILING] for s in results}
    return {"moved_outside_original_interval": moved, "at_ceiling": ceiling}


# ---- report --------------------------------------------------------------------------------------------------------

def num(x, nd=2, plus=False):
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else (f"{x:+.{nd}f}" if plus else f"{x:.{nd}f}")


def cell(v, plus=True):
    est = v.get("est", v.get("rho"))
    return f"{num(est, plus=plus)} [{num(v['ci'][0])}, {num(v['ci'][1])}]"


def table(header, rows):
    return ["| " + " | ".join(header) + " |", "|" + "---|" * len(header), *("| " + " | ".join(r) + " |" for r in rows), ""]


def report(results, ranges, rules, r4, repro, variants, audits, sheet, key, args, extra):
    vt = lambda v: VARIANT_TEXT.get(v, v)
    n_cont = {s: sum(k["set"] == s and k["group"].startswith("contested") for k in key) for s in SETS}
    out = ["# Label re-analysis: results", "",
           f"Generated by `scripts/label_sensitivity.py` on {datetime.date.today().isoformat()} from the saved replies. "
           f"Plan and reading rules: `prereg/label_sensitivity.md`. Contested items: those of audit sheet `{sheet}` "
           f"({n_cont['hard']} on the hard set, {n_cont['premise']} on the premise set). No item is named here.", "",
           "## Check: the original labels reproduce the saved analyses", ""]
    for s, (worst, n) in repro.items():
        out.append(f"- {s} set: {n} saved numbers compared, largest difference {worst:.1e}"
                   f"{' (exact)' if worst < 1e-9 else ' (**not exact**)'}.")
    out += ["", "## Reading rules", "",
            "A claim survives a variant when its rule gives the same answer there as under the original labels.", ""]
    names = {"R1": "R1, the stated rate is under-used (95% interval for ρ below 1)",
             "R2": 'R2, "contains an error" moves the threshold on the hard set',
             "R3": "R3, the 18 premise tests keep their outcome"}
    rows = []
    for r in ("R1", "R2", "R3"):
        cells = []
        for v in variants[1:]:
            x = rules[v][r]
            word = "survives" if not x["fails"] else f"**fails** ({len(x['fails'])} of {x['n']})"
            if r == "R1":
                word += f"; largest upper limit {x['largest_upper']:.2f}"
            cells.append(word)
        rows.append([f"{names[r]} ({rules[variants[1]][r]['n']} cases)", *cells])
    out += table(["rule", *(vt(v) for v in variants[1:])], rows)
    out.append(f"- **R4, every keep-or-flip assignment:** {'survives' if not r4['fails'] else '**fails**'}. The largest "
               f"base-rate ρ any assignment gives any critic run is {r4['largest_rho']:.2f} ({r4['largest_rho_at']}). Of the "
               f"{r4['n_held']} premise tests that held, {len(r4['sign_changes'])} can change the sign of their point estimate.")
    for v in variants[1:]:
        for r in ("R1", "R2", "R3"):
            for f in rules[v][r]["fails"]:
                out.append(f"- {r} fails under \"{vt(v)}\": {f}")
    for f in r4["sign_changes"]:
        out.append(f"- R4 sign change: {f}")
    for v in variants[1:]:
        out.append(f"- R1 under \"{vt(v)}\": the largest upper limit is at {rules[v]['R1']['largest_upper_at']}.")
    out += ["", "## Items per variant", ""]
    out += table(["set", *(vt(v) for v in variants)],
                 [[s, *(f"{results[s][v]['n_flawed']} flawed, {results[s][v]['n_correct']} correct" for v in variants)] for s in SETS])

    for a in audits:
        out += [f"## Audit by {a['auditor']}", "", "What the auditor said, by group of the sheet.", ""]
        rows = []
        for g, e in a["table"].items():
            rows.append([g.replace("_", ", labelled "), str(e["items"]), str(e["error"]), str(e["gap"]), str(e["none"]),
                         str(e["unsure"]), str(e["unjudged"]), f"{e['same_step']} of {e['error']}" if "same_step" in e else "–"])
        out += table(["group", "items", "error", "gap only", "no error", "can't tell", "not judged", "same earliest step as the label"], rows)

    def rho_table(s, arm, title):
        crit = [m for m, d in results[s]["original"]["critics"].items() if arm in d["arms"]]
        if not crit:
            return []
        rows = [[m, *(cell(results[s][v]["critics"][m]["arms"][arm], plus=False) for v in variants),
                 f"{ranges[s]['critics'][m]['arms'][arm]['min']:.2f} to {ranges[s]['critics'][m]['arms'][arm]['max']:.2f}"] for m in crit]
        return [f"### ρ, {title}", "", *table(["critic", *(vt(v) for v in variants), "every assignment (point estimate)"], rows)]

    for s, label in (("hard", "Hard set"), ("premise", "Premise set")):
        out += [f"## {label}", "",
                f"ρ with 95% intervals; reference d′ at `{SETS[s]['ref']}`; {args.bootstrap:,} resamples. 0 = ignores the stated "
                "value, 1 = ideal observer.", ""]
        for arm in ("base_rate", "use", "payoff", "labels", "item_rate"):
            out += rho_table(s, arm, ARM_LABELS[arm])
        if s == "hard":
            for sh in SHIFTS:
                rows = [[m, *(cell(results[s][v]["critics"][m]["shifts"][sh]) for v in variants),
                         f"{ranges[s]['critics'][m]['shifts'][sh]['min']:+.2f} to {ranges[s]['critics'][m]['shifts'][sh]['max']:+.2f}"]
                        for m in results[s]["original"]["critics"]]
                out += [f"### c(`{sh}`) − c(`neutral`)", "", "Negative = flags more than with no added line.", "",
                        *table(["critic", *(vt(v) for v in variants), "every assignment (point estimate)"], rows)]
        else:
            rng = {(t["critic"], t["test"]): t for t in ranges[s]["tests"]}
            rows = []
            for k, t in enumerate(results[s]["original"]["tests"]):
                r = rng[t["critic"], t["test"]]
                rows.append([t["critic"], t["test"], f"{t['a']} − {t['b']}",
                             *(f"{cell(results[s][v]['tests'][k])} {results[s][v]['tests'][k]['outcome']}" for v in variants),
                             f"{r['min']:+.2f} to {r['max']:+.2f}"])
            out += ["### Primary tests", "",
                    f"Difference in c with its 95% interval and the outcome under Holm across the 18; {args.bootstrap_tests:,} resamples.", "",
                    *table(["critic", "test", "contrast", *(vt(v) for v in variants), "every assignment (point estimate)"], rows)]

    out += ["## Added after the first run (not in the plan)", "",
            "The rules above ask whether an interval stays below 1. They do not ask how far the estimate itself moves, "
            "and they do not ask whether a relabelled set leaves a critic with too few errors to measure a threshold. "
            "Both turned out to matter, so they are counted here. See \"Deviations\" in the plan.", "",
            "**ρ estimates that leave their original 95% interval**", ""]
    for v in variants[1:]:
        mv = extra["moved_outside_original_interval"][v]
        out.append(f"- {vt(v)}: {len(mv['cases'])} of {mv['n']} critic-and-arm cases.")
        for c in mv["cases"]:
            out.append(f"  - {c['critic']}, {ARM_LABELS.get(c['arm'], c['arm'])}, {c['set']} set: {c['original']:.2f} "
                       f"[{c['original_ci'][0]:.2f}, {c['original_ci'][1]:.2f}] becomes {c['here']:.2f}")
    out += ["", f"**Critic runs with {CEILING} or fewer errors per 200 at neutral** (the ceiling rule of `prereg/premise.md`: "
            "shifts are reported but not interpreted)", ""]
    out += table(["set", *(vt(v) for v in variants)],
                 [[s, *(", ".join(extra["at_ceiling"][v][s]) or "none" for v in variants)] for s in SETS])
    out += ["## Described, not judged", "", "These are expected to move with the labels.", ""]
    for s, label in (("hard", "Hard set"), ("premise", "Premise set")):
        rows = []
        for m in results[s]["original"]["critics"]:
            g = lambda f: " / ".join(f(results[s][v]["critics"][m]) for v in variants)
            rows.append([m, g(lambda d: f"{d['d_ref']:.2f}"), g(lambda d: f"{100 * d['fa_neutral']:.0f}"),
                         g(lambda d: f"{100 * d['hit_neutral']:.0f}"), g(lambda d: f"{d['errors_per_200']:.1f}"),
                         g(lambda d: num(d["rho_bayes"]))])
        out += [f"### {label}: " + " / ".join(vt(v) for v in variants), "",
                *table(["critic", f"d′ at `{SETS[s]['ref']}`", "false alarms at neutral, %", "hits at neutral, %", "errors per 200 at neutral", "ρ_Bayes"], rows)]
    rows = []
    for m in pa.PRIMARY:
        for c in AUC_CONDS:
            if c in results["premise"]["original"]["critics"][m]["auc_stated"]:
                rows.append([m, c, *(num(results["premise"][v]["critics"][m]["auc_stated"][c], 3) for v in variants)])
    out += ["### Premise set: AUC of the stated P(error), primary critics", "",
            "Whether the stated probability still separates flawed from correct solutions under a claim.", "",
            *table(["critic", "condition", *(vt(v) for v in variants)], rows)]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audit", nargs="*", default=[], help="exported audit file(s) from audit/audit_sheet.html")
    ap.add_argument("--bootstrap", type=int, default=2000, help="resamples for ρ and the shifts (2,000 in the original analyses)")
    ap.add_argument("--bootstrap-tests", type=int, default=10000, help="resamples for the premise tests (10,000 originally)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out-dir", default=str(ROOT / "results" / "label_sensitivity"))
    args = ap.parse_args()

    key, sheet = read_key()
    items = {s: {it["id"]: it for it in map(json.loads, (ROOT / cfg["items"]).open())} for s, cfg in SETS.items()}
    contested = {s: {k["item_id"] for k in key if k["set"] == s and k["group"].startswith("contested")} for s in SETS}
    damaged = {s: {i for i, it in its.items() if any(ch in it["problem"] + "".join(it["steps"]) for ch in "\x0c\x08")}
               for s, its in items.items()}
    base = {s: {i: bool(it["has_error"]) for i, it in its.items()} for s, its in items.items()}
    labels = {"original": base,
              "drop": {s: {i: None if i in contested[s] else v for i, v in base[s].items()} for s in SETS},
              "flip": {s: {i: (not v) if i in contested[s] else v for i, v in base[s].items()} for s in SETS},
              "no_damaged": {s: {i: None if i in damaged[s] else v for i, v in base[s].items()} for s in SETS}}
    audits = []
    for path in args.audit:
        auditor, answers = read_audit(path, key, sheet)
        tab = audit_table(key, answers)
        audits.append({"auditor": auditor, "file": Path(path).name, "table": tab})
        if sum(e["gap"] for e in tab.values()):
            labels[f"audit, {auditor}: gap = no error"] = audit_labels(items, key, answers, False)
            labels[f"audit, {auditor}: gap = error"] = audit_labels(items, key, answers, True)
        else:
            labels[f"audit, {auditor}"] = audit_labels(items, key, answers, False)
    variants = list(labels)

    results, ranges, repro = {}, {}, {}
    for s, cfg in SETS.items():
        rows = load(cfg["globs"])
        if any(r["item_id"] not in items[s] or bool(r["has_error"]) != base[s][r["item_id"]] for r in rows):
            raise SystemExit(f"{s}: a result row disagrees with {cfg['items']}")
        results[s] = {}
        for v in variants:
            print(f"{s} set, {v} ...", flush=True)
            results[s][v], models = run_variant(s, cfg, rows, items[s], labels[v][s], args, keep_models=v == "original")
            if v == "original":
                ranges[s] = assignment_ranges(s, models, contested[s], results[s][v].get("tests", []))
                repro[s] = check_reproduction(s, cfg, results[s][v])
        # The assignment code must agree with the main code at its two ends.
        for m, e in ranges[s]["critics"].items():
            for a, r in e["arms"].items():
                assert close(r["keep_all"], results[s]["original"]["critics"][m]["arms"][a]["rho"]), (s, m, a)
                assert close(r["flip_all"], results[s]["flip"]["critics"][m]["arms"][a]["rho"]), (s, m, a)

    rules = {v: {"R1": rule_r1(results, v), "R2": rule_r2(results, v), "R3": rule_r3(results, v)} for v in variants[1:]}
    r4 = rule_r4(ranges, results)
    extra = post_hoc(results, variants)
    text = report(results, ranges, rules, r4, repro, variants, audits, sheet, key, args, extra)

    dest = Path(args.out_dir)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "report.md").write_text("\n".join(text) + "\n")
    (dest / "report.json").write_text(json.dumps(
        {"sheet": sheet, "bootstrap": args.bootstrap, "bootstrap_tests": args.bootstrap_tests, "variants": variants,
         "reproduction": {s: {"largest_difference": w, "numbers": n} for s, (w, n) in repro.items()},
         "rules": rules, "R4": r4, "added_after_first_run": extra, "audits": audits, "results": results, "assignment_ranges": ranges}, indent=1, default=float))
    start = text.index("## Reading rules")
    print("\n".join(text[2:text.index("## Items per variant", start)]))
    print(f"wrote {dest / 'report.md'} and {dest / 'report.json'}")


if __name__ == "__main__":
    main()
