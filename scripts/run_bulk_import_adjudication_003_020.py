"""Bulk import reviewed adjudication for batches 003 through 020."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


ALLOWED_LABELS = {"positif", "negatif", "netral"}
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
REPORT_PATH = Path("outputs/reports/12_bulk_import_adjudication_003_020.md")
SUMMARY_PATH = Path("outputs/reports/12_bulk_import_adjudication_003_020_summary.json")


def batch_tag(batch_id: str | int) -> str:
    """Normalize a batch id to a three-digit string.

    Args:
        batch_id: Batch id value.

    Returns:
        Three-digit batch id.
    """
    return str(batch_id).strip().zfill(3)


def batch_range(start_batch: str, end_batch: str) -> list[str]:
    """Build an inclusive list of normalized batch ids.

    Args:
        start_batch: First batch id.
        end_batch: Last batch id.

    Returns:
        Inclusive list of three-digit batch ids.

    Raises:
        ValueError: If the requested range is outside 003-020 or invalid.
    """
    start = int(start_batch)
    end = int(end_batch)
    if start > end:
        raise ValueError("start-batch must be less than or equal to end-batch")
    if start < 3 or end > 20:
        raise ValueError("This runner only supports batches 003 through 020")
    return [batch_tag(batch_id) for batch_id in range(start, end + 1)]


def paths_for_batch(batch_id: str) -> dict[str, Path]:
    """Return expected paths for one batch.

    Args:
        batch_id: Three-digit batch id.

    Returns:
        Dictionary of expected input and output paths.
    """
    return {
        "labeled": Path(
            f"data/processed/annotation_labeled_batches/annotation_batch_{batch_id}_labeled.csv"
        ),
        "semantic": Path(
            f"data/processed/annotation_reviews/annotation_batch_{batch_id}_semantic_review.csv"
        ),
        "adjudication": Path(
            f"data/processed/adjudication/annotation_batch_{batch_id}_adjudication_template.xlsx"
        ),
        "adjudicated": Path(
            f"data/processed/annotation_labeled_batches/annotation_batch_{batch_id}_adjudicated.csv"
        ),
        "normalized": Path(
            f"data/processed/adjudication/annotation_batch_{batch_id}_adjudication_normalized.csv"
        ),
        "report": Path(f"outputs/reports/07_batch_{batch_id}_adjudication_report.md"),
        "summary": Path(f"outputs/reports/07_batch_{batch_id}_adjudication_summary.json"),
    }


def normalize_label(value: object) -> str:
    """Normalize label values from adjudication cells.

    Args:
        value: Raw cell value.

    Returns:
        Lowercase stripped label or empty string.
    """
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def validate_adjudication_template(path: Path) -> dict[str, bool]:
    """Validate one reviewed adjudication template before import.

    Args:
        path: Reviewed per-batch adjudication template path.

    Returns:
        Validation checks.

    Raises:
        FileNotFoundError: If the template is missing.
        ValueError: If required columns are missing.
    """
    if not path.exists():
        raise FileNotFoundError(f"Missing adjudication template: {path}")

    df = pd.read_excel(path)
    missing = [col for col in REQUIRED_ADJUDICATION_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing adjudication columns in {path}: {missing}")

    human_labels = df["human_label"].apply(normalize_label)
    final_labels = df["final_label"].apply(normalize_label)
    sample_ids = df["sample_id"].fillna("").astype(str).str.strip()
    checks = {
        "row count > 0": len(df) > 0,
        "no missing sample_id": sample_ids.ne("").all(),
        "no duplicate sample_id": not sample_ids.duplicated().any(),
        "human_label values are allowed labels": set(human_labels).issubset(
            ALLOWED_LABELS
        ),
        "final_label values are allowed labels": set(final_labels).issubset(
            ALLOWED_LABELS
        ),
    }
    return {name: bool(passed) for name, passed in checks.items()}


def preflight_batches(batch_ids: list[str]) -> dict[str, dict[str, bool]]:
    """Run preflight checks for all requested batches.

    Args:
        batch_ids: Batch ids to check.

    Returns:
        Nested validation results by batch id.

    Raises:
        FileNotFoundError: If any expected input file is missing.
        ValueError: If any required template column is missing.
    """
    results: dict[str, dict[str, bool]] = {}
    for batch_id in batch_ids:
        paths = paths_for_batch(batch_id)
        for key in ["labeled", "semantic", "adjudication"]:
            if not paths[key].exists():
                raise FileNotFoundError(f"Missing {key} file for batch {batch_id}: {paths[key]}")
        results[batch_id] = validate_adjudication_template(paths["adjudication"])
    return results


def run_import(batch_id: str) -> subprocess.CompletedProcess[str]:
    """Run the existing single-batch adjudication importer.

    Args:
        batch_id: Three-digit batch id.

    Returns:
        Completed subprocess result.
    """
    command = [
        sys.executable,
        "scripts/import_adjudication_batch.py",
        "--batch-id",
        batch_id,
    ]
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )


def load_batch_summary(batch_id: str) -> dict[str, Any]:
    """Load a per-batch adjudication summary JSON.

    Args:
        batch_id: Three-digit batch id.

    Returns:
        Summary dictionary.

    Raises:
        FileNotFoundError: If the summary JSON was not created.
    """
    summary_path = paths_for_batch(batch_id)["summary"]
    if not summary_path.exists():
        raise FileNotFoundError(f"Missing import summary for batch {batch_id}: {summary_path}")
    return json.loads(summary_path.read_text(encoding="utf-8"))


def build_summary(
    batch_ids: list[str],
    preflight: dict[str, dict[str, bool]],
    import_results: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build aggregate bulk import summary.

    Args:
        batch_ids: Processed batch ids.
        preflight: Preflight checks by batch id.
        import_results: Import results and summaries by batch id.

    Returns:
        Aggregate summary dictionary.
    """
    total_rows = sum(
        int(result["summary"].get("adjudicated_rows", 0))
        for result in import_results.values()
    )
    total_adjudication_rows = sum(
        int(result["summary"].get("adjudication_rows", 0))
        for result in import_results.values()
    )
    changed_rows = sum(
        int(result["summary"].get("changed_label_rows", 0))
        for result in import_results.values()
    )
    after_counts: dict[str, int] = {}
    for result in import_results.values():
        distribution = result["summary"].get("label_distribution_after", {})
        for label, count in distribution.items():
            after_counts[str(label)] = after_counts.get(str(label), 0) + int(count)

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "batch_ids": batch_ids,
        "total_batches": len(batch_ids),
        "total_adjudicated_rows": total_rows,
        "total_adjudication_rows": total_adjudication_rows,
        "total_changed_label_rows": changed_rows,
        "label_distribution_after_overall": after_counts,
        "preflight_checks": preflight,
        "import_results": import_results,
        "all_preflight_checks_passed": all(
            all(checks.values()) for checks in preflight.values()
        ),
        "all_import_commands_succeeded": all(
            result["returncode"] == 0 for result in import_results.values()
        ),
        "all_batch_import_checks_passed": all(
            bool(result["summary"].get("all_checks_passed", False))
            for result in import_results.values()
        ),
    }


