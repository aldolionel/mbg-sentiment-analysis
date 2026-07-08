# Batch 017 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_017_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_017_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_017_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 11
- adjudicated rows: 50
- changed label rows: 9

## Validation Checks
- PASS: final labels are allowed values
- PASS: no missing final labels
- PASS: no duplicate sample_id in adjudication
- PASS: all adjudication sample_id values exist in labeled batch
- PASS: all adjudication sample_id values exist in semantic review

## Changed Label Rows
| sample_id | clean_text | before | after | human_label | human_notes |
| --- | --- | --- | --- | --- | --- |
| label_sample_0804 | hanya ibu yg tau apa yg terbaik unk anaknya baik gizinya kualitasnya maupun menu makanannya sekali lagi ahok benar semoga ga terjadi lg kasian mereka pelajarannya jadi terganggu geger makan bergizi gratis berujung keracunan massal di sukoharjo | netral | negatif | negatif | keracunan massal dan gangguan belajar terkait MBG |
| label_sample_0805 | ko diem aja to min pak prabowo juga mbok ya buka suara apa ya ga kasian sama pegawai yg pada dirumahkan mbok ya punya hati sedikit gitu lho alasan buat makan bergizi gratis tapi dg cara ngebuat anak lain sekeluarga gabisa makan karna bapak tulang punggungnya dipecat | netral | negatif | negatif | kritik PHK/efisiensi demi MBG |
| label_sample_0816 | kagak ada tuh dikomen gue juga yg blg mbg ala kadarnya terus gara gue bilang yg penting ada dulu katanya gak apa nasi pungut dijalan klw buat org bermobil emang ala kadarnya kali yah gue yg pernah di garis depan pendidikan aja miris makanya dukung mbg | netral | positif | positif | secara eksplisit menyatakan dukung MBG |
| label_sample_0818 | siapa sih orang tua yg g mau anaknya makan makanan bergizi sy yakin g ada cuma keadaan aja yg membuat orang tua memberi makanan seadanya kalau sy boleh ususl mending alihkan saja mbg jadi program wajib belajar thn pastika biayanya gratis sy jamin ini investasi yg tepat | netral | negatif | negatif | mengusulkan pengalihan MBG ke wajib belajar |
| label_sample_0820 | kalau orang tua bilang aku dulu tapi ngga ngerti esensi mbg udah gausah didengerin baca ngga dia rkp kalau mbg itu prioritas nasional ke bukan pribadi atau individu tercantum kok kalorinya jelly drink berapa kkal | netral | positif | positif | membela esensi dan prioritas nasional MBG |
| label_sample_0823 | cukup besar harga yang harus di bayar rakyat dalam degelan negeri pak inilah yang kami sebut dengan indonesiagelap ada mbg untuk sebagian kecil anak indonesia tapi ada puluhan ribu bapak anak indonesia tak ada pekerjaan terus harus penuhi kebutuhan gizi dng apa pak | netral | negatif | negatif | kritik biaya sosial MBG dan pengangguran |
| label_sample_0834 | tentu tidak murah karena itu dunia usaha turut berpartisipasi selengkapnya jawaban saya mengenai mbg gotong royong silahkan disimak di video berikut ini yuk tanya apa lagi tulis di kolom komentar dengan hastag tanyanin mbg makanbergizigratis mbggotongroyong kadin | netral | positif | positif | mendorong partisipasi dunia usaha untuk MBG |
| label_sample_0836 | elu terlalu positif ngeliat pemerintah nyet jadi tujuannya itu buat cuma makan gratis makan bergizi cegah stunting atau apa udah bandingin belom sama janji kampanyenya bangun woi baru keluar dari goa apa gimane apa kerjaan lu emang nyebokin program ngaco | netral | negatif | negatif | menyebut program ngaco dan menyerang pembela MBG |
| label_sample_0847 | rasional saja mitra catering mbg dengan paket menu makan anggaran rata rata sepuluhriburp dapat apa dapat apa dipahami kemitraan yg sehat yg makan kenyang bergizi dan tidak terancam keracunan tekanan memenuhi paket mbg menjadi buntung | netral | negatif | negatif | kritik anggaran katering, risiko keracunan, dan kerugian mitra |