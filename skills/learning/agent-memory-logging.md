# Agent memory for learning

AgentMemory is the durable store for prior learning evidence.

## Roles

- `/learn`, `/socratic-teacher`, `/illustrate`, `/lab`, and `/exam` recall
  knowledge read-only for routing or personalization.
- `/dunning-krueger` automatically persists demonstrated knowledge, confirmed
  gaps, and directly observed resolutions after a completed assessment.
- `/break-it` persists measured load thresholds.
- `/experience` persists user-requested session diagnostics.

## MCP server

- **Server:** `user-agentmemory`
- **Tools:** `memory_save`, `memory_recall`, `memory_smart_search`
- **Prerequisite:** agentmemory at `AGENTMEMORY_URL` (default
  `http://localhost:3111`). Start it with
  `npx @agentmemory/agentmemory@0.9.27`.

Read each tool's schema before calling it. Always pass `project` for scoping.
On MCP failure, report the failed recall or save and continue without a markdown
fallback.

## Project slug

Resolve once per run:

1. Use the `project` value in `docs/agents/agent-memory.md` when present.
2. Otherwise normalize `git remote get-url origin` to an `owner-repo` slug:
   strip `.git` and replace `/` with `-`.
3. Otherwise sanitize the workspace folder name to lowercase kebab-case.

Mention `/setup-devinat1-skills` when falling back to step 3.

## Content prefixes

| Prefix | Writer | Type |
| --- | --- | --- |
| `demonstrated-knowledge:` | dunning-krueger | `fact` |
| `blind-spot:` | dunning-krueger, experience | `fact` |
| `resolved-blind-spot:` | dunning-krueger, experience | `fact` |
| `skills-domain:` | experience | `workflow` |
| `load-threshold:` | break-it | `fact` |

Set `concepts` to comma-separated concept and domain names and `files` to
comma-separated `file:line` references when available.

## Templates

```text
demonstrated-knowledge: {concept} ({domain}) — {specific mechanism or
application demonstrated}. Evidence: {user-authored evidence}. Source:
/dunning-krueger on {source}
```

```text
blind-spot: {concept} ({domain}) — {confirmed gap}. Evidence: {user-authored
evidence and conflicting reference}. Source: /dunning-krueger on {source}
```

```text
resolved-blind-spot: {concept} ({domain}) — was: {prior gap}. Evidence:
{current user-authored demonstration}. Resolved: {YYYY-MM-DD}
```

```text
skills-domain: {domain} | status: {green|yellow|red} | diagnostic: {label} —
{details} | actionable-gap: {concrete exercise}
```

```text
load-threshold: {concept} (System Design) — measured {throughput} req/s, p99
{latency} at {trigger}. Predicted ceiling: {derived ceiling}
```

## Read-only recall

For routing and personalization:

1. Resolve the project slug.
2. Search candidate concept and domain names with `memory_smart_search`; use
   `memory_recall` when a broader project history is needed.
3. Prefer the newest specific evidence when entries conflict.
4. Label recalled claims as prior evidence. They guide depth and topic choice
   but never prove current mastery.

## Dunning-Krueger assessment workflow

Assessment results are learning workflow state configured for automatic saving.

1. Resolve the project slug.
2. Recall prior `demonstrated-knowledge:`, `blind-spot:`, and
   `resolved-blind-spot:` entries for every assessed concept.
3. Synthesize the current evidence with prior records without overwriting or
   deleting them.
4. Save one discrete record per demonstrated strength and confirmed gap.
5. When current evidence directly demonstrates mastery of a prior gap, also save
   one `resolved-blind-spot:` record.
6. Deduplicate first: skip a new record when an equivalent record already covers
   the same concept, domain, conclusion, and materially similar evidence.

Do not save `knowledge not demonstrated` as a blind spot. Insufficient evidence
produces no assessment memory.

## Recall-then-save for experience

1. Resolve the project slug.
2. Recall prior entries for each touched domain and concept.
3. Synthesize new evidence with prior entries; append rather than overwrite.
4. Save one entry per discrete update using `skills-domain:`, `blind-spot:`, or
   `resolved-blind-spot:`.
5. Deduplicate materially equivalent blind spots before saving.

## Break-it save

After the measured run, save one `load-threshold:` entry containing the concept,
throughput, p99, trigger, and predicted ceiling.