def write_report(summary: dict[str, Any]) -> None:
    """Write aggregate Markdown report.

    Args:
        summary: Aggregate summary dictionary.
    """
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 12 Bulk Import Adjudication 003-020",
        "",
        "## Summary",
        f"- total batches: {summary['total_batches']}",
        f"- total adjudicated rows: {summary['total_adjudicated_rows']}",
        f"- total adjudication rows: {summary['total_adjudication_rows']}",
        f"- total changed label rows: {summary['total_changed_label_rows']}",
        "",
        "## Label Distribution After Import",
    ]
    lines.extend(
        [
            f"- {label}: {count}"
            for label, count in summary["label_distribution_after_overall"].items()
        ]
    )
    lines.extend(["", "## Batch Results"])
    for batch_id, result in summary["import_results"].items():
        batch_summary = result["summary"]
        lines.append(
            f"- batch {batch_id}: returncode {result['returncode']}, "
            f"rows {batch_summary.get('adjudicated_rows')}, "
            f"changed {batch_summary.get('changed_label_rows')}, "
            f"checks {'PASS' if batch_summary.get('all_checks_passed') else 'FAIL'}"
        )

    lines.extend(["", "## Validation Checks"])
    lines.append(
        "- "
        f"{'PASS' if summary['all_preflight_checks_passed'] else 'FAIL'}: "
        "all preflight checks passed"
    )
    lines.append(
        "- "
        f"{'PASS' if summary['all_import_commands_succeeded'] else 'FAIL'}: "
        "all import commands succeeded"
    )
    lines.append(
        "- "
        f"{'PASS' if summary['all_batch_import_checks_passed'] else 'FAIL'}: "
        "all batch import checks passed"
    )
    lines.extend(
        [
            "",
            "## Outputs",
            "- finalized batch files: "
            "`data/processed/annotation_labeled_batches/annotation_batch_003_adjudicated.csv` "
            "through "
            "`data/processed/annotation_labeled_batches/annotation_batch_020_adjudicated.csv`",
            "- per-batch normalized adjudication files: "
            "`data/processed/adjudication/annotation_batch_003_adjudication_normalized.csv` "
            "through "
            "`data/processed/adjudication/annotation_batch_020_adjudication_normalized.csv`",
            f"- aggregate summary JSON: `{SUMMARY_PATH}`",
            "",
            "## Notes",
            "Batches 001 and 002 were not processed by this bulk runner.",
            "No model training, SMOTE, raw data modification, or automatic relabeling was performed.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_summary(summary: dict[str, Any]) -> None:
    """Write aggregate JSON summary.

    Args:
        summary: Aggregate summary dictionary.
    """
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Bulk import adjudication for batches 003 through 020."
    )
    parser.add_argument("--start-batch", default="003")
    parser.add_argument("--end-batch", default="020")
    return parser.parse_args()


def main() -> None:
    """Run bulk adjudication import."""
    args = parse_args()
    batch_ids = batch_range(args.start_batch, args.end_batch)
    preflight = preflight_batches(batch_ids)
    if not all(all(checks.values()) for checks in preflight.values()):
        raise SystemExit("Preflight validation failed; no imports were run.")

    import_results: dict[str, dict[str, Any]] = {}
    for batch_id in batch_ids:
        result = run_import(batch_id)
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        batch_summary = load_batch_summary(batch_id) if result.returncode == 0 else {}
        import_results[batch_id] = {
            "returncode": int(result.returncode),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "summary": batch_summary,
        }
        if result.returncode != 0:
            break

    summary = build_summary(batch_ids, preflight, import_results)
    write_report(summary)
    write_summary(summary)

    print(f"Bulk report saved to: {REPORT_PATH}")
    print(f"Bulk summary JSON saved to: {SUMMARY_PATH}")
    print(
        "Bulk validation: "
        f"{'PASS' if summary['all_batch_import_checks_passed'] else 'FAIL'}"
    )

    if not (
        summary["all_preflight_checks_passed"]
        and summary["all_import_commands_succeeded"]
        and summary["all_batch_import_checks_passed"]
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
