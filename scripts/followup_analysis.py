"""Rate-use follow-up: families A to D of prereg/rate_use_followup.md. Free; reads saved rows only.

    .venv/bin/python scripts/followup_analysis.py [--rows <globs>] [--audit audit/<file>.csv ...]

Joins the held-out rows of the premise test, the rate-wording run and the follow-up (results/followup/) by critic, and
reads every rule under each label variant (original, contested left out, contested flipped, and any audit). Inference
follows the results freeze (pilot/inference.py): exact within-item randomization tests for paired verdict contrasts,
studentized problem-cluster bootstrap for differences in criterion shifts, whole-problem bootstrap intervals (descriptive).
Run it only when every approved job has finished. Writes results/followup/analysis/followup.md and followup.json.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import label_sensitivity as ls  # noqa: E402
import premise_analysis as pa  # noqa: E402
from pilot.analyze import LN81, ci, model_sort_key  # noqa: E402
from pilot.inference import ProblemDesign, claim_test, holm, interaction_test, interval, stable_seed  # noqa: E402

A_CRITICS = ["opus-5.5-think", "qwen3.5:27b-think-bf16-t1", "gpt-6.1-sol-think"]
A_TESTS = [("A1", "note_bare", "neutral", -1, "a note's claim moves the threshold"),
           ("A2", "claim_bare", "note_bare", -1, "the system prompt's own claim moves more than a note's"),
           ("A3", "note_bare", "claim_random", 0, "the note against the note declared random")]
BR, BAYES, EXP = ("br10", "br90"), ("bayes10", "bayes90"), ("exp10", "exp90")
PAPER = {v: (f"paper_{v}10", f"paper_{v}90") for v in ("self", "other", "methods", "true")}
OPUS = "opus-5.5-think"
NO_SHIFT = 0.3      # A3 "no shift": the whole interval within this (prereg/premise.md's rule)
NEAR_IDEAL = (0.8, 0.5)   # B2, C2, D: rho at or above the first with its lower limit above the second
CEILING = 4
ALPHA = 0.05


def rho_of(cr, lo, hi, ref):
    """rho = [c(lo) - c(hi)] x d'(ref) / ln 81, with its bootstrap draws (nan where d' <= 0)."""
    k = cr.col
    d, bd = cr.d[k[ref]], cr.bd[:, k[ref]]
    dc, bdc = cr.shift(lo, hi)
    b = np.where(bd > 0, bdc * np.where(bd > 0, bd, 1.0) / LN81, np.nan)
    return float(dc * d / LN81), b


def contrast(cr, design, weights, pair, base, ref):
    """A difference in rho between two 10/90 arms: studentized interaction test on c (the freeze's W2 method) and the
    descriptive interval of the rho difference from the bootstrap draws."""
    r = interaction_test(cr.md, design, weights, [*pair, *base])
    rho_a, b_a = rho_of(cr, *pair, ref)
    rho_b, b_b = rho_of(cr, *base, ref)
    r.update(rho_a=rho_a, rho_a_ci=interval(b_a), rho_b=rho_b, rho_b_ci=interval(b_b),
             rho_diff=rho_a - rho_b, rho_diff_ci=interval(b_a - b_b))
    return r


def near_ideal(rho, lo_hi):
    return bool(rho >= NEAR_IDEAL[0] and lo_hi[0] > NEAR_IDEAL[1])


def analyse(rows, items, labels, n_boot, seed, draws):
    rows, items = ls.relabel(rows, items, labels)
    ids = sorted(items)
    design = ProblemDesign.build(items, ids)
    weights = design.weights(n_boot, stable_seed(seed, "followup"))
    fl_boot, co_boot = design.indices(weights)
    by = defaultdict(list)
    for r in rows:
        by[r["model"]].append(r)
    critics, out = {}, {"critics": {}, "A": [], "B": [], "C": [], "D": {}}
    for name in sorted(by, key=model_sort_key):
        if sorted({r["item_id"] for r in by[name]}) != ids:
            raise SystemExit(f"{name}: rows do not cover the items of this variant")
        cr = critics[name] = pa.Critic(name, by[name], fl_boot, co_boot)
        md, k0 = cr.md, cr.col["neutral"]
        wrong = (md.V[md.fl_idx, k0] - md.E[md.fl_idx, k0]).sum() + md.E[md.co_idx, k0].sum()
        res = out["critics"][name] = {"d_neutral": float(cr.d[k0]),
                                      "errors_per_200": float(200 * wrong / md.V[:, k0].sum()), "arms": {}}
        res["ceiling"] = res["errors_per_200"] <= CEILING
        for arm, (lo, hi), ref in (("br", BR, "neutral"), ("bayes", BAYES, "neutral"), ("exp", EXP, "exp50"),
                                   *((f"paper_{v}", p, "neutral") for v, p in PAPER.items())):
            if cr.has(lo, hi, ref):
                rho, b = rho_of(cr, lo, hi, ref)
                res["arms"][arm] = {"rho": rho, "ci": interval(b), "ref": ref, "samples": int(md.T[:, cr.col[lo]].max())}
        # Family A: attribution.
        if name in A_CRITICS and cr.has("note_bare", "neutral", "claim_bare", "claim_random"):
            for tid, a, bb, sign, what in A_TESTS:
                try:
                    r = claim_test(by[name], items, a, bb, draws, stable_seed("A", name, tid))
                except ValueError as e:   # unequal repeats with an unparsed reply: fall back to the bootstrap p
                    est, bt = cr.shift(a, bb)
                    r = dict(estimate=float(est), p=pa.two_sided_p(bt[np.isfinite(bt)]), method=f"bootstrap_fallback ({e})")
                r.update(critic=name, test=tid, a=a, b=bb, sign=sign, what=what, ci=interval(cr.shift(a, bb)[1]))
                out["A"].append(r)
            fa = lambda c: float(100 * cr.raw_f[cr.col[c]])
            res["false_alarms"] = {c: fa(c) for c in ("neutral", "note_bare", "claim_bare", "claim_random", "claim_reviewer") if cr.has(c)}
        # Family B: the posterior rule spelled out.
        if cr.has(*BAYES, *BR, "neutral"):
            r = contrast(cr, design, weights, BAYES, BR, "neutral")
            r.update(critic=name, family="B", ceiling=res["ceiling"])
            # B3, label-free: the reported posterior's shift, and whether verdicts follow the stated rule.
            lg = lambda p: np.log(np.clip(p, 1, 99) / (100 - np.clip(p, 1, 99)))
            sh, follow = {}, {}
            for c in BAYES:
                ps = [x["p_error"] for x in by[name] if x["condition"] == c and x.get("p_error") is not None]
                vs = [(x["p_error"] > 50) == (x["verdict"] == "error") for x in by[name]
                      if x["condition"] == c and x.get("p_error") is not None and x["verdict"] is not None]
                sh[c], follow[c] = float(np.mean(lg(np.array(ps, float)))) if ps else float("nan"), float(np.mean(vs)) if vs else float("nan")
            ps_br = {c: [x["p_error"] for x in by[name] if x["condition"] == c and x.get("p_error") is not None] for c in BR}
            r["B3"] = {"stated_p_shift_logodds": sh["bayes90"] - sh["bayes10"],
                       "stated_p_shift_logodds_br": float(np.mean(lg(np.array(ps_br["br90"], float))) - np.mean(lg(np.array(ps_br["br10"], float)))),
                       "verdict_follows_posterior_rule": follow}
            out["B"].append(r)
        # Family C: the rate shown in examples.
        if cr.has(*EXP, "exp50", *BR, "neutral"):
            r = contrast(cr, design, weights, EXP, BR, "neutral")   # the c interaction, scaled by d'(neutral) for the test
            rho_e, b_e = rho_of(cr, *EXP, "exp50")                  # the arm's own rho uses d'(exp50), as the plan fixes
            rho_b, b_b = rho_of(cr, *BR, "neutral")
            k = cr.col
            r.update(critic=name, family="C", ceiling=res["ceiling"], rho_a=rho_e, rho_a_ci=interval(b_e),
                     rho_diff=rho_e - rho_b, rho_diff_ci=interval(b_e - b_b),
                     d_exp50_minus_neutral=float(cr.d[k["exp50"]] - cr.d[k0]),
                     d_exp50_minus_neutral_ci=interval(cr.bd[:, k["exp50"]] - cr.bd[:, k0]),
                     c_exp50_minus_neutral=float(cr.c[k["exp50"]] - cr.c[k0]),
                     c_exp50_minus_neutral_ci=interval(cr.bc[:, k["exp50"]] - cr.bc[:, k0]))
            out["C"].append(r)
        # Family D: the paper, Opus only.
        if name == OPUS and cr.has(*PAPER["self"], *BR, "neutral"):
            D = out["D"]
            if cr.has(*PAPER["self"]):
                D["D1"] = contrast(cr, design, weights, PAPER["self"], BR, "neutral")
            if cr.has(*PAPER["other"]):
                D["D2"] = contrast(cr, design, weights, PAPER["self"], PAPER["other"], "neutral")
            if cr.has(*PAPER["methods"]):
                D["D3"] = contrast(cr, design, weights, PAPER["self"], PAPER["methods"], "neutral")
            if cr.has(*PAPER["true"]):
                D["D4"] = contrast(cr, design, weights, PAPER["true"], PAPER["self"], "neutral")
            rho_s, b_s = rho_of(cr, *PAPER["self"], "neutral")
            D["D5"] = {"rho_self": rho_s, "ci": interval(b_s), "overshoot": bool(interval(b_s)[0] > 1)}
            D["ceiling"] = res["ceiling"]
    # Corrections and readings.
    for r, p in zip(out["A"], holm([r["p"] for r in out["A"]]) if out["A"] else []):
        r["p_holm"] = p
        sig = p < ALPHA
        r["held"] = bool(sig and (r["sign"] == 0 or np.sign(r["estimate"]) == r["sign"]))
        r["no_shift"] = bool(-NO_SHIFT < r["ci"][0] and r["ci"][1] < NO_SHIFT)
    out["A_reading"] = {}
    for name in A_CRITICS:
        t = {r["test"]: r for r in out["A"] if r["critic"] == name}
        if len(t) == 3:
            a1, a2, a3 = t["A1"], t["A2"], t["A3"]
            if a2["held"] and a3["no_shift"]:
                word = "attribution alone discounts (A2 held, A3 no shift)"
            elif a3["held"] and a3["estimate"] < 0 and a1["held"]:
                word = "the reliability statement does the work (A3 held and negative, A1 held)"
            elif not a1["held"]:
                word = "neither: the note's claim does not move this critic (A1 not shown)"
            else:
                word = "mixed"
            out["A_reading"][name] = word
    for fam, up in (("B", "B1"), ("C", "C1")):
        tests = out[fam]
        for r, p in zip(tests, holm([r["p"] for r in tests]) if tests else []):
            r["p_holm"] = p
            r[up] = bool(p < ALPHA and r["rho_diff"] > 0)       # the instruction / the examples raise use
            r[up.replace("1", "2")] = near_ideal(r["rho_a"], r["rho_a_ci"])
    if out["C"]:
        for r in out["C"]:
            r["C3"] = bool(r["d_exp50_minus_neutral_ci"][0] > 0.5)
    D = out["D"]
    keys = [k for k in ("D1", "D2", "D3") if k in D]
    for k, p in zip(keys, holm([D[k]["p"] for k in keys]) if keys else []):
        D[k]["p_holm"] = p
        D[k]["held"] = bool(p < ALPHA)
    if "D4" in D:
        D["D4"]["p_holm"] = D["D4"]["p"]
        D["D4"]["held"] = bool(D["D4"]["p"] < ALPHA and D["D4"]["rho_diff"] < 0)
    return out, critics


def f(x, nd=2, plus=False):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else (f"{x:+.{nd}f}" if plus else f"{x:.{nd}f}")


def fci(est, lo_hi, nd=2, plus=False):
    return f"{f(est, nd, plus)} [{f(lo_hi[0], nd)}, {f(lo_hi[1], nd)}]"


def table(header, rows):
    return ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(r) + " |" for r in rows] + [""]


def report(results, health, variants, args, n_rows):
    names = list(results["original"]["critics"])
    L = ["# Rate-use follow-up: results", "",
         f"Plan: `prereg/rate_use_followup.md`. {n_rows} rows, {len(names)} critic runs, {args.bootstrap} whole-problem resamples, "
         f"{args.draws} randomization draws where needed. ρ is [c(10%) − c(90%)] × d′(ref) / ln 81; intervals are descriptive.", "",
         "## Labels and ceiling", "", "Errors per 200 at `neutral`. At 4 or fewer, ρ is reported but not interpreted (marked \\*).", ""]
    L += table(["critic"] + [ls.VARIANT_TEXT.get(v, v) for v in variants],
               [[n] + [f(results[v]["critics"][n]["errors_per_200"], 1) + ("\\*" if results[v]["critics"][n]["ceiling"] else "") for v in variants] for n in names])
    for v in variants:
        R = results[v]
        L += [f"## {ls.VARIANT_TEXT.get(v, v)} labels", "", "### ρ by arm (d′ reference in brackets)", ""]
        arms = list(dict.fromkeys(a for n in names for a in R["critics"][n]["arms"]))
        L += table(["critic"] + arms, [[n + ("\\*" if R["critics"][n]["ceiling"] else "")]
                                       + [("–" if a not in R["critics"][n]["arms"] else fci(R["critics"][n]["arms"][a]["rho"], R["critics"][n]["arms"][a]["ci"]) + f" ({R['critics'][n]['arms'][a]['ref']})") for a in arms] for n in names])
        if R["A"]:
            L += ["### Family A, attribution (exact within-item tests, Holm over the family)", ""]
            L += table(["critic", "test", "contrast", "predicted", "difference in c [95%]", "Holm p", "outcome"],
                       [[r["critic"], r["test"], f"{r['a']} − {r['b']}", {-1: "negative", 1: "positive", 0: "none"}[r["sign"]],
                         fci(r["estimate"], r["ci"], plus=True), f"{r['p_holm']:.4f}",
                         "held" if r["held"] else ("no shift" if r["no_shift"] and r["sign"] == 0 else "not shown")] for r in R["A"]])
            L += ["False alarms per 100 correct solutions:", ""]
            L += table(["critic", "neutral", "note_bare", "claim_bare", "claim_random", "claim_reviewer"],
                       [[n] + [f(R["critics"][n]["false_alarms"].get(c), 0) for c in ("neutral", "note_bare", "claim_bare", "claim_random", "claim_reviewer")]
                        for n in names if "false_alarms" in R["critics"][n]])
            L += ["Reading: " + "; ".join(f"**{n}**: {w}" for n, w in R["A_reading"].items()), ""]
        for fam, title, a_name in (("B", "Family B, the posterior rule spelled out", "ρ, bayes"), ("C", "Family C, the rate shown in examples", "ρ, exp (d′ at exp50)")):
            if R[fam]:
                L += [f"### {title} (studentized interaction test on c, Holm over the critics)", ""]
                extra = ["d′(exp50) − d′(neutral)", "c(exp50) − c(neutral)", "C3"] if fam == "C" else ["stated P shift, bayes / br (log-odds)", "verdict follows own posterior rule"]
                rows = []
                for r in R[fam]:
                    row = [r["critic"] + ("\\*" if r["ceiling"] else ""), fci(r["rho_a"], r["rho_a_ci"]), fci(r["rho_b"], r["rho_b_ci"]),
                           fci(r["rho_diff"], r["rho_diff_ci"], plus=True), f"{r['p_holm']:.4f}" + ("" if r["inferential_status"] == "eligible" else " (descriptive)"),
                           "yes" if r[fam + "1"] else "no", "yes" if r[fam + "2"] else "no"]
                    if fam == "C":
                        row += [fci(r["d_exp50_minus_neutral"], r["d_exp50_minus_neutral_ci"], plus=True), fci(r["c_exp50_minus_neutral"], r["c_exp50_minus_neutral_ci"], plus=True), "yes" if r["C3"] else "no"]
                    else:
                        b3 = r["B3"]
                        row += [f"{f(b3['stated_p_shift_logodds'])} / {f(b3['stated_p_shift_logodds_br'])}",
                                " / ".join(f"{100 * b3['verdict_follows_posterior_rule'][c]:.0f}%" for c in BAYES)]
                    rows.append(row)
                L += table(["critic", a_name, "ρ, br", "difference", "Holm p", fam + "1 raises use", fam + "2 near ideal"] + extra, rows)
        if R["D"]:
            D = R["D"]
            L += ["### Family D, the paper (Opus only, exploratory)" + (" \\*ceiling" if D.get("ceiling") else ""), ""]
            rows = []
            for k, what in (("D1", "self − br"), ("D2", "self − other"), ("D3", "self − methods"), ("D4", "true − self")):
                if k in D:
                    r = D[k]
                    rows.append([k, what, fci(r["rho_a"], r["rho_a_ci"]), fci(r["rho_b"], r["rho_b_ci"]), fci(r["rho_diff"], r["rho_diff_ci"], plus=True),
                                 f"{r['p_holm']:.4f}" + ("" if r["inferential_status"] == "eligible" else " (descriptive)"), "held" if r["held"] else "not shown"])
            L += table(["rule", "contrast", "ρ, first", "ρ, second", "difference", "Holm p", "outcome"], rows)
            L += [f"D5, overshoot: ρ_self {fci(D['D5']['rho_self'], D['D5']['ci'])}; " + ("**overshoot** (lower limit above 1)." if D["D5"]["overshoot"] else "no overshoot."), ""]
    return L + health


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rows", nargs="*", default=["results/premise/*.jsonl", "results/rate_wording/*.jsonl", "results/followup/*.jsonl"])
    ap.add_argument("--items", default="data/items_premise.jsonl")
    ap.add_argument("--audit", nargs="*", default=[])
    ap.add_argument("--variants", default="original,drop,flip", help="label variants to read (original,drop,flip)")
    ap.add_argument("--bootstrap", type=int, default=10000)
    ap.add_argument("--draws", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out-dir", default=str(ROOT / "results" / "followup" / "analysis"))
    ap.add_argument("--a-critics", default=",".join(A_CRITICS), help="critics for family A (simulated checks override this)")
    ap.add_argument("--paper-critic", default=OPUS, help="critic for family D (simulated checks override this)")
    args = ap.parse_args()
    A_CRITICS[:] = args.a_critics.split(",")
    globals()["OPUS"] = args.paper_critic

    items = {it["id"]: it for it in map(json.loads, (ROOT / args.items).open())}
    base = {i: bool(it["has_error"]) for i, it in items.items()}
    labels = {"original": base}
    if any(v in args.variants for v in ("drop", "flip")):
        key, sheet = ls.read_key()
        contested = {k["item_id"] for k in key if k["set"] == "premise" and k["group"].startswith("contested")}
        labels["drop"] = {i: None if i in contested else v for i, v in base.items()}
        labels["flip"] = {i: (not v) if i in contested else v for i, v in base.items()}
        all_items = {s: {it["id"]: it for it in map(json.loads, (ROOT / cfg["items"]).open())} for s, cfg in ls.SETS.items()}
        for path in args.audit:
            auditor, answers = ls.read_audit(path, key, sheet)
            gaps = any(a.get("verdict") == "gap" for a in answers.values())
            for gap_is_error in ((False, True) if gaps else (False,)):
                name = f"audit, {auditor}" + (f": gap = {'error' if gap_is_error else 'no error'}" if gaps else "")
                labels[name] = ls.audit_labels(all_items, key, answers, gap_is_error)["premise"]
    labels = {v: lab for v, lab in labels.items() if v in args.variants.split(",") or v.startswith("audit")}
    rows = ls.load(args.rows)
    seen = set()
    for r in rows:
        k = (r["model"], r["condition"], r["item_id"], r["sample"])
        if k in seen:
            raise SystemExit(f"duplicate trial {k}")
        seen.add(k)
        if r["item_id"] not in items or bool(r["has_error"]) != base[r["item_id"]]:
            raise SystemExit(f"a result row disagrees with {args.items}")
    results, critics0 = {}, None
    for v, lab in labels.items():
        print(f"{v} ...", flush=True)
        results[v], critics = analyse(rows, items, lab, args.bootstrap, args.seed, args.draws)
        critics0 = critics0 or critics
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    health = ["## Pipeline rules (original labels)", ""] + pa.rules_section(critics0)[2:]
    (out / "followup.md").write_text("\n".join(report(results, health, list(labels), args, len(rows))) + "\n")
    (out / "followup.json").write_text(json.dumps({"bootstrap": args.bootstrap, "draws": args.draws, "variants": list(labels), "results": results},
                                                  indent=1, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x)))
    print(f"wrote {out / 'followup.md'}")


if __name__ == "__main__":
    main()
