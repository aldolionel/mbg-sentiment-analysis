# 00 Data Audit Verification

## Environment
- Python version: 3.12.3
- pandas version: 3.0.3
- numpy version: 2.4.6
- matplotlib version: 3.11.0
- seed: 42

## Repository/data status
- raw files found:
  - data crawl mbg (in).xlsx
  - data crawl mbg.xlsx
- selected dataset: data crawl mbg (in).xlsx
- selected sheet: Sheet1
- selected text column: full_text
- selected label column: None

## Dataset fingerprint
- n_rows: 73900
- n_features: 15
- sha256 first 12 chars: 669768ad5f72

## Data quality
- missing values top columns:
  - image_url: 0.7366
  - location: 0.5651
  - in_reply_to_screen_name: 0.4900
  - favorite_count: 0.0000
  - created_at: 0.0000
  - id_str: 0.0000
  - conversation_id_str: 0.0000
  - full_text: 0.0000
  - lang: 0.0000
  - quote_count: 0.0000
- duplicate row count: 3743
- duplicate text count: 6046
- duplicate text rate: 0.0818
- empty text count: 0
- average text length: 142.14
- median text length: 118.00
- average word count: 20.74
- median word count: 17.00

## Label summary
No existing label column detected

## Key findings
- Found 2 raw dataset file(s) in data/raw.
- Selected dataset is data crawl mbg (in).xlsx sheet Sheet1 with 73900 rows and 15 columns.
- Selected text column 'full_text' has 73900 non-null values, 0 empty strings, and 6046 duplicate text values.
- No existing label column was detected.

## Self-run acceptance checks
- PASS: at least one raw dataset found
- PASS: selected dataset has > 0 rows
- PASS: selected dataset has at least one inferred text column
- PASS: selected text column has non-null text
- PASS: duplicate text rate is reported
- PASS: figures were saved
- PASS: report file was saved

## Figures generated
- C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\00_raw_rows_by_file.png
- C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\00_missing_rate_top_columns.png
- C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\00_text_length_distribution.png

## Next recommended step
Prepare a cleaned interim dataset, then continue with labeling validation.