import csv

from conftest import run_script

JOB = "2026-11-05-kowhai-analytics-data-analyst-intern"


def read_tracker(workspace):
    with open(workspace / "applications" / "tracker.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_init_creates_workspace(tmp_path):
    result = run_script("init_workspace.py", "--workspace", tmp_path / "ws")
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "ws" / "config.yaml").exists()
    assert (tmp_path / "ws" / "profile" / "cv_master.md").exists()
    assert (tmp_path / "ws" / "applications" / "tracker.csv").exists()
    assert (tmp_path / "ws" / "inbox").is_dir()


def test_init_never_overwrites(tmp_path):
    ws = tmp_path / "ws"
    run_script("init_workspace.py", "--workspace", ws)
    (ws / "config.yaml").write_text("candidate:\n  full_name: Kept\n", encoding="utf-8")
    run_script("init_workspace.py", "--workspace", ws)
    assert "Kept" in (ws / "config.yaml").read_text(encoding="utf-8")


def test_tracker_new_and_duplicate(workspace):
    ok = run_script("tracker.py", "--workspace", workspace, "new",
                    "--company", "Rata Energy", "--role", "Data Intern")
    assert ok.returncode == 0, ok.stderr
    dup = run_script("tracker.py", "--workspace", workspace, "new",
                     "--company", "Rata Energy", "--role", "Data Intern")
    assert dup.returncode != 0
    assert "EXISTS" in dup.stderr


def test_tracker_status_renames_folder(workspace):
    result = run_script("tracker.py", "--workspace", workspace, "set", JOB,
                        "--status", "Applied")
    assert result.returncode == 0, result.stderr
    apps = workspace / "applications"
    assert (apps / f"APPLIED_{JOB}").is_dir()
    assert not (apps / JOB).exists()
    row = read_tracker(workspace)[0]
    assert row["folder"] == f"APPLIED_{JOB}"
    assert row["date_applied"]

    again = run_script("tracker.py", "--workspace", workspace, "set", f"APPLIED_{JOB}",
                       "--status", "Interview")
    assert again.returncode == 0, again.stderr
    assert (apps / f"INTERVIEW_{JOB}").is_dir()


def test_export_and_check_pass(workspace):
    job = workspace / "applications" / JOB
    export = run_script("export_docx.py", job)
    assert export.returncode == 0, export.stderr
    assert (job / "Alex_Chen_CV_KowhaiAnalytics.docx").exists()
    assert (job / "Alex_Chen_Cover_Letter_KowhaiAnalytics.docx").exists()
    check = run_script("check_output.py", job)
    assert check.returncode == 0, check.stdout + check.stderr


def test_check_catches_dash_and_markdown(workspace):
    job = workspace / "applications" / JOB
    letter = job / "cover_letter.md"
    letter.write_text(letter.read_text(encoding="utf-8") +
                      "\n\nI love data — truly. **Bold leftover**\n", encoding="utf-8")
    run_script("export_docx.py", job)
    check = run_script("check_output.py", job)
    assert check.returncode == 1
    assert "No dashes between words" in check.stdout


def test_privacy_scan_finds_personal_terms(tmp_path):
    import subprocess
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    fake_email = "jane" + "@" + "realmail.co.nz"
    (repo / "notes.md").write_text(f"Contact Jane at {fake_email}\n", encoding="utf-8")
    ws = repo / "my-job-search"
    ws.mkdir()
    (ws / "config.yaml").write_text(
        "candidate:\n  full_name: Jane Doherty\nprivacy:\n  private_terms: [Fictional Bank]\n",
        encoding="utf-8")
    (repo / ".gitignore").write_text("my-job-search/\n", encoding="utf-8")
    result = run_script("privacy_scan.py", cwd=repo)
    assert result.returncode == 1
    assert "Email address" in result.stdout
    assert "Jane" in result.stdout


def test_privacy_scan_clean_repo(tmp_path):
    import subprocess
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / "README.md").write_text("Contact: someone@example.com\n", encoding="utf-8")
    result = run_script("privacy_scan.py", cwd=repo)
    assert result.returncode == 0, result.stdout


def test_reset_moves_workspace_to_backup(workspace):
    result = run_script("init_workspace.py", "--workspace", workspace, "--reset")
    assert result.returncode == 0, result.stderr
    backups = list(workspace.parent.glob("my-job-search-backup-*"))
    assert len(backups) == 1
    assert (backups[0] / "profile" / "projects" / "sales-forecasting.md").exists()
    import yaml
    config = yaml.safe_load((workspace / "config.yaml").read_text(encoding="utf-8"))
    assert config["candidate"]["full_name"] == ""
    assert not (workspace / "profile" / "projects" / "sales-forecasting.md").exists()


