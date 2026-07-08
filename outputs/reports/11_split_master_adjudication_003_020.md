# 11 Split Master Adjudication 003-020

## Input
- reviewed master workbook: `data\processed\adjudication\master_adjudication_template_003_020_REVIEWED_AI.xlsx`

## Summary
- total rows: 104

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

## Final Label Distribution Overall
- negatif: 63
- netral: 36
- positif: 5

## Final Label Distribution Per Batch
- batch 003: netral: 6
- batch 004: negatif: 4, netral: 9
- batch 005: negatif: 2
- batch 006: negatif: 2
- batch 007: negatif: 1
- batch 008: negatif: 2, netral: 1
- batch 009: negatif: 2
- batch 010: negatif: 1, netral: 1
- batch 011: negatif: 1, netral: 1
- batch 012: negatif: 3
- batch 013: negatif: 1, netral: 2
- batch 014: negatif: 6, netral: 1
- batch 015: negatif: 3, netral: 1
- batch 016: negatif: 7, netral: 2
- batch 017: negatif: 6, netral: 2, positif: 3
- batch 018: negatif: 6, netral: 3, positif: 2
- batch 019: negatif: 7, netral: 6
- batch 020: negatif: 9, netral: 1

## Validation Checks
- PASS: batch_id only from 003 through 020
- PASS: no missing batch_id
- PASS: no missing sample_id
- PASS: no duplicate batch_id + sample_id pairs
- PASS: human_label values are allowed labels
- PASS: final_label values are allowed labels
- PASS: total rows equals 104
- PASS: batch 003 row count matches template
- PASS: batch 003 sample_id values exist in template
- PASS: batch 004 row count matches template
- PASS: batch 004 sample_id values exist in template
- PASS: batch 005 row count matches template
- PASS: batch 005 sample_id values exist in template
- PASS: batch 006 row count matches template
- PASS: batch 006 sample_id values exist in template
- PASS: batch 007 row count matches template
- PASS: batch 007 sample_id values exist in template
- PASS: batch 008 row count matches template
- PASS: batch 008 sample_id values exist in template
- PASS: batch 009 row count matches template
- PASS: batch 009 sample_id values exist in template
- PASS: batch 010 row count matches template
- PASS: batch 010 sample_id values exist in template
- PASS: batch 011 row count matches template
- PASS: batch 011 sample_id values exist in template
- PASS: batch 012 row count matches template
- PASS: batch 012 sample_id values exist in template
- PASS: batch 013 row count matches template
- PASS: batch 013 sample_id values exist in template
- PASS: batch 014 row count matches template
- PASS: batch 014 sample_id values exist in template
- PASS: batch 015 row count matches template
- PASS: batch 015 sample_id values exist in template
- PASS: batch 016 row count matches template
- PASS: batch 016 sample_id values exist in template
- PASS: batch 017 row count matches template
- PASS: batch 017 sample_id values exist in template
- PASS: batch 018 row count matches template
- PASS: batch 018 sample_id values exist in template
- PASS: batch 019 row count matches template
- PASS: batch 019 sample_id values exist in template
- PASS: batch 020 row count matches template
- PASS: batch 020 sample_id values exist in template

## Output Paths Generated
- `data\processed\adjudication\annotation_batch_003_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_003_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_004_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_004_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_005_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_005_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_006_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_006_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_007_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_007_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_008_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_008_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_009_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_009_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_010_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_010_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_011_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_011_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_012_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_012_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_013_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_013_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_014_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_014_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_015_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_015_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_016_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_016_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_017_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_017_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_018_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_018_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_019_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_019_adjudication_template_reviewed.csv`
- `data\processed\adjudication\annotation_batch_020_adjudication_template.xlsx`
- `data\processed\adjudication\annotation_batch_020_adjudication_template_reviewed.csv`

## Recommendation
After successful split, run the adjudication import script for batches 003 through 020.