# Setup: build the profile from whatever the user gave you

Goal: turn the user's uploaded files and anything they said into the files in
`my-job-search/profile/`, with as few questions as possible.

## Rules
- Do the work silently. Do not narrate each file you read.
- Never ask for something that is already in the uploaded files or the chat.
- Ask at most **one batch of up to 4 questions**, only for facts that are
  missing AND needed (see "Must have" below). Everything else can wait.
- Accept "skip" or "don't know". Leave the field empty; never guess.
- Never record passport, visa, IRD, licence or bank numbers, or dates of birth,
  even if they are in the files.
- If the user also sent a job advert, finish setup, then continue straight to
  `workflow.md` Step 1 in the same reply unless you had to ask questions.

## Step 1: Read everything
`load_upload.py` already listed the files in `inbox/`. Read each one:
CVs, cover letters, transcripts, certificates, references, visa documents,
project write-ups, portfolio links, LinkedIn exports. For identity documents,
follow "Identity documents" in SKILL.md (take the facts, then delete the file).

## Step 2: Fill the files

| Put this | In this file |
|---|---|
| name, email, phone, city, LinkedIn, GitHub | `config.yaml` (`candidate`). Also set `file_name`, e.g. `Alex_Chen` |
| education, work history with duties, skills with where they were used, certifications, volunteering | `profile/cv_master.md` |
| citizenship, visa type, expiry, work conditions, study dates, availability, licence | `profile/eligibility.md` |
| one file per project: what it does, tools, solo or group and their own part, finished vs planned, real results | `profile/projects/<name>.md` |
| style of their past cover letters (tone, sentence length, common words); claims in old letters that their other files do not support ("Do not reuse") | `profile/writing_rules.md` |
| exact wording the user confirms | `profile/verified_facts.md` |
| what you filled and from which file | `profile/CHANGELOG.md` |

Where two files disagree (for example different dates), keep the more
conservative version and ask about it in the one question batch.

## Step 3: Must have (ask only if missing)
1. Work rights in NZ: citizenship or visa type, and the work conditions on the
   visa (for students: weekly hour limit during study, full-time in breaks or not)
2. Visa expiry date (if on a visa)
3. When they can start, and full-time or part-time
4. For each group project they want to use: which part was their own work

Phrase the batch simply, for example:
"I've read your files. 4 quick things I couldn't find: ..."

## Step 4: Finish
1. Tell the user in 2 or 3 lines what you built (for example "Profile ready:
   2 jobs, 3 projects, student visa until March 2028").
2. Web chat mode: offer `my-job-search.zip` (see SKILL.md).
3. If no job advert has been sent yet, say: "Paste a job advert or link whenever you're ready."
