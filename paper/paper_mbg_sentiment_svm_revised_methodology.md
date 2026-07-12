# Studi Klasifikasi Sentimen MBG pada Dataset Sekunder Media Sosial X dengan TF-IDF dan Support Vector Machine

## Abstract

Penelitian ini membahas klasifikasi sentimen terkait Program Makan Bergizi Gratis (MBG) pada dataset sekunder media sosial X/Twitter. Dataset yang digunakan berasosiasi dengan penelitian Sultoni et al. (2025), yang melaporkan 47.803 unggahan X/Twitter terkait MBG dan dikumpulkan melalui keyword-based scraping menggunakan kata kunci seperti "Makan Bergizi Gratis", "Program Gizi", "Stunting", serta hashtag terkait. Repository ini menggunakan file mentah terpilih `data/raw/data crawl mbg (in).xlsx`, kemudian memakai 1.000 baris sampel berlabel untuk eksperimen tesis. Label sentimen terdiri dari positif, negatif, dan netral, serta disusun melalui AI-assisted labeling dengan adjudication/manual review. Label tersebut belum dapat disebut sebagai pure manual gold standard karena validasi dua anotator manusia dan Cohen's Kappa belum selesai. Metode yang digunakan mencakup preprocessing teks, ekstraksi fitur TF-IDF, baseline model, tuning Support Vector Machine (SVM), class-weight ablation, near-duplicate train/test check, dan error analysis kelas negatif. Karena distribusi label tidak seimbang, macro F1 digunakan sebagai metrik utama. Tuned LinearSVC dipilih sebagai model final pada eksperimen ini karena memperoleh macro F1 tertinggi pada data uji, yaitu 0.7278, dengan accuracy 0.7950. Namun, perbedaan CV antar tuned SVM kecil sehingga klaim keunggulan model ditulis secara hati-hati. Hasil penelitian ini menggambarkan sampel data berlabel, bukan opini publik universal.

**Keywords:** Analisis Sentimen; Makan Bergizi Gratis; Dataset Sekunder; TF-IDF; Support Vector Machine

## Pendahuluan

Program Makan Bergizi Gratis (MBG) merupakan salah satu topik kebijakan publik yang banyak dibicarakan di media sosial. Percakapan tersebut dapat memuat dukungan, kritik, pertanyaan, atau informasi netral mengenai program. Dalam konteks penelitian klasifikasi teks, media sosial menyediakan data yang menarik karena bahasanya ringkas, informal, dan sering mengandung konteks implisit.

Penelitian ini tidak bertujuan mengukur opini publik secara universal. Fokusnya adalah membangun dan mengevaluasi workflow klasifikasi sentimen pada sampel data berlabel terkait MBG. Dengan demikian, hasil yang dilaporkan hanya berlaku untuk sampel berlabel yang digunakan dalam eksperimen ini.

Kontribusi penelitian ini bersifat metodologis dan edukasional, bukan klaim kebaruan platform atau kebaruan algoritma SVM. Kontribusi utamanya adalah: dokumentasi provenance dataset sekunder secara transparan, workflow AI-assisted labeling dengan codebook dan adjudication/manual review, evaluasi pada label imbalanced menggunakan macro F1, perbandingan baseline dan tuned SVM, class-weight ablation, near-duplicate train/test check, serta analisis kualitatif error pada kelas negatif.

## Tinjauan Pustaka

Analisis sentimen adalah proses mengelompokkan teks berdasarkan kecenderungan sikap atau polaritas. Dalam penelitian ini, label yang digunakan adalah `positif`, `negatif`, dan `netral`. Tiga kelas ini dipilih karena teks media sosial tidak selalu menyampaikan dukungan atau kritik secara eksplisit; banyak teks hanya bersifat informatif, ambigu, atau membutuhkan konteks tambahan.

Preprocessing teks diperlukan karena data media sosial biasanya mengandung URL, mention, hashtag, emoji, singkatan, dan struktur kalimat tidak baku. Pembersihan teks membantu membuat representasi fitur lebih konsisten sebelum diproses oleh model machine learning.

TF-IDF digunakan untuk mengubah teks menjadi representasi numerik berbasis bobot kata. Representasi ini umum dipakai dalam klasifikasi teks klasik karena sederhana, efisien, dan cocok untuk model linear pada ruang fitur berdimensi tinggi.

Support Vector Machine (SVM) merupakan salah satu metode klasifikasi yang sering digunakan pada data teks. Pada representasi TF-IDF, model linear seperti LinearSVC sering kompetitif karena data bersifat sparse dan high-dimensional. SVC dengan kernel linear dan RBF digunakan sebagai pembanding dalam eksperimen tuning.

