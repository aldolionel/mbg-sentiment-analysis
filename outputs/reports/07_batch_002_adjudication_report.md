# Batch 002 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_002_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_002_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_002_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 10
- adjudicated rows: 50
- changed label rows: 4

## Validation Checks
- PASS: final labels are allowed values
- PASS: no missing final labels
- PASS: no duplicate sample_id in adjudication
- PASS: all adjudication sample_id values exist in labeled batch
- PASS: all adjudication sample_id values exist in semantic review

## Changed Label Rows
| sample_id | clean_text | before | after | human_label | human_notes |
| --- | --- | --- | --- | --- | --- |
| label_sample_0051 | betul program mbg | netral | positif | positif | struktur kalimat tidak jelas tapi kalau dirangkai ulang mungkin hasilnya "program mbg bagus" |
| label_sample_0058 | mbg guys yokk | netral | positif | positif | cukup clear |
| label_sample_0084 | mikirin mbg ga kelarâ kapan mau mikir yg lain | netral | negatif | negatif | komen typo, maksudnya mikir mbg nggak selesai-selesai gmn mau mikir yang lain |
| label_sample_0091 | batalkan program mbg | netral | negatif | negatif | jelas, penolakan pada program |