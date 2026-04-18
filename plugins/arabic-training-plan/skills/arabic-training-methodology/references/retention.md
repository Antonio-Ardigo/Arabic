# Retention Schedule

Spaced retention drives each sub-goal from Mastery 2/5 (set when the Final Test passes) all the way to Mastery 5/5 (fully memorised). A plan is only "fully memorised" when every Key Fact sub-goal is at 5/5.

## Mastery → interval table

| Mastery | Meaning | Interval before next review |
|---------|---------|-----------------------------|
| 0 | Never passed, or failed last retention | test today |
| 1 | Shaky — recently failed | +1 day |
| 2 | Final Test passed (fresh) | +3 days |
| 3 | Held up at 3-day retention | +7 days |
| 4 | Held up at 7-day and 21-day retentions | +21 days |
| 5 | Fully memorised | +60 days (light rechecks to keep fresh) |

The table is deliberately SM-2-lite — not the full SuperMemo algorithm. It's easier to explain, and the low-data regime of a ≤30-word plan doesn't benefit from per-word ease factors.

## Transition rules

After each retention round, update each tested sub-goal:

| Result | New Mastery | Next Due offset | Status change |
|--------|-------------|-----------------|---------------|
| PASS | `min(M + 1, 5)` | interval for new M | if new M = 5 → `mastered`; if was `needs-review` → `complete` |
| PARTIAL | `M` (unchanged) | +1 day | none |
| FAIL | `max(M - 1, 0)` | +1 day | if FAIL twice in a row (check Progress Log) → `needs-review` |

Mastery is per **sub-goal**, not per word — a Key-Fact group of 5–8 words advances or drops as a unit. This keeps the review burden predictable: the learner gets through the whole plan's due list in one sitting, not 30 individual word reviews.

## Word-selection weighting inside a sub-goal

When a retention round picks which words from a group of >3 to test, weight by historical weakness:

```
weakness(word) = 1 - (stats.correct / max(stats.seen, 1))
if stats.last_result == "fail": weakness += 0.5
weakness = max(weakness, 0.1)    # everyone has a floor chance
```

Sort descending by weakness; pick the top 3. This ensures the words the learner consistently gets wrong resurface faster than ones they've nailed.

## Special cases

- **Motivation SGs:** skip retention entirely. In `due` mode, silently bump Motivation SGs to Mastery 5/5 — they don't benefit from spaced vocabulary recall.
- **Core Principle SGs:** retention uses the identification-task format (3 sentences, classify obey/violate). Different prompt set every time. No audio-rotation rule (use audio whenever the blueprint example had it).
- **`needs-review` SGs:** if a sub-goal is in `needs-review` after two consecutive FAILs, the next retention run should include a full Teach block before the test, not just a lightweight one. Flag to the learner: "This one is stuck — let's revisit the underlying principle before the retention check."

## Round size

- Default mode `/arabic-retention-check` (no arg) = "due": everything past Next Due, Mastery < 5
- If the due list is > 3 sub-goals, run them one at a time with a "continue?" prompt between rounds
- `/arabic-retention-check all` forces a full scan (ignores Next Due, still skips Mastery-5 SGs)
- `/arabic-retention-check SG-<N>` runs just one SG regardless of due date

## When is the plan "done"?

Every Key-Fact sub-goal at Mastery 5/5. At that point:
- Top of plan file → Status = `complete (mastered)`
- Congratulate the learner briefly
- Mastered SGs still cycle back every 60 days — the plan stays "live" until the learner archives it or creates a new plan that supersedes it