Evaluasi model pada dataset tidak seimbang perlu berhati-hati. Accuracy dapat terlihat tinggi meskipun model kurang baik pada kelas minoritas. Oleh karena itu, macro F1 digunakan sebagai metrik utama karena memberi bobot yang sama kepada setiap kelas.

## Metodologi

### Dataset Sekunder dan Provenance

Penelitian ini menggunakan dataset sekunder yang berasosiasi dengan:

Sultoni, A., Putra, D. A., Wahidah, H. N., Arief, M. M., & Putria, P. J. R. M. (2025). *Public Sentiment Analysis and Distribution Optimization MBG*. Jurnal Matematika Thales (JMT), 7(1), 35-53.

Sumber tersebut menyatakan bahwa dataset berisi 47.803 unggahan X/Twitter terkait MBG. Data dikumpulkan dari X/Twitter menggunakan keyword-based scraping dengan contoh kata kunci "Makan Bergizi Gratis", "Program Gizi", "Stunting", serta hashtag terkait. Paper sumber juga menyebutkan bahwa dataset dapat diakses melalui Google Drive link dalam paper tersebut.

Repository ini menggunakan file mentah terpilih `data/raw/data crawl mbg (in).xlsx`. Status lisensi dataset adalah: **license not explicitly identified from available local documents**. Karena itu, informasi lisensi dan hak distribusi perlu diverifikasi dari paper atau pemilik dataset sebelum publikasi final.

### Sampel dan Labeling

Eksperimen tesis menggunakan 1.000 baris sampel berlabel dari dataset tersebut. Distribusi label final adalah 116 negatif (11.60%), 472 netral (47.20%), dan 412 positif (41.20%). Sampel ini digunakan untuk eksperimen klasifikasi sentimen dan tidak dimaksudkan sebagai representasi seluruh opini publik.

Label disusun melalui AI-assisted initial labeling, semantic review, dan adjudication/manual review. Proses ini didokumentasikan dalam codebook anotasi. Namun, label belum dapat disebut pure manual gold standard karena belum ada validasi final oleh dua anotator independen manusia. Cohen's Kappa juga belum dihitung karena dua kolom anotator manusia belum tersedia.

### Feature Extraction dan Model

Teks dibersihkan melalui preprocessing konservatif, kemudian direpresentasikan menggunakan TF-IDF. Eksperimen baseline membandingkan Multinomial Naive Bayes, Logistic Regression, Linear SVM, dan RBF SVM. Eksperimen tuning berfokus pada LinearSVC, SVC linear kernel, dan SVC RBF kernel.

### Evaluation Design

Evaluasi menggunakan train/test split 80/20 dengan stratifikasi label dan `random_state=42`. Tuning dilakukan dengan 5-fold StratifiedKFold dan scoring macro F1. Macro F1 diprioritaskan karena kelas negatif merupakan kelas minoritas.

Selain evaluasi utama, penelitian ini menambahkan class-weight ablation, ringkasan CV model selection, near-duplicate train/test check berbasis TF-IDF cosine similarity, dan negative-class qualitative error analysis. Tambahan ini dilakukan untuk memperkuat metodologi setelah critical review.

## Hasil dan Pembahasan

### Distribusi Dataset Final

Dataset final berisi 1.000 sampel berlabel. Kelas netral menjadi kelas terbesar dengan 472 data, diikuti positif sebanyak 412 data, dan negatif sebanyak 116 data. Distribusi ini menunjukkan class imbalance yang cukup jelas, terutama karena kelas negatif hanya 11.60% dari total data.

### Perbandingan Baseline dan Tuned SVM

Pada baseline, Linear SVM memperoleh macro F1 0.6971. Setelah tuning, Tuned LinearSVC memperoleh test macro F1 0.7278 dan accuracy 0.7950. Peningkatan ini menunjukkan bahwa konfigurasi model dan parameter fitur dapat membantu performa pada eksperimen ini.

Namun, interpretasi hasil perlu hati-hati. Ringkasan CV menunjukkan bahwa Tuned SVC Linear Kernel memiliki CV mean macro F1 0.6966, Tuned LinearSVC memiliki CV mean macro F1 0.6924, dan Tuned SVC RBF Kernel memiliki CV mean macro F1 0.6917. Selisih CV antar tuned SVM sangat kecil. Dengan demikian, Tuned LinearSVC dipilih sebagai model final pada eksperimen ini karena memperoleh macro F1 tertinggi pada data uji. Namun, perbedaan CV antar model tuned SVM kecil, sehingga klaim keunggulan model ditulis secara hati-hati.

### Class-Weight Ablation

