"""Generate basic figures from the interim MBG crawl dataset."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INTERIM_PATH = Path("data/interim/mbg_crawl_interim.csv")
FIGURES_DIR = Path("outputs/figures")


def infer_clean_text_column(df: pd.DataFrame) -> str:
    """Infer the cleaned text column from an interim DataFrame.

    Args:
        df: Interim dataset.

    Returns:
        Name of the clean text column.

    Raises:
        KeyError: If no supported clean text column exists.
    """
    for column in ["clean_text", "clean_text_basic"]:
        if column in df.columns:
            return column
    raise KeyError("No clean text column found. Expected clean_text or clean_text_basic.")


def top_terms(texts: pd.Series, n_terms: int = 30) -> list[tuple[str, int]]:
    """Calculate top terms with simple whitespace tokenization.

    Args:
        texts: Cleaned text values.
        n_terms: Number of terms to return.

    Returns:
        List of term/count pairs.
    """
    counter: Counter[str] = Counter()
    for text in texts.fillna("").astype(str):
        tokens = [
            token
            for token in text.lower().split()
            if len(token) >= 3
        ]
        counter.update(tokens)
    return counter.most_common(n_terms)


def main() -> None:
    """Load interim data and save required figures."""
    if not INTERIM_PATH.exists():
        raise FileNotFoundError(f"Interim dataset not found: {INTERIM_PATH}")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INTERIM_PATH)
    clean_col = infer_clean_text_column(df)
    clean_text = df[clean_col].fillna("").astype(str)

    lengths = clean_text.str.len()
    plt.figure(figsize=(10, 5))
    plt.hist(lengths, bins=40)
    plt.xlabel("Clean text length")
    plt.ylabel("Frequency")
    plt.title("Clean Text Length Distribution")
    plt.tight_layout()
    length_path = FIGURES_DIR / "01_text_length_distribution_clean.png"
    plt.savefig(length_path, dpi=150)
    plt.close()

    terms = top_terms(clean_text, n_terms=30)
    terms_df = pd.DataFrame(terms, columns=["term", "count"])
    plt.figure(figsize=(10, 8))
    plt.barh(terms_df["term"], terms_df["count"])
    plt.xlabel("Count")
    plt.ylabel("Term")
    plt.title("Top 30 Basic Terms in Clean Text")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    terms_path = FIGURES_DIR / "01_top_terms_basic_clean.png"
    plt.savefig(terms_path, dpi=150)
    plt.close()

    print(f"Saved figure: {length_path}")
    print(f"Saved figure: {terms_path}")


if __name__ == "__main__":
    main()
