# AI-Assisted Sentiment Labeling Prompt - annotation_batch_017

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
| label_sample_0801 | ternyata presiden indonesia saat ini sangat pro rakyat ya sampai memikirkan tentang gizi anak anak setiap hari makanbergizi mbg |
| label_sample_0802 | suatu bangsa harus bersatu padu bareng garong benur untuk dijual ke vietnam dan ingpestasi di vietnam sekolah tinggi tinggi cuman tahunya jual yang ada bukan mengelola menjadi nilai lebih pantes manut aja buat mbg ternyata emang g punya otak semua |
| label_sample_0803 | sama kak kayak ibuku cuman baru engeh efeknya sekarang ini kak sebelumnya selalu bilang bagus dong dikasih makan dulu g ada yg ngasih pas program mbg baru mulai tapi ama adekku rutin dicengcengin sekarang |
| label_sample_0804 | hanya ibu yg tau apa yg terbaik unk anaknya baik gizinya kualitasnya maupun menu makanannya sekali lagi ahok benar semoga ga terjadi lg kasian mereka pelajarannya jadi terganggu geger makan bergizi gratis berujung keracunan massal di sukoharjo |
| label_sample_0805 | ko diem aja to min pak prabowo juga mbok ya buka suara apa ya ga kasian sama pegawai yg pada dirumahkan mbok ya punya hati sedikit gitu lho alasan buat makan bergizi gratis tapi dg cara ngebuat anak lain sekeluarga gabisa makan karna bapak tulang punggungnya dipecat |
| label_sample_0806 | mak gue cerita ketemu kang sate ngeluh dikit yg beli krn mbg nyesel katanya milih mak gua ketawa renyah blg alhamdulillah sadar bang saya mah untungnya ga pilih mereka tuh untung kgk ditusuk lidi sate |
| label_sample_0807 | dalam aksi tersebut terdapat beberapa isu yang dibawakan mulai dari program makan bergizi gratis hingga kabinet gemuk baca selengkapnya penulis zaffar nur hakim hasna kamilah penanggung jawab zaffar nur hakim |
| label_sample_0808 | panglima tni mengerahkan komando distrik militer kodim pangkalan utama tni angkatan laut lantamal dan pangkalan tni angkatan udara lanud untuk mendukung program makan bergizi gratis mbg tni berkomitmen penuh untuk mendukung keberhasilan program presiden ri |
| label_sample_0809 | mereka akan bikin kita semua miskin tapi tidak lapar on point program kayak mbg bansos udah jelas banget implementasinya dan terbukti ampuh belum lagi mayoritas orang indo punya mentalitas kalo dikasih makan harus manut alhasil segan untuk jadi kritis dan mengkritik |
| label_sample_0810 | menkop budi arie tinjau peternakan ayam petelur di bantul untuk persiapkan pasokan mbg koperasi petelur akan dibentuk dukung program presiden prabowo radar jogja budi arie setiadi budiariesetiadi koperasi prabowo u lewatberanda trending |
| label_sample_0811 | makan siang gratis di sekolah memastikan anak anak mendapatkan gizi yang cukup untuk tumbuh sehat dan cerdas indonesiaemas programpresiden presidenprabowo makansianggratis kesehatangratisuntuksemua |
| label_sample_0812 | huru hara yang terkumpul masalah ppn gas elpiji yg menumbalkan korban makan bergizi gratis yg g bergizi dan g gratis presiden yang arogan gak mau menerima kritik menganggap rakyat ini hanya anak kecil pagar di laut yg gk diadili dg jelas cont indonesiagelap |
| label_sample_0813 | yg berhak bilang mewakili rakyat ya memang orang yg sudah dapat mandat prabowo bisa bilang dia didukung rakyat karena punya suara kalau dia bilang rakyat setuju dengan mbg karena itu janji kampanyenya tapi ya sampai di situ aja kalau yg lain ya kek kamu juga klaim |
| label_sample_0814 | mbg udh dijalanin pr skrg dr pemerintah itu ngubah sifat anti kritik yg dibangun mulyono orang ngekritik itu berarti peduli kritikannya harus diterima dulu dan diakui klo memang ternyata masih ada kekurangan |
| label_sample_0815 | tingkat kepuasan publik terhadap kinerja prabowo gibran menurut salah satu lembaga survey mencapai persen di hari kerja apa yang perlu dievaluasi dari program program prabowo gibran yang sudah berjalan seperti program mbg talk pengamat komunikasi politik dr |
| label_sample_0816 | kagak ada tuh dikomen gue juga yg blg mbg ala kadarnya terus gara gue bilang yg penting ada dulu katanya gak apa nasi pungut dijalan klw buat org bermobil emang ala kadarnya kali yah gue yg pernah di garis depan pendidikan aja miris makanya dukung mbg |
| label_sample_0817 | ketika ditanya itu saya pun jawab pak sebenarnya indonesia seharusnya terlebih dahulu terimbas krisis daripada thailand ekonomi kita rapuh pak jadi bapak selama ini dibohongi apalagi adanya soal mbg danantara dan juga liga korupsi indonesia serta mundurnya smi |
| label_sample_0818 | siapa sih orang tua yg g mau anaknya makan makanan bergizi sy yakin g ada cuma keadaan aja yg membuat orang tua memberi makanan seadanya kalau sy boleh ususl mending alihkan saja mbg jadi program wajib belajar thn pastika biayanya gratis sy jamin ini investasi yg tepat |
| label_sample_0819 | sampean alergi telur tp ndakpapa jg sih krn trget mbg ini kn ank skolah bumil bkn bpk alergi itu slh satu kndala kndala yg mdh dmitigasi drpd program trilyunn jd mbadzir krn menunya tlr dadar ikn kring sarden dll blm lg resiko keracunan krn downgrade bahanbaku |
| label_sample_0820 | kalau orang tua bilang aku dulu tapi ngga ngerti esensi mbg udah gausah didengerin baca ngga dia rkp kalau mbg itu prioritas nasional ke bukan pribadi atau individu tercantum kok kalorinya jelly drink berapa kkal |
| label_sample_0821 | bacoot aja lo yg di gedein otak lo kecilin kalau orang mengkritik tuh program tandanya itu orang kepengen tuh program bisa berjalan dengan baik sesuai janji kampanye yang di gaung kan dulu dan makan bergizi gratis yg di janjikan sesuai kebutuhan para siswa yg menerima |
| label_sample_0822 | itu titipan bu menku yang ribet kesana kemari mencari tambahan kas negara demi nuruti keinginan sang presiden minta mbg jalan terus dan desakan sang mantan presiden minta ikn dilanjutkan bu menku telp pak menkes pak menkes wa dirut bpjs pokoknya naik pak menbumn senyum |
| label_sample_0823 | cukup besar harga yang harus di bayar rakyat dalam degelan negeri pak inilah yang kami sebut dengan indonesiagelap ada mbg untuk sebagian kecil anak indonesia tapi ada puluhan ribu bapak anak indonesia tak ada pekerjaan terus harus penuhi kebutuhan gizi dng apa pak |
| label_sample_0824 | ini habit petinggi yg dari dulu gua g srek tidak meneruskan sesuatu dari pemimpin sebelumnya proyek mbg wes gagal total gagal kalau mau berjalan solusi yg bagus berdayakan kantin canangkan program bersih alat makan setelah dipakai daripada jadiin proyek lahan basah oknum |
| label_sample_0825 | hasan nasbi mengatakan program makan bergizi gratis mbg yang diluncurkan pemerintah tidak hanya sekadar menyediakan makanan sehat bagi anak anak tetapi juga membawa dampak positif dalam pembentukan perilaku dan kebiasaan mereka |
| label_sample_0826 | masalah gizi dan stunting masih menjadi tantangan di indonesia program makan siang gratis di sekolah membantu memastikan setiap anak mendapatkan makanan bergizi yang mereka butuhkan untuk tumbuh optimal dan berprestasi indonesiaemas presidenprabowo makansianggratis |
| label_sample_0827 | program mbg itu bukan yg paling urgent lebih mendesak menambah lapangan kerja gaji untuk hidup baik menurunkan harga barang dan menegakkan supremasi hukum tapi akiâ gemoy ngga suka dikasih masukan mindsetnya jelek anda bersama saya atau anda melawan saya kusut jadinya |
| label_sample_0828 | pake dibandingin sama azka kalo ikut syuting dia gak komplen pas makan nasi kotak kan kocak mbg kan tiap hari kalo suka terjadi yg disajikan kurang layak gimana itu poinnya pak deddy nasi kotak azka juga pasti proper dan relatif yg oke kalo memungkinkan |
| label_sample_0829 | katanya sudah merdeka tapi mau kuliah kok biayanya seperti waktu di jaman penjajahan hanya anak pejabat dan pengusaha kaya yang bisa kuliah rakyat jelata cukup dikasih mbg saja kata sujiwo tesdo jancok |
| label_sample_0830 | mbg di seluruh indonesia kenyataannya di kabupaten tempat kami belum ada itu makan gratis begitu juga di ibukota provinsi lampung jarang sekolah yang ada mbg gabungnya seolah di seluruh sekolah telah ada mbg nyatanya jarang |
| label_sample_0831 | ini pemerintah an maunya apaan sih bener ga tahan gw sm gobloknya udah tau kurikulum kagak bener libur ditambah terus ortu blm mulai cuti anak udah libur ortu udah mulai masuk kerja anak masih libur biar mbg ngurang situ yg bikin program ga pake otak ortu yg jd korban |
| label_sample_0832 | program makan bergizi gratis oleh pemerintahan prabowo gibran memiliki sejumlah manfaat yaitu terpenuhinya gizi anak turunnya angka defisiensi makronutrien prabowogibran prabowo gibran quickwin makanbergizigratis indonesiasehat indonesiamaju kerjanyata merakyat |
| label_sample_0833 | polres jember polda jatim melaksanakan program dari presiden bapak prabowo subianto yaitu membagikan makan siang bergizi gratis untuk anak sekolah kegiatan membagikan makan siang bergizi bertujuan untuk menambah atau memberikan asupan gizi yang lebih baik kepada anak anak |
| label_sample_0834 | tentu tidak murah karena itu dunia usaha turut berpartisipasi selengkapnya jawaban saya mengenai mbg gotong royong silahkan disimak di video berikut ini yuk tanya apa lagi tulis di kolom komentar dengan hastag tanyanin mbg makanbergizigratis mbggotongroyong kadin |
| label_sample_0835 | kepala kantor komunikasi kepresidenan hasan nasbi menanggapi ancaman dari organisasi papua merdeka opm yang mengancam akan membakar sekolah sekolah penerima mbg dengan menyatakan bahwa siapa pun yang mencoba menghalangi program ini akan berhadapan dengan tni polri |
| label_sample_0836 | elu terlalu positif ngeliat pemerintah nyet jadi tujuannya itu buat cuma makan gratis makan bergizi cegah stunting atau apa udah bandingin belom sama janji kampanyenya bangun woi baru keluar dari goa apa gimane apa kerjaan lu emang nyebokin program ngaco |
| label_sample_0837 | mulai terasa efek bagi bagi jabatan mbg dan iikn plus hutang negara herannya yg dipangkas selalu yg berbau subsidi rakyat padahal penyakit kronis negara ini dari dulu kanker korupsi pejabat dan hasil sda yang menguap ok gaass kanlah |
| label_sample_0838 | bodoh banget udh mah ga tepat sasaran ga bergizi ga bernutrisi juga tidak ada urgensi nya mbg ini ga sepenting itu untuk diprioritaskan sekolah juga ga semuanya dapet bahkan di daerah kabupaten yang dapet malah sekolah percontohan yg emg udh bagus |
| label_sample_0839 | lebih lanjut stafsus lenis kogoya mengajak seluruh elemen masyarakat untuk mendukung program ini demi masa depan yang lebih baik bagi generasi muda papua stafsusleniskogoya kemhan kemhanri programmakanbergizigratis mbg |
| label_sample_0840 | mbg bukanlah bantuan karena ia dianggarkan dari dana apbn yang berasal dari pajak rakyat dan oleh sebab itu rakyat tak perlu bersyukur maupun berterima kasih kepada pemerintah letkol deddy corbuzier tak mampu memahami hal ini ulasan abil arqam |
| label_sample_0841 | sudah ada gak ya evaluasi dari makan bergizi gratis yang sudah jalan beberapa bulan coba cek apakah ada kenaikan skor iq dari sebelum atau setelah makan bergizi gratis atau malah ga ada data evaluasinya utk mengukur seberapa efektif program ini |
| label_sample_0842 | hi foters kalian masih ingatkan program makan siang gratis yang berubah menjadi makan bergizi gratis kita akan bahas malam ini dalam fokus terkini manfaat program makan gizi gratis apa ya foters fokusterkini tvrinasional makanbergizigratis |
| label_sample_0843 | gw pernah jd extras dan dapet makan siang dr mereka enak anjir bandingin sm mbg ya jauh wajar si azka masih mau makan isinya ada ayam telor kadang dapet daging lah lu liat mbg noh kek apaan tahu bentukannya coba azka suruh makan mbg |
| label_sample_0844 | halo program makan bergizi gratis mbg nggak bermasalah langsung meski ada tarif negatif trump ke impor ri pemerintah ri prioritaskan mbg rp t buat sdm lawan stunting tarif bisa tekan ekonomi tapi diplomasi ke as jaga stabilitas mbg tetap krusial apalagi |
| label_sample_0845 | gak paham isi uud isi pancasila cuma beri makan ikan mbg sembako warga jika paham beri pancingan jaring kapal memadai hingga dpt ikan banyak bagi rata masyarakat hasil dijual hingga export bikin peluang usaha yg profit mampu bayar pajak devisa kembali pemasukan negara |
| label_sample_0846 | intinya evaluasi masalahnya uang itu dipaksain dengan asal potong aggaran imo bakal lebih bagus tahapannya bikin fasilitasi tiap daerah buat sembada pangan baru bisa bilang mbg kalo caranya gitu biayanya bisa lebih murah petani dan pekerja muda yg lo bilang engga ilang |
| label_sample_0847 | rasional saja mitra catering mbg dengan paket menu makan anggaran rata rata sepuluhriburp dapat apa dapat apa dipahami kemitraan yg sehat yg makan kenyang bergizi dan tidak terancam keracunan tekanan memenuhi paket mbg menjadi buntung |
| label_sample_0848 | wuih keren nih pemerintah jepang undang pemerintah indonesia buat diskusi soal program makan bergizi gratis jepang mempersilakan pemerintah indonesia untuk bisa pelajari program makan gratis di jepang programpemerintah makanbergizigratis programmakansianggratis jepang |
| label_sample_0849 | kenapa mbg di tuduh kpk di media ada pengurangan harga coba utk oknum pejabat yg sdh pernah dipanggil kpk spt kasus migor dn bnyak lagi tp di diamkan saja berani utk mrk tdk punya backing emang dulunya dibentuk kpk krna polri dn kejaksaan melempem tp skrg terpilih dr polisi juga |
| label_sample_0850 | yth presidenku bapak salam hormat ijin usul pak sebaiknya yg diberi bantuan makan bergizi gratis yg membutuhkan saja sekolah mengusulkan nama anak yg membutuhkan dikandung maksud agar efektif dan efisien terima kasih |
