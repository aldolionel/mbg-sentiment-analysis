# Paper Figures

## Gambar 1. Distribusi Label Dataset Final

- File: `outputs/figures/16_final_label_distribution.png`
- Suggested caption: **Distribusi label sentimen pada 1.000 sampel teks media sosial terkait MBG.**
- Placement: Bagian Hasil dan Pembahasan, sebelum perbandingan model.
- Interpretation: Gambar ini menunjukkan bahwa kelas `negatif` merupakan kelas minoritas, sehingga macro F1 lebih sesuai digunakan sebagai metrik utama.

## Gambar 2. Perbandingan Model Berdasarkan Macro F1

- File: `outputs/figures/16_model_comparison_macro_f1.png`
- Suggested caption: **Perbandingan performa model berdasarkan macro F1 pada data uji.**
- Placement: Bagian Hasil dan Pembahasan, setelah penjelasan model baseline dan tuning.
- Interpretation: Tuned LinearSVC memiliki macro F1 tertinggi dan menjadi model terbaik dalam eksperimen.

## Gambar 3. Perbandingan Accuracy dan Macro F1

- File: `outputs/figures/16_model_comparison_accuracy_vs_macro_f1.png`
- Suggested caption: **Perbandingan accuracy dan macro F1 untuk model baseline dan model SVM hasil tuning.**
- Placement: Bagian Hasil dan Pembahasan, setelah Gambar 2.
- Interpretation: Accuracy dan macro F1 perlu dilihat bersama karena dataset tidak seimbang.

## Gambar 4. Peningkatan Linear SVM Setelah Tuning

- File: `outputs/figures/16_linear_svm_improvement.png`
- Suggested caption: **Peningkatan macro F1 dari baseline Linear SVM ke Tuned LinearSVC.**
- Placement: Subbagian SVM tuning results.
- Interpretation: Tuning meningkatkan macro F1 sekitar 3.06 percentage points dibandingkan Linear SVM baseline.

## Gambar 5. Confusion Matrix Model Terbaik

- File: `outputs/figures/15_confusion_matrix_tuned_linearsvc.png`
- Suggested caption: **Confusion matrix model TF-IDF + Tuned LinearSVC pada data uji.**
- Placement: Setelah pembahasan model terbaik.
- Interpretation: Gambar ini membantu melihat pola prediksi benar dan salah pada masing-masing kelas sentimen.

## Gambar 6. Performa Kelas Negatif pada Tuned SVM

- File: `outputs/figures/16_negative_class_performance_tuned_svm.png`
- Suggested caption: **Precision, recall, dan F1 kelas negatif pada model SVM hasil tuning.**
- Placement: Subbagian keterbatasan atau negative-class discussion.
- Interpretation: F1 kelas negatif masih lebih rendah dibandingkan performa keseluruhan, sehingga class imbalance perlu dibahas sebagai keterbatasan.
