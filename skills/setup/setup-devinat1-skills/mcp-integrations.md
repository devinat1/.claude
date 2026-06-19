# MCP integrations

Optional MCP servers used by some skills in this catalog.

## Agentmemory

**Used by:** `learn`, `grader`, `break-it`, `experience`

Log blind spots, domain diagnostics, and session feedback to long-term memory via `memory_save` / `memory_recall`.

**Requires:** agentmemory server running at `AGENTMEMORY_URL` (default `http://localhost:3111`). Start with `npx @agentmemory/agentmemory`.

**Status:** required for learning-loop logging — skills report failure if unavailable; no file fallback.

## Granola

**Used by:** `meeting-feedback`, `momtest`

Fetch meeting notes and transcripts for communication audits.

**Status:** optional — skills degrade gracefully if unavailable.

## Todoist

**Used by:** `focus`, `ramble`, `experience`

Search, create, and update tasks.

**Status:** optional — required only if you use those slash commands.
