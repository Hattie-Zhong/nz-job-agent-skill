"""Check the exported CV and cover letter .docx files in one job folder.

Usage:
    python check_output.py <job folder>

Checks (limits come from config.yaml):
- exactly one CV and one cover letter .docx, named <Name>_CV_<Company>.docx
  and <Name>_Cover_Letter_<Company>.docx, with the same <Company>
- page count, after converting each .docx to PDF
- no leftover Markdown or placeholders
- cover letter: word count, and no dashes between words (if enabled)

PDF conversion uses Microsoft Word (via docx2pdf) or LibreOffice, whichever is
available. If neither is installed, the page count check is SKIPPED, not failed.

Prints PASS, FAIL or SKIP for each check. Exit code 0 when nothing FAILED.
"""

import contextlib
import io
import re
import shutil
import subprocess
import sys
from pathlib import Path

from common import file_name_prefix, load_config, workspace_of_job

PLACEHOLDER_PATTERNS = [
    ("Markdown bold '**'", re.compile(r"\*\*")),
    ("Markdown heading '#'", re.compile(r"^\s*#")),
    ("Line starting with '- '", re.compile(r"^\s*- ")),
    ("Square bracket", re.compile(r"[\[\]]")),
    ("Curly brace", re.compile(r"[{}]")),
    ("Angle bracket", re.compile(r"[<>]")),
    ("TODO / TBC / XXX", re.compile(r"\b(TODO|TBC|XXX)\b")),
]

# En or em dash between words, or a hyphen with a space on either side.
# Hyphens inside words (part-time) are allowed.
DASH_RE = re.compile(r"\w+(?:\s*[\u2013\u2014]\s*|\s+-\s*|\s*-\s+)\w+")

failures = 0


def report(check, status, problems=None):
    """status is 'PASS', 'FAIL' or 'SKIP'."""
    global failures
    if status == "FAIL":
        failures += 1
    print(f"  {status:<4}  {check}")
    if status != "PASS":
        for problem in problems or []:
            print(f"          -> {problem}")


def docx_lines(path):
    from docx import Document
    document = Document(str(path))
    lines = [p.text for p in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                lines.extend(p.text for p in cell.paragraphs)
    return lines


def find_soffice():
    found = shutil.which("soffice") or shutil.which("libreoffice")
    if found:
        return found
    for candidate in (r"C:\Program Files\LibreOffice\program\soffice.exe",
                      "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        if Path(candidate).exists():
            return candidate
    return None


def convert_to_pdf(path):
    """Return (pdf_path, None) on success, or (None, reason) if no converter worked."""
    pdf_path = path.with_suffix(".pdf")
    if pdf_path.exists():
        pdf_path.unlink()  # never count pages of an old PDF
    reasons = []

    if sys.platform in ("win32", "darwin"):
        try:
            import docx2pdf
            with contextlib.redirect_stderr(io.StringIO()):
                docx2pdf.convert(str(path), str(pdf_path))
        except Exception as error:  # Word missing, or Word raised while closing
            reasons.append(f"Word: {type(error).__name__}")
        if pdf_path.exists():
            return pdf_path, None

    soffice = find_soffice()
    if soffice:
        try:
            subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                            "--outdir", str(path.parent), str(path)],
                           check=True, capture_output=True, timeout=180)
        except Exception as error:
            reasons.append(f"LibreOffice: {type(error).__name__}")
        if pdf_path.exists():
            return pdf_path, None
    else:
        reasons.append("LibreOffice not found")

    return None, "; ".join(reasons) or "no PDF converter available"


def check_pages(path, max_pages):
    label = f"Page count ({max_pages} or fewer)"
    pdf_path, reason = convert_to_pdf(path)
    if pdf_path is None:
        report(label, "SKIP", [f"Could not make a PDF ({reason}). "
                               "Open the .docx and check the page count yourself."])
        return
    from pypdf import PdfReader
    pages = len(PdfReader(str(pdf_path)).pages)
    report(f"{label}: {pages} page(s), saved {pdf_path.name}",
           "PASS" if pages <= max_pages else "FAIL",
           [f"{pages} pages, limit is {max_pages}"])


def context(line, match, width=40):
    start = max(match.start() - width, 0)
    return line[start:match.end() + width].strip()


def check_placeholders(lines):
    problems = []
    for line in lines:
        for label, pattern in PLACEHOLDER_PATTERNS:
            match = pattern.search(line)
            if match:
                problems.append(f'{label}: "...{context(line, match)}..."')
    report("No leftover Markdown or placeholders", "FAIL" if problems else "PASS", problems)


def check_dashes(lines):
    problems = [f'"{m.group(0)}" in "...{context(line, m)}..."'
                for line in lines for m in DASH_RE.finditer(line)]
    report("No dashes between words", "FAIL" if problems else "PASS", problems)


def check_words(lines, limit):
    words = sum(len(line.split()) for line in lines)
    report(f"Word count ({limit} or fewer): {words} words",
           "PASS" if words <= limit else "FAIL",
           [f"{words} words, limit is {limit}"])


def main():
    if len(sys.argv) != 2:
        print("Usage: python check_output.py <job folder>")
        sys.exit(2)
    folder = Path(sys.argv[1]).resolve()
    if not folder.is_dir():
        sys.exit(f"Not a folder: {folder}")

    config = load_config(workspace_of_job(folder))
    limits, style = config["limits"], config["style"]
    name = re.escape(file_name_prefix(config))
    cv_re = re.compile(rf"^{name}_CV_([A-Za-z0-9]+)\.docx$")
    letter_re = re.compile(rf"^{name}_Cover_Letter_([A-Za-z0-9]+)\.docx$")

    docs = [p for p in sorted(folder.glob("*.docx")) if not p.name.startswith("~$")]
    cv_files = [p for p in docs if cv_re.match(p.name)]
    letter_files = [p for p in docs if letter_re.match(p.name)]
    others = [p for p in docs if p not in cv_files and p not in letter_files]

    print(f"Checking: {folder}\n")
    report("No other .docx files in the folder", "FAIL" if others else "PASS",
           [f"Unexpected: {p.name}" for p in others])

    print("CV")
    report("Exactly one CV file", "PASS" if len(cv_files) == 1 else "FAIL",
           [f"Found {len(cv_files)}"])
    for path in cv_files:
        print(f" {path.name}")
        check_pages(path, limits["cv_max_pages"])
        check_placeholders(docx_lines(path))

    print("\nCOVER LETTER")
    report("Exactly one cover letter file", "PASS" if len(letter_files) == 1 else "FAIL",
           [f"Found {len(letter_files)}"])
    for path in letter_files:
        print(f" {path.name}")
        check_pages(path, limits["cover_letter_max_pages"])
        lines = docx_lines(path)
        check_placeholders(lines)
        if style.get("no_dashes_in_cover_letter", True):
            check_dashes(lines)
        check_words(lines, limits["cover_letter_max_words"])

    companies = {cv_re.match(p.name).group(1) for p in cv_files}
    companies |= {letter_re.match(p.name).group(1) for p in letter_files}
    if len(companies) > 1:
        print()
        report("Same company in both file names", "FAIL", [", ".join(sorted(companies))])

    print(f"\nRESULT: {'ALL CHECKS PASS' if failures == 0 else f'{failures} check(s) FAILED'}")
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
