# Step 3 — Six Research Tasks and Evidence Status

Project: Remote Patient Health Monitoring Using Machine Learning (offline ECG classification)

**Baseline:** Step 2 Week 3 showed that 825 of 867 evaluation V beats came from record 200. The pooled macro-F1 comparison (Random Forest 0.8065; Gaussian NB 0.7685) reversed after excluding record 200 (0.5607 vs 0.6123). These are previously committed findings, not new Step 3 experiments.

## Task 1 — Expanded evaluation design
**Prepared, not frozen:** `src/step3_protocol.json` proposes subject-separated training, development and held-out groups. Records 100/105/200 move to development because their outcomes have been inspected. Additional candidates require verification of MLII lead, N/V support, subject separation and annotations before freezing.

## Task 2 — Classifier comparison
**Specified, not executed:** reuse 27-feature extraction, majority baseline, GaussianNB and RandomForest settings from `src/week2_protocol.json`. No new predictions or scores exist.

## Task 3 — Subject-level performance
**Analysis code prepared and locally unit-tested:** `src/step3_analysis.py` calculates pooled/per-record N/V counts, macro-F1, V precision/recall and support from prediction CSVs. Expanded results await execution.

## Task 4 — False-positive investigation
**Procedure defined, not executed:** inspect development-record N-to-V errors and V-to-N misses; test preprocessing changes only on development data; preserve the no-change baseline.

## Task 5 — Reproducibility and validation
**Unit tests prepared:** metric arithmetic, duplicate keys, invalid labels and unexpected records. Full model rerun, provenance checks and subject audit remain pending.

## Task 6 — Consolidated reporting
**Preliminary report prepared:** separate established Week 2/3 results from new code and unexecuted work. Update final report after verified experiments and commits.

**Limitations:** original N/V symbols only; annotation-centered offline classification; convenience sample; no clinical validation or demonstrated generalization.
