---
name: learn
description: Route a conversation, path, URL, file, or topic to one focused learning modality. Use when the user wants to learn but has not chosen between a Socratic lesson, interactive illustration, coding lab, or exam. It identifies and confirms the topic, recommends a modality, and hands off without teaching or grading.
---

# Learn

Act as the learning router. Topic selection and modality handoff are the whole
job.

## Choose the topic

Read [learning context](../learning-context.md). Resolve the current conversation
plus any argument and recall relevant agent memory.

Infer a short list of plausible learning topics from user-authored context and
the supplied sources. Keep the list to the fewest distinct topics that explain
the request:

- If one topic is plausible, state it in one line and ask the user to confirm.
- If several are plausible, show the short list and ask the user to choose
  exactly one.
- If none has enough support, ask the user what they want to learn.

Ask one question per turn. Do not infer a knowledge gap from silence or from an
assistant-authored claim.

## Choose the modality

After topic confirmation, present all four choices with equal visual weight and
mark one as `Recommended`:

- `/socratic-teacher` — guided understanding through explanation and
  explain-back.
- `/illustrate` — an interactive map of relationships, terminology, and flow.
- `/lab` — an executable coding exercise with unit tests.
- `/exam` — a complete knowledge test with a separate answer key.

Recommend by the dominant need:

- incomplete understanding or guided reasoning → `/socratic-teacher`
- relationships, flow, terminology, or structure → `/illustrate`
- executable implementation practice → `/lab`
- measurement of existing knowledge → `/exam`

Ask the user to choose. Do not choose on their behalf.

## Hand off

Build the concise learning brief defined in
[learning context](../learning-context.md). Say which selected skill is being
used and why, then invoke it with the brief.

The selected modality owns the workflow and its completion suggestions from
this point. `/learn` does not teach, assess knowledge, grade, create artifacts,
or write knowledge claims to memory.
