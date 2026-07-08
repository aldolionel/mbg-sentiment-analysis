"""Utilities for creating labeling-ready sentiment datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


TEXT_COL = "clean_text"
USEFUL_METADATA_COLUMNS = [
    "interim_id",
    "source_file",
    "source_sheet",
    "source_row_number",
    "clean_text",
    "clean_text_length",
    "clean_word_count",
]
LABELING_COLUMNS = [
    "label",
    "label_source",
    "label_confidence",
    "annotator_1",
    "annotator_2",
    "adjudicated_label",
    "labeling_notes",
]


def load_interim_dataset(path: str | Path) -> pd.DataFrame:
    """Load an interim dataset from CSV.

    Args:
        path: Path to the interim CSV dataset.

    Returns:
        Loaded DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file suffix is unsupported.
    """
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Interim dataset not found: {dataset_path}")
    if dataset_path.suffix.lower() != ".csv":
        raise ValueError(f"Expected CSV interim dataset, got: {dataset_path}")
    return pd.read_csv(dataset_path)


def validate_interim_columns(
    df: pd.DataFrame,
    text_col: str = TEXT_COL,
) -> None:
    """Validate required interim dataset columns.

    Args:
        df: Interim DataFrame.
        text_col: Name of the cleaned text column.

    Raises:
        ValueError: If a required column is missing.
    """
    required_columns = {text_col}
    missing_columns = sorted(required_columns.difference(df.columns))
    if missing_columns:
        raise ValueError(
            "Missing required interim column(s): "
            + ", ".join(missing_columns)
        )


def deduplicate_by_clean_text(
    df: pd.DataFrame,
    text_col: str = TEXT_COL,
) -> pd.DataFrame:
    """Remove exact duplicate clean text values.

    The first occurrence is retained. Only useful metadata columns are
    preserved when present.

    Args:
        df: Interim DataFrame.
        text_col: Name of the cleaned text column.

    Returns:
        Deduplicated DataFrame.
    """
    validate_interim_columns(df, text_col=text_col)
    keep_columns = [
        column for column in USEFUL_METADATA_COLUMNS if column in df.columns
    ]
    if text_col not in keep_columns:
        keep_columns.append(text_col)

    dedup_df = (
        df.loc[:, keep_columns]
        .drop_duplicates(subset=[text_col], keep="first")
        .reset_index(drop=True)
    )
    return dedup_df


def add_labeling_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add empty columns needed for manual or assisted labeling.

    Args:
        df: DataFrame to extend.

    Returns:
        Copy of the DataFrame with empty labeling columns.
    """
    labeled_df = df.copy()
    for column in LABELING_COLUMNS:
        if column not in labeled_df.columns:
            labeled_df[column] = ""
    return labeled_df


def _random_sample(
    df: pd.DataFrame,
    sample_size: int,
    random_state: int,
) -> pd.DataFrame:
    """Return a random sample with at most sample_size rows."""
    n_rows = min(sample_size, len(df))
    return df.sample(n=n_rows, random_state=random_state).reset_index(drop=True)


def _stratified_length_sample(
    df: pd.DataFrame,
    sample_size: int,
    random_state: int,
    length_bins: int,
) -> pd.DataFrame:
    """Sample proportionally from clean-text-length bins."""
    working_df = df.copy()
    working_df["_length_bin"] = pd.qcut(
        working_df["clean_text_length"],
        q=length_bins,
        duplicates="drop",
    )
    if working_df["_length_bin"].isna().all():
        raise ValueError("Length binning produced only missing bins.")

    target_size = min(sample_size, len(working_df))
    sampled_parts: list[pd.DataFrame] = []
    sampled_indexes: set[int] = set()
    grouped = working_df.groupby("_length_bin", observed=True)
    remaining_slots = target_size

    for _, group in grouped:
        if remaining_slots <= 0:
            break
        proportional_n = round(len(group) / len(working_df) * target_size)
        group_n = max(1, proportional_n)
        group_n = min(group_n, len(group), remaining_slots)
        group_sample = group.sample(n=group_n, random_state=random_state)
        sampled_indexes.update(group_sample.index.tolist())
        sampled_parts.append(group_sample)
        remaining_slots -= group_n

    sampled_df = pd.concat(sampled_parts, ignore_index=True)

    if len(sampled_df) < target_size:
        remaining_df = working_df.drop(index=list(sampled_indexes), errors="ignore")
        needed = target_size - len(sampled_df)
        if not remaining_df.empty:
            sampled_df = pd.concat(
                [
                    sampled_df,
                    remaining_df.sample(
                        n=min(needed, len(remaining_df)),
                        random_state=random_state,
                    ),
                ],
                ignore_index=True,
            )

    if len(sampled_df) > target_size:
        sampled_df = sampled_df.sample(
            n=target_size,
            random_state=random_state,
        )

    return sampled_df.drop(columns=["_length_bin"]).reset_index(drop=True)


