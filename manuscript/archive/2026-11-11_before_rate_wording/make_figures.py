"""Figures and table numbers for the manuscript (rewrite of 2026-11-11).

Reads only finished analyses (hard set, claim test, label re-analysis) and the saved replies.
It does not read results/rate_wording/ (that run is analysed separately, once every job has finished),
and it never opens audit/.

    .venv/bin/python manuscript/figures/make_figures.py            # every figure, then the numbers
    .venv/bin/python manuscript/figures/make_figures.py --only 1   # one figure (1, 2, 3, 4, A1, A2)

Figures written to manuscript/figures/ (PDF for the paper, PNG for a quick look):
    fig1_ideal_observer        the model, the ideal-observer curve c*(p) with every critic, and ROC space
    fig2_prior_use             d', observed against ideal criterion shift, and the prior-use ratio, per critic
    fig3_numbers_vs_claims     effective probability of stated rates and of a claim; the preregistered claim test
    fig4_decision_vs_evidence  stated P(error) with and without the claim, two critics
    figA1_ideal_curves         appendix: each critic against its own ideal-observer curve
    figA2_claim_grid           appendix: false alarms for every critic and line on the held-out set

Colour is used for two things only, the same in every figure: a stated 10% rate (blue, left-pointing
triangle) and a stated 90% rate (orange, right-pointing triangle). Everything else is ink or grey, and
every colour is doubled by marker shape, so the figures survive greyscale printing. The pair was checked
with the dataviz validator (colour-vision-deficiency and normal-vision separation, contrast on white).
"""
import argparse
import json
import math
import sys
from pathlib import Path
from statistics import median

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from scipy.stats import norm, rankdata  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from pilot.analyze import ModelData, load_rows  # noqa: E402

LN81 = math.log(81)
INK, MUTED, FAINT, BAND = "#111111", "0.42", "0.80", "0.90"
BLUE, ORANGE = "#2a78d6", "#eb6834"     # told 10%, told 90%

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42,          # embedded TrueType, no Type 3 fonts
    "font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "font.size": 7.5, "axes.titlesize": 8, "axes.labelsize": 7.5,
    "xtick.labelsize": 6.8, "ytick.labelsize": 6.8, "legend.fontsize": 6.5,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5,
    "axes.edgecolor": "0.25", "xtick.color": "0.25", "ytick.color": "0.25",
    "axes.labelcolor": INK, "text.color": INK,
})

# The 14 critic runs on the hard set, grouped by model, reasoning off before on.
RUNS = [
    ("qwen3.5:4b-nothink-bf16-t1", "Qwen3.5-4B", "off"),
    ("qwen3.5:4b-think-bf16-t1", "Qwen3.5-4B", "on"),
    ("qwen3.5:9b-nothink-bf16-t1", "Qwen3.5-9B", "off"),
    ("qwen3.5:9b-think-bf16-t1", "Qwen3.5-9B", "on"),
    ("qwen3.5:27b-nothink-bf16-t1", "Qwen3.5-27B", "off"),
    ("qwen3.5:27b-think-bf16-t1", "Qwen3.5-27B", "on"),
    ("gemma4:12b-nothink-bf16-t1", "Gemma-4-12B", "off"),
    ("gemma4:12b-think-bf16-t1", "Gemma-4-12B", "on"),
    ("haiku-5.5-nothink", "Haiku 5.5", "off"),
    ("haiku-5.5-think", "Haiku 5.5", "high"),
    ("sonnet-5.5-nothink", "Sonnet 5.5", "off"),
    ("sonnet-5.5-think", "Sonnet 5.5", "high"),
    ("sonnet-5.5-think-max", "Sonnet 5.5", "max"),
    ("opus-5.5-think", "Opus 5.5", "high"),
]
REASONS = {k: t != "off" for k, _, t in RUNS}
OPEN = ("qwen", "gemma")
HARD_REPLIES = {k: ROOT / ("results/torch_hard" if k.startswith(OPEN) else "results/frontier/stage_c")
                / (k.replace(":", "_") + ".jsonl") for k, _, _ in RUNS}
# The ten critic runs of the held-out (claim-test) set.
PREMISE_RUNS = [(k, n, t) for k, n, t in RUNS if k.endswith("-t1")] + [
    ("haiku-5.5-think", "Haiku 5.5", "high"), ("opus-5.5-think", "Opus 5.5", "high")]
CLAIM_ROWS = [
    ("neutral", "no added line"),
    ("check_only", "“Check this solution carefully.”"),
    ("may_error", "“…may or may not contain an error…”"),
    ("presuppose", "“…contains an error. Check it…”"),
    ("claim_bare", "“This solution contains an error.”"),
    ("claim_mistake", "“There is a mistake somewhere…”"),
    ("claim_reviewer", "“A previous reviewer found an error…”"),
    ("claim_random", "the same note, “attached at random”"),
    ("claim_correct", "“This solution is correct. Check it…”"),
]


# ---------------------------------------------------------------- data helpers
def load_summaries(*paths):
    out = {}
    for p in paths:
        for m in json.load(open(ROOT / p)):
            out[m["model"]] = m
    return out


def cond(m, name):
    for c in m["conditions"]:
        if c["condition"] == name:
            return c
    return None


def d_ref(m):
    return cond(m, m["ref"])["d_prime"]


