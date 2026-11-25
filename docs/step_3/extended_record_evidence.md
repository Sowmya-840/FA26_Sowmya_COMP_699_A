# Extended record-level evidence

## Acquisition
Attempts to download record 101 header from PhysioNet and its AWS mirror failed with DNS resolution errors. The expanded record split remains provisional. No new classifier training or held-out predictions were performed.

## Existing-record comparison
Derived from results/week_3/v_errors_by_record.csv using FP/N support, FN/V support, TN/N support, TP/(TP+FP), and TP/V support. Zero denominators are reported as zero, consistent with the existing metric convention. Pooled counts cover 6504 N and 867 V beats. Gaussian NB has pooled macro-F1 0.768504 and equally weighted record macro-F1 0.785201; Random Forest has 0.806505 and 0.737039 respectively. The ordering reverses under equal record weighting. Record 100 has only one V beat, making its V metrics unstable. These are descriptive comparisons, not independent validation.

## Error distribution
RF false-positive rates for records 100, 105, 200 are 0.0447%, 16.5149%, 21.6992%; GNB rates are 0%, 3.9208%, 0.9759%. RF pooled V recall is 98.6159% versus GNB 46.3668%. Waveform explanations and preprocessing effects remain untested.

## Evidence
results/step_3/existing_record_error_rates.csv and existing_record_macro_summary.csv contain arithmetic derived from genuine committed confusion counts. No new prediction arrays were generated.

## Remaining work
Tasks 1 and 3–5 remain partial in their original expanded-experiment scope; Task 2 remains incomplete for expanded classifier training. The retrospective metric and error-rate extensions are complete. Full reproducibility and waveform intervention require raw recordings.
