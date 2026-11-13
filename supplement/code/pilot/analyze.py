"""Signal-detection analysis of critic verdicts.

Conventions (Macmillan & Creelman): the "signal" is a flawed solution and a "yes" is
the verdict "error".
    hit rate H         = P(says error | flawed)
    false-alarm rate F = P(says error | correct)
    d' = z(H) - z(F)              how well the critic separates flawed from correct
    c  = -(z(H) + z(F)) / 2       where it puts its threshold:
                                  c > 0 lenient (misses errors), c < 0 flag-happy
Rates use the log-linear correction (Hautus, 1995) so 0% and 100% stay finite.

An ideal observer told that a fraction p of solutions are flawed sets
c* = ln((1 - p) / p) / d'. Moving the stated rate from 10% to 90% should therefore
move c by ln(81) / d'. The prior-use ratio rho = observed shift / ideal shift
(0 = ignores the stated rate, 1 = ideal, > 1 overshoots) is the pilot's headline number.

All confidence intervals come from a bootstrap over items (flawed and correct items
resampled separately; the same resample is used for every condition, so differences
between conditions are paired). Every model gets the same resamples too, so differences
in rho between models run on the same items are paired as well.

Usage:
    uv run python -m pilot.analyze results/*.jsonl
"""
import argparse
import json
import math
import re
from pathlib import Path

import numpy as np
from scipy.stats import norm, rankdata

from .prompts import ARM_LABELS, CONDITIONS, FRAMING_LABELS

ROOT = Path(__file__).resolve().parent.parent
LN81 = math.log(81)


def load_rows(paths):
    rows = []
    for p in paths:
        for line in Path(p).open():
            r = json.loads(line)
            if not r.get("retryable"):  # drop network failures; parse failures stay (as unparsed)
                rows.append(r)
    return rows


class ModelData:
    """Per-model arrays: items x conditions (x samples)."""

    def __init__(self, rows, conditions, score_key="p_error", score_scale=1.0):
        self.conditions = conditions
        ids = sorted({r["item_id"] for r in rows})
        self.ids = ids
        row_of = {i: k for k, i in enumerate(ids)}
        col_of = {c: k for k, c in enumerate(conditions)}
        n_samples = max(r["sample"] for r in rows) + 1
        shape = (len(ids), len(conditions))
        self.E = np.zeros(shape)            # "error" verdicts
        self.V = np.zeros(shape)            # parsed verdicts
        self.T = np.zeros(shape)            # all trials
        self.P = np.full(shape + (n_samples,), np.nan)  # graded P(error) score used for ROC / AUC
        self.flawed = np.zeros(len(ids), bool)
        for r in rows:
            i, c = row_of[r["item_id"]], col_of[r["condition"]]
            self.flawed[i] = r["has_error"]
            self.T[i, c] += 1
            if r["verdict"] is not None:
                self.V[i, c] += 1
                self.E[i, c] += r["verdict"] == "error"
                if r.get(score_key) is not None:
                    self.P[i, c, r["sample"]] = r[score_key] * score_scale
        self.fl_idx = np.flatnonzero(self.flawed)
        self.co_idx = np.flatnonzero(~self.flawed)
        self._k = np.maximum(self.T.max(0), 1)   # samples per item in each condition

    def rates(self, fl, co):
        """fl, co: index arrays of shape (B, n). Returns H, F, d', c with shape (B, n_conditions)."""
        # Counts are per pass over the items, so the correction, and with it c near ceiling, does not depend on the
        # number of samples. Repeat samples of one item are not independent trials. With one sample this is the usual rule.
        h, ns = self.E[fl].sum(1) / self._k, self.V[fl].sum(1) / self._k
        f, nn = self.E[co].sum(1) / self._k, self.V[co].sum(1) / self._k
        H, F = (h + 0.5) / (ns + 1), (f + 0.5) / (nn + 1)
        zH, zF = norm.ppf(H), norm.ppf(F)
        return H, F, zH - zF, -(zH + zF) / 2

    def auc(self, fl, co, c):
        s = self.P[fl, c].ravel()
        n = self.P[co, c].ravel()
        s, n = s[~np.isnan(s)], n[~np.isnan(n)]
        if len(s) == 0 or len(n) == 0:
            return np.nan
        r = rankdata(np.concatenate([s, n]))
        return (r[: len(s)].sum() - len(s) * (len(s) + 1) / 2) / (len(s) * len(n))


