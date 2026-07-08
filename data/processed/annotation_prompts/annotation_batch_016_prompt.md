# AI-Assisted Sentiment Labeling Prompt - annotation_batch_016

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
| label_sample_0751 | pemerintah resmi meningkatkan anggaran untuk program makan bergizi gratis mbg menjadi rp triliun pada tahun demi meningkatkan kualitas gizi anak anak indonesia |
| label_sample_0752 | bikin kebijakan cuma buat buang buang duit hal sepele aja mbg banyak masalah kontol emang makin kesini otak pemerintah |
| label_sample_0753 | pakk di jakarta aja belum semua sdn dapat program mbg apalagi di daerah pakk negara mana pakk yg mau belajar program mbg |
| label_sample_0754 | hahahaha ini salah satu narasi yg pernah aku dpt ketika berkomentar di ig diserbu warga ig intinya mbg lebih realistis dibanding lainnya boomm |
| label_sample_0755 | yaelah voters masih aja tone deaf mana tuh yang koar koar siapapun presiden nya kita bakalan gini gini aja kasih makan tuh otak lo pake makanan gratis yang katanya bergizi itu fuck you all |
| label_sample_0756 | dengan makanan bergizi kita wujudkan generasi cerdas dan sehat langkah kecil hari ini dampak besar di masa depan penuhigiziindonesia makansianggratis kalbarpeduli generasisehat kalbar |
| label_sample_0757 | program makan bergizi gratis mbg adalah langkah strategis pemerintah dalam mengurangi angka kemiskinan dengan memastikan anak anak mendapatkan gizi yang baik sejak dini makanbergizigratis mbg |
| label_sample_0758 | mudahnya hidup sehat dan bahagia dengan program makan bergizi gratis di papua makanbergiziuntukindonesia makanbergizigratisbantuumkm |
| label_sample_0759 | dukung program makan bergizi gratis untuk anak anak agar mereka bisa tumbuh sehat dan kuat setiap anak berhak mendapatkan gizi yang seimbang demi masa depan yang lebih baik mbg |
| label_sample_0760 | beneran penasaran seberapa jauh pemerintah bakalan obrak abrik anggaran lain yang lebih penting demi program mbg ini dan berapa lama jg nih program akan bertahan |
| label_sample_0761 | stress masalahnya apa solusinya apa muak banget rasanya sama pemerintah dikira mbg bisa nyegah banjir kali ya gara gara mbg noh semuanya jdi bermasalah pgn berkata kasar tp dah puasa |
| label_sample_0762 | blm lagi kali dirinci ada yg belanja pegawai lebih apbd kalo dukung mbg pasti yg dikurangi sektor lain bukan belpeg nya |
| label_sample_0763 | generasi penerus bangsa palestina numpang makan dan berak di indonesia untuk sementara pak ga sia sia program makan bergizi gratis |
| label_sample_0764 | program mbg gimana kalau buat tingkatkan fasilitas sekolah pendidikan yang top masa depan lebih cerah kolaborasitingkatkanpendidikan |
| label_sample_0765 | kepala badan gizi nasional bgn dadan hindayana memberikan tanggapan terkait viralnya laporan menu makanan bergizi gratis mbg yang belum matang di media sosial |
| label_sample_0766 | mbg menunjukkan komitmen nyata pemerintah dalam memberikan akses gizi yang baik bagi masyarakat yang membutuhkan di papua makanbergiziuntukindonesia makanbergizigratisbantuumkm |
| label_sample_0767 | apa itu makan bergizi gratis yuuk sahabat sehat simak info lengkapnya pada slide diatas mbg makanbergizigratis dinkesklaten dinkeskabklaten |
| label_sample_0768 | program makan siang gratis dari pemerintah baru bapanas turun tangan langsung yuk dukung bersama makansianggratis prabowogibran makananbergizigratis indonesia makananbergizi |
| label_sample_0769 | pak menteri jalan lintas di kab musi rawas rusak parah apakah balai hanya diam tidak berbuat apa krn anggaran nya sdh dipake danantara dan mbg indonesiagelap |
| label_sample_0770 | prabowo gibran siap wujudkan program makan siang gratis bagi juta anak sekolah dan santri indonesiaemas programpresiden presidenprabowo makansianggratis kesehatangratisuntuksemua |
| label_sample_0771 | kamis agitsni m u luhkan kab skbmi koordinasi dengan sdn selajambe dan mi selajambe untuk mbg makan bergizi gratis dari kkp giatluhkansatmingkalbogor sukabumi aktivitas makanbergizi gemarikan |
| label_sample_0772 | program makan bergizi gratis tingkatkan kemampuan akademis generasi muda menuju indonesia emas programmbg makanbergizigratis dukungmbg indonesiaemas |
| label_sample_0773 | padahal kalo ortu anak ga di phk juga gizinya bisa lebih baik dari yg mereka kasih dasarnya mendesak karena di desak untuk menggaji yg ngurusin mbg tapi udh terlanjur di korup |
| label_sample_0774 | pendidikan keren itu dimulai dari sekolah yang nyaman ayo manfaatkan anggaran mbg buat benahin fasilitas sekolah kita kolaborasitingkatkanpendidikan |
| label_sample_0775 | pemerintah akan mendorong penggunaan anggaran pendapatan dan belanja daerah apbd untuk mendukung pelaksanaan program makan bergizi gratis mbg |
| label_sample_0776 | media asing aja udah kata andalan sdm rendah yg udh berasa paling keras dan kritis untung ada mbg skrg otaknya bisa berkembang untuk menerima pendidikan scr maksimal |
| label_sample_0777 | di adakan progam mbg ini sudah bagus apalagi progam ini langsung di awasi di setiap sekolah tambah bagus lagi tak merugikan siswa yg dapet mbg tadi |
| label_sample_0778 | efisiensi anggaran bukan berarti mengorbankan pendidikan program mbg dan pendidikan tetap berjalan untuk membangun generasi unggul pendidikanuntukbangsa efisiensiberkualitas |
| label_sample_0779 | udah lama banget bahkan gak inget kapan terakhir kesana pokoknya waktu gramedia yang masih di bagian dalam jadi sekalian keliling mengitari mbg sambil nunggu kak merry dateng |
| label_sample_0780 | nih awas ketuker dah mgb sama mbg by the way bantu aku buat bisa hype jossgawin if u see this let s be moots guys mygoldenblood jossgawin |
| label_sample_0781 | kabar baik buat anak anak indonesia anggaran makan bergizi gratis jadi triliun rupiah mari kita ciptakan generasi sehat dan kuat mbgdorongekonomi |
| label_sample_0782 | mbg memajukan umkm menumbuhkan ekonomi menciptakan generasi yang sehat fyp swasembadaenergi astacita mbgdorongekonomi peringatansuperdarurat pak bowo ciawi |
| label_sample_0783 | sumber video sekretariat presiden presidenprabowo prabowo prabowosubianto makansianggratis makansiang makansiangbergizi sidangkabinet makanbergizi |
| label_sample_0784 | lah kemaren ada yg makan ulet sagu dikasianin makanya pd seneng ada mbg biar ga makan itu skrg malah mau dikasih ulet sagu |
| label_sample_0785 | dear pemerintah konoha drpd jalanin mbg yg ga efisien dan ngorbanin banyak hal mendingan hapus dulu dah persyaratan daftar kerja yg ngeberatin khususnya batasan usia |
| label_sample_0786 | istana anggaran kemenham sebenarnya t hanya saja untuk efisiensi anggaran efektif hanya miliar saja prioritas utama kami mbg program ham hanya prioritas cadangan |
| label_sample_0787 | kaga penting urusin noh keluarga yang kena phk urusin hutan yang mau di gunduli urusin masalah stunting di pelosok program mbg mu ga guna pak |
| label_sample_0788 | program pendidikan dan makan bergizi gratis adalah bukti nyata komitmen pemerintah untuk kesejahteraan anak anak indonesia kolaborasitingkatkanpendidikan |
| label_sample_0789 | tadi pas jalan di mbg i see something ada bapak bapak jualan minuman i guess soalnya dia ada nyebutin yakult ngerasa terharu sama bersalah aja sih krn ga mampir buat sekedar liat menu beliau |
| label_sample_0790 | bersyukurlah karena sekarang ada makan bergizi gratis pemerintah sudah lama bikin aturan sekolah negeri gratis jadi kalo sekolah negeri bayar maka itu artinya gurunya jahat |
| label_sample_0791 | pov nya kemiskinan merajalela sekarang pengangguran korupsi pesta anggaran pejabat dan kalian dengan mbg berlagak seperti pahlawan |
| label_sample_0792 | mbg tuh gimmick pengalih isu alesan efisiensi faktor utama pemerintah bikin kebijakan efisiensi tuh bukan mbg tpi untuk danantara mbg yg bukan faktor utama dijadiin kambing hitam |
| label_sample_0793 | di tempat saya gak ada makan bergizi gratis tetap hidup anakâ sekolah gak ada dampaknya ya palingâ kebutuhan pokpk semakin mahal krn naiknya ppn dan pajak utk membiayai mbg ini |
| label_sample_0794 | dengan mbg fasilitas sekolah jadi prioritas untuk direnovasi demi kenyamanan belajar banyak orang kolaborasitingkatkanpendidikan |
| label_sample_0795 | makanan sehat tubuh kuat pikiran cerdas ï x f program mbg membantu membangun kebiasaan makan sehat sejak dini apakah kamu sudah menerapkan pola makan sehat hari ini sehatbersamambg |
| label_sample_0796 | ekspose mbg malah sdh dinikmati siswa yg terlihat byk dr kelompok yg cukup gizi tdk atunting bahkan konon sebagian org tuanya sebenarnya lbh suka diberikannkpd yg membutuhkan |
| label_sample_0797 | bhabinkamtibmas polsek muara batang gadis melaksanakan giat patroli pilar di desa tabuyung sekaligus menyampaikan pesan pesan kamtibmas kepada masyarakat desa tabuyung |
| label_sample_0798 | prabowo memastikan pembaruan di bidang pendidikan dan kesehatan dapat melalui inisiatif mbg kolaborasitingkatkanpendidikan |
| label_sample_0799 | wokwowok nyokap gue nyumpah nyumpahin prabski karna mbg kata nyokap itu dia ntar dikudeta tuh tinggal nunggu waktu aja |
| label_sample_0800 | ayo optimalkan anggaran mbg untuk sekolah yang sehat dan mendukung kreativitas anak anak kolaborasitingkatkanpendidikan |
