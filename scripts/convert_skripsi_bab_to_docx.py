"""Convert a skripsi chapter Markdown file into a formatted DOCX file."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

PROJECT_ROOT = Path(__file__).resolve().parents[1]

BOLD_ITALIC_PATTERN = re.compile(r"(\*\*.+?\*\*|\*.+?\*)")

# Margins per Panduan TA SI: kiri 4 cm, kanan/atas/bawah 3 cm.
MARGIN_LEFT_CM = 4
MARGIN_RIGHT_CM = 3
MARGIN_TOP_CM = 3
MARGIN_BOTTOM_CM = 3


def add_runs_with_inline_formatting(paragraph, text: str) -> None:
    """Add text to a paragraph, honoring **bold** and *italic* markdown spans."""
    for part in BOLD_ITALIC_PATTERN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith("*") and part.endswith("*"):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
        else:
            paragraph.add_run(part)


def set_base_style(document: Document) -> None:
    """Set default font to Times New Roman 12pt for the Normal style."""
    style = document.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style.paragraph_format.line_spacing = 1.5
    style.paragraph_format.space_after = Pt(12)


def set_page_setup(document: Document) -> None:
    """Set A4 page size and margins per Panduan TA SI (kiri 4cm, kanan/atas/bawah 3cm)."""
    section = document.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(MARGIN_LEFT_CM)
    section.right_margin = Cm(MARGIN_RIGHT_CM)
    section.top_margin = Cm(MARGIN_TOP_CM)
    section.bottom_margin = Cm(MARGIN_BOTTOM_CM)


def add_page_number_footer(document: Document) -> None:
    """Add a bottom-right Arabic page number field to the footer (Bab content pages)."""
    section = document.sections[0]
    footer_paragraph = section.footer.paragraphs[0]
    footer_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = footer_paragraph.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)

    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = "PAGE"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")

    run._r.append(fld_begin)
    run._r.append(instr_text)
    run._r.append(fld_end)


def format_heading_run(paragraph, bold: bool = True, size_pt: int = 12) -> None:
    """Force Times New Roman on every run of a heading paragraph, overriding the style theme font."""
    for run in paragraph.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.color.rgb = RGBColor(0, 0, 0)


def is_table_separator(line: str) -> bool:
    """Check whether a line is a Markdown table header separator (e.g. |---|---|)."""
    stripped = line.strip().strip("|")
    return bool(stripped) and all(c in "-: " for c in stripped)


def parse_table_row(line: str) -> list[str]:
    """Split a Markdown table row into trimmed cell values."""
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def add_table(document: Document, rows: list[list[str]]) -> None:
    """Add a Markdown table (header + data rows) to the document."""
    if not rows:
        return
    n_cols = len(rows[0])
    table = document.add_table(rows=len(rows), cols=n_cols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for row_idx, row_values in enumerate(rows):
        for col_idx in range(n_cols):
            cell = table.cell(row_idx, col_idx)
            cell.text = ""
            paragraph = cell.paragraphs[0]
            value = row_values[col_idx] if col_idx < len(row_values) else ""
            add_runs_with_inline_formatting(paragraph, value)
            if row_idx == 0:
                for run in paragraph.runs:
                    run.bold = True
    document.add_paragraph()


def convert(markdown_path: Path, docx_path: Path) -> None:
    """Convert one Markdown chapter file to DOCX."""
    document = Document()
    set_base_style(document)
    set_page_setup(document)
    add_page_number_footer(document)

    ordered_list_pattern = re.compile(r"^\d+\.\s+(.*)")
    lines = markdown_path.read_text(encoding="utf-8").splitlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if line.startswith("# "):
            # BAB heading: huruf kapital, tebal, posisi tengah, Times New Roman 12pt.
            heading = document.add_heading(level=1)
            heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_runs_with_inline_formatting(heading, line[2:].upper())
            format_heading_run(heading)
            i += 1
            continue

        if line.startswith("## "):
            # Subbab heading: title case, rata kiri, tebal, Times New Roman 12pt.
            heading = document.add_heading(level=2)
            heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_runs_with_inline_formatting(heading, line[3:])
            format_heading_run(heading)
            i += 1
            continue

        if (
            line.startswith("|")
            and i + 1 < len(lines)
            and is_table_separator(lines[i + 1])
        ):
            table_rows = [parse_table_row(line)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_rows.append(parse_table_row(lines[i]))
                i += 1
            add_table(document, table_rows)
            continue

        ordered_match = ordered_list_pattern.match(line)
        if ordered_match:
            paragraph = document.add_paragraph(style="List Number")
            paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_runs_with_inline_formatting(paragraph, ordered_match.group(1))
            i += 1
            continue

        paragraph = document.add_paragraph()
        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_runs_with_inline_formatting(paragraph, line)
        i += 1

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(docx_path)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Convert a skripsi chapter Markdown file to DOCX."
    )
    parser.add_argument("--input", required=True, help="Path to the source .md file.")
    parser.add_argument(
        "--output",
        default=None,
        help="Path to the output .docx file (defaults to same name as input).",
    )
    return parser.parse_args()


def main() -> None:
    """CLI entrypoint."""
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".docx")
    convert(input_path, output_path)
    print(f"DOCX saved to: {output_path}")


if __name__ == "__main__":
    main()
