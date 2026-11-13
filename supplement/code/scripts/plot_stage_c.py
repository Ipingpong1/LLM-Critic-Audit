"""Stage C figure: the Claude ladder (Haiku 5.5, Sonnet 5.5, Opus 5.5) on the 200 hard items.

    STEP=9 scripts/stage_c.sh                    # first: results/frontier/stage_c/analysis/summary.json
    .venv/bin/python scripts/plot_stage_c.py     # then: results/frontier/stage_c/analysis/stage_c.png

Panels: (a) how far each critic moves its threshold between "10%" and "90%", against the
equal-variance ideal (rho) and against its own stated confidence (rho_Bayes); (b) rho against the
share of items where the critic's confidence leaves room for a stated rate to matter; (c) the Bayes
check counts; (d) tone framings; (e) the other arms; (f) d' and output length.
"""
import argparse
import json
import statistics
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pilot.prompts import ARM_LABELS  # noqa: E402

COL = {"Haiku": "#eb6834", "Sonnet": "#2a78d6", "Opus": "#6250d6"}
INK, MUTED, GRID = "#1b2230", "#5a6476", "#dde1e8"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "text.color": INK, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "legend.frameon": False,
                     "axes.spines.top": False, "axes.spines.right": False})
# (label, model, setting), in ladder order: thinking off, thinking on at matched effort, max effort.
ORDER = [("haiku-5.5-nothink", "Haiku", "off"), ("sonnet-5.5-nothink", "Sonnet", "off"),
         ("haiku-5.5-think", "Haiku", "high"), ("sonnet-5.5-think", "Sonnet", "high"),
         ("opus-5.5-think", "Opus", "high"), ("sonnet-5.5-think-max", "Sonnet", "max")]
SETTING_NAME = {"off": "thinking off", "high": "thinking on (high)", "max": "max effort"}
MARK = {"off": "o", "high": "s", "max": "^"}


