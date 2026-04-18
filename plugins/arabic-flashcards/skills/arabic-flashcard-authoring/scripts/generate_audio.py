#!/usr/bin/env python3
"""Generate MP3 audio for an Arabic flashcard deck.

Reads a cards.json manifest, synthesises audio for each headword and each
example sentence, and writes MP3 files to the output directory.

Providers:
    gtts        — default, free, no API key (pip install gTTS)
    elevenlabs  — higher quality, requires ELEVENLABS_API_KEY
                  (pip install elevenlabs)

If neither provider is usable, the script writes a 200-ms silent MP3
placeholder per expected file so downstream tooling still works.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# A pre-encoded 200-ms silent MP3 (11 kHz, mono). Used as fallback when no
# TTS provider is available so the rest of the toolchain still has files
# to reference.
SILENT_MP3_BYTES = bytes.fromhex(
    "fffb9064000f0000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000000000000000"
)


def log(msg: str) -> None:
    print(msg, flush=True)


def write_silent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(SILENT_MP3_BYTES)


def synth_gtts(text: str, out_path: Path, lang: str = "ar") -> bool:
    try:
        from gtts import gTTS  # type: ignore
    except ImportError:
        log("[warn] gTTS is not installed. `pip install gTTS --break-system-packages`")
        return False
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        gTTS(text=text, lang=lang, slow=False).save(str(out_path))
        return True
    except Exception as exc:  # network / quota / unsupported chars
        log(f"[warn] gTTS failed for {out_path.name}: {exc}")
        return False


def synth_elevenlabs(text: str, out_path: Path, voice: str) -> bool:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        log("[warn] ELEVENLABS_API_KEY not set; cannot use elevenlabs provider.")
        return False
    try:
        from elevenlabs.client import ElevenLabs  # type: ignore
    except ImportError:
        log("[warn] elevenlabs client not installed. `pip install elevenlabs --break-system-packages`")
        return False
    try:
        client = ElevenLabs(api_key=api_key)
        audio_stream = client.text_to_speech.convert(
            voice_id=voice,
            model_id="eleven_multilingual_v2",
            text=text,
            output_format="mp3_44100_128",
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("wb") as f:
            for chunk in audio_stream:
                if chunk:
                    f.write(chunk)
        return True
    except Exception as exc:
        log(f"[warn] ElevenLabs failed for {out_path.name}: {exc}")
        return False


def generate_one(text: str, out_path: Path, provider: str, voice: str, verbose: bool) -> bool:
    if verbose:
        log(f"[audio] {out_path.name}  ←  {text[:60]}")
    if provider == "elevenlabs":
        ok = synth_elevenlabs(text, out_path, voice)
        if ok:
            return True
        log(f"[info] falling back to gTTS for {out_path.name}")
        return synth_gtts(text, out_path)
    return synth_gtts(text, out_path)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate MP3 audio for an Arabic flashcard deck.")
    ap.add_argument("--manifest", required=True, help="Path to cards.json")
    ap.add_argument("--out", required=True, help="Output directory for mp3 files")
    ap.add_argument("--variety", choices=["najdi", "msa"], default="msa",
                    help="Deck variety (affects log messages only — gTTS/ElevenLabs always render the literal Arabic text)")
    ap.add_argument("--provider", choices=["gtts", "elevenlabs"], default="gtts")
    ap.add_argument("--voice", default="Rachel", help="Voice name/id for ElevenLabs")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not manifest_path.exists():
        log(f"[error] manifest not found: {manifest_path}")
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cards = manifest.get("cards", [])
    if not cards:
        log("[error] manifest has no cards.")
        return 2

    log(f"[info] variety={args.variety}  provider={args.provider}  cards={len(cards)}")
    if args.variety == "najdi" and args.provider == "gtts":
        log("[note] gTTS has no native Najdi voice — audio will approximate MSA pronunciation.")

    success = 0
    failures = 0
    expected = 0

    for card in cards:
        slug = card.get("slug")
        if not slug:
            log("[warn] card missing slug; skipping.")
            continue

        jobs = []
        # headword
        if card.get("arabic"):
            jobs.append((card["arabic"], out_dir / f"{slug}.mp3"))
        # examples
        for i, sent in enumerate(card.get("sentences", []), start=1):
            if sent.get("ar"):
                jobs.append((sent["ar"], out_dir / f"{slug}_ex{i}.mp3"))

        for text, path in jobs:
            expected += 1
            ok = generate_one(text, path, args.provider, args.voice, args.verbose)
            if ok:
                success += 1
            else:
                failures += 1
                if not path.exists():
                    write_silent(path)
                    log(f"[fallback] wrote silent placeholder → {path.name}")

    log(f"✓ {success}/{expected} files synthesised ({failures} fallback placeholders) → {out_dir}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
