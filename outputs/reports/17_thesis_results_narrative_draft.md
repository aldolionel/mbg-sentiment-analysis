# 17 Thesis Results Narrative Draft

## Distribusi Label
Dataset yang digunakan pada tahap pemodelan terdiri dari 1000 data berlabel yang merupakan sampel dari hasil crawling media sosial terkait MBG. Label pada dataset ini diperoleh melalui proses AI-assisted labeling dengan adjudication/manual review, sehingga hasil analisis perlu dipahami sebagai gambaran pada sampel berlabel, bukan sebagai klaim universal mengenai opini publik.

Distribusi label menunjukkan bahwa kelas `netral` berjumlah 472 data (47.20%), kelas `positif` berjumlah 412 data (41.20%), dan kelas `negatif` berjumlah 116 data (11.60%). Ketidakseimbangan ini menjadi pertimbangan penting dalam pemilihan metrik evaluasi model.

## Perbandingan Model Baseline
Pada eksperimen baseline, beberapa model klasifikasi klasik dibandingkan menggunakan representasi fitur TF-IDF, yaitu Multinomial Naive Bayes, Logistic Regression, Linear SVM, dan RBF SVM. Perbandingan ini bertujuan memberikan gambaran awal mengenai performa model sebelum tuning lebih lanjut pada keluarga SVM.

Karena distribusi label tidak seimbang, macro F1 digunakan sebagai metrik utama. Macro F1 lebih sesuai dibandingkan akurasi saja karena memberikan bobot yang sama pada setiap kelas, termasuk kelas `negatif` yang jumlah datanya paling sedikit.

## Hasil Tuning SVM
Tuning SVM dilakukan pada LinearSVC, SVC dengan kernel linear, dan SVC dengan kernel RBF. Hasil tuning menunjukkan bahwa Tuned LinearSVC memperoleh macro F1 sebesar 0.7278 pada data uji, dengan akurasi sebesar 0.7950.

Dibandingkan baseline Linear SVM, tuning meningkatkan macro F1 dari 0.6971 menjadi 0.7278. Peningkatan absolut sebesar 0.0306 atau sekitar 3.06 percentage points menunjukkan bahwa pemilihan parameter berpengaruh terhadap performa model SVM.

## Pemilihan Model Terbaik
Berdasarkan macro F1 sebagai metrik utama, model yang direkomendasikan adalah Tuned LinearSVC + TF-IDF. Model ini dipilih karena menghasilkan macro F1 tertinggi di antara model baseline dan model SVM hasil tuning, yaitu 0.7278.

Pemilihan Tuned LinearSVC juga sejalan dengan fokus penelitian pada model SVM. Dengan kombinasi TF-IDF dan tuning hyperparameter, model ini memberikan performa yang lebih baik dibandingkan Linear SVM baseline dan juga melampaui Logistic Regression baseline pada macro F1.

## Keterbatasan
Meskipun Tuned LinearSVC memberikan performa terbaik secara keseluruhan, performa pada kelas `negatif` masih perlu dicermati. Pada model Tuned LinearSVC, F1 untuk kelas `negatif` adalah 0.5238, dengan recall 0.4783. Nilai ini menunjukkan bahwa model masih mengalami tantangan dalam mengenali sentimen negatif secara konsisten.

Keterbatasan lain adalah ukuran dataset berlabel yang berjumlah 1.000 sampel dari kumpulan data crawling yang lebih besar. Selain itu, proses pelabelan bersifat AI-assisted dengan adjudication/manual review, sehingga validasi manual yang lebih luas dapat menjadi arah pengembangan penelitian berikutnya.

## Ringkasan Temuan
Secara keseluruhan, hasil pemodelan menunjukkan bahwa pendekatan TF-IDF + Tuned LinearSVC merupakan model yang paling sesuai untuk digunakan sebagai model akhir pada tahap pembahasan hasil. Macro F1 digunakan sebagai dasar pemilihan karena dataset memiliki distribusi label yang tidak seimbang.

Temuan ini mendukung penggunaan SVM yang telah dituning sebagai pendekatan klasifikasi sentimen MBG pada sampel berlabel. Namun, interpretasi hasil tetap perlu dibatasi pada dataset sampel yang digunakan dan tidak boleh digeneralisasikan sebagai opini publik secara keseluruhan.