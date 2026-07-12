# 21 Thesis Rewrite Plan

## Bab 1
- Revisi background agar tidak mengklaim crawling sendiri.
- Revisi problem statement menjadi evaluasi workflow klasifikasi sentimen MBG pada dataset sekunder.
- Revisi objectives: membangun pipeline TF-IDF + SVM, mengevaluasi model pada label AI-assisted, dan menganalisis keterbatasan kelas negatif.
- Revisi benefits agar fokus pada kontribusi metodologis dan pembelajaran klasifikasi teks.
- Revisi limitations: dataset sekunder, label AI-assisted, class imbalance, dan keterbatasan gold validation.

## Bab 2
- Pertahankan referensi analisis sentimen, TF-IDF, SVM, evaluasi macro F1, dan class imbalance.
- Hapus referensi yang tidak dipakai dalam metodologi atau pembahasan.
- Tambahkan referensi Sultoni et al. (2025) sebagai sumber dataset.

## Bab 3
- Rename data collection menjadi secondary data source.
- Describe selected Sultoni dataset: X/Twitter, 47,803 posts, keyword-based scraping, Google Drive link in paper.
- Describe sampling 1,000 data untuk eksperimen tesis.
- Describe AI-assisted labeling and codebook.
- Describe evaluation design: split stratified 80/20, CV, macro F1, duplicate check, ablation.

## Bab 4
- Include dataset distribution.
- Include class-weight ablation.
- Include CV model selection caution.
- Include near-duplicate check result.
- Include negative-class error analysis.

## Bab 5
- Gunakan conclusion yang hati-hati: Tuned LinearSVC sebagai model final terpilih pada eksperimen ini.
- Hindari klaim opini publik universal.
- Jelaskan limitations: secondary dataset provenance, AI-assisted labels, class imbalance, limited human validation, possible duplicate/semantic similarity limits.