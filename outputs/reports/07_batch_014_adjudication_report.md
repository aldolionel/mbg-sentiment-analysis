# Batch 014 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_014_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_014_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_014_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 7
- adjudicated rows: 50
- changed label rows: 6

## Validation Checks
- PASS: final labels are allowed values
- PASS: no missing final labels
- PASS: no duplicate sample_id in adjudication
- PASS: all adjudication sample_id values exist in labeled batch
- PASS: all adjudication sample_id values exist in semantic review

## Changed Label Rows
| sample_id | clean_text | before | after | human_label | human_notes |
| --- | --- | --- | --- | --- | --- |
| label_sample_0656 | blunder ppn mbg pada gamau mikir dampak lainnya giliran dikasih lihat fakta di lapangan malah cuci tangan mana pendukungnya pada tolol lagi masih aja ngebelain | netral | negatif | negatif | menyebut blunder dan menyerang pembela MBG |
| label_sample_0659 | wooee zakat itu dibagikan kepada fakir miskin atau orang fisabilillah bukan untuk mbg yang mana sebagian besar masih mampu makan di rumah ojo ngawur bambaang | netral | negatif | negatif | menolak penggunaan zakat untuk MBG |
| label_sample_0660 | ini pemerintah sama legislatif kok kayak amatiran ya apa gak dipikir imbasnya apa banyak yg gak bisa menafkahi keluarga dan jadi pengangguran apa karena mbg jadi menghemat sampai segitunya | netral | negatif | negatif | mengkritik pemerintah/legislatif terkait dampak MBG |
| label_sample_0679 | mempersilakan apa minta nih banyak kegiatan apbd yg dipending nunggu juknis kemenkeu denger denger utk sharing biaya mbg emang hasyu kalian ini siapa berbuat siapa yg ikut tanggungjawab | netral | negatif | negatif | kritik sharing biaya dan tanggung jawab MBG |
| label_sample_0685 | tapera bpjs kelangkaan gas melon mbg berujung efisiensi pagar laut danatara ada yg mau nambahin ini baru jalan berapa bulan udah blunder banget pemerintah | netral | negatif | negatif | mengaitkan MBG dengan efisiensi dan blunder pemerintah |
| label_sample_0697 | mbg makan beracun gratis pelajar sdn kasipute di kab bombana sulawesi tenggara muntah usai menerima makan siang bergizi rabu min siapa yg bisa dituntut dg kasus spt ini | netral | negatif | negatif | menyebut MBG sebagai makan beracun gratis |