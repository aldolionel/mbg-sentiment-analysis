"""Run SVM hyperparameter tuning and imbalance experiments for MBG sentiment."""

from __future__ import annotations

import json
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC, SVC


warnings.filterwarnings(
    "ignore",
    message="The `probability` parameter was deprecated",
    category=FutureWarning,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


RANDOM_STATE = 42
ALLOWED_LABELS = {"positif", "negatif", "netral"}
LABEL_ORDER = ["negatif", "netral", "positif"]
REQUIRED_COLUMNS = ["sample_id", "clean_text", "label"]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "mbg_labeled_sample_1000.csv"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
MODELS_DIR = PROJECT_ROOT / "outputs" / "models"

REPORT_MD_PATH = REPORTS_DIR / "15_svm_tuning_report.md"
SUMMARY_JSON_PATH = REPORTS_DIR / "15_svm_tuning_summary.json"
ALL_CV_RESULTS_PATH = REPORTS_DIR / "15_svm_tuning_all_cv_results.csv"
TEST_RESULTS_PATH = REPORTS_DIR / "15_svm_tuning_test_results.csv"
BEST_MODEL_PATH = MODELS_DIR / "best_svm_model.joblib"
BEST_MODEL_METADATA_PATH = MODELS_DIR / "best_svm_model_metadata.json"

BASELINE_TEST_RESULTS_PATH = REPORTS_DIR / "14_modeling_test_results.csv"

EXPERIMENT_DISPLAY_NAMES = {
    "tuned_linearsvc": "Tuned LinearSVC",
    "tuned_svc_linear": "Tuned SVC Linear Kernel",
    "tuned_svc_rbf": "Tuned SVC RBF Kernel",
}

CONFUSION_MATRIX_PATHS = {
    "tuned_linearsvc": FIGURES_DIR / "15_confusion_matrix_tuned_linearsvc.png",
    "tuned_svc_linear": FIGURES_DIR / "15_confusion_matrix_tuned_svc_linear.png",
    "tuned_svc_rbf": FIGURES_DIR / "15_confusion_matrix_tuned_svc_rbf.png",
}


def ensure_output_dirs() -> None:
    """Create output directories for reports, figures, and model artifacts."""
    for directory in [REPORTS_DIR, FIGURES_DIR, MODELS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def validate_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load and strictly validate the final labeled dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Labeled dataset not found: {path}")

    df = pd.read_csv(path)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    if len(df) != 1000:
        raise ValueError(f"Expected 1000 rows, found {len(df)}")

    clean_text = df["clean_text"]
    labels = df["label"]
    if clean_text.isna().any() or clean_text.astype(str).str.strip().eq("").any():
        raise ValueError("Missing or empty clean_text values found")
    if labels.isna().any() or labels.astype(str).str.strip().eq("").any():
        raise ValueError("Missing or empty label values found")

    validated = df.copy()
    validated["clean_text"] = validated["clean_text"].astype(str).str.strip()
    validated["label"] = validated["label"].astype(str).str.strip().str.lower()

    invalid_labels = sorted(set(validated["label"]) - ALLOWED_LABELS)
    if invalid_labels:
        raise ValueError(
            f"Invalid labels found: {invalid_labels}. "
            f"Allowed labels: {sorted(ALLOWED_LABELS)}"
        )
    return validated


def dataset_summary(df: pd.DataFrame) -> dict[str, Any]:
    """Build dataset and label-balance summary."""
    counts = df["label"].value_counts().reindex(LABEL_ORDER)
    percentages = (counts / len(df) * 100).round(2)
    return {
        "total_rows": int(len(df)),
        "label_distribution": {
            str(label): int(count) for label, count in counts.items()
        },
        "label_percentage": {
            str(label): float(percent) for label, percent in percentages.items()
        },
    }


def make_pipeline(classifier: Any) -> Pipeline:
    """Create a TF-IDF + SVM pipeline."""
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer()),
            ("classifier", classifier),
        ]
    )


