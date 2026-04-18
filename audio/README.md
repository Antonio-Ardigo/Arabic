# Audio — Pronunciation Slides

This folder holds the `.mp4` pronunciation slides referenced by each flashcard. **The mp4 files are not committed** (see root `.gitignore`). You supply them.

## Filename convention

`<transliteration>.mp4` — matching the `audio_filename` field in [`../cards.json`](../cards.json).

Example: card 5 (`abgha`) expects `abgha.mp4`.

## Content specification

Each mp4 is a slide (static background is fine) showing:

1. The target word in Arabic + transliteration + English, at the top.
2. Both example sentences from the card, rendered in Arabic and transliteration.
3. A native Najdi speaker pronouncing:
   - the word in isolation, then
   - each example sentence at natural speed.
4. **While the target word is being spoken inside each sentence, it must be visually highlighted** (color change, box, underline — pick one and use it consistently across all 20 files).

## Production suggestions

- Keynote / PowerPoint → export to mp4, with a timed build that highlights the target word on the syllable it's spoken.
- [Remotion](https://www.remotion.dev/) (React-based programmatic video) if you want to generate all 20 from `cards.json`.
- [ffmpeg](https://ffmpeg.org/) + drawtext filter for a scripted pipeline.
- Whichever route you use, the audio should be a **real Najdi speaker**, not MSA TTS.

## Interim: Forvo links

Until you produce the mp4 files, each card's **Forvo** link covers the "pronunciation is mandatory" requirement with real native audio. Forvo does not cover every word in Najdi; if a word is missing there, see YouGlish (https://youglish.com/arabic) as a fallback.

## Verifying what's missing

```sh
jq -r '.[].audio_filename' ../cards.json | while read f; do
  [ -f "$f" ] || echo "MISSING: $f"
done
```
