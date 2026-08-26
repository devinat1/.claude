---
name: confounder
description: Check an idea's atomic claims for conflated concepts, variables, scopes, or reasoning. Use when the user invokes /confounder or asks whether an idea mixes distinct things together.
---

# Confounder

Expose distinctions that disappear inside an idea. Audit conflation rather
than the idea's overall quality or factual accuracy.

## Resolve the claims

Use the latest `unscramble` output that covers the requested source. If none
exists, say that you are using `/unscramble` to extract the source's atomic
claims, then invoke it. Support every source that skill resolves,
including the current conversation, pasted text, readable files, and Granola
meetings.

If the user added relevant material after the latest `unscramble` output, ask
whether to refresh it. If the user has said `skip questions`, refresh it and
continue.

## Audit the distinctions

Inspect both each atomic claim and the relationships among claims. Flag a
conflation when the idea combines distinct concepts in a way that erases a
relevant difference, or when a conclusion relies on treating them as
interchangeable. A meaningful relationship between two concepts is not by
itself a conflation.

Also detect these separately:

- **Missing bridge:** one claim is used to support another without the
  connecting premise or mechanism.
- **Contradiction:** claims cannot both hold under the same stated conditions.

Name each problem in plain language rather than forcing it into a fixed
taxonomy. Favor surfacing a plausible issue over silently missing it. Give
every finding a confidence of `clear`, `likely`, or `possible`.

Use external research only when domain knowledge is necessary to decide
whether concepts are genuinely distinct. Cite the sources used. Do not expand
this into general fact-checking.

## Resolve ambiguity

When the user's intended distinction is unclear, pause before the final audit
and ask one highest-leverage question at a time. Continue until a faithful
repair is possible.

If the user says `skip questions`, continue with provisional repairs and state
the assumption behind each one.

## Repair faithfully

For every finding:

1. Cite the affected claim numbers.
2. Explain what distinction was lost.
3. Separate the concepts without adding or strengthening claims.
4. Mark the repair provisional when ambiguity remains.

Stop at claim-level repairs. Do not reconstruct the full idea or judge whether
it is good, novel, useful, or viable.

## Final audit

Return these sections:

```markdown
## Claim status

1. clear — [claim]
2. **problematic** — [claim] → Finding 1

## Conflations

### Finding 1: [plain-language label]
- **Claims:** 2, 5
- **Confidence:** likely
- **Explanation:** [what was mixed and why the distinction matters]
- **Repair:** [faithful separated formulation]
- **Assumption:** [only when questions were skipped or ambiguity remains]

## Missing bridges

[Use the same finding fields, or `None detected.`]

## Contradictions

[Use the same finding fields, or `None detected.`]
```

Every extracted claim must appear exactly once in **Claim status**. Give clear
claims only their status; link each problematic claim to every relevant
finding. If a problem section is empty, write `None detected.`
