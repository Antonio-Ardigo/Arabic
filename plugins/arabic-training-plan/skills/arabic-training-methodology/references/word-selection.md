# Word Selection

How to pick the word list for a new training plan.

## Najdi decks

A Najdi plan exists so the learner can hold a Saudi-dialect conversation that MSA alone cannot support. The word list should therefore lean toward words that **mark the dialect** or are **structural workhorses** no native Najdi speaker would avoid.

Prefer:
- **Question words** that differ from MSA: `wesh` (what), `laish` (why), `meta` (when), `shlonak` (how are you)
- **Desire/volition particles:** `abgha`, `widdi`, `ma-widdi`
- **Aspect particles:** `gaa'id / gaa'da + imperfect` (progressive), `tawwuh` (just now), `al-heen` (now)
- **Demonstratives and attitude markers:** `kidha` (like this), `akeed` (for sure), `yimkin` (maybe), `khalaas` (enough / that's it)
- **Social glue:** `zain` (good/OK), `marra` (very), `tayyib` (fine then), `yalla` (let's go)
- **High-frequency verbs in Najdi form:** `shift` (I saw), `rahat` (went), `ja` / `jaa` (came), `bghait` (I wanted)
- **Possession/benefit:** `hagg` + noun
- **Body, family, money, food** — whichever the theme calls for, but use the **Najdi** forms (e.g. `floos` for money)

Avoid:
- Pan-Arabic beginner filler the learner already knows (`salaam`, `shukran`, `naʿam`)
- MSA forms labelled as Najdi (biggest single mistake — e.g. writing `uriidu` instead of `abgha`)
- Synonym dumps (one concept, one headword)
- Words where the Najdi form is identical to MSA and adds no dialect signal (unless the theme specifically requires them)

## MSA decks

An MSA plan targets domain-accurate vocabulary — the words a learner would actually hear or read in the chosen theme.

Prefer:
- For **business**: `ijtimaaʿ` (meeting), `ʿaqd` (contract), `ʿarḍ` (presentation/offer), `mīzāniya` (budget), `muqtaraḥ` (proposal), `taslīm` (delivery), `mahla` (deadline)
- For **travel**: `ṭā'ira` (airplane), `maṭār` (airport), `fundūq` (hotel), `ḥajz` (reservation), `tadhkira` (ticket), `jawāz safar` (passport)
- For **family**: `usra` (family), `wālidayn` (parents), `akh/ukht` (brother/sister), `qarīb` (relative), `jadd/jadda` (grandfather/grandmother)
- For **news/politics**: pick workhorse verbs (`aʿlana`, `aʿlana ʿan`, `waqqaʿa`, `rafaḍa`) and nouns tied to the domain

Mix parts of speech (usually 60% nouns, 25% verbs, 15% adjectives/adverbs/particles) unless the theme is strongly noun-heavy.

Avoid:
- Greetings in a business deck
- Religious idioms unless the theme explicitly covers them
- Classical/archaic words a modern speaker wouldn't use
- Domain-mismatched entries (no `qiṭṭa` "cat" in a business deck)

## Uniqueness

- Check any existing decks or `used-words.json` if the user points at one — don't duplicate headwords
- If a word has already appeared in a previous plan for the same learner, skip it unless the theme demands it

## Sign-off rule

Always show the proposed word list as a short table (Arabic · transliteration · English · POS) and get ONE round of edits from the user. Don't re-ask twice — one round is enough. After sign-off, the list is frozen for the plan.