def create_labeling_sample(
    df: pd.DataFrame,
    sample_size: int = 1000,
    random_state: int = 42,
    length_bins: int = 5,
) -> pd.DataFrame:
    """Create a representative labeling sample.

    Sampling prefers proportional clean-text-length bins when available. If
    binning fails, a regular random sample is used.

    Args:
        df: Labeling-ready DataFrame.
        sample_size: Requested sample size.
        random_state: Random seed.
        length_bins: Number of length bins for stratification.

    Returns:
        Sample DataFrame with a `sample_id` column.
    """
    if sample_size < 1:
        raise ValueError("sample_size must be at least 1")
    if df.empty:
        sample_df = df.copy()
    elif "clean_text_length" in df.columns and df["clean_text_length"].nunique() > 1:
        try:
            sample_df = _stratified_length_sample(
                df,
                sample_size=sample_size,
                random_state=random_state,
                length_bins=length_bins,
            )
        except Exception:
            sample_df = _random_sample(df, sample_size, random_state)
    else:
        sample_df = _random_sample(df, sample_size, random_state)

    sample_df = sample_df.reset_index(drop=True)
    sample_df.insert(
        0,
        "sample_id",
        [f"label_sample_{index:04d}" for index in range(1, len(sample_df) + 1)],
    )
    return sample_df


def export_for_labeling(df: pd.DataFrame, path: str | Path) -> None:
    """Export a labeling dataset to CSV or XLSX.

    Args:
        df: DataFrame to export.
        path: Output path with `.csv` or `.xlsx` suffix.

    Raises:
        ValueError: If the output suffix is unsupported.
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()

    if suffix == ".csv":
        df.to_csv(output_path, index=False, encoding="utf-8")
        return
    if suffix == ".xlsx":
        df.to_excel(output_path, index=False)
        return

    raise ValueError(f"Unsupported output format: {output_path}")


def compute_labeling_dataset_summary(
    df_before: pd.DataFrame,
    df_after: pd.DataFrame,
    sample_df: pd.DataFrame,
) -> dict[str, Any]:
    """Compute summary statistics for labeling dataset preparation.

    Args:
        df_before: Interim dataset before deduplication.
        df_after: Labeling-ready dataset after deduplication.
        sample_df: Labeling sample.

    Returns:
        Summary dictionary.
    """
    rows_before = int(len(df_before))
    rows_after = int(len(df_after))
    duplicates_removed = rows_before - rows_after
    duplicate_rate = (
        duplicates_removed / rows_before if rows_before > 0 else 0.0
    )

    return {
        "rows_before": rows_before,
        "rows_after_dedup": rows_after,
        "duplicates_removed": int(duplicates_removed),
        "duplicate_removal_rate": float(duplicate_rate),
        "sample_rows": int(len(sample_df)),
        "avg_clean_text_length": float(df_after["clean_text_length"].mean())
        if "clean_text_length" in df_after.columns and not df_after.empty
        else 0.0,
        "median_clean_text_length": float(df_after["clean_text_length"].median())
        if "clean_text_length" in df_after.columns and not df_after.empty
        else 0.0,
        "avg_clean_word_count": float(df_after["clean_word_count"].mean())
        if "clean_word_count" in df_after.columns and not df_after.empty
        else 0.0,
        "median_clean_word_count": float(df_after["clean_word_count"].median())
        if "clean_word_count" in df_after.columns and not df_after.empty
        else 0.0,
    }
