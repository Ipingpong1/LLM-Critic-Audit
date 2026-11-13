"""Stage A ceiling check: is Claude Sonnet 5.5 at ceiling on the original items, and do the hard items fix it?

    .venv/bin/python scripts/plot_ceiling.py

Reads results/frontier/{easy,hard}_sonnet-5.5-{nothink,think}.jsonl (neutral condition, 40 items each:
10 per split x class) and, for comparison on the same 40 easy items, the Torch open-model runs in
results/torch/. Writes results/frontier/ceiling_check.png and ceiling_summary.md.
Decision rule (set before the run): the hard set is usable if Sonnet makes at least ~10% misses and
~10% false alarms, so that a criterion shift can show up on both sides.
"""
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, rankdata

ROOT = Path(__file__).resolve().parent.parent
FR = ROOT / "results" / "frontier"
OFF, ON, REF = "#2a78d6", "#eb6834", "#9aa3b2"
INK, MUTED, GRID = "#1b2230", "#5a6476", "#dde1e8"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "text.color": INK, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "legend.frameon": False,
                     "axes.spines.top": False, "axes.spines.right": False})
RNG = np.random.default_rng(0)
N_BOOT = 4000


def load(path, ids=None):
    rows = [json.loads(l) for l in open(path)]
    # Unparsed replies are dropped, as in pilot/analyze.py (rates are over parsed verdicts).
    rows = [r for r in rows if r["condition"] == "neutral" and not r.get("retryable") and r["verdict"] is not None]
    if ids is not None:
        rows = [r for r in rows if r["item_id"] in ids]
    return sorted(rows, key=lambda r: r["item_id"])


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, mid - half, mid + half


def dprime(fl_err, co_err):
    """Log-linear corrected d' from arrays of 0/1 'said error' for flawed and correct items."""
    H = (fl_err.sum(-1) + 0.5) / (fl_err.shape[-1] + 1)
    F = (co_err.sum(-1) + 0.5) / (co_err.shape[-1] + 1)
    return norm.ppf(H) - norm.ppf(F)


def dprime_ci(rows):
    fl = np.array([r["verdict"] == "error" for r in rows if r["has_error"]], float)
    co = np.array([r["verdict"] == "error" for r in rows if not r["has_error"]], float)
    d = dprime(fl, co)
    bf = fl[RNG.integers(0, len(fl), (N_BOOT, len(fl)))]
    bc = co[RNG.integers(0, len(co), (N_BOOT, len(co)))]
    lo, hi = np.percentile(dprime(bf, bc), [2.5, 97.5])
    return d, lo, hi


def auc(rows):
    s = np.array([r["p_error"] for r in rows if r["has_error"] and r["p_error"] is not None], float)
    n = np.array([r["p_error"] for r in rows if not r["has_error"] and r["p_error"] is not None], float)
    rk = rankdata(np.concatenate([s, n]))
    return (rk[: len(s)].sum() - len(s) * (len(s) + 1) / 2) / (len(s) * len(n))


def counts(rows):
    fl = [r for r in rows if r["has_error"]]
    co = [r for r in rows if not r["has_error"]]
    return (sum(r["verdict"] == "correct" for r in fl), len(fl),
            sum(r["verdict"] == "error" for r in co), len(co))


