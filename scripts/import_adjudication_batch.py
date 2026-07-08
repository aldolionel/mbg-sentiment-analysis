"""Import, normalize, and merge adjudication for any annotation batch."""

from __future__ import annotations

import argparse
import json
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


def batch_tag(batch_id: str | int) -> str:
    """Normalize a batch id to three digits."""
    return str(batch_id).strip().zfill(3)


def default_paths(batch_id: str) -> dict[str, Path]:
    """Return default paths for a batch id."""
    tag = batch_tag(batch_id)
    return {
        "labeled": Path(
            f"data/processed/annotation_labeled_batches/annotation_batch_{tag}_labeled.csv"
        ),
        "semantic": Path(
            f"data/processed/annotation_reviews/annotation_batch_{tag}_semantic_review.csv"
        ),
        "adjudication": Path(
            f"data/processed/adjudication/annotation_batch_{tag}_adjudication_template.xlsx"
        ),
        "adjudicated": Path(
            f"data/processed/annotation_labeled_batches/annotation_batch_{tag}_adjudicated.csv"
        ),
        "normalized": Path(
            f"data/processed/adjudication/annotation_batch_{tag}_adjudication_normalized.csv"
        ),
        "report": Path(f"outputs/reports/07_batch_{tag}_adjudication_report.md"),
        "summary": Path(f"outputs/reports/07_batch_{tag}_adjudication_summary.json"),
    }


def normalize_label(value: object) -> str:
    """Normalize label cell value."""
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def normalize_adjudication(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Normalize adjudication using deterministic fallback rules."""
    missing = [col for col in REQUIRED_ADJUDICATION_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing adjudication columns: {missing}")
    out = df.copy()
    for col in ["current_label", "human_label", "final_label"]:
        out[f"{col}_normalized"] = out[col].apply(normalize_label)
    counts = {
        "human_label_valid_used": 0,
        "final_label_valid_used": 0,
        "fallback_to_current_label": 0,
    }
    final_labels: list[str] = []
    sources: list[str] = []
    for _, row in out.iterrows():
        human = row["human_label_normalized"]
        final = row["final_label_normalized"]
        current = row["current_label_normalized"]
        if human in ALLOWED_LABELS:
            final_labels.append(human)
            sources.append("human_label")
            counts["human_label_valid_used"] += 1
        elif final in ALLOWED_LABELS:
            final_labels.append(final)
            sources.append("final_label")
            counts["final_label_valid_used"] += 1
        else:
            final_labels.append(current)
            sources.append("current_label")
            counts["fallback_to_current_label"] += 1
    out["final_label_normalized"] = final_labels
    out["final_label_source"] = sources
    return out, counts


def validate(
    labeled_df: pd.DataFrame,
    semantic_df: pd.DataFrame,
    normalized_df: pd.DataFrame,
) -> dict[str, bool]:
    """Validate normalized adjudication."""
    labeled_ids = set(labeled_df["sample_id"].astype(str))
    semantic_ids = set(semantic_df["sample_id"].astype(str))
    adjudication_ids = normalized_df["sample_id"].astype(str)
    finals = normalized_df["final_label_normalized"].fillna("").astype(str)
    return {
        "final labels are allowed values": set(finals).issubset(ALLOWED_LABELS),
        "no missing final labels": finals.str.strip().ne("").all(),
        "no duplicate sample_id in adjudication": not adjudication_ids.duplicated().any(),
        "all adjudication sample_id values exist in labeled batch": set(
            adjudication_ids
        ).issubset(labeled_ids),
        "all adjudication sample_id values exist in semantic review": set(
            adjudication_ids
        ).issubset(semantic_ids),
    }


def merge(
    labeled_df: pd.DataFrame,
    semantic_df: pd.DataFrame,
    normalized_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merge adjudication into labeled batch."""
    text_lookup = semantic_df[["sample_id", "clean_text"]].copy()
    lookup = normalized_df[
        [
            "sample_id",
            "final_label_normalized",
            "human_label_normalized",
            "human_notes",
            "review_reason",
        ]
    ].copy()
    out = labeled_df.copy()
    out["label_before_adjudication"] = out["label"]
    if "clean_text" not in out.columns:
        out = out.merge(text_lookup, on="sample_id", how="left")
    out = out.merge(lookup, on="sample_id", how="left")
    out["adjudication_applied"] = out["final_label_normalized"].notna()
    out["label_after_adjudication"] = out["label"]
    mask = out["adjudication_applied"]
    out.loc[mask, "label_after_adjudication"] = out.loc[
        mask,
        "final_label_normalized",
    ]
    out["label"] = out["label_after_adjudication"]
    out["human_label"] = out["human_label_normalized"].fillna("")
    out["human_notes"] = out["human_notes"].fillna("")
    out["adjudication_review_reason"] = out["review_reason"].fillna("")
    return out.drop(
        columns=["final_label_normalized", "human_label_normalized", "review_reason"]
    )


def build_summary(
    batch_id: str,
    labeled_df: pd.DataFrame,
    normalized_df: pd.DataFrame,
    adjudicated_df: pd.DataFrame,
    source_counts: dict[str, int],
    checks: dict[str, bool],
) -> dict[str, Any]:
    """Build summary dictionary."""
    changed = adjudicated_df[
        adjudicated_df["label_before_adjudication"]
        != adjudicated_df["label_after_adjudication"]
    ]
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "batch_id": batch_tag(batch_id),
        "original_rows": int(len(labeled_df)),
        "adjudication_rows": int(len(normalized_df)),
        "adjudicated_rows": int(len(adjudicated_df)),
        "changed_label_rows": int(len(changed)),
        "label_distribution_before": {
            str(label): int(count)
            for label, count in labeled_df["label"].value_counts().items()
        },
        "label_distribution_after": {
            str(label): int(count)
            for label, count in adjudicated_df["label"].value_counts().items()
        },
        **source_counts,
        "validation_checks": {str(k): bool(v) for k, v in checks.items()},
        "all_checks_passed": bool(all(checks.values())),
    }


