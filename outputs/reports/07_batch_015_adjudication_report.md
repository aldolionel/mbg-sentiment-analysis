# Batch 015 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_015_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_015_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_015_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 4
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
| label_sample_0720 | gw masih gak ngerti sasaran program makan bergizi gratis ini buat siapa sih sebenarnya gw yg tolol apa emang berubah ubah sasarannya makansianggratis prabowogibran | netral | negatif | negatif | mengkritik sasaran program MBG yang tidak jelas |
| label_sample_0726 | makan tuh program makan bergizi gratis yang gak jelas dibalik program itu banyak sektor yang anggarannya dipangkas banyak yang nangis program jelek dipertahankan karena ego bodoh | netral | negatif | negatif | menyebut program tidak jelas dan jelek |
| label_sample_0749 | knapasi berita yg dari indonesia ni kalo bukan kucheng ngeliatin duel tikus buaya puraâ tenggelam sambil dadahâ ya program makan siang gratis yang ternyata basi dan tidak bergizi | netral | negatif | negatif | menilai program basi dan tidak bergizi |