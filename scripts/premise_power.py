"""How precise would the premise test be? A simulation for prereg/premise.md (free; no model is called).

Each item has its own tendency to be flagged (a logit drawn from a normal with sd `sigma`, centred so the mean rates stay
at 16% false alarms and 96.5% hits, about where the two target critics sit), shared across conditions; each sample is an
independent draw. `sigma` is calibrated on saved replies: how often a critic agrees with itself between the "neutral" and
"told 50%" prompts on the 100 correct solutions of the hard set. A claim adds delta_i ~ N(delta, (delta / 2)^2) to the
logit, because a claim does not move every item equally.

    .venv/bin/python scripts/premise_power.py     # writes results/premise/power.md
"""
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

ROOT = Path(__file__).resolve().parent.parent
CAL = {"qwen3.5:27b on": "results/torch_hard/qwen3.5_27b-think-bf16-t1.jsonl", "qwen3.5:4b on": "results/torch_hard/qwen3.5_4b-think-bf16-t1.jsonl",
       "opus on": "results/frontier/stage_c/opus-5.5-think.jsonl", "sonnet on": "results/frontier/stage_c/sonnet-5.5-think.jsonl"}
B, SIMS = 400, 300
GRID = norm.ppf((np.arange(4000) + 0.5) / 4000)
expit = lambda x: 1 / (1 + np.exp(-x))


def centre(rate, sigma):
    """Mean logit that keeps the average rate at `rate` for item spread `sigma`."""
    return brentq(lambda m: expit(m + sigma * GRID).mean() - rate, -25, 25)


def phi(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return 0.0 if a.std() == 0 or b.std() == 0 else float(np.corrcoef(a, b)[0, 1])


def observed():
    out = {}
    for name, path in CAL.items():
        k = {}
        for line in open(ROOT / path):
            r = json.loads(line)
            if r["condition"] in ("neutral", "br50") and not r["has_error"] and r["verdict"]:
                k[r["condition"], r["item_id"]] = r["verdict"] == "error"
        ids = sorted({i for c, i in k if ("neutral", i) in k and ("br50", i) in k})
        a, b = [k["neutral", i] for i in ids], [k["br50", i] for i in ids]
        out[name] = (np.mean(a), np.mean(b), phi(a, b))
    return out


def implied_phi(sigma, rng, n=400_000):
    p = expit(rng.normal(centre(0.16, sigma), sigma, n))
    return phi(rng.random(n) < p, rng.random(n) < p)


def c_of(h, ns, f, nn, k):
    H, F = (h / k + 0.5) / (ns / k + 1), (f / k + 0.5) / (nn / k + 1)
    return -(norm.ppf(H) + norm.ppf(F)) / 2


def one_design(n, k, delta, sigma, rng):
    half, excl, mid = [], 0, []
    mf, mh = centre(0.16, sigma), centre(0.965, sigma)
    for _ in range(SIMS):
        xc, xf = rng.normal(mf, sigma, n), rng.normal(mh, sigma, n)
        dc, df = rng.normal(delta, delta / 2, n), rng.normal(delta, delta / 2, n)
        fl0, fl1 = rng.binomial(k, expit(xf)), rng.binomial(k, expit(xf + df))
        co0, co1 = rng.binomial(k, expit(xc)), rng.binomial(k, expit(xc + dc))
        i_f, i_c = rng.integers(n, size=(B, n)), rng.integers(n, size=(B, n))
        t = n * k
        sh = c_of(fl1[i_f].sum(1), t, co1[i_c].sum(1), t, k) - c_of(fl0[i_f].sum(1), t, co0[i_c].sum(1), t, k)
        lo, hi = np.percentile(sh, [2.5, 97.5])
        half.append((hi - lo) / 2)
        excl += hi < 0 or lo > 0
        mid.append(c_of(fl1.sum(), t, co1.sum(), t, k) - c_of(fl0.sum(), t, co0.sum(), t, k))
    return float(np.mean(half)), excl / SIMS, float(np.mean(mid))


def main():
    rng = np.random.default_rng(0)
    obs = observed()
    lines = ["# Premise test: expected precision (simulation, no model called)", "",
             "## Calibration: agreement between neutral and told-50% on correct solutions (hard set)", "",
             "| critic | flagged at neutral | flagged at told 50% | phi |", "|---|---|---|---|"]
    lines += [f"| {k} | {a:.2f} | {b:.2f} | {p:.2f} |" for k, (a, b, p) in obs.items()]
    lines += ["", "| item spread sigma (logit) | implied phi at a 16% flag rate |", "|---|---|"]
    table = {s: implied_phi(s, rng) for s in (1, 2, 3, 4, 6, 8)}
    lines += [f"| {s} | {p:.2f} |" for s, p in table.items()]
    target = float(np.mean([p for _, _, p in obs.values()]))
    sigma = min(table, key=lambda s: abs(table[s] - target))
    lines += ["", f"Mean phi across these critics is {target:.2f}, so the simulation uses sigma = {sigma}. "
              "The two prompts are not identical, so this is if anything a lower bound on how stable a verdict is.", "",
              "## Designs", "",
              "Half-width of the 95% CI on c(claim) − c(neutral), and the share of runs whose CI excludes 0. "
              f"{SIMS} simulated runs, {B} bootstrap resamples each.", "",
              "| items per class | samples | requests per condition | logit shift | false alarms | mean c shift | CI half-width | CI excludes 0 |",
              "|---|---|---|---|---|---|---|---|"]
    mf = centre(0.16, sigma)
    for n, k in ((100, 1), (100, 3), (100, 5), (150, 2), (300, 1)):
        for delta in (0.0, 0.5, 1.0, 2.0, 4.0):
            half, power, mid = one_design(n, k, delta, sigma, rng)
            x = rng.normal(mf, sigma, 200000)
            d = rng.normal(delta, delta / 2, 200000)
            lines.append(f"| {n} | {k} | {2 * n * k} | {delta} | {100 * expit(x).mean():.0f} → {100 * expit(x + d).mean():.0f} "
                         f"| {mid:+.2f} | {half:.2f} | {power:.2f} |")
    out = ROOT / "results" / "premise"
    out.mkdir(parents=True, exist_ok=True)
    (out / "power.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
