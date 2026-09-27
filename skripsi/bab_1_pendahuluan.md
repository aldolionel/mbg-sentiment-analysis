# BAB 1

# PENDAHULUAN

## 1.1 Latar Belakang

Program Makan Bergizi Gratis (MBG) merupakan salah satu program unggulan pemerintah yang menyasar perbaikan gizi anak sekolah secara nasional. Sebagai program dengan skala implementasi besar dan menyentuh kepentingan publik secara langsung, MBG memicu beragam respons di media sosial, mulai dari dukungan terhadap tujuan program hingga kritik terhadap pelaksanaan teknisnya di lapangan. Memahami sentimen publik terhadap program ini menjadi penting sebagai salah satu bentuk pemantauan opini yang dapat menjadi masukan evaluatif bagi pemangku kebijakan.

Penelitian analisis sentimen menggunakan metode *machine learning*, khususnya *Support Vector Machine* (SVM), telah banyak dilakukan pada berbagai isu kebijakan pemerintah di Indonesia, misalnya pada isu kinerja kementerian, kebijakan fiskal, hingga reshuffle kabinet. Mayoritas penelitian tersebut mengikuti pola yang seragam. Data dikumpulkan, dilabeli, digunakan untuk melatih model klasifikasi, kemudian dilaporkan metrik performanya. Proses pelabelan itu sendiri jarang dipertanyakan sebagai sumber bias yang berpotensi mempengaruhi hasil akhir, padahal proses ini menjadi fondasi dari seluruh *pipeline* analisis sentimen berbasis *supervised learning*. Kesalahan pada tahap pelabelan akan diwariskan ke tahap-tahap berikutnya tanpa disadari.

Seiring berkembangnya teknologi kecerdasan buatan generatif, pelabelan data berbantuan AI (*AI-assisted labeling*) mulai banyak digunakan sebagai alternatif pelabelan manual penuh yang memakan waktu dan biaya besar. Nasution dan Onan (2024) dalam studinya yang diterbitkan di *IEEE Access* membandingkan kualitas label yang dihasilkan manusia dengan label yang dihasilkan *Large Language Model* (LLM) pada tugas pemrosesan bahasa alami untuk bahasa bersumber daya rendah (*low-resource language*). Studi tersebut menemukan bahwa label AI dapat mendekati kualitas label manusia, namun tetap memiliki celah pada kasus-kasus linguistik yang kompleks. Jadhav dkk. (2025) juga menunjukkan bahwa LLM sebagai anotator memiliki keterbatasan signifikan ketika diterapkan pada bahasa bersumber daya rendah, terutama pada teks informal dan konteks budaya yang spesifik.

Pada praktiknya, tidak semua pendekatan berbantuan AI menggunakan model bahasa besar yang sesungguhnya. Banyak *pipeline* penelitian, termasuk yang digunakan dalam penyusunan dataset penelitian ini, menerapkan pendekatan pelabelan awal semi-otomatis berbasis aturan (*rule-based*) menggunakan heuristik kata kunci sebagai tahap percepatan sebelum dilakukan adjudikasi atau peninjauan ulang oleh manusia. Pendekatan semacam ini belum banyak diteliti secara eksplisit dari sisi keandalannya, khususnya terkait pola kesalahan sistematis yang mungkin ditinggalkannya.

Observasi awal terhadap dataset penelitian ini menunjukkan indikasi ke arah tersebut. Dari 1.000 sampel data yang melalui proses pelabelan awal semi-otomatis dan kemudian diadjudikasi secara manual, tingkat kesepakatan antara label awal dan label akhir tercatat sebesar 92,5%, dengan nilai Cohen's Kappa sebesar 0,868. Nilai ini termasuk kategori kesepakatan hampir sempurna menurut skala Landis dan Koch (1977). Meskipun angka tersebut tampak tinggi, seluruh 75 kasus ketidaksepakatan berasal dari label awal netral yang dikoreksi menjadi kelas lain saat adjudikasi manual. Sebanyak 67 di antaranya dikoreksi menjadi negatif dan hanya 8 menjadi positif. Akibatnya, proporsi kelas negatif meningkat lebih dari dua kali lipat, dari 4,9% pada label awal menjadi 11,6% pada label akhir. Pola ini mengindikasikan bahwa pelabelan semi-otomatis secara sistematis cenderung menyembunyikan sinyal sentimen negatif ke dalam kelas netral sebagai nilai bawaan, bukan salah mengklasifikasikannya secara acak ke berbagai arah.

Temuan tersebut relevan dengan permasalahan ketidakseimbangan kelas (*class imbalance*) yang umum dijumpai pada penelitian analisis sentimen kebijakan pemerintah di Indonesia. Pada kasus-kasus tersebut, kelas minoritas, dalam penelitian ini adalah kelas negatif, secara konsisten menunjukkan performa klasifikasi yang lebih rendah dibandingkan kelas mayoritas. Henning dkk. (2023) dalam tinjauan sistematisnya mengenai penanganan ketidakseimbangan kelas pada pemrosesan bahasa alami berbasis *deep learning* menekankan bahwa sumber ketidakseimbangan kelas tidak selalu bersifat alami dari distribusi data, tetapi dapat pula berasal dari proses anotasi yang bias. Kesulitan mendeteksi sentimen negatif pada teks media sosial berbahasa Indonesia juga erat kaitannya dengan fenomena sarkasme dan sentimen implisit, sebagaimana dibahas dalam berbagai literatur mengenai deteksi sarkasme pada analisis sentimen.

