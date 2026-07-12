# Paper Summary

## Title

Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis (MBG) pada Media Sosial Menggunakan Support Vector Machine

## Objective

Menyusun companion paper berbahasa Indonesia yang menjelaskan pipeline analisis sentimen MBG pada sampel teks media sosial, mulai dari data, labeling, preprocessing, baseline modeling, tuning SVM, hingga interpretasi hasil.

## Dataset

- dataset final: `data/processed/mbg_labeled_sample_1000.csv`
- jumlah data: 1.000 sampel berlabel
- label: `positif`, `negatif`, `netral`
- proses label: AI-assisted labeling dengan adjudication/manual review

Distribusi label:

- negatif: 116 (11.60%)
- netral: 472 (47.20%)
- positif: 412 (41.20%)

## Method

Metode utama menggunakan preprocessing teks media sosial, ekstraksi fitur TF-IDF, model baseline klasik, dan tuning model SVM. Evaluasi dilakukan dengan train/test split 80/20, stratifikasi label, 5-fold cross-validation untuk tuning, dan macro F1 sebagai metrik utama.

## Best Model

Model terbaik adalah **TF-IDF + Tuned LinearSVC**.

Parameter utama:

- `classifier__C=0.5`
- `classifier__class_weight="balanced"`
- `tfidf__max_df=0.9`
- `tfidf__min_df=3`
- `tfidf__ngram_range=(1, 2)`
- `tfidf__sublinear_tf=True`

## Key Results

- macro F1: 0.7278
- accuracy: 0.7950
- weighted F1: 0.7930
- improvement dari baseline Linear SVM: 3.06 percentage points macro F1

## Limitations

- Hasil hanya menggambarkan sampel berlabel, bukan opini publik universal.
- Label bersifat AI-assisted dengan adjudication/manual review.
- Kelas negatif merupakan kelas minoritas.
- F1 kelas negatif masih lebih rendah dibandingkan performa agregat model.

## Recommended Next Edits Before Submission

1. Tambahkan sitasi pustaka nyata untuk analisis sentimen, TF-IDF, SVM, dan evaluasi macro F1.
2. Sesuaikan gaya penulisan dengan template jurnal atau format kampus.
3. Masukkan gambar yang relevan dari `outputs/figures/`.
4. Tambahkan nomor tabel dan gambar.
5. Periksa ulang istilah metodologi agar konsisten dengan skripsi utama.
