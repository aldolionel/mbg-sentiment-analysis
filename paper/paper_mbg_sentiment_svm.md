# Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis (MBG) pada Media Sosial Menggunakan Support Vector Machine

## Abstract

Program Makan Bergizi Gratis (MBG) menjadi salah satu topik kebijakan publik yang banyak dibicarakan di media sosial. Percakapan tersebut dapat dimanfaatkan untuk memahami kecenderungan sentimen pada sampel teks yang relevan, meskipun hasilnya tidak dapat langsung digeneralisasikan sebagai opini publik secara universal. Penelitian ini melakukan analisis sentimen terhadap 1.000 sampel teks media sosial terkait MBG dengan tiga kelas label, yaitu positif, negatif, dan netral. Proses pelabelan dilakukan secara AI-assisted dengan adjudication/manual review agar label akhir lebih konsisten dengan pedoman anotasi. Teks dibersihkan melalui preprocessing konservatif, kemudian direpresentasikan menggunakan TF-IDF. Beberapa model baseline, seperti Multinomial Naive Bayes dan Logistic Regression, dibandingkan dengan model utama berbasis Support Vector Machine (SVM). Eksperimen SVM mencakup baseline Linear SVM, RBF SVM, serta tuning pada LinearSVC, SVC kernel linear, dan SVC kernel RBF. Karena distribusi kelas tidak seimbang, macro F1 digunakan sebagai metrik utama. Hasil terbaik diperoleh oleh model TF-IDF + Tuned LinearSVC dengan macro F1 sebesar 0.7278 dan accuracy sebesar 0.7950. Meskipun demikian, performa kelas negatif masih lebih rendah karena kelas tersebut merupakan minoritas dalam sampel.

**Keywords:** Analisis Sentimen; Makan Bergizi Gratis; Support Vector Machine; TF-IDF; Media Sosial

## Pendahuluan

Program Makan Bergizi Gratis (MBG) merupakan program publik yang memiliki dampak sosial luas karena berkaitan dengan isu gizi, pendidikan, kesejahteraan, dan kebijakan pemerintah. Sebagai program yang dekat dengan kehidupan masyarakat, MBG juga menjadi bahan diskusi di media sosial. Teks media sosial dapat memberikan gambaran awal mengenai bagaimana suatu program dibicarakan, baik dalam bentuk dukungan, kritik, maupun komentar netral.

Analisis sentimen dapat digunakan untuk mengelompokkan teks media sosial ke dalam kategori positif, negatif, dan netral. Dalam konteks MBG, pendekatan ini berguna untuk memahami kecenderungan sentimen pada sampel percakapan yang tersedia. Namun, perlu ditekankan bahwa penelitian ini tidak bertujuan menyimpulkan opini publik secara universal. Hasil yang disajikan hanya menggambarkan sampel data berlabel yang digunakan dalam eksperimen.

Fokus penelitian ini adalah membangun pipeline klasifikasi sentimen menggunakan representasi TF-IDF dan model Support Vector Machine. Model baseline juga digunakan sebagai pembanding agar performa SVM dapat dinilai secara lebih objektif. Model akhir yang direkomendasikan adalah TF-IDF + Tuned LinearSVC berdasarkan macro F1 pada data uji.

## Tinjauan Pustaka Singkat

Analisis sentimen adalah proses mengidentifikasi polaritas opini atau sikap dalam teks. Pada penelitian ini, sentimen dibagi menjadi tiga kelas, yaitu positif, negatif, dan netral. Pembagian tiga kelas ini cocok untuk teks media sosial karena tidak semua unggahan berisi dukungan atau penolakan secara eksplisit; sebagian teks hanya bersifat informatif atau ambigu.

Text preprocessing merupakan tahap penting dalam pengolahan teks media sosial. Teks media sosial biasanya mengandung URL, mention, hashtag, emoji, variasi ejaan, dan tanda baca tidak baku. Oleh karena itu, preprocessing dilakukan untuk membersihkan teks agar lebih konsisten sebelum diekstraksi menjadi fitur numerik.

