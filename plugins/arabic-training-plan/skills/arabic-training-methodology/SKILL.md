---
name: arabic-training-methodology
description: TTT (Test-Teach-Test) methodology adapted to Arabic vocabulary learning — Najdi Saudi or Modern Standard Arabic. Decomposes a learning goal into SMART / Motivation / Core Principles (dialect grammar rules) / Key Facts (vocabulary batches). Interactive sessions only — no flashcards or HTML viewers. Audio is generated once per word into a referenced folder. Spaced retention advances each sub-goal toward Mastery 5/5. Load when creating or running an Arabic training plan, running a session, or running a retention check.
---

# Arabic Training Methodology

Build and run a Test-Teach-Test training plan for Arabic vocabulary that drills recognition, production, and retention through interactive sessions — never through flashcards.

## When to apply this skill

- User asks to "create an Arabic training plan", "train me on Najdi/MSA", "build a TTT plan for Arabic vocab"
- User invokes `/create-arabic-training`, `/run-arabic-session`, or `/arabic-retention-check`
- User references an existing `*_training_plan.md` file in an Arabic training folder
- User wants to re-test or confirm previously learned Arabic words

## Core principles

**TTT, not flashcards.** This plugin exists because flashcards break down at the production step — recognising a card flip isn't the same as producing the word in a sentence under pressure. Every session is a dialogue: prompt → learner answer → evaluation → targeted teaching on gaps → re-test.

**Principles before words.** A learner who has the dialect's grammar rules (Najdi `ma`-negation, `gaa'id` progressive, `abgha/widdi` desire) can absorb vocabulary 3–5× faster than one memorising words in isolation. Core Principle sub-goals always precede Key Fact sub-goals in the sequence.

**Key Facts = vocabulary batches.** Each Key Fact sub-goal holds 5–8 words that share a theme slice, part of speech, or governing principle. Individual words are not sub-goals (that would create 30+ SGs for a small deck). Within a sub-goal, the 5-prompt Initial Test samples one prompt type per word.

**Audio is a first-class signal.** Every word has an MP3. Tests reference it by filename (`audio/<slug>.mp3`) so the learner can click or open it. Recognition without audio is incomplete.

**Spaced retention until full memorisation.** Completing the Final Test is not the end — it sets Mastery 2/5. The learner climbs to 5/5 only by passing retention rounds at 1d, 3d, 7d, 21d, 60d intervals. A plan is **fully memorised** only when every Key Fact sub-goal is at 5/5.

## Plan structure

The plan file (`<plan-slug>_training_plan.md`) has exactly these sections, in this order:

1. **Header** — title, date, variety, theme, word count, status, audio dir
2. **Learning Goal** — user's raw input
3. **SMART Goal** — refined, ≤20 words
4. **Motivation** — paragraph
5. **Core Principles** — table of 3–5 grammar rules
6. **Word List (Key Facts)** — table of every word with principle + SG assignment + audio path
7. **Sub-Goals** — table: # | Axis | Statement | Difficulty | Principle | Status | Mastery | Last Tested | Next Due
8. **Sequence** — dependency notes
9. **Session Blueprints** — one block per sub-goal with Initial Test, Pass Criteria, Teach Topics, Final Test (Core Principle SGs also include a fully worked example)
10. **Progress Log** — appended to by every session and retention round
11. **Retention Schedule** — Mastery-to-interval table (always the same; reference the skill for source of truth)

See `references/` for the specifics of each section.

## Reference files

Load the relevant one for the current sub-task:

- **`references/word-selection.md`** — how to pick a word list: Najdi-marking vs MSA-domain-appropriate, POS mix, what to exclude.
- **`references/test-formats.md`** — the 5 prompt types (A audio→meaning, B English→Arabic, C fill-in-blank, D audio→translit, E translate sentence) and the rotation rules.
- **`references/retention.md`** — the mastery/interval table, transition rules, word-selection weighting for retention rounds.

## Bundled scripts

- **`scripts/generate_audio.py`** — reads `words.json`, synthesises MP3s for every headword and every example sentence via gTTS (default) or ElevenLabs (`--provider elevenlabs`, requires `ELEVENLABS_API_KEY`). In sandboxed environments that block `translate.google.com` it drops three recovery scripts (`regen_audio.bat`, `regen_audio.sh`, `regen_audio.py`) next to the manifest.

## Workflow

**Creating a plan:**
1. Parse theme, variety, word count
2. Refine SMART goal
3. Write Motivation
4. Identify 3–5 Core Principles
5. Propose word list → one round of user sign-off
6. Group words into Key-Fact sub-goals of 5–8
7. Generate audio
8. Write the plan file and `words.json`

**Running a session:**
1. Find the plan and `words.json`; check for checkpoint
2. Phase 1 INITIAL TEST — build prompts per axis; always append the two mandatory notes
3. Phase 2 EVALUATE — classify gaps using the word-level failure taxonomy
4. Phase 3 TEACH — one tight block per gap; short Quick Check
5. Phase 4 FINAL TEST — new prompt set, rotated types
6. Phase 5 EVALUATE FINAL — up to 2 loops
7. Phase 6 RECORD — update plan, transcript, learner profile, per-word stats, delete checkpoint

**Retention round:**
1. Collect sub-goals where Next Due ≤ today AND Mastery < 5
2. For each, build a 3-prompt mini-TTT weighted by historical weakness (`words.json.stats`)
3. Evaluate, teach briefly only on misses, update Mastery and Next Due per the transition table

## Word-level failure taxonomy

Use these tags (not the generic `training-plan` failure modes) when classifying vocabulary gaps:

- `[sound-to-meaning]` — heard audio but couldn't recall the meaning
- `[meaning-to-form]` — knew the concept but couldn't produce the Arabic
- `[grapheme-to-sound]` — read the Arabic but couldn't pronounce/transliterate
- `[usage]` — knew the word but couldn't use it in a sentence
- `[conflation]` — confused with a sister word in the same group or its MSA/Najdi counterpart

These tags drive `/arabic-retention-check`'s prompt-type selection — e.g. a `[meaning-to-form]` failure should come back as a type B or E prompt next round, not type A.

## Common mistakes to avoid

- Treating Key Facts as one-word sub-goals (explodes the plan — group them)
- Writing a Najdi plan but testing with MSA prompts (fails dialect fidelity)
- Building an HTML deck or any flashcard UI (the whole point is to avoid that)
- Skipping the Motivation sub-goal (it anchors the plan in a real situation)
- Skipping Core Principles (then Key Facts have nothing to rest on)
- Forgetting to update `words.json.stats` after a session (retention weighting breaks)
- Inventing an audio filename instead of reading it from `words.json`
