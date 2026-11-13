import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

import numpy as np

from pilot.analyze import ModelData
from pilot.inference import ProblemDesign, claim_test, exact_condition_test, holm, interaction_test, vector_swap_test

ROOT = Path(__file__).resolve().parents[1]


def fixture(changes=6, repeats=(1, 1)):
    items, rows = {}, []
    for i in range(200):
        y = i < 100
        iid = str(i)
        items[iid] = dict(id=iid, has_error=y, problem=f'p{i}', split='s')
        for c, k in zip(('a', 'b'), repeats):
            e = y or (c == 'a' and 100 <= i < 100 + changes)
            for sample in range(k):
                rows.append(dict(item_id=iid, condition=c, sample=sample, has_error=y,
                                 verdict='error' if e else 'correct', p_error=100 if e else 0))
    return items, rows


class InferenceTests(unittest.TestCase):
    def test_six_one_way_changes(self):
        _, rows = fixture()
        self.assertAlmostEqual(exact_condition_test(rows, 'a', 'b')['p'], .03125)

    def test_holm_nine(self):
        adjusted = holm([1e-20, 1e-20, .00048828125, .001953125, .03125, .03125, .03125, 1., 1.])
        self.assertAlmostEqual(adjusted[4], .15625)

    def test_exact_matches_vector_swap(self):
        items, rows = fixture()
        self.assertAlmostEqual(vector_swap_test(rows, items, 'a', 'b')['p'], .03125)

    def test_identical(self):
        items, rows = fixture(0)
        self.assertEqual(claim_test(rows, items, 'a', 'b')['p'], 1.)

    def test_order_invariance(self):
        _, rows = fixture(7)
        a = exact_condition_test(rows, 'a', 'b')
        self.assertEqual(a, exact_condition_test(list(reversed(rows)), 'a', 'b'))

    def test_unequal_counts(self):
        _, rows = fixture(1, (1, 2))
        self.assertAlmostEqual(exact_condition_test(rows, 'a', 'b')['p'], 2 / 3)

    def test_missingness_travels_with_vector(self):
        items, rows = fixture(6, (3, 3))
        next(r for r in rows if r['item_id'] == '100' and r['condition'] == 'a')['verdict'] = None
        self.assertIsNone(exact_condition_test(rows, 'a', 'b'))
        res = claim_test(rows, items, 'a', 'b')
        self.assertIn('vector_swap', res['method'])
        self.assertEqual(res['informative_problems'], 6)

    def test_problem_pairs_never_split(self):
        items, _ = fixture()
        items['100']['problem'] = items['0']['problem']
        ids = sorted(items)
        design = ProblemDesign.build(items, ids)
        self.assertEqual(len(design.clusters), 199)
        weights = design.weights(100, 5)
        fl, co = design.indices(weights)
        for f, c in zip(fl, co):
            self.assertEqual(np.count_nonzero(f == ids.index('0')), np.count_nonzero(c == ids.index('100')))
        self.assertEqual(fl.shape, (100, 100))

    def test_identical_interaction_is_descriptive(self):
        items, rows = fixture(0)
        rows = [{**r, 'condition': c} for r in rows if r['condition'] == 'a' for c in ('br10', 'br90', 'freq10', 'freq90')]
        md = ModelData(rows, ['br10', 'br90', 'freq10', 'freq90'])
        design = ProblemDesign.build(items, md.ids)
        result = interaction_test(md, design, design.weights(200, 0), ['freq10', 'freq90', 'br10', 'br90'])
        self.assertEqual(result['inferential_status'], 'descriptive_only')
        self.assertEqual(result['p'], 1.)


class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('label_sensitivity', ROOT / 'scripts/label_sensitivity.py')
        cls.ls = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.ls)
        cls.key, cls.sheet = cls.ls.read_key()

    def write(self, rows):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        p = Path(td.name) / 'audit.csv'
        with p.open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=['sheet_id', 'audit_id', 'auditor', 'verdict', 'step'])
            w.writeheader()
            w.writerows(rows)
        return p

    def rows(self):
        return [dict(sheet_id=self.sheet, audit_id=k['audit_id'], auditor='R1', verdict='none', step='') for k in self.key]

    def test_complete(self):
        name, answers = self.ls.read_audit(self.write(self.rows()), self.key, self.sheet)
        self.assertEqual(name, 'R1')
        self.assertEqual(len(answers), 42)

    def test_missing_rejected(self):
        with self.assertRaises(ValueError):
            self.ls.read_audit(self.write(self.rows()[:-1]), self.key, self.sheet)

    def test_duplicate_rejected(self):
        rows = self.rows()
        with self.assertRaises(ValueError):
            self.ls.read_audit(self.write(rows + rows[:1]), self.key, self.sheet)

    def test_blank_rejected(self):
        rows = self.rows()
        rows[0]['verdict'] = ''
        with self.assertRaises(ValueError):
            self.ls.read_audit(self.write(rows), self.key, self.sheet)

    def test_mixed_reviewer_rejected(self):
        rows = self.rows()
        rows[0]['auditor'] = 'R2'
        with self.assertRaises(ValueError):
            self.ls.read_audit(self.write(rows), self.key, self.sheet)

    def test_bad_step_rejected(self):
        rows = self.rows()
        rows[0].update(verdict='error', step='9999')
        with self.assertRaises(ValueError):
            self.ls.read_audit(self.write(rows), self.key, self.sheet)

    def test_explicit_uncertainty_allowed(self):
        rows = self.rows()
        rows[0]['verdict'] = 'unsure'
        self.ls.read_audit(self.write(rows), self.key, self.sheet)


if __name__ == '__main__':
    unittest.main()
