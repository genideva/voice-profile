---
name: build
description: Build a measured writing-voice profile from the user's own pre-AI writing and call transcripts, then turn it into a system prompt that makes AI write in their voice. Use when someone wants AI to "sound like me", wants their voice analyzed or measured, wants Big Five or personality scores from their writing, or wants a voice/style prompt built from samples. Walks through corpus intake, register detection, surface metrics, Big Five scoring with quoted evidence, shaping prompt, and a verify loop.
---

# Build a voice profile

You are helping the user build a profile of how they write, measured from their own pre-AI writing, and a shaping prompt that holds a model to it. The method inverts Serapio-García et al., *Nature Machine Intelligence* 7:1954-1968 (2025): instead of measuring a model's personality, score the user's writing to get a target, shape the model toward it, then verify the output landed.

Scripts live in `scripts/` next to this file (standard-library Python 3, nothing to install). Run them with `python3 <this skill's directory>/scripts/<name>.py`. References live in `references/`; read each one at the step that names it.

Work in a folder the user chooses (default `~/voice-profile/`). Everything you write goes there: `corpus/`, `corpus.csv`, `metrics.json`, `profile.json`, `profile.md`, `shaping-<register>.md`.

Tell the user up front, in one or two sentences: the metrics are computed by the scripts in whatever environment runs them (their own machine in Claude Code or Codex), but the Big Five scoring in step 5 means you (the model) read their writing in this session. If that's not acceptable for some documents, leave those out.

## Step 1: Collect the corpus, and throw most of it out

Ask the user for writing they produced **before they used AI tools**. Good sources: published articles, blog posts, essays, long emails and memos, old reports, talk scripts. Aim for 10-30 pieces and 5,000+ words. Fewer works, but the bands will be wide and marked provisional.

Explain the rule in one line: if AI helped write it, measuring it measures the assistant's version of them, and feeding that back makes every round drift further toward the model.

For each document, record a row in `corpus.csv`:

```
path,date,lane,register,ai_touched
corpus/2018-conference-talk.md,2018-05,written,,no
```

- `ai_touched` can't be detected; it's the user's attestation. Default to `unsure` and exclude unless they confirm `no`.
- Save each document as plain `.txt` or `.md` under `corpus/`. Paste-ins are fine; save them as files.
- Leave `register` blank for now.

**Calls and meetings (optional, second lane).** Transcripts are useful for argument shape and stance, never for prose numbers: speech runs far more contractions and looser sentences. Ask which name the user appears under, then:

```
python3 scripts/extract_turns.py call.vtt --speaker "Their Name" --list-speakers
python3 scripts/extract_turns.py call.vtt --speaker "Their Name" --alias "First" --out corpus/call-2024-03.txt
```

This keeps only the user's turns and replaces other people's names, emails and phone numbers with placeholders. Other people's words are dropped entirely. Ask the user to skim the output for anything identifying that slipped through, then add it with `lane=spoken`. Transcripts recorded after AI adoption are fine: no model wrote the speech.

## Step 2: Measure

```
python3 scripts/measure.py corpus.csv --out metrics.json
```

Show the user the summary: documents measured and skipped (with reasons), word counts, and the min/median/max of each metric. Explain any metric they ask about in plain terms (contractions per 1,000 words is a formality proxy; sentence-length standard deviation is rhythm, meaning how much lengths vary, not how long they are).

## Step 3: Find the registers

Most people write in more than one mode, and the modes can differ by 2-4x on these metrics. Averaging them produces a target that matches nothing they wrote.

- **8+ written documents:** run `python3 scripts/build_profile.py metrics.json --suggest-registers`. Read each group's documents and propose a genre name for what they share (for example "argue" for op-eds and memos, "reflect" for personal essays). Confirm with the user.
- **Under 8:** don't cluster. Ask the user to sort the documents by genre themselves.

Write the labels into the `register` column (short, lowercase, no spaces) and re-run step 2. One register is a fine answer if the writing really is one mode.

## Step 4: Build the bands

```
python3 scripts/build_profile.py metrics.json --out profile.json [--banned banned.txt]
```

Ask whether they have words or habits they want banned (a `banned.txt`, one per line). Then show the bands per register and the cross-check table. Distinct registers show few failed checks when a document is scored against its own register and many against the other. If a document fails its own register on 3+ checks, ask whether it's mislabelled or a third mode.

## Step 5: Score personality, with receipts

Read `references/big-five-rubric.md` now and follow its procedure exactly: one register at a time, 1-9 per domain, two verbatim quotes per score, a confidence label, a genre-opportunity check, and a note on what would move each score.

Then measure the model's default, as the rubric's last step describes: write three short drafts on one of the user's own topics with no voice instructions, score them on the same rubric, and report the gap per trait. Agreeableness is usually the largest gap, because assistants are tuned to be agreeable. Never assert a default you didn't score.

## Step 6: Write the profile and the shaping prompt

Read `references/shaping.md`. Write two kinds of file:

- `profile.md`: a readable summary. Per register: the genre, the documents, the surface centers and bands (from `profile.json`), the Big Five scores with quotes and confidence, the model-default gap, and a short "still provisional" note naming how thin the evidence is.
- `shaping-<register>.md`, one per register: the system prompt from the template in `shaping.md`, every placeholder filled from the profile, with two or three of the user's real short sentences quoted as rhythm examples.

## Step 7: Verify the loop works

Pick a topic the user cares about. Draft roughly 400 words using `shaping-<register>.md`, save it, and score it:

```
python3 scripts/verify.py profile.json draft.md --register <name>
```

Revise and re-run until it's in band (two or three passes is normal). Check contractions first, and read the short and long sentence shares together: forcing one breaks the other. Then re-read the draft against the Big Five scores, agreeableness first. If it hedges or softens where the user doesn't, it has drifted to the model's default, and passing numbers don't save it.

Show the user the final draft and the verifier output, and ask them whether it sounds like them. Their ear is the last check. If something specific sounds wrong, fix it in the shaping prompt, not just in the draft.

## Finish

Tell the user what they now have and how to use it: paste `shaping-<register>.md` into a system prompt or project instructions, pick the register before drafting, and use the voice-profile check skill (in Claude Code, `/voice-profile:check`) on anything that carries their name. Suggest the highest-value next addition: usually more pre-AI documents in whichever register is marked provisional.

## Rules

- Never fit anything to text the user says AI touched.
- Never average written and spoken numbers, or two registers.
- Every Big Five score cites the user's own words. No quote, no score.
- Call the bands "working ranges" and the scores "hypotheses with evidence." Don't overclaim precision.
- Don't send the user's writing to any external service or API.
