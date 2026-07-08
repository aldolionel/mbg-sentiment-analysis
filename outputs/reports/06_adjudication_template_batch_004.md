# 06 Adjudication Template - Batch 004

## Summary
- total rows in semantic review: 50
- rows requiring review: 13

## Current Label Distribution Among Review Rows
- netral: 13

## Output Template Paths
- CSV: `data\processed\adjudication\annotation_batch_004_adjudication_template.csv`
- XLSX: `data\processed\adjudication\annotation_batch_004_adjudication_template.xlsx`

## Reviewer Instructions
Human reviewer should fill `human_label` with only:
- `positif`
- `negatif`
- `netral`

Reviewer may optionally fill `human_notes`.
If `human_label` is filled, `final_label` should usually match `human_label`.
If no correction is needed, `final_label` may match `current_label`.

Do not change `sample_id` or `clean_text`.
Do not add or remove rows from the adjudication template.