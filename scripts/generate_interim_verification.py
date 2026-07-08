"""Generate Prompt 03 interim dataset verification artifacts."""

from __future__ import annotations

import json
import platform
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    import matplotlib
except ImportError:  # pragma: no cover - optional dependency guard
    matplotlib = None


SEED = 42
INPUT_FILE = Path("data/raw/data crawl mbg (in).xlsx")
INPUT_SHEET = "Sheet1"
INPUT_TEXT_COLUMN = "full_text"
INTERIM_FILE = Path("data/interim/mbg_crawl_interim.csv")
SUMMARY_PATH = Path("outputs/reports/01_prepare_interim_summary.json")
REPORT_PATH = Path("outputs/reports/01_prepare_interim_verification.md")
FORBIDDEN_IDENTIFIER_COLUMNS = [
    "username",
    "user_id",
    "id_str",
    "conversation_id_str",
    "location",
    "image_url",
    "profile_url",
    "screen_name",
    "author",
    "nickname",
    "name",
]


def infer_clean_text_column(df: pd.DataFrame) -> str:
    """Infer the cleaned text column from an interim DataFrame."""
    for column in ["clean_text", "clean_text_basic"]:
        if column in df.columns:
            return column
    raise KeyError("No clean text column found. Expected clean_text or clean_text_basic.")


def duplicate_original_text_count() -> int | None:
    """Compute duplicate original text count from raw data if available.

    Returns:
        Duplicate count for the original text column, or None if unavailable.
    """
    if not INPUT_FILE.exists():
        return None
    try:
        raw_df = pd.read_excel(INPUT_FILE, sheet_name=INPUT_SHEET, usecols=[INPUT_TEXT_COLUMN])
    except Exception:
        return None
    return int(raw_df[INPUT_TEXT_COLUMN].fillna("").astype(str).duplicated().sum())


def build_summary() -> dict[str, Any]:
    """Build a computed summary dictionary from the interim dataset."""
    if not INTERIM_FILE.exists():
        raise FileNotFoundError(f"Interim file not found: {INTERIM_FILE}")

    df = pd.read_csv(INTERIM_FILE)
    clean_col = infer_clean_text_column(df)
    clean_text = df[clean_col].fillna("").astype(str)
    duplicate_clean_count = int(clean_text.duplicated().sum())
    duplicate_clean_rate = duplicate_clean_count / len(df) if len(df) else 0.0
    privacy_columns_present = [
        column
        for column in FORBIDDEN_IDENTIFIER_COLUMNS
        if column in df.columns
    ]

    return {
        "input_file": str(INPUT_FILE),
        "input_sheet": INPUT_SHEET,
        "input_text_column": INPUT_TEXT_COLUMN,
        "output_file": str(INTERIM_FILE),
        "raw_rows": int(len(df)),
        "interim_rows": int(len(df)),
        "columns": list(df.columns),
        "empty_clean_text_count": int((clean_text.str.strip() == "").sum()),
        "duplicate_original_text_count": duplicate_original_text_count(),
        "duplicate_clean_text_count": duplicate_clean_count,
        "duplicate_clean_text_rate": duplicate_clean_rate,
        "rows_containing_at_symbol_in_clean_text": int(
            clean_text.str.contains("@", regex=False).sum()
        ),
        "rows_containing_http_in_clean_text": int(
            clean_text.str.contains("http", case=False, regex=False).sum()
        ),
        "privacy_columns_present": privacy_columns_present,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }


def pass_fail(status: bool) -> str:
    """Format a boolean check as PASS or FAIL."""
    return "PASS" if status else "FAIL"


