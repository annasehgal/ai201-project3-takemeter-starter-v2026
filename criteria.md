# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

<!-- Your criterion. It must name a number. -->

Overall accuracy on the held-out test split (the 15% the notebook holds out; `accuracy` in the results file) is **at least 0.75** on each of seeds 42, 7 and 2024.

**Why this target:**

In my Milestone 1 reading, `reaction` was over half of all comments, so a model that always guesses `reaction` would score about 0.50. 0.75 means getting roughly 23 of about 30 test posts right on every seed, which halves that guess's error rate. That's the point where I'd trust TakeMeter to sort a thread for me.

---

## 2.

<!-- Your criterion. -->

Every label (`info`, `opinion` and `reaction`) has an F1 of **at least 0.55** on the held-out test split (`per_label.<label>.f1`), on each of seeds 42, 7 and 2024.

**Why this target:**

TakeMeter is only useful if it pulls `info` and `opinion` out of the flood of `reaction`, so I hold every label to the same bar instead of letting the big one carry the average. I set it at 0.55 rather than higher because `info` may have only about 6 test posts. `opinion` also sits on my hardest boundary (`reaction` vs `opinion`).

---

## 3.

<!-- Your criterion. -->

In the final `labels.csv` (at least 200 rows), **no label is more than 60%** of the rows and **no label is less than 15%**, checked before training with `df["label"].value_counts(normalize=True)` on the file the notebook loads in section 2.

**Why this target:**

The brief's 70% cap would be easy to meet, so I set mine tighter. `reaction` was over half of what I read in photo-dump threads, which means staying under 60% will take deliberate collection from discussion, help and recommendation threads. The 15% floor guarantees at least 30 examples of each label, so even `info`, my likely smallest, gets about 4 or 5 posts in the test split.

---

## 4.

<!-- Your criterion. -->

On the held-out test split, accuracy on the model's most-confident third of predictions is **at least 0.30 higher** than accuracy on its least-confident third (`accuracy_most_confident_third` minus `accuracy_least_confident_third` in the results file), on each of seeds 42, 7 and 2024.

**Why this target:**

I want the confidence score to be usable for flagging unsure comments (most likely the `reaction`/`opinion` borderline ones) for a human to check. Each third is only about 10 posts, so a gap of 0.30 means about 3 more correct out of 10. Anything smaller could come from one or two lucky posts.

---

## 5.

<!-- Your criterion. -->

At least 7 days after finishing `labels.csv`, I re-label 30 rows drawn at random (`df.sample(30, random_state=5)`) using only the definitions and rules in my README, without looking at the original labels. I compare them by matching the `text` column. My new labels must match the originals on **at least 85%** (26 of 30). This measures my own consistency, not agreement between two annotators, because no second person labels my posts.

**Why this target:**

I have three labels and a written rule for every boundary, so a careful annotator should rarely change their mind. The 16/16 blind check in my stress test was an AI labelling synthetic posts, though, not me labelling real ones. 85% allows 4 changes out of 30, which is about what I expect at the `reaction`/`opinion` boundary.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
