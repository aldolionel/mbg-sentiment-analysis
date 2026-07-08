# AI-Assisted Sentiment Labeling Prompt - annotation_batch_006

Anda membantu memberi label sentimen publik terhadap Program Makan Bergizi Gratis (MBG) pada teks media sosial.

Gunakan hanya label berikut: `positif`, `negatif`, `netral`.

Aturan penting:
- Labeli sentimen terhadap Program MBG, bukan terhadap tokoh politik kecuali langsung terkait MBG.
- Jika teks memuat sentimen positif dan negatif, pilih sentimen yang paling dominan.
- Jika teks berupa informasi, berita, pertanyaan tanpa polaritas jelas, ambigu, atau Anda tidak yakin, gunakan `netral`.
- Sarkasme diberi label sesuai makna tersirat.
- Jangan mengubah `sample_id`.
- Jangan menambah baris.
- Jangan menghapus baris.
- Jangan mengisi label selain `positif`, `negatif`, atau `netral`.

Kembalikan jawaban hanya sebagai CSV block dengan kolom:

```csv
sample_id,label,labeling_notes
```

Isi `labeling_notes` secara singkat jika perlu. Jika tidak perlu catatan, kosongkan.

## Rows

| sample_id | clean_text |
| --- | --- |
| label_sample_0251 | mbg adalah booster buat umkm pangan supaya bisa bersinar mbgdorongekonomi |
| label_sample_0252 | tebak nama grup wa yang isinya tsamara deddy dkk utk melawan kritik mbg |
| label_sample_0253 | makan bergizi gratis ini bikin anak anak lebih bahagia dan bertenaga |
| label_sample_0254 | ahli gizi mbg dan stafnya bisa tersenyum lebaran ini gaji cair sebelum waktunya |
| label_sample_0255 | salah gambarnya di mana sih ada mbg yg sayur dan lauknya sebanyak itu |
| label_sample_0256 | engga bu kan lagi efisiensi mungkin pake uangnya prabowo seperti mbg |
| label_sample_0257 | program makan bergizi gratis jadi nyata berkat dukungan umkm umkmdukungmbg |
| label_sample_0258 | prabowo respons wacana dana zakat digunakan untuk program mbg ini penjelasannya |
| label_sample_0259 | udah dibilang dari awal mbg ini cuma sebagai sarana buat korupsi |
| label_sample_0260 | tolak mbg minta pendidikan gratis begitu dikirim guru malah di bantai |
| label_sample_0261 | bukannya buat ningkatin kualitas mbg malah dipake bayar buzzer |
| label_sample_0262 | program mbg mendukung percepatan perkembangan ekonomi negara |
| label_sample_0263 | koramil umbulharjo sukseskan program makan bergizi gratis di wilayah binaan |
| label_sample_0264 | no wonder anakuoneanga kijana shika adabu na adabu ikushike mshikamane |
| label_sample_0265 | pemprov kalbar siap luncurkan program makan bergizi gratis untuk pelajar bnetwork |
| label_sample_0266 | kalo negara belom siap jalankan program mbg mending ditunda dulu atau dibatalkan |
| label_sample_0267 | semakin banyak dukungan semakin sukses program mbg buat papua |
| label_sample_0268 | bertemu pm ishiba shigeru presiden prabowo pastikan jepang bantu program mbg |
| label_sample_0269 | bakti untuk negeri babinsa serui bahagia terlibat langsung distribusi mbg |
| label_sample_0270 | diperlukan dapur sehat mbg untuk melayani ribu pelajar di gunungkidul |
| label_sample_0271 | program mbg bangkitkan ekonomi lokal lewat produk susu keren |
| label_sample_0272 | bersama dukung makan bergizi gratis cegah stunting biar anak sekolah tambah sehat |
| label_sample_0273 | biar gak nongol terus bisa gak aguz dikasih program makan bergizi gratis biar diem |
| label_sample_0274 | presiden udah siapin rencana buat program mbg tetap jalan walau ada banjir |
| label_sample_0275 | sukseskan makan bergizi gratis makanbergizigratis mbg papua |
| label_sample_0276 | w dah bosen bebeh bgt tiap matkul bahasannya mbg mulu apalagi susu ikan |
| label_sample_0277 | program mbg di magelang tetap berjalan saat ramadan begini menu dan distribusinya |
| label_sample_0278 | apakah program makan bergizi gratis prabowo buruk bagi perekonomian |
| label_sample_0279 | distribusi program mbg tetap dijalankan meski ada banjir dari presiden |
| label_sample_0280 | umkm give full support untuk program mbg demi masyarakat sehat umkmdukungmbg |
| label_sample_0281 | lebaran lebih seru kalo gaji udah aman di rekening terima kasih buat staf gizi mbg |
| label_sample_0282 | program makan bergizi gratis gerakan perekonomian lokal penuhigiziindonesia |
| label_sample_0283 | lebih dari sekedar gerakan mbg adalah gaya hidup sehat dengan produk lokal |
| label_sample_0284 | bangga jadi bagian dari perubahan positif ini program mbg emang juara |
| label_sample_0285 | hilang cerita makan bergizi gratis anak sekolah sudah puasa siap tu libur panjang |
| label_sample_0286 | nasi kotak buat artis pasti budgetnya k up gak sih lah mbg berapa |
| label_sample_0287 | program mbg salah satu solusi terbaik untuk anak papua kita dukung yuk |
| label_sample_0288 | mbg jalan harga pangan naik gk pak kmi gk trimakasih nambah beban rakyat aj |
| label_sample_0289 | ikutan mbg biar tubuh lebih fit dan petani lokal makin dipanggil pahlawan |
| label_sample_0290 | langkah besar dari mbg buat pendidikan papua jadi makin terjangkau dan fleksibel |
| label_sample_0291 | walau sebenarnya makan bergizi gratis itu ga benar benar gratis |
| label_sample_0292 | keren upaya pemerintah dan militer buat dukung pendidikan lewat program mbg |
| label_sample_0293 | pemerintah pastikan mbg buat juta jiwa langkah optimis dan keren abis |
| label_sample_0294 | presiden totalitas pastikan lintas aliran mbg tetap sampai di setiap daerah banjir |
| label_sample_0295 | sekolah di papua akan diberdayakan menjadi dapur makan bergizi gratis |
| label_sample_0296 | di balik generasi sehat ada juta penerima mbg di sumbar salute for a better future |
| label_sample_0297 | video pro kontra susu ikan vs susu sapi di program mbg prabowo |
| label_sample_0298 | meski banjir tak kunjung usai presiden pastikan program mbg berlanjut |
| label_sample_0299 | kompak bener semua mendukung mbg ekonomi rakyat jadi prioritas |
| label_sample_0300 | kepedulian sumbar layak dicontoh program mbg bawa dampak positif untuk banyak orang |
