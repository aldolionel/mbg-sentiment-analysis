# Batch 005 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_005_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_005_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_005_adjudication_summary.json`

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
| label_sample_0201 | mbg tai emang | netral | negatif | negatif | umpatan langsung terhadap MBG |
| label_sample_0247 | hah maksudnya apa sih meninjau mbg kok malah bagi skincare woy kerja yang bener | netral | negatif | negatif | kritik terhadap kegiatan peninjauan MBG |