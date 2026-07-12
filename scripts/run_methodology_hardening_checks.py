"""Run methodology hardening checks after critical review."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "mbg_labeled_sample_1000.csv"
RAW_SELECTED_PATH = PROJECT_ROOT / "data" / "raw" / "data crawl mbg (in).xlsx"
BASELINE_TEST_PATH = PROJECT_ROOT / "outputs" / "reports" / "14_modeling_test_results.csv"
BASELINE_CV_PATH = PROJECT_ROOT / "outputs" / "reports" / "14_modeling_cv_results.csv"
SVM_TEST_PATH = PROJECT_ROOT / "outputs" / "reports" / "15_svm_tuning_test_results.csv"
SVM_ALL_CV_PATH = PROJECT_ROOT / "outputs" / "reports" / "15_svm_tuning_all_cv_results.csv"
FINAL_SUMMARY_PATH = (
    PROJECT_ROOT / "outputs" / "reports" / "16_final_modeling_comparison_summary.json"
)
BEST_SVM_MODEL_PATH = PROJECT_ROOT / "outputs" / "models" / "best_svm_model.joblib"

REPORT_DIR = PROJECT_ROOT / "outputs" / "reports"
HARDENING_REPORT_PATH = REPORT_DIR / "20_methodology_hardening_report.md"
HARDENING_SUMMARY_PATH = REPORT_DIR / "20_methodology_hardening_summary.json"
CLASS_WEIGHT_PATH = REPORT_DIR / "20_class_weight_ablation_results.csv"
CV_SELECTION_PATH = REPORT_DIR / "20_cv_model_selection_summary.csv"
NEAR_DUP_PATH = REPORT_DIR / "20_near_duplicate_train_test_check.csv"
NEGATIVE_ERROR_PATH = REPORT_DIR / "20_negative_class_error_analysis_candidates.csv"
REWRITE_NOTES_PATH = REPORT_DIR / "20_rewrite_notes_after_critical_review.md"
CODEBOOK_PATH = PROJECT_ROOT / "docs" / "annotation_codebook_mbg_sentiment.md"

ALLOWED_LABELS = {"positif", "negatif", "netral"}
LABEL_ORDER = ["negatif", "netral", "positif"]
RANDOM_STATE = 42


def read_json_if_exists(path: Path) -> dict[str, Any] | None:
    """Read JSON when available."""
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_if_exists(path: Path) -> pd.DataFrame | None:
    """Read CSV when available."""
    if not path.exists():
        return None
    return pd.read_csv(path)


def validate_dataset(df: pd.DataFrame) -> dict[str, Any]:
    """Validate final labeled dataset and return summary."""
    labels = df["label"].astype(str).str.strip().str.lower()
    clean_text = df["clean_text"].fillna("").astype(str).str.strip()
    counts = labels.value_counts().reindex(LABEL_ORDER).fillna(0).astype(int)
    percentages = (counts / len(df) * 100).round(2)
    return {
        "rows": int(len(df)),
        "label_distribution": {label: int(count) for label, count in counts.items()},
        "label_percentage": {
            label: float(percent) for label, percent in percentages.items()
        },
        "labels_only_allowed": set(labels).issubset(ALLOWED_LABELS),
        "missing_clean_text": int((clean_text == "").sum()),
        "missing_label": int((labels == "").sum()),
    }


def split_dataset(df: pd.DataFrame):
    """Create deterministic stratified train/test split."""
    return train_test_split(
        df,
        test_size=0.20,
        stratify=df["label"],
        random_state=RANDOM_STATE,
    )


def evaluate_predictions(y_true: pd.Series, y_pred: Any) -> dict[str, Any]:
    """Compute aggregate, per-class metrics, and confusion matrix."""
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision_macro": float(
            precision_score(y_true, y_pred, average="macro", zero_division=0)
        ),
        "recall_macro": float(
            recall_score(y_true, y_pred, average="macro", zero_division=0)
        ),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "f1_weighted": float(
            f1_score(y_true, y_pred, average="weighted", zero_division=0)
        ),
    }
    report = classification_report(
        y_true,
        y_pred,
        labels=LABEL_ORDER,
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(y_true, y_pred, labels=LABEL_ORDER)
    return {"metrics": metrics, "classification_report": report, "confusion_matrix": matrix}


def run_class_weight_ablation(train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Run controlled LinearSVC class_weight ablation."""
    rows: list[dict[str, Any]] = []
    details: dict[str, Any] = {}
    for class_weight, model_name in [
        (None, "LinearSVC class_weight=None"),
        ("balanced", 'LinearSVC class_weight="balanced"'),
    ]:
        pipeline = Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        ngram_range=(1, 2),
                        min_df=2,
                        max_df=0.95,
                        sublinear_tf=True,
                    ),
                ),
                (
                    "classifier",
                    LinearSVC(
                        class_weight=class_weight,
                        random_state=RANDOM_STATE,
                        max_iter=5000,
                    ),
                ),
            ]
        )
        pipeline.fit(train_df["clean_text"], train_df["label"])
        predictions = pipeline.predict(test_df["clean_text"])
        result = evaluate_predictions(test_df["label"], predictions)
        details[model_name] = {
            "class_weight": class_weight,
            "metrics": result["metrics"],
            "classification_report": result["classification_report"],
            "confusion_matrix": result["confusion_matrix"].tolist(),
        }
        row = {
            "model_name": model_name,
            "class_weight": "None" if class_weight is None else class_weight,
            **result["metrics"],
            "confusion_matrix_labels": "|".join(LABEL_ORDER),
            "confusion_matrix_values": result["confusion_matrix"].tolist(),
        }
        for label in LABEL_ORDER:
            class_metrics = result["classification_report"][label]
            row[f"{label}_precision"] = class_metrics["precision"]
            row[f"{label}_recall"] = class_metrics["recall"]
            row[f"{label}_f1"] = class_metrics["f1-score"]
            row[f"{label}_support"] = class_metrics["support"]
        rows.append(row)
    ablation_df = pd.DataFrame(rows)
    ablation_df.to_csv(CLASS_WEIGHT_PATH, index=False, encoding="utf-8")
    return ablation_df, details


