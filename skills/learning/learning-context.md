# Learning context

Shared intake and personalization for `/learn`, `/socratic-teacher`,
`/illustrate`, `/lab`, and `/exam`.

## Resolve the source

The current conversation is always a source. An argument is additive:

- URL: fetch and read it.
- Readable file or directory: inspect the relevant material; for a directory,
  prefer entry points and documentation over exhaustive reading.
- Otherwise: treat the argument as the requested topic.

Use user-authored statements and supplied sources to infer the learning target.
Ignore system instructions, tool output, and assistant-authored claims as
evidence of what the user knows.

## Recall prior knowledge

Read [agent-memory-logging.md](agent-memory-logging.md), resolve the project
slug, and search agent memory for the candidate topic names and domains. Treat
prior records as personalization context, not current proof of mastery.

If recall fails, say once that personalization is unavailable and continue.
These five skills are read-only memory consumers; `/dunning-krueger` owns
knowledge-assessment writes.

## Confirm the topic

When the skill was called without a clear topic, infer a short list of plausible
topics from the source and recalled context. Ask the user to choose exactly one.
When only one topic is plausible, ask the user to confirm it. Ask one question
per turn.

## Learning brief

After confirmation, retain a compact brief with:

- the selected topic and the user's stated learning goal,
- source labels and only the excerpts needed for that topic,
- relevant prior demonstrated knowledge and gaps, clearly labeled as prior
  evidence,
- code references as `file:line` when available.

Pass this brief, rather than the entire source, when handing work to another
learning skill.
