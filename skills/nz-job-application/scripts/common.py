"""Shared helpers for the nz-job-application scripts."""

import re
import sys
from pathlib import Path

import yaml

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_DIR / "templates"
DEFAULT_WORKSPACE = Path("my-job-search")

DEFAULT_CONFIG = {
    "candidate": {"full_name": "", "file_name": "", "email": "", "phone": "",
                  "location": "", "linkedin": "", "github": ""},
    "limits": {"cv_max_pages": 2, "cover_letter_max_pages": 1,
               "cover_letter_max_words": 450},
    "style": {"no_dashes_in_cover_letter": True},
    "privacy": {"private_terms": []},
}


def load_config(workspace):
    """Load config.yaml from the workspace, filling in defaults for missing keys."""
    path = Path(workspace) / "config.yaml"
    if not path.exists():
        sys.exit(f"No config.yaml in {Path(workspace).resolve()}. "
                 "Run scripts/init_workspace.py first.")
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    config = {}
    for section, defaults in DEFAULT_CONFIG.items():
        merged = dict(defaults)
        merged.update(data.get(section) or {})
        config[section] = merged
    return config


def file_name_prefix(config):
    """Return the name used at the start of exported files, e.g. 'Alex_Chen'."""
    candidate = config["candidate"]
    name = candidate.get("file_name") or candidate.get("full_name") or ""
    name = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
    if not name:
        sys.exit("Set candidate.full_name (or candidate.file_name) in config.yaml first.")
    return name


def workspace_of_job(job_folder):
    """A job folder lives in <workspace>/applications/<job>."""
    return Path(job_folder).resolve().parent.parent
