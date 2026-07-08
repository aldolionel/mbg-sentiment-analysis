"""Import, normalize, and merge batch 001 adjudication results."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


ALLOWED_LABELS = {"positif", "negatif", "netral"}
ORIGINAL_LABELED_PATH = Path(
    "data/processed/annotation_labeled_batches/annotation_batch_001_labeled.csv"
)
SEMANTIC_REVIEW_PATH = Path(
    "data/processed/annotation_reviews/annotation_batch_001_semantic_review.csv"
)
ADJUDICATION_XLSX_PATH = Path(
    "data/processed/adjudication/annotation_batch_001_adjudication_template.xlsx"
)
ADJUDICATED_OUTPUT_PATH = Path(
    "data/processed/annotation_labeled_batches/annotation_batch_001_adjudicated.csv"
)
NORMALIZED_ADJUDICATION_PATH = Path(
    "data/processed/adjudication/annotation_batch_001_adjudication_normalized.csv"
)
REPORT_PATH = Path("outputs/reports/07_adjudication_batch_001_report.md")
SUMMARY_PATH = Path("outputs/reports/07_adjudication_batch_001_summary.json")
REQUIRED_ADJUDICATION_COLUMNS = [
    "sample_id",
    "clean_text",
    "current_label",
    "labeling_notes",
    "review_reason",
    "human_label",
    "human_notes",
    "final_label",
]


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load original labeled batch, semantic review, and adjudication workbook."""
    for path in [ORIGINAL_LABELED_PATH, SEMANTIC_REVIEW_PATH, ADJUDICATION_XLSX_PATH]:
        if not path.exists():
            raise FileNotFoundError(f"Required input file not found: {path}")

    original_df = pd.read_csv(ORIGINAL_LABELED_PATH)
    semantic_df = pd.read_csv(SEMANTIC_REVIEW_PATH)
    adjudication_df = pd.read_excel(ADJUDICATION_XLSX_PATH)
    return original_df, semantic_df, adjudication_df


