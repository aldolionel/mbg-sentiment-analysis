"""Combine adjudication templates for batches 003 through 020."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


BATCH_IDS = list(range(3, 21))
ALLOWED_LABELS = {"positif", "negatif", "netral"}
REQUIRED_TEMPLATE_COLUMNS = [
    "sample_id",
    "clean_text",
    "current_label",
    "labeling_notes",
    "review_reason",
    "human_label",
    "human_notes",
    "final_label",
]
OUTPUT_COLUMNS = ["batch_id", *REQUIRED_TEMPLATE_COLUMNS]
INPUT_DIR = Path("data/processed/adjudication")
OUTPUT_CSV = INPUT_DIR / "master_adjudication_template_003_020.csv"
OUTPUT_XLSX = INPUT_DIR / "master_adjudication_template_003_020.xlsx"
REPORT_PATH = Path("outputs/reports/10_master_adjudication_template_003_020.md")
SUMMARY_PATH = Path(
    "outputs/reports/10_master_adjudication_template_003_020_summary.json"
)


def batch_tag(batch_id: int | str) -> str:
    """Normalize a batch identifier to a three-digit string.

    Args:
        batch_id: Batch number or string.

    Returns:
        Three-digit batch identifier.
    """
    return str(batch_id).strip().zfill(3)


def template_path(batch_id: int | str) -> Path:
    """Return the XLSX adjudication template path for a batch.

    Args:
        batch_id: Batch number or string.

    Returns:
        Expected XLSX template path.
    """
    tag = batch_tag(batch_id)
    return INPUT_DIR / f"annotation_batch_{tag}_adjudication_template.xlsx"


def load_template(batch_id: int | str) -> pd.DataFrame:
    """Load one adjudication template and add its batch id.

    Args:
        batch_id: Batch number or string.

    Returns:
        Template DataFrame with a `batch_id` column.

    Raises:
        FileNotFoundError: If the template file is missing.
        ValueError: If required columns are missing.
    """
    path = template_path(batch_id)
    if not path.exists():
        raise FileNotFoundError(f"Adjudication template not found: {path}")

    df = pd.read_excel(path)
    missing = [col for col in REQUIRED_TEMPLATE_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")

    out = df.loc[:, REQUIRED_TEMPLATE_COLUMNS].copy()
    out.insert(0, "batch_id", batch_tag(batch_id))
    out["sample_id"] = out["sample_id"].fillna("").astype(str).str.strip()
    out["current_label"] = (
        out["current_label"].fillna("").astype(str).str.strip().str.lower()
    )
    return out.loc[:, OUTPUT_COLUMNS]


def combine_templates(batch_ids: list[int]) -> tuple[pd.DataFrame, dict[str, int]]:
    """Combine adjudication templates for the requested batches.

    Args:
        batch_ids: Batch numbers to combine.

    Returns:
        A tuple of combined DataFrame and per-batch row counts.
    """
    frames = []
    rows_per_batch: dict[str, int] = {}
    for batch_id in batch_ids:
        tag = batch_tag(batch_id)
        batch_df = load_template(batch_id)
        frames.append(batch_df)
        rows_per_batch[tag] = int(len(batch_df))

    combined_df = pd.concat(frames, ignore_index=True)
    return combined_df, rows_per_batch


def validate_master(
    combined_df: pd.DataFrame,
    rows_per_batch: dict[str, int],
) -> dict[str, bool]:
    """Validate the combined adjudication template.

    Args:
        combined_df: Combined adjudication template DataFrame.
        rows_per_batch: Per-batch row counts.

    Returns:
        Validation check names mapped to boolean results.
    """
    expected_total = sum(rows_per_batch.values())
    batch_ids = combined_df["batch_id"].fillna("").astype(str).str.strip()
    sample_ids = combined_df["sample_id"].fillna("").astype(str).str.strip()
    current_labels = combined_df["current_label"].fillna("").astype(str)

    checks = {
        "total rows equals sum of all template rows": len(combined_df)
        == expected_total,
        "no missing batch_id": batch_ids.ne("").all(),
        "no missing sample_id": sample_ids.ne("").all(),
        "no duplicate batch_id + sample_id pairs": not combined_df.duplicated(
            subset=["batch_id", "sample_id"]
        ).any(),
        "current_label values are allowed labels": set(current_labels).issubset(
            ALLOWED_LABELS
        ),
    }
    return {name: bool(passed) for name, passed in checks.items()}


def write_master_outputs(combined_df: pd.DataFrame) -> None:
    """Write master CSV and XLSX outputs.

    Args:
        combined_df: Combined adjudication template DataFrame.
    """
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_XLSX.parent.mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    combined_df.to_excel(OUTPUT_XLSX, index=False)


def build_summary(
    combined_df: pd.DataFrame,
    rows_per_batch: dict[str, int],
    checks: dict[str, bool],
) -> dict[str, Any]:
    """Build JSON-serializable summary data.

    Args:
        combined_df: Combined adjudication template DataFrame.
        rows_per_batch: Per-batch row counts.
        checks: Validation check results.

    Returns:
        Summary dictionary.
    """
    label_counts = combined_df["current_label"].value_counts().to_dict()
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "batch_range": "003-020",
        "input_files": [str(template_path(batch_id)) for batch_id in BATCH_IDS],
        "output_files": {
            "csv": str(OUTPUT_CSV),
            "xlsx": str(OUTPUT_XLSX),
            "report": str(REPORT_PATH),
            "summary_json": str(SUMMARY_PATH),
        },
        "total_rows": int(len(combined_df)),
        "rows_per_batch": rows_per_batch,
        "current_label_distribution": {
            str(label): int(count) for label, count in label_counts.items()
        },
        "validation_checks": checks,
        "all_validation_checks_passed": all(checks.values()),
    }


def write_report(summary: dict[str, Any]) -> None:
    """Write Markdown report for the master adjudication template.

    Args:
        summary: Summary dictionary produced by `build_summary`.
    """
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows_per_batch = summary["rows_per_batch"]
    label_counts = summary["current_label_distribution"]
    checks = summary["validation_checks"]

    lines = [
        "# 10 Master Adjudication Template 003-020",
        "",
        "## Summary",
        f"- total rows: {summary['total_rows']}",
        "- batch range: 003-020",
        "",
        "## Rows Per Batch",
    ]
    lines.extend(
        [f"- batch {batch_id}: {count}" for batch_id, count in rows_per_batch.items()]
    )
    lines.extend(["", "## Current Label Distribution"])
    if label_counts:
        lines.extend([f"- {label}: {count}" for label, count in label_counts.items()])
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Output File Paths",
            f"- CSV: `{OUTPUT_CSV}`",
            f"- XLSX: `{OUTPUT_XLSX}`",
            f"- report: `{REPORT_PATH}`",
            f"- summary JSON: `{SUMMARY_PATH}`",
            "",
            "## Validation Checks",
        ]
    )
    lines.extend(
        [f"- {'PASS' if passed else 'FAIL'}: {name}" for name, passed in checks.items()]
    )
    lines.extend(
        [
            "",
            "## Reviewer Instruction",
            "Fill only `human_label`, `human_notes`, and `final_label`.",
            "Allowed labels are:",
            "- `positif`",
            "- `negatif`",
            "- `netral`",
            "",
            "Do not change `batch_id`, `sample_id`, `clean_text`, "
            "`current_label`, `labeling_notes`, or `review_reason`.",
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
    """Combine adjudication templates, validate, and write artifacts."""
    combined_df, rows_per_batch = combine_templates(BATCH_IDS)
    checks = validate_master(combined_df, rows_per_batch)
    summary = build_summary(combined_df, rows_per_batch, checks)

    write_master_outputs(combined_df)
    write_report(summary)
    write_summary(summary)

    print(f"Master CSV saved to: {OUTPUT_CSV}")
    print(f"Master XLSX saved to: {OUTPUT_XLSX}")
    print(f"Report saved to: {REPORT_PATH}")
    print(f"Summary JSON saved to: {SUMMARY_PATH}")
    print(f"Total rows: {len(combined_df)}")
    print(f"Validation: {'PASS' if all(checks.values()) else 'FAIL'}")

    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