Class-weight ablation dilakukan untuk membandingkan LinearSVC dengan `class_weight=None` dan `class_weight="balanced"` pada konfigurasi TF-IDF baseline. Hasilnya, LinearSVC `class_weight=None` memperoleh macro F1 0.6991, sedangkan LinearSVC `class_weight="balanced"` memperoleh macro F1 0.6971. Artinya, class_weight saja tidak menjelaskan peningkatan Tuned LinearSVC. Peningkatan model final kemungkinan terkait kombinasi parameter TF-IDF, nilai `C`, dan variasi evaluasi, sehingga tidak boleh diklaim sebagai akibat tunggal dari class_weight.

### Near-Duplicate Train/Test Check

Pemeriksaan near-duplicate dilakukan pada 200 baris test dengan threshold TF-IDF cosine similarity >= 0.90 terhadap data train. Hasilnya, tidak ditemukan near-duplicate test rows pada threshold tersebut. Ini mengurangi kekhawatiran leakage berbasis kemiripan tekstual tinggi, meskipun metode ini bukan deteksi duplikasi semantik yang sempurna.

### Negative-Class Error Analysis

Analisis error kelas negatif dilakukan pada 23 baris test yang label sebenarnya negatif. Dari jumlah tersebut, 11 baris diprediksi benar sebagai negatif dan 12 baris salah prediksi. Tema utama error meliputi kritik implisit, sarkasme, konteks kurang, dan model miss. Hal ini menunjukkan bahwa kelas negatif sulit karena kritik tidak selalu memakai kata negatif eksplisit dan sering membutuhkan pemahaman konteks.

### Rujukan Gambar

Gambar yang direkomendasikan untuk paper adalah distribusi label final, perbandingan macro F1, perbandingan accuracy dan macro F1, peningkatan Linear SVM setelah tuning, confusion matrix Tuned LinearSVC, serta performa kelas negatif pada model tuned SVM.

## Ketersediaan Data dan Kode

Kode pipeline tersedia dalam repository `mbg-sentiment-analysis`, meliputi preprocessing, baseline modeling, tuning SVM, pembuatan laporan, visualisasi, hardening checks, dan validation package. Dataset yang digunakan merupakan dataset sekunder yang berasosiasi dengan Sultoni et al. (2025). File mentah terpilih di repository adalah `data/raw/data crawl mbg (in).xlsx`.

Lisensi dataset tidak teridentifikasi secara eksplisit dari dokumen lokal yang tersedia. Karena itu, sebelum publikasi penuh, peneliti perlu memverifikasi lisensi, izin distribusi, dan source URL dari paper atau pemilik dataset.

## Keterbatasan

Penelitian ini memiliki beberapa keterbatasan. Pertama, dataset merupakan dataset sekunder sehingga provenance lengkap, lisensi, dan detail teknis pengumpulan data perlu diverifikasi dari sumber asli. Kedua, dataset final yang digunakan untuk eksperimen hanya 1.000 sampel berlabel dari dataset sumber yang lebih besar. Ketiga, label bersifat AI-assisted dengan adjudication/manual review, bukan pure manual gold standard. Keempat, Cohen's Kappa belum dihitung karena dua anotator independen manusia belum menyelesaikan validasi. Kelima, kelas negatif merupakan kelas minoritas sehingga performa pada kelas tersebut masih terbatas. Keenam, near-duplicate check berbasis TF-IDF cosine similarity tidak menjamin deteksi semua duplikasi semantik.

## Kesimpulan

Penelitian ini menunjukkan bahwa TF-IDF + Tuned LinearSVC dapat digunakan sebagai model final terpilih untuk eksperimen klasifikasi sentimen MBG pada sampel dataset sekunder media sosial X. Model ini memperoleh test macro F1 0.7278 dan accuracy 0.7950.

Namun, kesimpulan harus dibaca secara hati-hati. Perbedaan CV antar tuned SVM kecil, class-weight saja tidak menjelaskan peningkatan, dan performa kelas negatif masih menjadi keterbatasan. Oleh karena itu, hasil penelitian ini sebaiknya diposisikan sebagai evaluasi workflow klasifikasi pada sampel berlabel, bukan sebagai klaim universal mengenai opini publik terhadap MBG.

Pekerjaan lanjutan dapat mencakup validasi gold-label oleh dua anotator manusia, perhitungan Cohen's Kappa, perluasan dataset berlabel, eksperimen SMOTE, serta perbandingan dengan model transformer.

## Daftar Pustaka

- [REF-1] Sultoni, A., Putra, D. A., Wahidah, H. N., Arief, M. M., & Putria, P. J. R. M. (2025). Public Sentiment Analysis and Distribution Optimization MBG. Jurnal Matematika Thales (JMT), 7(1), 35-53.
- [REF-2] Referensi terkait TF-IDF.
- [REF-3] Referensi terkait Support Vector Machine.
- [REF-4] Referensi terkait evaluasi klasifikasi, macro F1, dan class imbalance.
