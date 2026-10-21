# How to finish Milestone 4

Every post here is a real r/bangtan comment. They were pulled from the Arctic
Shift public Reddit archive and copied exactly as posted. Each row's Reddit
comment ID and permalink are in `sources.csv`.

## Fastest way: the terminal labeller

    .venv/bin/python labelling/label.py cold     # step 1
    .venv/bin/python labelling/label.py review   # step 2 (refuses until step 1 is done)
    .venv/bin/python labelling/label.py hard     # step 3
    .venv/bin/python labelling/label.py status   # progress

It shows one row at a time. Type `i`, `o`, `r` or `x` (EXCLUDE) and Enter. In
review, Enter on its own keeps the AI label shown, `b` goes back a row and `q`
quits. It saves after every row and resumes where you stopped. It only records
what you type. Editing the CSVs by hand works too, as below.

## Step 1: cold labels first, on your own (about 15 min)

Open `cold_20.csv`. For each row, write `info`, `opinion`, or `reaction` in
`your_label`, using only the definitions and rules in the README and
`taxonomy_stress_test.md`. Use no AI and don't look at the review sheet first.
If a row can't be labelled (question-only, mod message, etc.), write `EXCLUDE`.

## Step 2: review every AI suggestion (about 40-60 min)

Open `review_ai_suggestions.csv`. Claude suggested a label for each row in
`ai_label`, and marked 77 rows as unsure (`ai_unsure` = yes, reason in
`ai_note`). For **every** row, read the post and write your own label in
`your_label`: the same as `ai_label` if you agree, a different one if you
don't, or `EXCLUDE`. A blank `your_label` means "not reviewed", and that row is
left out of `labels.csv`.

## Step 3: hard cases

In `hard_cases.md`, write your final label and reason for at least three of
the cases. Use the same label in the review sheet.

## Step 4: build and check

    python labelling/build_labels.py           # check only
    python labelling/build_labels.py --write   # writes labels.csv

The script only includes rows you labelled. It writes the `note` column
(`cold`, or AI-assisted and kept or changed, plus the Reddit ID). It also
checks label names, duplicates, the 200-row floor, the brief's 70% cap and
criterion 3.
