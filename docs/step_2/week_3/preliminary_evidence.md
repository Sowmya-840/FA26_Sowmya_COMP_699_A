# Preliminary Evidence

**Offline ECG Beat Classification**

## 1. Research question and tentative answer

How do Gaussian Naive Bayes and Random Forest compare for original N and V heartbeat symbols under subject-separated evaluation? The initial results suggest a recall versus precision trade-off for V beats. This analysis examines whether the comparison depends on which records are pooled.

## 2. Preliminary analysis

The error audit counts V-beat mistakes per record and recomputes pooled metrics after omitting each evaluation record in turn. The original predictions stay fixed.

## 3. Source data and conditions

Week 2 used MIT-BIH v1.0.0, MLII at 360 Hz, and annotation-centered 216-sample windows. Its 27 waveform and timing features fed models trained on records 106, 108, and 119. Evaluation used records 100, 105, and 200. Random Forest used 100 trees and seed 42. The majority reference predicts N.

Week 3 reads the 7,371 saved reference and predicted N/V labels in predictions.npz. V is positive. Precision = TP/(TP+FP), recall = TP/(TP+FN), and macro-F1 averages N and V F1 equally. Zero denominators are reported as zero. Exclusion sensitivity removes a record from evaluation only.

## 4. Per-record evidence

| Record | Model | V support | FP | FN | V precision | V recall |
| --- | --- | --- | --- | --- | --- | --- |
| 100 | Majority | 1 | 0 | 1 | 0.0000 | 0.0000 |
| 100 | Gaussian NB | 1 | 0 | 0 | 1.0000 | 1.0000 |
| 100 | Random Forest | 1 | 1 | 0 | 0.5000 | 1.0000 |
| 105 | Majority | 41 | 0 | 41 | 0.0000 | 0.0000 |
| 105 | Gaussian NB | 41 | 99 | 23 | 0.1538 | 0.4390 |
| 105 | Random Forest | 41 | 417 | 0 | 0.0895 | 1.0000 |
| 200 | Majority | 825 | 0 | 825 | 0.0000 | 0.0000 |
| 200 | Gaussian NB | 825 | 17 | 442 | 0.9575 | 0.4642 |
| 200 | Random Forest | 825 | 378 | 12 | 0.6826 | 0.9855 |

Source: v_errors_by_record.csv. FP counts normal beats classified as V, and FN counts V beats classified as normal.

## 5. Sensitivity of the pooled result

| Evaluation subset | V support | Majority F1 | Gaussian NB F1 | Random Forest F1 |
| --- | --- | --- | --- | --- |
| All records | 867 | 0.4688 | 0.7685 | 0.8065 |
| Exclude 100 | 866 | 0.4539 | 0.7572 | 0.7875 |
| Exclude 105 | 826 | 0.4530 | 0.7856 | 0.8774 |
| Exclude 200 | 42 | 0.4978 | 0.6123 | 0.5607 |

Source: record_exclusion_sensitivity.csv. F1 columns show fixed-label macro-F1.

Record 200 contributes 825 of the 867 V beats. Random Forest leads Gaussian NB on pooled macro-F1 (0.8065 vs. 0.7685). Removing record 200 reverses that comparison (0.5607 vs. 0.6123), with only 42 V beats remaining. On record 105, Random Forest detects all 41 V beats and produces 417 false positives. Gaussian NB detects 18 and produces 99 false positives.

## 6. Validity and reproducibility

The script checks aligned arrays, unique record/sample pairs and allowed symbols, then reconciles all pooled counts with the published confusion matrices and checks that per-record counts sum to the pooled totals. Run python src/run_week3_evidence.py with the NumPy dependency from src/requirements_week2.txt. This audit requires only the saved predictions.

The exclusion results reuse predictions from the same three evaluation records. They are sensitivity checks on this convenience sample. Record 100 has only one V beat. Differences in morphology, noise and prevalence may all affect errors, and this analysis cannot isolate their effects. Annotation-centered windows also limit the scope to offline beat classification.

## 7. Research design revision

Retain macro-F1 and report V precision, recall, support, and error counts by subject alongside it. Limit the current claim to the observed recall and false-positive trade-off. Expand the subject-separated evaluation before judging which classifier is more consistent.

## 8. Prioritized next research tasks

1. Predefine a larger subject-separated split with adequate V support.

2. Refit both models under the same feature and preprocessing protocol.

3. Report pooled and subject-level metrics with support and uncertainty.

4. Inspect false positives on high-error records and test preprocessing changes on development subjects.
