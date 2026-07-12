# Annotation Codebook MBG Sentiment

## Scope of Sentiment
Sentimen dinilai terhadap Program Makan Bergizi Gratis (MBG), bukan terhadap aktor politik, platform media sosial, atau isu lain yang hanya muncul sebagai konteks tambahan.

## Label Definitions
### positif
Teks mendukung, mengapresiasi, menyetujui, atau menyampaikan dampak baik dari Program MBG.

### negatif
Teks mengkritik, menolak, menyindir secara negatif, meragukan, atau menyampaikan dampak buruk/masalah terkait Program MBG.

### netral
Teks bersifat informatif, deskriptif, berita, pertanyaan tanpa polaritas jelas, atau konteksnya tidak cukup untuk menentukan positif/negatif.

## Decision Rules
- Mixed sentiment: pilih label dominan. Jika dukungan dan kritik seimbang atau tidak jelas, gunakan `netral`.
- Factual/news text: gunakan `netral` jika hanya menyampaikan informasi tanpa evaluasi.
- Rhetorical questions: nilai berdasarkan arah makna. Jika menyindir atau mengkritik MBG, gunakan `negatif`; jika tidak jelas, gunakan `netral`.
- Sarcasm: jika sarkasme jelas diarahkan negatif pada MBG, gunakan `negatif`; jika tidak jelas, gunakan `netral`.
- Unrelated but mentions MBG: gunakan `netral` jika MBG hanya disebut tanpa evaluasi relevan.
- Ambiguous/insufficient context: gunakan `netral` dan tandai untuk review jika diperlukan.

## Examples Template
Tambahkan contoh hanya dari baris dataset aktual atau contoh yang sudah diizinkan untuk publikasi.

| clean_text | label | alasan |
| --- | --- | --- |
| <contoh aktual dari dataset> | positif/negatif/netral | <alasan singkat> |

## Transparent Labeling Workflow
1. AI-assisted initial labeling digunakan untuk membantu pemberian label awal.
2. Semantic review dilakukan untuk meninjau kasus ambigu atau berpotensi salah.
3. Adjudication/manual review dilakukan untuk menetapkan label akhir pada kasus yang perlu koreksi.
4. Label saat ini tidak boleh disebut pure manual gold standard kecuali divalidasi ulang melalui studi gold-label terpisah.

## Future Validation Plan
- Ambil 150-200 sampel untuk gold validation.
- Gunakan dua annotator independen.
- Hitung Cohen's Kappa untuk inter-annotator agreement.
- Hitung AI-vs-gold agreement untuk mengukur kualitas label berbantuan AI.