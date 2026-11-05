"""Create a private workspace for one job seeker from the blank templates.

Usage:
    python init_workspace.py [--workspace my-job-search]
    python init_workspace.py --reset [--workspace my-job-search]

Without --reset, existing files are never overwritten, so it is safe to run again.

With --reset, the current workspace is NOT deleted. It is renamed to
my-job-search-backup-<date-time> and a fresh, blank workspace is created.
Use this after trying the Alex Chen example, or to start again from scratch.
Delete the backup folder yourself once you are sure you do not need it.
"""

import argparse
import shutil
from datetime import datetime
from pathlib import Path

from common import DEFAULT_WORKSPACE, TEMPLATES


def copy_templates(workspace):
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
    return created, kept


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    parser.add_argument("--reset", action="store_true",
                        help="Move the current workspace to a backup folder and start blank")
    args = parser.parse_args()
    workspace = Path(args.workspace)

    if args.reset and workspace.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = workspace.with_name(f"{workspace.name}-backup-{stamp}")
        workspace.rename(backup)
        print(f"Old workspace moved to: {backup.resolve()}")
        print("Delete that folder yourself when you no longer need it.\n")

    created, kept = copy_templates(workspace)

    print(f"Workspace: {workspace.resolve()}")
    for path in created:
        print(f"  created  {path}")
    for path in kept:
        print(f"  kept     {path} (already exists)")
    print("\nNext: put your current CV in inbox/, then ask your AI assistant to set up your profile.")


if __name__ == "__main__":
    main()
