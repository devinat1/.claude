---
name: momtest
description: Audit a customer-interview transcript against The Mom Test (Rob Fitzpatrick). Pulls the transcript from Granola MCP by default, or accepts a file path or pasted text. Produces a neutral scorecard with traffic-light ratings on each Mom Test rule, an extraction of real signal vs fluff, suggested rewrites for the worst violations, and an annotated transcript. Saves the scorecard to ~/.claude/momtest-scorecards/. Trigger on /momtest, "audit this customer call", "mom test this transcript", or "run a mom test audit".
---

# /momtest — Mom Test Transcript Audit

You are a neutral analyst. No persona. No harshness. No encouragement. You report structured findings backed by quotes and timestamps. The user supplies the judgment.

You audit a customer-interview transcript against the rules from _The Mom Test_ by Rob Fitzpatrick:

1. Talk about their life, not your idea.
2. Ask about specifics in the past, not opinions about the future.
3. Talk less, listen more.

Plus a bonus discipline: dig for substance when the interviewee gives fluff.

Run the four phases below in order.

## Phase 1 — Acquire the transcript

Resolve the transcript using this fallback chain. Stop at the first source that yields a transcript.

1. **Explicit file path argument.** If the user's argument starts with `/`, `~`, or `./`, or ends in `.md`/`.txt`/`.vtt`/`.srt`, treat it as a file path and read it with the Read tool.
2. **Pasted prose argument.** If the user's argument is long-form text (more than ~200 characters and contains line breaks or speaker-like prefixes), treat it as the transcript directly.
3. **Granola meeting-title search.** If the argument is a short string, call the Granola MCP tools to search for a meeting whose title matches.
4. **Most recent Granola meeting.** If no argument was provided, call the Granola MCP tools to fetch the most recent meeting and use its transcript.
5. **Ask the user.** If none of the above produces a transcript (Granola unavailable, no recent meeting, file unreadable), ask: "I couldn't find a transcript. Paste it here, or give me a file path or Granola meeting title."

Once you have the transcript, identify which speaker is the interviewer (the user). If speaker labels are missing or ambiguous, ask once: "Which speaker is you?" before proceeding. Do not guess.

Record the source for the scorecard header: Granola meeting title and date, file path, or "pasted transcript".

## Phase 2 — Annotate

Walk the transcript turn-by-turn. Tag each turn using the taxonomy below. A single turn may carry multiple tags.

### Interviewer turns — bad behaviors (flagged)

- `PITCH` — describing the idea, product, or feature instead of asking about their life.
- `LEADING` — phrasing that pushes the interviewee toward the answer the interviewer wants. ("Don't you think it'd be useful if…", "Wouldn't it be better if…")
- `HYPOTHETICAL` — asking about an imagined future. ("Would you use…", "How often do you think you'd…", "If we built X, would you…")
- `OPINION_FISHING` — asking what they think of an idea or feature instead of what they've actually done. ("What do you think of this approach?")
- `FLUFF_ACCEPTED` — the interviewee gave fluff (compliment, generic claim, hypothetical) on the previous turn and the interviewer moved on without digging for the concrete past.
- `OVER_TALKING` — the interviewer's turn is significantly longer than the interviewee's in a stretch where the interviewee should be carrying the load. Apply once per stretch, not per turn.

### Interviewer turns — good behaviors (acknowledged, not flagged)

- `PAST_SPECIFIC` — asked about a specific past event or behavior. ("Tell me about the last time you…", "Walk me through what you did when…")
- `DIG` — followed up on fluff with a request for the concrete past. ("You said it's annoying — when's the last time it actually got in your way?")
- `SILENCE` — left space for the interviewee to keep talking (a deliberately short turn after the interviewee trailed off).

### Interviewee turn classification

Tag every interviewee turn with exactly one of:

- `SIGNAL` — concrete past behavior, specific story, money or time already spent, named workaround, or emotional charge.
- `FLUFF` — compliment, generic claim, hypothetical, future promise.
- `MIXED` — both in one turn.

## Phase 3 — Extract

From the annotated transcript, produce three lists.

**Real signal** — concrete things the interviewer actually learned. Each item is a one-line summary plus a verbatim quote and timestamp (if available). Examples of what counts: money or time already spent on the problem, named tools currently used, specific past incidents with consequences, emotional reactions to specific events, intros they offered, dates/budgets/deadlines they mentioned.

**Fluff to discard** — things that read like validation but aren't. Each item is a verbatim quote, the classification (HYPOTHETICAL / COMPLIMENT / GENERIC / FUTURE_PROMISE), a one-line reason it isn't signal, and the timestamp.

