# Set up Voice Profile as a ChatGPT GPT

This turns the same method and scripts into a Custom GPT. It takes about 10 minutes in ChatGPT's GPT builder. Creating a GPT needs a paid ChatGPT plan. Anyone can use a GPT once it's shared.

## 1. Gather the files

From this repo you need:

| File | Where it is |
|---|---|
| `instructions.md` | `chatgpt/` (paste its text, don't upload it) |
| `textstats.py` | `skills/build/scripts/` |
| `measure.py` | `skills/build/scripts/` |
| `build_profile.py` | `skills/build/scripts/` |
| `verify.py` | `skills/build/scripts/` |
| `extract_turns.py` | `skills/build/scripts/` |
| `big-five-rubric.md` | `skills/build/references/` |
| `shaping.md` | `skills/build/references/` |
| `icon.png` | `.claude-plugin/` |

## 2. Create the GPT

1. Go to [chatgpt.com/gpts/editor](https://chatgpt.com/gpts/editor) and open the **Configure** tab.
2. **Image:** upload `icon.png`.
3. **Name:** `Voice Profile`
4. **Description:** `Measure your writing voice from your own pre-AI writing and get a prompt, plus a pass/fail check, that holds AI to it.`
5. **Instructions:** paste the full text of `chatgpt/instructions.md`.
6. **Conversation starters:**
   - `Build my voice profile from my old writing`
   - `Check whether this draft sounds like me`
   - `Rewrite this AI draft in my voice`
   - `What do the measurements mean?`
7. **Knowledge:** upload the five `.py` files and the two `.md` reference files from the table above (seven files).
8. **Capabilities:** turn on **Code Interpreter & Data Analysis**. Web search and image generation can stay off.
9. **Actions:** none.

## 3. Test before sharing

Start a chat with the GPT in preview and paste in three or four old pieces of your own. Confirm that:

- it asks whether AI touched each piece;
- it runs `measure.py` and shows real numbers instead of estimating them;
- `profile.json` and `shaping-<mode>.md` come back as downloadable files at the end.

If it describes metrics without running a script, Code Interpreter is off or the `.py` files didn't upload.

## 4. Share it

Click **Create** (or **Update**) and choose who can access it:

- **Only me:** for testing.
- **Anyone with the link:** share the link in your post or README.
- **GPT Store:** requires a verified builder profile (Settings → Builder profile: verify your name or a website you own). Pick the Writing category.

Use a personal ChatGPT account, not a work one, if you want the GPT kept separate from your employer.

## How it differs from the Claude Code version

- **Files don't persist.** ChatGPT clears its sandbox between chats. Users download `profile.json` and their shaping prompts at the end, and re-upload `profile.json` to check drafts later. The GPT tells them this.
- **Privacy.** In Claude Code the measurements run on the user's own machine. In the GPT, their writing and the scripts run in ChatGPT, so their files go to OpenAI. The GPT says this up front.
- **Updates.** When the scripts or references change in this repo, re-upload them under Knowledge.
