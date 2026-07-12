# Dataset Provenance

## Ringkasan Provenance
- dataset status: secondary dataset
- selected repo file: `data/raw/data crawl mbg (in).xlsx`
- source paper citation: Sultoni, A., Putra, D. A., Wahidah, H. N., Arief, M. M., & Putria, P. J. R. M. (2025). Public Sentiment Analysis and Distribution Optimization MBG. Jurnal Matematika Thales (JMT), 7(1), 35-53.
- source platform: X/Twitter
- source paper dataset size: 47,803 posts
- source paper collection method: keyword-based scraping
- source paper example keywords: "Makan Bergizi Gratis", "Program Gizi", "Stunting", related hashtags
- source paper dataset access: Google Drive link mentioned in source paper
- license status: license not explicitly identified from available local documents

## Penggunaan di Repository Ini
Repository ini menggunakan file `data/raw/data crawl mbg (in).xlsx` sebagai dataset mentah terpilih. Dataset tersebut diperlakukan sebagai dataset sekunder yang berasal dari atau berasosiasi dengan penelitian Sultoni et al. (2025).

Dataset final untuk eksperimen tesis adalah `data/processed/mbg_labeled_sample_1000.csv`, yaitu sampel berlabel sebanyak 1.000 data. Sampel ini diberi label melalui AI-assisted labeling dengan adjudication/manual review.

## Limitation
The current repo uses a sampled and relabeled subset for thesis modeling, so results are not directly comparable to the full Sultoni et al. dataset.

Detail lisensi, URL Google Drive, dan metadata izin penggunaan perlu diverifikasi langsung dari paper/source dataset owner sebelum publikasi final.

## Thesis-Ready Wording
> Penelitian ini menggunakan dataset sekunder dari penelitian Sultoni et al. (2025) yang berisi unggahan media sosial X/Twitter terkait Program MBG. Dari dataset tersebut, penelitian ini menggunakan sampel berlabel sebanyak 1.000 data untuk eksperimen klasifikasi sentimen dengan label AI-assisted dan adjudication/manual review.