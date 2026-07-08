# Ringkasan Hasil

Dokumen ini merangkum hasil akhir pemodelan untuk kebutuhan penulisan skripsi. Ringkasan ini bersifat thesis-friendly dan masih dapat disesuaikan dengan gaya penulisan kampus.

## Dataset Final

Dataset final yang digunakan pada tahap pemodelan adalah `data/processed/mbg_labeled_sample_1000.csv` dengan total 1.000 data berlabel. Dataset ini merupakan sampel dari hasil crawl media sosial terkait Program Makan Bergizi Gratis (MBG).

Label sentimen disusun melalui AI-assisted labeling dengan adjudication/manual review. Oleh karena itu, hasil penelitian harus dibaca sebagai analisis terhadap sampel berlabel, bukan sebagai klaim universal mengenai opini publik.

## Distribusi Label

Distribusi label final:

| Label | Jumlah | Persentase |
| --- | ---: | ---: |
| negatif | 116 | 11.60% |
| netral | 472 | 47.20% |
| positif | 412 | 41.20% |

Distribusi tersebut menunjukkan adanya ketidakseimbangan kelas, terutama karena kelas `negatif` memiliki jumlah data paling sedikit. Oleh sebab itu, macro F1 digunakan sebagai metrik utama dalam pemilihan model.

## Baseline Results

Eksperimen baseline membandingkan Multinomial Naive Bayes, Logistic Regression, Linear SVM, dan RBF SVM menggunakan fitur TF-IDF.

Ringkasan performa test set:

| Model | Accuracy | Macro F1 |
| --- | ---: | ---: |
| Logistic Regression | 0.7750 | 0.7151 |
| Linear SVM baseline | 0.7650 | 0.6971 |
| RBF SVM baseline | 0.7600 | 0.6072 |
| Multinomial Naive Bayes | 0.7300 | 0.5187 |

Logistic Regression menjadi baseline non-SVM terkuat, sedangkan Linear SVM menjadi baseline SVM terbaik sebelum tuning.

## SVM Tuning Results

Tuning dilakukan pada LinearSVC, SVC linear kernel, dan SVC RBF kernel. Ringkasan hasil test set:

| Model | Accuracy | Macro F1 |
| --- | ---: | ---: |
| Tuned LinearSVC | 0.7950 | 0.7278 |
| Tuned SVC Linear Kernel | 0.7950 | 0.7249 |
| Tuned SVC RBF Kernel | 0.7950 | 0.7247 |

Tuned LinearSVC memberikan macro F1 tertinggi dan menjadi model terbaik dalam eksperimen ini.

## Best Model

Model yang direkomendasikan:

**TF-IDF + Tuned LinearSVC**

Parameter utama:

- `classifier__C=0.5`
- `classifier__class_weight="balanced"`
- `tfidf__max_df=0.9`
- `tfidf__min_df=3`
- `tfidf__ngram_range=(1, 2)`
- `tfidf__sublinear_tf=True`

Performa:

- accuracy: 0.7950
- macro F1: 0.7278
- weighted F1: 0.7930

## Negative-Class Limitation

Walaupun Tuned LinearSVC menjadi model terbaik secara keseluruhan, performa kelas `negatif` masih lebih rendah dibandingkan performa agregat. Pada model Tuned LinearSVC, F1 kelas `negatif` adalah 0.5238 dengan recall 0.4783.

Kondisi ini perlu dibahas sebagai keterbatasan penelitian karena kelas `negatif` merupakan kelas minoritas.

## Suggested Figures to Use in Thesis

Urutan gambar yang disarankan untuk Bab Hasil dan Pembahasan:

1. `outputs/figures/16_final_label_distribution.png`
2. `outputs/figures/16_model_comparison_macro_f1.png`
3. `outputs/figures/16_model_comparison_accuracy_vs_macro_f1.png`
4. `outputs/figures/16_linear_svm_improvement.png`
5. `outputs/figures/15_confusion_matrix_tuned_linearsvc.png`
6. `outputs/figures/16_negative_class_performance_tuned_svm.png`
