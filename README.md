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
the main English-language BTS subreddit, into four labels:
- `info`: gives the reader something checkable.
- `opinion`: takes a side another fan could argue with.
- `reaction`: expresses the writer's own feelings or experience.
- `question`: asks other fans for an answer. This was added later as a stretch feature; the first trained model (`results.json`) used only the first three.

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

### `question`

Added after the first training run, as stretch feature 3 (see [Stretch Features](#stretch-features)).

**Definition:** The comment's main point is to ask other fans for information, a recommendation, or help the writer doesn't have, so the natural reply is an answer.

**Example 1:**
> Anyone know when the digital viewing tickets for buenos Aires will come on weverse?
>
> (r/bangtan comment [phrewqm](https://www.reddit.com/r/bangtan/comments/1tkbrpt/_/phrewqm/))

**Example 2:**
> Where can we find a list of the reliable translators?
>
> (r/bangtan comment [pgmnoth](https://www.reddit.com/r/bangtan/comments/1x539re/_/pgmnoth/))

**Its hardest boundary, `question` vs `reaction` (Rule 4):** it is `question` only if another fan could answer it with a fact or a recommendation and the writer seems to want that answer. Rhetorical or gushing questions ("What even is that pose JK?") are not requests, so they go through Rule 1 as before. If a comment also makes a claim, label it by its main point: is it there to get an answer?

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

The rules for the other two boundaries, the exclusion list, and the full AI stress test are in [taxonomy_stress_test.md](taxonomy_stress_test.md). The other boundaries are `info` vs `opinion` and `info` vs `reaction`. The exclusion list covers image-only, link-only, mod, non-English, and off-topic comments. It used to include question-only comments too; since `question` was added they are labelled `question` instead.

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
I labelled in the terminal with [labelling/label.py](labelling/label.py), one post at a time, then built `labels.csv` with [labelling/build_labels.py](labelling/build_labels.py). Every row's `note` says which path it took.
- **Cold first, no AI:** I labelled 20 randomly chosen posts on my own, before starting the review of AI suggestions (the tool will not start the review until those are done). I kept 12 and excluded 8. Their note is `cold`.
- **AI pre-labelled, then reviewed by me:** Claude Code suggested a label for the other 370 posts and marked 77 as unsure with its reason. I read every one and entered my own label: I kept the AI label on 285, changed it on 19 (15 of those from `reaction` to `info`), and excluded 66, including the 16 the AI had already suggested excluding. Their note is `AI-assisted; human-reviewed`, with "kept AI label" or "changed from <label>".
- **Exclusions:** 74 of the 390 in total, so `labels.csv` had 316 rows for the original training run.
- **Stretch batches, added later and reviewed the same way:** 64 extra likely-`opinion` comments and 57 comments for the new `question` label (see [Stretch Features](#stretch-features)). I kept the AI label on all 121. I also re-labelled the six questions I had excluded under the old rules: five stay excluded and one (r275) became `opinion`. That brings `labels.csv` to 438 rows.
- **Known weakness:** after I built the file, Claude flagged about 24 of my labels (most of the cold rows and several early review rows) as possibly conflicting with my written rules, for example "idk why but this vlog made me tear up" labelled `info`, and plain gushing excluded although it is on none of my exclusion lists. I kept the labels as committed. This matters for criterion 5 and is a likely source of noise in the model.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
Current `labels.csv`, after the stretch features:

| Label | Count | Share |
|---|---|---|
| `info` | 73 | 16.7% |
| `opinion` | 122 | 27.9% |
| `reaction` | 192 | 43.8% |
| `question` | 51 | 11.6% |
| **Total** | 438 | 100% |

The largest label is 43.8%, well under the brief's 70% cap. Criterion 3 (largest at most 60%, smallest at least 15%) is **missed**, because `question` is 11.6%.

The original training run (`results.json`) used `labels.csv` as of commit 32a4243, before the stretch features:

| Label | Count | Share |
|---|---|---|
| `info` | 71 | 22.5% |
| `opinion` | 56 | 17.7% |
| `reaction` | 189 | 59.8% |
| **Total** | 316 | 100% |

On that file the largest label was 59.8% and the smallest 17.7%, so criterion 3 was met, narrowly.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

All eight hard cases I recorded, with my decisions, are in [labelling/hard_cases.md](labelling/hard_cases.md).

**1.**
> *The post:* "Bencoolen might be a better choice as the train station is closer to the National Musuem of Singapore, which already has announced themed light and sound installations" (r/bangtan comment [phmjlb7](https://www.reddit.com/r/bangtan/comments/1x9iv6m/_/phmjlb7/))
>
> *Could have been:* `info` (Rule 3: advice to readers with a checkable fact about the station) or `opinion` (Rule 2: a recommendation of X over Y)
>
> *I chose, because:* `opinion`, because it is an opinion about which place might be better. The facts are there to support choosing one station over another.

**2.**
> *The post:* "I'm so so excited I feel like throwing up guys, there's already thousands outside the stadium it seems, I will be arriving in a few hours. [...] Don't expect many videos because the internet connection at the concert will be terrible, so most will upload them later." (r/bangtan comment [pgotr45](https://www.reddit.com/r/bangtan/comments/1x5qn7y/_/pgotr45/))
>
> *Could have been:* `reaction` (almost all of it is the writer's excitement) or `info` (it ends with a heads-up to readers, which Rule 3 sends to `info`)
>
> *I chose, because:* `reaction`, because it is a reaction to how it feels to be outside the stadium. The heads-up is one line at the end of a post about the writer's own experience.

**3.**
> *The post:* "Jin - Crystal Snow Yoongi - Pied Piper Hobi - Jamais Vu Namjoon - One more night Jimin - Lights Taehyung - Epilogue Young Forever Jungkook - Dynamite" (r/bangtan comment [phglz9l](https://www.reddit.com/r/bangtan/comments/1x8xi2j/_/phglz9l/))
>
> *Could have been:* `opinion` (Rule 1(c): an unmarked comparison) or `reaction` (nearly identical lists in the same thread that say "for me" are `reaction`)
>
> *I chose, because:* `opinion`, because it is the writer's view of which song each member is, given with no "for me" to mark it as personal taste.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`, fine-tuned for 3-label classification with the notebook's `train_model`.

**Settings:** <!-- epochs, learning rate, batch size, seed -->
3 epochs, learning rate 2e-5, batch size 16, max length 128 tokens, seed 42 (the notebook defaults). Trained on 316 rows of `labels.csv` (commit 32a4243), with the three original labels.
- **Device:** `mps` (Apple Silicon GPU, Apple M2 Pro), torch 2.14.1, transformers 4.57.6. `results.json` records the device too. Another machine with the same data and seed can give slightly different numbers.
- **Run time:** about 15 seconds of training.
- **How it was run:** Claude Code ran the code cells of sections 1-5 in order, unchanged, as a script with this project's `.venv` Python from the repo folder (the `.venv` has no `ipykernel`, so it could not run as a notebook kernel). Sections 6 and 7 were not run.
- **Notebook outputs:** later, `ipykernel` was added to the `.venv` and `takemeter.ipynb` itself was run with that kernel, so sections 1-5 now show their outputs in the notebook. That run used the current `labels.csv` (438 rows, four labels), so its section 5 numbers (accuracy 0.500, macro F1 0.271) are the four-label run under [Stretch Features](#stretch-features) and match [experiments/results_4labels.json](experiments/results_4labels.json). Section 5 rewrote `results.json` and `test_split.csv`, and both were put back to the committed originals, which stay the record of this run. Sections 6 and 7 are next unit's and have no outputs.

**Anything I changed from the defaults, and why:** Nothing. Every setting is the default. A second run with one setting changed is documented under [Stretch Features](#stretch-features); it does not replace this run.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->
Stratified 70/15/15 split, seed 42: **train 220, validation 48, test 48.**

| Label | Train | Val | Test |
|---|---|---|---|
| `info` | 49 | 11 | 11 |
| `opinion` | 40 | 8 | 8 |
| `reaction` | 131 | 29 | 29 |

`opinion` has only 8 posts in the test split, right at the "about 8" line, so its per-label score can move a lot between seeds. `info` has 11.



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
- **The 20 cold rows** were not pre-labelled. I labelled those myself, without AI, before starting the review.
- **I read every pre-labelled row and gave it my own label** before it entered `labels.csv`: 285 kept, 19 changed, 66 excluded. The `note` column records which, row by row.
- **Claude Code also** wrote the labelling and build scripts and, after I built the file, flagged labels of mine that looked inconsistent with my rules. It did not change any label.
- **Stretch features:** Claude Code pre-screened the unused comments for likely `opinion` posts, wrote and ran the second training experiment, and proposed the fourth label. Details and status are under [Stretch Features](#stretch-features).

---

## Stretch Features

I set out to complete all three stretch features (stated here before starting). Status:

| Feature | Status |
|---|---|
| 1. 50 extra examples for the thinnest label (`opinion`) | **Done**: 64 added, `opinion` 56 → 122 |
| 2. Second training run with one hyperparameter changed | **Done** (results below) |
| 3. A fourth label | **Done**: `question` added to the taxonomy, label map and notebook; 51 rows; retrained with four labels |

### 1. 50 extra `opinion` examples

- **Why `opinion`:** it is the thinnest label in `labels.csv`, with 56 of 316 rows (17.7%).
- **Where they came from:** the same Arctic Shift download as the main set (r/bangtan, 13-20 Oct 2026). After the same filters, 989 comments had never been sampled. Claude Code keyword-matched 242 of them (for example "I think", "should", "better", "underrated", "because") and read all 242 against my rules. It proposed **64** as likely `opinion`, 21 of them marked unsure with a reason.
- **Unlike the main set, these were chosen because they looked like `opinion`.** That is the point of this feature, but it means they are not a random sample of the community.
- **Files:** [labelling/extra_opinion_review.csv](labelling/extra_opinion_review.csv) (text copied exactly as posted). Each row's comment ID and permalink are in [labelling/sources.csv](labelling/sources.csv), batch `stretch1_opinion_topup`. None duplicates or near-duplicates a row already in the dataset.
- **Review:** I labelled every row with `python labelling/label.py extra` and kept `opinion` on all 64. Their note reads `AI-assisted (opinion top-up); human-reviewed, kept AI label`.
- **Result:** `opinion` went from 56 to 122 rows (17.7% → 27.9%), and it is no longer the thinnest label (`question` is).

### 2. Second training run: 6 epochs instead of 3

- **What changed:** `EPOCHS` 3 → 6. Nothing else: same `labels.csv` (316 rows, commit 32a4243), same seed 42, same base model, learning rate 2e-5, batch size 16, max length 128, same device (`mps`, Apple M2 Pro).
- **Why epochs:** in the first run the validation macro F1 stayed at 0.251 for all three epochs, which is what predicting `reaction` for every post scores, while validation loss was still falling (0.925 → 0.883). That looked like a model that had not trained long enough to move off the majority label, so more passes over the same data was the single change to test.
- **How it was run:** [run_experiment.py](run_experiment.py) runs the notebook's own section 1-5 cells unchanged, with only the setting override and a different output filename, so `results.json` and `test_split.csv` were not touched. The test split was byte-identical to `test_split.csv` in every run.
- **Is the change bigger than run-to-run noise?** I first re-ran the default settings the same way ([experiments/results_rerun_default.json](experiments/results_rerun_default.json)). It reproduced `results.json` exactly (same predictions and scores), so on this machine the difference below comes from the setting, not from chance in the run.

| Measure (48 test posts) | Run 1: 3 epochs (`results.json`) | Run 2: 6 epochs ([experiments/results_exp2_epochs6.json](experiments/results_exp2_epochs6.json)) |
|---|---|---|
| Accuracy | 0.604 | 0.625 |
| Macro F1 | 0.251 | 0.310 |
| F1 `info` (n=11) | 0.000 | 0.167 |
| F1 `opinion` (n=8) | 0.000 | 0.000 |
| F1 `reaction` (n=29) | 0.753 | 0.763 |
| Most-confident third accuracy | 0.812 | 0.812 |
| Least-confident third accuracy | 0.312 | 0.375 |
| Final validation loss | 0.883 | 0.805 |
| Training time | about 14 s | about 26 s |

**What moved:** almost nothing. Run 1 predicted `reaction` for all 48 test posts. Run 2 got exactly one more post right: one `info` post is now predicted `info` instead of `reaction`, and every other prediction is the same. One post out of 48 on a single seed is not evidence that 6 epochs is better. What it does show is that doubling training time does not fix the problem: the model still never predicts `opinion`, so the cause is more likely the data (few `opinion` and `info` examples, and the labelling inconsistencies noted in The Dataset) than the number of epochs.

### 3. A fourth label: `question`

- **What I found:** one kind of comment my three labels had no place for: a fan asking other fans for something. The 2,000 comments downloaded include 44 question-only ones (after the usual thread and mod filters), for example "Where can I find the translations of the ments?". During review I also excluded several longer ones (such as r048, asking for Rio activity and food recommendations), because my v3 rules sent all question-only comments to the exclusion list. They are not `info` (they supply nothing checkable), not `opinion` (no side) and not really `reaction`, and the natural reply to them is an answer.
- **What I decided:** I approved `question` as the fourth label, with the definition, examples and Rule 4 under [Label Taxonomy](#question). Considered and rejected: a `joke` label, because jokes on r/bangtan are a tone, not a different main point; Rule 1 already sends a joking claim to `opinion` and a joking feeling to `reaction`.
- **What changed:** `question` is now in `LABELS` in [takemeter.ipynb](takemeter.ipynb) and [labelling/build_labels.py](labelling/build_labels.py), in [label_definitions.txt](label_definitions.txt) (so the baseline sees it), and in the rules in [taxonomy_stress_test.md](taxonomy_stress_test.md). The labelling tool takes `?` for `question`. No existing label was changed.
- **Data:** [labelling/question_review.csv](labelling/question_review.csv) holds 57 real comments: the 44 question-only comments minus one near-duplicate, plus 14 longer requests from the unused pool. Claude Code suggested `question` for 51 and another label for 6 (for example a rhetorical joke as `reaction`), and marked 19 as unsure. Provenance is in `labelling/sources.csv`, batch `stretch3_question`. I labelled all 57 and kept the AI label on every one: 51 `question`, 3 `reaction`, 2 `info`, 1 `opinion`. Their note reads `AI-assisted (question batch); human-reviewed, kept AI label`.
- **Rows already in the sheet that my old rule excluded:** r027, r043, r048, r137, r146 and r275 are questions I marked `EXCLUDE` under the v3 rules. I labelled them again under Rule 4 (`python labelling/label.py redo ...`): five I kept as `EXCLUDE`, and r275 became `opinion`. That is relabelling because the rule changed, not to move the counts.
- **Retrained with four labels:** default settings (3 epochs, lr 2e-5, batch 16, max length 128, seed 42, `mps`) on all 438 rows, run with `python run_experiment.py --out experiments/results_4labels.json`. The notebook's data check printed "Data looks fine." Split: train 306, validation 66, test 66; the test split has 11 `info`, 18 `opinion`, 29 `reaction` and **8 `question`**, right at the "about 8" line. Its test posts are in [experiments/results_4labels_test_split.csv](experiments/results_4labels_test_split.csv), and results in [experiments/results_4labels.json](experiments/results_4labels.json).

| Measure | Four labels, 438 rows (66 test posts) |
|---|---|
| Accuracy | 0.500 |
| Macro F1 | 0.271 |
| F1 `info` (n=11) | 0.000 |
| F1 `opinion` (n=18) | 0.452 |
| F1 `reaction` (n=29) | 0.634 |
| F1 `question` (n=8) | 0.000 |
| Most-confident third accuracy | 0.682 |
| Least-confident third accuracy | 0.227 |

| true \ predicted | `info` | `opinion` | `reaction` | `question` |
|---|---|---|---|---|
| **`info`** | 0 | 3 | 8 | 0 |
| **`opinion`** | 0 | 7 | 11 | 0 |
| **`reaction`** | 0 | 3 | 26 | 0 |
| **`question`** | 0 | 0 | 8 | 0 |

- **What moved:** this is a different dataset and a different test split from run 1, so the numbers are not a like-for-like comparison. The model now predicts `opinion` for 13 posts (7 correctly), where run 1 never predicted it. It still never predicts `info` or `question`, and sends all 8 `question` posts to `reaction`. Part of the `opinion` gain may come from how the top-up was chosen: those comments were picked partly by words like "I think" and "should", so they may be easier to spot than a random `opinion` comment, and 11 of the 18 `opinion` test posts came from that batch.
- **The stress test was not repeated for `question`.** The 16 synthetic posts in taxonomy_stress_test.md tested the three-label rules only.

### Limitations

- With four labels, criterion 3 (smallest label at least 15%) is missed: `question` is 11.6%. criteria.md was filed before training and stays as written.
- I kept the AI label on all 121 stretch rows, so those labels rest on my agreeing with every suggestion, including the 40 marked unsure.
- The four-label run is one seed with only 8 `question` posts in test, so its `question` score could move a lot on another seed.
- Feature 2 is one seed and one test split of 48 posts. A one-post difference could reverse on another seed.
- `label_definitions.txt` now has four definitions. The Unit 6 baseline in `baseline_results.json` was rerun with `--data test_split.csv`, so it is offered only the three labels those test posts were labelled with. Only the three matching definitions are used.
- `results.json` and `test_split.csv` (run 1) were trained and tested on `labels.csv` as of commit 32a4243 (316 rows, three labels) and are unchanged; they remain the record of the original run. Running the notebook now trains on the 438-row, four-label file and would overwrite them, so later runs should go through `run_experiment.py` or be committed under a new name.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Both models were scored on the same 48 posts in [test_split.csv](test_split.csv). These are the three-label held-out posts from run 1, compared against the three-label trained model in [results.json](results.json). The baseline is `facebook/bart-large-mnli` zero-shot, given only the definitions in [label_definitions.txt](label_definitions.txt). Command: `python baseline.py --data test_split.csv --trained results.json`. `--data test_split.csv` limits the candidate labels to the three these posts were labelled with, so the baseline is not offered `question`. Output: [baseline_results.json](baseline_results.json).

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.208 | 0.604 | +0.396 |
| Macro F1 | 0.205 | 0.251 | +0.046 |
| F1 — `info` | 0.303 | 0.000 | -0.303 |
| F1 — `opinion` | 0.312 | 0.000 | -0.312 |
| F1 — `reaction` | 0.000 | 0.753 | +0.753 |

**What I predicted before I looked:**
Run 1 predicted `reaction` for every test post, so I expected the trained model to beat the baseline only on `reaction` F1 and on overall accuracy, and to lose on `info` and `opinion`. *(Written after the baseline had already run, so this is not a blind prediction.)*

**What the gap actually means:**

The trained model wins on accuracy only because it predicts `reaction` for every post, and 29 of the 48 test posts are `reaction`. Macro F1 is almost the same (0.251 vs 0.205). The two models fail in opposite ways:
- **Trained model:** never predicts `info` or `opinion`.
- **Baseline with definitions:** almost never predicts `reaction`. All 29 real `reaction` posts went to `info` (14) or `opinion` (15), and it predicted `reaction` only twice in total.

So fine-tuning has not yet taught the model anything a general model can't do. What it learned is the majority label.

**Definitions vs. bare label names.** I ran the baseline a second time with no definitions file, so it saw only the words `info`, `opinion` and `reaction`. Output: [experiments/baseline_bare_names.json](experiments/baseline_bare_names.json).

| Measure | Baseline, definitions | Baseline, bare names | Trained |
|---|---|---|---|
| Overall accuracy | 0.208 | **0.667** | 0.604 |
| Macro F1 | 0.205 | **0.575** | 0.251 |
| F1 — `info` | 0.303 | 0.545 | 0.000 |
| F1 — `opinion` | 0.312 | 0.400 | 0.000 |
| F1 — `reaction` | 0.000 | 0.780 | 0.753 |

On this model, my definitions were worth **−0.458 accuracy**: they made the baseline much worse. With bare names, the baseline beats the trained model on every measure.

The likely reason is how the `reaction` definition is phrased. It is long and ends in two exclusions ("without supplying checkable information … or taking a side another fan could argue with"). Zero-shot NLI models are known to handle negation poorly. If that is what happened here, the model matched on "checkable information" and "taking a side" and read the hypothesis as being about exactly what it excludes. This is a guess I have not tested.

The definitions still work as written rules for a human labeller. But this result shows they are a weak prompt for an NLI model. I report the definitions run as my baseline because that is what this milestone asks for. The bare-names run is the stronger opponent, and it is the one my model has to beat.

**Four-label check (extra).** For the stretch model I also ran the baseline with all four definitions on that run's own 66 test posts. Command: `python baseline.py --held-out experiments/results_4labels_test_split.csv --trained experiments/results_4labels.json --out experiments/baseline_4labels.json`. Baseline: accuracy 0.288, macro F1 0.218. Trained: 0.500 and 0.271. The pattern is the same as above: the baseline scores 0.121 F1 on `reaction` and 0.000 on `question`.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

**Setup:**
- **Data:** the final four-label `labels.csv` (438 rows: `info`, `opinion`, `reaction`, `question`).
- **Settings:** the notebook's defaults: `distilbert-base-uncased`, 3 epochs, lr 2e-5, batch 16, max length 128.
- **Device:** Apple Silicon GPU (MPS), torch 2.14.1.
- **How it ran:** notebook sections 1–3, then 6 and 7. Section 4's single training run and section 5's write were skipped, so `results.json` and `test_split.csv` from run 1 are unchanged.
- **Output:** [results_three_seeds_before.json](results_three_seeds_before.json).
- **Test split:** 66 posts per seed (11 `info`, 18 `opinion`, 29 `reaction`, 8 `question`).
- **Reproducibility check:** seed 42 reproduced [experiments/results_4labels.json](experiments/results_4labels.json) exactly (accuracy 0.500, macro F1 0.271).

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.75 on every seed | 0.500 | 0.561 | 0.545 | **Missed** |
| 2. Every label's F1 | ≥ 0.55 on every seed | min 0.000 (`info`, `question`) | min 0.000 (`info`, `question`) | min 0.000 (`info`, `question`) | **Missed** |
| 3. Label balance in `labels.csv` | largest ≤ 60%, smallest ≥ 15% | `reaction` 43.8%, `question` 11.6% | same file | same file | **Missed** (`question` < 15%) |
| 4. Confidence gap (most-sure third − least-sure third) | ≥ 0.30 on every seed | 0.682 − 0.227 = **0.455** | 0.727 − 0.455 = **0.273** | 0.818 − 0.318 = **0.500** | **Missed** (seed 7) |
| 5. Self re-label agreement (30 rows, `random_state=5`) | ≥ 85% (26/30) | n/a | n/a | n/a | **Not tested** (not valid before 27 Oct) |

Criterion 3 is a property of the data file, so it is the same on every seed. Criterion 5 is my own blind re-label and doesn't depend on a seed.

Per-measure spread from section 6:

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.500 | 0.561 | 0.545 | 0.061 |
| Macro F1 | 0.271 | 0.323 | 0.298 | 0.051 |
| F1 — `info` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `opinion` | 0.452 | 0.625 | 0.519 | 0.173 |
| F1 — `reaction` | 0.634 | 0.667 | 0.674 | 0.040 |
| F1 — `question` | 0.000 | 0.000 | 0.000 | 0.000 |

**The spread:** accuracy moved 6.1 points across seeds, under the 10-point line, so the overall number is fairly stable. `opinion` F1 is the jumpy one, moving 17 points.

The stability is mostly not good news, though. The model never predicts `info` or `question` on any seed, so those two F1s are stuck at 0.000. That makes them perfectly stable and perfectly useless. Criterion 1 misses by 19 to 25 points on every seed, far outside the spread, so the miss is real and not an unlucky draw.

### Confusion matrix

Seed 42, the first seed in section 7:

| true \ predicted | info | opinion | reaction | question |
|---|---|---|---|---|
| **info** | 0 | 3 | 8 | 0 |
| **opinion** | 0 | 7 | 11 | 0 |
| **reaction** | 0 | 3 | 26 | 0 |
| **question** | 0 | 0 | 8 | 0 |

**My biggest off-diagonal number, and what it means:**

The model has not learned my hardest boundary, `opinion` vs `reaction`. 11 of the 18 real `opinion` posts were called `reaction`, and only 3 went the other way, so it defaults to `reaction` whenever a comment isn't clearly an opinion.

The same lean shows up on every seed: 8 and 11 `opinion` posts were sent to `reaction` on seeds 7 and 2024. All 8 `question` posts and 8 of 11 `info` posts also went to `reaction` on seed 42. `reaction` works as the catch-all for everything the model can't place.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy on the held-out split | ≥ 0.75 on seeds 42, 7 and 2024 | **MISSED** | 0.500, 0.561, 0.545. All three are below 0.75, and the best is 19 points short, far more than the 6-point spread between seeds. |
| 2 | Every label's F1 | ≥ 0.55 on every seed | **MISSED** | `info` and `question` are 0.000 on all three seeds. `opinion` reaches 0.55 only on seed 7 (0.452, 0.625, 0.519). Only `reaction` clears it everywhere (0.634, 0.667, 0.674). |
| 3 | Label balance in `labels.csv` | largest ≤ 60%, smallest ≥ 15% | **MISSED** | `value_counts(normalize=True)` on the 438-row file: `reaction` 43.8%, `opinion` 27.9%, `info` 16.7%, `question` 11.6%. The cap holds; the floor fails on `question`. |
| 4 | Confidence gap (most-sure third − least-sure third) | ≥ 0.30 on every seed | **MISSED** | 0.455, **0.273**, 0.500. Two of three seeds clear it and the average (0.409) does, but my criterion says every seed, and seed 7 is 0.027 short. |
| 5 | Self re-label agreement on 30 random rows | ≥ 85% (26/30) | **NOT TESTED** | My criterion requires waiting at least 7 days after finishing `labels.csv`. I finished it on 20 Oct 2026, so the earliest valid date is 27 Oct, two days after this unit's deadline. Running it sooner would break the rule I set, so I have no verdict. |

**Diagnoses**

The evidence I use below:
- **Training data:** the training split is identical on every seed, because the split is stratified: 134 `reaction`, 86 `opinion`, 51 `info`, 35 `question`.
- **The confusion matrices** in the run log above.
- **The baseline** (Baseline vs. Trained).
- **The agreement report:** 30/30 with staff, including 7 posts staff marked as borderline.
- **My labelling notes** in The Dataset.

**Criterion 1 (accuracy) is missed because the model mostly predicts `reaction`.**
- **What the model does:** across the three seeds it predicts `reaction` 53, 52 and 57 times out of 66, and never predicts `info` or `question`. Accuracy is close to the 44% you'd get by always guessing `reaction`, plus whatever `opinion` posts it catches.
- **Cause:** this is a task the model doesn't reach from this much data with these settings. Validation loss was still falling at epoch 3 on every seed (for example 1.227 → 1.171 → 1.146 on seed 42), and validation macro F1 ended between 0.27 and 0.34. So training stopped before it had learned anything beyond the majority label and the clearest `opinion` posts.
- **Why more epochs alone won't fix it:** the 6-epoch run in Stretch 2 moved one post out of 48. So it's not only training time.
- **What isn't the cause:** this miss isn't explained by my labelling being inconsistent. Criterion 2 below covers where labelling does play a part.

**Criterion 2 (every label's F1) is missed on three labels, for different reasons.**
- **`question` (F1 0.000, all 8 test posts called `reaction` on every seed): too few examples.**
  - It has only 35 training examples, the fewest of any label. All 57 `question` rows came from one late stretch batch where I kept every AI suggestion.
  - A few are wrapped in feeling: 4 of 51 contain words like "omg", "love" or 😭. One example is "Omg the girl with the dimple is sooo cutee!! 🥹✨ I'm curious where do they find these pictures of fans?", which reads like `reaction` until the question at the end. Most aren't, so the main cause here is still the low count.
  - The agreement check can't speak to this label, because the staff taxonomy has no question category.
- **`info` (F1 0.000, 8–9 of 11 test posts called `reaction` on every seed): too few examples, plus a boundary I applied inconsistently.**
  - It has only 51 training examples. Run 1 had 71 `info` rows and also never predicted it, so the count alone isn't the whole story.
  - My labelling log points at the `info`/`reaction` boundary. Of the 19 pre-labels I changed during review, 16 became `info`, and 15 of those went from `reaction` to `info`.
  - Claude also flagged rows like "idk why but this vlog made me tear up" as `info` that my own rules would call `reaction`.
  - So the AI pre-labeller and I disagreed most on this boundary, and some rows on the wrong side of my own rule are still in the training data.
- **`opinion` (0.452 / 0.625 / 0.519, mostly missed into `reaction`): a genuinely hard pair, not loose labelling.**
  - The matrix sends 11, 8 and 11 of the 18 real `opinion` posts to `reaction`, and only 0–3 go the other way.
  - Precision is decent (0.54, 0.71, 0.78) but recall is low (0.39, 0.56, 0.39). When the model does say `opinion` it is usually right. It just won't say it unless a post is clearly argumentative.
  - The agreement report is the evidence that this isn't my labelling. Staff Rule 2 (claim about the world vs. report of the writer) is the same cut as my `opinion`/`reaction` rule. I matched staff on both borderline posts that hinge on it (sp_019 `hot_take`, sp_029 `reaction`) and on every other post.
  - So when I apply that kind of rule myself, I apply it the way it's written.
  - What makes the pair hard is my own decision rule. It asks the reader to strip the feeling out before judging, and the model can't do that: most `opinion` posts in my data are wrapped in fan affection.
  - The baseline backs this up. Even zero-shot with bare names, `opinion` was its weakest label (F1 0.400).
  - **Caveat:** the agreement check tested me labelling 30 posts by myself. Most of my training rows are AI pre-labels I kept, so it can't rule out inconsistency in those.

**Criterion 3 (balance) is missed because `question` was added late with too few rows.**
- `question` is 51 of 438 rows (11.6%). It was a Stretch 3 addition: I collected 57 candidates aimed at that label and kept 51 after review.
- The criterion was written for three labels, and the three-label file from run 1 passed it: `reaction` 59.8%, `info` 22.5%, `opinion` 17.7%.
- Adding a fourth label without collecting at least 66 rows of it (15% of 438) is what broke the floor.
- I'm not revising this criterion. It was measurable and I missed it.

**Criterion 4 (confidence gap) is missed on one seed, by less than one post.**
- Each third is 22 posts, so seed 7's 0.273 vs. the 0.30 target is a difference of about 0.6 of a post. That is inside the noise I warned about when I set the target.
- The model's confidence is mostly a measure of how `reaction`-like a post looks. That is useful for flagging, because the least-confident third is where its wrong guesses on `opinion` and `info` collect.
- The cause of the miss is the same as criterion 1: the model can't tell four labels apart, so on some splits its confident `reaction` guesses include mislabelled `info` and `question` posts.
- **The case for MET:** two of three seeds and the average clear 0.30. But the target says every seed, and seed 7 doesn't, so I'm keeping the miss.

**Criterion 5 has no verdict because it hasn't been run.**
- It isn't a miss: the test isn't valid until 27 Oct.
- The closest evidence I have is the 30/30 staff agreement. That checks whether I can apply a written rule, not whether I'd re-label my own posts the same way a week later, so I'm not counting it as a substitute.
- If I run it on or after 27 Oct, I'll add the result here without changing the criterion.

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 30 / 30 = 100%

**How I labelled them:** I read [data/staff_taxonomy.md](data/staff_taxonomy.md) and labelled all 30 posts in [data/staff_posts.csv](data/staff_posts.csv) under its three definitions and four rules. I saved them to [my_staff_labels.csv](my_staff_labels.csv). The staff file ([data/staff_labels.csv](data/staff_labels.csv)) was already downloaded by the time I last saved mine, but I hadn't opened it. I only looked at it after `python agreement.py` had run. Output: [agreement_results.json](agreement_results.json).

**Disagreements**

None. `agreement.py` found 0 disagreements, so there is nothing to sort into piles (a), (b) or (c).

**The posts staff marked as borderline.** Staff flagged 7 of the 30 as deliberately hard. I matched all 7. In each case, the rule below is the one that settled it for me:

| Post | Label | The rule that decided it |
|---|---|---|
| sp_005, "Carbon plates aren't the whole story…" | `analysis` | Rule 1. The first clause sounds like a hot take, but the two 2% drops, with mileage as the only change, are the argument. |
| sp_010, "Three of us ran the same session…" | `analysis` | Rule 1. The sample is tiny and the conclusion is hedged, but the observation is checkable and the claim rests on it. |
| sp_014, "Times are down about 3%… so obviously…" | `hot_take` | Rule 1. "So obviously" draws the conclusion; the 3% is decoration. It is nearly the taxonomy's own example. |
| sp_019, "Nobody actually enjoys the long run…" | `hot_take` | Rule 2. It sounds reflective, but it is a general claim about everyone, not a report of the writer's own run. |
| sp_020, "Every injury thread on this forum…" | `hot_take` | Rule 1. It could be checked in principle, but no count is given, so nothing is shown. |
| sp_028, "Third DNF this year…" | `reaction` | Rule 3. "Third this year" is countable, but nothing is argued from it. It reports the writer's own state. |
| sp_029, "…the shoes I set every PB in… wrong size" | `reaction` | Rule 2. It could read as a wry take on shoe talk, but it reports the writer's own realisation. |

**What the pattern in my disagreements tells me:**

With no disagreements, there is no pattern to read. What the 100% does show is that the staff rules are tight: each boundary has one test that gives a yes or no answer. "Is the fact load-bearing?" and "Is it about the writer or about the world?" settled all 7 borderline posts without needing Rule 4, the tie-break.

That doesn't make this set easy. It means the written rule did its job. It also means this check found no sign that I apply a written rule loosely, at least when I label 30 posts carefully, by myself.

That matters for Milestone 4, because my own 438 labels don't look this clean. Claude flagged about 24 of them as possibly conflicting with my own rules (see [The Dataset](#the-dataset)). And most of my rows were AI pre-labelled, with my review keeping the AI label on 285 of 370 and on all 121 stretch rows. So the more likely source of my own inconsistency is how I labelled at volume (accepting pre-labels) and my own `reaction`/`opinion` rule (which needs a "strip the feeling" step first), rather than whether I can apply a rule at all.

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
