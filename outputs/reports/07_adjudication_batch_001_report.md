# 07 Adjudication Batch 001 Report

## Input Files
- original labeled batch: `data\processed\annotation_labeled_batches\annotation_batch_001_labeled.csv`
- semantic review CSV: `data\processed\annotation_reviews\annotation_batch_001_semantic_review.csv`
- adjudication XLSX: `data\processed\adjudication\annotation_batch_001_adjudication_template.xlsx`

## Output Files
- adjudicated batch CSV: `data\processed\annotation_labeled_batches\annotation_batch_001_adjudicated.csv`
- normalized adjudication CSV: `data\processed\adjudication\annotation_batch_001_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_adjudication_batch_001_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 24
- adjudicated rows: 50

## Final Label Source Counts
- human_label valid and used: 24
- final_label valid and used: 0
- fallback to current_label: 0

## Label Distribution Before Adjudication
- netral: 23
- negatif: 15
- positif: 12

## Label Distribution After Adjudication
- netral: 20
- negatif: 17
- positif: 13

## Changed Label Rows
| sample_id | clean_text | label_before_adjudication | label_after_adjudication | human_label | human_notes |
| --- | --- | --- | --- | --- | --- |
| label_sample_0003 | dapoer ibu boyolali terus salurkan mbg untuk para siswa | netral | positif | positif | seperti support mbg |
| label_sample_0023 | idiih minjem motor siapa lagi si mbg | netral | negatif | negatif | sindiran |
| label_sample_0029 | utk menyukseskan mbg asn perlu bekerja hari seminggu | netral | negatif | negatif | sindiran |

## Validation Checks
- PASS: final labels are allowed values
- PASS: no missing final labels
- PASS: no duplicate sample_id in adjudication
- PASS: all adjudication sample_id values exist in original labeled batch
- PASS: all adjudication sample_id values exist in semantic review

## Recommendation
- Batch 001 is ready to be included in the labeled dataset after researcher review of the changed rows.
- Do not proceed to model training until the full labeled dataset and validation protocol are complete.