#!/usr/bin/env python3
"""Measure every document in a corpus manifest.

Usage:
  python3 measure.py corpus.csv [--out metrics.json] [--include-unsure]

corpus.csv columns (header row required):
  path        file path, relative to the csv or absolute (.txt or .md)
  date        when you wrote it (YYYY or YYYY-MM-DD)
  lane        written | spoken
  register    a short label you choose (e.g. argue, reflect); blank = unassigned
  ai_touched  no | yes | unsure

Rows with ai_touched=yes are always excluded. Rows marked unsure are excluded
unless --include-unsure is passed. Fitting a voice model to AI-assisted text
measures the assistant's version of you, then feeds it back to the assistant.
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from textstats import measure, METRICS  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--out", default="metrics.json")
    ap.add_argument("--include-unsure", action="store_true")
    a = ap.parse_args()

    base = os.path.dirname(os.path.abspath(a.manifest))
    docs, skipped = [], []
    with open(a.manifest, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row = {k.strip(): (v or "").strip() for k, v in row.items() if k}
            ai = row.get("ai_touched", "unsure").lower() or "unsure"
            if ai == "yes" or (ai != "no" and not a.include_unsure):
                skipped.append((row.get("path"), "ai_touched=" + ai))
                continue
            path = row["path"] if os.path.isabs(row["path"]) else os.path.join(base, row["path"])
            if not os.path.exists(path):
                skipped.append((row["path"], "file not found"))
                continue
            raw = open(path, encoding="utf-8", errors="replace").read()
            m, counts = measure(raw)
            if m is None or counts["sentences"] < 5:
                skipped.append((row["path"], "under 5 sentences after cleaning"))
                continue
            docs.append({
                "path": row["path"],
                "date": row.get("date", ""),
                "lane": (row.get("lane") or "written").lower(),
                "register": row.get("register", ""),
                "metrics": m,
                "counts": counts,
            })

    json.dump({"docs": docs, "skipped": skipped}, open(a.out, "w"), indent=1)

    written = [d for d in docs if d["lane"] == "written"]
    spoken = [d for d in docs if d["lane"] == "spoken"]
    print("Measured %d documents (%d written, %d spoken). Skipped %d." %
          (len(docs), len(written), len(spoken), len(skipped)))
    for p, why in skipped:
        print("  skipped %-40s %s" % (p, why))
    words = sum(d["counts"]["words"] for d in written)
    print("Written words: %d. Spoken words: %d." % (words, sum(d["counts"]["words"] for d in spoken)))
    if words < 3000:
        print("WARNING: under 3,000 written words. Bands will be wide and provisional.")
    print("\n%-34s %8s %8s %8s" % ("written lane", "min", "median", "max"))
    for k, label in METRICS.items():
        vals = sorted(d["metrics"][k] for d in written)
        if vals:
            mid = vals[len(vals) // 2]
            print("%-34s %8.1f %8.1f %8.1f" % (label[:34], vals[0], mid, vals[-1]))
    print("\nWrote", a.out)


if __name__ == "__main__":
    main()