def ci(x):
    x = x[np.isfinite(x)]
    return (np.nan, np.nan) if len(x) == 0 else tuple(np.percentile(x, [2.5, 97.5]))


def zroc_slope(md, c):
    """Slope of the z-transformed ROC from p_error ratings; 1.0 means the equal-variance model fits."""
    s = md.P[md.fl_idx, c].ravel(); s = s[~np.isnan(s)]
    n = md.P[md.co_idx, c].ravel(); n = n[~np.isnan(n)]
    pts = []
    for t in np.unique(np.concatenate([s, n]))[1:]:
        H, F = (s >= t).mean(), (n >= t).mean()
        if 0 < H < 1 and 0 < F < 1:
            pts.append((norm.ppf(F), norm.ppf(H)))
    if len(pts) < 3:
        return np.nan
    x, y = np.array(pts).T
    return np.polyfit(x, y, 1)[0]


def sdt_c(E, V, fl, co):
    """Criterion c per column of E (error verdicts) / V (parsed verdicts), items x columns, log-linear corrected."""
    h, ns = E[fl].sum(1), V[fl].sum(1)
    f, nn = E[co].sum(1), V[co].sum(1)
    return -(norm.ppf((h + 0.5) / (ns + 1)) + norm.ppf((f + 0.5) / (nn + 1))) / 2


def bayes_check(rows, md, boot_fl, boot_co):
    """Is the critic's response to the stated rate what its own stated confidence implies?

    The stated P(error) at the 50% rate, p, is read as a posterior under a 50% prior, so its
    likelihood ratio is p / (1 - p). Told a rate pi, a Bayesian says "error" iff
    p / (1 - p) * pi / (1 - pi) > 1: told 10%, iff p > 90; told 90%, iff p > 10 (a posterior of
    exactly one half counts as "correct"). The equal-variance ideal (ln 81 / d') asks every critic
    to move the same amount whatever its confidence; this benchmark asks only for the moves its
    own confidence implies. Uses sample 0 and the items whose br50 verdict and p_error and br10 and
    br90 verdicts all parsed. Pre-registered in prereg/stage_c.md (exploratory in Stage B).
    """
    need = ("br10", "br50", "br90")
    by = {(r["condition"], r["item_id"]): r for r in rows if r["condition"] in need and r["sample"] == 0}
    n = len(md.ids)
    ok, p50 = np.zeros(n, bool), np.full(n, np.nan)
    v = {c: np.zeros(n, bool) for c in need}
    for k, iid in enumerate(md.ids):
        rs = [by.get((c, iid)) for c in need]
        if any(r is None or r["verdict"] is None for r in rs) or rs[1].get("p_error") is None:
            continue
        ok[k], p50[k] = True, rs[1]["p_error"]
        for c, r in zip(need, rs):
            v[c][k] = r["verdict"] == "error"
    if ok.sum() < 10:
        return None, None
    b10, b90 = ok & (p50 > 90), ok & (p50 > 10)   # a Bayesian's "error" verdicts told 10% / 90%
    flagged, passed = ok & v["br50"], ok & ~v["br50"]
    E = np.stack([v["br10"], v["br90"], b10, b90], 1).astype(float)
    V = np.repeat(ok[:, None], 4, 1).astype(float)
    c_pt = sdt_c(E, V, md.fl_idx[None], md.co_idx[None])[0]
    c_bt = sdt_c(E, V, boot_fl, boot_co)
    dc_obs, dc_bay = c_pt[0] - c_pt[1], c_pt[2] - c_pt[3]
    b_obs, b_bay = c_bt[:, 0] - c_bt[:, 1], c_bt[:, 2] - c_bt[:, 3]
    b_ratio = np.where(b_bay > 0, b_obs / np.where(b_bay > 0, b_bay, 1.0), np.nan)
    res = {
        "n_items": int(ok.sum()),
        # Share of items whose stated confidence is in the range where a stated rate can flip a Bayesian.
        "share_flippable": float((ok & (p50 > 10) & (p50 <= 90)).sum() / ok.sum()),
        # Told 10%: flags at 50% that a Bayesian would drop (p <= 90), and how many the critic dropped.
        "flagged_at_50": int(flagged.sum()),
        "clear_predicted": int((flagged & ~b10).sum()),
        "clear_predicted_done": int((flagged & ~b10 & ~v["br10"]).sum()),
        "clear_unpredicted": int((flagged & b10 & ~v["br10"]).sum()),
        # Told 90%: passes at 50% that a Bayesian would flag (p > 10), and how many the critic flagged.
        "passed_at_50": int(passed.sum()),
        "flag_predicted": int((passed & b90).sum()),
        "flag_predicted_done": int((passed & b90 & v["br90"]).sum()),
        "flag_unpredicted": int((passed & ~b90 & v["br90"]).sum()),
        # Changes against the stated rate (flagging more when told errors are rare, or fewer when told common).
        "wrong_way": int((passed & v["br10"]).sum() + (flagged & ~v["br90"]).sum()),
        "delta_c_obs": dc_obs, "delta_c_obs_ci": ci(b_obs),
        "delta_c_bayes": dc_bay, "delta_c_bayes_ci": ci(b_bay),
        "rho_bayes": dc_obs / dc_bay if dc_bay > 0 else float("nan"), "rho_bayes_ci": ci(b_ratio),
        "rho_bayes_resamples_dropped": int(np.isnan(b_ratio).sum()),
    }
    return res, b_ratio