def p_eff(m, name):
    """Stated error rate at which an ideal observer with this critic's d' (reference condition) would move
    its threshold as far as the critic did under `name`: logit(p) = -(c(name) - c(neutral)) * d'."""
    c = cond(m, name)
    if c is None or c.get("c_minus_neutral") is None:
        return None
    return 1 / (1 + math.exp(c["c_minus_neutral"] * d_ref(m)))


def logit(p):
    return math.log(p / (1 - p))


def premise_path(key):
    return ROOT / "results/premise" / (key.replace(":", "_") + ".jsonl")


def raw_rates(path):
    """Uncorrected false-alarm and hit rates per condition over parsed replies, every sample pooled, as in the
    per-critic tables of scripts/premise_analysis.py (summary.json holds log-linear corrected rates)."""
    n = {}
    for line in open(path):
        r = json.loads(line)
        if r.get("verdict") is None:
            continue
        k = (r["condition"], r["has_error"])
        e, t = n.get(k, (0, 0))
        n[k] = (e + (r["verdict"] == "error"), t + 1)
    return {c: {"fa": n[(c, False)][0] / n[(c, False)][1], "hit": n[(c, True)][0] / n[(c, True)][1]}
            for c in {c for c, _ in n}}


def scores(path, condition):
    """Stated P(error) of parsed replies under one condition, every sample pooled: (correct, flawed)."""
    co, fl = [], []
    for line in open(path):
        r = json.loads(line)
        if r["condition"] == condition and r.get("verdict") is not None and r.get("p_error") is not None:
            (fl if r["has_error"] else co).append(r["p_error"])
    return np.array(co, float), np.array(fl, float)


def auc(co, fl):
    r = rankdata(np.concatenate([fl, co]))
    return (r[: len(fl)].sum() - len(fl) * (len(fl) + 1) / 2) / (len(fl) * len(co))


def shifts_from_50(key, summary, n_boot=2000, seed=20261111):
    """c(told 10%) - c(told 50%) and c(told 90%) - c(told 50%) on the hard set with paired item-bootstrap
    intervals, recomputed from the saved replies. Stops if the point estimates differ from the saved analysis."""
    rows = load_rows([HARD_REPLIES[key]])
    conds = ["br10", "br50", "br90"]
    md = ModelData([r for r in rows if r["condition"] in conds], conds)
    c = md.rates(md.fl_idx[None], md.co_idx[None])[3][0]
    for k, name in enumerate(conds):
        assert abs(c[k] - cond(summary, name)["c"]) < 1e-9, (key, name, c[k], cond(summary, name)["c"])
    rng = np.random.default_rng(seed)
    bc = md.rates(rng.choice(md.fl_idx, size=(n_boot, len(md.fl_idx))),
                  rng.choice(md.co_idx, size=(n_boot, len(md.co_idx))))[3]
    out = {}
    for k, name in ((0, "br10"), (2, "br90")):
        out[name] = (c[k] - c[1], *np.percentile(bc[:, k] - bc[:, 1], [2.5, 97.5]))
    return out


def median_tokens(key):
    """Median output tokens per reply on the hard set, reasoning included, over every condition run."""
    toks = [json.loads(line).get("completion_tokens") for line in open(HARD_REPLIES[key])]
    return median(t for t in toks if t is not None)


def clean(ax, keep=("left", "bottom")):
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(s in keep)


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", pad_inches=0.02, dpi=220)
    plt.close(fig)
    print(f"wrote {name}.pdf")


def row_label(name, think):
    return f"{name} ({think})"


