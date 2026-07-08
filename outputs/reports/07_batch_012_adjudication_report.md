# Batch 012 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_012_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_012_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_012_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 3
- adjudicated rows: 50
- changed label rows: 3

## Validation Checks
- PASS: final labels are allowed values
- PASS: no missing final labels
- PASS: no duplicate sample_id in adjudication
- PASS: all adjudication sample_id values exist in labeled batch
- PASS: all adjudication sample_id values exist in semantic review

## Changed Label Rows
| sample_id | clean_text | before | after | human_label | human_notes |
| --- | --- | --- | --- | --- | --- |
| label_sample_0554 | pemimpin dunia mana yang mau belajar mbg dari indonesia cepat kau kasih tau mana siapa yeuu kocak | netral | negatif | negatif | mengejek klaim dunia belajar MBG |
| label_sample_0574 | mari kita lihat siapa ajah investornya boleh spill dan ihsg anjlok karena invest ke mbg ups | netral | negatif | negatif | mengaitkan MBG dengan investor/IHSG secara sinis |
| label_sample_0595 | lagi kepikiran kan yg dapet mbg kan anak sekolah ya trs yg ga sekolah ttp dapet apa ga ya | netral | negatif | negatif | mempertanyakan cakupan penerima di luar anak sekolah |