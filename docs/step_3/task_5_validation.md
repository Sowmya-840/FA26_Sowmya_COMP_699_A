# Step 3 — Task 5: Reproducibility verification

**Verified in the local working environment on November 16–17, 2026:** `python -m unittest discover -s src -p 'test_step3_analysis.py' -v` completed with four tests passing.

The tests cover (1) fixed-label N/V macro-F1 and confusion arithmetic using known synthetic fixtures, (2) duplicate record/sample key rejection, (3) non-N/V symbol rejection, and (4) rejection of records outside an allowed set. This validates the Step 3 metrics utility's limited behavior on test fixtures, **not** the correctness of expanded ECG predictions.

The existing Week 3 CSVs were read directly from the repository for a retrospective consistency review. Record-level false positives sum to GaussianNB 116 and RandomForest 796; false negatives sum to 465 and 12 respectively. These agree with the previously reported pooled counts.

**Still required for full reproducibility:** acquire and hash additional versioned MIT-BIH raw records, verify lead and class support, freeze subject groups, rerun feature extraction and models, record environment/protocol hashes, audit missing and excluded beats, verify no train/held-out subject leakage, save genuine per-beat predictions, and regenerate subject-level metrics. The execution environment could not resolve physionet.org, so none of these expanded-dataset steps has been completed.

Run tests: `python -m unittest discover -s src -p 'test_step3_analysis.py' -v`.

Run the Step 3 metrics tool **only after a real prediction CSV exists**: `python src/step3_analysis.py --predictions results/step_3/predictions.csv`. Required columns: `record_id,sample,true_label,majority,gaussian_nb,random_forest`. No fabricated predictions or empty results files are committed.
