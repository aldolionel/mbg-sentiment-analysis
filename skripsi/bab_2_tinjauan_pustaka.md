# BAB 2

# TINJAUAN PUSTAKA

## 2.1 Landasan Teori

## 2.1.1 Analisis Sentimen

Analisis sentimen adalah proses komputasional untuk mengidentifikasi dan mengklasifikasikan orientasi opini yang terkandung dalam suatu teks, umumnya ke dalam kategori positif, negatif, atau netral. Pada konteks kebijakan publik, analisis sentimen digunakan untuk memahami reaksi masyarakat terhadap suatu program pemerintah berdasarkan opini yang dinyatakan secara terbuka di media sosial. Hasil analisis ini dapat menjadi salah satu bentuk pemantauan opini yang bersifat *data-driven*, melengkapi metode survei konvensional.

## 2.1.2 Ekstraksi Fitur Term Frequency-Inverse Document Frequency (TF-IDF)

TF-IDF merupakan metode pembobotan fitur teks yang memberikan nilai lebih tinggi pada kata yang sering muncul dalam suatu dokumen namun jarang muncul pada keseluruhan korpus (Manning dkk., 2008). Metode ini banyak digunakan sebagai representasi fitur pada tugas klasifikasi teks karena kesederhanaannya dan efektivitasnya, terutama ketika dikombinasikan dengan pengaturan *unigram* dan *bigram*, ambang batas frekuensi dokumen minimum dan maksimum (*min_df*, *max_df*), serta penskalaan logaritmik pada frekuensi *term* (*sublinear_tf*).

## 2.1.3 Support Vector Machine (SVM)

*Support Vector Machine* adalah algoritma klasifikasi yang bekerja dengan mencari *hyperplane* pemisah dengan margin maksimal antar kelas pada ruang fitur (Cortes dan Vapnik, 1995). SVM dikenal efektif pada data berdimensi tinggi dan jarang (*sparse*), sehingga cocok digunakan bersama representasi fitur TF-IDF pada tugas klasifikasi teks. SVM dapat menggunakan kernel linear untuk data yang dapat dipisahkan secara linear, maupun kernel non-linear seperti *Radial Basis Function* (RBF) untuk pola yang lebih kompleks.

## 2.1.4 Pelabelan Data Otomatis dan Berbantuan AI

Pelabelan data berbantuan AI (*AI-assisted labeling*) merupakan pendekatan penyusunan dataset berlabel yang memanfaatkan proses otomatis untuk mempercepat anotasi, dengan atau tanpa peninjauan manusia. Nasution dan Onan (2024) menunjukkan bahwa label yang dihasilkan oleh *Large Language Model* dapat mendekati kualitas label manusia pada tugas pemrosesan bahasa alami untuk bahasa bersumber daya rendah, namun tetap memiliki celah pada kasus linguistik yang kompleks. Jadhav dkk. (2025) juga menegaskan bahwa performa LLM sebagai anotator masih tertinggal dibandingkan model yang di-*fine-tune* secara khusus ketika diterapkan pada bahasa bersumber daya rendah. Selain pendekatan berbasis LLM, terdapat pula pendekatan pelabelan otomatis berbasis aturan (*rule-based*) yang menggunakan daftar kata kunci atau pola linguistik sederhana untuk memberikan label awal. Kualitas label otomatis umumnya diukur dengan membandingkannya terhadap label acuan (*gold standard*) hasil anotasi manusia, yang idealnya dibuat oleh lebih dari satu anotator independen tanpa melihat label otomatis. Tanpa acuan tersebut, kesepakatan antara dua proses otomatis, atau antara proses otomatis dan tinjauan berbantuan AI, tidak dapat dianggap sebagai ukuran kualitas label yang sebenarnya. Pelabelan otomatis berbasis aturan yang disertai peninjauan terbatas belum banyak dievaluasi secara eksplisit terhadap acuan hasil anotasi manusia.

## 2.1.5 Ketidakseimbangan Kelas (*Class Imbalance*) dalam Klasifikasi Teks

