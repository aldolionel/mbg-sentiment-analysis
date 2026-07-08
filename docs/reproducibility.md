# Reproducibility Guide

Panduan ini menjelaskan cara menjalankan ulang pipeline dari file lokal yang tersedia di repository.

## 1. Setup Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 2. Data Audit

```powershell
python scripts/generate_interim_verification.py
```

## 3. Prepare Interim Dataset

```powershell
python scripts/prepare_interim_dataset.py
```

## 4. Create Labeling Sample

```powershell
python scripts/create_labeling_dataset.py
```

## 5. Labeling and Adjudication Artifacts

Tahap labeling/adjudication adalah proses panjang dan sebagian besar sudah tersedia sebagai artifact di `data/processed/annotation_labeled_batches/`, `data/processed/adjudication/`, dan `data/processed/mbg_labeled_sample_1000.csv`.

Jika ingin mereproduksi dari awal, ikuti guideline:

- `docs/annotation_guideline_mbg_sentiment.md`
- `docs/labeling_guideline.md`

Kemudian gunakan script batch/adjudication yang tersedia di `scripts/`.

## 6. Combine Final Labeled Dataset

Jika batch adjudication sudah tersedia:

```powershell
python scripts/combine_final_labeled_batches.py
```

Output utama:

```text
data/processed/mbg_labeled_sample_1000.csv
```

## 7. Run Baseline Modeling

```powershell
python scripts/run_modeling_baselines.py
```

Output utama:

- `outputs/reports/14_modeling_baseline_report.md`
- `outputs/reports/14_modeling_test_results.csv`
- `outputs/models/best_baseline_model.joblib`

## 8. Run SVM Tuning

```powershell
python scripts/run_svm_tuning_experiments.py
```

Output utama:

- `outputs/reports/15_svm_tuning_report.md`
- `outputs/reports/15_svm_tuning_test_results.csv`
- `outputs/models/best_svm_model.joblib`

## 9. Generate Final Comparison Report

```powershell
python scripts/create_final_modeling_comparison.py
```

Output utama:

- `outputs/reports/16_final_modeling_comparison.md`
- `outputs/reports/16_final_modeling_comparison_table.csv`

## 10. Generate Final Figures and Thesis Draft

```powershell
python scripts/create_final_results_visualizations.py
```

Output utama:

- `outputs/figures/16_final_label_distribution.png`
- `outputs/figures/16_model_comparison_macro_f1.png`
- `outputs/reports/17_final_visual_results_report.md`
- `outputs/reports/17_thesis_results_narrative_draft.md`

## 11. Execute Notebooks

Notebook dapat dieksekusi dengan:

```powershell
python scripts/run_notebook.py notebooks/05_Modeling_Baselines_SVM.ipynb
python scripts/run_notebook.py notebooks/06_SVM_Tuning_Experiments.ipynb
```

## 12. Repository Publication Check

```powershell
python scripts/check_repo_publication_ready.py
```

Output:

```text
outputs/reports/18_repo_publication_readiness.md
```
