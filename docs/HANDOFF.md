# Handoff Proyek: Skripsi Analisis Sentimen MBG

Dibuat: 2026-10-11, di akhir sesi cloud Claude Code (branch `claude/adoring-heisenberg-t05kny`).
Tujuan: agar sesi baru bisa melanjutkan pekerjaan tanpa membaca percakapan sebelumnya. Dokumen ini sengaja tidak memuat rahasia (API key, kredensial) maupun penilaian personal tentang pihak ketiga.

## 0. Baca ini dulu

- **Proyek:** skripsi S1 Sistem Informasi (Universitas Muhammadiyah Jember) tentang analisis sentimen publik terhadap Program Makan Bergizi Gratis (MBG), memakai TF-IDF dan SVM.
- **Klaim kebaruan yang dituju:** bukan topik dan bukan algoritma, melainkan **kerangka pelabelan data sentimen**: mengukur kualitas label otomatis terhadap anotasi manusia dan dampaknya pada performa kelas minoritas (negatif). Topik dan algoritma hanya testbed dan baseline.
- **Status:** draf Bab 1-3 ada (md dan docx, format institusi). Bab 4-5 sengaja belum ditulis sampai seluruh pengujian selesai.
- **Sedang ditunggu:** 307 baris sampel gold yang dilabeli manusia (lihat bagian 6).
- **Rencana berikutnya:** mengumpulkan data baru hasil scraping sendiri (rencana: komentar YouTube lewat notebook Google Colab). Dosen pembimbing mewajibkan data primer.
- **Jangan lakukan:** menulis Bab 4-5 sebelum pengujian selesai; menyebut label sebagai "adjudikasi manual" atau "gold standard"; membuat ulang sampel gold; membuka atau membagikan file kunci sampel gold; mengunggah PDF paper pihak ketiga ke repo; menaruh API key di chat atau repo; push ke `main`.

Prompt pembuka yang disarankan untuk thread baru: *"Baca `docs/HANDOFF.md` dulu, lalu ringkas status dan keputusan yang masih terbuka sebelum mengerjakan apa pun."*

## 1. Peran dan cara bekerja

- Pengguna adalah pembantu penulis skripsi (bukan mahasiswanya). Mahasiswa adalah penulis skripsi dan yang berhubungan langsung dengan dosen pembimbing. Percakapan berbahasa Indonesia santai.
- Sesi cloud tidak punya akses ke komputer lokal pengguna maupun browsernya. Pengguna menjalankan hal-hal lokal (anotasi, Colab, API key) sendiri.
- Pengguna ingin melihat teks skripsi lebih dulu sebelum dianggap final, tetapi hook repo memaksa commit dan push di akhir giliran bila ada perubahan. Semua push hanya ke branch fitur, tidak pernah ke `main`.

## 2. Arahan dosen pembimbing (dari ekstraksi rekaman pihak ketiga)

1. Opsi alternatif yang ditawarkan: Latent Class Analysis untuk tipologi digitalisasi dan kinerja ekonomi usaha formal non-pertanian, dilanjutkan uji beda antar kelas. **Tidak diambil.**
2. Jika tetap analisis sentimen: **wajib scraping data sendiri**, tidak memakai data lampau milik orang lain, dan wajib ada kebaruan (contoh dari dosen: platform atau algoritma berbeda; kata "misalnya" berarti contoh tidak eksklusif).
3. Segera putuskan topik, kebaruan, dan kumpulkan rancangan.

Pembaruan dari pengguna: topik dan judul sudah mendapat persetujuan (go ahead); yang berubah hanya sumber data (data baru hasil scraping sendiri). **Judul persis yang disetujui perlu dikonfirmasi** (lihat bagian 11).

## 3. Fakta kunci tentang data dan pelabelan

