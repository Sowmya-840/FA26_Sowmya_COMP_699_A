"""Dependency-free unit tests for Step 3 metrics and data integrity."""
import unittest
from step3_analysis import analyze, validate

class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            dict(record_id='A', sample='1', true_label='N', majority='N', gaussian_nb='N', random_forest='V'),
            dict(record_id='A', sample='2', true_label='V', majority='N', gaussian_nb='V', random_forest='V'),
            dict(record_id='B', sample='1', true_label='N', majority='N', gaussian_nb='N', random_forest='N'),
            dict(record_id='B', sample='2', true_label='V', majority='N', gaussian_nb='N', random_forest='V')]
    def test_metrics(self):
        pooled, per_record = analyze(self.rows)
        self.assertEqual(len(per_record), 6)
        rf = next(x for x in pooled if x['model'] == 'random_forest')
        self.assertEqual((rf['tn'],rf['fp'],rf['fn'],rf['tp']), (1,1,0,2))
        self.assertAlmostEqual(rf['macro_f1'], (2/3+4/5)/2)
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError): validate(self.rows + [self.rows[0]])
    def test_unknown_symbol_rejected(self):
        bad = [dict(x) for x in self.rows]
        bad[0]['true_label'] = 'A'
        with self.assertRaises(ValueError): validate(bad)
    def test_unknown_record_rejected(self):
        with self.assertRaises(ValueError): validate(self.rows, {'A'})

if __name__ == '__main__':
    unittest.main()
