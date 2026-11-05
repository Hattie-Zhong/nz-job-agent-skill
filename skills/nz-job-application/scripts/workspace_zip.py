"""Pack the workspace into one zip, or unpack it again.

Used in web chat apps (Claude.ai, ChatGPT), where files are lost when a new
conversation starts. The user keeps my-job-search.zip on their own computer
and uploads it at the start of each conversation.

Usage:
    python workspace_zip.py pack   [--workspace my-job-search] [--out my-job-search.zip]
    python workspace_zip.py unpack <zip file> [--workspace my-job-search]

pack:   every file in the workspace goes into the zip, except temporary
        Word lock files. Existing .docx and .pdf exports are included.
unpack: extracts the zip into the workspace folder. Refuses to overwrite an
        existing, non-empty workspace.
"""

import argparse
import sys
import zipfile
from pathlib import Path, PurePosixPath

from common import DEFAULT_WORKSPACE


def pack(workspace, out):
    workspace = Path(workspace)
    if not (workspace / "config.yaml").exists():
        sys.exit(f"No workspace found at {workspace.resolve()} (config.yaml missing).")
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(workspace.rglob("*")):
            if path.is_dir() or path.name.startswith("~$"):
                continue
            arcname = PurePosixPath(workspace.name, *path.relative_to(workspace).parts)
            zf.write(path, str(arcname))
            count += 1
    print(f"PACKED: {count} file(s) into {Path(out).resolve()}")


def unpack(zip_path, workspace):
    workspace = Path(workspace)
    if workspace.exists() and any(workspace.iterdir()):
        sys.exit(f"Workspace {workspace.resolve()} is not empty. Move it away first.")
    with zipfile.ZipFile(zip_path) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        if not names:
            sys.exit("The zip file is empty.")
        # Accept zips with or without a single top-level folder.
        tops = {PurePosixPath(n).parts[0] for n in names}
        strip = len(tops) == 1 and all(len(PurePosixPath(n).parts) > 1 for n in names)
        for name in names:
            parts = PurePosixPath(name).parts[1:] if strip else PurePosixPath(name).parts
            if any(p in ("..", "") for p in parts) or PurePosixPath(name).is_absolute():
                sys.exit(f"Unsafe path in zip: {name}")
            target = workspace.joinpath(*parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(name))
    if not (workspace / "config.yaml").exists():
        print("WARNING: no config.yaml in the zip. Is this a my-job-search zip?")
    print(f"UNPACKED: {len(names)} file(s) into {workspace.resolve()}")


def main():
    parser = argparse.ArgumentParser(description="Pack or unpack the workspace")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("pack")
    p.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    p.add_argument("--out", default="my-job-search.zip")
    u = sub.add_parser("unpack")
    u.add_argument("zip_file")
    u.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    args = parser.parse_args()
    if args.command == "pack":
        pack(args.workspace, args.out)
    else:
        unpack(args.zip_file, args.workspace)


if __name__ == "__main__":
    main()
