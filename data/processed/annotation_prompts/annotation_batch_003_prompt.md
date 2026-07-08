# AI-Assisted Sentiment Labeling Prompt - annotation_batch_003

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
| label_sample_0101 | makan gratis bergizi demi anak indonesia berprestasi |
| label_sample_0102 | miris ditengah program mbg |
| label_sample_0103 | gpp ngotot aja terus gass mbg biar makin ambles |
| label_sample_0104 | makan bergizi gratis bkin enerjik dan smangat trus |
| label_sample_0105 | kasih mbg malah tambah letoy |
| label_sample_0106 | mbg mall bringkits galleria |
| label_sample_0107 | penampakan mbg kalau tidak dikorupsi kira kira seperti ini |
| label_sample_0108 | gktau tuh blm dapet samsek si mbg mbg itu |
| label_sample_0109 | haha sponsor mbg ternyata wong tuwo ku dhewe |
| label_sample_0110 | udah gitu masih maksa mbg hdehh |
| label_sample_0111 | btul mbg di rumah selain itu gk seru |
| label_sample_0112 | cobain menu mbg dong buat bukber |
| label_sample_0113 | si mulisema tukubali watufinye instead tuwafinye |
| label_sample_0114 | side dish mbg soon |
| label_sample_0115 | eeh mpangi |
| label_sample_0116 | hebat gerakan mbg bikin dunia lebih peduli sama gizi |
| label_sample_0117 | kalo sampe sekeren itu mbg bayar lah gaji staffnya ndut |
| label_sample_0118 | mbg jadi mgb makan nggak bayar |
| label_sample_0119 | hizo falta again mbg |
| label_sample_0120 | ramadhan mbg tetap berjalan |
| label_sample_0121 | mbg makan bayar gratis |
| label_sample_0122 | udah isinya evaluasi mbg gelombang pertama |
| label_sample_0123 | mbg tuh apa si makan bersama gratis |
| label_sample_0124 | mbg adek gweh lontonge basi lagi anjink |
| label_sample_0125 | terima kasih pak prabowo makanbergizigratis mbg papua |
| label_sample_0126 | keren banget program mbg sukses besar dalam hari pertama |
| label_sample_0127 | bubarin danantara sama stop mbg dlu baru dimaapin |
| label_sample_0128 | mantapp mbg semoga makin lancarr |
| label_sample_0129 | banyak negara ingin mencontoh mbg |
| label_sample_0130 | yg deket mbg |
| label_sample_0131 | hii km dah dpt mbg brp kali |
| label_sample_0132 | abis pada di kasih makan bergizi gratis |
| label_sample_0133 | ndut santai vs ndut mbg |
| label_sample_0134 | ogiaahh kalau duta mbg nanti kena tabox deddy botax |
| label_sample_0135 | ya kan telat ga dapat mbg cuy |
| label_sample_0136 | menu mbg dong harusnya pak biar kelihatan konsistensinya |
| label_sample_0137 | dengan program mbg sehat untuk semua bukan lagi mimpi |
| label_sample_0138 | mbg bukan |
| label_sample_0139 | lumayan dapet sisa mbg |
| label_sample_0140 | nyiapin mbg untuk kenzo |
| label_sample_0141 | ust abd somad kajian makan bergizi gratis |
| label_sample_0142 | emang mbg masih ada |
| label_sample_0143 | jangan dibuang kak sayang buat lauk mbg |
| label_sample_0144 | makansianggratis di london diperpanjang |
| label_sample_0145 | trikot |
| label_sample_0146 | mbg aja diambil yg bukan jatahnya kocak lu semua |
| label_sample_0147 | maaf bgt aku salah baca mgb jadi mbg |
| label_sample_0148 | coba aja menu mbg gitu |
| label_sample_0149 | endingnya plg makan bergizi gratis ga jalanw wkwk |
| label_sample_0150 | oke mbg nan |
