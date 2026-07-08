"""Create annotation batches and prompts for MBG sentiment labeling."""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


REQUIRED_SAMPLE_COLUMNS = ["sample_id", "clean_text"]
BATCH_COLUMNS = ["sample_id", "clean_text", "label", "labeling_notes"]
ALLOWED_LABELS = ["positif", "negatif", "netral"]


def load_labeling_sample(path: str | Path) -> pd.DataFrame:
    """Load a labeling sample CSV or XLSX file.

    Args:
        path: Path to the labeling sample.

    Returns:
        Loaded DataFrame.

    Raises:
        FileNotFoundError: If the sample file does not exist.
        ValueError: If the suffix is unsupported.
    """
    sample_path = Path(path)
    if not sample_path.exists():
        raise FileNotFoundError(f"Labeling sample not found: {sample_path}")

    suffix = sample_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(sample_path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(sample_path)

    raise ValueError(f"Unsupported sample file format: {sample_path}")


def validate_sample(df: pd.DataFrame) -> None:
    """Validate required columns in a labeling sample.

    Args:
        df: Labeling sample DataFrame.

    Raises:
        ValueError: If required columns are missing.
    """
    missing_columns = [
        column for column in REQUIRED_SAMPLE_COLUMNS if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            "Missing required sample column(s): "
            + ", ".join(missing_columns)
        )


def create_annotation_batches(
    df: pd.DataFrame,
    batch_size: int = 50,
    output_dir: str | Path = "data/processed/annotation_batches",
) -> list[Path]:
    """Split a labeling sample into sequential CSV annotation batches.

    Args:
        df: Labeling sample DataFrame.
        batch_size: Number of rows per batch.
        output_dir: Directory where batch CSV files are written.

    Returns:
        List of written batch paths.

    Raises:
        ValueError: If `batch_size` is invalid or sample columns are missing.
    """
    validate_sample(df)
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")

    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    n_batches = math.ceil(len(df) / batch_size)
    batch_paths: list[Path] = []

    for batch_index in range(n_batches):
        start = batch_index * batch_size
        end = start + batch_size
        batch_df = df.iloc[start:end].copy()
        batch_export = pd.DataFrame(
            {
                "sample_id": batch_df["sample_id"].astype(str),
                "clean_text": batch_df["clean_text"].fillna("").astype(str),
                "label": "",
                "labeling_notes": "",
            }
        )
        batch_path = target_dir / f"annotation_batch_{batch_index + 1:03d}.csv"
        batch_export.to_csv(batch_path, index=False, encoding="utf-8")
        batch_paths.append(batch_path)

    return batch_paths


def _escape_markdown_table(value: object) -> str:
    """Escape text for compact Markdown table cells."""
    text = "" if pd.isna(value) else str(value)
    text = text.replace("\n", " ").replace("\r", " ")
    text = text.replace("|", "\\|")
    return " ".join(text.split())


def create_batch_prompt(batch_df: pd.DataFrame, batch_id: str) -> str:
    """Create a Markdown prompt for AI-assisted batch labeling.

    Args:
        batch_df: Annotation batch DataFrame.
        batch_id: Batch identifier used in the prompt title.

    Returns:
        Markdown prompt string.
    """
    validate_sample(batch_df)
    rows = [
        "| sample_id | clean_text |",
        "| --- | --- |",
    ]
    for _, row in batch_df.iterrows():
        rows.append(
            "| "
            f"{_escape_markdown_table(row['sample_id'])} | "
            f"{_escape_markdown_table(row['clean_text'])} |"
        )

    allowed = ", ".join(f"`{label}`" for label in ALLOWED_LABELS)
    table = "\n".join(rows)
    return f"""# AI-Assisted Sentiment Labeling Prompt - {batch_id}

Anda membantu memberi label sentimen publik terhadap Program Makan Bergizi Gratis (MBG) pada teks media sosial.

Gunakan hanya label berikut: {allowed}.

Aturan penting:
- Labeli sentimen terhadap Program MBG, bukan terhadap tokoh politik kecuali langsung terkait MBG.
- Jika teks memuat sentimen positif dan negatif, pilih sentimen yang paling dominan.
- Jika teks berupa informasi, berita, pertanyaan tanpa polaritas jelas, ambigu, atau Anda tidak yakin, gunakan `netral`.
- Sarkasme diberi label sesuai makna tersirat.
- Jangan mengubah `sample_id`.
- Jangan menambah baris.
- Jangan menghapus baris.
- Jangan mengisi label selain `positif`, `negatif`, atau `netral`.

Kembalikan jawaban hanya sebagai CSV block dengan kolom:

```csv
sample_id,label,labeling_notes
```

Isi `labeling_notes` secara singkat jika perlu. Jika tidak perlu catatan, kosongkan.

## Rows

{table}
"""


def export_batch_prompts(
    batch_paths: list[Path],
    output_dir: str | Path = "data/processed/annotation_prompts",
) -> list[Path]:
    """Create one Markdown prompt for each annotation batch CSV.

    Args:
        batch_paths: Paths to batch CSV files.
        output_dir: Directory where prompt Markdown files are written.

    Returns:
        List of written prompt paths.
    """
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    prompt_paths: list[Path] = []

    for batch_path in batch_paths:
        batch_df = pd.read_csv(batch_path)
        batch_id = batch_path.stem
        prompt = create_batch_prompt(batch_df, batch_id=batch_id)
        prompt_path = target_dir / f"{batch_id}_prompt.md"
        prompt_path.write_text(prompt, encoding="utf-8")
        prompt_paths.append(prompt_path)

    return prompt_paths
