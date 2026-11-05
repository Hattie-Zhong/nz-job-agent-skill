"""Scan the files git would publish for personal information. Run before every push.

Usage (from the repository root):
    python skills/nz-job-application/scripts/privacy_scan.py [--workspace my-job-search]

It checks every file git tracks or would add (ignored files are skipped) for:
- your own name, email, phone and private_terms from <workspace>/config.yaml
  (strings listed in allowed_terms, such as your GitHub username, are skipped)
- any email address not at example.com / example.org
- NZ-style phone numbers
- numbers written like IRD numbers (three digit groups joined by hyphens)
- passport-like codes (two letters followed by 6 or 7 digits)
- files inside the workspace folder that are not ignored

Exit code 0 when nothing is found, 1 otherwise.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

TEXT_SUFFIXES = {".md", ".txt", ".py", ".yaml", ".yml", ".csv", ".json", ".toml",
                 ".cfg", ".ini", ".html", ".gitignore", ""}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
ALLOWED_EMAIL_DOMAINS = {"example.com", "example.org", "anthropic.com"}
PATTERNS = [
    ("NZ phone number", re.compile(r"(?<!\d)(\+?64[\s-]?|0)2\d[\s-]?\d{3}[\s-]?\d{3,4}(?!\d)")),
    ("IRD-style number", re.compile(r"(?<!\d)\d{2,3}-\d{3}-\d{3}(?!\d)")),
    ("Passport-like code", re.compile(r"\b[A-Z]{2}\d{6,7}\b")),
]


def git_files():
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        capture_output=True, text=True, check=True)
    return [Path(line) for line in result.stdout.splitlines() if line]


def personal_terms(workspace):
    """Return (terms that must not appear, allowed strings that may contain them)."""
    path = Path(workspace) / "config.yaml"
    if not path.exists():
        return [], []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    candidate = data.get("candidate") or {}
    terms = []
    for part in re.split(r"[\s_]+", candidate.get("full_name") or ""):
        if len(part) >= 3:
            terms.append(part)
    for key in ("email", "phone", "linkedin"):
        if candidate.get(key):
            terms.append(str(candidate[key]))
    privacy = data.get("privacy") or {}
    terms += [str(t) for t in privacy.get("private_terms") or [] if t]
    allowed = [str(t) for t in privacy.get("allowed_terms") or [] if t]
    return terms, allowed


def main():
    parser = argparse.ArgumentParser(description="Privacy scan before publishing")
    parser.add_argument("--workspace", default="my-job-search")
    args = parser.parse_args()

    try:
        files = git_files()
    except (subprocess.CalledProcessError, FileNotFoundError):
        sys.exit("Run this inside a git repository (git must be installed).")

    terms, allowed = personal_terms(args.workspace)
    workspace_name = Path(args.workspace).name
    findings = []

    for path in files:
        if path.parts and path.parts[0].startswith(workspace_name):
            findings.append((path, 0, "Workspace file is not ignored", str(path)))
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES or not path.exists():
            if path.suffix.lower() in {".docx", ".pdf", ".xlsx", ".pptx", ".zip"}:
                findings.append((path, 0, "Document file would be published", path.name))
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            for match in EMAIL_RE.finditer(line):
                if match.group(1).lower() not in ALLOWED_EMAIL_DOMAINS:
                    findings.append((path, number, "Email address", match.group(0)))
            for label, pattern in PATTERNS:
                for match in pattern.finditer(line):
                    findings.append((path, number, label, match.group(0)))
            lower = line.lower()
            for ok in allowed:
                lower = lower.replace(ok.lower(), " ")
            for term in terms:
                if term.lower() in lower:
                    findings.append((path, number, "Personal term from config.yaml", term))

    if not terms:
        print("Note: no personal terms loaded (no config.yaml found in the workspace).")
    print(f"Scanned {len(files)} file(s).")
    if not findings:
        print("PASS: nothing personal found.")
        sys.exit(0)
    for path, number, label, value in findings:
        where = f"{path}:{number}" if number else str(path)
        print(f"FOUND  {where}  {label}: {value}")
    print(f"\nFAIL: {len(findings)} finding(s). Remove them before pushing.")
    sys.exit(1)


if __name__ == "__main__":
    main()
