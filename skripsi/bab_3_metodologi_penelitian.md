# BAB 3

# METODOLOGI PENELITIAN

## 3.1 Bahan Penelitian

Bahan utama penelitian ini adalah data teks opini publik terkait Program MBG yang diperoleh melalui *crawling* media sosial. Dari kumpulan data mentah hasil *crawling*, diambil sampel sejumlah 1.000 baris yang kemudian dilabeli untuk digunakan sebagai dataset pemodelan. Setiap baris data memuat teks bersih hasil praproses (*clean text*), label pra-pelabelan semi-otomatis, label hasil adjudikasi manual, serta catatan adjudikasi yang menjelaskan alasan koreksi label apabila terjadi perbedaan antara label awal dan label akhir. Label sentimen dibatasi pada tiga kelas, yaitu positif, negatif, dan netral.

## 3.2 Peralatan Penelitian

Peralatan penelitian terdiri dari perangkat keras, perangkat lunak, serta teori dan persamaan yang mendasari analisis.

Perangkat lunak yang digunakan meliputi bahasa pemrograman Python beserta pustaka pandas dan NumPy untuk pengolahan data, scikit-learn untuk ekstraksi fitur TF-IDF dan pemodelan SVM, imbalanced-learn untuk teknik penyeimbangan kelas, NLTK dan Sastrawi untuk praproses teks Bahasa Indonesia, serta Jupyter Notebook sebagai lingkungan eksekusi dan dokumentasi eksperimen.

Teori dan persamaan yang digunakan meliputi persamaan pembobotan TF-IDF, formulasi *hyperplane* dan margin maksimal pada SVM, persamaan interpolasi SMOTE, serta formula Cohen's Kappa untuk mengukur tingkat kesepakatan antar label sebagaimana telah diuraikan pada Bab 2.

Variabel penelitian terdiri dari variabel bebas berupa representasi fitur TF-IDF dari teks bersih, dan variabel terikat berupa label sentimen (positif, negatif, netral). Selain itu, terdapat variabel pembanding berupa label sebelum adjudikasi dan label sesudah adjudikasi, yang digunakan khusus untuk menjawab rumusan masalah terkait bias pelabelan.

## 3.3 Prosedur Penelitian

Prosedur penelitian terdiri dari delapan tahap sebagaimana diuraikan pada subbab berikut.

## 3.3.1 Audit dan Pengumpulan Data

Tahap ini memeriksa struktur data hasil *crawling*, meliputi identifikasi kolom teks, potensi nilai kosong, duplikasi data, dan risiko privasi. Audit dilakukan untuk memastikan data yang masuk ke tahap praproses memiliki kolom teks yang dapat diproses dan tidak menonjolkan identitas personal.

## 3.3.2 Praproses Teks

Teks mentah dibersihkan secara konservatif melalui tahapan decoding entitas HTML, penghapusan prefiks retweet, penghapusan URL dan mention, normalisasi hashtag dengan mempertahankan kata, *case folding*, normalisasi karakter berulang, penghapusan emoji dan tanda baca, serta normalisasi spasi.

## 3.3.3 Pra-Pelabelan Semi-Otomatis

Data hasil praproses diberi label awal menggunakan pendekatan semi-otomatis berbasis aturan, yaitu pencocokan kata kunci yang mengindikasikan sentimen positif atau negatif. Teks yang tidak menunjukkan sinyal polaritas yang jelas diberi label netral sebagai nilai bawaan.

## 3.3.4 Adjudikasi Manual dan Pengukuran Kesepakatan

Label awal ditinjau kembali secara manual melalui proses adjudikasi untuk menghasilkan label akhir yang lebih andal. Pada tahap ini, tingkat kesepakatan antara label awal dan label akhir diukur menggunakan Cohen's Kappa, dan pola kesalahan sistematis pada kasus yang dikoreksi diidentifikasi dan dikarakterisasi berdasarkan arah perubahan labelnya. Tahap ini secara langsung menjawab rumusan masalah pertama dan kedua.

## 3.3.5 Ekstraksi Fitur TF-IDF

Teks bersih hasil adjudikasi direpresentasikan menggunakan TF-IDF dengan konfigurasi unigram dan bigram, ambang batas frekuensi dokumen minimum dan maksimum (*min_df*, *max_df*), serta penskalaan logaritmik pada frekuensi *term* (*sublinear_tf*).

## 3.3.6 Pemodelan dan *Tuning* SVM

Model klasifikasi dibangun menggunakan algoritma SVM, dimulai dari model *baseline* berupa Linear SVM dan RBF SVM, dibandingkan dengan model pembanding Multinomial Naive Bayes dan Logistic Regression. Selanjutnya dilakukan *tuning* hyperparameter melalui pencarian grid (*grid search*) untuk menghasilkan model Tuned LinearSVC dan Tuned SVC dengan kernel linear maupun RBF.

## 3.3.7 Evaluasi Model dan Analisis Kelas Minoritas

Evaluasi dilakukan menggunakan pembagian data latih dan data uji sebesar 80:20 dengan stratifikasi berdasarkan label dan *random state* tetap, serta validasi silang 5-fold *Stratified K-Fold* pada tahap *tuning*. Metrik evaluasi yang digunakan meliputi akurasi, presisi makro, recall makro, F1 makro, dan F1 berbobot, dengan F1 makro sebagai metrik utama karena distribusi label yang tidak seimbang. Performa model pada kelas negatif yang minoritas dianalisis secara khusus untuk menjawab rumusan masalah keempat.

## 3.3.8 Analisis Keterkaitan Bias Pelabelan dengan Performa Kelas Minoritas

Tahap terakhir mengaitkan kembali pola bias yang teridentifikasi pada tahap adjudikasi dengan hasil evaluasi performa model pada kelas minoritas, untuk menjawab rumusan masalah ketiga mengenai kontribusi bias pelabelan terhadap kesulitan deteksi sentimen negatif.

## 3.4 Jadwal Penelitian

Jadwal pelaksanaan penelitian disusun sebagai berikut. Rentang bulan dan minggu bersifat sementara dan perlu disesuaikan dengan jadwal akademik yang berlaku saat pengajuan proposal.

| No | Kegiatan | Bulan 1 | Bulan 2 | Bulan 3 | Bulan 4 |
| --- | --- | --- | --- | --- | --- |
| 1 | Audit dan pengumpulan data | X | | | |
| 2 | Praproses teks | X | | | |
| 3 | Pra-pelabelan semi-otomatis | X | X | | |
| 4 | Adjudikasi manual dan pengukuran kesepakatan | | X | | |
| 5 | Ekstraksi fitur TF-IDF | | X | | |
| 6 | Pemodelan dan *tuning* SVM | | X | X | |
| 7 | Evaluasi model dan analisis kelas minoritas | | | X | |
| 8 | Analisis keterkaitan bias pelabelan | | | X | |
| 9 | Penyusunan laporan tugas akhir | | | X | X |
