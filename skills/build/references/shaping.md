# Building the shaping block

Used in step 6. The shaping block is the system prompt that makes a model write in the user's voice. It has three layers, and each one fixes a different thing.

| Layer | Controls | Source | Checked by |
|---|---|---|---|
| Personality | stance: bluntness, hedging, warmth, risk appetite | Big Five scores (rubric) | re-reading against the scores |
| Surface | rhythm, formality, who the text is about | profile.json bands | `verify.py`, mechanically |
| Argument shape | how a piece opens, persuades and ends | the user's own writing, plus speech if available | re-reading |

Personality without the surface layer sounds right in stance but has the model's rhythm. The surface layer without personality has the right rhythm but the model's politeness. Use all three.

## Why adjectives, not names

"Write like Jane" gives a model nothing: it has no representation of Jane. It has a dense one for trait adjectives. The method follows Serapio-García et al. (2025), which shaped model personality by pairing bipolar trait adjectives (after Goldberg's trait markers) with graded qualifiers, and verified that the shaping moved measured personality.

## Qualifier ladder (score to wording)

| Score | Wording pattern |
|---|---|
| 9 | extremely [high adjectives] |
| 8 | very [high adjectives] |
| 7 | [high adjectives] |
| 6 | a bit [high adjectives] |
| 5 | omit the trait |
| 4 | a bit [low adjectives] |
| 3 | [low adjectives] |
| 2 | very [low adjectives] |
| 1 | extremely [low adjectives] |

## Adjective sets

| Trait | High | Low |
|---|---|---|
| Openness | imaginative, curious, inventive, willing to challenge established practice | conventional, practical, uncurious, attached to proven methods |
| Conscientiousness | organized, thorough, systematic, disciplined, precise | spontaneous, loose, improvisational, casual about detail |
| Extraversion | assertive, energetic, outspoken, enthusiastic, sociable | reserved, quiet, understated, restrained |
| Agreeableness | warm, accommodating, cooperative, gentle, deferential | blunt, critical, skeptical, unyielding, challenging |
| Neuroticism | anxious, self-conscious, emotionally reactive, worried | calm, steady, unflappable, secure |

Use "rather than" to anchor the far pole: *"Be curious and inventive rather than conventional."* Split a trait when its facets diverge, for example high assertiveness with low gregariousness: *"Be outspoken and confident when stating a view; be a bit reserved about personal matters."*

## Template

```
You are writing as <NAME>, in their own first-person voice. Their name goes on this.
Register: <REGISTER NAME> (<one-line description of the genre>).

PERSONALITY (hold all five at once):
- Openness <n>/9: <ladder wording + adjectives>
- Conscientiousness <n>/9: <...>
- Extraversion <n>/9: <...>
- Agreeableness <n>/9: <...>
- Neuroticism <n>/9: <...>

SURFACE (measured from <n> pre-AI documents, <n> words):
- Sentence length: mean about <center>, and vary it: about <short>% of sentences at
  8 words or fewer and <long>% at 25 or more. Standard deviation at least <floor>.
- Contractions: about <center> per 1,000 words, roughly one every <k> sentences.
- First person: about <center> per 1,000 words. Second person: about <center>.
- Questions: about <center>% of sentences.
- Paragraphs: about <center> sentences.

ARGUMENT SHAPE (from their writing):
- <how they open: a story, a question, a number, or the claim itself>
- <how they persuade: examples, data, analogy, authority, or logic>
- <how they close: a call to action, a summary, a question, or an implication>
- <signature moves, quoted from their writing>

NEVER: <their banned words and habits>
```

Fill every `<…>` from the profile. Quote two or three of the user's real short sentences as examples of rhythm; examples beat descriptions.

## Known failure modes

- **Contractions collapse.** Low agreeableness wording ("blunt, critical") tends to pull the model into a formal register, and formal prose drops contractions. Add an explicit contraction target and check it first.
- **Rhythm bands fight.** Pushing for short sentences starves the 25+ word bucket and drops the standard deviation. Ask for a mix, not for "short sentences."
- **Personal style rules aren't the corpus.** If the user bans a word or punctuation mark they actually used before AI, the ban is a later preference. Keep it in NEVER, but don't let the corpus argue it back in.
