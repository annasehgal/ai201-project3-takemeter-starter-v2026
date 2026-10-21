# Taxonomy stress test (Milestone 2)

> **Every post on this page is SYNTHETIC.** An AI wrote them to sit on my
> label boundaries. They are **not** r/bangtan comments. They are **not** in
> `labels.csv` and don't count toward the 200 real examples. Emoji have been
> removed from them; otherwise they are as generated.

The label definitions and the rule for the hardest boundary (`reaction` vs
`opinion`, Rule 1 below) are in [README.md, Label Taxonomy](README.md#label-taxonomy).
This page holds the complete final rules, how they were tested, and what changed.

## Final rules (v3)

**Not labelled at all:** comments that are only an image, GIF or link, only a
question or request with no claim or information in it, mod or AutoModerator
messages, not in English, or not about BTS or the fandom at all (for
example, comments in the sub's off-topic book club). If a question *also* contains a claim or a fact,
it's labelled by that content.

Apply the rules in order. Use the tie-breaker only if the rules don't decide.

**Rule 1 (`reaction` vs `opinion`, the hardest boundary).** First strip emotion
words (love, adore, crying), bare praise and superlatives (so pretty, unreal,
perfect), feeling idioms ("hits different", "sent me"), emojis, and fandom set
phrases ("boyfriend-coded", "the most Yoongi thing ever"). Then:
- **(a)** If what's left is about the writer ("my favorite", "for me", "I've
  never heard", "I was there"), it's `reaction`.
- **(b)** If what's left only restates what's plainly in the post ("he's
  smiling", "he's holding a guitar"), it's `reaction`.
- **(c)** If what's left adds something about BTS, their work or the fandom
  that the post doesn't show, it's `opinion`, even if joking or exaggerated.
  That covers:
  - why something happened, or what it means
  - what it says about who they are
  - a generalization ("he always...")
  - a specific, nameable quality (dated, overproduced, off-key)
  - a comparison or ranking not marked as personal
  - a prediction

**Rule 2 (`info` vs `opinion`).** Label by the main point.
- Facts used as ammunition for a side ("for everyone saying X: <fact>") make it
  `opinion`.
- Incidental praise of a shared resource ("excellent translations") doesn't.
- A recommendation is `info` when it mainly says what exists and where to find
  it, and `opinion` when its point is that X is better than Y ("start with A,
  not B").
- A short tag at the end ("which explains a lot") doesn't flip a factual
  comment.
- Truth isn't required: a checkable factual claim, even a rumor, is `info`.

**Rule 3 (`info` vs `reaction`).** Explicit advice or a warning to readers that
contains a checkable fact ("PSA", "heads up", "go early") is `info`, even inside
a personal story. Otherwise, if the facts are there to tell the writer's own
story or feeling, it's `reaction`.

**Tie-breaker.** Imagine the natural reply:
- "Thanks, didn't know that" means `info`.
- "Agree / hard disagree" means `opinion`.
- "Same / so jealous" means `reaction`.

## Method

1. **Round 1.** One AI agent was given *only the three definitions* (no
   decision rules) and asked for 8 comments on the boundaries, at least two
   per boundary, without saying which label was right. I then classified them
   under my draft rules.
2. **Revise.** Wherever I couldn't classify a post cleanly, I changed the
   definitions or rules.
3. **Round 2.** A fresh agent got the revised definitions *and* rules and was
   asked for 8 comments designed to **break** them. I classified these and
   revised again.
4. **Blind check.** A third, independent agent labelled all 16 synthetic
   comments using only the final rules. I wrote my own labels down *before*
   seeing its answers and then compared.

## Round 1: definitions only (v1)

v1 definitions differed from the final ones in two ways:
- `info` said only that the checkable content had to be "the point".
- There was no rule for the `info`/`reaction` boundary.

| # | Synthetic comment | Intended boundary | Clean under v1? | Final label |
|---|---|---|---|---|
| 1 | "reminder that joon has writing credits on basically every title track since debut, so the 'company writes all their songs' crowd can stop now lol" | info / opinion | **No.** Is the fact the point, or the rebuttal? | opinion |
| 2 | "tbh the lives are shorter lately because of the new contract terms, they're capped now. someone posted the clause on twitter a while back" | info / opinion | Yes | info |
| 3 | "chart data tho: it debuted lower than butter but stayed on the hot 100 way longer, so calling it a flop is kinda wild" | info / opinion | **No.** Same problem as #1 | opinion |
| 4 | "jimin's vocals in the bridge are just unreal, I've never heard him sound like that" | opinion / reaction | Mostly. Is "unreal" a merit judgment? | reaction |
| 5 | "ngl jin's solo stuff just isn't for me, the production feels kind of dated?? love him tho" | opinion / reaction | Yes | opinion |
| 6 | "this is the most yoongi thing he has ever said and I'm crying" | opinion / reaction | **No.** Is "most yoongi thing" a claim about his character? | reaction |
| 7 | "ok I was AT the busan show and they did the full spring day outro with the whole crowd singing. still not over it" | info / reaction | No rule existed yet | reaction |
| 8 | "just checked and the merch restock sold out in like 4 minutes AGAIN I give up" | info / reaction | **No.** No rule existed yet | reaction |

**What changed after round 1:**

- **`info` was redefined.** It now means supplying something checkable *without
  taking a side*, and **facts used as ammunition for a side make a comment
  `opinion`** (#1, #3). "That content is the point" couldn't decide these,
  because a rebuttal's fact *is* its point.
- **Rule 1 strips more than emotion words.** Bare praise and superlatives
  ("unreal") and fandom set phrases ("the most Yoongi thing ever") now count as
  feeling words (#4, #6). Without this, almost every gushing comment could be
  read as a merit judgment.
- **Rule 3 was added** for `info` vs `reaction` (#7, #8).
- **The "natural reply" tie-breaker was added.**

## Round 2: trying to break the v2 rules

| # | Synthetic comment | Boundary / exploit | Clean under v2? | Final label |
|---|---|---|---|---|
| 9 | "the way Namjoon always looks at whoever's talking instead of the camera... that's just who he is fr" | reaction / opinion. Restating the post, or reading his character? | **No** | opinion |
| 10 | "Spring Day hits different in winter, I don't make the rules" | reaction / opinion. Taste in a joking universal voice | **No** | reaction |
| 11 | "never understood the Butter hype tbh but I've also never been a summer song person so maybe that's on me" | reaction / opinion. Implied judgment, framed around the writer | Yes (1a) | reaction |
| 12 | "for everyone saying the album was rushed: Yoongi said on the Weverse live they'd been working on some of these tracks for 18 months" | info / opinion. A sourced fact used as a rebuttal | Yes (Rule 2) | opinion |
| 13 | "if you're new, start with the HYYH era, not Dynamite. The trilogy is where all the lore is and a lot of later MVs reference it" | info / opinion. A recommendation framed as X over Y | Yes (Rule 2) | opinion |
| 14 | "heard from a Korean fan cafe that the comeback got pushed so HYBE could lock in bigger stadiums, which honestly explains a lot" | info / opinion. A rumor with a "why" tag | **No** | info |
| 15 | "I was at Busan night 2 and the merch line was capped by like 2pm, I almost cried in the queue lmao. Seoul people go EARLY" | info / reaction. A personal story ending in a tip | **No** | info |
| 16 | "PSA from someone who learned the hard way Weverse Shop cancelled my lightstick order bc they don't ship that item to Brazil. I was devastated for a week" | info / reaction. A PSA wrapped in grief | **No** | info |

**What changed after round 2 (the final v3 rules):**

- **Rule 1(c):** a generalization beyond the post ("he *always*…") counts as
  adding something, so it's `opinion` (#9). Feeling idioms ("hits different",
  "sent me") are stripped (#10).
- **Rule 1(c):** a quality claim has to be a *specific, nameable* quality
  (dated, overproduced, off-key), or a comparison or ranking not marked as
  personal (#5, #10).
- **Rule 2:** a short evaluative tag at the end ("which explains a lot") doesn't
  turn a factual comment into opinion (#14).
- **Rule 3:** explicit advice or a warning to readers ("PSA", "heads up", "go
  early") makes it `info`, even inside a personal story (#15, #16).
- **Tie-breaker:** apply the rules in order. The tie-breaker is used only when
  they don't decide. #12's natural reply might be "thanks", but Rule 2 decides
  it first.

## Blind check under the final rules

| | Result |
|---|---|
| Agreement between me and the independent annotator | **16 / 16** |
| Posts the annotator said it had to guess | **#8** (a checkable sell-out fact with frustration attached and no advice) |
| Posts it flagged as weaker edge cases | **#2** (a "why" claim that Rule 2's "a rumor is still info" decides) |

**How far to trust this:** the blind annotator was another instance of the same
AI model, reading rules I wrote, so 16/16 overstates how well *people* will
agree. It shows the rules decide every case they were revised for. It doesn't
show they're unambiguous to a human. **The breakout check (asking classmates to
label the borderline post cold) is still to do.**

**Known weak spot to watch while labelling:** comments like #8, where a news-like
fact ("sold out", "tickets drop at 8pm KST") comes with only a feeling attached.
My current call is `reaction` when there's no advice to readers. If several real
ones come up during Milestone 4, I'll record them as hard cases in the README.

## The borderline real post: two-sided case

I gave the definitions and the real borderline comment (phv7dt2, quoted in the
README) to a separate agent with the brief's prompt: *"Make the strongest case
for each of the two labels. Don't tell me which one is right and don't rewrite
my definitions."*

- **Its case for `opinion`:** "Even when he's 60, Jungkook will be annoying and
  Yoongi will be so happy about it" is a prediction and a reading of the
  members' relationship. It claims the dynamic is lasting and that Yoongi is
  truly happy about it, not just putting up with it. A fan could dispute that
  without denying the writer's feelings. "He chose" also reads intent into
  Yoongi's choice.
- **Its case for `reaction`:** it opens with "I really adore", a direct
  statement of feeling. The middle just describes the photo, and the "when
  he's 60" line is affectionate exaggeration, not a forecast anyone would argue
  with. Replying "actually people change by 60" would miss the point.

Both cases were strong, which is why the boundary needs the written rule in the
README. Under Rule 1 it's **`opinion`**. Strip "I really adore" and what's left
makes a claim about the members' lasting relationship that isn't in the photo.
Exaggeration doesn't cancel a claim.
