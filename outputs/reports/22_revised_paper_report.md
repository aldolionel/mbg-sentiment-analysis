# 22 Revised Paper Report

## Files Created
- `paper/paper_mbg_sentiment_svm_revised_methodology.md`
- `paper/paper_tables_revised_methodology.md`
- `paper/paper_figures_revised_methodology.md`
- `paper/paper_mbg_sentiment_svm_revised_methodology.docx`
- `outputs/reports/22_revised_paper_report.md`

## Major Changes from Previous Paper
- Reframed the dataset as a secondary dataset associated with Sultoni et al. (2025).
- Removed any claim that the student/researcher crawled the data.
- Reframed contribution as methodology/evaluation rather than platform or SVM novelty.
- Added cautious wording about CV evidence and test-set model selection.

## Methodology Hardening Items Included
- Dataset provenance subsection.
- AI-assisted labeling and codebook limitation.
- Class-weight ablation result.
- CV model selection caution.
- Near-duplicate train/test check result.
- Negative-class qualitative error analysis.
- Data and code availability section.

## Remaining Limitations
- Dataset license is not explicitly identified from available local documents.
- Labels are not pure manual gold standard.
- Cohen's Kappa has not been computed because two independent human annotators have not completed validation.
- Results describe the sampled labeled dataset, not universal public opinion.

## Figures Inserted
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_final_label_distribution.png`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_model_comparison_macro_f1.png`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_model_comparison_accuracy_vs_macro_f1.png`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_linear_svm_improvement.png`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\15_confusion_matrix_tuned_linearsvc.png`
- `C:\Users\hpdk1\Documents\Projects\mbg-sentiment-analysis\outputs\figures\16_negative_class_performance_tuned_svm.png`

## Figures Missing
- none

## Readiness Status
PASS: Revised paper Markdown, tables, figure guide, and DOCX were generated. DOCX still requires visual QA/render review before final submission.

## Render QA Note
Visual render QA was attempted with the document renderer, but the local environment could not find the LibreOffice/`soffice` executable required to convert DOCX to PDF/PNG. The DOCX was generated successfully and should be opened manually in Microsoft Word or LibreOffice for final visual review before submission.
