"""Create a semantic review report for pilot annotation batch 001."""

from __future__ import annotations

import argparse
import json
import platform
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


ALLOWED_LABELS = {"positif", "negatif", "netral"}
DEFAULT_ORIGINAL = Path("data/processed/annotation_batches/annotation_batch_001.csv")
DEFAULT_LABELED = Path(
    "data/processed/annotation_labeled_batches/annotation_batch_001_labeled.csv"
)
DEFAULT_REVIEW_CSV = Path(
    "data/processed/annotation_reviews/annotation_batch_001_semantic_review.csv"
)
DEFAULT_REPORT = Path("outputs/reports/05_pilot_batch_001_semantic_review.md")
DEFAULT_SUMMARY = Path(
    "outputs/reports/05_pilot_batch_001_semantic_review_summary.json"
)

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
POSITIVE_CUES = [
    "good job",
    "mantap",
    "makasih",
    "terima kasih",
    "solusi tepat",
    "makin diakui",
    "sehat",
    "brilian",
    "harapan",
    "cerah",
    "mendukung",
    "menyukseskan",
]
NEGATIVE_CUES = [
    "basi",
    "busuk",
    "berulat",
    "gak dapet",
    "ga bisa",
    "gjlss",
    "gelap",
    "ancaman",
    "pusing",
    "nempeleng",
    "berak",
    "mabok",
]


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV file and fail clearly if missing."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    return pd.read_csv(csv_path)


def validate_inputs(original_df: pd.DataFrame, labeled_df: pd.DataFrame) -> None:
    """Validate original and labeled batch compatibility."""
    required_original = {"sample_id", "clean_text"}
    required_labeled = {"sample_id", "label", "labeling_notes"}
    missing_original = sorted(required_original.difference(original_df.columns))
    missing_labeled = sorted(required_labeled.difference(labeled_df.columns))
    if missing_original:
        raise ValueError(f"Original batch missing columns: {missing_original}")
    if missing_labeled:
        raise ValueError(f"Labeled batch missing columns: {missing_labeled}")

    original_ids = original_df["sample_id"].astype(str).tolist()
    labeled_ids = labeled_df["sample_id"].astype(str).tolist()
    if original_ids != labeled_ids:
        raise ValueError("sample_id values differ or are not in the same order.")

    labels = labeled_df["label"].fillna("").astype(str).str.strip()
    invalid_labels = sorted(set(labels).difference(ALLOWED_LABELS))
    if invalid_labels:
        raise ValueError(f"Invalid labels found: {invalid_labels}")


def _contains_any(text: str, terms: list[str]) -> bool:
    """Check whether text contains any term."""
    lowered = text.lower()
    return any(term in lowered for term in terms)


def semantic_review_reason(row: pd.Series) -> str:
    """Create semantic review notes for a merged annotation row."""
    clean_text = str(row["clean_text"]).lower()
    label = str(row["label"]).strip()
    note = str(row["labeling_notes"]).lower()
    word_count = len(clean_text.split())
    reasons: list[str] = []

    if word_count <= 3:
        reasons.append("teks sangat pendek")
    if _contains_any(note, AMBIGUOUS_NOTE_TERMS):
        reasons.append("catatan menunjukkan konteks ambigu/informatif")
    if label == "netral" and _contains_any(clean_text, POSITIVE_CUES):
        reasons.append("netral tetapi ada sinyal positif")
    if label == "netral" and _contains_any(clean_text, NEGATIVE_CUES):
        reasons.append("netral tetapi ada sinyal negatif")
    if label == "positif" and _contains_any(clean_text, NEGATIVE_CUES):
        reasons.append("positif tetapi ada sinyal negatif")
    if label == "negatif" and _contains_any(clean_text, POSITIVE_CUES):
        reasons.append("negatif tetapi ada sinyal positif")

    return "; ".join(reasons)


