# Milestone 1 — Community and reading notes

## The community: r/bangtan (the BTS subreddit)

**Where:** [r/bangtan](https://www.reddit.com/r/bangtan/), the main
English-language subreddit for BTS. It's public, and reading needs no account or
invite.

**Why this one:**

- **It has a lot of text.** In one day (2026-10-20) it had 100+ comments across
  photo-dump threads, a "resources for new ARMY" thread, a nostalgia thread, a
  census thread and a ticketing megathread.
- **Quality really does vary.** The same thread has a careful, sourced answer
  next to "Oh YASSS!". That spread is what a classifier can learn.
- **It isn't built around one show or one release.** BTS have thirteen years of
  music, tours, documentaries and solo work. Comments mention the current
  *Arirang* tour, but nothing in them is a plot spoiler a reader would need to
  be caught up on.

**How I read it (and a limitation):** this environment can't reach
reddit.com directly. Every request (`www.reddit.com`, `old.reddit.com`,
`api.reddit.com`) came back 403 or redirected to a login page. I read the
comments through **[Arctic Shift](https://arctic-shift.photon-reddit.com)**, a
public research archive of Reddit:

```
https://arctic-shift.photon-reddit.com/api/comments/search?subreddit=bangtan&limit=100
```

These are the real public comments, word for word. Each one has a permanent
link at `https://www.reddit.com/r/bangtan/comments/<post id>/_/<comment id>/`.
The IDs quoted below are the comment IDs. I also tried Mastodon's #bts and
#bangtan tags and Lemmy's c/bts. Mastodon was mostly bot-posted video links and
spam, and Lemmy had almost no posts, so neither would give 200 real posts.

## What I read

The 100 most recent r/bangtan comments, all dated 2026-10-20. About 25 were only
an image link, a GIF, a bare URL or mod boilerplate, and I skipped those.
**That left 65 that I actually read.** They came from about 10 threads: a Yoongi
Instagram photo dump, Jungkook's story about *Cyberpunk: Edgerunners* season 2,
"what should baby ARMY watch", old-fandom nostalgia, the 2026 ARMY census,
J-Hope wine tasting, and the ticketing help megathread. Quotes below are
verbatim except that curly apostrophes are straightened, and cut where marked `…`.

## Candidate distinctions I saw in the text

### 1. Some comments give the reader information they can use. Most don't.

A named resource, a list, a quote from a source, a product, or context that
explains what's going on. You could check it, and someone else could act on it.

- phuw1r1: *"1. The Rise of Bangtan (2015) - 21 episodes (made by fans) …
  2. Burn the Stage (2018) - 8 episodes and movie, Wings tour 3. Bring the Soul
  (2019) - 6 episodes and movie, Love Yourself tour …"*
- phxpxpc: *"Hybe Boy on YouTube has excellent English-language translations of
  Lives, interviews, and other stuff going back several years. … He explains
  inside jokes or references that would only be known by older army."*
- phtsxvh: *"It looks like this one: [Yamaha Silent Guitar](…) Pretty cool that
  it's super quiet and breaks down for travel!"*
- phtu6mr: *"the screenshots are from netflix, showing that season 2 of
  cyberpunk: edgerunners (the animated series jk reaaaally likes) will premiere
  later today"*
- phveobm quotes the mods' census post: *"… we only receive 650 responses
  (2025 ARMY Time Census)."*

### 2. Some comments are pure feeling about a member or a post, with no content past the emotion.

This is the largest group by far.

- phu1xse: *"So much beauty it's overwhelming"*
- phu1mah: *"Every pic is attack after attack."*
- phv3luq: *"my precious hobii, seeing him smile makes me so happyy"*
- phuyndv: *"I loooove when yoongi plays the guitar 🥹🥹"*
- phtzuo5: *"Oh YASSS!"*

**Watch out:** phtsofe (*"Awesome shots as usual! He's so freaking handsome and
I love that his hair is only getting longer"*) is longer but still only feeling.
Length isn't the distinction.

### 3. Some comments read something into what the members did: an interpretation you could disagree with.

Not just "I love this". It's a claim about *why* or *what it means*, based on
something visible in the post.

- phv7dt2: *"I really adore that he chose a photo of him and Jungkook where
  Jungkook is being silly and doing Yoongi's signature dance move. Even when
  he's 60, Jungkook will be annoying and Yoongi will be so happy about it"*
- phunz4m: *"So I think that's now two guitarists, one bass player, one
  drummer, two keyboards. I guess that leaves Jimin on main vocal until Yoongi
  talks him into something 😇"*
- phtsc6k: *"I want to know if this was JK or a staff photo (since it was taken
  while he was playing with JK's guitar so presumably hanging out in JK's
  suite)."*
- phtsy91: *"Looks like Bandtan isn't so far off from becoming a reality soon"*

**Watch out:** phv7dt2 opens with "I really adore", which is distinction 2, and
then makes an interpretation. **The boundary between 2 and 3 looks like the
hardest one.** Milestone 2 needs a rule, probably "if it points at a specific
detail and draws a conclusion from it, it's 3, however gushy the wrapping".

### 4. Some comments tell the writer's own fan story.

When they found BTS, what the fandom used to be like, what they did. The
support is "this happened to me".

- phvyfyl: *"When they announced the world tour and album for Arirang. I legit
  thought they ended when they enlisted and solo performances were it from then
  on."*
- phtrvub: *"I've been around since at least Covid and I'm still learning new
  old things all the time. They're such different people to me pre-COVID
  because I didn't know them then."*
- phucy11: *"yesss the twitter layouts honestly had me stressed, i wanted mine
  to be so cute hahaha. Some people were so artistic and creative with them …"*

### Also seen: questions and help requests

Examples are phu3yey's long ticketing question (*"Do I need an ARMY membership?
… How does VIP/floor ticket purchases work?"*), phtyoxf (*"Where can I see those
videos?"*) and phttfqu (*"Can someone share the context … I didn't get it"*).
There are a lot of these. They might be their own label, or they might fold
into an exclusion rule.

## Leaning, before Milestone 2

- **1 (information), 2 (pure feeling) and 3 (interpretation)** are the
  strongest candidates. Each comes up often, and each can be pointed at in the
  text.
- **Class imbalance is a real risk.** Distinction 2 covers more than half of
  what I read, mostly because photo-dump threads dominate. To keep every label
  under 70% I'll need to collect from discussion, help and nostalgia threads,
  not only photo dumps.
- **Exclude at collection:** image-only, GIF-only and link-only comments, plus
  AutoModerator and mod boilerplate. There's no text to label.
