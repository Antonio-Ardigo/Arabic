---
description: Run a periodic spaced-retention check against completed sub-goals of an Arabic training plan. Advances Mastery 0→5 per SM-2-lite schedule until full memorisation.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: "[SG-N | all | due]"
---

# /arabic-retention-check — Periodic Retention

You are running a **spaced-retention check** to push each sub-goal toward full memorisation (Mastery 5/5). A sub-goal is only truly mastered once it has passed at retention intervals 1d → 3d → 7d → 21d → 60d.

Load `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/SKILL.md` and `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/retention.md` before starting.

## Step 0: Find the plan

Glob for `*_training_plan.md` in the current directory. Read it. Read the sibling `words.json`. If absent, tell the learner to run `/create-arabic-training` first.

## Step 1: Pick sub-goals to re-test

Today's date: ask `date +%Y-%m-%d` via Bash (or use the system date from context).

Parse `$ARGUMENTS`:
- `SG-<N>` — re-test just that sub-goal
- `all` — re-test every sub-goal with Status in {complete, needs-review} AND Mastery < 5
- `due` (default) — re-test every sub-goal whose Next-Due date ≤ today AND Mastery < 5

From the Sub-Goals table in the plan file, collect the matching rows. If the list is empty (nothing is due), tell the learner:
> Nothing is due for review. Next retention is scheduled for `<earliest Next Due across non-mastered SGs>`. You can force a round with `/arabic-retention-check all`.

If the list has > 3 sub-goals, run them **one at a time** — ask after each whether to continue, so a retention round never becomes a marathon.

## Step 2: Build each retention mini-TTT

A retention check is a **shortened TTT** — leaner than `/run-arabic-session`, with weighted word selection.

### For a Key Fact sub-goal

**Prompt count:** 3 prompts (not 5 — retention is a check, not a fresh test).

**Word selection inside the sub-goal:**
If the sub-goal's word group has more than 3 words, weight selection by historical weakness using the `stats` object in `words.json`:

```
weakness_weight(word) = 1 - (stats.correct / max(stats.seen, 1))
# Add +0.5 if stats.last_result == "fail"
# Clamp so every word has a minimum weight of 0.1
```

Sort by weight desc; pick the top 3. If fewer than 3 words exist in the group, test them all.

**Prompt types:** pick from `${CLAUDE_PLUGIN_ROOT}/skills/arabic-training-methodology/references/test-formats.md` types A–E. Rules:
- Never test a word with the same prompt type two retention rounds in a row (check `stats.last_prompt_type` if present)
- Always include at least one audio-based prompt (A or D) if audio files exist
- Always include at least one production prompt (B or E)

Present the 3 prompts. Mandatory notes at the end.

### For a Core Principle sub-goal

Present ONE new identification task: 3 short sentences (different from any previous round) — some obey the principle, some violate it. Ask which obey and which violate. Mandatory notes at the end.

### For a Motivation sub-goal

Skip retention — Motivation doesn't benefit from spaced recall. If `due` mode hits a Motivation SG, silently bump its Mastery to 5 and its Status to `mastered`, no test.

## Step 3: Evaluate

Grade as in `/run-arabic-session` Phase 2.

- Key Fact: PASS = all 3 correct; PARTIAL = 2/3; FAIL = ≤1/3.
- Core Principle: PASS = all sentences classified correctly AND principle re-stated; otherwise FAIL.

## Step 4: Teach on demand (optional, lightweight)

- PASS: no teaching. Skip to Step 5.
- PARTIAL: deliver ONE brief teach block for the failed word(s) — just the headword line + two example sentences + memory hook. No worked example rebuild. No Quick Check — the retention round is the check.
- FAIL: deliver brief teach blocks for each failed word/principle. Do NOT loop — the fail already lowers the mastery level and the next retention round will catch it.

## Step 5: Update mastery and reschedule

For each re-tested sub-goal, apply this transition table. Let `M` = current Mastery.

| Result | New Mastery | Next Due offset |
|--------|-------------|-----------------|
| PASS | `min(M + 1, 5)` | interval for new mastery (see below) |
| PARTIAL | `M` (unchanged) | +1 day (short retry) |
| FAIL | `max(M - 1, 0)` | +1 day |

Mastery-to-interval table (same as in the plan file):

| Mastery | Interval |
|---------|----------|
| 0 | test today |
| 1 | +1 day |
| 2 | +3 days |
| 3 | +7 days |
| 4 | +21 days |
| 5 | +60 days (mastered — still rechecked once per cycle) |

**Status transition:**
- If new Mastery = 5 → Status = `mastered`
- If new Mastery < 5 and old Status = `needs-review` and result = PASS → Status = `complete`
- If result = FAIL twice in a row (check Progress Log) → Status = `needs-review`

Edit the plan file in-place: update the sub-goal row (Status, Mastery, Last Tested, Next Due). Append a Progress Log entry:

```markdown
### SG-<N> — Retention <YYYY-MM-DD>
- Scope: <word slugs tested | "core principle">
- Prompts: <type letters used, e.g. A, C, E>
- Result: <PASS/PARTIAL/FAIL> (<n>/3)
- Mastery: <old>/5 → <new>/5
- Next Due: <YYYY-MM-DD>
- Notes: <brief — which words failed, which passed>
```

Update `words.json`:
- For each tested word, increment `stats.seen` and `stats.correct` (if correct)
- Set `stats.last_result` to "pass" or "fail"
- Set `stats.last_prompt_type` to the letter used

## Step 6: Summary

After the round, show the learner a short summary:

```
Retention round — <YYYY-MM-DD>
Re-tested: <K> sub-goals
  PASS: <a>   PARTIAL: <b>   FAIL: <c>
Mastery distribution:
  5/5 (mastered): <count>
  4/5: <count>
  3/5: <count>
  2/5: <count>
  1/5: <count>
  0/5: <count>
Next review due: <earliest Next Due among non-mastered SGs>
```

If every sub-goal is at Mastery 5/5, declare the plan **fully memorised** and mark the top-level plan status as `complete (mastered)`. Congratulate briefly. Note: even mastered SGs still cycle back every 60 days to stay fresh — the plan stays "live" unless the learner archives it.

## Rules

- Retention is a CHECK — keep it short; do not rebuild worked examples
- Weight word selection by historical error rate — the whole point is to surface weaknesses
- Audio-based prompts MUST use filenames from `words.json` verbatim
- Every retention round writes: a Progress Log entry, updated sub-goal row, updated word stats
- Never advance Mastery past 5; never drop below 0
- Never touch Motivation sub-goals beyond the silent Mastery-5 bump