**Dataset sumber (lama)**
- Dataset sekunder dari Sultoni dkk. (2025), *Public Sentiment Analysis and Distribution Optimization MBG*, JMT 7(1), 35-53. X/Twitter, 47.803 unggahan (jumlah di publikasi aslinya), `data/raw/data crawl mbg (in).xlsx`.
- Tidak ada kolom tanggal; rentang waktu, kata kunci lengkap, dan lisensi tidak terdokumentasi dan tidak boleh dikarang. Detail ada di `docs/dataset_provenance.md`.
- Pool: 73.900 baris interim, 15,5% duplikat, sisa **62.446 teks unik** (`data/processed/mbg_labeling_ready.csv`), median 14 kata. Hanya 1.000 yang dilabeli; 61.446 belum dipakai.

**Sampel berlabel**
- `data/processed/mbg_labeled_sample_1000.csv`: 1.000 baris, 20 batch x 50. Label final: negatif 116, netral 472, positif 412.
- Kolom penting: `batch_id, sample_id, clean_text, label, label_before_adjudication, label_after_adjudication, adjudication_applied, human_label, human_notes, adjudication_review_reason`.

**Siapa yang melabeli (berdasarkan bukti di data, belum seluruhnya dikonfirmasi pengguna)**
- Batch 001 (50 baris): label dari LLM (ChatGPT) lewat prompt di `data/processed/annotation_prompts/`; catatan `labeling_notes` berupa kalimat bebas; 15 dari 50 berlabel negatif.
- Batch 002-020 (950 baris): label dari skrip kata kunci `scripts/label_batch_rule_based.py` (sebelumnya bernama dengan nama tool AI, sudah di-rename). Bukti: 100% `labeling_notes` identik dengan kalimat tetap skrip. Pada batch 003-020 hanya 33 dari 900 berlabel negatif. Pengguna menyebut semua `labeling_notes` berasal dari ChatGPT; kemungkinan skrip itu dibuat dan dijalankan agen AI OpenAI. **Perlu konfirmasi.**
- Penandaan baris untuk ditinjau: `scripts/create_semantic_review.py` menandai teks sangat pendek atau yang catatannya menyebut "ambigu/informatif". Hasil: **138 baris ditandai** (137 berlabel awal netral, 1 positif), **862 baris tidak ditandai** (410 netral, 403 positif, 49 negatif) dan tidak pernah ditinjau siapa pun.
- Tinjauan 138 baris: dilakukan AI (ada file `data/processed/adjudication/master_adjudication_template_003_020_REVIEWED_AI.xlsx`) dan disetujui pengguna. Menurut pengguna, hanya kurang dari 20 sampel yang ia tinjau sendiri dan `human_notes` sebagian besar berupa persetujuan formalitas.
- Hasil tinjauan: 75 label berubah (67 netral ke negatif, 8 netral ke positif). Proporsi negatif naik dari 49 (4,9%) ke 116 (11,6%).
- **Tidak ada gold standard manusia.** `data/processed/validation/validation_sample_200_*` hanya template dan versi terisi AI, tanpa anotasi manusia; digantikan oleh sampel gold 307 baris (bagian 6).

**Hasil pemodelan yang sudah ada (terhadap label otomatis, bukan gold)**
- Model terpilih: TF-IDF + Tuned LinearSVC, macro F1 0,7278, akurasi 0,795 (test 200 baris). Baseline: Logistic Regression 0,7151, Linear SVM 0,6971, RBF SVM 0,6072, Multinomial NB 0,5187. CV macro F1 Tuned LinearSVC 0,6924 +/- 0,0298. Pemilihan model terutama berdasarkan test set; selisih antar SVM tuned kecil.
- Kelas negatif: F1 0,5238, recall 0,4783 (11 benar dari 23 baris negatif di test, 12 salah).
- Cek near-duplicate train/test: 0 baris. SMOTE belum diimplementasikan (`imbalanced-learn` ada di requirements tetapi tidak dipakai di `src/`); ablation `class_weight` sudah ada.

