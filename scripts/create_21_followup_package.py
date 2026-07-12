"""Create provenance fix, error analysis, and validation package outputs."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "mbg_labeled_sample_1000.csv"
CANDIDATE_PATH = (
    PROJECT_ROOT / "outputs" / "reports" / "20_negative_class_error_analysis_candidates.csv"
)
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
VALIDATION_DIR = PROJECT_ROOT / "data" / "processed" / "validation"

PROVENANCE_REPORT_PATH = REPORTS_DIR / "21_dataset_provenance_fix_report.md"
DATASET_PROVENANCE_DOC_PATH = PROJECT_ROOT / "docs" / "dataset_provenance.md"
NEGATIVE_FILLED_PATH = REPORTS_DIR / "21_negative_class_error_analysis_filled.csv"
NEGATIVE_REPORT_PATH = REPORTS_DIR / "21_negative_class_error_analysis_report.md"
VALIDATION_TEMPLATE_CSV_PATH = VALIDATION_DIR / "validation_sample_200_template.csv"
VALIDATION_TEMPLATE_XLSX_PATH = VALIDATION_DIR / "validation_sample_200_template.xlsx"
VALIDATION_AI_PREFILLED_PATH = VALIDATION_DIR / "validation_sample_200_ai_prefilled.csv"
VALIDATION_REPORT_PATH = REPORTS_DIR / "21_validation_package_report.md"
PAPER_REWRITE_PLAN_PATH = REPORTS_DIR / "21_paper_rewrite_plan.md"
THESIS_REWRITE_PLAN_PATH = REPORTS_DIR / "21_thesis_rewrite_plan.md"
FOLLOWUP_VALIDATION_REPORT_PATH = REPORTS_DIR / "21_followup_validation_report.md"

RANDOM_STATE = 42
ALLOWED_LABELS = ["positif", "negatif", "netral"]

SOURCE_CITATION = (
    "Sultoni, A., Putra, D. A., Wahidah, H. N., Arief, M. M., & Putria, "
    "P. J. R. M. (2025). Public Sentiment Analysis and Distribution "
    "Optimization MBG. Jurnal Matematika Thales (JMT), 7(1), 35-53."
)
THESIS_READY_PROVENANCE = (
    "Penelitian ini menggunakan dataset sekunder dari penelitian Sultoni et al. "
    "(2025) yang berisi unggahan media sosial X/Twitter terkait Program MBG. "
    "Dari dataset tersebut, penelitian ini menggunakan sampel berlabel sebanyak "
    "1.000 data untuk eksperimen klasifikasi sentimen dengan label AI-assisted "
    "dan adjudication/manual review."
)


ERROR_ANALYSIS_MAP: dict[str, tuple[str, str]] = {
    "label_sample_0946": (
        "correct_negative",
        "Prediksi sudah benar; teks berisi kritik eksplisit terhadap realisme program, respons terhadap kritik, dan pemborosan anggaran.",
    ),
    "label_sample_0791": (
        "kritik_implisit;model_miss",
        "Model melewatkan kritik implisit yang mengaitkan MBG dengan kemiskinan, korupsi, dan belanja pejabat.",
    ),
    "label_sample_0761": (
        "sarkasme;kritik_implisit;model_miss",
        "Teks memakai nada muak dan sarkastik tentang MBG sebagai solusi yang tidak relevan untuk masalah lain.",
    ),
    "label_sample_0926": (
        "correct_negative",
        "Prediksi sudah benar; teks sangat eksplisit mengkritik MBG, korupsi katering, dan pemaksaan anggaran.",
    ),
    "label_sample_0934": (
        "kritik_implisit;model_miss",
        "Model melewatkan kritik terhadap efektivitas dan pemaksaan program prematur serta efek domino anggaran.",
    ),
    "label_sample_0862": (
        "model_miss",
        "Teks berisi penolakan eksplisit dan frasa negatif kuat seperti program tidak berguna, lahan korupsi, dan pajak tinggi.",
    ),
    "label_sample_0657": (
        "kritik_implisit;model_miss",
        "Model melewatkan konteks negatif tentang dugaan dana MBG yang dikorupsi supplier.",
    ),
    "label_sample_0006": (
        "correct_negative",
        "Prediksi sudah benar; teks menyindir MBG sebagai makanan basi.",
    ),
    "label_sample_0107": (
        "kritik_implisit;model_miss",
        "Model melewatkan kritik implisit tentang korupsi melalui perbandingan penampakan MBG jika tidak dikorupsi.",
    ),
    "label_sample_0404": (
        "correct_negative",
        "Prediksi sudah benar; teks bernada merendahkan dan mengkritik skema pendanaan/barang MBG.",
    ),
    "label_sample_0836": (
        "correct_negative",
        "Prediksi sudah benar; teks berisi kritik eksplisit terhadap pemerintah dan program yang dianggap tidak jelas tujuannya.",
    ),
    "label_sample_0042": (
        "kritik_implisit;model_miss",
        "Model melewatkan kritik singkat/implisit bahwa MBG diposisikan sebagai solusi untuk kemiskinan.",
    ),
    "label_sample_0702": (
        "correct_negative",
        "Prediksi sudah benar; teks mengkritik respons sistem terhadap makanan basi/keracunan dalam MBG.",
    ),
    "label_sample_0963": (
        "correct_negative",
        "Prediksi sudah benar; teks mempertanyakan manfaat MBG dan memprioritaskan pendidikan gratis berkualitas.",
    ),
    "label_sample_0953": (
        "kritik_implisit;campuran;model_miss",
        "Model melewatkan kritik kebijakan anggaran; bahasanya relatif moderat sehingga mudah terbaca netral.",
    ),
    "label_sample_0960": (
        "sarkasme;kritik_implisit;model_miss",
        "Model melewatkan sarkasme tentang buzzer, pemerintah, dan keuntungan dari program.",
    ),
    "label_sample_0860": (
        "correct_negative",
        "Prediksi sudah benar; teks mengkritik pemotongan anggaran dan risiko proyek MBG terhadap penggunaan uang rakyat.",
    ),
    "label_sample_0247": (
        "kritik_implisit;model_miss",
        "Model melewatkan kritik berbentuk pertanyaan/keluhan tentang kegiatan meninjau MBG yang dikaitkan dengan skincare.",
    ),
    "label_sample_0895": (
        "correct_negative",
        "Prediksi sudah benar; teks berisi kritik luas terhadap MBG, tata kelola, korupsi, dan isu politik lain.",
    ),
    "label_sample_0124": (
        "correct_negative",
        "Prediksi sudah benar; teks menyebut pengalaman makanan basi dalam MBG dengan nada negatif.",
    ),
    "label_sample_0009": (
        "kritik_implisit;model_miss",
        "Model melewatkan ekspresi kemarahan terhadap pencetus program MBG.",
    ),
    "label_sample_0658": (
        "correct_negative",
        "Prediksi sudah benar; teks mengkritik sasaran program yang dianggap tidak tepat dan boros anggaran/makanan.",
    ),
    "label_sample_0155": (
        "konteks_kurang;kritik_implisit;model_miss",
        "Model melewatkan pertanyaan bernada curiga tentang kementerian yang ngotot terhadap MBG; konteksnya singkat.",
    ),
}


def ensure_dirs() -> None:
    """Create required output directories."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    DATASET_PROVENANCE_DOC_PATH.parent.mkdir(parents=True, exist_ok=True)


