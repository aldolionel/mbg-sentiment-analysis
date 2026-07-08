"""Reusable modeling utilities for MBG sentiment baseline experiments."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import LogisticRegression


RANDOM_STATE = 42
ALLOWED_LABELS = {"positif", "negatif", "netral"}
REQUIRED_COLUMNS = ["sample_id", "clean_text", "label"]
METRIC_SCORING = {
    "accuracy": "accuracy",
    "precision_macro": make_scorer(
        precision_score,
        average="macro",
        zero_division=0,
    ),
    "recall_macro": make_scorer(
        recall_score,
        average="macro",
        zero_division=0,
    ),
    "f1_macro": make_scorer(f1_score, average="macro", zero_division=0),
    "f1_weighted": make_scorer(f1_score, average="weighted", zero_division=0),
}


def load_labeled_dataset(path: str | Path) -> pd.DataFrame:
    """Load and validate the final labeled modeling dataset.

    Args:
        path: CSV path containing sample_id, clean_text, and label.

    Returns:
        Validated DataFrame. The ``attrs["dropped_missing_count"]`` value
        reports any rows dropped for missing clean_text or label.

    Raises:
        FileNotFoundError: If the CSV does not exist.
        ValueError: If required columns are missing or labels are invalid.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Labeled dataset not found: {file_path}")

    df = pd.read_csv(file_path)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    working = df.copy()
    missing_mask = (
        working["clean_text"].isna()
        | working["label"].isna()
        | working["clean_text"].astype(str).str.strip().eq("")
        | working["label"].astype(str).str.strip().eq("")
    )
    dropped_missing_count = int(missing_mask.sum())
    if dropped_missing_count:
        working = working.loc[~missing_mask].copy()

    working["clean_text"] = working["clean_text"].astype(str).str.strip()
    working["label"] = working["label"].astype(str).str.strip().str.lower()

    invalid_labels = sorted(set(working["label"]) - ALLOWED_LABELS)
    if invalid_labels:
        raise ValueError(
            "Invalid labels found. "
            f"Expected only {sorted(ALLOWED_LABELS)}, found {invalid_labels}"
        )

    working.attrs["dropped_missing_count"] = dropped_missing_count
    return working


def build_tfidf_vectorizer() -> TfidfVectorizer:
    """Build the default TF-IDF vectorizer for baseline experiments."""
    return TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,
    )


def get_models() -> dict[str, Any]:
    """Return baseline classifiers for sentiment classification."""
    return {
        "multinomial_nb": MultinomialNB(),
        "logistic_regression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "linear_svm": LinearSVC(
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "rbf_svm": SVC(
            kernel="rbf",
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
    }


def default_cv() -> StratifiedKFold:
    """Create the default 5-fold stratified cross-validator."""
    return StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)


def evaluate_model_cv(
    model: Any,
    X: pd.Series,
    y: pd.Series,
    cv: StratifiedKFold | None = None,
) -> dict[str, dict[str, float]]:
    """Evaluate a model with stratified cross-validation.

    Args:
        model: Scikit-learn estimator or pipeline.
        X: Text features or feature matrix.
        y: Labels.
        cv: Optional cross-validator. Defaults to 5-fold stratified CV.

    Returns:
        Nested dict containing mean and standard deviation for each metric.
    """
    splitter = default_cv() if cv is None else cv
    results = cross_validate(
        model,
        X,
        y,
        cv=splitter,
        scoring=METRIC_SCORING,
        n_jobs=None,
        error_score="raise",
    )

    summary: dict[str, dict[str, float]] = {}
    for metric in METRIC_SCORING:
        scores = results[f"test_{metric}"]
        summary[metric] = {
            "mean": float(scores.mean()),
            "std": float(scores.std()),
        }
    return summary


def train_test_evaluate(
    model: Any,
    X_train: pd.Series,
    X_test: pd.Series,
    y_train: pd.Series,
    y_test: pd.Series,
) -> dict[str, Any]:
    """Fit a model and evaluate it on a held-out test split."""
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    labels = sorted(ALLOWED_LABELS)

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
            labels=labels,
            output_dict=True,
            zero_division=0,
        ),
        "classification_report_text": classification_report(
            y_test,
            y_pred,
            labels=labels,
            zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=labels),
        "labels": labels,
        "predictions": y_pred,
    }
