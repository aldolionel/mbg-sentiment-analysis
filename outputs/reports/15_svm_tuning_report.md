# 15 SVM Tuning Report

## Scope
This report documents SVM-focused hyperparameter tuning and class imbalance experiments for MBG sentiment classification using TF-IDF features. These are baseline/tuning experiments, not final thesis conclusions.
No raw files were modified, no data was relabeled, no baseline reports were overwritten, and SMOTE was not applied.

## Dataset Summary
- input dataset: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\data\processed\mbg_labeled_sample_1000.csv`
- total rows: 1000

### Label Distribution
- negatif: 116 (11.60%)
- netral: 472 (47.20%)
- positif: 412 (41.20%)

## Evaluation Priority
Macro F1 is prioritized because the labels are imbalanced and the minority `negatif` class should influence model selection. Accuracy is reported, but not used alone as the main conclusion.

## Experiment Setup
- random_state: 42
- train/test split: 80/20, stratified by label
- tuning: GridSearchCV with 5-fold StratifiedKFold and scoring=`f1_macro`
- model focus: LinearSVC, SVC with linear kernel, and SVC with RBF kernel
- imbalance comparison: class_weight=None versus class_weight='balanced' through the tuning grid

## Baseline References
- baseline Linear SVM test macro F1: 0.6971
- baseline Logistic Regression test macro F1: 0.7151

## Best Parameters Per Experiment
      experiment experiment_display_name  best_cv_f1_macro                                                                                                                                                                                  best_params
tuned_svc_linear Tuned SVC Linear Kernel          0.696580                            {"classifier__C": 1, "classifier__class_weight": "balanced", "tfidf__max_df": 0.9, "tfidf__min_df": 2, "tfidf__ngram_range": [1, 2], "tfidf__sublinear_tf": true}
 tuned_linearsvc         Tuned LinearSVC          0.692395                          {"classifier__C": 0.5, "classifier__class_weight": "balanced", "tfidf__max_df": 0.9, "tfidf__min_df": 3, "tfidf__ngram_range": [1, 2], "tfidf__sublinear_tf": true}
   tuned_svc_rbf    Tuned SVC RBF Kernel          0.691738 {"classifier__C": 5, "classifier__class_weight": "balanced", "classifier__gamma": 0.1, "tfidf__max_df": 0.95, "tfidf__min_df": 2, "tfidf__ngram_range": [1, 2], "tfidf__sublinear_tf": true}

## Test Metrics Per Experiment
      experiment experiment_display_name  best_cv_f1_macro  accuracy  precision_macro  recall_macro  f1_macro  f1_weighted
 tuned_linearsvc         Tuned LinearSVC          0.692395     0.795         0.745477      0.715989  0.727761     0.793010
tuned_svc_linear Tuned SVC Linear Kernel          0.696580     0.795         0.747504      0.713763  0.724858     0.793770
   tuned_svc_rbf    Tuned SVC RBF Kernel          0.691738     0.795         0.750557      0.713207  0.724738     0.793735

## Class Weight Comparison
class_weight       experiment experiment_display_name  best_cv_f1_macro  cv_macro_f1_std  cv_rank
    balanced tuned_svc_linear Tuned SVC Linear Kernel          0.696580         0.037231        1
        none tuned_svc_linear Tuned SVC Linear Kernel          0.695116         0.025234        5

## Best Tuned SVM
- selected by test macro F1: Tuned LinearSVC (`tuned_linearsvc`)
- test macro F1: 0.7278
- artifact: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\models\best_svm_model.joblib`

## Negative-Class Performance
- Tuned LinearSVC: precision=0.5789, recall=0.4783, F1=0.5238, support=23
- Tuned SVC Linear Kernel: precision=0.5500, recall=0.4783, F1=0.5116, support=23
- Tuned SVC RBF Kernel: precision=0.5500, recall=0.4783, F1=0.5116, support=23

## Logistic Regression Baseline Warning
- The best tuned SVM matches or exceeds the previous Logistic Regression baseline on test macro F1 (0.7278 vs 0.7151).

## Classification Reports

### Tuned LinearSVC
```text
              precision    recall  f1-score   support

     negatif       0.58      0.48      0.52        23
      netral       0.76      0.85      0.81        95
     positif       0.89      0.82      0.85        82

    accuracy                           0.80       200
   macro avg       0.75      0.72      0.73       200
weighted avg       0.80      0.80      0.79       200

```
- confusion matrix figure: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\15_confusion_matrix_tuned_linearsvc.png`

### Tuned SVC Linear Kernel
```text
              precision    recall  f1-score   support

     negatif       0.55      0.48      0.51        23
      netral       0.75      0.89      0.82        95
     positif       0.94      0.77      0.85        82

    accuracy                           0.80       200
   macro avg       0.75      0.71      0.72       200
weighted avg       0.81      0.80      0.79       200

```
- confusion matrix figure: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\15_confusion_matrix_tuned_svc_linear.png`

### Tuned SVC RBF Kernel
```text
              precision    recall  f1-score   support

     negatif       0.55      0.48      0.51        23
      netral       0.75      0.91      0.82        95
     positif       0.95      0.76      0.84        82

    accuracy                           0.80       200
   macro avg       0.75      0.71      0.72       200
weighted avg       0.81      0.80      0.79       200

```
- confusion matrix figure: `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\15_confusion_matrix_tuned_svc_rbf.png`