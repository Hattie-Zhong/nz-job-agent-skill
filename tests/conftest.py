import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "nz-job-application" / "scripts"
EXAMPLE = ROOT / "examples" / "alex-chen"


@pytest.fixture
def workspace(tmp_path):
    """A copy of the fictional example workspace with a real config.yaml."""
    target = tmp_path / "my-job-search"
    shutil.copytree(EXAMPLE, target)
    (target / "config.example.yaml").rename(target / "config.yaml")
    return target


def run_script(name, *args, cwd=None):
    import subprocess
    return subprocess.run([sys.executable, str(SCRIPTS / name), *map(str, args)],
                          capture_output=True, text=True, cwd=cwd)