TF-IDF digunakan untuk mengubah teks menjadi representasi numerik berdasarkan frekuensi kata dan tingkat kekhasan kata dalam kumpulan dokumen. Representasi ini umum digunakan pada model machine learning klasik untuk klasifikasi teks karena sederhana, efisien, dan cukup kuat untuk dataset berukuran kecil hingga menengah.

Support Vector Machine (SVM) merupakan algoritma klasifikasi yang sering digunakan pada data teks berdimensi tinggi. SVM linear sering cocok untuk fitur TF-IDF karena ruang fitur teks biasanya sparse dan berdimensi besar. Selain itu, kernel RBF dapat digunakan sebagai pembanding untuk melihat apakah pemetaan non-linear memberikan peningkatan performa.

Evaluasi model tidak hanya menggunakan accuracy. Karena dataset memiliki class imbalance, terutama pada kelas negatif, macro F1 digunakan sebagai metrik utama. Macro F1 memberi bobot yang sama pada setiap kelas sehingga performa kelas minoritas tetap diperhitungkan.

## Metodologi

### Data Source and Scope

Data penelitian berasal dari sampel crawl media sosial yang membahas Program MBG. Dataset final untuk pemodelan berisi 1.000 baris teks berlabel. Dataset ini digunakan untuk eksperimen klasifikasi sentimen dan tidak dimaksudkan sebagai representasi menyeluruh dari opini publik.

### Data Audit and Preprocessing

Tahap audit dilakukan untuk memeriksa struktur dataset, kolom teks, missing values, duplikasi, serta aspek privasi. Setelah itu, teks dibersihkan melalui preprocessing konservatif, termasuk penghapusan URL, mention, tanda baca, angka, emoji, normalisasi hashtag, case folding, normalisasi karakter berulang, dan normalisasi whitespace.

### Labeling Workflow

Label yang digunakan adalah `positif`, `negatif`, dan `netral`. Proses pelabelan dilakukan dengan pendekatan AI-assisted labeling, kemudian dilanjutkan dengan adjudication/manual review. Pendekatan ini digunakan agar label akhir lebih konsisten dengan pedoman anotasi, terutama pada teks yang ambigu.

### AI-Assisted Labeling with Adjudication/Manual Review

Penelitian ini secara eksplisit tidak mengklaim bahwa semua label dibuat secara manual. Label akhir merupakan hasil bantuan AI yang ditinjau melalui adjudication/manual review. Transparansi ini penting agar pembaca memahami konteks kualitas label dan keterbatasan penelitian.

### TF-IDF Feature Extraction

Teks bersih direpresentasikan menggunakan TF-IDF. Eksperimen menggunakan kombinasi unigram dan bigram serta parameter seperti `min_df`, `max_df`, dan `sublinear_tf`. Pada tahap tuning SVM, beberapa parameter TF-IDF ikut dicari untuk menemukan kombinasi yang lebih baik.

### Baseline Models

Model baseline yang digunakan adalah Multinomial Naive Bayes, Logistic Regression, Linear SVM, dan RBF SVM. Baseline membantu menunjukkan posisi performa model utama dibandingkan pendekatan klasifikasi klasik lainnya.

### SVM Tuning

Tuning dilakukan pada LinearSVC, SVC dengan kernel linear, dan SVC dengan kernel RBF. Parameter yang dicari mencakup nilai `C`, `class_weight`, `ngram_range`, `min_df`, `max_df`, serta `gamma` untuk kernel RBF.

### Train/Test Split and Cross-Validation

Data dibagi menjadi train/test split 80/20 dengan stratifikasi berdasarkan label dan `random_state=42`. Tuning menggunakan 5-fold StratifiedKFold cross-validation dengan scoring macro F1. Stratifikasi digunakan agar distribusi label tetap terjaga pada data train dan test.

### Evaluation Metrics

