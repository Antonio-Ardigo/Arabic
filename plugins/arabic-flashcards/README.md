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

If no TTS provider is reachable, the script writes silent placeholder MP3s so the rest of the build still succeeds; re-run audio generation once you have network access.

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
│           └── generate_audio.py         # TTS runner (gTTS default, ElevenLabs optional)
└── README.md
```

## Credits

Card format and selection philosophy adapted from the Najdi flashcard repository by Antonio Ardigò. MSA support and the three-format output are new additions in this plugin.
