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

Dataset berlabel disiapkan melalui workflow batch (20 batch, masing-masing 50 baris). Label awal dibuat secara otomatis:

- batch 001 (50 baris): dilabeli oleh LLM melalui prompt di `data/processed/annotation_prompts/`;
- batch 002-020 (950 baris): dilabeli oleh skrip pencocokan kata kunci `scripts/label_batch_rule_based.py`.

Penting: label tidak dibuat secara manual. Formulasi yang digunakan adalah **pelabelan otomatis dengan tinjauan ulang berbantuan AI**, dan belum ada acuan (*gold standard*) hasil anotasi manusia independen.

## 5. Tinjauan Ulang Baris Ambigu

Baris yang teksnya sangat pendek atau yang catatan pelabelannya menunjukkan konteks ambigu ditandai oleh `scripts/create_semantic_review.py` untuk ditinjau ulang (138 dari 1.000 baris; hampir seluruhnya berlabel awal netral). Peninjauan tersebut sebagian besar dilakukan dengan bantuan AI dan disetujui peneliti, sedangkan peninjauan langsung oleh peneliti hanya mencakup sebagian kecil sampel. Sebanyak 862 baris yang tidak ditandai tidak ditinjau, sehingga label akhirnya sama dengan label awal. Catatan tinjauan disimpan pada artifact terproses di `data/processed/adjudication/`. Kesepakatan antara label awal dan label akhir tidak boleh ditafsirkan sebagai kesepakatan dengan anotator manusia.

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

- label bersifat otomatis dengan tinjauan ulang berbantuan AI, dan belum divalidasi terhadap anotasi manusia independen;
- dataset final berjumlah 1.000 sampel dari crawl media sosial yang lebih besar;
- kelas `negatif` merupakan kelas minoritas;
- performa kelas `negatif` masih lebih rendah dibandingkan performa keseluruhan;
- hasil menjelaskan sampel berlabel, bukan opini publik universal.

Pekerjaan lanjutan dapat mencakup validasi manual yang lebih luas, eksperimen SMOTE, penambahan data berlabel, atau perbandingan dengan model transformer.
