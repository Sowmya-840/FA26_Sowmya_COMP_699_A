# Selective evaluation expansion

The six-record baseline is retained. The revised eight-record design uses training records 106, 108, 119, inspected evaluation records 100, 105, 200 and additional evaluation records 203, 208. The latter are not used for training or tuning. The documented shared-subject pair 201/202 is excluded; independent patient identity verification beyond the dataset record mapping has not been performed.

Six user-supplied files were inspected locally. Both headers specify 360 Hz, 650000 samples per channel, MLII and V1. Decoding packed format 212 samples reproduced both initial ADC values and both modulo-65536 checksums for each record. Binary annotation parsing counted 2529 N and 444 V for 203, and 1586 N and 992 V for 208 (5551 target annotations before window exclusions). Local SHA-256 hashes are recorded, not independently matched to provider hashes. Raw files are not committed.

The original 27-feature protocol and classifier settings remain unchanged. The additional evaluation has not been executed. Original training inputs or recoverable fitted models are required. Existing baseline predictions may be reused only after consistency verification.

Task 1: selective design and local input validation completed, subject mapping caveat noted. Task 2: expanded classifier execution pending. Tasks 3 and 4: retrospective analysis completed, additional-record performance pending. Task 5: input integrity checks completed, full rerun and additional unit tests pending. Task 6: this supplemental progress note records the milestone; consolidated final report pending.

Source: https://physionet.org/content/mitdb/1.0.0/ and supplied recording files.
