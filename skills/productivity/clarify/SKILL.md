---
name: clarify
description: Explores purpose, constraints, and success criteria through extensive one-at-a-time questioning before any building. Use when the user has a vague idea, says "clarify this", "help me figure out what I want", "what should I build", or wants discovery without a design doc or implementation.
---

# Clarify

Help turn a vague idea into clear requirements through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Keep interviewing until purpose, constraints, and success criteria are thoroughly clear — then output a copy-paste prompt, remind the user to practice it with `/coherent`, and stop.

<HARD-GATE>
Do NOT write code, scaffold projects, propose implementation plans, write design docs, commit specs, or invoke writing-plans. This skill ends with a single copy-pasteable prompt plus one `/coherent` reminder line.
</HARD-GATE>

## Checklist

Complete these in order:

1. **Explore project context** — check files, docs, recent commits
2. **Scope check** — if the request spans multiple independent subsystems, flag it and interview one slice at a time
3. **Ask clarifying questions — extensively, one at a time** — purpose, constraints, success criteria, non-goals, priorities, edge cases, users/audience, what "done" looks like
4. **Stop when thorough** — all three pillars are specific enough to act on, not just stated once
5. **Deliver copy-paste prompt** — one self-contained prompt in a fenced code block, followed by exactly one `/coherent` reminder line; stop

## Question discipline

- **One question per message** — if a topic needs more exploration, break it into multiple questions
- **Multiple choice preferred** when it speeds answers; open-ended is fine when needed
- **Explore the codebase** when a question can be answered from the repo instead of asking the user
- **Go deep on branches** — constraints often hide in edge cases and non-goals

**Extensive bar:** each pillar should survive "what about when…?" Shallow one-liners mean keep asking.

## Scope check

Before detailed questions, assess scope. If the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), flag it immediately. Don't spend questions refining details of a project that needs to be decomposed first.

Help the user pick one slice to clarify now. Other slices get their own clarify session later.

## Drawing the user out

Unlike `grill-me`, do not lead with recommended answers. Draw the user's thinking out with questions. If they are stuck on a specific decision, a short recommendation is fine — then return to asking.

## End artifact

When purpose, constraints, and success criteria are thoroughly clear, your **final message contains only a fenced code block** with a self-contained prompt the user can copy-paste into a new session, followed by this exact line:

```text
Next: run /coherent to practice explaining this clearly.
```

No preamble, no recap, and no other text outside the block.

Weave into the prompt: what to build, why, constraints, success criteria, non-goals, and any unresolved open questions. Write it as instructions to a fresh agent — imperative, specific, complete enough to act on without this conversation's history.

Example shape (adapt to the actual topic):

```
Build [what]. The goal is [purpose].

Constraints:
- [constraint]
- [constraint]

Done when:
- [success criterion]
- [success criterion]

Out of scope:
- [non-goal]

Open questions (resolve if ambiguous):
- [question, if any]
```

No file write. No git commit.

## Key principles

- **YAGNI in questioning** — ask about what matters for the current slice, not every hypothetical feature
- **Incremental clarity** — each answer should sharpen the picture; vague answers get follow-ups
- **Be flexible** — go back and re-ask when something new contradicts an earlier answer
