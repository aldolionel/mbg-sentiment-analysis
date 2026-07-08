# AI-Assisted Sentiment Labeling Prompt - annotation_batch_004

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
| label_sample_0151 | lah iya menunya gak kaya mbg |
| label_sample_0152 | kebalikannya bang ipul kwkwkwk |
| label_sample_0153 | katanya king indonesia kok gak masuk list |
| label_sample_0154 | bolehkah makan bergizi gratis mbg di sekolah pilih menu |
| label_sample_0155 | kok hampir semua kementrian pd ngotot mbg ada apa |
| label_sample_0156 | mending ini drpd mbg |
| label_sample_0157 | ga salah sih mbg kan makanan beracun gratis |
| label_sample_0158 | prabowo sukses angkat harapan rakyat mbg top |
| label_sample_0159 | ompreng penjara mbg |
| label_sample_0160 | demi mbg semua di korbankan |
| label_sample_0161 | good job polri dukung terus program gizi mbg |
| label_sample_0162 | degeul domram bi |
| label_sample_0163 | gawin kaya lagi makan makanan bergizi gratis |
| label_sample_0164 | apapun masih mending dibanding mbg asu ini wkwkw |
| label_sample_0165 | otw mbg |
| label_sample_0166 | mbg opo |
| label_sample_0167 | pawankalyanbdaycelebrations adv hbd my man ï x f |
| label_sample_0168 | mending gaji dpd aja yg dipake mbg |
| label_sample_0169 | kemenkop fasilitasi gakoptindo jadi penyuplai program mbg |
| label_sample_0170 | asosiasi minta program mbg berpihak pada peternak lokal |
| label_sample_0171 | mbemba |
| label_sample_0172 | ora mangan mbg ora pateken |
| label_sample_0173 | mbg sopo |
| label_sample_0174 | program mbg patut diacungi jempol inspiratif |
| label_sample_0175 | tunjangan gaji lu pada aja dikurangin buat mbg gimana |
| label_sample_0176 | kelompok knpb bawa semangat perjuangkan papua dari mbg |
| label_sample_0177 | haish dasar hoax jelas jelas mbg bagus untuk rakyat |
| label_sample_0178 | full untuk mbg |
| label_sample_0179 | nggak perlu khawatir lagi kesehatan terjamin sama mbg |
| label_sample_0180 | masakan nuna lebih enak padahaal timbang mbg wkwkw |
| label_sample_0181 | mbg malak bapa gratis |
| label_sample_0182 | mantap mbg sukses dukung kesejahteraan gizi bangsa |
| label_sample_0183 | khan ada makan siang gratis |
| label_sample_0184 | sangat bermanfaat semoga mbg makin meluas jangkauannya |
| label_sample_0185 | skema makan bergizi gratis asa besar yang membebani umkm |
| label_sample_0186 | mbg nj m |
| label_sample_0187 | gk liat aja vendor mbg kabur |
| label_sample_0188 | wallah comp na wa vas y toi |
| label_sample_0189 | mbg tu program pemerintah apa rakyat sebenernya |
| label_sample_0190 | di mbg aja kalau mau murmer ya erlangga kris a |
| label_sample_0191 | budone senegal baniuni kou goor ki dako ligey ptdr |
| label_sample_0192 | ya kan lucunya kemarin tuh smpet bahas mbg |
| label_sample_0193 | wacha kucheka sana mtu wa mjengo asituskie |
| label_sample_0194 | muka kebanyakan mbg ceking kucel ngomong tak jelas |
| label_sample_0195 | janganâ yang ngirim si jelmaan napoleon dr animal farm |
| label_sample_0196 | mbg dorong sdm unggul untuk sambut dengan senyuman |
| label_sample_0197 | itu mah mbg cuy |
| label_sample_0198 | mbg tuh apa ya kak makanan babi gendut kahh |
| label_sample_0199 | setidaknya biar jelas maunya apa mbg |
| label_sample_0200 | dia ngomong apa emang ttg mbg ikn |
