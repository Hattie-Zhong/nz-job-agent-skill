"""Create a private workspace for one job seeker from the templates.

Usage:
    python init_workspace.py [--workspace my-job-search]

Existing files are never overwritten, so it is safe to run again.
"""

import argparse
import shutil
from pathlib import Path

from common import DEFAULT_WORKSPACE, TEMPLATES


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    args = parser.parse_args()
    workspace = Path(args.workspace)

    created, kept = [], []
    (workspace / "inbox").mkdir(parents=True, exist_ok=True)

    for source in sorted(TEMPLATES.rglob("*")):
        if source.is_dir():
            continue
        relative = source.relative_to(TEMPLATES)
        if relative.name == "config.template.yaml":
            relative = relative.with_name("config.yaml")
        target = workspace / relative
        if target.exists():
            kept.append(relative)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        created.append(relative)

    print(f"Workspace: {workspace.resolve()}")
    for path in created:
        print(f"  created  {path}")
    for path in kept:
        print(f"  kept     {path} (already exists)")
    print("\nNext: put your current CV in inbox/, then ask your AI assistant to run setup.")


if __name__ == "__main__":
    main()
