---
name: blog
description: Convert the current conversation into a focused blog post (clarify scope first, then distill). Use when the user invokes /blog.
disable-model-invocation: true
---

Turn this conversation into a blog post. Follow these steps exactly:

## Blog location

- Repository: `~/Desktop/blog`
- Content: `~/Desktop/blog/content`

Use these paths directly; do not require per-repo blog-directory setup.

## Step 1: Clarify post scope

Read and follow [`skills/productivity/clarify/SKILL.md`](../productivity/clarify/SKILL.md) to interview the user before drafting.

### Clarify adaptation

Follow clarify's **interview discipline** only:

1. Explore project context — check files, docs, recent commits
2. Scope check — if the conversation spans multiple independent threads, flag it and clarify one slice at a time
3. Ask clarifying questions — extensively, one at a time — purpose, constraints, success criteria, non-goals, audience, what "done" looks like
4. Stop when thorough — all three pillars are specific enough to act on

**Do not** follow clarify's HARD-GATE or end artifact. Do not output a copy-paste prompt. Do not stop after clarify. Do not draft during this phase.

Focus questions on: the single narrative thread, audience, angle, and what to include vs exclude from the conversation.

## Step 2: Summarize and gate

When clarify is thorough, present a brief summary:

- **Topic** — the one thing this post is about
- **Include** — what belongs in the post
- **Exclude** — what to leave out (even if it appeared in the conversation)
- **Shape** — intended structure or angle

Wait for explicit yes/no before proceeding. If the user says no, revise the summary or return to Step 1.

## Step 3: Study existing writing style

Read 3-5 existing posts from the blog content directory above to learn the user's writing style. Pay attention to:
- Tone (casual vs formal, use of humor, directness)
- Sentence structure and length
- How posts are structured (intro style, use of headings, how they conclude)
- Vocabulary and voice
- Use of code blocks, links, lists, and other formatting

## Step 4: Draft the post

Write a blog post draft in markdown **matching the writing style you observed in Step 3** and **the scope agreed in Steps 1–2**. The post should:
- Sound like the user wrote it, not an AI
- Follow one narrative thread — do not dump the full conversation
- Use proper markdown formatting (headings, code blocks, lists as appropriate)
- Include this frontmatter at the top:

```
---
draft: "false"
---
```

### Distill rules

Structure comes from existing posts (style-adaptive), but length and completeness do not mirror the conversation. A good post tells one story — e.g. the problem, the key design choice, one concrete example — not a transcript.

**Include:**
- One narrative thread agreed in clarify
- Core insight or story and key design decisions
- At most one concrete illustration where it earns its keep

**Exclude (even if in the conversation):**
- Implementation minutiae (file paths, configs, exact commands, full code listings)
- Side threads and tangents
- Step-by-step replay of how the chat unfolded

### Ponytail review gate

After drafting, invoke `$ponytail:ponytail-review` on the post. Apply valid `delete` and `shrink` findings, then review again until it reports `Lean already. Ship.` Do not show the draft, ask the user to act, save, or publish before this gate passes.

## Step 5: Show the draft for review

Present the full draft to the user. Ask:
- Does the content look good? Any sections to add, remove, or rewrite?
- What should the post title be? (This becomes the filename)

Incorporate all feedback. Repeat this step until the user approves.

## Step 6: Save the file

Save the final post to `~/Desktop/blog/content/<title>.md`, where `<title>` is the approved post title.

## Step 7: Update related links

After saving the new post, suggest related links:

1. Read all existing posts in the blog content directory above (excluding `index.md` and `images/`).
2. Identify which existing posts are meaningfully related to the new post. Two posts are related when they discuss the same tool/system/concept, one is a sequel or deep dive of another, they approach the same problem from different angles, or one describes building something the other uses. Do not link posts that only share a broad theme.
3. Propose a `## Related` section for the new post listing related existing posts.
4. Propose adding the new post to existing posts' `## Related` sections where it fits.
5. Show all proposals to the user and wait for approval before writing.
6. Apply approved changes. The `## Related` section goes at the very end of each file, preceded by `---`. Format:

```
---

## Related
- [[Post Title]]
```

If an existing post already has a `## Related` section, add the new link to it rather than creating a duplicate section.

## Step 8: Publish (with confirmation)

Ask the user: "Ready to publish with `npx quartz sync`?"

Only if they confirm, run `npx quartz sync` from `~/Desktop/blog`.

If they decline, let them know the file is saved and they can publish later.
