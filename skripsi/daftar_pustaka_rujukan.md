# Daftar Pustaka Rujukan (Working Bibliography)

Dokumen ini berisi metadata dan tautan (DOI/URL) untuk paper rujukan yang dibahas selama proses ideation penelitian ini. Tidak ada file PDF yang diunggah ke repository ini; setiap paper diakses langsung dari sumber aslinya melalui tautan di bawah.

Status indeksasi (Scopus/Sinta) dicantumkan berdasarkan reputasi umum venue pada saat penyusunan dokumen ini. Sebelum dipakai di daftar pustaka final skripsi, verifikasi ulang status indeksasi masing-masing jurnal secara langsung di scopus.com/sources atau sinta.kemdikbud.go.id, karena status ini dapat berubah.

## A. Rujukan Utama — Metodologi Pelabelan AI/Semi-Otomatis

1. Nasution, A. H., & Onan, A. (2024). ChatGPT Label: Comparing the Quality of Human-Generated and LLM-Generated Annotations in Low-Resource Language NLP Tasks. *IEEE Access*, 12, 71876–71900. https://doi.org/10.1109/ACCESS.2024.3402809
   - Status: IEEE Access, Scopus-indexed (Open Access, CC BY).
   - Peran: rujukan utama metodologi pengukuran kesepakatan label AI vs manusia; dasar perbandingan Cohen's Kappa.

2. Nasution, A. H., et al. (2025). Benchmarking Open-Source Large Language Models for Sentiment and Emotion Classification in Indonesian Tweets. *IEEE Access*. https://doi.org/10.1109/ACCESS.2025.3574629
   - Status: IEEE Access, Scopus-indexed. **Daftar penulis lengkap belum terverifikasi dari pencarian ini — cek halaman IEEE Xplore sebelum disitasi.**
   - Peran: baseline performa LLM sungguhan (ChatGPT-4 macro F1 0.84) di Bahasa Indonesia; pembanding untuk pendekatan rule-based di penelitian ini.

3. Jadhav, S., Shanbhag, A., Thakurdesai, A., Sinare, R., & Joshi, R. (2025). On Limitations of LLM as Annotator for Low Resource Languages. *Proceedings of the 8th International Conference on Natural Language and Speech Processing (ICNLSP 2025)*, 277–282. https://aclanthology.org/2025.icnlsp-1.27/
   - Status: ACL Anthology (prosiding ICNLSP), Open Access.
   - Peran: landasan argumen keterbatasan AI/LLM sebagai anotator pada bahasa bersumber daya rendah.

## B. Rujukan Utama — Class Imbalance & Kelas Minoritas

4. Henning, S., Beluch, W., Fraser, A., & Friedrich, A. (2023). A Survey of Methods for Addressing Class Imbalance in Deep-Learning Based Natural Language Processing. *Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2023)*, 523–540. https://aclanthology.org/2023.eacl-main.38/
   - Status: ACL Anthology, prosiding EACL (top-tier NLP conference), Open Access.
   - Peran: landasan teori taksonomi penyebab dan solusi class imbalance di NLP.

5. Taskiran, S. F., Turkoglu, B., Kaya, E., & Asuroglu, T. (2025). A comprehensive evaluation of oversampling techniques for enhancing text classification performance. *Scientific Reports*, 15(1). https://doi.org/10.1038/s41598-025-05791-7
   - Status: Scientific Reports (Nature Portfolio), Scopus/SCIE-indexed, Open Access.
   - Peran: dasar teknis pemilihan metode oversampling (SMOTE dan variannya).

## C. Rujukan Pendukung — Sarkasme & Sentimen Implisit

6. Joshi, A., Bhattacharyya, P., & Carman, M. J. (2017). Automatic Sarcasm Detection: A Survey. *ACM Computing Surveys*, 50(5), Article 73. https://doi.org/10.1145/3124420
   - Status: ACM Computing Surveys, Scopus Q1. **Kemungkinan paywalled** (bukan Open Access) — akses via langganan kampus/perpustakaan.
   - Peran: landasan teori umum sarkasme sebagai penyebab kesalahan klasifikasi sentimen.

7. Kunneman, F., Liebrecht, C., van Mulken, M., & van den Bosch, A. (2015). Signaling sarcasm: From hyperbole to hashtag. *Information Processing & Management*, 51(4), 500–509. https://doi.org/10.1016/j.ipm.2014.07.006
   - Status: Information Processing & Management (Elsevier), Scopus Q1. **Kemungkinan paywalled.**
   - Peran: penanda linguistik sarkasme (hiperbola, hashtag) yang relevan untuk menjelaskan pola netral→negatif pada data penelitian ini.

