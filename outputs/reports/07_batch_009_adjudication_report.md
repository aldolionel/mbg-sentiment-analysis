# Batch 009 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_009_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_009_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_009_adjudication_summary.json`

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
| label_sample_0404 | mbg kan mau didanain mereka dgn syarat ambil barang dari mereka jg jadi yg bego siapa | netral | negatif | negatif | menyindir skema pendanaan/pengadaan MBG |
| label_sample_0444 | gak heran lh mereka kerja kan gotong royong gak apa lah toh urusan mbg menteri hutan jg ikut kok | netral | negatif | negatif | sindiran terhadap koordinasi/gotong royong urusan MBG |