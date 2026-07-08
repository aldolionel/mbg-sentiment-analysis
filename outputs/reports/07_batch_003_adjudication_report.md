# Batch 003 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_003_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_003_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_003_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 6
- adjudicated rows: 50
- changed label rows: 0

## Validation Checks
- PASS: final labels are allowed values
- PASS: no missing final labels
- PASS: no duplicate sample_id in adjudication
- PASS: all adjudication sample_id values exist in labeled batch
- PASS: all adjudication sample_id values exist in semantic review

## Changed Label Rows
- none