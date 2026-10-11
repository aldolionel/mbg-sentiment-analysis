# BAB 3

# METODOLOGI PENELITIAN

## 3.1 Bahan Penelitian

Bahan utama penelitian ini adalah data teks opini publik terkait Program MBG dari dataset sekunder Sultoni dkk. (2025), yang berisi unggahan media sosial X (Twitter) hasil *scraping* berbasis kata kunci sebanyak 47.803 unggahan pada publikasi aslinya. Setelah dibersihkan dan dihapus duplikasinya, tersedia 62.446 teks unik. Dari kumpulan tersebut diambil sampel 1.000 baris yang dilabeli dan dibagi menjadi 20 batch masing-masing 50 baris. Rentang waktu pengumpulan, kata kunci lengkap, dan lisensi dataset sumber belum terdokumentasi dan perlu dilengkapi dari pemilik dataset.

Setiap baris sampel memuat teks bersih hasil praproses, label awal otomatis, catatan pelabelan, penanda peninjauan, dan label akhir. Label sentimen dibatasi pada tiga kelas, yaitu positif, negatif, dan netral. Distribusi label akhir pada sampel adalah 116 negatif, 472 netral, dan 412 positif. Label acuan hasil anotasi manusia disusun pada tahap penelitian sebagaimana diuraikan pada subbab 3.3.5.

## 3.2 Peralatan Penelitian

Peralatan penelitian terdiri dari perangkat lunak, teori dan persamaan, serta variabel penelitian.

Perangkat lunak yang digunakan meliputi bahasa pemrograman Python beserta pustaka pandas dan NumPy untuk pengolahan data, scikit-learn untuk ekstraksi fitur TF-IDF dan pemodelan SVM, imbalanced-learn untuk teknik penyeimbangan kelas, NLTK dan Sastrawi untuk praproses teks Bahasa Indonesia, serta Jupyter Notebook sebagai lingkungan eksekusi dan dokumentasi eksperimen. Pelabelan awal dan peninjauan ulang berbantuan AI menggunakan model bahasa ChatGPT dan skrip pencocokan kata kunci berbasis Python.

Teori dan persamaan yang digunakan meliputi persamaan pembobotan TF-IDF, formulasi *hyperplane* dan margin maksimal pada SVM, persamaan interpolasi SMOTE, serta formula Cohen's Kappa untuk mengukur tingkat kesepakatan antar label sebagaimana telah diuraikan pada Bab 2.

Variabel penelitian terdiri dari variabel bebas berupa representasi fitur TF-IDF dari teks bersih, dan variabel terikat berupa label sentimen (positif, negatif, netral). Selain itu, terdapat dua variabel pembanding, yaitu label otomatis dan label acuan hasil anotasi manusia, yang digunakan untuk menjawab rumusan masalah terkait kualitas label.

## 3.3 Prosedur Penelitian

Prosedur penelitian terdiri dari sembilan tahap sebagaimana diuraikan pada subbab berikut.

## 3.3.1 Audit dan Pengambilan Sampel Data

Tahap ini memeriksa struktur data, meliputi identifikasi kolom teks, potensi nilai kosong, duplikasi data, dan risiko privasi. Audit dilakukan untuk memastikan data yang masuk ke tahap praproses memiliki kolom teks yang dapat diproses dan tidak menonjolkan identitas personal. Setelah itu, diambil sampel 1.000 baris yang dibagi menjadi batch anotasi.

## 3.3.2 Praproses Teks

Teks mentah dibersihkan secara konservatif melalui tahapan decoding entitas HTML, penghapusan prefiks retweet, penghapusan URL dan mention, normalisasi hashtag dengan mempertahankan kata, *case folding*, normalisasi karakter berulang, penghapusan emoji dan tanda baca, serta normalisasi spasi.

## 3.3.3 Pelabelan Awal Otomatis

Label awal dibuat tanpa anotator manusia. Batch pertama (50 sampel) dilabeli oleh ChatGPT melalui prompt yang menetapkan tiga kelas, aturan pelabelan, dan catatan singkat untuk setiap label. Batch kedua hingga kedua puluh (950 sampel) dilabeli oleh skrip pencocokan kata kunci positif dan negatif. Pada skrip tersebut, teks yang tidak menunjukkan sinyal polaritas yang jelas dan teks berupa pertanyaan diberi label netral sebagai nilai bawaan.

## 3.3.4 Penandaan dan Peninjauan Baris Ambigu

Baris yang teksnya sangat pendek atau yang catatan pelabelannya menunjukkan konteks ambigu ditandai untuk ditinjau ulang, yaitu 138 dari 1.000 baris. Peninjauan sebagian besar dilakukan dengan bantuan AI dan disetujui peneliti, sedangkan peninjauan langsung oleh peneliti hanya mencakup sebagian kecil sampel. Baris yang tidak ditandai (862 baris) tidak ditinjau. Dataset hasil tahap ini disebut dataset berlabel otomatis dan belum dianggap sebagai acuan hasil anotasi manusia.