def analyze_model(model, rows, items_by_id, n_boot, ref, rng, boot_indices=None, auc_bootstrap_limit=1000):
    conditions = [c for c in CONDITIONS if any(r["condition"] == c for r in rows)]
    # Prefer token-logprob scores for the ROC when they were recorded; verbalized p_error is often 0/100 only.
    parsed = [r for r in rows if r["verdict"] is not None]
    use_lp = parsed and sum(r.get("p_error_lp") is not None for r in parsed) >= 0.9 * len(parsed)
    score = "p_error_lp" if use_lp else "p_error"
    md = ModelData(rows, conditions, score, 100.0 if use_lp else 1.0)
    rating_levels = len({r["p_error"] for r in parsed if r.get("p_error") is not None})
    col = {c: k for k, c in enumerate(conditions)}
    ref = ref if ref in col else ("br50" if "br50" in col else conditions[0])

    point = md.rates(md.fl_idx[None], md.co_idx[None])
    point = [a[0] for a in point]
    if boot_indices is None:
        boot_fl = rng.choice(md.fl_idx, size=(n_boot, len(md.fl_idx)))
        boot_co = rng.choice(md.co_idx, size=(n_boot, len(md.co_idx)))
    else:
        # The results-freeze path supplies common whole-problem resamples.
        # Historical commands retain their original sampling when omitted.
        boot_fl, boot_co = boot_indices
        if boot_fl.shape != (n_boot, len(md.fl_idx)) or boot_co.shape != (n_boot, len(md.co_idx)):
            raise ValueError('Bootstrap indices must preserve class sample counts')
    bH, bF, bd, bc = md.rates(boot_fl, boot_co)

    out = {"model": model, "ref": ref, "score": score, "rating_levels": rating_levels, "conditions": []}
    d_ref, bd_ref = point[2][col[ref]], bd[:, col[ref]]
    k_neu = col.get("neutral")
    for c in conditions:
        k = col[c]
        p = CONDITIONS[c]["stated_p_error"]
        auc_boot = np.array([md.auc(boot_fl[b], boot_co[b], k) for b in range(min(n_boot, auc_bootstrap_limit))])
        out["conditions"].append({
            "condition": c,
            "arm": CONDITIONS[c]["arm"],
            "stated_p_error": p,
            "n_flawed": int(md.V[md.fl_idx, k].sum()),
            "n_correct": int(md.V[md.co_idx, k].sum()),
            "unparsed": int(md.T[:, k].sum() - md.V[:, k].sum()),
            "hit_rate": point[0][k], "fa_rate": point[1][k],
            "d_prime": point[2][k], "d_prime_ci": ci(bd[:, k]),
            "c": point[3][k], "c_ci": ci(bc[:, k]),
            # Paired shift from the no-instruction baseline; negative = more flag-happy than neutral.
            "c_minus_neutral": None if k_neu is None else point[3][k] - point[3][k_neu],
            "c_minus_neutral_ci": (None, None) if k_neu is None else ci(bc[:, k] - bc[:, k_neu]),
            "ideal_c": None if p is None else math.log((1 - p) / p) / d_ref,
            "auc": md.auc(md.fl_idx, md.co_idx, k), "auc_ci": ci(auc_boot),
        })

    # One prior-use ratio per arm that has a 10% and a 90% condition (base rate, base rate + instruction, payoff).
    # Every arm is scaled by the same ideal shift, ln 81 / d'(ref), so ratios are comparable across arms.
    out["arms"], out["_b_rho_arm"] = {}, {}
    for arm in dict.fromkeys(CONDITIONS[c]["arm"] for c in conditions):
        lo = next((c for c in conditions if CONDITIONS[c]["arm"] == arm and CONDITIONS[c]["stated_p_error"] == 0.1), None)
        hi = next((c for c in conditions if CONDITIONS[c]["arm"] == arm and CONDITIONS[c]["stated_p_error"] == 0.9), None)
        if lo is None or hi is None:
            continue
        dc = point[3][col[lo]] - point[3][col[hi]]
        bdc = bc[:, col[lo]] - bc[:, col[hi]]
        # Resamples with d' <= 0 have no meaningful ideal shift; drop them from the ratio's interval.
        b_rho = np.where(bd_ref > 0, bdc * np.where(bd_ref > 0, bd_ref, 1.0) / LN81, np.nan)
        out["arms"][arm] = {"low": lo, "high": hi, "delta_c": dc, "delta_c_ci": ci(bdc),
                            "rho": dc / (LN81 / d_ref), "rho_ci": ci(b_rho)}
        out["_b_rho_arm"][arm] = b_rho
    out["ideal_delta_c"] = LN81 / d_ref
    if "base_rate" in out["arms"]:
        a = out["arms"]["base_rate"]
        out["delta_c"], out["delta_c_ci"], out["rho"], out["rho_ci"] = a["delta_c"], a["delta_c_ci"], a["rho"], a["rho_ci"]
        out["_b_rho"] = out["_b_rho_arm"]["base_rate"]
    # Within-model contrasts: does each follow-up arm move the threshold more than the plain base rate?
    out["arm_contrasts"] = {
        arm: {"diff": out["arms"][arm]["rho"] - out["rho"], "ci": ci(out["_b_rho_arm"][arm] - out["_b_rho"])}
        for arm in out["arms"] if arm != "base_rate" and "rho" in out
    }
    if "neutral" in col and "br50" in col:
        out["c_br50_minus_neutral"] = point[3][col["br50"]] - point[3][col["neutral"]]
        out["c_br50_minus_neutral_ci"] = ci(bc[:, col["br50"]] - bc[:, col["neutral"]])
    out["zroc_slope_ref"] = zroc_slope(md, col[ref])
    if all(c in col for c in ("br10", "br50", "br90")):
        out["bayes"], out["_b_rho_bayes"] = bayes_check(rows, md, boot_fl, boot_co)

    # Hits split by whether the flawed solution still reached the right final answer.
    k0 = col["neutral"] if "neutral" in col else col[ref]
    split = {}
    for name, want in (("right_answer", True), ("wrong_answer", False)):
        idx = [i for i in md.fl_idx if items_by_id.get(md.ids[i], {}).get("final_answer_correct") == want]
        if idx:
            split[name] = (int(md.E[idx, k0].sum()), int(md.V[idx, k0].sum()))
    out["hits_by_final_answer"] = {"condition": conditions[k0], **split}
    out["_md"], out["_col"] = md, col
    return out


