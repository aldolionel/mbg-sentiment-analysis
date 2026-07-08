# Batch 006 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_006_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_006_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_006_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 2
- adjudicated rows: 50
- changed label rows: 2

## Validation Checks
- PASS: final labels are allowed values
- PASS: no missing final labels
- PASS: no duplicate sample_id in adjudication
- PASS: all adjudication sample_id values exist in labeled batch
- PASS: all adjudication sample_id values exist in semantic review

## Changed Label Rows
| sample_id | clean_text | before | after | human_label | human_notes |
| --- | --- | --- | --- | --- | --- |
| label_sample_0255 | salah gambarnya di mana sih ada mbg yg sayur dan lauknya sebanyak itu | netral | negatif | negatif | skeptis terhadap kualitas/menu MBG |
| label_sample_0286 | nasi kotak buat artis pasti budgetnya k up gak sih lah mbg berapa | netral | negatif | negatif | membandingkan anggaran MBG secara kritis |