def build_cv_model_selection_summary() -> pd.DataFrame:
    """Build CV model-selection summary from existing CV artifacts."""
    rows: list[dict[str, Any]] = []
    baseline_cv = read_csv_if_exists(BASELINE_CV_PATH)
    baseline_test = read_csv_if_exists(BASELINE_TEST_PATH)
    if baseline_cv is not None:
        for _, row in baseline_cv.iterrows():
            test_match = (
                baseline_test.loc[baseline_test["model"] == row["model"]]
                if baseline_test is not None
                else pd.DataFrame()
            )
            rows.append(
                {
                    "model_name": row["model_display_name"],
                    "model_key": row["model"],
                    "source": "14_modeling_cv_results.csv",
                    "cv_mean_macro_f1": row.get("f1_macro_mean"),
                    "cv_std_macro_f1": row.get("f1_macro_std"),
                    "test_macro_f1": (
                        float(test_match.iloc[0]["f1_macro"])
                        if not test_match.empty
                        else None
                    ),
                    "notes": "Baseline CV mean/std available.",
                }
            )

    svm_cv = read_csv_if_exists(SVM_ALL_CV_PATH)
    svm_test = read_csv_if_exists(SVM_TEST_PATH)
    if svm_cv is not None:
        best_per_experiment = (
            svm_cv.sort_values("mean_test_score", ascending=False)
            .groupby("experiment", as_index=False)
            .first()
        )
        for _, row in best_per_experiment.iterrows():
            test_match = (
                svm_test.loc[svm_test["experiment"] == row["experiment"]]
                if svm_test is not None
                else pd.DataFrame()
            )
            rows.append(
                {
                    "model_name": row["experiment_display_name"],
                    "model_key": row["experiment"],
                    "source": "15_svm_tuning_all_cv_results.csv",
                    "cv_mean_macro_f1": row.get("mean_test_score"),
                    "cv_std_macro_f1": row.get("std_test_score"),
                    "test_macro_f1": (
                        float(test_match.iloc[0]["f1_macro"])
                        if not test_match.empty
                        else None
                    ),
                    "notes": "Best grid-search CV row per tuned SVM experiment.",
                }
            )

    cv_df = pd.DataFrame(rows)
    if not cv_df.empty:
        cv_df = cv_df.sort_values(
            ["cv_mean_macro_f1", "test_macro_f1"],
            ascending=[False, False],
        )
    cv_df.to_csv(CV_SELECTION_PATH, index=False, encoding="utf-8")
    return cv_df


