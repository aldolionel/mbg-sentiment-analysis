# AI-Assisted Sentiment Labeling Prompt - annotation_batch_020

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
| label_sample_0951 | turut bersimpati tapi untuk kasus kek gini ya mari dihitung berapa jumlah orang yg kehilangan pekerjaan para honorer di lingkungan pemerintah dengan berapa juta orang miskin yg dapat manfaat dari mbg kalo beneran efisiensi cuma gegara mbg dan bukan faktor lain |
| label_sample_0952 | wah kalo beneran jadi lahan basah ngeri banget semoga enggak btw di beberapa daerah pihak mbg datang ngirim makanan berboncengan dengan lembaga uji lab jadi mereka bertugas ngecek kandungan makanan yg akan dibagikan on the spot |
| label_sample_0953 | sorry typo anggaran kementerian kan saat ini dipotong sampai mengorbankan banyak kementerian contohnya kemenkes dan kemendikdasmen menurut gw ga cocok aja kalo kementerian itu dipotong apa lagi kalau hanya untuk membantu anggaran mbg |
| label_sample_0954 | kata siapa negara efisiensi belanja cuma beda alokasi aja dulu uangnya dipake buat asn dan berbagai proyek sekarang duitnya dikumpulin buat support mbg dan bayarin gaji dan tunjangan pejabat kabinet gembrot |
| label_sample_0955 | ketua dewan perwakilan daerah dpd ri sultan bachtiar najamudin mengusulkan agar rakyat memberi sumbangan uang untuk program makan bergizi gratis mbg menurutnya cara itu dapat membantu menyukseskan program pemerintahan presiden ri prabowo subianto dan wakil presiden gibran |
| label_sample_0956 | momen mahasiswa demo indonesiagelap ada mobil pejabat tutup kawan ndasmu patwal kunyuk sering menutup dan membuka jalan rakyat sekarang gantian tolak makan bergizi gratis ganti pendidikan gratis tolak danantara efisiensi malah kumpulin pejabat periode |
| label_sample_0957 | kota tegal menjadi salah salah satu dari empat daerah yang terpilih untuk melaksanakan uji coba mbg di jawa tengah dimana anggaran yang di gunakan untuk uji coba dari anggaran csr hal itu disampaikan kepala dinas pendidikan dan kebudayaan kota tegal m ismail fahmi jumat |
| label_sample_0958 | potret personel polri saat membagikan makanan gratis kepada siswa di sekolah alternatif anak jalanan saaj jakarta selatan program ini merupakan wujud kepedulian terhadap perkembangan sekaligus masa depan generasi emas bangsa polri mendukung makanbergizigratis untuk |
| label_sample_0959 | santai bro se jelek nya mata uang indonesia pelajarnya tetep makan siang gratis pejabatnya tetap koleksi mobil mewah polisinya tetep punya sampingan pungli dan pemerintahnya tetep punya jatah posisi buat anak cucu |
| label_sample_0960 | oh buzzer udh disanguin berapa sama pemerintah cukup kan buat makan sama susu anak trus anak yg skolah tetep dpt mbg wah enak bgt udhnya dibayarin pemerintah bgini ikut program pemerintah kok enak bgt udh bisa umroh berarti kan sama naik haji dr ngebuzzernya |
| label_sample_0961 | kaka yg disini permisi ya ada yg pernah ikut jd anggota barisan relawan nusantara raya brnr ga ka ini tu katanya organisasi yg katanya mengawasi program makan bergizi gratis pak prabowo ktnya anggota tuh digaji umk masing wilayah ktnya entahlah |
| label_sample_0962 | dari tadi lagi scroll tiktok banyak banget video dari kegiatan makan bergizi gratis ank sd rela gk makan kerena memikirkan orang tuanya di rumah anak sd pun sudah mengerti kasih sayang org tua walaupun dia sendiri merasa kurang karena ortunya sibuk bekerja |
| label_sample_0963 | buat apa program mbg jika akan melahirkan generasi otak dan etik kosong indonesia itu butuh pendidikan gratis berkualitas untuk jenjang paud s d pt agar generasi indonesia bangkit dan mampu bersaing di dunia bukan terus dijajah asing dan aseng |
| label_sample_0964 | dgn tni aktif di siber mengawasi pihak yg melemahkan kepercayaan ke pemerintah pertahana itu sdh balik ke pemilu orba bagaimana ada capres kompetitor kalau kritik dianggap melemahkan kepercayaam pertahana dan dibabat tni |
| label_sample_0965 | kata ketua bappenas semua itu ga penting kak yg terpenting dan urgent itu mbg bodo amat rupiah melemah kek ihsg anjlok kek banyak pengangguran dll biar rakyat sendiri yg mikirin tuhas pemerintah hanya mensukseskan mbg titik |
| label_sample_0966 | ini beneran ngomong begini logikanya kalau kerja bisa ngasih makanan yg bergizi buat anaknya bahkan sekeluarga lebih dr x sehari mbg cuma anaknya yg dikasih makan itu juga cuma sehari x sedih sih menteri ngomongnya begini |
| label_sample_0967 | selamat untuk pendukung yg sedang menunggu makan bergizi gratis puyeng dah mikirin dananya yg tetep dr pinjaman pajak qt jg krn aku pendukung yg menunggu internet gratis biar bisa jualan d rmh sambil ngurus rt |
| label_sample_0968 | eh kocak banget wkwkwkw org yg obsess ama mbg tu mendadak relate ke us dan china anjir kalo di kelas udh dimarahin ama prof w yakin kejauhann konteksnya mendadak ke food poisoning padahal masalah utama lebih genting di accessibility mau mara gajadi wkwkwk kocak coyy |
| label_sample_0969 | unjuk rasa tolak program makan bergizi gratis ratusan pelajar papua tuntut pendidikan gratis berkualitas pelajarpapua demopelajar demo wamena makanbergizigratis tolakmbg prndidikangratis strategiid |
| label_sample_0970 | coba dananya yg buat mbg yg puluhan triliun untuk restrukturisasi pendidikan mutasi gurunya dibenerin gaji guru dinaikin biaya pendidikan dimurahin klo bisa gratis standardisasi sekolahnya yg bener infrastruktur nya dimeratakan akan lbh dri rb yg terdampak manfaat |
| label_sample_0971 | terpantau sodara sodara gue yang voters marah marah liat ini mereka gak terima gajinya dipake mbg dan milih mbg aja dibatalin sebelumnya pas pemilu koar mulu jelekkin paslon bangke emang padahal merekanya kerja dibawah pemerintahan yang kena imbas semua bangsat |
| label_sample_0972 | presidential communication office pco meninjau uji coba program makan bergizi gratis mbg di sekolah di bogor senin uji coba dilaksanakan di satuan pelayanan pemenuhan gizi sppg tanah sareal tirtodaily |
| label_sample_0973 | rejim antri nenek antri bpjs mandiri bapak antri bbm subsidi ibu antri gas subsidi anak antri makan gratis yg belum tentu lebih bergizi sementara paraâ menteri paraâ wakil menteri paraâ staf paraâ utusan khusus wira wiri berplup plup tot tot nyerobot jalan tanpa antri |
| label_sample_0974 | dukung ketahanan pangan polres barru bersama bhayangkari tanam jagung di balusu poldasulsel swasembadapangan ketahananpangan polri polisiindonesia polrimendukungketahananpangan polisicintapetani sulsel prabowo gibranrakabumingraka indonesia makanbergizigratis |
| label_sample_0975 | kunjungan ke sekolah apa ini program pendidikan atau sekadar sesi foto buat pencitraan mbg mungkin biar dibilang merakyat padahal rakyat lebih butuh harga sembako turun daripada salam salaman di trotoar |
| label_sample_0976 | orang tua suruh patungan sukseskan program mbg gaji jaksa anggaran polri naik kabinet gendut ini malah jatah budget mbg di turunkan bpjs tahun ini keluar aturan baru yang membatasi pengobatan pengangguran kemisikinan makin banyak pemerintah gagal mensejahterakan rakyatnya |
| label_sample_0977 | bikin pea masyarakatnya konten konten receh sama misinformasi bikin kenyang masyarakatnya anak mudanya liwat mbg jurus ampuh nha adem dha tu rezim yang berkuasa kalau mau aneh aneh soal kebijakan atau bahkan korupsi |
| label_sample_0978 | ada kabar kurang sedep nih dari kepala badan gizi nasional sehingga orang siswa sd negeri dukuh jawa tengah keracunan menurut kalian penyebabnya karena apa ya share pendapat kalian di kolom komentar ya detikfood mbg kbgn |
| label_sample_0979 | bacot panjang lebar cuma pamer tolol ikn di stop mbg ancur itu artinya jujungan kau yg kontol anjing itu bikin kebijakan gak pake otak sama kyk kau anggaran negara abis utang numpuk hasil zonk bangsat |
| label_sample_0980 | pemerintah jepang berminat untuk membantu program makan bergizi gratis mbg yang menjadi program prioritas pemerintahan presiden prabowo subianto untuk mengakomodir keinginan besar presiden prabowo untuk meyediakan makan bergizi tinggi untuk anak anak di indonesia jepang |
| label_sample_0981 | lah iya kan dgn list dr gambar itu org pada takut pendidikan kesehatan ga masuk prioritas utama malah dibawah mbg makanya pada koar kalo diamati sampe pelaksanaannya doang mah jgn sampe udh kejadian kita baru demo karna ya udh ada fotonya itu dr kemenkeu yg asbun itu |
| label_sample_0982 | negri kita negri maritim dgn kekayaan laut yg sangat berlimpah aneka macam ikan dgn kandungan gizinya sangat tinggi ada disana kenapa bukan itu yg dijadikan target mbg kenapa musti serangga emang anak kita binatang ternak ya |
| label_sample_0983 | waktu pemilu ditanya apapun solusinya hilirisasi ditanya sekarang jawabnya mbg mulu us tarif gimana dijawab harus tabah dan kuat emang dari awal semangatnya doang tinggi kalo dikasih pertanyaan apa yang penting jawabnya semangat |
| label_sample_0984 | menteri pertanian mentan andi amran sulaiman bakal menggenjot produksi daging dan hilirisasi bekerja sama dengan para pengusaha untuk mendukung program pemerintah selanjutnya yakni makan bergizi gratis prabowo gibran prabowogibran makanbergizigratis mbg anakanak mentan |
| label_sample_0985 | mbg yang jadi program sorotan pas kampanye skrg selama praktiknya keliatan dikorupsi militerisasi demokrasi yg mantep gini malah rakyat gak dikasih kisi kisi gagalkanruutni tolakruutni tolakrevisiuutni indonesiagelap tolakdwifungsiabri tolakruupolri supremasisipil |
| label_sample_0986 | makan bergizi gratis mbg adalah awal yang sangat fundamental untuk membentuk generasi penerus bangsa indonesia yang kuat cerdas dan tahan terhadap segala ujian sejarah terimakasih bpk presiden karena belum juga genap hari kerja program ini sudah meluncur |
| label_sample_0987 | gue clearly bilang ke temen gue yang akhirnya sadar bahwa pilihannya salah kalau itu bukan ketipu dari debat pilpres udah keliatan kosong program mbg yang asbun doang proses pemilihan wakil yg menyalahi konstitusi dll masih bilang ketipu hahaha jelas ya bukan ketipu |
| label_sample_0988 | program mbg ini juga akan berdampak positif pada pembentukan ekosistem sekolah yang baik seperti kesehatan anak didik dan menekan terjadinya bullying antar siswa kita harus berkolaborasi mengajak banyak pihak untuk mensukseskan program mbg ini |
| label_sample_0989 | tkw baby aisyah minta anaknya tidak ambil makan bergizi gratis tkw di taiwan ini viral setelah meminta anaknya tak mengambil paket makan bergizi gratis di sekolahnya dia mengatakan mengambil paket makan bergizi gratis sama saja merendahkan dirinya yg punya gaji juta sebulan |
| label_sample_0990 | solusine tlfn cc gojek indonesia mbg buat batalin orderan bisa koq saya sering dapt orderan fiktif reecheese factory kena nasi kulit lovers solo rb tak susruh batalin cc orderan batal saldo ga kepotong dan makanan suruh kasih ke yang membutuhkan pnti |
| label_sample_0991 | orde baru again mulai dari presiden yg memangkas rumput rakyat yg katanya untuk makan bergizi gratis dan aparat yg katanya mengayomi mana ngoni band keras yg dpe lirik full kata kata kotor so boleh bangun ato bubar jo |
| label_sample_0992 | homili khotbah hari ini memang manusia butuh makan makanya skrg ada program makan siang gratis atau yg skrg disebut mbg itu ya yah memang susah menolak godaan utk nerima makanan gratis tapi perlu diingat kalau godaan tsb datangnya dr iblis sy ouch |
| label_sample_0993 | komitmen indonesia untuk memastikan setiap anak di indonesia mendapatkan akses terhadap makan bergizi mbg makanbergizigratis makanbergiziuntukindonesi anaksehatbangsahebat gizigratisuntuknegeri ekonomimaju indonesiaemas |
| label_sample_0994 | kalo solusi lebih waras tahan dulu programnya cari alternatif lain buat anggaran mbg selain pecat pecatin yang dibawah bisa cari investor kek sita semua aset koruptor kek dan nyatanya sekolah di daerah terpencil malah diundur mbgnya sy guru daerah terpencil |
| label_sample_0995 | terima kasih untuk semua komponen pendukung program makanan bergizi gratis mbg tanpa kalian program pak prabowosubianto tidak berjalan dengan baik para pengemudi ojol terlihat mendatangi sdn lowokwaru kota malang senin pagi |
| label_sample_0996 | benar sekali apa yg dikatakan ustadz abdul somad sejatinya hanya orangtua yg tahu kesukaan makanan anakâ nya apalagi kualitas dan kuantitas mbg jauuh dibawah standard yg diberikan orangtua mereka sendiri banyak yg tidak mau menghabiskan makanan ala kadarnya akhirnya mubazir |
| label_sample_0997 | berdasarkan analisis kenaikan tarif impor as tidak akan berdampak signifikan pada program mbg prabowo program ini mengandalkan sumber pangan lokal seperti singkong dan beras sehingga minim terpengaruh langsung anggaran sebesar rp triliun juga sudah dialokasikan dan |
| label_sample_0998 | peknas dan badan gizi nasional mencermati semua evaluasi dari simulasi program makan bergizi gratis tsb untuk kemudian bersinergi mengambil langkahâ strategis sehingga program mbg nanti dapat dilakasanakan dgn baik sesuai target dn tujuannya peknas badangizinasional |
| label_sample_0999 | badan gizi nasional bgn menggelar uji coba makan bergizi gratis mbg di kota makassar hari ini uji coba program ini berlangsung di sekolah dengan menyasar siswa bgn makanbergizigratis mbg mbgmakassar pemkotmakassar dannypomanto makassar detiksulsel |
| label_sample_1000 | cmiiw makan bergizi gratis kan buat anak sekolah nih tapi yg dikasih makan gizi gratis ga ada karena ga sekolah putus sekolah karena ortunya kena phk jadinya ga ada duit buat sekolahin anaknya jadinya gmn dong yg makan siapa jadinya |
