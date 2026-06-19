---
name: youtube
description: Writes YouTube-style teleprompter scripts from user-provided context — markdown, line-broken for spoken pacing, with hook and CTA. Use when the user invokes /youtube.
disable-model-invocation: true
---

Turn user-provided context into a spoken YouTube script for teleprompter rehearsal. Generation only — never fetch or parse transcripts from YouTube URLs.

Typical video types: educational/explainer, commentary/opinion, tutorial/walkthrough (often a mix).

## Step 1: Pre-writing question

Before generating any script — even when context looks complete — ask exactly:

> Anything else I should know before writing?

Wait for the answer (or confirmation that nothing else is needed), then proceed.

## Step 2: Draft the script

From the user's context plus their answer:

**Structure**
- Markdown with a section header for each part
- **Hook** at the top and **CTA** at the end — always
- Middle sections flex by video type and context

**Pacing**
- Line-break for teleprompter use: break where a natural spoken pause would land
- One breath-sized phrase per line where it helps readability

**Cues**
- Spoken lines plus light production cues only: `[pause]`, `[emphasis]`, brief section timing notes
- No b-roll, cuts, on-screen text, or visual production notes

**Voice**
- Neutral default
- Honor an optional style note from the user if provided

**Length**
- Infer target length from depth and scope of provided context
- Default cap: ~10 minutes of spoken content (~1,300–1,500 words at ~130–150 wpm) unless the user overrides
- Note the assumed length briefly after the script if helpful

**Output**
- Deliver in chat only — do not save to files unless the user separately asks
- Spoken script only — no title, description, tags, or other metadata

## Step 3: Revision loop

After the first draft, stay in a revision loop. The user gives freeform feedback in plain language. Revise and re-present the **full** updated script each time.

Repeat until the user explicitly approves for rehearsal — e.g. "ready for teleprompter", "good to go", "done". Only then end the workflow.

## Out of scope

- Pulling or parsing transcripts from existing YouTube video URLs
- Title, description, tags, or other YouTube metadata
- Thumbnail, recording, editing, or upload workflows

## Script template

```markdown
# [Working title — internal reference only, not metadata]

## Hook
[Opening lines — line-broken for pacing]
[pause]

## [Section name]
[Body lines]
[emphasis] key phrase [/emphasis]

## [Next section]
...

## CTA
[Closing call-to-action lines]
```
