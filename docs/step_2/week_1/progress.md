# Week 1 research progress

## Question and working hypothesis
Compare Gaussian Naive Bayes and Random Forest on selected MIT-BIH heartbeat classes using subject-disjoint evaluation. Performance may differ; no direction is established. Final classes and features remain unresolved.

## Executed locally
The student ran Jupyter acquisition and inspection for records 100 and 106. Each has 650,000 samples per channel, two channels, a 360-Hz frequency, and approximately 30.09 minutes of recording. All 14 structural checks passed; annotation counts matched loaded entries. Four channels contained no NaN or infinite values.

Record 100 annotations: N=2239, A=33, V=1, +=1. Record 106: N=1507, V=520, +=41, ~=30. These are original symbols, not finalized classes. Channels are MLII/V5 and MLII/V1. Ten-second MLII plots, descriptive summaries, provenance, dependencies, and execution records were saved.

## Evidence boundaries
No segmentation, feature extraction, train-test partitioning, classifier training, or classification metrics are claimed. Two convenience records and finite-value checks do not establish clinical reliability or generalization.

## Problems and changes
A system-wide Anaconda install failed with access denied. A user-directory Conda environment and dedicated Jupyter kernel resolved imports. Unequal label support and different second leads require additional records and explicit selection policies.

## Week 2 plan
Finalize symbols and lead policy; acquire adequate records; map subjects and create disjoint partitions; implement validated beat features; compare a majority reference, Gaussian Naive Bayes, and Random Forest with consistent preprocessing and metrics.

## Repository status
The uploaded-to-chat notebook, original outputs, environment snapshot, and required PDF remain pending GitHub upload. This note is supplementary and does not replace research_foundation.pdf.