def normalize_label_value(value: object) -> str:
    """Normalize a label-like value.

    Args:
        value: Raw cell value.

    Returns:
        Lowercase stripped label text, or an empty string for missing values.
    """
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def validate_adjudication_columns(adjudication_df: pd.DataFrame) -> None:
    """Validate required adjudication workbook columns."""
    missing_columns = [
        column
        for column in REQUIRED_ADJUDICATION_COLUMNS
        if column not in adjudication_df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing adjudication columns: {missing_columns}")


def normalize_adjudication(
    adjudication_df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Normalize adjudication labels using deterministic final-label rules."""
    validate_adjudication_columns(adjudication_df)
    normalized_df = adjudication_df.copy()

    for column in ["current_label", "human_label", "final_label"]:
        normalized_df[f"{column}_normalized"] = normalized_df[column].apply(
            normalize_label_value
        )
    normalized_df["human_notes"] = normalized_df["human_notes"].fillna("").astype(str)
    normalized_df["review_reason"] = (
        normalized_df["review_reason"].fillna("").astype(str)
    )

    source_counts = {
        "human_label_valid_used": 0,
        "final_label_valid_used": 0,
        "fallback_to_current_label": 0,
    }
    final_labels: list[str] = []
    final_sources: list[str] = []

    for _, row in normalized_df.iterrows():
        human_label = row["human_label_normalized"]
        final_label = row["final_label_normalized"]
        current_label = row["current_label_normalized"]

        if human_label in ALLOWED_LABELS:
            final_labels.append(human_label)
            final_sources.append("human_label")
            source_counts["human_label_valid_used"] += 1
        elif final_label in ALLOWED_LABELS:
            final_labels.append(final_label)
            final_sources.append("final_label")
            source_counts["final_label_valid_used"] += 1
        else:
            final_labels.append(current_label)
            final_sources.append("current_label")
            source_counts["fallback_to_current_label"] += 1

    normalized_df["final_label_normalized"] = final_labels
    normalized_df["final_label_source"] = final_sources
    return normalized_df, source_counts


def validate_normalized_adjudication(
    original_df: pd.DataFrame,
    semantic_df: pd.DataFrame,
    normalized_df: pd.DataFrame,
) -> dict[str, bool]:
    """Run validation checks for normalized adjudication."""
    original_ids = set(original_df["sample_id"].astype(str))
    semantic_ids = set(semantic_df["sample_id"].astype(str))
    adjudication_ids = normalized_df["sample_id"].astype(str)
    final_labels = normalized_df["final_label_normalized"].fillna("").astype(str)

    return {
        "final labels are allowed values": set(final_labels).issubset(ALLOWED_LABELS),
        "no missing final labels": final_labels.str.strip().ne("").all(),
        "no duplicate sample_id in adjudication": not adjudication_ids.duplicated().any(),
        "all adjudication sample_id values exist in original labeled batch": set(
            adjudication_ids
        ).issubset(original_ids),
        "all adjudication sample_id values exist in semantic review": set(
            adjudication_ids
        ).issubset(semantic_ids),
    }


def merge_adjudication(
    original_df: pd.DataFrame,
    semantic_df: pd.DataFrame,
    normalized_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merge normalized adjudication labels into full batch 001."""
    adjudication_columns = [
        "sample_id",
        "final_label_normalized",
        "human_label_normalized",
        "human_notes",
        "review_reason",
    ]
    lookup_df = normalized_df.loc[:, adjudication_columns].copy()
    text_lookup_df = semantic_df.loc[:, ["sample_id", "clean_text"]].copy()
    merged_df = original_df.copy()
    merged_df["label_before_adjudication"] = merged_df["label"]
    if "clean_text" not in merged_df.columns:
        merged_df = merged_df.merge(text_lookup_df, on="sample_id", how="left")
    merged_df = merged_df.merge(lookup_df, on="sample_id", how="left")
    merged_df["adjudication_applied"] = merged_df["final_label_normalized"].notna()
    merged_df["label_after_adjudication"] = merged_df["label"]
    mask = merged_df["adjudication_applied"]
    merged_df.loc[mask, "label_after_adjudication"] = merged_df.loc[
        mask,
        "final_label_normalized",
    ]
    merged_df["label"] = merged_df["label_after_adjudication"]
    merged_df["human_label"] = merged_df["human_label_normalized"].fillna("")
    merged_df["human_notes"] = merged_df["human_notes"].fillna("")
    merged_df["adjudication_review_reason"] = merged_df["review_reason"].fillna("")
    merged_df = merged_df.drop(
        columns=[
            "final_label_normalized",
            "human_label_normalized",
            "review_reason",
        ]
    )
    return merged_df


def build_summary(
    original_df: pd.DataFrame,
    normalized_df: pd.DataFrame,
    adjudicated_df: pd.DataFrame,
    source_counts: dict[str, int],
    checks: dict[str, bool],
) -> dict[str, Any]:
    """Build JSON-serializable adjudication summary."""
    before_counts = (
        original_df["label"].fillna("").astype(str).value_counts().to_dict()
    )
    after_counts = (
        adjudicated_df["label"].fillna("").astype(str).value_counts().to_dict()
    )
    changed_mask = (
        adjudicated_df["label_before_adjudication"]
        != adjudicated_df["label_after_adjudication"]
    )
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_files": {
            "original_labeled_batch": str(ORIGINAL_LABELED_PATH),
            "semantic_review": str(SEMANTIC_REVIEW_PATH),
            "adjudication_xlsx": str(ADJUDICATION_XLSX_PATH),
        },
        "output_files": {
            "adjudicated_batch": str(ADJUDICATED_OUTPUT_PATH),
            "normalized_adjudication": str(NORMALIZED_ADJUDICATION_PATH),
            "markdown_report": str(REPORT_PATH),
        },
        "original_rows": int(len(original_df)),
        "adjudication_rows": int(len(normalized_df)),
        "adjudicated_rows": int(len(adjudicated_df)),
        "human_label_valid_used": int(source_counts["human_label_valid_used"]),
        "final_label_valid_used": int(source_counts["final_label_valid_used"]),
        "fallback_to_current_label": int(source_counts["fallback_to_current_label"]),
        "changed_label_rows": int(changed_mask.sum()),
        "label_distribution_before": {
            str(label): int(count) for label, count in before_counts.items()
        },
        "label_distribution_after": {
            str(label): int(count) for label, count in after_counts.items()
        },
        "validation_checks": {
            str(name): bool(status) for name, status in checks.items()
        },
        "all_checks_passed": bool(all(checks.values())),
    }


