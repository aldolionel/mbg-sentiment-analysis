"""Create a deduplicated labeling-ready dataset and labeling sample."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mbg_sentiment.labeling_data import (  # noqa: E402
    LABELING_COLUMNS,
    add_labeling_columns,
    compute_labeling_dataset_summary,
    create_labeling_sample,
    deduplicate_by_clean_text,
    export_for_labeling,
    load_interim_dataset,
    validate_interim_columns,
)


DEFAULT_INPUT = Path("data/interim/mbg_crawl_interim.csv")
DEFAULT_READY_OUTPUT = Path("data/processed/mbg_labeling_ready.csv")
DEFAULT_SAMPLE_CSV = Path("data/processed/mbg_labeling_sample_1000.csv")
DEFAULT_SAMPLE_XLSX = Path("data/processed/mbg_labeling_sample_1000.xlsx")
DEFAULT_SUMMARY_JSON = Path("outputs/reports/02_labeling_dataset_summary.json")
DEFAULT_VERIFICATION_REPORT = Path(
    "outputs/reports/02_labeling_dataset_verification.md"
)
SEED = 42


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Create MBG labeling-ready dataset and sample."
    )
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--text-column", default="clean_text")
    parser.add_argument("--ready-output", default=str(DEFAULT_READY_OUTPUT))
    parser.add_argument("--sample-csv", default=str(DEFAULT_SAMPLE_CSV))
    parser.add_argument("--sample-xlsx", default=str(DEFAULT_SAMPLE_XLSX))
    parser.add_argument("--summary-json", default=str(DEFAULT_SUMMARY_JSON))
    parser.add_argument(
        "--verification-report",
        default=str(DEFAULT_VERIFICATION_REPORT),
    )
    parser.add_argument("--sample-size", type=int, default=1000)
    parser.add_argument("--random-state", type=int, default=SEED)
    parser.add_argument("--length-bins", type=int, default=5)
    return parser.parse_args()


def _relative(path: str | Path) -> str:
    """Return a stable display path."""
    path_obj = Path(path)
    try:
        return str(path_obj.relative_to(REPO_ROOT))
    except ValueError:
        return str(path_obj)


def build_full_summary(
    base_summary: dict[str, Any],
    input_path: Path,
    ready_output: Path,
    sample_csv: Path,
    sample_xlsx: Path,
    ready_df: pd.DataFrame,
    sample_df: pd.DataFrame,
    sample_size: int,
    random_state: int,
    length_bins: int,
) -> dict[str, Any]:
    """Build a JSON-serializable labeling preparation summary."""
    empty_label_counts = {
        column: int((ready_df[column].fillna("").astype(str).str.strip() == "").sum())
        for column in LABELING_COLUMNS
        if column in ready_df.columns
    }
    sample_empty_label_counts = {
        column: int((sample_df[column].fillna("").astype(str).str.strip() == "").sum())
        for column in LABELING_COLUMNS
        if column in sample_df.columns
    }

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": (
            "Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis "
            "(MBG) pada Media Sosial Menggunakan Support Vector Machine (SVM)"
        ),
        "prototype_source": "X/Twitter crawl",
        "input_file": _relative(input_path),
        "ready_output": _relative(ready_output),
        "sample_csv": _relative(sample_csv),
        "sample_xlsx": _relative(sample_xlsx),
        "random_state": random_state,
        "requested_sample_size": sample_size,
        "length_bins": length_bins,
        "columns_ready": list(ready_df.columns),
        "columns_sample": list(sample_df.columns),
        "label_columns": LABELING_COLUMNS,
        "empty_label_counts_ready": empty_label_counts,
        "empty_label_counts_sample": sample_empty_label_counts,
        **base_summary,
    }


def write_summary_json(summary: dict[str, Any], path: Path) -> None:
    """Write summary JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_verification_report(summary: dict[str, Any], path: Path) -> None:
    """Write Markdown verification report."""
    checks = {
        "input interim file exists": Path(summary["input_file"]).exists(),
        "labeling-ready file exists": Path(summary["ready_output"]).exists(),
        "sample CSV exists": Path(summary["sample_csv"]).exists(),
        "sample XLSX exists": Path(summary["sample_xlsx"]).exists(),
        "rows after dedup > 0": summary["rows_after_dedup"] > 0,
        "duplicates removed > 0": summary["duplicates_removed"] > 0,
        "sample rows > 0": summary["sample_rows"] > 0,
        "sample rows <= requested size": (
            summary["sample_rows"] <= summary["requested_sample_size"]
        ),
        "label columns are present": all(
            column in summary["columns_ready"]
            for column in summary["label_columns"]
        ),
        "label columns are empty": all(
            count == summary["rows_after_dedup"]
            for count in summary["empty_label_counts_ready"].values()
        ),
        "no sentiment labels fabricated": all(
            count == summary["sample_rows"]
            for count in summary["empty_label_counts_sample"].values()
        ),
    }
    pass_fail = lambda status: "PASS" if status else "FAIL"

    lines = [
        "# 02 Labeling Dataset Verification",
        "",
        "## Environment",
        f"- Python version: {platform.python_version()}",
        f"- pandas version: {pd.__version__}",
        f"- numpy version: {np.__version__}",
        f"- seed: {summary['random_state']}",
        "",
        "## Scope",
        f"- {summary['scope']}",
        f"- Prototype source: {summary['prototype_source']}",
        "- No labeling, SVM modeling, or SMOTE was applied.",
        "",
        "## Input/output",
        f"- input interim file: `{summary['input_file']}`",
        f"- labeling-ready CSV: `{summary['ready_output']}`",
        f"- labeling sample CSV: `{summary['sample_csv']}`",
        f"- labeling sample XLSX: `{summary['sample_xlsx']}`",
        "",
        "## Deduplication summary",
        f"- rows before: {summary['rows_before']}",
        f"- rows after dedup: {summary['rows_after_dedup']}",
        f"- duplicates removed: {summary['duplicates_removed']}",
        f"- duplicate removal rate: {summary['duplicate_removal_rate']:.4f}",
        "",
        "## Labeling sample",
        f"- sample rows: {summary['sample_rows']}",
        f"- requested sample size: {summary['requested_sample_size']}",
        f"- random state: {summary['random_state']}",
        f"- length bins: {summary['length_bins']}",
        "",
        "## Text statistics after deduplication",
        f"- average clean text length: {summary['avg_clean_text_length']:.2f}",
        f"- median clean text length: {summary['median_clean_text_length']:.2f}",
        f"- average clean word count: {summary['avg_clean_word_count']:.2f}",
        f"- median clean word count: {summary['median_clean_word_count']:.2f}",
        "",
        "## Label columns",
    ]
    lines.extend([f"- `{column}`" for column in summary["label_columns"]])
    lines.extend(
        [
            "",
            "## Key findings",
            "- Exact duplicate `clean_text` rows were removed while keeping the first occurrence.",
            f"- {summary['duplicates_removed']} duplicate rows were removed.",
            "- Label columns were added but intentionally left empty.",
            "- A representative sample was created for manual or AI-assisted sentiment labeling.",
            "",
            "## Self-run acceptance checks",
        ]
    )
    lines.extend([f"- {pass_fail(status)}: {name}" for name, status in checks.items()])
    lines.extend(
        [
            "",
            "## Next recommended step",
            "- Review the labeling sample.",
            "- Create a formal annotation workflow and label definitions.",
            "- Perform manual or AI-assisted labeling without fabricating labels.",
            "- After labels are validated, prepare train/test split and baseline modeling.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Create labeling-ready outputs."""
    args = parse_args()
    input_path = Path(args.input)
    ready_output = Path(args.ready_output)
    sample_csv = Path(args.sample_csv)
    sample_xlsx = Path(args.sample_xlsx)
    summary_json = Path(args.summary_json)
    verification_report = Path(args.verification_report)

    interim_df = load_interim_dataset(input_path)
    validate_interim_columns(interim_df, text_col=args.text_column)
    dedup_df = deduplicate_by_clean_text(interim_df, text_col=args.text_column)
    ready_df = add_labeling_columns(dedup_df)
    sample_df = create_labeling_sample(
        ready_df,
        sample_size=args.sample_size,
        random_state=args.random_state,
        length_bins=args.length_bins,
    )

    export_for_labeling(ready_df, ready_output)
    export_for_labeling(sample_df, sample_csv)
    export_for_labeling(sample_df, sample_xlsx)

    base_summary = compute_labeling_dataset_summary(
        df_before=interim_df,
        df_after=ready_df,
        sample_df=sample_df,
    )
    full_summary = build_full_summary(
        base_summary,
        input_path=input_path,
        ready_output=ready_output,
        sample_csv=sample_csv,
        sample_xlsx=sample_xlsx,
        ready_df=ready_df,
        sample_df=sample_df,
        sample_size=args.sample_size,
        random_state=args.random_state,
        length_bins=args.length_bins,
    )
    write_summary_json(full_summary, summary_json)
    write_verification_report(full_summary, verification_report)

    print(f"Labeling-ready dataset saved to: {ready_output}")
    print(f"Labeling sample CSV saved to: {sample_csv}")
    print(f"Labeling sample XLSX saved to: {sample_xlsx}")
    print(f"Summary JSON saved to: {summary_json}")
    print(f"Verification report saved to: {verification_report}")


if __name__ == "__main__":
    main()
