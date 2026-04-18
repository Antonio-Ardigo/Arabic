---
description: Build a TTT training plan for Arabic vocabulary (Najdi or MSA) with SMART goal, motivation, core principles, and key-fact sub-goals. Generates audio per word.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "[theme] [najdi|msa] [word-count]"
---

# /create-arabic-training — Arabic TTT Training Plan Builder

You are building a **Test-Teach-Test (TTT) training plan** for Arabic vocabulary — not a flashcard deck. There is no HTML viewer, no flip-card UI. Learning happens through interactive TTT sessions; audio is stored in a folder and referenced by filename in the session prompts.

Load and follow the `arabic-training-methodology` skill before anything else — it contains the plan schema, word-selection rules, test-prompt formats, and the retention scheduler.

## Step 0: Load the skill

Read `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/SKILL.md` in full. Also read:
- `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/word-selection.md` — how to pick words per variety and theme
- `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/test-formats.md` — prompt formats you'll bake into session blueprints
- `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/retention.md` — the spaced-retention schedule this plan will run under

## Step 1: Parse arguments

The command argument is `$ARGUMENTS`. Parse into:
- **theme** — e.g. "daily conversation", "business", "travel", "family"
- **variety** — `najdi` | `msa`
- **word-count** — integer total vocabulary count; default **25**

If theme or variety is missing, ask ONE consolidated question via AskUserQuestion. Do not re-ask if they're already present.

## Step 2: Refine into a SMART Goal

A single sentence, ≤ 20 words, naming: the variety, the theme, the word count, and an implied verification (e.g. "Master 25 Najdi daily-conversation words — recognise by audio and produce from English prompts").

## Step 3: Motivation

Write ONE Motivation sub-goal that captures *why* the learner is doing this (e.g. "Hold a casual Najdi conversation in Riyadh without switching to English"). This becomes SG-1 and it tests whether the learner can state their own motivation and pick a target situation.

## Step 4: Core Principles (dialect grammar rules)

Identify **3–5 core principles** that govern the chosen variety and theme. Examples:

**Najdi core principles:**
- Negation with `ma` + verb (not MSA `la/lam/laysa`)
- Progressive aspect with `gaa'id / gaa'da + imperfect`
- Desire/volition particles: `abgha` (want), `widdi` (wish), replacing MSA `uriidu`
- Feminine `-a` elision in many positions; `-ich` 2nd-person-feminine suffix
- Possession with `hagg` + noun (not MSA `li-`)

**MSA core principles (pick per theme):**
- Verbal sentence vs nominal sentence (VSO default)
- Iḍāfa (construct state) for possession
- Sound vs broken plurals
- Case endings for definite / indefinite
- Root-pattern morphology (form I–X)

For each principle, fill this table:

| Principle | Statement | Example | Prerequisites |
|-----------|-----------|---------|---------------|
| <short name> | <one sentence> | <one Arabic example + gloss> | <what the learner must already know> |

Each principle becomes a Core Principle sub-goal (one per principle).

## Step 5: Plan the word list (Key Facts)

Propose `word-count` high-frequency, in-theme head-entries. Follow `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/word-selection.md`:
- Najdi: prefer words that *mark* the dialect or are structural workhorses
- MSA: prefer domain-accurate corporate / travel / family register (no greetings in a business deck)
- Mix parts of speech unless theme is noun-heavy
- No duplicates; no pan-Arabic beginner filler

Show the learner a table: `# | Arabic | Translit | English | POS`. Get ONE round of sign-off — edits permitted. Don't over-ask.

**Grouping.** Split the approved list into Key-Fact sub-goals of **5–8 words each**. Pick the grouping so that words in the same sub-goal share a theme slice or part of speech (e.g. "question words", "desire verbs", "time adverbs"). Each group becomes ONE sub-goal.

## Step 6: Build the plan skeleton

