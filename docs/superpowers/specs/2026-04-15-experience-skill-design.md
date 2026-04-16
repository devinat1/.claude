# Experience Skill — Skills Tracker Design Spec

**Date:** 2026-04-15
**Status:** Draft

## Overview

A user-triggered skill (`/experience`) that spawns a background agent to evaluate the user's technical and reasoning skills from the current session. The agent updates a persistent skills tracker document with domain-specific diagnostic feedback, tracks blind spots over time, and creates Todoist tasks for serious gaps.

## Goals

1. Track the user's strengths, weaknesses, and blind spots across any domain that comes up in conversation
2. Provide deeply specific, actionable feedback — not generic ratings
3. Maintain a historical record of blind spot resolution (growth over time)
4. Create concrete practice tasks in Todoist for new blind spots and red-status items
5. Never block the main conversation or pollute the session context

## Components

### 1. Skills Tracker Document

**Location:** `~/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md`

**Frontmatter:**

```yaml
---
name: skills-tracker
description: Living diagnostic of user's technical and reasoning skills — strengths, weaknesses, blind spots, and growth
type: user
---
```

**Document structure:**

```markdown
# Skills Tracker

Last updated: YYYY-MM-DD

## Current Blind Spots

- **[Topic]** — [Specific diagnostic: what the user misunderstands or consistently misses, and why it matters]. First identified: YYYY-MM-DD.

## Skills

### [Domain — e.g., System Design]
**Status:** 🟢 | 🟡 | 🔴
**[Domain-Specific Diagnostic Label]:** [Deep, specific analysis tailored to what matters in this domain. Not "you're weak at X" but "you do Y which breaks because Z."]
**Actionable Gap:** [Concrete, specific next step to practice or study. Not "learn more about X" but "do Y exercise with Z constraint."]

## Resolved Blind Spots

- **[Topic]** — Identified: YYYY-MM-DD. Resolved: YYYY-MM-DD.
  Evidence of resolution: [What changed in their prompts/thinking]
```

**Domain evolution rules:**
- New domain headers are created as topics appear organically in conversation
- Domains start broad (e.g., "React") and split into sub-domains (e.g., "React Hooks", "React State Management") after 3+ interactions show distinct sub-topic patterns
- Each domain adopts diagnostic dimensions appropriate to that domain (see table below)

**Domain-specific diagnostic dimensions (examples, not exhaustive):**

| Domain | Diagnostic Focus |
|--------|-----------------|
| System Design | Scale blind spots, capacity reasoning, tradeoff analysis |
| React / Frontend | Mental model mistakes, lifecycle misunderstandings, pattern confusion |
| General Reasoning | First-principles gaps, pattern-matching errors, wrong conclusions from limited experience |
| Databases / SQL | Query reasoning, indexing intuition, data modeling assumptions |
| DevOps / Infra | Environment-awareness gaps, deployment mental models |

New domains not in this table: the background agent determines the most useful diagnostic lens from context.

**Rating definitions:**
- 🟢 **Green** — High-specificity prompts, correct assumptions, owns decisions, demonstrates deep understanding
- 🟡 **Yellow** — Mixed signals, developing competence, occasional incorrect assumptions
- 🔴 **Red** — Consistent gaps, incorrect assumptions stated with confidence, delegates key decisions

### 2. CLAUDE.md Instruction

Appended to the user's existing CLAUDE.md at `~/.claude/CLAUDE.md`:

```markdown
# Skills Tracker

At natural breakpoints (end of a task, after debugging, when the user wraps up), if the session had meaningful skill signals, remind the user once:

> "Want me to update your skills tracker? `/experience`"

- One reminder per session max
- Skip if the session was trivial
- NEVER auto-update — only when the user invokes /experience
```

### 3. `/experience` Skill

**Trigger:** User invokes `/experience`

**Main conversation behavior:**
1. Output a one-liner: "Updating skills tracker in the background."
2. Spawn a background agent (`run_in_background: true`)
3. No results returned to the main conversation context

**Background agent prompt must include:**
- The user's prompts from the session
- Thinking Check scores observed during the session
- Any incorrect assumptions the user made (with what was wrong and why)

**Background agent responsibilities:**

1. Read the current skills tracker from memory
2. Evaluate session signals using three lenses:
   - **Thinking Check scores** per domain touched by the session
   - **Prompt precision** — decisive and specific (green signal) vs. vague and delegating (yellow/red signal)
   - **Incorrect assumptions** — anything stated as fact that was wrong (strongest blind spot signal)
3. Update existing domains or create new domain headers
4. Split broad domains into sub-domains when 3+ interactions show distinct sub-topic patterns
5. Move blind spots to "Resolved Blind Spots" when corrected understanding is demonstrated (with date and evidence)
6. Adjust status colors based on accumulated evidence, not single interactions
7. Write domain-specific diagnostic feedback:
   - Use the diagnostic lens appropriate to the domain
   - Be deeply specific — name exact mistakes, patterns, and misconceptions
   - End every domain entry with a concrete **Actionable Gap**
8. If a **new blind spot** or **new red-status item** is identified: create a Todoist task (see below)
9. Write the updated tracker back to the file
10. Update MEMORY.md index if the tracker is new

### 4. Todoist Integration

**Trigger conditions (ALL must be met):**
- A new blind spot is added to "Current Blind Spots" section, OR
- A domain is newly rated as 🔴 Red

**Not triggered by:**
- Yellow items or updates to existing entries
- Resolved blind spots
- Status changes that aren't to red (e.g., red to yellow improvement)

**Task properties:**
- **Project:** "claude"
- **Content:** Specific, actionable practice item. Examples:
  - "Implement a React form using useReducer with validation — focus on controlled components only. Compare your approach to the React docs 'Extracting State Logic' guide."
  - "Design a connection pooling strategy for a 100K-user app — start with pgBouncer docs and calculate max connections per instance given 4 app server replicas."
  - "Take a past decision where you pattern-matched from a previous project. Write down what was different about the new context and whether the pattern still held. Focus on environmental constraints (serverless vs. server, scale, latency)."
- **NOT:** Vague tasks like "Learn about database scaling" or "Get better at React"

## Signal Evaluation Details

### Thinking Check Score Mapping

The Thinking Check system already scores each prompt on three dimensions (1-5):
- **Specificity of Intent** — maps to domain mastery
- **Decision Ownership** — maps to confidence/experience level
- **Diagnostic Effort** — maps to debugging/analytical skill

These scores, evaluated per-domain, provide the primary signal. The background agent maps them:
- Avg 4-5 in a domain → 🟢 Green signal
- Avg 2.5-3.9 → 🟡 Yellow signal  
- Avg < 2.5 → 🔴 Red signal

Scores are weighted by the incorrectness signal — if a user scores 4/5 on specificity but includes confident misinformation, the effective signal drops significantly.

### Incorrect Assumption Detection

The strongest blind spot signal. Examples:
- User states "LEFT JOIN excludes rows from the right table" (misunderstanding of JOIN semantics)
- User assumes JWT refresh works identically in serverless and server contexts
- User confidently claims useEffect runs synchronously after render

These get documented with: what was stated, what's actually true, and what underlying mental model gap this reveals.

## Non-Goals

- No automatic updates — user must invoke `/experience`
- No blocking of main conversation
- No results returned to session context
- No tracking of prompts with zero skill signal (greetings, confirmations, slash commands)
- No predetermined domain list — domains emerge organically