## 4. Koreksi penting atas klaim sebelumnya (jangan diulang)

1. **Kappa 0,868 dan agreement 92,5% antara label awal dan akhir tidak valid sebagai ukuran kualitas.** 862 baris tidak pernah ditinjau sehingga pasti sama; pada 138 baris yang ditinjau hanya 63 (45,7%) yang tidak berubah. Tinjauan hanya menyasar baris berlabel awal netral yang ditandai, jadi pola "semua koreksi berasal dari netral" sebagian besar artefak desain, bukan bukti bias sistematis.
2. Pra-label **bukan seluruhnya rule-based**: batch 001 dari LLM.
3. Istilah "adjudikasi manual" dan "AI-assisted labeling dengan manual review" tidak boleh dipakai; yang akurat: pelabelan otomatis (LLM dan skrip kata kunci), tinjauan ulang berbantuan AI pada baris yang ditandai, verifikasi manusia minimal, belum ada gold independen.
4. Bug konverter docx: tabel Markdown multi-kolom sempat tidak ter-render (sudah diperbaiki di `scripts/convert_skripsi_bab_to_docx.py`; selalu cek `len(doc.tables)` setelah konversi).

Bab 1-3 dan docs sudah dikoreksi sesuai butir di atas (commit `a58169b`). Folder `paper/` dan laporan lama di `outputs/reports/` **belum** dikoreksi dan masih memuat klaim lama.

## 5. Desain penelitian saat ini

