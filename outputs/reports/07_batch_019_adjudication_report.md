# Batch 019 Adjudication Report

## Outputs
- adjudicated batch: `data\processed\annotation_labeled_batches\annotation_batch_019_adjudicated.csv`
- normalized adjudication: `data\processed\adjudication\annotation_batch_019_adjudication_normalized.csv`
- summary JSON: `outputs\reports\07_batch_019_adjudication_summary.json`

## Row Counts
- original labeled rows: 50
- adjudication rows: 13
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
| label_sample_0902 | bingung bingung bingung mau diumpetin dimana lagi mukaku lebih baik mana program mbg bila dibanding apa yg pernah dengungkan saat kampanye pilpres yg berjanji untuk generasi penerus bangsa nkriðÿ ðÿ yg salah nya program pendidikan gratis | netral | negatif | negatif | membandingkan MBG dengan janji pendidikan gratis secara kritis |
| label_sample_0915 | sumpah deh dia tu tau ga si lebih baik harga bahan pokok yg dimurahin drpd mbg ga jelas itu emangnya yg butuh makan cm anakâ doang org dewasa jg butuh makan yg bergizi cok oke fokusnya ke anak tp dg harga pangan yg murah kan ortunya mampu beli anak mau apa aja bs diusahain | netral | negatif | negatif | menyebut MBG tidak jelas dan lebih memilih harga bahan pokok murah |
| label_sample_0929 | pantesab mbg cuma k per anak mending makan paket nasi ayam di ciputat nambah k udah mah kenyang enak pula bingung gue sama kebijakan danantara sampe sah begini mana namanya kaya pinjol ilegal ajg wkkwk strezz | netral | negatif | negatif | mengkritik porsi/biaya MBG dan kebijakan terkait |
| label_sample_0934 | menurut gue kalo emang makan siang gratis bergizi itu ga efektif yaudah batalin aja toh sebelumnya gaada pun ga jadi masalah yang jadi masalah adalah ketika memaksakan program prematur dengan merelakan program yang udah ada efek dominonya jadi meluas kemana mana | netral | negatif | negatif | menilai MBG tidak efektif dan prematur |
| label_sample_0935 | sebetulnya apa yg seharusnya pemerintah lakukan untuk membalikan keadaan kalo dari gw mengurangi jumlah kabinet stafsus mengurangi gaji tunjangan pejabat tinggi mengurangi belanja tidak esensial menunda mbg ganti blt stop ikn | netral | negatif | negatif | menyarankan menunda MBG dan mengganti dengan BLT |
| label_sample_0940 | mana dipaksa target ngurus swasembada buat program mbg tapi kena efisiensi paling gede itu konsepny gmn deh kita survey ke lapangan pake tenaga dan otak juga harus keluarin modal sendiri buat uang jalan dan makan kah | netral | negatif | negatif | mengkritik beban target swasembada untuk MBG di tengah efisiensi |
| label_sample_0946 | lah kan nama programnya makan bergizi gratis bukan makan yang penting abis makanya kalo bikin program yg realistis lah giliran dikritik malah disururuh bersyukur karena yg bikin programnya udah mumet kalo kaya gini mah tujuan awal ga tercapai tapi buang anggaran doang malih | netral | negatif | negatif | menilai program tidak realistis dan buang anggaran |