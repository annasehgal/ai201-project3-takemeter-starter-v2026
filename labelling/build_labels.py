#!/usr/bin/env python3
"""
Build labels.csv from the two labelling sheets, then validate it.

    python labelling/build_labels.py            # check only, writes nothing
    python labelling/build_labels.py --write    # write labels.csv

Inputs (all in labelling/):
    cold_20.csv                 your 20 cold labels (your_label column)
    review_ai_suggestions.csv   AI suggestions; your_label is YOUR reviewed label
    extra_opinion_review.csv    stretch feature 1: extra likely-`opinion` comments
    question_review.csv         stretch feature 3: comments for the fourth label
    sources.csv                 Reddit comment ID and permalink for every row

Rules:
    - A row goes into labels.csv only if YOU filled in your_label.
      Blank your_label means "not reviewed yet", and the row is left out.
    - your_label = EXCLUDE drops the row (e.g. question-only, mod message).
    - Notes record exactly what happened to each row, plus its Reddit ID:
        cold; reddit:<id>
        AI-assisted; human-reviewed, kept AI label; reddit:<id>
        AI-assisted; human-reviewed, changed from <ai_label>; reddit:<id>
"""
import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
LABELS = ["info", "opinion", "reaction", "question"]   # must match LABELS in takemeter.ipynb
MAX_SHARE, MIN_SHARE = 0.60, 0.15          # criteria.md, criterion 3
BRIEF_CAP = 0.70


def read(name):
    with open(HERE / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write labels.csv")
    args = parser.parse_args()

    sources = {r["row_id"]: r for r in read("sources.csv")}
    out, problems = [], []
    unreviewed, excluded = [], []
    cold_kept = changed = kept = 0

    for r in read("cold_20.csv"):
        label = r["your_label"].strip().lower()
        if not label:
            unreviewed.append(r["row_id"])
            continue
        if label == "exclude":
            excluded.append(r["row_id"])
            continue
        out.append((r["text"], label, f"cold; reddit:{sources[r['row_id']]['reddit_comment_id']}"))
        cold_kept += 1

    for r in read("review_ai_suggestions.csv"):
        label = r["your_label"].strip().lower()
        if not label:
            unreviewed.append(r["row_id"])
            continue
        if label == "exclude":
            excluded.append(r["row_id"])
            continue
        rid = sources[r["row_id"]]["reddit_comment_id"]
        if label == r["ai_label"].strip().lower():
            note = f"AI-assisted; human-reviewed, kept AI label; reddit:{rid}"
            kept += 1
        else:
            note = f"AI-assisted; human-reviewed, changed from {r['ai_label']}; reddit:{rid}"
            changed += 1
        out.append((r["text"], label, note))

    # Stretch features: extra batches, each reviewed the same way as the main sheet.
    #   1: comments pre-screened as likely `opinion`
    #   3: comments for the fourth label, `question`
    extra_kept = 0
    for sheet, tag in (("extra_opinion_review.csv", "opinion top-up"),
                       ("question_review.csv", "question batch")):
        if not (HERE / sheet).exists():
            continue
        for r in read(sheet):
            label = r["your_label"].strip().lower()
            if not label:
                unreviewed.append(r["row_id"])
                continue
            if label == "exclude":
                excluded.append(r["row_id"])
                continue
            rid = sources[r["row_id"]]["reddit_comment_id"]
            how = ("kept AI label" if label == r["ai_label"].strip().lower()
                   else f"changed from {r['ai_label']}")
            out.append((r["text"], label, f"AI-assisted ({tag}); human-reviewed, {how}; reddit:{rid}"))
            extra_kept += sheet.startswith("extra") and label == "opinion"

    bad = sorted({lab for _, lab, _ in out if lab not in LABELS})
    if bad:
        problems.append(f"labels not in {LABELS}: {bad} (use EXCLUDE to drop a row)")
    dupes = [t for t, n in Counter(" ".join(t.split()) for t, _, _ in out).items() if n > 1]
    if dupes:
        problems.append(f"{len(dupes)} duplicate texts")
    if any(not t.strip() for t, _, _ in out):
        problems.append("empty text in at least one row")

    total = len(out)
    counts = Counter(lab for _, lab, _ in out)
    print(f"rows in labels.csv: {total}")
    print(f"  cold: {cold_kept}   AI-assisted kept: {kept}   AI-assisted changed: {changed}")
    print(f"  excluded by you: {len(excluded)}   not reviewed yet (left out): {len(unreviewed)}")
    if (HERE / "extra_opinion_review.csv").exists():
        print(f"  opinion top-up rows you kept as opinion: {extra_kept}")
    print()
    for lab in LABELS:
        share = counts[lab] / total if total else 0
        print(f"  {lab:<9} {counts[lab]:>4}  {share:6.1%}")
    print()

    if total < 200:
        print(f"[look at] {total} rows, under the 200 the brief asks for")
    if cold_kept != 20:
        print(f"[look at] {cold_kept} cold rows kept, not 20")
    if total:
        top = max(counts.values()) / total
        low = min(counts[lab] for lab in LABELS) / total
        print(f"[brief]       largest label {top:.1%} (cap {BRIEF_CAP:.0%}): "
              f"{'OK' if top <= BRIEF_CAP else 'OVER THE CAP'}")
        print(f"[criterion 3] largest {top:.1%} <= {MAX_SHARE:.0%} and smallest {low:.1%} >= "
              f"{MIN_SHARE:.0%}: {'MET' if top <= MAX_SHARE and low >= MIN_SHARE else 'MISSED'}")
    for p in problems:
        print(f"[FIX ME] {p}")

    if args.write:
        if problems:
            sys.exit("Not writing labels.csv until the [FIX ME] lines are fixed.")
        with open(REPO / "labels.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["text", "label", "note"])
            w.writerows(out)
        print(f"\nWrote {REPO / 'labels.csv'}")


if __name__ == "__main__":
    main()
