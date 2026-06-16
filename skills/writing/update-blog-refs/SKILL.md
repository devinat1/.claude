---
name: update-blog-refs
description: Scan blog posts and suggest related cross-links. Use when the user invokes /update-blog-refs.
disable-model-invocation: true
---

Scan blog posts and suggest related links between them. Follow these steps exactly:

## Step 1: Read all posts

Read every file in the blog content directory from `docs/agents/blog-directory.md` in the current repo (or run `/setup-devinat1-skills` first) except `index.md` and the `images/` directory. For each post, note its title (filename without `.md`) and core topic.

## Step 2: Identify related posts

For each post, identify which other posts are meaningfully related. Two posts are related when:
- They discuss the same tool, system, or concept
- One is a sequel, reference card, or deep dive of another
- They approach the same problem from different angles
- One describes building something the other uses

Posts are NOT related just because they share a broad theme like "AI" or "coding." The connection should be specific enough that a reader of one would genuinely benefit from reading the other.

## Step 3: Check existing related sections

For each post, check whether it already has a `## Related` section at the bottom. Note which posts already have one and what links they contain.

## Step 4: Present proposed changes

Show the user a summary of all proposed changes:
- Posts that need a new `## Related` section added
- Posts with an existing section that should have links added or removed
- Posts with no meaningful connections (these get skipped)

Format each proposal as:
```
**Post Title**
Add: [[Link 1]], [[Link 2]]
Remove: [[Link 3]] (if applicable)
```

Wait for user approval before making any changes.

## Step 5: Apply approved changes

For each approved post, add or update the `## Related` section at the very end of the file, preceded by a horizontal rule:

```
---

## Related
- [[Post Title]]
- [[Another Post Title]]
```

If the post already has a `## Related` section, update it in place rather than adding a duplicate.

## Conventions
- Heading is always `## Related`
- Each link is a bullet with an Obsidian-style `[[wikilink]]`
- No descriptions — just titles
- Bidirectionality is not enforced — each post's list is independent
- Posts with no meaningful connections omit the section entirely
