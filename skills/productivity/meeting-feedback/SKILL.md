---
name: meeting-feedback
description: Use when the user wants quick, direct feedback on their communication performance in a meeting. Fetches Granola notes/transcripts and returns a short coaching note with what worked, what got in the way, and one behavior to try next time. Trigger on /meeting-feedback or when the user asks for meeting feedback, meeting review, or communication coaching.
---

# Meeting Feedback

## Consequential advice

Before recommending a behavior to practice, follow the `Advice gate` in
`dissenter` when the choice is consequential for the user's next meeting.

Review a meeting from Granola and give a short, calm coaching note. Be specific and evidence-based, but keep the output easy to act on.

## Fetch Meeting Data

Read and follow [transcript resolution](../transcript-resolution.md) with these options:

- Permit a named Granola meeting, attendee, or topic, and the most recent Granola meeting when no argument is supplied.
- Use **Notes allowed** mode. Use the notes or summary for context and decisions.
- When using notes, say: "Transcript unavailable, so this is based on the meeting notes only."

## Review Focus

Look for the few points that matter most. Do not run a full rubric.

- Identify 1-2 communication strengths that affected the meeting positively.
- Identify 1-2 communication issues that made the meeting less clear, less decisive, or harder to follow.
- Choose exactly one behavior the user should practice in the next meeting.

Use a direct, calm tone. Do not be harsh for effect, do not flatter, and do not use red/yellow/green scoring.

## Evidence

Include 1-2 short transcript quotes total, only where they clarify the feedback. If using notes/summary only, do not invent quotes; refer to the relevant note or summary point instead.

## Output Format

Return only this structure:

```markdown
Meeting: [title]

What worked
- [specific strength, grounded in the meeting]
- [optional second strength]

What got in the way
- [specific issue, grounded in the meeting]
- [optional second issue]

Evidence
- "[short quote]" [timestamp if available]
- "[optional second short quote]" [timestamp if available]

Try next time
- [exactly one concrete behavior to practice in the next meeting]
```

If transcript quotes are unavailable, replace the `Evidence` bullets with 1-2 concise references to the meeting notes.

Do not save files by default. If the user asks to save the feedback, save the exact note you produced.