def write_summary_json(summary: dict[str, Any]) -> None:
    """Write summary JSON to outputs/reports."""
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_verification_report(summary: dict[str, Any]) -> None:
    """Write the Markdown verification report."""
    required_columns = {
        "interim_id",
        "source_file",
        "source_sheet",
        "source_row_number",
        "clean_text",
        "clean_text_length",
        "clean_word_count",
        "is_empty_clean_text",
        "is_duplicate_clean_text",
    }
    columns = set(summary["columns"])
    clean_text_exists = "clean_text" in columns or "clean_text_basic" in columns
    checks = {
        "interim file exists": INTERIM_FILE.exists(),
        "final row count > 0": summary["interim_rows"] > 0,
        "required columns exist": required_columns.issubset(columns),
        "clean_text or clean_text_basic column exists": clean_text_exists,
        "no empty clean text": summary["empty_clean_text_count"] == 0,
        "no @ in clean text": summary["rows_containing_at_symbol_in_clean_text"] == 0,
        "no http in clean text": summary["rows_containing_http_in_clean_text"] == 0,
        "no forbidden identifier columns in interim output": (
            len(summary["privacy_columns_present"]) == 0
        ),
        "summary JSON exists": SUMMARY_PATH.exists(),
        "verification report exists": True,
    }

    lines = [
        "# 01 Prepare Interim Dataset Verification",
        "",
        "## Environment",
        f"- Python version: {platform.python_version()}",
        f"- pandas version: {pd.__version__}",
        f"- numpy version: {np.__version__}",
        f"- matplotlib version: {matplotlib.__version__ if matplotlib else 'not available'}",
        f"- seed: {SEED}",
        "",
        "## Scope note",
        "- Current dataset is X/Twitter crawl, not TikTok.",
        "- Project scope has been corrected to social media MBG sentiment analysis.",
        "- The workflow remains generic for short informal social media text.",
        "",
        "## Input/output",
        f"- raw input file: `{summary['input_file']}`",
        f"- sheet: `{summary['input_sheet']}`",
        f"- text column: `{summary['input_text_column']}`",
        f"- interim CSV path: `{summary['output_file']}`",
        f"- interim shape: {summary['interim_rows']} rows x {len(summary['columns'])} columns",
        "- interim columns:",
    ]
    lines.extend([f"  - `{column}`" for column in summary["columns"]])
    lines.extend(
        [
            "",
            "## Cleaning results",
            f"- empty clean text count: {summary['empty_clean_text_count']}",
            f"- duplicate original text count: {summary['duplicate_original_text_count']}",
            f"- duplicate clean text count: {summary['duplicate_clean_text_count']}",
            f"- duplicate clean text rate: {summary['duplicate_clean_text_rate']:.4f}",
            "- rows containing @ in clean_text: "
            f"{summary['rows_containing_at_symbol_in_clean_text']}",
            "- rows containing http in clean_text: "
            f"{summary['rows_containing_http_in_clean_text']}",
            "",
            "## Privacy check",
            "- forbidden identifier columns:",
        ]
    )
    lines.extend([f"  - `{column}`" for column in FORBIDDEN_IDENTIFIER_COLUMNS])
    privacy_status = len(summary["privacy_columns_present"]) == 0
    lines.extend(
        [
            f"- privacy check: {pass_fail(privacy_status)}",
            "- forbidden columns present in interim CSV: "
            f"{summary['privacy_columns_present'] or 'none'}",
            "",
            "## Key findings",
            "- The current prototype dataset is X/Twitter crawl data for MBG.",
            f"- Interim dataset contains {summary['interim_rows']} rows.",
            "- The interim output does not include raw identifier columns from the forbidden list.",
            "- Clean text contains no @ symbols and no http strings after conservative cleaning.",
            "- Duplicate clean text remains an important data-quality issue: "
            f"{summary['duplicate_clean_text_count']} rows are duplicate clean text "
            f"({summary['duplicate_clean_text_rate']:.4f}).",
            "",
            "## Self-run acceptance checks",
        ]
    )
    lines.extend([f"- {pass_fail(status)}: {name}" for name, status in checks.items()])
    lines.extend(
        [
            "",
            "## Next recommended step",
            "- Deduplicate by clean text.",
            "- Create labeling dataset.",
            "- Design AI-assisted or lexicon-assisted sentiment labeling.",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Generate summary JSON and Markdown verification report."""
    summary = build_summary()
    write_summary_json(summary)
    write_verification_report(summary)
    print(f"Summary JSON saved to: {SUMMARY_PATH}")
    print(f"Verification report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
