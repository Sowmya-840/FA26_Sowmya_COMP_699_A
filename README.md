# Wearable-Sensor Activity Classification for Remote Monitoring: A Comparison of Decision Tree and Random Forest Models

## 1. Project Overview

This project investigates the classification of human physical activities using smartphone inertial sensor data. It compares two machine-learning algorithms, Decision Tree and Random Forest, using the UCI Human Activity Recognition (HAR) Using Smartphones dataset.

The purpose is to establish a reproducible baseline comparison and evaluate whether Random Forest provides better classification performance than a single Decision Tree. The project focuses on activity recognition as a potential component of remote-monitoring applications. It does not diagnose medical conditions or evaluate patient health outcomes.

## 2. Research Question

On the official subject-separated UCI HAR training and test split, how do Decision Tree and Random Forest compare in accuracy, macro-precision, macro-recall, and macro-F1 when classifying six physical activities using smartphone inertial sensor features?

## 3. Dataset

**Dataset:** UCI Human Activity Recognition Using Smartphones

**Source:** https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones

The dataset contains smartphone accelerometer and gyroscope measurements collected from 30 volunteers performing six activities:

1. Walking
2. Walking upstairs
3. Walking downstairs
4. Sitting
5. Standing
6. Laying

The experiment uses the dataset's provided training and test partitions and its precomputed sensor features.

## 4. Research Method

The project uses Python and the following tools:

- pandas and NumPy for data handling
- scikit-learn for machine-learning models and evaluation
- Matplotlib for visualizing confusion matrices

The Decision Tree and Random Forest classifiers are evaluated on the same official test set. Performance is measured using accuracy, macro-precision, macro-recall, macro-F1, and confusion matrices.

## 5. Preliminary Results

The initial experiment produced the following results:

| Metric | Decision Tree | Random Forest |
|---|---:|---:|
| Accuracy | 86.36% | 92.81% |
| Macro-precision | 86.26% | 92.94% |
| Macro-recall | 86.03% | 92.49% |
| Macro-F1 | 86.05% | 92.62% |

In this preliminary experiment, Random Forest achieved higher scores on all four reported metrics. These results apply to the selected dataset, test split, and model settings; they do not establish performance on real patients or other devices.

## 6. Project Structure

- `README.md` — Project overview and instructions
- `docs/` — Research design, methodology, and supporting documentation
- `src/` — Python source code for the experiment
- `results/` — Preliminary metrics and confusion-matrix visualizations

The `results/` folder will be included when the output files are added to the repository.

## 7. Reproducibility

The repository will document:

- Python and required package versions
- Dataset download and setup instructions
- Commands for running the experiment
- Scripts used to generate the evaluation metrics and confusion matrices

The dataset itself should be obtained from the official UCI repository. Do not commit unnecessary large dataset archives or private information.

## 8. Limitations

The experiment uses a publicly available dataset collected under controlled conditions. Its findings may not generalize to other smartphones, sensor placements, populations, or everyday environments. Activity classification is not equivalent to medical diagnosis or clinical remote patient monitoring.

## 9. Project Status

The project is being developed in stages. Research planning, implementation, preliminary evaluation, and documentation will be tracked through GitHub commits as the work progresses.
