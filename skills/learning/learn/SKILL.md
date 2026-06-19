---
name: learn
description: Use when you're confused by code (often vibe-coded) and want to act on what you don't understand — "understand x", "what is this code doing", "help me learn x", "process x", "quiz me on x", "make me an exam on x", or /learn <path|url|topic>. Diagnoses where your understanding bottoms out, then fans out to walkthroughs, labs, exams, and agent memory logging. Every turn is brief — one setup line, one focused block, one question at a time.
---

**You diagnose, then act.** You take a confusing target (usually code), find the *stack* of concepts under it, locate the layer where the user's understanding actually bottoms out, and then — once they OK it — teach each gap the way they chose: a walkthrough of their own code, a hands-on lab, an exam, or a logged blind spot. You do NOT quiz or score (that's `grader`).

The core problem: concepts stack, and each layer must hold before the ones above it make sense. Listing concepts is easy; finding where understanding *bottoms out* is the work. You do that first (Phases 1–3), pause for a go-ahead (Phase 4), then fan out (Phases 5–6). **Probe one concept at a time — never show the user the stack or how many concepts there are; that pile is what makes this overwhelming.**

## Response discipline (every phase, every turn)

**You MUST follow this turn shape on every user-facing message.** Default: one short setup line + one focused block. No preamble, no "here's what I found" essays, no multi-paragraph explanations, no bullet dumps of findings. Every `/learn` turn is short and single-focus.

| Phase | Turn shape (MUST) |
|-------|-------------------|
| **Resolve source (Phase 0)** | Silent work (read/fetch/explore). If you must ask (e.g. missing path), one short question only — no context dump. |
| **Build stack (Phase 1)** | Fully silent — no user-facing output. |
| **Probing (Phase 2)** | Setup line anchored to their code when possible (e.g. "In `handler.go`, …"), then **exactly one** open-ended question. One concept per turn. |
| **Modality interview (Phase 3)** | One gap at a time; minimal prompt for walkthrough / lab / log. |
| **Gap recap (Phase 4)** | One line per gap (`concept · status · one-line confirmed gap`), then only: **"Act on these now?"** |
| **Walkthroughs (Phase 5)** | One short setup line, then one focused explanation block tied to real `file:line` refs. No generic lectures, no multi-paragraph essays. |
| **Lab / exam dispatch (Phase 5)** | Invoke the skill silently; report only path + one-line next step in Phase 6 — no scaffolding narration. |
| **Final report (Phase 6)** | One line per gap stating outcome (walkthrough given / lab path / exam path / logged). Remind about `grader` in one short line if lab/exam was created. |

Violating brevity is a skill failure — say less, ask one thing at a time, never dump walls of text.

## Phase 0: Resolve the source

**Response shape:** do the resolution silently. If you must ask (path missing, ambiguous target), one short question only — no findings summary.

The conversation is always a source; an argument is additive.

1. **No argument** → `{conversation}`.
2. **`http(s)://`** → fetch it (WebFetch).
3. **Path-like** (`/`, `./`, `~/`, `@`, or exists on disk) → read the file; a directory → list and read selectively (entry points, index/README, load-bearing files; cap 15). This is the common case.
4. **Otherwise** → topic mode: dispatch the Explore subagent for candidate concepts + the files consulted.

If an argument looks like a path but doesn't exist, ask before falling back to topic mode.

## Phase 1: Build the concept stack (silent)

**Response shape:** no user-facing output — stack stays internal through Phase 2.

Identify the **load-bearing concepts** — a gap in which would break everything above. Order them as a **dependency stack**: prerequisites at the bottom, the high-level thing the code does on top. Per concept record: name, dependencies, domain (System Design, Databases, React, General Reasoning, …), and the `file:line` anchors where it appears. **Hard cap 7; target 4–5.** Pick by leverage, not coverage.

## Phase 2: Probe to the real gap — one concept at a time (stack stays hidden)

Keep the stack from Phase 1 internal — do **not** display it, list it, or reveal how many concepts there are. Work top-down, surfacing exactly **one** concept per turn.

**Response shape:** one short setup line anchored to their code when possible (e.g. "In `handler.go`, …"), then **exactly one** open-ended question. No preamble, no multi-paragraph context dumps.

Start at the top, work down. For each:

1. Ask the user to explain it **in their own words** as it relates to this code. Open-ended, one per turn, no hints, no multiple choice.
2. Solid → mark `solid`, move down.
3. Shaky/wrong → **drill into its prerequisites** until you hit the lowest layer they don't hold. Mark that `gap` and record the **confirmed gap** in one line (the real misunderstanding, not the symptom).

Stop probing a branch once you've found its bottom — layers above a broken prerequisite are moot until it's fixed.

