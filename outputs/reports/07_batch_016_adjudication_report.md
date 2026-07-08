# Batch 016 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_016_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_016_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_016_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 9
- adjudicated rows: 50
- changed label rows: 7

## Validation Checks
- PASS: final labels are allowed values
- PASS: no missing final labels
- PASS: no duplicate sample_id in adjudication
- PASS: all adjudication sample_id values exist in labeled batch
- PASS: all adjudication sample_id values exist in semantic review

## Changed Label Rows
| sample_id | clean_text | before | after | human_label | human_notes |
| --- | --- | --- | --- | --- | --- |
| label_sample_0753 | pakk di jakarta aja belum semua sdn dapat program mbg apalagi di daerah pakk negara mana pakk yg mau belajar program mbg | netral | negatif | negatif | kritik pemerataan dan klaim program MBG |
| label_sample_0755 | yaelah voters masih aja tone deaf mana tuh yang koar koar siapapun presiden nya kita bakalan gini gini aja kasih makan tuh otak lo pake makanan gratis yang katanya bergizi itu fuck you all | netral | negatif | negatif | nada marah/sarkastik terkait makanan gratis bergizi |
| label_sample_0760 | beneran penasaran seberapa jauh pemerintah bakalan obrak abrik anggaran lain yang lebih penting demi program mbg ini dan berapa lama jg nih program akan bertahan | netral | negatif | negatif | khawatir anggaran penting dikorbankan demi MBG |
| label_sample_0761 | stress masalahnya apa solusinya apa muak banget rasanya sama pemerintah dikira mbg bisa nyegah banjir kali ya gara gara mbg noh semuanya jdi bermasalah pgn berkata kasar tp dah puasa | netral | negatif | negatif | muak dan mengaitkan MBG dengan berbagai masalah |
| label_sample_0763 | generasi penerus bangsa palestina numpang makan dan berak di indonesia untuk sementara pak ga sia sia program makan bergizi gratis | netral | negatif | negatif | sarkasme terhadap manfaat program MBG |
| label_sample_0769 | pak menteri jalan lintas di kab musi rawas rusak parah apakah balai hanya diam tidak berbuat apa krn anggaran nya sdh dipake danantara dan mbg indonesiagelap | netral | negatif | negatif | mengaitkan anggaran MBG dengan jalan rusak |
| label_sample_0793 | di tempat saya gak ada makan bergizi gratis tetap hidup anakâ sekolah gak ada dampaknya ya palingâ kebutuhan pokpk semakin mahal krn naiknya ppn dan pajak utk membiayai mbg ini | netral | negatif | negatif | menyatakan MBG tidak berdampak dan membebani biaya |