def experiment_configs() -> dict[str, dict[str, Any]]:
    """Return SVM tuning experiment definitions."""
    linear_grid = {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__min_df": [1, 2, 3],
        "tfidf__max_df": [0.90, 0.95],
        "tfidf__sublinear_tf": [True],
        "classifier__C": [0.1, 0.5, 1, 2, 5],
        "classifier__class_weight": [None, "balanced"],
    }
    return {
        "tuned_linearsvc": {
            "pipeline": make_pipeline(LinearSVC(random_state=RANDOM_STATE, max_iter=5000)),
            "param_grid": linear_grid,
        },
        "tuned_svc_linear": {
            "pipeline": make_pipeline(
                SVC(kernel="linear", probability=False, random_state=RANDOM_STATE)
            ),
            "param_grid": linear_grid,
        },
        "tuned_svc_rbf": {
            "pipeline": make_pipeline(
                SVC(kernel="rbf", probability=False, random_state=RANDOM_STATE)
            ),
            "param_grid": {
                "tfidf__ngram_range": [(1, 1), (1, 2)],
                "tfidf__min_df": [1, 2],
                "tfidf__max_df": [0.95],
                "tfidf__sublinear_tf": [True],
                "classifier__C": [0.5, 1, 2, 5],
                "classifier__gamma": ["scale", 0.1, 0.01],
                "classifier__class_weight": [None, "balanced"],
            },
        },
    }


def evaluate_estimator(
    estimator: Any,
    X_test: pd.Series,
    y_test: pd.Series,
) -> dict[str, Any]:
    """Evaluate a fitted estimator on the test split."""
    y_pred = estimator.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision_macro": float(
            precision_score(y_test, y_pred, average="macro", zero_division=0)
        ),
        "recall_macro": float(
            recall_score(y_test, y_pred, average="macro", zero_division=0)
        ),
        "f1_macro": float(f1_score(y_test, y_pred, average="macro", zero_division=0)),
        "f1_weighted": float(
            f1_score(y_test, y_pred, average="weighted", zero_division=0)
        ),
    }
    return {
        "metrics": metrics,
        "classification_report": classification_report(
            y_test,
            y_pred,
            labels=LABEL_ORDER,
            output_dict=True,
            zero_division=0,
        ),
        "classification_report_text": classification_report(
            y_test,
            y_pred,
            labels=LABEL_ORDER,
            zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=LABEL_ORDER),
        "labels": LABEL_ORDER,
    }


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


