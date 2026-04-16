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

## Step 5: Publish (with confirmation)

Ask the user: "Ready to publish with `npx quartz sync`?"

Only if they confirm, run:
```
cd ~/Desktop/blog && npx quartz sync
```

If they decline, let them know the file is saved and they can publish later.