def run_near_duplicate_check(train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Find near-duplicate test rows by max TF-IDF cosine similarity to train rows."""
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
        sublinear_tf=True,
    )
    train_matrix = vectorizer.fit_transform(train_df["clean_text"])
    test_matrix = vectorizer.transform(test_df["clean_text"])
    similarity = cosine_similarity(test_matrix, train_matrix)
    max_indices = similarity.argmax(axis=1)
    max_scores = similarity.max(axis=1)
    rows = []
    for test_position, (train_position, score) in enumerate(zip(max_indices, max_scores)):
        if float(score) >= 0.90:
            test_row = test_df.iloc[test_position]
            train_row = train_df.iloc[int(train_position)]
            rows.append(
                {
                    "test_sample_id": test_row.get("sample_id", ""),
                    "test_label": test_row["label"],
                    "nearest_train_sample_id": train_row.get("sample_id", ""),
                    "nearest_train_label": train_row["label"],
                    "similarity_score": float(score),
                    "test_clean_text": test_row["clean_text"],
                    "nearest_train_clean_text": train_row["clean_text"],
                }
            )
    near_dup_df = pd.DataFrame(rows)
    if near_dup_df.empty:
        near_dup_df = pd.DataFrame(
            columns=[
                "test_sample_id",
                "test_label",
                "nearest_train_sample_id",
                "nearest_train_label",
                "similarity_score",
                "test_clean_text",
                "nearest_train_clean_text",
            ]
        )
    near_dup_df.to_csv(NEAR_DUP_PATH, index=False, encoding="utf-8")
    summary = {
        "test_rows_checked": int(len(test_df)),
        "near_duplicate_threshold": 0.90,
        "near_duplicate_rows": int(len(near_dup_df)),
        "near_duplicate_percentage": (
            float(len(near_dup_df) / len(test_df) * 100) if len(test_df) else 0.0
        ),
    }
    return near_dup_df, summary


def build_negative_error_candidates(test_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Create negative-class error analysis candidate file."""
    model_available = BEST_SVM_MODEL_PATH.exists()
    warning = None
    negative_df = test_df.loc[test_df["label"] == "negatif"].copy()
    if model_available:
        model = joblib.load(BEST_SVM_MODEL_PATH)
        predictions = model.predict(test_df["clean_text"])
        test_with_pred = test_df.copy()
        test_with_pred["predicted_label"] = predictions
        negative_df = test_with_pred.loc[test_with_pred["label"] == "negatif"].copy()
        negative_df["is_correct"] = negative_df["label"] == negative_df["predicted_label"]
    else:
        negative_df["predicted_label"] = ""
        negative_df["is_correct"] = ""
        warning = "best_svm_model.joblib not available; prediction columns left blank."

    output_df = pd.DataFrame(
        {
            "sample_id": negative_df.get("sample_id", ""),
            "clean_text": negative_df["clean_text"],
            "true_label": negative_df["label"],
            "predicted_label": negative_df["predicted_label"],
            "is_correct": negative_df["is_correct"],
            "suggested_error_type": "",
            "reviewer_notes": "",
        }
    )
    output_df.to_csv(NEGATIVE_ERROR_PATH, index=False, encoding="utf-8")
    summary = {
        "model_available": model_available,
        "warning": warning,
        "negative_test_rows": int(len(output_df)),
        "negative_correct": (
            int(output_df["is_correct"].sum()) if model_available else None
        ),
        "negative_errors": (
            int((~output_df["is_correct"]).sum()) if model_available else None
        ),
    }
    return output_df, summary


def audit_sampling_metadata(df: pd.DataFrame) -> dict[str, Any]:
    """Audit available sampling/provenance columns."""
    expected = [
        "sample_id",
        "interim_id",
        "source_file",
        "source_sheet",
        "source_row_number",
        "clean_text",
        "label",
    ]
    available = [column for column in expected if column in df.columns]
    docs_text = ""
    for relative_path in [
        "README.md",
        "docs/methodology.md",
        "docs/reproducibility.md",
        "outputs/reports/13_labeled_dataset_1000_report.md",
        "outputs/reports/14_modeling_baseline_report.md",
        "outputs/reports/15_svm_tuning_report.md",
    ]:
        path = PROJECT_ROOT / relative_path
        if path.exists():
            docs_text += "\n" + path.read_text(encoding="utf-8", errors="ignore").lower()
    return {
        "selected_raw_dataset": str(RAW_SELECTED_PATH),
        "selected_raw_dataset_exists": RAW_SELECTED_PATH.exists(),
        "dataset_status": "secondary dataset",
        "source_provenance_status": "needs citation/source URL/license from dataset owner",
        "final_labeled_dataset": str(DATA_PATH),
        "available_metadata_columns": available,
        "sample_id_unique": (
            bool(df["sample_id"].is_unique) if "sample_id" in df.columns else None
        ),
        "source_row_number_exists": "source_row_number" in df.columns,
        "source_row_number_min": (
            int(df["source_row_number"].min()) if "source_row_number" in df.columns else None
        ),
        "source_row_number_max": (
            int(df["source_row_number"].max()) if "source_row_number" in df.columns else None
        ),
        "sampling_reproducible_from_existing_columns": all(
            column in df.columns for column in ["sample_id", "source_row_number"]
        ),
        "random_state_detected_in_docs": "random_state" in docs_text or "random state" in docs_text,
        "sampling_strategy_detected_in_docs": (
            "sample" in docs_text and ("random" in docs_text or "strat" in docs_text)
        ),
        "manual_provenance_limitation": (
            "Exact original crawler identity, crawl date range, keywords, source URL, "
            "and license must be filled manually if not already documented by the dataset owner."
        ),
    }


def write_codebook() -> None:
    """Create explicit annotation codebook documentation."""
    CODEBOOK_PATH.write_text(
        "\n".join(
            [
                "# Annotation Codebook MBG Sentiment",
                "",
                "## Scope of Sentiment",
                "Sentimen dinilai terhadap Program Makan Bergizi Gratis (MBG), bukan terhadap aktor politik, platform media sosial, atau isu lain yang hanya muncul sebagai konteks tambahan.",
                "",
                "## Label Definitions",
                "### positif",
                "Teks mendukung, mengapresiasi, menyetujui, atau menyampaikan dampak baik dari Program MBG.",
                "",
                "### negatif",
                "Teks mengkritik, menolak, menyindir secara negatif, meragukan, atau menyampaikan dampak buruk/masalah terkait Program MBG.",
                "",
                "### netral",
                "Teks bersifat informatif, deskriptif, berita, pertanyaan tanpa polaritas jelas, atau konteksnya tidak cukup untuk menentukan positif/negatif.",
                "",
                "## Decision Rules",
                "- Mixed sentiment: pilih label dominan. Jika dukungan dan kritik seimbang atau tidak jelas, gunakan `netral`.",
                "- Factual/news text: gunakan `netral` jika hanya menyampaikan informasi tanpa evaluasi.",
                "- Rhetorical questions: nilai berdasarkan arah makna. Jika menyindir atau mengkritik MBG, gunakan `negatif`; jika tidak jelas, gunakan `netral`.",
                "- Sarcasm: jika sarkasme jelas diarahkan negatif pada MBG, gunakan `negatif`; jika tidak jelas, gunakan `netral`.",
                "- Unrelated but mentions MBG: gunakan `netral` jika MBG hanya disebut tanpa evaluasi relevan.",
                "- Ambiguous/insufficient context: gunakan `netral` dan tandai untuk review jika diperlukan.",
                "",
                "## Examples Template",
                "Tambahkan contoh hanya dari baris dataset aktual atau contoh yang sudah diizinkan untuk publikasi.",
                "",
                "| clean_text | label | alasan |",
                "| --- | --- | --- |",
                "| <contoh aktual dari dataset> | positif/negatif/netral | <alasan singkat> |",
                "",
                "## Transparent Labeling Workflow",
                "1. AI-assisted initial labeling digunakan untuk membantu pemberian label awal.",
                "2. Semantic review dilakukan untuk meninjau kasus ambigu atau berpotensi salah.",
                "3. Adjudication/manual review dilakukan untuk menetapkan label akhir pada kasus yang perlu koreksi.",
                "4. Label saat ini tidak boleh disebut pure manual gold standard kecuali divalidasi ulang melalui studi gold-label terpisah.",
                "",
                "## Future Validation Plan",
                "- Ambil 150-200 sampel untuk gold validation.",
                "- Gunakan dua annotator independen.",
                "- Hitung Cohen's Kappa untuk inter-annotator agreement.",
                "- Hitung AI-vs-gold agreement untuk mengukur kualitas label berbantuan AI.",
            ]
        ),
        encoding="utf-8",
    )


def write_rewrite_notes() -> None:
    """Write Indonesian thesis/paper rewrite notes after critical review."""
    REWRITE_NOTES_PATH.write_text(
        "\n".join(
            [
                "# 20 Rewrite Notes After Critical Review",
                "",
                "## Framing Dataset",
                "- Ganti framing `crawling sendiri` menjadi `dataset sekunder`.",
                "- Tulis dataset mentah terpilih sebagai `data/raw/data crawl mbg (in).xlsx`.",
                "- Tambahkan catatan bahwa sumber URL, pemilik dataset, lisensi, periode crawl, dan keyword crawl perlu dilengkapi manual dari pemilik dataset.",
                "",
                "## Framing Gap Penelitian",
                "- Hindari novelty berbasis platform saja.",
                "- Ganti gap menjadi gap metodologi/evaluasi: workflow klasifikasi sentimen MBG pada dataset sekunder, label AI-assisted, class imbalance, dan evaluasi SVM dengan macro F1.",
                "",
                "## Alternatif Judul",
                "Studi Klasifikasi Sentimen MBG pada Dataset Sekunder Media Sosial X dengan TF-IDF dan SVM",
                "",
                "## Revisi Rumusan Masalah",
                "- Fokus pada workflow klasifikasi dan performa model pada label AI-assisted yang imbalanced.",
                "- Jelaskan bahwa tujuan bukan mengukur opini publik universal, melainkan mengevaluasi klasifikasi sentimen pada sampel berlabel.",
                "",
                "## Revisi Limitations",
                "- Dataset sekunder dan provenance masih perlu dilengkapi.",
                "- Label AI-assisted dengan adjudication/manual review, bukan pure manual gold standard.",
                "- Class imbalance, terutama kelas negatif.",
                "- Gold validation masih terbatas/belum tersedia.",
                "- Near-duplicate train/test memungkinkan dan sudah dicek menggunakan TF-IDF cosine similarity, tetapi bukan deteksi semantik sempurna.",
                "",
                "## Revisi Kesimpulan",
                "- Hindari klaim opini publik universal.",
                "- Hindari klaim tuning saja menyebabkan peningkatan kecuali ablation mendukung secara hati-hati.",
                "- Posisikan Tuned LinearSVC sebagai model final terpilih berdasarkan macro F1 dengan wording hati-hati.",
            ]
        ),
        encoding="utf-8",
    )


def markdown_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    """Create a compact Markdown table without requiring tabulate."""
    if df.empty:
        return "_Tidak ada data._"
    view = df.head(max_rows)
    columns = list(view.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in view.iterrows():
        values = []
        for column in columns:
            value = row[column]
            if isinstance(value, float):
                values.append(f"{value:.4f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_hardening_report(
    dataset_summary: dict[str, Any],
    sampling_audit: dict[str, Any],
    ablation_df: pd.DataFrame,
    cv_df: pd.DataFrame,
    near_dup_summary: dict[str, Any],
    negative_summary: dict[str, Any],
    final_summary: dict[str, Any] | None,
) -> None:
    """Write Indonesian methodology hardening report."""
    baseline_linear_f1 = None
    tuned_linear_f1 = None
    if final_summary:
        improvement = final_summary.get("linear_svm_improvement", {})
        baseline_linear_f1 = improvement.get("baseline_linear_svm_f1_macro")
        tuned_linear_f1 = improvement.get("tuned_linearsvc_f1_macro")

    none_row = ablation_df.loc[ablation_df["class_weight"] == "None"]
    balanced_row = ablation_df.loc[ablation_df["class_weight"] == "balanced"]
    ablation_note = "Tidak dapat dihitung."
    if not none_row.empty and not balanced_row.empty:
        diff = float(balanced_row.iloc[0]["f1_macro"] - none_row.iloc[0]["f1_macro"])
        ablation_note = (
            f"Pada konfigurasi TF-IDF baseline, class_weight='balanced' mengubah macro F1 "
            f"sebesar {diff:.4f} dibanding class_weight=None. Pada ablation ini, class_weight "
            "saja tidak menjelaskan peningkatan Tuned LinearSVC; peningkatan kemungkinan terkait "
            "kombinasi parameter TF-IDF, nilai C, dan variasi evaluasi. Jangan mengklaim hubungan "
            "kausal tunggal dari class_weight."
        )

    tuned_rows = cv_df[cv_df["model_key"].astype(str).str.startswith("tuned_")]
    cv_warning = "CV tuned SVM tidak tersedia."
    if not tuned_rows.empty:
        spread = tuned_rows["cv_mean_macro_f1"].max() - tuned_rows["cv_mean_macro_f1"].min()
        top_cv_name = tuned_rows.sort_values("cv_mean_macro_f1", ascending=False).iloc[0][
            "model_name"
        ]
        cv_warning = (
            f"Perbedaan CV mean macro F1 antar model tuned SVM hanya {spread:.4f}. "
            f"Model tuned SVM dengan CV mean tertinggi adalah {top_cv_name}, sedangkan "
            "Tuned LinearSVC dipilih karena test macro F1 tertinggi. Jadi, pemilihan Tuned "
            "LinearSVC terutama didasarkan pada test-set macro F1, sementara CV mendukung "
            "bahwa keluarga tuned SVM kompetitif tetapi tidak memberi bukti kuat bahwa "
            "Tuned LinearSVC unggul secara stabil atas tuned SVM lain."
        )

    lines = [
        "# 20 Methodology Hardening Report",
        "",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## 1. Dataset Provenance dan Sampling Audit",
        f"- selected raw dataset: `{sampling_audit['selected_raw_dataset']}`",
        f"- raw dataset exists locally: {sampling_audit['selected_raw_dataset_exists']}",
        "- dataset status: secondary dataset",
        "- source provenance status: needs citation/source URL/license from dataset owner",
        f"- final labeled dataset: `{sampling_audit['final_labeled_dataset']}`",
        f"- final labeled rows: {dataset_summary['rows']}",
        "- label distribution:",
    ]
    for label, count in dataset_summary["label_distribution"].items():
        percent = dataset_summary["label_percentage"][label]
        lines.append(f"  - {label}: {count} ({percent:.2f}%)")

    lines.extend(
        [
            "",
            "### Metadata Sampling",
            f"- available metadata columns: {sampling_audit['available_metadata_columns']}",
            f"- sample_id unique: {sampling_audit['sample_id_unique']}",
            f"- source_row_number exists: {sampling_audit['source_row_number_exists']}",
            f"- source_row_number min/max: {sampling_audit['source_row_number_min']} / {sampling_audit['source_row_number_max']}",
            f"- sampling reproducible from existing columns: {sampling_audit['sampling_reproducible_from_existing_columns']}",
            f"- random_state detected in docs: {sampling_audit['random_state_detected_in_docs']}",
            f"- sampling strategy detected in docs: {sampling_audit['sampling_strategy_detected_in_docs']}",
            f"- limitation: {sampling_audit['manual_provenance_limitation']}",
            "",
            "Interpretasi: dataset harus ditulis sebagai dataset sekunder. Detail identitas crawler asli, rentang tanggal crawl, keyword, URL sumber, dan lisensi tidak boleh diinventarisasi secara fiktif; bagian tersebut perlu dilengkapi manual dari pemilik dataset.",
            "",
            "## 2. Class Weight Ablation",
            markdown_table(ablation_df[["model_name", "class_weight", "accuracy", "precision_macro", "recall_macro", "f1_macro", "f1_weighted"]]),
            "",
            ablation_note,
            "",
            "## 3. CV Model Selection Summary",
            markdown_table(cv_df[["model_name", "cv_mean_macro_f1", "cv_std_macro_f1", "test_macro_f1", "notes"]]),
            "",
            cv_warning,
            "",
            "Rekomendasi wording: gunakan frasa `model terpilih berdasarkan macro F1 pada eksperimen ini`, bukan `model terbaik secara universal`.",
            "",
            "## 4. Near-Duplicate Train/Test Leakage Check",
            f"- test rows checked: {near_dup_summary['test_rows_checked']}",
            f"- threshold: TF-IDF cosine similarity >= {near_dup_summary['near_duplicate_threshold']}",
            f"- near-duplicate test rows: {near_dup_summary['near_duplicate_rows']}",
            f"- percentage: {near_dup_summary['near_duplicate_percentage']:.2f}%",
            "",
            "Interpretasi: pemeriksaan ini mendeteksi kemiripan berbasis TF-IDF cosine similarity, bukan deteksi duplikasi semantik sempurna. Jika ditemukan near-duplicate, bahas sebagai potensi leakage atau risiko evaluasi yang terlalu optimistis.",
            "",
            "## 5. Negative-Class Error Analysis Candidates",
            f"- best_svm_model.joblib available: {negative_summary['model_available']}",
            f"- negative test rows: {negative_summary['negative_test_rows']}",
            f"- negative correct: {negative_summary['negative_correct']}",
            f"- negative errors: {negative_summary['negative_errors']}",
            "",
            "Kategori review manual yang direkomendasikan:",
            "- sarkasme",
            "- kritik implisit",
            "- negasi",
            "- campuran",
            "- konteks kurang",
            "- label noisy",
            "- model miss",
            "",
            "## 6. Labeling/Codebook Documentation",
            f"Codebook dibuat/diupdate di `{CODEBOOK_PATH}`. Dokumen tersebut menegaskan scope sentimen terhadap Program MBG, definisi label, decision rules, workflow AI-assisted labeling, adjudication/manual review, dan rencana validasi gold-label.",
            "",
            "## 7. Kesimpulan Hardening",
        ]
    )
    if baseline_linear_f1 is not None and tuned_linear_f1 is not None:
        lines.append(
            f"Tuned LinearSVC tetap dapat diposisikan sebagai model final terpilih, "
            f"dengan baseline Linear SVM macro F1 {baseline_linear_f1:.4f} dan "
            f"Tuned LinearSVC macro F1 {tuned_linear_f1:.4f}. Namun, kesimpulan harus "
            "menyebut keterbatasan provenance dataset sekunder, label AI-assisted, class imbalance, "
            "near-duplicate risk, dan belum adanya gold validation independen."
        )
    else:
        lines.append(
            "Model final dapat dibahas secara hati-hati berdasarkan output yang tersedia, dengan batasan metodologis yang dijelaskan di atas."
        )
    HARDENING_REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def run_checks() -> dict[str, Any]:
    """Run all methodology hardening checks and write outputs."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH)
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    df["clean_text"] = df["clean_text"].fillna("").astype(str).str.strip()
    train_df, test_df = split_dataset(df)

    dataset_summary = validate_dataset(df)
    sampling_audit = audit_sampling_metadata(df)
    ablation_df, ablation_details = run_class_weight_ablation(train_df, test_df)
    cv_df = build_cv_model_selection_summary()
    near_dup_df, near_dup_summary = run_near_duplicate_check(train_df, test_df)
    negative_df, negative_summary = build_negative_error_candidates(test_df)
    final_summary = read_json_if_exists(FINAL_SUMMARY_PATH)

    write_codebook()
    write_rewrite_notes()
    write_hardening_report(
        dataset_summary,
        sampling_audit,
        ablation_df,
        cv_df,
        near_dup_summary,
        negative_summary,
        final_summary,
    )

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dataset_summary": dataset_summary,
        "sampling_audit": sampling_audit,
        "class_weight_ablation": ablation_details,
        "cv_model_selection_rows": int(len(cv_df)),
        "near_duplicate_summary": near_dup_summary,
        "negative_class_error_summary": negative_summary,
        "outputs": {
            "methodology_hardening_report": str(HARDENING_REPORT_PATH),
            "methodology_hardening_summary": str(HARDENING_SUMMARY_PATH),
            "class_weight_ablation_results": str(CLASS_WEIGHT_PATH),
            "cv_model_selection_summary": str(CV_SELECTION_PATH),
            "near_duplicate_train_test_check": str(NEAR_DUP_PATH),
            "negative_class_error_analysis_candidates": str(NEGATIVE_ERROR_PATH),
            "annotation_codebook": str(CODEBOOK_PATH),
            "rewrite_notes": str(REWRITE_NOTES_PATH),
        },
    }
    HARDENING_SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Saved report: {HARDENING_REPORT_PATH}")
    print(f"Saved summary: {HARDENING_SUMMARY_PATH}")
    print(f"Saved class weight ablation: {CLASS_WEIGHT_PATH}")
    print(f"Saved CV selection summary: {CV_SELECTION_PATH}")
    print(f"Saved near-duplicate check: {NEAR_DUP_PATH}")
    print(f"Saved negative-class candidates: {NEGATIVE_ERROR_PATH}")
    print(f"Saved codebook: {CODEBOOK_PATH}")
    print(f"Saved rewrite notes: {REWRITE_NOTES_PATH}")
    return summary


def main() -> None:
    """CLI entrypoint."""
    run_checks()


if __name__ == "__main__":
    main()
