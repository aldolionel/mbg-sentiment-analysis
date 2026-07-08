# 03 Annotation Batches Verification

## Environment
- Python version: 3.12.3
- pandas version: 3.0.3
- seed: 42

## Scope
- Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis (MBG) pada Media Sosial Menggunakan Support Vector Machine (SVM)
- Prototype source: X/Twitter crawl
- No external API calls were made.
- No sentiment labels were generated.

## Input/output
- labeling sample: `data\processed\mbg_labeling_sample_1000.csv`
- sample rows: 1000
- batch size: 50
- batch count: 20
- prompt count: 20
- batch directory: `data\processed\annotation_batches`
- prompt directory: `data\processed\annotation_prompts`

## Batch columns
- `sample_id`
- `clean_text`
- `label`
- `labeling_notes`

## Key findings
- Created 20 sequential annotation batch CSV files.
- Created 20 matching Markdown prompt files.
- Batch label fields remain empty for manual or AI-assisted annotation.
- Prompts require CSV output with `sample_id,label,labeling_notes`.

## Self-run acceptance checks
- PASS: sample file exists
- PASS: sample rows > 0
- PASS: batch count > 0
- PASS: prompt count equals batch count
- PASS: batch rows total equals sample rows
- PASS: all batch labels are empty
- PASS: no labels generated
- PASS: summary JSON exists
- PASS: verification report exists

## Next recommended step
- Label one batch at a time using the guideline.
- Import completed batch outputs and validate allowed labels.
- Resolve disagreements before model training.