def label_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return label counts and percentages."""
    counts = df["label"].value_counts().reindex(["negatif", "netral", "positif"])
    result = counts.rename("count").reset_index()
    result.columns = ["label", "count"]
    result["percentage"] = result["count"] / len(df) * 100
    return result


def provenance_markdown(title: str) -> str:
    """Build provenance documentation content."""
    return "\n".join(
        [
            f"# {title}",
            "",
            "## Ringkasan Provenance",
            "- dataset status: secondary dataset",
            "- selected repo file: `data/raw/data crawl mbg (in).xlsx`",
            f"- source paper citation: {SOURCE_CITATION}",
            "- source platform: X/Twitter",
            "- source paper dataset size: 47,803 posts",
            "- source paper collection method: keyword-based scraping",
            "- source paper example keywords: \"Makan Bergizi Gratis\", \"Program Gizi\", \"Stunting\", related hashtags",
            "- source paper dataset access: Google Drive link mentioned in source paper",
            "- license status: license not explicitly identified from available local documents",
            "",
            "## Penggunaan di Repository Ini",
            "Repository ini menggunakan file `data/raw/data crawl mbg (in).xlsx` sebagai dataset mentah terpilih. Dataset tersebut diperlakukan sebagai dataset sekunder yang berasal dari atau berasosiasi dengan penelitian Sultoni et al. (2025).",
            "",
            "Dataset final untuk eksperimen tesis adalah `data/processed/mbg_labeled_sample_1000.csv`, yaitu sampel berlabel sebanyak 1.000 data. Sampel ini diberi label melalui AI-assisted labeling dengan adjudication/manual review.",
            "",
            "## Limitation",
            "The current repo uses a sampled and relabeled subset for thesis modeling, so results are not directly comparable to the full Sultoni et al. dataset.",
            "",
            "Detail lisensi, URL Google Drive, dan metadata izin penggunaan perlu diverifikasi langsung dari paper/source dataset owner sebelum publikasi final.",
            "",
            "## Thesis-Ready Wording",
            f"> {THESIS_READY_PROVENANCE}",
        ]
    )


def write_provenance_docs() -> None:
    """Write provenance report and docs page."""
    DATASET_PROVENANCE_DOC_PATH.write_text(
        provenance_markdown("Dataset Provenance"),
        encoding="utf-8",
    )
    PROVENANCE_REPORT_PATH.write_text(
        provenance_markdown("21 Dataset Provenance Fix Report")
        + "\n\n## Catatan Implementasi\n"
        + "- Dokumen ini tidak mengubah data mentah, dataset final, atau label.\n"
        + "- Dokumen ini hanya memperbaiki framing provenance agar sesuai dengan kritik metodologis.\n",
        encoding="utf-8",
    )


def fill_negative_error_analysis() -> tuple[pd.DataFrame, dict[str, Any]]:
    """Fill negative-class error analysis candidates with AI-assisted notes."""
    candidates = pd.read_csv(CANDIDATE_PATH)
    filled_rows = []
    for _, row in candidates.iterrows():
        sample_id = row["sample_id"]
        suggested, note = ERROR_ANALYSIS_MAP.get(
            sample_id,
            (
                "correct_negative" if bool(row["is_correct"]) else "model_miss",
                "Catatan otomatis berdasarkan prediksi dan label; perlu review manusia.",
            ),
        )
        new_row = row.to_dict()
        new_row["suggested_error_type"] = suggested
        new_row["reviewer_notes"] = note
        filled_rows.append(new_row)

    filled = pd.DataFrame(filled_rows)
    filled.to_csv(NEGATIVE_FILLED_PATH, index=False, encoding="utf-8")

    type_counts: Counter[str] = Counter()
    for value in filled["suggested_error_type"]:
        for category in str(value).split(";"):
            type_counts[category] += 1

    total = int(len(filled))
    correct = int(filled["is_correct"].astype(str).str.lower().eq("true").sum())
    errors = total - correct
    examples = filled.head(10)

    lines = [
        "# 21 Negative-Class Error Analysis Report",
        "",
        "## Ringkasan",
        f"- total negative test rows: {total}",
        f"- correct negative rows: {correct}",
        f"- negative error rows: {errors}",
        "",
        "## Distribusi Suggested Error Type",
    ]
    for category, count in sorted(type_counts.items()):
        lines.append(f"- {category}: {count}")

    lines.extend(["", "## Representative Examples"])
    for _, row in examples.iterrows():
        lines.extend(
            [
                f"### {row['sample_id']}",
                f"- true_label: {row['true_label']}",
                f"- predicted_label: {row['predicted_label']}",
                f"- is_correct: {row['is_correct']}",
                f"- suggested_error_type: {row['suggested_error_type']}",
                f"- clean_text: {row['clean_text']}",
                f"- reviewer_notes: {row['reviewer_notes']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Thesis-Ready Paragraph",
            "Kelas negatif menjadi kelas yang paling menantang karena jumlah datanya lebih sedikit dan banyak teks negatif disampaikan secara implisit, sarkastik, atau melalui konteks kebijakan yang lebih luas. Beberapa kesalahan model terjadi ketika kritik tidak menggunakan kata negatif yang eksplisit, melainkan berupa pertanyaan retoris, sindiran, atau hubungan tidak langsung dengan isu anggaran, korupsi, dan efektivitas program. Oleh karena itu, performa kelas negatif perlu dibahas sebagai keterbatasan penting dalam penelitian.",
            "",
            "## Limitation",
            "Analisis ini adalah AI-assisted qualitative error analysis. Hasil kategori dan catatan harus ditinjau oleh peneliti/manusia sebelum digunakan dalam naskah final.",
        ]
    )
    NEGATIVE_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    return filled, {
        "total_negative_test_rows": total,
        "correct_negative_rows": correct,
        "negative_error_rows": errors,
        "suggested_error_type_distribution": dict(type_counts),
    }


def make_validation_sample(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Create stratified 200-row validation templates."""
    sample, _ = train_test_split(
        df,
        train_size=200,
        stratify=df["label"],
        random_state=RANDOM_STATE,
    )
    sample = sample.sort_values("sample_id").reset_index(drop=True)
    base = pd.DataFrame(
        {
            "sample_id": sample["sample_id"],
            "clean_text": sample["clean_text"],
            "existing_label": sample["label"],
            "annotator_1_label": "",
            "annotator_1_notes": "",
            "annotator_2_label": "",
            "annotator_2_notes": "",
            "final_gold_label": "",
            "adjudication_notes": "",
            "ai_suggested_label": "",
            "ai_suggested_notes": "",
        }
    )
    template = base.copy()
    template.to_csv(VALIDATION_TEMPLATE_CSV_PATH, index=False, encoding="utf-8")
    template.to_excel(VALIDATION_TEMPLATE_XLSX_PATH, index=False)

    ai_prefilled = base.copy()
    ai_prefilled["ai_suggested_label"] = ai_prefilled["existing_label"]
    ai_prefilled["ai_suggested_notes"] = (
        "Proxy AI-assisted suggestion copied from existing project label; "
        "must be independently reviewed by human annotators."
    )
    ai_prefilled.to_csv(VALIDATION_AI_PREFILLED_PATH, index=False, encoding="utf-8")

    counts = sample["label"].value_counts().reindex(["negatif", "netral", "positif"])
    summary = {
        "rows": int(len(sample)),
        "label_distribution": {label: int(count) for label, count in counts.items()},
        "random_state": RANDOM_STATE,
    }

    lines = [
        "# 21 Validation Package Report",
        "",
        "## Ringkasan",
        "- Paket ini menyiapkan template validasi AI-assisted/proxy untuk review manusia.",
        "- Cohen's Kappa belum dihitung karena belum ada dua anotator independen manusia.",
        "- Template tidak mengisi `annotator_1_label`, `annotator_2_label`, atau `final_gold_label`.",
        "- File AI-prefilled hanya mengisi `ai_suggested_label` dan `ai_suggested_notes`.",
        "",
        "## Sampling",
        f"- source dataset: `{DATA_PATH}`",
        "- sampling: stratified 200-row sample where possible",
        f"- random_state: {RANDOM_STATE}",
        "- label distribution:",
    ]
    for label, count in summary["label_distribution"].items():
        lines.append(f"  - {label}: {count}")
    lines.extend(
        [
            "",
            "## Output Files",
            f"- `{VALIDATION_TEMPLATE_CSV_PATH}`",
            f"- `{VALIDATION_TEMPLATE_XLSX_PATH}`",
            f"- `{VALIDATION_AI_PREFILLED_PATH}`",
            "",
            "## Instructions for Human Annotators",
            "- Gunakan `docs/annotation_codebook_mbg_sentiment.md` sebagai pedoman label.",
            "- Isi `annotator_1_label` dan `annotator_1_notes` untuk anotator pertama.",
            "- Isi `annotator_2_label` dan `annotator_2_notes` untuk anotator kedua.",
            "- Gunakan label yang valid: `positif`, `negatif`, `netral`.",
            "- Setelah dua anotator selesai, lakukan adjudication dan isi `final_gold_label` serta `adjudication_notes`.",
            "- Jalankan `python scripts/compute_validation_kappa.py <path_to_annotated_csv>` untuk menghitung Cohen's Kappa.",
            "",
            "## Limitation",
            "File AI-prefilled bukan gold standard manusia. File tersebut hanya membantu persiapan review dan tidak boleh dipakai untuk mengklaim validasi manusia.",
        ]
    )
    VALIDATION_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return sample, summary


