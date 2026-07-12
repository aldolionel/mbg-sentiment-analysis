# 20 Rewrite Notes After Critical Review

## Framing Dataset
- Ganti framing `crawling sendiri` menjadi `dataset sekunder`.
- Tulis dataset mentah terpilih sebagai `data/raw/data crawl mbg (in).xlsx`.
- Tambahkan catatan bahwa sumber URL, pemilik dataset, lisensi, periode crawl, dan keyword crawl perlu dilengkapi manual dari pemilik dataset.

## Framing Gap Penelitian
- Hindari novelty berbasis platform saja.
- Ganti gap menjadi gap metodologi/evaluasi: workflow klasifikasi sentimen MBG pada dataset sekunder, label AI-assisted, class imbalance, dan evaluasi SVM dengan macro F1.

## Alternatif Judul
Studi Klasifikasi Sentimen MBG pada Dataset Sekunder Media Sosial X dengan TF-IDF dan SVM

## Revisi Rumusan Masalah
- Fokus pada workflow klasifikasi dan performa model pada label AI-assisted yang imbalanced.
- Jelaskan bahwa tujuan bukan mengukur opini publik universal, melainkan mengevaluasi klasifikasi sentimen pada sampel berlabel.

## Revisi Limitations
- Dataset sekunder dan provenance masih perlu dilengkapi.
- Label AI-assisted dengan adjudication/manual review, bukan pure manual gold standard.
- Class imbalance, terutama kelas negatif.
- Gold validation masih terbatas/belum tersedia.
- Near-duplicate train/test memungkinkan dan sudah dicek menggunakan TF-IDF cosine similarity, tetapi bukan deteksi semantik sempurna.

## Revisi Kesimpulan
- Hindari klaim opini publik universal.
- Hindari klaim tuning saja menyebabkan peningkatan kecuali ablation mendukung secara hati-hati.
- Posisikan Tuned LinearSVC sebagai model final terpilih berdasarkan macro F1 dengan wording hati-hati.