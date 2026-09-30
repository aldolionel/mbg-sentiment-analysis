# BAB 1

# PENDAHULUAN

## 1.1 Latar Belakang

Program Makan Bergizi Gratis (MBG) merupakan salah satu program unggulan pemerintah yang menyasar perbaikan gizi anak sekolah secara nasional. Sebagai program dengan skala implementasi besar dan menyentuh kepentingan publik secara langsung, MBG memicu beragam respons di media sosial, mulai dari dukungan terhadap tujuan program hingga kritik terhadap pelaksanaan teknisnya di lapangan. Memahami sentimen publik terhadap program ini menjadi penting sebagai salah satu bentuk pemantauan opini yang dapat menjadi masukan evaluatif bagi pemangku kebijakan.

Penelitian analisis sentimen menggunakan metode *machine learning*, khususnya *Support Vector Machine* (SVM), telah banyak dilakukan pada berbagai isu kebijakan pemerintah di Indonesia, misalnya pada isu kinerja kementerian, kebijakan fiskal, hingga reshuffle kabinet. Mayoritas penelitian tersebut mengikuti pola yang seragam. Data dikumpulkan, dilabeli, digunakan untuk melatih model klasifikasi, kemudian dilaporkan metrik performanya. Proses pelabelan itu sendiri jarang dipertanyakan sebagai sumber bias yang berpotensi mempengaruhi hasil akhir, padahal proses ini menjadi fondasi dari seluruh *pipeline* analisis sentimen berbasis *supervised learning*. Kesalahan pada tahap pelabelan akan diwariskan ke tahap-tahap berikutnya tanpa disadari.

Seiring berkembangnya teknologi kecerdasan buatan generatif, pelabelan data berbantuan AI (*AI-assisted labeling*) mulai banyak digunakan sebagai alternatif pelabelan manual penuh yang memakan waktu dan biaya besar. Nasution dan Onan (2024) dalam studinya yang diterbitkan di *IEEE Access* membandingkan kualitas label yang dihasilkan manusia dengan label yang dihasilkan *Large Language Model* (LLM) pada tugas pemrosesan bahasa alami untuk bahasa bersumber daya rendah (*low-resource language*). Studi tersebut menemukan bahwa label AI dapat mendekati kualitas label manusia, namun tetap memiliki celah pada kasus-kasus linguistik yang kompleks. Jadhav dkk. (2025) juga menunjukkan bahwa LLM sebagai anotator memiliki keterbatasan signifikan ketika diterapkan pada bahasa bersumber daya rendah, terutama pada teks informal dan konteks budaya yang spesifik.

Pada praktiknya, penyusunan dataset berlabel sering menggabungkan beberapa mekanisme otomatis dengan peninjauan manusia yang terbatas, dan dataset penelitian ini disusun dengan cara tersebut. Label awal untuk 1.000 sampel dibuat secara otomatis. Batch pertama (50 sampel) dilabeli oleh model bahasa ChatGPT, sedangkan 19 batch berikutnya (950 sampel) dilabeli oleh skrip pencocokan kata kunci (*rule-based*). Baris yang dinilai ambigu ditandai untuk ditinjau ulang. Peninjauan tersebut sebagian besar dilakukan dengan bantuan AI dan disetujui oleh peneliti, sedangkan peninjauan langsung oleh peneliti hanya mencakup sebagian kecil sampel. Dengan demikian, dataset ini belum memiliki acuan (*gold standard*) hasil anotasi manusia independen, sehingga keandalan label otomatisnya belum diketahui.

Observasi awal terhadap dataset penelitian ini memberikan indikasi bahwa label otomatis kurang andal pada kelas negatif. Dari 1.000 sampel, 138 baris (13,8%) ditandai ambigu dan ditinjau ulang, dan 75 di antaranya berubah label, yaitu 67 dari netral menjadi negatif dan 8 dari netral menjadi positif. Akibatnya, proporsi kelas negatif meningkat dari 4,9% pada label awal menjadi 11,6% pada label akhir. Namun demikian, peninjauan hanya dilakukan pada baris berlabel awal netral yang ditandai ambigu dan sebagian besar dibantu AI, sedangkan 862 baris lainnya tidak ditinjau. Oleh karena itu, temuan ini baru berupa indikasi dan belum dapat dikonfirmasi tanpa acuan hasil anotasi manusia yang independen.

Indikasi tersebut relevan dengan permasalahan ketidakseimbangan kelas (*class imbalance*) yang umum dijumpai pada penelitian analisis sentimen kebijakan pemerintah di Indonesia. Pada kasus-kasus tersebut, kelas minoritas, dalam penelitian ini adalah kelas negatif, secara konsisten menunjukkan performa klasifikasi yang lebih rendah dibandingkan kelas mayoritas. Henning dkk. (2023) dalam tinjauan sistematisnya mengenai penanganan ketidakseimbangan kelas pada pemrosesan bahasa alami berbasis *deep learning* menekankan bahwa sumber ketidakseimbangan kelas tidak selalu bersifat alami dari distribusi data, tetapi dapat pula berasal dari proses anotasi yang bias. Kesulitan mendeteksi sentimen negatif pada teks media sosial berbahasa Indonesia juga erat kaitannya dengan fenomena sarkasme dan sentimen implisit, sebagaimana dibahas dalam berbagai literatur mengenai deteksi sarkasme pada analisis sentimen.

