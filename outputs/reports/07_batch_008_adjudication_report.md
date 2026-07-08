# Batch 008 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_008_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_008_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_008_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 3
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
| label_sample_0385 | iya yg saya heran tuh kata merata maksudnya apa sih sdh merata semua daerah dpt mbg | netral | negatif | negatif | mempertanyakan pemerataan MBG secara kritis |
| label_sample_0395 | yaallah makan gratis bergizi dari mana gue yg liatnya aja gak nafsu apalagi anak | netral | negatif | negatif | menilai makanan MBG tidak menggugah selera |