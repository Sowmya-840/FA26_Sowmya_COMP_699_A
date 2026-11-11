# Remote Patient Health Monitoring Using Machine Learning

## Research scope
This study investigates offline ECG heartbeat classification using MIT-BIH data. This project does not implement live monitoring, predict heart attacks, or establish clinical reliability.

## Question and tentative answer
How do Gaussian Naive Bayes and Random Forest compare in classifying selected MIT-BIH heartbeat classes under subject-disjoint evaluation? Their error patterns and macro-F1 may differ; no direction of superiority is assumed. Target classes, exclusions and features are specified before modeling.

## Completed locally: Week 1
The Week 1 Jupyter notebook was executed using MIT-BIH v1.0.0 records 100 and 106. Both records loaded; all 14 structural checks and annotation-count checks passed. Four channels had zero NaN and infinite values. The outputs include descriptive tables, annotation counts, signal plots, provenance and execution records. Week 1 did not include model training or classification metrics.

## Repository artifact status
The executed notebook, principal dependencies, environment snapshot, eight CSV/JSON evidence files, three PNG plots, and research_foundation.pdf are committed in the locations below. These artifacts document the Week 1 computational foundation, not a completed model comparison.

## Repository structure
- src/week1_ecg_research_foundation.ipynb: executed notebook
- src/requirements.txt: principal dependencies
- src/environment_lock.txt: recorded local environment
- results/week_1/: eight CSV/JSON evidence files and three PNG plots
- docs/step_2/week_1/research_foundation.pdf: required report
- docs/step_2/week_1/progress.md: supporting progress note

## Execution instructions
Use Python 3.11 with Jupyter and ipykernel. Install principal packages with `python -m pip install -r src/requirements.txt`. Select the environment containing those packages as the notebook kernel. Open the notebook from the repository root or src/ and verify the displayed project root. Execute cells in order. Initial acquisition requires internet; existing nonempty downloads are reused. Skip the optional installation cell when already configured. The saved notebook outputs document sequential local execution; a fresh-kernel full rerun remains recommended.

## Data and attribution
Moody, G., & Mark, R. (2005). MIT-BIH Arrhythmia Database (version 1.0.0) [Data set]. PhysioNet. https://doi.org/10.13026/C2F305
Dataset: https://physionet.org/content/mitdb/1.0.0/
WFDB API: https://wfdb.readthedocs.io/en/latest/io.html
The notebook obtains raw .hea/.dat/.atr files, which are excluded from version control. The download manifest records versioned source URLs and local SHA-256 hashes; these have not been independently compared against provider checksums.

## Limitations and next work
Two convenience records do not establish generalization. Lead configurations and label distributions differ. Numerical completeness does not establish physiological quality. The Week 1 plan called for finalizing classes and leads, acquiring adequate records, defining subject-disjoint partitions and implementing validated beat features and majority/GaussianNB/RandomForest comparisons. The foundation alone provides no evidence of classifier superiority.

## History
Unrelated earlier project files were removed from the current branch. Existing commit history is retained; current work is not backdated.

## Week 2: method implementation and baseline experiment
Week 2 extends the foundation to a fixed six-record N/V beat-classification experiment. Training uses records 106, 108 and 119; evaluation uses records 100, 105 and 200, preserving subject separation. The methods are a majority-class reference, Gaussian Naive Bayes and Random Forest, using 27 MLII waveform/timing features. This is an initial offline comparison, not live monitoring or a final clinical evaluation.

### Reproduce Week 2
Use a dedicated Python environment and run these separate commands from the repository root:
```bash
python -m pip install -r src/requirements_week2.txt
python src/run_week2_ecg.py
python src/build_week2_report.py
```
Alternatively open `src/week1_ecg_research_foundation.ipynb` from the root or src directory and run its appended Week 2 section in order. That section is independent of Week 1 variables. The complete Week 2 computation is present both in notebook cells and the standalone script. The first run downloads approximately 12 MB; later runs reuse raw data under ignored `data/raw/`. Jupyter and ipykernel are optional interface dependencies. Running the standalone script preserves Week 1 artifacts; the original Week 1 notebook cells still regenerate their own earlier outputs if rerun.

