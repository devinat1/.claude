---
name: setup-devinat1-skills
description: Sets up an `## Agent skills` block in AGENTS.md/CLAUDE.md and `docs/agents/` so devinat1's skills know the skills tracker path, blog directory, and MCP integrations. Run before first use of `learn`, `grader`, `break-it`, `experience`, `blog`, or `update-blog-refs`.
disable-model-invocation: true
---

# Setup devinat1 Skills

Scaffold the per-repo configuration that these skills assume:

- **Skills tracker** — where learning skills log blind spots and diagnostics
- **Blog directory** — where `/blog` and `/update-blog-refs` read existing posts
- **MCP integrations** — which optional MCP servers you use (Granola, Todoist)

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state:

- `git remote -v` — identify the repo
- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already an `## Agent skills` section?
- `docs/agents/` — does prior setup output already exist?
- `~/.claude/projects/` — note existing project memory directories if relevant

### 2. Present findings and ask

Summarise what's present and what's missing. Walk the user through three decisions **one at a time**.

**Section A — Skills tracker path.**

> Explainer: The learning loop skills (`learn`, `grader`, `break-it`, `experience`) read and write a markdown skills tracker. They need to know where that file lives on your machine.

Default: `~/.claude/projects/<project-slug>/memory/skills_tracker.md` where `<project-slug>` matches the current workspace.

Ask if they want to override the path.

**Section B — Blog content directory.**

> Explainer: `/blog` and `/update-blog-refs` read your existing posts to match voice and suggest cross-links.

Default: ask the user for their blog content directory (no default assumed).

**Section C — MCP integrations.**

> Explainer: Some skills use MCP servers. Record which you have so skills know what's available.

Ask about Granola (meeting-feedback, momtest) and Todoist (overwhelmed, ramble). Options: configured / not configured / not needed.

### 3. Confirm and edit

Show drafts of:

- The `## Agent skills` block for `CLAUDE.md` or `AGENTS.md`
- `docs/agents/skills-tracker.md`, `docs/agents/blog-directory.md`, `docs/agents/mcp-integrations.md`

Let the user edit before writing.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create.

If an `## Agent skills` block already exists, update it in-place — don't append a duplicate.

The block:

```markdown
## Agent skills

### Skills tracker

[one-line summary of tracker path]. See `docs/agents/skills-tracker.md`.

### Blog directory

[one-line summary of blog path]. See `docs/agents/blog-directory.md`.

### MCP integrations

[one-line summary]. See `docs/agents/mcp-integrations.md`.
```

Write `docs/agents/*.md` using the seed templates in this skill folder as starting points:

- [skills-tracker.md](./skills-tracker.md)
- [blog-directory.md](./blog-directory.md)
- [mcp-integrations.md](./mcp-integrations.md)

Substitute the user's chosen paths into the written files.

### 5. Done

Tell the user setup is complete and which skills now read from `docs/agents/*.md`. They can edit those files directly later.
