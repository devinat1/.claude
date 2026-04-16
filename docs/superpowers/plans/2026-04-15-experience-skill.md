# /experience Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the `/experience` skill — a user-triggered command that spawns a background agent to evaluate the user's skills from the current session, update a persistent tracker with domain-specific diagnostics, and create Todoist tasks for blind spots.

**Architecture:** Four files: a skill markdown file (`commands/experience.md`), an initial skills tracker document in memory, a MEMORY.md index, and a CLAUDE.md append. The skill instructs Claude to summarize session signals and dispatch a background agent. The agent reads/writes the tracker and conditionally creates Todoist tasks.

**Tech Stack:** Markdown skill files, Claude Code memory system, Todoist MCP tools (`find-projects`, `add-tasks`)

---

### Task 1: Create the Initial Skills Tracker Document

**Files:**
- Create: `/Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md`

- [ ] **Step 1: Create the skills tracker file**

```markdown
---
name: skills-tracker
description: Living diagnostic of user's technical and reasoning skills — strengths, weaknesses, blind spots, and growth over time
type: user
---

# Skills Tracker

Last updated: 2026-04-15

## Current Blind Spots

_No blind spots identified yet._

## Skills

_No domains tracked yet. Domains are added as they emerge from conversations._

## Resolved Blind Spots

_No resolved blind spots yet._
```

- [ ] **Step 2: Verify the file was created**

Run: `cat /Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md`
Expected: The full file contents from Step 1.

- [ ] **Step 3: Commit**

```bash
git add projects/-Users-devinat1--claude/memory/skills_tracker.md
git commit -m "feat: create initial skills tracker document in memory"
```

---

### Task 2: Create the MEMORY.md Index

**Files:**
- Create: `/Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/MEMORY.md`

- [ ] **Step 1: Create MEMORY.md with a pointer to the skills tracker**

```markdown
- [Skills Tracker](skills_tracker.md) — Living diagnostic of technical/reasoning skills, blind spots, and growth
```

- [ ] **Step 2: Verify the file was created**

Run: `cat /Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/MEMORY.md`
Expected: The single-line index entry from Step 1.

- [ ] **Step 3: Commit**

```bash
git add projects/-Users-devinat1--claude/memory/MEMORY.md
git commit -m "feat: create MEMORY.md index with skills tracker pointer"
```

---

### Task 3: Append Skills Tracker Reminder to CLAUDE.md

**Files:**
- Modify: `/Users/devinat1/.claude/CLAUDE.md` (append after existing content)

- [ ] **Step 1: Read the current CLAUDE.md**

Read `/Users/devinat1/.claude/CLAUDE.md` to confirm current contents end with the Thinking Check section.

- [ ] **Step 2: Append the skills tracker instruction**

Add the following after the existing content (with a blank line separator):

```markdown

# Skills Tracker

At natural breakpoints (end of a task, after debugging, when the user wraps up), if the session had meaningful skill signals, remind the user once:

> "Want me to update your skills tracker? `/experience`"

- One reminder per session max
- Skip if the session was trivial
- NEVER auto-update — only when the user invokes /experience
```

- [ ] **Step 3: Verify the append**

Read `/Users/devinat1/.claude/CLAUDE.md` and confirm the Skills Tracker section appears after the Thinking Check section, with no corruption of existing content.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "feat: add skills tracker reminder instruction to CLAUDE.md"
```

---

### Task 4: Create the `/experience` Skill

**Files:**
- Create: `/Users/devinat1/.claude/commands/experience.md`

This is the core deliverable. The skill file instructs Claude to:
1. Summarize the session's skill signals
2. Spawn a background agent with those signals
3. The agent reads the tracker, evaluates, updates, and optionally creates Todoist tasks

- [ ] **Step 1: Create the skill file**

```markdown
---
name: experience
description: Update the skills tracker with diagnostic feedback from the current session. Use when the user invokes /experience or says "update my skills tracker". Spawns a background agent — never blocks the main conversation.
---

**You are a skills assessment dispatcher.** Your job is to summarize the session's skill signals and hand them to a background agent for tracker updates.

## When triggered

### Step 1: Summarize session signals

Re-read the full conversation. For each domain touched (e.g., React, System Design, SQL, General Reasoning), extract:

1. **Thinking Check scores** — the Specificity, Ownership, and Diagnostic scores from each evaluated prompt, grouped by domain
2. **Prompt precision** — for each domain, note whether the user was decisive and specific (green signal), mixed (yellow signal), or vague and delegating (red signal)
3. **Incorrect assumptions** — list anything the user stated as fact that was wrong. For each, note:
   - What they said
   - What is actually true
   - What underlying mental model gap this reveals
4. **Strengths demonstrated** — areas where the user showed clear mastery, made good decisions unprompted, or corrected their own mistakes

### Step 2: Dispatch background agent

Spawn a single background Agent (`run_in_background: true`) with the following prompt structure. Include ALL of the signal data from Step 1 directly in the agent prompt — the agent has no access to this conversation.

The agent prompt must instruct it to:

