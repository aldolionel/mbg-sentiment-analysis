# Metodologi Penelitian

Dokumen ini menjelaskan metodologi proyek **Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis (MBG) pada Media Sosial Menggunakan Support Vector Machine**.

## 1. Data Source and Scope

Data penelitian berasal dari crawl teks media sosial terkait Program Makan Bergizi Gratis (MBG). Dataset akhir yang digunakan untuk pemodelan adalah sampel berlabel berjumlah 1.000 baris di `data/processed/mbg_labeled_sample_1000.csv`.

Hasil penelitian harus dipahami sebagai analisis terhadap sampel berlabel tersebut, bukan sebagai klaim universal mengenai opini publik secara keseluruhan.

## 2. Data Audit

Tahap audit data dilakukan untuk memeriksa struktur file, kolom teks, potensi missing values, duplikasi, dan risiko privasi. Audit awal membantu memastikan bahwa data yang masuk ke tahap preprocessing dan labeling memiliki kolom teks yang dapat diproses dan tidak menonjolkan identifier personal.

Script terkait:

```powershell
python scripts/generate_interim_verification.py
```

## 3. Cleaning and Preprocessing

Preprocessing teks dilakukan secara konservatif untuk teks media sosial informal. Tahap cleaning meliputi:

- decoding HTML entity;
- penghapusan prefix retweet;
- penghapusan URL dan mention;
- normalisasi hashtag dengan mempertahankan kata;
- case folding;
- normalisasi karakter berulang;
- penghapusan emoji, simbol, tanda baca, dan angka;
- normalisasi whitespace.

Fungsi preprocessing utama tersedia di `src/mbg_sentiment/preprocessing.py`.

## 4. Labeling Workflow

Label sentimen terdiri dari tiga kelas:

- `positif`
- `negatif`
- `netral`

Dataset berlabel disiapkan melalui workflow batch. Label awal dibuat dengan bantuan AI, kemudian diproses melalui adjudication/manual review untuk memperbaiki kasus yang ambigu atau tidak konsisten.

Penting: repository ini tidak mengklaim bahwa semua label dibuat sepenuhnya manual. Formulasi yang digunakan adalah **AI-assisted labeling dengan adjudication/manual review**.

## 5. AI-Assisted Adjudication

Adjudication digunakan untuk meninjau label awal dan memastikan label akhir lebih konsisten dengan guideline anotasi. Catatan adjudication disimpan pada artifact terproses agar proses pelabelan tetap transparan.

Dokumen terkait:

- `docs/annotation_guideline_mbg_sentiment.md`
- `docs/labeling_guideline.md`

## 6. TF-IDF Feature Extraction

Teks yang sudah dibersihkan direpresentasikan menggunakan TF-IDF. Eksperimen baseline menggunakan konfigurasi utama:

- unigram dan bigram;
- `min_df`;
- `max_df`;
- `sublinear_tf=True`.

Pada tuning SVM, parameter TF-IDF ikut dicari melalui grid search.

## 7. Baseline Models

Model baseline yang digunakan:

- Multinomial Naive Bayes
- Logistic Regression
- Linear SVM
- RBF SVM

Baseline digunakan sebagai pembanding untuk menilai apakah tuning SVM memberikan peningkatan yang bermakna.

## 8. Main Models

Fokus utama penelitian adalah keluarga SVM:

- Linear SVM
- RBF SVM
- Tuned LinearSVC
- Tuned SVC Linear Kernel
- Tuned SVC RBF Kernel

Model akhir yang direkomendasikan berdasarkan hasil eksperimen adalah **TF-IDF + Tuned LinearSVC**.

## 9. Evaluation

Evaluasi dilakukan dengan:

- train/test split 80/20;
- stratifikasi berdasarkan label;
- `random_state=42`;
- 5-fold StratifiedKFold cross-validation untuk evaluasi/tuning;
- metrik accuracy, precision macro, recall macro, macro F1, dan weighted F1.

Macro F1 diprioritaskan karena distribusi label tidak seimbang. Accuracy tetap dilaporkan, tetapi tidak dijadikan satu-satunya dasar kesimpulan.

## 10. Limitations

Keterbatasan utama:

- label bersifat AI-assisted dengan adjudication/manual review;
- dataset final berjumlah 1.000 sampel dari crawl media sosial yang lebih besar;
- kelas `negatif` merupakan kelas minoritas;
- performa kelas `negatif` masih lebih rendah dibandingkan performa keseluruhan;
- hasil menjelaskan sampel berlabel, bukan opini publik universal.

Pekerjaan lanjutan dapat mencakup validasi manual yang lebih luas, eksperimen SMOTE, penambahan data berlabel, atau perbandingan dengan model transformer.
