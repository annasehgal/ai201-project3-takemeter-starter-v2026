#!/usr/bin/env python3
"""
Label the sheets from the terminal, one row at a time. Progress is saved after
every row, so you can quit (q) and come back later; it resumes where you left off.

    python labelling/label.py status    # how far along you are
    python labelling/label.py cold      # step 1: the 20 cold rows, text only
    python labelling/label.py review    # step 2: the 370 AI-suggested rows
    python labelling/label.py hard      # step 3: your decisions on the hard cases
    python labelling/label.py extra     # stretch 1: the extra likely-opinion comments
    python labelling/label.py questions # stretch 3: comments for the fourth label
    python labelling/label.py redo r014 r065   # clear those rows and label them again

Keys (type the letter, then Enter):
    i = info    o = opinion    r = reaction    ? = question    x = EXCLUDE
    b = back one row    q = save and quit
    In review only: Enter on its own = keep the AI label shown.

This only records what you type. It never fills a label in for you.
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEYS = {"i": "info", "o": "opinion", "r": "reaction", "?": "question", "x": "EXCLUDE"}
KEYS.update({v.lower(): v for v in list(KEYS.values())})   # full names work too
RULES = ("Rule 1: strip feelings; about the writer or restating the post = reaction, "
         "adds a claim = opinion.\nRule 2: facts used as ammunition = opinion.  "
         "Rule 3: advice/PSA with a checkable fact = info.\n"
         "Rule 4: main point is asking fans for an answer they could give = question; "
         "rhetorical questions go through Rule 1.")


def load(name):
    with open(HERE / name, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def save(name, fields, rows):
    tmp = HERE / (name + ".tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    tmp.replace(HERE / name)


def done(rows):
    return sum(1 for r in rows if r["your_label"].strip())


def ask(prompt, allow_enter=False):
    while True:
        try:
            k = input(prompt).strip().lower()
        except EOFError:
            return "q"
        if k in KEYS or k in ("b", "q") or (allow_enter and k == ""):
            return k
        print("  use i / o / r / ? / x, b (back), q (quit)" + (", or Enter to keep" if allow_enter else ""))


def run(name, show_ai):
    fields, rows = load(name)
    todo = [n for n, r in enumerate(rows) if not r["your_label"].strip()]
    if not todo:
        print(f"All {len(rows)} rows in {name} are labelled. Edit the CSV directly to change one.")
        return
    pos = 0
    while 0 <= pos < len(todo):
        r = rows[todo[pos]]
        print("\n" + "=" * 78)
        print(f"{r['row_id']}   ({done(rows)} of {len(rows)} labelled)")
        if show_ai:
            print(f"thread: {r['thread_title']}")
        print("-" * 78)
        print(r["text"])
        print("-" * 78)
        if show_ai:
            flag = "   [AI was UNSURE]" if r["ai_unsure"].strip() else ""
            print(f"AI suggests: {r['ai_label']}{flag}")
            if r["ai_note"].strip():
                print(f"AI note: {r['ai_note']}")
        k = ask("label [i/o/r/?/x" + (", Enter=keep" if show_ai else "") + ", b, q]: ", allow_enter=show_ai)
        if k == "q":
            break
        if k == "b":
            pos = max(0, pos - 1)
            rows[todo[pos]]["your_label"] = ""
            save(name, fields, rows)
            continue
        r["your_label"] = r["ai_label"] if k == "" else KEYS[k]
        save(name, fields, rows)
        pos += 1
    print(f"\nSaved. {done(rows)} of {len(rows)} labelled in {name}.")


def hard():
    md = (HERE / "hard_cases.md").read_text(encoding="utf-8")
    fields, rows = load("review_ai_suggestions.csv")
    by_id = {r["row_id"]: r for r in rows}
    parts = re.split(r"(?m)^(?=## \d+\. )", md)
    filled = 0
    for n, part in enumerate(parts):
        m = re.match(r"## \d+\. (r\d+)", part)
        if not m:
            continue
        rid = m.group(1)
        if not re.search(r"(?m)^- \*\*My final label:\*\* *$", part):
            filled += 1
            continue
        print("\n" + "=" * 78)
        print(part.split("- **My final label:**")[0].strip())
        print("=" * 78)
        k = ask("your final label [i/o/r/?/x, Enter=skip this case, q]: ", allow_enter=True)
        if k == "q":
            break
        if k in ("", "b"):
            continue
        why = input("why, using your written rules (one or two sentences): ").strip()
        label = KEYS[k]
        part = re.sub(r"(?m)^- \*\*My final label:\*\* *$", f"- **My final label:** `{label}`", part)
        part = re.sub(r"(?m)^- \*\*Why, using my written rules:\*\* *$",
                      lambda _: f"- **Why, using my written rules:** {why}", part)
        parts[n] = part
        (HERE / "hard_cases.md").write_text("".join(parts), encoding="utf-8")
        if rid in by_id:
            by_id[rid]["your_label"] = label
            save("review_ai_suggestions.csv", fields, rows)
        filled += 1
    print(f"\n{filled} hard cases have your decision (the README needs at least 3).")


def status():
    _, cold = load("cold_20.csv")
    _, rev = load("review_ai_suggestions.csv")
    md = (HERE / "hard_cases.md").read_text(encoding="utf-8")
    total = len(re.findall(r"(?m)^- \*\*My final label:\*\*", md))
    blank = len(re.findall(r"(?m)^- \*\*My final label:\*\* *$", md))
    print(f"cold:   {done(cold)} / {len(cold)}")
    print(f"review: {done(rev)} / {len(rev)}")
    print(f"hard:   {total - blank} / {total} decided (need 3)")
    if (HERE / "extra_opinion_review.csv").exists():
        _, ex = load("extra_opinion_review.csv")
        print(f"extra:  {done(ex)} / {len(ex)}")
    if (HERE / "question_review.csv").exists():
        _, qs = load("question_review.csv")
        print(f"question: {done(qs)} / {len(qs)}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    print(RULES)
    if cmd == "cold":
        run("cold_20.csv", show_ai=False)
    elif cmd == "review":
        _, cold = load("cold_20.csv")
        if done(cold) < len(cold):
            sys.exit("Do the cold rows first (python labelling/label.py cold), so your "
                     "cold labels aren't influenced by the AI suggestions.")
        run("review_ai_suggestions.csv", show_ai=True)
    elif cmd == "hard":
        hard()
    elif cmd == "extra":
        run("extra_opinion_review.csv", show_ai=True)
    elif cmd == "questions":
        run("question_review.csv", show_ai=True)
    elif cmd == "redo":
        ids = set(sys.argv[2:])
        for name, show_ai in (("cold_20.csv", False), ("review_ai_suggestions.csv", True),
                              ("extra_opinion_review.csv", True), ("question_review.csv", True)):
            fields, rows = load(name)
            hit = [r for r in rows if r["row_id"] in ids]
            if not hit:
                continue
            for r in hit:
                r["your_label"] = ""
            save(name, fields, rows)
            print(f"\nRelabelling {len(hit)} rows in {name}")
            run(name, show_ai)
    else:
        status()
