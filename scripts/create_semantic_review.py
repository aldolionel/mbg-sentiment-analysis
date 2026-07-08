"""Create semantic review artifacts for any labeled annotation batch."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


ALLOWED_LABELS = {"positif", "negatif", "netral"}
AMBIGUOUS_NOTE_TERMS = [
    "ambigu",
    "tidak jelas",
    "tidak relevan",
    "konteks",
    "candaan",
    "pertanyaan",
    "informatif",
    "informasi",
    "pernyataan",
    "perbandingan",
    "saran",
    "terlalu pendek",
]
POSITIVE_CUES = ["good job", "mantap", "makasih", "sehat", "brilian", "harapan"]
NEGATIVE_CUES = ["basi", "busuk", "berulat", "gak dapet", "gjlss", "sindiran"]


def batch_tag(batch_id: str | int) -> str:
    """Normalize a batch id to three digits."""
    return str(batch_id).strip().zfill(3)


def default_paths(batch_id: str) -> dict[str, Path]:
    """Return default paths for a batch id."""
    tag = batch_tag(batch_id)
    return {
        "original": Path(f"data/processed/annotation_batches/annotation_batch_{tag}.csv"),
        "labeled": Path(
            f"data/processed/annotation_labeled_batches/annotation_batch_{tag}_labeled.csv"
        ),
        "review": Path(
            f"data/processed/annotation_reviews/annotation_batch_{tag}_semantic_review.csv"
        ),
        "report": Path(f"outputs/reports/05_batch_{tag}_semantic_review.md"),
        "summary": Path(
            f"outputs/reports/05_batch_{tag}_semantic_review_summary.json"
        ),
    }


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV file."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    return pd.read_csv(csv_path)


def validate_inputs(original_df: pd.DataFrame, labeled_df: pd.DataFrame) -> None:
    """Validate original and labeled batch compatibility."""
    for column in ["sample_id", "clean_text"]:
        if column not in original_df.columns:
            raise ValueError(f"Original batch missing column: {column}")
    for column in ["sample_id", "label", "labeling_notes"]:
        if column not in labeled_df.columns:
            raise ValueError(f"Labeled batch missing column: {column}")
    if original_df["sample_id"].astype(str).tolist() != labeled_df[
        "sample_id"
    ].astype(str).tolist():
        raise ValueError("sample_id values differ or are not ordered identically.")
    labels = labeled_df["label"].fillna("").astype(str).str.strip()
    invalid = sorted(set(labels).difference(ALLOWED_LABELS))
    if invalid:
        raise ValueError(f"Invalid labels found: {invalid}")


def contains_any(text: str, terms: list[str]) -> bool:
    """Return whether any term appears in text."""
    lowered = text.lower()
    return any(term in lowered for term in terms)


def semantic_review_reason(row: pd.Series) -> str:
    """Generate review reason for one row."""
    clean_text = str(row["clean_text"]).lower()
    label = str(row["label"]).strip()
    note = str(row["labeling_notes"]).lower()
    reasons: list[str] = []
    if len(clean_text.split()) <= 3:
        reasons.append("teks sangat pendek")
    if contains_any(note, AMBIGUOUS_NOTE_TERMS):
        reasons.append("catatan menunjukkan konteks ambigu/informatif")
    if label == "netral" and contains_any(clean_text, POSITIVE_CUES):
        reasons.append("netral tetapi ada sinyal positif")
    if label == "netral" and contains_any(clean_text, NEGATIVE_CUES):
        reasons.append("netral tetapi ada sinyal negatif")
    return "; ".join(reasons)


def create_semantic_review(
    original_df: pd.DataFrame,
    labeled_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merge clean text with labels and review flags."""
    validate_inputs(original_df, labeled_df)
    review_df = original_df[["sample_id", "clean_text"]].copy()
    review_df["label"] = labeled_df["label"].fillna("").astype(str).str.strip()
    review_df["labeling_notes"] = (
        labeled_df["labeling_notes"].fillna("").astype(str).str.strip()
    )
    review_df["word_count"] = review_df["clean_text"].fillna("").astype(str).apply(
        lambda value: len(value.split())
    )
    review_df["semantic_review_notes"] = review_df.apply(
        semantic_review_reason,
        axis=1,
    )
    review_df["needs_manual_review"] = review_df["semantic_review_notes"].ne("")
    review_df["semantic_review_status"] = review_df["needs_manual_review"].map(
        {True: "review", False: "ok"}
    )
    return review_df


def build_summary(batch_id: str, review_df: pd.DataFrame) -> dict[str, Any]:
    """Build semantic review summary."""
    flagged = review_df[review_df["needs_manual_review"]]
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "batch_id": batch_tag(batch_id),
        "rows": int(len(review_df)),
        "label_counts": {
            str(label): int(count)
            for label, count in review_df["label"].value_counts().items()
        },
        "needs_manual_review_count": int(len(flagged)),
        "needs_manual_review_rate": float(len(flagged) / len(review_df))
        if len(review_df)
        else 0.0,
    }


def write_outputs(
    batch_id: str,
    review_df: pd.DataFrame,
    summary: dict[str, Any],
    paths: dict[str, Path],
) -> None:
    """Write semantic review CSV, JSON, and report."""
    paths["review"].parent.mkdir(parents=True, exist_ok=True)
    paths["report"].parent.mkdir(parents=True, exist_ok=True)
    review_df.to_csv(paths["review"], index=False, encoding="utf-8")
    paths["summary"].write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        f"# Batch {batch_tag(batch_id)} Semantic Review",
        "",
        f"- rows reviewed: {summary['rows']}",
        f"- needs manual review: {summary['needs_manual_review_count']} "
        f"({summary['needs_manual_review_rate']:.4f})",
        "",
        "## Label Counts",
    ]
    lines.extend(
        [f"- {label}: {count}" for label, count in summary["label_counts"].items()]
    )
    lines.extend(["", "## Outputs", f"- CSV: `{paths['review']}`", f"- JSON: `{paths['summary']}`"])
    paths["report"].write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Create semantic review for a batch.")
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--original-batch", default=None)
    parser.add_argument("--labeled-batch", default=None)
    parser.add_argument("--output-csv", default=None)
    parser.add_argument("--output-report", default=None)
    parser.add_argument("--output-summary", default=None)
    return parser.parse_args()


def main() -> None:
    """Create semantic review artifacts for one batch."""
    args = parse_args()
    paths = default_paths(args.batch_id)
    if args.original_batch:
        paths["original"] = Path(args.original_batch)
    if args.labeled_batch:
        paths["labeled"] = Path(args.labeled_batch)
    if args.output_csv:
        paths["review"] = Path(args.output_csv)
    if args.output_report:
        paths["report"] = Path(args.output_report)
    if args.output_summary:
        paths["summary"] = Path(args.output_summary)

    original_df = load_csv(paths["original"])
    labeled_df = load_csv(paths["labeled"])
    review_df = create_semantic_review(original_df, labeled_df)
    summary = build_summary(args.batch_id, review_df)
    write_outputs(args.batch_id, review_df, summary, paths)
    print(f"Semantic review CSV saved to: {paths['review']}")
    print(f"Semantic review report saved to: {paths['report']}")


if __name__ == "__main__":
    main()
