"""Validate a labeled annotation batch against its original batch."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ALLOWED_LABELS = {"positif", "negatif", "netral"}
REQUIRED_COLUMNS = ["sample_id", "label", "labeling_notes"]


def batch_tag(batch_id: str | int) -> str:
    """Normalize a batch id to three digits."""
    return str(batch_id).strip().zfill(3)


def default_paths(batch_id: str | int) -> dict[str, Path]:
    """Return default validation paths for a batch id."""
    tag = batch_tag(batch_id)
    return {
        "original": Path(f"data/processed/annotation_batches/annotation_batch_{tag}.csv"),
        "labeled": Path(
            f"data/processed/annotation_labeled_batches/annotation_batch_{tag}_labeled.csv"
        ),
        "report": Path(f"outputs/reports/04_batch_{tag}_validation.md"),
    }


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV file and fail clearly if missing.

    Args:
        path: CSV path.

    Returns:
        Loaded DataFrame.

    Raises:
        FileNotFoundError: If the path does not exist.
    """
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    return pd.read_csv(csv_path)


def validate_labeled_batch(
    original_batch: pd.DataFrame,
    labeled_batch: pd.DataFrame,
) -> dict[str, object]:
    """Validate labeled batch structure and label values.

    Args:
        original_batch: Original unlabeled annotation batch.
        labeled_batch: Labeled batch output.

    Returns:
        Dictionary with validation results.
    """
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in labeled_batch.columns
    ]
    original_ids = original_batch["sample_id"].astype(str).tolist()
    labeled_ids = (
        labeled_batch["sample_id"].astype(str).tolist()
        if "sample_id" in labeled_batch.columns
        else []
    )
    labels = (
        labeled_batch["label"].fillna("").astype(str).str.strip()
        if "label" in labeled_batch.columns
        else pd.Series(dtype=str)
    )
    notes = (
        labeled_batch["labeling_notes"].fillna("").astype(str).str.strip()
        if "labeling_notes" in labeled_batch.columns
        else pd.Series(dtype=str)
    )
    invalid_labels = sorted(set(labels).difference(ALLOWED_LABELS))

    checks = {
        "original row count > 0": len(original_batch) > 0,
        "labeled row count matches original": len(original_batch) == len(labeled_batch),
        "required columns present": not missing_columns,
        "sample_id values unchanged and ordered": original_ids == labeled_ids,
        "labels are all filled": bool(len(labels) > 0 and labels.ne("").all()),
        "labels use allowed values only": not invalid_labels,
        "labeling_notes column exists": "labeling_notes" in labeled_batch.columns,
    }

    return {
        "checks": checks,
        "original_rows": int(len(original_batch)),
        "labeled_rows": int(len(labeled_batch)),
        "missing_columns": missing_columns,
        "invalid_labels": invalid_labels,
        "label_counts": labels.value_counts().to_dict(),
        "empty_notes_count": int(notes.eq("").sum()) if len(notes) else 0,
    }


def write_report(
    results: dict[str, object],
    output_report: str | Path,
    batch_id: str | None = None,
) -> None:
    """Write a Markdown validation report.

    Args:
        results: Validation result dictionary.
        output_report: Markdown report path.
    """
    report_path = Path(output_report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    checks = results["checks"]
    pass_fail = lambda status: "PASS" if status else "FAIL"

    lines = [
        f"# 04 Batch {batch_tag(batch_id) if batch_id else ''} Validation".strip(),
        "",
        "## Scope",
        "- Labeled annotation batch validation.",
        "- No model training, SMOTE, external API calls, or raw file changes were performed.",
        "",
        "## Row Counts",
        f"- original rows: {results['original_rows']}",
        f"- labeled rows: {results['labeled_rows']}",
        "",
        "## Label Counts",
    ]
    label_counts = results["label_counts"]
    if label_counts:
        lines.extend([f"- {label}: {count}" for label, count in label_counts.items()])
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Issues",
            f"- missing columns: {results['missing_columns'] or 'none'}",
            f"- invalid labels: {results['invalid_labels'] or 'none'}",
            f"- empty labeling notes count: {results['empty_notes_count']}",
            "",
            "## Self-run acceptance checks",
        ]
    )
    lines.extend([f"- {pass_fail(status)}: {name}" for name, status in checks.items()])
    lines.extend(
        [
            "",
            "## Next Recommended Step",
            "- Review the pilot labels manually before labeling more batches.",
            "- If the label distribution and notes look acceptable, continue with batch 002.",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Validate a labeled annotation batch.")
    parser.add_argument("--batch-id", default=None, help="Batch id, e.g. 002.")
    parser.add_argument("--original-batch", default=None)
    parser.add_argument("--labeled-batch", default=None)
    parser.add_argument("--output-report", default=None)
    return parser.parse_args()


def main() -> None:
    """Validate a labeled batch and write the report."""
    args = parse_args()
    if args.batch_id:
        paths = default_paths(args.batch_id)
        original_batch = Path(args.original_batch) if args.original_batch else paths["original"]
        labeled_batch = Path(args.labeled_batch) if args.labeled_batch else paths["labeled"]
        output_report = Path(args.output_report) if args.output_report else paths["report"]
    else:
        if not all([args.original_batch, args.labeled_batch, args.output_report]):
            raise SystemExit(
                "Provide --batch-id or all of --original-batch, --labeled-batch, "
                "and --output-report."
            )
        original_batch = Path(args.original_batch)
        labeled_batch = Path(args.labeled_batch)
        output_report = Path(args.output_report)

    original_df = load_csv(original_batch)
    labeled_df = load_csv(labeled_batch)
    results = validate_labeled_batch(original_df, labeled_df)
    write_report(results, output_report, batch_id=args.batch_id)

    all_passed = all(results["checks"].values())
    print(f"Validation report saved to: {output_report}")
    print(f"Validation status: {'PASS' if all_passed else 'FAIL'}")
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
