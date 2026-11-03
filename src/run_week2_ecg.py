"""Week 2 ECG experiment. Run from repository root or src; raw data downloads on first run."""

from pathlib import Path
import json, hashlib, platform, importlib.metadata, time
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import wfdb
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, precision_recall_fscore_support, confusion_matrix
ROOT = Path.cwd().resolve()
if ROOT.name == "src": ROOT = ROOT.parent
assert (ROOT / "src/week2_protocol.json").exists(), "Run from the repository root or src folder"
RAW = ROOT / "data/raw"
OUT = ROOT / "results/week_2"
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
PROTOCOL_BYTES = (ROOT / "src/week2_protocol.json").read_bytes()
P = json.loads(PROTOCOL_BYTES)
STARTED = datetime.now(timezone.utc).isoformat()
RECORDS = P["train_records"] + P["evaluation_records"]
print("Training records:", P["train_records"])
print("Evaluation records:", P["evaluation_records"])
print("Class labels:", P["classes"], "| fixed RF seed:", P["random_forest"]["random_state"])


from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
BASE = "https://physionet.org/files/mitdb/1.0.0/"
def obtain_file(item):
    rid, extension = item
    name = rid + "." + extension
    dest = RAW / name
    if not dest.exists() or dest.stat().st_size == 0:
        with urlopen(BASE + name, timeout=45) as response:
            content = response.read()
        if not content: raise ValueError("Empty input: " + name)
        temporary = dest.with_suffix(dest.suffix + ".part")
        temporary.write_bytes(content)
        temporary.replace(dest)
    content = dest.read_bytes()
    return {"record_id": rid, "file": name, "bytes": len(content), "url": BASE + name, "sha256": hashlib.sha256(content).hexdigest()}
items = [(rid, ext) for rid in RECORDS for ext in ["hea", "dat", "atr"]]
with ThreadPoolExecutor(max_workers=6) as pool:
    download_rows = list(pool.map(obtain_file, items))
(OUT / "download_manifest.json").write_text(json.dumps({"dataset_version": "1.0.0", "files": download_rows}, indent=2) + "\n")
print("Verified nonempty local inputs:", len(download_rows))


BEAT_SYMBOLS = set(["N", "L", "R", "B", "A", "a", "J", "S", "V", "r", "F", "e", "j", "n", "E", "/", "f", "Q", "?"])
FEATURES = ["previous_rr_seconds", "raw_std_mv", "raw_peak_to_peak_mv"] + [f"morphology_{i:02d}" for i in range(P["morphology_samples"])]
def subject_group(rid):
    return "shared_201_202" if rid in {"201", "202"} else "subject_" + rid

def beat_features(window, previous_rr):
    x = np.asarray(window, dtype=float)
    if x.ndim != 1 or len(x) != P["samples_before"] + P["samples_after_exclusive"]: raise ValueError("Invalid beat window")
    if not np.isfinite(x).all() or not np.isfinite(previous_rr) or previous_rr <= 0: raise ValueError("Invalid numerical input")
    std = x.std(ddof=0)
    if std <= 1e-12: raise ValueError("Constant beat window")
    normalized = (x - x.mean()) / std
    morphology = np.interp(np.linspace(0, len(x)-1, P["morphology_samples"]), np.arange(len(x)), normalized)
    return np.r_[previous_rr, std, np.ptp(x), morphology]

feature_rows, audit_rows, symbol_rows, exclusion_rows = [], [], [], []
for rid in RECORDS:
    record = wfdb.rdrecord(str(RAW / rid))
    ann = wfdb.rdann(str(RAW / rid), "atr")
    assert record.fs == P["fs_hz"] and P["lead"] in record.sig_name
    assert len(ann.sample) == len(ann.symbol) and np.all(np.diff(ann.sample) >= 0)
    assert np.all(ann.sample >= 0) and np.all(ann.sample < record.sig_len)
    lead = record.p_signal[:, record.sig_name.index(P["lead"])]
    assert np.isfinite(lead).all() and len(lead) == record.sig_len
    beat_indices = [i for i, symbol in enumerate(ann.symbol) if symbol in BEAT_SYMBOLS]
    preceding = {current: int(ann.sample[previous]) for previous, current in zip(beat_indices, beat_indices[1:])}
    counts = pd.Series(ann.symbol).value_counts()
    for symbol, count in counts.items(): symbol_rows.append({"record_id": rid, "symbol": symbol, "count": int(count)})
    target_count, included = 0, 0
    for index, (sample, symbol) in enumerate(zip(ann.sample, ann.symbol)):
        if symbol not in P["classes"]: continue
        target_count += 1
        sample = int(sample); start = sample - P["samples_before"]; end = sample + P["samples_after_exclusive"]
        reason = None
        if index not in preceding: reason = "no_previous_reference_beat"
        elif start < 0 or end > len(lead): reason = "incomplete_window"
        else:
            try: features = beat_features(lead[start:end], (sample-preceding[index])/record.fs)
            except ValueError: reason = "invalid_or_constant_window"
        if reason:
            exclusion_rows.append({"record_id": rid, "sample": sample, "label": symbol, "reason": reason}); continue
        feature_rows.append({"record_id": rid, "subject_id": subject_group(rid), "sample": sample, "label": symbol, "partition": "train" if rid in P["train_records"] else "evaluation", **dict(zip(FEATURES, features))})
        included += 1
    audit_rows.append({"record_id": rid, "subject_id": subject_group(rid), "partition": "train" if rid in P["train_records"] else "evaluation", "lead": P["lead"], "fs_hz": record.fs, "all_annotation_entries": len(ann.sample), "target_annotations": target_count, "included": included, "excluded_targets": target_count-included})