def main():
    sonnet = {(s, m): load(FR / f"{s}_sonnet-5.5-{m}.jsonl") for s in ("easy", "hard") for m in ("nothink", "think")}
    easy_ids = {json.loads(l)["id"] for l in open(ROOT / "data" / "items_a40.jsonl")}
    open_models = [("qwen3.5_4b", "qwen\n4b"), ("qwen3.5_9b", "qwen\n9b"), ("qwen3.5_27b", "qwen\n27b"),
                   ("gemma4_12b", "gemma\n12b")]
    torch = {(m, k): load(ROOT / "results" / "torch" / f"{m}-{suf}.jsonl", easy_ids)
             for m, _ in open_models for k, suf in (("nothink", "nothink-bf16-t1"), ("think", "think-bf16-t1"))}
    items = {json.loads(l)["id"]: json.loads(l) for f in ("items_a40.jsonl", "items_hard_a40.jsonl")
             for l in open(ROOT / "data" / f)}

    fig = plt.figure(figsize=(12.5, 8.2))
    gs = fig.add_gridspec(2, 4, width_ratios=[1, 1, 2.3, 0.05], height_ratios=[1, 1], hspace=0.55, wspace=0.42)
    ax_m, ax_f, ax_d = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2])
    ax_p, ax_t = fig.add_subplot(gs[1, 0:2]), fig.add_subplot(gs[1, 2])

    # (a, b) miss and false-alarm rates, easy vs hard, thinking off vs on
    for ax, which, title in ((ax_m, "miss", "a  Miss rate (flawed items)"), (ax_f, "fa", "b  False-alarm rate (correct items)")):
        ax.axhspan(0, 0.10, color=GRID, alpha=0.45, lw=0)
        ax.axhline(0.10, color=MUTED, ls="--", lw=1)
        ax.text(-0.5, 0.107, "10% bar", color=MUTED, fontsize=7.5, ha="left", va="bottom")
        for j, (m, col, mk, lab) in enumerate((("nothink", OFF, "o", "thinking off"), ("think", ON, "D", "thinking on"))):
            for i, s in enumerate(("easy", "hard")):
                mi, nf, fa, nc = counts(sonnet[s, m])
                k, n = (mi, nf) if which == "miss" else (fa, nc)
                p, lo, hi = wilson(k, n)
                x = i + (j - 0.5) * 0.34
                ax.errorbar(x, p, yerr=[[p - lo], [hi - p]], marker=mk, ms=7, color=col, mfc=col, mec="white",
                            mew=1, ls="none", capsize=3, elinewidth=1.2, label=lab if i == 0 else None, zorder=3)
                ax.text(x + (0.09 if j else -0.09), p, f"{k}/{n}", fontsize=7.5, color=INK, va="center",
                        ha="left" if j else "right")
        ax.set_xticks([0, 1], ["easy\n(GSM8K,\nMATH)", "hard\n(Olympiad,\nOmni-MATH)"])
        ax.set_xlim(-0.6, 1.6)
        ax.set_ylim(0, 0.45)
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1, decimals=0))
        ax.grid(axis="y", color=GRID, lw=0.6)
        ax.set_title(title)
    ax_m.legend(loc="upper left", fontsize=8, handletextpad=0.3)

    # (c) d' on the same 40 items: open models (Torch, T = 1) vs Sonnet 5.5
    ceiling = dprime(np.ones(20), np.zeros(20))
    ax_d.axhline(ceiling, color=MUTED, ls=":", lw=1)
    ax_d.text(5.45, ceiling + 0.06, f"max measurable with 20 + 20 items ({ceiling:.2f})", color=MUTED,
              fontsize=7.5, ha="right", va="bottom")
    groups = [(lab, torch[m, "nothink"], torch[m, "think"]) for m, lab in open_models]
    groups += [("easy set", sonnet["easy", "nothink"], sonnet["easy", "think"]),
               ("hard set", sonnet["hard", "nothink"], sonnet["hard", "think"])]
    for i, (lab, r_off, r_on) in enumerate(groups):
        for rows, col, mk, dx in ((r_off, OFF, "o", -0.14), (r_on, ON, "D", 0.14)):
            d, lo, hi = dprime_ci(rows)
            ax_d.errorbar(i + dx, d, yerr=[[d - lo], [hi - d]], marker=mk, ms=7, color=col, mfc=col, mec="white",
                          mew=1, ls="none", capsize=3, elinewidth=1.2, zorder=3)
    ax_d.axvline(3.5, color=MUTED, lw=0.8)
    ax_d.text(1.5, 0.15, "open models (Torch)", color=MUTED, fontsize=7.5, ha="center")
    ax_d.text(4.5, 0.15, "Claude Sonnet 5.5", color=MUTED, fontsize=7.5, ha="center")
    ax_d.set_xticks(range(len(groups)), [g[0] for g in groups])
    ax_d.set_xlim(-0.6, 5.6)
    ax_d.set_ylim(0, 4.6)
    ax_d.set_ylabel("d′ (95% CI over items)")
    ax_d.grid(axis="y", color=GRID, lw=0.6)
    ax_d.set_title("c  Discrimination on 40 items (open models: easy set, T = 1)")
    ax_d.text(0.0, -0.22, "Open models: the same 40 easy items, from the Torch runs. No open-model runs on the hard set yet.",
              transform=ax_d.transAxes, fontsize=7.5, color=MUTED)

    # (d) verbalized p_error by true class, hard set
    ax_p.axhline(50, color=MUTED, ls="--", lw=0.8)
    for k, (m, col, mk) in enumerate((("nothink", OFF, "o"), ("think", ON, "D"))):
        for c, flawed in enumerate((False, True)):
            rows = [r for r in sonnet["hard", m] if r["has_error"] == flawed]
            ys = np.array([r["p_error"] for r in rows], float)
            wrong = np.array([(r["verdict"] == "error") != flawed for r in rows])
            xs = c * 2.4 + k * 0.9 + RNG.uniform(-0.28, 0.28, len(ys))
            ax_p.scatter(xs[~wrong], ys[~wrong], s=22, marker=mk, color=col, alpha=0.75, edgecolors="white",
                         linewidths=0.5, zorder=3)
            ax_p.scatter(xs[wrong], ys[wrong], s=60, marker=mk, facecolors="white", edgecolors=INK,
                         linewidths=1.3, zorder=4)
            for x, y, r in zip(xs[wrong], ys[wrong], [r for r, w in zip(rows, wrong) if w]):
                if m == "think":
                    ax_p.annotate(r["item_id"].replace("olympiadbench", "olymp"), (x, y), xytext=(8, 0),
                                  textcoords="offset points", fontsize=7, color=INK, va="center")
    ax_p.set_xticks([0, 0.9, 2.4, 3.3], ["off", "on", "off", "on"])
    ax_p.set_xlim(-0.6, 4.3)
    for x, lab in ((0.45, "correct solutions (n = 20)"), (2.85, "flawed solutions (n = 20)")):
        ax_p.text(x, -24, lab, ha="center", fontsize=8.5, color=INK)
    ax_p.set_ylim(-5, 105)
    ax_p.set_ylabel("stated P(error), %")
    ax_p.grid(axis="y", color=GRID, lw=0.6)
    ax_p.scatter([], [], s=60, marker="o", facecolors="white", edgecolors=INK, linewidths=1.3, label="wrong verdict\n(the same 4 items off and on)")
    ax_p.legend(loc="center", bbox_to_anchor=(0.5, 0.33), fontsize=8)
    ax_p.set_title("d  Hard set: Sonnet's stated P(error) by true class")

    # (e) output tokens per item, thinking off vs on (both sets)
    for s, mk, lab in (("easy", "o", "easy set"), ("hard", "^", "hard set")):
        off = {r["item_id"]: r for r in sonnet[s, "nothink"]}
        on = {r["item_id"]: r for r in sonnet[s, "think"]}
        ids = sorted(off.keys() & on.keys())
        x = np.array([off[i]["completion_tokens"] for i in ids], float)
        y = np.array([on[i]["completion_tokens"] for i in ids], float)
        thought = np.array([bool(on[i].get("reasoning")) for i in ids])
        ax_t.scatter(x[thought], y[thought], marker=mk, s=30, color=ON, edgecolors="white", linewidths=0.5,
                     label=f"{lab}, thinking block returned", zorder=3)
        ax_t.scatter(x[~thought], y[~thought], marker=mk, s=30, facecolors="white", edgecolors=MUTED,
                     linewidths=1, label=f"{lab}, no thinking block", zorder=3)
    lim = (40, 1500)
    ax_t.plot(lim, lim, color=MUTED, lw=0.8, ls="--", label="same length on and off")
    ax_t.set_xscale("log"); ax_t.set_yscale("log")
    ax_t.set_xlim(lim); ax_t.set_ylim(lim)
    ax_t.set_xlabel("output tokens, thinking off (visible text only)")
    ax_t.set_ylabel("output tokens, thinking on\n(thinking + answer)")
    ax_t.grid(color=GRID, lw=0.6)
    ax_t.legend(loc="lower right", fontsize=7.5, ncol=1)
    ax_t.set_title("e  Output tokens per item: thinking on vs off")

    fig.suptitle("Stage A ceiling check: Claude Sonnet 5.5 as a critic, neutral prompt, 40 items per set",
                 x=0.06, ha="left", fontsize=12, fontweight="bold", y=0.985)
    fig.text(0.06, 0.935, "Each item judged once per setting (API-default sampling). Thinking off = between_tools; "
             "thinking on = adaptive, default effort. Total cost $0.73.", fontsize=8.5, color=MUTED)
    fig.subplots_adjust(left=0.06, right=0.98, top=0.86, bottom=0.08)
    out = FR / "ceiling_check.png"
    fig.savefig(out, dpi=170)
    print(f"wrote {out.relative_to(ROOT)}")

    # Summary table
    lines = ["# Stage A ceiling check: Claude Sonnet 5.5", "",
             "Neutral prompt, 40 items per set (10 per split x class), one sample each. "
             "Decision rule: hard set usable if misses and false alarms are each about 10% or more.", "",
             "| set | thinking | misses | false alarms | d′ [95% CI] | AUC (p_error) | trials with thinking block | median output tokens | cost |",
             "|---|---|---|---|---|---|---|---|---|"]
    for s in ("easy", "hard"):
        for m in ("nothink", "think"):
            rows = sonnet[s, m]
            mi, nf, fa, nc = counts(rows)
            d, lo, hi = dprime_ci(rows)
            toks = sorted(r["completion_tokens"] for r in rows)
            lines.append(f"| {s} | {'on' if m == 'think' else 'off'} | {mi}/{nf} | {fa}/{nc} | {d:.2f} [{lo:.2f}, {hi:.2f}] | "
                         f"{auc(rows):.3f} | {sum(bool(r.get('reasoning')) for r in rows)}/{len(rows)} | "
                         f"{toks[len(toks) // 2]} | ${sum(r['cost_usd'] for r in rows):.3f} |")
    lines += ["", "Open models on the same 40 easy items (Torch, neutral, T = 1):", "",
              "| model | thinking | misses | false alarms | d′ [95% CI] |", "|---|---|---|---|---|"]
    for m, lab in open_models:
        for k in ("nothink", "think"):
            rows = torch[m, k]
            mi, nf, fa, nc = counts(rows)
            d, lo, hi = dprime_ci(rows)
            lines.append(f"| {lab.replace(chr(10), ' ')} | {'on' if k == 'think' else 'off'} | {mi}/{nf} | {fa}/{nc} | "
                         f"{d:.2f} [{lo:.2f}, {hi:.2f}] |")
    lines += ["", "Sonnet's wrong verdicts on the hard set (the same four items in both settings):", ""]
    for r in sonnet["hard", "nothink"]:
        if (r["verdict"] == "error") != r["has_error"]:
            it = items[r["item_id"]]
            on = next(x for x in sonnet["hard", "think"] if x["item_id"] == r["item_id"])
            lines.append(f"- {'miss' if r['has_error'] else 'false alarm'} `{r['item_id']}`: p_error {r['p_error']} off / "
                         f"{on['p_error']} on; first error step {it['first_error_step']}; final answer correct: "
                         f"{it['final_answer_correct']}")
    (FR / "ceiling_summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
