#!/usr/bin/env python3
"""Keep only your own turns from a call transcript, with other people removed.

Usage:
  python3 extract_turns.py transcript.vtt --speaker "Jane Doe" [--alias Jane --alias JD] [--out mine.txt]
  python3 extract_turns.py notes.txt --speaker "Jane Doe" --list-speakers

Handles two formats:
  - WebVTT / SRT with "Name: text" or "<v Name>text" cues
  - plain lines of "Name: text"
Anything else: clean it by hand into "Name: text" lines first.

Privacy: other speakers' words are dropped entirely. Their names, plus any
email address or phone number, are replaced inside your turns with
placeholders. Read the output before you use it; automatic redaction misses
things (nicknames, company names, details that identify someone).
"""
import argparse
import re
import sys

CUE_TIME = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?[.,]\d{3}\s+-->")
VOICE_TAG = re.compile(r"^<v\s+([^>]+)>(.*)$")
NAME_LINE = re.compile(r"^\s*([A-Z][\w .'\-]{0,40}?)\s*:\s+(.+)$")
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
PHONE = re.compile(r"(?<!\d)(\+?\d[\d ()\-]{7,}\d)(?!\d)")


def parse(text):
    turns = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s == "WEBVTT" or s.isdigit() or CUE_TIME.match(s) or s.startswith("NOTE"):
            continue
        m = VOICE_TAG.match(s)
        if m:
            turns.append([m.group(1).strip(), re.sub(r"</?v[^>]*>", "", m.group(2)).strip()])
            continue
        m = NAME_LINE.match(s)
        if m:
            turns.append([m.group(1).strip(), m.group(2).strip()])
        elif turns:
            turns[-1][1] += " " + s           # continuation of previous cue
    return turns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("--speaker", required=True)
    ap.add_argument("--alias", action="append", default=[])
    ap.add_argument("--out")
    ap.add_argument("--list-speakers", action="store_true")
    a = ap.parse_args()

    turns = parse(open(a.transcript, encoding="utf-8", errors="replace").read())
    speakers = sorted({t[0] for t in turns})
    if a.list_speakers:
        print("\n".join(speakers))
        return
    me = {a.speaker.lower(), *[x.lower() for x in a.alias]}
    others = [s for s in speakers if s.lower() not in me]
    placeholder = {s: "[person %d]" % (i + 1) for i, s in enumerate(others)}
    # Also catch first names on their own ("thanks, Priya").
    for s in others:
        first = s.split()[0]
        if len(first) > 2 and first.lower() not in me:
            placeholder.setdefault(first, placeholder[s])

    mine = []
    for who, said in turns:
        if who.lower() not in me:
            continue
        for name in sorted(placeholder, key=len, reverse=True):
            said = re.sub(r"\b" + re.escape(name) + r"\b", placeholder[name], said)
        said = EMAIL.sub("[email]", said)
        said = PHONE.sub("[phone]", said)
        mine.append(said)
    if not mine:
        sys.exit("No turns for '%s'. Speakers found: %s" % (a.speaker, ", ".join(speakers)))
    out = "\n\n".join(mine) + "\n"
    if a.out:
        open(a.out, "w", encoding="utf-8").write(out)
        print("Kept %d of %d turns (%d words). Replaced %d other speaker names. Wrote %s. Read it before use."
              % (len(mine), len(turns), len(out.split()), len(others), a.out))
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
