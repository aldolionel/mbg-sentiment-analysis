# AI-Assisted Sentiment Labeling Prompt - annotation_batch_001

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
| label_sample_0001 | belum selesai lomba di mbg sekarang udah di living |
| label_sample_0002 | good job polri rekrut gizi spesialis buat mbg makin mantap |
| label_sample_0003 | dapoer ibu boyolali terus salurkan mbg untuk para siswa |
| label_sample_0004 | duitnya buat mbg ga bisa bayar artist lokal |
| label_sample_0005 | deket rumah udah ada simulasi makan bergizi gratis |
| label_sample_0006 | mbg tuh makan basi gratis kh |
| label_sample_0007 | mbg hari ini nasi thiwul bothok oseng ndeso tempe bacem |
| label_sample_0008 | kurang mahkotanya king |
| label_sample_0009 | lagi pengen nempeleng orang pencetus program mbg |
| label_sample_0010 | makasih mbg njung |
| label_sample_0011 | fifi masuka |
| label_sample_0012 | sinii mam sma bayiku lebih bergizi dibanding mbg ntu |
| label_sample_0013 | indonesiagelap dibawah rezim ini demi mbg |
| label_sample_0014 | mbg solusi tepat naikin gizi pelajar |
| label_sample_0015 | mbg resmi dimulai |
| label_sample_0016 | ini baru prestasi mbg makin diakui dan dikagumi |
| label_sample_0017 | kl gua ketawa gua dikasi mbg ga |
| label_sample_0018 | pusing tuh mikirin mbg sama danantara awowkwokwok |
| label_sample_0019 | bilahi kone ma nokk la |
| label_sample_0020 | mbg mabok bersama gibran |
| label_sample_0021 | makan bergizi gratis bikin anak makin sehat mantap |
| label_sample_0022 | smpn surabaya mbg nya mirip adkesmah bagi takjil |
| label_sample_0023 | idiih minjem motor siapa lagi si mbg |
| label_sample_0024 | inilah orang yg butuh mbg biar gak stunting |
| label_sample_0025 | mbg mbg adek gw noh gak dapet |
| label_sample_0026 | ndeko |
| label_sample_0027 | mbg upaya populis angkat kualitas sdm yang ancaman apbn |
| label_sample_0028 | kok makan bukanya gak pake makan siang bergizi gratis sih |
| label_sample_0029 | utk menyukseskan mbg asn perlu bekerja hari seminggu |
| label_sample_0030 | mantap mbg dapat apresiasi sepenuh hati |
| label_sample_0031 | makan bergizi gratis langkah brilian kemenrans bgn |
| label_sample_0032 | next bio meat sebagai sumber protein mbg |
| label_sample_0033 | potret penting pendidikan lebih penting dari mbg catat |
| label_sample_0034 | mbg gak mangkrak masih terus berjalan sampai saat ini |
| label_sample_0035 | program mbg diatur sama menteri apa yak |
| label_sample_0036 | iya sebenernya mbg kan makan berisi gula upsie |
| label_sample_0037 | urusin gas aja sono drpd mbg gjlss |
| label_sample_0038 | oo photobox di mbg paling gede |
| label_sample_0039 | tp mbg dan kcic surabaya jalan terus |
| label_sample_0040 | kalo pemerintah kan fokus mbg |
| label_sample_0041 | makan bergizi untuk anak bangsa mbg |
| label_sample_0042 | negara membiarkan kemiskinan solusinya mbg |
| label_sample_0043 | qobul aamiin mbg apa itu |
| label_sample_0044 | untung mha coba mbg |
| label_sample_0045 | mbg b nya katanya bukan bergizi ya tp busuk basi berulat |
| label_sample_0046 | mbg biyokimya |
| label_sample_0047 | surga itu makan bergizi gratis |
| label_sample_0048 | kontol emang mbg makan tuh nasi berak |
| label_sample_0049 | zindagi |
| label_sample_0050 | bersama mbg harapan cerah menyongsong masa depan emas di |
