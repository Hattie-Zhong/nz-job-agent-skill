# Apply workflow: one job, start to finish

This workflow runs in stages. **Each CHECKPOINT ends your turn.** Never run
two stages in one turn. Follow the steps in order.

Paths: `WS` = the workspace (`my-job-search/`), `JOB` = this job's folder.
Read `nz_context.md` once before Step 2.

## Step 1: Job extraction

1. Open the job link. If it cannot be opened or is incomplete (LinkedIn often
   is), STOP and ask the user to paste the full advert. Never guess.
2. Create the folder and tracker row with the script:
   ```
   python <skill>/scripts/tracker.py new --company "<Company>" --role "<Role>" --closing-date YYYY-MM-DD
   ```
   If it reports that a folder for the same role already exists, STOP and tell the user.
3. Save the advert text, unedited, as `JOB/jd.md`. Nothing else goes in jd.md.
4. Extract: company, job title, location, type, dates, hours, deadline,
   responsibilities, hard requirements, preferred requirements, education,
   technical, domain, work rights, driver licence, experience, soft skills.
   Keep HARD REQUIREMENTS, PREFERRED REQUIREMENTS and RESPONSIBILITIES separate.
5. Flag if the deadline has passed or is within 3 days.

## Step 2: Eligibility gate

Compare the advert with `WS/profile/eligibility.md`. Result: PASS / UNCLEAR / FAIL.

- Judge only against requirements the advert states. Inferences are never blockers.
- If the advert has a formal "Eligibility" section, judge against it first.
- "Ideally" or "preferred" is a preference, not a gate.
- Do not assume a postgraduate student meets a rule written for undergraduates
  (for example "penultimate year of a Bachelor's"). That is UNCLEAR.
- **Hours vs visa conditions are UNCLEAR, not FAIL.** If the role is full-time
  but the user's visa limits hours during study, the employer may still accept
  full-time in holidays and fewer hours during term. Mark UNCLEAR and draft the
  question to the recruiter. Use FAIL only when the advert itself rules the
  user out (for example "must be an NZ citizen or resident", "no visa
  sponsorship" for someone who needs it, or a start or end date the user's visa
  cannot cover).

Then:
- **PASS:** continue to Step 3. No checkpoint.
- **FAIL** (a confirmed hard blocker): print the reason, run
  `tracker.py set <folder> --status "Not eligible"`, END YOUR TURN.
- **UNCLEAR:** go to Checkpoint 0.

### CHECKPOINT 0 (UNCLEAR only)
Print the exact advert wording, the user's matching eligibility facts, and your
reading. Draft one short, polite question the user can send the recruiter.
Ask: "Eligibility is unclear on <item>. Continue to scoring? (yes / no)"
END YOUR TURN.
- "no": set status Skipped.
- "yes": continue, and keep the risk visible in every later summary.

## Step 3: Company and people research

- Company: what it does, business model, customers, size, ownership, strategy,
  recent changes, technology and data initiatives.
- People: CEO or MD, relevant business unit leader, likely hiring manager,
  recruiter if publicly linked to the role. Label each CONFIRMED / HIGHLY LIKELY
  / POSSIBLE / UNKNOWN. A department leader is not automatically the hiring manager.
- Recent signals (last 12 months if possible), each with its relevance to this role.
- Source priority: official site, annual report, newsroom, official social
  media, parent company, reputable NZ media.
- Every fact needs a source URL, date and confidence.
- Keep research short: **at most 6 sources and about 10 searches or page
  reads in total.** Start with the company's own site and newsroom. Stop as
  soon as you have one confirmed recent signal for the letter and enough to
  judge the role; more would not change the strategy.

## Step 4: Role intelligence

Answer, keeping two lists, FACTS (stated in the advert) and INFERENCES
(labelled STRONG or WEAK, with evidence):
- why they are likely hiring now (the business problem)
- what the person will spend most time doing
- what success after three months looks like
- hidden selection criteria and the kind of person they want
- hard screening risks (from FACTS only)

A weak inference must never appear as a fact in the application.

**Internship fairness:** for internships, never treat prior work experience,
career length, age or being a postgraduate as a negative. Do not infer a
preference for younger or undergraduate candidates unless the advert says so.

## Step 5: Evidence

Read `WS/profile/` and the relevant `WS/profile/projects/` files.
Build a match matrix: requirement -> evidence -> source file -> STRONG / PARTIAL / MISSING.
The project file is the authority on the user's role and allowed claims.
If sources conflict, use the more conservative claim and list the conflict at Checkpoint 1.

## Step 6: Match score

Use `scoring.md`. Show points, reason, evidence file and missing evidence for
every category. Never award points for anything not verifiable.

## Step 7: Evidence selection