def write_rewrite_plans() -> None:
    """Write paper and thesis rewrite plans."""
    PAPER_REWRITE_PLAN_PATH.write_text(
        "\n".join(
            [
                "# 21 Paper Rewrite Plan",
                "",
                "## Data Source Wording",
                "- Replace old data-source wording with secondary dataset wording.",
                "- Remove any claim that data were crawled by the student/researcher.",
                f"- Use provenance wording: {THESIS_READY_PROVENANCE}",
                "",
                "## Gap and Contribution",
                "- Revise gap from platform novelty to methodology/evaluation gap.",
                "- Emphasize classification workflow, imbalanced AI-assisted labels, SVM tuning, CV/test comparison, and error analysis.",
                "",
                "## Model Conclusion",
                "Tuned LinearSVC dipilih sebagai model final pada eksperimen ini karena memperoleh macro F1 test tertinggi, tetapi perbedaan CV antar tuned SVM kecil sehingga klaim keunggulan ditulis secara hati-hati.",
                "",
                "## Required Additions",
                "- Add provenance subsection citing Sultoni et al. (2025).",
                "- Add codebook/labeling limitation.",
                "- Add near-duplicate check result.",
                "- Add class-weight ablation result.",
                "- Add negative-class error analysis.",
                "- Add data and code availability section.",
                "",
                "## Data and Code Availability Draft",
                "Data yang digunakan merupakan dataset sekunder yang berasosiasi dengan Sultoni et al. (2025). Repository penelitian menyertakan script preprocessing, modeling, evaluasi, dan laporan hasil. Lisensi dataset perlu diverifikasi dari pemilik dataset sebelum publikasi penuh.",
            ]
        ),
        encoding="utf-8",
    )

    THESIS_REWRITE_PLAN_PATH.write_text(
        "\n".join(
            [
                "# 21 Thesis Rewrite Plan",
                "",
                "## Bab 1",
                "- Revisi background agar tidak mengklaim crawling sendiri.",
                "- Revisi problem statement menjadi evaluasi workflow klasifikasi sentimen MBG pada dataset sekunder.",
                "- Revisi objectives: membangun pipeline TF-IDF + SVM, mengevaluasi model pada label AI-assisted, dan menganalisis keterbatasan kelas negatif.",
                "- Revisi benefits agar fokus pada kontribusi metodologis dan pembelajaran klasifikasi teks.",
                "- Revisi limitations: dataset sekunder, label AI-assisted, class imbalance, dan keterbatasan gold validation.",
                "",
                "## Bab 2",
                "- Pertahankan referensi analisis sentimen, TF-IDF, SVM, evaluasi macro F1, dan class imbalance.",
                "- Hapus referensi yang tidak dipakai dalam metodologi atau pembahasan.",
                "- Tambahkan referensi Sultoni et al. (2025) sebagai sumber dataset.",
                "",
                "## Bab 3",
                "- Rename data collection menjadi secondary data source.",
                "- Describe selected Sultoni dataset: X/Twitter, 47,803 posts, keyword-based scraping, Google Drive link in paper.",
                "- Describe sampling 1,000 data untuk eksperimen tesis.",
                "- Describe AI-assisted labeling and codebook.",
                "- Describe evaluation design: split stratified 80/20, CV, macro F1, duplicate check, ablation.",
                "",
                "## Bab 4",
                "- Include dataset distribution.",
                "- Include class-weight ablation.",
                "- Include CV model selection caution.",
                "- Include near-duplicate check result.",
                "- Include negative-class error analysis.",
                "",
                "## Bab 5",
                "- Gunakan conclusion yang hati-hati: Tuned LinearSVC sebagai model final terpilih pada eksperimen ini.",
                "- Hindari klaim opini publik universal.",
                "- Jelaskan limitations: secondary dataset provenance, AI-assisted labels, class imbalance, limited human validation, possible duplicate/semantic similarity limits.",
            ]
        ),
        encoding="utf-8",
    )


