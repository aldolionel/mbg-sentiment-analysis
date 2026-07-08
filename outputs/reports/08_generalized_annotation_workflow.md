# 08 Generalized Annotation Workflow

## Scope

Generalized the annotation workflow so remaining batches can be processed one batch at a time.

No remaining batches were labeled automatically. Finalized batch 001 was not changed.

## Generic Scripts

### 1. Local Codex-Style Labeling Aid

```powershell
python scripts/label_batch_with_codex.py --batch-id 002
```

Creates:

- `data/processed/annotation_labeled_batches/annotation_batch_002_labeled.csv`
- `outputs/reports/04_batch_002_labeling_with_codex.md`

Notes:

- Does not call external APIs.
- Labels one explicitly requested batch only.
- Refuses to overwrite an existing labeled output unless `--overwrite` is passed.
- Output labels should still be manually reviewed.

### 2. Validate Labeled Batch

```powershell
python scripts/validate_labeled_batch.py --batch-id 002
```

Creates:

- `outputs/reports/04_batch_002_validation.md`

### 3. Semantic Review

```powershell
python scripts/create_semantic_review.py --batch-id 002
```

Creates:

- `data/processed/annotation_reviews/annotation_batch_002_semantic_review.csv`
- `outputs/reports/05_batch_002_semantic_review.md`
- `outputs/reports/05_batch_002_semantic_review_summary.json`

### 4. Adjudication Template

```powershell
python scripts/create_adjudication_template.py --batch-id 002
```

Creates:

- `data/processed/adjudication/annotation_batch_002_adjudication_template.csv`
- `data/processed/adjudication/annotation_batch_002_adjudication_template.xlsx`
- `outputs/reports/06_adjudication_template_batch_002.md`

### 5. Import Adjudication and Finalize Batch

```powershell
python scripts/import_adjudication_batch.py --batch-id 002
```

Creates:

- `data/processed/annotation_labeled_batches/annotation_batch_002_adjudicated.csv`
- `data/processed/adjudication/annotation_batch_002_adjudication_normalized.csv`
- `outputs/reports/07_batch_002_adjudication_report.md`
- `outputs/reports/07_batch_002_adjudication_summary.json`

## Recommended Batch-by-Batch Flow

1. Run `label_batch_with_codex.py` for one batch.
2. Run `validate_labeled_batch.py`.
3. Run `create_semantic_review.py`.
4. Review rows marked `review`.
5. Run `create_adjudication_template.py`.
6. Human reviewer fills the adjudication XLSX.
7. Run `import_adjudication_batch.py`.
8. Inspect the final adjudication report before moving to the next batch.

## Verification

- Python compilation passed for all generalized scripts.
- CLI help was checked for all generalized scripts.
- `annotation_batch_001_adjudicated.csv` still exists.
- `annotation_batch_002_labeled.csv` was not created during this generalization step.

## Constraints Preserved

- No SVM modeling.
- No SMOTE.
- No raw file changes.
- No automatic labeling of all remaining batches.
- Labels remain constrained to `positif`, `negatif`, `netral`.