## 3.3.5 Penyusunan Label Acuan Manusia dan Pengukuran Kesepakatan

Sampel acak sebanyak 300 baris diambil dari 1.000 baris tanpa memandang label maupun status peninjauan. Jumlah ini bersifat rencana dan ukuran finalnya ditetapkan sesuai kapasitas anotator. Anotator manusia melabeli sampel tersebut tanpa melihat label otomatis, dengan mengikuti pedoman anotasi. Apabila tersedia, digunakan dua anotator independen, dan perbedaan label di antara keduanya diselesaikan melalui diskusi untuk menghasilkan label acuan.

Tingkat kesepakatan antar anotator dan antara label otomatis dengan label acuan diukur menggunakan Cohen's Kappa. Kualitas label otomatis dianalisis lebih lanjut melalui presisi, recall, dan matriks konfusi per kelas terhadap label acuan. Baris yang labelnya berbeda dikelompokkan berdasarkan pola teks, misalnya sarkasme, kritik implisit, negasi, teks pendek, dan konteks kurang. Tahap ini secara langsung menjawab rumusan masalah pertama dan kedua.

## 3.3.6 Ekstraksi Fitur TF-IDF

Teks bersih direpresentasikan menggunakan TF-IDF dengan konfigurasi unigram dan bigram, ambang batas frekuensi dokumen minimum dan maksimum (*min_df*, *max_df*), serta penskalaan logaritmik pada frekuensi *term* (*sublinear_tf*).

## 3.3.7 Pemodelan dan *Tuning* SVM

Model klasifikasi dibangun menggunakan algoritma SVM, dimulai dari model *baseline* berupa Linear SVM dan RBF SVM, dibandingkan dengan model pembanding Multinomial Naive Bayes dan Logistic Regression. Selanjutnya dilakukan *tuning* hyperparameter melalui pencarian grid (*grid search*) untuk menghasilkan model Tuned LinearSVC dan Tuned SVC dengan kernel linear maupun RBF.

Untuk menjawab rumusan masalah ketiga, model dilatih pada dua skenario label. Skenario A menggunakan label otomatis sebagaimana adanya. Skenario B menggunakan label otomatis yang dikoreksi berdasarkan label acuan pada baris yang tersedia. Agar tidak terjadi kebocoran data, baris berlabel acuan yang menjadi data uji tidak dipakai sebagai data latih pada lipatan yang sama, sehingga skenario B dijalankan dengan validasi silang pada baris berlabel acuan.

## 3.3.8 Evaluasi Model dan Analisis Kelas Minoritas

Evaluasi pada konfigurasi awal menggunakan pembagian data latih dan data uji sebesar 80:20 dengan stratifikasi berdasarkan label dan *random state* tetap, serta validasi silang 5-fold *Stratified K-Fold* pada tahap *tuning*. Evaluasi utama untuk menjawab rumusan masalah ketiga dan keempat dilakukan terhadap baris berlabel acuan manusia. Metrik evaluasi yang digunakan meliputi akurasi, presisi makro, recall makro, F1 makro, dan F1 berbobot, dengan F1 makro sebagai metrik utama karena distribusi label yang tidak seimbang. Karena jumlah sampel kelas negatif pada data uji kecil, hasil pada kelas negatif dilaporkan bersama interval kepercayaan hasil *bootstrap*.

## 3.3.9 Analisis Keterkaitan Kualitas Label dengan Performa Kelas Minoritas

Tahap terakhir membandingkan performa model pada kelas negatif ketika dievaluasi terhadap label otomatis dan terhadap label acuan, serta ketika dilatih dengan skenario A dan skenario B. Hasil perbandingan tersebut dikaitkan dengan pola perbedaan label yang teridentifikasi pada subbab 3.3.5, untuk menjawab rumusan masalah ketiga mengenai pengaruh kualitas label terhadap performa deteksi sentimen negatif.

## 3.4 Jadwal Penelitian

Jadwal pelaksanaan penelitian disusun sebagai berikut. Rentang bulan dan minggu bersifat sementara dan perlu disesuaikan dengan jadwal akademik yang berlaku saat pengajuan proposal.

| No | Kegiatan | Bulan 1 | Bulan 2 | Bulan 3 | Bulan 4 |
| --- | --- | --- | --- | --- | --- |
| 1 | Audit dan pengambilan sampel data | X | | | |
| 2 | Praproses teks | X | | | |
| 3 | Pelabelan awal otomatis dan peninjauan baris ambigu | X | | | |
| 4 | Penyusunan label acuan manusia dan pengukuran kesepakatan | | X | X | |
| 5 | Ekstraksi fitur TF-IDF | | X | | |
| 6 | Pemodelan dan *tuning* SVM | | X | X | |
| 7 | Evaluasi model dan analisis kelas minoritas | | | X | |
| 8 | Analisis keterkaitan kualitas label dengan performa kelas minoritas | | | X | X |
| 9 | Penyusunan laporan tugas akhir | | | X | X |
