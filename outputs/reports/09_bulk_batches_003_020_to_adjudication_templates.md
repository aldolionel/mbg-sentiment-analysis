# 09 Bulk Batches 003-020 to Adjudication Templates

Generated: 2026-07-07 20:33:41 +07:00

## Scope

Processed annotation batches 003 through 020 using the existing generic workflow and stopped after creating adjudication templates.

No adjudication import was run for batches 003-020. No adjudicated files were created for batches 003-020. Finalized batches 001 and 002 were not modified.

## Commands Run

For each batch from 003 through 020:

```powershell
python scripts/label_batch_rule_based.py --batch-id <batch>
python scripts/validate_labeled_batch.py --batch-id <batch>
python scripts/create_semantic_review.py --batch-id <batch>
python scripts/create_adjudication_template.py --batch-id <batch>
```

## Aggregate Results

- Batches processed: 18
- Total labeled rows: 900
- Total rows requiring adjudication review: 104
- Total adjudication template rows: 104
- Adjudicated outputs created for 003-020: 0
- Normalized adjudication outputs created for 003-020: 0

## Label Totals

- `netral`: 484
- `positif`: 383
- `negatif`: 33

## Batch Summary

| batch | labeled_rows | netral | positif | negatif | review_rows | adjudication_rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 003 | 50 | 39 | 8 | 3 | 6 | 6 |
| 004 | 50 | 41 | 9 | 0 | 13 | 13 |
| 005 | 50 | 33 | 16 | 1 | 2 | 2 |
| 006 | 50 | 26 | 23 | 1 | 2 | 2 |
| 007 | 50 | 24 | 26 | 0 | 1 | 1 |
| 008 | 50 | 29 | 20 | 1 | 3 | 3 |
| 009 | 50 | 28 | 22 | 0 | 2 | 2 |
| 010 | 50 | 22 | 26 | 2 | 2 | 2 |
| 011 | 50 | 22 | 28 | 0 | 2 | 2 |
| 012 | 50 | 24 | 25 | 1 | 3 | 3 |
| 013 | 50 | 21 | 27 | 2 | 3 | 3 |
| 014 | 50 | 22 | 24 | 4 | 7 | 7 |
| 015 | 50 | 23 | 23 | 4 | 4 | 4 |
| 016 | 50 | 25 | 23 | 2 | 9 | 9 |
| 017 | 50 | 24 | 23 | 3 | 11 | 11 |
| 018 | 50 | 28 | 19 | 3 | 11 | 11 |
| 019 | 50 | 30 | 18 | 2 | 13 | 13 |
| 020 | 50 | 23 | 23 | 4 | 10 | 10 |

## Outputs Created

For each batch 003-020:

- `data/processed/annotation_labeled_batches/annotation_batch_<batch>_labeled.csv`
- `outputs/reports/04_batch_<batch>_labeling_rule_based.md`
- `outputs/reports/04_batch_<batch>_validation.md`
- `data/processed/annotation_reviews/annotation_batch_<batch>_semantic_review.csv`
- `outputs/reports/05_batch_<batch>_semantic_review.md`
- `outputs/reports/05_batch_<batch>_semantic_review_summary.json`
- `data/processed/adjudication/annotation_batch_<batch>_adjudication_template.csv`
- `data/processed/adjudication/annotation_batch_<batch>_adjudication_template.xlsx`
- `outputs/reports/06_adjudication_template_batch_<batch>.md`

## Verification

- All input batches 003-020 existed before processing.
- All validation reports 003-020 contain PASS checks for row count and allowed labels.
- `data/processed/annotation_labeled_batches/annotation_batch_001_adjudicated.csv` exists.
- `data/processed/annotation_labeled_batches/annotation_batch_002_adjudicated.csv` exists.
- No `annotation_batch_003_adjudicated.csv` through `annotation_batch_020_adjudicated.csv` files were created.
- No `annotation_batch_003_adjudication_normalized.csv` through `annotation_batch_020_adjudication_normalized.csv` files were created.

## Next Step

Human reviewers should fill the adjudication templates for batches 003-020. Then import adjudication one batch at a time with:

```powershell
python scripts/import_adjudication_batch.py --batch-id 003
```

Proceed sequentially and inspect each adjudication report before moving to the next batch.
