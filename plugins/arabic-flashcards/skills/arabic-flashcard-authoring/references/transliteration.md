# Transliteration schemes

Use **one** scheme per deck. Do not mix.

## Najdi popular scheme

Approximates how Najdi is written in casual Romanised chat (close to the style used in the reference repo). Readable, non-diacritic-heavy.

| Arabic | Najdi popular |
|--------|---------------|
| ا / آ  | aa (long) / a (short) |
| ب | b |
| ت | t |
| ث | th |
| ج | j |
| ح | 7 or h (prefer `h` in prose) |
| خ | kh |
| د | d |
| ذ | dh |
| ر | r |
| ز | z |
| س | s |
| ش | sh |
| ص | s (context) |
| ض | d (context) |
| ط | t (context) |
| ظ | th (context) |
| ع | ʿ (or `3`) |
| غ | gh |
| ف | f |
| ق | g (Najdi often pronounces ق as /g/) |
| ك | k or ch (when pronounced /tʃ/) |
| ل | l |
| م | m |
| ن | n |
| ه | h |
| و | w / uu (long) |
| ي | y / ii (long) |

Najdi-specific notes:
- The letter ق often becomes `/g/` in Najdi pronunciation — transliterate as `g` where it's actually said that way (`gahwa` قهوة, `gaaʿid` قاعد, `hagg` حق).
- The letter ك can palatalise to `/tʃ/` before front vowels — write `ch` when that happens (`chaan` كان in some subdialects — optional, only if the learner will actually hear it).
- The feminine ending ة is usually `-a`, not `-ah`.
- Definite article `al-` assimilates with sun letters: write `as-` / `ash-` / `ar-` as pronounced.

## MSA DIN-31635-lite scheme

Simplified DIN-31635 — accurate enough for learners, friendly enough to type.

| Arabic | MSA |
|--------|-----|
| ا | aa |
| ب | b |
| ت | t |
| ث | th |
| ج | j |
| ح | ḥ |
| خ | kh |
| د | d |
| ذ | dh |
| ر | r |
| ز | z |
| س | s |
| ش | sh |
| ص | ṣ |
| ض | ḍ |
| ط | ṭ |
| ظ | ẓ |
| ع | ʿ |
| غ | gh |
| ف | f |
| ق | q |
| ك | k |
| ل | l |
| م | m |
| ن | n |
| ه | h |
| و | w / uu |
| ي | y / ii |
| ة | a (pausal) / at (construct) |
| ء | ʾ |

MSA notes:
- Keep ق as `q` (don't write `g`).
- Mark long vowels explicitly: `aa`, `uu`, `ii`.
- Use `ʿ` for ع and `ʾ` for hamza. If the user prefers ASCII-only, substitute `'` for hamza and `3` for ʿain and say so in the README.

## Which scheme when

| Variety | Scheme |
|---------|--------|
| `najdi` | Najdi popular |
| `msa`   | MSA DIN-31635-lite |

Record the scheme name in the first card's comment line so a future editor sees it.
