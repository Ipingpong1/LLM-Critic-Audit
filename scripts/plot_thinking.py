"""Figures comparing thinking off and on, from the Torch summary (run pilot.analyze on results/torch first).

    .venv/bin/python scripts/plot_thinking.py [results/torch]

Writes thinking_summary.png, thinking_criterion.png, thinking_roc.png and thinking_strictness.png.
Thinking on vs off is compared at the same sampling (T = 1, the model cards' setting); the greedy
thinking-off run (T = 0) is shown as a hollow grey reference in the summary figure.
"""
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pilot.prompts import FRAMING_LABELS  # noqa: E402

MODELS = [("qwen3.5:4b", "qwen 4b"), ("qwen3.5:9b", "qwen 9b"), ("qwen3.5:27b", "qwen 27b"), ("gemma4:12b", "gemma 12b")]
# (label suffix, legend text, color, marker, filled)
SETTINGS = [("nothink-bf16", "thinking off, T = 0", "#9aa3b2", "o", False),
            ("nothink-bf16-t1", "thinking off, T = 1", "#2a78d6", "o", True),
            ("think-bf16-t1", "thinking on, T = 1", "#eb6834", "D", True)]
MAIN = SETTINGS[1:]
INK, MUTED, GRID = "#1b2230", "#5a6476", "#dde1e8"

plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "text.color": INK, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "legend.frameon": False, "axes.spines.top": False, "axes.spines.right": False})


def load(d):
    res = {r["model"]: r for r in json.load(open(d / "summary.json"))}
    for r in res.values():
        r["by"] = {c["condition"]: c for c in r["conditions"]}
    return res


def get(res, model, suffix):
    return res.get(f"{model}-{suffix}")


def marker_kw(color, marker, filled, ms=7):
    return dict(marker=marker, ms=ms, color=color, mfc=color if filled else "white", mec=color, mew=1.5,
                ls="none", capsize=3, elinewidth=1.2)