# ---------------------------------------------------------------- Figure 1
def fig1(hard):
    fig = plt.figure(figsize=(7.0, 2.45))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.2, 0.86], wspace=0.34)

    # (a) the model: two evidence distributions and the ideal criteria
    ax = fig.add_subplot(gs[0])
    d = 2.0
    x = np.linspace(-4.3, 4.3, 600)
    top = norm.pdf(0)
    ax.fill_between(x, norm.pdf(x, -d / 2), color="0.88", lw=0)
    ax.plot(x, norm.pdf(x, -d / 2), color="0.5", lw=0.8)
    ax.plot(x, norm.pdf(x, d / 2), color=INK, lw=1.0)
    ax.text(-3.05, top * 0.92, "correct\nsolutions", ha="center", va="center", fontsize=6.6, color="0.3")
    ax.text(3.05, top * 0.92, "flawed\nsolutions", ha="center", va="center", fontsize=6.6)
    for p, col, lab, ha, dx in ((0.1, BLUE, "told 10%", "left", 0.12), (0.5, "0.3", "told 50%", "left", 0.12),
                                (0.9, ORANGE, "told 90%", "right", -0.12)):
        cs = math.log((1 - p) / p) / d
        ax.plot([cs, cs], [0, top * 1.52], color=col, lw=1.1, ls=(0, (4, 2)))
        ax.text(cs + dx, top * 1.50, lab, ha=ha, va="top", fontsize=6.2, color="0.2", rotation=90)
    lo, hi = -math.log(9) / d, math.log(9) / d
    ax.annotate("", xy=(lo, top * 1.63), xytext=(hi, top * 1.63),
                arrowprops=dict(arrowstyle="<->", lw=0.7, color=INK, shrinkA=0, shrinkB=0))
    ax.text(0, top * 1.68, r"ideal shift $=\ln 81\,/\,d'$", ha="center", va="bottom", fontsize=6.6)
    ax.annotate("", xy=(-d / 2, -top * 0.09), xytext=(d / 2, -top * 0.09), annotation_clip=False,
                arrowprops=dict(arrowstyle="<->", lw=0.6, color="0.35", shrinkA=0, shrinkB=0))
    ax.text(d / 2 + 0.2, -top * 0.09, r"$d'$", ha="left", va="center", fontsize=6.8, color="0.25")
    ax.set_xlim(-4.3, 4.3)
    ax.set_ylim(-top * 0.02, top * 1.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("evidence for an error  →", labelpad=13)
    ax.set_title("(a) The ideal observer's criterion", loc="left")
    clean(ax, keep=("bottom",))

    # (b) the ideal-observer curve c*(p), against every critic's observed criterion
    bx = fig.add_subplot(gs[1])
    ds = {k: d_ref(hard[k]) for k, _, _ in RUNS}
    dmin, dmax = min(ds.values()), max(ds.values())
    p = np.linspace(0.035, 0.965, 400)
    ideal = np.log((1 - p) / p)
    bx.fill_between(p, ideal / dmin, ideal / dmax, color=BAND, lw=0, zorder=0)
    for dd in (dmin, dmax):
        bx.plot(p, ideal / dd, color=INK, lw=0.9, ls=(0, (4, 2)), zorder=1)
        bx.text(0.978, ideal[-1] / dd, f"$d'={dd:.1f}$", fontsize=6.2, ha="left", va="center", color="0.2")
    bx.axhline(0, xmax=0.9, color=FAINT, lw=0.5, zorder=0)
    for key, _, _ in RUNS:
        m = hard[key]
        c10, c50, c90 = (cond(m, n)["c"] for n in ("br10", "br50", "br90"))
        on = REASONS[key]
        bx.plot([0.1, 0.5, 0.9], [c10 - c50, 0, c90 - c50], color="0.15" if on else "0.55", lw=0.75, zorder=2,
                solid_capstyle="round")
        for xx, yy, col, mk in ((0.1, c10 - c50, BLUE, "<"), (0.9, c90 - c50, ORANGE, ">")):
            bx.scatter(xx, yy, marker=mk, s=16, zorder=3, linewidths=0.7, edgecolors=col,
                       facecolors=col if on else "white")
    bx.set_xlim(0.02, 1.13)
    bx.set_ylim(-2.4, 2.4)
    bx.set_xticks([0.1, 0.3, 0.5, 0.7, 0.9], ["10%", "30%", "50%", "70%", "90%"])
    bx.set_yticks([-2, -1, 0, 1, 2])
    bx.spines["bottom"].set_bounds(0.02, 0.98)
    bx.set_xlabel("stated share of flawed solutions, $p$", x=0.43)
    bx.set_ylabel("criterion relative to “told 50%”\n(higher = more lenient)", fontsize=7, linespacing=1.1)
    bx.set_title(r"(b) The ideal-observer curve $c^*(p)$", loc="left")
    bx.legend(handles=[Line2D([], [], color=INK, lw=0.9, ls=(0, (4, 2)), label="ideal observer"),
                       Line2D([], [], color="0.15", lw=0.75, marker="o", ms=3.4, mfc="0.15", mec="0.15",
                              label="critic, reasoning on"),
                       Line2D([], [], color="0.55", lw=0.75, marker="o", ms=3.4, mfc="white", mec="0.45", mew=0.7,
                              label="critic, reasoning off")],
              loc="upper right", bbox_to_anchor=(0.93, 1.0), frameon=False, handlelength=1.9, borderaxespad=0.1,
              labelspacing=0.25)
    clean(bx)

    # (c) the same comparison in ROC space, for the least sensitive critic and a highly sensitive one
    cx = fig.add_subplot(gs[2])
    cx.plot([0, 1], [0, 1], color=FAINT, lw=0.5, zorder=0)
    cg = np.linspace(-5, 5, 500)
    picks = (("opus-5.5-think", "Opus 5.5", "-"), ("qwen3.5:4b-nothink-bf16-t1", "Qwen3.5-4B (off)", (0, (1.2, 1.2))))
    handles = []
    for key, name, ls in picks:
        m = hard[key]
        dd = d_ref(m)
        cx.plot(norm.cdf(-dd / 2 - cg), norm.cdf(dd / 2 - cg), color="0.5", lw=0.9, ls=ls, zorder=1)
        handles.append(Line2D([], [], color="0.5", lw=0.9, ls=ls, label=f"{name}, $d'={dd:.1f}$"))
        for pp, col, mk, cn in ((0.1, BLUE, "<", "br10"), (0.5, "0.3", "o", "br50"), (0.9, ORANGE, ">", "br90")):
            cs = math.log((1 - pp) / pp) / dd
            cx.scatter(norm.cdf(-dd / 2 - cs), norm.cdf(dd / 2 - cs), marker=mk, s=26, facecolors="white",
                       edgecolors=col, linewidths=0.9, zorder=3)
            o = cond(m, cn)
            cx.scatter(o["fa_rate"], o["hit_rate"], marker=mk, s=17, color=col, zorder=4, linewidths=0)
    key = cx.legend(handles=[Line2D([], [], ls="", marker="o", ms=4.4, mfc="white", mec="0.3", mew=0.9, label="ideal observer"),
                             Line2D([], [], ls="", marker="o", ms=3.6, mfc="0.3", mec="0.3", label="critic")],
                    loc="center right", bbox_to_anchor=(1.0, 0.36), frameon=False, handletextpad=0.2,
                    borderaxespad=0.1, labelspacing=0.28, fontsize=6.2)
    cx.add_artist(key)
    cx.set_xlim(-0.03, 1.0)
    cx.set_ylim(0.0, 1.03)
    cx.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    cx.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    cx.set_xlabel("false-alarm rate")
    cx.set_ylabel("hit rate", labelpad=1)
    cx.set_title("(c) Operating points", loc="left")
    cx.legend(handles=handles, loc="lower right", frameon=False, handletextpad=0.5, borderaxespad=0.1,
              labelspacing=0.2, handlelength=1.5, fontsize=6.2)
    clean(cx)
    save(fig, "fig1_ideal_observer")


# ---------------------------------------------------------------- Figure 2
def row_positions():
    """y position per run, with a gap between models. Returns positions and the spans of each model."""
    ys, y, spans, prev = [], 0.0, [], None
    for key, name, _ in RUNS:
        if prev is not None and name != prev:
            y -= 0.45
        if name != prev:
            spans.append([name, y, y])
        spans[-1][2] = y
        ys.append(y)
        y -= 1.0
        prev = name
    return ys, spans


def fig2(hard, ranges):
    ys, spans = row_positions()
    fig, (ax, bx, cx, dx) = plt.subplots(1, 4, figsize=(7.0, 2.8), sharey=True,
                                         gridspec_kw={"width_ratios": [0.58, 1.12, 1.12, 0.50], "wspace": 0.09})
    for a in (ax, bx, cx, dx):
        for i, (_, y0, y1) in enumerate(spans):
            if i % 2 == 0:
                a.axhspan(y1 - 0.5, y0 + 0.5, color="0.955", lw=0, zorder=0)
        a.tick_params(axis="y", length=0)
        clean(a, keep=("bottom",))

    def face(key):
        return INK if REASONS[key] else "white"

    for y, (key, name, think) in zip(ys, RUNS):
        m = hard[key]
        ref = cond(m, m["ref"])
        # (a) sensitivity
        ax.plot(ref["d_prime_ci"], [y, y], color="0.45", lw=0.8, zorder=2)
        ax.scatter(ref["d_prime"], y, s=17, facecolors=face(key), edgecolors=INK, linewidths=0.8, zorder=3)
        # (b) observed shift against the ideal shift
        ideal = LN81 / ref["d_prime"]
        bx.plot([m["delta_c"], ideal], [y, y], color="0.82", lw=0.6, zorder=1)
        bx.plot([ideal, ideal], [y - 0.36, y + 0.36], color=INK, lw=1.3, zorder=3, solid_capstyle="butt")
        bx.plot(m["delta_c_ci"], [y, y], color="0.45", lw=0.8, zorder=2)
        bx.scatter(m["delta_c"], y, s=17, facecolors=face(key), edgecolors=INK, linewidths=0.8, zorder=4)
        # (c) prior-use ratio: relabelling range, interval, point; payoffs where run
        r = ranges[key]["arms"]["base_rate"]
        cx.plot([r["min"], r["max"]], [y, y], color="0.78", lw=4.6, zorder=1, solid_capstyle="butt")
        cx.plot(m["rho_ci"], [y, y], color="0.25", lw=0.8, zorder=2)
        cx.scatter(m["rho"], y, s=17, facecolors=face(key), edgecolors=INK, linewidths=0.8, zorder=4)
        pay = m["arms"].get("payoff")
        if pay:
            cx.scatter(pay["rho"], y - 0.30, marker="D", s=9, facecolors="white", edgecolors="0.35", linewidths=0.7, zorder=3)
        # (d) budget
        tok = median_tokens(key)
        dx.plot([10, tok], [y, y], color="0.82", lw=0.6, zorder=1)
        dx.scatter(tok, y, s=17, facecolors=face(key), edgecolors=INK, linewidths=0.8, zorder=3)

    ax.set_yticks(ys, [row_label(n, t) for _, n, t in RUNS])
    ax.set_ylim(min(ys) - 0.75, max(ys) + 0.75)
    ax.set_xlim(0.9, 4.1)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xlabel("sensitivity $d'$")
    ax.set_title("(a) Skill", loc="left", pad=14)

    bx.axvline(0, color=FAINT, lw=0.6, zorder=0)
    bx.set_xlim(-0.35, 3.35)
    bx.set_xticks([0, 1, 2, 3])
    bx.set_xlabel("criterion shift, “told 10%” to “told 90%”")
    bx.set_title("(b) Observed and ideal shift", loc="left", pad=14)

    cx.axvline(0, color=FAINT, lw=0.6, zorder=0)
    cx.axvline(1, color=INK, lw=0.9, ls=(0, (4, 2)), zorder=0)
    cx.text(0.0, max(ys) + 0.80, "ignores\nthe rate", ha="center", va="bottom", fontsize=6.0, color=MUTED, linespacing=0.9)
    cx.text(1.0, max(ys) + 0.80, "ideal\nobserver", ha="center", va="bottom", fontsize=6.0, color="0.2", linespacing=0.9)
    cx.set_xlim(-0.36, 1.12)
    cx.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "0.25", "0.5", "0.75", "1"])
    cx.set_xlabel(r"prior-use ratio $\rho$ (observed / ideal)")
    cx.set_title("(c) Prior use", loc="left", pad=14)
    dx.set_xscale("log")
    dx.set_xlim(10, 14000)
    dx.set_xticks([10, 100, 1000, 10000], ["10", "100", "1k", "10k"])
    dx.minorticks_off()
    dx.set_xlabel("output tokens per reply")
    dx.set_title("(d) Budget", loc="left", pad=14)
    fig.legend(handles=[Line2D([], [], color="0.35", lw=0.8, marker="o", ms=4, mfc="white", mec=INK, mew=0.8, label="reasoning off"),
                        Line2D([], [], color="0.35", lw=0.8, marker="o", ms=4, mfc=INK, mec=INK, label="reasoning on (with 95% interval)"),
                        Line2D([], [], ls="", marker="|", ms=7, mec=INK, mew=1.3, label=r"ideal shift, $\ln 81/d'$"),
                        Patch(facecolor="0.78", edgecolor="none", label=r"range of $\rho$ over disputed labels"),
                        Line2D([], [], ls="", marker="D", ms=3.2, mfc="white", mec="0.35", mew=0.7, label=r"$\rho$ for stated payoffs")],
               loc="upper center", bbox_to_anchor=(0.5, -0.015), ncol=5, frameon=False, handletextpad=0.4,
               columnspacing=1.3, handlelength=1.5)
    save(fig, "fig2_prior_use")


