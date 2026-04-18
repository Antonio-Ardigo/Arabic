# Saudi Arabic (Najdi) Flashcards

A training deck of 20 high-frequency **Najdi Saudi** dialect words. Each card gives the word in Arabic, a transliteration, the English meaning, two example sentences with word-by-word glosses, and pronunciation links.

This is **Najdi-only**. We deliberately skip pan-Arabic basics (`marhaba`, `as-salaam alaykum`, `na'am`, `la`) — those appear inside example sentences but don't get their own cards. The list focuses on words that mark Najdi dialect or are structural workhorses (`wesh`, `abgha`, `gaa'id`, `hagg`, `widdi`, etc.).

## How to use

- Start at [index.md](index.md) for the full table.
- Click through to individual cards in [`cards/`](cards/).
- Each card has two pronunciation links:
  1. A **Forvo** link — works immediately, real native speakers.
  2. A local `audio/<transliteration>.mp4` — the proper artifact per the spec (slide with both example sentences, target word visually highlighted as it is pronounced). These files are **not committed** (see [audio/README.md](audio/README.md)).

## Transliteration scheme

| Sound | Written as | Note |
|---|---|---|
| Long vowels | `aa`, `ee`, `ii`, `oo`, `uu` | |
| ق (Najdi) | `g` | Najdi fronts ق to a hard `g` (`gaal`, `gidar`) |
| ك (Najdi, sometimes) | `ch` | Affrication in some words (`chidhi`); not all speakers |
| ج | `j` | |
| غ | `gh` | |
| خ | `kh` | |
| ش | `sh` | |
| ث | `th` | |
| ذ | `dh` | |
| ع | `'` | Before a vowel: `'a`, `'i`, `'u` |
| ء | `'` | Glottal stop (same symbol; context resolves) |
| ح | `h` | We don't distinguish ح from ه in this scheme for readability |

Stress and emphatics are not marked. This is a learner-friendly scheme, not IPA.

## Reusable skill

A Claude Code skill lives at [`.claude/skills/saudi-flashcard/SKILL.md`](.claude/skills/saudi-flashcard/SKILL.md). It encodes the card template, Najdi-only rule, transliteration scheme, and audio-link convention so future cards come out identical. Invoke it by asking Claude to "add a Saudi flashcard" or use the Skill tool.

## Layout

```
README.md            this file
index.md             table of all 20 cards
cards.json           machine-readable manifest
cards/               20 markdown flashcards
audio/               mp4 pronunciation slides (user-supplied, gitignored)
.claude/skills/      the saudi-flashcard skill
```
