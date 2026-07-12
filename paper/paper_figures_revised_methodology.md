# Paper Figures - Revised Methodology

## Gambar 1. Distribusi Label Final

- File: `outputs/figures/16_final_label_distribution.png`
- Caption: **Distribusi label pada 1.000 sampel berlabel terkait MBG.**
- Placement: Hasil dan Pembahasan, subbagian distribusi dataset.
- Interpretation: Menunjukkan class imbalance, terutama kelas negatif sebagai minoritas.

## Gambar 2. Perbandingan Macro F1 Antar Model

- File: `outputs/figures/16_model_comparison_macro_f1.png`
- Caption: **Perbandingan macro F1 pada model baseline dan model tuned SVM.**
- Placement: Hasil dan Pembahasan, setelah tabel baseline dan tuned SVM.
- Interpretation: Tuned LinearSVC memiliki test macro F1 tertinggi, tetapi perlu dibaca bersama ringkasan CV.

## Gambar 3. Accuracy vs Macro F1

- File: `outputs/figures/16_model_comparison_accuracy_vs_macro_f1.png`
- Caption: **Perbandingan accuracy dan macro F1 untuk menyoroti dampak class imbalance.**
- Placement: Hasil dan Pembahasan, setelah Gambar 2.
- Interpretation: Accuracy tidak cukup sebagai satu-satunya metrik karena kelas negatif minoritas.

## Gambar 4. Peningkatan Linear SVM

- File: `outputs/figures/16_linear_svm_improvement.png`
- Caption: **Peningkatan macro F1 dari Linear SVM baseline ke Tuned LinearSVC.**
- Placement: Subbagian SVM tuning.
- Interpretation: Tuning meningkatkan test macro F1, tetapi class-weight ablation menunjukkan class_weight saja tidak menjelaskan peningkatan.

## Gambar 5. Confusion Matrix Tuned LinearSVC

- File: `outputs/figures/15_confusion_matrix_tuned_linearsvc.png`
- Caption: **Confusion matrix model TF-IDF + Tuned LinearSVC pada data uji.**
- Placement: Setelah pembahasan model final.
- Interpretation: Membantu melihat pola kesalahan prediksi antar kelas.

## Gambar 6. Negative-Class Performance

- File: `outputs/figures/16_negative_class_performance_tuned_svm.png`
- Caption: **Precision, recall, dan F1 kelas negatif pada model tuned SVM.**
- Placement: Subbagian negative-class error analysis atau keterbatasan.
- Interpretation: Menunjukkan bahwa kelas negatif masih menjadi tantangan utama.

## Gambar Opsional 7. Top Terms Clean Text

- File: belum tersedia.
- Caption: **Kata atau frasa yang paling sering muncul pada clean text.**
- Placement: Metodologi atau eksplorasi dataset.
- Interpretation: Dapat membantu pembaca memahami karakteristik teks, tetapi perlu dibuat dari data bersih dan tidak mengandung informasi sensitif.

## Gambar Opsional 8. Text Length Distribution Clean

- File: belum tersedia.
- Caption: **Distribusi panjang teks setelah preprocessing.**
- Placement: Metodologi atau data exploration.
- Interpretation: Dapat menunjukkan karakteristik teks pendek media sosial dan membantu menjelaskan pemilihan model TF-IDF.