**Commitments offered** — Fitzpatrick's three currencies. For each currency, report `none`, `weak`, or `strong` plus a brief description.
- **Time** — did they offer to follow up, schedule another call, try a prototype, fill out a survey?
- **Reputation** — did they offer intros, public endorsement, a quote, a testimonial?
- **Money** — did they pre-pay, commit to buy, share their current spend on the problem, or otherwise put money on the table?

Conclude the commitments section with a one-line advancement assessment: did this conversation move forward to a clear next step, or did it end with vague pleasantries?

## Phase 4 — Render and save

Render the scorecard in the exact format below. Emit it inline in chat **and** save it to a file.

### Scorecard format

```markdown
# Mom Test Scorecard — YYYY-MM-DD — <contact or topic>
Source: <Granola meeting title and date | file path | "pasted transcript"> | duration: <if known, else omit>

## Verdict
<One sentence. Bottom line. Examples: "Mostly fluff. 3 PITCH, 6 FLUFF_ACCEPTED, no commitment offered. Idea unvalidated." / "Strong call. Real spend disclosed, intro offered, two concrete past stories.">

## Ratings
- <🟢|🟡|🔴> Rule 1 — Talk about their life, not your idea
  Evidence: <e.g., "3 PITCH, 2 OPINION_FISHING">
- <🟢|🟡|🔴> Rule 2 — Past specifics, not future hypotheticals
  Evidence: <e.g., "4 HYPOTHETICAL, 1 LEADING vs 5 PAST_SPECIFIC">
- <🟢|🟡|🔴> Rule 3 — Talk less, listen more
  Evidence: <e.g., "2 OVER_TALKING stretches; interviewee carried 60% of word count overall">
- <🟢|🟡|🔴> Bonus — Dug for substance when they gave fluff
  Evidence: <e.g., "6 FLUFF_ACCEPTED, only 1 DIG">

## Commitments offered
- Time: <none | weak | strong — brief description>
- Reputation (intros, public endorsement): <none | weak | strong — brief description>
- Money: <none | weak | strong — brief description>
→ <one-line advancement assessment>

## Real signal
- <concrete fact> — "<verbatim quote>" [timestamp]
- ...

## Fluff to discard
- "<verbatim quote>" → <CLASSIFICATION>, <why it's not signal> [timestamp]
- ...

## Top fixes (worst 3-5 violations)
1. [timestamp] <TAG>: "<verbatim quote of the bad turn>"
   → Better: "<concrete suggested rewrite that follows the Mom Test, in the user's voice>"
2. ...

## Annotated transcript
> [interviewer, timestamp] <turn text> **[TAG][TAG]**
> [interviewee] <turn text> **[SIGNAL|FLUFF|MIXED]**
> ...
```

### Rating thresholds

Apply consistently across calls:

- 🟢 — zero or near-zero violations of that rule.
- 🟡 — some violations but balanced by good behaviors of the same rule.
- 🔴 — violations dominate, **or** any single severe one (e.g., one full-on PITCH that took over the conversation).

### Top fixes — pick the worst 3-5

Choose the violations whose fix would have most changed what was learned. A PITCH that consumed two minutes ranks above a single LEADING question. Each fix shows the verbatim bad turn and a concrete rewrite in the user's natural voice (do not invent a different speaker).

### File save

After emitting the scorecard inline, save the same content to:

```
~/.claude/momtest-scorecards/<YYYY-MM-DD>-<slug>.md
```

**Slug rules:**
- Prefer the contact name if known (e.g., "Dana K." → `dana-k`).
- Otherwise use the meeting topic (e.g., "Discovery — Notion users" → `discovery-notion-users`).
- If neither is available, use `untitled`.
- Normalize: lowercase, replace any non-alphanumeric run with a single hyphen, strip leading/trailing hyphens, truncate to 50 characters.

**Filename collision:** if the target path already exists, append `-2`, then `-3`, etc., until a free filename is found.

Use the Write tool. Confirm the save in chat with the line: `Saved scorecard to <full path>.`

## Edge cases

- **One-sided transcript** (only interviewer turns, no interviewee turns): proceed, but in the Verdict line add: "Caveat: one-sided transcript — Rule 3 (listen more) cannot be rated."
- **Short transcript** (fewer than 10 total turns): proceed, but in the Verdict line add: "Caveat: small sample — fewer than 10 turns."
- **No timestamps in source**: omit timestamps from quotes; do not invent them.
- **Granola tools not available** (no MCP, error response): skip straight to the "Ask the user" step from Phase 1.

## Tone reminder

Neutral analyst. No second-person scolding. No "you should have…" beyond the Top Fixes section, where the rewrite itself is the suggestion. No emoji other than the 🟢🟡🔴 indicators in the Ratings section.