1. **Read the current skills tracker** at `/Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md`

2. **Evaluate and update each domain** touched in the session:
   - If the domain exists in the tracker: update status, diagnostic, and actionable gap based on new evidence combined with existing evidence. Do not overwrite existing evidence — synthesize.
   - If the domain is new: create a new `### Domain` section under `## Skills`.
   - If a broad domain now has 3+ interactions across distinct sub-topics: split into sub-domain headers (e.g., `### React` becomes `### React` with `#### React Hooks`, `#### React State Management`).
   - Adjust status (green/yellow/red) based on accumulated evidence, not single interactions.

3. **Write domain-specific diagnostics** — not generic assessments. Each domain gets a diagnostic label appropriate to that domain:
   - System Design: **Scale Blind Spots**, **Tradeoff Analysis**
   - React / Frontend: **Thinking Mistakes**, **Mental Model Gaps**
   - General Reasoning: **First Principles Gaps**, **Pattern-Matching Errors**
   - Databases: **Query Reasoning**, **Data Modeling Assumptions**
   - Any new domain: choose the most useful diagnostic lens from context
   - Every domain entry must end with a concrete **Actionable Gap** — a specific exercise, study item, or thinking practice. Not "learn more about X" but "do Y with Z constraint."

4. **Update blind spots:**
   - Add new entries to `## Current Blind Spots` if incorrect assumptions reveal a systematic gap (not a one-off mistake)
   - Move entries to `## Resolved Blind Spots` if the session shows corrected understanding. Include the identified date, resolved date, and evidence of resolution.

5. **Update the "Last updated" date** to today's date.

6. **Write the updated tracker** back to the file.

7. **Todoist integration** — ONLY if a new blind spot was added or a domain was newly rated as red:
   - Use `find-projects` to find the project named "claude"
   - Use `add-tasks` to create a task with:
     - `content`: A specific, actionable practice item (e.g., "Design a connection pooling strategy for a 100K-user app — start with pgBouncer docs and calculate max connections per instance given 4 app server replicas")
     - `description`: Context from the session — what the blind spot is, why it matters, what evidence triggered it
     - `projectId`: the "claude" project ID
   - Do NOT create tasks for yellow items, existing entries, or resolved blind spots

### Step 3: Confirm to user

Output only: "Updating skills tracker in the background."

Do not output any other information. Do not wait for the agent to complete. Do not show agent results.

## Rules

- NEVER block the main conversation. The agent runs in the background.
- NEVER show agent results or tracker contents to the user unless they explicitly ask.
- NEVER update the tracker without the user invoking /experience.
- Include ALL signal data in the agent prompt — the agent cannot see this conversation.
- If the session had zero skill signals (only greetings, confirmations, or slash commands), say "No meaningful skill signals in this session — nothing to update." and do not spawn an agent.
```

- [ ] **Step 2: Verify the skill file was created**

Run: `cat /Users/devinat1/.claude/commands/experience.md`
Expected: Full contents from Step 1, starting with the YAML frontmatter.

- [ ] **Step 3: Verify the skill appears in the available skills list**

The skill should now appear in the system reminder's skill list as:
`- experience: Update the skills tracker with diagnostic feedback...`

This can only be verified in a new session or by checking that the file exists at the correct path with correct frontmatter.

Run: `head -4 /Users/devinat1/.claude/commands/experience.md`
Expected:
```
---
name: experience
description: Update the skills tracker with diagnostic feedback from the current session...
---
```

- [ ] **Step 4: Commit**

```bash
git add commands/experience.md
git commit -m "feat: create /experience skill for skills tracker updates"
```

---

### Task 5: End-to-End Verification

This task verifies all components are in place and correctly wired together.

- [ ] **Step 1: Verify all four files exist**

Run: `ls -la /Users/devinat1/.claude/commands/experience.md /Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md /Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/MEMORY.md /Users/devinat1/.claude/CLAUDE.md`
Expected: All four files listed with non-zero sizes.

- [ ] **Step 2: Verify CLAUDE.md has both sections**

Read `/Users/devinat1/.claude/CLAUDE.md` and confirm it contains:
1. The original Thinking Check section (unchanged)
2. The new Skills Tracker reminder section (appended)

- [ ] **Step 3: Verify MEMORY.md points to tracker**

Run: `cat /Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/MEMORY.md`
Expected: Contains a link to `skills_tracker.md`.

- [ ] **Step 4: Verify skills tracker has correct frontmatter**

Run: `head -5 /Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md`
Expected: YAML frontmatter with `name: skills-tracker`, `type: user`.

- [ ] **Step 5: Verify skill frontmatter is parseable**

Run: `head -4 /Users/devinat1/.claude/commands/experience.md`
Expected: Valid YAML frontmatter with `name: experience`.

- [ ] **Step 6: Manual test instruction**

To test the full flow, start a new Claude Code session and:
1. Have a technical conversation (ask about a topic, make some claims)
2. Invoke `/experience`
3. Verify the background agent runs and the tracker file is updated
4. If a blind spot was detected, check Todoist "claude" project for a new task
