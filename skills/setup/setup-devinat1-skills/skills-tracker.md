# Skills tracker (deprecated)

> **Deprecated:** Learning-loop skills (`learn`, `grader`, `break-it`, `experience`) no longer write to a markdown skills tracker. They log to agent memory via the `user-agentmemory` MCP server instead. See [`agent-memory.md`](./agent-memory.md) and [`agent-memory-logging.md`](../../learning/agent-memory-logging.md).

This file is kept for reference if you maintain a manual tracker outside the learning loop.

## Legacy path

`~/.claude/projects/<project-slug>/memory/skills_tracker.md`

Replace `<project-slug>` with the slug for the current workspace (e.g. `-Users-you--Projects-myapp`).

## Legacy template

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
