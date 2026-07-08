# Batch 004 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_004_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_004_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_004_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 13
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
| label_sample_0155 | kok hampir semua kementrian pd ngotot mbg ada apa | netral | negatif | negatif | nada curiga terhadap dorongan kementerian pada MBG |
| label_sample_0159 | ompreng penjara mbg | netral | negatif | negatif | asosiasi ompreng penjara bernada merendahkan MBG |
| label_sample_0198 | mbg tuh apa ya kak makanan babi gendut kahh | netral | negatif | negatif | candaan/ejekan terhadap istilah MBG |
| label_sample_0199 | setidaknya biar jelas maunya apa mbg | netral | negatif | negatif | menyiratkan ketidakjelasan arah MBG |