Penelitian-penelitian terdahulu yang menggabungkan SVM dengan teknik penyeimbangan kelas seperti SMOTE pada domain sentimen kebijakan pemerintah di Indonesia umumnya menempatkan sentimen negatif sebagai kelas mayoritas, misalnya pada isu reshuffle kabinet atau kritik kebijakan fiskal. Kondisi ini berbeda arah dengan kasus Program MBG, di mana sentimen negatif justru menjadi kelas minoritas. Penelitian-penelitian tersebut umumnya juga langsung menerapkan teknik penyeimbangan data pada tahap pemodelan, tanpa menelusuri kemungkinan bahwa sumber ketidakseimbangan tersebut telah terbentuk sejak tahap pelabelan data.

Berdasarkan uraian di atas, penelitian ini berupaya mengisi celah tersebut. Selain membangun model klasifikasi sentimen berbasis SVM terhadap opini publik Program MBG, penelitian ini juga menganalisis secara eksplisit apakah bias sistematis pada tahap pelabelan semi-otomatis berkontribusi terhadap kesulitan deteksi kelas sentimen negatif yang minoritas. Aspek metodologis ini belum banyak dibahas secara eksplisit dalam literatur analisis sentimen berbahasa Indonesia yang telah ada.

## 1.2 Rumusan Masalah

Berdasarkan latar belakang di atas, rumusan masalah dalam penelitian ini adalah sebagai berikut.

1. Seberapa tinggi tingkat kesepakatan antara label hasil pelabelan semi-otomatis dengan label akhir hasil adjudikasi manual pada dataset opini publik Program MBG, diukur menggunakan Cohen's Kappa?
2. Apakah terdapat pola kesalahan sistematis pada teks yang dikoreksi selama proses adjudikasi manual, dan bagaimana karakteristik pola tersebut?
3. Apakah bias sistematis pada tahap pra-pelabelan berkontribusi terhadap rendahnya performa klasifikasi model SVM pada kelas sentimen negatif yang minoritas?
4. Bagaimana performa model TF-IDF dan SVM, baik pada konfigurasi awal maupun hasil *tuning*, dalam mengklasifikasikan sentimen publik terhadap Program MBG ke dalam kelas positif, negatif, dan netral, khususnya pada kelas minoritas?

## 1.3 Tujuan Penelitian

Sejalan dengan rumusan masalah, tujuan penelitian ini adalah sebagai berikut.

1. Mengukur tingkat kesepakatan antara label pra-pelabelan semi-otomatis dan label hasil adjudikasi manual menggunakan Cohen's Kappa.
2. Mengidentifikasi dan mengkarakterisasi pola kesalahan sistematis yang muncul selama proses adjudikasi manual.
3. Menganalisis keterkaitan antara bias pada tahap pelabelan dengan performa klasifikasi model pada kelas sentimen negatif yang minoritas.
4. Membangun dan mengevaluasi model klasifikasi sentimen berbasis TF-IDF dan SVM, termasuk hasil *tuning* hyperparameter, terhadap data opini publik Program MBG.

## 1.4 Manfaat Penelitian

Secara teoritis, penelitian ini diharapkan memberikan kontribusi metodologis pada bidang analisis sentimen, berupa evaluasi keandalan pendekatan pelabelan semi-otomatis dan keterkaitannya dengan permasalahan ketidakseimbangan kelas, sebuah aspek yang belum banyak dieksplorasi secara eksplisit dalam literatur analisis sentimen berbahasa Indonesia.

Secara praktis, bagi pemangku kepentingan Program MBG, hasil analisis sentimen dapat menjadi salah satu masukan pemantauan opini publik. Bagi peneliti atau praktisi lain yang menggunakan pendekatan pelabelan semi-otomatis dalam menyusun dataset berlabel, penelitian ini memberikan gambaran empiris mengenai risiko bias yang perlu diantisipasi, khususnya pada teks berbahasa Indonesia informal.

## 1.5 Batasan Masalah

Agar penelitian lebih terarah, batasan masalah ditetapkan sebagai berikut.

1. Data yang digunakan adalah sampel berlabel sejumlah 1.000 baris hasil crawling media sosial terkait Program MBG, bukan keseluruhan populasi opini publik.
2. Klasifikasi sentimen dibatasi pada tiga kelas, yaitu positif, negatif, dan netral.
3. Model klasifikasi yang dianalisis dibatasi pada keluarga SVM (*Linear SVM*, *RBF SVM*, dan hasil *tuning*-nya) dengan representasi fitur TF-IDF. Perbandingan dengan model *deep learning* atau *transformer* berada di luar cakupan penelitian ini.
4. Analisis bias pelabelan difokuskan pada pendekatan semi-otomatis berbasis aturan yang telah diterapkan pada penyusunan dataset ini, bukan perbandingan berbagai jenis model *AI-assisted labeling* lain seperti LLM komersial.
5. Hasil penelitian menggambarkan karakteristik sampel data yang digunakan dan tidak diklaim merepresentasikan opini publik Indonesia secara keseluruhan.
