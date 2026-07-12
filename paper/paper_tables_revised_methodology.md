# Paper Tables - Revised Methodology

## Tabel 1. Dataset Provenance Summary

| Aspek | Keterangan |
| --- | --- |
| Status dataset | Dataset sekunder |
| File mentah terpilih | `data/raw/data crawl mbg (in).xlsx` |
| Sumber | Sultoni et al. (2025), Jurnal Matematika Thales, 7(1), 35-53 |
| Platform | X/Twitter |
| Ukuran dataset sumber | 47,803 posts |
| Metode pengumpulan sumber | Keyword-based scraping |
| Contoh keyword | "Makan Bergizi Gratis", "Program Gizi", "Stunting", hashtag terkait |
| Akses dataset sumber | Google Drive link disebutkan dalam paper sumber |
| Status lisensi | License not explicitly identified from available local documents |

## Tabel 2. Final Label Distribution

| Label | Jumlah | Persentase |
| --- | ---: | ---: |
| Negatif | 116 | 11.60% |
| Netral | 472 | 47.20% |
| Positif | 412 | 41.20% |

## Tabel 3. Baseline Model Results

| Model | Accuracy | Precision Macro | Recall Macro | Macro F1 | Weighted F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.7750 | 0.7164 | 0.7211 | 0.7151 | 0.7784 |
| Linear SVM baseline | 0.7650 | 0.7203 | 0.6828 | 0.6971 | 0.7609 |
| RBF SVM baseline | 0.7600 | 0.7359 | 0.5997 | 0.6072 | 0.7351 |
| Multinomial Naive Bayes | 0.7300 | 0.4958 | 0.5484 | 0.5187 | 0.6869 |

## Tabel 4. Tuned SVM Results

| Model | Accuracy | Precision Macro | Recall Macro | Macro F1 | Weighted F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Tuned LinearSVC | 0.7950 | 0.7455 | 0.7160 | 0.7278 | 0.7930 |
| Tuned SVC Linear Kernel | 0.7950 | 0.7475 | 0.7138 | 0.7249 | 0.7938 |
| Tuned SVC RBF Kernel | 0.7950 | 0.7506 | 0.7132 | 0.7247 | 0.7937 |

## Tabel 5. Class-Weight Ablation

| Model | Class Weight | Accuracy | Precision Macro | Recall Macro | Macro F1 | Weighted F1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| LinearSVC | None | 0.7750 | 0.7409 | 0.6794 | 0.6991 | 0.7681 |
| LinearSVC | balanced | 0.7650 | 0.7203 | 0.6828 | 0.6971 | 0.7609 |

## Tabel 6. CV Model Selection Caution

| Model | CV Mean Macro F1 | CV Std Macro F1 | Test Macro F1 | Catatan |
| --- | ---: | ---: | ---: | --- |
| Logistic Regression | 0.7023 | 0.0189 | 0.7151 | Baseline CV tertinggi |
| Tuned SVC Linear Kernel | 0.6966 | 0.0372 | 0.7249 | Tuned SVM dengan CV mean tertinggi |
| Tuned LinearSVC | 0.6924 | 0.0298 | 0.7278 | Test macro F1 tertinggi |
| Tuned SVC RBF Kernel | 0.6917 | 0.0334 | 0.7247 | Selisih kecil dari tuned SVM lain |

## Tabel 7. Negative-Class Error Analysis Summary

| Item | Nilai |
| --- | ---: |
| Negative test rows | 23 |
| Correct negative rows | 11 |
| Negative error rows | 12 |
| Tema utama error | kritik implisit, sarkasme, konteks kurang, model miss |

## Tabel 8. Limitations and Mitigation

| Limitation | Mitigation / Wording |
| --- | --- |
| Dataset sekunder | Jelaskan provenance Sultoni et al. (2025) dan hindari klaim crawling sendiri |
| License belum jelas | Tulis "license not explicitly identified from available local documents" |
| Label AI-assisted | Jelaskan adjudication/manual review dan jangan klaim pure manual gold standard |
| Cohen's Kappa belum tersedia | Tulis bahwa dua anotator manusia belum menyelesaikan validasi |
| Class imbalance | Gunakan macro F1 dan bahas kelas negatif secara khusus |
| CV antar tuned SVM kecil | Gunakan wording hati-hati untuk model final |
| Near-duplicate check terbatas | Jelaskan bahwa cek memakai TF-IDF cosine similarity, bukan semantic duplicate detection |
