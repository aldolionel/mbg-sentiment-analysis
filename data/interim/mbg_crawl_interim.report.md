# 01 Prepare Interim Dataset Report

## Source
- input file: `data\raw\data crawl mbg (in).xlsx`
- sheet: `Sheet1`
- text column: `full_text`
- sha256 first 12 chars: `669768ad5f72`

## Output
- output file: `data\interim\mbg_crawl_interim.csv`
- raw personal identifiers: not exported
- raw text: not exported

## Row Counts
- raw rows: 73900
- interim rows: 73900

## Clean Text Quality
- empty clean text count: 0
- duplicate clean text count: 11454
- duplicate clean text rate: 0.1550
- average clean text length: 120.20
- median clean text length: 99.00
- average clean word count: 18.00
- median clean word count: 14.00

## Columns Exported
- `interim_id`
- `source_file`
- `source_sheet`
- `source_row_number`
- `clean_text`
- `clean_text_length`
- `clean_word_count`
- `is_empty_clean_text`
- `is_duplicate_clean_text`

## Notes
- This stage performs conservative basic cleaning only.
- No stemming, stopword removal, sentiment labeling, SMOTE, or modeling was applied.
- Mentions and URLs were removed to reduce exposure of personal identifiers.