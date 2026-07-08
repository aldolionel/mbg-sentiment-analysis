"""Create a manual adjudication template for pilot review rows."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


SEMANTIC_REVIEW_PATH = Path(
    "data/processed/annotation_reviews/annotation_batch_001_semantic_review.csv"
)
OUTPUT_DIR = Path("data/processed/adjudication")
OUTPUT_CSV = OUTPUT_DIR / "annotation_batch_001_adjudication_template.csv"
OUTPUT_XLSX = OUTPUT_DIR / "annotation_batch_001_adjudication_template.xlsx"
REPORT_PATH = Path("outputs/reports/06_adjudication_template_batch_001.md")
OUTPUT_COLUMNS = [
    "sample_id",
    "clean_text",
    "current_label",
    "labeling_notes",
    "review_reason",
    "human_label",
    "human_notes",
    "final_label",
]
ALLOWED_LABELS = ["positif", "negatif", "netral"]


def batch_tag(batch_id: str | int) -> str:
    """Normalize a batch id to three digits."""
    return str(batch_id).strip().zfill(3)


def paths_for_batch(batch_id: str | int) -> dict[str, Path]:
    """Return default adjudication template paths for a batch id."""
    tag = batch_tag(batch_id)
    return {
        "semantic": Path(
            f"data/processed/annotation_reviews/annotation_batch_{tag}_semantic_review.csv"
        ),
        "csv": Path(
            f"data/processed/adjudication/annotation_batch_{tag}_adjudication_template.csv"
        ),
        "xlsx": Path(
            f"data/processed/adjudication/annotation_batch_{tag}_adjudication_template.xlsx"
        ),
        "report": Path(f"outputs/reports/06_adjudication_template_batch_{tag}.md"),
    }


def load_semantic_review(path: str | Path = SEMANTIC_REVIEW_PATH) -> pd.DataFrame:
    """Load the semantic review CSV.

    Args:
        path: Path to semantic review CSV.

    Returns:
        Semantic review DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing.
    """
    review_path = Path(path)
    if not review_path.exists():
        raise FileNotFoundError(f"Semantic review file not found: {review_path}")

    df = pd.read_csv(review_path)
    required_columns = {
        "sample_id",
        "clean_text",
        "label",
        "labeling_notes",
        "semantic_review_notes",
        "needs_manual_review",
        "semantic_review_status",
    }
    missing_columns = sorted(required_columns.difference(df.columns))
    if missing_columns:
        raise ValueError(f"Missing semantic review columns: {missing_columns}")
    return df


def _as_bool(series: pd.Series) -> pd.Series:
    """Convert a mixed boolean/string series into booleans."""
    return series.fillna(False).astype(str).str.lower().isin(["true", "1", "yes"])


def create_template(review_df: pd.DataFrame) -> pd.DataFrame:
    """Create adjudication template rows from semantic review flags.

    Args:
        review_df: Semantic review DataFrame.

    Returns:
        Adjudication template DataFrame.
    """
    review_mask = (
        _as_bool(review_df["needs_manual_review"])
        | review_df["semantic_review_status"].fillna("").astype(str).str.lower().eq(
            "review"
        )
    )
    selected = review_df.loc[review_mask].copy()

    template_df = pd.DataFrame(
        {
            "sample_id": selected["sample_id"].astype(str),
            "clean_text": selected["clean_text"].fillna("").astype(str),
            "current_label": selected["label"].fillna("").astype(str),
            "labeling_notes": selected["labeling_notes"].fillna("").astype(str),
            "review_reason": selected["semantic_review_notes"]
            .fillna("")
            .astype(str),
            "human_label": "",
            "human_notes": "",
            "final_label": "",
        }
    )
    return template_df.loc[:, OUTPUT_COLUMNS].reset_index(drop=True)


def write_outputs(template_df: pd.DataFrame, output_csv: Path, output_xlsx: Path) -> None:
    """Write adjudication template files."""
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_xlsx.parent.mkdir(parents=True, exist_ok=True)
    template_df.to_csv(output_csv, index=False, encoding="utf-8")
    template_df.to_excel(output_xlsx, index=False)


def write_report(
    review_df: pd.DataFrame,
    template_df: pd.DataFrame,
    output_csv: Path,
    output_xlsx: Path,
    report_path: Path,
    batch_id: str | int,
) -> None:
    """Write the adjudication template report."""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    label_counts = template_df["current_label"].value_counts().to_dict()
    lines = [
        f"# 06 Adjudication Template - Batch {batch_tag(batch_id)}",
        "",
        "## Summary",
        f"- total rows in semantic review: {len(review_df)}",
        f"- rows requiring review: {len(template_df)}",
        "",
        "## Current Label Distribution Among Review Rows",
    ]
    if label_counts:
        lines.extend([f"- {label}: {count}" for label, count in label_counts.items()])
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Output Template Paths",
            f"- CSV: `{output_csv}`",
            f"- XLSX: `{output_xlsx}`",
            "",
            "## Reviewer Instructions",
            "Human reviewer should fill `human_label` with only:",
        ]
    )
    lines.extend([f"- `{label}`" for label in ALLOWED_LABELS])
    lines.extend(
        [
            "",
            "Reviewer may optionally fill `human_notes`.",
            "If `human_label` is filled, `final_label` should usually match `human_label`.",
            "If no correction is needed, `final_label` may match `current_label`.",
            "",
            "Do not change `sample_id` or `clean_text`.",
            "Do not add or remove rows from the adjudication template.",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> object:
    """Parse command-line arguments."""
    import argparse

    parser = argparse.ArgumentParser(description="Create adjudication template.")
    parser.add_argument("--batch-id", default="001")
    parser.add_argument("--semantic-review", default=None)
    parser.add_argument("--output-csv", default=None)
    parser.add_argument("--output-xlsx", default=None)
    parser.add_argument("--output-report", default=None)
    return parser.parse_args()


def main() -> None:
    """Create adjudication CSV/XLSX template and report."""
    args = parse_args()
    paths = paths_for_batch(args.batch_id)
    semantic_path = Path(args.semantic_review) if args.semantic_review else paths["semantic"]
    output_csv = Path(args.output_csv) if args.output_csv else paths["csv"]
    output_xlsx = Path(args.output_xlsx) if args.output_xlsx else paths["xlsx"]
    output_report = Path(args.output_report) if args.output_report else paths["report"]

    review_df = load_semantic_review(semantic_path)
    template_df = create_template(review_df)
    write_outputs(template_df, output_csv, output_xlsx)
    write_report(
        review_df,
        template_df,
        output_csv,
        output_xlsx,
        output_report,
        args.batch_id,
    )

    print(f"Adjudication CSV saved to: {output_csv}")
    print(f"Adjudication XLSX saved to: {output_xlsx}")
    print(f"Report saved to: {output_report}")


if __name__ == "__main__":
    main()
