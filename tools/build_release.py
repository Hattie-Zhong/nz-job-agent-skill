"""Build the two upload packages that go on the GitHub Releases page.

Usage (from the repository root):
    python tools/build_release.py

Creates:
    dist/nz-job-application.zip     upload to Claude.ai (Customize > Skills)
                                    or unzip into an agent's skills folder
    dist/chatgpt-project-files.zip  unzip, then add the files to a ChatGPT Project

Runs the privacy scan first and stops if it finds anything.
"""

import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "nz-job-application"
CHATGPT = ROOT / "platforms" / "chatgpt-project"
DIST = ROOT / "dist"

SKIP_PARTS = {"__pycache__", ".pytest_cache"}

# Files copied flat into the ChatGPT Project pack.
CHATGPT_FILES = [
    SKILL / "SKILL.md",
    *sorted((SKILL / "references").glob("*.md")),
    *sorted((SKILL / "scripts").glob("*.py")),
]


def skill_name():
    for line in (SKILL / "SKILL.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    sys.exit("SKILL.md has no name: line")


def profile_templates_md():
    """All workspace templates in one Markdown file, for tools without a folder tree."""
    parts = ["# Workspace templates\n",
             "Create each file below inside my-job-search/ with exactly this content.\n"]
    for path in sorted((SKILL / "templates").rglob("*")):
        if path.is_dir():
            continue
        relative = path.relative_to(SKILL / "templates").as_posix()
        if relative == "config.template.yaml":
            relative = "config.yaml"
        fence = "yaml" if relative.endswith(".yaml") else ""
        parts.append(f"\n## File: {relative}\n\n```{fence}\n"
                     f"{path.read_text(encoding='utf-8').rstrip()}\n```\n")
    return "".join(parts)


def build_skill_zip():
    name = skill_name()
    if name != SKILL.name:
        sys.exit(f"Skill name '{name}' must match folder name '{SKILL.name}'.")
    out = DIST / f"{name}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(SKILL.rglob("*")):
            if path.is_dir() or SKIP_PARTS & set(path.parts):
                continue
            zf.write(path, f"{name}/{path.relative_to(SKILL).as_posix()}")
    return out


def build_chatgpt_zip():
    out = DIST / "chatgpt-project-files.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(CHATGPT / "PROJECT_INSTRUCTIONS.md",
                 "chatgpt-project-files/PROJECT_INSTRUCTIONS.md")
        for path in CHATGPT_FILES:
            zf.write(path, f"chatgpt-project-files/project-files/{path.name}")
        zf.writestr("chatgpt-project-files/project-files/profile_templates.md",
                    profile_templates_md())
    return out


def main():
    scan = subprocess.run([sys.executable, str(SKILL / "scripts" / "privacy_scan.py")],
                          cwd=ROOT)
    if scan.returncode != 0:
        sys.exit("Privacy scan failed. Fix the findings before building a release.")
    DIST.mkdir(exist_ok=True)
    for out in (build_skill_zip(), build_chatgpt_zip()):
        with zipfile.ZipFile(out) as zf:
            print(f"BUILT: {out.relative_to(ROOT)} ({len(zf.namelist())} files)")


if __name__ == "__main__":
    main()
