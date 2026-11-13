"""The "contains an error" test on 200 held-out items (prereg/premise.md).

    .venv/bin/python -m pilot.analyze results/premise/*.jsonl --items data/items_premise.jsonl --ref neutral \
        --out-dir results/premise/analysis
    .venv/bin/python scripts/premise_analysis.py
    .venv/bin/python scripts/plot_premise.py      # results/premise/analysis/premise.png

Panels: (a) the 18 pre-registered tests, Holm-corrected; (b) false alarms per condition for the two primary critics;
(c) every critic's shift in c from neutral, uncorrected.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "results" / "premise" / "analysis"
OPEN, CLAUDE = "#eb6834", "#2a78d6"          # same family colours as torch_hard.png
INK, MUTED, GRID, BAND = "#1b2230", "#5a6476", "#dde1e8", "#eef0f4"
# Diverging: purple = flags more, green = flags less, light grey at 0 (ColorBrewer PRGn ends, colour-blind safe).
DIV = LinearSegmentedColormap.from_list("prgn", ["#40004b", "#9970ab", "#f2f2f2", "#5aae61", "#00441b"])
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "text.color": INK, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "legend.frameon": False,
                     "axes.spines.top": False, "axes.spines.right": False})

PRIMARY = [("qwen3.5:27b-think-bf16-t1", "qwen3.5:27b, thinking on", OPEN, "o"),
           ("opus-5.5-think", "Opus 5.5, thinking on", CLAUDE, "s")]
TESTS = {"T1": 'original wording − neutral', "T2": 'bare claim − neutral', "T3": '"a mistake" − neutral',
         "T4": '"a reviewer found" − neutral', "T5": 'original − "check carefully"',
         "T6": 'original − "may or may not"', "T7": 'random note − neutral', "T8": 'random note − bare claim',
         "T9": '"is correct" − neutral'}
# (condition, short label, group)
CONDS = [("presuppose", "contains an error.\nCheck it carefully.", "claim of an error"),
         ("claim_bare", "contains\nan error.", "claim of an error"),
         ("claim_mistake", "a mistake\nsomewhere.", "claim of an error"),
         ("claim_reviewer", "a reviewer\nfound an error.", "claim of an error"),
         ("check_only", "Check it\ncarefully.", "no claim"),
         ("may_error", "may or may not\ncontain an error.", "no claim"),
         ("claim_random", "random note\nsays: an error.", "said to be\nuninformative"),
         ("claim_correct", "is correct.", "opposite")]
CRITICS = [("qwen3.5:4b-think-bf16-t1", "qwen3.5:4b"), ("qwen3.5:9b-think-bf16-t1", "qwen3.5:9b"),
           ("gemma4:12b-think-bf16-t1", "gemma4:12b"), ("qwen3.5:27b-think-bf16-t1", "qwen3.5:27b ★"),
           ("haiku-5.5-think", "Haiku 5.5"), ("opus-5.5-think", "Opus 5.5 ★"),
           ("qwen3.5:4b-nothink-bf16-t1", "qwen3.5:4b"), ("qwen3.5:9b-nothink-bf16-t1", "qwen3.5:9b"),
           ("gemma4:12b-nothink-bf16-t1", "gemma4:12b"), ("qwen3.5:27b-nothink-bf16-t1", "qwen3.5:27b")]


def cond(m, name):
    return next((c for c in m["conditions"] if c["condition"] == name), None)


def main():
    tests = json.load(open(D / "premise.json"))["primary_tests"]
    summ = {m["model"]: m for m in json.load(open(D / "summary.json"))}

    fig = plt.figure(figsize=(14, 11))
    top = fig.add_gridspec(1, 2, left=0.17, right=0.975, top=0.9, bottom=0.53, wspace=0.6, width_ratios=[1.2, 1])
    ax_a, ax_b = fig.add_subplot(top[0, 0]), fig.add_subplot(top[0, 1])
    ax_c = fig.add_subplot(fig.add_gridspec(1, 1, left=0.17, right=0.86, top=0.315, bottom=0.03)[0, 0])
    cax = fig.add_axes([0.885, 0.05, 0.012, 0.25])

    # (a) the pre-registered tests
    names = list(TESTS)
    for j, (crit, lab, col, mk) in enumerate(PRIMARY):
        for t in tests:
            if t["critic"] != crit:
                continue
            y = names.index(t["test"]) + (-0.17 if j == 0 else 0.17)
            lo, hi = t["ci"]
            ax_a.errorbar(t["est"], y, xerr=[[t["est"] - lo], [hi - t["est"]]], marker=mk, ms=6.5, color=col,
                          mfc=col if t["held"] else "white", mec=col, mew=1.3, ls="none", capsize=2.5, elinewidth=1.1,
                          zorder=3)
    ax_a.axvspan(-0.3, 0.3, color=BAND, zorder=0)
    ax_a.axvline(0, color=MUTED, lw=0.8)
    for y in (3.5, 5.5):
        ax_a.axhline(y, color=GRID, lw=0.8)
    ax_a.set_yticks(range(len(names)), [f"{k}  {v}" for k, v in TESTS.items()], fontsize=8.5)
    ax_a.tick_params(axis="y", length=0, labelcolor=INK)
    ax_a.set_ylim(len(names) - 0.4, -0.9)
    ax_a.set_xlim(-1.75, 1.55)
    ax_a.grid(axis="x", color=GRID, lw=0.6)
    ax_a.set_axisbelow(True)
    ax_a.set_xlabel("difference in criterion c   ← flags more · flags less →")
    ax_a.text(0, -0.72, '"no shift" range (±0.3)', color=MUTED, fontsize=7.5, ha="center", va="center")
    ax_a.set_title("(a) 16 of 18 pre-registered tests held", pad=10)
    ax_a.legend(handles=[Line2D([], [], marker="o", color=MUTED, ls="none", ms=6.5, label="held (Holm p < .05)"),
                         Line2D([], [], marker="o", mfc="white", mec=MUTED, mew=1.3, ls="none", ms=6.5,
                                label="not held (no direction predicted for T7)")],
                fontsize=7.5, loc="lower left", handletextpad=0.3, borderaxespad=0.2)

    # (b) false alarms per condition, primary critics
    rows = [("neutral", "no added line")] + [(c, lab.replace("\n", " ")) for c, lab, _ in CONDS]
    for j, (crit, lab, col, mk) in enumerate(PRIMARY):
        m = summ[crit]
        for i, (c, _) in enumerate(rows):
            x = 100 * cond(m, c)["fa_rate"]
            ax_b.plot(x, i + (-0.13 if j == 0 else 0.13), marker=mk, ms=7, color=col, mec="white", mew=0.8, ls="none", zorder=3)
        base = 100 * cond(m, "neutral")["fa_rate"]
        ax_b.axvline(base, color=col, lw=0.9, ls=(0, (3, 2)), zorder=1)
    for y in (0.5, 4.5, 6.5, 7.5):
        ax_b.axhline(y, color=GRID, lw=0.8)
    ax_b.set_yticks(range(len(rows)), [r[1] for r in rows], fontsize=8.5)
    ax_b.tick_params(axis="y", length=0, labelcolor=INK)
    ax_b.set_ylim(len(rows) - 0.4, -0.9)
    ax_b.set_xlim(0, 100)
    ax_b.grid(axis="x", color=GRID, lw=0.6)
    ax_b.set_axisbelow(True)
    ax_b.set_xlabel("false alarms per 100 correct solutions (dashed: no added line)")
    # start the title at the row labels, not the axes, so it fits
    ax_b.text(-0.5, 1.035, "(b) A claim raises false alarms; checking alone does not", transform=ax_b.transAxes,
              fontsize=10, fontweight="bold", ha="left", va="bottom")
    ax_b.legend(handles=[Line2D([], [], marker=mk, color=col, mec="white", ls="none", ms=7, label=lab)
                         for _, lab, col, mk in PRIMARY], fontsize=7.5, loc="lower right", handletextpad=0.3)

    # (c) every critic, shift from neutral
    M = np.full((len(CRITICS), len(CONDS)), np.nan)
    sig = np.zeros_like(M, bool)
    for i, (crit, _) in enumerate(CRITICS):
        for k, (c, _, _) in enumerate(CONDS):
            r = cond(summ[crit], c)
            if r is not None:
                M[i, k] = r["c_minus_neutral"]
                lo, hi = r["c_minus_neutral_ci"]
                sig[i, k] = lo > 0 or hi < 0
    norm = TwoSlopeNorm(vmin=-1.4, vcenter=0, vmax=1.4)
    im = ax_c.imshow(np.ma.masked_invalid(M), cmap=DIV, norm=norm, aspect="auto")
    for i in range(M.shape[0]):
        for k in range(M.shape[1]):
            v = M[i, k]
            ax_c.add_patch(plt.Rectangle((k - 0.5, i - 0.5), 1, 1, fill=False, ec="white", lw=2))
            if np.isnan(v):
                continue
            ax_c.text(k, i, f"{v:+.2f}", ha="center", va="center", fontsize=8,
                      color="white" if abs(v) > 0.75 else INK, fontweight="bold" if sig[i, k] else "normal")
    ax_c.set_xticks(range(len(CONDS)), [lab for _, lab, _ in CONDS], fontsize=8)
    ax_c.xaxis.tick_top()
    ax_c.tick_params(axis="both", length=0)
    ax_c.set_yticks(range(len(CRITICS)), [lab for _, lab in CRITICS], fontsize=8.5)
    ax_c.tick_params(axis="y", labelcolor=INK)
    for s in ax_c.spines.values():
        s.set_visible(False)
    for y in (3.5, 5.5):
        ax_c.axhline(y, color="white", lw=5)
    tr = ax_c.get_yaxis_transform()
    for y0, y1, lab in ((0, 3, "open models,\nthinking on"), (4, 5, "Claude,\nthinking on"), (6, 9, "open models,\nthinking off")):
        ax_c.plot([-0.115, -0.115], [y0 - 0.35, y1 + 0.35], color=MUTED, lw=1, transform=tr, clip_on=False)
        ax_c.text(-0.125, (y0 + y1) / 2, lab, transform=tr, ha="right", va="center", fontsize=8, fontweight="bold")
    # group headers above the column labels
    xt = ax_c.get_xaxis_transform()
    for k0, k1, lab in ((0, 3, "claim of an error"), (4, 5, "no claim"), (6, 6, "claim said to be\nuninformative"),
                        (7, 7, "opposite claim")):
        ax_c.plot([k0 - 0.42, k1 + 0.42], [1.2, 1.2], color=MUTED, lw=1, transform=xt, clip_on=False)
        ax_c.text((k0 + k1) / 2, 1.23, lab, transform=xt, ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax_c.set_title("(c) Every critic: c − c(neutral). Bold: 95% CI excludes 0 (uncorrected). ★ primary critics",
                   pad=92)
    cb = fig.colorbar(im, cax=cax)
    cb.outline.set_visible(False)
    cb.ax.tick_params(labelsize=7.5, length=0)
    cb.set_label("← flags more · flags less →", fontsize=8)

    fig.suptitle('"This solution contains an error": 200 held-out items, 3 samples per item (Opus: 1–2)',
                 x=0.035, y=0.975, ha="left", fontsize=12, fontweight="bold")
    fig.savefig(D / "premise.png", dpi=170, facecolor="white")
    print(D / "premise.png")


if __name__ == "__main__":
    main()
