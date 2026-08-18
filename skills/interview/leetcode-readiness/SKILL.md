---
name: leetcode-readiness
description: Use when the user invokes /leetcode-readiness or wants an evidence-based LeetCode progress assessment, interview-readiness date, or next-week problem plan from LeetCode and Obsidian history.
---

# LeetCode Readiness

## Consequential advice

Before selecting the readiness date or next-week problem plan, follow the
`Advice gate` in `dissenter`. Wait for the user's choice before updating the
persistent weekly plan.

Assess progress from observed work, choose the next problems, and update one persistent weekly plan. Keep the critique brief; this is not a mock interview or a generic curriculum.

## Hard boundaries

- Use the installed `obsidian` CLI directly for every vault read and write. Do not use MCP or raw filesystem access to the vault.
- Target `vault=State` and `Notes/CP/LeetCode Weekly Plan.md`.
- Do not ask for a company, target date, role, or readiness standard.
- Do not emit a pass/fail band, detailed daily schedule, or per-activity time budget.
- Treat the readiness date as a ballpark estimate, not a validated prediction.

## Intake

Ask exactly two questions, one at a time:

1. LeetCode username
2. Hours available over the next seven days

Reject an invalid username or a non-positive hours value. Then proceed without more intake.

## Gather evidence

Use `https://leetcode-api-pied.vercel.app` and fetch what is available from:

- `/user/{username}`
- `/user/{username}/solved`
- `/user/{username}/skills`
- `/user/{username}/calendar`
- `/user/{username}/submissions`

Use `/problem/{slug}` and `/problem/{slug}/similar` when selecting problems. Ignore company tags. Cross-check inconsistent totals instead of treating every endpoint as complete.

Use direct CLI commands such as `obsidian files vault=State folder=Notes/CP`, `obsidian search ...`, and `obsidian read ...`. Ignore Obsidian startup-banner lines. Inspect relevant problem notes for `minutes_taken`, difficulty, topics, `last_attempted`, rating/status, repeated attempts, hints, mistakes, and prose describing confusion. Missing fields are unknown, not poor performance.

Read the existing weekly plan before analysis so its previous estimate and history can be retained.

## Assess

Cover four dimensions with short, evidence-backed observations:

- topic coverage
- solving speed relative to the user's own same-difficulty history
- difficulty progression
- recent consistency

Name only useful strengths and weaknesses. Raw solve count alone is not mastery; prefer agreement between API activity, timing, recurrence, and note prose. Mark thin evidence as tentative.

Choose one ballpark readiness date. Estimate remaining practice from the demonstrated gaps and the user's observed pace, then account for this run's available hours. Compare it with the previous date and state why it moved earlier, later, or stayed unchanged. If there is no prior run, say so. Do not invent precision or a pass/fail rubric.

## Select the next questions

Create an ordered list that reasonably fits the available hours using the user's recorded pace when available. Include both:

- **Review:** slow, stale, repeated, low-confidence, or explicitly confusing solved problems.
- **New:** unseen problems similar to those struggles, preferring direct similarity and matching weak topics.

Include at least one of each when the available time permits. For every item provide `[New]` or `[Review]`, title, LeetCode link, topic, and one short evidence-based reason. Do not divide the list into days or fixed sessions.

## Update Obsidian

Generate this compact section, carrying forward every existing history row and adding the current run:

```markdown
## Current assessment — YYYY-MM-DD

**Ballpark interview-ready date:** YYYY-MM-DD  
**Change:** [previous date and brief reason for movement, or first estimate]  
**Next seven days:** [hours] hours

### Brief critique
- **Strong:** [evidence → implication]
- **Improve:** [evidence → action]

### Question queue
1. **[Review] [Problem](URL)** — [topic]: [reason]
2. **[New] [Problem](URL)** — [topic]: [reason]

### Data limits
- [missing, partial, or inconsistent evidence; omit when none]

### Run history
| Run | Hours | Solved/difficulty snapshot | Main focus | Ready date |
|---|---:|---|---|---|
| YYYY-MM-DD | N | ... | ... | YYYY-MM-DD |
```

Pass that Markdown on stdin to `scripts/update_plan.py` from this skill. The script creates the note when absent, replaces only the `leetcode-readiness` marker block, preserves manual text, rejects malformed markers, and verifies the saved note.

## Best effort

- API unavailable: use Obsidian evidence and disclose the missing current account data.
- Obsidian unavailable: use API evidence, leave the plan untouched, and never fall back to raw vault access.
- Both unavailable or evidence too thin: state that no defensible assessment or date can be produced.
- Update script failure: report it and do not claim the plan changed.

In chat, return the date, its movement reason, the brief critique, the queue, data limits, and whether the note update verified.
