# Privacy policy

**Effective:** 26 October 2026 · **Applies to:** the voice-profile plugin, its scripts, and the ChatGPT GPT built from this repo.

## The short version

voice-profile has no server, no account and no analytics. Its authors receive none of your data.

## What the plugin reads

- **The documents you give it:** your own writing, and any call or meeting transcripts you choose to add.
- **Drafts you ask it to check.**

Transcripts can contain other people's names, email addresses and phone numbers. The transcript script reads them only to remove them. Other speakers' words are dropped entirely, and their names, emails and phone numbers inside your turns are replaced with placeholders.

## What it stores, and where

Everything is written as plain files to a folder you choose on your own computer (default `~/voice-profile/`):

- your documents (`corpus/`) and the list describing them (`corpus.csv`);
- your measurements (`metrics.json`) and profile (`profile.json`, `profile.md`, which quotes passages from your writing);
- your shaping prompts (`shaping-<mode>.md`).

Nothing is retained anywhere else by the plugin. Delete the folder and the data is gone.

## What is sent off your computer

- **The scripts send nothing.** They use only the Python standard library and make no network calls.
- **The personality-scoring step happens inside your AI session.** In Claude Code, Claude reads your writing to score it, so that text is handled under your agreement with Anthropic. Nothing goes to any other service.
- **The ChatGPT version** runs in ChatGPT, so the files you upload there are handled by OpenAI under your agreement with them, including whether chats are used for training.

## Your choices

- Leave out any document you don't want an AI to read.
- Read transcript output before using it. Automatic redaction can miss nicknames, company names and other identifying details.
- Keep your corpus and profile outside this repository, so they never end up in a commit.

## Children

voice-profile is not intended for users under 18.

## Changes and contact

Changes to this policy are made in this file, and its history is public in the repository. Questions: open an issue at [github.com/genideva/voice-profile/issues](https://github.com/genideva/voice-profile/issues).