def place_labels(ax, pts, fig):
    """Label points without overlaps: try a few offsets per point, keep the first that collides with nothing."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    taken = [ax.transData.transform(xy) for xy, _ in pts]
    taken = [(x - 6, y - 6, x + 6, y + 6) for x, y in taken]
    for (x, y), text in pts:
        for dx, dy, ha in ((7, 4, "left"), (7, -11, "left"), (-7, 4, "right"), (-7, -11, "right"),
                           (7, 14, "left"), (-7, 14, "right"), (7, -21, "left"), (-7, -21, "right")):
            t = ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, fontsize=7.5, color=INK)
            bb = t.get_window_extent(r)
            box = (bb.x0, bb.y0, bb.x1, bb.y1)
            if not any(box[0] < o[2] and o[0] < box[2] and box[1] < o[3] and o[1] < box[3] for o in taken):
                taken.append(box)
                break
            t.remove()
        else:
            ax.annotate(text, (x, y), xytext=(7, 4), textcoords="offset points", fontsize=7.5, color=INK)


def errbar(ax, x, y, ci, col, filled=True, horizontal=False, ms=7, mk="o"):
    if y is None or not np.isfinite(y):
        return
    lo, hi = (ci if ci and ci[0] is not None else (y, y))
    err = [[max(0, y - lo)], [max(0, hi - y)]]
    kw = dict(marker=mk, ms=ms, color=col, mfc=col if filled else "white", mec=col if not filled else "white",
              mew=1.4 if not filled else 1, ls="none", capsize=3, elinewidth=1.2, zorder=3)
    if horizontal:
        ax.errorbar(y, x, xerr=err, **kw)
    else:
        ax.errorbar(x, y, yerr=err, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(ROOT / "results" / "frontier" / "stage_c"))
    ap.add_argument("--title-note", default="")
    args = ap.parse_args()
    d = Path(args.dir)
    summ = {m["model"]: m for m in json.load(open(d / "analysis" / "summary.json"))}
    for m in summ.values():
        m["by"] = {c["condition"]: c for c in m["conditions"]}
    order = [(lab, mod, st) for lab, mod, st in ORDER if lab in summ]
    toks, thought = {}, {}
    for lab, *_ in order:
        f = d / f"{lab}.jsonl"
        rows = [json.loads(l) for l in f.open()] if f.exists() else []
        t = [r["completion_tokens"] for r in rows if r.get("completion_tokens") is not None]
        toks[lab] = statistics.median(t) if t else None
        thought[lab] = 100 * sum(bool(r.get("reasoning")) for r in rows) / len(rows) if rows else None
    spent = sum(json.loads(l)["usd"] for l in (ROOT / "results" / "api_spend.jsonl").open())

    fig = plt.figure(figsize=(14, 9.8))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.25, 0.95, 1.0], hspace=0.62, wspace=0.42)
    ax_a, ax_b, ax_c = (fig.add_subplot(gs[0, k]) for k in range(3))
    ax_d, ax_e, ax_f = (fig.add_subplot(gs[1, k]) for k in range(3))

    # x positions with gaps between the three settings
    xs, x, prev = {}, 0.0, None
    for lab, mod, st in order:
        if prev is not None and st != prev:
            x += 0.6
        xs[lab] = x
        x += 1.0
        prev = st
    ticks = [xs[lab] for lab, *_ in order]
    ticklabels = [f"{mod}\n{st}" for lab, mod, st in order]

    # (a) rho and rho_Bayes
    ax_a.axhline(1, color=MUTED, ls="--", lw=1)
    ax_a.text(0.99, 1.02, "moves as far as the benchmark says", ha="right", va="bottom", fontsize=7.5, color=MUTED,
              transform=ax_a.get_yaxis_transform())
    ax_a.axhspan(-0.45, 0, color="#f3f4f7", zorder=0)
    for lab, mod, st in order:
        m = summ[lab]
        errbar(ax_a, xs[lab] - 0.15, m.get("rho"), m.get("rho_ci"), COL[mod], filled=True, mk=MARK[st])
        b = m.get("bayes") or {}
        errbar(ax_a, xs[lab] + 0.15, b.get("rho_bayes"), b.get("rho_bayes_ci"), COL[mod], filled=False, mk=MARK[st])
    groups = {}
    for lab, mod, st in order:
        groups.setdefault(st, []).append(xs[lab])
    ax_a.set_xticks(ticks, ticklabels, fontsize=8)
    ax_a.set_xlim(ticks[0] - 0.6, ticks[-1] + 0.6)
    ax_a.set_ylim(-0.45, 1.75)
    ax_a.set_yticks([0, 0.25, 0.5, 0.75, 1.0, 1.25])
    ax_a.set_ylabel("observed shift ÷ benchmark shift")
    ax_a.grid(axis="y", color=GRID, lw=0.6)
    ax_a.legend(handles=[Line2D([], [], marker="o", color=MUTED, ls="none", ms=7, label="filled: ρ, vs the equal-variance ideal"),
                         Line2D([], [], marker="o", color=MUTED, mfc="white", ls="none", ms=7, mew=1.4,
                                label="open: ρ_Bayes, vs its own stated confidence")],
                loc="upper left", fontsize=7.5, ncol=1, borderaxespad=0.2)
    ax_a.set_title("a  How far the threshold moves from \"10%\" to \"90%\"")

    # (b) rho vs share of items where a stated rate can flip a Bayesian
    pts_b = []
    for lab, mod, st in order:
        m = summ[lab]
        b = m.get("bayes") or {}
        if b.get("share_flippable") is None or m.get("rho") is None:
            continue
        ax_b.plot(100 * b["share_flippable"], m["rho"], marker=MARK[st], ms=8, color=COL[mod], mec="white", ls="none", zorder=3)
        pts_b.append(((100 * b["share_flippable"], m["rho"]), f"{mod} {st}"))
    ax_b.axhline(0, color=MUTED, lw=0.8)
    if pts_b:
        xmax = max(x for (x, _), _ in pts_b)
        ymin, ymax = min(y for (_, y), _ in pts_b), max(y for (_, y), _ in pts_b)
        ax_b.set_xlim(0, max(20, xmax * 1.35))
        ax_b.set_ylim(min(-0.1, ymin - 0.1), max(0.5, ymax + 0.15))
    ax_b.set_xlabel("items with 10 < stated P(error) ≤ 90 at \"50%\" (%)")
    ax_b.set_ylabel("ρ (equal-variance)")
    ax_b.grid(color=GRID, lw=0.6)
    ax_b.set_title("b  Is it confidence?")

    # (c) Bayes check counts: share of the predicted changes the critic made
    rows_c = [(lab, mod, st) for lab, mod, st in order if summ[lab].get("bayes")]
    yy = np.arange(len(rows_c))[::-1]
    for y, (lab, mod, st) in zip(yy, rows_c):
        b = summ[lab]["bayes"]
        for dy, done, pred, extra, alpha in ((0.18, b["clear_predicted_done"], b["clear_predicted"], b["clear_unpredicted"], 1.0),
                                             (-0.18, b["flag_predicted_done"], b["flag_predicted"], b["flag_unpredicted"], 0.45)):
            frac = done / pred if pred else 0
            ax_c.barh(y + dy, frac, 0.32, color=COL[mod], alpha=alpha, zorder=2)
            ax_c.text(max(frac, 0) + 0.02, y + dy, f"{done}/{pred}" + (f" (+{extra})" if extra else ""),
                      va="center", fontsize=7, color=INK)
    ax_c.set_yticks(yy, [f"{mod} {st}" for _, mod, st in rows_c], fontsize=8)
    ax_c.set_xlim(0, 1.3)
    ax_c.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax_c.axvline(1, color=MUTED, ls="--", lw=1)
    ax_c.set_xlabel("share of a Bayesian's changes the critic made\n(+n: changes a Bayesian would not make)")
    ax_c.grid(axis="x", color=GRID, lw=0.6)
    ax_c.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=MUTED), plt.Rectangle((0, 0), 1, 1, color=MUTED, alpha=0.45)],
                labels=["told 10%: flags dropped", "told 90%: flags added"], loc="upper center",
                bbox_to_anchor=(0.45, -0.3), ncol=2, fontsize=7.5)
    ax_c.set_title("c  Bayes check: changes made / predicted")

    # (d) tone
    frames = [("presuppose", '"contains\nan error"'), ("lenient", '"be\nlenient"')]
    for k, (cond, name) in enumerate(frames):
        for j, (lab, mod, st) in enumerate(order):
            c = summ[lab]["by"].get(cond)
            if not c:
                continue
            y = len(frames) - 1 - k + (len(order) - 1 - j) * 0.13 - 0.33
            errbar(ax_d, y, c["c_minus_neutral"], c["c_minus_neutral_ci"], COL[mod], horizontal=True, ms=6, mk=MARK[st])
    ax_d.axvline(0, color=INK, lw=0.8)
    ax_d.set_yticks(range(len(frames))[::-1], [n for _, n in frames], fontsize=8)
    ax_d.set_ylim(-0.6, len(frames) - 0.4)
    ax_d.set_xlabel("c − c(neutral)   ← flags more · flags less →")
    ax_d.grid(axis="x", color=GRID, lw=0.6)
    ax_d.set_title("d  Tone: threshold shift from neutral")

    # (e) the other arms, for the critics that ran all 18 conditions
    arms = ["base_rate", "use", "payoff", "labels"]
    full = [(lab, mod, st) for lab, mod, st in order if all(a in summ[lab]["arms"] for a in arms)]
    w = 0.8 / max(1, len(full))
    for j, (lab, mod, st) in enumerate(full):
        for k, arm in enumerate(arms):
            a = summ[lab]["arms"][arm]
            errbar(ax_e, k + (j - (len(full) - 1) / 2) * w, a["rho"], a["rho_ci"], COL[mod], ms=6, mk=MARK[st])
    ax_e.axhline(0, color=MUTED, lw=0.8)
    ax_e.set_xticks(range(len(arms)), ["stated\nbase rate", "+ use it\nas prior", "stated\npayoffs", "label\nswap"], fontsize=8)
    ax_e.set_ylabel("ρ (equal-variance)")
    ax_e.grid(axis="y", color=GRID, lw=0.6)
    ax_e.set_title("e  Other ways of stating the prior")
    ax_e.text(0.0, -0.3, "critics that ran all 18 conditions: " + ", ".join(f"{mod} {st}" for _, mod, st in full),
              transform=ax_e.transAxes, fontsize=7.5, color=MUTED)

    # (f) d' at 50% and median output tokens
    for lab, mod, st in order:
        c = summ[lab]["by"]["br50"]
        errbar(ax_f, xs[lab], c["d_prime"], c["d_prime_ci"], COL[mod], mk=MARK[st])
        if toks[lab]:
            ax_f.text(xs[lab], 0.12, f"{toks[lab]:.0f}", ha="center", fontsize=7, color=MUTED)
        if thought[lab] is not None:
            ax_f.text(xs[lab], 0.66, f"{thought[lab]:.0f}%" if thought[lab] else "–", ha="center", fontsize=7, color=MUTED)
    ax_f.text(ticks[0] - 0.55, 0.36, "median output tokens per reply:", fontsize=7, color=MUTED)
    ax_f.text(ticks[0] - 0.55, 0.90, "replies with a thinking summary:", fontsize=7, color=MUTED)
    ax_f.set_xticks(ticks, [f"{mod}\n{st}" for _, mod, st in order], fontsize=8)
    ax_f.set_xlim(ticks[0] - 0.6, ticks[-1] + 0.6)
    ax_f.set_ylim(0, max(4.2, max(summ[l]["by"]["br50"]["d_prime_ci"][1] or 0 for l, *_ in order) + 0.3))
    ax_f.set_ylabel("d′ when told \"50%\"")
    ax_f.grid(axis="y", color=GRID, lw=0.6)
    ax_f.set_title("f  Accuracy on the 200 hard items")

    fig.suptitle("Stage C: the Claude ladder on 200 hard ProcessBench items" + args.title_note,
                 x=0.05, y=0.985, ha="left", fontsize=14, fontweight="bold")
    fig.text(0.05, 0.935,
             "One call per item and condition, API-default sampling, paired item bootstrap (95% CIs). Thinking on = adaptive "
             "thinking at effort \"high\" for every model; max = Sonnet at effort \"max\".\nρ_Bayes reads the stated P(error) at "
             "\"50%\" as the critic's posterior and asks how far its verdicts should move when told 10% or 90%. "
             f"Total API spend so far: ${spent:.2f}.", fontsize=8.3, color=MUTED)
    handles = [Line2D([], [], marker="s", color=COL[m], ls="none", ms=8, label=f"{m} 5.5") for m in COL] + \
              [Line2D([], [], marker=MARK[st], color=MUTED, ls="none", ms=7, label=SETTING_NAME[st]) for st in MARK]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.05, 0.905), ncol=6, fontsize=8.5,
               handletextpad=0.3, columnspacing=1.6)
    fig.subplots_adjust(left=0.07, right=0.98, top=0.84, bottom=0.09)
    if pts_b:
        place_labels(ax_b, pts_b, fig)
    out = d / "analysis" / "stage_c.png"
    fig.savefig(out, dpi=170)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