# ---------------------------------------------------------------- Figure 3
def fig3(hard):
    ys, spans = row_positions()
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.0, 2.8), gridspec_kw={"width_ratios": [1.22, 1.0], "wspace": 0.80})

    # (a) effective probability on the hard set
    for i, (_, y0, y1) in enumerate(spans):
        if i % 2 == 0:
            ax.axhspan(y1 - 0.5, y0 + 0.5, color="0.955", lw=0, zorder=0)
    for y, (key, name, think) in zip(ys, RUNS):
        m = hard[key]
        p10, p90, pc = p_eff(m, "br10"), p_eff(m, "br90"), p_eff(m, "presuppose")
        on = REASONS[key]
        ax.plot([logit(p10), logit(p90)], [y, y], color="0.6", lw=1.3, zorder=1, solid_capstyle="round")
        ax.scatter(logit(p10), y, marker="<", s=20, edgecolors=BLUE, facecolors=BLUE if on else "white", linewidths=0.8, zorder=3)
        ax.scatter(logit(p90), y, marker=">", s=20, edgecolors=ORANGE, facecolors=ORANGE if on else "white", linewidths=0.8, zorder=3)
        ax.scatter(logit(pc), y, marker="X", s=30, color=INK, zorder=4, linewidths=0.3, edgecolors="white")
    for p, col in ((0.1, BLUE), (0.9, ORANGE)):
        ax.axvline(logit(p), color=col, ls=(0, (4, 2)), lw=0.9, zorder=0)
    ax.axvline(0, color=FAINT, lw=0.5, zorder=0)
    ax.text(logit(0.1), max(ys) + 0.62, "ideal,\ntold 10%", ha="center", va="bottom", fontsize=6.0, color="0.2", linespacing=0.9)
    ax.text(logit(0.9), max(ys) + 0.62, "ideal,\ntold 90%", ha="center", va="bottom", fontsize=6.0, color="0.2", linespacing=0.9)
    ticks = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]
    ax.set_xticks([logit(t) for t in ticks], [f"{t:g}" for t in ticks])
    ax.set_xlim(logit(0.04), logit(0.992))
    ax.set_ylim(min(ys) - 0.75, max(ys) + 0.75)
    ax.set_yticks(ys, [row_label(n, t) for _, n, t in RUNS])
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("effective probability of an error: the stated rate that would\njustify the critic's shift from its threshold with no added line")
    ax.set_title("(a) Hard set: what each line was worth", loc="left", pad=14)
    ax.legend(handles=[Line2D([], [], ls="", marker="<", ms=4.2, mfc=BLUE, mec=BLUE, label="told 10% flawed"),
                       Line2D([], [], ls="", marker=">", ms=4.2, mfc=ORANGE, mec=ORANGE, label="told 90% flawed"),
                       Line2D([], [], ls="", marker="X", ms=5, mfc=INK, mec="white", mew=0.3, label="told “This solution contains an error…”")],
              loc="upper center", bbox_to_anchor=(0.5, -0.26), ncol=3, frameon=False, handletextpad=0.1, columnspacing=1.0)
    clean(ax, keep=("bottom",))

    # (b) the preregistered claim test: false alarms per 100 correct solutions
    crit = [("qwen3.5:27b-think-bf16-t1", "Qwen3.5-27B (on)", "o", INK, INK),
            ("opus-5.5-think", "Opus 5.5 (high)", "s", "white", INK)]
    raw = {key: raw_rates(premise_path(key)) for key, *_ in crit}
    yb = list(range(len(CLAIM_ROWS)))[::-1]
    bx.axhspan(1.5, 5.5, color="0.94", lw=0, zorder=0)   # the four claims of an error
    for key, name, mk, fc, ec in crit:
        for y, (cn, _) in zip(yb, CLAIM_ROWS):
            v = 100 * raw[key][cn]["fa"]
            bx.plot([100 * raw[key]["neutral"]["fa"], v], [y, y], color="0.75", lw=0.6, zorder=1)
            bx.scatter(v, y, marker=mk, s=22, facecolors=fc, edgecolors=ec, linewidths=0.9, zorder=3,
                       label=name if cn == "neutral" else None)
    base = [100 * raw[k]["neutral"]["fa"] for k, *_ in crit]
    bx.axvspan(min(base), max(base), color="0.80", lw=0, zorder=0.5)
    bx.text(np.mean(base), len(CLAIM_ROWS) - 0.42, "no added\nline", fontsize=5.8, color=MUTED, ha="center", va="bottom", linespacing=0.9)
    for y0, txt in ((8.38, "no claim"), (5.38, "claims of an error"), (1.38, "discounted, opposite")):
        bx.text(99.5, y0, txt, fontsize=6.0, color=MUTED, ha="right", va="top", style="italic")
    bx.set_yticks(yb, [r for _, r in CLAIM_ROWS])
    bx.set_xlim(0, 100)
    bx.set_ylim(-0.6, len(CLAIM_ROWS) - 0.4)
    bx.set_xlabel("false alarms per 100 correct solutions")
    bx.set_title("(b) Held-out set: the preregistered claim test", loc="left", pad=14)
    bx.legend(loc="upper center", bbox_to_anchor=(0.5, -0.26), ncol=2, frameon=False, handletextpad=0.2, columnspacing=1.2)
    bx.tick_params(axis="y", length=0)
    clean(bx, keep=("bottom",))
    save(fig, "fig3_numbers_vs_claims")


