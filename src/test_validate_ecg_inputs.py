import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from validate_ecg_inputs import annotation_counts, validate_record

class InputTests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(annotation_counts(bytes([1,4,1,20,0,0]),10),(1,1))
    def test_missing_terminator(self):
        with self.assertRaises(ValueError): annotation_counts(bytes([1,4]),10)
    def test_outside_signal(self):
        with self.assertRaises(ValueError): annotation_counts(bytes([10,4,0,0]),10)
    def test_truncated_aux(self):
        with self.assertRaises(ValueError): annotation_counts(bytes([8,252,0,0]),10)
    def test_truncated_skip(self):
        with self.assertRaises(ValueError): annotation_counts(bytes([0,236,0,0]),10)
    def test_signal_validation(self):
        with TemporaryDirectory() as d:
            p=Path(d)
            (p/'x.hea').write_text('x 2 360 3\nx.dat 212 200 11 0 0 0 0 MLII\nx.dat 212 200 11 0 0 0 0 V1\n')
            (p/'x.dat').write_bytes(bytes(9))
            (p/'x.atr').write_bytes(bytes([1,4,1,20,0,0]))
            self.assertEqual(validate_record(p,'x')['v_annotations'],1)
            (p/'x.dat').write_bytes(bytes(8)+b'\x01')
            with self.assertRaisesRegex(ValueError,'Checksum'): validate_record(p,'x')
            (p/'x.dat').write_bytes(bytes(8))
            with self.assertRaisesRegex(ValueError,'length'): validate_record(p,'x')
