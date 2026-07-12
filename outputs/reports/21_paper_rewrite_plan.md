# 21 Paper Rewrite Plan

## Data Source Wording
- Replace old data-source wording with secondary dataset wording.
- Remove any claim that data were crawled by the student/researcher.
- Use provenance wording: Penelitian ini menggunakan dataset sekunder dari penelitian Sultoni et al. (2025) yang berisi unggahan media sosial X/Twitter terkait Program MBG. Dari dataset tersebut, penelitian ini menggunakan sampel berlabel sebanyak 1.000 data untuk eksperimen klasifikasi sentimen dengan label AI-assisted dan adjudication/manual review.

## Gap and Contribution
- Revise gap from platform novelty to methodology/evaluation gap.
- Emphasize classification workflow, imbalanced AI-assisted labels, SVM tuning, CV/test comparison, and error analysis.

## Model Conclusion
Tuned LinearSVC dipilih sebagai model final pada eksperimen ini karena memperoleh macro F1 test tertinggi, tetapi perbedaan CV antar tuned SVM kecil sehingga klaim keunggulan ditulis secara hati-hati.

## Required Additions
- Add provenance subsection citing Sultoni et al. (2025).
- Add codebook/labeling limitation.
- Add near-duplicate check result.
- Add class-weight ablation result.
- Add negative-class error analysis.
- Add data and code availability section.

## Data and Code Availability Draft
Data yang digunakan merupakan dataset sekunder yang berasosiasi dengan Sultoni et al. (2025). Repository penelitian menyertakan script preprocessing, modeling, evaluasi, dan laporan hasil. Lisensi dataset perlu diverifikasi dari pemilik dataset sebelum publikasi penuh.