"""Retrospective held-out score policies; thresholds fit only on training problems."""
import numpy as np
from pilot.inference import ProblemDesign, interval, stable_seed

THRESHOLDS = np.arange(-1, 101)


def choose_threshold(risks):
    """Smallest threshold among numerical ties; final axis is candidate threshold."""
    risks = np.asarray(risks)
    return np.argmax(risks <= np.min(risks, axis=-1, keepdims=True) + 1e-12, axis=-1)


def problem_folds(items, ids, n_folds=5, seed=20261112):
    design = ProblemDesign.build(items, ids)
    folds = np.empty(len(design.clusters), int)
    rng = np.random.default_rng(seed)
    for group in design.strata:
        order = rng.permutation(group)
        folds[order] = np.arange(len(order)) % n_folds
    return folds[design.item_cluster]


def score_arrays(rows, ids, condition):
    ix = {iid: k for k, iid in enumerate(ids)}
    sums = np.zeros((len(ids), len(THRESHOLDS)))
    native, n, scheduled = [np.zeros(len(ids)) for _ in range(3)]
    for r in rows:
        if r['condition'] != condition:
            continue
        i = ix[r['item_id']]
        scheduled[i] += 1
        if r.get('verdict') not in ('correct', 'error') or r.get('p_error') is None:
            continue
        p = float(r['p_error'])
        if not 0 <= p <= 100:
            raise ValueError('Score outside 0..100')
        sums[i] += p > THRESHOLDS
        native[i] += r['verdict'] == 'error'
        n[i] += 1
    return sums / np.maximum(n[:, None], 1), native / np.maximum(n, 1), n, scheduled


def fit_oof(train, target, y, folds, weights, prevalence, train_valid):
    """Each row of weights is a full refit, with bootstrap copies in one fold."""
    out = np.zeros((len(weights), len(y)))
    selections = []
    for fold in range(5):
        tr, te = (folds != fold) & train_valid, folds == fold
        w1, w0 = weights * (tr & y), weights * (tr & ~y)
        n1, n0 = w1.sum(1), w0.sum(1)
        if np.any(n1 == 0) or np.any(n0 == 0):
            raise ValueError('A training fold has no observations in a label class')
        risk = prevalence * (1 - w1 @ train / n1[:, None]) + (1 - prevalence) * (w0 @ train / n0[:, None])
        chosen = choose_threshold(risk)
        out[:, te] = target[te][:, chosen].T
        selections.append(int(THRESHOLDS[chosen[0]]))
    return out, selections


def evaluate(rows, items, bootstrap=999, seed=20261112):
    ids = sorted(items)
    design = ProblemDesign.build(items, ids)
    y = design.labels
    folds = problem_folds(items, ids, seed=seed)
    weights = np.vstack((np.ones((1, len(ids))), design.weights(bootstrap, stable_seed(seed, 'policies'))[:, design.item_cluster]))
    neutral, _, neutral_n, _ = score_arrays(rows, ids, 'neutral')
    output = []
    for condition in ('neutral', 'claim_bare', 'presuppose'):
        scores, native, count, scheduled = score_arrays(rows, ids, condition)
        valid = count > 0
        if not np.any(valid):
            continue
        w1, w0 = weights * (valid & y), weights * (valid & ~y)
        n1, n0 = w1.sum(1), w0.sum(1)
        for prevalence in (.1, .5, .9):
            native_prediction = np.broadcast_to(native, weights.shape)
            fitted, cuts = fit_oof(scores, scores, y, folds, weights, prevalence, valid)
            transferred, neutral_cuts = fit_oof(neutral, scores, y, folds, weights, prevalence, neutral_n > 0)
            fixed_t = int(round(100 * (1 - prevalence)))
            predictions = {
                'native': (native_prediction, None),
                'probability_threshold': (np.broadcast_to(scores[:, fixed_t + 1], weights.shape), [fixed_t]),
                'empirical_oof': (fitted, cuts),
                'neutral_transfer_oof': (transferred, neutral_cuts),
                'constant_error': (np.ones_like(weights), None),
                'constant_correct': (np.zeros_like(weights), None),
            }
            risks = {}
            for policy, (pred, selected) in predictions.items():
                hit = (w1 * pred).sum(1) / n1
                fa = (w0 * pred).sum(1) / n0
                risk = risks[policy] = prevalence * (1 - hit) + (1 - prevalence) * fa
                output.append(dict(condition=condition, prevalence=prevalence, policy=policy,
                    risk=float(risk[0]), risk_ci=interval(risk[1:]), hit_rate=float(hit[0]), fa_rate=float(fa[0]),
                    matched_problems=int(valid.sum()), matched_flawed=int((valid & y).sum()),
                    matched_correct=int((valid & ~y).sum()), matched_replies=int(count.sum()),
                    scheduled_replies=int(scheduled.sum()), selected_thresholds=selected,
                    weighting='equal problem weight within label class; individual replies averaged within problem',
                    uncertainty='retrospective percentile problem bootstrap; full threshold refit; fixed folds'))
            for entry in output[-len(predictions):]:
                delta = risks[entry['policy']] - risks['native']
                entry['risk_minus_native'] = float(delta[0])
                entry['risk_minus_native_ci'] = interval(delta[1:])
    return dict(folds={iid: int(folds[i]) for i, iid in enumerate(ids)}, results=output)
