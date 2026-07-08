# 13 Labeled Dataset 1000 Report

## Scope
Dataset ini menggabungkan batch final/adjudicated 001 sampai 020 sebagai sampel berlabel untuk persiapan modeling sentimen MBG pada media sosial.
Tidak ada training model, SMOTE, modifikasi raw data, atau pelabelan ulang otomatis.

## Input Batch Files
- `data\processed\annotation_labeled_batches\annotation_batch_001_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_002_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_003_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_004_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_005_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_006_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_007_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_008_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_009_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_010_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_011_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_012_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_013_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_014_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_015_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_016_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_017_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_018_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_019_adjudicated.csv`
- `data\processed\annotation_labeled_batches\annotation_batch_020_adjudicated.csv`

## Row Summary
- total rows: 1000

## Rows Per Batch
- batch 001: 50
- batch 002: 50
- batch 003: 50
- batch 004: 50
- batch 005: 50
- batch 006: 50
- batch 007: 50
- batch 008: 50
- batch 009: 50
- batch 010: 50
- batch 011: 50
- batch 012: 50
- batch 013: 50
- batch 014: 50
- batch 015: 50
- batch 016: 50
- batch 017: 50
- batch 018: 50
- batch 019: 50
- batch 020: 50

## Final Label Distribution
- negatif: 116 (11.60%)
- netral: 472 (47.20%)
- positif: 412 (41.20%)

## Adjudication Summary
- adjudication applied count: 138
- changed label count: 75

## Validation Checks
- PASS: all 20 finalized batch files exist
- PASS: each batch has 50 rows
- PASS: total rows equals 1000
- PASS: no missing batch_id
- PASS: no duplicate sample_id
- PASS: no missing clean_text
- PASS: no missing label
- PASS: labels are allowed values

## Output File Paths
- CSV: `data\processed\mbg_labeled_sample_1000.csv`
- XLSX: `data\processed\mbg_labeled_sample_1000.xlsx`
- report: `outputs\reports\13_labeled_dataset_1000_report.md`
- summary JSON: `outputs\reports\13_labeled_dataset_1000_summary.json`

## Recommendation
Dataset siap untuk tahap persiapan modeling. Pada penulisan tesis, label sebaiknya dijelaskan sebagai hasil AI-assisted labeling dengan proses adjudication/manual review.