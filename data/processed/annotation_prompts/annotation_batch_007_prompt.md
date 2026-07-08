# AI-Assisted Sentiment Labeling Prompt - annotation_batch_007

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
| label_sample_0301 | dana mbg hadir pendidikan tetap adem sinergimencerdaskanbangsa |
| label_sample_0302 | kebijakan mbg di papua diapresiasi warga harap dampaknya bisa jauh ke depan |
| label_sample_0303 | makan bergizi gratis mantap jiwa semua bisa dapat makanan sehat makanbergiziponpes |
| label_sample_0304 | siswa sd di sukoharjo keracunan mbg dpr jangan digeneralisir jadi sebuah kegagalan |
| label_sample_0305 | mbok uwess ah mbg teroos negara genting kayak gini masih aja mbg |
| label_sample_0306 | sudah kudugem makan bergizi gratis bakalan ada kasus keracunan tipikal konoha |
| label_sample_0307 | sok peduli anak global dulu aja bikin program mbg bt anak indonesia diejekk |
| label_sample_0308 | ragil gojo lihat dengar pahami sabrina siang makan bergizi gratis |
| label_sample_0309 | generasi sehat dimulai dari dukungan kita semua untuk papua barat daya dengan mbg |
| label_sample_0310 | perancis suruh lihat menu mbg yg minimalis kalau nggak nangis |
| label_sample_0311 | kalo anggaran mbg dipotong bisa bisa jatah makannya cuman ribu rupiah dong |
| label_sample_0312 | keberhasilan mbg bergantung pada integritas dan akuntabilitas |
| label_sample_0313 | anggota dpr dorong pemerintah kuatkan pengawasan makanan dalam mbg |
| label_sample_0314 | makan bergizi gratis itu jadi taktik perang dagang dgn amrik tak tik apaan tuh |
| label_sample_0315 | langkah prabowo dengan makan bergizi gratis adalah solusi hebat |
| label_sample_0316 | pokoknya tim mbg dan umkm bikin hidup sehat itu jadi lebih realistis umkmdukungmbg |
| label_sample_0317 | muncul usulan makan bergizi gratis minta dibiayai zakat pan berikan respon |
| label_sample_0318 | kali aja jadi staf khusus buat nakut in anak yg gak mau makan mbg |
| label_sample_0319 | program makan bergizi gratis menurunkan angka stunting di papua papuasejahtera |
| label_sample_0320 | wakil presiden terpilih uji coba program mbg di kota tangerang |
| label_sample_0321 | generasi sehat bukan sekedar wacana dengan adanya program makan bergizi gratis ini |
| label_sample_0322 | mbg memicu perkembangan pesat anak papua ke arah lebih baik |
| label_sample_0323 | bukan soal modal tapi strategi mbg kasih insight nya mbgdorongekonomi |
| label_sample_0324 | puasaa yuk dengan makan bergizi gratis ayo dukung agar tetap jalan |
| label_sample_0325 | program makan bergizi gratis untuk anak anak indonesia penuhigiziindonesia |
| label_sample_0326 | ã ã pada baik bgtt full dpt makan enakk dan bneran gratiss rill mbg |
| label_sample_0327 | presiden yakinkan program mbg tersalur meski banjir melanda |
| label_sample_0328 | jubir kepresidenan menu susu di mbg diprioritaskan bagi daerah penghasil |
| label_sample_0329 | keracunan usai konsumsi mbg belasan murid sd di takalar dilarikan ke puskesmas |
| label_sample_0330 | kodim oku panen sayur dukung program makan bergizi gratis untuk masyarakat |
| label_sample_0331 | ya kali udh dukung mbg sampe berani keluar kata tabok ga diangkat |
| label_sample_0332 | iya kan pak kasih lah mereka ini makan bergizi gratis biar ga stunting otaknya |
| label_sample_0333 | daripada bayar buzzer bot mending cairin gaji pegawai mbg ya min |
| label_sample_0334 | mbg lebih parah daripada pandemi covid waktu covid aja tetep cair |
| label_sample_0335 | umkm ngeluarin peran penting untuk bantu makan bergizi gratis umkmdukungmbg |
| label_sample_0336 | intip menu makan bergizi gratis hingga proses pembagiannya ke siswa di makassar |
| label_sample_0337 | mirip siapa gitu yaa digencarkan program mbg ketimbang pendidikan gratis lagulama |
| label_sample_0338 | presiden ambil tindakan nyata agar mbg tetap ada di masa banjir |
| label_sample_0339 | almuniza banda aceh siap laksanakan program makan bergizi gratis |
| label_sample_0340 | ketua bgn ungkap faktor kunci sukses program makan bergizi gratis |
| label_sample_0341 | gerakan program mbg papua barat bawa angin segar untuk masa depan sehat |
| label_sample_0342 | potensi mo di betak untuk kemana lagi si untuk mbg yang ga seberapa itu |
| label_sample_0343 | program mbg jadi makin ciamik berkat kontribusi cerdas dari umkm umkmdukungmbg |
| label_sample_0344 | mbg makan bergizi gratis ï x f makan bersyukur gratis ï x f |
| label_sample_0345 | presiden punya tindak lanjut pastikan mbg di wilayah banjir |
| label_sample_0346 | berarti makan siang gratis harusnya gak rb ya per porsi biar dpt yg bergizi |
| label_sample_0347 | atau mbg yang t hr pdhl mbg seminggu bisa buat beli vaksin setahun |
| label_sample_0348 | mbg bantu umkm capai potensi maksimalnya tanpa batas mbgdorongekonomi |
| label_sample_0349 | salut buat semua yang udah saling support untuk kesuksesan mbg papua |
| label_sample_0350 | politik gak ngaruh ke kehidupan kita makan noh mbg minyak oplosan dll |
