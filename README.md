# Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis (MBG) pada Media Sosial Menggunakan Support Vector Machine

Repository ini berisi proyek penelitian analisis sentimen teks media sosial terkait Program Makan Bergizi Gratis (MBG). Pipeline penelitian mencakup audit data, preprocessing teks, penyusunan sampel berlabel, evaluasi model baseline, tuning model SVM, serta pembuatan laporan dan visualisasi hasil.

Model akhir yang direkomendasikan untuk pembahasan pemodelan adalah **TF-IDF + Tuned LinearSVC**. Dataset yang digunakan pada tahap akhir adalah sampel crawl media sosial berjumlah 1.000 baris. Label sentimen disusun melalui **pelabelan otomatis** (batch pertama oleh LLM, sisanya oleh skrip kata kunci) dengan **tinjauan ulang berbantuan AI** pada baris yang ditandai ambigu. Peninjauan langsung oleh manusia sangat terbatas dan belum ada acuan (*gold standard*) hasil anotasi manusia independen, sehingga label tidak boleh dianggap sebagai label manual.

## Struktur Repository

```text
mbg-sentiment-analysis/
|-- data/
|   |-- raw/          # Data mentah lokal
|   |-- interim/      # Data hasil proses antara
|   |-- processed/    # Dataset siap analisis/modeling
|   `-- external/     # Data referensi eksternal jika diperlukan
|-- docs/             # Dokumentasi metodologi, hasil, dan reproducibility
|-- notebooks/        # Notebook audit, preprocessing, dan eksperimen
|-- outputs/
|   |-- figures/      # Visualisasi hasil
|   |-- reports/      # Laporan eksperimen dan ringkasan hasil
|   `-- models/       # Artefak model tersimpan
|-- scripts/          # Script pipeline reproducible
|-- src/
|   `-- mbg_sentiment/ # Modul Python utama
|-- tests/            # Test sederhana bila diperlukan
|-- requirements.txt
`-- README.md
```

Folder `automation_logs/` dan artifact internal workflow diabaikan dari GitHub agar repository tetap bersih sebagai proyek akademik, bukan transcript otomasi.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Alternatif Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Reproducibility Guide

Jalankan perintah berikut dari root repository.

```powershell
python scripts/generate_interim_verification.py
python scripts/prepare_interim_dataset.py
python scripts/create_labeling_dataset.py
python scripts/run_modeling_baselines.py
python scripts/run_svm_tuning_experiments.py
python scripts/create_final_modeling_comparison.py
python scripts/create_final_results_visualizations.py
python scripts/check_repo_publication_ready.py
```

Catatan: hasil pelabelan otomatis dan tinjauan ulang sudah tersedia sebagai artifact di `data/processed/` dan `outputs/reports/`. Untuk reproduksi penuh dari nol, proses pelabelan dan tinjauan ulang perlu dilakukan sesuai guideline di `docs/`.

Notebook dapat dieksekusi menggunakan runner:

```powershell
python scripts/run_notebook.py notebooks/05_Modeling_Baselines_SVM.ipynb
python scripts/run_notebook.py notebooks/06_SVM_Tuning_Experiments.ipynb
```

## Final Key Results

Dataset final berlabel:

- total baris: 1.000
- negatif: 116
- netral: 472
- positif: 412

Model terbaik:

- model: **TF-IDF + Tuned LinearSVC**
- macro F1: **0.7278**
- accuracy: **0.7950**

Macro F1 digunakan sebagai metrik utama karena distribusi label tidak seimbang, khususnya kelas `negatif` yang menjadi kelas minoritas.

## Important Limitations

- Label bersifat otomatis dengan tinjauan ulang berbantuan AI, bukan label manual. Hanya 138 dari 1.000 baris yang ditandai untuk ditinjau, sebagian besar tinjauan dibantu AI, dan belum ada validasi oleh anotator manusia independen.
- Metrik model dihitung terhadap label otomatis tersebut, sehingga belum mencerminkan akurasi terhadap sentimen sebenarnya.
- Kelas `negatif` merupakan kelas minoritas, sehingga performa pada kelas ini masih perlu dibahas sebagai keterbatasan.
- Hasil penelitian mendeskripsikan sampel data berlabel yang digunakan, bukan opini publik universal.
- Dataset berjumlah 1.000 sampel dari crawl media sosial yang lebih besar.

## Ethical and Privacy Note

Dataset digunakan untuk kepentingan akademik. Analisis tidak boleh digunakan untuk menyasar individu atau menyalahgunakan konten media sosial. Informasi yang dapat mengidentifikasi individu sebaiknya tidak ditonjolkan dalam analisis, visualisasi, atau laporan publik.

## Dokumentasi Tambahan

- [Methodology](docs/methodology.md)
- [Results Summary](docs/results_summary.md)
- [Reproducibility](docs/reproducibility.md)
- [GitHub Publication Checklist](docs/github_publication_checklist.md)
