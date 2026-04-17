---
name: saudi-flashcard
description: Generate a batch of 20 Najdi Saudi Arabic flashcards plus a Test–Teach–Test training program. Use when the user asks for Saudi Arabic flashcards, a new vocabulary batch, a Najdi training session, or wants to extend the deck. Every invocation produces a fresh batch of 20 words that have not appeared before (tracked via used-words.json), plus a matching TTT training.
---

# saudi-flashcard

Produces **20 Najdi Saudi Arabic flashcards + a Test–Teach–Test training** per invocation.

## Hard rules

1. **Najdi only.** Use dialect forms (ق → `g`, ك → `ch` where applicable, Najdi lexicon: `wesh`, `abgha`, `ugub`, `gaa'id`, `widdi`, `hagg`, etc.). Do **not** use MSA when a Najdi form exists.
2. **No pan-Arabic basics as standalone cards.** `marhaba`, `as-salaam alaykum`, `na'am`, `la`, and similar first-week greetings are too basic to be cards — they may appear inside example sentences only.
3. **20 cards per batch, always.** Not 19, not 21.
4. **No repeats across batches.** Before choosing words, read `used-words.json` and exclude every transliteration already listed. After the batch is written, append the 20 new transliterations to `used-words.json`.
5. **Pronunciation is mandatory on every card.** Each card must carry both:
   - a working **Forvo link** (`https://forvo.com/word/<arabic>/#ar`), and
   - an `audio/<transliteration>.mp4` slot (the file itself is user-supplied and gitignored).
6. **Transliteration scheme** matches the project README. Long vowels doubled (`aa`, `ii`, `uu`); Najdi ق → `g`; `sh`, `th`, `dh`, `kh`, `gh` digraphs; `'` for ع and ء.
7. **Audio filenames** use the transliteration with no spaces. If a transliteration contains a hyphen (e.g. `al-heen`) or apostrophe (e.g. `gaa'id`), keep hyphens but replace apostrophes with hyphens in the filename (`gaa-id.mp4`).

## Inputs

- The project root (flashcards live in `cards/`, manifest is `cards.json`, training goes in `training/batch-NN/`).
- `used-words.json` — the exclusion list. Create it if missing.
- Optional user hint (e.g. "focus on kitchen verbs", "prioritize question words this batch").

## Output per invocation

For batch N (determined by `max(existing batch-NN) + 1`, starting at 1):

```
cards/            NN-<slug>.md × 20, numbered continuing from the last batch
cards.json        append the 20 new entries under "cards", bump meta.batch_id and meta.count
used-words.json   append the 20 new transliterations
index.md          regenerate the table to include the new rows
training/batch-NN/
  pre-test.md     20 prompts covering all 20 new words (no answers visible)
  teach.md        a short read-through pointing to each of the 20 cards, grouped by category
  post-test.md    20 mixed prompts (translate EN→AR, AR→EN, fill-in-blank, listen-via-Forvo)
  answer-key.md   answers for pre-test and post-test
```

## Card template (exact)

Each `cards/NN-<slug>.md`:

```markdown
# NN. <arabic> (<translit>) — "<english>"

| Field | Value |
|---|---|
| Arabic | <arabic> |
| Transliteration | <translit> |
| English | <english> |
| Forvo | [<arabic>](<forvo_url>) |
| Local audio | [<audio_filename>](../audio/<audio_filename>) |

## Example 1
**Arabic:** <sentence>
**Transliteration:** <sentence_translit>
**English:** <sentence_en>

| Arabic | Transliteration | English |
|---|---|---|
| <w> | <w_translit> | <w_en> |
...

## Example 2
(same shape)

---
[← Index](../index.md) | [Prev](prev.md) | [Next](next.md)
```

On the first card of the project, omit Prev; on the last, omit Next.

## TTT training structure

Test–Teach–Test. When the user's `create-training-plan` plugin (to be published at github.com/antonio-ardigo/...) is available, **replace the body of `training/batch-NN/` by delegating to that plugin** with the 20-word list as input. Until then, use the inline scaffold below.

### pre-test.md (inline scaffold)

- 20 numbered prompts, one per new word.
- Mix of: (a) English → give me the Najdi word, (b) fill in the blank in a Najdi sentence, (c) listen via the Forvo link and write what you hear.
- No answers in this file. Learner self-scores using `answer-key.md`.

### teach.md (inline scaffold)

- One paragraph of dialect framing (what makes this batch Najdi).
- Grouped list of the 20 cards by category (question words / discourse markers / verbs / nouns / particles), each linking to its `cards/NN-<slug>.md`.
- A "watch for" note flagging any words that inflect (e.g. `tawwuh` → `tawwni`, `tawwak`).

### post-test.md (inline scaffold)

- 20 prompts again, but **different prompts than pre-test** and in **different order**.
- Include at least 5 EN→AR production prompts, 5 AR→EN comprehension prompts, 5 fill-in-blank, 5 Forvo-listening.
- No answers in this file.

### answer-key.md

- Pre-test answers, then post-test answers. Each answer cites the card file so the learner can jump back.

## Word-selection heuristic

Pick 20 Najdi words that are:
- **high-frequency in daily speech** (not register-specific), AND
- **dialect-marked** (ق→g, Najdi-only vocabulary, Najdi particles), OR **structural workhorses** (discourse markers, common verbs, tense/aspect particles, question words, possessives), AND
- **not in `used-words.json`**.

Good second-batch candidates (illustrative, not mandatory): `khoy`, `ajeeb`, `jeeb`, `ashoof`, `ta'aal`, `wain`, `meta`, `minu`, `kam`, `shway`, `bas`, `ba'ad`, `gabl`, `yoom`, `baakir`, `ams`, `wihda`, `ithnain`, `halg`, `ma'aay`.

Avoid: `marhaba`, `salaam`, `na'am`, `la`, `shukran`, `afwan`, `min fadlak` — these are too basic for cards but can appear in sentences.

## Execution checklist

Before writing anything, run through this:

- [ ] Read `used-words.json`; pick 20 new words not in it.
- [ ] Confirm each word is Najdi-appropriate (not MSA-only).
- [ ] Draft all 20 with Arabic, translit, English, Forvo URL, audio filename, 2 sentences × word-by-word.
- [ ] Write `cards/NN-<slug>.md` × 20 using the exact template.
- [ ] Append to `cards.json` under `"cards"`; bump `meta.batch_id` and `meta.count`.
- [ ] Append the 20 transliterations to `used-words.json`.
- [ ] Regenerate `index.md`.
- [ ] Write `training/batch-NN/{pre-test,teach,post-test,answer-key}.md`.
- [ ] Verify: all 20 cards have working Forvo links (real Arabic script in URL), all 20 reference an `audio/<translit>.mp4` path, Prev/Next navigation is wired.
- [ ] Commit with a message naming the batch and word count.

## Non-goals

- Do NOT generate `.mp4` files — they are produced outside this workflow (native speaker + slide with highlighted-on-speak target word). The skill only writes the path reference.
- Do NOT use TTS for Arabic audio — available TTS voices are MSA and would defeat the Najdi-only rule.
- Do NOT invent transliterations for words whose Najdi form you are unsure of; pick a different word.
