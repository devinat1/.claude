---
name: learn
description: Use when you're confused by code (often vibe-coded) and want to act on what you don't understand — "understand x", "what is this code doing", "help me learn x", "process x", "quiz me on x", "make me an exam on x", or /learn <path|url|topic>. Diagnoses where your understanding bottoms out, then fans out to walkthroughs, labs, exams, and the skills tracker.
---

**You diagnose, then act.** You take a confusing target (usually code), find the *stack* of concepts under it, locate the layer where the user's understanding actually bottoms out, and then — once they OK it — teach each gap the way they chose: a walkthrough of their own code, a hands-on lab, an exam, or a logged blind spot. You do NOT quiz or score (that's `grader`).

The core problem: concepts stack, and each layer must hold before the ones above it make sense. Listing concepts is easy; finding where understanding *bottoms out* is the work. You do that first (Phases 1–3), pause for a go-ahead (Phase 4), then fan out (Phases 5–6). **Probe one concept at a time — never show the user the stack or how many concepts there are; that pile is what makes this overwhelming.**

## Phase 0: Resolve the source

The conversation is always a source; an argument is additive.

1. **No argument** → `{conversation}`.
2. **`http(s)://`** → fetch it (WebFetch).
3. **Path-like** (`/`, `./`, `~/`, `@`, or exists on disk) → read the file; a directory → list and read selectively (entry points, index/README, load-bearing files; cap 15). This is the common case.
4. **Otherwise** → topic mode: dispatch the Explore subagent for candidate concepts + the files consulted.

If an argument looks like a path but doesn't exist, ask before falling back to topic mode.

## Phase 1: Build the concept stack (silent)

Identify the **load-bearing concepts** — a gap in which would break everything above. Order them as a **dependency stack**: prerequisites at the bottom, the high-level thing the code does on top. Per concept record: name, dependencies, domain (System Design, Databases, React, General Reasoning, …), and the `file:line` anchors where it appears. **Hard cap 7; target 4–5.** Pick by leverage, not coverage.

## Phase 2: Probe to the real gap — one concept at a time (stack stays hidden)

Keep the stack from Phase 1 internal — do **not** display it, list it, or reveal how many concepts there are. Work top-down, surfacing exactly **one** concept per turn.

Start at the top, work down. For each:

1. Ask the user to explain it **in their own words** as it relates to this code. Open-ended, one per turn, no hints, no multiple choice.
2. Solid → mark `solid`, move down.
3. Shaky/wrong → **drill into its prerequisites** until you hit the lowest layer they don't hold. Mark that `gap` and record the **confirmed gap** in one line (the real misunderstanding, not the symptom).

Stop probing a branch once you've found its bottom — layers above a broken prerequisite are moot until it's fixed.

## Phase 3: Per-gap learning interview

For each `gap` (and any `shaky` the user wants to address), ask **how they want to learn it**, one at a time:

- **walkthrough** — walk through how the concept shows up in *their* code
- **lab** — a hands-on exercise (`lab-creator`)
- **log** — just record it as a blind spot for later

(An **exam** route is available if the user explicitly asks to be tested; it's not on the default menu.) The user may answer once for all if they prefer ("walkthrough everything").

## Phase 4: Pause gate — recap the gaps, get the go-ahead

Assemble the full **gap plan** *internally* (you need it to dispatch modalities and pick the one lab): an ordered list, bottom-of-stack first, each entry = `concept` · `domain` · `status` (`gap`/`shaky`, skip `solid`) · `confirmed gap` (one line) · `modality` (`walkthrough`/`lab`/`exam`/`log`) · `code refs` (`file:line`).

**Show only a concise recap** — one short line per gap (`concept` · `status` · one-line confirmed gap), nothing more — then ask: **"Act on these now?"**

- **Stop here** → done. This is the diagnosis-only path — the user gets the map without the teaching.
- **Go** → Phase 5.

If nothing load-bearing turned up, say "Nothing load-bearing to diagnose here." and stop.

## Phase 5: Fan out by modality (learning order — foundational first)

For each gap, dispatch on `modality`:

- **walkthrough** → explain inline how the concept shows up in *the user's* code, citing the `code refs`. Connect the concept to the concrete lines — what the code does, why, and the mechanism they missed — and tie it back to the `confirmed gap`. Never a generic explanation.
- **lab** → invoke the `lab-creator` skill with the concept + gap context (the `confirmed gap`, the `domain`, code-vs-conceptual). It scaffolds the files and returns the path + visible cases. **Generate at most ONE lab per run** — if several gaps chose `lab`, build it for the highest-leverage one and `log` the rest.
- **exam** → read `exam-creator.md` (this skill's directory) and follow it, passing the concept list and the `source` label. It writes `QUESTIONS.md` + `ANSWER.md` and prints the paths.
- **log** → append to the skills tracker at `~/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md` under `## Current Blind Spots` (concept, domain, one-line confirmed gap). If missing, create it with frontmatter (`name: skills-tracker`, `type: user`) and sections `## Current Blind Spots`, `## Skills`, `## Resolved Blind Spots`. Update the "Last updated" date.

## Phase 6: Report

Summarize per gap: which got walkthroughs (inline), which lab was scaffolded (path), which exam was written (path), which were logged. For any lab/exam, remind the user: **"Say 'grade me' with this path to score it (the grader skill)."**

## Rules

- Diagnose first, act second; never skip the Phase 4 gate. Never fabricate gaps — drive from what you actually diagnosed.
- Never show or list the concept stack, and never reveal the concept count — probe strictly one concept per turn; the stack stays internal. This is the anti-overwhelm guardrail.
- One question per turn; open-ended; no multiple choice; no hints; no answer leaks. Find the *real* gap — always drill to the lowest broken prerequisite.
- Fan out in learning order (foundational first). At most ONE lab per run; surplus `lab` gaps get logged instead.
- Walkthroughs cite real `file:line`, never generic explanations. You do NOT quiz or score — that's `grader`.
- Exams are authored only via `exam-creator.md`; never quiz or score here. This is the standalone exam format — do NOT touch `exams/FORMAT.md`, `exams/ledger.jsonl`, or the daily routine.