beats = pd.DataFrame(feature_rows)
audit = pd.DataFrame(audit_rows)
audit.to_csv(OUT / "record_audit.csv", index=False)
pd.DataFrame(symbol_rows).to_csv(OUT / "annotation_counts.csv", index=False)
pd.DataFrame(exclusion_rows, columns=["record_id", "sample", "label", "reason"]).to_csv(OUT / "excluded_targets.csv", index=False)
support = beats.groupby(["partition", "record_id", "label"]).size().unstack(fill_value=0).reindex(columns=P["classes"], fill_value=0)
support.to_csv(OUT / "class_support.csv")
beats.groupby("record_id", sort=False).head(2).to_csv(OUT / "feature_examples.csv", index=False)
print("Feature count:", len(FEATURES)); print(support.to_string()); print("Target exclusions:", len(exclusion_rows))


checks = {}
def check(name, condition):
    checks[name] = bool(condition)
    if not checks[name]: raise AssertionError(name)

def rejects(window, rr):
    try: beat_features(window, rr)
    except ValueError: return True
    return False
known = np.arange(216, dtype=float)
f = beat_features(known, .75)
check("known_feature_length_27", f.shape == (27,))
check("known_previous_rr", np.isclose(f[0], .75))
check("known_std", np.isclose(f[1], np.sqrt((216**2-1)/12)))
check("known_peak_to_peak", np.isclose(f[2], 215))
check("known_morphology_endpoints", np.allclose(f[[3,-1]], ((known-known.mean())/known.std())[[0,-1]]))
check("reject_constant_window", rejects(np.ones(216), 1))
check("reject_nonfinite_window", rejects(np.r_[np.nan, np.ones(215)], 1))
check("reject_wrong_window_length", rejects(np.arange(215), 1))
check("reject_nonpositive_rr", rejects(known, 0))
check("same_subject_201_202_grouped", subject_group("201") == subject_group("202"))
check("distinct_selected_records", len(set(RECORDS)) == len(RECORDS))
train = beats.loc[beats.partition == "train"].copy()
evaluation = beats.loc[beats.partition == "evaluation"].copy()
check("subject_disjoint", set(train.subject_id).isdisjoint(evaluation.subject_id))
check("record_disjoint", set(train.record_id).isdisjoint(evaluation.record_id))
check("unique_record_sample_keys", not beats.duplicated(["record_id", "sample"]).any())
check("finite_features", np.isfinite(beats[FEATURES].to_numpy()).all())
check("both_classes_in_training", set(train.label) == set(P["classes"]))
check("both_classes_in_evaluation", set(evaluation.label) == set(P["classes"]))
check("audit_target_accounting", int(audit.target_annotations.sum()) == len(beats)+len(exclusion_rows))
# A known classification example independently checks evaluation math.
check("known_macro_f1", np.isclose(f1_score(["N","N","V","V"], ["N","V","V","V"], labels=P["classes"], average="macro"), 11/15))
check("known_confusion_matrix", np.array_equal(confusion_matrix(["N","N","V","V"], ["N","V","V","V"], labels=P["classes"]), [[1,1],[0,2]]))
print("Pre-fit checks passed:", len(checks))


