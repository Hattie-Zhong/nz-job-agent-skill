# nz-job-agent-skill

An AI skill that helps job seekers in **New Zealand** apply for one job or
internship at a time. It checks eligibility, researches the company, gives an
honest match score, then writes a targeted CV and cover letter **using only
facts from your own profile**. It never invents experience.

It uses the open [Agent Skills](https://agentskills.io) format, so the same
skill works in several AI tools.

[中文使用说明（不会编程也能用）](README.zh.md)

## What it does

1. **Eligibility gate**: PASS / UNCLEAR / FAIL against your visa and availability.
2. **Research**: company, people and recent news, every fact with a source.
3. **Match score out of 100**: technical, domain, projects, experience, role fit.
4. **Checkpoint**: you decide whether to continue.
5. **Strategy**: what your CV and letter will emphasise. You approve it.
6. **CV and cover letter**, then a **recruiter-style review** of both.
7. **Export to .docx** and an automatic check: page count, word count,
   leftover Markdown, dashes, file names.
8. **Tracker** of every application.

## Choose how to use it

| You have | Route | Install anything? |
|---|---|---|
| A Claude account (Free, Pro or Max) | A. Claude web or desktop app | No |
| ChatGPT Plus | B. ChatGPT Project (beta, being tested) | No |
| Claude Code, Codex CLI or Gemini CLI | C. Command line | Python 3.10+ and git |

Download the upload packages from the
[Releases page](https://github.com/Hattie-Zhong/nz-job-agent-skill/releases/latest).

### A. Claude web or desktop app
1. Settings > Capabilities: turn on **Code execution and file creation**
   (called **Create and edit files** in newer layouts).
2. Customize > Skills > **+** > **Create skill** > **Upload a skill**:
   upload `nz-job-application.zip`.
3. Start a new chat, upload anything about yourself (CV, old cover letters,
   visa, certificates, a zip of everything) or just describe yourself, then
   paste a job advert. Copying the advert text (Ctrl+A, Ctrl+C on the job page)
   works best; links also work, but sites such as SEEK sometimes block AI tools.
4. At the end you can download `my-job-search.zip`. Next time, uploading just
   that file is enough, but uploading your files again also works.

### B. ChatGPT Project (beta)
1. Unzip `chatgpt-project-files.zip`.
2. Create a new Project in ChatGPT.
3. Project settings: paste the text of `PROJECT_INSTRUCTIONS.txt` into the
   instructions box. Set memory to project-only and turn off file library access.
4. Sources: add every file in the `project-files` folder.
5. Start a chat inside the Project, upload anything about yourself, then paste
   a job advert or link.

This route has not been fully tested yet. Please report what works and what does not.

### C. Command line (Claude Code, Codex CLI, Gemini CLI)

```bash
git clone https://github.com/Hattie-Zhong/nz-job-agent-skill.git
cd nz-job-agent-skill
pip install -r requirements.txt
python skills/nz-job-application/scripts/init_workspace.py
```

This creates `my-job-search/`, your private workspace. It is in `.gitignore`
and never leaves your computer. Put any of your files (CV, old letters,
certificates) in `my-job-search/inbox/`, open your agent in this folder, say
`help me apply for jobs`, then paste a job advert or link.
Claude Code reads `CLAUDE.md`, Codex reads `AGENTS.md`, Gemini CLI reads
`GEMINI.md`; all three point to the skill.

## The Alex Chen example

`examples/alex-chen/` is a **fully fictional** sample workspace. It shows what a
filled-in profile looks like and is used by the automated tests. The skill
never reads it as your profile.

To try it (command line route):

```bash
cp -r examples/alex-chen my-job-search
mv my-job-search/config.example.yaml my-job-search/config.yaml
```

When you are done and want to start with your own details:

```bash
python skills/nz-job-application/scripts/init_workspace.py --reset
```

This moves the old workspace to `my-job-search-backup-<date>` (nothing is
deleted) and creates a blank one. Delete the backup folder yourself when you
no longer need it.

## Your privacy

- Everything about you lives in `my-job-search/` (or `my-job-search.zip` in the
  web apps). Git ignores both.
- The skill never stores passport, visa, IRD or bank account numbers.
- Before publishing a fork, run
  `python skills/nz-job-application/scripts/privacy_scan.py`.

## For maintainers

```bash
pytest -q                        # run the tests
python tools/build_release.py    # build dist/*.zip for the Releases page
```

## Disclaimer

This tool helps you write; you are responsible for what you send. Always read
the final CV and letter yourself. Visa and work-rights information comes only
from what you enter; check your own visa conditions.

## Licence

MIT
