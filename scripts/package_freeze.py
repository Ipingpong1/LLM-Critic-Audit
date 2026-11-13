"""Seal a completed numerical run with its source snapshot and clarified figures.

Verifies the numerical manifest first. This is the final packaging step before
handoff, not an analysis rerun. Refuses a second packaging pass.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def package(dest):
    dest = Path(dest)
    path = dest / 'manifest.json'
    prior_bytes = path.read_bytes()
    manifest = json.loads(prior_bytes)
    if 'packaging' in manifest:
        raise ValueError('Already packaged; do not mutate a delivered freeze')
    for rel, expected in manifest['outputs'].items():
        if sha(dest / rel) != expected:
            raise ValueError(f'Output changed before packaging: {rel}')
    for rel, expected in manifest['source_inputs'].items():
        if sha(ROOT / rel) != expected:
            raise ValueError(f'Executed source/input changed before packaging: {rel}')
    results = json.loads((dest / 'premise.json').read_text())['variants']
    original = results['original']
    counts = {}
    for v, r in results.items():
        counts[v] = dict(claim_support={family: sum(t['predicted_direction_supported'] for t in r['claim_tests'] if t['family'] == family)
                         for family in ['original_18', 'sol_9']},
                         wording_significant=[{'critic': t['critic'], 'arm': t['arm'], 'p_holm': t['p_holm']} for t in r['wording_tests'] if t['significant']],
                         wording_descriptive=sum(t['inferential_status'] == 'descriptive_only' for t in r['wording_tests']))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    evaluations = original['threshold_policies']
    policies = ['native', 'probability_threshold', 'empirical_oof', 'neutral_transfer_oof']
    titles = ['Native verdict', 'Fixed probability threshold', 'Fitted on same wording', 'Fitted on neutral']
    colors = ['#175ea8', '#c7711e', '#238052', '#a94d69']
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.7), layout='constrained', sharey=True)
    degenerate = []
    for ax, (model, e) in zip(axes, evaluations.items()):
        for policy, label, color in zip(policies, titles, colors):
            r = [x for x in e['results'] if x['condition'] == 'claim_bare' and x['policy'] == policy]
            ax.plot([x['prevalence'] for x in r], [x['risk'] for x in r], 'o-', label=label, color=color)
        ps = np.array([.1, .5, .9])
        ax.plot(ps, np.minimum(ps, 1 - ps), '--', color='#555', label='Best constant verdict', lw=1.5)
        p10 = next(x for x in e['results'] if x['condition'] == 'claim_bare' and x['policy'] == 'empirical_oof' and x['prevalence'] == .1)
        if p10['hit_rate'] == 0 and p10['fa_rate'] == 0:
            ax.text(.04, .93, 'At p = 0.1, fitted policy flags nothing', transform=ax.transAxes,
                    ha='left', va='top', fontsize=9, bbox=dict(facecolor='white', edgecolor='#ccc', alpha=.9))
            degenerate.append(model)
        ax.set(title=model.replace('-think-bf16-t1', '').replace('-think', ''), xlabel='Assumed error prevalence', xticks=ps, ylim=(-.025, 1.))
        ax.grid(alpha=.2)
    axes[0].set_ylabel('Weighted error risk on held-out problems')
    handles, labels = axes[-1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='outside lower center', ncol=3, fontsize=9, frameon=False)
    fig.suptitle('Bare claim: retrospective score-policy comparison\nOriginal labels; thresholds fit on training problems; intervals and coverage in CSV', fontsize=13)
    fig.savefig(dest / 'figures/threshold_policies.png', dpi=180)
    fig.savefig(dest / 'figures/threshold_policies.svg')
    plt.close(fig)
    ledger_path = dest / 'claim_ledger.json'
    ledger = json.loads(ledger_path.read_text())
    ledger['results_by_label_variant'] = counts
    ledger['threshold_interpretation'] = dict(
        original_label_bare_claim_fitted_policy_flags_nothing_at_p10=degenerate,
        requirement='Report hit rate, false-alarm rate and best constant-verdict baseline alongside weighted risk. Lower risk achieved by flagging nothing is not recovered detection.',
        audit_dependency='All threshold-policy labelings are retained; original-label utility does not establish utility under adjudicated labels.')
    ledger_path.write_text(json.dumps(ledger, indent=2) + '\n')
    with (dest / 'README.md').open('a') as f:
        f.write('\n## Final packaging and checks\n\n')
        f.write('`source_snapshot.tar.gz` contains the exact analysis sources and small inputs named in the numerical manifest, plus this packaging script and the pre-packaging manifest. Raw responses remain in the repository and are covered by the 97-file checksum manifest. Reproduce the numerical run first, then run `scripts/package_freeze.py <new-directory>` for this final presentation.\n\n')
        f.write('The threshold figure includes the best constant-verdict baseline. At 10% error prevalence, Qwen-27B and Sol choose the all-correct policy under the bare claim: zero hits and zero false alarms. Their low weighted risk at that prevalence is not evidence of recovered error detection. All corresponding hit/false-alarm rates are in `threshold_policies.csv`.\n\n')
        f.write('`claim_ledger.json` also records the support counts and wording-test eligibility for every label variant. The retained revised wording inference does not establish equivalence for non-significant or sparse comparisons.\n')
    own = Path(__file__).resolve()
    manifest['source_inputs'][str(own.relative_to(ROOT))] = sha(own)
    snapshot = dest / 'source_snapshot.tar.gz'
    with tarfile.open(snapshot, 'w:gz') as archive:
        for rel in sorted(manifest['source_inputs']):
            archive.add(ROOT / rel, arcname=rel, recursive=False)
        info = tarfile.TarInfo('provenance/numerical_manifest.json')
        info.size = len(prior_bytes)
        archive.addfile(info, io.BytesIO(prior_bytes))
    manifest['analysis_completed_at'] = manifest['completed_at']
    manifest['completed_at'] = datetime.now(timezone.utc).isoformat()
    manifest['packaging'] = dict(script='scripts/package_freeze.py', source_sha256=sha(own),
        change='Source snapshot; constant-verdict baseline and zero-hit annotation in policy figure; derived claim counts. Numerical tables unchanged.',
        numerical_manifest_sha256=hashlib.sha256(prior_bytes).hexdigest())
    manifest['outputs'] = {str(p.relative_to(dest)): sha(p) for p in sorted(dest.rglob('*')) if p.is_file() and p != path}
    path.write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'sealed': str(dest), 'outputs': len(manifest['outputs']), 'variant_counts': counts}, indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory', type=Path)
    package(ap.parse_args().directory)