def summary(res, path):
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.0), gridspec_kw={"width_ratios": [1, 1, 1]})
    off = {s[0]: (i - 1) * 0.24 for i, s in enumerate(SETTINGS)}
    panels = [("skill: d′ with no instruction", lambda r: (r["by"]["neutral"]["d_prime"], r["by"]["neutral"]["d_prime_ci"])),
              ("prior use: stated base rate (ρ)", lambda r: (r["arms"]["base_rate"]["rho"], r["arms"]["base_rate"]["rho_ci"])),
              ("prior use: stated payoffs (ρ)", lambda r: (r["arms"]["payoff"]["rho"], r["arms"]["payoff"]["rho_ci"]))]
    for k, (ax, (title, fn)) in enumerate(zip(axes, panels)):
        for suf, lab, col, mk, filled in SETTINGS:
            for i, (m, _) in enumerate(MODELS):
                r = get(res, m, suf)
                if r is None:
                    continue
                y, (lo, hi) = fn(r)
                ax.errorbar(i + off[suf], y, yerr=[[y - lo], [hi - y]], label=lab if i == 0 else None,
                            **marker_kw(col, mk, filled))
        ax.set_xticks(range(len(MODELS)), [n for _, n in MODELS])
        ax.set_xlim(-0.6, len(MODELS) - 0.4)
        ax.set_title(title, loc="left")
        ax.grid(axis="y", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        if k == 0:
            ax.set_ylim(0, 5.2)
            ax.set_ylabel("d′  (higher = better at telling flawed from correct)")
        else:
            ax.set_ylim(-0.45, 1.1)
            ax.axhline(1, color=MUTED, ls="--", lw=1)
            ax.text(len(MODELS) - 0.45, 1.02, "ideal observer", ha="right", va="bottom", fontsize=8, color=MUTED)
            ax.axhline(0, color=MUTED, lw=0.8)
            if k == 1:
                ax.set_ylabel("ρ = observed ÷ ideal threshold shift")
    axes[0].legend(loc="lower right", fontsize=8)
    fig.suptitle("Thinking makes critics much better detectors, but they still barely use the stated base rate or payoffs",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(path, dpi=200)
    plt.close(fig)


def criterion(res, path):
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.9), sharey=True)
    for ax, (m, name) in zip(axes, MODELS):
        notes = []
        for suf, lab, col, mk, filled in MAIN:
            r = get(res, m, suf)
            if r is None:
                continue
            pts = [(c["stated_p_error"], c) for c in r["conditions"] if c["arm"] == "base_rate" and c["stated_p_error"]]
            x = np.array([math.log(p / (1 - p)) for p, _ in pts])
            y = np.array([c["c"] for _, c in pts])
            lo = y - np.array([c["c_ci"][0] for _, c in pts]); hi = np.array([c["c_ci"][1] for _, c in pts]) - y
            d50, c50 = r["by"]["br50"]["d_prime"], r["by"]["br50"]["c"]
            xs = np.linspace(-2.4, 2.4, 10)
            ax.plot(xs, c50 - xs / d50, ls="--", color=col, lw=1.2, alpha=0.8)
            ax.errorbar(x, y, yerr=[lo, hi], label=lab, **marker_kw(col, mk, filled))
            ax.plot(x, y, color=col, lw=1.5)
            notes.append((col, f"ρ = {r['arms']['base_rate']['rho']:.2f}"))
        for j, (col, t) in enumerate(notes):
            ax.text(0.97, 0.97 - 0.08 * j, t, transform=ax.transAxes, ha="right", va="top", color=col, fontsize=9,
                    fontweight="bold")
        ax.axhline(0, color=GRID, lw=1)
        ax.set_xticks([math.log(1 / 9), 0, math.log(9)], ["10%", "50%", "90%"])
        ax.set_title(name, loc="left")
        ax.set_xlabel("stated error rate (log-odds scale)")
    axes[0].set_ylabel("criterion c  (+ lenient, − flag-happy)")
    axes[0].legend(loc="lower left", fontsize=8)
    fig.suptitle("Solid: observed criterion. Dashed: where an ideal observer with the same skill would put it.",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(path, dpi=200)
    plt.close(fig)


def roc(res, path):
    """Operating points for br10/br50/br90, with the ideal observer's br10/br90 points on the same iso-d′ curve."""
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.75))
    f = np.linspace(0.0005, 0.9995, 400)
    for ax, (m, name) in zip(axes, MODELS):
        for suf, lab, col, mk, filled in MAIN:
            r = get(res, m, suf)
            if r is None:
                continue
            d50, c50 = r["by"]["br50"]["d_prime"], r["by"]["br50"]["c"]
            ax.plot(f, norm.cdf(d50 + norm.ppf(f)), color=col, lw=1, alpha=0.45)
            obs = [r["by"][c] for c in ("br10", "br50", "br90")]
            ax.plot([o["fa_rate"] for o in obs], [o["hit_rate"] for o in obs], color=col, lw=1.5,
                    marker=mk, ms=6, mfc=col, mec="white", mew=1, label=f"{lab}: observed", zorder=3)
            ideal = [c50 + math.log((1 - p) / p) / d50 for p in (0.1, 0.9)]
            ax.plot([norm.cdf(-d50 / 2 - c) for c in ideal], [norm.cdf(d50 / 2 - c) for c in ideal], ls="none",
                    marker=mk, ms=7, mfc="white", mec=col, mew=1.5, label=f"{lab}: ideal at 10% / 90%", zorder=3)
        ax.plot([0, 1], [0, 1], color=GRID, lw=1)
        ax.set(xlim=(0, 0.75), ylim=(0.25, 1.0), aspect="equal")
        ax.set_title(name, loc="left")
        ax.set_xlabel("false-alarm rate")
        ax.grid(color=GRID, lw=0.6)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("hit rate")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=8.5, bbox_to_anchor=(0.5, 0.005))
    fig.suptitle("Stated base rate 10% → 50% → 90%: observed operating points (filled) vs ideal observer (hollow)",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.tight_layout(rect=(0, 0.1, 1, 0.93))
    fig.subplots_adjust(bottom=0.2)  # aspect="equal" panels ignore the rect; keep the legend clear of the x labels
    fig.savefig(path, dpi=200)
    plt.close(fig)


def strictness(res, path):
    framings = ["presuppose", "find_bugs", "harsh", "persona", "lenient", "stakes_miss", "stakes_fa"]
    fig, axes = plt.subplots(1, 4, figsize=(13, 4.2), sharey=True, sharex=True)
    for ax, (m, name) in zip(axes, MODELS):
        for j, (suf, lab, col, mk, filled) in enumerate(MAIN):
            r = get(res, m, suf)
            if r is None:
                continue
            ys = [i + (j - 0.5) * 0.3 for i, fr in enumerate(framings) if fr in r["by"]]
            xs = [r["by"][fr]["c_minus_neutral"] for fr in framings if fr in r["by"]]
            ci = [r["by"][fr]["c_minus_neutral_ci"] for fr in framings if fr in r["by"]]
            ax.errorbar(xs, ys, xerr=[[x - c[0] for x, c in zip(xs, ci)], [c[1] - x for x, c in zip(xs, ci)]],
                        label=lab, **marker_kw(col, mk, filled, ms=6))
        ax.axvline(0, color=MUTED, lw=0.8)
        ax.axhspan(4.5, 6.5, color=GRID, alpha=0.45, lw=0)  # the two stakes lines: the ones with a right direction
        ax.set_title(name, loc="left")
        ax.grid(axis="x", color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.set_xlabel("c − c(neutral)")
    axes[0].set_yticks(range(len(framings)), [FRAMING_LABELS[f] for f in framings])
    axes[0].invert_yaxis()
    axes[0].set_xlim(-1.25, 1.05)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, fontsize=8.5, bbox_to_anchor=(0.5, 0.005))
    fig.suptitle("One-line framings vs no instruction (← more flag-happy · more lenient →). Shaded: stated costs, "
                 "which should move the threshold in opposite directions.", x=0.01, ha="left", fontsize=10.5,
                 fontweight="bold")
    fig.tight_layout(rect=(0, 0.07, 1, 0.93))
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main():
    d = Path(sys.argv[1] if len(sys.argv) > 1 else "results/torch")
    res = load(d)
    summary(res, d / "thinking_summary.png")
    criterion(res, d / "thinking_criterion.png")
    roc(res, d / "thinking_roc.png")
    strictness(res, d / "thinking_strictness.png")
    print("wrote", ", ".join(f"thinking_{n}.png" for n in ("summary", "criterion", "roc", "strictness")), "to", d)


if __name__ == "__main__":
    main()
