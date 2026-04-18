# TTS Setup

Two audio providers are supported. Pick one per deck.

## Provider 1: gTTS (default, free, no key)

`gTTS` wraps Google Translate's text-to-speech. Free, no API key, reasonable MSA-style Arabic voice. This is the default used by `scripts/generate_audio.py`.

### Install

```bash
pip install gTTS --break-system-packages
```

### Run

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/arabic-flashcard-authoring/scripts/generate_audio.py \
    --manifest <deck-folder>/cards.json \
    --out <deck-folder>/audio \
    --variety najdi
```

### Limitations

- Only produces one Arabic voice (MSA-flavoured). There is no native Najdi TTS voice in gTTS.
- For Najdi decks, the audio pronunciation will sound MSA — mention this to the user and include Forvo links on every card for native Najdi pronunciation.
- Requires network access at generation time; not suitable for fully offline decks.

## Provider 2: ElevenLabs (paid, higher quality)

ElevenLabs supports multilingual voices and produces more natural-sounding Arabic than gTTS. Still MSA-leaning but notably more human.

### Setup

1. Create an ElevenLabs account and get an API key.
2. Export the key:
   ```bash
   export ELEVENLABS_API_KEY="sk-..."
   ```
3. Install the client:
   ```bash
   pip install elevenlabs --break-system-packages
   ```

### Run

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/arabic-flashcard-authoring/scripts/generate_audio.py \
    --manifest <deck-folder>/cards.json \
    --out <deck-folder>/audio \
    --variety msa \
    --provider elevenlabs \
    --voice "Rachel"
```

### Notes

- `--voice` defaults to `Rachel` (a default ElevenLabs multilingual voice). Any voice ID or voice name from the user's account works.
- ElevenLabs charges per character. A 10-card deck with 2 sentences each is roughly 2–3 thousand characters including headwords — well inside the free tier at time of writing.
- Never commit the API key to the generated deck. The script reads it from the environment only.

## Offline fallback

If neither provider is available (no network, no key), the script falls back to writing silent 200-ms placeholder MP3s so the HTML/Anki builds still succeed. The user can re-run audio generation later with the same manifest.

## Verifying output

After generation the script prints:

```
[audio] <slug>.mp3        (headword)
[audio] <slug>_ex1.mp3
[audio] <slug>_ex2.mp3
...
✓ 30 files written to <out-dir>
```

Confirm the file count matches `(cards × 3)`. Any mismatch means a TTS call failed; re-run with `--verbose` to see the failing string.
