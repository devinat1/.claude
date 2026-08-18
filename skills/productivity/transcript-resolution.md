# Transcript Resolution

Use only the source forms enabled by the calling skill. Stop at the first source that resolves.

1. Use a permitted supplied source such as pasted text or a readable file.
2. For a named meeting, attendee, or topic, search Granola for the best match. Ask for clarification only when several meetings are equally plausible.
3. When no source is supplied, fetch the most recent Granola meeting.

For a Granola meeting, prefer its transcript. The calling skill chooses one fallback mode:

- **Notes allowed:** use meeting notes when the transcript is unavailable, label the evidence as notes, and do not present notes as quotes.
- **Transcript required:** treat notes-only results as unresolved and follow the calling skill's missing-transcript instruction.

Record the resolved source title and date, file path, or pasted-text label required by the calling skill. If no permitted source resolves, follow that skill's missing-source instruction.
