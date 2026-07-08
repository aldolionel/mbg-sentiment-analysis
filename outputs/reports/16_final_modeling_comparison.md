# 16 Final Modeling Comparison

## Scope
This report compares existing modeling experiments for MBG sentiment classification. It uses only the saved baseline and SVM tuning result files and does not retrain models, relabel data, modify raw files, or overwrite earlier reports.
The report is intended for thesis discussion of the modeling stage; it does not claim that the entire thesis is finished.

## Dataset
- total rows: 1000
- label distribution:
  - negatif: 116 (11.60%)
  - netral: 472 (47.20%)
  - positif: 412 (41.20%)
- imbalance note: the `negatif` class is much smaller than `netral` and `positif`, so minority-class behavior needs special attention.

## Evaluation Design
- train/test split: 800/200 rows
- stratification: label
- main selection metric: macro F1
- macro F1 is prioritized because it gives each class equal weight. Accuracy alone is insufficient because a model can score well by favoring the larger `netral` and `positif` classes while performing poorly on `negatif`.

## Baseline Models
- Multinomial Naive Bayes
- Logistic Regression
- Linear SVM
- RBF SVM

## Tuned SVM Models
- Tuned LinearSVC
- Tuned SVC Linear Kernel
- Tuned SVC RBF Kernel

## Unified Comparison Table
| model_group | model_name | accuracy | precision_macro | recall_macro | f1_macro | f1_weighted | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tuned SVM | Tuned LinearSVC | 0.7950 | 0.7455 | 0.7160 | 0.7278 | 0.7930 | Best tuned SVM by test macro F1. |
| Tuned SVM | Tuned SVC Linear Kernel | 0.7950 | 0.7475 | 0.7138 | 0.7249 | 0.7938 | Tuned SVC with linear kernel. |
| Tuned SVM | Tuned SVC RBF Kernel | 0.7950 | 0.7506 | 0.7132 | 0.7247 | 0.7937 | Tuned nonlinear SVM with RBF kernel. |
| Baseline | Logistic Regression | 0.7750 | 0.7164 | 0.7211 | 0.7151 | 0.7784 | Strong non-SVM baseline with class_weight='balanced'. |
| Baseline | Linear SVM baseline | 0.7650 | 0.7203 | 0.6828 | 0.6971 | 0.7609 | Baseline SVM reference before tuning. |
| Baseline | RBF SVM baseline | 0.7600 | 0.7359 | 0.5997 | 0.6072 | 0.7351 | Baseline nonlinear SVM reference before tuning. |
| Baseline | Multinomial Naive Bayes | 0.7300 | 0.4958 | 0.5484 | 0.5187 | 0.6869 | Baseline probabilistic classifier. |

## Best Model Findings
- best overall model by macro F1: Tuned LinearSVC (0.7278)
- best SVM model by macro F1: Tuned LinearSVC (0.7278)
- best SVM beats Logistic Regression baseline: True
- recommended thesis modeling choice: Tuned LinearSVC + TF-IDF
- best SVM parameters: `classifier__C=0.5`, `classifier__class_weight=balanced`, `tfidf__max_df=0.9`, `tfidf__min_df=3`, `tfidf__ngram_range=(1, 2)`, `tfidf__sublinear_tf=True`

## Improvement Analysis
- baseline Linear SVM macro F1: 0.6971
- tuned LinearSVC macro F1: 0.7278
- absolute improvement: 0.0306
- percentage-point improvement: 3.06 points

## Negative-Class Discussion
The dataset is imbalanced, and the `negatif` class remains the most difficult class. Negative-class F1 for tuned SVM models is lower than their weighted F1, which means the model still benefits from discussion as a limitation rather than a fully solved minority-class problem.
- Tuned LinearSVC: negative precision=0.5789, recall=0.4783, F1=0.5238, support=23
- Tuned SVC Linear Kernel: negative precision=0.5500, recall=0.4783, F1=0.5116, support=23
- Tuned SVC RBF Kernel: negative precision=0.5500, recall=0.4783, F1=0.5116, support=23

## Narasi untuk Bab Hasil dan Pembahasan
Pada tahap pemodelan, penelitian ini membandingkan beberapa model klasifikasi sentimen berbasis fitur TF-IDF. Model baseline yang diuji meliputi Multinomial Naive Bayes, Logistic Regression, Linear SVM, dan RBF SVM. Setelah itu, fokus eksperimen diarahkan pada keluarga SVM melalui tuning hyperparameter pada LinearSVC, SVC dengan kernel linear, dan SVC dengan kernel RBF.

Pemilihan model utama didasarkan pada macro F1 karena distribusi label tidak seimbang. Kelas `negatif` memiliki jumlah data yang lebih sedikit dibandingkan kelas `netral` dan `positif`, sehingga akurasi saja tidak cukup untuk menilai kualitas model. Macro F1 memberikan bobot yang setara kepada setiap kelas dan lebih sesuai untuk mengevaluasi performa model pada kondisi class imbalance.

Hasil perbandingan menunjukkan bahwa model terbaik berdasarkan macro F1 adalah Tuned LinearSVC dengan nilai macro F1 sebesar 0.7278. Model ini juga menjadi model SVM terbaik dan menunjukkan peningkatan dibandingkan Linear SVM baseline, dari 0.6971 menjadi 0.7278. Dengan demikian, model TF-IDF + Tuned LinearSVC dapat direkomendasikan sebagai model akhir untuk tahap pembahasan pemodelan sentimen MBG.

Meskipun performa keseluruhan meningkat, performa pada kelas `negatif` masih relatif lebih rendah. Hal ini menunjukkan bahwa model masih menghadapi tantangan dalam mengenali sentimen negatif yang jumlah datanya lebih terbatas. Oleh karena itu, hasil ini perlu dibahas sebagai keterbatasan penelitian, terutama terkait ketidakseimbangan kelas dan ukuran sampel data berlabel.

## Limitation Note
- Labels are AI-assisted with adjudication/manual review, so label quality should be described transparently.
- The dataset contains 1,000 sampled labeled rows from a larger social media crawl.
- Future work can include larger manual validation, SMOTE comparison, or transformer-based models.