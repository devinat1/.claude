Turn this conversation into a blog post. Follow these steps exactly:

## Step 1: Study existing writing style

Read 3-5 existing posts in `~/Desktop/blog/content/` to learn the user's writing style. Pay attention to:
- Tone (casual vs formal, use of humor, directness)
- Sentence structure and length
- How posts are structured (intro style, use of headings, how they conclude)
- Vocabulary and voice
- Use of code blocks, links, lists, and other formatting

## Step 2: Draft the post

Analyze the conversation and write a blog post draft in markdown **matching the writing style you observed in Step 1**. The post should:
- Sound like the user wrote it, not an AI
- Extract the key insights, learnings, or story from the conversation
- Use proper markdown formatting (headings, code blocks, lists as appropriate)
- Include this frontmatter at the top:

```
---
draft: "false"
---
```

## Step 3: Show the draft for review

Present the full draft to the user. Ask:
- Does the content look good? Any sections to add, remove, or rewrite?
- What should the post title be? (This becomes the filename)

Incorporate all feedback. Repeat this step until the user approves.

## Step 4: Save the file

Save the final post to `~/Desktop/blog/content/<title>.md` where `<title>` is the approved post title.

## Step 5: Update related links

After saving the new post, suggest related links:

1. Read all existing posts in `~/Desktop/blog/content/` (excluding `index.md` and `images/`).
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

## Step 6: Publish (with confirmation)

Ask the user: "Ready to publish with `npx quartz sync`?"

Only if they confirm, run:
```
cd ~/Desktop/blog && npx quartz sync
```

If they decline, let them know the file is saved and they can publish later.
