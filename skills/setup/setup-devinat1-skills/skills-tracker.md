# Skills tracker

The skills tracker is a markdown file where learning skills log blind spots and diagnostic progress.

## Path

`~/.claude/projects/<project-slug>/memory/skills_tracker.md`

Replace `<project-slug>` with the slug for the current workspace (e.g. `-Users-you--Projects-myapp`).

## Template

If the file does not exist, create it with:

```markdown
---
name: skills-tracker
type: user
---

# Skills Tracker

Last updated: YYYY-MM-DD

## Current Blind Spots

## Skills

## Resolved Blind Spots
```

## Consumers

These skills read and write the tracker:

- `learn` — logs blind spots
- `grader` — updates domains after exams/labs
- `break-it` — logs measured load thresholds
- `experience` — session diagnostic updates
