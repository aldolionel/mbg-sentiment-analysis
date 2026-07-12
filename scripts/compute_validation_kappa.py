"""Compute Cohen's Kappa after human validation labels are completed."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, cohen_kappa_score


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "validation"
    / "validation_sample_200_template.csv"
)
REPORT_PATH = PROJECT_ROOT / "outputs" / "reports" / "21_validation_kappa_report.md"
SUMMARY_PATH = PROJECT_ROOT / "outputs" / "reports" / "21_validation_kappa_summary.json"
ALLOWED_LABELS = {"positif", "negatif", "netral"}


def load_table(path: Path) -> pd.DataFrame:
    """Load CSV or XLSX validation table."""
    if not path.exists():
        raise FileNotFoundError(f"Validation file not found: {path}")
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError("Input must be a CSV or Excel file.")


def normalize_label_series(series: pd.Series) -> pd.Series:
    """Normalize label values."""
    return series.fillna("").astype(str).str.strip().str.lower()


def validate_required_labels(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Validate annotator label columns are complete and allowed."""
    required = ["annotator_1_label", "annotator_2_label"]
    missing_columns = [column for column in required if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    ann1 = normalize_label_series(df["annotator_1_label"])
    ann2 = normalize_label_series(df["annotator_2_label"])
    incomplete = int((ann1 == "").sum() + (ann2 == "").sum())
    if incomplete:
        raise ValueError(
            "Cohen's Kappa belum dihitung karena annotator_1_label dan/atau "
            f"annotator_2_label belum lengkap. Empty cells: {incomplete}"
        )

    invalid = sorted((set(ann1) | set(ann2)) - ALLOWED_LABELS)
    if invalid:
        raise ValueError(f"Invalid annotator labels found: {invalid}")
    return ann1, ann2


def optional_agreement(df: pd.DataFrame, gold: pd.Series, column: str) -> float | None:
    """Compute optional agreement against final_gold_label when available."""
    if column not in df.columns:
        return None
    values = normalize_label_series(df[column])
    valid_mask = values.isin(ALLOWED_LABELS) & gold.isin(ALLOWED_LABELS)
    if not valid_mask.all():
        return None
    return float(accuracy_score(gold, values))


def compute_kappa(input_path: Path) -> dict[str, object]:
    """Compute Kappa and optional gold agreements."""
    df = load_table(input_path)
    ann1, ann2 = validate_required_labels(df)
    kappa = float(cohen_kappa_score(ann1, ann2, labels=sorted(ALLOWED_LABELS)))

    summary: dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_file": str(input_path),
        "rows": int(len(df)),
        "cohen_kappa_annotator_1_vs_annotator_2": kappa,
    }

    final_gold_complete = False
    if "final_gold_label" in df.columns:
        gold = normalize_label_series(df["final_gold_label"])
        final_gold_complete = bool((gold != "").all() and set(gold).issubset(ALLOWED_LABELS))
        if final_gold_complete:
            summary["existing_label_vs_final_gold_agreement"] = optional_agreement(
                df,
                gold,
                "existing_label",
            )
            summary["ai_suggested_label_vs_final_gold_agreement"] = optional_agreement(
                df,
                gold,
                "ai_suggested_label",
            )
        else:
            summary["final_gold_label_note"] = (
                "final_gold_label is not complete/valid, so gold agreement was not computed."
            )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    lines = [
        "# 21 Validation Kappa Report",
        "",
        f"Generated at: {summary['generated_at']}",
        f"- input file: `{input_path}`",
        f"- rows: {summary['rows']}",
        f"- Cohen's Kappa annotator_1 vs annotator_2: {kappa:.4f}",
    ]
    if final_gold_complete:
        lines.extend(
            [
                f"- existing_label vs final_gold_label agreement: {summary.get('existing_label_vs_final_gold_agreement')}",
                f"- ai_suggested_label vs final_gold_label agreement: {summary.get('ai_suggested_label_vs_final_gold_agreement')}",
            ]
        )
    else:
        lines.append(
            "- final_gold_label agreement not computed because final_gold_label is incomplete or invalid."
        )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> None:
    """CLI entrypoint."""
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    try:
        summary = compute_kappa(input_path)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(f"Kappa report saved to: {REPORT_PATH}")
    print(f"Kappa summary saved to: {SUMMARY_PATH}")
    print(
        "Cohen's Kappa: "
        f"{summary['cohen_kappa_annotator_1_vs_annotator_2']:.4f}"
    )


if __name__ == "__main__":
    main()
