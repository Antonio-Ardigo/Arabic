---
name: arabic-flashcard-authoring
description: Authoring methodology for Arabic flashcard decks — Najdi Saudi or Modern Standard Arabic — with strict card format, two short example sentences per card, transliteration conventions, and TTS audio generation. Load this when creating, editing, or extending an Arabic flashcard deck, when the user asks for a thematic deck (e.g. "business MSA arabic", "Najdi daily words", "travel Arabic"), when the user references their Najdi Saudi flashcard repository, or when building cards that follow the two-sentences-plus-audio pattern.
---

# Arabic Flashcard Authoring

Build Arabic flashcard decks that follow a consistent, audited template so every card is drillable, pronounceable, and dialect-accurate.

## When to apply this skill

- User asks for an Arabic flashcard deck, vocabulary list, or study set in Najdi or MSA.
- User requests a thematic set (`business`, `travel`, `coffee shop`, `office`, `WhatsApp chat`, `negotiation`, etc.).
- User references the source repository at `https://github.com/Antonio-Ardigo/Arabic` or wants to extend it.
- User asks to add one more card to an existing deck.
- The `/create-deck` command is invoked.

## Core principles

**One entry, one concept.** Each card teaches one headword. No synonym dumps, no multi-sense entries — split them into separate cards.

**Two sentences, no more.** Every card contains exactly **two example sentences**. Each sentence must be **short (≤ 8 words)**, natural, and in-theme. No drill sentences, no textbook clichés. If a sentence would need more than 8 words, rewrite it.

**Dialect fidelity.** Najdi means Najdi — dialectal grammar (`ma` negation, `gaa'id + imperfect`, `widdi`, `abgha`, `hagg`, elision of `-a` feminine endings in many positions) and dialectal vocabulary. MSA means فصحى — standard syntax, no dialect particles. Never mix.

**Theme-biased selection.** Don't produce pan-Arabic beginner lists. Pick words that actually appear in the requested domain. A "business MSA" deck should lean on real corporate vocabulary (`اجتماع`, `عقد`, `ميزانية`, `عرض`, `مقترح`, `تسليم`, `مهلة`), not greetings.

**Every sentence is audible.** Every example and every headword gets a MP3. Cards without audio paths are incomplete.

## Reference files

Load the reference file that matches the sub-task:

- **`references/card-templates.md`** — Exact markdown template for a card, JSON manifest schema, slug rules, selection philosophy for Najdi vs MSA.
- **`references/transliteration.md`** — Two transliteration schemes (Najdi popular / MSA DIN-31635-lite), letter table, which scheme to use when.
- **`references/tts-setup.md`** — How to install and invoke the audio generation script, supported providers (gTTS default, ElevenLabs optional), known limitations for Najdi.

## Bundled scripts

All scripts live in `scripts/` and are invokable with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/arabic-flashcard-authoring/scripts/<name>.py`:

- **`generate_audio.py`** — synthesises MP3s from `cards.json` via gTTS (default) or ElevenLabs. From v0.2.0 it no longer writes silent placeholder MP3s on failure; it removes 0-byte remnants and drops self-contained recovery scripts next to the manifest. From v0.3.0 it emits three wrappers for one-click recovery: `regen_audio.bat` (Windows double-click), `regen_audio.sh` (macOS/Linux), and `regen_audio.py` (any OS). Each Windows/Unix wrapper checks Python, installs gTTS, runs the regen, and opens `deck.html`.
- **`build_deck_html.py`** — emits a self-contained flip-card `deck.html` (RTL Arabic, keyboard nav, shuffle) from `cards.json`. No external dependencies.
- **`build_anki.py`** — emits an Anki 2.1+ `anki.csv` with `#separator:tab`, `#html:false`, `#columns:…` headers and 10 columns (Arabic, Translit, English, Sentence1/2 AR+EN, three `[sound:…]` tags).

## Workflow for building a deck

1. **Clarify variety and theme** — `najdi | msa` and a concrete theme string. Default deck size is **10** cards.
2. **Plan the word list** — produce a table of candidate headwords; get user sign-off once.
3. **Write each card** — headword, transliteration, English gloss, two in-theme sentences with word-by-word glosses, audio path placeholders. Use the template from `references/card-templates.md` verbatim.
4. **Emit the JSON manifest** — `cards.json` with every card's data in machine-readable form (used by the HTML deck and audio script).
5. **Generate audio** — run `scripts/generate_audio.py` against the manifest; confirms every MP3 path exists.
6. **Emit the three outputs** — markdown cards + index, single-file HTML deck, Anki TSV.
7. **Share with the user** — present the HTML deck and a sample card; flag any audio caveats (Najdi TTS limitation).

## Sentence-quality checklist

Before you accept a card, verify each sentence against this list:

- [ ] ≤ 8 words
- [ ] Natural in the target register (conversational for Najdi, domain-appropriate for MSA)
- [ ] Uses the headword in a meaningful position, not parroted
- [ ] Contains at most one new difficult word beyond the headword
- [ ] Has a word-by-word gloss in English
- [ ] Has a full English translation
- [ ] Has an audio path placeholder that the TTS script can fill

Reject and rewrite any sentence that fails a box.

## Common mistakes to avoid

- Writing MSA sentences and labelling them Najdi (very common — verify negation, aspect particles, and vocabulary).
- Using non-thematic sentences on thematic decks ("The cat is on the table" in a business deck).
- Over-long sentences packed with multiple new words.
- Skipping diacritics on headwords where a learner actually needs them.
- Producing duplicate or near-duplicate headwords.
- Forgetting to regenerate audio after editing a sentence.
