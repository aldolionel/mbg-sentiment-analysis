# AI-Assisted Sentiment Labeling Prompt - annotation_batch_018

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
| label_sample_0851 | kpk temukan dugaan pengurangan anggaran dalam program makan bergizi gratis yang berpotensi memengaruhi kualitas makanan masyarakat pengawasan ketat terus dilakukan baca lebih lanjut di bawah ini idncitizen promedia |
| label_sample_0852 | mengenai program makan bergizi gratis kalian termasuk yg mana a tidak setuju dengan programnya b setuju dengan programnya tapi implementasi harus tetap dievaluasi c tidak setuju dengan penyelenggara tapi kalau diselenggarakan oleh kubu kami sih otomatis akan setuju |
| label_sample_0853 | iyakann asli yg voters ini otak nya dangkal dangkal bngt bahkan aku pun bilang mbg itu program aneh ga ada yg namanya makan siang gratis klo sampe ada itu bakalan chaos bngt karna org cuma mikirin soal makan aja ga ada yg mikir buat nyari makan karna udh d suapin |
| label_sample_0854 | masyarakat yg sejahtera adalah yg bisa makan bergizi gratis di saat banyak mahasiswa yg kuliah di ln lebih milih dpt ilmu yg mumpuni tp rela sehari makan sekali atau di kasus aku seminggu hari makan mi hari bru makan nasi biar hemat pendidikan tuh hrsnya prioritas |
| label_sample_0855 | burhan pun meminta pemberantasan korupsi kpk kejaksaan agung dan polri turut membantu pemerintah mengawasi program mbg agar tidak dikorupsi karena besar sekali warga yang mengat menyatakan tidak percaya pelaksana mbg ini bebas korupsi ujarnya |
| label_sample_0856 | mulai maret makan bergizi gratis bakal habiskan anggaran rp triliun per bulan jika jumlah penerima mbg meningkat menjadi juta maka anggaran yang diperlukan bakal menjadi rp triliun per bulan kata kepala bgn dadan hindayana |
| label_sample_0857 | gue gk suka sih sama mbg ini tapi tapi pak prabs udah terlanjur blunder kan bawa program ini pas kampanye dan psti ditagih dong dan skrg programnya udah jalan nih mau realisasinya buruk tp kan at least ke deliver kan wkwwkkw tipikal pemerintah kita bgt kan so no wonder la |
| label_sample_0858 | kasau tinjau program ketahanan pangan dan makan bergizi gratis di lanud sulaiman kepala staf angkatan udara kasau marsekal tni m tonny harjono s e m m meninjau langsung program ketahanan pangan dan pelaksanaan program makan bergizi gratis mbg di lanud sulaiman dalam |
| label_sample_0859 | rl assaamualaikum bray hahahahay selamat sore selamat sigma alpha beta izin kenalan ketua gua sedang mencari teman teman tongkrongan timeline butuh banget syarat nafas makan minum sendiri bukan mbg mengakui gw pacar hantaesan homophobe dni sawrry |
| label_sample_0860 | oke katakan proyek ikn ini memang distop dulu karena mmg mau revisi anggaran yang perlu dipikirkan termasuk kau juga mikir jelek jeleknya si owo mau fokus proyek mbg ini yang berujung anggaran ikn dipotong ikn setengah jadi apa gak hancur kita duit rakyat itu loh wak |
| label_sample_0861 | pemerintah mulai merealisasikan program makan bergizi gratis mbg program ini diluncurkan untuk mendukung salah satu dari delapan misi asta cita yaitu memperkuat pembangunan sumber daya manusia sdm swasembadaenergi astacitapemerintah makanbergizigratis anakgenerasiemas |
| label_sample_0862 | program gak guna lahan korupsi baru mending gratiskan sekolah subsidi uang kuliah transportasi murah sembako murah lapangan kerja mudah untuk rakyat ri kasih makan rakyat aja ribet amat dah gitu dicekik dgn pajak yg tinggi gak guna itu mbg |
| label_sample_0863 | penjabat gubernur jabar bey machmudin memastikan menganggarkan rp triliun untuk melaksanakan program makan bergizi gratis mbg di seluruh kota kabupaten se jabar selama setahun tvonenews programmakanbergizigratis jabar jawabarat anggaranmgb |
| label_sample_0864 | yaudah biayain aja itu mbg pake uangmu ya pak pdhl udh jelas mbg dari pajak pajak darimana dari rakyat yg banting tulang kerja keras dulu janjinya mau buka lapangan kerja seluas luasnya eh trnyt lapangan kerja nya cuma buat circle nya doang |
| label_sample_0865 | kali ini aku kurang setuju meneruskan produk seperti itu hanya akan membuat siklus persaingan dagang yang sama kurang sehatnya tolong elaborasi lagi contoh diversifikasi ekonomi yang bisa diterapkan untuk indonesia selain yang berkaitan dengan mbg |
| label_sample_0866 | komisi pemberantasan korupsi kpk akan membuat kajian pencegahan rasuah dalam program makan siang gratis proyek itu harus dipantau ketat karena membutuhkan anggaran yang besar kpk makansianggratis medcomid |
| label_sample_0867 | sayur timun minimal dibuat sayur acar plus wortel biar ada rasaâ nya sedikit nikmat ini timun sebagai lalapan telornya kena korting pula mbg fix cuma gugur kewajiban atau tunai janji aja praktiknya ala kadarnya |
| label_sample_0868 | kau paham kata status mis istri cuma ada binikmu atau bukan jangan samakan dg wanits simpanan demikian pula status ibukota negara kota bandung ibukota prov jabar lagi belum karena bla bla bla koplak kali otakmu nanti makan yg bergizi ya lagi gratis |
| label_sample_0869 | hh hari hari merenung kenapa aku wni prioritas utama perumahan tp gabisa kasih rumah terjangkau ya buat apa makan bergizi gratis tp pendidikan dikalahin ya buat apa yg beneran laper gabisa makan tu yg gabisa sekolah |
| label_sample_0870 | kalau gw mah mending mbg fokus di daerah t dulu dah ga usah ngoyo satu indonesia dulu heck janji presiden terdahulu aja ga terpenuhi rakyat tetep biasa aja bapak menuhin janji dgn sebagian dulu juga dah bagus banget kok |
| label_sample_0871 | ubahlah cara gaya meraih simpati massa pencitraan pun harus diubah dg gaya sombong terbukti kalah misal bantu program makan bergizi gratis anda bantu susunya atau tempenya dijamin orang akan bersimpati |
| label_sample_0872 | program mbg presiden mendapat sambutan luar biasa dr sdm unggul indonesia melangitlah generasi sehat cerdas berakhlak sekolah semakin menyenangkan memupuk rasa senasib sepenanggungan tiada batas kaya miskin semua bahagia jadi ingin muda lagi eh sekolah lagi |
| label_sample_0873 | perwakilan plt deputi ii kepala staf kepresidenan melakukan de bottlenecking pelaksanaan mbg melalui rapat koordinasi tindak lanjut percepatan pembayaran hak keuangan bgn dan alternatif sbml bersama bgn kemenkeu ri kementerian pan rb serta kemensetneg di gedung bina graha |
| label_sample_0874 | program makan bergizi gratis mbg yang diperuntukkan bagi siswa sekolah kini menuai sorotan setelah menu yang diberikan saat ramadan diganti menjadi roti dan produk mayora energen berupa sereal instan perubahan ini dianggap semakin menjauh dari prinsip gizi seimbang terutama |
| label_sample_0875 | haha ada benernya sejujurnya setelah kepilih gua baca ulang program dan telaah lagi banyak halangan aja mbg ini secara bahan baku negara ini tidak satu harga ini jadi kendala kalo contoh jepang beli beras di kyoto sama di tokyo harganya sama makanya bisa jalan |
| label_sample_0876 | polres kotabaru turut mendukung pelaksanaan kegiatan uji coba makan bergizi gratis mbg yang berlangsung pada jumat program ini bertujuan meningkatkan gizi anak anak usia dini sekaligus menekan angka stunting di kabupaten kotabaru |
| label_sample_0877 | program makan bergizi gratis mbg yang baru berjalan beberapa bulan menjadi sorotan setelah komisi pemberantasan korupsi kpk menerima laporan adanya dugaan pemotongan anggaran seporsi makanan bagi anak anak dari rp menjadi rp |
| label_sample_0878 | berdasarkan survei awal kedaikopi litbang kompas publik indonesia mayoritas puas dengan kinerja prabowo gibran dengan tingkat kepuasan sekitar program mbg dan respons bencana jadi alasan utama namun protes mahasiswa dark indonesia feb maret tunjukkan |
| label_sample_0879 | nyatanya efesiensi itu untuk kebijakan tdk tepat sasaran seperti mbg gemuknya kabinet gemuknya pengeluaran ruu itu dibahas dpr dan presiden stlh jadi baru diparaf presiden dan kursi di dpr milik kim plus prabowo ngefans prabowo boleh tp bkn berarti semua anda bela |
| label_sample_0880 | ga ada sejarahnya negara maju karena pertanian dan mbg ini malah sekarang pertanian dan mbg buat genjot pertumbuhan ekonomi ke pertanian itu nilai tambah nya kecil dan sangat sensitif terhadap harga kalau naik dikit aja harganya udah diprotes sama konsumen |
| label_sample_0881 | kalau ada apa bilang kalau ada apa bilang ituu kamisan udh puluhan tahun depan istana gk diwaro itu ada pagar laut gk lu samperin sekalian itu ada dosen nuntut tukin gk lu bantu itu anak papua minta pendidikan daripada mbg gk lu samperin indonesiagelap |
| label_sample_0882 | buat pelajar yg dapet mbg kayak gw kalian gk usah ikut protes dengan cara gk makan mbg makan aja soalnya sayang mubazir kasian juga yg udh masak selama kita dapet mbg ayo kita bantu dengan cara yang lain indonesiagelap |
| label_sample_0883 | hari nunggu sisaan sayur mbg si kaka gurunya resah karena di sekolah lain sampah sisa makanan jd masalah baru terutama sayur utk menyiasatinya guru menyarankan anak bawa wadah utk makanan sisa mereka dr sekolah |
| label_sample_0884 | program makan bergizi gratis mbg untuk meningkatkan gizi anak sekaligus memberdayakan umkm serta meningkatkan ekonomi masyarakat kecil di daerah jaringan kuat di daerah akan mempercepat akselerasi umkm melalui penyediaan makanan bergizi dalam program mbg makanbergizigratis |
| label_sample_0885 | jadi buat apa ya gedung dpr coba di list pembahasan uu apa saja di hotel mewah uu kejaksaan di sheraton uu pdp di intercontinental ruu tni di fairmont rakyat makan mbg minyak ga cukup sekitar ditulis liter bensin ga sesuai dibayar begitu kah |
| label_sample_0886 | mangga asam dekat mbg alam sentral sendiri pilih mangga jambu nenas etc sendiri senduk serbuk asam masuk bekas max charge rm tupperware popiah basah dekat tapak penjaja sek belakang de palma nama dia mr popiah sebelah dia ada apam balik sedap nama apam balik istana |
| label_sample_0887 | ga salah belajar ke sini pak anggaran anda sediakan t untuk mbg hari ini pa sudah cerdas anak anak sy setuju mbg tp akan lebih cerdas jika benar benar anda gratiskan sekolah dan kuliah soal makan sediakan aja juta lap kerja yg wapres anda janjikan |
| label_sample_0888 | jujur aja sy makin gak paham arahnya efisiensi anggaran katanya buat mbg tapi salah satu imbasnya mahasiswa poltek di bawah kementerian harus ngirit bahan praktik yg jelas bakal ngefek ke output belajarnya terus sekarang malah ada wacana ini ini negara mau diapain sih |
| label_sample_0889 | program mbg baik program ini hrs di tata dgn baik sasaran utama anak di pelosok kurang mampu termasuk yg tdk sekolah menu di buat o ahli gizi melibatkan ibu pkk di wilayah sekolah u masak bahan baku di beli ke petani sekitar sekolah melakukan pengawasan lbh efisien |
| label_sample_0890 | live now program makansianggratis yang diusung prabowo gibran ramai diperbincangkan sumber anggaran program ini bakal menyedot ratusan triliun rupiah dari mana dananya kami bahas di ruangpublikkbr bersama dan live yt |
| label_sample_0891 | nanya ke dpr dibilang wewenangnya pemerintah nanya ke pemerintah pejabat politis bakal promosiin presiden minta anggaran dipake untuk yg berdampak langsung ke masyarakat tapi ga disebut tuh selain mbg nanya bendahara negara kabur mulu |
| label_sample_0892 | nih staffsus bisanya gaslighting teruus playing victim terus manipulatif teruuss wkwk habis mbg sekarang ruu tni nyalahin terus korbannya dengan menghighlight caranya merespon ketidakwajaran hal yg ga wajarr sudah seharusnya dilawan |
| label_sample_0893 | pemerintah lagi butuh duit tum buat mbg entar ujungnya subsidi gas dikurangin bahkan dihapus ini tes the water aja niatnya cuma warung pengecer berbadan usaha jd pemerintah dapat pajak kalau itu ngak terlaksana pangkalan jd ujung tombak kalau lancar subsidi dikurangi |
| label_sample_0894 | anggota dpd ri provinsi papua david harold waromi melakukan pertemuan dengan penjabat gubernur papua ramses limbong pada pertemuan ini membahas pelaksanaan program makan bergizi gratis mbg di papua dpdri papua mbg daridaerahuntukindonesia |
| label_sample_0895 | gue sih amitâ kasih nilai aja udah bagus gak ada yg bener program mbg gak jalan danantara rampok duit rakyat liat jaksa agung mudah bgt di inversi erik tohir lgsg bilang tak ada korupsi dipertamina uu tni ubah uu tni reformasi seenak perutnya jokowi mentri korupsi tak diadili |
| label_sample_0896 | menu makan bergizi gratis mbg yang disediakan pada pekan pertama ramadhan menuai perdebatan di kalangan masyarakat dalam unggahan yang viral di media sosial terlihat menu mbg berupa roti sereal instan dua buah kurma dan telur rebus |
| label_sample_0897 | dandim manggarai memantau makan bergizi gratis di sdn labuan bajo tniprima tniadprima tniadbekerjadenganhati tniaddihatirakyat tniadberjuangbersamarakyat prajaraksakapedulirakyat pangdamudayana pangdamzamroni mayjenzamroni |
| label_sample_0898 | budi sulistiyo dirjen pdspkp kkp siap mendukung program mbg karena program ini memberikan efek positif baik sisi peningkatan asupan protein masyarakat maupun pemberdayaan ekonomi indonesiaemas programpresiden presidenprabowo makansianggratis kesehatangratisuntuksemua |
| label_sample_0899 | gizi seimbang merupakan fondasi penting untuk mewujudkan generasi indonesia emas yang sehat cerdas dan produktif ini juga yang jadi semangat program makan bergizi gratis yang diluncurkan beberapa waktu lalu yuk sama sama kita dukung program ini selamat hari gizi nasional |
| label_sample_0900 | intinya saat ini pemberitaan fokusnya ke mbg sementara rs menanggung dosa bpjs kesehatan warga tertolong rs bengong ke siapa minta tolong bpjs hanya mengimkan pepesan kosong fraud fraud fraud masa sii karena itu apa karena sudah gak punya dana |
