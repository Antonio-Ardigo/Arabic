#!/usr/bin/env python3
"""Build an Anki-compatible tab-separated import file from a deck's cards.json.

Output format (Anki 2.1+):
    - Tab-separated
    - Leading Anki metadata comments (#separator, #html, #columns)
    - 10 columns, in this order:
        1. Arabic         (headword)
        2. Transliteration
        3. English        (definition)
        4. Sentence1_AR
        5. Sentence1_EN
        6. Sentence2_AR
        7. Sentence2_EN
        8. Audio_Headword  (as [sound:xxx.mp3])
        9. Audio_Sentence1
        10. Audio_Sentence2

After importing into Anki, copy the deck's audio/*.mp3 files into
Anki's collection.media folder so the [sound:] tags resolve.

Usage:
    python build_anki.py --manifest path/to/cards.json [--out path/to/anki.csv]
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

COLUMNS = [
    "Arabic",
    "Transliteration",
    "English",
    "Sentence1_AR",
    "Sentence1_EN",
    "Sentence2_AR",
    "Sentence2_EN",
    "Audio_Headword",
    "Audio_Sentence1",
    "Audio_Sentence2",
]


def build(manifest_path: Path, out_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cards = manifest.get("cards", [])

    with out_path.open("w", encoding="utf-8", newline="") as f:
        # Anki 2.1 metadata lines — must come before data, preceded by '#'
        tab = "\t"
        f.write("#separator:tab\n")
        f.write("#html:false\n")
        f.write(f"#columns:{tab.join(COLUMNS)}\n")

        w = csv.writer(f, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        for c in cards:
            slug = c["slug"]
            sents = c.get("sentences", [])
            s1 = sents[0] if len(sents) >= 1 else {"ar": "", "en": ""}
            s2 = sents[1] if len(sents) >= 2 else {"ar": "", "en": ""}
            w.writerow([
                c.get("arabic", ""),
                c.get("translit", ""),
                c.get("english", ""),
                s1.get("ar", ""),
                s1.get("en", ""),
                s2.get("ar", ""),
                s2.get("en", ""),
                f"[sound:{slug}.mp3]",
                f"[sound:{slug}_ex1.mp3]",
                f"[sound:{slug}_ex2.mp3]",
            ])

    print(f"[OK] wrote {out_path}  ({len(cards)} cards, {len(COLUMNS)} columns)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, help="Path to cards.json")
    ap.add_argument("--out", default=None, help="Output CSV path (default: anki.csv next to manifest)")
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    out_path = Path(args.out) if args.out else manifest_path.parent / "anki.csv"
    build(manifest_path, out_path)


if __name__ == "__main__":
    main()
