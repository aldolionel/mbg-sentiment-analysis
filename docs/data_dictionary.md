# Data Dictionary

Dokumen ini menjelaskan kolom dataset yang direncanakan untuk penelitian analisis sentimen publik terhadap Program MBG pada media sosial.

Dataset prototype saat ini berasal dari X/Twitter crawl. Struktur data dibuat generik agar X/Twitter, TikTok, atau platform media sosial lain dapat digunakan pada tahap final jika tersedia.

## Kolom Dataset Mentah yang Mungkin Ada

| Kolom | Status | Deskripsi |
| --- | --- | --- |
| `post_id` / `comment_id` | Opsional | ID post atau komentar. Jika berasal dari platform asli, sebaiknya dianonimkan atau diganti dengan ID internal. |
| `source_platform` | Opsional | Platform sumber data, misalnya `x_twitter`, `tiktok`, atau platform lain. |
| `source_url` | Opsional | URL sumber post/komentar. Gunakan hanya jika diperlukan dan aman untuk penelitian. |
| `created_at` | Opsional | Waktu post/komentar dibuat, jika tersedia dan relevan untuk analisis. |
| `text` / `full_text` / `komentar` | Wajib | Teks asli atau teks yang sudah aman digunakan. |
| `clean_text` | Wajib setelah preprocessing | Teks setelah proses pembersihan dan normalisasi. |
| `label` | Wajib untuk supervised learning | Label sentimen, misalnya `positif`, `negatif`, atau `netral`. |
| `label_source` | Opsional | Sumber label, misalnya `manual`, `assisted`, atau `validated`. |
| `notes` | Opsional | Catatan tambahan, misalnya alasan label atau konteks teks yang ambigu. |

## Kolom Interim Saat Ini

Interim dataset dari MBG crawl dataset menyimpan kolom privacy-safe berikut:

| Kolom | Deskripsi |
| --- | --- |
| `interim_id` | ID internal untuk baris interim. |
| `source_file` | Nama file sumber, tanpa path pribadi. |
| `source_sheet` | Sheet sumber untuk file Excel. |
| `source_row_number` | Nomor baris sumber untuk traceability lokal. |
| `clean_text` | Teks hasil basic cleaning. |
| `clean_text_length` | Panjang karakter `clean_text`. |
| `clean_word_count` | Jumlah token whitespace sederhana. |
| `is_empty_clean_text` | Penanda teks kosong setelah cleaning. |
| `is_duplicate_clean_text` | Penanda duplikasi berdasarkan `clean_text`. |

## Catatan Privasi

Identifier pengguna harus dihapus atau dianonimkan. Dataset interim, processed, laporan, dan notebook publik tidak boleh menyimpan username, user ID, `id_str`, `conversation_id_str`, screen name, nama profil, link profil, lokasi, URL gambar, atau informasi lain yang dapat mengidentifikasi individu.

Untuk repository publik, hindari commit file data mentah maupun data hasil olahan yang masih mengandung informasi sensitif.
