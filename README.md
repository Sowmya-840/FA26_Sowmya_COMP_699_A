# Remote Patient Health Monitoring Using Machine Learning

## Research scope
I am investigating offline ECG heartbeat classification using MIT-BIH data. This project does not implement live monitoring, predict heart attacks, or establish clinical reliability.

## Question and tentative answer
How do Gaussian Naive Bayes and Random Forest compare in classifying selected MIT-BIH heartbeat classes under subject-disjoint evaluation? Their error patterns and macro-F1 may differ; I have not established a direction. I will finalize classes, exclusions, and features before modeling.

## Completed locally: Week 1
I executed a Jupyter notebook using MIT-BIH v1.0.0 records 100 and 106. Both records loaded; all 14 structural checks and annotation-count checks passed. Four channels had zero NaN and infinite values. I generated descriptive tables, annotation counts, signal plots, provenance, and execution records. I have not trained a model or computed classification metrics.

## Repository artifact status
My executed notebook, principal dependencies, environment snapshot, eight CSV/JSON evidence files, three PNG plots, and research_foundation.pdf are committed in the locations below. These artifacts document the Week 1 computational foundation, not a completed model comparison.

## Repository structure
- src/week1_ecg_research_foundation.ipynb: my executed notebook
- src/requirements.txt: principal dependencies
- src/environment_lock.txt: my recorded local environment
- results/week_1/: eight CSV/JSON evidence files and three PNG plots
- docs/step_2/week_1/research_foundation.pdf: required report
- docs/step_2/week_1/progress.md: supporting progress note

## Execution instructions
Use Python 3.11 with Jupyter and ipykernel. Install principal packages with `python -m pip install -r src/requirements.txt`. Select the environment containing those packages as the notebook kernel. Open the notebook from the repository root or src/ and verify the displayed project root. Execute cells in order. Initial acquisition requires internet; existing nonempty downloads are reused. Skip the optional installation cell when already configured. My saved notebook outputs document sequential local execution; a fresh-kernel full rerun remains recommended.

## Data and attribution
Moody, G., & Mark, R. (2005). MIT-BIH Arrhythmia Database (version 1.0.0) [Data set]. PhysioNet. https://doi.org/10.13026/C2F305
Dataset: https://physionet.org/content/mitdb/1.0.0/
WFDB API: https://wfdb.readthedocs.io/en/latest/io.html
The notebook obtains raw .hea/.dat/.atr files, which are excluded from version control. My download manifest records versioned source URLs and local SHA-256 hashes; I have not independently compared them against provider checksums.

## Limitations and next work
Two convenience records do not establish generalization. Lead configurations and label distributions differ. Numerical completeness does not establish physiological quality. In Week 2, I will finalize classes and leads, acquire adequate records, define subject-disjoint partitions, and implement validated beat features and majority/GaussianNB/RandomForest comparisons. I cannot yet draw a conclusion about classifier superiority.

## History
I removed unrelated earlier project files from the current branch. Existing commit history is retained; current work is not backdated.
