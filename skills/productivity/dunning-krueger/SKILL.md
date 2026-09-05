---
name: dunning-krueger
description: Assess what knowledge the user demonstrated and which gaps the evidence confirms from the current conversation, supplied context, or completed questions and answers. Use for an evidence-based knowledge assessment or blind-spot check. Reports and persists both strengths and gaps without generating a grill or lesson.
---

# Dunning-Krueger

Assess demonstrated knowledge without diagnosing a cognitive bias. Missing
evidence is not ignorance.

## Evidence

Use the current conversation and any supplied transcript, readable path, exam,
answer key, lab output, questions, or user answers. Read supplied paths before
assessing them.

Treat only user-authored explanations, answers, predictions, and work products
as demonstrations of the user's knowledge. Questions, answer keys, sources,
assistant-authored text, system instructions, and tool output may establish the
reference standard but are not evidence that the user knows it.

For completed questions and answers, compare each user answer with the supplied
reference answer or authoritative source. Do not invent a reference standard
when none is available.

## Evidence gate

The context is sufficient only when it contains user-authored evidence that can
support at least one specific demonstrated strength or confirmed gap against a
known reference.

When evidence is insufficient, say `Not enough evidence to assess your
knowledge.` Name the missing evidence in one line and append the conditional
suggestions for `dunning-krueger` from
[skill connections](../../../docs/skill-connections.md). Stop without saving.

## Assessment

Report both sections:

### Demonstrated knowledge

For each item, name the concept, cite the user's specific evidence, and state
what mechanism or application the evidence demonstrates.

### Confirmed knowledge gaps

For each item, cite the user's specific evidence, state the reference it
conflicts with or omits, and describe the narrow gap. Use `knowledge not
demonstrated` when evidence is absent or unclear; do not promote that label to a
confirmed gap.

Do not add a confidence score, study plan, lesson, or prescription. Report no
gap when the evidence supports none.

## Persist the assessment

Read [agent-memory-logging.md](../../learning/agent-memory-logging.md) and follow
its Dunning-Krueger assessment workflow. Recall related entries first, then save
one discrete memory for each demonstrated strength and confirmed gap. Save a
resolution record when current evidence directly resolves a prior gap.

These assessment records are learning workflow state and are configured for
automatic persistence after a completed evidence-based assessment. If recall or
saving fails, report the failure and keep the assessment result; do not write a
markdown fallback.
