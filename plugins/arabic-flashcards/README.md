# arabic-flashcards

Build thematic Arabic flashcard decks — Najdi Saudi dialect or Modern Standard Arabic — with two short example sentences per card and text-to-speech MP3 audio.

Inspired by and designed to extend the [Najdi flashcard repository](https://github.com/Antonio-Ardigo/Arabic).

## What you get

Run `/create-deck` and the plugin produces a deck in three formats at once:

- **Markdown + JSON** — one `cards/<slug>.md` per entry plus a machine-readable `cards.json` manifest and an `index.md`. Same layout as the source repo.
- **Single-file HTML deck** — `deck.html`, an interactive flip-card viewer with RTL Arabic layout, keyboard nav, and shuffle.
- **Anki CSV** — `anki.csv`, tab-separated, ready to import into Anki with `[sound:...]` audio tags.

Every card has three MP3s: the headword, example sentence 1, example sentence 2.

## Usage

```
/create-deck business msa
/create-deck coffee-shop najdi 15
/create-deck airport msa
/create-deck "WhatsApp chat" najdi
```

Arguments (any order, all optional — the plugin asks for what's missing):

| Arg | Values | Default |
|-----|--------|---------|
| theme | any noun phrase | *required* |
| variety | `najdi` or `msa` | *required* |
| size | integer | `10` |

## How cards are structured

Every card follows a fixed template:

- Arabic script (vocalised where helpful)
- Transliteration (Najdi popular scheme or MSA DIN-31635-lite)
- One-line English definition
- Exactly two short example sentences (≤ 8 words each, in theme, with word-by-word gloss)
- Audio for the headword and both sentences
- Forvo link for native pronunciation

See `skills/arabic-flashcard-authoring/references/card-templates.md` for the full template.

## Audio

Two TTS providers are supported:

- **gTTS** (default) — free, no API key, MSA-flavoured Arabic voice. Install with `pip install gTTS --break-system-packages`.
- **ElevenLabs** — higher quality, multilingual voices. Set `ELEVENLABS_API_KEY` and pass `--provider elevenlabs`.

**Najdi caveat:** no native Najdi TTS voice exists in either provider. For Najdi decks the generated audio will approximate MSA pronunciation. Every card also links to Forvo so learners can hear native speakers.

If no TTS provider is reachable (e.g. a sandbox blocks `translate.google.com`), the script skips synthesis, removes any 0-byte remnants, and drops three one-click recovery scripts next to the deck:

- `regen_audio.bat` — Windows: double-click it. Checks Python, installs gTTS, synthesises all MP3s, opens `deck.html`.
- `regen_audio.sh` — macOS/Linux: `bash regen_audio.sh`. Same flow.
- `regen_audio.py` — any OS: `pip install gTTS && python regen_audio.py`.

## What's in the plugin

```
arabic-flashcards/
├── .claude-plugin/plugin.json
├── commands/
│   └── create-deck.md                    # the /create-deck command
├── skills/
│   └── arabic-flashcard-authoring/
│       ├── SKILL.md                      # authoring methodology
│       ├── references/
│       │   ├── card-templates.md         # markdown template + cards.json schema
│       │   ├── transliteration.md        # Najdi popular + MSA DIN-31635-lite
│       │   └── tts-setup.md              # gTTS & ElevenLabs setup
│       └── scripts/
│           ├── generate_audio.py         # TTS runner (gTTS default, ElevenLabs optional)
│           ├── build_deck_html.py        # emit self-contained flip-card HTML viewer
│           └── build_anki.py             # emit Anki 2.1+ tab-separated import file
└── README.md
```

## Changelog

### 0.3.0

- **One-click audio recovery.** When synthesis fails, `generate_audio.py` now drops three wrappers next to the deck instead of one: `regen_audio.bat` (Windows double-click), `regen_audio.sh` (macOS/Linux), and the existing `regen_audio.py`. Each Windows/Unix wrapper checks Python, installs gTTS, runs the regen, and opens `deck.html` — no more copy-pasting PowerShell snippets.
- Updated recovery message in `generate_audio.py` lists the three options explicitly so users pick the right one on their OS.

### 0.2.0

- **Audio fallback rewritten.** `generate_audio.py` no longer writes silent placeholder MP3s when synthesis fails. It now cleans up 0-byte remnants and writes a standalone `regen_audio.py` next to the deck so the user can re-run on an unrestricted network. Clear recovery message is printed.
- **New `build_deck_html.py`.** Self-contained flip-card HTML viewer (RTL Arabic, keyboard nav ← → space, shuffle, card counter). No external dependencies. Replaces hand-rolled HTML per deck.
- **New `build_anki.py`.** Anki 2.1+ tab-separated import file with proper `#separator:tab`, `#html:false`, `#columns:…` metadata headers and 10 fixed columns.
- `commands/create-deck.md` updated to reference the new builders instead of open-coded HTML/CSV generation.

### 0.1.0

- Initial release: `/create-deck` command, authoring skill with three reference files, `generate_audio.py` TTS runner.

## Credits

Card format and selection philosophy adapted from the Najdi flashcard repository by Antonio Ardigò. MSA support and the three-format output are new additions in this plugin.
