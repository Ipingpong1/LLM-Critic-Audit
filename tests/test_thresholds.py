import unittest
import numpy as np
from pilot.thresholds import THRESHOLDS, choose_threshold, fit_oof, problem_folds, score_arrays

class ThresholdTests(unittest.TestCase):
    def test_ties_choose_smallest_threshold(self):
        r = np.ones(102); r[12:20] = 0
        self.assertEqual(int(THRESHOLDS[choose_threshold(r)]), 11)

    def test_strict_threshold_and_individual_replies(self):
        rows = [dict(item_id='a', condition='c', p_error=p, verdict='error') for p in (0, 100)]
        pred, native, n, scheduled = score_arrays(rows, ['a'], 'c')
        self.assertEqual(pred[0, 51], .5)
        self.assertEqual(pred[0, 101], 0.)
        self.assertEqual(pred[0, 0], 1.)
        self.assertEqual(n[0], 2)

    def test_duplicate_problem_cannot_cross_folds(self):
        items = {str(i):dict(problem=str(i // 2), has_error=bool(i % 2), split='s') for i in range(40)}
        ids = sorted(items)
        folds = problem_folds(items, ids)
        by = {}
        for i, f in zip(ids, folds):
            by.setdefault(items[i]['problem'], set()).add(f)
        self.assertTrue(all(len(v) == 1 for v in by.values()))

    def test_test_labels_cannot_change_own_fold_predictions(self):
        rng = np.random.default_rng(3)
        y = np.arange(100) % 2 == 0
        folds = np.arange(100) // 20
        scores = (rng.integers(0, 101, 100)[:, None] > THRESHOLDS).astype(float)
        w = np.ones((1, 100))
        a, _ = fit_oof(scores, scores, y, folds, w, .5, np.ones(100, bool))
        changed = y.copy(); changed[folds == 0] = ~changed[folds == 0]
        b, _ = fit_oof(scores, scores, changed, folds, w, .5, np.ones(100, bool))
        np.testing.assert_array_equal(a[:, folds == 0], b[:, folds == 0])
