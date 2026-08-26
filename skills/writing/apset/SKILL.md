---
name: apset
description: Organizes current work into APSET (Area, Problem, System, Evaluation, Takeaway) through a clarify-style interview. Use when the user explicitly asks for an APSET, says "/apset", or says "organize this with APSET".
---

# APSET

## Consequential advice

When the user is stuck on a consequential decision, follow the `Advice gate`
in `dissenter` before giving a recommendation.
When the gate applies, first say that you are using `/dissenter` and why.

Help organize what the user is working on into the APSET format through natural collaborative dialogue.

Start by understanding the current project context, then interview one APSET section at a time. Keep interviewing until each section is concrete enough to act on — then output a brief APSET document and stop.

<HARD-GATE>
Do NOT write code, edit files, scaffold projects, produce implementation plans, write design docs, commit specs, or invoke writing-plans. This skill ends with a brief APSET markdown document in chat.
</HARD-GATE>

## Checklist

Complete these in order:

1. **Explore project context** — check files, docs, recent commits, and the current conversation
2. **Scope check** — if the work spans multiple independent threads, flag it and APSET one slice at a time
3. **Interview one APSET section at a time** — use the core questions below; one question per turn
4. **Threat model when security is relevant** — probe System until actors, assets, trust boundaries, and adversary are concrete
5. **Stop when thorough** — each section survives "what about when…?"; shallow one-liners mean keep asking
6. **Deliver brief APSET doc** — markdown sections in chat; no preamble beyond the doc itself

## Question discipline

Before the first interview question, say that you are using `/clarify`'s
interview style to structure the APSET questions.

Follow the same interview style as [`skills/productivity/clarify/SKILL.md`](../../productivity/clarify/SKILL.md):

- **One question per message** — break multi-part topics across turns
- **Multiple choice preferred** when it speeds answers; open-ended when needed
- **Explore the codebase** when a question can be answered from the repo instead of asking the user
- **Go deep on branches** — gaps and assumptions often hide in edge cases

Do not lead with recommended answers. Draw the user's thinking out with questions. If they are stuck, a short recommendation is fine — then return to asking.

## Core questions

Weave these across the interview (never dump all at once):

1. What is the Problem?
2. What has been done already to address this problem?
3. What is the gap that still remains?
4. How do you propose to address this gap?

## APSET sections

### Area

- **Research work:** the research domain as a single label (e.g. TLS, privacy, blockchain)
- **Non-research work:** scope/context as a single label (e.g. billing, onboarding, harness)

**Length:** one word.

### Problem

Answer: **What is the Problem?**

**Length:** 2–3 sentences — enough to act on, no essays.

### System

Cover:

1. **What has been done already** to address this problem
2. **Threat model** — only when security is relevant to the work

When security is relevant, **create** a threat model here: actors, assets, trust boundaries, adversary capabilities. Do not hunt for or cite external threat-model exemplars. Without a clear threat model, security work fails review — the security relevance won't be clear.

**Length:** 2–3 sentences for what's been done; add a concise threat-model subsection (bullets OK) when applicable.

### Evaluation

Cover:

1. **What gap still remains**
2. **How you propose to address that gap**

**Length:** 2–3 sentences.

### Takeaway

The **single decision or claim** the work hinges on.

**Length:** one sentence.

## End artifact

When all sections are thorough, deliver the APSET document in this shape:

```md
## Area
[one word]

## Problem
[2–3 sentences]

## System
[2–3 sentences on what's been done]

### Threat model
[only when security is relevant — actors, assets, trust boundaries, adversary]

## Evaluation
[2–3 sentences on gap and proposed approach]

## Takeaway
[one sentence]
```

No file write. No git commit. No copy-paste handoff prompt for a new session.
After the APSET document, append the `apset` completion suggestions from
[skill connections](../../../docs/skill-connections.md).

## Non-goals

- Do not fetch or bundle external threat-model examples
- Do not write to Obsidian
- Do not continue into implementation after delivering APSET unless the user starts a new request
- Do not auto-trigger — only when the user explicitly requests an APSET

## Key principles

- **Context first** — use conversation and repo context to avoid redundant questions
- **Incremental clarity** — each answer should sharpen the picture; vague answers get follow-ups
- **Security when relevant** — threat model lives in System, not as a separate research step
- **Be flexible** — go back and re-ask when something new contradicts an earlier answer
