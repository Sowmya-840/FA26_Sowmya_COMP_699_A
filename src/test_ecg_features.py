"""Offline feature checks; no recordings, downloads or model fitting required."""

import ast
import json
from pathlib import Path
import unittest
import numpy as np

PROTOCOL = json.loads((Path(__file__).parent / "week2_protocol.json").read_text())


def existing_feature_functions():
    """Load only pure function definitions, avoiding the script's top-level I/O."""
    source = (Path(__file__).parent / "run_week2_ecg.py").read_text()
    definitions = [
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef)
        and node.name in {"beat_features", "subject_group"}
    ]
    if {node.name for node in definitions} != {"beat_features", "subject_group"}:
        raise RuntimeError("Expected feature functions were not found in the experiment script")
    namespace = {"np": np, "P": PROTOCOL}
    exec(compile(ast.Module(body=definitions, type_ignores=[]), "run_week2_ecg.py", "exec"), namespace)
    return namespace["beat_features"], namespace["subject_group"]


beat_features, subject_group = existing_feature_functions()



class FeatureTests(unittest.TestCase):
    def test_known_ramp(self):
        window = np.arange(216, dtype=float)
        features = beat_features(window, 0.75)
        self.assertEqual(features.shape, (27,))
        self.assertEqual(features[0], 0.75)
        self.assertAlmostEqual(features[1], np.sqrt((216**2 - 1) / 12))
        self.assertEqual(features[2], 215)
        np.testing.assert_allclose(
            features[[3, -1]], [-107.5, 107.5] / np.sqrt((216**2 - 1) / 12)
        )

    def test_constant_window_rejected(self):
        with self.assertRaisesRegex(ValueError, "Constant"):
            beat_features(np.ones(216), 1)

    def test_nonfinite_window_rejected(self):
        for value in [np.nan, np.inf]:
            window = np.arange(216, dtype=float)
            window[0] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                beat_features(window, 1)

    def test_invalid_shape_rejected(self):
        for window in [np.arange(215), np.ones((216, 1))]:
            with self.subTest(shape=window.shape), self.assertRaisesRegex(
                ValueError, "window"
            ):
                beat_features(window, 1)

    def test_invalid_intervals_rejected(self):
        for rr in [0, -1, np.nan, np.inf]:
            with self.subTest(rr=rr), self.assertRaises(ValueError):
                beat_features(np.arange(216), rr)

    def test_shared_subject_grouping(self):
        self.assertEqual(subject_group("201"), subject_group("202"))
        self.assertNotEqual(subject_group("100"), subject_group("105"))


if __name__ == "__main__":
    unittest.main()
