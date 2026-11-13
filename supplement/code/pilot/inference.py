"""Inference used by the versioned results freeze (2026-11-12 amendment).

Historical analysis scripts remain reproducible. This module is the revised path.
Randomization tests test exchangeability of condition assignments within problem;
descriptive bootstrap intervals are not inversions of those tests.
"""
from collections import defaultdict
from dataclasses import dataclass
import hashlib

import numpy as np
from scipy.stats import beta, hypergeom, norm


def stable_seed(*parts):
    return int.from_bytes(hashlib.sha256('|'.join(map(str, parts)).encode()).digest()[:4], 'little')


def holm(ps):
    ps = np.asarray(ps, float)
    if not np.all(np.isfinite(ps)) or np.any((ps < 0) | (ps > 1)):
        raise ValueError('Holm requires finite p-values in [0,1]')
    order = np.argsort(ps, kind='stable')
    out = np.empty(len(ps))
    out[order] = np.minimum(1, np.maximum.accumulate(ps[order] * np.arange(len(ps), 0, -1)))
    return out.tolist()


def interval(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    return np.percentile(x, [2.5, 97.5]).tolist() if len(x) else [None, None]


def binomial_interval(successes, n, alpha=.05):
    return [0. if successes == 0 else float(beta.ppf(alpha / 2, successes, n - successes + 1)),
            1. if successes == n else float(beta.ppf(1 - alpha / 2, successes + 1, n - successes))]


@dataclass
class ProblemDesign:
    ids: list
    clusters: list
    item_cluster: np.ndarray
    strata: list
    labels: np.ndarray

    @classmethod
    def build(cls, items, ids):
        groups = defaultdict(list)
        for k, iid in enumerate(ids):
            groups[items[iid]['problem']].append(k)
        clusters = [np.array(groups[p], dtype=int) for p in sorted(groups)]
        item_cluster = np.empty(len(ids), int)
        strata = defaultdict(list)
        labels = np.array([items[i]['has_error'] for i in ids], bool)
        for g, ix in enumerate(clusters):
            item_cluster[ix] = g
            # Exact class composition preserves the original case-control counts,
            # while a problem contributing to both classes is always resampled whole.
            signature = (tuple(sorted({items[ids[k]]['split'] for k in ix})), tuple(sorted(labels[ix].tolist())))
            strata[signature].append(g)
        return cls(ids, clusters, item_cluster, [np.array(strata[s]) for s in sorted(strata)], labels)

    def weights(self, n_boot, seed):
        rng = np.random.default_rng(seed)
        w = np.zeros((n_boot, len(self.clusters)), dtype=float)
        for ix in self.strata:
            w[:, ix] = rng.multinomial(len(ix), np.full(len(ix), 1 / len(ix)), size=n_boot)
        return w

    def indices(self, weights):
        item_weights = weights[:, self.item_cluster].astype(int)
        idx = np.arange(len(self.ids))
        fl, co = np.flatnonzero(self.labels), np.flatnonzero(~self.labels)
        return (np.stack([np.repeat(idx[fl], w[fl]) for w in item_weights]),
                np.stack([np.repeat(idx[co], w[co]) for w in item_weights]))

    def aggregate(self, x):
        x = np.asarray(x)
        out = np.zeros((len(self.clusters),) + x.shape[1:], dtype=float)
        np.add.at(out, self.item_cluster, x)
        return out


def _z(count, repeats, n_items):
    return norm.ppf((count / repeats + .5) / (n_items + 1))


def exact_condition_test(rows, a, b):
    """Conditional exact test, including unequal repeats, when all replies parse.

    Each item's pooled Bernoulli outcomes are allocated to conditions with their
    original sample counts. Across items, convolutions yield class count PMFs.
    Requires exchangeability of individual repeats under the null.
    """
    by = defaultdict(lambda: defaultdict(list))
    truth = {}
    for r in rows:
        if r['condition'] in (a, b):
            if r.get('verdict') is None:
                return None
            by[r['item_id']][r['condition']].append(int(r['verdict'] == 'error'))
            truth[r['item_id']] = bool(r['has_error'])
    ids = sorted(by)
    if not ids or any(a not in by[i] or b not in by[i] for i in ids):
        raise ValueError('Incomplete paired conditions')
    ka, kb = {len(by[i][a]) for i in ids}, {len(by[i][b]) for i in ids}
    if len(ka) != 1 or len(kb) != 1:
        return None
    ka, kb = ka.pop(), kb.pop()
    dist, contrib, obs, counts, discord = [], [], 0., [], []
    for label in (True, False):
        cls = [i for i in ids if truth[i] == label]
        if not cls:
            raise ValueError('Both label classes are required')
        pmf, total, na, nb = np.array([1.]), 0, 0, 0
        for i in cls:
            ea, eb = sum(by[i][a]), sum(by[i][b])
            total += ea + eb
            na += ea
            nb += eb
            pmf = np.convolve(pmf, hypergeom.pmf(np.arange(ka + 1), ka + kb, ea + eb, ka))
        n = len(cls)
        idx = np.arange(len(pmf))
        valid = (total - idx >= 0) & (total - idx <= n * kb)
        vals = np.full(len(pmf), np.nan)
        vals[valid] = -.5 * (_z(idx[valid], ka, n) - _z(total - idx[valid], kb, n))
        dist.append(pmf)
        contrib.append(vals)
        obs += -.5 * (_z(na, ka, n) - _z(nb, kb, n))
        counts.append([int(na), int(nb), n])
        discord.append(sum(sum(by[i][a]) / ka != sum(by[i][b]) / kb for i in cls))
    null = contrib[0][:, None] + contrib[1][None, :]
    mass = dist[0][:, None] * dist[1][None, :]
    p = min(1., 2 * min(mass[null <= obs + 1e-12].sum(), mass[null >= obs - 1e-12].sum()))
    return dict(estimate=float(obs), p=float(p), method='exact_conditional_within_item',
                repeats=[ka, kb], counts_by_class=counts, discordant_by_class=discord,
                assumption='Within-item replies exchangeable across conditions under the null; fixed observed repeat counts')


def vector_swap_test(rows, items, a, b, draws=200000, seed=0, batch=5000):
    """Swap complete equal-length response vectors within whole problems.

    Unparsed replies travel with their condition vector; no complete-case deletion.
    """
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r['condition'] in (a, b):
            by[r['item_id']][r['condition']].append(r.get('verdict'))
    ids = sorted(by)
    if not ids or any(a not in by[i] or b not in by[i] for i in ids):
        raise ValueError('Incomplete paired conditions')
    ks = {len(by[i][c]) for i in ids for c in (a, b)}
    if len(ks) != 1:
        raise ValueError('Vector swaps require equal repeat counts; use a separately reported matched-repeat sensitivity')
    k = ks.pop()
    y = np.array([items[i]['has_error'] for i in ids], bool)
    ea, eb = [np.array([sum(v == 'error' for v in by[i][c]) for i in ids], float) for c in (a, b)]
    va, vb = [np.array([sum(v is not None for v in by[i][c]) for i in ids], float) for c in (a, b)]
    counts = lambda e: np.array([e[y].sum(), e[~y].sum()])
    first = np.r_[counts(ea), counts(va)]
    total = np.r_[counts(ea + eb), counts(va + vb)]
    delta = np.column_stack(((eb - ea) * y, (eb - ea) * ~y, (vb - va) * y, (vb - va) * ~y))
    design = ProblemDesign.build(items, ids)
    delta = design.aggregate(delta)
    delta = delta[np.any(delta != 0, axis=1)]

    def c(x):
        return -.5 * np.sum(norm.ppf((x[..., :2] / k + .5) / (x[..., 2:] / k + 1)), axis=-1)

    obs = float(c(first) - c(total - first))
    if not len(delta):
        return dict(estimate=obs, p=1., method='paired_problem_vector_swap_exact', informative_problems=0, draws=1)
    exact = len(delta) <= 18
    n = 2 ** len(delta) if exact else draws
    rng = np.random.default_rng(seed)
    extreme = 0
    for start in range(0, n, batch):
        size = min(batch, n - start)
        if exact:
            swaps = ((np.arange(start, start + size)[:, None] >> np.arange(len(delta))) & 1)
        else:
            swaps = rng.integers(0, 2, size=(size, len(delta)), dtype=np.int8)
        ac = first + swaps @ delta
        diffs = c(ac) - c(total - ac)
        extreme += int((np.abs(diffs) >= abs(obs) - 1e-12).sum())
    p = extreme / n if exact else (extreme + 1) / (n + 1)
    return dict(estimate=obs, p=float(p), method='paired_problem_vector_swap_' + ('exact' if exact else 'monte_carlo'),
                informative_problems=len(delta), draws=n,
                mc_p_interval=None if exact else binomial_interval(extreme, n),
                assumption='Whole condition-specific response vectors exchangeable within problem under the null')


def claim_test(rows, items, a, b, draws=200000, seed=0):
    # Exact item convolution requires unique problems, as in the held-out set.
    relevant = {r['item_id'] for r in rows if r['condition'] in (a, b)}
    unique = len({items[i]['problem'] for i in relevant}) == len(relevant)
    result = exact_condition_test(rows, a, b) if unique else None
    if result is not None:
        return result
    return vector_swap_test(rows, items, a, b, draws, seed)


def interaction_test(md, design, weights, conditions, min_informative=20, max_degenerate=.01):
    """Studentized centered cluster bootstrap for a four-condition c interaction.

    conditions = [wording10, wording90, original10, original90]. Point and
    resample SEs use the joint delta-method cluster influence, centered by stratum.
    No permutation of wording labels (which would test a stronger null).
    """
    ix = [md.conditions.index(c) for c in conditions]
    coeff = np.array([1., -1., -1., 1.])
    E, V = md.E[:, ix] / md._k[ix], md.V[:, ix] / md._k[ix]
    y = md.flawed[:, None]
    raw = np.concatenate((E * y, V * y, E * ~y, V * ~y), axis=1)
    clusters = design.aggregate(raw)
    all_weights = np.vstack((np.ones((1, len(clusters))), weights))
    totals = all_weights @ clusters
    h, ns, f, nn = np.split(totals, 4, axis=1)
    H, F = (h + .5) / (ns + 1), (f + .5) / (nn + 1)
    zH, zF = norm.ppf(H), norm.ppf(F)
    estimates = (-.5 * (zH + zF)) @ coeff
    g_h = -.5 * coeff / ((ns + 1) * norm.pdf(zH))
    g_f = -.5 * coeff / ((nn + 1) * norm.pdf(zF))
    grad = np.concatenate((g_h, -g_h * H, g_f, -g_f * F), axis=1)
    influence = grad @ clusters.T
    variance = np.zeros(len(estimates))
    for ids in design.strata:
        n = len(ids)
        if n > 1:
            w, g = all_weights[:, ids], influence[:, ids]
            variance += n / (n - 1) * np.maximum(0, (w * g * g).sum(1) - (w * g).sum(1) ** 2 / n)
    se = np.sqrt(variance)
    valid = np.isfinite(se[1:]) & (se[1:] > 1e-12)
    active_raw = np.column_stack((E @ coeff, V @ coeff))
    active = int(np.count_nonzero(np.any(np.abs(design.aggregate(active_raw)) > 1e-12, axis=1)))
    degenerate = float(1 - valid.mean())
    reliable = se[0] > 1e-12 and active >= min_informative and degenerate <= max_degenerate
    result = dict(estimate=float(estimates[0]), ci=interval(estimates[1:]), se=float(se[0]),
                  informative_problems=active, degenerate_fraction=degenerate,
                  method='studentized_centered_problem_bootstrap', inferential_status='eligible' if reliable else 'descriptive_only',
                  p=1., draws=len(weights))
    if reliable:
        ts = (estimates[1:][valid] - estimates[0]) / se[1:][valid]
        t0 = estimates[0] / se[0]
        result['p'] = float((np.count_nonzero(np.abs(ts) >= abs(t0)) + 1) / (len(ts) + 1))
        q = np.percentile(ts, [2.5, 97.5])
        result['studentized_ci'] = [float(estimates[0] - q[1] * se[0]), float(estimates[0] - q[0] * se[0])]
    else:
        result['reason'] = 'Sparse/degenerate interaction: no revised significance or equivalence claim'
    return result
