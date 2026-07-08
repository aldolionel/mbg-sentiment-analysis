# 02 Labeling Dataset Verification

## Environment
- Python version: 3.12.3
- pandas version: 3.0.3
- numpy version: 2.4.6
- seed: 42

## Scope
- Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis (MBG) pada Media Sosial Menggunakan Support Vector Machine (SVM)
- Prototype source: X/Twitter crawl
- No labeling, SVM modeling, or SMOTE was applied.

## Input/output
- input interim file: `data\interim\mbg_crawl_interim.csv`
- labeling-ready CSV: `data\processed\mbg_labeling_ready.csv`
- labeling sample CSV: `data\processed\mbg_labeling_sample_1000.csv`
- labeling sample XLSX: `data\processed\mbg_labeling_sample_1000.xlsx`

## Deduplication summary
- rows before: 73900
- rows after dedup: 62446
- duplicates removed: 11454
- duplicate removal rate: 0.1550

## Labeling sample
- sample rows: 1000
- requested sample size: 1000
- random state: 42
- length bins: 5

## Text statistics after deduplication
- average clean text length: 119.68
- median clean text length: 97.00
- average clean word count: 18.26
- median clean word count: 14.00

## Label columns
- `label`
- `label_source`
- `label_confidence`
- `annotator_1`
- `annotator_2`
- `adjudicated_label`
- `labeling_notes`

## Key findings
- Exact duplicate `clean_text` rows were removed while keeping the first occurrence.
- 11454 duplicate rows were removed.
- Label columns were added but intentionally left empty.
- A representative sample was created for manual or AI-assisted sentiment labeling.

## Self-run acceptance checks
- PASS: input interim file exists
- PASS: labeling-ready file exists
- PASS: sample CSV exists
- PASS: sample XLSX exists
- PASS: rows after dedup > 0
- PASS: duplicates removed > 0
- PASS: sample rows > 0
- PASS: sample rows <= requested size
- PASS: label columns are present
- PASS: label columns are empty
- PASS: no sentiment labels fabricated

## Next recommended step
- Review the labeling sample.
- Create a formal annotation workflow and label definitions.
- Perform manual or AI-assisted labeling without fabricating labels.
- After labels are validated, prepare train/test split and baseline modeling.