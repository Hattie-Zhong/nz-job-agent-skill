"""Export cv_targeted.md and cover_letter.md in one job folder to .docx.

Usage:
    python export_docx.py <job folder>

Writes, in the same folder:
    <Name>_CV_<Company>.docx
    <Name>_Cover_Letter_<Company>.docx

<Name> comes from config.yaml. <Company> comes from the tracker row for this
folder, keeping only letters and digits.

Supported Markdown:
    CV:     "# " name, contact lines, "## " section headings, "### " sub headings,
            "- " bullets, **bold**, *italic*
    Letter: paragraphs separated by one blank line, **bold**, *italic*
"""

import csv
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

from common import file_name_prefix, load_config, workspace_of_job

INLINE = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*)")
HEADING_COLOUR = RGBColor(0x1F, 0x3A, 0x5F)


def strip_status_prefix(name):
    return re.sub(r"^[A-Z]+_", "", name)


def company_name(folder):
    """Return the short company name for the folder from tracker.csv."""
    tracker = folder.parent / "tracker.csv"
    key = strip_status_prefix(folder.name)
    with open(tracker, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if strip_status_prefix(row["folder"]) == key:
                name = re.sub(r"[^A-Za-z0-9]", "", row["company"])
                if name:
                    return name
    sys.exit(f"No tracker row with a company name for folder: {folder.name}")


def base_doc(font_size):
    doc = Document()
    for section in doc.sections:
        section.top_margin = section.bottom_margin = Cm(1.8)
        section.left_margin = section.right_margin = Cm(2.0)
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(font_size)
    style.paragraph_format.space_after = Pt(2)
    style.paragraph_format.space_before = Pt(0)
    return doc


def add_runs(paragraph, text):
    """Add text, turning **bold** and *italic* into formatted runs."""
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            paragraph.add_run(part[2:-2]).bold = True
        elif part.startswith("*") and part.endswith("*"):
            paragraph.add_run(part[1:-1]).italic = True
        else:
            paragraph.add_run(part)


def export_cv(md_path, out_path):
    doc = base_doc(10)
    in_header = False  # lines between "# Name" and the first "## " are centred
    for line in md_path.read_text(encoding="utf-8").splitlines():
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("# "):
            in_header = True
            paragraph = doc.add_paragraph()
            run = paragraph.add_run(line[2:])
            run.bold = True
            run.font.size = Pt(18)
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif line.startswith("## "):
            in_header = False
            paragraph = doc.add_paragraph()
            paragraph.paragraph_format.space_before = Pt(8)
            paragraph.paragraph_format.space_after = Pt(3)
            run = paragraph.add_run(line[3:])
            run.bold = True
            run.font.size = Pt(11.5)
            run.font.color.rgb = HEADING_COLOUR
        elif line.startswith("### "):
            paragraph = doc.add_paragraph()
            paragraph.paragraph_format.space_before = Pt(4)
            add_runs(paragraph, line[4:])
            for run in paragraph.runs:
                run.bold = True
        elif line.startswith("- "):
            paragraph = doc.add_paragraph(style="List Bullet")
            paragraph.paragraph_format.space_after = Pt(1)
            add_runs(paragraph, line[2:])
        else:
            paragraph = doc.add_paragraph()
            add_runs(paragraph, line)
            if in_header:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.save(out_path)


def export_letter(md_path, out_path):
    doc = base_doc(11)
    doc.styles["Normal"].paragraph_format.space_after = Pt(0)
    for block in md_path.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = block.splitlines()
        for i, line in enumerate(lines):
            paragraph = doc.add_paragraph()
            add_runs(paragraph, line.strip())
            if i == len(lines) - 1:
                paragraph.paragraph_format.space_after = Pt(9)
    doc.save(out_path)


def main():
    if len(sys.argv) != 2:
        print("Usage: python export_docx.py <job folder>")
        sys.exit(2)
    folder = Path(sys.argv[1]).resolve()
    if not folder.is_dir():
        sys.exit(f"Not a folder: {folder}")
    for needed in ("cv_targeted.md", "cover_letter.md"):
        if not (folder / needed).exists():
            sys.exit(f"Missing {needed} in {folder}")

    config = load_config(workspace_of_job(folder))
    name = file_name_prefix(config)
    company = company_name(folder)
    cv_out = folder / f"{name}_CV_{company}.docx"
    letter_out = folder / f"{name}_Cover_Letter_{company}.docx"
    export_cv(folder / "cv_targeted.md", cv_out)
    export_letter(folder / "cover_letter.md", letter_out)
    print(f"Exported: {cv_out.name}, {letter_out.name}")


if __name__ == "__main__":
    main()
