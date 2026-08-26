---
name: linear
description: Convert conversations, current chat context, transcripts, meeting notes, or rough discussions into scoped Linear tickets. Use when the user invokes /linear or asks to turn a conversation into Linear issues, search for existing related tickets, merge context into existing issues, or create reviewed Linear tickets.
---

# Linear

## Consequential advice

Before proposing consequential follow-up work or acceptance criteria as advice
to the user, follow the `Advice gate` in `dissenter`.
When the gate applies, first say that you are using `/dissenter` and why.

Turn the current conversation or a supplied transcript into scoped Linear work, then create or update Linear only after explicit approval.

## Hard Rules

- Require Linear tools. If Linear tools are unavailable, stop and say what is missing.
- Never create, update, comment on, or link Linear issues before the user approves the proposed batch.
- If no transcript is supplied, use the current chat conversation as the source.
- Use `~/.agents` only as installed context if it appears; do not treat it as a source repo.
- Paraphrase transcript context. Do not paste raw transcript excerpts or long quotes into Linear.
- Keep tickets brief and actionable.
- Leave priority, labels, assignee, cycle, estimate, due date, state/status, milestone, and delegate unset unless the user or transcript explicitly provides them.
- Default project to blank. Ask about project during review before creation.
- Infer the Linear team from transcript/context and show the guess during review.

## Linear Tools

Use the Linear MCP/plugin tools when available:

- `list_issues` to search existing work by concise query terms.
- `save_issue` to create or update issues. On create, pass only `title`, `team`, `description`, and `project` when the user approved a project.
- `save_comment` to merge transcript-derived context into existing issues.
- `save_issue` relationship fields such as `parentId`, `blocks`, `blockedBy`, `relatedTo`, `duplicateOf`, and `links` when the approved batch includes relationships.

When passing Markdown to Linear tools, use literal Markdown and real newlines.

## Workflow

1. Identify the transcript source:
   - Use supplied transcript text if present.
   - Otherwise use the current chat.
2. Extract candidate work:
   - Capture explicit requests, decisions, implied follow-up work, unresolved issues, and implementation steps.
   - Ignore pure commentary that does not imply work.
3. Split by clean ownership:
   - Prefer one ticket per clear owner/team.
   - Keep tickets independently actionable.
   - Avoid vague "do the whole feature" tickets.
   - Avoid tiny task spam when one owner can handle the work coherently.
4. For each candidate, infer:
   - Linear team
   - optional project, defaulting to blank
   - whether it is new work, duplicate work, follow-up work, or relationship-only work
5. Search Linear before proposing writes:
   - Use short query terms from the title, product area, bug, feature, and relevant nouns.
   - Search enough to catch obvious duplicates and related issues.
   - Surface strong and weak matches in the review batch.
6. Prepare a review batch and stop for approval.
7. Apply only the approved creates, comments, links, and relationship updates.
8. Return a short summary with Linear identifiers/links and how to verify the changes in Linear.

## Review Batch

Show proposed changes in concise sections:

```md
## Proposed Linear Changes

### Create
| # | Title | Team | Project | Why this is separate | Existing matches |
|---|---|---|---|---|

### Merge Into Existing
| # | Existing issue | Action | Context to add |
|---|---|---|---|

### Relationships
| # | Relationship | Reason |
|---|---|---|

### Clarify
- [Only include if ambiguity affects scope, ownership, project, or acceptance criteria.]
```

For each proposed new issue, include this compact body under the table or in collapsible-style subsections:

```md
Title:
Team:
Project: none | [project]

Summary:
Acceptance criteria:
- ...
Context:
- Paraphrased transcript-derived context.
Dependencies/order:
Open questions:
```

End the review with one approval question, such as:

```md
Approve these Linear changes, or tell me what to drop/edit?
```

Handle edits by updating the review batch and asking again. Proceed only after an explicit approval such as "approved," "create them," or "looks good."

## Duplicate Handling

- Strong existing match: default to merging by comment instead of creating a duplicate.
- Weak existing match: show it and ask whether to merge, link, or create new.
- Related but distinct work: propose a new ticket and add a `relatedTo` link after approval.
- True duplicate after approval: use Linear duplicate relationships only when the user approved that relationship.

## Comments For Existing Issues

When merging transcript-derived context into an existing issue, add a comment rather than rewriting the issue body.

Comment shape:

```md
Transcript context update

Summary:
[Brief paraphrase of the new context.]

Why it matters:
[What changed, became clearer, or was newly requested.]

Suggested acceptance criteria or follow-up:
- [Only include if useful.]

Source:
Current conversation or supplied transcript, summarized by Codex.
```

## New Issue Descriptions

Keep descriptions short:

```md
Summary
[One short paragraph.]

Acceptance criteria
- [Observable outcome]
- [Observable outcome]

Context
[Paraphrased source context. No raw transcript dump.]

Dependencies / order
[Blocking issue, blocked-by issue, parent issue, related issue, or "None known".]

Open questions
- [Only include if needed.]
```

## Clarify Section

If the transcript is too vague to scope safely, include a `Clarify` section in the review batch. Use the clarify skill's style:

Before the first clarification question, say that you are using `/clarify`'s
question style to resolve the ticket's missing decisions.

- Ask concise, decision-shaping questions.
- Prefer one question per unresolved decision.
- Do not block clear tickets just because other tickets need clarification.
- Mark blocked proposals as "needs clarification" instead of creating them.

## Approval And Writes

After approval:

1. Create approved new issues with `save_issue`.
2. Add approved merge comments with `save_comment`.
3. Add approved relationships with `save_issue` update calls.
4. Attach audit trail through Linear comments or links.
5. Return only the created/updated issue identifiers, links when available, and a brief verification note.

Never create test Linear issues unless the user explicitly asks for a real test write.
