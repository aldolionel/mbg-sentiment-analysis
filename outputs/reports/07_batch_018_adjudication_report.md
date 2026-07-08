# Batch 018 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_018_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_018_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_018_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 11
- adjudicated rows: 50
- changed label rows: 8

## Validation Checks
- PASS: final labels are allowed values
- PASS: no missing final labels
- PASS: no duplicate sample_id in adjudication
- PASS: all adjudication sample_id values exist in labeled batch
- PASS: all adjudication sample_id values exist in semantic review

## Changed Label Rows
| sample_id | clean_text | before | after | human_label | human_notes |
| --- | --- | --- | --- | --- | --- |
| label_sample_0860 | oke katakan proyek ikn ini memang distop dulu karena mmg mau revisi anggaran yang perlu dipikirkan termasuk kau juga mikir jelek jeleknya si owo mau fokus proyek mbg ini yang berujung anggaran ikn dipotong ikn setengah jadi apa gak hancur kita duit rakyat itu loh wak | netral | negatif | negatif | kritik pengalihan anggaran IKN ke MBG |
| label_sample_0869 | hh hari hari merenung kenapa aku wni prioritas utama perumahan tp gabisa kasih rumah terjangkau ya buat apa makan bergizi gratis tp pendidikan dikalahin ya buat apa yg beneran laper gabisa makan tu yg gabisa sekolah | netral | negatif | negatif | mengkritik prioritas MBG dibanding pendidikan/perumahan |
| label_sample_0871 | ubahlah cara gaya meraih simpati massa pencitraan pun harus diubah dg gaya sombong terbukti kalah misal bantu program makan bergizi gratis anda bantu susunya atau tempenya dijamin orang akan bersimpati | netral | positif | positif | menyarankan bantuan susu/tempe untuk mendukung MBG |
| label_sample_0872 | program mbg presiden mendapat sambutan luar biasa dr sdm unggul indonesia melangitlah generasi sehat cerdas berakhlak sekolah semakin menyenangkan memupuk rasa senasib sepenanggungan tiada batas kaya miskin semua bahagia jadi ingin muda lagi eh sekolah lagi | netral | positif | positif | memuji sambutan dan manfaat MBG bagi generasi |
| label_sample_0881 | kalau ada apa bilang kalau ada apa bilang ituu kamisan udh puluhan tahun depan istana gk diwaro itu ada pagar laut gk lu samperin sekalian itu ada dosen nuntut tukin gk lu bantu itu anak papua minta pendidikan daripada mbg gk lu samperin indonesiagelap | netral | negatif | negatif | menyiratkan prioritas lain lebih penting daripada MBG |
| label_sample_0885 | jadi buat apa ya gedung dpr coba di list pembahasan uu apa saja di hotel mewah uu kejaksaan di sheraton uu pdp di intercontinental ruu tni di fairmont rakyat makan mbg minyak ga cukup sekitar ditulis liter bensin ga sesuai dibayar begitu kah | netral | negatif | negatif | keluhan anggaran dan kebutuhan rakyat terkait MBG |
| label_sample_0895 | gue sih amitâ kasih nilai aja udah bagus gak ada yg bener program mbg gak jalan danantara rampok duit rakyat liat jaksa agung mudah bgt di inversi erik tohir lgsg bilang tak ada korupsi dipertamina uu tni ubah uu tni reformasi seenak perutnya jokowi mentri korupsi tak diadili | netral | negatif | negatif | menyatakan program MBG tidak jalan dan kritik keras pemerintah |
| label_sample_0900 | intinya saat ini pemberitaan fokusnya ke mbg sementara rs menanggung dosa bpjs kesehatan warga tertolong rs bengong ke siapa minta tolong bpjs hanya mengimkan pepesan kosong fraud fraud fraud masa sii karena itu apa karena sudah gak punya dana | netral | negatif | negatif | kritik fokus pada MBG saat isu BPJS/RS bermasalah |