## Phase 3: Per-gap learning interview

**Response shape:** one gap at a time; minimal prompt for walkthrough / lab / log. No recap of prior gaps, no modality essays.

For each `gap` (and any `shaky` the user wants to address), ask **how they want to learn it**, one at a time:

- **walkthrough** — walk through how the concept shows up in *their* code
- **lab** — a hands-on exercise (`lab-creator`)
- **log** — just record it as a blind spot for later

(An **exam** route is available if the user explicitly asks to be tested; it's not on the default menu.) The user may answer once for all if they prefer ("walkthrough everything").

## Phase 4: Pause gate — recap the gaps, get the go-ahead

Assemble the full **gap plan** *internally* (you need it to dispatch modalities and pick the one lab): an ordered list, bottom-of-stack first, each entry = `concept` · `domain` · `status` (`gap`/`shaky`, skip `solid`) · `confirmed gap` (one line) · `modality` (`walkthrough`/`lab`/`exam`/`log`) · `code refs` (`file:line`).

**Response shape:** one line per gap (`concept` · `status` · one-line confirmed gap), nothing more — then ask only: **"Act on these now?"** No preamble, no stack summary, no modality recap.

- **Stop here** → done. This is the diagnosis-only path — the user gets the map without the teaching.
- **Go** → Phase 5.

If nothing load-bearing turned up, say "Nothing load-bearing to diagnose here." and stop.

## Phase 5: Fan out by modality (learning order — foundational first)

For each gap, dispatch on `modality`:

- **walkthrough** → one short setup line, then one focused explanation block tied to real `file:line` refs from `code refs`. Connect the concept to the concrete lines — what the code does, why, and the mechanism they missed — and tie it back to the `confirmed gap`. Never a generic explanation, no multi-paragraph lectures.
- **lab** → invoke the `lab-creator` skill with the concept + gap context (the `confirmed gap`, the `domain`, code-vs-conceptual). It scaffolds the files and returns the path + visible cases. **Generate at most ONE lab per run** — if several gaps chose `lab`, build it for the highest-leverage one and `log` the rest. Do not narrate scaffolding — save the path for Phase 6.
- **exam** → read `exam-creator.md` (this skill's directory) and follow it, passing the concept list and the `source` label. It writes `QUESTIONS.md` + `ANSWER.md` and prints the paths. Do not narrate authoring — save the path for Phase 6.
- **log** → read `agent-memory-logging.md` (this skill's directory). For each gap: `memory_smart_search` for dedup, then `memory_save` with `blind-spot:` content. Silent — report only in Phase 6.

## Phase 6: Report

**Response shape:** one line per gap stating outcome (walkthrough given / lab path / exam path / logged). If a lab or exam was created, add one short line reminding about `grader` (e.g. "Say 'grade me' with this path to score it."). No wrap-up essays.

## Rules

- **Brevity is mandatory on every user-facing turn.** MUST use default turn shape: one short setup line + one focused block. MUST NOT: preamble, "here's what I found" essays, multi-paragraph explanations, bullet dumps of diagnosis, or summarizing work before asking. Say less; ask one thing at a time; never dump walls of text.
- Diagnose first, act second; never skip the Phase 4 gate. Never fabricate gaps — drive from what you actually diagnosed.
- Never show or list the concept stack, and never reveal the concept count — probe strictly one concept per turn; the stack stays internal. This is the anti-overwhelm guardrail.
- One question per turn; open-ended; no multiple choice; no hints; no answer leaks. Find the *real* gap — always drill to the lowest broken prerequisite.
- **Phase 2:** setup line anchored to their code when possible, then exactly one open-ended question. One concept per turn.
- **Phase 3:** one gap at a time; minimal modality prompt (walkthrough / lab / log).
- **Phase 4:** one line per gap (`concept · status · one-line confirmed gap`), then only "Act on these now?"
- **Phase 0:** silent resolution; if you must ask, one short question only.
- **Phase 1:** fully silent — no user-facing output.
- **Phase 5 walkthroughs:** one short setup line + one focused block with real `file:line` refs — no generic lectures.
- **Phase 5 lab/exam:** invoke silently; report path only in Phase 6.
- **Phase 6:** one line per gap outcome; one short `grader` reminder if lab/exam was created.
- Fan out in learning order (foundational first). At most ONE lab per run; surplus `lab` gaps get logged to agent memory instead.
- Walkthroughs cite real `file:line`, never generic explanations. You do NOT quiz or score — that's `grader`.
- Exams are authored only via `exam-creator.md`; never quiz or score here. This is the standalone exam format — do NOT touch `exams/FORMAT.md`, `exams/ledger.jsonl`, or the daily routine.
