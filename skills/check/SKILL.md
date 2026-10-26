---
name: check
description: Check whether a draft sounds like the user, using the voice profile built with /voice-profile:build. Use when the user asks "does this sound like me", wants a draft scored against their voice, wants an AI draft rewritten into their voice, or wants to write something new in their voice. Requires profile.json and shaping-<register>.md from a previous build.
---

# Check a draft against a voice profile

The scripts are in the sibling `build` skill: `<this skill's directory>/../build/scripts/`. The user's profile is in the folder they built it in (default `~/voice-profile/`). If there is no `profile.json`, tell the user to run `/voice-profile:build` first and stop.

## Pick the register first

Read `profile.json` and list the registers. Ask which one this draft is, or infer it from the genre and confirm. Scoring against the wrong register is worse than not scoring: the numbers are confident and pull the prose into the wrong genre. If unsure, run with `--all` and show both.

## Score

```
python3 <build>/scripts/verify.py ~/voice-profile/profile.json draft.md --register <name>
```

Report each FAIL in plain terms with the direction to move ("sentences run too uniform: mix in more under 8 words and a few over 25"). Contractions first. Then re-read the draft against the Big Five scores in `profile.md`, agreeableness first: flag hedges, softening clauses and deferential openings the user wouldn't write.

## If the user wants it rewritten

Load `shaping-<register>.md` as your instructions, rewrite, re-score, and repeat until in band, usually two or three passes. Keep the user's facts and argument; change voice, not content. Show the final verifier output with the draft.

## If the user wants something new written

Same loop: draft with `shaping-<register>.md`, score, revise, then show the draft with its scores.

Never claim a draft "sounds like them" on the numbers alone. The bands catch drift; the user's ear decides.
