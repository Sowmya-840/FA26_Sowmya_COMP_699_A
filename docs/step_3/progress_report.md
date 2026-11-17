# Step 3 — Weekly Research Progress Report

This update builds on the earlier offline MIT-BIH ECG beat-classification experiment and the Week 3 record-exclusion audit. The original three-record evaluation contained 867 ventricular (V) beats, of which 825 came from record 200. The observed Random Forest versus Gaussian Naive Bayes macro-F1 ordering reversed when record 200 was omitted, highlighting the need for a broader subject-separated evaluation.

**Task 1 — Expanded evaluation design.** A provisional training/development/held-out record protocol is documented in `src/step3_protocol.json`. The previous evaluation records are assigned to development because their results were inspected. Additional candidates still require verification of lead availability, class support, and subject identity before the split can be frozen.

**Task 2 — Classifier comparison.** The expanded study will reuse the existing 27-feature method and fixed majority-class, Gaussian Naive Bayes, and Random Forest settings. No expanded model fitting or predictions have yet been executed; no new performance estimates are claimed.

**Task 3 — Subject-level performance.** The new `src/step3_analysis.py` calculates pooled and per-record confusion counts, macro-F1, V precision, recall, support, and error totals from genuine prediction CSVs. It reconciles per-record totals with pooled totals. Expanded results await execution.

**Task 4 — False-positive investigation.** A development-only review of normal beats classified as ventricular and missed ventricular beats is specified. Any proposed preprocessing adjustment will be compared with the unchanged baseline before evaluation on held-out records.

**Task 5 — Reproducibility.** Four unit tests exercise metric arithmetic, duplicate-key rejection, invalid-symbol rejection, and unexpected-record rejection. These tests do not replace a full experiment rerun or a source-data integrity audit.

**Task 6 — Reporting.** The six-task research register and protocol preserve the distinction between previously measured evidence, implemented analysis utilities, and pending experiments.

**Limitations and next steps.** The research remains offline, annotation-centered N/V classification rather than live monitoring or clinical validation. Next, verify candidate records, execute the expanded comparison, inspect subject-level variability and development errors, then revise the final report with actual measured results.