Metrik evaluasi yang digunakan mencakup accuracy, precision macro, recall macro, macro F1, dan weighted F1. Macro F1 diprioritaskan karena distribusi label tidak seimbang.

## Hasil dan Pembahasan

### Final Dataset Distribution

Dataset final terdiri dari 1.000 sampel berlabel. Distribusi labelnya adalah 116 data negatif (11.60%), 472 data netral (47.20%), dan 412 data positif (41.20%). Distribusi ini menunjukkan bahwa kelas negatif merupakan kelas minoritas.

### Baseline Model Comparison

Pada eksperimen baseline, Logistic Regression memperoleh macro F1 terbaik di antara model non-tuned, yaitu 0.7151 dengan accuracy 0.7750. Linear SVM baseline memperoleh macro F1 0.6971, sedangkan RBF SVM baseline memperoleh macro F1 0.6072. Multinomial Naive Bayes menjadi baseline terendah dengan macro F1 0.5187.

### SVM Tuning Results

Setelah tuning, performa model SVM meningkat. Tuned LinearSVC memperoleh macro F1 0.7278 dan accuracy 0.7950. Tuned SVC Linear Kernel memperoleh macro F1 0.7249, sedangkan Tuned SVC RBF Kernel memperoleh macro F1 0.7247. Ketiga model tuned SVM menunjukkan performa yang lebih baik dibandingkan baseline SVM awal.

### Best Model Selection

Model terbaik pada eksperimen ini adalah TF-IDF + Tuned LinearSVC. Model ini dipilih karena memiliki macro F1 tertinggi, yaitu 0.7278. Model ini juga melampaui Logistic Regression baseline yang memiliki macro F1 0.7151. Parameter terbaik Tuned LinearSVC meliputi `C=0.5`, `class_weight="balanced"`, `ngram_range=(1,2)`, `min_df=3`, `max_df=0.90`, dan `sublinear_tf=True`.

### Negative-Class Limitation

Kelas negatif masih menjadi tantangan utama. Pada Tuned LinearSVC, F1 untuk kelas negatif adalah 0.5238 dengan recall 0.4783. Ini menunjukkan bahwa meskipun performa keseluruhan model cukup baik, model masih belum optimal dalam mengenali sentimen negatif. Hal ini wajar dibahas sebagai keterbatasan karena kelas negatif memiliki jumlah data paling sedikit.

### Suggested Figure References

Beberapa gambar yang disarankan untuk mendukung pembahasan adalah distribusi label, perbandingan macro F1 antar model, perbandingan accuracy dan macro F1, peningkatan Linear SVM setelah tuning, confusion matrix Tuned LinearSVC, dan performa kelas negatif pada model tuned SVM.

## Kesimpulan

Penelitian ini menunjukkan bahwa TF-IDF + Tuned LinearSVC menjadi model terbaik dalam eksperimen klasifikasi sentimen MBG pada sampel media sosial berlabel. Model tersebut memperoleh macro F1 sebesar 0.7278 dan accuracy sebesar 0.7950.

Hasil ini menunjukkan bahwa tuning SVM dapat meningkatkan performa dibandingkan Linear SVM baseline. Macro F1 digunakan sebagai metrik utama karena dataset memiliki distribusi label yang tidak seimbang, terutama pada kelas negatif.

Meskipun model akhir menunjukkan performa terbaik, class imbalance tetap menjadi keterbatasan. Performa kelas negatif masih relatif lebih rendah, sehingga perlu dibahas secara hati-hati dalam interpretasi hasil.

Pekerjaan lanjutan dapat mencakup validasi manual yang lebih luas, eksperimen SMOTE sebagai pembanding, penambahan data berlabel, serta perbandingan dengan model berbasis transformer.

## Daftar Pustaka Placeholder

- [REF-1] Referensi terkait analisis sentimen MBG pada media sosial.
- [REF-2] Referensi terkait TF-IDF.
- [REF-3] Referensi terkait Support Vector Machine.
- [REF-4] Referensi terkait evaluasi klasifikasi dan macro F1.