def test_workspace_zip_round_trip(workspace, tmp_path):
    out = tmp_path / "my-job-search.zip"
    packed = run_script("workspace_zip.py", "pack", "--workspace", workspace, "--out", out)
    assert packed.returncode == 0, packed.stderr
    restored = tmp_path / "restored"
    unpacked = run_script("workspace_zip.py", "unpack", out, "--workspace", restored)
    assert unpacked.returncode == 0, unpacked.stderr
    assert (restored / "config.yaml").exists()
    assert (restored / "applications" / "tracker.csv").exists()
    again = run_script("workspace_zip.py", "unpack", out, "--workspace", restored)
    assert again.returncode != 0


def test_build_release(tmp_path):
    import shutil
    import subprocess
    import sys
    import zipfile
    from conftest import ROOT
    repo = tmp_path / "repo"
    shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns(
        ".git", "dist", "my-job-search*", "__pycache__", ".pytest_cache"))
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    result = subprocess.run([sys.executable, "tools/build_release.py"], cwd=repo,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    with zipfile.ZipFile(repo / "dist" / "nz-job-application.zip") as zf:
        names = zf.namelist()
    assert "nz-job-application/SKILL.md" in names
    assert "nz-job-application/templates/config.template.yaml" in names
    assert not any("__pycache__" in n for n in names)
    with zipfile.ZipFile(repo / "dist" / "chatgpt-project-files.zip") as zf:
        names = zf.namelist()
    assert "chatgpt-project-files/PROJECT_INSTRUCTIONS.txt" in names
    assert "chatgpt-project-files/project-files/profile_templates.md" in names
    assert "chatgpt-project-files/project-files/workflow.md" in names


def _zip(path, files):
    import zipfile
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in files.items():
            zf.writestr(name, data)
    return path


def test_load_upload_accepts_anything(tmp_path):
    import io
    import zipfile
    inner = io.BytesIO()
    with zipfile.ZipFile(inner, "w") as zf:
        zf.writestr("certificate.txt", "Certificate in Excel")
    bundle = _zip(tmp_path / "my stuff.zip", {
        "Documents/CV final.docx": b"fake docx",
        "Documents/old letters/letter1.txt": "Dear hiring manager",
        "__MACOSX/._junk": "junk",
        "../evil.txt": "should be skipped",
        "certs.zip": inner.getvalue(),
    })
    loose = tmp_path / "transcript.pdf"
    loose.write_bytes(b"%PDF fake")
    ws = tmp_path / "my-job-search"
    result = run_script("load_upload.py", bundle, loose, "--workspace", ws)
    assert result.returncode == 0, result.stderr
    assert "(NEW)" in result.stdout
    inbox = ws / "inbox"
    assert (inbox / "my stuff" / "Documents" / "CV final.docx").exists()
    assert (inbox / "my stuff" / "Documents" / "old letters" / "letter1.txt").exists()
    assert (inbox / "my stuff" / "certs" / "certificate.txt").exists()
    assert (inbox / "transcript.pdf").exists()
    assert not any("MACOSX" in str(p) or "evil" in str(p) for p in inbox.rglob("*"))
    assert (ws / "config.yaml").exists() and (ws / "profile" / "cv_master.md").exists()


def test_load_upload_restores_saved_workspace(workspace, tmp_path):
    saved = tmp_path / "anything I like.zip"
    packed = run_script("workspace_zip.py", "pack", "--workspace", workspace, "--out", saved)
    assert packed.returncode == 0, packed.stderr
    fresh = tmp_path / "fresh" / "my-job-search"
    result = run_script("load_upload.py", saved, "--workspace", fresh)
    assert result.returncode == 0, result.stderr
    assert "RESTORED" in result.stdout
    assert "Alex Chen" in (fresh / "config.yaml").read_text(encoding="utf-8")
    assert (fresh / "profile" / "projects" / "sales-forecasting.md").exists()


def test_load_upload_never_overwrites_existing_profile(workspace, tmp_path):
    other = _zip(tmp_path / "other.zip", {"my-job-search/config.yaml":
                                         'candidate:\n  full_name: "Someone Else"\n'})
    result = run_script("load_upload.py", other, "--workspace", workspace)
    assert result.returncode == 0, result.stderr
    assert "Alex Chen" in (workspace / "config.yaml").read_text(encoding="utf-8")
    assert (workspace / "inbox" / "other" / "my-job-search" / "config.yaml").exists()


def test_chinese_readme_has_current_chatgpt_instructions():
    from conftest import ROOT
    txt = (ROOT / "platforms" / "chatgpt-project" / "PROJECT_INSTRUCTIONS.txt").read_text(encoding="utf-8").strip()
    readme = (ROOT / "README.zh.md").read_text(encoding="utf-8")
    assert txt in readme
