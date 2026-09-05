# MCP integrations

Optional MCP servers used by some skills in this catalog.

## Agentmemory

**Used by:** `learn`, `socratic-teacher`, `illustrate`, `lab`, `exam`, `dunning-krueger`, `break-it`, `experience`

Recall prior learning context for routing and personalization. Persist evidence-based assessments, load thresholds, and requested session diagnostics via `memory_save` / `memory_recall`.

**Requires:** agentmemory server running at `AGENTMEMORY_URL` (default `http://localhost:3111`). Start with `npx @agentmemory/agentmemory@0.9.27`.

**Status:** optional for learning flow completion — skills report recall or saving failures and continue without a file fallback.

## Granola

**Used by:** `meeting-feedback`, `momtest`

Fetch meeting notes and transcripts for communication audits.

**Status:** optional — skills degrade gracefully if unavailable.

## Todoist

**Used by:** `focus`, `ramble`, `experience`

Search, create, and update tasks.

**Status:** optional — required only if you use those slash commands.
