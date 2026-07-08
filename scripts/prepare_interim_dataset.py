"""Prepare a privacy-safe interim dataset from raw crawl data."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mbg_sentiment.data_audit import file_sha256, load_table  # noqa: E402
from mbg_sentiment.preprocessing import (  # noqa: E402
    basic_clean_text,
    basic_text_stats,
    safe_text,
    tokenize_basic,
)


def prepare_interim_dataframe(
    df: pd.DataFrame,
    text_column: str,
    source_file: str,
    source_sheet: str | int | None,
) -> pd.DataFrame:
    """Create a privacy-safe interim DataFrame.

    Args:
        df: Raw input DataFrame.
        text_column: Column containing raw text.
        source_file: Relative or display path for the source file.
        source_sheet: Source sheet name or index.

    Returns:
        Interim DataFrame without raw personal identifiers.

    Raises:
        KeyError: If the text column is missing.
    """
    if text_column not in df.columns:
        raise KeyError(f"Text column not found: {text_column}")

    raw_text = df[text_column].apply(safe_text)
    clean_text = raw_text.apply(basic_clean_text)
    word_count = clean_text.apply(lambda value: len(tokenize_basic(value)))

    interim_df = pd.DataFrame(
        {
            "interim_id": [f"mbg_crawl_{index:06d}" for index in range(1, len(df) + 1)],
            "source_file": Path(source_file).name,
            "source_sheet": "" if source_sheet is None else str(source_sheet),
            "source_row_number": range(2, len(df) + 2),
            "clean_text": clean_text,
            "clean_text_length": clean_text.str.len(),
            "clean_word_count": word_count,
        }
    )
    interim_df["is_empty_clean_text"] = interim_df["clean_text"].str.strip() == ""
    interim_df["is_duplicate_clean_text"] = interim_df.duplicated(
        subset=["clean_text"],
        keep="first",
    )
    return interim_df


def write_summary_report(
    output_path: Path,
    input_path: Path,
    sheet_name: str | int | None,
    text_column: str,
    raw_df: pd.DataFrame,
    interim_df: pd.DataFrame,
) -> Path:
    """Write a concise preparation report beside the interim dataset.

    Args:
        output_path: Path to the generated interim CSV.
        input_path: Path to the raw input file.
        sheet_name: Source sheet name or index.
        text_column: Source text column.
        raw_df: Raw DataFrame.
        interim_df: Interim DataFrame.

    Returns:
        Path to the Markdown report.
    """
    report_path = output_path.with_suffix(".report.md")
    stats = basic_text_stats(interim_df["clean_text"])
    duplicate_count = int(interim_df["is_duplicate_clean_text"].sum())
    duplicate_rate = duplicate_count / len(interim_df) if len(interim_df) else 0.0

    lines = [
        "# 01 Prepare Interim Dataset Report",
        "",
        "## Source",
        f"- input file: `{input_path}`",
        f"- sheet: `{sheet_name}`",
        f"- text column: `{text_column}`",
        f"- sha256 first 12 chars: `{file_sha256(input_path)}`",
        "",
        "## Output",
        f"- output file: `{output_path}`",
        "- raw personal identifiers: not exported",
        "- raw text: not exported",
        "",
        "## Row Counts",
        f"- raw rows: {len(raw_df)}",
        f"- interim rows: {len(interim_df)}",
        "",
        "## Clean Text Quality",
        f"- empty clean text count: {stats['empty_count']}",
        f"- duplicate clean text count: {duplicate_count}",
        f"- duplicate clean text rate: {duplicate_rate:.4f}",
        f"- average clean text length: {stats['avg_length']:.2f}",
        f"- median clean text length: {stats['median_length']:.2f}",
        f"- average clean word count: {stats['avg_word_count']:.2f}",
        f"- median clean word count: {stats['median_word_count']:.2f}",
        "",
        "## Columns Exported",
    ]
    lines.extend([f"- `{column}`" for column in interim_df.columns])
    lines.extend(
        [
            "",
            "## Notes",
            "- This stage performs conservative basic cleaning only.",
            "- No stemming, stopword removal, sentiment labeling, SMOTE, or modeling was applied.",
            "- Mentions and URLs were removed to reduce exposure of personal identifiers.",
        ]
    )

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Prepare a privacy-safe interim MBG crawl dataset."
    )
    parser.add_argument("--input", required=True, help="Raw CSV/Excel input path.")
    parser.add_argument("--sheet", default=None, help="Excel sheet name.")
    parser.add_argument(
        "--text-column",
        required=True,
        help="Column containing the raw text to clean.",
    )
    parser.add_argument("--output", required=True, help="Output interim CSV path.")
    return parser.parse_args()


def main() -> None:
    """Run interim dataset preparation."""
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        raise SystemExit(1)

    try:
        raw_df = load_table(input_path, sheet_name=args.sheet)
        interim_df = prepare_interim_dataframe(
            raw_df,
            text_column=args.text_column,
            source_file=str(input_path),
            source_sheet=args.sheet,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    interim_df.to_csv(output_path, index=False, encoding="utf-8")
    report_path = write_summary_report(
        output_path=output_path,
        input_path=input_path,
        sheet_name=args.sheet,
        text_column=args.text_column,
        raw_df=raw_df,
        interim_df=interim_df,
    )

    print(f"Interim dataset saved to: {output_path}")
    print(f"Preparation report saved to: {report_path}")


if __name__ == "__main__":
    main()
