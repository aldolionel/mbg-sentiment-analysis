# 20 Methodology Hardening Report

Generated at: 2026-07-12T15:34:37

## 1. Dataset Provenance dan Sampling Audit
- selected raw dataset: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\data\raw\data crawl mbg (in).xlsx`
- raw dataset exists locally: True
- dataset status: secondary dataset
- source provenance status: needs citation/source URL/license from dataset owner
- final labeled dataset: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\data\processed\mbg_labeled_sample_1000.csv`
- final labeled rows: 1000
- label distribution:
  - negatif: 116 (11.60%)
  - netral: 472 (47.20%)
  - positif: 412 (41.20%)

### Metadata Sampling
- available metadata columns: ['sample_id', 'clean_text', 'label']
- sample_id unique: True
- source_row_number exists: False
- source_row_number min/max: None / None
- sampling reproducible from existing columns: False
- random_state detected in docs: True
- sampling strategy detected in docs: True
- limitation: Exact original crawler identity, crawl date range, keywords, source URL, and license must be filled manually if not already documented by the dataset owner.

Interpretasi: dataset harus ditulis sebagai dataset sekunder. Detail identitas crawler asli, rentang tanggal crawl, keyword, URL sumber, dan lisensi tidak boleh diinventarisasi secara fiktif; bagian tersebut perlu dilengkapi manual dari pemilik dataset.

## 2. Class Weight Ablation
| model_name | class_weight | accuracy | precision_macro | recall_macro | f1_macro | f1_weighted |
| --- | --- | --- | --- | --- | --- | --- |
| LinearSVC class_weight=None | None | 0.7750 | 0.7409 | 0.6794 | 0.6991 | 0.7681 |
| LinearSVC class_weight="balanced" | balanced | 0.7650 | 0.7203 | 0.6828 | 0.6971 | 0.7609 |

Pada konfigurasi TF-IDF baseline, class_weight='balanced' mengubah macro F1 sebesar -0.0020 dibanding class_weight=None. Pada ablation ini, class_weight saja tidak menjelaskan peningkatan Tuned LinearSVC; peningkatan kemungkinan terkait kombinasi parameter TF-IDF, nilai C, dan variasi evaluasi. Jangan mengklaim hubungan kausal tunggal dari class_weight.

## 3. CV Model Selection Summary
| model_name | cv_mean_macro_f1 | cv_std_macro_f1 | test_macro_f1 | notes |
| --- | --- | --- | --- | --- |
| Logistic Regression | 0.7023 | 0.0189 | 0.7151 | Baseline CV mean/std available. |
| Tuned SVC Linear Kernel | 0.6966 | 0.0372 | 0.7249 | Best grid-search CV row per tuned SVM experiment. |
| Tuned LinearSVC | 0.6924 | 0.0298 | 0.7278 | Best grid-search CV row per tuned SVM experiment. |
| Tuned SVC RBF Kernel | 0.6917 | 0.0334 | 0.7247 | Best grid-search CV row per tuned SVM experiment. |
| Linear SVM | 0.6698 | 0.0180 | 0.6971 | Baseline CV mean/std available. |
| RBF SVM | 0.5829 | 0.0323 | 0.6072 | Baseline CV mean/std available. |
| Multinomial Naive Bayes | 0.5196 | 0.0141 | 0.5187 | Baseline CV mean/std available. |

Perbedaan CV mean macro F1 antar model tuned SVM hanya 0.0048. Model tuned SVM dengan CV mean tertinggi adalah Tuned SVC Linear Kernel, sedangkan Tuned LinearSVC dipilih karena test macro F1 tertinggi. Jadi, pemilihan Tuned LinearSVC terutama didasarkan pada test-set macro F1, sementara CV mendukung bahwa keluarga tuned SVM kompetitif tetapi tidak memberi bukti kuat bahwa Tuned LinearSVC unggul secara stabil atas tuned SVM lain.

Rekomendasi wording: gunakan frasa `model terpilih berdasarkan macro F1 pada eksperimen ini`, bukan `model terbaik secara universal`.

## 4. Near-Duplicate Train/Test Leakage Check
- test rows checked: 200
- threshold: TF-IDF cosine similarity >= 0.9
- near-duplicate test rows: 0
- percentage: 0.00%

Interpretasi: pemeriksaan ini mendeteksi kemiripan berbasis TF-IDF cosine similarity, bukan deteksi duplikasi semantik sempurna. Jika ditemukan near-duplicate, bahas sebagai potensi leakage atau risiko evaluasi yang terlalu optimistis.

## 5. Negative-Class Error Analysis Candidates
- best_svm_model.joblib available: True
- negative test rows: 23
- negative correct: 11
- negative errors: 12

Kategori review manual yang direkomendasikan:
- sarkasme
- kritik implisit
- negasi
- campuran
- konteks kurang
- label noisy
- model miss

## 6. Labeling/Codebook Documentation
Codebook dibuat/diupdate di `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\docs\annotation_codebook_mbg_sentiment.md`. Dokumen tersebut menegaskan scope sentimen terhadap Program MBG, definisi label, decision rules, workflow AI-assisted labeling, adjudication/manual review, dan rencana validasi gold-label.

## 7. Kesimpulan Hardening
Tuned LinearSVC tetap dapat diposisikan sebagai model final terpilih, dengan baseline Linear SVM macro F1 0.6971 dan Tuned LinearSVC macro F1 0.7278. Namun, kesimpulan harus menyebut keterbatasan provenance dataset sekunder, label AI-assisted, class imbalance, near-duplicate risk, dan belum adanya gold validation independen.