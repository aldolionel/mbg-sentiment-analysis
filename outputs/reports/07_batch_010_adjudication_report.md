# Batch 010 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_010_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_010_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_010_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 2
- adjudicated rows: 50
- changed label rows: 1

## Validation Checks
- PASS: final labels are allowed values
- PASS: no missing final labels
- PASS: no duplicate sample_id in adjudication
- PASS: all adjudication sample_id values exist in labeled batch
- PASS: all adjudication sample_id values exist in semantic review

## Changed Label Rows
| sample_id | clean_text | before | after | human_label | human_notes |
| --- | --- | --- | --- | --- | --- |
| label_sample_0461 | siapa sih yg ngeyakinin dia program mbg bisa nguntungin dia eh salah nguntungin rakyat | netral | negatif | negatif | sarkasme soal manfaat MBG bagi rakyat |