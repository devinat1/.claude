---
name: illustrate
description: Create a reusable interactive diagram that explains one concept, its terminology, connections, flow, and mental model. Use when the user asks to illustrate, visualize, map, or show how a concept fits together. It explains visually but does not grade understanding.
---

# Illustrate

Turn one confirmed topic into a reopenable interactive explanation.

## Intake

Read [learning context](../learning-context.md). Use a learning brief supplied by
`/learn` as the source; otherwise resolve the current conversation plus any
argument and confirm one topic. In both cases, recall relevant prior knowledge
at invocation and refresh the brief before illustrating.

Use recalled knowledge only to choose vocabulary, depth, and which connections
need emphasis. Continue without personalization after reporting a recall
failure.

## Artifact

Create a self-contained HTML artifact under:

```text
~/.claude/illustrations/<repo>/YYYY-MM-DD-<topic-slug>.html
```

Append `-2`, `-3`, and so on when the name already exists. Resolve `<repo>` from
the git root basename, then the current directory basename, then `no-repo`.

The artifact must make these relationships visible:

- the concept's central mental model,
- important terms and their plain-language meanings,
- dependencies, connections, or sequence,
- relevant examples or source excerpts.

Include meaningful interaction such as selecting nodes to reveal explanations,
tracing a flow, switching views, or expanding examples. A static image with
hover labels is insufficient. Keep all CSS and JavaScript inside the HTML so it
can be reopened without a build step or network connection.

Show or open the artifact with the environment's artifact-preview capability
when available, and always report its absolute path.

## Boundary

The artifact explains. It does not quiz, grade, infer mastery, or write to agent
memory.

At completion, append the configured `illustrate` suggestions from
[skill connections](../../../docs/skill-connections.md).
