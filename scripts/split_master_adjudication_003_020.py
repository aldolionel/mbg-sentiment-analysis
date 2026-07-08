"""Split reviewed master adjudication workbook back into batch templates."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


BATCH_IDS = [f"{batch_id:03d}" for batch_id in range(3, 21)]
ALLOWED_LABELS = {"positif", "negatif", "netral"}
EXPECTED_TOTAL_ROWS = 104
INPUT_PATH = Path(
    "data/processed/adjudication/master_adjudication_template_003_020_REVIEWED_AI.xlsx"
)
ADJUDICATION_DIR = Path("data/processed/adjudication")
REPORT_PATH = Path("outputs/reports/11_split_master_adjudication_003_020.md")
SUMMARY_PATH = Path(
    "outputs/reports/11_split_master_adjudication_003_020_summary.json"
)
REQUIRED_COLUMNS = [
    "batch_id",
    "sample_id",
    "clean_text",
    "current_label",
    "labeling_notes",
    "review_reason",
    "human_label",
    "human_notes",
    "final_label",
]


def safe_text(value: object) -> str:
    """Convert spreadsheet cell values to clean strings.

    Args:
        value: Raw spreadsheet value.

    Returns:
        Empty string for missing values, otherwise stripped string.
    """
    if pd.isna(value):
        return ""
    return str(value).strip()


def normalize_batch_id(value: object) -> str:
    """Normalize batch ids as three-digit strings.

    Args:
        value: Raw batch id value from spreadsheet.

    Returns:
        Three-digit batch id string, or empty string for missing values.
    """
    text = safe_text(value)
    if not text:
        return ""
    try:
        return f"{int(float(text)):03d}"
    except ValueError:
        return text.zfill(3)


def normalize_label(value: object) -> str:
    """Normalize label values to lowercase strings.

    Args:
        value: Raw label value.

    Returns:
        Lowercase, stripped label value or empty string.
    """
    return safe_text(value).lower()


def template_path(batch_id: str) -> Path:
    """Return the per-batch adjudication template path.

    Args:
        batch_id: Three-digit batch id.

    Returns:
        Existing per-batch adjudication template path.
    """
    return ADJUDICATION_DIR / f"annotation_batch_{batch_id}_adjudication_template.xlsx"


def reviewed_csv_path(batch_id: str) -> Path:
    """Return the reviewed per-batch CSV output path.

    Args:
        batch_id: Three-digit batch id.

    Returns:
        Reviewed CSV path.
    """
    return (
        ADJUDICATION_DIR
        / f"annotation_batch_{batch_id}_adjudication_template_reviewed.csv"
    )


def load_reviewed_master(path: Path = INPUT_PATH) -> pd.DataFrame:
    """Load and normalize the reviewed master adjudication workbook.

    Args:
        path: Reviewed master workbook path.

    Returns:
        Normalized master adjudication DataFrame.

    Raises:
        FileNotFoundError: If the reviewed workbook is missing.
        ValueError: If required columns are missing.
    """
    if not path.exists():
        raise FileNotFoundError(f"Reviewed master workbook not found: {path}")

    df = pd.read_excel(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in reviewed workbook: {missing}")

    out = df.loc[:, REQUIRED_COLUMNS].copy()
    out["batch_id"] = out["batch_id"].apply(normalize_batch_id)
    out["sample_id"] = out["sample_id"].apply(safe_text)
    for col in ["clean_text", "labeling_notes", "review_reason", "human_notes"]:
        out[col] = out[col].apply(safe_text)
    for col in ["current_label", "human_label", "final_label"]:
        out[col] = out[col].apply(normalize_label)
    return out


def load_original_templates() -> dict[str, pd.DataFrame]:
    """Load existing per-batch adjudication templates.

    Returns:
        Mapping of batch id to template DataFrame.

    Raises:
        FileNotFoundError: If any expected template is missing.
        ValueError: If any expected template is missing required columns.
    """
    templates: dict[str, pd.DataFrame] = {}
    template_required = [col for col in REQUIRED_COLUMNS if col != "batch_id"]
    for batch_id in BATCH_IDS:
        path = template_path(batch_id)
        if not path.exists():
            raise FileNotFoundError(f"Per-batch template not found: {path}")

        df = pd.read_excel(path)
        missing = [col for col in template_required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns in {path}: {missing}")

        normalized = df.copy()
        normalized["sample_id"] = normalized["sample_id"].apply(safe_text)
        templates[batch_id] = normalized
    return templates


def label_distribution(df: pd.DataFrame, group_col: str | None = None) -> dict[str, Any]:
    """Compute final label distribution.

    Args:
        df: Adjudication DataFrame.
        group_col: Optional grouping column.

    Returns:
        Label count dictionary.
    """
    if group_col is None:
        counts = df["final_label"].value_counts().sort_index()
        return {str(label): int(count) for label, count in counts.items()}

    distribution: dict[str, dict[str, int]] = {}
    grouped = df.groupby(group_col, sort=True)
    for group_value, group_df in grouped:
        counts = group_df["final_label"].value_counts().sort_index()
        distribution[str(group_value)] = {
            str(label): int(count) for label, count in counts.items()
        }
    return distribution


def validate_split(
    master_df: pd.DataFrame,
    templates: dict[str, pd.DataFrame],
) -> dict[str, bool]:
    """Validate reviewed master workbook against original templates.

    Args:
        master_df: Normalized reviewed master adjudication DataFrame.
        templates: Original per-batch templates.

    Returns:
        Validation check names mapped to booleans.
    """
    batch_ids = master_df["batch_id"].fillna("").astype(str)
    sample_ids = master_df["sample_id"].fillna("").astype(str)
    human_labels = master_df["human_label"].fillna("").astype(str)
    final_labels = master_df["final_label"].fillna("").astype(str)

    checks: dict[str, bool] = {
        "batch_id only from 003 through 020": set(batch_ids).issubset(set(BATCH_IDS)),
        "no missing batch_id": batch_ids.str.strip().ne("").all(),
        "no missing sample_id": sample_ids.str.strip().ne("").all(),
        "no duplicate batch_id + sample_id pairs": not master_df.duplicated(
            subset=["batch_id", "sample_id"]
        ).any(),
        "human_label values are allowed labels": set(human_labels).issubset(
            ALLOWED_LABELS
        ),
        "final_label values are allowed labels": set(final_labels).issubset(
            ALLOWED_LABELS
        ),
        "total rows equals 104": len(master_df) == EXPECTED_TOTAL_ROWS,
    }

    for batch_id in BATCH_IDS:
        reviewed_batch = master_df.loc[master_df["batch_id"] == batch_id]
        template_df = templates[batch_id]
        reviewed_ids = set(reviewed_batch["sample_id"].astype(str))
        template_ids = set(template_df["sample_id"].astype(str))
        checks[f"batch {batch_id} row count matches template"] = len(
            reviewed_batch
        ) == len(template_df)
        checks[f"batch {batch_id} sample_id values exist in template"] = (
            reviewed_ids.issubset(template_ids)
        )

    return {name: bool(passed) for name, passed in checks.items()}


def write_split_outputs(master_df: pd.DataFrame) -> list[str]:
    """Write reviewed rows back to per-batch XLSX and CSV files.

    Args:
        master_df: Normalized reviewed master adjudication DataFrame.

    Returns:
        List of generated output file paths.
    """
    generated_paths: list[str] = []
    ADJUDICATION_DIR.mkdir(parents=True, exist_ok=True)
    for batch_id in BATCH_IDS:
        batch_df = master_df.loc[master_df["batch_id"] == batch_id].copy()
        batch_output = batch_df.drop(columns=["batch_id"])

        xlsx_path = template_path(batch_id)
        csv_path = reviewed_csv_path(batch_id)
        batch_output.to_excel(xlsx_path, index=False)
        batch_output.to_csv(csv_path, index=False, encoding="utf-8")

        generated_paths.extend([str(xlsx_path), str(csv_path)])
    return generated_paths


def build_summary(
    master_df: pd.DataFrame,
    checks: dict[str, bool],
    generated_paths: list[str],
) -> dict[str, Any]:
    """Build summary data for report and JSON output.

    Args:
        master_df: Normalized reviewed master adjudication DataFrame.
        checks: Validation check results.
        generated_paths: Output file paths generated by the split.

    Returns:
        JSON-serializable summary dictionary.
    """
    rows_per_batch = master_df["batch_id"].value_counts().sort_index()
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_file": str(INPUT_PATH),
        "total_rows": int(len(master_df)),
        "rows_per_batch": {
            str(batch_id): int(count) for batch_id, count in rows_per_batch.items()
        },
        "final_label_distribution_overall": label_distribution(master_df),
        "final_label_distribution_per_batch": label_distribution(
            master_df,
            group_col="batch_id",
        ),
        "validation_checks": checks,
        "all_validation_checks_passed": all(checks.values()),
        "output_paths_generated": generated_paths,
    }


def write_report(summary: dict[str, Any]) -> None:
    """Write Markdown report for the split operation.

    Args:
        summary: Split summary dictionary.
    """
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 11 Split Master Adjudication 003-020",
        "",
        "## Input",
        f"- reviewed master workbook: `{summary['input_file']}`",
        "",
        "## Summary",
        f"- total rows: {summary['total_rows']}",
        "",
        "## Rows Per Batch",
    ]
    lines.extend(
        [
            f"- batch {batch_id}: {count}"
            for batch_id, count in summary["rows_per_batch"].items()
        ]
    )

    lines.extend(["", "## Final Label Distribution Overall"])
    lines.extend(
        [
            f"- {label}: {count}"
            for label, count in summary[
                "final_label_distribution_overall"
            ].items()
        ]
    )

    lines.extend(["", "## Final Label Distribution Per Batch"])
    for batch_id, counts in summary["final_label_distribution_per_batch"].items():
        count_text = ", ".join(
            f"{label}: {count}" for label, count in counts.items()
        )
        lines.append(f"- batch {batch_id}: {count_text}")

    lines.extend(["", "## Validation Checks"])
    lines.extend(
        [
            f"- {'PASS' if passed else 'FAIL'}: {name}"
            for name, passed in summary["validation_checks"].items()
        ]
    )

    lines.extend(["", "## Output Paths Generated"])
    lines.extend([f"- `{path}`" for path in summary["output_paths_generated"]])

    lines.extend(
        [
            "",
            "## Recommendation",
            "After successful split, run the adjudication import script for batches "
            "003 through 020.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_summary(summary: dict[str, Any]) -> None:
    """Write JSON summary.

    Args:
        summary: Split summary dictionary.
    """
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def main() -> None:
    """Split reviewed master adjudication workbook into per-batch files."""
    master_df = load_reviewed_master(INPUT_PATH)
    templates = load_original_templates()
    checks = validate_split(master_df, templates)

    generated_paths: list[str] = []
    if all(checks.values()):
        generated_paths = write_split_outputs(master_df)

    summary = build_summary(master_df, checks, generated_paths)
    write_report(summary)
    write_summary(summary)

    print(f"Input reviewed workbook: {INPUT_PATH}")
    print(f"Total rows: {len(master_df)}")
    print(f"Report saved to: {REPORT_PATH}")
    print(f"Summary JSON saved to: {SUMMARY_PATH}")
    print(f"Validation: {'PASS' if all(checks.values()) else 'FAIL'}")

    if generated_paths:
        print(f"Generated output files: {len(generated_paths)}")

    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
