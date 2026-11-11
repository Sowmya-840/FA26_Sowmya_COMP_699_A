"""Audit V-beat errors and record influence using saved Week 2 predictions."""

import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "results/week_2"
OUT = ROOT / "results/week_3"
MODELS = ("majority", "gaussian_nb", "random_forest")


def counts(truth, prediction):
    actual_v, predicted_v = truth == "V", prediction == "V"
    return tuple(int(np.count_nonzero(mask)) for mask in (
        ~actual_v & ~predicted_v, ~actual_v & predicted_v,
        actual_v & ~predicted_v, actual_v & predicted_v,
    ))


def summarize(model, subset, tn, fp, fn, tp):
    def divide(a, b):
        return a / b if b else 0.0

    return dict(model=model, subset=subset, n_support=tn + fp, v_support=fn + tp,
                tn=tn, fp=fp, fn=fn, tp=tp, v_precision=divide(tp, tp + fp),
                v_recall=divide(tp, tp + fn), v_f1=divide(2 * tp, 2 * tp + fp + fn),
                macro_f1=(divide(2 * tp, 2 * tp + fp + fn)
                          + divide(2 * tn, 2 * tn + fp + fn)) / 2)


def write_rows(name, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run():
    with np.load(BASELINE / "predictions.npz", allow_pickle=False) as archive:
        records, samples, truth = (archive[key] for key in ("record_id", "sample", "true_label"))
        predictions = {model: archive[model] for model in MODELS}
    if truth.ndim != 1 or not truth.size or any(
        a.shape != truth.shape for a in (records, samples, *predictions.values())
    ):
        raise ValueError("Saved prediction arrays must be nonempty, aligned vectors")
    if len(set(zip(records, samples))) != truth.size:
        raise ValueError("Duplicate evaluation beat identifiers")
    if any(not np.isin(a, ("N", "V")).all() for a in (truth, *predictions.values())):
        raise ValueError("Only original N and V symbols are expected")
    record_ids = sorted(np.unique(records))
    if record_ids != ["100", "105", "200"]:
        raise ValueError(f"Unexpected evaluation records: {record_ids}")
    with (BASELINE / "confusion_matrices.csv").open(newline="") as source:
        original = {(r["model"], r["true_class"], r["predicted_class"]): int(r["count"])
                    for r in csv.DictReader(source)}

    by_record, sensitivity = [], []
    for model, prediction in predictions.items():
        pooled = counts(truth, prediction)
        published = tuple(original[model, a, b] for a, b in (("N", "N"), ("N", "V"), ("V", "N"), ("V", "V")))
        if pooled != published:
            raise ValueError(f"Published confusion counts disagree: {model}")
        record_counts = []
        sensitivity.append(summarize(model, "all_records", *pooled))
        for record in record_ids:
            selected = records == record
            row = counts(truth[selected], prediction[selected])
            record_counts.append(row)
            by_record.append(summarize(model, record, *row))
            remaining = counts(truth[~selected], prediction[~selected])
            if tuple(a + b for a, b in zip(row, remaining)) != pooled:
                raise ValueError(f"Record counts do not reconcile: {model}, {record}")
            sensitivity.append(summarize(model, f"exclude_{record}", *remaining))
        if tuple(map(sum, zip(*record_counts))) != pooled:
            raise ValueError(f"Record counts do not sum to the pooled counts: {model}")
    OUT.mkdir(parents=True, exist_ok=True)
    write_rows("v_errors_by_record.csv", by_record)
    write_rows("record_exclusion_sensitivity.csv", sensitivity)
    print(f"Checked {truth.size} unique evaluation beats and reconciled three confusion matrices.")


if __name__ == "__main__":
    run()
