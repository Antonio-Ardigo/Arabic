# Card Templates

## Slug rules

- Lowercase ASCII transliteration of the headword, hyphen-separated.
- Strip `al-` prefixes and diacritics.
- If two headwords produce the same slug, suffix with `-2`, `-3`, etc.
- Examples: `wesh`, `abgha`, `gaaid`, `ijtima` (for اجتماع), `aqd` (for عقد).

## Markdown card template

Use this template **exactly**. Do not reorder sections. Do not invent new sections.

```markdown
# <arabic-script> — <transliteration>

**Variety:** <Najdi | MSA>
**Part of speech:** <noun | verb | adjective | particle | interjection>
**Theme:** <theme>

## Definition
<one short English line>

## Notes
<optional: one-line register/usage note. Omit section if nothing to say.>

## Example 1
**AR:** <arabic sentence>
**Translit:** <transliteration>
**EN:** <english translation>
**Gloss:** <word1=w1> · <word2=w2> · <word3=w3> …
**Audio:** [headword](audio/<slug>.mp3) · [sentence](audio/<slug>_ex1.mp3)

## Example 2
**AR:** <arabic sentence>
**Translit:** <transliteration>
**EN:** <english translation>
**Gloss:** <word1=w1> · <word2=w2> · <word3=w3> …
**Audio:** [sentence](audio/<slug>_ex2.mp3)

## Pronunciation
- Local: [headword mp3](audio/<slug>.mp3)
- Forvo: https://forvo.com/word/<url-encoded-arabic>/#ar
```

## JSON manifest schema (`cards.json`)

```json
{
  "deck": {
    "variety": "najdi",
    "theme": "business",
    "created": "2026-04-18",
    "count": 10
  },
  "cards": [
    {
      "slug": "ijtima",
      "arabic": "اجتماع",
      "translit": "ijtimaaʿ",
      "english": "meeting",
      "pos": "noun",
      "notes": "",
      "sentences": [
        {
          "ar": "عندنا اجتماع الساعة عشرة.",
          "translit": "ʿindana ijtimaaʿ as-saaʿa ʿashra.",
          "en": "We have a meeting at ten.",
          "gloss": "ʿindana=we-have · ijtimaaʿ=meeting · as-saaʿa=the-hour · ʿashra=ten",
          "audio": "audio/ijtima_ex1.mp3"
        },
        {
          "ar": "الاجتماع تأجّل إلى الغد.",
          "translit": "al-ijtimaaʿ taʾajjal ila l-ghad.",
          "en": "The meeting was postponed to tomorrow.",
          "gloss": "al-ijtimaaʿ=the-meeting · taʾajjal=was-postponed · ila=to · l-ghad=the-tomorrow",
          "audio": "audio/ijtima_ex2.mp3"
        }
      ],
      "audio_headword": "audio/ijtima.mp3",
      "forvo": "https://forvo.com/word/%D8%A7%D8%AC%D8%AA%D9%85%D8%A7%D8%B9/#ar"
    }
  ]
}
```

## Selection philosophy

### Najdi decks

Pick words that **mark the dialect** or are **structural workhorses** — the kind of thing that, if a learner already knew MSA, would unlock real Najdi listening comprehension. Typical keepers:

- Question words and particles: `wesh` (what), `wen` (where), `mita` (when), `laish` (why), `cham` (how many).
- Dialect verbs and modals: `abgha` (want), `widdi` (I want), `gaa'id` (currently, -ing), `trooh` (you go), `yaji` (he comes).
- High-frequency nouns with dialect pronunciation: `hagg` (for/of), `zain` (good), `gahwa` (coffee).
- Discourse markers: `yaʿni`, `tara`, `khalli`, `ʿaad`.

Skip pan-Arabic basics (`salaam`, `shukran`) unless the theme actually demands them.

### MSA decks

Pick words a reader/listener will encounter in the **register** the theme implies. For "business MSA":

- Formal nouns: `اجتماع`, `عقد`, `ميزانية`, `عرض`, `مقترح`, `تسليم`, `مهلة`, `تقرير`, `مراجعة`, `فاتورة`.
- Useful verbs: `اجتمع`, `وقّع`, `سلّم`, `راجع`, `أرسل`, `اتفق`.
- Useful adjectives/adverbs: `عاجل`, `نهائي`, `تقريبي`, `مبدئياً`, `رسمياً`.

For "travel MSA" or "academic MSA" adjust accordingly. Always explain your picks to the user in one sentence.

## Do / Don't — example sentences

**DO** (Najdi, theme = coffee shop, headword = `abgha`):
- `أبغى قهوة سادة.` — *abgha gahwa saada.* — "I want plain coffee."
- `ويش تبغى تشرب؟` — *wesh tabgha tishrab?* — "What do you want to drink?"

**DON'T** — wrong variety (this is MSA, not Najdi):
- `أريد فنجان قهوة من فضلك.` — *ʾuriidu finjaana qahwatin min faḍlik.* — ✗ Not Najdi.

**DO** (MSA, theme = business, headword = `ميزانية`):
- `الميزانية محدودة هذا الربع.` — *al-miizaaniyya maḥduuda haadha r-rubʿ.* — "The budget is limited this quarter."

**DON'T** — too long, multiple new words:
- `أرسلت إليكم الميزانية المعدّلة مع الملاحظات التفصيلية صباح اليوم.` — ✗ Over 8 words, too many unknowns.
