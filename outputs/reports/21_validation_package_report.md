# 21 Validation Package Report

## Ringkasan
- Paket ini menyiapkan template validasi AI-assisted/proxy untuk review manusia.
- Cohen's Kappa belum dihitung karena belum ada dua anotator independen manusia.
- Template tidak mengisi `annotator_1_label`, `annotator_2_label`, atau `final_gold_label`.
- File AI-prefilled hanya mengisi `ai_suggested_label` dan `ai_suggested_notes`.

## Sampling
- source dataset: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\data\processed\mbg_labeled_sample_1000.csv`
- sampling: stratified 200-row sample where possible
- random_state: 42
- label distribution:
  - negatif: 23
  - netral: 94
  - positif: 83

## Output Files
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\data\processed\validation\validation_sample_200_template.csv`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\data\processed\validation\validation_sample_200_template.xlsx`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\data\processed\validation\validation_sample_200_ai_prefilled.csv`

## Instructions for Human Annotators
- Gunakan `docs/annotation_codebook_mbg_sentiment.md` sebagai pedoman label.
- Isi `annotator_1_label` dan `annotator_1_notes` untuk anotator pertama.
- Isi `annotator_2_label` dan `annotator_2_notes` untuk anotator kedua.
- Gunakan label yang valid: `positif`, `negatif`, `netral`.
- Setelah dua anotator selesai, lakukan adjudication dan isi `final_gold_label` serta `adjudication_notes`.
- Jalankan `python scripts/compute_validation_kappa.py <path_to_annotated_csv>` untuk menghitung Cohen's Kappa.

## Limitation
File AI-prefilled bukan gold standard manusia. File tersebut hanya membantu persiapan review dan tidak boleh dipakai untuk mengklaim validasi manusia.