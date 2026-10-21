# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter classifies comments from r/bangtan (https://www.reddit.com/r/bangtan/),
the main English-language BTS subreddit, into three labels:
- `info`: gives the reader something checkable.
- `opinion`: takes a side another fan could argue with.
- `reaction`: expresses the writer's own feelings or experience.

I chose r/bangtan because it is public, posts 100+ comments a day, and varies
widely in substance: a sourced, detailed answer often sits next to a one-word
cheer in the same thread. It is not built around one show or release, so the
examples carry no spoilers. My Milestone 1 reading notes are in
[community_notes.md](community_notes.md).

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `info`

**Definition:** The comment supplies something checkable the reader could use or verify (a fact, a resource, a source, or context about what happened) without taking a side another fan could argue with.

**Example 1:**
> The last photo that most are discussing in this thread is an ARMY at the barricade at one of the concerts, with a sign that says "i wanna be you dimple match". She is smiling and showing off her dimples, which are very similar to Namjoons dimples!
>
> (r/bangtan comment [phri391](https://www.reddit.com/r/bangtan/comments/1xa1z82/_/phri391/))

**Example 2:**
> Welcome! Generally BT21 stuff is easier to come by than BTS stuff. If you have a Miniso by you, they usually have lots of BT21 things. :)
>
> (r/bangtan comment [phrzej4](https://www.reddit.com/r/bangtan/comments/1x8bnqb/_/phrzej4/))

### `opinion`

**Definition:** The comment takes a side another fan could argue with (a judgment about the quality of BTS's work, a comparison or ranking, an explanation of why something happened, a reading of what something says about the members, or a prediction), whether or not it cites facts.

**Example 1:**
> Hands down the documentaries - burn the stage, bring the soul, break the silence, and the latest beyond the star. I prefer the series versions over the films.
>
> The Netflix documentary was good too but I liked that the ones produced by bighit had individual interviews and seemed to explore the harder topics rather than just fly on the wall.
>
> (r/bangtan comment [phrw4iy](https://www.reddit.com/r/bangtan/comments/1xa5j1v/_/phrw4iy/))

**Example 2:**
> Translation: I AM WINNING. THEY ARE BECOMING AN INSTRUMENT BAND.
>
> (But really, learning new instruments in your 30s takes commitment. BTS really loves BTS.)
>
> (r/bangtan comment [phtragd](https://www.reddit.com/r/bangtan/comments/1xagki0/_/phtragd/))

### `reaction`

**Definition:** The comment expresses the writer's own feelings, taste, or personal experience about a post, a member, or a moment, without supplying checkable information for the reader or taking a side another fan could argue with.

**Example 1:**
> my precious hobii, seeing him smile makes me so happyy
>
> (r/bangtan comment [phv3luq](https://www.reddit.com/r/bangtan/comments/1xa2yl2/_/phv3luq/))

**Example 2:**
> So much beauty it’s overwhelming
>
> (r/bangtan comment [phu1xse](https://www.reddit.com/r/bangtan/comments/1xagki0/_/phu1xse/))

### The hardest boundary

**Which two labels:** `reaction` vs `opinion`. The real comment that sits between them is [phv7dt2](https://www.reddit.com/r/bangtan/comments/1xagki0/_/phv7dt2/), posted under Yoongi's Instagram photo dump:

> I really adore that he chose a photo of him and Jungkook where Jungkook is being silly and doing Yoongi’s signature dance move. Even when he’s 60, Jungkook will be annoying and Yoongi will be so happy about it

Each label is plausible:
- *`reaction`:* it opens with "I really adore", and the last line reads as affectionate exaggeration.
- *`opinion`:* the last line predicts something about the members' relationship that a fan could dispute.

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->

First strip the feeling, then decide by what is left:
- **Strip:** emotion words (love, adore, crying), bare praise and superlatives (so pretty, unreal, perfect), feeling idioms ("hits different"), emojis, and fandom set phrases ("boyfriend-coded").
- **About the writer** ("my favorite", "for me", "I was there"): it's `reaction`.
- **Only restates what is plainly in the post** ("he's smiling", "he looks like he's enjoying himself"): it's `reaction`.
- **Adds something about BTS, their work, or the fandom that the post doesn't show:** it's `opinion`, even if joking or exaggerated. That covers why something happened, what it means, a generalization ("he always..."), a specific quality ("dated"), an unmarked comparison or ranking, or a prediction.

Under this rule phv7dt2 is `opinion`: after "I really adore" is stripped, the second sentence makes a claim about the members' lasting relationship that the photo does not show.

The rules for the other two boundaries, the exclusion list, and the full AI stress test are in [taxonomy_stress_test.md](taxonomy_stress_test.md). The other boundaries are `info` vs `opinion` and `info` vs `reaction`. The exclusion list covers image-only, link-only, question-only, mod, non-English, and off-topic comments.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** These are public r/bangtan comments, copied exactly as posted. Reddit blocks access from my working environment, so they were pulled through the Arctic Shift public Reddit archive (https://arctic-shift.photon-reddit.com). Every row's Reddit comment ID and permalink are in [labelling/sources.csv](labelling/sources.csv), and the ID is also in each row's `note`.

How the pool was built:
- **Download:** the 2,000 most recent comments, posted 13-20 Oct 2026.
- **Automatic filter:** removed comments that were deleted, from bots or mods, image/GIF/link-only (under 4 words outside links), non-English, question-only, over 220 words, or an exact or near-duplicate of another kept comment.
- **Thread exclusions:** dropped marketplace (buy/sell) threads, and off-topic threads that aren't about BTS or the fandom (the book club, the weekly off-topic room, a "letters to your younger self" project). That left 1,379 comments.
- **First sample:** 280 at random (seed 201), at most 8 per thread so photo-dump threads can't dominate.
- **Top-up:** the first sample leaned heavily `reaction`, so I added 110 more (seed 202), drawn only from discussion, question, info, milestone, news, live-translation, weekly-room and tour-megathread threads. They were chosen by thread type, not by label.

That makes 390 candidate comments from 70 threads.

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `info` |  |  |
| `opinion` |  |  |
| `reaction` |  |  |
| **Total** |  | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

**2.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

**3.**
> *The post:*
>
> *Could have been:*
>
> *I chose, because:*

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Using Claude Code, I gave an AI agent my three label definitions without the decision rules, and asked for eight synthetic comments that sit on the label boundaries, without saying which label was correct.
- *What came back:* Eight realistic fan comments. Three of them I could not classify cleanly: two used a fact to win an argument, and one rested on the set phrase "the most yoongi thing he has ever said".
- *What I changed:* I changed the `info` definition to exclude taking a side. I added bare praise and set phrases to the strip list in the decision rule. I added rules for the two other boundaries. A second round, aimed at breaking the revised rules, led to five more clarifications. A blind re-label of all 16 posts under the final rules agreed with mine 16/16. Details are in [taxonomy_stress_test.md](taxonomy_stress_test.md).

**Moment 2**

- *What I asked for:* For the borderline comment phv7dt2, the brief's prompt: make the strongest case for each of the two labels, without saying which is right or rewriting my definitions.
- *What came back:* A strong case for both labels. The best argument for `reaction` was that "when he's 60" is affectionate exaggeration, not a real forecast.
- *What I changed:* I made the decision rule settle that case explicitly. Exaggeration does not cancel a claim; what matters is whether what is left says something about the members that the post does not show.

**Pre-labelling disclosure:** Claude Code (an AI agent) did most of the Milestone 1-4 setup work:
- **Milestones 1 and 2:** it pulled the comments, drafted the reading notes, proposed the labels and rules, and ran the stress test. I reviewed the results.
- **Milestone 4:** it collected the 390 candidate comments and pre-labelled 370 of them, marking 77 as unsure with a reason. Those pre-labels are in [labelling/review_ai_suggestions.csv](labelling/review_ai_suggestions.csv).
- **The 20 cold rows** were not pre-labelled. I label those myself, without AI.
- **Every pre-labelled row has to be read and given my own label** before it can enter `labels.csv`. The `note` column records, for each row, whether I kept or changed the AI label.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
