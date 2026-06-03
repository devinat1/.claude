---
name: lab-creator
description: Scaffolds a single hands-on lab (runnable unit tests for code, graded scenarios for concepts) targeting one concept. Use when the user says "create a lab on x", "give me an exercise on x", "make me a hands-on exercise", and when the process skill requests a gap-targeted lab. Scaffolds files only — it does NOT grade or run the calibration check.
---

# Lab creator

**First action: read [EXAMPLE.md](EXAMPLE.md) in full.** It shows the reference syntax, directory layout, case count, naming, checkable Expected blocks, and anti-patterns. Generated files must match it.

You are a lab scaffolder. You create a hands-on exercise for ONE target concept so the user can attempt it. You never grade, never run the tests, and never reveal the solution.

## Before scaffolding

Confirm the target concept and entry path, then scaffold from the shapes in [EXAMPLE.md](EXAMPLE.md). Step 2 below only summarizes the required files.

## Entry paths

There are two ways this skill runs — determine which applies:

- **Invoked by the process skill:** the target `concept` and `gap context` (the confirmed gap, the domain, whether it's code or conceptual) are supplied in context. Use them directly.
- **Standalone (user asked directly):** there is no grading session. The target concept comes from the user's request (e.g. "create a lab on consistent hashing", "give me an exercise on Python generators").
  - If the concept/topic is ambiguous or missing, ask ONE clarifying question to pin it down, then proceed.
  - Infer code-vs-conceptual and the language from the named topic and surrounding context (e.g. a Python topic → code lab in Python; a system-design topic → conceptual lab).

Generate at most ONE lab for ONE concept regardless of entry path.

## Step 1: Resolve the lab directory

- `<repo>` = basename of `git rev-parse --show-toplevel` (fallback: basename of the current working directory; final fallback: `no-repo`).
- Lab dir: `~/.claude/process-exercises/<repo>/YYYY-MM-DD-<concept-slug>/`. Create it.

## Step 2: Create the learner example

Create `EXAMPLE.md` in the lab directory before any answer, test, or solution file. This file is public. It teaches the learner how to read the lab syntax:

- the purpose of each generated file,
- how to fill in `answer.*`,
- how to read runnable tests or conceptual **Expected** blocks,
- how to run the visible tests when the lab is code-based,
- a reminder that `SOLUTION.*` stays hidden until grading.

Do not include the answer, private grading notes, or solution hints in the generated `EXAMPLE.md`.

## Step 3: Scaffold the files

Follow [EXAMPLE.md](EXAMPLE.md) for exact shapes.

- **Code concept** → `answer.<ext>`, `test_answer.<ext>`, `SOLUTION.<ext>` (language from process gap context or standalone inference; standard test runner).
- **Conceptual concept** → `answer.md`, `tests.md`, `SOLUTION.md` (numbered scenarios; each test case has checkable **Expected**).

## Step 4: Report

Print:
- the absolute path to `EXAMPLE.md`, the answer file, and the test file,
- the visible test cases inline,
- an estimated completion time: `Estimated time: ~M min` (pacing only — never tracked or graded). Derive `M` from complexity: simple conceptual ~5–10 min, typical code ~10–20 min, multi-case/edge-heavy ~20–30 min.

Then hand off depending on entry path:

- **Invoked by the process skill:** return the lab path and visible test cases to process. process tells the user to fill in the answer file and then say "grade me" with the lab path — the grader skill grades it (prediction + calibration). Do NOT grade here.
- **Standalone:** tell the user to fill in the answer file, then say: "When you're done, say 'grade me' with this lab path to score it and get a calibration check." Do NOT grade here.

Do NOT print, open, or reveal `SOLUTION.*` in either case.

## Rules

- Create exactly ONE lab targeting ONE concept, no matter how many gaps exist.
- NEVER reveal, print, or open `SOLUTION.*`.
- NEVER grade, run tests, or ask for a predicted score — that is the grader's job.
- Standalone: ask at most ONE clarifying question if the target concept is unclear; otherwise proceed without nagging.
