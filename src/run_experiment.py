"""Preliminary comparison of Decision Tree and Random Forest on UCI HAR.

This is research code for activity classification, not medical diagnosis.
"""
from pathlib import Path
import io, zipfile, urllib.request
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay, classification_report

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
DATA_URL = "https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip"
DATASET_DIR = DATA_DIR / "UCI HAR Dataset"


def ensure_dataset():
    if (DATASET_DIR / "train" / "X_train.txt").exists():
        return
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading the UCI HAR dataset. This may take a few minutes...")
    try:
        with urllib.request.urlopen(DATA_URL, timeout=60) as response:
            archive_bytes = response.read()
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as zf:
            zf.extractall(DATA_DIR)
    except Exception as exc:
        raise RuntimeError(
            "Automatic download failed. Download the dataset from "
            "https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones "
            "and extract the folder so data/UCI HAR Dataset/train/X_train.txt exists."
        ) from exc
    if not (DATASET_DIR / "train" / "X_train.txt").exists():
        raise FileNotFoundError("Could not find UCI HAR Dataset/train/X_train.txt after extraction.")


def load_data():
    ensure_dataset()
    train = DATASET_DIR / "train"
    test = DATASET_DIR / "test"
    X_train = pd.read_csv(train / "X_train.txt", sep=r"\s+", header=None)
    X_test = pd.read_csv(test / "X_test.txt", sep=r"\s+", header=None)
    y_train = pd.read_csv(train / "y_train.txt", sep=r"\s+", header=None).iloc[:, 0]
    y_test = pd.read_csv(test / "y_test.txt", sep=r"\s+", header=None).iloc[:, 0]
    labels = pd.read_csv(DATASET_DIR / "activity_labels.txt", sep=r"\s+", header=None, names=["id", "activity"])
    label_names = dict(zip(labels["id"], labels["activity"]))
    return X_train, X_test, y_train, y_test, label_names


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    X_train, X_test, y_train, y_test, label_names = load_data()
    print(f"Training rows: {len(X_train)}; test rows: {len(X_test)}; features: {X_train.shape[1]}")
    print("Activity labels:", ", ".join(f"{k}={v}" for k, v in sorted(label_names.items())))
    models = {
        "Decision Tree": DecisionTreeClassifier(random_state=42, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced", n_jobs=-1),
    }
    rows = []
    ordered_ids = sorted(label_names)
    ordered_names = [label_names[i] for i in ordered_ids]
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        row = {
            "model": name,
            "accuracy": accuracy_score(y_test, pred),
            "macro_precision": precision_score(y_test, pred, average="macro", zero_division=0),
            "macro_recall": recall_score(y_test, pred, average="macro", zero_division=0),
            "macro_f1": f1_score(y_test, pred, average="macro", zero_division=0),
        }
        rows.append(row)
        print("\n" + "=" * 60 + f"\n{name}\n" + "=" * 60)
        for metric in ["accuracy", "macro_precision", "macro_recall", "macro_f1"]:
            print(f"{metric}: {row[metric]:.4f}")
        print("\nClass-level report (descriptive pilot output):")
        print(classification_report(y_test, pred, labels=ordered_ids, target_names=ordered_names, zero_division=0))
        cm = confusion_matrix(y_test, pred, labels=ordered_ids)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=ordered_names)
        fig, ax = plt.subplots(figsize=(9, 7))
        disp.plot(ax=ax, xticks_rotation=45, colorbar=False)
        ax.set_title(f"{name}: UCI HAR official test split")
        fig.tight_layout()
        fig.savefig(RESULTS_DIR / (name.lower().replace(" ", "_") + "_confusion_matrix.png"), dpi=160)
        plt.close(fig)
    metrics = pd.DataFrame(rows)
    metrics.to_csv(RESULTS_DIR / "model_metrics.csv", index=False)
    print("\nSaved results/model_metrics.csv and confusion-matrix images.")
    print("Interpret results cautiously: this is activity classification on one public dataset, not clinical or medical-risk prediction.")

if __name__ == "__main__":
    main()