def validate_outputs() -> dict[str, bool]:
    """Validate expected files exist and write validation report."""
    expected = [
        PROVENANCE_REPORT_PATH,
        DATASET_PROVENANCE_DOC_PATH,
        NEGATIVE_FILLED_PATH,
        NEGATIVE_REPORT_PATH,
        VALIDATION_TEMPLATE_CSV_PATH,
        VALIDATION_TEMPLATE_XLSX_PATH,
        VALIDATION_AI_PREFILLED_PATH,
        VALIDATION_REPORT_PATH,
        PROJECT_ROOT / "scripts" / "compute_validation_kappa.py",
        PAPER_REWRITE_PLAN_PATH,
        THESIS_REWRITE_PLAN_PATH,
        FOLLOWUP_VALIDATION_REPORT_PATH,
    ]
    status = {str(path): path.exists() for path in expected}
    lines = [
        "# 21 Follow-Up Validation Report",
        "",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## File Existence Checks",
    ]
    for path, exists in status.items():
        lines.append(f"- {'PASS' if exists else 'FAIL'}: `{path}`")
    lines.extend(
        [
            "",
            "## Conclusion",
            "PASS: all required files exist." if all(status.values()) else "FAIL: one or more required files are missing.",
        ]
    )
    FOLLOWUP_VALIDATION_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return status


