---
description: Build a thematic Arabic flashcard deck (Najdi or MSA) with two example sentences and audio per card
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "[theme] [najdi|msa] [size]"
---

# /create-deck — Arabic Flashcard Deck Builder

You are building a thematic Arabic flashcard deck for the user. Load and follow the `arabic-flashcard-authoring` skill before doing anything else — it contains the card template, transliteration rules, sentence-quality rules, and the audio-generation workflow.

## Step 1: Load the authoring skill

Read `${CLAUDE_PLUGIN_ROOT}/skills/arabic-flashcard-authoring/SKILL.md` in full. Also read any of its `references/*.md` files relevant to the user's request (at minimum: `card-templates.md`, `transliteration.md`, and `tts-setup.md`).

## Step 2: Collect deck parameters

The command argument is `$ARGUMENTS`. Parse it into these fields (any order, any missing):
- **theme** — e.g. "business", "travel", "coffee shop", "family", "airport", "WhatsApp chat", "negotiation"
- **variety** — `najdi` (Najdi Saudi dialect, like the source repo) OR `msa` (Modern Standard Arabic, فصحى)
- **size** — integer number of cards; default to **10** if not given

If ANY of theme or variety is missing, use AskUserQuestion to ask ONE consolidated question. Do not ask again if the user already provided them. If the user wrote a freeform theme like "business MSA arabic", infer `theme=business` and `variety=msa` without re-asking.

## Step 3: Plan the word list

Generate a list of `size` high-frequency **thematic** head-entries for the deck:
- For Najdi decks: prefer words that MARK the Najdi dialect or are structural workhorses (follow the selection philosophy in `references/card-templates.md`). Avoid pan-Arabic basics the learner would already know.
- For MSA decks: prefer words a learner would actually hear/read in the chosen theme (e.g. a "business MSA" deck leans on words like اجتماع, عقد, عرض, ميزانية, اقتراح).
- Mix parts of speech (nouns, verbs, common adjectives/particles) unless the theme is strongly noun-heavy.
- Do NOT duplicate entries that already exist in a passed-in existing deck (if the user pointed at one).

Show the user the proposed word list as a short table (Arabic · transliteration · English gloss) and ask for approval or edits before you generate full cards. One round of edits is enough — don't over-ask.

## Step 4: Generate each card

Follow the **exact card template** in `references/card-templates.md`. For every head-entry produce:
- Arabic script (fully vocalised where it aids learners)
- Transliteration per the active scheme for the chosen variety
- English definition (one short line)
- Exactly **TWO** short, natural example sentences. Rules:
  - ≤ 8 words each
  - Everyday register matching the theme
  - For Najdi: use dialectal grammar and vocabulary (e.g. `widdi`, `abgha`, negation with `ma`, `gaa'id + verb`). Do NOT write MSA sentences and label them Najdi.
  - For MSA: use full case marking only where unambiguous; otherwise keep it readable.
- Word-by-word gloss under each sentence.
- Placeholder paths for the three audio files: `audio/<slug>.mp3` (headword), `audio/<slug>_ex1.mp3`, `audio/<slug>_ex2.mp3`.

Write each card as `cards/<slug>.md` using the template.

## Step 5: Generate audio

Run the bundled script to synthesise MP3s for every sentence and headword:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/arabic-flashcard-authoring/scripts/generate_audio.py \
    --manifest <deck-folder>/cards.json \
    --out <deck-folder>/audio \
    --variety <najdi|msa>
```

The script uses Google TTS (`gTTS`) by default (free, no key). If the env var `ELEVENLABS_API_KEY` is set and `--provider elevenlabs` is passed, it uses ElevenLabs for higher-quality audio. See `references/tts-setup.md` for install/setup. If `gTTS` isn't installed, install it with `pip install gTTS --break-system-packages` before running.

**Sandbox fallback (v0.3.0).** If the environment blocks `translate.google.com` (common in Claude sandboxes with allowlists), `generate_audio.py` no longer writes silent placeholder MP3s. Instead it cleans up any 0-byte remnants and drops three one-click recovery scripts next to the manifest: `regen_audio.bat` (Windows), `regen_audio.sh` (macOS/Linux), and `regen_audio.py` (any OS). Tell the user the simple path for their machine — e.g. for Windows: "Audio was skipped because the sandbox blocks Google. Double-click `regen_audio.bat` in the deck folder — it installs gTTS and populates all MP3s in about a minute."

**Caveat to state to the user:** there is no native Najdi TTS voice — for Najdi decks the generated audio will approximate MSA pronunciation. Include Forvo links on each card for native Najdi pronunciation when available.

## Step 6: Build the three output formats

From the card files and `cards.json` manifest, produce three outputs. Starting in v0.2.0 the HTML and Anki outputs have **bundled builder scripts** — don't hand-roll them:

1. **Markdown + JSON deck** (matches the reference GitHub repo):
   - `cards/<slug>.md` (one per card — already written in step 4)
   - `cards.json` (machine-readable manifest with arabic, translit, english, sentences, audio paths)
   - `index.md` (table linking every card)
   - `audio/*.mp3` (from step 5)

2. **Single-file HTML deck** (`deck.html`) — use the bundled builder:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/arabic-flashcard-authoring/scripts/build_deck_html.py \
       --manifest <deck-folder>/cards.json
   ```
   Produces a self-contained flip-card viewer with RTL layout, keyboard nav (← → space, S=shuffle), card counter, and inline CSS/JS — no external dependencies.

3. **Anki import file** (`anki.csv`) — use the bundled builder:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/arabic-flashcard-authoring/scripts/build_anki.py \
       --manifest <deck-folder>/cards.json
   ```
   Produces an Anki 2.1+ tab-separated file with proper `#separator:tab`, `#html:false`, `#columns:…` metadata headers and 10 columns (Arabic, Transliteration, English, Sentence1/2 AR+EN, three `[sound:…]` tags). Instruct the user to copy `audio/*.mp3` into their Anki `collection.media` folder after importing.

All files must be written under the workspace outputs folder in a sub-directory named `arabic-<variety>-<theme-slug>-<YYYYMMDD>/`.

## Step 7: Share with the user

Present (via `mcp__cowork__present_files`) at least:
- `deck.html` (primary viewing experience)
- `anki.csv`
- `index.md`
- A sample card like `cards/<first-slug>.md`

Keep the final chat message short: state the theme, variety, card count, audio provider used, and any caveats (e.g. "Najdi audio approximates MSA pronunciation").
