"""Figures and table numbers for the workshop manuscript.

Reads only finished analyses (hard set, premise test, label re-analysis) and the saved replies
for token counts. It does not read results/rate_wording/ (that run is analysed separately,
once every job has finished).

    .venv/bin/python manuscript/figures/make_figures.py

Writes manuscript/figures/fig_numbers_vs_claims.pdf and prints the numbers in Tables 2 and 3 of the paper.
"""
import json
import math
from pathlib import Path
from statistics import median

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42,          # embedded TrueType, no Type 3 fonts
    "font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 6.8,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
})

# The 14 critic runs on the hard set, in display order: thinking off, then on.
RUNS = [
    ("qwen3.5:4b-nothink-bf16-t1", "Qwen3.5-4B", "off"),
    ("qwen3.5:9b-nothink-bf16-t1", "Qwen3.5-9B", "off"),
    ("qwen3.5:27b-nothink-bf16-t1", "Qwen3.5-27B", "off"),
    ("gemma4:12b-nothink-bf16-t1", "Gemma-4-12B", "off"),
    ("haiku-5.5-nothink", "Haiku 5.5", "off"),
    ("sonnet-5.5-nothink", "Sonnet 5.5", "off"),
    ("qwen3.5:4b-think-bf16-t1", "Qwen3.5-4B", "on"),
    ("qwen3.5:9b-think-bf16-t1", "Qwen3.5-9B", "on"),
    ("qwen3.5:27b-think-bf16-t1", "Qwen3.5-27B", "on"),
    ("gemma4:12b-think-bf16-t1", "Gemma-4-12B", "on"),
    ("haiku-5.5-think", "Haiku 5.5", "high"),
    ("sonnet-5.5-think", "Sonnet 5.5", "high"),
    ("sonnet-5.5-think-max", "Sonnet 5.5", "max"),
    ("opus-5.5-think", "Opus 5.5", "high"),
]
REPLIES = {  # saved replies per hard-set run, for token counts
    **{k: ROOT / "results/torch_hard" / (k.replace(":", "_") + ".jsonl") for k, _, _ in RUNS if k.startswith(("qwen", "gemma"))},
    **{k: ROOT / "results/frontier/stage_c" / f"{k}.jsonl" for k, _, _ in RUNS if not k.startswith(("qwen", "gemma"))},
}


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


def raw_rates(path):
    """Uncorrected false-alarm and hit rates per condition over parsed replies, every sample pooled,
    as in the per-critic tables of scripts/premise_analysis.py (summary.json holds log-linear corrected rates)."""
    n = {}
    for line in open(path):
        r = json.loads(line)
        if r.get("verdict") is None:
            continue
        k = (r["condition"], r["has_error"])
        e, t = n.get(k, (0, 0))
        n[k] = (e + (r["verdict"] == "error"), t + 1)
    conds = {c for c, _ in n}
    return {c: {"fa": n[(c, False)][0] / n[(c, False)][1], "hit": n[(c, True)][0] / n[(c, True)][1]} for c in conds}


def p_eff(m, name):
    """Stated error probability at which an ideal observer with this critic's d' (reference condition)
    would place its threshold where the critic did under `name`, starting from an unbiased threshold
    at `neutral`: logit(p) = -(c(name) - c(neutral)) * d'."""
    c = cond(m, name)
    if c is None or c.get("c_minus_neutral") is None:
        return None
    return 1 / (1 + math.exp(c["c_minus_neutral"] * d_ref(m)))


def logit(p):
    return math.log(p / (1 - p))


def fmt(x, nd=2):
    return "--" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{nd}f}".replace("-", "$-$")


def fmt_ci(x, lohi, nd=2):
    if x is None:
        return "--"
    return f"{fmt(x, nd)} [{fmt(lohi[0], nd)}, {fmt(lohi[1], nd)}]"


