"""Keep applications/tracker.csv and the job folder names in step.

Usage:
    python tracker.py new --company "Kowhai Analytics" --role "Data Analyst Intern"
                          [--closing-date 2026-12-01] [--channel SEEK]
    python tracker.py set <folder> [--status Applied] [--score 72]
                          [--next-step "..."] [--channel "..."] [--closing-date ...]
    python tracker.py list

All commands accept --workspace (default: my-job-search).

Each job folder name starts with a prefix that shows its status, for example
APPLIED_2026-11-05-kowhai-analytics-data-analyst-intern. Changing the status
renames the folder and updates the folder column.
"""

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path

from common import DEFAULT_WORKSPACE

FIELDS = ["folder", "company", "role", "score", "status", "date_applied",
          "channel", "next_step", "closing_date"]

STATUS_PREFIX = {
    "In progress": "", "Paused": "", "Ready to submit": "",
    "Applied": "APPLIED_", "Interview": "INTERVIEW_", "Offer": "OFFER_",
    "Rejected": "REJECTED_", "Skipped": "SKIPPED_", "Low score": "LOWSCORE_",
    "Not eligible": "NOTELIGIBLE_",
}
PREFIX_RE = re.compile(r"^(" + "|".join(
    p.rstrip("_") for p in STATUS_PREFIX.values() if p) + r")_")


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def strip_prefix(name):
    return PREFIX_RE.sub("", name)


def read_rows(tracker):
    if not tracker.exists():
        return []
    with open(tracker, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(tracker, rows):
    tracker.parent.mkdir(parents=True, exist_ok=True)
    with open(tracker, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS})


def find_row(rows, folder):
    key = strip_prefix(Path(folder).name)
    for row in rows:
        if strip_prefix(row["folder"]) == key:
            return row
    return None


def cmd_new(args, apps):
    tracker = apps / "tracker.csv"
    rows = read_rows(tracker)
    base = f"{date.today().isoformat()}-{slugify(args.company)}-{slugify(args.role)}"
    same_role = f"-{slugify(args.company)}-{slugify(args.role)}"
    for row in rows:
        if strip_prefix(row["folder"])[10:] == same_role:
            sys.exit(f"EXISTS: a folder for this role already exists: {row['folder']}")
    folder = apps / base
    folder.mkdir(parents=True, exist_ok=False)
    rows.append({"folder": base, "company": args.company, "role": args.role,
                 "status": "In progress", "channel": args.channel or "",
                 "closing_date": args.closing_date or ""})
    write_rows(tracker, rows)
    print(f"CREATED: {folder}")


def cmd_set(args, apps):
    tracker = apps / "tracker.csv"
    rows = read_rows(tracker)
    row = find_row(rows, args.folder)
    if row is None:
        sys.exit(f"No tracker row for folder: {args.folder}")

    if args.score is not None:
        row["score"] = str(args.score)
    if args.channel is not None:
        row["channel"] = args.channel
    if args.next_step is not None:
        row["next_step"] = args.next_step
    if args.closing_date is not None:
        row["closing_date"] = args.closing_date

    if args.status is not None:
        if args.status not in STATUS_PREFIX:
            sys.exit(f"Unknown status '{args.status}'. Allowed: {', '.join(STATUS_PREFIX)}")
        row["status"] = args.status
        if args.status == "Applied" and not row.get("date_applied"):
            row["date_applied"] = date.today().isoformat()
        new_name = STATUS_PREFIX[args.status] + strip_prefix(row["folder"])
        old_path = apps / row["folder"]
        new_path = apps / new_name
        if new_name != row["folder"]:
            if old_path.exists():
                old_path.rename(new_path)
            row["folder"] = new_name

    write_rows(tracker, rows)
    print(f"UPDATED: {row['folder']} | status={row['status']} | score={row.get('score', '')}")


def cmd_list(args, apps):
    rows = read_rows(apps / "tracker.csv")
    if not rows:
        print("No applications yet.")
        return
    for row in rows:
        print(f"{row['status']:<16} {row.get('score', ''):>3}  {row['company']} | "
              f"{row['role']} | next: {row.get('next_step', '')}")


def main():
    parser = argparse.ArgumentParser(description="Application tracker")
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new")
    new.add_argument("--company", required=True)
    new.add_argument("--role", required=True)
    new.add_argument("--closing-date")
    new.add_argument("--channel")

    upd = sub.add_parser("set")
    upd.add_argument("folder")
    upd.add_argument("--status")
    upd.add_argument("--score", type=int)
    upd.add_argument("--channel")
    upd.add_argument("--next-step")
    upd.add_argument("--closing-date")

    sub.add_parser("list")

    args = parser.parse_args()
    apps = Path(args.workspace) / "applications"
    {"new": cmd_new, "set": cmd_set, "list": cmd_list}[args.command](args, apps)


if __name__ == "__main__":
    main()