def sanitize_for_json(value: Any) -> Any:
    """Convert numpy/scikit-learn values into JSON-safe structures."""
    if isinstance(value, dict):
        return {str(key): sanitize_for_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [sanitize_for_json(item) for item in value]
    if hasattr(value, "item"):
        return value.item()
    return value


def is_not_missing(value: Any) -> bool:
    """Return True for values that should be retained from cv_results params."""
    if isinstance(value, (list, tuple)):
        return True
    return bool(pd.notna(value))


def dataframe_markdown(df: pd.DataFrame, float_format: str = ".4f") -> str:
    """Convert a DataFrame to Markdown with a plain-text fallback."""
    try:
        return df.to_markdown(index=False, floatfmt=float_format)
    except ImportError:
        return df.to_string(index=False)


def load_baseline_references() -> dict[str, Any]:
    """Load previous baseline metrics if available."""
    if not BASELINE_TEST_RESULTS_PATH.exists():
        return {"available": False}

    baseline_df = pd.read_csv(BASELINE_TEST_RESULTS_PATH)
    references: dict[str, Any] = {"available": True, "path": str(BASELINE_TEST_RESULTS_PATH)}
    for model_key in ["linear_svm", "logistic_regression"]:
        match = baseline_df.loc[baseline_df["model"] == model_key]
        if not match.empty:
            references[model_key] = match.iloc[0].to_dict()
    return references


def summarize_class_weight_results(
    all_cv_df: pd.DataFrame,
) -> dict[str, Any]:
    """Compare the best CV result for class_weight=None and balanced SVMs."""
    comparisons: dict[str, Any] = {}
    for class_weight, key in [(None, "none"), ("balanced", "balanced")]:
        if class_weight is None:
            subset = all_cv_df[all_cv_df["param_classifier__class_weight"].isna()]
        else:
            subset = all_cv_df[
                all_cv_df["param_classifier__class_weight"].astype(str) == class_weight
            ]
        if subset.empty:
            continue

        best_row = subset.sort_values("mean_test_score", ascending=False).iloc[0]
        experiment = str(best_row["experiment"])
        params = {
            column.removeprefix("param_"): best_row[column]
            for column in subset.columns
            if column.startswith("param_") and is_not_missing(best_row[column])
        }

        comparisons[key] = {
            "experiment": experiment,
            "experiment_display_name": EXPERIMENT_DISPLAY_NAMES[experiment],
            "best_cv_macro_f1": float(best_row["mean_test_score"]),
            "cv_macro_f1_std": float(best_row["std_test_score"]),
            "cv_rank": int(best_row["rank_test_score"]),
            "best_params": sanitize_for_json(params),
        }
    return comparisons


def write_markdown_report(
    summary: dict[str, Any],
    test_df: pd.DataFrame,
    best_params_df: pd.DataFrame,
    class_weight_df: pd.DataFrame,
    test_results: dict[str, dict[str, Any]],
) -> None:
    """Write the SVM tuning report."""
    baseline = summary["baseline_reference"]
    best = summary["best_svm"]
    lines = [
        "# 15 SVM Tuning Report",
        "",
        "## Scope",
        "This report documents SVM-focused hyperparameter tuning and class imbalance experiments for MBG sentiment classification using TF-IDF features. These are baseline/tuning experiments, not final thesis conclusions.",
        "No raw files were modified, no data was relabeled, no baseline reports were overwritten, and SMOTE was not applied.",
        "",
        "## Dataset Summary",
        f"- input dataset: `{summary['input_dataset']}`",
        f"- total rows: {summary['dataset']['total_rows']}",
        "",
        "### Label Distribution",
    ]
    for label, count in summary["dataset"]["label_distribution"].items():
        percent = summary["dataset"]["label_percentage"][label]
        lines.append(f"- {label}: {count} ({percent:.2f}%)")

    lines.extend(
        [
            "",
            "## Evaluation Priority",
            "Macro F1 is prioritized because the labels are imbalanced and the minority `negatif` class should influence model selection. Accuracy is reported, but not used alone as the main conclusion.",
            "",
            "## Experiment Setup",
            f"- random_state: {RANDOM_STATE}",
            "- train/test split: 80/20, stratified by label",
            "- tuning: GridSearchCV with 5-fold StratifiedKFold and scoring=`f1_macro`",
            "- model focus: LinearSVC, SVC with linear kernel, and SVC with RBF kernel",
            "- imbalance comparison: class_weight=None versus class_weight='balanced' through the tuning grid",
            "",
            "## Baseline References",
        ]
    )
    if baseline.get("available"):
        linear_ref = baseline.get("linear_svm")
        logistic_ref = baseline.get("logistic_regression")
        if linear_ref:
            lines.append(
                "- baseline Linear SVM test macro F1: "
                f"{linear_ref['f1_macro']:.4f}"
            )
        if logistic_ref:
            lines.append(
                "- baseline Logistic Regression test macro F1: "
                f"{logistic_ref['f1_macro']:.4f}"
            )
    else:
        lines.append("- previous baseline test results were not available")

    lines.extend(
        [
            "",
            "## Best Parameters Per Experiment",
            dataframe_markdown(best_params_df),
            "",
            "## Test Metrics Per Experiment",
            dataframe_markdown(test_df),
            "",
            "## Class Weight Comparison",
            dataframe_markdown(class_weight_df) if not class_weight_df.empty else "No class_weight comparison was available.",
            "",
            "## Best Tuned SVM",
            f"- selected by test macro F1: {best['experiment_display_name']} (`{best['experiment']}`)",
            f"- test macro F1: {best['test_f1_macro']:.4f}",
            f"- artifact: `{BEST_MODEL_PATH}`",
            "",
            "## Negative-Class Performance",
        ]
    )
    for experiment, result in test_results.items():
        neg = result["classification_report"]["negatif"]
        lines.append(
            f"- {EXPERIMENT_DISPLAY_NAMES[experiment]}: "
            f"precision={neg['precision']:.4f}, recall={neg['recall']:.4f}, "
            f"F1={neg['f1-score']:.4f}, support={int(neg['support'])}"
        )

    lines.extend(["", "## Logistic Regression Baseline Warning"])
    warning = summary["comparison_to_logistic_regression_baseline"]
    if warning["baseline_available"]:
        if warning["tuned_svm_underperforms"]:
            lines.append(
                "- WARNING: the best tuned SVM still underperforms the previous Logistic Regression baseline on test macro F1 "
                f"({best['test_f1_macro']:.4f} vs {warning['logistic_regression_f1_macro']:.4f})."
            )
        else:
            lines.append(
                "- The best tuned SVM matches or exceeds the previous Logistic Regression baseline on test macro F1 "
                f"({best['test_f1_macro']:.4f} vs {warning['logistic_regression_f1_macro']:.4f})."
            )
    else:
        lines.append("- Logistic Regression baseline was not available for comparison.")

    lines.extend(["", "## Classification Reports"])
    for experiment, result in test_results.items():
        lines.extend(
            [
                "",
                f"### {EXPERIMENT_DISPLAY_NAMES[experiment]}",
                "```text",
                result["classification_report_text"],
                "```",
                f"- confusion matrix figure: `{CONFUSION_MATRIX_PATHS[experiment]}`",
            ]
        )

    REPORT_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def run_svm_tuning_experiments() -> dict[str, Any]:
    """Run SVM tuning experiments and save all requested artifacts."""
    ensure_output_dirs()
    df = validate_dataset(DATA_PATH)
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

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_frames: list[pd.DataFrame] = []
    test_rows: list[dict[str, Any]] = []
    best_params_rows: list[dict[str, Any]] = []
    test_results: dict[str, dict[str, Any]] = {}
    best_estimators: dict[str, Any] = {}

    for experiment, config in experiment_configs().items():
        print(f"Tuning {EXPERIMENT_DISPLAY_NAMES[experiment]}...")
        grid_search = GridSearchCV(
            estimator=config["pipeline"],
            param_grid=config["param_grid"],
            scoring="f1_macro",
            cv=cv,
            n_jobs=1,
            refit=True,
            return_train_score=True,
            verbose=0,
        )
        grid_search.fit(X_train, y_train)

        cv_df = pd.DataFrame(grid_search.cv_results_)
        cv_df.insert(0, "experiment", experiment)
        cv_df.insert(1, "experiment_display_name", EXPERIMENT_DISPLAY_NAMES[experiment])
        cv_frames.append(cv_df)

        test_result = evaluate_estimator(grid_search.best_estimator_, X_test, y_test)
        test_results[experiment] = test_result
        best_estimators[experiment] = grid_search.best_estimator_

        test_row = {
            "experiment": experiment,
            "experiment_display_name": EXPERIMENT_DISPLAY_NAMES[experiment],
            "best_cv_f1_macro": float(grid_search.best_score_),
        }
        test_row.update(test_result["metrics"])
        test_rows.append(test_row)

        best_params_rows.append(
            {
                "experiment": experiment,
                "experiment_display_name": EXPERIMENT_DISPLAY_NAMES[experiment],
                "best_cv_f1_macro": float(grid_search.best_score_),
                "best_params": json.dumps(
                    sanitize_for_json(grid_search.best_params_),
                    ensure_ascii=False,
                    sort_keys=True,
                ),
            }
        )

        save_confusion_matrix(
            test_result["confusion_matrix"],
            test_result["labels"],
            f"{EXPERIMENT_DISPLAY_NAMES[experiment]} Confusion Matrix",
            CONFUSION_MATRIX_PATHS[experiment],
        )

    all_cv_df = pd.concat(cv_frames, ignore_index=True)
    all_cv_df.to_csv(ALL_CV_RESULTS_PATH, index=False, encoding="utf-8")

    test_df = pd.DataFrame(test_rows).sort_values("f1_macro", ascending=False)
    test_df.to_csv(TEST_RESULTS_PATH, index=False, encoding="utf-8")

    best_params_df = pd.DataFrame(best_params_rows).sort_values(
        "best_cv_f1_macro",
        ascending=False,
    )
    best_experiment = str(test_df.iloc[0]["experiment"])
    best_test_result = test_results[best_experiment]
    joblib.dump(best_estimators[best_experiment], BEST_MODEL_PATH)

    class_weight_comparison = summarize_class_weight_results(all_cv_df)
    class_weight_rows = []
    for key, value in class_weight_comparison.items():
        class_weight_rows.append(
            {
            "class_weight": key,
            "experiment": value["experiment"],
            "experiment_display_name": value["experiment_display_name"],
            "best_cv_f1_macro": value["best_cv_macro_f1"],
            "cv_macro_f1_std": value["cv_macro_f1_std"],
            "cv_rank": value["cv_rank"],
            }
        )
    class_weight_df = pd.DataFrame(class_weight_rows).sort_values(
        "best_cv_f1_macro",
        ascending=False,
    ) if class_weight_rows else pd.DataFrame()

    baseline_reference = load_baseline_references()
    logistic_ref = baseline_reference.get("logistic_regression", {})
    logistic_f1 = logistic_ref.get("f1_macro")
    comparison_to_logistic = {
        "baseline_available": logistic_f1 is not None,
        "logistic_regression_f1_macro": float(logistic_f1) if logistic_f1 is not None else None,
        "tuned_svm_underperforms": (
            bool(float(test_df.iloc[0]["f1_macro"]) < float(logistic_f1))
            if logistic_f1 is not None
            else None
        ),
    }

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
        "experiments": {
            experiment: {
                "display_name": EXPERIMENT_DISPLAY_NAMES[experiment],
                "best_cv_macro_f1": float(
                    best_params_df.loc[
                        best_params_df["experiment"] == experiment,
                        "best_cv_f1_macro",
                    ].iloc[0]
                ),
                "best_params": sanitize_for_json(
                    json.loads(
                        best_params_df.loc[
                            best_params_df["experiment"] == experiment,
                            "best_params",
                        ].iloc[0]
                    )
                ),
                "test_metrics": test_results[experiment]["metrics"],
                "negative_class": test_results[experiment]["classification_report"][
                    "negatif"
                ],
                "confusion_matrix_figure": str(CONFUSION_MATRIX_PATHS[experiment]),
            }
            for experiment in EXPERIMENT_DISPLAY_NAMES
        },
        "class_weight_comparison": sanitize_for_json(class_weight_comparison),
        "baseline_reference": sanitize_for_json(baseline_reference),
        "comparison_to_logistic_regression_baseline": comparison_to_logistic,
        "best_svm": {
            "experiment": best_experiment,
            "experiment_display_name": EXPERIMENT_DISPLAY_NAMES[best_experiment],
            "selection_metric": "test_f1_macro",
            "test_f1_macro": float(test_df.iloc[0]["f1_macro"]),
            "test_metrics": best_test_result["metrics"],
            "best_params": sanitize_for_json(
                json.loads(
                    best_params_df.loc[
                        best_params_df["experiment"] == best_experiment,
                        "best_params",
                    ].iloc[0]
                )
            ),
            "artifact_path": str(BEST_MODEL_PATH),
            "metadata_path": str(BEST_MODEL_METADATA_PATH),
        },
        "outputs": {
            "markdown_report": str(REPORT_MD_PATH),
            "summary_json": str(SUMMARY_JSON_PATH),
            "all_cv_results_csv": str(ALL_CV_RESULTS_PATH),
            "test_results_csv": str(TEST_RESULTS_PATH),
            "confusion_matrix_figures": {
                key: str(path) for key, path in CONFUSION_MATRIX_PATHS.items()
            },
            "best_model": str(BEST_MODEL_PATH),
            "best_model_metadata": str(BEST_MODEL_METADATA_PATH),
        },
    }

    metadata = {
        "generated_at": summary["generated_at"],
        "experiment": best_experiment,
        "experiment_display_name": EXPERIMENT_DISPLAY_NAMES[best_experiment],
        "selection_metric": "test_f1_macro",
        "test_metrics": best_test_result["metrics"],
        "best_params": summary["best_svm"]["best_params"],
        "pipeline_steps": ["tfidf", "classifier"],
        "input_dataset": str(DATA_PATH),
        "random_state": RANDOM_STATE,
        "note": "SVM tuning experiment artifact; not final thesis result.",
    }

    SUMMARY_JSON_PATH.write_text(
        json.dumps(sanitize_for_json(summary), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    BEST_MODEL_METADATA_PATH.write_text(
        json.dumps(sanitize_for_json(metadata), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_markdown_report(
        sanitize_for_json(summary),
        test_df,
        best_params_df,
        class_weight_df,
        test_results,
    )

    print(f"All CV results saved to: {ALL_CV_RESULTS_PATH}")
    print(f"Test results saved to: {TEST_RESULTS_PATH}")
    print(f"Summary JSON saved to: {SUMMARY_JSON_PATH}")
    print(f"Markdown report saved to: {REPORT_MD_PATH}")
    print(f"Best SVM saved to: {BEST_MODEL_PATH}")
    print(f"Best SVM metadata saved to: {BEST_MODEL_METADATA_PATH}")
    print(
        "Best tuned SVM by test macro F1: "
        f"{EXPERIMENT_DISPLAY_NAMES[best_experiment]} "
        f"({summary['best_svm']['test_f1_macro']:.4f})"
    )
    return sanitize_for_json(summary)


def main() -> None:
    """CLI entrypoint."""
    run_svm_tuning_experiments()


if __name__ == "__main__":
    main()