Create a working folder: `arabic-training-<variety>-<theme-slug>-<YYYYMMDD>/`. Inside it:

- `words.json` — machine-readable manifest. Schema:
  ```json
  {
    "variety": "najdi",
    "theme": "daily conversation",
    "words": [
      {
        "slug": "abgha",
        "arabic": "أبغى",
        "translit": "abgha",
        "english": "I want (Najdi)",
        "pos": "verb",
        "principle": "P3-desire-particles",
        "sub_goal": "SG-7",
        "sentences": [
          { "ar": "أبغى قهوة", "tr": "abgha gahwa", "en": "I want coffee" },
          { "ar": "وش تبغى؟", "tr": "wesh tabgha?", "en": "What do you want?" }
        ],
        "audio": {
          "word": "audio/abgha.mp3",
          "ex1": "audio/abgha_ex1.mp3",
          "ex2": "audio/abgha_ex2.mp3"
        }
      }
    ]
  }
  ```
- `audio/` — MP3s generated in step 7
- `<plan-slug>_training_plan.md` — the plan file (step 8)

## Step 7: Generate audio

Run the bundled script once:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/scripts/generate_audio.py \
    --manifest <plan-folder>/words.json \
    --out <plan-folder>/audio
```

Every word gets `<slug>.mp3`; every example sentence gets `<slug>_ex1.mp3` / `<slug>_ex2.mp3`. If the sandbox blocks `translate.google.com`, the script drops `regen_audio.bat` / `regen_audio.sh` / `regen_audio.py` next to the manifest — tell the user the one-click recovery path for their OS.

**Caveat for Najdi:** gTTS has no native Najdi voice; the audio approximates MSA. Mention this to the learner and link Forvo in the plan file for dialect-critical words.

## Step 8: Write the plan file

Use Write to create `<plan-slug>_training_plan.md`. Exact layout:

```markdown
# Arabic Training Plan: <Title>
Generated: <YYYY-MM-DD> | Variety: <najdi|msa> | Theme: <theme> | Words: <N>
Status: in-progress | Audio dir: audio/

## Learning Goal
<user's original input>

## SMART Goal
<≤20 words — variety, theme, count, implied verification>

## Motivation
<one short paragraph — why this deck, for this learner, now>

## Core Principles

| # | Principle | Statement | Example | Prerequisites |
|---|-----------|-----------|---------|---------------|
| P1 | <name> | <sentence> | <Arabic + gloss> | <prior knowledge> |
| ... | ... | ... | ... | ... |

## Word List (Key Facts)

| # | Arabic | Translit | English | POS | Principle | Sub-Goal | Audio |
|---|--------|----------|---------|-----|-----------|----------|-------|
| 1 | أبغى | abgha | I want | verb | P3 | SG-7 | audio/abgha.mp3 |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Sub-Goals

| # | Axis | Sub-Goal | Difficulty | Principle | Status | Mastery | Last Tested | Next Due |
|---|------|----------|-----------|-----------|--------|---------|-------------|----------|
| SG-1 | Motivation | State why I'm learning <variety> for <theme> | low | — | pending | 0/5 | — | — |
| SG-2 | Core Principle | Apply <P1 name> in simple sentences | low | P1 | pending | 0/5 | — | — |
| ... | Core Principle | ... | low | ... | pending | 0/5 | — | — |
| SG-K | Key Fact | Master words [<slug1>, <slug2>, ...] (group 1) | low | <linked P> | pending | 0/5 | — | — |
| ... | Key Fact | ... | ... | ... | ... | 0/5 | — | — |

## Sequence
Motivation first → Core Principles in dependency order → Key Fact groups in word-frequency order.

## Session Blueprints

### SG-1: Motivation
- **Initial Test:** Ask the learner to name ONE concrete situation where they'll use this vocabulary in the next 30 days, and what success would look like.
- **Pass Criteria:** Learner names a concrete situation AND a measurable success signal.
- **Estimated Depth:** introductory
- **Principle:** —
- **Teach Topics:** Refining vague motivations into measurable targets; cost of vague goals.
- **Final Test:** Same question, new angle: "If you only learned 5 of these words, which 5 and why?"

