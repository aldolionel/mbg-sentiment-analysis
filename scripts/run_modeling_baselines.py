"""Run TF-IDF classical ML baseline experiments for MBG sentiment labels."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.base import clone
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.mbg_sentiment.modeling import (  # noqa: E402
    RANDOM_STATE,
    build_tfidf_vectorizer,
    default_cv,
    evaluate_model_cv,
    get_models,
    load_labeled_dataset,
    train_test_evaluate,
)


DATA_PATH = PROJECT_ROOT / "data" / "processed" / "mbg_labeled_sample_1000.csv"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
MODELS_DIR = PROJECT_ROOT / "outputs" / "models"
SUMMARY_JSON_PATH = REPORTS_DIR / "14_modeling_baseline_summary.json"
REPORT_MD_PATH = REPORTS_DIR / "14_modeling_baseline_report.md"
CV_RESULTS_PATH = REPORTS_DIR / "14_modeling_cv_results.csv"
TEST_RESULTS_PATH = REPORTS_DIR / "14_modeling_test_results.csv"
BEST_MODEL_PATH = MODELS_DIR / "best_baseline_model.joblib"
BEST_MODEL_METADATA_PATH = MODELS_DIR / "best_baseline_model_metadata.json"


MODEL_DISPLAY_NAMES = {
    "multinomial_nb": "Multinomial Naive Bayes",
    "logistic_regression": "Logistic Regression",
    "linear_svm": "Linear SVM",
    "rbf_svm": "RBF SVM",
}

CONFUSION_MATRIX_PATHS = {
    "multinomial_nb": FIGURES_DIR / "14_confusion_matrix_multinomial_nb.png",
    "logistic_regression": FIGURES_DIR / "14_confusion_matrix_logistic_regression.png",
    "linear_svm": FIGURES_DIR / "14_confusion_matrix_linear_svm.png",
    "rbf_svm": FIGURES_DIR / "14_confusion_matrix_rbf_svm.png",
}


def ensure_output_dirs() -> None:
    """Create output directories used by this experiment."""
    for directory in [REPORTS_DIR, FIGURES_DIR, MODELS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def build_pipeline(model: Any) -> Pipeline:
    """Create a fresh TF-IDF + classifier pipeline."""
    return Pipeline(
        [
            ("tfidf", build_tfidf_vectorizer()),
            ("classifier", clone(model)),
        ]
    )


def dataset_summary(df: pd.DataFrame) -> dict[str, Any]:
    """Summarize row count and class balance."""
    counts = df["label"].value_counts().sort_index()
    percentages = (counts / len(df) * 100).round(2)
    return {
        "total_rows": int(len(df)),
        "dropped_missing_count": int(df.attrs.get("dropped_missing_count", 0)),
        "label_distribution": {str(label): int(count) for label, count in counts.items()},
        "label_percentage": {
            str(label): float(percent) for label, percent in percentages.items()
        },
    }


def cv_summary_to_row(model_key: str, cv_summary: dict[str, dict[str, float]]) -> dict[str, Any]:
    """Flatten cross-validation results for CSV output."""
    row: dict[str, Any] = {
        "model": model_key,
        "model_display_name": MODEL_DISPLAY_NAMES[model_key],
    }
    for metric, values in cv_summary.items():
        row[f"{metric}_mean"] = values["mean"]
        row[f"{metric}_std"] = values["std"]
    return row


def test_result_to_row(model_key: str, result: dict[str, Any]) -> dict[str, Any]:
    """Flatten train/test metrics for CSV output."""
    row: dict[str, Any] = {
        "model": model_key,
        "model_display_name": MODEL_DISPLAY_NAMES[model_key],
    }
    row.update(result["metrics"])
    return row


def save_confusion_matrix(
    matrix: Any,
    labels: list[str],
    title: str,
    output_path: Path,
) -> None:
    """Save a confusion matrix heatmap."""
    plt.figure(figsize=(6.5, 5.5))
    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels,
        cbar=False,
    )
    plt.title(title)
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def dataframe_markdown(df: pd.DataFrame, float_format: str = ".4f") -> str:
    """Convert a DataFrame to Markdown with graceful fallback."""
    try:
        return df.to_markdown(index=False, floatfmt=float_format)
    except ImportError:
        return df.to_string(index=False)


def write_markdown_report(
    summary: dict[str, Any],
    cv_df: pd.DataFrame,
    test_df: pd.DataFrame,
    test_results: dict[str, dict[str, Any]],
    best_model_key: str,
) -> None:
    """Write the baseline modeling Markdown report."""
    lines = [
        "# 14 Modeling Baseline Report",
        "",
        "## Scope",
        "This report documents baseline modeling experiments for MBG sentiment classification using TF-IDF features and classical ML models. These results are baseline experiments, not final thesis results.",
        "No raw files were modified, no data was relabeled, and SMOTE was not applied in this script.",
        "",
        "## Evaluation Priority",
        "Macro F1 is prioritized because the labeled dataset is imbalanced, especially for the `negatif` class. Accuracy is reported, but it is not used alone as the main conclusion.",
        "",
        "## Dataset Summary",
        f"- input dataset: `{summary['input_dataset']}`",
        f"- total rows: {summary['dataset']['total_rows']}",
        f"- dropped rows with missing clean_text or label: {summary['dataset']['dropped_missing_count']}",
        "",
        "### Label Distribution",
    ]
    for label, count in summary["dataset"]["label_distribution"].items():
        percent = summary["dataset"]["label_percentage"][label]
        lines.append(f"- {label}: {count} ({percent:.2f}%)")

    lines.extend(
        [
            "",
            "## Experiment Setup",
            f"- random_state: {RANDOM_STATE}",
            "- train/test split: 80/20, stratified by label",
            "- cross-validation: 5-fold StratifiedKFold with shuffle=True",
            "- features: TF-IDF, unigrams and bigrams, min_df=2, max_df=0.95, sublinear_tf=True",
            "- main model family: SVM",
            "- baselines: Multinomial Naive Bayes and Logistic Regression",
            "- imbalance handling: class_weight='balanced' for Logistic Regression, Linear SVM, and RBF SVM",
            "",
            "## Cross-Validation Results",
            dataframe_markdown(cv_df),
            "",
            "## Test Results",
            dataframe_markdown(test_df),
            "",
            "## Best Baseline Model",
            f"- selected by test macro F1: {MODEL_DISPLAY_NAMES[best_model_key]} (`{best_model_key}`)",
            f"- test macro F1: {summary['best_model']['test_f1_macro']:.4f}",
            f"- artifact: `{BEST_MODEL_PATH}`",
            "",
            "## Classification Reports",
        ]
    )
    for model_key, result in test_results.items():
        lines.extend(
            [
                "",
                f"### {MODEL_DISPLAY_NAMES[model_key]}",
                "```text",
                result["classification_report_text"],
                "```",
                f"- confusion matrix figure: `{CONFUSION_MATRIX_PATHS[model_key]}`",
            ]
        )

    REPORT_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def run_baselines() -> dict[str, Any]:
    """Run all baseline experiments and save reports, figures, and model artifacts."""
    ensure_output_dirs()
    df = load_labeled_dataset(DATA_PATH)
    summary_dataset = dataset_summary(df)
    print(f"Loaded dataset: {DATA_PATH}")
    print(f"Total rows: {summary_dataset['total_rows']}")
    print("Label distribution:")
    for label, count in summary_dataset["label_distribution"].items():
        percent = summary_dataset["label_percentage"][label]
        print(f"  {label}: {count} ({percent:.2f}%)")

    X = df["clean_text"]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    cv_rows: list[dict[str, Any]] = []
    test_rows: list[dict[str, Any]] = []
    test_results: dict[str, dict[str, Any]] = {}
    trained_pipelines: dict[str, Pipeline] = {}
    models = get_models()
    cv = default_cv()

    for model_key, estimator in models.items():
        print(f"Evaluating {MODEL_DISPLAY_NAMES[model_key]}...")
        cv_pipeline = build_pipeline(estimator)
        cv_summary = evaluate_model_cv(cv_pipeline, X, y, cv)
        cv_rows.append(cv_summary_to_row(model_key, cv_summary))

        test_pipeline = build_pipeline(estimator)
        test_result = train_test_evaluate(test_pipeline, X_train, X_test, y_train, y_test)
        test_rows.append(test_result_to_row(model_key, test_result))
        test_results[model_key] = test_result
        trained_pipelines[model_key] = test_pipeline

        save_confusion_matrix(
            test_result["confusion_matrix"],
            test_result["labels"],
            f"{MODEL_DISPLAY_NAMES[model_key]} Confusion Matrix",
            CONFUSION_MATRIX_PATHS[model_key],
        )

    cv_df = pd.DataFrame(cv_rows).sort_values("f1_macro_mean", ascending=False)
    test_df = pd.DataFrame(test_rows).sort_values("f1_macro", ascending=False)
    cv_df.to_csv(CV_RESULTS_PATH, index=False, encoding="utf-8")
    test_df.to_csv(TEST_RESULTS_PATH, index=False, encoding="utf-8")

    best_model_key = str(test_df.iloc[0]["model"])
    joblib.dump(trained_pipelines[best_model_key], BEST_MODEL_PATH)

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_dataset": str(DATA_PATH),
        "random_state": RANDOM_STATE,
        "dataset": summary_dataset,
        "split": {
            "train_rows": int(len(X_train)),
            "test_rows": int(len(X_test)),
            "test_size": 0.20,
            "stratify": "label",
        },
        "evaluation_priority": "macro F1 is prioritized due to class imbalance",
        "smote_applied": False,
        "model_keys": list(models.keys()),
        "best_model": {
            "model": best_model_key,
            "model_display_name": MODEL_DISPLAY_NAMES[best_model_key],
            "selection_metric": "test_f1_macro",
            "test_f1_macro": float(test_df.iloc[0]["f1_macro"]),
            "artifact_path": str(BEST_MODEL_PATH),
            "metadata_path": str(BEST_MODEL_METADATA_PATH),
        },
        "outputs": {
            "summary_json": str(SUMMARY_JSON_PATH),
            "markdown_report": str(REPORT_MD_PATH),
            "cv_results_csv": str(CV_RESULTS_PATH),
            "test_results_csv": str(TEST_RESULTS_PATH),
            "confusion_matrix_figures": {
                key: str(path) for key, path in CONFUSION_MATRIX_PATHS.items()
            },
        },
    }

    metadata = {
        "generated_at": summary["generated_at"],
        "model": best_model_key,
        "model_display_name": MODEL_DISPLAY_NAMES[best_model_key],
        "selection_metric": "test_f1_macro",
        "test_metrics": test_results[best_model_key]["metrics"],
        "pipeline_steps": ["tfidf", "classifier"],
        "input_dataset": str(DATA_PATH),
        "random_state": RANDOM_STATE,
        "note": "Baseline experiment artifact; not final thesis result.",
    }

    SUMMARY_JSON_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    BEST_MODEL_METADATA_PATH.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_markdown_report(summary, cv_df, test_df, test_results, best_model_key)

    print(f"CV results saved to: {CV_RESULTS_PATH}")
    print(f"Test results saved to: {TEST_RESULTS_PATH}")
    print(f"Summary JSON saved to: {SUMMARY_JSON_PATH}")
    print(f"Markdown report saved to: {REPORT_MD_PATH}")
    print(f"Best model saved to: {BEST_MODEL_PATH}")
    print(f"Best model metadata saved to: {BEST_MODEL_METADATA_PATH}")
    print(
        "Best model by test macro F1: "
        f"{MODEL_DISPLAY_NAMES[best_model_key]} "
        f"({summary['best_model']['test_f1_macro']:.4f})"
    )
    return summary


def main() -> None:
    """CLI entrypoint."""
    run_baselines()


if __name__ == "__main__":
    main()
