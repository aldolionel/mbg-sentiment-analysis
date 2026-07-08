"""Combine final adjudicated annotation batches into one labeled dataset."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


BATCH_IDS = [f"{batch_id:03d}" for batch_id in range(1, 21)]
ALLOWED_LABELS = {"positif", "negatif", "netral"}
EXPECTED_ROWS_PER_BATCH = 50
EXPECTED_TOTAL_ROWS = 1000
OUTPUT_COLUMNS = [
    "batch_id",
    "sample_id",
    "clean_text",
    "label",
    "label_before_adjudication",
    "label_after_adjudication",
    "adjudication_applied",
    "human_label",
    "human_notes",
    "adjudication_review_reason",
]
OUTPUT_CSV = Path("data/processed/mbg_labeled_sample_1000.csv")
OUTPUT_XLSX = Path("data/processed/mbg_labeled_sample_1000.xlsx")
REPORT_PATH = Path("outputs/reports/13_labeled_dataset_1000_report.md")
SUMMARY_PATH = Path("outputs/reports/13_labeled_dataset_1000_summary.json")


def adjudicated_path(batch_id: str) -> Path:
    """Return finalized adjudicated batch path.

    Args:
        batch_id: Three-digit batch id.

    Returns:
        Adjudicated CSV path.
    """
    return Path(
        f"data/processed/annotation_labeled_batches/"
        f"annotation_batch_{batch_id}_adjudicated.csv"
    )


def annotation_batch_path(batch_id: str) -> Path:
    """Return original annotation batch path for clean text fallback.

    Args:
        batch_id: Three-digit batch id.

    Returns:
        Original annotation batch CSV path.
    """
    return Path(f"data/processed/annotation_batches/annotation_batch_{batch_id}.csv")


def safe_text(value: object) -> str:
    """Convert a value to a stripped string, preserving missing as empty.

    Args:
        value: Raw value.

    Returns:
        Clean string value.
    """
    if pd.isna(value):
        return ""
    return str(value).strip()


def normalize_label(value: object) -> str:
    """Normalize a sentiment label.

    Args:
        value: Raw label value.

    Returns:
        Lowercase stripped label.
    """
    return safe_text(value).lower()


def normalize_bool(value: object) -> bool:
    """Normalize boolean-like adjudication flags.

    Args:
        value: Raw value.

    Returns:
        Boolean flag.
    """
    if isinstance(value, bool):
        return value
    if pd.isna(value):
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "ya"}


def load_clean_text_fallback(batch_id: str) -> pd.DataFrame:
    """Load clean text fallback for a batch.

    Args:
        batch_id: Three-digit batch id.

    Returns:
        DataFrame with sample_id and clean_text.

    Raises:
        FileNotFoundError: If fallback batch is missing.
        ValueError: If fallback batch lacks required columns.
    """
    path = annotation_batch_path(batch_id)
    if not path.exists():
        raise FileNotFoundError(f"Clean text fallback file not found: {path}")

    fallback_df = pd.read_csv(path)
    missing = [col for col in ["sample_id", "clean_text"] if col not in fallback_df.columns]
    if missing:
        raise ValueError(f"Missing fallback columns in {path}: {missing}")
    return fallback_df.loc[:, ["sample_id", "clean_text"]].copy()


def load_final_batch(batch_id: str) -> pd.DataFrame:
    """Load and standardize one finalized adjudicated batch.

    Args:
        batch_id: Three-digit batch id.

    Returns:
        Standardized batch DataFrame.

    Raises:
        FileNotFoundError: If finalized batch is missing.
        ValueError: If required columns are missing.
    """
    path = adjudicated_path(batch_id)
    if not path.exists():
        raise FileNotFoundError(f"Final adjudicated batch not found: {path}")

    df = pd.read_csv(path)
    required = ["sample_id", "label"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in {path}: {missing}")

    if "clean_text" not in df.columns:
        fallback_df = load_clean_text_fallback(batch_id)
        df = df.merge(fallback_df, on="sample_id", how="left")

    if "clean_text" not in df.columns:
        raise ValueError(f"Unable to provide clean_text for batch {batch_id}")

    out = pd.DataFrame()
    out["sample_id"] = df["sample_id"].apply(safe_text)
    out["batch_id"] = batch_id
    out["clean_text"] = df["clean_text"].apply(safe_text)
    out["label"] = df["label"].apply(normalize_label)
    out["label_before_adjudication"] = (
        df["label_before_adjudication"].apply(normalize_label)
        if "label_before_adjudication" in df.columns
        else out["label"]
    )
    out["label_after_adjudication"] = (
        df["label_after_adjudication"].apply(normalize_label)
        if "label_after_adjudication" in df.columns
        else out["label"]
    )
    out["adjudication_applied"] = (
        df["adjudication_applied"].apply(normalize_bool)
        if "adjudication_applied" in df.columns
        else False
    )
    out["human_label"] = (
        df["human_label"].apply(normalize_label) if "human_label" in df.columns else ""
    )
    out["human_notes"] = (
        df["human_notes"].apply(safe_text) if "human_notes" in df.columns else ""
    )
    out["adjudication_review_reason"] = (
        df["adjudication_review_reason"].apply(safe_text)
        if "adjudication_review_reason" in df.columns
        else ""
    )
    return out.loc[:, OUTPUT_COLUMNS]


def combine_batches() -> pd.DataFrame:
    """Load and combine finalized batches 001 through 020.

    Returns:
        Combined labeled dataset.
    """
    frames = [load_final_batch(batch_id) for batch_id in BATCH_IDS]
    return pd.concat(frames, ignore_index=True)


def validate_dataset(df: pd.DataFrame, rows_per_batch: dict[str, int]) -> dict[str, bool]:
    """Validate the combined labeled dataset.

    Args:
        df: Combined labeled dataset.
        rows_per_batch: Row counts by batch.

    Returns:
        Validation check results.
    """
    batch_ids = df["batch_id"].fillna("").astype(str).str.strip()
    sample_ids = df["sample_id"].fillna("").astype(str).str.strip()
    clean_text = df["clean_text"].fillna("").astype(str).str.strip()
    labels = df["label"].fillna("").astype(str)
    checks = {
        "all 20 finalized batch files exist": all(
            adjudicated_path(batch_id).exists() for batch_id in BATCH_IDS
        ),
        "each batch has 50 rows": all(
            count == EXPECTED_ROWS_PER_BATCH for count in rows_per_batch.values()
        ),
        "total rows equals 1000": len(df) == EXPECTED_TOTAL_ROWS,
        "no missing batch_id": batch_ids.ne("").all(),
        "no duplicate sample_id": not sample_ids.duplicated().any(),
        "no missing clean_text": clean_text.ne("").all(),
        "no missing label": labels.str.strip().ne("").all(),
        "labels are allowed values": set(labels).issubset(ALLOWED_LABELS),
    }
    return {name: bool(passed) for name, passed in checks.items()}


def build_summary(df: pd.DataFrame, checks: dict[str, bool]) -> dict[str, Any]:
    """Build JSON summary for the labeled dataset.

    Args:
        df: Combined labeled dataset.
        checks: Validation check results.

    Returns:
        Summary dictionary.
    """
    rows_per_batch = df["batch_id"].value_counts().sort_index()
    label_counts = df["label"].value_counts().sort_index()
    label_percentages = (label_counts / len(df) * 100).round(2)
    changed_mask = df["label_before_adjudication"] != df["label_after_adjudication"]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_rows": int(len(df)),
        "rows_per_batch": {
            str(batch_id): int(count) for batch_id, count in rows_per_batch.items()
        },
        "label_distribution": {
            str(label): int(count) for label, count in label_counts.items()
        },
        "label_distribution_percentage": {
            str(label): float(percent)
            for label, percent in label_percentages.items()
        },
        "adjudication_applied_count": int(df["adjudication_applied"].sum()),
        "changed_label_count": int(changed_mask.sum()),
        "validation_checks": checks,
        "all_validation_checks_passed": all(checks.values()),
        "output_files": {
            "csv": str(OUTPUT_CSV),
            "xlsx": str(OUTPUT_XLSX),
            "report": str(REPORT_PATH),
            "summary_json": str(SUMMARY_PATH),
        },
    }


def write_outputs(df: pd.DataFrame) -> None:
    """Write combined labeled dataset outputs.

    Args:
        df: Combined labeled dataset.
    """
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    df.to_excel(OUTPUT_XLSX, index=False)


def write_report(summary: dict[str, Any]) -> None:
    """Write Markdown report for the labeled dataset.

    Args:
        summary: Summary dictionary.
    """
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 13 Labeled Dataset 1000 Report",
        "",
        "## Scope",
        "Dataset ini menggabungkan batch final/adjudicated 001 sampai 020 "
        "sebagai sampel berlabel untuk persiapan modeling sentimen MBG pada media sosial.",
        "Tidak ada training model, SMOTE, modifikasi raw data, atau pelabelan ulang otomatis.",
        "",
        "## Input Batch Files",
    ]
    lines.extend([f"- `{adjudicated_path(batch_id)}`" for batch_id in BATCH_IDS])

    lines.extend(
        [
            "",
            "## Row Summary",
            f"- total rows: {summary['total_rows']}",
            "",
            "## Rows Per Batch",
        ]
    )
    lines.extend(
        [
            f"- batch {batch_id}: {count}"
            for batch_id, count in summary["rows_per_batch"].items()
        ]
    )

    lines.extend(["", "## Final Label Distribution"])
    for label, count in summary["label_distribution"].items():
        percent = summary["label_distribution_percentage"][label]
        lines.append(f"- {label}: {count} ({percent:.2f}%)")

    lines.extend(
        [
            "",
            "## Adjudication Summary",
            f"- adjudication applied count: {summary['adjudication_applied_count']}",
            f"- changed label count: {summary['changed_label_count']}",
            "",
            "## Validation Checks",
        ]
    )
    lines.extend(
        [
            f"- {'PASS' if passed else 'FAIL'}: {name}"
            for name, passed in summary["validation_checks"].items()
        ]
    )
    lines.extend(
        [
            "",
            "## Output File Paths",
            f"- CSV: `{OUTPUT_CSV}`",
            f"- XLSX: `{OUTPUT_XLSX}`",
            f"- report: `{REPORT_PATH}`",
            f"- summary JSON: `{SUMMARY_PATH}`",
            "",
            "## Recommendation",
            "Dataset siap untuk tahap persiapan modeling. Pada penulisan tesis, "
            "label sebaiknya dijelaskan sebagai hasil AI-assisted labeling "
            "dengan proses adjudication/manual review.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_summary(summary: dict[str, Any]) -> None:
    """Write JSON summary file.

    Args:
        summary: Summary dictionary.
    """
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def main() -> None:
    """Combine final labeled batches and write modeling preparation dataset."""
    combined_df = combine_batches()
    rows_per_batch = {
        batch_id: int((combined_df["batch_id"] == batch_id).sum())
        for batch_id in BATCH_IDS
    }
    checks = validate_dataset(combined_df, rows_per_batch)
    summary = build_summary(combined_df, checks)

    write_outputs(combined_df)
    write_report(summary)
    write_summary(summary)

    print(f"Labeled CSV saved to: {OUTPUT_CSV}")
    print(f"Labeled XLSX saved to: {OUTPUT_XLSX}")
    print(f"Report saved to: {REPORT_PATH}")
    print(f"Summary JSON saved to: {SUMMARY_PATH}")
    print(f"Total rows: {len(combined_df)}")
    print(f"Validation: {'PASS' if all(checks.values()) else 'FAIL'}")

    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