# ---------------------------------------------------------------- Figure 4
def fig4(prem):
    crit = [("opus-5.5-think", "Opus 5.5 (high)"), ("qwen3.5:27b-think-bf16-t1", "Qwen3.5-27B (on)")]
    rows = [("neutral", "no added line"), ("claim_bare", "“This solution\ncontains an error.”")]
    edges = np.arange(0, 101, 10)
    mid = (edges[:-1] + edges[1:]) / 2
    fig, axes = plt.subplots(2, 2, figsize=(3.35, 2.55), sharex=True, sharey=True,
                             gridspec_kw={"wspace": 0.10, "hspace": 0.22})
    for j, (key, name) in enumerate(crit):
        rates = raw_rates(premise_path(key))
        for i, (cn, lab) in enumerate(rows):
            ax = axes[i, j]
            co, fl = scores(premise_path(key), cn)
            a = auc(co, fl)
            assert abs(a - cond(prem[key], cn)["auc"]) < 1e-9, (key, cn, a)
            hc = 100 * np.histogram(np.clip(co, 0, 99.9), edges)[0] / len(co)
            hf = 100 * np.histogram(np.clip(fl, 0, 99.9), edges)[0] / len(fl)
            ax.bar(mid - 2.1, hc, width=4.0, color="0.72", lw=0, zorder=2)
            ax.bar(mid + 2.1, hf, width=4.0, color=INK, lw=0, zorder=2)
            ax.axvline(50, color="0.35", lw=0.6, ls=(0, (2, 2)), zorder=1)
            ax.text(47, 97, f"AUC {a:.2f}\n{100 * rates[cn]['fa']:.0f} false alarms\nper 100 correct", fontsize=6.0,
                    ha="right", va="top", color="0.15", linespacing=1.05)
            ax.set_ylim(0, 104)
            ax.set_xlim(0, 100)
            ax.set_yticks([0, 50, 100])
            ax.set_xticks([0, 50, 100])
            clean(ax)
            if i == 0:
                ax.set_title(name, fontsize=7.5, pad=3)
            if j == 0:
                ax.set_ylabel(lab + "\n% of solutions", fontsize=6.6)
    fig.supxlabel("stated probability that the solution contains an error (%)", fontsize=7.2, y=-0.045)
    fig.legend(handles=[Patch(facecolor="0.72", edgecolor="none", label="correct solutions"),
                        Patch(facecolor=INK, edgecolor="none", label="flawed solutions"),
                        Line2D([], [], color="0.35", lw=0.6, ls=(0, (2, 2)), label="even odds")],
               loc="upper center", bbox_to_anchor=(0.5, 1.065), ncol=3, frameon=False, handlelength=1.1,
               handletextpad=0.4, columnspacing=1.0)
    save(fig, "fig4_decision_vs_evidence")


