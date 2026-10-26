# voice-profile

**Teach AI your voice with a personality test.**

voice-profile is a Claude Code plugin that measures how you write and turns the result into instructions an AI can follow. You give it writing you produced before you started using AI tools. It gives you back three things:

- a **profile** of your voice: ten measured features of your prose, plus your Big Five personality scores, each backed by quotes from your own writing;
- a **shaping prompt** you can paste into any AI tool so it writes the way you do;
- a **verifier** that scores any draft against your profile and says pass or fail on each feature.

Most "write like me" prompts are a few adjectives and a hope. This replaces the hope with numbers you can check.

---

## Contents

- [Quick start](#quick-start)
- [What you need](#what-you-need)
- [What you get](#what-you-get)
- [How it works](#how-it-works)
- [Using your profile day to day](#using-your-profile-day-to-day)
- [Running the scripts without Claude Code](#running-the-scripts-without-claude-code)
- [Privacy](#privacy)
- [Limits](#limits)
- [FAQ](#faq)
- [Background](#background)

---

## Quick start

1. **Install the plugin.** In Claude Code, run:

   ```
   /plugin marketplace add genideva/voice-profile
   /plugin install voice-profile@voice-profile
   ```

2. **Build your profile:**

   ```
   /voice-profile:build
   ```

   Claude walks you through each step and asks for your writing as it goes. Plan on 30 to 60 minutes the first time, most of it spent gathering files.

3. **Check a draft against it:**

   ```
   /voice-profile:check
   ```

Requirements: [Claude Code](https://claude.com/claude-code) and Python 3.8 or newer. There are no packages to install.

---

## What you need

**Writing you did before you used AI tools.** This is the one hard rule. If an AI helped write a document, measuring it measures the AI's version of you. Feed that back as a target and each round drifts a little further from you.

Good sources:

- published articles, blog posts and newsletters
- essays, op-eds and talk scripts
- long emails, memos and reports

How much:

| Amount | What you get |
|---|---|
| 3-5 pieces, under 3,000 words | It works, but the profile is marked provisional and the ranges are wide. |
| 10-30 pieces, 5,000+ words | A solid profile. |
| 8+ pieces in each style you write in | Enough for the plugin to detect your writing modes on its own. |

**Optional: call or meeting transcripts.** These capture how you argue and what you stand for, which helps the shaping prompt. They are never used for the prose measurements, because speech has far more contractions and looser sentences than writing. Transcripts recorded after you started using AI are fine, since no model wrote what you said.

---

## What you get

Everything is saved to a folder you choose (default `~/voice-profile/`):

| File | What it is |
|---|---|
| `profile.md` | Your profile in plain language: your writing modes, your measurements, your Big Five scores with the quotes behind them, and how far the AI's default style sits from yours. |
| `shaping-<mode>.md` | One prompt per writing mode. Paste it into ChatGPT, Claude, a project's instructions, or any system prompt. |
| `profile.json` | The numbers the verifier checks against. |
| `corpus/`, `corpus.csv` | Your documents and the list describing them. |

---

## How it works

The build has seven steps. Claude runs them with you and explains each result.

**1. Collect, and leave most of it out.** You list your documents and confirm for each one whether AI touched it. AI involvement can't be detected reliably, so this is your call, and anything marked unsure is left out by default. For transcripts, a script keeps only your turns and replaces other people's names, emails and phone numbers.

**2. Measure.** Each document is scored on ten features:

| Feature | What it tells you |
|---|---|
| Mean and median sentence length | How long your sentences run |
| Variation in sentence length | Your rhythm: whether you mix short and long sentences, or keep them even |
| Share of sentences of 8 words or fewer | How often you land a short, hard stop |
| Share of sentences of 25 words or more | How often you build a long one |
| Contractions per 1,000 words | How formal you sound ("do not" versus "don't") |
| First person per 1,000 words | How much the writing is about you |
| Second person per 1,000 words | How much you address the reader directly |
| Share of sentences that are questions | Whether you use questions to move an argument along |
| Sentences per paragraph | How dense your paragraphs are |

**3. Find your writing modes.** Most people write in more than one register, for example making an argument versus reflecting on their own experience. The two can differ by two to four times on the features above. An average of the two describes nothing you actually wrote, so each mode gets its own profile. With 8 or more documents the plugin suggests a split. With fewer, you sort them by genre yourself.

**4. Set target ranges.** Each feature gets a working range per mode, taken from the spread across your documents. With few documents the ranges are padded, so no single odd document sets your target. A cross-check then confirms your modes really are different.

**5. Score your personality.** Claude reads your writing against the five Big Five traits (openness, conscientiousness, extraversion, agreeableness, neuroticism) and scores each from 1 to 9. Every score must quote at least two passages of yours and carry a confidence label. Claude then scores three of its own drafts written with no voice instructions, so you can see where the AI's default differs from you. Agreeableness is usually the biggest gap, because assistants are tuned to be polite and accommodating.

**6. Write your shaping prompt.** The prompt has three layers:

- **Personality** sets stance: how blunt or diplomatic, how much you hedge, how much risk you take in a claim. It's written with graded trait adjectives ("very direct," "a bit reserved"), because a model understands trait words far better than "write like Jane."
- **Surface** sets rhythm and formality, using your measured numbers.
- **Argument shape** covers how you open, persuade and close, taken from your own writing.

**7. Test it.** Claude writes a short draft with your prompt, scores it, and revises until it lands in range. Then you read it. Your ear is the final check, and anything that still sounds off gets fixed in the prompt itself, not just in that one draft.

---

## Using your profile day to day

- **Writing with AI:** paste the `shaping-<mode>.md` that matches what you're writing into the system prompt or project instructions. Pick the mode first. A reflective essay held to your argumentative profile will sound wrong, and vice versa.
- **Checking a draft:** run `/voice-profile:check` and point it at the file. It tells you which features are out of range and which way to move them, then rereads the draft for tone.
- **Rewriting an AI draft into your voice:** run `/voice-profile:check` and ask for a rewrite. It keeps your facts and argument and changes only the voice.
- **Improving the profile:** add more pre-AI documents to whichever mode is marked provisional, then run `/voice-profile:build` again.

---

## Running the scripts without Claude Code

The scripts in `skills/build/scripts/` use only the Python standard library and work on their own:

```bash
# 1. measure every document listed in corpus.csv
python3 measure.py corpus.csv --out metrics.json

# 2. optional: look for writing modes (needs 8+ documents)
python3 build_profile.py metrics.json --suggest-registers

# 3. build target ranges for each mode
python3 build_profile.py metrics.json --out profile.json --banned banned.txt

# 4. score a draft (the exit code is the number of failed checks)
python3 verify.py profile.json draft.md --register argue

# keep only your own turns from a transcript
python3 extract_turns.py call.vtt --speaker "Your Name" --out mine.txt
```

`corpus.csv` has one row per document:

```
path,date,lane,register,ai_touched
corpus/2018-conference-talk.md,2018-05,written,argue,no
corpus/2019-essay-on-burnout.md,2019-03,written,reflect,no
corpus/call-2024-03.txt,2024-03,spoken,,no
```

| Column | Values |
|---|---|
| `path` | path to a `.txt` or `.md` file, relative to the CSV |
| `date` | when you wrote it |
| `lane` | `written` or `spoken` |
| `register` | your label for the writing mode, or blank |
| `ai_touched` | `no`, `yes` or `unsure`. Only `no` is measured unless you pass `--include-unsure`. |

The scripts skip headings, tables, code, links, block quotes and a trailing sources list, so you can feed them Markdown as it is.

---

## Privacy

- **The scripts run on your machine** and send nothing anywhere.
- **The personality step is different.** Claude reads your writing in your own session to score it. Leave out anything you wouldn't paste into Claude.
- **Transcripts:** other people's words are dropped entirely, and their names, emails and phone numbers are replaced inside your turns. Automatic redaction misses things (nicknames, company names, identifying details), so read the output before using it.
- **Keep your files out of this repo.** Your corpus and profile live in your own folder. The `.gitignore` blocks the usual filenames as a backstop.

---

## Limits

- **The personality scores are hypotheses, not measurements.** A validated personality test asks a person hundreds of calibrated questions. Here a model reads your prose against the trait definitions. The quotes are there so you can check each score and disagree with it.
- **Small samples give wide ranges.** A FAIL from the verifier means "look at this," not "this is wrong."
- **Two known traps are built into the prompts.** Telling a model to be blunt tends to make it formal, and formal writing drops contractions, so contractions get checked first. And pushing for short sentences squeezes out long ones, so the two are read together.
- **English prose only.** The measurements assume English punctuation and contractions.

---

## FAQ

**Can I use writing that AI only lightly edited?**
Mark it `unsure`, and it's left out by default. Light edits change exactly the features being measured: sentence length, contractions and hedging.

**I only have a few old pieces. Is it worth it?**
Yes. You'll get a provisional profile with wide ranges, which still catches the biggest drift. Add documents as you find them.

**Does it work with ChatGPT or other models?**
The shaping prompt is plain text and works in any model. The build and check steps run in Claude Code, and the scripts run anywhere Python does.

**Why the Big Five and not a style guide?**
A style guide describes surface habits. Trait scores set stance: how hard you push, how much you soften. Stance is what makes AI writing sound generically polite, and it's what most style guides never touch.

---

## Background

The method inverts a published study. Serapio-García and colleagues gave language models a validated personality test, showed the results were reliable, and then shaped the models' personalities on purpose using graded trait adjectives. This plugin runs the same idea in reverse: measure a person's writing, shape the model toward that person, and verify the result.

> Serapio-García, G., Safdari, M., Crepy, C., Sun, L., Fitz, S., Romero, P., Abdulhai, M., Faust, A. & Matarić, M. "A psychometric framework for evaluating and shaping personality traits in large language models." *Nature Machine Intelligence* 7, 1954-1968 (2025). [doi.org/10.1038/s42256-025-01115-6](https://www.nature.com/articles/s42256-025-01115-6)

The trait definitions follow the public-domain [International Personality Item Pool](https://ipip.ori.org/) (IPIP-NEO).

## License

MIT. See [LICENSE](LICENSE).