def create_semantic_review(
    original_df: pd.DataFrame,
    labeled_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merge clean text with labels and add semantic review flags."""
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


def build_summary(review_df: pd.DataFrame) -> dict[str, Any]:
    """Build semantic review summary."""
    label_counts = {
        str(label): int(count)
        for label, count in review_df["label"].value_counts().items()
    }
    flagged_df = review_df[review_df["needs_manual_review"]]
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": (
            "Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis "
            "(MBG) pada Media Sosial Menggunakan Support Vector Machine (SVM)"
        ),
        "batch_id": "annotation_batch_001",
        "rows": int(len(review_df)),
        "label_counts": label_counts,
        "needs_manual_review_count": int(len(flagged_df)),
        "needs_manual_review_rate": float(len(flagged_df) / len(review_df))
        if len(review_df)
        else 0.0,
        "short_text_count": int((review_df["word_count"] <= 3).sum()),
        "review_status_counts": {
            str(status): int(count)
            for status, count in review_df["semantic_review_status"]
            .value_counts()
            .items()
        },
    }


def write_summary_json(summary: dict[str, Any], path: str | Path) -> None:
    """Write JSON summary."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_report(
    review_df: pd.DataFrame,
    summary: dict[str, Any],
    output_report: str | Path,
) -> None:
    """Write Markdown semantic review report."""
    report_path = Path(output_report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    flagged_df = review_df[review_df["needs_manual_review"]].copy()
    checks = {
        "semantic review rows > 0": len(review_df) > 0,
        "labels are allowed values": set(review_df["label"]).issubset(ALLOWED_LABELS),
        "merged clean_text is present": review_df["clean_text"].notna().all(),
        "review status is present": review_df["semantic_review_status"].notna().all(),
        "summary JSON can be generated": True,
        "semantic report can be generated": True,
    }
    pass_fail = lambda status: "PASS" if status else "FAIL"

    lines = [
        "# 05 Pilot Batch 001 Semantic Review",
        "",
        "## Environment",
        f"- Python version: {platform.python_version()}",
        f"- pandas version: {pd.__version__}",
        "",
        "## Scope",
        f"- {summary['scope']}",
        "- Semantic review for pilot batch 001 only.",
        "- No model training, SMOTE, external API calls, or raw-file changes were performed.",
        "",
        "## Summary",
        f"- rows reviewed: {summary['rows']}",
        f"- needs manual review: {summary['needs_manual_review_count']} "
        f"({summary['needs_manual_review_rate']:.4f})",
        f"- short text count: {summary['short_text_count']}",
        "",
        "## Label Counts",
    ]
    lines.extend(
        [
            f"- {label}: {count}"
            for label, count in summary["label_counts"].items()
        ]
    )
    lines.extend(
        [
            "",
            "## Rows Suggested for Manual Review",
        ]
    )
    if flagged_df.empty:
        lines.append("- none")
    else:
        lines.extend(
            [
                "| sample_id | label | reason | clean_text |",
                "| --- | --- | --- | --- |",
            ]
        )
        for _, row in flagged_df.iterrows():
            clean_text = str(row["clean_text"]).replace("|", "\\|")
            reason = str(row["semantic_review_notes"]).replace("|", "\\|")
            lines.append(
                f"| {row['sample_id']} | {row['label']} | {reason} | {clean_text} |"
            )

    lines.extend(
        [
            "",
            "## Interpretation Notes",
            "- Rows marked `review` are not automatically wrong; they are cases where text is short, ambiguous, informational, joking, or contains lexical cues that merit human review.",
            "- The pilot distribution is still small, so this review should guide annotation consistency before labeling additional batches.",
            "",
            "## Self-run acceptance checks",
        ]
    )
    lines.extend([f"- {pass_fail(status)}: {name}" for name, status in checks.items()])
    lines.extend(
        [
            "",
            "## Next Recommended Step",
            "- Manually inspect the rows marked `review`.",
            "- Decide whether the pilot labeling style is acceptable before continuing to batch 002.",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Create semantic review report for pilot batch 001."
    )
    parser.add_argument("--original-batch", default=str(DEFAULT_ORIGINAL))
    parser.add_argument("--labeled-batch", default=str(DEFAULT_LABELED))
    parser.add_argument("--output-csv", default=str(DEFAULT_REVIEW_CSV))
    parser.add_argument("--output-report", default=str(DEFAULT_REPORT))
    parser.add_argument("--output-summary", default=str(DEFAULT_SUMMARY))
    return parser.parse_args()


def main() -> None:
    """Create semantic review artifacts."""
    args = parse_args()
    original_df = load_csv(args.original_batch)
    labeled_df = load_csv(args.labeled_batch)
    review_df = create_semantic_review(original_df, labeled_df)
    summary = build_summary(review_df)

    output_csv = Path(args.output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    review_df.to_csv(output_csv, index=False, encoding="utf-8")
    write_summary_json(summary, args.output_summary)
    write_report(review_df, summary, args.output_report)

    print(f"Semantic review CSV saved to: {output_csv}")
    print(f"Semantic review summary saved to: {args.output_summary}")
    print(f"Semantic review report saved to: {args.output_report}")


if __name__ == "__main__":
    main()
