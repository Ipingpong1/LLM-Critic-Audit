"""Rate wording run: the rules W1-W5 and the planned secondary measures of prereg/rate_wording.md.

    .venv/bin/python scripts/rate_wording_analysis.py [--audit audit/<file>.csv ...]

Free; reads saved rows only. It joins the rows of the premise test (results/premise/) with the new ones
(results/rate_wording/) by critic, and reads every rule under each label variant of prereg/label_sensitivity.md.
Run it only when every approved job has finished. Writes rate_wording.md and rate_wording.json.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import label_sensitivity as ls  # noqa: E402
import premise_analysis as pa  # noqa: E402
from pilot.analyze import LN81, ci, model_sort_key  # noqa: E402

ARMS = {"br": ("br10", "br90"), "freq": ("freq10", "freq90"), "comp": ("comp10", "comp90"),
        "hist": ("hist10", "hist90"), "user": ("user10", "user90"), "item": ("item_p10", "item_p90")}
OPUS, SOL = "opus-5.5-think", "gpt-6.1-sol-think"   # W4 is about the first, W5 about the second
STAGE_C = (0.05, 0.44)    # Opus's interval for the original line on the hard set (prereg/stage_c.md)
NO_DIFF = 0.15            # W2: "no difference" only when the whole 95% interval lies within this
CEILING = 4               # errors per 200 at neutral at or under which a critic's rho is not interpreted
ALPHA = 0.05


def analyse(rows, items, labels, n_boot, seed):
    """Every rule under one labelling. labels: item id -> True (flawed), False (correct) or None (left out)."""
    rows, items = ls.relabel(rows, items, labels)
    ids = sorted(items)
    fl = np.array([k for k, i in enumerate(ids) if items[i]["has_error"]])
    co = np.array([k for k, i in enumerate(ids) if not items[i]["has_error"]])
    rng = np.random.default_rng(seed)
    fl_boot, co_boot = rng.choice(fl, size=(n_boot, len(fl))), rng.choice(co, size=(n_boot, len(co)))
    by = defaultdict(list)
    for r in rows:
        by[r["model"]].append(r)
    critics, out, brho, w2 = {}, {}, {}, []
    for name in sorted(by, key=model_sort_key):
        if sorted({r["item_id"] for r in by[name]}) != ids:
            raise SystemExit(f"{name}: rows do not cover the items of this variant")
        cr = critics[name] = pa.Critic(name, by[name], fl_boot, co_boot)
        md, k0 = cr.md, cr.col["neutral"]
        wrong = (md.V[md.fl_idx, k0] - md.E[md.fl_idx, k0]).sum() + md.E[md.co_idx, k0].sum()
        d0, bd0 = cr.d[k0], cr.bd[:, k0]
        res = out[name] = {"d_neutral": float(d0), "errors_per_200": float(200 * wrong / md.V[:, k0].sum()), "arms": {}}
        res["ceiling"] = res["errors_per_200"] <= CEILING
        brho[name] = {}
        for arm, (lo, hi) in ARMS.items():
            if not cr.has(lo, hi):
                continue
            dc, bdc = cr.shift(lo, hi)
            b = brho[name][arm] = np.where(bd0 > 0, bdc * np.where(bd0 > 0, bd0, 1.0) / LN81, np.nan)
            res["arms"][arm] = {"rho": float(dc * d0 / LN81), "ci": list(ci(b)), "delta_c": float(dc),
                                "delta_c_ci": list(ci(bdc)), "samples": int(md.T[:, cr.col[lo]].max())}
        if res["arms"]:
            ups = {a: v["ci"][1] for a, v in res["arms"].items()}
            top = max(ups, key=ups.get)
            res["W1"] = {"holds": all(u < 1 for u in ups.values()), "fails_in": [a for a, u in ups.items() if not u < 1],
                         "largest_upper": ups[top], "largest_upper_arm": top, "all_below_half": all(u < 0.5 for u in ups.values())}
        if "br" in res["arms"]:
            for arm in res["arms"]:
                if arm != "br":
                    b = brho[name][arm] - brho[name]["br"]
                    w2.append({"critic": name, "arm": arm, "diff": res["arms"][arm]["rho"] - res["arms"]["br"]["rho"],
                               "ci": list(ci(b)), "p": pa.two_sided_p(b[np.isfinite(b)])})
        if "comp" in res["arms"]:
            lo_, hi_ = res["arms"]["comp"]["delta_c_ci"]
            res["W3"] = "information" if lo_ > 0 else ("number" if hi_ < 0 else "unclear")
        # Secondary: a rate against a claim, as shifts from neutral toward flagging (positive = flags more).
        res["toward_flagging"] = {}
        for cond in ("br90", "item_p90", "claim_bare"):
            if cr.has(cond):
                est, b = cr.shift("neutral", cond)
                res["toward_flagging"][cond] = {"est": float(est), "ci": list(ci(b))}
        # Secondary: accuracy if the stated rate were the true one, beside the neutral verdicts and the ideal observer.
        res["accuracy_at_stated_rate"] = {}
        for arm, (lo, hi) in ARMS.items():
            if arm in res["arms"]:
                for p, cond in ((0.1, lo), (0.9, hi)):
                    k, cs = cr.col[cond], np.log((1 - p) / p) / d0
                    acc = lambda kk: float(p * cr.raw_h[kk] + (1 - p) * (1 - cr.raw_f[kk]))
                    res["accuracy_at_stated_rate"][f"{arm}@{int(100 * p)}"] = {
                        "critic": acc(k), "neutral_verdicts": acc(k0),
                        "ideal": float(p * norm.cdf(d0 / 2 - cs) + (1 - p) * norm.cdf(d0 / 2 + cs))}
    for r, adj in zip(w2, pa.holm([r["p"] for r in w2]) if w2 else []):
        r["p_holm"] = adj
        r["outcome"] = ("differs" if adj < ALPHA else
                        "no difference" if -NO_DIFF < r["ci"][0] and r["ci"][1] < NO_DIFF else "inconclusive")
    w4 = None
    if OPUS in out and "br" in out[OPUS]["arms"]:
        a = out[OPUS]["arms"]["br"]
        w4 = {"rho": a["rho"], "ci": a["ci"], "holds": a["ci"][1] < 1, "inside_stage_c": STAGE_C[0] <= a["rho"] <= STAGE_C[1]}
    w5 = []
    if SOL in critics and critics[SOL].has("presuppose"):
        keep, pa.PRIMARY = pa.PRIMARY, [SOL]
        try:
            for r in pa.primary_tests(critics):
                w5.append({"test": r["test"], "a": r["a"], "b": r["b"], "sign": r["sign"], "est": float(r["est"]),
                           "ci": list(r["ci"]), "p_holm": r["p_holm"], "outcome": ls.outcome(r),
                           "no_shift": bool(-pa.NO_EFFECT < r["ci"][0] and r["ci"][1] < pa.NO_EFFECT)})
        finally:
            pa.PRIMARY = keep
    # Secondary: thinking on minus off in rho, paired, for the open models.
    on_off = []
    for name in brho:
        off = name.replace("-think-", "-nothink-")
        if "-think-" in name and off in brho:
            for arm in brho[name]:
                if arm in brho[off]:
                    on_off.append({"critic": name, "arm": arm, "diff": out[name]["arms"][arm]["rho"] - out[off]["arms"][arm]["rho"],
                                   "ci": list(ci(brho[name][arm] - brho[off][arm]))})
    return {"n_flawed": len(fl), "n_correct": len(co), "critics": out, "W2": w2, "W4": w4, "W5": w5, "on_minus_off": on_off}, critics


def label_free(rows, seed, n_boot=2000):
    """Secondary measures that use no label: flag-rate shift, stated-P shift, flips and the own-confidence benchmark."""
    by = defaultdict(list)
    for r in rows:
        by[r["model"]].append(r)
    rng, out = np.random.default_rng(seed), {}
    logit = lambda p: np.log(np.clip(p, 1, 99) / (100 - np.clip(p, 1, 99)))
    for name in sorted(by, key=model_sort_key):
        ids = sorted({r["item_id"] for r in by[name]})
        ix, n = {i: k for k, i in enumerate(ids)}, len(ids)
        boot = rng.integers(0, n, size=(n_boot, n))
        e, v, lg, nl = (defaultdict(lambda: np.zeros(n)) for _ in range(4))
        v0, p0 = defaultdict(lambda: np.full(n, np.nan)), defaultdict(lambda: np.full(n, np.nan))
        for r in by[name]:
            if r["verdict"] is None:
                continue
            c, k = r["condition"], ix[r["item_id"]]
            v[c][k] += 1
            e[c][k] += r["verdict"] == "error"
            if r.get("p_error") is not None:
                lg[c][k] += logit(r["p_error"]); nl[c][k] += 1
            if r["sample"] == 0:
                v0[c][k] = r["verdict"] == "error"
                p0[c][k] = np.nan if r.get("p_error") is None else r["p_error"]

        def est(x):
            return {"est": float(np.nanmean(x)), "ci": [float(q) for q in np.percentile(np.nanmean(x[boot], 1), [2.5, 97.5])]}
        res = out[name] = {}
        for arm, (lo, hi) in ARMS.items():
            if lo not in v or hi not in v:
                continue
            rate = lambda c: np.where(v[c] > 0, e[c] / np.maximum(v[c], 1), np.nan)
            lgt = lambda c: np.where(nl[c] > 0, lg[c] / np.maximum(nl[c], 1), np.nan)
            a = res[arm] = {"flag_shift_pp": est(100 * (rate(hi) - rate(lo))), "stated_p_shift_logodds": est(lgt(hi) - lgt(lo))}
            ok = np.isfinite(v0[lo]) & np.isfinite(v0[hi])
            vl, vh = v0[lo] == 1, v0[hi] == 1
            a["flips"] = {"n": int(ok.sum()), "to_error_at_90": int((ok & vh & ~vl).sum()), "to_correct_at_90": int((ok & ~vh & vl).sum())}
            if "br50" in v:
                # A Bayesian reading the stated P(error) at the 50% line as a posterior flags iff p > 90 when told 10%,
                # and iff p > 10 when told 90% (pilot/analyze.py, bayes_check). Counts only, so no label is used.
                ok = ok & np.isfinite(v0["br50"]) & np.isfinite(p0["br50"])
                p50 = np.where(ok, p0["br50"], 50.0)
                flagged, passed, b10, b90 = ok & (v0["br50"] == 1), ok & (v0["br50"] == 0), p50 > 90, p50 > 10
                a["own_confidence"] = {
                    "n": int(ok.sum()),
                    "predicted": int((flagged & ~b10).sum() + (passed & b90).sum()),
                    "made": int((flagged & ~b10 & ~vl).sum() + (passed & b90 & vh).sum()),
                    "unpredicted": int((flagged & b10 & ~vl).sum() + (passed & ~b90 & vh).sum()),
                    "wrong_way": int((passed & vl).sum() + (flagged & ~vh).sum())}
    return out


def f(x, nd=2, plus=False):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else (f"{x:+.{nd}f}" if plus else f"{x:.{nd}f}")


def fci(v, plus=False, nd=2, key="rho"):
    return "–" if v is None else f"{f(v[key], nd, plus)} [{f(v['ci'][0], nd)}, {f(v['ci'][1], nd)}]"


def table(header, rows):
    return ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(r) + " |" for r in rows] + [""]


def report(results, free, health, variants, args, n_rows):
    names = list(results["original"]["critics"])
    L = ["# Rate wording run: results", "",
         f"Plan: `prereg/rate_wording.md`. {n_rows} rows, {len(names)} critic runs, {args.bootstrap} resamples. "
         "ρ is [c(10%) − c(90%)] × d′(neutral) / ln 81. Intervals are 95%, from an item bootstrap.", "",
         "## Labels and ceiling", "",
         "Errors per 200 at `neutral`. At 4 or fewer, ρ is reported but not interpreted under that labelling (marked \\*).", ""]
    L += table(["critic"] + [ls.VARIANT_TEXT.get(v, v) for v in variants],
               [[n] + [f(results[v]["critics"][n]["errors_per_200"], 1) + ("\\*" if results[v]["critics"][n]["ceiling"] else "")
                       for v in variants] for n in names])
    L += ["## W1, under-use in every wording", "", "Holds when the interval for ρ lies below 1 in every arm the critic has.", ""]
    L += table(["critic"] + [ls.VARIANT_TEXT.get(v, v) for v in variants] + ["all below 0.5 (original labels)"],
               [[n] + [("–" if "W1" not in (c := results[v]["critics"][n]) else
                        ("holds" if c["W1"]["holds"] else "fails in " + ", ".join(c["W1"]["fails_in"]))
                        + f" (largest upper limit {f(c['W1']['largest_upper'])}, {c['W1']['largest_upper_arm']})"
                        + ("\\*" if c["ceiling"] else "")) for v in variants]
                + [("–" if "W1" not in results["original"]["critics"][n] else
                    "yes" if results["original"]["critics"][n]["W1"]["all_below_half"] else "no")] for n in names])
    for v in variants:
        L += [f"### ρ by arm, {ls.VARIANT_TEXT.get(v, v)} ({results[v]['n_flawed']} flawed, {results[v]['n_correct']} correct)", ""]
        L += table(["critic"] + list(ARMS), [[n + ("\\*" if results[v]["critics"][n]["ceiling"] else "")]
                                              + [fci(results[v]["critics"][n]["arms"].get(a)) for a in ARMS] for n in names])
    L += ["## W2, a wording changes use", "",
          f"ρ(arm) − ρ(`br`), paired, Holm across all tests of a labelling. \"No difference\" needs the whole interval within ±{NO_DIFF}.", ""]
    for v in variants:
        w2 = results[v]["W2"]
        count = {o: sum(r["outcome"] == o for r in w2) for o in ("differs", "no difference", "inconclusive")}
        L += [f"### {ls.VARIANT_TEXT.get(v, v)}: {len(w2)} tests; {count['differs']} differ, {count['no difference']} no difference, "
              f"{count['inconclusive']} inconclusive", ""]
        cell = {(r["critic"], r["arm"]): f"{fci(r, True, key='diff')}, {r['outcome']}" + (f" (Holm p {r['p_holm']:.3f})" if r["outcome"] == "differs" else "")
                for r in w2}
        L += table(["critic"] + [a for a in ARMS if a != "br"], [[n] + [cell.get((n, a), "–") for a in ARMS if a != "br"] for n in names])
    L += ["## W3, information or number", "",
          "Under `comp`, c(told 10% have errors) − c(told 90% have errors). Above 0: follows the information. Below 0: the number or the word.", ""]
    L += table(["critic"] + [ls.VARIANT_TEXT.get(v, v) for v in variants],
               [[n] + [("–" if "comp" not in (c := results[v]["critics"][n])["arms"] else
                        f"{f(c['arms']['comp']['delta_c'], 2, True)} [{f(c['arms']['comp']['delta_c_ci'][0])}, {f(c['arms']['comp']['delta_c_ci'][1])}], {c['W3']}")
                       for v in variants] for n in names])
    L += ["## W4, Opus on new items", ""]
    for v in variants:
        w = results[v]["W4"]
        L.append(f"- **{ls.VARIANT_TEXT.get(v, v)}:** " + ("not run." if w is None else
                 f"ρ for `br` {fci(w)}; {'holds' if w['holds'] else 'fails'}; "
                 f"{'inside' if w['inside_stage_c'] else 'outside'} the Stage C interval [{STAGE_C[0]}, {STAGE_C[1]}]."))
    L += ["", "## W5, the claim tests on GPT-6.1 Sol", ""]
    if not results["original"]["W5"]:
        L += ["Not run.", ""]
    else:
        # A test with no predicted direction (T7) reads "no shift" or "inconclusive" when it did not move (prereg/premise.md).
        word = lambda r: r["outcome"] if r["sign"] or r["outcome"] == "moved" else ("no shift" if r["no_shift"] else "inconclusive")
        tests = [(r["test"], f"`{r['a']}` − `{r['b']}`") for r in results["original"]["W5"]]
        by = {v: {r["test"]: r for r in results[v]["W5"]} for v in variants}
        L += table(["test", "contrast"] + [ls.VARIANT_TEXT.get(v, v) for v in variants],
                   [[t, what] + [f"{fci(by[v][t], True, key='est')}, {word(by[v][t])}" for v in variants] for t, what in tests])
    o = results["original"]
    L += ["## Secondary measures", "", "Planned, uncorrected, not primary. The first three use no label.", "",
          "### Flag-rate shift: share of all solutions flagged when told 90%, minus when told 10% (points)", ""]
    L += table(["critic"] + list(ARMS), [[n] + [fci(free[n].get(a, {}).get("flag_shift_pp"), True, 1, "est") for a in ARMS] for n in names])
    L += ["### Own-confidence benchmark: verdict changes made, of those the critic's stated P(error) at `br50` predicts (sample 0)", ""]
    oc = lambda n, a: free[n].get(a, {}).get("own_confidence")
    L += table(["critic"] + list(ARMS), [[n] + [("–" if oc(n, a) is None else f"{oc(n, a)['made']} of {oc(n, a)['predicted']}"
                                                 f" (+{oc(n, a)['unpredicted']} unpredicted, {oc(n, a)['wrong_way']} wrong way)") for a in ARMS] for n in names])
    L += ["### Stated P(error) shift in log-odds, 90% minus 10% (a calibrated Bayesian: 4.39 before clipping at 1 and 99)", ""]
    L += table(["critic"] + list(ARMS), [[n] + [fci(free[n].get(a, {}).get("stated_p_shift_logodds"), True, 2, "est") for a in ARMS] for n in names])
    L += ["### Verdicts that flip between the 10% and the 90% version (sample 0): toward \"error\" at 90% / toward \"correct\" at 90%", ""]
    fl = lambda n, a: free[n].get(a, {}).get("flips")
    L += table(["critic"] + list(ARMS), [[n] + [("–" if fl(n, a) is None else f"{fl(n, a)['to_error_at_90']} / {fl(n, a)['to_correct_at_90']} of {fl(n, a)['n']}")
                                                 for a in ARMS] for n in names])
    L += ["### A rate against a claim: shift from `neutral` toward flagging, original labels", ""]
    L += table(["critic", "told 90% of the batch", "told 90% for this solution", "\"This solution contains an error.\""],
               [[n] + [fci(o["critics"][n]["toward_flagging"].get(c), True, key="est") for c in ("br90", "item_p90", "claim_bare")] for n in names])
    L += ["### What under-use costs if the stated rate were true: accuracy (%) for `br`, original labels", "",
          "Critic's verdicts under that line / its neutral verdicts / ideal observer with its d′.", ""]
    acc = lambda n, k: o["critics"][n]["accuracy_at_stated_rate"].get(k)
    L += table(["critic", "true rate 10%", "true rate 90%"],
               [[n] + [("–" if acc(n, k) is None else " / ".join(f(100 * acc(n, k)[x], 1) for x in ("critic", "neutral_verdicts", "ideal")))
                       for k in ("br@10", "br@90")] for n in names])
    if o["on_minus_off"]:
        L += ["### Thinking on − off in ρ, paired, original labels", ""]
        cell = {(r["critic"], r["arm"]): fci(r, True, key="diff") for r in o["on_minus_off"]}
        L += table(["critic (thinking on)"] + list(ARMS), [[n] + [cell.get((n, a), "–") for a in ARMS] for n in dict.fromkeys(r["critic"] for r in o["on_minus_off"])])
    return L + health


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rows", nargs="*", default=["results/premise/*.jsonl", "results/rate_wording/*.jsonl"], help="globs, from the project root")
    ap.add_argument("--audit", nargs="*", default=[], help="exported audit file(s) from audit/audit_sheet.html")
    ap.add_argument("--bootstrap", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out-dir", default=str(ROOT / "results" / "rate_wording" / "analysis"))
    args = ap.parse_args()

    key, sheet = ls.read_key()
    all_items = {s: {it["id"]: it for it in map(json.loads, (ROOT / cfg["items"]).open())} for s, cfg in ls.SETS.items()}
    items = all_items["premise"]
    base = {i: bool(it["has_error"]) for i, it in items.items()}
    contested = {k["item_id"] for k in key if k["set"] == "premise" and k["group"].startswith("contested")}
    labels = {"original": base,
              "drop": {i: None if i in contested else v for i, v in base.items()},
              "flip": {i: (not v) if i in contested else v for i, v in base.items()}}
    for path in args.audit:
        auditor, answers = ls.read_audit(path, key, sheet)
        gaps = any(a.get("verdict") == "gap" for a in answers.values())
        for gap_is_error in ((False, True) if gaps else (False,)):
            name = f"audit, {auditor}" + (f": gap = {'error' if gap_is_error else 'no error'}" if gaps else "")
            labels[name] = ls.audit_labels(all_items, key, answers, gap_is_error)["premise"]
    rows = ls.load(args.rows)
    seen = set()
    for r in rows:
        k = (r["model"], r["condition"], r["item_id"], r["sample"])
        if k in seen:
            raise SystemExit(f"duplicate trial {k}")
        seen.add(k)
        if r["item_id"] not in items or bool(r["has_error"]) != base[r["item_id"]]:
            raise SystemExit("a result row disagrees with data/items_premise.jsonl")
    results, critics0 = {}, None
    for v, lab in labels.items():
        print(f"{v} ...", flush=True)
        results[v], critics = analyse(rows, items, lab, args.bootstrap, args.seed)
        critics0 = critics0 or critics
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    free = label_free(rows, args.seed)
    health = ["## Pipeline rules (original labels)", ""] + pa.rules_section(critics0)[2:]
    (out / "rate_wording.md").write_text("\n".join(report(results, free, health, list(labels), args, len(rows))) + "\n")
    (out / "rate_wording.json").write_text(json.dumps({"bootstrap": args.bootstrap, "sheet": sheet, "variants": list(labels),
                                                        "results": results, "label_free": free}, indent=1, default=float))
    print(f"wrote {out / 'rate_wording.md'}")


if __name__ == "__main__":
    main()
