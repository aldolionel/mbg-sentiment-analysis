# Panduan Anotasi Sentimen MBG

## 1. Objective

Tujuan anotasi ini adalah memberi label sentimen publik terhadap Program Makan Bergizi Gratis (MBG) berdasarkan teks media sosial. Dataset prototype saat ini berasal dari X/Twitter crawl, tetapi panduan ini dibuat generik untuk teks pendek informal dari media sosial.

## 2. Allowed Labels

Label yang diperbolehkan hanya:

- `positif`
- `negatif`
- `netral`

Label harus ditulis lowercase persis seperti daftar di atas.

## 3. Definisi Label

### Positif

Gunakan label `positif` jika teks menunjukkan dukungan, persetujuan, optimisme, apresiasi, atau persepsi manfaat terhadap Program MBG.

### Negatif

Gunakan label `negatif` jika teks menunjukkan kritik, penolakan, ketidakpercayaan, kekhawatiran, atau sarkasme terhadap pelaksanaan program, anggaran, kualitas makanan, dugaan korupsi, atau penyalahgunaan politik terkait MBG.

### Netral

Gunakan label `netral` jika teks berupa pernyataan faktual, judul berita, pertanyaan tanpa polaritas jelas, ambigu, atau tidak relevan tetapi tetap menyebut MBG.

## 4. Decision Rules

1. Labeli sentimen terhadap Program MBG, bukan terhadap tokoh politik, kecuali tokoh tersebut dibahas langsung dalam konteks MBG.
2. Jika teks memiliki unsur positif dan negatif, pilih sentimen yang paling dominan.
3. Jika teks tidak jelas, hanya informatif, atau hanya bertanya, pilih `netral`.
4. Sarkasme diberi label sesuai makna tersiratnya.
5. Jangan menyimpulkan sentimen di luar isi teks.
6. Jangan memakai identitas pengguna, sumber akun, atau metadata sebagai dasar label.
7. Jika ragu setelah membaca teks, pilih `netral`.

## 5. Edge Cases

### Political Attack

Jika teks menyerang tokoh politik tetapi tidak membahas MBG secara jelas, gunakan `netral`. Jika serangan politik langsung mengaitkan MBG sebagai alat politik, pemborosan, atau pencitraan, gunakan `negatif`.

### Budget Concern

Kekhawatiran terhadap anggaran, pemborosan, utang, atau prioritas belanja negara untuk MBG biasanya `negatif`.

### Food Safety Concern

Kekhawatiran tentang makanan basi, keracunan, gizi buruk, kebersihan dapur, atau keamanan pangan dalam MBG biasanya `negatif`.

### Distribution Concern

Keluhan tentang distribusi tidak merata, keterlambatan, salah sasaran, atau sekolah belum menerima MBG biasanya `negatif`, kecuali hanya bertanya tanpa nada keluhan maka `netral`.

### Jokes/Memes

Jika candaan tetap menunjukkan dukungan atau kritik, beri label sesuai makna dominan. Jika hanya bercanda tanpa sikap jelas terhadap MBG, gunakan `netral`.

### News Reposts

Judul berita atau repost informasi tanpa opini tambahan biasanya `netral`.

### Questions

Pertanyaan murni seperti "MBG mulai kapan?" biasanya `netral`. Pertanyaan retoris yang menyiratkan kritik dapat diberi `negatif`.

### One-word/Short Posts

Teks sangat pendek seperti "mantap" dapat `positif` jika jelas merujuk MBG. Teks seperti "parah" dapat `negatif` jika jelas merujuk MBG. Jika konteks tidak cukup, gunakan `netral`.

## 6. Contoh Positif

1. "Program MBG bagus untuk bantu anak sekolah dapat makanan bergizi."
2. "Semoga MBG berjalan lancar dan merata sampai daerah pelosok."
3. "Setuju dengan makan bergizi gratis, banyak keluarga bisa terbantu."
4. "Kalau dijalankan serius, MBG bisa meningkatkan kesehatan siswa."
5. "Good job, program makanan bergizi ini penting buat anak-anak."
6. "MBG bermanfaat untuk siswa yang sering berangkat sekolah tanpa sarapan."
7. "Saya dukung MBG asal pengawasannya ketat dan menunya sehat."
8. "Program ini langkah baik untuk memperhatikan gizi anak Indonesia."
9. "Semoga MBG terus diperbaiki supaya manfaatnya makin terasa."
10. "Makan bergizi gratis bisa membantu semangat belajar siswa."

## 7. Contoh Negatif

1. "MBG cuma buang-buang anggaran kalau pelaksanaannya asal-asalan."
2. "Takut program MBG jadi lahan korupsi baru."
3. "Makan gratis tapi gizinya tidak jelas, buat apa?"
4. "Anggaran MBG terlalu besar, masih banyak kebutuhan lain yang lebih penting."
5. "Kalau distribusinya kacau, MBG hanya jadi pencitraan."
6. "Program MBG rawan dimanfaatkan untuk kepentingan politik."
7. "Saya tidak percaya MBG bisa berjalan bersih tanpa pengawasan."
8. "Jangan sampai anak-anak dikasih makanan murahan demi mengejar target."
9. "MBG terdengar bagus, tapi praktiknya bisa jadi masalah besar."
10. "Kalau banyak sekolah belum kebagian, berarti program ini belum siap."

## 8. Contoh Netral

1. "Program MBG mulai diterapkan tahun ini."
2. "MBG adalah singkatan dari Makan Bergizi Gratis."
3. "Menu MBG hari ini apa saja?"
4. "Berapa anggaran yang disiapkan untuk Program MBG?"
5. "Di daerah saya belum ada informasi soal MBG."
6. "Pemerintah membahas teknis pelaksanaan MBG."
7. "Sekolah mana saja yang menjadi lokasi uji coba MBG?"
8. "Berita terbaru tentang MBG sedang ramai di media sosial."
9. "MBG akan melibatkan dapur dan penyedia makanan."
10. "Ada yang tahu jadwal pembagian MBG?"

## 9. Output Format Rules

Saat mengisi dataset atau hasil batch, label harus lowercase persis:

- `positif`
- `negatif`
- `netral`

Jangan memakai label lain seperti `positive`, `negative`, `neutral`, `pro`, `kontra`, `campuran`, atau `tidak tahu`.