Penelitian-penelitian terdahulu yang menggabungkan SVM dengan teknik penyeimbangan kelas seperti SMOTE pada domain sentimen kebijakan pemerintah di Indonesia umumnya menempatkan sentimen negatif sebagai kelas mayoritas, misalnya pada isu reshuffle kabinet atau kritik kebijakan fiskal. Kondisi ini berbeda arah dengan kasus Program MBG, di mana sentimen negatif justru menjadi kelas minoritas. Penelitian-penelitian tersebut umumnya juga langsung menerapkan teknik penyeimbangan data pada tahap pemodelan, tanpa menelusuri kemungkinan bahwa sumber ketidakseimbangan tersebut telah terbentuk sejak tahap pelabelan data.

Berdasarkan uraian di atas, penelitian ini berupaya mengisi celah tersebut dengan mengevaluasi kualitas label otomatis terhadap acuan hasil anotasi manusia pada sampel acak, menganalisis pola perbedaannya, serta menguji dampaknya terhadap performa klasifikasi SVM pada kelas sentimen negatif yang minoritas. Aspek metodologis ini belum banyak dibahas secara eksplisit dalam literatur analisis sentimen berbahasa Indonesia yang telah ditinjau.

## 1.2 Rumusan Masalah

Berdasarkan latar belakang di atas, rumusan masalah dalam penelitian ini adalah sebagai berikut.

1. Seberapa tinggi tingkat kesepakatan antara label otomatis, yaitu hasil pelabelan awal dan tinjauan berbantuan AI, dengan label acuan hasil anotasi manusia pada sampel acak dataset opini publik Program MBG, diukur menggunakan Cohen's Kappa?
2. Pada kelas dan pola teks apa saja label otomatis paling sering berbeda dari label acuan hasil anotasi manusia, terutama pada kelas negatif?
3. Seberapa besar perbedaan performa model SVM pada kelas sentimen negatif apabila dievaluasi terhadap label otomatis dibandingkan terhadap label acuan hasil anotasi manusia, serta apabila dilatih dengan label otomatis dibandingkan dengan label yang dikoreksi berdasarkan acuan tersebut?
4. Bagaimana performa model TF-IDF dan SVM, baik pada konfigurasi awal maupun hasil *tuning*, dalam mengklasifikasikan sentimen publik terhadap Program MBG ke dalam kelas positif, negatif, dan netral, khususnya pada kelas minoritas?

## 1.3 Tujuan Penelitian

Sejalan dengan rumusan masalah, tujuan penelitian ini adalah sebagai berikut.

1. Mengukur tingkat kesepakatan antara label otomatis dan label acuan hasil anotasi manusia menggunakan Cohen's Kappa.
2. Mengidentifikasi dan mengkarakterisasi pola perbedaan antara label otomatis dan label acuan hasil anotasi manusia.
3. Menganalisis pengaruh kualitas label terhadap performa klasifikasi model SVM pada kelas sentimen negatif yang minoritas.
4. Membangun dan mengevaluasi model klasifikasi sentimen berbasis TF-IDF dan SVM, termasuk hasil *tuning* hyperparameter, terhadap data opini publik Program MBG.

## 1.4 Manfaat Penelitian

Secara teoritis, penelitian ini diharapkan memberikan kontribusi metodologis pada bidang analisis sentimen, berupa evaluasi keandalan pelabelan otomatis terhadap acuan hasil anotasi manusia dan keterkaitannya dengan permasalahan ketidakseimbangan kelas, sebuah aspek yang belum banyak dieksplorasi secara eksplisit dalam literatur analisis sentimen berbahasa Indonesia.

Secara praktis, bagi pemangku kepentingan Program MBG, hasil analisis sentimen dapat menjadi salah satu masukan pemantauan opini publik. Bagi peneliti atau praktisi lain yang menyusun dataset berlabel dengan pelabelan otomatis, penelitian ini memberikan gambaran empiris mengenai risiko kesalahan label yang perlu diantisipasi, khususnya pada teks berbahasa Indonesia informal.

## 1.5 Batasan Masalah

Agar penelitian lebih terarah, batasan masalah ditetapkan sebagai berikut.

1. Data yang digunakan adalah sampel sejumlah 1.000 baris dari dataset sekunder hasil *crawling* media sosial X terkait Program MBG, bukan keseluruhan populasi opini publik.
2. Klasifikasi sentimen dibatasi pada tiga kelas, yaitu positif, negatif, dan netral.
3. Model klasifikasi yang dianalisis dibatasi pada keluarga SVM (*Linear SVM*, *RBF SVM*, dan hasil *tuning*-nya) dengan representasi fitur TF-IDF. Perbandingan dengan model *deep learning* atau *transformer* berada di luar cakupan penelitian ini.
4. Label otomatis yang dievaluasi dibatasi pada proses yang telah diterapkan pada dataset ini, yaitu pelabelan awal oleh ChatGPT dan skrip kata kunci beserta tinjauan berbantuan AI. Perbandingan dengan model bahasa besar lain berada di luar cakupan penelitian ini.
5. Label acuan hasil anotasi manusia disusun pada sampel acak terbatas dari 1.000 baris, sehingga estimasi kualitas label berlaku untuk sampel tersebut dan bergantung pada jumlah anotator yang tersedia.
6. Hasil penelitian menggambarkan karakteristik sampel data yang digunakan dan tidak diklaim merepresentasikan opini publik Indonesia secara keseluruhan.
