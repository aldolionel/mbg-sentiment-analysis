# 14 Modeling Baseline Report

## Scope
This report documents baseline modeling experiments for MBG sentiment classification using TF-IDF features and classical ML models. These results are baseline experiments, not final thesis results.
No raw files were modified, no data was relabeled, and SMOTE was not applied in this script.

## Evaluation Priority
Macro F1 is prioritized because the labeled dataset is imbalanced, especially for the `negatif` class. Accuracy is reported, but it is not used alone as the main conclusion.

## Dataset Summary
- input dataset: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\data\processed\mbg_labeled_sample_1000.csv`
- total rows: 1000
- dropped rows with missing clean_text or label: 0

### Label Distribution
- negatif: 116 (11.60%)
- netral: 472 (47.20%)
- positif: 412 (41.20%)

## Experiment Setup
- random_state: 42
- train/test split: 80/20, stratified by label
- cross-validation: 5-fold StratifiedKFold with shuffle=True
- features: TF-IDF, unigrams and bigrams, min_df=2, max_df=0.95, sublinear_tf=True
- main model family: SVM
- baselines: Multinomial Naive Bayes and Logistic Regression
- imbalance handling: class_weight='balanced' for Logistic Regression, Linear SVM, and RBF SVM

## Cross-Validation Results
              model      model_display_name  accuracy_mean  accuracy_std  precision_macro_mean  precision_macro_std  recall_macro_mean  recall_macro_std  f1_macro_mean  f1_macro_std  f1_weighted_mean  f1_weighted_std
logistic_regression     Logistic Regression          0.780      0.019494              0.714261             0.016821           0.700050          0.023434       0.702280      0.018922          0.778501         0.016955
         linear_svm              Linear SVM          0.778      0.023152              0.690514             0.028237           0.661354          0.014583       0.669800      0.018014          0.770467         0.019260
            rbf_svm                 RBF SVM          0.756      0.032000              0.735598             0.089830           0.586365          0.028669       0.582885      0.032300          0.724167         0.029239
     multinomial_nb Multinomial Naive Bayes          0.732      0.019131              0.493026             0.015392           0.552313          0.014237       0.519559      0.014085          0.687299         0.018337

## Test Results
              model      model_display_name  accuracy  precision_macro  recall_macro  f1_macro  f1_weighted
logistic_regression     Logistic Regression     0.775         0.716421      0.721140  0.715071     0.778398
         linear_svm              Linear SVM     0.765         0.720340      0.682839  0.697124     0.760918
            rbf_svm                 RBF SVM     0.760         0.735897      0.599661  0.607241     0.735115
     multinomial_nb Multinomial Naive Bayes     0.730         0.495833      0.548438  0.518653     0.686919

## Best Baseline Model
- selected by test macro F1: Logistic Regression (`logistic_regression`)
- test macro F1: 0.7151
- artifact: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\models\best_baseline_model.joblib`

## Classification Reports

### Multinomial Naive Bayes
```text
              precision    recall  f1-score   support

     negatif       0.00      0.00      0.00        23
      netral       0.68      0.85      0.75        95
     positif       0.81      0.79      0.80        82

    accuracy                           0.73       200
   macro avg       0.50      0.55      0.52       200
weighted avg       0.65      0.73      0.69       200

```
- confusion matrix figure: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\14_confusion_matrix_multinomial_nb.png`

### Logistic Regression
```text
              precision    recall  f1-score   support

     negatif       0.48      0.57      0.52        23
      netral       0.77      0.84      0.80        95
     positif       0.90      0.76      0.82        82

    accuracy                           0.78       200
   macro avg       0.72      0.72      0.72       200
weighted avg       0.79      0.78      0.78       200

```
- confusion matrix figure: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\14_confusion_matrix_logistic_regression.png`

### Linear SVM
```text
              precision    recall  f1-score   support

     negatif       0.59      0.43      0.50        23
      netral       0.75      0.82      0.78        95
     positif       0.82      0.79      0.81        82

    accuracy                           0.77       200
   macro avg       0.72      0.68      0.70       200
weighted avg       0.76      0.77      0.76       200

```
- confusion matrix figure: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\14_confusion_matrix_linear_svm.png`

### RBF SVM
```text
              precision    recall  f1-score   support

     negatif       0.60      0.13      0.21        23
      netral       0.68      0.94      0.79        95
     positif       0.92      0.73      0.82        82

    accuracy                           0.76       200
   macro avg       0.74      0.60      0.61       200
weighted avg       0.77      0.76      0.74       200

```
- confusion matrix figure: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\14_confusion_matrix_rbf_svm.png`