def fmt(x, nd=2):
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{nd}f}"


def fmt_ci(x, lo_hi, nd=2):
    return f"{fmt(x, nd)} [{fmt(lo_hi[0], nd)}, {fmt(lo_hi[1], nd)}]"


def to_markdown(res):
    lines = [f"### {res['model']}", "",
             "| condition | stated p(error) | n flawed / correct | unparsed | hit rate | false-alarm rate | d′ [95% CI] | c [95% CI] | c − c(neutral) [95% CI] | ideal c* | AUC [95% CI] |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res["conditions"]:
        lines.append(f"| {r['condition']} | {fmt(r['stated_p_error'])} | {r['n_flawed']} / {r['n_correct']} | {r['unparsed']} | "
                     f"{fmt(r['hit_rate'])} | {fmt(r['fa_rate'])} | {fmt_ci(r['d_prime'], r['d_prime_ci'])} | "
                     f"{fmt_ci(r['c'], r['c_ci'])} | {fmt_ci(r['c_minus_neutral'], r['c_minus_neutral_ci'])} | "
                     f"{fmt(r['ideal_c'])} | {fmt_ci(r['auc'], r['auc_ci'])} |")
    lines.append("")
    if "rho" in res:
        lines.append(f"- **Prior-use ratio ρ = {fmt_ci(res['rho'], res['rho_ci'])}** (0 = ignores the stated base rate, "
                     f"1 = ideal observer, >1 overshoots). Observed c(10%) − c(90%) = {fmt_ci(res['delta_c'], res['delta_c_ci'])}; "
                     f"ideal = ln 81 / d′({res['ref']}) = {fmt(res['ideal_delta_c'])}.")
    for arm, a in res["arms"].items():
        if arm == "base_rate":
            continue
        con = res["arm_contrasts"].get(arm)
        lines.append(f"- ρ for {ARM_LABELS.get(arm, arm)} ({a['low']} vs {a['high']}) = **{fmt_ci(a['rho'], a['rho_ci'])}**"
                     + (f"; minus base-rate ρ = {fmt_ci(con['diff'], con['ci'])} (paired)." if con else "."))
    if "c_br50_minus_neutral" in res:
        lines.append(f"- Saying \"50%\" vs saying nothing: c(br50) − c(neutral) = "
                     f"{fmt_ci(res['c_br50_minus_neutral'], res['c_br50_minus_neutral_ci'])}.")
    if bc := res.get("bayes"):
        lines.append(f"- **Bayes check** (own stated confidence at 50% as the posterior; {bc['n_items']} items, "
                     f"{100 * bc['share_flippable']:.0f}% with 10 < p_error ≤ 90): "
                     f"told 10%, a Bayesian drops {bc['clear_predicted']} of {bc['flagged_at_50']} flags, the critic dropped "
                     f"{bc['clear_predicted_done']} of those (+{bc['clear_unpredicted']} others); told 90%, a Bayesian adds "
                     f"{bc['flag_predicted']} of {bc['passed_at_50']} passes as flags, the critic added {bc['flag_predicted_done']} "
                     f"(+{bc['flag_unpredicted']} others); {bc['wrong_way']} changes against the stated rate. "
                     f"c(10%) − c(90%): observed {fmt_ci(bc['delta_c_obs'], bc['delta_c_obs_ci'])}, Bayesian "
                     f"{fmt_ci(bc['delta_c_bayes'], bc['delta_c_bayes_ci'])}; **ρ_Bayes = "
                     f"{fmt_ci(bc['rho_bayes'], bc['rho_bayes_ci'])}** (1 = moves as far as its own confidence implies"
                     + (f"; {bc['rho_bayes_resamples_dropped']} resamples with no predicted shift dropped" if bc['rho_bayes_resamples_dropped'] else "")
                     + ").")
    src = "verdict-token logprobs" if res["score"] == "p_error_lp" else "verbalized p_error"
    lines.append(f"- ROC, AUC and z-ROC use {src}. Verbalized p_error took {res['rating_levels']} distinct values"
                 f"{' (too coarse for a useful ROC; rerun with --logprobs)' if res['rating_levels'] < 5 and res['score'] == 'p_error' else ''}.")
    lines.append(f"- z-ROC slope in {res['ref']}: {fmt(res['zroc_slope_ref'])} "
                 f"(≈1 supports the equal-variance model behind d′ and c*).")
    hb = res["hits_by_final_answer"]
    parts = [f"{k.replace('_', ' ')} {v[0]}/{v[1]}" for k, v in hb.items() if k != "condition"]
    if parts:
        lines.append(f"- Hits on flawed solutions in {hb['condition']}, by final answer: " + "; ".join(parts) + ".")
    return "\n".join(lines)


def compare_models(results):
    """Paired differences in rho between models run on the same items (they share bootstrap resamples)."""
    lines = []
    for i, a in enumerate(results):
        for b in results[i + 1:]:
            if a["_md"].ids != b["_md"].ids:
                continue
            for arm in a["arms"]:
                if arm in b["arms"] and len(a["_b_rho_arm"][arm]) == len(b["_b_rho_arm"][arm]):
                    diff = a["arms"][arm]["rho"] - b["arms"][arm]["rho"]
                    lines.append(f"- {ARM_LABELS.get(arm, arm)}: ρ({a['model']}) − ρ({b['model']}) = "
                                 f"{fmt_ci(diff, ci(a['_b_rho_arm'][arm] - b['_b_rho_arm'][arm]))}")
            if a.get("_b_rho_bayes") is not None and b.get("_b_rho_bayes") is not None:
                diff = a["bayes"]["rho_bayes"] - b["bayes"]["rho_bayes"]
                lines.append(f"- Bayes check: ρ_Bayes({a['model']}) − ρ_Bayes({b['model']}) = "
                             f"{fmt_ci(diff, ci(a['_b_rho_bayes'] - b['_b_rho_bayes']))}")
    return lines


def model_sort_key(name):
    """Natural sort, so qwen3.5:4b < qwen3.5:9b < qwen3.5:27b."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", name)]


def model_styles(models):
    """Color + marker per model. The first family with several sizes (e.g. qwen3.5 4b/9b/27b) gets
    light-to-dark steps of one hue, since size is ordered; every other model gets its own hue."""
    ramp, hues, markers = ["#8fbbea", "#2a78d6", "#0f4a8f", "#06284f"], ["#eb6834", "#1baf7a", "#6250d6", "#e34948"], "osD^vP"
    fams = {}
    for m in models:
        fams.setdefault(m.split(":")[0], []).append(m)
    sized = next((f for f in fams.values() if len(f) > 1), [])
    others = [m for m in models if m not in sized]
    return {m: {"color": ramp[min(sized.index(m), len(ramp) - 1)] if m in sized else hues[others.index(m) % len(hues)],
                "marker": markers[j % len(markers)]} for j, m in enumerate(models)}


def plot(results, path):
    """Base-rate arm only: one ROC-space panel per model, then criterion vs stated log-odds."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n = len(results)
    ncols = min(n + 1, 3)
    nrows = math.ceil((n + 1) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.6 * ncols, 4.4 * nrows), squeeze=False)
    axes = axes.ravel()
    for ax in axes[n + 1:]:
        ax.axis("off")
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    styles = model_styles([r["model"] for r in results])
    for ax, res in zip(axes[:n], results):
        md, col = res["_md"], res["_col"]
        conds = [r for r in res["conditions"] if r["arm"] == "base_rate"]
        k = col[res["ref"]]
        s = md.P[md.fl_idx, k].ravel(); s = s[~np.isnan(s)]
        nn = md.P[md.co_idx, k].ravel(); nn = nn[~np.isnan(nn)]
        d_ref = next(r["d_prime"] for r in res["conditions"] if r["condition"] == res["ref"])
        f = np.linspace(0.001, 0.999, 200)
        # When the operating points cluster, draw everything twice: full ROC space and a zoomed inset.
        fx = [r["fa_rate"] for r in conds]; hy = [r["hit_rate"] for r in conds]
        span = max(max(fx) - min(fx), max(hy) - min(hy))
        ins = ax.inset_axes([0.47, 0.08, 0.5, 0.45]) if span < 0.25 else None
        for a, main in ((ax, True), (ins, False))[: 2 if ins else 1]:
            if len(s) and len(nn):
                ts = np.unique(np.concatenate([s, nn, [101]]))[::-1]
                src = "logprobs" if res["score"] == "p_error_lp" else "p_error"
                a.plot([(nn >= t).mean() for t in ts], [(s >= t).mean() for t in ts], color="0.55", lw=1.2,
                       label=f"ROC from {src} ({res['ref']})" if main else None)
            a.plot(f, norm.cdf(d_ref + norm.ppf(f)), ls="--", color="0.75", lw=1,
                   label=f"iso-d′ = {d_ref:.2f}" if main else None)
            a.plot([0, 1], [0, 1], color="0.9", lw=1)
            for j, r in enumerate(conds):
                a.scatter(r["fa_rate"], r["hit_rate"], color=colors[j % len(colors)], zorder=3, s=30 if main else 36,
                          label=r["condition"] if main else None)
        if ins:
            half = span / 2 + 0.03
            cx, cy = (max(fx) + min(fx)) / 2, (max(hy) + min(hy)) / 2
            ins.set(xlim=(max(0, cx - half), min(1, cx + half)), ylim=(max(0, cy - half), min(1, cy + half)))
            ins.tick_params(labelsize=6)
            ax.indicate_inset_zoom(ins, edgecolor="0.6")
        ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="false-alarm rate (flags correct work)", ylabel="hit rate (catches real errors)",
               title=res["model"], aspect="equal")
        ax.legend(fontsize=7, loc="center right", bbox_to_anchor=(1, 0.72))

    ax = axes[n]
    for res in results:
        pts = [(r["stated_p_error"], r) for r in res["conditions"] if r["arm"] == "base_rate" and r["stated_p_error"] is not None]
        if len(pts) < 2:
            continue
        x = np.array([math.log(p / (1 - p)) for p, _ in pts])
        y = np.array([r["c"] for _, r in pts])
        lo = y - np.array([r["c_ci"][0] for _, r in pts]); hi = np.array([r["c_ci"][1] for _, r in pts]) - y
        st = styles[res["model"]]
        ax.errorbar(x, y, yerr=[lo, hi], fmt=st["marker"], color=st["color"], capsize=3,
                    label=f"{res['model']} (ρ={fmt(res.get('rho'))})")
        d_ref = next(r["d_prime"] for r in res["conditions"] if r["condition"] == res["ref"])
        anchor = next((r["c"] for p, r in pts if p == 0.5), y.mean())
        xs = np.linspace(x.min(), x.max(), 10)
        ax.plot(xs, anchor - xs / d_ref, ls="--", color=st["color"], lw=1, alpha=0.7)
    ax.axhline(0, color="0.9", lw=1)
    ax.set(xlabel="stated log-odds of an error, ln(p / (1 − p))", ylabel="criterion c  (+ lenient, − flag-happy)",
           title="Criterion vs stated base rate\n(dashed = ideal observer)")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_followups(results, path):
    """Left: rho per arm and model. Right: threshold shift from neutral per strictness framing and model.
    Returns False (and draws nothing) when there is nothing beyond the base-rate arm."""
    arms = list(dict.fromkeys(a for r in results for a in r["arms"]))
    framings = list(dict.fromkeys(c["condition"] for r in results for c in r["conditions"] if c["arm"] == "strictness"))
    if len(arms) < 2 and not framings:
        return False
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    styles = model_styles([r["model"] for r in results])
    n = len(results)
    off = lambda j: (j - (n - 1) / 2) * min(0.18, 0.7 / max(n, 1))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1, 1.25]})
    for j, res in enumerate(results):
        st = styles[res["model"]]
        xs = [i + off(j) for i, a in enumerate(arms) if a in res["arms"]]
        ys = [res["arms"][a]["rho"] for a in arms if a in res["arms"]]
        cis = [res["arms"][a]["rho_ci"] for a in arms if a in res["arms"]]
        if xs:
            a1.errorbar(xs, ys, yerr=[[y - c[0] for y, c in zip(ys, cis)], [c[1] - y for y, c in zip(ys, cis)]],
                        fmt=st["marker"], color=st["color"], capsize=3, ms=6, lw=1.2, label=res["model"])
        by = {c["condition"]: c for c in res["conditions"]}
        ys2 = [i + off(j) for i, f in enumerate(framings) if f in by]
        xs2 = [by[f]["c_minus_neutral"] for f in framings if f in by]
        cis2 = [by[f]["c_minus_neutral_ci"] for f in framings if f in by]
        if ys2:
            a2.errorbar(xs2, ys2, xerr=[[x - c[0] for x, c in zip(xs2, cis2)], [c[1] - x for x, c in zip(xs2, cis2)]],
                        fmt=st["marker"], color=st["color"], capsize=3, ms=6, lw=1.2, label=res["model"])
    a1.axhline(1, color="0.45", ls="--", lw=1); a1.text(len(arms) - 0.5, 1, "ideal", va="bottom", ha="right", fontsize=8, color="0.3")
    a1.axhline(0, color="0.85", lw=1)
    a1.set_xticks(range(len(arms)), [ARM_LABELS.get(a, a).replace(" + ", "\n+ ") for a in arms], fontsize=8)
    a1.set(xlim=(-0.6, len(arms) - 0.4), ylabel="prior-use ratio ρ (observed ÷ ideal shift)",
           title="How far each manipulation moves the threshold")
    a1.legend(fontsize=7, loc="upper left")
    if framings:
        a2.axvline(0, color="0.85", lw=1)
        a2.set_yticks(range(len(framings)), [FRAMING_LABELS.get(f, f) for f in framings], fontsize=8)
        a2.invert_yaxis()
        a2.set(xlabel="c − c(neutral)   (← more flag-happy · more lenient →)",
               title="Strictness framings vs no instruction")
        a2.legend(fontsize=7, loc="lower right")
    else:
        a2.axis("off")
    for a in (a1, a2):
        a.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results", nargs="+", help="results JSONL file(s); one model per file or mixed")
    ap.add_argument("--items", default=str(ROOT / "data" / "items.jsonl"))
    ap.add_argument("--ref", default="br50", help="condition whose d′ anchors the ideal-observer predictions")
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out-dir", default=str(ROOT / "results"))
    ap.add_argument("--subset", action="store_true",
                    help="analyze only the items listed in --items (e.g. the Stage C items Stage B never saw)")
    args = ap.parse_args()

    rows = load_rows(args.results)
    items_by_id = {}
    if Path(args.items).exists():
        items_by_id = {it["id"]: it for it in map(json.loads, Path(args.items).open())}
    if args.subset:
        rows = [r for r in rows if r["item_id"] in items_by_id]
        print(f"subset: {len({r['item_id'] for r in rows})} items listed in {args.items}")
    # A fresh generator per model gives every model the same item resamples (paired comparisons).
    results = [analyze_model(m, [r for r in rows if r["model"] == m], items_by_id, args.bootstrap, args.ref,
                             np.random.default_rng(args.seed))
               for m in sorted({r["model"] for r in rows}, key=model_sort_key)]

    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    md_text = "\n\n".join(to_markdown(r) for r in results)
    if cmp := compare_models(results):
        md_text += "\n\n### Model comparison (paired over the same items)\n\n" + "\n".join(cmp)
    (out / "summary.md").write_text(md_text + "\n")
    clean = [{k: v for k, v in r.items() if not k.startswith("_")} for r in results]
    (out / "summary.json").write_text(json.dumps(clean, indent=1, default=float))
    fig_path = out / "base_rate_pilot.png"
    plot(results, fig_path)
    written = [out / "summary.md", out / "summary.json", fig_path]
    if plot_followups(results, out / "followups.png"):
        written.append(out / "followups.png")
    print(md_text)
    print("\nwrote " + ", ".join(map(str, written)))


if __name__ == "__main__":
    main()
