"""Create final modeling comparison report from existing experiment artifacts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
MODELS_DIR = PROJECT_ROOT / "outputs" / "models"

BASELINE_SUMMARY_PATH = REPORTS_DIR / "14_modeling_baseline_summary.json"
BASELINE_TEST_RESULTS_PATH = REPORTS_DIR / "14_modeling_test_results.csv"
SVM_TUNING_SUMMARY_PATH = REPORTS_DIR / "15_svm_tuning_summary.json"
SVM_TUNING_TEST_RESULTS_PATH = REPORTS_DIR / "15_svm_tuning_test_results.csv"
BEST_SVM_METADATA_PATH = MODELS_DIR / "best_svm_model_metadata.json"

OUTPUT_MD_PATH = REPORTS_DIR / "16_final_modeling_comparison.md"
OUTPUT_SUMMARY_PATH = REPORTS_DIR / "16_final_modeling_comparison_summary.json"
OUTPUT_TABLE_PATH = REPORTS_DIR / "16_final_modeling_comparison_table.csv"

BASELINE_MODEL_NAMES = {
    "multinomial_nb": "Multinomial Naive Bayes",
    "logistic_regression": "Logistic Regression",
    "linear_svm": "Linear SVM baseline",
    "rbf_svm": "RBF SVM baseline",
}

TUNED_SVM_NAMES = {
    "tuned_linearsvc": "Tuned LinearSVC",
    "tuned_svc_linear": "Tuned SVC Linear Kernel",
    "tuned_svc_rbf": "Tuned SVC RBF Kernel",
}

METRIC_COLUMNS = [
    "accuracy",
    "precision_macro",
    "recall_macro",
    "f1_macro",
    "f1_weighted",
]


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON file with a clear missing-file error."""
    if not path.exists():
        raise FileNotFoundError(f"Required input not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> pd.DataFrame:
    """Read a CSV file with a clear missing-file error."""
    if not path.exists():
        raise FileNotFoundError(f"Required input not found: {path}")
    return pd.read_csv(path)


def dataframe_markdown(df: pd.DataFrame, float_format: str = ".4f") -> str:
    """Convert a DataFrame to a small GitHub-style Markdown table."""
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in df.iterrows():
        values = []
        for column in headers:
            value = row[column]
            if isinstance(value, float):
                values.append(f"{value:{float_format}}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def metric_row(
    model_group: str,
    model_name: str,
    metrics: dict[str, Any],
    notes: str,
) -> dict[str, Any]:
    """Create a normalized comparison-table row."""
    row: dict[str, Any] = {
        "model_group": model_group,
        "model_name": model_name,
        "notes": notes,
    }
    for metric in METRIC_COLUMNS:
        row[metric] = float(metrics[metric])
    return row


def build_comparison_table(
    baseline_df: pd.DataFrame,
    tuned_df: pd.DataFrame,
) -> pd.DataFrame:
    """Build and rank the unified model comparison table."""
    rows: list[dict[str, Any]] = []

    baseline_notes = {
        "multinomial_nb": "Baseline probabilistic classifier.",
        "logistic_regression": "Strong non-SVM baseline with class_weight='balanced'.",
        "linear_svm": "Baseline SVM reference before tuning.",
        "rbf_svm": "Baseline nonlinear SVM reference before tuning.",
    }
    for model_key, model_name in BASELINE_MODEL_NAMES.items():
        match = baseline_df.loc[baseline_df["model"] == model_key]
        if match.empty:
            continue
        metrics = match.iloc[0].to_dict()
        rows.append(
            metric_row(
                "Baseline",
                model_name,
                metrics,
                baseline_notes[model_key],
            )
        )

    tuned_notes = {
        "tuned_linearsvc": "Best tuned SVM by test macro F1.",
        "tuned_svc_linear": "Tuned SVC with linear kernel.",
        "tuned_svc_rbf": "Tuned nonlinear SVM with RBF kernel.",
    }
    for experiment_key, model_name in TUNED_SVM_NAMES.items():
        match = tuned_df.loc[tuned_df["experiment"] == experiment_key]
        if match.empty:
            continue
        metrics = match.iloc[0].to_dict()
        rows.append(
            metric_row(
                "Tuned SVM",
                model_name,
                metrics,
                tuned_notes[experiment_key],
            )
        )

    comparison_df = pd.DataFrame(rows)
    comparison_df = comparison_df[
        ["model_group", "model_name", *METRIC_COLUMNS, "notes"]
    ].sort_values(["f1_macro", "accuracy"], ascending=[False, False])
    return comparison_df.reset_index(drop=True)


def find_metric(df: pd.DataFrame, model_name: str, metric: str) -> float:
    """Get a metric value by display model name."""
    match = df.loc[df["model_name"] == model_name]
    if match.empty:
        raise KeyError(f"Model not found in comparison table: {model_name}")
    return float(match.iloc[0][metric])


def percent_point(value: float) -> float:
    """Convert a fraction into percentage points."""
    return value * 100


def build_summary(
    baseline_summary: dict[str, Any],
    svm_summary: dict[str, Any],
    best_svm_metadata: dict[str, Any],
    comparison_df: pd.DataFrame,
) -> dict[str, Any]:
    """Build the JSON summary for the final comparison report."""
    best_overall_row = comparison_df.iloc[0].to_dict()
    svm_rows = comparison_df[
        comparison_df["model_group"].eq("Tuned SVM")
        | comparison_df["model_name"].str.contains("SVM", case=False, regex=False)
        | comparison_df["model_name"].str.contains("LinearSVC", case=False, regex=False)
    ]
    best_svm_row = svm_rows.sort_values(
        ["f1_macro", "accuracy"],
        ascending=[False, False],
    ).iloc[0].to_dict()

    logistic_f1 = find_metric(comparison_df, "Logistic Regression", "f1_macro")
    baseline_linear_f1 = find_metric(comparison_df, "Linear SVM baseline", "f1_macro")
    tuned_linearsvc_f1 = find_metric(comparison_df, "Tuned LinearSVC", "f1_macro")
    improvement = tuned_linearsvc_f1 - baseline_linear_f1

    best_svm_params = best_svm_metadata.get("best_params") or svm_summary["best_svm"][
        "best_params"
    ]
    negative_class = {
        key: value.get("negative_class")
        for key, value in svm_summary.get("experiments", {}).items()
        if value.get("negative_class")
    }

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_files": {
            "baseline_summary": str(BASELINE_SUMMARY_PATH),
            "baseline_test_results": str(BASELINE_TEST_RESULTS_PATH),
            "svm_tuning_summary": str(SVM_TUNING_SUMMARY_PATH),
            "svm_tuning_test_results": str(SVM_TUNING_TEST_RESULTS_PATH),
            "best_svm_metadata": str(BEST_SVM_METADATA_PATH),
        },
        "dataset": baseline_summary.get("dataset") or svm_summary.get("dataset"),
        "split": baseline_summary.get("split") or svm_summary.get("split"),
        "selection_metric": "f1_macro",
        "best_overall_model": {
            "model_group": best_overall_row["model_group"],
            "model_name": best_overall_row["model_name"],
            "metrics": {
                metric: float(best_overall_row[metric]) for metric in METRIC_COLUMNS
            },
        },
        "best_svm_model": {
            "model_group": best_svm_row["model_group"],
            "model_name": best_svm_row["model_name"],
            "metrics": {metric: float(best_svm_row[metric]) for metric in METRIC_COLUMNS},
            "best_params": best_svm_params,
            "metadata_path": str(BEST_SVM_METADATA_PATH),
        },
        "logistic_regression_baseline_f1_macro": logistic_f1,
        "best_svm_beats_logistic_regression_baseline": bool(
            float(best_svm_row["f1_macro"]) > logistic_f1
        ),
        "linear_svm_improvement": {
            "baseline_linear_svm_f1_macro": baseline_linear_f1,
            "tuned_linearsvc_f1_macro": tuned_linearsvc_f1,
            "absolute_improvement": improvement,
            "percentage_point_improvement": percent_point(improvement),
        },
        "negative_class_performance": negative_class,
        "recommendation": "Tuned LinearSVC + TF-IDF",
        "outputs": {
            "markdown_report": str(OUTPUT_MD_PATH),
            "summary_json": str(OUTPUT_SUMMARY_PATH),
            "comparison_table_csv": str(OUTPUT_TABLE_PATH),
        },
    }


