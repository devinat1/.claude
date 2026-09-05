# Agent memory

Learning skills recall prior knowledge from the `user-agentmemory` MCP server. `/dunning-krueger`, `/break-it`, and `/experience` also persist learning evidence there.

## Project ID

`devinat1-claude`

Replace with a stable slug for this repo (e.g. `owner-repo` from `git remote get-url origin`). Do not use filesystem paths — they change across machines.

## MCP server

- **Server:** `user-agentmemory`
- **URL:** `http://localhost:3111` (set via `AGENTMEMORY_URL` in MCP config)
- **Start server:** `npx @agentmemory/agentmemory@0.9.27`

## Reference

See [`agent-memory-logging.md`](../../learning/agent-memory-logging.md) in the skills catalog for content templates and workflows.