def write_report(
    summary: dict[str, Any],
    adjudicated_df: pd.DataFrame,
) -> None:
    """Write Markdown adjudication import report."""
    changed_df = adjudicated_df[
        adjudicated_df["label_before_adjudication"]
        != adjudicated_df["label_after_adjudication"]
    ].copy()
    pass_fail = lambda status: "PASS" if status else "FAIL"

    lines = [
        "# 07 Adjudication Batch 001 Report",
        "",
        "## Input Files",
        f"- original labeled batch: `{ORIGINAL_LABELED_PATH}`",
        f"- semantic review CSV: `{SEMANTIC_REVIEW_PATH}`",
        f"- adjudication XLSX: `{ADJUDICATION_XLSX_PATH}`",
        "",
        "## Output Files",
        f"- adjudicated batch CSV: `{ADJUDICATED_OUTPUT_PATH}`",
        f"- normalized adjudication CSV: `{NORMALIZED_ADJUDICATION_PATH}`",
        f"- summary JSON: `{SUMMARY_PATH}`",
        "",
        "## Row Counts",
        f"- original labeled rows: {summary['original_rows']}",
        f"- adjudication rows: {summary['adjudication_rows']}",
        f"- adjudicated rows: {summary['adjudicated_rows']}",
        "",
        "## Final Label Source Counts",
        f"- human_label valid and used: {summary['human_label_valid_used']}",
        f"- final_label valid and used: {summary['final_label_valid_used']}",
        f"- fallback to current_label: {summary['fallback_to_current_label']}",
        "",
        "## Label Distribution Before Adjudication",
    ]
    lines.extend(
        [
            f"- {label}: {count}"
            for label, count in summary["label_distribution_before"].items()
        ]
    )
    lines.append("")
    lines.append("## Label Distribution After Adjudication")
    lines.extend(
        [
            f"- {label}: {count}"
            for label, count in summary["label_distribution_after"].items()
        ]
    )
    lines.extend(
        [
            "",
            "## Changed Label Rows",
        ]
    )
    if changed_df.empty:
        lines.append("- none")
    else:
        lines.extend(
            [
                "| sample_id | clean_text | label_before_adjudication | label_after_adjudication | human_label | human_notes |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for _, row in changed_df.iterrows():
            clean_text = _markdown_cell(row.get("clean_text", ""))
            human_notes = _markdown_cell(row.get("human_notes", ""))
            lines.append(
                f"| {row['sample_id']} | {clean_text} | "
                f"{row['label_before_adjudication']} | "
                f"{row['label_after_adjudication']} | "
                f"{row['human_label']} | {human_notes} |"
            )

    lines.extend(
        [
            "",
            "## Validation Checks",
        ]
    )
    lines.extend(
        [
            f"- {pass_fail(status)}: {name}"
            for name, status in summary["validation_checks"].items()
        ]
    )
    recommendation = (
        "Batch 001 is ready to be included in the labeled dataset after "
        "researcher review of the changed rows."
        if summary["all_checks_passed"]
        else "Batch 001 is not ready; fix failed validation checks first."
    )
    lines.extend(
        [
            "",
            "## Recommendation",
            f"- {recommendation}",
            "- Do not proceed to model training until the full labeled dataset and validation protocol are complete.",
        ]
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def _markdown_cell(value: object) -> str:
    """Escape a value for a Markdown table cell."""
    if pd.isna(value):
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def main() -> None:
    """Import adjudication, normalize labels, merge, and write reports."""
    original_df, semantic_df, adjudication_df = load_inputs()
    normalized_df, source_counts = normalize_adjudication(adjudication_df)
    checks = validate_normalized_adjudication(original_df, semantic_df, normalized_df)
    if not all(checks.values()):
        print("WARNING: validation checks failed; outputs will still document issues.")

    adjudicated_df = merge_adjudication(original_df, semantic_df, normalized_df)
    summary = build_summary(
        original_df=original_df,
        normalized_df=normalized_df,
        adjudicated_df=adjudicated_df,
        source_counts=source_counts,
        checks=checks,
    )

    ADJUDICATED_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    NORMALIZED_ADJUDICATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    adjudicated_df.to_csv(ADJUDICATED_OUTPUT_PATH, index=False, encoding="utf-8")
    normalized_df.to_csv(
        NORMALIZED_ADJUDICATION_PATH,
        index=False,
        encoding="utf-8",
    )
    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_report(summary, adjudicated_df)

    print(f"Adjudicated batch saved to: {ADJUDICATED_OUTPUT_PATH}")
    print(f"Normalized adjudication saved to: {NORMALIZED_ADJUDICATION_PATH}")
    print(f"Report saved to: {REPORT_PATH}")
    print(f"Summary saved to: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
