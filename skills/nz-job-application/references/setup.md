# Setup: build the user's profile

Goal: turn the user's existing CV and a short interview into the files in
`my-job-search/profile/`, so later applications never need to ask again.

## Rules for this conversation
- Ask at most 4 questions per turn. Group related questions.
- Write each answer into the right file immediately, before asking the next batch.
- Accept "skip" or "don't know" for anything. Leave the field empty; never guess.
- Never ask for passport, visa, IRD or bank account numbers. If the user offers
  one, do not store it.
- Explain in plain words why you need each item if the user seems unsure.

## Step 0: Create the workspace
If `my-job-search/config.yaml` does not exist, run:

```
python <skill>/scripts/init_workspace.py
```

Then tell the user what was created and that this folder never leaves their computer.

## Step 1: Existing materials
Ask the user to put their current CV, and one or two past cover letters if they
have them, into `my-job-search/inbox/`, or paste the text into the chat.
Read them. Never modify files in `inbox/`.

## Step 2: Contact details -> config.yaml
Fill in `candidate` in `config.yaml`: full name as it should appear on a CV,
file name form (for example `Alex_Chen`), email, phone, city, LinkedIn, GitHub.
Also add the user's surname and any former employer or school names they do
not want published to `privacy.private_terms`.

## Step 3: CV facts -> cv_master.md
Extract everything from the old CV into `profile/cv_master.md` using its
template sections. Then confirm with the user in one batch:
- anything that looked unclear or inconsistent (dates, titles)
- for each job: the 3 to 6 duties they actually did and any real results with numbers
- skills they actually use, and where each was used (job, course or project)

## Step 4: Eligibility -> eligibility.md
Ask, in up to two batches:
1. Citizenship, and NZ residency or visa type (for example student visa,
   post-study work visa, resident). No visa numbers.
2. Visa expiry date and the exact work conditions written on their visa
   (for example the weekly hour limit during study and whether full-time work
   is allowed in scheduled breaks). Ask them to copy the wording from their
   visa, not from memory.
3. Study: qualification name, institution, year of study, expected completion,
   and term and exam end dates for the coming months.
4. Availability: earliest start date, hours, locations they can work in,
   willingness to relocate, NZ driver licence status.

## Step 5: Projects -> profile/projects/
For each project they want to use (course, personal or work):
one file per project from `projects/_template.md`. Must record:
- what the project does, tools used, link if public
- group or solo; if group, exactly which parts were their own work
- what is finished and what is still planned
- results with numbers, only if real
- "Do not claim" lines for anything easy to overstate

## Step 6: Writing style -> writing_rules.md
If past cover letters exist, describe their style in `writing_rules.md`
(tone, typical sentence length, words they often use, habits to watch).
Record any claim in an old letter that the profile does not support in the
"Do not reuse" table. Ask for any personal rules (for example "never mention
my age", "always say Master of Applied Data Science in full").

## Step 7: Check and finish
1. Re-read every profile file and confirm there are no ID numbers, bank
   details or passwords.
2. Show the user a short summary: what was filled, what is still empty.
3. Say: "Setup is done. Send me a job link or paste an advert to start."