def write_report(
    paths: dict[str, Path],
    summary: dict[str, Any],
    adjudicated_df: pd.DataFrame,
) -> None:
    """Write Markdown adjudication report."""
    paths["report"].parent.mkdir(parents=True, exist_ok=True)
    changed = adjudicated_df[
        adjudicated_df["label_before_adjudication"]
        != adjudicated_df["label_after_adjudication"]
    ]
    pass_fail = lambda status: "PASS" if status else "FAIL"
    lines = [
        f"# Batch {summary['batch_id']} Adjudication Report",
        "",
        "## Outputs",
        f"- adjudicated batch: `{paths['adjudicated']}`",
        f"- normalized adjudication: `{paths['normalized']}`",
        f"- summary JSON: `{paths['summary']}`",
        "",
        "## Row Counts",
        f"- original labeled rows: {summary['original_rows']}",
        f"- adjudication rows: {summary['adjudication_rows']}",
        f"- adjudicated rows: {summary['adjudicated_rows']}",
        f"- changed label rows: {summary['changed_label_rows']}",
        "",
        "## Validation Checks",
    ]
    lines.extend(
        [
            f"- {pass_fail(status)}: {name}"
            for name, status in summary["validation_checks"].items()
        ]
    )
    lines.extend(["", "## Changed Label Rows"])
    if changed.empty:
        lines.append("- none")
    else:
        lines.extend(
            [
                "| sample_id | clean_text | before | after | human_label | human_notes |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for _, row in changed.iterrows():
            lines.append(
                f"| {row['sample_id']} | {_cell(row.get('clean_text', ''))} | "
                f"{row['label_before_adjudication']} | "
                f"{row['label_after_adjudication']} | {row['human_label']} | "
                f"{_cell(row.get('human_notes', ''))} |"
            )
    paths["report"].write_text("\n".join(lines), encoding="utf-8")


def _cell(value: object) -> str:
    """Escape Markdown table cell."""
    if pd.isna(value):
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ")


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Import adjudication for one batch.")
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--labeled-batch", default=None)
    parser.add_argument("--semantic-review", default=None)
    parser.add_argument("--adjudication-xlsx", default=None)
    parser.add_argument("--output-adjudicated", default=None)
    parser.add_argument("--output-normalized", default=None)
    parser.add_argument("--output-report", default=None)
    parser.add_argument("--output-summary", default=None)
    return parser.parse_args()


def main() -> None:
    """Run adjudication import for one batch."""
    args = parse_args()
    paths = default_paths(args.batch_id)
    overrides = {
        "labeled": args.labeled_batch,
        "semantic": args.semantic_review,
        "adjudication": args.adjudication_xlsx,
        "adjudicated": args.output_adjudicated,
        "normalized": args.output_normalized,
        "report": args.output_report,
        "summary": args.output_summary,
    }
    for key, value in overrides.items():
        if value:
            paths[key] = Path(value)

    labeled_df = pd.read_csv(paths["labeled"])
    semantic_df = pd.read_csv(paths["semantic"])
    adjudication_df = pd.read_excel(paths["adjudication"])
    normalized_df, source_counts = normalize_adjudication(adjudication_df)
    checks = validate(labeled_df, semantic_df, normalized_df)
    adjudicated_df = merge(labeled_df, semantic_df, normalized_df)
    summary = build_summary(
        args.batch_id,
        labeled_df,
        normalized_df,
        adjudicated_df,
        source_counts,
        checks,
    )
    paths["adjudicated"].parent.mkdir(parents=True, exist_ok=True)
    paths["normalized"].parent.mkdir(parents=True, exist_ok=True)
    paths["summary"].parent.mkdir(parents=True, exist_ok=True)
    adjudicated_df.to_csv(paths["adjudicated"], index=False, encoding="utf-8")
    normalized_df.to_csv(paths["normalized"], index=False, encoding="utf-8")
    paths["summary"].write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_report(paths, summary, adjudicated_df)
    print(f"Adjudicated batch saved to: {paths['adjudicated']}")
    print(f"Report saved to: {paths['report']}")


if __name__ == "__main__":
    main()
