# Big Five scoring rubric for writing samples

Used in step 5 of the build. The model reads the user's pre-AI writing, one register at a time, and scores each of the five domains on a 1-9 scale. The domain definitions follow the public-domain IPIP-NEO (International Personality Item Pool, Goldberg et al.), paraphrased here for written text.

**Be honest about what this is.** A validated instrument asks a person 300 calibrated questions. This is a model reading prose against definitions. The output is a set of hypotheses with quoted evidence, not a measurement. Say so in the profile.

## Scale

| Score | Meaning |
|---|---|
| 1 | extremely low |
| 2 | very low |
| 3 | low |
| 4 | a bit low |
| 5 | neutral, or no evidence either way |
| 6 | a bit high |
| 7 | high |
| 8 | very high |
| 9 | extremely high |

## The five domains, as they show up on the page

### Openness to experience
How much the writer reaches for new ideas, unusual framings and analogies from other fields, and how readily they argue against an established view.
- **High signals:** cross-domain analogies, arguing against consensus, proposing mechanisms that don't exist yet, curiosity questions.
- **Low signals:** convention as justification ("best practice is"), concrete-only framing, skepticism toward new methods for their own sake.
- Facets: imagination, artistic interests, emotionality, adventurousness, intellect, liberalism.

### Conscientiousness
Order, thoroughness and drive, visible in the structure of the writing.
- **High signals:** numbered steps, explicit sequencing ("First... Second..."), checklists, criteria, follow-through language, precise numbers.
- **Low signals:** loose structure, digressions left unresolved, improvisation praised over planning.
- Facets: self-efficacy, orderliness, dutifulness, achievement-striving, self-discipline, cautiousness. Cautiousness often moves separately; note it.

### Extraversion
Assertiveness and energy, plus warmth and sociability when the genre allows it.
- **High signals:** direct address to the reader, confident declaratives, exclamation, naming people, describing collaboration with enthusiasm.
- **Low signals:** understatement, impersonal constructions, restraint.
- Facets: friendliness, gregariousness, assertiveness, activity level, excitement-seeking, cheerfulness. Argumentative writing shows assertiveness and hides warmth; don't read the missing warmth as a low score.

### Agreeableness
How much the writer softens, defers and accommodates. **This is usually the trait that separates a person's writing from default model prose**, because assistants are tuned to be agreeable.
- **High signals:** hedges ("perhaps," "you might consider"), softening clauses before criticism, praise before critique, inclusive "we," apologies.
- **Low signals:** criticism stated flatly, named targets ("the industry got this wrong"), no cushioning, disagreement as assertion rather than question.
- Facets: trust, morality, altruism, cooperation, modesty, sympathy.

### Neuroticism (emotional volatility)
How much worry, stress or self-consciousness shows, and how the writer handles pressure on the page.
- **High signals:** anxiety stated in the present tense, catastrophizing, defensiveness, repeated self-doubt.
- **Low signals:** calm under criticism, problems named and then solved, steady tone.
- Facets: anxiety, anger, depression, self-consciousness, immoderation, vulnerability.

## Procedure

1. **Score one register at a time.** Never pool registers. A trait can legitimately differ between them; agreeableness often does.
2. **Quote evidence for every score:** at least two verbatim passages of one or two sentences each, from different documents where possible. No quote, no score; write 5 and mark it "no evidence."
3. **Label confidence.** HIGH = several passages across documents agree. MODERATE = one strong passage or two weak ones. LOW = inferred from absence, or one document.
4. **Check genre opportunity.** Ask whether the genre could show the trait at all. An op-ed rarely shows warmth or distress. If it can't, mark the score LOW confidence rather than scoring the absence as a low trait.
5. **Separate disclosure from trait.** Writing openly about a hard time shows willingness to disclose, which depends heavily on genre. It is weak evidence of high neuroticism.
6. **Note what would move each score**, so the user can argue with it.
7. **Optional but recommended: score the model's default.** Ask for three drafts on one of the user's topics with no voice instructions, score them on the same rubric, and record the gap. A measured gap ("default 6, you 3") is far more useful, and more honest, than an assumed one.

## Output format, per register

```
### Register: <name>   (n docs, n words)

Openness <n>/9 · confidence <HIGH|MODERATE|LOW>
  "…quote…"  (doc, year)
  "…quote…"  (doc, year)
  Would move down if: …

…all five…

Model default (3 unshaped drafts): O <n> · C <n> · E <n> · A <n> · N <n>
Largest gap: <trait> (you <n>, default <n>)
```
