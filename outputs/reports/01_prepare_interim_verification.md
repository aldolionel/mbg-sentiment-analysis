# 01 Prepare Interim Dataset Verification

## Environment
- Python version: 3.12.3
- pandas version: 3.0.3
- numpy version: 2.4.6
- matplotlib version: 3.11.0
- seed: 42

## Scope note
- Current dataset is X/Twitter crawl, not TikTok.
- Project scope has been corrected to social media MBG sentiment analysis.
- The workflow remains generic for short informal social media text.

## Input/output
- raw input file: `data\raw\data crawl mbg (in).xlsx`
- sheet: `Sheet1`
- text column: `full_text`
- interim CSV path: `data\interim\mbg_crawl_interim.csv`
- interim shape: 73900 rows x 9 columns
- interim columns:
  - `interim_id`
  - `source_file`
  - `source_sheet`
  - `source_row_number`
  - `clean_text`
  - `clean_text_length`
  - `clean_word_count`
  - `is_empty_clean_text`
  - `is_duplicate_clean_text`

## Cleaning results
- empty clean text count: 0
- duplicate original text count: 5991
- duplicate clean text count: 11454
- duplicate clean text rate: 0.1550
- rows containing @ in clean_text: 0
- rows containing http in clean_text: 0

## Privacy check
- forbidden identifier columns:
  - `username`
  - `user_id`
  - `id_str`
  - `conversation_id_str`
  - `location`
  - `image_url`
  - `profile_url`
  - `screen_name`
  - `author`
  - `nickname`
  - `name`
- privacy check: PASS
- forbidden columns present in interim CSV: none

## Key findings
- The current prototype dataset is X/Twitter crawl data for MBG.
- Interim dataset contains 73900 rows.
- The interim output does not include raw identifier columns from the forbidden list.
- Clean text contains no @ symbols and no http strings after conservative cleaning.
- Duplicate clean text remains an important data-quality issue: 11454 rows are duplicate clean text (0.1550).

## Self-run acceptance checks
- PASS: interim file exists
- PASS: final row count > 0
- PASS: required columns exist
- PASS: clean_text or clean_text_basic column exists
- PASS: no empty clean text
- PASS: no @ in clean text
- PASS: no http in clean text
- PASS: no forbidden identifier columns in interim output
- PASS: summary JSON exists
- PASS: verification report exists

## Next recommended step
- Deduplicate by clean text.
- Create labeling dataset.
- Design AI-assisted or lexicon-assisted sentiment labeling.