def main():
    hard = load_summaries("results/torch_hard/analysis/summary.json", "results/frontier/stage_c/analysis/summary.json")
    prem = load_summaries("results/premise/analysis/summary.json")
    lab = json.load(open(ROOT / "results/label_sensitivity/report.json"))
    ranges = lab["assignment_ranges"]["hard"]["critics"]

    # ---------------- Figure 1 ----------------
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.0, 2.75), gridspec_kw={"width_ratios": [1.25, 1.0], "wspace": 0.62})

    # (a) effective probability on the hard set
    ys = list(range(len(RUNS)))[::-1]
    for y, (key, name, think) in zip(ys, RUNS):
        m = hard[key]
        p10, p90, pc = p_eff(m, "br10"), p_eff(m, "br90"), p_eff(m, "presuppose")
        ax.plot([logit(p10), logit(p90)], [y, y], color="0.75", lw=1.6, zorder=1, solid_capstyle="round")
        ax.scatter(logit(p10), y, marker="<", s=22, color="#2b6cb0", zorder=3, label="told 10% flawed" if y == ys[0] else None)
        ax.scatter(logit(p90), y, marker=">", s=22, color="#dd6b20", zorder=3, label="told 90% flawed" if y == ys[0] else None)
        ax.scatter(logit(pc), y, marker="X", s=26, color="#c53030", zorder=4, label="“…contains an error.”" if y == ys[0] else None)
    for p, lab_ in ((0.1, "ideal, told 10%"), (0.9, "ideal, told 90%")):
        ax.axvline(logit(p), color="0.35", ls="--", lw=0.7, zorder=0)
        ax.text(logit(p) - 0.08, -0.45, lab_, ha="right", va="bottom", rotation=90, fontsize=6.0, color="0.3")
    ax.axvline(0, color="0.85", lw=0.6, zorder=0)
    ticks = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]
    ax.set_xticks([logit(t) for t in ticks], [f"{t:g}" for t in ticks])
    ax.set_xlim(logit(0.035), logit(0.995))
    ax.set_ylim(-0.7, len(RUNS) + 1.1)
    ax.set_yticks(ys, [f"{n} ({t})" for _, n, t in RUNS])
    ax.axhline(7.5, color="0.6", lw=0.5, ls=":")
    ax.text(logit(0.037), 7.62, "reasoning off ↑", fontsize=6.0, color="0.35", va="bottom", ha="left")
    ax.text(logit(0.037), 7.38, "reasoning on ↓", fontsize=6.0, color="0.35", va="top", ha="left")
    ax.set_xlabel("effective P(error): the stated rate at which an ideal observer\nwould move its threshold as far as the critic did")
    ax.set_title("(a) Same 200 hard items, 14 critic configurations", loc="left")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=True, framealpha=0.95, edgecolor="0.8",
              handletextpad=0.2, columnspacing=0.8, borderpad=0.35, fontsize=6.2)
    ax.tick_params(axis="y", length=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    # (b) premise test: false alarms per 100 correct solutions
    rows = [("neutral", "no added line"), ("check_only", "“Check this solution carefully.”"),
            ("may_error", "“…may or may not contain an error…”"),
            ("presuppose", "“…contains an error. Check it…”"), ("claim_bare", "“This solution contains an error.”"),
            ("claim_mistake", "“There is a mistake somewhere…”"), ("claim_reviewer", "“A previous reviewer found an error…”"),
            ("claim_random", "same note, “attached at random”"), ("claim_correct", "“This solution is correct…”")]
    crit = [("qwen3.5:27b-think-bf16-t1", "Qwen3.5-27B (on)", "o", "#2f855a"), ("opus-5.5-think", "Opus 5.5 (high)", "s", "#6b46c1")]
    raw = {key: raw_rates(ROOT / "results/premise" / (key.replace(":", "_") + ".jsonl")) for key, *_ in crit}
    yb = list(range(len(rows)))[::-1]
    for key, name, mk, col in crit:
        fa0 = 100 * raw[key]["neutral"]["fa"]
        bx.axvline(fa0, color=col, lw=0.6, ls=":", zorder=0)
        for y, (cn, _) in zip(yb, rows):
            bx.scatter(100 * raw[key][cn]["fa"], y, marker=mk, s=20, color=col, zorder=3,
                       label=name if cn == "neutral" else None, edgecolors="white", linewidths=0.3)
    bx.axhspan(1.5, 5.5, color="0.93", zorder=-1)   # the four claims of an error
    for y0, txt in ((8.4, "no claim"), (5.4, "claims of an error"), (1.4, "discounted / opposite")):
        bx.text(99, y0, txt, fontsize=6.0, color="0.35", ha="right", va="top", style="italic")
    bx.set_yticks(yb, [r for _, r in rows])
    bx.set_xlim(0, 100)
    bx.set_ylim(-0.6, len(rows) - 0.4)
    bx.set_xlabel("false alarms per 100 correct solutions\n(200 held-out items; hits stay at 96–100%)")
    bx.set_title("(b) One sentence (preregistered, held-out items)", loc="left")
    bx.legend(loc="center right", bbox_to_anchor=(1.0, 0.80), frameon=True, framealpha=0.95, edgecolor="0.8",
              handletextpad=0.2, fontsize=6.2)
    bx.tick_params(axis="y", length=0)
    for s in ("top", "right"):
        bx.spines[s].set_visible(False)

    fig.savefig(OUT / "fig_numbers_vs_claims.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(OUT / "fig_numbers_vs_claims.png", bbox_inches="tight", pad_inches=0.02, dpi=220)

    # ---------------- Numbers for the text ----------------
    print("== effective P(error), hard set: told 10% / told 90% / 'contains an error'")
    e10, e90, ec = [], [], []
    for key, name, think in RUNS:
        m = hard[key]
        a, b, c = p_eff(m, "br10"), p_eff(m, "br90"), p_eff(m, "presuppose")
        e10.append(a); e90.append(b); ec.append(c)
        print(f"  {name:12s} {think:5s} {a:.2f} {b:.2f} {c:.2f}")
    print(f"  median told 10%: {median(e10):.2f} (range {min(e10):.2f}-{max(e10):.2f}); told 90%: {median(e90):.2f} "
          f"(range {min(e90):.2f}-{max(e90):.2f}); claim: median {median(ec):.2f} (range {min(ec):.2f}-{max(ec):.2f})")

    print("\n== Table 1 rows (hard set)")
    for key, name, think in RUNS:
        m = hard[key]
        arms = m.get("arms", {})
        rho = arms.get("base_rate", {})
        r = ranges[key]["arms"]["base_rate"]
        pay = arms.get("payoff", {}).get("rho")
        use = arms.get("use", {}).get("rho")
        pre, len_ = cond(m, "presuppose"), cond(m, "lenient")
        toks = [json.loads(l).get("completion_tokens") for l in open(REPLIES[key])]
        toks = [t for t in toks if t is not None]
        print(f"  {name} & {think} & {fmt(d_ref(m))} & {fmt_ci(rho.get('rho'), rho.get('rho_ci', (None, None)))} & "
              f"{fmt(r['min'])}--{fmt(r['max'])} & {fmt(use)} & {fmt(pay)} & {fmt(pre['c_minus_neutral'])} & "
              f"{fmt(len_['c_minus_neutral'])} & {round(median(toks)):,} \\\\   % n_rows={len(toks)}")

    print("\n== premise set: raw FA per 100 / hits per 100 (as in results/premise/analysis/premise.md)")
    for key, name, *_ in crit:
        print("  " + name + ": " + "; ".join(f"{cn} FA {100*raw[key][cn]['fa']:.0f} hit {100*raw[key][cn]['hit']:.0f}" for cn, _ in rows))

    print("\n== premise set, effective P(error) for numbers vs claims (open models; d' at neutral)")
    for key, m in prem.items():
        vals = {k: p_eff(m, k) for k in ("br10", "br90", "item_p10", "item_p90", "claim_bare", "claim_random", "claim_correct")}
        print(f"  {key:28s} " + " ".join(f"{k}={v:.2f}" for k, v in vals.items() if v is not None))


if __name__ == "__main__":
    main()
