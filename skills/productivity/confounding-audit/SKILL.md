---
name: confounding-audit
description: Audit a Granola meeting, pasted conversation, research idea, or journal entry for tangled concepts, compound claims, and weak conceptual connections. Use when the user wants to separate what they said, inspect how ideas were linked, or consider both the strongest case for and against a claim without an AI verdict.
---

# Confounding Audit

Turn an idea-rich source into a neutral review the user can evaluate before presenting it to someone else.

## Collect the source

Read and follow [transcript resolution](../transcript-resolution.md) with these options:

- Permit pasted text, a named Granola meeting or topic, and the most recent Granola meeting when no source is supplied.
- Use **Notes allowed** mode.
- If no source resolves, ask the user for pasted text or a Granola meeting.

## Separate the ideas

1. List distinct concepts or variables. Merge only direct synonyms.
2. Split each substantive statement into atomic claims: one proposed relationship, effect, or conclusion per claim.
3. Record each explicit connection between concepts separately from its component claims.
4. For every claim and connection, preserve a short supporting quote or concise source reference.
5. When an explanation combines several concepts, write a minimal restatement that retains only the concepts needed to express its point.

## Pair the interpretations

For each claim and connection, write two brief, independent interpretations:

- **Could hold because:** the strongest mechanism or evidence supplied by the source.
- **Could fail because:** a plausible missing condition, alternative explanation, ambiguity, or unsupported link.

Call these interpretations candidates. Do not treat either as verification, choose a winner, recommend action, research the literature, or make persistent changes.

## Output

Return Markdown only, using this structure:

```markdown
Source: [meeting title/date or “Pasted text”]

## Concepts
- [concept] — [brief source-grounded meaning]

## Claims
### [atomic claim]
Evidence: "[short quote]" [timestamp if available]

Could hold because: [brief interpretation]

Could fail because: [brief interpretation]

Minimal restatement: [only when the source statement bundles concepts]

## Connections
### [concept A] ↔ [concept B]
Source link: "[short quote]" [timestamp if available]

Could hold because: [brief interpretation]

Could fail because: [brief interpretation]

Minimal restatement: [only when useful]
```

Include only material that is distinct and substantive. Preserve uncertainty when the source does not establish direction, mechanism, or scope.
