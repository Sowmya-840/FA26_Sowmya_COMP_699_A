"""Step 3 subject-level audit of genuine predictions; no generated classifier scores.
Input CSV columns: record_id,sample,true_label,majority,gaussian_nb,random_forest
Run: python src/step3_analysis.py --predictions results/step_3/predictions.csv
"""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

MODELS = ('majority', 'gaussian_nb', 'random_forest')
LABELS = {'N', 'V'}

def metrics(rows, model):
    c = Counter((r['true_label'], r[model]) for r in rows)
    tn, fp, fn, tp = (c['N', 'N'], c['N', 'V'], c['V', 'N'], c['V', 'V'])
    def div(a, b): return a / b if b else 0.0
    f1_n = div(2 * tn, 2 * tn + fp + fn)
    f1_v = div(2 * tp, 2 * tp + fp + fn)
    return dict(model=model, beats=len(rows), n_support=tn+fp, v_support=fn+tp,
                tn=tn, fp=fp, fn=fn, tp=tp,
                v_precision=div(tp, tp+fp), v_recall=div(tp, tp+fn),
                v_f1=f1_v, macro_f1=(f1_n+f1_v)/2,
                accuracy=div(tn+tp, len(rows)))

def validate(rows, expected_records=None):
    if not rows: raise ValueError('No predictions provided')
    seen = set()
    for row in rows:
        for field in ('record_id', 'sample', 'true_label', *MODELS):
            if field not in row: raise ValueError('Missing column: ' + field)
        key = (row['record_id'], row['sample'])
        if key in seen: raise ValueError('Duplicate beat key: ' + repr(key))
        seen.add(key)
        if any(row[field] not in LABELS for field in ('true_label', *MODELS)):
            raise ValueError('Invalid target/prediction symbol')
        if expected_records is not None and row['record_id'] not in expected_records:
            raise ValueError('Unexpected record: ' + row['record_id'])
    return True

def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def analyze(rows):
    validate(rows)
    by_record = defaultdict(list)
    for row in rows:
        by_record[row['record_id']].append(row)
    pooled = [dict(scope='pooled', record_id='all', **metrics(rows, m)) for m in MODELS]
    per_record = [dict(scope='record', record_id=rid, **metrics(group, m))
                  for rid, group in sorted(by_record.items()) for m in MODELS]
    for model in MODELS:
        total = next(r for r in pooled if r['model'] == model)
        for field in ('tn', 'fp', 'fn', 'tp', 'beats'):
            assert sum(r[field] for r in per_record if r['model'] == model) == total[field]
    return pooled, per_record

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--predictions', required=True)
    p.add_argument('--out', default='results/step_3')
    args = p.parse_args()
    with open(args.predictions, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    pooled, per_record = analyze(rows)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / 'pooled_metrics.csv', pooled)
    write_csv(out / 'subject_metrics.csv', per_record)
    summary = {'records': sorted(set(r['record_id'] for r in rows)), 'beats': len(rows),
               'warning': 'Descriptive, record-level analysis; not clinical validation or a blind holdout guarantee.'}
    (out / 'audit.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
