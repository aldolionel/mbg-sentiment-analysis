# 12 Bulk Import Adjudication 003-020

## Summary
- total batches: 18
- total adjudicated rows: 900
- total adjudication rows: 104
- total changed label rows: 68

## Label Distribution After Import
- netral: 416
- positif: 388
- negatif: 96

## Batch Results
- batch 003: returncode 0, rows 50, changed 0, checks PASS
- batch 004: returncode 0, rows 50, changed 4, checks PASS
- batch 005: returncode 0, rows 50, changed 2, checks PASS
- batch 006: returncode 0, rows 50, changed 2, checks PASS
- batch 007: returncode 0, rows 50, changed 1, checks PASS
- batch 008: returncode 0, rows 50, changed 2, checks PASS
- batch 009: returncode 0, rows 50, changed 2, checks PASS
- batch 010: returncode 0, rows 50, changed 1, checks PASS
- batch 011: returncode 0, rows 50, changed 1, checks PASS
- batch 012: returncode 0, rows 50, changed 3, checks PASS
- batch 013: returncode 0, rows 50, changed 1, checks PASS
- batch 014: returncode 0, rows 50, changed 6, checks PASS
- batch 015: returncode 0, rows 50, changed 3, checks PASS
- batch 016: returncode 0, rows 50, changed 7, checks PASS
- batch 017: returncode 0, rows 50, changed 9, checks PASS
- batch 018: returncode 0, rows 50, changed 8, checks PASS
- batch 019: returncode 0, rows 50, changed 7, checks PASS
- batch 020: returncode 0, rows 50, changed 9, checks PASS

## Validation Checks
- PASS: all preflight checks passed
- PASS: all import commands succeeded
- PASS: all batch import checks passed

## Outputs
- finalized batch files: `data/processed/annotation_labeled_batches/annotation_batch_003_adjudicated.csv` through `data/processed/annotation_labeled_batches/annotation_batch_020_adjudicated.csv`
- per-batch normalized adjudication files: `data/processed/adjudication/annotation_batch_003_adjudication_normalized.csv` through `data/processed/adjudication/annotation_batch_020_adjudication_normalized.csv`
- aggregate summary JSON: `outputs\reports\12_bulk_import_adjudication_003_020_summary.json`

## Notes
Batches 001 and 002 were not processed by this bulk runner.
No model training, SMOTE, raw data modification, or automatic relabeling was performed.