def create_package() -> None:
    """Create the complete follow-up package."""
    ensure_dirs()
    df = pd.read_csv(DATA_PATH)
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["clean_text"] = df["clean_text"].fillna("").astype(str).str.strip()

    write_provenance_docs()
    negative_filled, negative_summary = fill_negative_error_analysis()
    _, validation_summary = make_validation_sample(df)
    write_rewrite_plans()

    validation_status = validate_outputs()
    # Re-run validation after the validation report creates itself.
    validation_status = validate_outputs()

    package_summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "provenance": {
            "source_citation": SOURCE_CITATION,
            "dataset_status": "secondary dataset",
            "license_status": "license not explicitly identified from available local documents",
        },
        "negative_error_analysis": negative_summary,
        "validation_sample": validation_summary,
        "validation_status": validation_status,
    }
    (REPORTS_DIR / "21_followup_package_summary.json").write_text(
        json.dumps(package_summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Saved provenance report: {PROVENANCE_REPORT_PATH}")
    print(f"Saved provenance doc: {DATASET_PROVENANCE_DOC_PATH}")
    print(f"Saved negative error filled CSV: {NEGATIVE_FILLED_PATH}")
    print(f"Saved validation template CSV: {VALIDATION_TEMPLATE_CSV_PATH}")
    print(f"Saved validation template XLSX: {VALIDATION_TEMPLATE_XLSX_PATH}")
    print(f"Saved validation report: {VALIDATION_REPORT_PATH}")
    print(f"Saved paper rewrite plan: {PAPER_REWRITE_PLAN_PATH}")
    print(f"Saved thesis rewrite plan: {THESIS_REWRITE_PLAN_PATH}")
    print(f"Saved validation report: {FOLLOWUP_VALIDATION_REPORT_PATH}")


def main() -> None:
    """CLI entrypoint."""
    create_package()


if __name__ == "__main__":
    main()
