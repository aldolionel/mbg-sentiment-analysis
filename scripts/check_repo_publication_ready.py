"""Check whether the repository is ready for GitHub publication."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = PROJECT_ROOT / "outputs" / "reports" / "18_repo_publication_readiness.md"

REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    ".gitignore",
    "docs/methodology.md",
    "docs/results_summary.md",
    "docs/reproducibility.md",
    "docs/github_publication_checklist.md",
    "data/processed/mbg_labeled_sample_1000.csv",
    "outputs/reports/16_final_modeling_comparison.md",
    "outputs/reports/17_final_visual_results_report.md",
]

IMPORTANT_FIGURES = [
    "outputs/figures/16_final_label_distribution.png",
    "outputs/figures/16_model_comparison_macro_f1.png",
    "outputs/figures/15_confusion_matrix_tuned_linearsvc.png",
]

ALLOWED_LABELS = {"positif", "negatif", "netral"}


def read_gitignore() -> list[str]:
    """Read active .gitignore lines."""
    gitignore_path = PROJECT_ROOT / ".gitignore"
    if not gitignore_path.exists():
        return []
    lines = []
    for raw_line in gitignore_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#"):
            lines.append(line)
    return lines


def has_ignore(patterns: list[str], target: str) -> bool:
    """Check whether a simple target pattern is present."""
    return target in patterns


def required_file_checks() -> tuple[list[dict[str, Any]], list[str]]:
    """Check required files."""
    checks = []
    missing = []
    for relative_path in REQUIRED_FILES:
        exists = (PROJECT_ROOT / relative_path).exists()
        checks.append(
            {
                "name": f"required file exists: {relative_path}",
                "passed": exists,
                "details": "present" if exists else "missing",
            }
        )
        if not exists:
            missing.append(relative_path)
    return checks, missing


def figure_checks() -> list[dict[str, Any]]:
    """Check important figures."""
    checks = []
    for relative_path in IMPORTANT_FIGURES:
        exists = (PROJECT_ROOT / relative_path).exists()
        checks.append(
            {
                "name": f"important figure exists: {relative_path}",
                "passed": exists,
                "details": "present" if exists else "missing",
            }
        )
    return checks


def hygiene_checks(patterns: list[str]) -> list[dict[str, Any]]:
    """Check repository hygiene expectations."""
    automation_logs_path = PROJECT_ROOT / "automation_logs"
    env_path = PROJECT_ROOT / ".env"
    pycache_dirs = [
        path
        for path in PROJECT_ROOT.rglob("__pycache__")
        if ".git" not in path.parts
    ]
    checkpoint_dirs = [
        path
        for path in PROJECT_ROOT.rglob(".ipynb_checkpoints")
        if ".git" not in path.parts
    ]

    return [
        {
            "name": "automation_logs/ exists locally",
            "passed": automation_logs_path.exists(),
            "details": str(automation_logs_path),
        },
        {
            "name": "automation_logs/ ignored by .gitignore",
            "passed": has_ignore(patterns, "automation_logs/"),
            "details": "automation_logs/" if has_ignore(patterns, "automation_logs/") else "not ignored",
        },
        {
            "name": "no .env file present",
            "passed": not env_path.exists(),
            "details": "absent" if not env_path.exists() else str(env_path),
        },
        {
            "name": "__pycache__ folders ignored",
            "passed": has_ignore(patterns, "__pycache__/"),
            "details": f"local folders found: {len(pycache_dirs)}",
        },
        {
            "name": "notebook checkpoints ignored",
            "passed": has_ignore(patterns, ".ipynb_checkpoints/"),
            "details": f"local checkpoint folders found: {len(checkpoint_dirs)}",
        },
    ]


def dataset_validation() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Validate the final labeled dataset."""
    dataset_path = PROJECT_ROOT / "data" / "processed" / "mbg_labeled_sample_1000.csv"
    if not dataset_path.exists():
        return (
            [
                {
                    "name": "final dataset can be validated",
                    "passed": False,
                    "details": "dataset missing",
                }
            ],
            {"error": "dataset missing"},
        )

    df = pd.read_csv(dataset_path)
    labels = set(df["label"].dropna().astype(str).str.strip().str.lower())
    clean_missing = int(
        df["clean_text"].isna().sum()
        + df["clean_text"].fillna("").astype(str).str.strip().eq("").sum()
    )
    label_missing = int(
        df["label"].isna().sum()
        + df["label"].fillna("").astype(str).str.strip().eq("").sum()
    )
    label_counts = df["label"].astype(str).str.strip().str.lower().value_counts()
    summary = {
        "rows": int(len(df)),
        "label_counts": {str(label): int(count) for label, count in label_counts.items()},
        "labels": sorted(labels),
        "missing_clean_text": clean_missing,
        "missing_label": label_missing,
    }
    checks = [
        {
            "name": "final dataset has 1,000 rows",
            "passed": len(df) == 1000,
            "details": f"rows: {len(df)}",
        },
        {
            "name": "final dataset labels are allowed",
            "passed": labels.issubset(ALLOWED_LABELS),
            "details": f"labels: {sorted(labels)}",
        },
        {
            "name": "final dataset has no missing clean_text",
            "passed": clean_missing == 0,
            "details": f"missing/empty clean_text: {clean_missing}",
        },
        {
            "name": "final dataset has no missing label",
            "passed": label_missing == 0,
            "details": f"missing/empty label: {label_missing}",
        },
    ]
    return checks, summary


def pass_fail(value: bool) -> str:
    """Format check status."""
    return "PASS" if value else "FAIL"


def write_report(
    checks: list[dict[str, Any]],
    missing_files: list[str],
    dataset_summary: dict[str, Any],
) -> None:
    """Write Markdown readiness report."""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    all_passed = all(check["passed"] for check in checks)
    lines = [
        "# 18 Repository Publication Readiness",
        "",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## PASS/FAIL Checklist",
    ]
    for check in checks:
        lines.append(
            f"- {pass_fail(check['passed'])}: {check['name']} ({check['details']})"
        )

    lines.extend(["", "## Missing Files"])
    if missing_files:
        lines.extend([f"- `{path}`" for path in missing_files])
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Dataset Validation Summary",
            f"- rows: {dataset_summary.get('rows', 'n/a')}",
            f"- labels: {dataset_summary.get('labels', 'n/a')}",
            f"- label counts: {dataset_summary.get('label_counts', 'n/a')}",
            f"- missing clean_text: {dataset_summary.get('missing_clean_text', 'n/a')}",
            f"- missing label: {dataset_summary.get('missing_label', 'n/a')}",
            "",
            "## GitHub Readiness Conclusion",
        ]
    )
    if all_passed:
        lines.append(
            "PASS: Repository is ready for GitHub publication after final manual review of files selected for commit."
        )
    else:
        lines.append(
            "FAIL: Repository needs fixes before GitHub publication. Review failed checklist items above."
        )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def run_checks() -> bool:
    """Run all readiness checks and write the report."""
    patterns = read_gitignore()
    checks, missing_files = required_file_checks()
    checks.extend(hygiene_checks(patterns))
    dataset_checks, dataset_summary = dataset_validation()
    checks.extend(dataset_checks)
    checks.extend(figure_checks())

    write_report(checks, missing_files, dataset_summary)
    all_passed = all(check["passed"] for check in checks)
    print(f"Readiness report saved to: {REPORT_PATH}")
    print(f"Status: {pass_fail(all_passed)}")
    return all_passed


def main() -> None:
    """CLI entrypoint."""
    if not run_checks():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
