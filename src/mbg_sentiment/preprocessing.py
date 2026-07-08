"""Conservative text preprocessing utilities for interim datasets."""

from __future__ import annotations

import html
import re
import unicodedata
from typing import Any

import pandas as pd


URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)
MENTION_PATTERN = re.compile(r"(?<!\w)@\w+")
HASHTAG_PATTERN = re.compile(r"#(\w+)")
RT_PATTERN = re.compile(r"^\s*rt\b[:\s-]*", flags=re.IGNORECASE)
REPEATED_CHAR_PATTERN = re.compile(r"(.)\1{2,}")
PUNCTUATION_NUMBER_PATTERN = re.compile(r"[^A-Za-zÀ-ÿ\s]")
WHITESPACE_PATTERN = re.compile(r"\s+")


def safe_text(value: object) -> str:
    """Convert a value to text safely.

    Args:
        value: Input value that may be text, missing, or another object.

    Returns:
        String value, or an empty string for None/NaN.
    """
    if value is None:
        return ""
    if pd.isna(value):
        return ""
    return str(value)


def remove_urls(text: str) -> str:
    """Remove URL tokens from text.

    Args:
        text: Input text.

    Returns:
        Text without URL tokens.
    """
    return URL_PATTERN.sub(" ", text)


def remove_mentions(text: str) -> str:
    """Remove @username mention tokens.

    Args:
        text: Input text.

    Returns:
        Text without mention tokens.
    """
    return MENTION_PATTERN.sub(" ", text)


def normalize_hashtags(text: str) -> str:
    """Remove hashtag symbols while keeping the hashtag word.

    Args:
        text: Input text.

    Returns:
        Text with hashtags converted from ``#word`` to ``word``.
    """
    return HASHTAG_PATTERN.sub(r"\1", text)


def remove_html_entities(text: str) -> str:
    """Decode common HTML entities.

    Args:
        text: Input text.

    Returns:
        Text with entities such as ``&amp;`` decoded.
    """
    return html.unescape(text)


def remove_rt_prefix(text: str) -> str:
    """Remove a leading retweet marker.

    Args:
        text: Input text.

    Returns:
        Text without a leading ``RT`` or ``rt`` prefix.
    """
    return RT_PATTERN.sub("", text)


def remove_emoji_and_symbols(text: str) -> str:
    """Remove emoji and unusual symbol characters.

    Args:
        text: Input text.

    Returns:
        Text with letters, numbers, punctuation, and whitespace retained while
        Unicode symbol characters are removed.
    """
    cleaned_chars: list[str] = []
    for char in text:
        category = unicodedata.category(char)
        if category.startswith("S"):
            cleaned_chars.append(" ")
        else:
            cleaned_chars.append(char)
    return "".join(cleaned_chars)


def case_fold(text: str) -> str:
    """Lowercase text with casefolding.

    Args:
        text: Input text.

    Returns:
        Case-folded text.
    """
    return text.casefold()


def normalize_repeated_characters(text: str, max_repeat: int = 2) -> str:
    """Limit repeated characters.

    Args:
        text: Input text.
        max_repeat: Maximum repeated occurrences to keep.

    Returns:
        Text with long repeated character runs shortened.
    """
    if max_repeat < 1:
        raise ValueError("max_repeat must be at least 1")

    return REPEATED_CHAR_PATTERN.sub(lambda match: match.group(1) * max_repeat, text)


def remove_punctuation_numbers(text: str) -> str:
    """Remove punctuation and numbers while keeping whitespace.

    Args:
        text: Input text.

    Returns:
        Text containing only alphabetic characters and whitespace.
    """
    return PUNCTUATION_NUMBER_PATTERN.sub(" ", text)


def normalize_whitespace(text: str) -> str:
    """Normalize repeated whitespace.

    Args:
        text: Input text.

    Returns:
        Text stripped at both ends with single spaces between tokens.
    """
    return WHITESPACE_PATTERN.sub(" ", text).strip()


def basic_clean_text(text: object) -> str:
    """Apply the conservative interim text-cleaning pipeline.

    Args:
        text: Raw text-like value.

    Returns:
        Cleaned text suitable for interim data inspection and later labeling.
    """
    cleaned = safe_text(text)
    cleaned = remove_html_entities(cleaned)
    cleaned = remove_rt_prefix(cleaned)
    cleaned = remove_urls(cleaned)
    cleaned = remove_mentions(cleaned)
    cleaned = normalize_hashtags(cleaned)
    cleaned = case_fold(cleaned)
    cleaned = normalize_repeated_characters(cleaned)
    cleaned = remove_emoji_and_symbols(cleaned)
    cleaned = remove_punctuation_numbers(cleaned)
    cleaned = normalize_whitespace(cleaned)
    return cleaned


def tokenize_basic(text: str) -> list[str]:
    """Tokenize text using whitespace splitting.

    Args:
        text: Input text.

    Returns:
        List of non-empty whitespace-separated tokens.
    """
    return [token for token in normalize_whitespace(text).split(" ") if token]


def basic_text_stats(texts: pd.Series) -> dict[str, Any]:
    """Compute basic descriptive statistics for cleaned text.

    Args:
        texts: Series of text values.

    Returns:
        Dictionary with count, empty count, length, and word-count statistics.
    """
    safe_values = texts.apply(safe_text).str.strip()
    lengths = safe_values.str.len()
    word_counts = safe_values.apply(lambda value: len(tokenize_basic(value)))

    return {
        "n_texts": int(len(safe_values)),
        "empty_count": int((safe_values == "").sum()),
        "avg_length": float(lengths.mean()) if not lengths.empty else 0.0,
        "median_length": float(lengths.median()) if not lengths.empty else 0.0,
        "avg_word_count": (
            float(word_counts.mean()) if not word_counts.empty else 0.0
        ),
        "median_word_count": (
            float(word_counts.median()) if not word_counts.empty else 0.0
        ),
    }