Choose best project #1, #2 and optional #3, best professional experience and
best transferable experience, each linked to the business problem from Step 4.
Do not reuse the same projects by default. Also list **What NOT to emphasise**.

Save `JOB/research_report.md` (Steps 1 to 4 with sources) and
`JOB/match_matrix.md` (Steps 5 to 7). Record the score:
`tracker.py set <folder> --score <N>`.

### CHECKPOINT 1: Match score (HARD STOP)
Print in the chat:

```
ELIGIBILITY: PASS / UNCLEAR (reason)
MATCH SCORE: XX / 100
  Technical            xx / 30
  Domain / Business    xx / 20
  Project evidence     xx / 20
  Professional         xx / 15
  Role-specific fit    xx / 15
CLASSIFICATION: ...
Strongest reasons: 1. 2. 3.
Biggest gaps: 1. 2. 3.
Best project #1: ...
Best project #2: ...
What NOT to emphasise: ...
RECOMMENDATION: PROCEED / CONSIDER / SKIP
```

Ask exactly: "Score is <N>/100 (<classification>). Continue to CV and cover letter strategy? (yes / no)"
END YOUR TURN. Do not create any strategy, CV or letter file in this turn.
- "no": status Low score if below 55, otherwise Skipped.
- "yes": continue.

## Step 8: CV strategy

Decide summary emphasis, skills order, project order, experience order, bullet
priority, keywords, links, and what to shorten or cut. Never add a skill just
because the advert mentions it. Save `JOB/cv_strategy.md`.

## Step 9: Cover letter strategy

Save `JOB/cover_letter_strategy.md`: core story, company signal, why this
company, why this role, main and secondary evidence, transferable experience,
main risk and whether to address it, what not to mention, tone, paragraph plan.
The logic must break if the company name is swapped for another employer.

Default paragraph plan (one short paragraph each):
1. What this company is doing now that draws the user in (a confirmed signal)
2. Why this role fits
3. Strongest evidence, linked to their problem
4. Secondary evidence or experience
5. What the user would bring to the team

### CHECKPOINT 2: Strategy (HARD STOP)
Summarise the planned CV changes (what moves up, what is cut) and the letter story.
Ask exactly: "Approve this strategy and write the CV and cover letter? (yes / changes)"
END YOUR TURN.

## Step 10: Write the CV and cover letter

- CV: from `cv_master.md`, `verified_facts.md` and project files only, following
  the approved strategy, `writing_rules_default.md` and the user's
  `writing_rules.md` (user rules win). Save `JOB/cv_targeted.md`.
- Letter: from the approved strategy, the same rules, and the user's style.
  Never reuse claims in the "Do not reuse" table. Save `JOB/cover_letter.md`.
- Wherever `verified_facts.md` gives exact wording, use it.

Markdown format the export script understands:
- CV: `# Full Name`, then contact lines, then `## Section` headings, `- ` bullets, `**bold**`.
- Letter: plain paragraphs separated by one blank line. No headings, no bullets.

## Step 10b: Recruiter review

1. Self-check both drafts against "What NOT to emphasise" in match_matrix.md. Fix conflicts.
2. Run the review in `reviewer.md`: in a subagent if your tool has them,
   otherwise as a separate pass that reads only `jd.md`, `cv_targeted.md` and
   `cover_letter.md`.
3. Check each suggested fix against the user's rules and verified facts. Show
   the review unchanged, your self-check changes, and one line under any fix
   that conflicts with the user's rules.
4. Ask: "Reply OK to apply all fixes, or 'OK but skip 2' to skip some." END YOUR TURN.
5. Apply the approved fixes and list each change in one line.

## Step 11: Final check (no questions)

Fix these yourself:
- every claim about the user traces to `profile/`; group work is not shown as
  solo; nothing planned is described as done
- every company fact has a source in research_report.md
- dates, availability and work rights match eligibility.md
- the CV and letter agree on dates, titles, availability and work rights
- every duty named in the letter also appears under the same employer in the CV
- correct company, role and links; the letter is dated today
- word limit from `config.yaml` (count every word in the letter, including
  heading, date, greeting and sign-off)

Show the final letter and the list of changes. Ask for approval to export. END YOUR TURN.

## Step 12: Export and check

```
python <skill>/scripts/export_docx.py <JOB>
python <skill>/scripts/check_output.py <JOB>
```

If any check FAILS, fix the .md source, export again and re-check, up to 3
times without asking. List every sentence you cut or changed. If it still
fails, show the result and stop. A SKIP for page count means no PDF converter
is installed: tell the user to open the .docx and check the page count themselves.

When all checks pass: `tracker.py set <folder> --status "Ready to submit"`
and tell the user the files are ready.

## Step 13: Submission

When the user says they submitted:
`tracker.py set <folder> --status "Applied" --next-step "Wait for response"`.
Do not ask anything else.
