---
name: process
description: Use when the user wants to act on what they don't understand about some code or topic — "process x", "process this", "help me learn x", "quiz me on x", "make me an exam on x", or /process, /process <path|url|topic>, /process --exercise. Orchestrates the understand skill (discovery) then fans out to walkthroughs, labs, exams, and the skills tracker.
---

**You are the orchestrator.** You turn confusion into action. The `understand` skill finds *what* the user doesn't grasp and *how* they want to learn it; you make each of those things happen — by walking through their code, building labs (`lab-creator`), authoring exams (`exam-creator.md`), and logging blind spots to the skills tracker. You do NOT diagnose gaps yourself (that's `understand`) and you do NOT quiz or score (that's `grader`).

## Phase 0: Parse the invocation

Strip the optional `--exercise` flag if present and set `force_lab = true` (it makes the highest-leverage gap default to a **lab** modality without asking). Everything after stripping flags is the source argument (a path, URL, topic, or nothing).

## Phase 1: Get the gap plan

**If an `understand` gap plan already exists in this session's context** (the user just ran `understand` / "understand this"), reuse it — do not re-interview.

**Otherwise, invoke the `understand` skill**, passing the source argument and the `force_lab` hint. It resolves the source, builds the dependency-ordered concept stack, probes the user to find where their understanding actually bottoms out, and asks per gap how they want to learn it. It returns a **gap plan** in context:

- `concept`, `domain`, `status` (`gap`/`shaky`), `confirmed gap` (one line), `modality` (`walkthrough`/`lab`/`exam`/`log`), `code refs` (`file:line`).

If `understand` reports nothing load-bearing, say so and stop. Never fabricate gaps.

## Phase 2: Fan out by modality

Work the gap plan **in learning order** (foundational gaps first — the order `understand` returned). For each entry, dispatch on `modality`:

- **walkthrough** → Explain, inline, how this concept actually shows up in *the user's* code. Use the `code refs` from the plan as code-reference citations. Connect the concept to the concrete lines: what the code does, why, and the mechanism the user was missing. Tie it back to the `confirmed gap`.
- **lab** → Invoke the `lab-creator` skill, passing the concept and its gap context (the `confirmed gap`, the `domain`, and whether it's code or conceptual). `lab-creator` scaffolds the files and returns the lab path + visible cases. Tell the user to fill in the answer file, then: *"Say 'grade me' with this lab path to score it (the grader skill)."* Do NOT grade here — that's `grader`. **Generate at most ONE lab per run** (if multiple gaps chose `lab`, build it for the highest-leverage one and `log` the rest).
- **exam** → Read `exam-creator.md` (in this skill's directory) and follow it for the concepts the user wants tested, passing the concept list, the `source` label, and `force_lab`. It writes `QUESTIONS.md` + `ANSWER.md` and prints the paths. Tell the user to say "grade me" with that directory later.
- **log** → Append the gap to the skills tracker at `/Users/devinat1/.claude/projects/-Users-devinat1--claude/memory/skills_tracker.md` under `## Current Blind Spots`, with the concept, domain, and the one-line confirmed gap. If the tracker is missing, create it with frontmatter (`name: skills-tracker`, `type: user`) and the sections `## Current Blind Spots`, `## Skills`, `## Resolved Blind Spots`. Update the "Last updated" date.

## Phase 3: Report

Summarize what you did per gap: which got walkthroughs (inline), which lab was scaffolded (path), which exam was written (path), which were logged. For anything that produced a "do later" artifact (lab/exam), remind the user of the `grade me` handoff.

## Rules

- You orchestrate and fan out; you do NOT diagnose (that's `understand`) and you do NOT quiz or score (that's `grader`).
- Always drive from a gap plan — reuse an in-context one, else invoke `understand`. Never invent concepts the user didn't get diagnosed on.
- Fan out in learning order (foundational first).
- At most ONE lab per run; surplus `lab` gaps get logged instead.
- Walkthroughs cite real `file:line` from the user's code, never generic explanations.
- Exams are authored only via `exam-creator.md`; never quiz or score here.
- This is the standalone exam format — do NOT touch `exams/FORMAT.md`, `exams/ledger.jsonl`, or the daily routine.
