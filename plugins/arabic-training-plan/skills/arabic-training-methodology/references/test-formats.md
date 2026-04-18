# Test Formats

The five prompt types for Key-Fact testing. Rotate them so every word gets exercised along all modalities before the learner reaches Mastery 5/5.

## The five types

### Type A — Audio → meaning

Pick a word. Present:

> **1.** Play `audio/<slug>.mp3`.
>
> What does this word mean in English?

Expected answer: the English gloss. Accept synonyms that convey the core sense.

**Probes:** recognition from sound alone. Use early in the plan and in every retention round (since it's the hardest to fake from context).

### Type B — English → Arabic production

> **2.** Write the Arabic word for **"<english gloss>"** — give Arabic script AND transliteration.

Expected: the headword's Arabic + transliteration. Accept missing short-vowel diacritics; penalise wrong root/form.

**Probes:** active production from meaning. The gap between recognition and production is where most learners stall — this type catches it.

### Type C — Fill-in-the-blank

Pick example sentence 1 or 2 for the word. Blank the headword. Present:

> **3.** Fill in the blank:
>
> **Arabic:** <example sentence with ___ where headword was>
>
> **Translit:** <sentence translit with ___ blanked>
>
> **English:** <full translation>

Expected: the headword (Arabic preferred; accept transliteration alone if the Arabic is close).

**Probes:** in-context production — the hardest step up from type B because the learner must also get the form right (verb conjugation, gender agreement, possessive suffix).

### Type D — Audio → transliteration

> **4.** Play `audio/<slug>.mp3`. Write the transliteration (Roman letters).

Expected: any unambiguous transliteration. `shlonak / šlōnak / shloonak` are all fine; `slonak` misses the `sh` and is penalised.

**Probes:** grapheme-to-sound mapping. Surfaces confusions between similar sounds (`ḥ` vs `h`, `s` vs `ṣ`, `t` vs `ṭ`).

### Type E — Translate the sentence

> **5.** Translate this English sentence into Arabic (target word: **<headword>**):
>
> "<English sentence containing the target word>"

Give them a fresh sentence — not one of the two examples from `words.json`. Keep it short (≤ 8 words).

Expected: a grammatical Arabic sentence using the target word correctly. Accept reasonable word order variations.

**Probes:** productive use in a novel frame. The closest proxy for "could the learner actually say this in a conversation".

## Rotation rules

- In the Initial Test (5 prompts, one per word), use all 5 types
- In the Final Test, rotate so no word is tested with the same type as in the Initial Test
- In retention rounds (3 prompts), never repeat a type used in the previous retention round for the same word (check `words.json.stats.last_prompt_type`)
- Always include at least one audio-based prompt (A or D) if audio files exist
- Always include at least one production prompt (B or E) — recognition alone doesn't prove mastery

## Failure-mode → next-prompt-type mapping

If a word failed with failure mode X, next round should target the complementary skill:

| Failure mode | Next prompt type |
|--------------|------------------|
| `[sound-to-meaning]` | A (more sound practice) |
| `[meaning-to-form]` | B or E (force production) |
| `[grapheme-to-sound]` | D (sound-out practice) |
| `[usage]` | C or E (in-context production) |
| `[conflation]` | contrast probe (see below) |

## Contrast probe (for conflation gaps)

When two words in the same group are confused, design a single disambiguating prompt:

> Which word fits the blank — **<word A>** or **<word B>**?
>
> "<sentence with ___ where only one of them fits>"
>
> Explain in one sentence why the other is wrong.

This tests both recognition AND the boundary between the two.

## Motivation & Core Principle prompts

- Motivation SGs: narrative prompts ("Name one situation where you'll use this in the next 30 days"). No audio. No vocabulary production.
- Core Principle SGs: identification tasks ("Which of these 3 sentences obey <principle>? Fix the violators"). Always include audio of the example sentences so the learner hears the rule in action.

## Grading tolerance

- Transliteration: accept any unambiguous variant; penalise only when letters don't map
- Arabic production: accept missing short-vowel diacritics; penalise wrong root, wrong form, wrong letter
- Meaning: accept synonyms conveying the core sense; flag nuance misses as PARTIAL
- Sentence translation: accept reasonable word-order and morphology variations; the target word MUST be present in correct form
