# job-agent-skill

An AI skill that helps job seekers in **New Zealand** apply for one job or
internship at a time: it checks eligibility, researches the company, gives an
honest match score, then writes a targeted CV and cover letter **using only
facts from your own profile**. It never invents experience.

Works with any AI coding agent that supports the open
[Agent Skills](https://agentskills.io) format and can run Python, for example
Claude Code, OpenAI Codex CLI and Google Gemini CLI.

[中文说明](README.zh.md)

## What it does

1. **Eligibility gate**: PASS / UNCLEAR / FAIL against your visa and availability.
2. **Research**: company, people and recent news, every fact with a source.
3. **Match score out of 100**: technical, domain, projects, experience, role fit.
4. **Checkpoint**: you decide whether to continue.
5. **Strategy**: what your CV and letter will emphasise. You approve it.
6. **CV and cover letter**, then a **recruiter-style review** of both.
7. **Export to .docx** and an automatic check: page count, word count,
   leftover Markdown, dashes, file names.
8. **Tracker** of every application, with folders renamed by status.

## Quick start

You need Python 3.10+ and git.

```bash
git clone https://github.com/<your-account>/job-agent-skill.git
cd job-agent-skill
pip install -r requirements.txt
python skills/nz-job-application/scripts/init_workspace.py
```

This creates `my-job-search/`, your private workspace. It is in `.gitignore`
and never leaves your computer.

Then open your AI agent **in this folder** and say:

1. `Set up my job profile` (put your current CV in `my-job-search/inbox/` first)
2. `Apply for this job: <link>` or paste the advert

The agent stops at each checkpoint and waits for your answer.

## How your AI finds the skill

- Claude Code reads `CLAUDE.md`, Codex reads `AGENTS.md`, Gemini CLI reads
  `GEMINI.md`. All three point to `skills/nz-job-application/SKILL.md`.
- To use the skill in any folder, copy `skills/nz-job-application/` to your
  agent's skills folder (for example `~/.claude/skills/`, `~/.codex/skills/`
  or `~/.gemini/skills/`).

## Your privacy

- Everything about you lives in `my-job-search/`, which git ignores.
- The skill never stores passport, visa, IRD or bank account numbers.
- Before publishing a fork, run:
  ```bash
  python skills/nz-job-application/scripts/privacy_scan.py
  ```

## Try the example

`examples/alex-chen/` is a fully fictional workspace. Copy it to
`my-job-search/`, rename `config.example.yaml` to `config.yaml`, and run:

```bash
python skills/nz-job-application/scripts/export_docx.py my-job-search/applications/2026-11-05-kowhai-analytics-data-analyst-intern
python skills/nz-job-application/scripts/check_output.py my-job-search/applications/2026-11-05-kowhai-analytics-data-analyst-intern
```

Page counts need Microsoft Word or LibreOffice. Without either, that check is
skipped and you check the page count yourself.

## Run the tests

```bash
pytest -q
```

## Disclaimer

This tool helps you write; you are responsible for what you send. Always read
the final CV and letter yourself. Visa and work-rights information comes only
from what you enter; check your own visa conditions.

## Licence

MIT
