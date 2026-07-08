# AI-Assisted Sentiment Labeling Prompt - annotation_batch_014

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
| label_sample_0651 | udah deh makan bergizi gratis itu mending ditiadakan saja anggarannya bisa dialihkan untuk jaminan kesehatan masyarakat |
| label_sample_0652 | adik aku berekspektasi mbg yang diberikan bakal kaya di kantin kantin korea yang banyak org korea nge buat videonya lunch part sekian gituu adik kamu sangat naif |
| label_sample_0653 | ada buzzer pemerintah yang digaji pakai uang pajak rakyat menjelaskan soal makan bergizi gratis tak komentar sedikit ya |
| label_sample_0654 | mungkin ini implementasi dari sumber protein alternatif ibu ibu di surabaya protes temukan ulat dan lalat di menu makan bergizi gratis anaknya via |
| label_sample_0655 | mbg itu diambil dari ppn yg naik jadi dari pph org tua mereka yg dipotong dari gajinya tiap bulan makin besar pendapatannya pph nya juga makin besar so stop nyamain mbg sm charity |
| label_sample_0656 | blunder ppn mbg pada gamau mikir dampak lainnya giliran dikasih lihat fakta di lapangan malah cuci tangan mana pendukungnya pada tolol lagi masih aja ngebelain |
| label_sample_0657 | baru banget kmrn diceritain temen kalau dana mbg dikorupsi sama suppliernya alias udah dana nya ga banyak dikorupsi pulaa |
| label_sample_0658 | kan ga semua butuh mbg bisa kan diberikan kepada yang butuh aja di data juga bisa mana anak orang mampu mana yang kagak jadi ga buang buang anggaran sama makanan |
| label_sample_0659 | wooee zakat itu dibagikan kepada fakir miskin atau orang fisabilillah bukan untuk mbg yang mana sebagian besar masih mampu makan di rumah ojo ngawur bambaang |
| label_sample_0660 | ini pemerintah sama legislatif kok kayak amatiran ya apa gak dipikir imbasnya apa banyak yg gak bisa menafkahi keluarga dan jadi pengangguran apa karena mbg jadi menghemat sampai segitunya |
| label_sample_0661 | melalui program makan bergizi gratis pemerintah berupaya untuk memenuhi gizi pada anak anak seluruh indonesia mbg makanbergizigratis dukungmbg |
| label_sample_0662 | dan pemerintah masih insist kalo mbg membuka lapangan pekerjaan dan menurunkan kemiskinan ï x f program gak rasional ya allah kenapa masih bersikeras |
| label_sample_0663 | heheheh mari kita tunggu realisasinya gimana ges fyp fyp prabowo prabowosubianto makansianggratis proker explore explorepage |
| label_sample_0664 | ps kanit samapta polsek muara batang gadis melaksanakan giat sambang sekaligus menyampaikan pesan pesan kamtibmas kepada masyarakat desa singkuang i |
| label_sample_0665 | harusnya sesuai tujuannya makan bergizi gratis untuk mengatasi stunting klo trrnyata makananya ga bergizi gmn mencapai tujuan awal mengatasi stunting |
| label_sample_0666 | nah betul del orang yg duduk di kursi empuk harus sama menu y dngn menu mbg ulat belalang dasar yg ngasih ide y stres tidak smua anak suka mkn ulat sama belalang |
| label_sample_0667 | wujudkan sekolah impian dengan fasilitas terbaik mari optimalkan anggaran lewat program mbg demi pendidikan mumpuni kolaborasitingkatkanpendidikan |
| label_sample_0668 | juta rumah ga ada juta lapangan pekerjaan malah makin banyak phk mbg menunya mau diganti pake batagor jadi ini rezim kerjanya ngapain sih |
| label_sample_0669 | alhamdulillah bisa makan bergizi gratis tanpa mikirin harga sayur naik lagi semoga yang butuh beneran dapat ya jangan malah disikat oknum |
| label_sample_0670 | di mbg extension lantai sudah ada store baru nih yukk mampir cek siapa tau ada kebutuhan perlengkapan olahraga fashion yg kamu butuhkan malbaligaleria familymall mbgextension |
| label_sample_0671 | ia membantah bahwa dalam pertemuan itu ada pembicaraan soal tawaran menteri termasuk soal program makan bergizi gratis mbg |
| label_sample_0672 | enggak kagetlah dia berjasa sudah memarahi anak sd yg protes mbg udah capek gedein badan gak pake baju biar anak sd pd takut |
| label_sample_0673 | segala macam kasus menutupi kasus sebelumnya occrp mbg pagar laut penembakan efisiensi danantara pertamina timah dan lain lain |
| label_sample_0674 | panyabungan startnews bupati mandailing natal madina hm jafar sukhairi nasution menyambut baik program makanan bergizi gratis mbg yang digalakkan pemerintah untuk pelajar |
| label_sample_0675 | langkah inovatif prabowo dengan mbg sinergikan gizi optimal dan pendidikan plus untuk masa depan hebat kolaborasitingkatkanpendidikan |
| label_sample_0676 | program mbg ini bukti nyata niat baik pemerintah buat peduli kesehatan masyarakat semoga makin banyak yang terbantu harikerjanyata |
| label_sample_0677 | makanan mbg prabowo gibran yg keliatan makanannya proper kayakny cmn buzzer imposter yg ngaku ngaku dari subang kemaren oke gas |
| label_sample_0678 | juru bicara jubir kantor komunikasi kepresidenan pco dedek prayudi menegaskan bahwa program makan bergizi gratis mbg tidak memangkas anggaran lainnya |
| label_sample_0679 | mempersilakan apa minta nih banyak kegiatan apbd yg dipending nunggu juknis kemenkeu denger denger utk sharing biaya mbg emang hasyu kalian ini siapa berbuat siapa yg ikut tanggungjawab |
| label_sample_0680 | iya iya suka mu aja iyain aja deh di atas ngarang kalaupun iya ga mengubah fakta lapangan jika mbg ini berdampak negatif terhadap umkm satu karangan cerita tidak bisa mengubah fakta lapangan kan |
| label_sample_0681 | horas dusanakmido kantor imigrasi kelas ii tpi sibolga bekerja sama dengan bank bri cabang sibolga menghadirkan kegiatan makan bergizi gratis di sd muhammadiyah plus sibuluan indah kamis januari |
| label_sample_0682 | budi mengutarakan rencananya untuk mewujudkan kop hub untuk menyuplai kebutuhan mbg budiariesetiadi menkop budiarie menteri mbg |
| label_sample_0683 | contohnya waktu kesehatan dan pendidikan ga dijadiin prioritas tapi yang malah dipush itu mbg katanya buat ningkatin gizi anak dan bantu umkm tapi eksekusinya berantakan total |
| label_sample_0684 | mbg di papua harusnya bukan prioritas di papua lbh butuh pendidikan dan kesehatan kampung yg dekat dng ibukota kabupaten kota msh bnyk yg blm bisa akses kedua hal tsb |
| label_sample_0685 | tapera bpjs kelangkaan gas melon mbg berujung efisiensi pagar laut danatara ada yg mau nambahin ini baru jalan berapa bulan udah blunder banget pemerintah |
| label_sample_0686 | semangat bakti wujudkan kebaikan polri mendukung penuh program makan bergizi gratis memastikan supaya masyarakat mendapatkan asupan gizi yang layak makanbergizigratis |
| label_sample_0687 | jumlah pelajar di indonesia juta orang x harga porsi makan bergizi gratis mbg rp rp miliar artinya negara butuh uang rp miliar x hari rp trilyun per bulan untuk program mbg sebulan |
| label_sample_0688 | pak mohon agar pemain bola nasional diikutkan ke program makan bergizi gratis mbg agar mereka tidak kurang gizi lagi seperti klaim dari kepala badan gizi nasional terima kasih |
| label_sample_0689 | mari kita dukung program makan bergizi gratis untuk menciptakan masa depan indonesia yang lebih sehat dan lebih sejahtera makanbergizibangunnegeri |
| label_sample_0690 | presiden prabowo subianto disebut menggunakan dana pribadi dalam program makan bergizi gratis mbg karena penerapannya masih dalam tahap uji coba dan belum dibiayai apbn simak selengkapnya |
| label_sample_0691 | center for strategic and international studies csis nilai program makan bergizi gratis memiliki banyak manfaat positif prabowo presidenprabowo makananbergizigratis mbg astacita |
| label_sample_0692 | ketua dewan ekonomi nasional luhut binsar pandjaitan bilang kalau program makan bergizi gratis mbg punya dampak luar biasa buat ekonomi indonesia |
| label_sample_0693 | otak mereka kopong nder baru ke isi pas jam makan bergizi gratis percuma debat sama orang budeg mah nggak mau kalah yg ada |
| label_sample_0694 | setiap sendok makanan bergizi adalah investasi bagi masa depan bangsa mari kita dukung program makan bergizi gratis untuk anak anak indonesia giziuntukanak makanbergizigratis |
| label_sample_0695 | mbg hari kedua nggak dimakan sama ghifari catering dari sekolah biasanya kemakan walau kadang nggak habis tapi ini nggak disentuh pusing bangett besok blg apa sama prof mei |
| label_sample_0696 | saya jujur masih bingung program makan bergizi gratis mbg setiap sekolah itu tiap hari atau bulan sekali atau tahun sekali pak dikasihnya |
| label_sample_0697 | mbg makan beracun gratis pelajar sdn kasipute di kab bombana sulawesi tenggara muntah usai menerima makan siang bergizi rabu min siapa yg bisa dituntut dg kasus spt ini |
| label_sample_0698 | kontras pemikiran exmertua dengan ps project mbg hasilnya tai kata exmertua bagaimana turunkan harga pangan jika utang ln hanya jadi tai mimpi disiang bolong |
| label_sample_0699 | kan yg masih banyak yg ga sekolah karena ga mampu miskin yg berarti gabisa ikut merasakan fasilitas mbg itu orang penyalurannya aja lewat sekolah hadeuhh |
| label_sample_0700 | bang jangan tersinggung lho ya tapi jawaban elu selalu positif tentang mbg ini elu salah satu warga yang all in all in joget joget ok gas ya |
