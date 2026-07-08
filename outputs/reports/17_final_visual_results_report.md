# 17 Final Visual Results Report

## Scope
This report documents thesis-ready visualization assets created from existing final modeling comparison outputs. No models were retrained, no labels were changed, and no raw files were modified.

## Input Files
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\data\processed\mbg_labeled_sample_1000.csv`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\reports\16_final_modeling_comparison_table.csv`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\reports\16_final_modeling_comparison_summary.json`

## Output Figures
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_final_label_distribution.png`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_final_label_distribution_pie.png`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_model_comparison_macro_f1.png`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_model_comparison_accuracy_vs_macro_f1.png`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_linear_svm_improvement.png`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_negative_class_performance_tuned_svm.png`
- existing final model confusion matrix: `outputs/figures/15_confusion_matrix_tuned_linearsvc.png`

## Key Numbers
- total rows: 1000
- final label distribution:
  - negatif: 116 (11.60%)
  - netral: 472 (47.20%)
  - positif: 412 (41.20%)
- best model: Tuned LinearSVC + TF-IDF
- best macro F1: 0.7278
- improvement from baseline Linear SVM: 0.0306 (3.06 percentage points)

## Catatan Interpretasi Gambar
### Distribusi Label
Grafik distribusi label menunjukkan bahwa sampel berlabel didominasi oleh kelas `netral` dan `positif`, sedangkan kelas `negatif` memiliki proporsi paling kecil. Kondisi ini menjelaskan mengapa evaluasi model perlu menekankan macro F1, bukan hanya akurasi.

### Perbandingan Model
Grafik perbandingan macro F1 memperlihatkan bahwa model hasil tuning SVM berada pada peringkat teratas. Tuned LinearSVC menjadi model terbaik berdasarkan macro F1 pada data uji.

### Peningkatan Tuning SVM
Grafik peningkatan Linear SVM menunjukkan adanya kenaikan macro F1 setelah tuning hyperparameter. Peningkatan ini mendukung pemilihan Tuned LinearSVC sebagai model yang direkomendasikan.

### Keterbatasan Kelas Negatif
Grafik performa kelas negatif menunjukkan bahwa F1 kelas `negatif` masih lebih rendah dibandingkan performa keseluruhan model. Hal ini perlu dibahas sebagai keterbatasan karena jumlah data negatif relatif sedikit.

## Recommendation for Thesis
- Include `16_final_label_distribution.png` early in Bab Hasil dan Pembahasan to establish class imbalance.
- Follow with `16_model_comparison_macro_f1.png` and `16_model_comparison_accuracy_vs_macro_f1.png` to compare model performance.
- Present `16_linear_svm_improvement.png` when discussing the effect of SVM tuning.
- Include `15_confusion_matrix_tuned_linearsvc.png` and `16_negative_class_performance_tuned_svm.png` for final model interpretation and limitations.
- Suggested order: label distribution, unified model comparison, SVM tuning improvement, final confusion matrix, negative-class limitation.

_Generated at: 2026-07-08T14:28:03_