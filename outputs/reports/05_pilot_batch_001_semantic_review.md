# 05 Pilot Batch 001 Semantic Review

## Environment
- Python version: 3.12.3
- pandas version: 3.0.3

## Scope
- Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis (MBG) pada Media Sosial Menggunakan Support Vector Machine (SVM)
- Semantic review for pilot batch 001 only.
- No model training, SMOTE, external API calls, or raw-file changes were performed.

## Summary
- rows reviewed: 50
- needs manual review: 24 (0.4800)
- short text count: 7

## Label Counts
- netral: 23
- negatif: 15
- positif: 12

## Rows Suggested for Manual Review
| sample_id | label | reason | clean_text |
| --- | --- | --- | --- |
| label_sample_0001 | netral | catatan menunjukkan konteks ambigu/informatif | belum selesai lomba di mbg sekarang udah di living |
| label_sample_0003 | netral | catatan menunjukkan konteks ambigu/informatif | dapoer ibu boyolali terus salurkan mbg untuk para siswa |
| label_sample_0005 | netral | catatan menunjukkan konteks ambigu/informatif | deket rumah udah ada simulasi makan bergizi gratis |
| label_sample_0007 | netral | catatan menunjukkan konteks ambigu/informatif | mbg hari ini nasi thiwul bothok oseng ndeso tempe bacem |
| label_sample_0008 | netral | teks sangat pendek; catatan menunjukkan konteks ambigu/informatif | kurang mahkotanya king |
| label_sample_0010 | positif | teks sangat pendek | makasih mbg njung |
| label_sample_0011 | netral | teks sangat pendek; catatan menunjukkan konteks ambigu/informatif | fifi masuka |
| label_sample_0015 | netral | teks sangat pendek; catatan menunjukkan konteks ambigu/informatif | mbg resmi dimulai |
| label_sample_0017 | netral | catatan menunjukkan konteks ambigu/informatif | kl gua ketawa gua dikasi mbg ga |
| label_sample_0019 | netral | catatan menunjukkan konteks ambigu/informatif | bilahi kone ma nokk la |
| label_sample_0022 | netral | catatan menunjukkan konteks ambigu/informatif | smpn surabaya mbg nya mirip adkesmah bagi takjil |
| label_sample_0023 | netral | catatan menunjukkan konteks ambigu/informatif | idiih minjem motor siapa lagi si mbg |
| label_sample_0026 | netral | teks sangat pendek; catatan menunjukkan konteks ambigu/informatif | ndeko |
| label_sample_0028 | netral | catatan menunjukkan konteks ambigu/informatif | kok makan bukanya gak pake makan siang bergizi gratis sih |
| label_sample_0029 | netral | catatan menunjukkan konteks ambigu/informatif; netral tetapi ada sinyal positif | utk menyukseskan mbg asn perlu bekerja hari seminggu |
| label_sample_0032 | netral | catatan menunjukkan konteks ambigu/informatif | next bio meat sebagai sumber protein mbg |
| label_sample_0035 | netral | catatan menunjukkan konteks ambigu/informatif | program mbg diatur sama menteri apa yak |
| label_sample_0038 | netral | catatan menunjukkan konteks ambigu/informatif | oo photobox di mbg paling gede |
| label_sample_0039 | netral | catatan menunjukkan konteks ambigu/informatif | tp mbg dan kcic surabaya jalan terus |
| label_sample_0040 | netral | catatan menunjukkan konteks ambigu/informatif | kalo pemerintah kan fokus mbg |
| label_sample_0043 | netral | catatan menunjukkan konteks ambigu/informatif | qobul aamiin mbg apa itu |
| label_sample_0044 | netral | catatan menunjukkan konteks ambigu/informatif | untung mha coba mbg |
| label_sample_0046 | netral | teks sangat pendek; catatan menunjukkan konteks ambigu/informatif | mbg biyokimya |
| label_sample_0049 | netral | teks sangat pendek; catatan menunjukkan konteks ambigu/informatif | zindagi |

## Interpretation Notes
- Rows marked `review` are not automatically wrong; they are cases where text is short, ambiguous, informational, joking, or contains lexical cues that merit human review.
- The pilot distribution is still small, so this review should guide annotation consistency before labeling additional batches.

## Self-run acceptance checks
- PASS: semantic review rows > 0
- PASS: labels are allowed values
- PASS: merged clean_text is present
- PASS: review status is present
- PASS: summary JSON can be generated
- PASS: semantic report can be generated

## Next Recommended Step
- Manually inspect the rows marked `review`.
- Decide whether the pilot labeling style is acceptable before continuing to batch 002.