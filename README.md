# Smartphone-Based Human Activity Recognition: A Comparison of Decision Tree and Random Forest Models

## 1. Project Overview

This project investigates the performance of two machine-learning algorithms, Decision Tree and Random Forest, for classifying human physical activities using smartphone sensor data.

The project uses the UCI Human Activity Recognition Using Smartphones (UCI HAR) dataset. The dataset contains sensor-derived features collected from 30 volunteers performing six physical activities.

The purpose of the experiment is to compare the classification performance of both algorithms using the same training data, test data, and evaluation metrics.

This is a preliminary research experiment for COMP-699-A Professional Seminar.

## 2. Research Question

On the official UCI HAR training and test split, how do Decision Tree and Random Forest compare in accuracy, macro-precision, macro-recall, and macro-F1 when classifying six physical activities?

The project also examines classification errors using confusion matrices.

## 3. Dataset

The experiment uses the UCI Human Activity Recognition Using Smartphones dataset.

**Official dataset source:**  
https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones

The dataset contains six activity classes:

- WALKING
- WALKING_UPSTAIRS
- WALKING_DOWNSTAIRS
- SITTING
- STANDING
- LAYING

The experiment uses the dataset's existing feature files and official training/test split.

The dataset contains smartphone accelerometer- and gyroscope-derived features. It does not contain heart-rate measurements or clinical outcomes.

## 4. Technologies Used

- Python 3
- pandas
- Matplotlib
- scikit-learn
- GitHub

## 5. Machine-Learning Algorithms

### Decision Tree

A Decision Tree learns rules from the training data and uses those rules to classify physical activities.

### Random Forest

A Random Forest combines predictions from multiple decision trees to classify physical activities.

Both models are evaluated using the same dataset split and evaluation metrics.

## 6. Project Structure

```text
FA26_Sowmya_COMP_699_A/
├── README.md
├── requirements.txt
├── src/
│   ├── run_experiment.py
│   └── smoke_test.py
├── data/
├── results/
│   ├── model_metrics.csv
│   ├── decision_tree_confusion_matrix.png
│   └── random_forest_confusion_matrix.png
└── docs/
```

The `data/` directory is used for the dataset, `src/` contains the Python scripts, `results/` contains experiment outputs, and `docs/` contains project documentation.

## 7. Requirements

The following software is required:

- Python 3
- pandas
- Matplotlib
- scikit-learn
- An internet connection for the initial automatic dataset download, if the dataset is not already available locally

No smartwatch, ECG device, or other special hardware is required for this experiment.

## 8. How to Run

### Step 1: Obtain the Project

Clone or download this GitHub repository to your computer.

### Step 2: Open a Terminal

Open a terminal in the repository's main directory, where `README.md` and `requirements.txt` are located.

### Step 3: Install the Required Libraries

Run:

```bash
pip install -r requirements.txt
```

### Step 4: Prepare the Dataset

The experiment attempts to download the UCI HAR dataset automatically if the expected dataset files are missing.

Make sure your computer has an internet connection before running the experiment.

If automatic downloading fails, download the dataset from the official source:

https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones

Extract the dataset into the location expected by `src/run_experiment.py`. The script expects the training feature file at:

`data/UCI HAR Dataset/train/X_train.txt`

### Step 5: Run the Experiment

Run the following command from the repository's main directory:

```bash
python src/run_experiment.py
```

The script loads the dataset, trains both machine-learning models, calculates evaluation metrics, prints classification reports, and generates confusion-matrix images.

### Step 6: Review the Results

After the experiment finishes, review the output files in the `results/` directory.

## 9. Evaluation Metrics

The models are evaluated using the following metrics:

- **Accuracy:** The proportion of all predictions that are correct.
- **Macro-precision:** The average precision across the six activity classes.
- **Macro-recall:** The average recall across the six activity classes.
- **Macro-F1:** The average F1-score across the six activity classes.

Confusion matrices are also used to examine which activities are misclassified.

## 10. Preliminary Results

The preliminary experiment produced the following results:

| Metric | Decision Tree | Random Forest |
|---|---:|---:|
| Accuracy | 0.8636 | 0.9281 |
| Macro-precision | 0.8626 | 0.9294 |
| Macro-recall | 0.8603 | 0.9249 |
| Macro-F1 | 0.8605 | 0.9262 |

In this experiment, Random Forest achieved higher scores than Decision Tree across all four reported metrics.

These are preliminary results from one public dataset and its official test split. They do not establish performance on real patients, heart-rate monitoring, medical diagnosis, or emergency detection.

## 11. Results Files

The `results/` directory contains:

- `model_metrics.csv` — evaluation metrics for both models.
- `decision_tree_confusion_matrix.png` — Decision Tree classification errors.
- `random_forest_confusion_matrix.png` — Random Forest classification errors.

These files support the comparison of model performance and classification errors.

## 12. Limitations

This experiment is limited to the UCI HAR dataset and its six physical activity classes. The results may not generalize to different devices, sensor placements, populations, or real-world conditions.

The experiment evaluates activity classification rather than clinical health monitoring. Additional research would be required before making claims about medical applications.

## 13. Reproducibility

To reproduce the experiment:

1. Obtain the repository.
2. Install the dependencies using `requirements.txt`.
3. Ensure the dataset is available in the expected location or allow the script to download it.
4. Run `python src/run_experiment.py`.
5. Review the generated metrics and confusion matrices in `results/`.

The experiment uses fixed random seeds in the model configuration to support reproducibility.

## 14. Project Status

This repository contains preliminary Python code and results for a machine-learning comparison experiment conducted for COMP-699-A Professional Seminar.

The research design, literature review, and final project scope remain subject to the course requirements and instructor feedback.

## 15. References

Anguita, Davide, Alessandro Ghio, Luca Oneto, Xavier Parra, and Jorge Luis Reyes-Ortiz. 2013. “A Public Domain Dataset for Human Activity Recognition Using Smartphones.” In *Proceedings of the 21st European Symposium on Artificial Neural Networks, Computational Intelligence and Machine Learning*.

Breiman, Leo. 2001. “Random Forests.” *Machine Learning* 45: 5–32. https://doi.org/10.1023/A:1010933404324.

Pedregosa, Fabian, Gaël Varoquaux, Alexandre Gramfort, et al. 2011. “Scikit-learn: Machine Learning in Python.” *Journal of Machine Learning Research* 12: 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html.

Quinlan, J. Ross. 1986. “Induction of Decision Trees.” *Machine Learning* 1: 81–106. https://doi.org/10.1007/BF00116251.
