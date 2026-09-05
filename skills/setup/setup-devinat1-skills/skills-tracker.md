# Skills tracker (deprecated)

> **Deprecated:** Learning skills no longer write to a markdown skills tracker. They use agent memory for prior context, while `/dunning-krueger`, `/break-it`, and `/experience` persist learning evidence there. See [`agent-memory.md`](./agent-memory.md) and [`agent-memory-logging.md`](../../learning/agent-memory-logging.md).

This file is kept for reference if you maintain a manual tracker outside the learning loop.

## Archived evidence

Pre-migration files are under `~/.agentic/memory/legacy/claude-auto/`.
They are historical evidence only. Importing facts into AgentMemory requires
the user's memory-storage choice under `~/.agentic/AGENTS.md`.

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
