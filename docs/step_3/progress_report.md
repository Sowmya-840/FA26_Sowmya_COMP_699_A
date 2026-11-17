# Step 3 — Weekly Research Progress Report

This update builds on the earlier offline MIT-BIH ECG beat-classification experiment and the Week 3 record-exclusion audit. The original three-record evaluation contained 867 ventricular (V) beats, of which 825 came from record 200. The observed Random Forest versus Gaussian Naive Bayes macro-F1 ordering reversed when record 200 was omitted, highlighting the need for a broader subject-separated evaluation.

**Task 1 — Expanded evaluation design.** A provisional training/development/held-out record protocol is documented in `src/step3_protocol.json`. The previous evaluation records are assigned to development because their results were inspected. Additional candidates still require verification of lead availability, class support, and subject identity before the split can be frozen.

**Task 2 — Classifier comparison.** The expanded study will reuse the existing 27-feature method and fixed majority-class, Gaussian Naive Bayes, and Random Forest settings. No expanded model fitting or predictions have yet been executed; no new performance estimates are claimed.

**Task 3 — Subject-level performance.** The new `src/step3_analysis.py` calculates pooled and per-record confusion counts, macro-F1, V precision, recall, support, and error totals from genuine prediction CSVs. It reconciles per-record totals with pooled totals. Expanded results await execution.

**Task 4 — False-positive investigation.** A development-only review of normal beats classified as ventricular and missed ventricular beats is specified. Any proposed preprocessing adjustment will be compared with the unchanged baseline before evaluation on held-out records.

**Task 5 — Reproducibility.** Four unit tests exercise metric arithmetic, duplicate-key rejection, invalid-symbol rejection, and unexpected-record rejection. These tests do not replace a full experiment rerun or a source-data integrity audit.

**Task 6 — Reporting.** The six-task research register and protocol preserve the distinction between previously measured evidence, implemented analysis utilities, and pending experiments.

**Limitations and next steps.** The research remains offline, annotation-centered N/V classification rather than live monitoring or clinical validation. Next, verify candidate records, execute the expanded comparison, inspect subject-level variability and development errors, then revise the final report with actual measured results.

## Subsequent verification update

Task 4's retrospective false-positive audit is now completed and documented in `docs/step_3/task_4_existing_error_audit.md`. Across the three previously evaluated records, Gaussian NB generated 116 N-to-V false positives and 465 V-to-N false negatives; Random Forest generated 796 false positives and 12 false negatives. These are original Week 2/3 results, not new expanded-record measurements. The existing data do not isolate the causes of the errors or validate any preprocessing improvement.

For Task 5, all four local unit tests in `src/test_step3_analysis.py` were executed successfully. This checks metric arithmetic and input validation only. The full expanded-dataset model rerun remains blocked because additional MIT-BIH files were not accessible from the current execution environment. See `docs/step_3/task_5_validation.md`.

**Completion status:** Task 4 retrospective analysis and Task 5 unit-level verification are completed. Tasks 1–3 still require verified additional records and real model execution; Task 4's proposed preprocessing intervention and Task 5's full-data reproducibility audit remain pending. Task 6's documentation is updated to reflect these boundaries.

## Final status for this weekly progress milestone

The **weekly progress documentation is complete**, but the **research itself is not**. Task 1 is partially completed (provisional design only); Task 2 is incomplete (no expanded classifier execution); Task 3 is partially completed (analysis utility, no expanded evaluation); Task 4 is partially completed (existing-data error audit, no waveform-level intervention); Task 5 is partially completed (four unit tests, no full reproducibility rerun); and Task 6 is completed for the present reporting milestone. These labels intentionally preserve outstanding work rather than implying results that have not been obtained. The authoritative six-task status register is `docs/step_3/tasks_1_to_6.md`.