Ketidakseimbangan kelas terjadi ketika proporsi antar kelas pada suatu dataset tidak merata, sehingga model klasifikasi cenderung bias terhadap kelas mayoritas dan kurang mampu mengenali pola pada kelas minoritas. Henning dkk. (2023) mengelompokkan pendekatan penanganan ketidakseimbangan kelas pada pemrosesan bahasa alami berbasis *deep learning* menjadi beberapa kategori, meliputi teknik *sampling*, augmentasi data, penyesuaian fungsi *loss*, *staged learning*, dan modifikasi arsitektur model. Salah satu teknik *sampling* yang umum digunakan adalah *Synthetic Minority Over-sampling Technique* (SMOTE), yang menghasilkan sampel sintetis pada kelas minoritas berdasarkan interpolasi antar sampel yang sudah ada (Chawla dkk., 2002). Taskiran dkk. (2025) melakukan evaluasi komprehensif terhadap SMOTE beserta puluhan variannya pada tugas klasifikasi teks, dan menunjukkan bahwa efektivitas masing-masing teknik *oversampling* dapat bervariasi tergantung karakteristik data. Henning dkk. (2023) juga menekankan bahwa sumber ketidakseimbangan kelas tidak selalu berasal dari distribusi data secara alami, tetapi dapat pula terbentuk akibat proses anotasi yang bias, sebuah aspek yang menjadi dasar pertanyaan penelitian ini.

## 2.1.6 Sarkasme dan Sentimen Implisit dalam Teks Media Sosial

Sarkasme merupakan salah satu tantangan utama dalam analisis sentimen karena penuturnya menyampaikan sentimen negatif menggunakan kata-kata yang secara literal bermakna positif (Joshi dkk., 2017). Kunneman dkk. (2015) mengidentifikasi sejumlah penanda linguistik sarkasme, seperti penggunaan hiperbola dan *hashtag* tertentu, yang dapat membantu membedakan ujaran sarkastik dari ujaran literal. Pada konteks Bahasa Indonesia, Lunando dan Purwarianti (2015) menunjukkan bahwa sarkasme juga menjadi tantangan signifikan pada teks media sosial berbahasa Indonesia, dan mengusulkan fitur tambahan berupa informasi negasi dan jumlah kata seru untuk membantu mendeteksinya. Ketiga studi ini menjadi dasar dugaan awal bahwa kesulitan mendeteksi sentimen negatif pada penelitian ini berkaitan dengan fenomena sarkasme dan sentimen implisit yang tidak tertangkap oleh pelabelan berbasis kata kunci sederhana. Dugaan tersebut akan diuji melalui analisis kesalahan terhadap label acuan hasil anotasi manusia.

## 2.1.7 Cohen's Kappa sebagai Ukuran Kesepakatan Antar-Anotator

Cohen's Kappa adalah statistik yang digunakan untuk mengukur tingkat kesepakatan antara dua penilai (*rater*) pada data kategorikal, dengan memperhitungkan kemungkinan kesepakatan yang terjadi secara kebetulan. Landis dan Koch (1977) mengusulkan skala interpretasi nilai Kappa, di mana nilai di atas 0,81 dikategorikan sebagai kesepakatan hampir sempurna (*almost perfect agreement*). Pada penelitian ini, Cohen's Kappa digunakan untuk mengukur tingkat kesepakatan antara label otomatis dan label acuan hasil anotasi manusia, serta antar anotator manusia, sebagai dasar kuantitatif untuk menilai kualitas label otomatis.

## 2.2 Penelitian Terdahulu

Berikut ringkasan penelitian terdahulu yang relevan dengan penelitian ini, beserta perbedaannya dengan fokus penelitian yang diajukan.

