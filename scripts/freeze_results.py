"""Versioned saved-response results. Never writes manuscript or legacy analysis files.

Run with an explicit new destination. Completion requires manifest.json, written last.
Human-audit updates require a new destination and a validated receipt directory.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import label_sensitivity as ls
import premise_analysis as pa
from rate_wording_analysis import ARMS
from pilot.analyze import LN81, analyze_model, model_sort_key
from pilot.inference import ProblemDesign, claim_test, holm, interaction_test, interval, stable_seed
from pilot.thresholds import evaluate as evaluate_thresholds

SETS = {
 'hard': dict(items='data/items_hard.jsonl', globs=['results/torch_hard/*.jsonl', 'results/frontier/stage_c/*.jsonl'], ref='br50'),
 'premise': dict(items='data/items_premise.jsonl', globs=['results/premise/*.jsonl', 'results/rate_wording/*.jsonl'], ref='neutral'),
 'easy': dict(items='data/items.jsonl', globs=['results/torch/*.jsonl', 'results/pilot/*.jsonl'], ref='br50'),
}
SOL = 'gpt-6.1-sol-think'


def clean(x):
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items() if not str(k).startswith('_')}
    if isinstance(x, (list, tuple, np.ndarray)):
        return [clean(v) for v in x]
    if isinstance(x, np.generic):
        return clean(x.item())
    if isinstance(x, float) and not np.isfinite(x):
        return None
    if isinstance(x, Path):
        return str(x)
    return x


def save(path, data):
    path.write_text(json.dumps(clean(data), indent=2, allow_nan=False) + '\n')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(2 ** 20), b''):
            h.update(block)
    return h.hexdigest()


def csv_write(path, rows):
    if not rows:
        return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: json.dumps(clean(v)) if isinstance(v, (dict, list, tuple, np.ndarray)) else clean(v) for k, v in row.items()})


def validate_rows(rows, items):
    seen, trials = set(), defaultdict(lambda: defaultdict(set))
    for r in rows:
        key = (r['model'], r['condition'], r['item_id'], r['sample'])
        if key in seen:
            raise ValueError(f'Duplicate accepted trial {key}')
        seen.add(key)
        if r['item_id'] not in items or bool(r['has_error']) != bool(items[r['item_id']]['has_error']):
            raise ValueError('Response labels do not match item file')
        if r.get('verdict') not in (None, 'correct', 'error'):
            raise ValueError('Unexpected parsed verdict')
        trials[r['model'], r['condition']][r['item_id']].add(r['sample'])
    for (m, c), counts in trials.items():
        if set(counts) != set(items):
            raise ValueError(f'Missing items: {m}, {c}')
        values = {tuple(sorted(v)) for v in counts.values()}
        if len(values) != 1 or next(iter(values)) != tuple(range(len(next(iter(values))))):
            raise ValueError(f'Incomplete scheduled sample slots: {m}, {c}')
    return dict(accepted_rows=len(rows), models=len({r['model'] for r in rows}), items=len(items),
                unique_problems=len({v['problem'] for v in items.values()}), duplicate_trials=0,
                missing_scheduled_slots=0, response_label_mismatches=0)


def variants(items, contested):
    base = {i: bool(it['has_error']) for i, it in items.items()}
    damaged = {i for i, it in items.items() if any(ch in it['problem'] + ''.join(it['steps']) for ch in '\x0c\x08')}
    return dict(original=base, drop={i: None if i in contested else v for i, v in base.items()},
                flip={i: not v if i in contested else v for i, v in base.items()},
                no_damaged={i: None if i in damaged else v for i, v in base.items()})


def missing_bounds(res):
    """Monotone bounds in all missing error counts for each three-condition rho.

    c and d' are monotone in each class-specific count, so extrema occur at
    vertices for distinct low/high/reference conditions. No new labels inferred.
    """
    md, col = res['_md'], res['_col']
    out = {}
    for arm, v in res['arms'].items():
        cs = list(dict.fromkeys([v['low'], v['high'], res['ref']]))
        indices = [col[c] for c in cs]
        h = md.E[md.fl_idx][:, indices].sum(0) / md._k[indices]
        f = md.E[md.co_idx][:, indices].sum(0) / md._k[indices]
        ns = md.T[md.fl_idx][:, indices].sum(0) / md._k[indices]
        nn = md.T[md.co_idx][:, indices].sum(0) / md._k[indices]
        mh = (md.T - md.V)[md.fl_idx][:, indices].sum(0) / md._k[indices]
        mf = (md.T - md.V)[md.co_idx][:, indices].sum(0) / md._k[indices]
        masks = ((np.arange(2 ** (2 * len(cs)))[:, None] >> np.arange(2 * len(cs))) & 1)
        zh = norm.ppf((h + masks[:, :len(cs)] * mh + .5) / (ns + 1))
        zf = norm.ppf((f + masks[:, len(cs):] * mf + .5) / (nn + 1))
        c = -.5 * (zh + zf)
        d = zh[:, cs.index(res['ref'])] - zf[:, cs.index(res['ref'])]
        vals = (c[:, cs.index(v['low'])] - c[:, cs.index(v['high'])]) * d / LN81
        out[arm] = dict(min=float(vals.min()), max=float(vals.max()), imputations=len(vals),
                        note='Point sensitivity assigning all missing replies within each label/condition to either verdict; no uncertainty interval')
    return out


def claims(models, rows_by, items, boot, draws):
    all_tests = []
    for names, family in [(pa.PRIMARY, 'original_18'), ([SOL], 'sol_9')]:
        tests = []
        for name in names:
            if name not in models:
                continue
            res = models[name]
            md, col = res['_md'], res['_col']
            bc = md.rates(*boot)[3]
            for test, a, b, sign, what in pa.TESTS:
                r = claim_test(rows_by[name], items, a, b, draws, stable_seed('claim', name, test))
                r.update(critic=name, test=test, a=a, b=b, predicted_sign=sign, description=what, family=family,
                         ci=interval(bc[:, col[a]] - bc[:, col[b]]),
                         ci_status='descriptive paired problem percentile interval; not a test inversion')
                tests.append(r)
        for r, p in zip(tests, holm([r['p'] for r in tests])):
            r['p_holm'] = p
            r['significant'] = p < .05
            r['predicted_direction_supported'] = bool(p < .05 and r['predicted_sign'] and np.sign(r['estimate']) == r['predicted_sign'])
            r['equivalence'] = 'not established by this analysis'
        all_tests.extend(tests)
    return all_tests


def wording(models, design, weights, boot, validation):
    tests = []
    for name, res in models.items():
        md, col = res['_md'], res['_col']
        d = next(c['d_prime'] for c in res['conditions'] if c['condition'] == res['ref'])
        _, _, bd, bc = md.rates(*boot)
        if not all(c in col for c in ARMS['br']):
            continue
        for arm, pair in ARMS.items():
            if arm == 'br' or not all(c in col for c in pair):
                continue
            conds = [*pair, *ARMS['br']]
            r = interaction_test(md, design, weights, conds)
            b = (bc[:, col[conds[0]]] - bc[:, col[conds[1]]] - bc[:, col[conds[2]]] + bc[:, col[conds[3]]]) * bd[:, col[res['ref']]] / LN81
            r.update(critic=name, arm=arm, rho_difference=r['estimate'] * d / LN81,
                     rho_difference_ci=interval(b), ceiling=res['ceiling'])
            if not validation['wording_validation_passed']:
                r.update(p=1., inferential_status='descriptive_only', reason='Simulation validation failed')
            tests.append(r)
    if len(tests) != 60:
        raise ValueError(f'Expected 60 wording-family slots, got {len(tests)}')
    for r, p in zip(tests, holm([r['p'] for r in tests])):
        r.update(p_holm=p, significant=bool(p < .05), equivalence='not established by this analysis')
    return tests


def reasoning_contrasts(models, boot):
    out = []
    for name, on in models.items():
        if 'nothink' in name or '-think' not in name:
            continue
        off_name = name.replace('-think', '-nothink')
        if off_name not in models:
            continue
        off = models[off_name]
        if 'base_rate' not in on['arms'] or 'base_rate' not in off['arms']:
            continue
        a, b = on['arms']['base_rate'], off['arms']['base_rate']
        ion, ioff = on['_col'], off['_col']
        don, con = on['_md'].rates(*boot)[2:]
        doff, coff = off['_md'].rates(*boot)[2:]
        c_diff = con[:, ion[a['low']]] - con[:, ion[a['high']]] - coff[:, ioff[b['low']]] + coff[:, ioff[b['high']]]
        out.append(dict(on=name, off=off_name, delta_rho=a['rho'] - b['rho'],
            delta_rho_ci=interval(on['_b_rho'] - off['_b_rho']),
            delta_observed_shift=a['delta_c'] - b['delta_c'], delta_observed_shift_ci=interval(c_diff),
            delta_d_ref=float(don[0, ion[on['ref']]] - doff[0, ioff[off['ref']]]),
            note='Paired descriptive comparison of configured modes; no claim about isolated internal reasoning'))
        # Point d-prime must use actual observations, not the first bootstrap draw.
        out[-1]['delta_d_ref'] = next(c['d_prime'] for c in on['conditions'] if c['condition'] == on['ref']) - next(c['d_prime'] for c in off['conditions'] if c['condition'] == off['ref'])
        out[-1]['delta_d_ref_ci'] = interval(don[:, ion[on['ref']]] - doff[:, ioff[off['ref']]])
    return out


def run_set(name, cfg, args, key, validation, audit_labels):
    items = {it['id']: it for it in map(json.loads, (ROOT / cfg['items']).read_text().splitlines())}
    rows = ls.load(cfg['globs'])
    health = validate_rows(rows, items)
    contested = {k['item_id'] for k in key if k['set'] == name and k['group'].startswith('contested')}
    labelings = variants(items, contested) if name != 'easy' else {'original': {i: it['has_error'] for i, it in items.items()}}
    if name != 'easy':
        labelings.update({v: labels[name] for v, labels in audit_labels.items()})
    output = dict(health=health, variants={})
    for variant, labels in labelings.items():
        rows2, items2 = ls.relabel(rows, items, labels)
        design = ProblemDesign.build(items2, sorted(items2))
        weights = design.weights(args.bootstrap, stable_seed(args.seed, name, variant))
        boot = design.indices(weights)
        by = defaultdict(list)
        for r in rows2:
            by[r['model']].append(r)
        models = {}
        result = dict(n_items=len(items2), n_problems=len(design.clusters), n_flawed=int(design.labels.sum()),
                      n_correct=int((~design.labels).sum()), singleton_strata=sum(len(s) == 1 for s in design.strata),
                      critics=models)
        for model in sorted(by, key=model_sort_key):
            print(f'{name}/{variant}: {model}', flush=True)
            res = analyze_model(model, by[model], items2, args.bootstrap, cfg['ref'], np.random.default_rng(args.seed),
                                boot_indices=boot, auc_bootstrap_limit=args.auc_bootstrap)
            md, col = res['_md'], res['_col']
            neu = col.get('neutral', col[res['ref']])
            errors = md.V[md.fl_idx, neu].sum() - md.E[md.fl_idx, neu].sum() + md.E[md.co_idx, neu].sum()
            res['errors_per_200'] = 200 * errors / md.V[:, neu].sum()
            res['ceiling'] = bool(res['errors_per_200'] <= 4)
            for c in res['conditions']:
                k = col[c['condition']]
                c['raw_hit_rate'] = md.E[md.fl_idx, k].sum() / md.V[md.fl_idx, k].sum()
                c['raw_fa_rate'] = md.E[md.co_idx, k].sum() / md.V[md.co_idx, k].sum()
                c['scheduled_trials'] = int(md.T[:, k].sum())
                c['unparsed_fraction'] = c['unparsed'] / c['scheduled_trials']
                c['stated_score_auc'] = ls.stated_auc(by[model], c['condition'])
            res['missing_verdict_rho_bounds'] = missing_bounds(res)
            models[model] = res
        result['reasoning_contrasts'] = reasoning_contrasts(models, boot)
        if name == 'premise':
            result['claim_tests'] = claims(models, by, items2, boot, args.randomization_draws)
            result['wording_tests'] = wording(models, design, weights, boot, validation)
            result['threshold_policies'] = {m: evaluate_thresholds(by[m], items2, args.policy_bootstrap, args.seed) for m in [*pa.PRIMARY, SOL]}
        if variant == 'original' and name != 'easy':
            output['all_contested_label_assignments'] = ls.assignment_ranges(name, models, contested,
                [{**t, 'est': t['estimate']} for t in result.get('claim_tests', []) if t['critic'] in pa.PRIMARY])
        output['variants'][variant] = clean(result)
        # Progress checkpoint, not a completed freeze (no manifest yet).
        save(args.out_dir / f'{name}.json', output)
    return output


def reconciliation(results):
    checks = []
    for name, paths in [('hard', ['results/torch_hard/analysis/summary.json']),
                        ('easy', ['results/torch/summary.json', 'results/pilot/summary.json']),
                        ('premise', ['results/premise/analysis/summary.json'])]:
        now = results[name]['variants']['original']['critics']
        diffs = []
        for path in paths:
            for old in json.loads((ROOT / path).read_text()):
                new = now[old['model']]
                nc = {c['condition']: c for c in new['conditions']}
                for c in old['conditions']:
                    for field in ['c', 'd_prime', 'hit_rate', 'fa_rate']:
                        diffs.append(abs(c[field] - nc[c['condition']][field]))
                for arm, entry in old['arms'].items():
                    diffs.append(abs(entry['rho'] - new['arms'][arm]['rho']))
        checks.append(dict(set=name, point_estimates_compared=len(diffs), max_absolute_difference=max(diffs)))
    if any(c['max_absolute_difference'] > 1e-10 for c in checks):
        raise ValueError(f'Unexpected point estimate discrepancy {checks}')
    old = json.loads((ROOT / 'results/premise/analysis/premise.json').read_text())['primary_tests']
    old = {(t['critic'], t['test']): t for t in old}
    word = json.loads((ROOT / 'results/rate_wording/analysis/rate_wording.json').read_text())
    old.update({(SOL, t['test']): t for t in word['results']['original']['W5']})
    comparisons = []
    for t in results['premise']['variants']['original']['claim_tests']:
        prior = old.get((t['critic'], t['test']))
        comparisons.append(dict(critic=t['critic'], test=t['test'], family=t['family'],
            old_p_holm=None if prior is None else prior['p_holm'], revised_p_holm=t['p_holm'],
            old_supported=None if prior is None else (prior.get('held', False) if 'held' in prior else prior.get('outcome') == 'held'),
            revised_significant=t['significant'], predicted_direction_supported=t['predicted_direction_supported']))
    return dict(point_estimates=checks, claim_tests=comparisons,
                intervals='Changed by whole-problem split-stratified resampling; old intervals are not freeze outputs',
                legacy_equivalence='Not carried forward; lack of significance does not establish equivalence')


def tables(results, dest):
    arms, conditions, tests, wording_rows, policies, reasoning = [], [], [], [], [], []
    for name, output in results.items():
        for variant, r in output['variants'].items():
            for model, res in r['critics'].items():
                common = dict(set=name, variant=variant, critic=model, ceiling=res['ceiling'], errors_per_200=res['errors_per_200'])
                arms.extend([{**common, 'arm': a, **v} for a, v in res['arms'].items()])
                conditions.extend([{**common, **c} for c in res['conditions']])
            tests.extend([dict(variant=variant, **t) for t in r.get('claim_tests', [])])
            wording_rows.extend([dict(variant=variant, **t) for t in r.get('wording_tests', [])])
            reasoning.extend([dict(set=name, variant=variant, **t) for t in r['reasoning_contrasts']])
            for m, evaluation in r.get('threshold_policies', {}).items():
                policies.extend([dict(variant=variant, critic=m, **entry) for entry in evaluation['results']])
    for file, data in [('arms', arms), ('conditions', conditions), ('claim_tests', tests), ('wording_tests', wording_rows),
                       ('threshold_policies', policies), ('reasoning_contrasts', reasoning)]:
        csv_write(dest / (file + '.csv'), data)


def figures(results, dest):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    dest.mkdir()
    hard = results['hard']['variants']
    names = list(hard['original']['critics'])
    fig, ax = plt.subplots(figsize=(10, 6.5), layout='constrained')
    for j, v in enumerate(['original', 'drop', 'flip']):
        for i, m in enumerate(names):
            r = hard[v]['critics'][m]
            a = r['arms']['base_rate']
            ax.errorbar(a['rho'], i + (j - 1) * .2, xerr=np.array([[a['rho'] - a['rho_ci'][0]], [a['rho_ci'][1] - a['rho']]]),
                        fmt='o' if not r['ceiling'] else 'x', color=['#175ea8','#be6224','#308863'][j], capsize=2,
                        label=v if i == 0 else None)
    ax.axvline(1, color='#777', ls='--'); ax.axvline(0, color='#ccc', lw=.8)
    ax.set(yticks=range(len(names)), yticklabels=names, xlabel='Prior-use ratio ρ (conditional Gaussian reference)',
           title='Hard set: label sensitivity\n95% descriptive problem-bootstrap intervals; × marks near-ceiling estimates')
    ax.legend(); fig.savefig(dest / 'hard_label_sensitivity.png', dpi=180); fig.savefig(dest / 'hard_label_sensitivity.svg'); plt.close(fig)
    models = results['premise']['variants']['original']['critics']
    names = list(models)
    conds = ['neutral', 'presuppose', 'claim_bare', 'claim_mistake', 'claim_reviewer', 'claim_random']
    matrix = np.array([[next(c['raw_fa_rate'] for c in models[m]['conditions'] if c['condition'] == cond) for cond in conds] for m in names])
    fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')
    im = ax.imshow(matrix * 100, vmin=0, vmax=100, cmap='Blues', aspect='auto')
    for i in range(len(names)):
        for j in range(len(conds)):
            ax.text(j, i, f'{100 * matrix[i,j]:.1f}', ha='center', va='center', color='white' if matrix[i,j] > .55 else 'black')
    ax.set(xticks=range(len(conds)), xticklabels=conds, yticks=range(len(names)), yticklabels=names,
           title='Held-out set: false alarms per 100 originally correct solutions\nParsed replies; original labels; means over repeated replies')
    ax.tick_params(axis='x', labelrotation=25); fig.colorbar(im, ax=ax, label='False-alarm rate (%)')
    fig.savefig(dest / 'heldout_false_alarms.png', dpi=180); fig.savefig(dest / 'heldout_false_alarms.svg'); plt.close(fig)
    evaluations = results['premise']['variants']['original']['threshold_policies']
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), layout='constrained', sharey=True)
    policy_names = ['native', 'probability_threshold', 'empirical_oof', 'neutral_transfer_oof']
    for ax, (m, e) in zip(axes, evaluations.items()):
        for policy in policy_names:
            rs = [r for r in e['results'] if r['condition'] == 'claim_bare' and r['policy'] == policy]
            ax.plot([r['prevalence'] for r in rs], [r['risk'] for r in rs], 'o-', label=policy)
        ax.set(title=m.replace('-think-bf16-t1','').replace('-think',''), xlabel='Assumed error prevalence', xticks=[.1,.5,.9])
        ax.grid(alpha=.2)
    axes[0].set_ylabel('Weighted error risk on held-out problems')
    axes[-1].legend(fontsize=8); fig.suptitle('Bare claim: retrospective score-policy comparison\nOriginal labels; training-only threshold selection; intervals and coverage in CSV')
    fig.savefig(dest / 'threshold_policies.png', dpi=180); fig.savefig(dest / 'threshold_policies.svg'); plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--validation', type=Path, required=True)
    ap.add_argument('--bootstrap', type=int, default=10000)
    ap.add_argument('--auc-bootstrap', type=int, default=1000)
    ap.add_argument('--policy-bootstrap', type=int, default=999)
    ap.add_argument('--randomization-draws', type=int, default=200000)
    ap.add_argument('--seed', type=int, default=20261112)
    ap.add_argument('--audit-receipt', type=Path, action='append', default=[])
    args = ap.parse_args()
    if args.out_dir.exists():
        raise SystemExit('Use a new output directory; freezes and partial runs are never overwritten')
    validation = json.loads(args.validation.read_text())
    key, sheet = ls.read_key()
    audit_variants, receipts = {}, []
    original_items = {s: {it['id']: it for it in map(json.loads, (ROOT / cfg['items']).read_text().splitlines())} for s, cfg in SETS.items() if s != 'easy'}
    for directory in args.audit_receipt:
        receipt = json.loads((directory / 'receipt.json').read_text())
        response = directory / 'responses.csv'
        if sha(response) != receipt['response_sha256']:
            raise ValueError('Audit snapshot checksum mismatch')
        reviewer, answers = ls.read_audit(response, key, sheet)
        if reviewer != receipt['reviewer']:
            raise ValueError('Audit reviewer does not match receipt')
        for gap in (False, True):
            name = f'audit_{reviewer}_gap_' + ('error' if gap else 'correct')
            if name in audit_variants:
                raise ValueError('Duplicate reviewer identifier across receipts')
            audit_variants[name] = ls.audit_labels(original_items, key, answers, gap)
        receipts.append(receipt)
    # Check all declared raw responses before any analysis.
    raw_manifest = ROOT / 'data/RESPONSE_FILES.sha256'
    checked = []
    for line in raw_manifest.read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        expected, rel = line.split(maxsplit=1)
        rel = rel.lstrip('* ')
        path = ROOT / rel
        actual = sha(path)
        if actual != expected:
            raise ValueError(f'Raw response checksum mismatch: {rel}')
        checked.append(dict(path=rel, sha256=actual, bytes=path.stat().st_size))
    args.out_dir.mkdir(parents=True)
    save(args.out_dir / 'validation.json', validation)
    results = {s: run_set(s, cfg, args, key, validation, audit_variants) for s, cfg in SETS.items()}
    reconcile = reconciliation(results)
    save(args.out_dir / 'reconciliation.json', reconcile)
    tables(results, args.out_dir)
    figures(results, args.out_dir / 'figures')
    tests = results['premise']['variants']['original']['claim_tests']
    counts = {family: sum(t['predicted_direction_supported'] for t in tests if t['family'] == family) for family in ['original_18', 'sol_9']}
    ledger = dict(status='Saved-response freeze conditional on original labels' if not receipts else 'Saved-response freeze including declared human audit variants',
        human_audit_status='pending' if not receipts else 'completed response snapshots; see declared assistance and unresolved counts',
        supported_claim_contrasts=counts,
        mandatory_limits=['Gaussian optimum is a conditional reference, not an identified optimum for actual critics',
                         'Effective prior is shift-equivalent, not an estimate of internal belief',
                         'Reported-score AUC does not measure preservation of latent evidence',
                         'Attribution and declared randomness are confounded; no isolated reliability-remedy claim',
                         'Reasoning gains are model-specific; report paired observed shifts as well as rho',
                         'Near-ceiling rho is descriptive; percentile uncertainty undercovers in simulated ceiling regimes',
                         'Threshold evaluation is retrospective, uses previously inspected data, and requires matched-score coverage reporting',
                         'No revised population-equivalence conclusions; non-significance is not equivalence',
                         'Label-assignment ranges cover contested labels only; audited controls may also change',
                         'A selected audit cannot estimate overall benchmark label-error prevalence'],
        human_audits=receipts)
    save(args.out_dir / 'claim_ledger.json', ledger)
    readme = f'''# Saved-response freeze — 2026-11-12

Status: {ledger['status']}. Human audit: {ledger['human_audit_status']}.
This directory supports a human-authored manuscript; it contains technical evidence, not replacement manuscript prose.

## Entry points

- `claim_ledger.json`: usable conclusions and mandatory limits.
- `arms.csv`, `conditions.csv`: publication-number ledger, label variant and ceiling flag on every row. H/F in the original fields use the historical correction; `raw_hit_rate` / `raw_fa_rate` are observed fractions.
- `claim_tests.csv`: corrected exact/randomization tests; Holm families 18 and 9. Original-label predicted-direction support: {counts['original_18']}/18 and {counts['sol_9']}/9.
- `wording_tests.csv`: studentized interaction tests, 60-slot Holm family per labeling. Sparse/degenerate cases are descriptive and keep p=1 in the family. rho intervals are descriptive.
- `threshold_policies.csv`: five-fold problem-held-out risk, matched reply coverage, selected thresholds and full-refit bootstrap intervals. These are retrospective analyses, not fresh confirmatory experiments.
- `reasoning_contrasts.csv`: paired changes in d-prime, observed criterion shift, and rho.
- `hard.json`, `premise.json`, `easy.json`: full numerical results, missing-verdict sensitivities, all contested-label assignments, fixed folds and detailed test provenance.
- `reconciliation.json`: old/new point-estimate agreement and corrected claim inference.
- `validation.json`: finite simulation checks, including rho undercoverage near ceiling; not a proof of calibration.
- `figures/`: PNG and editable SVG figures generated solely from these results.
- `manifest.json`: input/source/output checksums and runtime settings; written last. A directory without it is incomplete.

## Interpretation and pending work

Original, drop, flip and damaged-text exclusions are sensitivity variants, not estimates of correct labels. Drop/flip were selected using model disagreements. A completed human audit must be archived using `scripts/check_audit.py` and supplied as `--audit-receipt` to a NEW output directory. Report both gap readings and explicit uncertainty. Never replace this version in place. Two reviewers require separate first-pass files and a separate adjudication record.

Bootstrap intervals are descriptive and are not inversions of the randomization tests. Whole problems are resampled within split and exact label-composition strata, with paired conditions and common critic resamples; singleton strata contribute no resampling uncertainty. No latent-evidence, internal-belief, universal reasoning, or isolated attribution/reliability causal claim is supported by these calculations alone.

Raw outputs and manuscript files are untouched. No new model calls were made. Source baseline: `.local/results-freeze-baseline-2026-11-12/`. Historical scripts remain legacy paths; use this freeze's CSV/JSON for revised inference.

## Reproduction

Use the same environment in `uv.lock`, then run `scripts/validate_freeze.py --simulations 500 --bootstrap 999 --out <validation.json>` and `scripts/freeze_results.py --validation <validation.json> --out-dir <new-directory>`. Defaults match this run unless the manifest settings say otherwise. Run `python -m unittest discover -s tests -v` first. Hashes establish integrity of these saved inputs, not provider revision identity or experimental randomization.
'''
    (args.out_dir / 'README.md').write_text(readme)
    sources = sorted(set([*ROOT.glob('pilot/*.py'), *ROOT.glob('scripts/*.py'), *ROOT.glob('tests/*.py'),
                          *ROOT.glob('prereg/*'), ROOT / 'pyproject.toml', ROOT / 'uv.lock',
                          ROOT / 'audit/audit_sheet.html', ROOT / 'audit/audit_key.csv', ROOT / 'audit/START_HERE.html',
                          ROOT / 'manuscript/main.pdf', ROOT / 'manuscript/main.tex', raw_manifest,
                          *[ROOT / cfg['items'] for cfg in SETS.values()]]))
    manifest = dict(completed_at=datetime.now(timezone.utc).isoformat(), settings=vars(args),
        python=sys.version, platform=platform.platform(), numpy=np.__version__, scipy=scipy.__version__,
        source_inputs={str(p.relative_to(ROOT)): sha(p) for p in sources if p.is_file()},
        raw_responses=checked, audit_receipts=receipts,
        outputs={str(p.relative_to(args.out_dir)): sha(p) for p in sorted(args.out_dir.rglob('*')) if p.is_file()})
    save(args.out_dir / 'manifest.json', manifest)
    print(f'COMPLETE: {args.out_dir}; claim support {counts}', flush=True)


if __name__ == '__main__':
    main()
