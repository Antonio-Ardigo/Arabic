---
description: Run an interactive Test-Teach-Test session for one sub-goal of an Arabic training plan. Uses audio filenames and production/recognition prompts — no flashcards.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: "SG-<N>"
---

# /run-arabic-session — Interactive TTT for Arabic

You are running ONE interactive Test-Teach-Test session for a sub-goal of an Arabic training plan. No flashcard UI. No HTML deck. Everything happens in this conversation; audio is referenced by filename so the learner can click/open the MP3 themselves.

Load `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/SKILL.md` before anything else, plus `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/test-formats.md` (prompt templates) and `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/retention.md` (mastery advancement rules).

## Step 0: Find the plan

Glob for `*_training_plan.md` in the current directory. Read it. Also read the sibling `words.json` (same folder). If neither exists, tell the learner to run `/create-arabic-training` first and stop.

## Step 1: Identify the target sub-goal

From `$ARGUMENTS`:
- `SG-<N>` or `<N>` → that sub-goal
- a slug or keyword → match the closest sub-goal by its slug list
- nothing → show the sub-goal table and ask which to run

If the sub-goal is already `mastered` (Mastery 5/5), ask whether they really want to re-test. Treat as a retention check if they say yes.

## Step 1.5: Checkpoint

Glob for `<plan-slug>_checkpoint_SG<N>.md`. If present, summarise the phase reached and offer to resume. If they decline, delete the checkpoint and start fresh.

## Step 2: Run the TTT protocol

### Phase 1 — INITIAL TEST

Branch by sub-goal axis (from the plan table).

**Motivation SG:**
Present the Initial Test from the blueprint verbatim (name a concrete situation and a success signal). Append the two mandatory notes:
> *If you are not familiar with this topic, write **"not familiar"** to receive a full explanation before attempting the test.*
>
> *If any term is unclear, ask for a **clarification** — I will explain the term without helping you solve the problem.*

**Core Principle SG:**
Present the 3-sentence identification task from the blueprint. Include the example sentences with:
- Arabic script
- Transliteration
- English translation
- Audio reference: `[▶ play]` followed by the filename, e.g. `[▶ play] audio/abgha_ex1.mp3` — the learner can click the filename if their viewer supports it, or open it manually. Never embed raw HTML.

Append the two mandatory notes.

