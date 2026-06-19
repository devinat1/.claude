# Agent memory logging

Learning-loop skills (`learn`, `grader`, `break-it`, `experience`) persist blind spots and diagnostics via the **agentmemory** MCP server — not a markdown file.

## MCP server

- **Server:** `user-agentmemory`
- **Tools used:** `memory_save`, `memory_recall`, `memory_smart_search`
- **Prerequisite:** agentmemory server running at `AGENTMEMORY_URL` (default `http://localhost:3111`). Start with `npx @agentmemory/agentmemory`.

Read each tool's schema before calling. Only `content` is required on `memory_save`; always pass `project` for scoping.

## Project slug resolution

Resolve once per run, in order:

1. Read `docs/agents/agent-memory.md` in the current repo (written by `/setup-devinat1-skills`). Use the `project` value from that file.
2. Else run `git remote get-url origin` → normalize to `owner/repo` slug (e.g. `devinat1-claude`). Strip `.git` suffix; replace `/` with `-`.
3. Else sanitize the workspace folder name (lowercase, non-alphanumeric → `-`).

If `/setup-devinat1-skills` has not been run and git remote is unavailable, use step 3 and mention setup in the report.

## Content prefixes

Use these prefixes at the start of `content` so `memory_recall` / `memory_smart_search` can find entries reliably:

| Prefix | Used by | `type` |
|---|---|---|
| `blind-spot:` | learn, grader, experience | `fact` |
| `skills-domain:` | grader, experience | `workflow` |
| `resolved-blind-spot:` | grader, experience | `fact` |
| `metacognition-gap:` | grader (lab calibration) | `fact` |
| `load-threshold:` | break-it | `fact` |

Also set `concepts` (comma-separated concept + domain names) and `files` (comma-separated `file:line` refs) when available.

## Templates

### blind-spot

```
blind-spot: {concept} ({domain}) — {confirmed gap}. Source: {skill} on {source}
```

Example:

```json
{
  "content": "blind-spot: Connection pooling (Databases) — thought pgBouncer was optional at 10K users; pool exhaustion is the first bottleneck. Source: /learn on handler.go",
  "type": "fact",
  "concepts": "Connection pooling,Databases",
  "files": "internal/db/handler.go:42",
  "project": "devinat1-claude"
}
```

### skills-domain

```
skills-domain: {domain} | status: {green|yellow|red} | diagnostic: {label} — {details} | actionable-gap: {concrete exercise}
```

Example:

```json
{
  "content": "skills-domain: Databases | status: red | diagnostic: Query Reasoning — assumes indexes cover all filter columns without checking explain plans | actionable-gap: Run EXPLAIN on the three slowest queries in staging and document which need composite indexes",
  "type": "workflow",
  "concepts": "Databases,Query Reasoning",
  "project": "devinat1-claude"
}
```

### resolved-blind-spot

```
resolved-blind-spot: {concept} ({domain}) — was: {gap}. Evidence: {resolution}. Resolved: {YYYY-MM-DD}
```

### metacognition-gap

```
metacognition-gap: {concept} — over-estimates mastery: predicted {X/N}, passed {Y/N}. Source: /grader lab
```

### load-threshold

```
load-threshold: {concept} (System Design) — measured {throughput} req/s, p99 {latency} at {trigger}. Predicted ceiling: {derived ceiling}
```

## Workflows

### Simple save (learn, break-it)

1. Resolve project slug.
2. For `blind-spot:` entries only: `memory_smart_search` with the concept name. If an equivalent blind spot exists, skip the save and note "already logged".
3. `memory_save` with the appropriate template.
4. On MCP failure: do not fall back to a file. Report that the entry was not persisted and that `npx @agentmemory/agentmemory` may need to be running.

### Recall-then-save (grader, experience background agents)

1. Read this file.
2. Resolve project slug.
3. For each touched domain/concept: `memory_recall` or `memory_smart_search` to gather prior `skills-domain:`, `blind-spot:`, and `resolved-blind-spot:` entries.
4. Synthesize new evidence with prior entries — append-only; do not overwrite or delete prior memories.
5. `memory_save` one entry per discrete update:
   - persistent gaps → `blind-spot:`
   - domain status changes → `skills-domain:`
   - corrected understanding → `resolved-blind-spot:`
   - lab over-confidence → `metacognition-gap:`
6. On MCP failure: report failure in agent output; do not write to any markdown tracker file.

## Dedup rule

Before saving a `blind-spot:`, search with `memory_smart_search` using the concept name. Skip if an existing entry covers the same concept and domain with substantially the same gap.
