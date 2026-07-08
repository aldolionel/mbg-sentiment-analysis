# Batch 007 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_007_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_007_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_007_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 1
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
| label_sample_0337 | mirip siapa gitu yaa digencarkan program mbg ketimbang pendidikan gratis lagulama | netral | negatif | negatif | mengkritik prioritas MBG dibanding pendidikan gratis |