# ---------------------------------------------------------------- Appendix figures
def figA1(hard):
    fig, axes = plt.subplots(2, 7, figsize=(7.0, 2.9), sharex=True, sharey=True,
                             gridspec_kw={"wspace": 0.10, "hspace": 0.42})
    p = np.linspace(0.04, 0.96, 300)
    for ax, (key, name, think) in zip(axes.ravel(), RUNS):
        m = hard[key]
        dd = d_ref(m)
        sh = shifts_from_50(key, m)
        ax.axhline(0, color=FAINT, lw=0.5, zorder=0)
        ax.plot(p, np.log((1 - p) / p) / dd, color=INK, lw=0.9, ls=(0, (4, 2)), zorder=1)
        on = REASONS[key]
        ax.plot([0.1, 0.5, 0.9], [sh["br10"][0], 0, sh["br90"][0]], color="0.45", lw=0.8, zorder=2)
        for xx, cn, col, mk in ((0.1, "br10", BLUE, "<"), (0.9, "br90", ORANGE, ">")):
            est, lo, hi = sh[cn]
            ax.plot([xx, xx], [lo, hi], color=col, lw=1.0, zorder=3)
            ax.scatter(xx, est, marker=mk, s=16, edgecolors=col, facecolors=col if on else "white", linewidths=0.8, zorder=4)
        ax.scatter(0.5, 0, marker="o", s=9, color="0.35", zorder=4, linewidths=0)
        ax.set_title(f"{name} ({think})\n$d'={dd:.2f}$, $\\rho={m['rho']:.2f}$", fontsize=6.3, pad=2.5, linespacing=1.05)
        ax.set_xlim(0, 1)
        ax.set_ylim(-1.75, 1.75)
        ax.set_xticks([0.1, 0.5, 0.9], ["10", "50", "90"])
        ax.set_yticks([-1, 0, 1])
        clean(ax)
    fig.supxlabel("stated share of flawed solutions (%)", fontsize=7.5, y=-0.02)
    fig.supylabel("criterion relative to “told 50%”", fontsize=7.5, x=0.075)
    fig.legend(handles=[Line2D([], [], color=INK, lw=0.9, ls=(0, (4, 2)), label=r"ideal observer, $c^*(p)=\ln[(1-p)/p]\,/\,d'$"),
                        Line2D([], [], color="0.45", lw=0.8, marker="<", ms=3.8, mfc=BLUE, mec=BLUE, label="critic, told 10% (95% interval)"),
                        Line2D([], [], color="0.45", lw=0.8, marker=">", ms=3.8, mfc=ORANGE, mec=ORANGE, label="critic, told 90% (95% interval)")],
               loc="upper center", bbox_to_anchor=(0.5, 1.07), ncol=3, frameon=False, columnspacing=1.6)
    save(fig, "figA1_ideal_curves")


