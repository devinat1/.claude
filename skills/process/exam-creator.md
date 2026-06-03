# Exam Creator (reference)

This is a reference file for the `process` skill — not a standalone skill. The `process` skill reads it during Phase 2 to author the exam files.

**Role:** Receive a ranked list of load-bearing concepts (produced by `process` Phase 1) and write two files: the questions and a separate reference answer key. Never quiz the user and never score.

## Input (provided in context by `process`)

A ranked concept list. Each item carries:
- `concept` — the concept name
- `correct understanding` — the internal model of a correct answer (goes in ANSWER.md, never in QUESTIONS.md)
- `source category` — misconception / tracker gap / new concept
- `domain` — e.g. System Design, Databases, React, General Reasoning
- `probe type` (optional suggestion) — one of: predict-failure, boring-version, distinguish-from-neighbor, load-bearing-assumption, concrete-instance

Also provided: the `source` label (conversation / `<path>` / `<url>` / `<topic>`) and a `force_lab` boolean hint (default false).

## Step 1: Resolve the exam directory

- `<repo>` = basename of `git rev-parse --show-toplevel` (fallback: basename of the current working directory; final fallback: `no-repo`).
- `<topic-slug>` = short kebab-case slug of the source (e.g. `process-command`); use `conversation` when there is no arg-source.
- Exam dir: `~/.claude/exams/<repo>/YYYY-MM-DD-<topic-slug>/`. Create it (append `-2`, `-3`, … if a dir for the same slug already exists today).

## Step 2: Compose probes

For each concept, write ONE open-ended probe that makes the user think, not recite. Choose a high-leverage probe type:

- **Predict failure mode** — "describe a scenario where this doesn't hold; what assumption breaks?"
- **Concrete instance** — "describe a specific real case where you'd apply this, not a generic one"
- **Boring-version** — "explain this without the jargon — what's the underlying mechanism?"
- **Load-bearing assumption** — "which single claim here, if wrong, breaks the whole thing?"
- **Distinguish from neighbor** — "how is this different from [adjacent concept], and when does the distinction matter?"

Do NOT write definition / list-the-features / name-the-pattern probes. Do NOT use multiple choice. Do NOT leak the answer in the probe.

Assign each probe an internal think-time (used only to sum the total, never written per-question):
- boring-version / distinguish-from-neighbor → ~1–2 min
- predict-failure / load-bearing-assumption / concrete-instance → ~2–4 min

`est_total_min` = sum of the per-probe midpoints, rounded to a whole number.

## Step 3: Write `QUESTIONS.md`

No answers anywhere in this file.

```markdown
---
date: YYYY-MM-DD
source: <conversation | path | url | topic>
concept_count: <N>
est_total_min: <T>
force_lab: <true|false>
---

# Exam — <topic-slug> — YYYY-MM-DD

Estimated time: ~<T> min

## Questions

### Q1  ·  id: <slug>-q1  ·  <domain>
[probe text]

### Q2  ·  id: <slug>-q2  ·  <domain>
[probe text]
```

Question ids use `<topic-slug>-qN`. Keep ids stable — the grader and answer key key off them.

## Step 4: Write `ANSWER.md`

One entry per question id. This is the file the grader scores against.

```markdown
---
date: YYYY-MM-DD
source: <conversation | path | url | topic>
---

# Answer Key — <topic-slug> — YYYY-MM-DD

- **<slug>-q1**: What a 🟢 answer contains — the load-bearing points, plus the concept's correct understanding and the common wrong turn to watch for.
- **<slug>-q2**: ...
```

## Step 5: Report

Print the absolute paths to both files, then tell the user:

> Exam written. Take it later by saying "grade me" with the exam directory path (the grader skill).

Do not grade, do not offer a lab — both happen in the grader skill.

## Rules

- NEVER put answers, hints, or the answer key in `QUESTIONS.md`.
- NEVER quiz or score — you only author files.
- NEVER write a per-question `⏱ ~T min`; the single `Estimated time` line and `est_total_min` are the only time signals.
- This is a standalone exam format — do NOT touch `exams/FORMAT.md`, `exams/ledger.jsonl`, or the daily routine.
