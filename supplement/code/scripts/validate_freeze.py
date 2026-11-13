"""Saved-data inference validation. No model calls; outputs to an explicit path."""
import argparse
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from scipy.stats import binomtest, norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pilot.inference import ProblemDesign, binomial_interval, interaction_test, interval, stable_seed


def validate(sims=500, bootstrap=999, seed=20261112):
    ids = [f'{i:03}' for i in range(200)]
    y = np.arange(200) < 100
    items = {iid: dict(problem=iid, has_error=bool(y[i]), split=str(i % 2)) for i, iid in enumerate(ids)}
    design = ProblemDesign.build(items, ids)
    weights = design.weights(bootstrap, seed)
    iw = weights[:, design.item_cluster]
    outputs = []
    scenarios = [(1.5, 1, .4), (1.5, 3, .4), (3.2, 1, .4), (3.2, 3, .4), (4.5, 1, .4), (3.2, 3, 0.)]
    for d, k, offset in scenarios:
        rng = np.random.default_rng(stable_seed(seed, d, k, offset))
        rejected, eligible = 0, 0
        for _ in range(sims):
            evidence = ((y.astype(float) - .5) * d)[:, None, None]
            evidence = evidence + np.sqrt(.7) * rng.normal(size=(200, 1, 1)) + np.sqrt(.3) * rng.normal(size=(200, 4, k))
            thresholds = np.array([.3, -.3, .3 + offset, -.3 + offset])
            e = (evidence > thresholds[None, :, None]).sum(2).astype(float)
            md = SimpleNamespace(E=e, V=np.full_like(e, k), _k=np.full(4, k), flawed=y,
                                 conditions=['br10', 'br90', 'freq10', 'freq90'])
            r = interaction_test(md, design, weights, ['freq10', 'freq90', 'br10', 'br90'])
            eligible += r['inferential_status'] == 'eligible'
            rejected += r['p'] < .05
        # A null with equal prior shifts but a nonzero wording main effect.
        low, high = binomial_interval(rejected, sims)
        outputs.append(dict(kind='wording_null', d_prime=d, repeats=k, wording_main_effect=offset,
                            simulations=sims, eligible=eligible, rejections=rejected, rejection_rate=rejected / sims,
                            rejection_rate_ci=[low, high], excessive_rejection=bool(low > .05)))
        print(f'W2 null d={d}, repeats={k}, offset={offset}: {rejected}/{sims}; eligible {eligible}', flush=True)
    rho_results = []
    for d in (1.5, 3.2, 4.5):
        rng = np.random.default_rng(stable_seed(seed, 'rho', d))
        covered, ceiling, estimates = 0, 0, []
        true_rho = .5
        cs = np.array([true_rho * np.log(9) / d, -true_rho * np.log(9) / d, 0.])
        for _ in range(sims):
            x = ((y.astype(float) - .5) * d)[:, None] + np.sqrt(.7) * rng.normal(size=(200, 1)) + np.sqrt(.3) * rng.normal(size=(200, 3))
            e = (x > cs).astype(float)
            w = np.vstack((np.ones((1, 200)), iw))
            zh = norm.ppf(((w * y) @ e + .5) / ((w * y).sum(1)[:, None] + 1))
            zf = norm.ppf(((w * ~y) @ e + .5) / ((w * ~y).sum(1)[:, None] + 1))
            c = -.5 * (zh + zf)
            rho = (c[:, 0] - c[:, 1]) * (zh[:, 2] - zf[:, 2]) / np.log(81)
            lo, hi = interval(rho[1:])
            covered += lo <= true_rho <= hi
            estimates.append(rho[0])
            errors = np.sum(e[:, 2] != y)
            ceiling += errors <= 4
        rho_results.append(dict(kind='rho_coverage', d_prime=d, true_rho=true_rho, simulations=sims,
                                coverage=covered / sims, coverage_ci=binomial_interval(covered, sims),
                                mean_estimate=float(np.mean(estimates)), near_ceiling=ceiling,
                                warning='Percentile intervals are descriptive; ceiling regimes are not promoted to precise normative claims'))
        print(f'rho d={d}: coverage {covered}/{sims}, near ceiling {ceiling}', flush=True)
    # Sparse exact paired inference is independently tested analytically in unit tests.
    rng = np.random.default_rng(seed)
    rejects = []
    for _ in range(5000):
        n = rng.binomial(100, .08)
        wins = rng.binomial(n, .5)
        rejects.append(False if n == 0 else binomtest(wins, n, .5).pvalue < .05)
    return dict(seed=seed, bootstrap=bootstrap, wording_nulls=outputs, rho_coverage=rho_results,
                wording_validation_passed=not any(r['excessive_rejection'] for r in outputs),
                sparse_exact_null=dict(simulations=len(rejects), rejection_rate=float(np.mean(rejects)),
                                       ci=binomial_interval(sum(rejects), len(rejects))),
                scope='Finite simulation screen, not proof of universal calibration. Holm relies on valid individual tests. No simulated 60-test family claim is made.')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--simulations', type=int, default=500)
    ap.add_argument('--bootstrap', type=int, default=999)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    result = validate(args.simulations, args.bootstrap)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, default=lambda x: x.item()) + '\n')


if __name__ == '__main__':
    main()