def figA2():
    cols = [("neutral", "no added\nline"), ("check_only", "“Check…\ncarefully”"), ("may_error", "“may or\nmay not”"),
            ("presuppose", "“error.\nCheck it”"), ("claim_bare", "“contains\nan error”"),
            ("claim_mistake", "“a mistake\nsomewhere”"), ("claim_reviewer", "“previous\nreviewer”"),
            ("claim_random", "“attached\nat random”"), ("claim_correct", "“is\ncorrect”"),
            ("br10", "batch:\n10%"), ("br90", "batch:\n90%"), ("item_p10", "this one:\n10%"), ("item_p90", "this one:\n90%")]
    Z = np.full((len(PREMISE_RUNS), len(cols)), np.nan)
    for i, (key, _, _) in enumerate(PREMISE_RUNS):
        raw = raw_rates(premise_path(key))
        for j, (cn, _) in enumerate(cols):
            if cn in raw:
                Z[i, j] = 100 * raw[cn]["fa"]
    fig, ax = plt.subplots(figsize=(7.0, 2.75))
    cmap = matplotlib.colormaps["Greys"].copy()
    cmap.set_bad("white")
    ax.imshow(np.ma.masked_invalid(Z), cmap=cmap, vmin=0, vmax=118, aspect="auto")
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            v = Z[i, j]
            ax.text(j, i, "–" if np.isnan(v) else f"{v:.0f}", ha="center", va="center", fontsize=6.6,
                    color="0.55" if np.isnan(v) else ("white" if v > 55 else INK))
    ax.set_xticks(range(len(cols)), [c for _, c in cols], fontsize=5.8, linespacing=0.95)
    ax.set_yticks(range(len(PREMISE_RUNS)), [row_label(n, t) for _, n, t in PREMISE_RUNS])
    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    for xline in (0.5, 2.5, 6.5, 8.5):
        ax.axvline(xline, color="white", lw=2.2)
    ax.axhline(7.5, color="white", lw=2.2)
    for x0, x1, txt in ((1, 2, "no claim"), (3, 6, "claims of an error"), (7, 8, "discounted, opposite"), (9, 12, "stated rates")):
        ax.text((x0 + x1) / 2, len(PREMISE_RUNS) - 0.32, txt, ha="center", va="top", fontsize=6.4, color=MUTED, style="italic")
    clean(ax, keep=())
    save(fig, "figA2_claim_grid")


# ---------------------------------------------------------------- numbers for the text and tables
def fmt(x, nd=2):
    return "--" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{nd}f}".replace("-", "$-$")


def fmt_ci(x, lohi, nd=2):
    return "--" if x is None else f"{fmt(x, nd)} [{fmt(lohi[0], nd)}, {fmt(lohi[1], nd)}]"


