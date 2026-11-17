# Step 3 — Consolidated Weekly Research Progress Report

**Project:** Remote Patient Health Monitoring Using Machine Learning (offline ECG classification)  
**Reporting period:** November 12–17, 2026

## 1. Reporting period and baseline
This report consolidates Step 3 research and GitHub updates. The baseline is the previous MIT-BIH annotation-centered N/V heartbeat classification study using 27 features, Gaussian Naive Bayes, Random Forest, and a majority-class reference. Week 2 pooled macro-F1 was 0.7685 for Gaussian NB and 0.8065 for Random Forest. The Week 3 audit found that 825 of 867 evaluation V beats came from record 200, making pooled results sensitive to record composition.

## 2. Work completed
A provisional expanded subject-separated evaluation protocol was prepared. A record-level analysis utility was implemented to calculate confusion counts, macro-F1, V precision, recall, and support from genuine prediction CSVs. Four local unit tests passed, checking metric arithmetic and input validation. The existing Week 2/3 results were audited for false positives and false negatives. No expanded classifier experiment has been executed.

## 3. New evidence and findings
The retrospective audit of existing predictions found Gaussian NB had **116 false positives and 465 false negatives**, while Random Forest had **796 false positives and 12 false negatives**. On record 105, Random Forest produced 417 false positives alongside 41 V true positives. These are previously measured results, not new expanded-dataset findings. They document a sensitivity-versus-false-alarm trade-off. No new subject-level uncertainty estimates or preprocessing effects have been measured.

## 4. Repository changes
Repository: [Sowmya-840/FA26_Sowmya_COMP_699_A](https://github.com/Sowmya-840/FA26_Sowmya_COMP_699_A), branch `main`.

- `docs/step_3/tasks_1_to_6.md`: task register and honest completion status (commits `36dc0b7`, `00cc00b`).
- `src/step3_protocol.json`: provisional subject-separated study design (`6b22f6e`).
- `src/step3_analysis.py`: pooled/per-record analysis utility (`5fcc895`).
- `src/test_step3_analysis.py`: four validation tests (`5f1b874`).
- `docs/step_3/task_4_existing_error_audit.md`: retrospective FP/FN audit (`e024961`).
- `docs/step_3/task_5_validation.md`: unit-test and reproducibility status (`9a27aaa`).
- `docs/step_3/progress_report.md`: progress report and status corrections (`788db56`, `ea6cec7`, `00cad6b`; this revision adds the agreed five-section consolidated format).

These changes were committed to GitHub. No expanded-dataset predictions or performance claims were committed.

## 5. Problems and next steps
Additional MIT-BIH recordings were inaccessible from the execution environment, preventing verification of candidate records and expanded experiment execution. **Task 1: partially completed; Task 2: incomplete; Task 3: partially completed; Task 4: partially completed; Task 5: partially completed; Task 6: completed for the current progress-reporting milestone.** Next, acquire and verify the additional recordings, freeze subject-disjoint groups, run the fixed classifiers, calculate genuine per-record metrics and uncertainty, inspect waveform-level errors, test preprocessing on development records only, and update the final research evidence. This is offline annotation-centered classification, not live monitoring or clinical validation.
