# Week 2 progress - November 3, 2026

I implemented beat segmentation, 27 waveform/timing features, a majority reference, Gaussian Naive Bayes and Random Forest. I fixed the target symbols N/V, MLII lead policy, train/evaluation record assignments and model settings before computing classifier scores. The selection is a small convenience subset and not a full inter-patient benchmark.

My experiment retained 5,767 training and 7,371 evaluation beats across six subjects. All 30 validation checks passed. A same-seed Random Forest refit produced identical predictions. GaussianNB macro-F1 was 0.768504; Random Forest was 0.806505. The higher Random Forest macro-F1 came with more false positives, so I do not claim general superiority.

I preserved the existing Week 1 notebook cells, report, result files and environment snapshot. The appended Week 2 notebook section includes executed code and observations; src/run_week2_ecg.py provides the same experiment without notebook state. The required method_and_baseline.pdf documents the method, source locations, reference, procedure, execution, results, validation and unresolved issues.

This is genuine progress from data inspection to initial evidence generation. Additional subjects, error analysis, development/validation design and assessment of subject variability remain Week 3 work. The current commit reflects this preparation session and is not backdated.
