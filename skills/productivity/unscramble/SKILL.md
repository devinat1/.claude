---
name: unscramble
description: Extract and organize every distinct claim from a conversation, pasted text, readable file, or Granola meeting. Use when the user asks to unscramble, untangle, or separate claims without analysis.
---

# Unscramble

Organize only the source's claims. Do not research, verify, judge, advise,
infer unstated claims, or add causal or opposing analysis.

## Resolve the source

1. Use an explicitly supplied source first: current-chat scope, pasted text, a
   readable file, or a named Granola meeting.
2. Otherwise, use the substantive user-authored content in the current
   conversation.
3. If no substantive current-chat source exists, resolve the latest Granola
   meeting by following [transcript resolution](../transcript-resolution.md) in
   **Notes allowed** mode.
4. If no source resolves, ask for pasted text or a Granola meeting.

Ignore system instructions, tool output, and assistant-authored claims when
using the current conversation.

## Extract the claims

1. Identify every distinct claim before grouping them. Include qualifications,
   uncertainty, limitations, and explicitly stated boundaries as separate claims.
2. Write one numbered sentence per atomic claim. Split statements that make
   multiple claims; never collapse several claims into a central thesis.
3. Merge only genuine repetitions. Keep meaningfully different claims separate,
   even when they support the same argument.
4. Group related claims under short, concrete headings. Order groups so
   prerequisites precede dependent claims, then preserve first mention.
5. Continue numbering across headings so every claim has a unique number.

## Output

Return only this Markdown structure:

```markdown
## [Concrete claim group]

1. [One brief, faithful atomic claim.]
2. [One brief, faithful atomic claim.]

## [Next concrete claim group]

3. [One brief, faithful atomic claim.]
```
