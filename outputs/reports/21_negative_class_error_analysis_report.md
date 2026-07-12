# 21 Negative-Class Error Analysis Report

## Ringkasan
- total negative test rows: 23
- correct negative rows: 11
- negative error rows: 12

## Distribusi Suggested Error Type
- campuran: 1
- correct_negative: 11
- konteks_kurang: 1
- kritik_implisit: 11
- model_miss: 12
- sarkasme: 2

## Representative Examples
### label_sample_0946
- true_label: negatif
- predicted_label: negatif
- is_correct: True
- suggested_error_type: correct_negative
- clean_text: lah kan nama programnya makan bergizi gratis bukan makan yang penting abis makanya kalo bikin program yg realistis lah giliran dikritik malah disururuh bersyukur karena yg bikin programnya udah mumet kalo kaya gini mah tujuan awal ga tercapai tapi buang anggaran doang malih
- reviewer_notes: Prediksi sudah benar; teks berisi kritik eksplisit terhadap realisme program, respons terhadap kritik, dan pemborosan anggaran.

### label_sample_0791
- true_label: negatif
- predicted_label: netral
- is_correct: False
- suggested_error_type: kritik_implisit;model_miss
- clean_text: pov nya kemiskinan merajalela sekarang pengangguran korupsi pesta anggaran pejabat dan kalian dengan mbg berlagak seperti pahlawan
- reviewer_notes: Model melewatkan kritik implisit yang mengaitkan MBG dengan kemiskinan, korupsi, dan belanja pejabat.

### label_sample_0761
- true_label: negatif
- predicted_label: netral
- is_correct: False
- suggested_error_type: sarkasme;kritik_implisit;model_miss
- clean_text: stress masalahnya apa solusinya apa muak banget rasanya sama pemerintah dikira mbg bisa nyegah banjir kali ya gara gara mbg noh semuanya jdi bermasalah pgn berkata kasar tp dah puasa
- reviewer_notes: Teks memakai nada muak dan sarkastik tentang MBG sebagai solusi yang tidak relevan untuk masalah lain.

### label_sample_0926
- true_label: negatif
- predicted_label: negatif
- is_correct: True
- suggested_error_type: correct_negative
- clean_text: tapi ya ini mbg fucked up juga from the beginning banyak bgt oknum catering yg nyari duit terus korupsi ini catering yg korupsi bsk kalo mati gw doakan liang lahat nisan atau peti nya bau dan lembab kayak nasi basi selain dari dana yg terlalu dipaksakan yaa
- reviewer_notes: Prediksi sudah benar; teks sangat eksplisit mengkritik MBG, korupsi katering, dan pemaksaan anggaran.

### label_sample_0934
- true_label: negatif
- predicted_label: netral
- is_correct: False
- suggested_error_type: kritik_implisit;model_miss
- clean_text: menurut gue kalo emang makan siang gratis bergizi itu ga efektif yaudah batalin aja toh sebelumnya gaada pun ga jadi masalah yang jadi masalah adalah ketika memaksakan program prematur dengan merelakan program yang udah ada efek dominonya jadi meluas kemana mana
- reviewer_notes: Model melewatkan kritik terhadap efektivitas dan pemaksaan program prematur serta efek domino anggaran.

### label_sample_0862
- true_label: negatif
- predicted_label: positif
- is_correct: False
- suggested_error_type: model_miss
- clean_text: program gak guna lahan korupsi baru mending gratiskan sekolah subsidi uang kuliah transportasi murah sembako murah lapangan kerja mudah untuk rakyat ri kasih makan rakyat aja ribet amat dah gitu dicekik dgn pajak yg tinggi gak guna itu mbg
- reviewer_notes: Teks berisi penolakan eksplisit dan frasa negatif kuat seperti program tidak berguna, lahan korupsi, dan pajak tinggi.

### label_sample_0657
- true_label: negatif
- predicted_label: netral
- is_correct: False
- suggested_error_type: kritik_implisit;model_miss
- clean_text: baru banget kmrn diceritain temen kalau dana mbg dikorupsi sama suppliernya alias udah dana nya ga banyak dikorupsi pulaa
- reviewer_notes: Model melewatkan konteks negatif tentang dugaan dana MBG yang dikorupsi supplier.

### label_sample_0006
- true_label: negatif
- predicted_label: negatif
- is_correct: True
- suggested_error_type: correct_negative
- clean_text: mbg tuh makan basi gratis kh
- reviewer_notes: Prediksi sudah benar; teks menyindir MBG sebagai makanan basi.

### label_sample_0107
- true_label: negatif
- predicted_label: netral
- is_correct: False
- suggested_error_type: kritik_implisit;model_miss
- clean_text: penampakan mbg kalau tidak dikorupsi kira kira seperti ini
- reviewer_notes: Model melewatkan kritik implisit tentang korupsi melalui perbandingan penampakan MBG jika tidak dikorupsi.

### label_sample_0404
- true_label: negatif
- predicted_label: negatif
- is_correct: True
- suggested_error_type: correct_negative
- clean_text: mbg kan mau didanain mereka dgn syarat ambil barang dari mereka jg jadi yg bego siapa
- reviewer_notes: Prediksi sudah benar; teks bernada merendahkan dan mengkritik skema pendanaan/barang MBG.

## Thesis-Ready Paragraph
Kelas negatif menjadi kelas yang paling menantang karena jumlah datanya lebih sedikit dan banyak teks negatif disampaikan secara implisit, sarkastik, atau melalui konteks kebijakan yang lebih luas. Beberapa kesalahan model terjadi ketika kritik tidak menggunakan kata negatif yang eksplisit, melainkan berupa pertanyaan retoris, sindiran, atau hubungan tidak langsung dengan isu anggaran, korupsi, dan efektivitas program. Oleh karena itu, performa kelas negatif perlu dibahas sebagai keterbatasan penting dalam penelitian.

## Limitation
Analisis ini adalah AI-assisted qualitative error analysis. Hasil kategori dan catatan harus ditinjau oleh peneliti/manusia sebelum digunakan dalam naskah final.