### Initial measured evidence
The experiment retained 5,767 training and 7,371 evaluation beats and excluded eight target annotations because a preceding reference beat or complete window was unavailable. All 30 method, integrity, leakage and repeatability checks passed.

| Method | Accuracy | Balanced accuracy | Macro-F1 |
|---|---:|---:|---:|
| Majority class | 0.882377 | 0.500000 | 0.468757 |
| Gaussian Naive Bayes | 0.921178 | 0.722916 | 0.768504 |
| Random Forest | 0.890381 | 0.931886 | 0.806505 |

Random Forest had higher macro-F1 but lower accuracy and more false positives. Its V recall was 0.986159 versus GaussianNB's 0.463668; V precision was 0.517868 versus 0.776062. Evaluation V support is concentrated in record 200. This small subject sample does not establish general classifier superiority.

### Week 2 artifacts
- `src/week1_ecg_research_foundation.ipynb`: original Week 1 cells preserved, followed by executed Week 2 cells and observations.
- `src/run_week2_ecg.py`: the same executable Week 2 code, independent of notebook state.
- `src/week2_protocol.json`: predeclared classes, record partitions, feature definitions and model settings.
- `src/requirements_week2.txt`: tested principal package versions.
- `src/build_week2_report.py`: optional PDF/Markdown report renderer.
- `results/week_2/`: input manifest, class/record/exclusion audits, feature examples, metrics, confusion matrices, validation checks, environment/protocol hashes, and complete predictions.
- `docs/step_2/week_2/method_and_baseline.pdf`: required report covering all eight milestone items; editable Markdown is included.

Load complete prediction arrays with `numpy.load('results/week_2/predictions.npz', allow_pickle=False)`. Arrays are `record_id`, `sample`, `true_label`, `majority`, `gaussian_nb` and `random_forest`, in the same row order. Feature examples illustrate the schema; full features are regenerated from raw recordings by the notebook or script. Model binaries are not needed to reproduce training.

### Boundaries and next work
Only original N and V symbols are targets, not full AAMI categories. Reference annotations provide beat centers and timing. The window extends after the annotation, and beat detection, streaming and alarms are not implemented. Record 100 was inspected in Week 1; this is a fixed development evaluation rather than a pristine final holdout. No weight/parameter search, independent validation or significance test was performed. A larger subject-separated evaluation remains planned.

The saved Week 2 outputs come from the environment recorded in `results/week_2/execution_summary.json`, not a separate local Windows run. Existing Week 1 submissions remain unchanged.


## Maintenance: independently runnable feature checks

Six offline tests cover the existing feature calculations: a known ramp, constant or malformed windows, nonfinite values, invalid RR intervals, and shared-subject grouping for records 201 and 202. The tests load only the two relevant function definitions from the experiment script using Python's syntax tree, so they exercise the existing implementation without running its acquisition or training steps. NumPy is required; recordings and model fitting are not.

Run from the repository root:

```bash
python -m unittest discover -s src -p 'test_ecg_features.py' -v
```

The feature tests run independently of the Week 2 experiment and use its existing protocol.

## Week 3 preliminary evidence

The error audit counts V-beat mistakes per record and recomputes pooled metrics after omitting each evaluation record in turn. The original predictions stay fixed.

Run `python src/run_week3_evidence.py` from the repository root to recreate the tables in `results/week_3/`. The script uses NumPy from the Week 2 environment. The notebook includes a runnable Week 3 section with the record sensitivity results and observations.

- [Preliminary evidence report](docs/step_2/week_3/preliminary_evidence.pdf)
- [Editable report](docs/step_2/week_3/preliminary_evidence.md)