**Rumusan masalah (versi Bab 1)**
1. Seberapa tinggi kesepakatan (Cohen's Kappa) antara label otomatis (pelabelan awal dan tinjauan berbantuan AI) dan label acuan anotasi manusia pada sampel acak?
2. Pada kelas dan pola teks apa label otomatis paling sering berbeda dari acuan manusia, terutama kelas negatif?
3. Seberapa besar perbedaan performa SVM pada kelas negatif bila dievaluasi terhadap label otomatis vs acuan manusia, dan bila dilatih dengan label otomatis (skenario A) vs label terkoreksi (skenario B)?
4. Bagaimana performa TF-IDF + SVM (baseline dan tuning), khususnya kelas minoritas?

**Kerangka yang diusulkan (konsep, belum dituliskan sebagai dokumen)**
(1) pelabelan otomatis, (2) penandaan keraguan, (3) audit manusia bertingkat termasuk baris yang tidak ditandai, (4) estimasi kesalahan berbobot per kelas, (5) uji dampak ke SVM pada kelas minoritas.
**Hipotesis (belum teruji):** tinjauan yang hanya menyasar baris ditandai meleset dari kesalahan label sebenarnya, terutama pada negatif implisit atau sarkasme. Hasil gold bisa saja menyangkalnya; klaim harus mengikuti data.

**Desain evaluasi**
- Skenario B memakai validasi silang pada baris gold agar tidak bocor (baris gold uji tidak dipakai melatih pada lipatan yang sama; baris non-gold selalu berlabel otomatis).
- Laporkan hasil kelas negatif dengan interval kepercayaan bootstrap (negatif di test sangat sedikit).
- Evaluasi tambahan: algoritma lain (LogReg, NB, mungkin IndoBERT) hanya sebagai uji ketahanan kesimpulan.
- **Protokol pengujian belum ditulis.** Rencananya dibekukan (data, metrik, seed, kriteria) sebelum melihat hasil gold.

**Literatur yang belum ditelaah tetapi diperlukan untuk menjaga klaim kebaruan:** pelabelan dengan LLM, *human-in-the-loop*, *weak supervision*, dan deteksi label noise. Penelitian sentimen MBG sudah banyak (2025-2026, termasuk Stacked LSTM+SMOTE di Scientific Journal of Informatics UNNES 2026), jadi kebaruan topik lemah; kebaruan harus di kerangka pelabelan.

## 6. Pekerjaan berjalan: anotasi gold

**Sampel:** `scripts/create_gold_annotation_sample.py` (seed 42), 307 baris, bertingkat:

| Kelompok | Populasi di 1.000 | Diambil |
|---|---|---|
| ditandai perlu tinjauan (`flagged`) | 138 | 138 (semua) |
| tidak ditandai, label negatif | 49 | 49 (semua) |
| tidak ditandai, label positif | 403 | 60 (acak) |
| tidak ditandai, label netral | 410 | 60 (acak) |

**File**
- Untuk anotator (buta, di repo): `data/processed/validation/gold_annotation_blind.xlsx` dan `.csv`. Kolom: `item_id` (G001-G307, diacak), `clean_text`, `annotator_label` (wajib: positif/negatif/netral, ada dropdown di xlsx), `annotator_notes` (opsional).
- Kunci (JANGAN dibuka anotator): `data/processed/validation/gold_annotation_key.private.csv`, di-gitignore (`*.private.csv`), hanya ada di container sesi yang membuatnya. Kolom: `item_id, sample_id, batch_id, stratum, stratum_population, auto_label_initial, auto_label_final`.
- **Regenerasi kunci di sesi baru:** jalankan `python scripts/create_gold_annotation_sample.py` (butuh `openpyxl`), lalu **verifikasi bahwa `gold_annotation_blind.csv` hasil regenerasi identik dengan versi di repo** (`git diff`) sebelum memakai kunci. Jika berbeda (mis. beda versi Python), jangan pakai kunci hasil regenerasi.
- Jangan menjalankan ulang skrip dengan ukuran berbeda setelah anotasi dimulai (ID dan urutan berubah).

**Rencana anotator:** 2 anotator independen (penulis skripsi dan satu orang yang belum terlibat serta tidak tahu hipotesis), penutur Indonesia akrab bahasa medsos, tahu konteks MBG, tidak memakai AI. Latihan 20 contoh di luar 307 baris disarankan tetapi **belum dibuat** (bisa diambil dari pool 62 ribu yang tidak ada di sampel). Pedoman: `docs/annotation_guideline_mbg_sentiment.md` (PDF 3 halaman sudah dikirim ke pengguna, tidak disimpan di repo) dan `docs/annotation_codebook_mbg_sentiment.md`. Waktu perkiraan 1,5-2,5 jam per orang. Perbedaan antar anotator diselesaikan lewat diskusi atau orang ketiga; Kappa antar-manusia dihitung dari label mentah sebelum diskusi.

**Analisis setelah label masuk** (script belum ditulis): estimator bertingkat dengan bobot `N_h / n_h` per kelompok untuk menaksir kualitas label pada 1.000 baris; jangan menghitung akurasi langsung dari 307 baris. Hitung Kappa (antar-manusia, otomatis vs gold), presisi dan recall per kelas, matriks konfusi, kategori pola kesalahan (sarkasme, kritik implisit, negasi, teks pendek, konteks kurang), lalu eksperimen skenario A vs B.

## 7. Rencana: pengumpulan data baru (belum dikerjakan)

**Sumber utama yang disarankan: komentar YouTube via YouTube Data API v3, dijalankan di Google Colab.**
- Gratis, kuota default 10.000 unit per hari; `commentThreads.list` berbiaya 1 unit per halaman (maksimal 100 komentar). Komentar lama dapat diambil. (Diverifikasi lewat pencarian web, Oktober 2026.)
- Hemat kuota: setahu penulis, `search.list` berbiaya 100 unit per panggilan sehingga sebaiknya dihindari; gunakan daftar unggahan kanal (`playlistItems`) lalu saring judul yang menyebut MBG di sisi klien. **Biaya selain `commentThreads.list` belum diverifikasi; cek tabel kuota resmi.**
- Rancangan notebook Colab: API key dari Colab Secrets (tidak pernah di notebook atau chat), keluaran dan checkpoint ke Google Drive, dapat dilanjutkan jika sesi putus (batas idle dan sekitar 12 jam), berhenti otomatis di sekitar 9.500 unit lalu lanjut hari berikutnya (kuota direset tengah malam Pasifik), dua keluaran: data mentah privat di Drive dan CSV interim bebas identitas untuk repo. Konfigurasi (kanal, jendela tanggal, batas komentar per video) di satu sel.
- Desain pengambilan: per video/kanal, **bukan per kata kunci sentimen** (filter kata negatif membuat sampel terlalu mudah dan merusak pengujian kerangka); batasi komentar per video; hapus duplikat dan spam; filter bahasa Indonesia dan panjang minimum; **simpan tanggal komentar** (data lama tidak punya). Simpan hanya teks, tanggal, ID video, dan penanda anonim; data mentah beridentitas tidak di-commit.
- Catat protokol (kanal, rentang tanggal, versi API, tanggal pengambilan) di `docs/dataset_provenance.md` dan Bab 3.
- Data X lama dipertahankan sebagai **dataset replikasi kedua**, bukan data utama.

**X/Twitter (alasan tidak jadi sumber utama):** tidak ada tier gratis untuk pendaftar baru (2026); pay-per-use sekitar $0,005 per baca; recent search hanya 7 hari terakhir; full-archive hanya Pro/Enterprise (Pro tertutup untuk pendaftar baru, Enterprise mulai sekitar $42.000 per bulan). Backfill ke periode lampau tidak feasible.

**Belum diputuskan pengguna:** jendela waktu komentar (saran 6-12 bulan, batas atas 2026-08-31 sesuai keinginan awal), target volume (saran 5.000-20.000 komentar), daftar kanal (saran: kanal berita besar dan kanal resmi terkait; ID kanal di-resolve oleh skrip, jangan ditebak), dan apakah ada platform tambahan. Pengguna perlu membuat API key sendiri (Google Cloud Console, aktifkan YouTube Data API v3, batasi key hanya untuk API itu).

## 8. Dokumen skripsi

**File:** `skripsi/bab_1_pendahuluan`, `bab_2_tinjauan_pustaka`, `bab_3_metodologi_penelitian` (masing-masing `.md` sebagai sumber dan `.docx` hasil konversi) dan `skripsi/daftar_pustaka_rujukan.md` (metadata dan tautan, tanpa PDF).
**Konversi:** `python scripts/convert_skripsi_bab_to_docx.py --input skripsi/<file>.md` (butuh `python-docx`).

**Format dari Panduan TA SI Unmuh Jember 2026 (file PDF 87 halaman, tidak ada di repo)**
- A4, margin kiri 4 cm, kanan/atas/bawah 3 cm; Times New Roman 12; spasi 1,5; rata kanan-kiri; tanpa indentasi baris pertama; nomor halaman kanan bawah (angka Arab untuk bab).
- Judul bab dua baris, tengah, kapital, tebal: "BAB 1" lalu "PENDAHULUAN" (angka Arab, bukan romawi). Subbab: title case, rata kiri, tebal. Sub-subbab bergaya sama dengan subbab.
- Bab 1 hanya lima subbab: Latar Belakang, Rumusan Masalah, Tujuan Penelitian, Manfaat Penelitian, Batasan Masalah. Bab 2 dan 3 bebas (Bab 3 harus memuat bahan, peralatan, cara kerja, jadwal; jadwal berformat tabel bulan x minggu).
- Bahasa baku, tanpa kata ganti orang, istilah asing dicetak miring. Sitasi: "Nama (Tahun)" atau "(Nama, Tahun)"; dua penulis dengan "dan", tiga atau lebih "dkk.".
- Daftar pustaka: **panduan kontradiktif** (Tabel 5.5 menyebut APA, bagian 5.1 menjelaskan gaya Harvard dengan contoh). Belum dikonfirmasi ke dosen.
- Proposal terdiri dari Bab 1-3 dan Daftar Pustaka; laporan akhir menambah Bab 4-5.

**Hal yang masih perlu diselesaikan di dokumen**
- Nama penulis paper UNNES (*Scientific Journal of Informatics* 13(3), 569-580, 2026) masih placeholder "Penulis UNNES" di tabel 2.2 Bab 2; baca full text paper itu karena sangat dekat dengan topik (MBG + SMOTE, Instagram, LSTM).
- Status indeksasi Scopus/Sinta setiap jurnal belum diverifikasi di sumber resmi.
- Jadwal penelitian di Bab 3 bersifat sementara.
- Teks Bab 1-3 menyebut ChatGPT secara eksplisit sebagai pelabel batch pertama (fakta metodologi); docs repo memakai istilah generik "LLM".
- Bab 1-3 masih berpusat pada kerangka evaluasi kualitas label; **perlu disesuaikan** bila judul yang disetujui dosen ternyata judul awal, dan perlu diperbarui untuk data baru (sumber data, protokol crawl, platform).

## 9. Peta repo

```
README.md, docs/                 dokumentasi (methodology, dataset_provenance, results_summary, codebook, guideline, HANDOFF)
skripsi/                         draf Bab 1-3, daftar pustaka kerja
scripts/                         pipeline; relevan: label_batch_rule_based.py, create_semantic_review.py,
                                 create_gold_annotation_sample.py, convert_skripsi_bab_to_docx.py,
                                 run_modeling_baselines.py, run_svm_tuning_experiments.py
src/mbg_sentiment/               modul (preprocessing, modeling, dll.)
notebooks/                       00, 01, 05, 06 (+ versi .executed)
data/raw, interim, processed/    data (processed/validation: sampel gold)
outputs/reports, figures, models laporan, gambar, model terlatih
paper/                           draf paper (klaim lama belum dikoreksi)
```

## 10. Status pekerjaan

**Sudah**
- Pipeline lengkap: audit, praproses, pelabelan batch, tinjauan, dataset 1.000, 4 baseline, 3 SVM tuned, hardening, draf paper.
- Pembersihan jejak nama tool AI dan satu kebocoran path lokal (PR #1).
- Ideation kebaruan, peta sitasi, bibliography, Bab 1-3 (format institusi), koreksi klaim pelabelan, sampel gold buta, pedoman anotasi PDF.
- Keputusan: tidak crawl X; data utama baru dari sumber lain.

**Belum**
1. Anotasi manusia atas 307 baris (sedang berjalan di sisi pengguna) dan pengumpulan hasilnya.
2. Protokol pengujian yang dibekukan dan skrip analisis (Kappa, estimasi berbobot, presisi/recall per kelas, bootstrap CI), dengan uji data tiruan.
3. Eksperimen skenario A vs B dan evaluasi terhadap gold; jalankan ulang baseline dan tuning dengan protokol baku.
4. Notebook Colab crawler YouTube dan dokumen protokol pengambilan data; pengambilan data aktual; pelabelan dan gold untuk data baru.
5. Satu halaman pernyataan kebaruan (kerangka) dan telaah literatur pembanding (bagian 5).
6. Bab 4-5, daftar pustaka final, bagian awal skripsi (sampul, pengesahan, dll.).
7. Koreksi klaim lama di `paper/` dan `outputs/reports/`; folder `tests/` disebut di README tetapi tidak ada; SMOTE belum dijalankan.
8. **Delapan laporan di `outputs/reports/` masih memuat path Windows lokal dengan nama pengguna** (`00_data_audit_verification`, `14_modeling_baseline_report`, `15_svm_tuning_report`, `17_final_visual_results_report`, `20_methodology_hardening_report`, `21_followup_validation_report`, `21_validation_package_report`, `22_revised_paper_report`); perlu dibersihkan.

**Urutan yang disarankan:** (2) protokol dan skrip analisis, sambil (4) notebook crawler; lalu hasil anotasi masuk, (3) eksperimen; baru Bab 4-5.

## 11. Keputusan dan konfirmasi yang masih terbuka

1. Judul persis yang disetujui dosen (judul awal README "Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis (MBG) pada Media Sosial Menggunakan Support Vector Machine", atau versi kerangka pelabelan), dan apakah kebaruan di kerangka pelabelan diterima secara eksplisit.
2. Sumber label batch 002-020 (skrip yang dijalankan agen AI atau ChatGPT langsung) dan angka pasti peninjauan langsung oleh pengguna.
3. Jumlah dan identitas anotator; apakah ada anotator yang belum terlibat dan tidak tahu hipotesis.
4. Jendela waktu, target volume, daftar kanal, platform tambahan untuk data baru.
5. Format daftar pustaka (APA vs Harvard).
6. PR #1 (open, mergeable) masih berjudul "Remove AI tool brand names from repo" padahal berisi banyak commit lain; perlu judul dan deskripsi baru atau dipecah, lalu keputusan kapan di-merge ke `main`.
7. Apakah data X lama tetap dipakai sebagai dataset replikasi kedua.

## 12. Konvensi kerja dan jebakan

- **Gaya penulisan:** Indonesia, ringkas. Hindari ciri tulisan AI di teks skripsi dan docs (tanda pisah panjang atau dua tanda hubung sebagai jeda, pola "tidak hanya X, tetapi juga Y"). Jangan memakai nama tool AI untuk nama file, folder, atau skrip. Klaim harus sebanding dengan bukti; koreksi kesalahan sendiri secara eksplisit.
- **Git:** kerja di branch `claude/adoring-heisenberg-t05kny` (atau branch yang ditunjuk sesi), push dengan `git push -u origin <branch>`. Jangan push ke `main`. Jangan membuat PR baru kecuali diminta. Stage file spesifik, bukan `git add -A`. Trailer commit mengikuti pengingat atribusi sesi (baris `Co-Authored-By` dan `Claude-Session`). Hook repo menuntut tidak ada perubahan yang tertinggal.
- **Hak cipta:** repo publik berlisensi MIT, tetapi itu tidak mencakup paper pihak ketiga. Simpan metadata dan tautan, bukan PDF.
- **Privasi:** jangan commit data mentah beridentitas, username, atau path lokal. Kunci sampel gold dan file `*.private.csv` tetap di luar git.
- **Rahasia:** API key hanya di Colab Secrets atau variabel lingkungan lokal.
- **Cek konversi docx:** selalu verifikasi jumlah tabel dan heading setelah konversi (bug lama).
- **Cek fakta eksternal** (harga API, kuota, indeksasi jurnal) lewat pencarian web dan tuliskan batas keyakinannya; harga dan kuota sering berubah.

## 13. Lingkungan dan perintah cepat

- Sandbox cloud: Python 3.11; `pandas` dan `scikit-learn` tidak terpasang secara default (`pip install -r requirements.txt` bila perlu menjalankan pemodelan); perlu `pip install python-docx openpyxl reportlab` untuk konversi docx, sampel gold, dan PDF; `apt-get install poppler-utils` untuk `pdftotext`/`pdftoppm`. Pencarian web tersedia; browser dan komputer pengguna tidak.
- Konversi Bab ke docx: `python scripts/convert_skripsi_bab_to_docx.py --input skripsi/bab_1_pendahuluan.md`
- Sampel gold: `python scripts/create_gold_annotation_sample.py` (lihat peringatan regenerasi di bagian 6).
- Status PR: `gh api repos/aldolionel/mbg-sentiment-analysis/pulls/1`.
- Sesi cloud asal: https://claude.ai/code/session_012GsMtoJaFpqnvD8d8kDjDX