**Key Fact SG:** build the 5 prompts dynamically. Read the words in this SG from `words.json` (the slugs listed in the blueprint's "Words in scope"). For each word, roll ONE prompt type from `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/test-formats.md`:

| Type | Template |
|------|----------|
| A | **Audio → meaning** — "Play `audio/<slug>.mp3`. What does it mean in English?" |
| B | **English → Arabic production** — "Write the Arabic word for '<english>'. Give Arabic script + transliteration." |
| C | **Fill-in-the-blank** — Pick example 1 or 2 for the word; blank the headword; ask the learner to fill in. Show transliteration and English of the sentence with the same blank. |
| D | **Audio → transliteration** — "Play `audio/<slug>.mp3`. Write the transliteration." |
| E | **Translate the sentence** — Give the English of an example sentence; ask for the full Arabic sentence (with the target word). |

Rules for the 5-prompt set:
- Use all 5 types if the SG has ≥5 words; if fewer, repeat types but never test the same word twice with the same type
- Every prompt that references audio MUST show the filename exactly as it appears in `words.json.audio.*` — no guessing, no path rewriting
- Number the prompts 1–5

End with the two mandatory notes.

**"not familiar" handling:** deliver a concise concept explanation for the SG's principle (Core Principle SG) or a quick primer on the 5 words (Key Fact SG — show each as: Arabic · translit · English · one example · audio filename), then re-present the test. Don't count this as a loop.

**Clarification handling:** if the learner asks about a term, explain the term without leaking the target answer. For a vocabulary word currently being tested, do NOT translate it — explain the grammatical role only.

**Checkpoint:** write `<plan-slug>_checkpoint_SG<N>.md` with the test presented and the learner's response. Set `## Current Phase: EVALUATE`.

### Phase 2 — EVALUATE

Score each prompt against its expected answer:

- Transliteration: accept any unambiguous variant (e.g. `shlonak` / `šlōnak` / `shloonak`). Penalise only if the letters don't clearly map.
- Arabic production: accept missing short-vowel diacritics. Penalise wrong letters, wrong root, wrong form.
- Fill-in-the-blank: exact-match the target slug (diacritics optional).
- Meaning/translation: accept any answer that conveys the same core sense; flag nuance misses as partial.

Classify gaps per word using the failure mode taxonomy from `training-plan` conventions:
- `[sound-to-meaning]` — heard the word but couldn't recall the meaning
- `[meaning-to-form]` — knew the meaning but couldn't produce the Arabic
- `[grapheme-to-sound]` — read the Arabic but couldn't pronounce/transliterate
- `[usage]` — recognised the word but couldn't use it in a sentence
- `[conflation]` — confused with another word in the same group or with MSA/Najdi counterpart

Determine: **PASS**, **PARTIAL**, **FAIL**.
- Motivation/Core Principle: follow the blueprint's pass criteria literally.
- Key Fact: PASS = ≥4/5 correct; PARTIAL = 3/5 with gaps classifiable; FAIL = ≤2/5.

If PASS, skip to Phase 6.

Checkpoint update: record evaluation + classified gaps. Phase → TEACH (or RECORD if PASS).

### Phase 3 — TEACH

Deliver ONE targeted teaching block per gap. Keep each block tight — this is vocabulary, not theory.

**For a word-level gap [sound-to-meaning / meaning-to-form / grapheme-to-sound / usage]:**
Show exactly:
```
**<Arabic>** — <transliteration> — <english>
  Audio: audio/<slug>.mp3
  Example 1: <Arabic>  ·  <translit>  ·  <english>   (audio/<slug>_ex1.mp3)
  Example 2: <Arabic>  ·  <translit>  ·  <english>   (audio/<slug>_ex2.mp3)
  Memory hook: <one line — etymology, cognate, sound-shape, mnemonic>
```
Then ONE Quick Check: a new prompt using the same word but a DIFFERENT prompt type than the one it failed on. End with `*If any term is unclear, ask for a **clarification**.*`. Wait for the answer before evaluating.

**For a [conflation] gap between two words in the group:** use a comparison table:
| | Word A | Word B |
|---|--------|--------|
| Arabic | | |
| Translit | | |
| English | | |
| Typical frame | | |
| Distinguishing cue | | |

Quick Check: give one sentence containing ONE of the two; ask the learner which it is and why.

**For a Core Principle gap:** re-deliver the blueprint's worked example, then a new one at the same level. Quick Check = apply the principle to a fresh sentence.

Mention **once**, after the first block: "You can ask me to go deeper on any word or the governing principle." Do not repeat the offer.

If a Quick Check fails twice for the same word, note it as a persistent gap and move on. It will carry into the next retention check.

Checkpoint after each block. Phase → FINAL_TEST when all gaps are processed.

### Phase 4 — FINAL TEST

Build a NEW prompt set covering the SAME words (Key Fact) or the SAME principle (Core Principle). Rotate prompt types so no word is tested with the same type as in the Initial Test. For Core Principle, use a fresh set of sentences.

Append the two mandatory notes. Wait for the answer.

### Phase 5 — EVALUATE FINAL

- PASS → Phase 6.
- FAIL (first time) → identify persistent gaps, run ONE more Teach pass targeting only those words, then a third test (Loop 1). Max two loops.
- FAIL (second time) → record as `needs-review`. Tell the learner: the sub-goal will come back in the retention schedule sooner (Mastery stays 0).

### Phase 6 — RECORD

Do seven things:

**A) Update the plan file** via Edit:
- Sub-goal Status: `complete` (PASS) or `needs-review`
- Mastery column: set to **2** on first Final-Test PASS (Motivation / Core Principle SGs jump straight to 3 since they don't benefit from vocabulary spaced-recall in the same way; but Key Facts start at 2 and climb via retention)
- Last Tested: today's date (YYYY-MM-DD)
- Next Due: today + interval for the new mastery level (see `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/retention.md`)
- Append a Progress Log entry:

```markdown
### SG-<N> — <Completed/Needs Review> — <YYYY-MM-DD>
- Initial Test: <PASS/PARTIAL/FAIL> (<N>/5 correct — or Core Principle / Motivation detail)
- Gaps: <slug [tag], slug [tag], ...> or "none"
- Teach blocks: <N> delivered
- Final Test: <PASS/FAIL> (<N>/5)
- Loops: <0/1/2>
- Mastery: <old>/5 → <new>/5
- Next Due: <YYYY-MM-DD>
- Notes: <brief>
```

**B) Write a session transcript** to `<plan-slug>_session_SG<N>_<YYYY-MM-DD>.md` — full prompts, learner answers, evaluation, teaching blocks, final test, final evaluation.

**C) Delete the checkpoint file.**

**D) Update `learner_profile.md`** (create if absent) — add the session, update Gap Patterns with any `[tag]` that appeared, add Strengths if PASS with zero gaps.

**E) Update per-word stats** in `words.json`: for each word, bump its `stats.seen` and `stats.correct` counters (add the `stats` object if missing: `{ "seen": 0, "correct": 0, "last_result": null }`). This lets `/arabic-retention-check` weight word selection toward historically weak words.

**F) Report the plan's overall completion** — count sub-goals by status (pending / complete / mastered / needs-review), and the weighted-average mastery across Key-Fact SGs.

**G) Suggest the next step:**
- If there are still `pending` sub-goals in sequence → `/run-arabic-session SG-<next>`
- If all sub-goals are at least `complete` → remind the learner to run `/arabic-retention-check` to keep climbing toward Mastery 5/5

## Non-negotiable rules

- Every Initial Test and Final Test ends with the two mandatory notes (not-familiar + clarification)
- NEVER reveal expected answers before the learner responds
- NEVER open an HTML/flashcard viewer — this plugin is interactive-only
- Audio references use the exact filename from `words.json`; never invent a path
- One gap, one teach block; never batch
- Update `words.json` stats on every session — retention weighting depends on it
- Delete the checkpoint file only after the plan file and transcript are both written
