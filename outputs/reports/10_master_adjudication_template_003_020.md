# 10 Master Adjudication Template 003-020

## Summary
- total rows: 104
- batch range: 003-020

## Rows Per Batch
- batch 003: 6
- batch 004: 13
- batch 005: 2
- batch 006: 2
- batch 007: 1
- batch 008: 3
- batch 009: 2
- batch 010: 2
- batch 011: 2
- batch 012: 3
- batch 013: 3
- batch 014: 7
- batch 015: 4
- batch 016: 9
- batch 017: 11
- batch 018: 11
- batch 019: 13
- batch 020: 10

## Current Label Distribution
- netral: 104

## Output File Paths
- CSV: `data\processed\adjudication\master_adjudication_template_003_020.csv`
- XLSX: `data\processed\adjudication\master_adjudication_template_003_020.xlsx`
- report: `outputs\reports\10_master_adjudication_template_003_020.md`
- summary JSON: `outputs\reports\10_master_adjudication_template_003_020_summary.json`

## Validation Checks
- PASS: total rows equals sum of all template rows
- PASS: no missing batch_id
- PASS: no missing sample_id
- PASS: no duplicate batch_id + sample_id pairs
- PASS: current_label values are allowed labels

## Reviewer Instruction
Fill only `human_label`, `human_notes`, and `final_label`.
Allowed labels are:
- `positif`
- `negatif`
- `netral`

Do not change `batch_id`, `sample_id`, `clean_text`, `current_label`, `labeling_notes`, or `review_reason`.