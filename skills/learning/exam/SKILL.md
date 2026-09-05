---
name: exam
description: Generate a complete standalone exam and a separate visible answer key for one confirmed topic. Use when the user asks for an exam, knowledge test, multiple-choice or free-form questions, or selects the exam modality in /learn. It authors files but does not administer or grade them.
---

# Exam

Author an exam and its answer key, then stop.

## Intake

Read [learning context](../learning-context.md). Use a learning brief supplied by
`/learn` as the source; otherwise resolve the current conversation plus any
argument and confirm one topic. In both cases, recall relevant prior knowledge
at invocation and refresh the brief before asking exam setup questions.

Ask these setup questions one at a time:

1. Format: multiple-choice, free-form, or mixed?
2. Length: how many questions?
3. Difficulty: introductory, intermediate, advanced, or a requested mix?

Use recalled knowledge to avoid wasting questions on already-demonstrated
material and to target prior gaps. Continue without personalization after
reporting a recall failure.

## Write the exam

Resolve the destination as:

```text
~/.agentic/artifacts/exams/<repo>/YYYY-MM-DD-<topic-slug>/
```

Append `-2`, `-3`, and so on when needed. Resolve `<repo>` from the git root
basename, then the current directory basename, then `no-repo`.

Create:

- `exam.md` containing the complete exam,
- `answers.md` containing the complete answer key and concise grading criteria.

Make every question answerable from the confirmed scope. Free-form questions
should probe mechanisms, application, limits, or distinctions rather than rote
feature lists. Multiple-choice distractors should represent plausible wrong
models, not word games. Put answers only in `answers.md`; the file is visible and
does not need an unlock step.

Report both absolute paths and a concrete estimated completion time.

## Boundary

This skill does not administer questions, wait for responses, grade answers, or
write to agent memory. At completion, append the configured `exam` suggestions
from [skill connections](../../../docs/skill-connections.md).
