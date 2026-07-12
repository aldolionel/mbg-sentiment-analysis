# 19 Paper Draft Report

## Files Created

- `paper/paper_mbg_sentiment_svm.md`
- `paper/paper_summary.md`
- `paper/paper_tables.md`
- `paper/paper_figures.md`
- `outputs/reports/19_paper_draft_report.md`

## Source Files Used

- `README.md`
- `docs/methodology.md`
- `docs/results_summary.md`
- `docs/reproducibility.md`
- `outputs/reports/13_labeled_dataset_1000_report.md`
- `outputs/reports/14_modeling_baseline_report.md`
- `outputs/reports/15_svm_tuning_report.md`
- `outputs/reports/16_final_modeling_comparison.md`
- `outputs/reports/17_final_visual_results_report.md`
- `outputs/reports/17_thesis_results_narrative_draft.md`

## Paper Scope

Draft paper ini merupakan companion paper berbahasa Indonesia untuk mendampingi skripsi. Naskah membahas analisis sentimen MBG pada sampel teks media sosial berlabel menggunakan TF-IDF dan Support Vector Machine.

Paper ini tidak mengklaim opini publik universal. Hasil hanya merujuk pada 1.000 sampel data berlabel yang digunakan dalam eksperimen.

## Key Findings Included

- Dataset final berisi 1.000 sampel berlabel.
- Distribusi label: negatif 116, netral 472, positif 412.
- Label bersifat AI-assisted dengan adjudication/manual review.
- Macro F1 digunakan sebagai metrik utama karena class imbalance.
- Model terbaik adalah TF-IDF + Tuned LinearSVC.
- Macro F1 model terbaik adalah 0.7278.
- Accuracy model terbaik adalah 0.7950.
- Kelas negatif masih menjadi keterbatasan karena performanya lebih rendah dan jumlah datanya paling sedikit.

## Validation Notes

Created file checklist:

- `paper/paper_mbg_sentiment_svm.md`: created
- `paper/paper_summary.md`: created
- `paper/paper_tables.md`: created
- `paper/paper_figures.md`: created
- `outputs/reports/19_paper_draft_report.md`: created

No model retraining, relabeling, or raw data modification was performed.

## Missing Items Still Needed

- Referensi pustaka asli perlu ditambahkan menggantikan placeholder.
- Format perlu disesuaikan dengan template jurnal/kampus.
- Nomor tabel dan gambar perlu disesuaikan saat paper dipindahkan ke format final.
- Sitasi di dalam teks perlu ditambahkan setelah daftar pustaka final tersedia.

## Recommended Next Task

Langkah berikutnya yang direkomendasikan adalah mengubah draft Markdown menjadi format Word atau PDF sesuai template kampus/jurnal, lalu menambahkan referensi pustaka yang valid.