X_train = train[FEATURES].to_numpy(); y_train = train.label.to_numpy()
X_eval = evaluation[FEATURES].to_numpy(); y_eval = evaluation.label.to_numpy()
models = {
    "majority": DummyClassifier(strategy="most_frequent"),
    "gaussian_nb": make_pipeline(StandardScaler(), GaussianNB(**P["gaussian_nb"])),
    "random_forest": make_pipeline(StandardScaler(), RandomForestClassifier(**P["random_forest"]))
}
metric_rows, class_rows, matrix_rows, record_metric_rows = [], [], [], []
predictions = {}; durations = {}
for name, model in models.items():
    start_time = time.perf_counter(); model.fit(X_train, y_train); pred = model.predict(X_eval)
    durations[name] = time.perf_counter()-start_time; predictions[name] = pred
    check(name + "_predictions_valid", len(pred)==len(y_eval) and set(pred)<=set(P["classes"]))
    if name != "majority":
        check(name + "_scaler_train_only", np.allclose(model[0].mean_, X_train.mean(axis=0)) and int(model[0].n_samples_seen_)==len(X_train))
    metric_rows.append({"model": name, "accuracy": accuracy_score(y_eval, pred), "balanced_accuracy": balanced_accuracy_score(y_eval, pred), "macro_f1": f1_score(y_eval, pred, labels=P["classes"], average="macro", zero_division=0)})
    precision, recall, f1, counts = precision_recall_fscore_support(y_eval, pred, labels=P["classes"], zero_division=0)
    for i, label in enumerate(P["classes"]): class_rows.append({"model": name, "class": label, "precision": precision[i], "recall": recall[i], "f1": f1[i], "support": int(counts[i])})
    matrix = confusion_matrix(y_eval, pred, labels=P["classes"])
    check(name + "_confusion_total", matrix.sum()==len(y_eval))
    for i, true_label in enumerate(P["classes"]):
        for j, predicted_label in enumerate(P["classes"]): matrix_rows.append({"model": name, "true_class": true_label, "predicted_class": predicted_label, "count": int(matrix[i,j])})
    for rid in P["evaluation_records"]:
        mask = evaluation.record_id.to_numpy()==rid
        record_metric_rows.append({"model": name, "record_id": rid, "beats": int(mask.sum()), "macro_f1": f1_score(y_eval[mask], pred[mask], labels=P["classes"], average="macro", zero_division=0), "accuracy": accuracy_score(y_eval[mask], pred[mask])})
metrics = pd.DataFrame(metric_rows); per_class = pd.DataFrame(class_rows)
metrics.to_csv(OUT / "metrics_summary.csv", index=False)
per_class.to_csv(OUT / "metrics_by_class.csv", index=False)
pd.DataFrame(matrix_rows).to_csv(OUT / "confusion_matrices.csv", index=False)
pd.DataFrame(record_metric_rows).to_csv(OUT / "metrics_by_record.csv", index=False)
# Compact, complete per-beat predictions: decoded with np.load, allow_pickle=False.
np.savez_compressed(OUT / "predictions.npz", record_id=evaluation.record_id.to_numpy(dtype="U3"), sample=evaluation["sample"].to_numpy(dtype=np.int64), true_label=y_eval.astype("U1"), **{name: pred.astype("U1") for name,pred in predictions.items()})
print(metrics.to_string(index=False)); print("\nPer-class results:\n", per_class.to_string(index=False))


second_rf = make_pipeline(StandardScaler(), RandomForestClassifier(**P["random_forest"]))
second_rf.fit(X_train, y_train)
check("same_seed_rf_predictions_repeated", np.array_equal(second_rf.predict(X_eval), predictions["random_forest"]))
check("protocol_unchanged_during_execution", (ROOT/"src/week2_protocol.json").read_bytes()==PROTOCOL_BYTES)
validation = pd.DataFrame([{"check": name, "passed": passed} for name, passed in checks.items()])
validation.to_csv(OUT / "validation_checks.csv", index=False)
fig, axes = plt.subplots(1, 3, figsize=(10, 3.3))
for ax, (name, pred) in zip(axes, predictions.items()):
    matrix = confusion_matrix(y_eval, pred, labels=P["classes"])
    ax.imshow(matrix, cmap="Blues")
    for i in range(2):
        for j in range(2): ax.text(j, i, str(matrix[i,j]), ha="center", va="center", color="white" if matrix[i,j] > matrix.max()/2 else "black")
    ax.set(xticks=[0,1], yticks=[0,1], xticklabels=P["classes"], yticklabels=P["classes"], xlabel="Predicted", ylabel="Reference", title=name.replace("_", " "))
fig.suptitle("Initial ECG evaluation: raw beat counts")
fig.tight_layout(); fig.savefig(OUT/"confusion_matrices.png", dpi=160); plt.close(fig)
versions = {name: importlib.metadata.version(name) for name in ["numpy", "pandas", "scipy", "matplotlib", "wfdb", "scikit-learn"]}
summary = {"started_utc": STARTED, "completed_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(), "packages": versions, "protocol": P, "protocol_sha256": hashlib.sha256(PROTOCOL_BYTES).hexdigest(), "feature_names": FEATURES, "training_beats": len(train), "evaluation_beats": len(evaluation), "features": len(FEATURES), "checks_passed": len(checks), "same_seed_repeatability": True, "run_seconds_by_model_including_prediction": durations, "raw_file_hashes": {r["file"]: r["sha256"] for r in download_rows}, "feature_matrix_sha256": hashlib.sha256(np.ascontiguousarray(beats[FEATURES].to_numpy(dtype="<f8")).tobytes()).hexdigest(), "clinical_validation": False, "note": "One fixed development comparison. Ground-truth beat locations are used. No fitted quantities use evaluation rows."}
(OUT/"execution_summary.json").write_text(json.dumps(summary, indent=2)+"\n")
print("Training beats:", len(train), "| evaluation beats:", len(evaluation))
print("Validation checks passed:", len(checks))
print(pd.DataFrame(record_metric_rows).to_string(index=False))
