# Step 3 — Six Research Tasks and Evidence Status

Project: Remote Patient Health Monitoring Using Machine Learning (offline ECG classification)

**Baseline:** Step 2 Week 3 showed that 825 of 867 evaluation V beats came from record 200. The pooled macro-F1 comparison (Random Forest 0.8065; Gaussian NB 0.7685) reversed after excluding record 200 (0.5607 vs 0.6123). These are previously committed findings, not new Step 3 experiments.

## Task 1 — Expanded evaluation design
**Partially completed:** A provisional subject-separated training/development/held-out protocol is documented in `src/step3_protocol.json`. Records 100/105/200 are development records because their outcomes were inspected. New candidate records, MLII lead availability, N/V support and subject identities have not yet been verified; the split is not frozen.

## Task 2 — Classifier comparison
**Incomplete:** The comparison is specified using the existing 27-feature method, majority baseline, GaussianNB and RandomForest. The expanded experiment has not been executed and no new performance scores are available.

## Task 3 — Subject-level performance
**Partially completed:** `src/step3_analysis.py` implements pooled and per-record confusion counts, macro-F1, V precision/recall and support from real prediction CSVs. No expanded-record predictions have been generated or evaluated.

## Task 4 — False-positive investigation
**Partially completed:** The retrospective audit of existing Week 2/3 predictions is completed in `docs/step_3/task_4_existing_error_audit.md`. Gaussian NB had 116 false positives and 465 false negatives; Random Forest had 796 false positives and 12 false negatives. These are previously observed counts. Waveform-level error investigation and preprocessing intervention have not been executed.

## Task 5 — Reproducibility and validation
**Partially completed:** Four local unit tests passed for metric arithmetic and input validation, as documented in `docs/step_3/task_5_validation.md`. Expanded-record acquisition, provenance checks, leakage audit and full experiment rerun remain incomplete.

## Task 6 — Consolidated reporting
**Completed for the current weekly progress milestone:** The Step 3 report (`docs/step_3/progress_report.md`) documents verified evidence, implemented methods, limitations and incomplete research tasks. It is a progress report, not a claim of completed research or clinical validity.

## Research integrity and next steps
The current progress milestone is documented even though the underlying study is unfinished. Additional MIT-BIH recordings were unavailable in the execution environment. Do not infer results for unexecuted experiments. Next, verify and freeze a suitable subject-separated record split, run the fixed classifier comparison, audit subject-level results and waveform errors, and revise the report only when actual evidence is available.

**Limitations:** Original N/V symbols only; annotation-centered offline classification; convenience sample; no clinical validation or demonstrated generalization.