8. Lunando, E., & Purwarianti, A. (2015). Indonesian Social Media Sentiment Analysis with Sarcasm Detection. *arXiv:1505.03085*. https://arxiv.org/abs/1505.03085
   - Status: arXiv preprint, Open Access, belum tentu peer-reviewed.
   - Peran: preseden spesifik Bahasa Indonesia bahwa sarkasme di medsos merupakan tantangan tersendiri.

## D. Related Work — Domain Sejenis (Sentimen Kebijakan Pemerintah + SMOTE)

9. Pateman, D., Prasetyo, T. F., & Sujadi, H. (2025). Sentiment Analysis of Government on TikTok and X Platforms with SVM and SMOTE Approach. *JITK (Jurnal Ilmu Pengetahuan dan Teknologi Komputer)*, 10(4), 900–908. https://doi.org/10.33480/jitk.v10i4.6645
   - Status: Jurnal nasional (Sinta), kemungkinan Open Access via OJS.
   - Peran: "closest related work" dari sisi metode (SVM+SMOTE) dan domain (sentimen pemerintah); arah imbalance berlawanan dengan kasus MBG (negatif mayoritas di sana, minoritas di MBG).

10. [Penulis belum terverifikasi]. (2026). An Ablation Study on Stacked LSTM and SMOTE for Government Policy Sentiment Classification. *Scientific Journal of Informatics*, 13(3), 569–580. https://doi.org/10.15294/sji.v13i3.53853
    - Status: Jurnal nasional UNNES (Sinta), kemungkinan Open Access. **PENTING: paper ini langsung membahas sentimen kebijakan Program MBG (komentar Instagram) dengan Stacked LSTM + SMOTE.** Ini kandidat kuat "direct related work" — wajib dibaca lengkap dan disitasi eksplisit di Bab 1/2 untuk memperkuat posisi novelty (fokus penelitian ini pada bias pelabelan semi-otomatis belum dibahas di paper tersebut).
    - **Nama penulis perlu dicek langsung di halaman jurnal sebelum disitasi.**

11. Rofi'i. (2026). Implementasi SMOTE dan GrideSearchCV untuk Klasifikasi Sentimen Imbalanced pada Isu Reshuffle Kabinet. *VOCATECH: Vocational Education and Technology Journal*. https://ojs.aknacehbarat.ac.id/index.php/vocatech/article/view/305
    - Status: Jurnal nasional (Sinta), kemungkinan Open Access. **Volume/issue/halaman belum terverifikasi dari pencarian ini.**
    - Peran: preseden metodologis kombinasi SMOTE + GridSearchCV pada domain sentimen kebijakan pemerintah Indonesia.

## E. Catatan Penting — Paper Lain yang Langsung Membahas Topik MBG

Daftar ini ditemukan saat pengecekan positioning gap, belum sepenuhnya dibaca lengkap. Tujuannya sebagai alarm bahwa domain "analisis sentimen MBG" sendiri sudah mulai ramai diteliti pada 2025-2026, sehingga wajib dicek satu per satu apakah ada yang bersinggungan dengan sudut pandang penelitian ini (bias pelabelan semi-otomatis terhadap kelas minoritas).

- Munir, R. A. (2025). Analisis Sentimen Cuitan di Media Sosial X tentang Program Makan Bergizi Gratis dengan Metode NLP. *Jurnal Informatika dan Teknik Elektro Terapan*, 13(3). https://journal.eng.unila.ac.id/index.php/jitet/article/view/6912
- Riwaldi, M. R. F., & Aripin. (2026). Hybrid CNN-BiLSTM untuk Analisis Sentimen Multi-Platform terhadap Insiden Keamanan Pangan Program Makan Bergizi Gratis. *Building of Informatics, Technology and Science (BITS)*, 8(1). https://doi.org/10.47065/bits.v8i1.9896
- Beberapa skripsi/paper lain ditemukan membahas MBG + SVM di platform YouTube, TikTok, serta perbandingan SVM vs IndoBERT dan SVM+KNN dengan TF-IDF/TF-ABS. Judul dan penulis lengkap belum dicatat di sini; disarankan pencarian manual lanjutan via Google Scholar/Garuda dengan kata kunci "Makan Bergizi Gratis" + "sentimen" + "SVM" sebelum menyusun Bab II secara final.

---

**Catatan umum**: dokumen ini adalah working bibliography hasil riset literatur assisted-AI pada tahap ideation. Sebelum masuk ke Bab II/Daftar Pustaka final skripsi, seluruh metadata (terutama nama penulis dan volume/issue yang ditandai "belum terverifikasi") wajib dicek ulang langsung ke halaman jurnal aslinya oleh adik ipar Anda.
