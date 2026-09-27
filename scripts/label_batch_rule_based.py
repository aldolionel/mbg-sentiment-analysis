"""Create local rule-based pilot labels for a single annotation batch.

This script does not call external APIs. It applies a conservative local
rule-based labeling aid to one explicitly requested batch.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ALLOWED_LABELS = {"positif", "negatif", "netral"}
POSITIVE_CUES = [
    "bagus",
    "baik",
    "mantap",
    "makasih",
    "terima kasih",
    "good job",
    "solusi",
    "tepat",
    "sehat",
    "bergizi",
    "brilian",
    "apresiasi",
    "dukung",
    "bermanfaat",
    "harapan",
]
NEGATIVE_CUES = [
    "basi",
    "busuk",
    "berulat",
    "korupsi",
    "gak dapet",
    "ga dapet",
    "tidak dapet",
    "gak jelas",
    "gjlss",
    "ancaman",
    "pusing",
    "pencitraan",
    "mabok",
    "berak",
    "mahal",
    "utang",
    "buang",
]
QUESTION_CUES = ["apa", "kapan", "berapa", "mana", "siapa", "yak", "kah"]


def batch_tag(batch_id: str | int) -> str:
    """Normalize a batch id to three digits."""
    return str(batch_id).strip().zfill(3)


def default_paths(batch_id: str) -> dict[str, Path]:
    """Return default paths for a batch id."""
    tag = batch_tag(batch_id)
    return {
        "batch": Path(f"data/processed/annotation_batches/annotation_batch_{tag}.csv"),
        "labeled": Path(
            f"data/processed/annotation_labeled_batches/annotation_batch_{tag}_labeled.csv"
        ),
        "report": Path(f"outputs/reports/04_batch_{tag}_labeling_rule_based.md"),
    }


def label_text(text: str) -> tuple[str, str]:
    """Assign a conservative local label to one text value."""
    lowered = str(text).lower()
    positive_hits = [cue for cue in POSITIVE_CUES if cue in lowered]
    negative_hits = [cue for cue in NEGATIVE_CUES if cue in lowered]
    is_question = any(cue in lowered.split() for cue in QUESTION_CUES)

    if negative_hits and not positive_hits:
        return "negatif", f"sinyal negatif: {', '.join(negative_hits[:3])}"
    if positive_hits and not negative_hits and not is_question:
        return "positif", f"sinyal positif: {', '.join(positive_hits[:3])}"
    if positive_hits and negative_hits:
        return "netral", "campuran atau ambigu, perlu review"
    if is_question:
        return "netral", "pertanyaan tanpa polaritas jelas"
    return "netral", "tidak ada polaritas jelas"


def create_labeled_batch(batch_df: pd.DataFrame) -> pd.DataFrame:
    """Create a labeled batch from an annotation batch DataFrame."""
    required = {"sample_id", "clean_text"}
    missing = sorted(required.difference(batch_df.columns))
    if missing:
        raise ValueError(f"Missing batch columns: {missing}")

    rows = []
    for _, row in batch_df.iterrows():
        label, note = label_text(str(row["clean_text"]))
        rows.append(
            {
                "sample_id": row["sample_id"],
                "label": label,
                "labeling_notes": note,
            }
        )
    return pd.DataFrame(rows)


def write_report(
    batch_id: str,
    batch_path: Path,
    labeled_path: Path,
    labeled_df: pd.DataFrame,
    report_path: Path,
) -> None:
    """Write a compact labeling-aid report."""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    counts = labeled_df["label"].value_counts().to_dict()
    lines = [
        f"# Batch {batch_tag(batch_id)} Local Rule-Based Labeling",
        "",
        "## Scope",
        "- This script labels one explicitly requested batch only.",
        "- No external API calls were made.",
        "- No model training or SMOTE was applied.",
        "- Labels should still be manually reviewed before final use.",
        "",
        "## Input/output",
        f"- input batch: `{batch_path}`",
        f"- labeled output: `{labeled_path}`",
        f"- rows: {len(labeled_df)}",
        "",
        "## Label Counts",
    ]
    lines.extend([f"- {label}: {count}" for label, count in counts.items()])
    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Label one annotation batch locally.")
    parser.add_argument("--batch-id", required=True, help="Batch id, e.g. 002.")
    parser.add_argument("--input-batch", default=None)
    parser.add_argument("--output-labeled", default=None)
    parser.add_argument("--output-report", default=None)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting an existing labeled batch.",
    )
    return parser.parse_args()


def main() -> None:
    """Run local labeling for one requested batch."""
    args = parse_args()
    paths = default_paths(args.batch_id)
    batch_path = Path(args.input_batch) if args.input_batch else paths["batch"]
    labeled_path = (
        Path(args.output_labeled) if args.output_labeled else paths["labeled"]
    )
    report_path = Path(args.output_report) if args.output_report else paths["report"]

    if not batch_path.exists():
        raise FileNotFoundError(f"Batch file not found: {batch_path}")
    if labeled_path.exists() and not args.overwrite:
        raise FileExistsError(
            f"Labeled output already exists: {labeled_path}. "
            "Use --overwrite to replace it."
        )

    batch_df = pd.read_csv(batch_path)
    labeled_df = create_labeled_batch(batch_df)
    labeled_path.parent.mkdir(parents=True, exist_ok=True)
    labeled_df.to_csv(labeled_path, index=False, encoding="utf-8")
    write_report(args.batch_id, batch_path, labeled_path, labeled_df, report_path)
    print(f"Labeled batch saved to: {labeled_path}")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
