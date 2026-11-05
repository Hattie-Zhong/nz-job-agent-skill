---
name: nz-job-application
description: Research one New Zealand job or internship at a time and write a targeted CV and cover letter using only facts from the user's own profile files. Use when the user wants to set up their job-search profile, apply for a job (gives a job link or pastes an advert), update their profile, or record an application outcome.
---

# NZ Job Application Agent

This skill helps a job seeker in New Zealand apply for one job at a time:
eligibility check, company research, an honest 100-point match score, then a
targeted CV and cover letter, a recruiter-style review, and a clean .docx export.

It never invents experience. Every claim about the user must come from their
own profile files or from what they say in the conversation.

## Where things live

- `<skill>` means the folder that contains this SKILL.md.
- All personal data lives in a **workspace** folder, by default `my-job-search/`
  in the current working directory. Nothing personal is ever stored inside `<skill>`.

```
my-job-search/
  config.yaml            # name, contact details, limits (private)
  profile/               # the only source of truth about the user
    cv_master.md
    eligibility.md
    verified_facts.md
    writing_rules.md
    links.md
    projects/<project>.md
    CHANGELOG.md
  inbox/                 # user's original files (old CVs, letters). Read only.
  applications/
    tracker.csv
    <YYYY-MM-DD>-<company>-<role>/
```

If `my-job-search/config.yaml` does not exist, the user has not set up yet:
run `python <skill>/scripts/init_workspace.py` and follow `references/setup.md`.

## What the user can ask for

| User says | Do this |
|---|---|
| "set up", "start", first use | `references/setup.md` |
| a job URL, a pasted advert, "apply for ..." | `references/workflow.md` |
| "update my profile", a new CV, project, grade or visa change | "Updating the profile" below |
| "I submitted", "rejected", "got an interview", "skip it" | update the tracker (see below) |
| "status", "what have I applied for" | `python <skill>/scripts/tracker.py list` |

Read the reference file for a task before starting it. Do not load all
reference files at once.

## Core rules (apply to every task)

### Evidence
1. `profile/` is the only authoritative source about the user, together with
   what the user states directly in the current conversation.
2. Never invent or exaggerate experience, duties, skills, results, grades,
   qualifications, work rights, or employment or client relationships.
3. Never infer an employment or client relationship from a project or repo name.
4. For group projects, only claim the parts recorded as the user's own work.
5. Never describe planned or unfinished work as completed.

### Facts
1. **Write back.** Any fact the user states, confirms or corrects is written
   into the right file in `profile/` immediately (or `verified_facts.md` if
   nothing fits), and logged in `profile/CHANGELOG.md`.
2. **Never ask twice.** Search `profile/` before asking anything.
3. **No fact questions during an application.** If a claim is not supported,
   use the safer supported wording or leave it out, and list the change in the
   next summary. Missing hard requirements go under "Biggest gaps" at Checkpoint 1.

### Checkpoints
A checkpoint is a decision the user makes. At every checkpoint in
`references/workflow.md` you must **end your turn and wait for the reply**,
even if the score is high and even in auto-approve mode. Writing "wait for
the user" into a file is not stopping.

### Files
- Never modify or delete anything in `inbox/`.
- Never overwrite `profile/cv_master.md` during an application.
- Do not edit application folders whose status is Applied, Interview, Offer,
  Rejected, Skipped, Low score or Not eligible (renaming them is allowed).

### Privacy
- Never store passport, visa, IRD or bank account numbers, or passwords.
- Collect only public professional information about people. Never collect
  private contact details.
- Never copy anything from the workspace into `<skill>` or into a public repo.

### Language
- Talk to the user in the language they write in.
- Write all profile files, research, CVs and cover letters in NZ English.

## Updating the profile

1. Find which files in `profile/` are affected and read them first.
2. Compare: additions, changes, conflicts, outdated lines.
3. Update only the affected lines. Never rewrite unrelated content or create duplicates.
4. Append a dated line to `profile/CHANGELOG.md`.
5. Tell the user what changed in a short list.

## Tracker

`applications/tracker.csv` is the single record of every application. Never
ask the user to edit it. Always change it with the script, which also renames
the folder with the right status prefix:

```
python <skill>/scripts/tracker.py new --company "<Company>" --role "<Role>"
python <skill>/scripts/tracker.py set <folder> --status "Applied"
python <skill>/scripts/tracker.py set <folder> --score 72 --next-step "Wait for response"
python <skill>/scripts/tracker.py list
```

Statuses: In progress, Paused, Ready to submit, Applied, Interview, Offer,
Rejected, Skipped, Low score, Not eligible.

## Platform notes

This skill works in any agent that can read files and run Python
(Claude Code, Codex CLI, Gemini CLI and others).

- **No web access:** ask the user to paste the advert and any company pages.
  Never guess page content.
- **No subagents:** run the recruiter review in `references/reviewer.md` as a
  separate pass that reads only the three files it lists, ignoring everything
  else you know.
- **Cannot run Python:** write the Markdown files, then tell the user that the
  export and checks need Python on their own computer.
