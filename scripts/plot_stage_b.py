"""Stage B figure: Claude Sonnet 5.5 on the 40 hard items under every Stage B condition.

    STEP=4 scripts/stage_b.sh                    # first: writes results/frontier/stage_b/summary.json
    .venv/bin/python scripts/plot_stage_b.py     # then: results/frontier/stage_b/stage_b.png

Panels: (a) prior-use ratio rho per manipulation, with the open models' values on the easy set for
reference; (b) threshold shift from neutral for the tone framings; (c) the verdict on every item in
every condition; (d) verdict changes a Bayesian would make from Sonnet's own stated confidence vs the
changes it made (exploratory); (e) the max-effort probe.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pilot.prompts import CONDITION_SETS  # noqa: E402

FR = ROOT / "results" / "frontier"
OUT = FR / "stage_b"
OFF, ON, MAX, REF = "#2a78d6", "#eb6834", "#6250d6", "#9aa3b2"
INK, MUTED, GRID, WRONG = "#1b2230", "#5a6476", "#dde1e8", "#c2410c"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "text.color": INK, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "legend.frameon": False,
                     "axes.spines.top": False, "axes.spines.right": False})
SETTINGS = [("sonnet-5.5-nothink", "thinking off", OFF, "o"), ("sonnet-5.5-think", "thinking on", ON, "D")]
COND_SHORT = {"neutral": "neutral", "br10": "10%", "br50": "50%", "br90": "90%", "br10_use": "10% +use",
              "br90_use": "90% +use", "pay_fa9": "FA costs 9", "pay_miss9": "miss costs 9",
              "presuppose": '"has error"', "lenient": "lenient", "lab_neutral": "swap: neutral",
              "lab_br10": "swap: 10%", "lab_br90": "swap: 90%"}


def load_rows(label):
    d = defaultdict(dict)
    name = {"sonnet-5.5-nothink": "nothink", "sonnet-5.5-think": "think", "sonnet-5.5-think-max": "think-max"}[label]
    for l in open(FR / f"hard_sonnet-5.5-{name}.jsonl"):
        r = json.loads(l)
        d[r["condition"]][r["item_id"]] = r
    return d


def errbar(ax, x, y, ci, col, mk, horizontal=False, **kw):
    lo, hi = y - ci[0], ci[1] - y
    if horizontal:
        ax.errorbar(y, x, xerr=[[lo], [hi]], marker=mk, ms=7, color=col, mfc=col, mec="white", mew=1, ls="none",
                    capsize=3, elinewidth=1.2, zorder=3, **kw)
    else:
        ax.errorbar(x, y, yerr=[[lo], [hi]], marker=mk, ms=7, color=col, mfc=col, mec="white", mew=1, ls="none",
                    capsize=3, elinewidth=1.2, zorder=3, **kw)


def main():
    summ = {m["model"]: m for m in json.load(open(OUT / "summary.json"))}
    for m in summ.values():
        m["by"] = {c["condition"]: c for c in m["conditions"]}
    torch = {m["model"]: m for m in json.load(open(ROOT / "results" / "torch" / "summary.json")) if m["model"].endswith("-t1")}
    for m in torch.values():
        m["by"] = {c["condition"]: c for c in m["conditions"]}
    rows = {lab: load_rows(lab) for lab, *_ in SETTINGS}
    rows["sonnet-5.5-think-max"] = load_rows("sonnet-5.5-think-max")

    fig = plt.figure(figsize=(13.5, 9.6))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.15, 1.0, 0.95], height_ratios=[1, 1.12], hspace=0.5, wspace=0.42)
    ax_a, ax_b, ax_e = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2])
    gsc = gs[1, 0:2].subgridspec(1, 2, wspace=0.08)
    ax_c1, ax_c2 = fig.add_subplot(gsc[0, 0]), fig.add_subplot(gsc[0, 1])
    ax_d = fig.add_subplot(gs[1, 2])

    # (a) rho per arm
    arms = [("base_rate", "stated\nbase rate"), ("use", "+ use it\nas prior"), ("payoff", "stated\npayoffs"),
            ("labels", "label\nswap")]
    ax_a.axhspan(-0.1, 0, color=GRID, alpha=0.3, lw=0)
    ax_a.axhline(1, color=MUTED, ls="--", lw=1)
    ax_a.text(3.55, 1.02, "ideal observer", color=MUTED, fontsize=7.5, ha="right", va="bottom")
    ax_a.axhline(0, color=MUTED, lw=0.8)
    for i, (arm, _) in enumerate(arms):
        for j, (lab, name, col, mk) in enumerate(SETTINGS):
            a = summ[lab]["arms"].get(arm)
            if a:
                errbar(ax_a, i + (j - 0.5) * 0.3, a["rho"], a["rho_ci"], col, mk, label=name if i == 0 else None)
        if arm in ("base_rate", "payoff"):
            vals = [m["arms"][arm]["rho"] for m in torch.values() if arm in m["arms"]]
            ax_a.scatter(np.full(len(vals), i + 0.36), vals, marker="_", s=90, color=REF, lw=1.6, zorder=2,
                         label="open models, easy set (Torch, T = 1)" if i == 0 else None)
    ax_a.set_xticks(range(len(arms)), [a[1] for a in arms])
    ax_a.set_xlim(-0.55, 3.6)
    ax_a.set_ylim(-0.1, 1.15)
    ax_a.set_ylabel("prior-use ratio ρ (observed ÷ ideal shift)")
    ax_a.grid(axis="y", color=GRID, lw=0.6)
    ax_a.legend(loc="upper left", fontsize=7.5, bbox_to_anchor=(0.02, 0.83))
    ax_a.set_title("a  Information: does the threshold follow the stated rate?")

    # (b) tone framings: c - c(neutral)
    tone = [("presuppose", '"This solution\ncontains an error"'), ("lenient", '"Be a lenient\nreviewer"'),
            ("br50", '"About 50% contain\nan error"'), ("lab_neutral", "label swap,\nno rate")]
    ax_b.axvline(0, color=MUTED, lw=0.8)
    for i, (cond, _) in enumerate(tone):
        for j, (lab, name, col, mk) in enumerate(SETTINGS):
            c = summ[lab]["by"][cond]
            errbar(ax_b, i + (j - 0.5) * 0.3, c["c_minus_neutral"], c["c_minus_neutral_ci"], col, mk, horizontal=True)
        if cond in ("presuppose", "lenient"):
            for mname, m in torch.items():
                v = m["by"][cond]["c_minus_neutral"]
                ax_b.scatter(v, i + 0.36, marker="|", s=90, color=REF, lw=1.6, zorder=2)
                if mname == "qwen3.5:27b-think-bf16-t1" and cond == "presuppose":
                    ax_b.annotate("qwen 27b, thinking", (v, i + 0.36), xytext=(-4, -11), textcoords="offset points",
                                  fontsize=7, color=MUTED, ha="left")
    ax_b.set_yticks(range(len(tone)), [t[1] for t in tone], fontsize=8)
    ax_b.set_ylim(3.55, -0.85)   # inverted: first framing at the top, room above it for the note
    ax_b.set_xlim(-1.0, 0.8)
    ax_b.set_xlabel("c − c(neutral)   ← flags more · flags less →")
    ax_b.grid(axis="x", color=GRID, lw=0.6)
    ax_b.text(0.78, -0.58, "grey ticks: open models,\neasy set (Torch, T = 1)", ha="right", va="center",
              fontsize=7.5, color=MUTED)
    ax_b.set_title("b  Tone: threshold shift from neutral")

    # (c) verdict grid: item x condition, right / wrong / unparsed
    conds = CONDITION_SETS["stage_b"]
    base = rows["sonnet-5.5-nothink"]["br50"]
    ids = sorted(base, key=lambda i: (base[i]["has_error"], base[i]["p_error"] or 0))
    cmap = ListedColormap(["#ffffff", "#e9ecf1", WRONG])
    for ax, (lab, name, col, mk) in zip((ax_c1, ax_c2), SETTINGS):
        g = np.zeros((len(ids), len(conds)))
        for x, c in enumerate(conds):
            for y, i in enumerate(ids):
                r = rows[lab][c].get(i)
                g[y, x] = 0 if r is None or r["verdict"] is None else (2 if (r["verdict"] == "error") != r["has_error"] else 1)
        ax.imshow(g, cmap=cmap, vmin=0, vmax=2, aspect="auto", interpolation="nearest")
        for y in range(len(ids)):
            for x in range(len(conds)):
                if g[y, x] == 0:
                    ax.text(x, y, "×", ha="center", va="center", fontsize=7, color=INK)
        ax.set_xticks(range(len(conds)), [COND_SHORT[c] for c in conds], rotation=60, ha="right", fontsize=7)
        ax.set_xticks(np.arange(-0.5, len(conds)), minor=True)
        ax.set_yticks(np.arange(-0.5, len(ids)), minor=True)
        ax.grid(which="minor", color="white", lw=0.8)
        ax.tick_params(which="minor", length=0)
        n_cor = sum(not base[i]["has_error"] for i in ids)
        ax.axhline(n_cor - 0.5, color=INK, lw=1.2)
        same = sum(len({rows[lab][c][i]["verdict"] for c in conds if rows[lab][c].get(i) and rows[lab][c][i]["verdict"]}) == 1
                   for i in ids)
        ax.set_title(f"{name}: {same}/40 items same verdict throughout", fontsize=9, fontweight="normal", loc="center")
        for s in ax.spines.values():
            s.set_visible(False)
        if ax is ax_c1:
            ax.set_yticks([n_cor / 2 - 0.5, n_cor + (len(ids) - n_cor) / 2 - 0.5], ["correct\nsolutions", "flawed\nsolutions"])
        else:
            ax.set_yticks([])
    ax_c1.text(0, 1.13, "c  Every verdict: 40 items (rows) × 13 conditions (columns)", transform=ax_c1.transAxes,
               fontsize=10, fontweight="bold")
    ax_c2.legend(handles=[Patch(color="#e9ecf1", label="right verdict"), Patch(color=WRONG, label="wrong verdict"),
                          Patch(facecolor="white", edgecolor=MUTED, label="× no answer")],
                 loc="lower right", bbox_to_anchor=(1.0, 1.06), fontsize=7.5, ncol=3)

    # (d) Bayes-consistent with own confidence vs observed (exploratory)
    cats, pred, obs, wrong = [], [], [], []
    for lab, name, col, mk in SETTINGS:
        d = rows[lab]
        for c, p_thr in (("br10", 90), ("br90", 10)):
            p_ids = [i for i in ids if d["br50"][i]["p_error"] is not None]
            if c == "br10":   # flagged at 50% but below 90% confidence: a Bayesian told 10% clears it
                pv = sum(d["br50"][i]["verdict"] == "error" and d["br50"][i]["p_error"] <= p_thr for i in p_ids)
            else:             # passed at 50% but above 10% confidence: a Bayesian told 90% flags it
                pv = sum(d["br50"][i]["verdict"] == "correct" and d["br50"][i]["p_error"] > p_thr for i in p_ids)
            # Observed: changes in the direction the stated rate implies (told 10%: error -> correct;
            # told 90%: correct -> error). Changes the other way are counted separately.
            toward, away = ("error", "correct") if c == "br10" else ("correct", "error")
            ov = sum(d["br50"][i]["verdict"] == toward and d[c][i]["verdict"] == away for i in p_ids)
            ww = sum(d["br50"][i]["verdict"] == away and d[c][i]["verdict"] == toward for i in p_ids)
            cats.append((name, c)); pred.append(pv); obs.append(ov); wrong.append(ww)
    x = np.arange(len(cats))
    ax_d.bar(x - 0.18, pred, 0.34, color="white", edgecolor=INK, lw=1.2, label="a Bayesian using Sonnet's\nown 50%-rate confidence")
    ax_d.bar(x + 0.18, obs, 0.34, color=[OFF if n == "thinking off" else ON for n, _ in cats], label="Sonnet")
    for xi, (p, o) in enumerate(zip(pred, obs)):
        ax_d.text(xi - 0.18, p + 0.08, str(p), ha="center", fontsize=8)
        ax_d.text(xi + 0.18, o + 0.08, str(o), ha="center", fontsize=8)
        if wrong[xi]:
            ax_d.text(xi + 0.04, o + 0.45, f"+{wrong[xi]} the\nother way", ha="left", va="bottom", fontsize=7, color=MUTED)
    ax_d.set_xticks(x, [f"{'off' if n == 'thinking off' else 'on'}\ntold {c[2:]}%" for n, c in cats])
    ax_d.set_ylim(0, 6)
    ax_d.set_ylabel("verdicts changed toward the stated rate\n(vs the 50% condition)")
    ax_d.grid(axis="y", color=GRID, lw=0.6)
    ax_d.legend(loc="upper right", fontsize=7.5)
    ax_d.set_title("d  Bayes check (exploratory)")

    # (e) effort probe: output tokens, default vs max, neutral
    dflt, mx = rows["sonnet-5.5-think"]["neutral"], rows["sonnet-5.5-think-max"]["neutral"]
    pid = sorted(dflt.keys() & mx.keys())
    xs = np.array([dflt[i]["completion_tokens"] for i in pid], float)
    ys = np.array([mx[i]["completion_tokens"] for i in pid], float)
    flawed = np.array([dflt[i]["has_error"] for i in pid])
    changed = sum(dflt[i]["verdict"] != mx[i]["verdict"] for i in pid)
    lim = (80, 20000)
    ax_e.plot(lim, lim, color=MUTED, ls="--", lw=0.8, label="same length")
    ax_e.scatter(xs[~flawed], ys[~flawed], s=26, marker="o", facecolors="white", edgecolors=MAX, lw=1.2, label="correct solution")
    ax_e.scatter(xs[flawed], ys[flawed], s=26, marker="o", color=MAX, edgecolors="white", lw=0.5, label="flawed solution")
    ax_e.set_xscale("log"); ax_e.set_yscale("log"); ax_e.set_xlim(lim); ax_e.set_ylim(lim)
    ax_e.set_xlabel("output tokens, default effort")
    ax_e.set_ylabel("output tokens, max effort")
    ax_e.grid(color=GRID, lw=0.6)
    ax_e.legend(loc="lower right", fontsize=7.5)
    ax_e.text(0.03, 0.97, f"median ×{np.median(ys) / np.median(xs):.1f} tokens\n{changed}/40 verdicts changed\n"
              f"same 4 items wrong", transform=ax_e.transAxes, va="top", fontsize=8, color=INK)
    ax_e.set_title("e  Max-effort thinking (neutral)")

    spent = sum(json.loads(l)["usd"] for l in open(ROOT / "results" / "api_spend.jsonl"))
    fig.suptitle("Stage B: Claude Sonnet 5.5's threshold barely moves (40 hard items, 13 conditions)",
                 x=0.05, ha="left", fontsize=12.5, fontweight="bold", y=0.99)
    fig.text(0.05, 0.94, "One call per item and condition, API-default sampling. ρ and c from pilot/analyze.py "
             "(paired item bootstrap). Panel d: verdicts a Bayesian would change if it took Sonnet's stated P(error) "
             "at the 50% rate as its posterior.\nOpen-model values are on the easy item set, so they are context, "
             f"not a paired comparison. Total API spend so far: ${spent:.2f}.", fontsize=8.3, color=MUTED)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.875, bottom=0.08)
    path = OUT / "stage_b.png"
    fig.savefig(path, dpi=170)
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
