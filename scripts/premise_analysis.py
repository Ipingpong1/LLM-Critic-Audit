"""Premise test: the pre-registered tests and checks (prereg/premise.md). Free; reads saved rows only.

    .venv/bin/python -m pilot.analyze results/premise/*.jsonl --items data/items_premise.jsonl --ref neutral \
        --out-dir results/premise/analysis
    .venv/bin/python scripts/premise_analysis.py       # writes results/premise/analysis/premise.md and premise.json

c − c(neutral) < 0 means a critic flags more than it does with no added line. Every critic gets the same item resamples, so
differences between conditions and between critics are paired. Run it only when every job has finished (prereg/premise.md).
"""
import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pilot.analyze import LN81, ModelData, ci, load_rows, model_sort_key  # noqa: E402
from pilot.prompts import CONDITIONS  # noqa: E402

# The critics the primary tests are about. The rest are described, with uncorrected intervals, and are not tested.
PRIMARY = ["qwen3.5:27b-think-bf16-t1", "opus-5.5-think"]
# id, condition, compared with, predicted sign (0: no direction fixed), what it asks
TESTS = [
    ("T1", "presuppose", "neutral", -1, "the original wording replicates on new items"),
    ("T2", "claim_bare", "neutral", -1, "the claim alone, with no instruction to check"),
    ("T3", "claim_mistake", "neutral", -1, "the claim in other words"),
    ("T4", "claim_reviewer", "neutral", -1, "the claim attributed to someone else"),
    ("T5", "presuppose", "check_only", -1, "the claim beyond an instruction to check"),
    ("T6", "presuppose", "may_error", -1, "the claim beyond raising the possibility"),
    ("T7", "claim_random", "neutral", 0, "a claim the critic is told carries no information"),
    ("T8", "claim_random", "claim_bare", 1, "saying so weakens the claim"),
    ("T9", "claim_correct", "neutral", 1, "the opposite claim moves the threshold the other way"),
]
NO_EFFECT = 0.3   # "no shift" is claimed only when the whole 95% CI lies within this
ALPHA = 0.05


def fmt(x, nd=2, plus=False):
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else (f"{x:+.{nd}f}" if plus else f"{x:.{nd}f}")


def fci(x, lo_hi, nd=2):
    return f"{fmt(x, nd, True)} [{fmt(lo_hi[0], nd)}, {fmt(lo_hi[1], nd)}]"


def two_sided_p(b):
    return min(1.0, (2 * min((b <= 0).sum(), (b >= 0).sum()) + 1) / (len(b) + 1))


def holm(ps):
    """Holm-adjusted p-values, in the order given."""
    order = np.argsort(ps)
    adj, running = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = running
    return adj


class Critic:
    def __init__(self, name, rows, fl_boot, co_boot):
        self.name, self.rows = name, rows
        self.conds = [c for c in CONDITIONS if any(r["condition"] == c for r in rows)]
        self.col = {c: k for k, c in enumerate(self.conds)}
        self.md = ModelData(rows, self.conds)
        md = self.md
        H, F, d, c = md.rates(md.fl_idx[None], md.co_idx[None])
        self.d, self.c = d[0], c[0]
        self.bd, self.bc = md.rates(fl_boot, co_boot)[2:]
        self.raw_f = md.E[md.co_idx].sum(0) / md.V[md.co_idx].sum(0)
        self.raw_h = md.E[md.fl_idx].sum(0) / md.V[md.fl_idx].sum(0)
        self.bf = md.E[co_boot].sum(1) / md.V[co_boot].sum(1)
        self.bh = md.E[fl_boot].sum(1) / md.V[fl_boot].sum(1)

    def has(self, *conds):
        return all(c in self.col for c in conds)

    def shift(self, a, b):
        i, j = self.col[a], self.col[b]
        return self.c[i] - self.c[j], self.bc[:, i] - self.bc[:, j]

    def correct_flags(self, cond):
        """Share of samples flagged, per correct solution."""
        k = self.col[cond]
        return (self.md.E[self.md.co_idx, k] / np.maximum(self.md.V[self.md.co_idx, k], 1))

    def verdicts(self):
        return {(r["condition"], r["item_id"], r["sample"]): r["verdict"] for r in self.rows if r["verdict"] is not None}


