"""Load whatever the user uploaded into the workspace.

Usage:
    python load_upload.py <file or folder> [<file or folder> ...] [--workspace my-job-search]

Accepts anything: single files (CV, cover letters, certificates, transcripts),
zip files packed any way the user likes, nested zips, or a my-job-search.zip
from a previous conversation.

- A zip that contains config.yaml (at the top or one folder down) is treated
  as a saved workspace and restored, if the workspace is still empty.
- Everything else is copied into <workspace>/inbox/. Zips are extracted into
  inbox/<zip name>/, including zips inside zips (one level).
- The workspace is created from the blank templates if it does not exist.

Prints one line per file in inbox/ so the assistant knows what to read.
"""

import argparse
import io
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath

from common import DEFAULT_WORKSPACE
from init_workspace import copy_templates

SKIP_NAMES = {"__MACOSX", ".DS_Store", "Thumbs.db", "desktop.ini"}


def safe_parts(name):
    """Return the path parts of a zip member, or None if it is unsafe or junk."""
    path = PurePosixPath(name.replace("\\", "/"))
    if path.is_absolute() or any(p in ("..", "") for p in path.parts):
        return None
    if any(p in SKIP_NAMES or p.startswith("._") for p in path.parts):
        return None
    return path.parts


def workspace_root_in_zip(zf):
    """Return the folder prefix that holds config.yaml, or None if this is not a workspace zip."""
    for name in zf.namelist():
        parts = safe_parts(name)
        if parts and parts[-1] == "config.yaml" and len(parts) <= 2:
            return parts[:-1]
    return None


def is_empty_workspace(workspace):
    """True if the workspace has no profile content beyond the blank templates."""
    config = workspace / "config.yaml"
    if not config.exists():
        return True
    text = config.read_text(encoding="utf-8")
    return 'full_name: ""' in text and not any((workspace / "applications").glob("*/"))


def restore_workspace(zf, prefix, workspace):
    count = 0
    for name in zf.namelist():
        parts = safe_parts(name)
        if not parts or name.endswith("/") or tuple(parts[:len(prefix)]) != tuple(prefix):
            continue
        target = workspace.joinpath(*parts[len(prefix):])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(zf.read(name))
        count += 1
    return count


def extract_into(zf, dest, depth=0):
    for name in zf.namelist():
        parts = safe_parts(name)
        if not parts or name.endswith("/"):
            continue
        target = dest.joinpath(*parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        data = zf.read(name)
        if target.suffix.lower() == ".zip" and depth == 0:
            inner = target.with_suffix("")
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as inner_zf:
                    extract_into(inner_zf, inner, depth + 1)
                continue
            except zipfile.BadZipFile:
                pass
        target.write_bytes(data)


def unique_path(path):
    if not path.exists():
        return path
    for i in range(2, 1000):
        candidate = path.with_name(f"{path.stem}_{i}{path.suffix}")
        if not candidate.exists():
            return candidate
    sys.exit(f"Too many files named {path.name}")


def load(source, workspace):
    inbox = workspace / "inbox"
    source = Path(source)
    if source.is_dir():
        for path in sorted(source.rglob("*")):
            if path.is_file() and not (set(path.parts) & SKIP_NAMES):
                target = unique_path(inbox / source.name / path.relative_to(source))
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
        return f"folder {source.name} copied to inbox"
    if zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as zf:
            prefix = workspace_root_in_zip(zf)
            if prefix is not None and is_empty_workspace(workspace):
                count = restore_workspace(zf, prefix, workspace)
                return f"RESTORED saved workspace from {source.name} ({count} files)"
            extract_into(zf, unique_path(inbox / source.stem))
        return f"zip {source.name} extracted to inbox"
    target = unique_path(inbox / source.name)
    shutil.copyfile(source, target)
    return f"file {source.name} copied to inbox"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("sources", nargs="+")
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    args = parser.parse_args()
    workspace = Path(args.workspace)

    new = not (workspace / "config.yaml").exists()
    workspace.mkdir(parents=True, exist_ok=True)

    messages = []
    for source in args.sources:
        if not Path(source).exists():
            messages.append(f"MISSING {source}")
            continue
        messages.append(load(source, workspace))
    copy_templates(workspace)  # fills in any template files still missing

    restored = any(m.startswith("RESTORED") for m in messages)
    status = "RESTORED" if restored else ("NEW" if new else "UPDATED")
    print(f"WORKSPACE: {workspace.resolve()} ({status})")
    for m in messages:
        print(f"  {m}")
    print("INBOX FILES:")
    files = sorted(p for p in (workspace / "inbox").rglob("*") if p.is_file())
    for path in files:
        print(f"  {path.relative_to(workspace).as_posix()}  ({path.stat().st_size // 1024} KB)")
    if not files:
        print("  (none)")


if __name__ == "__main__":
    main()
