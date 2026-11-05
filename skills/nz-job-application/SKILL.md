---
name: nz-job-application
description: Research one New Zealand job or internship at a time and write a targeted CV and cover letter using only facts from the user's own materials. Use when the user asks for help applying for jobs, uploads a CV or other personal documents for a job search, pastes a job advert or job link, or reports an application outcome.
---

# NZ Job Application Agent

This skill helps a job seeker in New Zealand apply for one job at a time:
eligibility check, company research, an honest 100-point match score, then a
targeted CV and cover letter, a recruiter-style review, and a clean .docx export.

It never invents experience. Every claim about the user must come from what
the user uploaded or told you.

**Make it effortless.** Users are not technical. Never ask them to type
commands, name files a certain way, or use a special format. Accept whatever
they give you and work out what it is.

## Where things live

- `<skill>` means the folder that contains this SKILL.md.
- All personal data lives in a **workspace** folder, by default `my-job-search/`
  in the current working directory. Nothing personal is ever stored inside `<skill>`.

```
my-job-search/
  config.yaml            # name, contact details, limits
  profile/               # the facts about the user, built from their materials
    cv_master.md  eligibility.md  verified_facts.md  writing_rules.md
    links.md  projects/<project>.md  CHANGELOG.md
  inbox/                 # the user's own files, as uploaded. Read only.
  applications/
    tracker.csv
    <YYYY-MM-DD>-<company>-<role>/
```

`examples/alex-chen/` in the repository is a fictional sample. Never read it
as the user's profile.

## Starting a conversation

If the user has not given you anything yet, send this one short message in
their language, and nothing else:

> Upload anything about yourself: CV, old cover letters, visa, certificates,
> a zip of everything, or the file I gave you last time. If you'd rather not
> upload something, just tell me in words. Then paste the job advert or link.

## When the user uploads anything

Run, with every uploaded file path:

```
python <skill>/scripts/load_upload.py <file> [<file> ...]
```

It accepts any files or zips, restores a saved workspace if one is inside, and
copies everything else into `inbox/`. Then:

- **RESTORED:** the user's profile is back. Do not ask setup questions again.
- **NEW or UPDATED:** read every file listed under INBOX FILES and build or
  update the profile by following `references/setup.md`. Do this silently;
  only ask about facts that are still missing and needed.

Files you cannot read (for example scanned images when you cannot view them):
tell the user in one line and ask them to paste the text or tell you the facts.

### Identity documents
For a passport, visa label, visa approval letter, driver licence or national ID:
- record only what an application needs: citizenship, visa type, expiry date,
  work conditions, licence class
- **never** record document numbers, dates of birth, addresses or photos
- then delete that file from `inbox/` so it is never packed or kept

## When the user pastes a job advert or a job link

Anything that looks like a job advert (pasted text, a screenshot, a file) or a
link to a job page **is** the request to apply. Do not wait for words like
"apply". Follow `references/workflow.md` from Step 1.

If no profile exists yet and nothing was uploaded, ask once for their CV (or a
few lines about their study, work and visa), then continue.

## Other things the user may say

| User says | Do this |
|---|---|
| "I submitted", "rejected", "got an interview", "skip it" | update the tracker (below) |
| "status", "what have I applied for" | `python <skill>/scripts/tracker.py list` |
| a new fact, correction, or new file | update the profile ("Updating the profile") |
| "start again", "clear everything" | `python <skill>/scripts/init_workspace.py --reset` (moves the old workspace to a backup folder; never deletes it) |

## Core rules (apply to every task)

### Evidence
1. The user's materials, `profile/`, and what the user says in the conversation
   are the only sources about the user.
2. Never invent or exaggerate experience, duties, skills, results, grades,
   qualifications, work rights, or employment or client relationships.
3. Never infer an employment or client relationship from a project or repo name.
4. For group projects, only claim the parts recorded as the user's own work.
   If a file does not say which part was theirs, ask once.
5. Never describe planned or unfinished work as completed.

### Facts
1. **Write back.** Any fact the user states, confirms or corrects is written
   into the right file in `profile/` immediately (or `verified_facts.md` if
   nothing fits), and logged in `profile/CHANGELOG.md`.
2. **Never ask twice.** Search `profile/` and `inbox/` before asking anything.
3. **No fact questions during an application.** If a claim is not supported,
   use the safer supported wording or leave it out, and list the change in the
   next summary. Missing hard requirements go under "Biggest gaps" at Checkpoint 1.

### Checkpoints
A checkpoint is a decision the user makes. At every checkpoint in
`references/workflow.md` you must **end your turn and wait for the reply**,
even if the score is high and even in auto-approve mode. Writing "wait for
the user" into a file is not stopping.

### Files
- Never modify anything in `inbox/` (except deleting identity documents as above).
- Never overwrite `profile/cv_master.md` during an application.
- Do not edit application folders whose status is Applied, Interview, Offer,
  Rejected, Skipped, Low score or Not eligible (renaming them is allowed).

### Privacy
- Never store passport, visa, IRD, driver licence or bank account numbers,
  dates of birth, or passwords.
- Collect only public professional information about other people. Never
  collect private contact details.
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

## Web chat mode (Claude.ai, ChatGPT, Gemini in the browser)

You are in web chat mode when files do not survive between conversations.
Then also:

1. Never rely on memory of an earlier conversation. Only uploaded files and
   this conversation count.
2. After the profile is first built, at the end of each application, and
   whenever a profile fact changes, run
   `python <skill>/scripts/workspace_zip.py pack` and offer `my-job-search.zip`
   for download with this line (in the user's language):
   "Optional: save this file. Next time you can upload just this one file
   instead of everything again."
3. Give the exported CV and cover letter .docx files as separate downloads.
4. If the templates folder is not available (for example in a ChatGPT
   Project), create the workspace files from `profile_templates.md`.
5. If Python cannot run at all, keep the same workflow, write the CV and letter
   as plain text the user can paste into Word, and keep any changed profile
   facts in the chat.

## Platform notes

- **No web access:** ask the user to paste the advert and any company pages.
  Never guess page content.
- **No subagents:** run the recruiter review in `references/reviewer.md` as a
  separate pass that reads only the three files it lists, ignoring everything
  else you know.
