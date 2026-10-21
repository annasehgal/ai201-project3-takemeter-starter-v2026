#!/usr/bin/env python3
"""
Re-run notebook sections 1-5 with settings overridden, writing to NEW files so
the original results.json and test_split.csv are never touched.

    python run_experiment.py --out results_exp2_epochs6.json --epochs 6

It executes the code cells of takemeter.ipynb exactly as written, in order, up
to the "Unit 6 starts here" line. The only changes:
  - after the settings cell runs, the settings you pass here replace the
    notebook's values;
  - the results cell writes to --out and --split-out instead of results.json
    and test_split.csv.
The settings actually used are added to the output file under "settings".
"""
import argparse
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True, help="results file to write (not results.json)")
    p.add_argument("--split-out", default=None, help="test split file (default: <out>_test_split.csv)")
    p.add_argument("--csv", default="labels.csv")
    p.add_argument("--epochs", type=int)
    p.add_argument("--lr", type=float)
    p.add_argument("--batch", type=int)
    p.add_argument("--max-length", type=int)
    p.add_argument("--seed", type=int)
    a = p.parse_args()

    out = a.out
    split_out = a.split_out or out.replace(".json", "") + "_test_split.csv"
    for f in (out, split_out):
        if Path(f).name in ("results.json", "test_split.csv"):
            raise SystemExit(f"Refusing to overwrite the original {f}.")

    overrides = {k: v for k, v in {
        "EPOCHS": a.epochs, "LEARNING_RATE": a.lr, "BATCH_SIZE": a.batch,
        "MAX_LENGTH": a.max_length, "SEED": a.seed}.items() if v is not None}

    os.chdir(REPO)
    nb = json.loads((REPO / "takemeter.ipynb").read_text(encoding="utf-8"))
    ns = {"__name__": "__main__"}
    for cell in nb["cells"]:
        src = "".join(cell["source"])
        if cell["cell_type"] == "markdown" and "Unit 6 starts here" in src:
            break
        if cell["cell_type"] != "code":
            continue
        if 'CSV = "labels.csv"' in src:
            src = src.replace('CSV = "labels.csv"', f"CSV = {a.csv!r}")
        if 'open("results.json", "w")' in src:
            assert 'test_df.to_csv("test_split.csv"' in src
            src = (src.replace('open("results.json", "w")', f"open({out!r}, \"w\")")
                      .replace('test_df.to_csv("test_split.csv"', f"test_df.to_csv({split_out!r}"))
        exec(compile(src, "takemeter.ipynb", "exec"), ns)
        if "EPOCHS = " in src and "LEARNING_RATE = " in src:
            ns.update(overrides)
            print(f"[experiment] overrides: {overrides or 'none'}")
            print(f"[experiment] seed {ns['SEED']}, {ns['EPOCHS']} epochs, lr {ns['LEARNING_RATE']}, "
                  f"batch {ns['BATCH_SIZE']}, max_length {ns['MAX_LENGTH']}")

    res = json.loads(Path(out).read_text())
    res["settings"] = {
        "csv": a.csv, "base_model": ns["BASE_MODEL"], "seed": ns["SEED"],
        "epochs": ns["EPOCHS"], "learning_rate": ns["LEARNING_RATE"],
        "batch_size": ns["BATCH_SIZE"], "max_length": ns["MAX_LENGTH"],
        "overrides": overrides, "test_split_file": split_out,
    }
    Path(out).write_text(json.dumps(res, indent=2))
    print(f"[experiment] wrote {out} and {split_out}")


if __name__ == "__main__":
    main()