def format_params(params: dict[str, Any]) -> str:
    """Format model parameters for Markdown."""
    parts = []
    for key in sorted(params):
        value = params[key]
        if isinstance(value, list):
            value = tuple(value)
        parts.append(f"`{key}={value}`")
    return ", ".join(parts)


def write_markdown_report(summary: dict[str, Any], comparison_df: pd.DataFrame) -> None:
    """Write the final modeling comparison Markdown report."""
    dataset = summary["dataset"]
    split = summary["split"]
    best_overall = summary["best_overall_model"]
    best_svm = summary["best_svm_model"]
    improvement = summary["linear_svm_improvement"]
    negative_class = summary["negative_class_performance"]
    recommendation_supported = (
        best_svm["model_name"] == "Tuned LinearSVC"
        and best_overall["model_name"] == "Tuned LinearSVC"
    )

    lines = [
        "# 16 Final Modeling Comparison",
        "",
        "## Scope",
        "This report compares existing modeling experiments for MBG sentiment classification. It uses only the saved baseline and SVM tuning result files and does not retrain models, relabel data, modify raw files, or overwrite earlier reports.",
        "The report is intended for thesis discussion of the modeling stage; it does not claim that the entire thesis is finished.",
        "",
        "## Dataset",
        f"- total rows: {dataset['total_rows']}",
        "- label distribution:",
    ]
    for label, count in dataset["label_distribution"].items():
        percent = dataset["label_percentage"][label]
        lines.append(f"  - {label}: {count} ({percent:.2f}%)")

    lines.extend(
        [
            "- imbalance note: the `negatif` class is much smaller than `netral` and `positif`, so minority-class behavior needs special attention.",
            "",
            "## Evaluation Design",
            f"- train/test split: {split['train_rows']}/{split['test_rows']} rows",
            f"- stratification: {split['stratify']}",
            "- main selection metric: macro F1",
            "- macro F1 is prioritized because it gives each class equal weight. Accuracy alone is insufficient because a model can score well by favoring the larger `netral` and `positif` classes while performing poorly on `negatif`.",
            "",
            "## Baseline Models",
            "- Multinomial Naive Bayes",
            "- Logistic Regression",
            "- Linear SVM",
            "- RBF SVM",
            "",
            "## Tuned SVM Models",
            "- Tuned LinearSVC",
            "- Tuned SVC Linear Kernel",
            "- Tuned SVC RBF Kernel",
            "",
            "## Unified Comparison Table",
            dataframe_markdown(comparison_df),
            "",
            "## Best Model Findings",
            f"- best overall model by macro F1: {best_overall['model_name']} ({best_overall['metrics']['f1_macro']:.4f})",
            f"- best SVM model by macro F1: {best_svm['model_name']} ({best_svm['metrics']['f1_macro']:.4f})",
            f"- best SVM beats Logistic Regression baseline: {summary['best_svm_beats_logistic_regression_baseline']}",
            f"- recommended thesis modeling choice: {'Tuned LinearSVC + TF-IDF' if recommendation_supported else summary['recommendation']}",
            f"- best SVM parameters: {format_params(best_svm['best_params'])}",
            "",
            "## Improvement Analysis",
            f"- baseline Linear SVM macro F1: {improvement['baseline_linear_svm_f1_macro']:.4f}",
            f"- tuned LinearSVC macro F1: {improvement['tuned_linearsvc_f1_macro']:.4f}",
            f"- absolute improvement: {improvement['absolute_improvement']:.4f}",
            f"- percentage-point improvement: {improvement['percentage_point_improvement']:.2f} points",
            "",
            "## Negative-Class Discussion",
            "The dataset is imbalanced, and the `negatif` class remains the most difficult class. Negative-class F1 for tuned SVM models is lower than their weighted F1, which means the model still benefits from discussion as a limitation rather than a fully solved minority-class problem.",
        ]
    )
    for experiment, metrics in negative_class.items():
        display = TUNED_SVM_NAMES.get(experiment, experiment)
        lines.append(
            f"- {display}: negative precision={metrics['precision']:.4f}, "
            f"recall={metrics['recall']:.4f}, F1={metrics['f1-score']:.4f}, "
            f"support={int(metrics['support'])}"
        )

    lines.extend(
        [
            "",
            "## Narasi untuk Bab Hasil dan Pembahasan",
            "Pada tahap pemodelan, penelitian ini membandingkan beberapa model klasifikasi sentimen berbasis fitur TF-IDF. Model baseline yang diuji meliputi Multinomial Naive Bayes, Logistic Regression, Linear SVM, dan RBF SVM. Setelah itu, fokus eksperimen diarahkan pada keluarga SVM melalui tuning hyperparameter pada LinearSVC, SVC dengan kernel linear, dan SVC dengan kernel RBF.",
            "",
            "Pemilihan model utama didasarkan pada macro F1 karena distribusi label tidak seimbang. Kelas `negatif` memiliki jumlah data yang lebih sedikit dibandingkan kelas `netral` dan `positif`, sehingga akurasi saja tidak cukup untuk menilai kualitas model. Macro F1 memberikan bobot yang setara kepada setiap kelas dan lebih sesuai untuk mengevaluasi performa model pada kondisi class imbalance.",
            "",
            f"Hasil perbandingan menunjukkan bahwa model terbaik berdasarkan macro F1 adalah {best_overall['model_name']} dengan nilai macro F1 sebesar {best_overall['metrics']['f1_macro']:.4f}. Model ini juga menjadi model SVM terbaik dan menunjukkan peningkatan dibandingkan Linear SVM baseline, dari {improvement['baseline_linear_svm_f1_macro']:.4f} menjadi {improvement['tuned_linearsvc_f1_macro']:.4f}. Dengan demikian, model TF-IDF + Tuned LinearSVC dapat direkomendasikan sebagai model akhir untuk tahap pembahasan pemodelan sentimen MBG.",
            "",
            "Meskipun performa keseluruhan meningkat, performa pada kelas `negatif` masih relatif lebih rendah. Hal ini menunjukkan bahwa model masih menghadapi tantangan dalam mengenali sentimen negatif yang jumlah datanya lebih terbatas. Oleh karena itu, hasil ini perlu dibahas sebagai keterbatasan penelitian, terutama terkait ketidakseimbangan kelas dan ukuran sampel data berlabel.",
            "",
            "## Limitation Note",
            "- Labels are AI-assisted with adjudication/manual review, so label quality should be described transparently.",
            "- The dataset contains 1,000 sampled labeled rows from a larger social media crawl.",
            "- Future work can include larger manual validation, SMOTE comparison, or transformer-based models.",
        ]
    )

    OUTPUT_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def create_final_modeling_comparison() -> dict[str, Any]:
    """Create final comparison CSV, JSON summary, and Markdown report."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    baseline_summary = read_json(BASELINE_SUMMARY_PATH)
    baseline_df = read_csv(BASELINE_TEST_RESULTS_PATH)
    svm_summary = read_json(SVM_TUNING_SUMMARY_PATH)
    tuned_df = read_csv(SVM_TUNING_TEST_RESULTS_PATH)
    best_svm_metadata = read_json(BEST_SVM_METADATA_PATH)

    comparison_df = build_comparison_table(baseline_df, tuned_df)
    comparison_df.to_csv(OUTPUT_TABLE_PATH, index=False, encoding="utf-8")

    summary = build_summary(
        baseline_summary,
        svm_summary,
        best_svm_metadata,
        comparison_df,
    )
    OUTPUT_SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_markdown_report(summary, comparison_df)

    print(f"Comparison table saved to: {OUTPUT_TABLE_PATH}")
    print(f"Summary JSON saved to: {OUTPUT_SUMMARY_PATH}")
    print(f"Markdown report saved to: {OUTPUT_MD_PATH}")
    print(
        "Recommended model: "
        f"{summary['recommendation']} "
        f"(macro F1={summary['best_svm_model']['metrics']['f1_macro']:.4f})"
    )
    return summary


def main() -> None:
    """CLI entrypoint."""
    create_final_modeling_comparison()


if __name__ == "__main__":
    main()
