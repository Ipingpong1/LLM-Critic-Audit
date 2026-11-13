"""Open models beside Claude on the same 200 hard items (prereg/torch_hard.md).

    .venv/bin/python -m pilot.analyze results/torch_hard/*.jsonl results/frontier/stage_c/*.jsonl \
        --items data/items_hard.jsonl --out-dir results/torch_hard/analysis
    .venv/bin/python scripts/plot_torch_hard.py      # results/torch_hard/analysis/torch_hard.png

Panels: (a) rho; (b) the "contains an error" shift; (c) d' on these items, and on the easier items for the open
models; (d) verdicts changed between "10%" and "90%", against what the critic's own stated confidence predicts;
(e) false alarms on the 100 correct solutions.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
OPEN, CLAUDE = "#eb6834", "#2a78d6"
INK, MUTED, GRID = "#1b2230", "#5a6476", "#dde1e8"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "text.color": INK, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "legend.frameon": False,
                     "axes.spines.top": False, "axes.spines.right": False})


def open_name(m, s):
    return f"{m}-{s}-bf16-t1"


OPEN_MODELS = ["qwen3.5:4b", "qwen3.5:9b", "gemma4:12b", "qwen3.5:27b"]
# (row label, summary name, family colour, marker)
OFF = [(m, open_name(m, "nothink"), OPEN, "o") for m in OPEN_MODELS] + \
      [("Haiku 5.5", "haiku-5.5-nothink", CLAUDE, "o"), ("Sonnet 5.5", "sonnet-5.5-nothink", CLAUDE, "o")]
ON = [(m, open_name(m, "think"), OPEN, "s") for m in OPEN_MODELS] + \
     [("Haiku 5.5", "haiku-5.5-think", CLAUDE, "s"), ("Sonnet 5.5", "sonnet-5.5-think", CLAUDE, "s"),
      ("Opus 5.5", "opus-5.5-think", CLAUDE, "s"), ("Sonnet 5.5, max", "sonnet-5.5-think-max", CLAUDE, "^")]


def cond(m, name):
    return next(c for c in m["conditions"] if c["condition"] == name)


def dot(ax, y, x, ci, col, mk, filled=True):
    err = [[max(0, x - ci[0])], [max(0, ci[1] - x)]]
    ax.errorbar(x, y, xerr=err, marker=mk, ms=6.5, color=col, mfc=col if filled else "white", mec=col if not filled else "white",
                mew=1.3 if not filled else 0.8, ls="none", capsize=2.5, elinewidth=1.1, zorder=3)


def main():
    d = ROOT / "results" / "torch_hard" / "analysis"
    summ = {m["model"]: m for m in json.load(open(d / "summary.json"))}
    easy = {m["model"]: m for m in json.load(open(ROOT / "results" / "torch" / "summary.json"))}

    rows, labels, y = [], [], 0.0
    for group in (OFF, ON):
        for r in group:
            rows.append((y, r))
            labels.append(r[0])
            y += 1
        y += 0.9
    ys = [yy for yy, _ in rows]

    fig = plt.figure(figsize=(14, 10.4))
    top = fig.add_gridspec(1, 3, left=0.1, right=0.975, top=0.915, bottom=0.5, wspace=0.16)
    low = fig.add_gridspec(1, 2, left=0.1, right=0.975, top=0.385, bottom=0.065, wspace=0.62)
    ax_a = fig.add_subplot(top[0, 0])
    ax_b = fig.add_subplot(top[0, 1], sharey=ax_a)
    ax_c = fig.add_subplot(top[0, 2], sharey=ax_a)
    ax_d = fig.add_subplot(low[0, 0])
    ax_e = fig.add_subplot(low[0, 1])

    for yy, (lab, name, col, mk) in rows:
        m = summ[name]
        dot(ax_a, yy, m["rho"], m["rho_ci"], col, mk)
        p = cond(m, "presuppose")
        dot(ax_b, yy, p["c_minus_neutral"], p["c_minus_neutral_ci"], col, mk)
        r = cond(m, "br50")
        dot(ax_c, yy, r["d_prime"], r["d_prime_ci"], col, mk)
        if name in easy:
            ax_c.plot(cond(easy[name], "br50")["d_prime"], yy, marker=mk, ms=6.5, mfc="white", mec=col, mew=1.3, ls="none", zorder=4)

    for ax in (ax_a, ax_b, ax_c):
        ax.grid(axis="x", color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.set_ylim(max(ys) + 0.7, min(ys) - 1.3)
    ax_a.set_yticks(ys, labels, fontsize=8.5)
    ax_a.tick_params(axis="y", length=0, labelcolor=INK)
    for ax in (ax_b, ax_c):
        ax.tick_params(axis="y", length=0, labelleft=False)
    ax_a.text(-0.018, -0.85, "thinking off", transform=ax_a.get_yaxis_transform(), fontsize=8.5, fontweight="bold", ha="right", va="center")
    ax_a.text(-0.018, len(OFF) - 0.05, "thinking on", transform=ax_a.get_yaxis_transform(), fontsize=8.5, fontweight="bold", ha="right", va="center")

    ax_a.axvline(1, color=MUTED, ls="--", lw=1)
    ax_a.text(0.985, min(ys) - 0.95, "ideal", color=MUTED, fontsize=7.5, ha="right", va="center")
    ax_a.axvline(0, color=MUTED, lw=0.8)
    ax_a.set_xlim(-0.3, 1.1)
    ax_a.set_xlabel("ρ = observed shift ÷ ideal shift")
    ax_a.set_title("(a) All critics use the stated rate little")

    ax_b.axvline(0, color=MUTED, lw=0.8)
    ax_b.set_xlim(-1.4, 0.75)
    ax_b.set_xticks([-1, -0.5, 0, 0.5])
    ax_b.set_xlabel("c − c(neutral)   ← flags more · flags less →")
    ax_b.set_title('(b) "This solution contains an error"')

    ax_c.set_xlim(0.8, 4.4)
    ax_c.set_xlabel('d′ when told "50%"')
    ax_c.set_title("(c) Harder items, lower d′")
    ax_c.legend(handles=[Line2D([], [], marker="s", color=MUTED, ls="none", ms=6.5, label="these 200 hard items"),
                         Line2D([], [], marker="s", mfc="white", mec=MUTED, mew=1.3, ls="none", ms=6.5, label="easier items (open models)")],
                fontsize=7.5, loc="upper right", handletextpad=0.3, borderaxespad=0.1)

    # (d) verdict changes, thinking on: what the critic did against what its own confidence predicts
    bars = ON
    yd = list(range(len(bars)))
    for yy, (lab, name, col, mk) in zip(yd, bars):
        b = summ[name]["bayes"]
        made = b["clear_predicted_done"] + b["flag_predicted_done"]
        other = b["clear_unpredicted"] + b["flag_unpredicted"]
        pred = b["clear_predicted"] + b["flag_predicted"]
        ax_d.barh(yy, made, height=0.56, color=col, zorder=3)
        ax_d.barh(yy, other, left=made, height=0.56, facecolor="white", edgecolor=col, hatch="////", lw=0.9, zorder=3)
        ax_d.plot(pred, yy, marker="D", ms=6.5, color=INK, mec="white", mew=0.8, ls="none", zorder=4)
        rb, ci = b["rho_bayes"], b["rho_bayes_ci"]
        ax_d.text(1.005, yy, f"{rb:.2f} [{ci[0]:.2f}, {ci[1]:.2f}]", transform=ax_d.get_yaxis_transform(), va="center", ha="left", fontsize=8)
    ax_d.text(1.005, -1.02, "ρ_Bayes [95% CI]", transform=ax_d.get_yaxis_transform(), va="center", ha="left", fontsize=8, fontweight="bold")
    ax_d.set_yticks(yd, [b[0] for b in bars], fontsize=8.5)
    ax_d.tick_params(axis="y", length=0, labelcolor=INK)
    ax_d.set_ylim(len(bars) - 0.45, -0.6)
    ax_d.set_xlim(0, 48)
    ax_d.grid(axis="x", color=GRID, lw=0.6)
    ax_d.set_axisbelow(True)
    ax_d.set_xlabel('verdicts changed from "50%", told 10% and told 90% together (thinking on)')
    ax_d.set_title("(d) Confidence does not predict open models' changes", pad=14)
    ax_d.legend(handles=[Patch(facecolor=MUTED, label="predicted by its confidence"),
                         Patch(facecolor="white", edgecolor=MUTED, hatch="////", label="not predicted"),
                         Line2D([], [], marker="D", color=INK, mec="white", ls="none", ms=6.5, label="all a Bayesian would change")],
                fontsize=7.5, loc="upper right", handletextpad=0.5)

    # (e) false alarms per 100 correct solutions, thinking on
    mark = [("neutral", "neutral", "o", "white", MUTED), ("br10", 'told 10%', "<", MUTED, MUTED), ("br90", 'told 90%', ">", MUTED, MUTED),
            ("presuppose", '"contains an error"', "*", INK, INK)]
    for yy, (lab, name, col, mk) in zip(yd, bars):
        m = summ[name]
        xs = {c: 100 * cond(m, c)["fa_rate"] for c, *_ in mark}
        ax_e.plot([min(xs.values()), max(xs.values())], [yy, yy], color=col, lw=1.6, zorder=2)
        for c, _, mm, fc, ec in mark:
            ax_e.plot(xs[c], yy, marker=mm, ms=11 if mm == "*" else 6.5, mfc=fc, mec=ec, mew=1.1, ls="none", zorder=3)
    ax_e.set_yticks(yd, [b[0] for b in bars], fontsize=8.5)
    ax_e.tick_params(axis="y", length=0, labelcolor=INK)
    ax_e.set_ylim(len(bars) - 0.45, -0.6)
    ax_e.set_xlim(0, 65)
    ax_e.grid(axis="x", color=GRID, lw=0.6)
    ax_e.set_axisbelow(True)
    ax_e.set_xlabel("false alarms per 100 correct solutions (thinking on)")
    ax_e.set_title("(e) One sentence takes two critics to about 60 false alarms", pad=14)
    ax_e.legend(handles=[Line2D([], [], marker=mm, mfc=fc, mec=ec, mew=1.1, ls="none", ms=11 if mm == "*" else 6.5, label=lab)
                         for _, lab, mm, fc, ec in mark], fontsize=7.5, loc="upper right", handletextpad=0.3)

    fig.legend(handles=[Patch(facecolor=OPEN, label="open models (full reasoning returned, model-card sampling at t=1)"),
                        Patch(facecolor=CLAUDE, label="Claude (summaries returned, API default sampling)"),
                        Line2D([], [], marker="o", color=MUTED, ls="none", ms=6.5, label="thinking off"),
                        Line2D([], [], marker="s", color=MUTED, ls="none", ms=6.5, label="thinking on"),
                        Line2D([], [], marker="^", color=MUTED, ls="none", ms=6.5, label="max effort")],
               loc="upper left", bbox_to_anchor=(0.03, 0.975), ncol=5, fontsize=8, columnspacing=1.6, handletextpad=0.4)
    fig.savefig(d / "torch_hard.png", dpi=170, facecolor="white")
    print(d / "torch_hard.png")


if __name__ == "__main__":
    main()
