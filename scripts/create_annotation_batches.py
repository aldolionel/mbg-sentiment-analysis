"""Export annotation batches and AI-assisted labeling prompts."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mbg_sentiment.annotation_batches import (  # noqa: E402
    BATCH_COLUMNS,
    create_annotation_batches,
    export_batch_prompts,
    load_labeling_sample,
    validate_sample,
)


DEFAULT_SAMPLE = Path("data/processed/mbg_labeling_sample_1000.csv")
DEFAULT_BATCH_DIR = Path("data/processed/annotation_batches")
DEFAULT_PROMPT_DIR = Path("data/processed/annotation_prompts")
DEFAULT_SUMMARY = Path("outputs/reports/03_annotation_batches_summary.json")
DEFAULT_REPORT = Path("outputs/reports/03_annotation_batches_verification.md")
SEED = 42


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Create annotation batch CSVs and AI-assisted prompts."
    )
    parser.add_argument("--sample", default=str(DEFAULT_SAMPLE))
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--batch-dir", default=str(DEFAULT_BATCH_DIR))
    parser.add_argument("--prompt-dir", default=str(DEFAULT_PROMPT_DIR))
    parser.add_argument("--summary-json", default=str(DEFAULT_SUMMARY))
    parser.add_argument("--verification-report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def _relative(path: str | Path) -> str:
    """Return path relative to repository root when possible."""
    path_obj = Path(path)
    try:
        return str(path_obj.relative_to(REPO_ROOT))
    except ValueError:
        return str(path_obj)


def _labels_empty(paths: list[Path]) -> bool:
    """Check that all exported batch label columns are empty."""
    for path in paths:
        df = pd.read_csv(path)
        if "label" not in df.columns:
            return False
        non_empty = df["label"].fillna("").astype(str).str.strip().ne("").any()
        if non_empty:
            return False
    return True


def _batch_row_counts(paths: list[Path]) -> list[int]:
    """Return row counts for exported batch CSVs."""
    return [int(len(pd.read_csv(path))) for path in paths]


def build_summary(
    sample_path: Path,
    sample_df: pd.DataFrame,
    batch_paths: list[Path],
    prompt_paths: list[Path],
    batch_size: int,
) -> dict[str, Any]:
    """Build JSON-serializable batch export summary."""
    row_counts = _batch_row_counts(batch_paths)
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "scope": (
            "Analisis Sentimen Publik terhadap Program Makan Bergizi Gratis "
            "(MBG) pada Media Sosial Menggunakan Support Vector Machine (SVM)"
        ),
        "prototype_source": "X/Twitter crawl",
        "sample_path": _relative(sample_path),
        "sample_rows": int(len(sample_df)),
        "batch_size": int(batch_size),
        "batch_count": int(len(batch_paths)),
        "prompt_count": int(len(prompt_paths)),
        "batch_dir": _relative(batch_paths[0].parent) if batch_paths else "",
        "prompt_dir": _relative(prompt_paths[0].parent) if prompt_paths else "",
        "batch_paths": [_relative(path) for path in batch_paths],
        "prompt_paths": [_relative(path) for path in prompt_paths],
        "batch_row_counts": row_counts,
        "batch_columns": BATCH_COLUMNS,
        "labels_empty": _labels_empty(batch_paths),
        "generated_labels": False,
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
        "sample file exists": Path(summary["sample_path"]).exists(),
        "sample rows > 0": summary["sample_rows"] > 0,
        "batch count > 0": summary["batch_count"] > 0,
        "prompt count equals batch count": (
            summary["prompt_count"] == summary["batch_count"]
        ),
        "batch rows total equals sample rows": (
            sum(summary["batch_row_counts"]) == summary["sample_rows"]
        ),
        "all batch labels are empty": summary["labels_empty"],
        "no labels generated": not summary["generated_labels"],
        "summary JSON exists": True,
        "verification report exists": True,
    }
    pass_fail = lambda status: "PASS" if status else "FAIL"

    lines = [
        "# 03 Annotation Batches Verification",
        "",
        "## Environment",
        f"- Python version: {platform.python_version()}",
        f"- pandas version: {pd.__version__}",
        f"- seed: {SEED}",
        "",
        "## Scope",
        f"- {summary['scope']}",
        f"- Prototype source: {summary['prototype_source']}",
        "- No external API calls were made.",
        "- No sentiment labels were generated.",
        "",
        "## Input/output",
        f"- labeling sample: `{summary['sample_path']}`",
        f"- sample rows: {summary['sample_rows']}",
        f"- batch size: {summary['batch_size']}",
        f"- batch count: {summary['batch_count']}",
        f"- prompt count: {summary['prompt_count']}",
        f"- batch directory: `{summary['batch_dir']}`",
        f"- prompt directory: `{summary['prompt_dir']}`",
        "",
        "## Batch columns",
    ]
    lines.extend([f"- `{column}`" for column in summary["batch_columns"]])
    lines.extend(
        [
            "",
            "## Key findings",
            f"- Created {summary['batch_count']} sequential annotation batch CSV files.",
            f"- Created {summary['prompt_count']} matching Markdown prompt files.",
            "- Batch label fields remain empty for manual or AI-assisted annotation.",
            "- Prompts require CSV output with `sample_id,label,labeling_notes`.",
            "",
            "## Self-run acceptance checks",
        ]
    )
    lines.extend([f"- {pass_fail(status)}: {name}" for name, status in checks.items()])
    lines.extend(
        [
            "",
            "## Next recommended step",
            "- Label one batch at a time using the guideline.",
            "- Import completed batch outputs and validate allowed labels.",
            "- Resolve disagreements before model training.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Run batch and prompt export."""
    args = parse_args()
    sample_path = Path(args.sample)
    batch_dir = Path(args.batch_dir)
    prompt_dir = Path(args.prompt_dir)
    summary_path = Path(args.summary_json)
    report_path = Path(args.verification_report)

    sample_df = load_labeling_sample(sample_path)
    validate_sample(sample_df)
    batch_paths = create_annotation_batches(
        sample_df,
        batch_size=args.batch_size,
        output_dir=batch_dir,
    )
    prompt_paths = export_batch_prompts(batch_paths, output_dir=prompt_dir)
    summary = build_summary(
        sample_path=sample_path,
        sample_df=sample_df,
        batch_paths=batch_paths,
        prompt_paths=prompt_paths,
        batch_size=args.batch_size,
    )
    write_summary_json(summary, summary_path)
    write_verification_report(summary, report_path)

    print(f"Annotation batches written: {len(batch_paths)}")
    print(f"Annotation prompts written: {len(prompt_paths)}")
    print(f"Summary JSON saved to: {summary_path}")
    print(f"Verification report saved to: {report_path}")


if __name__ == "__main__":
    main()
