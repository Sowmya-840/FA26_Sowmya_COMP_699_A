# Step 3 — Task 4: Existing-record false-positive audit

**Status: completed as a retrospective audit of existing Week 2/3 results.** This is not a new expanded-dataset experiment, and no preprocessing intervention was tested.

Source: `results/week_3/v_errors_by_record.csv`, cross-checked against `results/week_2/metrics_by_record.csv`. V denotes original premature ventricular beat annotation; FP means an N beat classified as V.

| Evaluation record | V support | Gaussian NB FP | Gaussian NB FN | Random Forest FP | Random Forest FN |
| --- | ---: | ---: | ---: | ---: | ---: |
| 100 | 1 | 0 | 0 | 1 | 0 |
| 105 | 41 | 99 | 23 | 417 | 0 |
| 200 | 825 | 17 | 442 | 378 | 12 |
| **Total** | **867** | **116** | **465** | **796** | **12** |

Random Forest generates **680 more false positives** than Gaussian NB (796 versus 116), while missing **453 fewer V beats** (12 versus 465). On record 105, RF's V precision is only **0.0895** (41 TP / [41 TP + 417 FP]); Gaussian NB's is **0.1538** (18 TP / [18 TP + 99 FP]). On record 200, RF generates 378 FP versus Gaussian NB's 17, but captures 813 of 825 V beats versus Gaussian NB's 383.

**Interpretation:** the original model comparison reflects a substantial sensitivity/false-alarm trade-off. Record-level heterogeneity and V support concentration make pooled scores insufficient to establish a consistently preferable classifier. This aggregate audit does not identify whether individual false alarms arose from noise, morphology, signal drift, or annotation ambiguity. Those explanations require examining raw waveform windows and annotation neighborhoods.

**Next experimental procedure:** inspect the waveform windows for N-to-V errors on development records 105 and 200; categorize artifacts and morphology patterns; predefine any candidate filtering or normalization changes; compare changes against the unchanged baseline on development records only; then evaluate once on a newly verified held-out subject split. Do not treat the existing inspected records as a blind holdout.

No clinical sensitivity, false-alarm rate per hour, or deployment reliability is inferred from these annotation-centered beat predictions.
