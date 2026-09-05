---
name: setup-devinat1-skills
description: Sets up an `## Agent skills` block in AGENTS.md/CLAUDE.md and `docs/agents/` so devinat1's skills know the agent memory project ID, blog directory, and MCP integrations. Run before first use of the learning skills, `experience`, `blog`, or `update-blog-refs`.
disable-model-invocation: true
---

# Setup devinat1 Skills

Scaffold the per-repo configuration that these skills assume:

- **Agent memory** — stable project ID for learning skills to scope MCP memories
- **Blog directory** — where `/blog` and `/update-blog-refs` read existing posts
- **MCP integrations** — which optional MCP servers you use (agentmemory, Granola, Todoist)

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state:

- `git remote -v` — identify the repo and derive a default project slug (`owner-repo`)
- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already an `## Agent skills` section?
- `docs/agents/` — does prior setup output already exist?

### 2. Present findings and ask

Summarise what's present and what's missing. Walk the user through three decisions **one at a time**.

**Section A — Agent memory project ID.**

> Explainer: The learning skills recall prior knowledge for routing and personalization. `/dunning-krueger`, `/break-it`, and `/experience` also write learning evidence to the `user-agentmemory` MCP server. They need a stable project slug to scope memories.

Default: `owner-repo` from `git remote get-url origin` (e.g. `devinat1-claude`).

Ask if they want to override the project ID.

**Section B — Blog content directory.**

> Explainer: `/blog` and `/update-blog-refs` read your existing posts to match voice and suggest cross-links.

Default: ask the user for their blog content directory (no default assumed).

**Section C — MCP integrations.**

> Explainer: Some skills use MCP servers. Record which you have so skills know what's available.

Ask about agentmemory (learning skills and experience), Granola (meeting-feedback, momtest), and Todoist (focus, ramble). Options: configured / not configured / not needed.

### 3. Confirm and edit

Show drafts of:

- The `## Agent skills` block for `CLAUDE.md` or `AGENTS.md`
- `docs/agents/agent-memory.md`, `docs/agents/blog-directory.md`, `docs/agents/mcp-integrations.md`

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

### Agent memory

[one-line summary of project ID]. See `docs/agents/agent-memory.md`.

### Blog directory

[one-line summary of blog path]. See `docs/agents/blog-directory.md`.

### MCP integrations

[one-line summary]. See `docs/agents/mcp-integrations.md`.
```

Write `docs/agents/*.md` using the seed templates in this skill folder as starting points:

- [agent-memory.md](./agent-memory.md)
- [blog-directory.md](./blog-directory.md)
- [mcp-integrations.md](./mcp-integrations.md)

Substitute the user's chosen values into the written files.

### 5. Done

Tell the user setup is complete and which skills now read from `docs/agents/*.md`. They can edit those files directly later. Remind them that agentmemory requires `npx @agentmemory/agentmemory@0.9.27` running at `AGENTMEMORY_URL`.
