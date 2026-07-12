# Paper Tables

## Tabel 1. Distribusi Label Dataset Final

| Label | Jumlah | Persentase |
| --- | ---: | ---: |
| Negatif | 116 | 11.60% |
| Netral | 472 | 47.20% |
| Positif | 412 | 41.20% |

## Tabel 2. Hasil Model Baseline pada Data Uji

| Model | Accuracy | Precision Macro | Recall Macro | Macro F1 | Weighted F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 0.7750 | 0.7164 | 0.7211 | 0.7151 | 0.7784 |
| Linear SVM baseline | 0.7650 | 0.7203 | 0.6828 | 0.6971 | 0.7609 |
| RBF SVM baseline | 0.7600 | 0.7359 | 0.5997 | 0.6072 | 0.7351 |
| Multinomial Naive Bayes | 0.7300 | 0.4958 | 0.5484 | 0.5187 | 0.6869 |

## Tabel 3. Hasil Tuning SVM pada Data Uji

| Model | Accuracy | Precision Macro | Recall Macro | Macro F1 | Weighted F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Tuned LinearSVC | 0.7950 | 0.7455 | 0.7160 | 0.7278 | 0.7930 |
| Tuned SVC Linear Kernel | 0.7950 | 0.7475 | 0.7138 | 0.7249 | 0.7938 |
| Tuned SVC RBF Kernel | 0.7950 | 0.7506 | 0.7132 | 0.7247 | 0.7937 |

## Tabel 4. Parameter Model Terbaik

| Komponen | Parameter | Nilai |
| --- | --- | --- |
| Classifier | `classifier__C` | 0.5 |
| Classifier | `classifier__class_weight` | balanced |
| TF-IDF | `tfidf__max_df` | 0.90 |
| TF-IDF | `tfidf__min_df` | 3 |
| TF-IDF | `tfidf__ngram_range` | (1, 2) |
| TF-IDF | `tfidf__sublinear_tf` | True |

## Tabel 5. Performa Kelas Negatif pada Model Tuned SVM

| Model | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Tuned LinearSVC | 0.5789 | 0.4783 | 0.5238 | 23 |
| Tuned SVC Linear Kernel | 0.5500 | 0.4783 | 0.5116 | 23 |
| Tuned SVC RBF Kernel | 0.5500 | 0.4783 | 0.5116 | 23 |