### SG-2: Core Principle — <P1 name>
- **Principle:** <P1 name> — <statement>
- **Worked Example (foundational):**
  **Given:** <simplest example, 1 sentence>
  **Step 1:** <identify the principle's marker>
  > **Why:** <reasoning>
  **Step 2:** <produce/transform using it>
  > **Why:** <reasoning>
  **Result:** <target sentence>
- **Initial Test:** Present 3 short Arabic sentences (some following P1, some violating it). Ask: which ones obey the principle? Fix the violators.
- **Pass Criteria:** Identifies ≥2/3 correctly AND can re-state the principle in own words.
- **Estimated Depth:** introductory
- **Teach Topics:** The principle; its boundary; one contrastive counter-example from the other variety.
- **Final Test:** Different set of 3 sentences testing the same principle.

(repeat for every Core Principle sub-goal)

### SG-K: Key Fact — Group <g> (<pos or slice label>)
- **Words in scope:** <slug1>, <slug2>, <slug3>, <slug4>, <slug5>  (list the slugs in this group)
- **Initial Test:** 5 mixed prompts, one per word:
  1. [audio → meaning]  Play `audio/<slug1>.mp3` — what does it mean?
  2. [English → Arabic production]  How do you say "<english gloss of word 2>"? (Arabic + transliteration)
  3. [fill-in-the-blank]  "<example sentence with ___ blanked>" — fill in `<word 3>`.
  4. [audio → transliteration]  Play `audio/<slug4>.mp3` — write the transliteration.
  5. [English → Arabic in a sentence]  Translate: "<English sentence using word 5>".
- **Pass Criteria:** ≥4/5 correct, AND transliteration close enough to be unambiguous.
- **Estimated Depth:** introductory
- **Principle:** <linked P>
- **Teach Topics:** For each missed word: card data (Arabic, transliteration, English, two example sentences with glosses, audio filename). For persistent confusion across words, contrast them.
- **Final Test:** Same 5 words, NEW prompt set — rotate the five prompt types so no word is tested the same way twice in a row.

(repeat for every Key-Fact group)

## Progress Log
(updated by /run-arabic-session and /arabic-retention-check)

## Retention Schedule
See `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/retention.md`. Intervals per mastery level:
- Level 0 → test now
- Level 1 → +1 day
- Level 2 → +3 days
- Level 3 → +7 days
- Level 4 → +21 days
- Level 5 → +60 days (mastered)

A Key-Fact sub-goal is **mastered** only when it reaches Mastery 5. First Final-Test pass sets Mastery 2. Each retention pass advances the level; each fail drops it by 1 (min 0).
```

## Step 9: Hand off

Show the learner:
- The SMART goal
- The core-principles table
- The word-list table (first ~10 rows if long)
- The sub-goal table
- The audio folder path and a sample filename
- The command to start: `/run-arabic-session SG-1`
- A note that `/arabic-retention-check` should be run periodically (suggest: after finishing the first 3 Key-Fact sub-goals, and then every few days)

Do NOT open an HTML viewer. Do NOT produce `deck.html`, `anki.csv`, or any card-flipping artefact — this plugin is deliberately interactive-session-only.

## Important

- Key Facts = vocabulary batches (5–8 words), NOT individual words as sub-goals (that would create too many SGs)
- Every Key-Fact sub-goal must list the `slug`s of the words it covers so `/run-arabic-session` can find them in `words.json`
- Audio filenames must match `words.json` entries exactly
- Never inline teaching content into the plan file EXCEPT the Core-Principle worked examples (which are explicitly allowed and required)
- The plan file is the single source of truth — `/run-arabic-session` and `/arabic-retention-check` read and edit it
