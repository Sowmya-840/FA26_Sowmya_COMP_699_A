# Remote Patient Health Monitoring Using Machine Learning

## Research scope
Offline ECG heartbeat classification using MIT-BIH data. This project does not implement live monitoring, predict heart attacks, or establish clinical reliability.

## Question and tentative answer
How do Gaussian Naive Bayes and Random Forest compare in classifying selected MIT-BIH heartbeat classes under subject-disjoint evaluation? Their error patterns and macro-F1 may differ; no direction is established. Classes, exclusions, and features remain to be finalized.

## Completed locally: Week 1
Executed a Jupyter notebook using MIT-BIH v1.0.0 records 100 and 106. Both records loaded; 14 structural checks and annotation-count checks passed. Four channels had zero NaN and infinite values. Descriptive tables, annotation counts, signal plots, provenance, and execution records were generated. No model training or classification metrics are claimed.

## Repository artifact status
The notebook, original result files, environment snapshot, and research_foundation.pdf are pending upload. This documentation commit does not by itself complete the milestone.

## Intended structure
- src/week1_ecg_research_foundation.ipynb: executed notebook
- src/requirements.txt: principal dependencies
- src/environment_lock.txt: recorded local environment
- results/week_1/: actual inspection outputs
- docs/step_2/week_1/research_foundation.pdf: required report

## Run after notebook upload
Use Python 3.11 with Jupyter and ipykernel. Install principal packages with `python -m pip install -r src/requirements.txt`. Select the environment containing those packages as the notebook kernel. Open the notebook from the repository root or src/ and verify the displayed project root. Execute cells in order. Initial acquisition requires internet; existing nonempty downloads are reused. Skip the optional installation cell when already configured. A fresh-kernel full rerun remains recommended; sequential local execution is what the submitted artifacts establish.

## Data and attribution
Moody, G., & Mark, R. (2005). MIT-BIH Arrhythmia Database (version 1.0.0) [Data set]. PhysioNet. https://doi.org/10.13026/C2F305
Dataset: https://physionet.org/content/mitdb/1.0.0/
WFDB API: https://wfdb.readthedocs.io/en/latest/io.html
Raw .hea/.dat/.atr files are obtained by notebook code and excluded from version control. The download manifest records versioned source URLs and local SHA-256 hashes, not independently verified provider checksums.

## Limitations and next work
Two convenience records do not establish generalization. Lead configurations and label distributions differ. Numerical completeness does not establish physiological quality. Week 2 will finalize classes and leads, acquire adequate records, define subject-disjoint partitions, and implement validated beat features and majority/GaussianNB/RandomForest comparisons. No conclusion about classifier superiority is yet supported.

## History
Unrelated earlier project files were removed from the current branch. Existing commit history is retained; current work is not backdated.