def per_critic_table(cr):
    md = cr.md
    out = [f"### {cr.name}", "",
           "| condition | samples | false alarms % | hits % | Δ false alarms [95% CI] | Δ hits [95% CI] | d′ − d′(neutral) [95% CI] "
           "| c | c − c(neutral) [95% CI] | stated P(error) on correct: mean, median | unparsed |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    n0 = cr.col.get("neutral")
    for c in cr.conds:
        k = cr.col[c]
        ps = [r["p_error"] for r in cr.rows if r["condition"] == c and not r["has_error"] and r.get("p_error") is not None]
        dF = 100 * (cr.raw_f[k] - cr.raw_f[n0])
        dH = 100 * (cr.raw_h[k] - cr.raw_h[n0])
        dF_b, dH_b = 100 * (cr.bf[:, k] - cr.bf[:, n0]), 100 * (cr.bh[:, k] - cr.bh[:, n0])
        dd = cr.d[k] - cr.d[n0]
        dd_b = cr.bd[:, k] - cr.bd[:, n0]
        s, sb = cr.shift(c, "neutral")
        same = c == "neutral"
        unp = int(md.T[:, k].sum() - md.V[:, k].sum())
        out.append(f"| {c} | {int(md.T[:, k].max())} | {100 * cr.raw_f[k]:.0f} | {100 * cr.raw_h[k]:.0f} "
                   f"| {'–' if same else fci(dF, ci(dF_b), 0)} | {'–' if same else fci(dH, ci(dH_b), 0)} "
                   f"| {'–' if same else fci(dd, ci(dd_b))} | {fmt(cr.c[k])} | {'–' if same else fci(s, ci(sb))} "
                   f"| {np.mean(ps):.0f}, {np.median(ps):.0f} | {unp} |")
    return out


def primary_tests(critics):
    """All primary tests with Holm adjustment across them. Returns rows of results."""
    res = []
    for name in PRIMARY:
        cr = critics.get(name)
        if cr is None:
            continue
        for tid, a, b, sign, what in TESTS:
            if not cr.has(a, b):
                continue
            est, boot = cr.shift(a, b)
            res.append(dict(critic=name, test=tid, a=a, b=b, sign=sign, what=what, est=est, ci=ci(boot), p=two_sided_p(boot)))
    for r, adj in zip(res, holm([r["p"] for r in res]) if res else []):
        r["p_holm"] = adj
        sig = adj < ALPHA
        r["held"] = bool(sig and (r["sign"] == 0 or np.sign(r["est"]) == r["sign"]))
        r["against"] = bool(sig and r["sign"] != 0 and np.sign(r["est"]) != r["sign"])
    return res


def readings(res):
    """The reading rules fixed in prereg/premise.md, applied to each primary critic."""
    out = []
    for name in PRIMARY:
        t = {r["test"]: r for r in res if r["critic"] == name}
        if not t:
            continue
        got = lambda *ids: [i for i in ids if t.get(i, {}).get("held")]
        out.append(f"- **{name}**")
        out.append(f"  - Holds across wordings (T1–T4): {len(got('T1', 'T2', 'T3', 'T4'))} of 4.")
        scrutiny = got("T5", "T6")
        out.append("  - About the claim, not scrutiny (T5, T6): " + ("yes." if len(scrutiny) == 2 else f"not shown ({len(scrutiny)} of 2)."))
        if "T7" in t:
            r = t["T7"]
            lo, hi = r["ci"]
            if r["held"] and r["est"] < 0:
                word = "**still moves verdicts** when the critic is told the claim carries no information"
            elif r["held"]:
                word = "moves verdicts the other way when the critic is told the claim carries no information"
            elif -NO_EFFECT <= lo and hi <= NO_EFFECT:
                word = f"no shift (the whole interval is within ±{NO_EFFECT})"
            else:
                word = "inconclusive (no clear shift, but the interval reaches past the no-shift range)"
            out.append(f"  - Worthless claim (T7): {word}. Saying so weakens the claim (T8): {'yes' if t.get('T8', {}).get('held') else 'not shown'}.")
        if "T9" in t:
            out.append(f"  - Opposite claim moves the threshold the other way (T9): {'yes' if t['T9']['held'] else 'not shown'}.")
    return out


def retest(cr, claim="presuppose"):
    """Correct solutions. Verdicts can change between two samples of one prompt, and some 'flips' under a claim are only that.
    Compares passing in sample 0 and flagging in sample 1, within neutral and from neutral to the claim."""
    v = cr.verdicts()
    ids = [cr.md.ids[i] for i in cr.md.co_idx]
    both = [i for i in ids if ("neutral", i, 0) in v and ("neutral", i, 1) in v and (claim, i, 1) in v]
    if len(both) < 10:
        return None
    a = np.array([v["neutral", i, 0] == "error" for i in both])
    b = np.array([v["neutral", i, 1] == "error" for i in both])
    c = np.array([v[claim, i, 1] == "error" for i in both])
    noise, flips = ~a & b, ~a & c
    rng = np.random.default_rng(0)
    idx = rng.integers(len(both), size=(10000, len(both)))
    excess = flips.astype(float)[idx].mean(1) - noise.astype(float)[idx].mean(1)
    phi = float(np.corrcoef(a, b)[0, 1]) if a.std() > 0 and b.std() > 0 else float("nan")
    return dict(n=len(both), passed=int((~a).sum()), noise=int(noise.sum()), flips=int(flips.sum()), phi=phi,
                excess=100 * (flips.mean() - noise.mean()), excess_ci=tuple(100 * np.percentile(excess, [2.5, 97.5])))


def retest_section(critics):
    rows = [(n, retest(cr)) for n, cr in critics.items() if cr.has("neutral", "presuppose")]
    rows = [(n, r) for n, r in rows if r]
    if not rows:
        return []
    out = ["## Are the flips more than sampling noise? (correct solutions)", "",
           'Passed in sample 0 of neutral, then flagged in sample 1 of neutral (noise), or in sample 1 of "contains an error" (flips).', "",
           "| critic | passed in sample 0 | flagged again at neutral | flagged under the claim | excess, per 100 correct [95% CI] | phi, neutral sample 0 vs 1 |",
           "|---|---|---|---|---|---|"]
    for n, r in rows:
        out.append(f"| {n} | {r['passed']} of {r['n']} | {r['noise']} | {r['flips']} | {fci(r['excess'], r['excess_ci'], 0)} | {fmt(r['phi'])} |")
    return out + [""]


def flag_counts_section(critics, claim="presuppose"):
    out = ['## How consistent is the effect on an item? Correct solutions flagged in 0, 1, 2 or 3 of 3 samples', "",
           '| critic | neutral: 0 / 1 / 2 / 3 | "contains an error": 0 / 1 / 2 / 3 |', "|---|---|---|"]
    n = 0
    for name, cr in critics.items():
        if not cr.has("neutral", claim) or cr.md.T[:, cr.col[claim]].max() != 3 or cr.md.T[:, cr.col["neutral"]].max() != 3:
            continue
        hist = lambda c: " / ".join(str(int((cr.md.E[cr.md.co_idx, cr.col[c]] == j).sum())) for j in range(4))
        out.append(f"| {name} | {hist('neutral')} | {hist(claim)} |")
        n += 1
    return out + [""] if n else []


def shared_items_section(critics):
    """Do two critics move on the same correct solutions? Correlation of the per-item change in flag rate."""
    pairs = [("qwen3.5:27b-think-bf16-t1", "opus-5.5-think", "pre-registered"),
             ("qwen3.5:4b-think-bf16-t1", "qwen3.5:27b-think-bf16-t1", "descriptive"),
             ("sonnet-5.5-think", "opus-5.5-think", "descriptive")]
    rng = np.random.default_rng(0)
    lines = []
    for a, b, kind in pairs:
        if a not in critics or b not in critics:
            continue
        da = critics[a].correct_flags("presuppose") - critics[a].correct_flags("neutral")
        db = critics[b].correct_flags("presuppose") - critics[b].correct_flags("neutral")
        r = float(np.corrcoef(da, db)[0, 1])
        sims = np.array([np.corrcoef(rng.permutation(da), db)[0, 1] for _ in range(10000)])
        lines.append(f"| {a} & {b} | {kind} | {r:+.2f} | {((sims >= r).sum() + 1) / 10001:.4f} |")
    if not lines:
        return []
    return ['## Do critics move on the same correct solutions?', "",
            'Correlation over correct solutions of the change in flag rate under "contains an error"; one-sided p from 10,000 permutations.', "",
            "| critics | status | r | p |", "|---|---|---|---|", *lines, ""]


def rate_arm_section(critics):
    """Is a stated chance for this solution used more than a base rate for the batch? rho with d'(neutral) as the benchmark."""
    need = ("neutral", "item_p10", "item_p90", "br10", "br90")
    lines = []
    for name, cr in critics.items():
        if not cr.has(*need):
            continue
        k = cr.col
        d, bd = cr.d[k["neutral"]], cr.bd[:, k["neutral"]]
        rho = lambda lo, hi: (cr.c[k[lo]] - cr.c[k[hi]]) * d / LN81
        brho = lambda lo, hi: np.where(bd > 0, (cr.bc[:, k[lo]] - cr.bc[:, k[hi]]) * bd / LN81, np.nan)
        ri, rb = rho("item_p10", "item_p90"), rho("br10", "br90")
        bi, bb = brho("item_p10", "item_p90"), brho("br10", "br90")
        lines.append(f"| {name} | {fci(ri, ci(bi))} | {fci(rb, ci(bb))} | {fci(ri - rb, ci(bi - bb))} |")
    if not lines:
        return []
    return ["## A chance for this solution, against a rate for the batch", "",
            "ρ from told 10% to told 90%, with d′ at neutral as the benchmark (1 = ideal). Paired.", "",
            "| critic | ρ, this solution | ρ, this batch | difference |", "|---|---|---|---|", *lines, ""]


def contrasts_section(critics):
    """Paired differences between critics, and thinking on vs off, in the shift under 'contains an error'."""
    lines = []
    def add(a, b):
        if a in critics and b in critics and critics[a].has("neutral", "presuppose") and critics[b].has("neutral", "presuppose"):
            ea, ba = critics[a].shift("presuppose", "neutral")
            eb, bb = critics[b].shift("presuppose", "neutral")
            lines.append(f"| {a} − {b} | {fci(ea - eb, ci(ba - bb))} |")
    add("qwen3.5:27b-think-bf16-t1", "opus-5.5-think")
    for m in ("qwen3.5:4b", "qwen3.5:9b", "gemma4:12b", "qwen3.5:27b"):
        add(f"{m}-think-bf16-t1", f"{m}-nothink-bf16-t1")
    if not lines:
        return []
    return ['## Paired differences in the "contains an error" shift', "", "| critics | difference [95% CI] |", "|---|---|", *lines, ""]


def rules_section(critics):
    """The health rules from prereg/premise.md: unparsed replies per condition, and the ceiling."""
    out, flagged = ["## Rules", ""], False
    for name, cr in critics.items():
        md = cr.md
        k0 = cr.col["neutral"]
        passes = md.T[:, k0].max()
        errs = ((md.V[md.fl_idx, k0] - md.E[md.fl_idx, k0]).sum() + md.E[md.co_idx, k0].sum()) / passes
        if errs <= 4:
            out.append(f"- **Ceiling:** {name} makes {errs:.1f} errors per 200 at neutral, so its shifts are reported but not interpreted.")
            flagged = True
        for c in cr.conds:
            k = cr.col[c]
            total, parsed = md.T[:, k].sum(), md.V[:, k].sum()
            share = 1 - parsed / total
            if share > 0.02:
                flagged = True
                # Every unparsed trial counted as "error", then as "correct".
                sens = []
                for counted in ("error", "correct"):
                    E2, V2 = md.E.copy(), md.V.copy()
                    V2[:, k] = md.T[:, k]
                    if counted == "error":
                        E2[:, k] += md.T[:, k] - md.V[:, k]
                    alt = ModelData.__new__(ModelData)
                    alt.E, alt.V, alt._k, alt.fl_idx, alt.co_idx = E2, V2, md._k, md.fl_idx, md.co_idx
                    c_alt = alt.rates(md.fl_idx[None], md.co_idx[None])[3][0]
                    # Neutral is the baseline of every shift, so report c itself there.
                    sens.append(f"{counted}: {c_alt[k]:+.2f}" if k == k0 else f"{counted}: {c_alt[k] - c_alt[k0]:+.2f}")
                what = "c" if k == k0 else "Shift from neutral"
                out.append(f"- **Unparsed:** {name}, {c}: {100 * share:.1f}% ({'over 5%, flagged' if share > 0.05 else 'over 2%'}). "
                           f"{what} with those trials counted as {'; '.join(sens)}.")
    if not flagged:
        out.append("- No trigger: every condition is at or under 2% unparsed, and no critic is at the ceiling.")
    return out + [""]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=str(ROOT / "results" / "premise"))
    ap.add_argument("--items", default=str(ROOT / "data" / "items_premise.jsonl"))
    ap.add_argument("--out-dir", default=None, help="default: <dir>/analysis")
    ap.add_argument("--bootstrap", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    paths = sorted(Path(args.dir).glob("*.jsonl"))
    if not paths:
        raise SystemExit(f"no results in {args.dir}")
    rows = load_rows(paths)
    has_error = {it["id"]: it["has_error"] for it in map(json.loads, open(args.items))}
    item_ids = sorted(has_error)
    names = sorted({r["model"] for r in rows}, key=model_sort_key)
    # Indexes follow the sorted item ids, which every critic kept below shares (ModelData sorts them the same way).
    fl = np.array([k for k, i in enumerate(item_ids) if has_error[i]])
    co = np.array([k for k, i in enumerate(item_ids) if not has_error[i]])
    rng = np.random.default_rng(args.seed)
    fl_boot = rng.choice(fl, size=(args.bootstrap, len(fl)))
    co_boot = rng.choice(co, size=(args.bootstrap, len(co)))

    critics, problems = {}, []
    for n in names:
        r = [x for x in rows if x["model"] == n]
        got = sorted({x["item_id"] for x in r})
        if got != item_ids:
            problems.append(f"- {n}: rows cover {len(got)} of {len(item_ids)} items, so it is left out.")
            continue
        critics[n] = Critic(n, r, fl_boot, co_boot)

    res = primary_tests(critics)
    out = ["# Premise test: results", "",
           "Generated by `scripts/premise_analysis.py` from the saved replies. Plan and reading rules: `prereg/premise.md`. "
           "c − c(neutral) < 0 means flagging more than with no added line.", ""]
    if problems:
        out += ["## Problems", "", *problems, ""]
    out += rules_section(critics)
    out += ["## Primary tests", "",
            f"Critics: {', '.join(n for n in PRIMARY if n in critics)}. {args.bootstrap:,} paired item-bootstrap resamples; two-sided p; "
            f"Holm across the {len(res)} tests below. Held: Holm p < {ALPHA} in the predicted direction.", "",
            "| critic | test | contrast | asks | predicted | difference in c [95% CI] | p | Holm p | outcome |",
            "|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        pred = {-1: "negative", 1: "positive", 0: "no direction"}[r["sign"]]
        verdict = "held" if r["held"] and r["sign"] else ("moved" if r["held"] else ("**against**" if r["against"] else "not shown"))
        out.append(f"| {r['critic']} | {r['test']} | {r['a']} − {r['b']} | {r['what']} | {pred} | {fci(r['est'], r['ci'])} "
                   f"| {r['p']:.4f} | {r['p_holm']:.4f} | {verdict} |")
    out += ["", "## Reading rules, applied", "", *readings(res), ""]
    out += retest_section(critics)
    out += flag_counts_section(critics)
    out += shared_items_section(critics)
    out += rate_arm_section(critics)
    out += contrasts_section(critics)
    out += ["## Per critic", "", "Intervals here are uncorrected. Δ is the change from neutral.", ""]
    for cr in critics.values():
        out += per_critic_table(cr) + [""]

    dest = Path(args.out_dir or Path(args.dir) / "analysis")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "premise.md").write_text("\n".join(out) + "\n")
    (dest / "premise.json").write_text(json.dumps({"primary_tests": res}, indent=1, default=float))
    print("\n".join(out))
    print(f"\nwrote {dest / 'premise.md'} and {dest / 'premise.json'}")


if __name__ == "__main__":
    main()