def numbers(hard, prem, ranges):
    print("\n== effective P(error), hard set: told 10% / told 90% / claim")
    e10, e90, ec, beats90, beats_span = [], [], [], 0, 0
    for key, name, think in RUNS:
        m = hard[key]
        a, b, c = p_eff(m, "br10"), p_eff(m, "br90"), p_eff(m, "presuppose")
        e10.append(a); e90.append(b); ec.append(c)
        beats90 += c > b
        beats_span += -cond(m, "presuppose")["c_minus_neutral"] >= m["delta_c"]
        print(f"  {name:12s} {think:5s} {a:.2f} {b:.2f} {c:.2f}")
    print(f"  median told 10%: {median(e10):.2f} (range {min(e10):.2f}-{max(e10):.2f}); told 90%: {median(e90):.2f} "
          f"(range {min(e90):.2f}-{max(e90):.2f}); claim: median {median(ec):.2f} (range {min(ec):.2f}-{max(ec):.2f})")
    print(f"  claim further toward 'error' than told 90%: {beats90} of {len(RUNS)}; claim shift >= whole 10%->90% shift: {beats_span}")

    print("\n== Table 1 rows (hard set): critic & reasoning & tokens & d' & rho [CI] & rho payoffs & p_eff 10 / 90 / claim")
    for key, name, think in RUNS:
        m = hard[key]
        pay = m["arms"].get("payoff", {}).get("rho")
        r = ranges[key]["arms"]["base_rate"]
        print(f"  {name} & {think} & {round(median_tokens(key)):,} & {fmt(d_ref(m))} & {fmt_ci(m['rho'], m['rho_ci'])} & {fmt(pay)} & "
              f"{fmt(p_eff(m, 'br10'))} & {fmt(p_eff(m, 'br90'))} & {fmt(p_eff(m, 'presuppose'))} \\\\"
              f"   % relabelled {r['min']:.2f}..{r['max']:.2f}; delta_c {m['delta_c']:.2f}; ideal {m['ideal_delta_c']:.2f}; "
              f"lenient {cond(m, 'lenient')['c_minus_neutral']:+.2f}; claim {cond(m, 'presuppose')['c_minus_neutral']:+.2f}")
    rhos = [hard[k]["rho"] for k, _, _ in RUNS]
    print(f"  rho range {min(rhos):.2f}-{max(rhos):.2f}; largest upper limit {max(hard[k]['rho_ci'][1] for k, _, _ in RUNS):.2f}")
    len_ = [cond(hard[k], "lenient")["c_minus_neutral"] for k, _, _ in RUNS]
    share = sum(l >= 0.8 * hard[k]["delta_c"] for l, (k, _, _) in zip(len_, RUNS))
    print(f"  'lenient' shift: {min(len_):+.2f}..{max(len_):+.2f}; positive in {sum(l > 0 for l in len_)}; >= 80% of the 10->90 shift in {share}")

    print("\n== reasoning: d' off -> on, observed shift off -> on")
    by = {}
    for key, name, think in RUNS:
        by.setdefault(name, []).append((think, d_ref(hard[key]), hard[key]["delta_c"], hard[key]["rho"]))
    for name, v in by.items():
        print(f"  {name:12s} " + "  ".join(f"{t}: d'={d:.2f} dc={dc:.2f} rho={r:.2f}" for t, d, dc, r in v))

    print("\n== held-out set: raw false alarms / hits per 100")
    for key, name, think in PREMISE_RUNS:
        raw = raw_rates(premise_path(key))
        print(f"  {name} ({think}): " + "; ".join(f"{cn} {100 * raw[cn]['fa']:.0f}/{100 * raw[cn]['hit']:.0f}" for cn, _ in CLAIM_ROWS))

    print("\n== held-out set: effective P(error), numbers against claims (d' with no added line)")
    for key, name, think in PREMISE_RUNS:
        m = prem[key]
        vals = {k: p_eff(m, k) for k in ("br10", "br90", "item_p10", "item_p90", "claim_bare", "claim_mistake", "claim_random", "claim_correct")}
        print(f"  {name:12s} {think:5s} " + " ".join(f"{k}={v:.2f}" for k, v in vals.items() if v is not None))

    print("\n== held-out set: AUC of stated P(error), and its median on correct solutions")
    for key in ("opus-5.5-think", "qwen3.5:27b-think-bf16-t1"):
        out = []
        for cn, _ in CLAIM_ROWS:
            co, fl = scores(premise_path(key), cn)
            out.append(f"{cn} {auc(co, fl):.3f} (median {np.median(co):.0f})")
        print(f"  {key}: " + "; ".join(out))

    print("\n== post hoc (not preregistered): a cut-off on stated P(error) instead of the verdict, per 100 solutions")
    for key in ("opus-5.5-think", "qwen3.5:27b-think-bf16-t1"):
        raw = raw_rates(premise_path(key))
        for cn in ("neutral", "presuppose", "claim_bare", "claim_mistake"):
            co, fl = scores(premise_path(key), cn)
            cuts = "; ".join(f">{t}: FA {100 * np.mean(co > t):.0f}, hits {100 * np.mean(fl > t):.0f}" for t in (50, 80, 90, 99))
            print(f"  {key} {cn}: verdicts FA {100 * raw[cn]['fa']:.0f}, hits {100 * raw[cn]['hit']:.0f} | {cuts}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="one of 1, 2, 3, 4, A1, A2, numbers")
    args = ap.parse_args()
    hard = load_summaries("results/torch_hard/analysis/summary.json", "results/frontier/stage_c/analysis/summary.json")
    prem = load_summaries("results/premise/analysis/summary.json")
    ranges = json.load(open(ROOT / "results/label_sensitivity/report.json"))["assignment_ranges"]["hard"]["critics"]
    jobs = {"1": lambda: fig1(hard), "2": lambda: fig2(hard, ranges), "3": lambda: fig3(hard), "4": lambda: fig4(prem),
            "A1": lambda: figA1(hard), "A2": figA2, "numbers": lambda: numbers(hard, prem, ranges)}
    for name, job in jobs.items():
        if args.only in (None, name):
            job()


if __name__ == "__main__":
    main()