| No | Peneliti (Tahun) | Metode dan Objek | Temuan Utama | Perbedaan dengan Penelitian Ini |
| --- | --- | --- | --- | --- |
| 1 | Pateman dkk. (2025) | SVM dan SMOTE pada sentimen pemerintah di TikTok dan X | Akurasi meningkat dari 61% ke 76% (TikTok) dan 74% ke 86% (X) setelah SMOTE diterapkan | Sentimen negatif berperan sebagai kelas mayoritas (arah *imbalance* berlawanan dengan MBG); tidak menelusuri kemungkinan sumber *imbalance* dari proses pelabelan |
| 2 | Penulis UNNES, *Scientific Journal of Informatics* (2026) | *Stacked* LSTM dan SMOTE pada komentar Instagram terkait kebijakan Program MBG | Perbandingan ablasi 4 konfigurasi LSTM dengan dan tanpa SMOTE | Fokus pada perbandingan arsitektur *deep learning*, bukan pada sumber bias di tahap pelabelan; platform berbeda (Instagram) |
| 3 | Rofi'i (2026) | SMOTE dan *GridSearchCV* pada isu reshuffle kabinet | Distribusi kelas asli 83,5% negatif dan 16,5% positif; SMOTE menurunkan bias kelas mayoritas | Ketidakseimbangan kelas dianggap sebagai karakteristik data yang sudah ada, bukan hasil telaah proses pelabelan |
| 4 | Munir (2025) | Analisis sentimen Program MBG di media sosial X dengan metode NLP | Klasifikasi sentimen pada opini publik terkait MBG | Tidak membahas keandalan proses pelabelan maupun ketidakseimbangan kelas secara eksplisit |
| 5 | Riwaldi dan Aripin (2026) | *Hybrid* CNN-BiLSTM untuk sentimen multi-platform terkait insiden keamanan pangan Program MBG | Model *hybrid* CNN-BiLSTM untuk klasifikasi sentimen | Berfokus pada perbandingan arsitektur model, bukan pada proses pelabelan data |
| 6 | Nasution dan Onan (2024) | Perbandingan kualitas label manusia dan LLM pada tugas pemrosesan bahasa alami untuk bahasa bersumber daya rendah | Label AI mendekati kualitas label manusia namun memiliki celah pada kasus kompleks | Domain penelitian bersifat umum (bukan sentimen kebijakan pemerintah Indonesia) dan tidak dikaitkan dengan dampaknya terhadap performa klasifikasi pada kelas minoritas |

Berdasarkan tabel di atas, penelitian yang secara eksplisit mengevaluasi kualitas label otomatis terhadap acuan hasil anotasi manusia dan mengaitkannya dengan performa klasifikasi pada kelas sentimen minoritas, khususnya pada domain Program MBG, belum ditemukan pada literatur yang ditinjau. Kondisi inilah yang menjadi celah penelitian yang diisi oleh penelitian ini.

## 2.3 Kerangka Pemikiran

Penelitian ini disusun berdasarkan alur berpikir sebagai berikut. Data opini publik terkait Program MBG diperoleh dari dataset sekunder hasil *crawling* media sosial, kemudian diambil sampel 1.000 baris untuk dilabeli. Label awal dibuat secara otomatis, yaitu oleh ChatGPT pada batch pertama dan oleh skrip kata kunci pada batch berikutnya. Baris yang ambigu ditandai dan ditinjau ulang dengan bantuan AI, sehingga dihasilkan dataset berlabel otomatis yang belum memiliki acuan hasil anotasi manusia.

Pada sampel acak dari dataset tersebut, anotator manusia menyusun label acuan tanpa melihat label otomatis. Tingkat kesepakatan antara label otomatis dan label acuan diukur menggunakan Cohen's Kappa, dan pola perbedaannya dianalisis per kelas. Selanjutnya, model klasifikasi sentimen berbasis TF-IDF dan SVM dibangun dan dievaluasi terhadap label otomatis maupun label acuan, serta dilatih dengan label otomatis dan label yang dikoreksi. Melalui alur ini, penelitian menjelaskan seberapa jauh kualitas label mempengaruhi performa model pada kelas sentimen negatif yang minoritas.
