# Shared agent instructions

Be candid, concrete, and concise. Lead with the next useful action or result.
Use short paragraphs and at most five numbered steps. Give concrete time estimates
for substantial work. End change reports with one short plain-language paragraph
and a concrete way to test the result.

## Start-of-chat goal check

At the first substantive task in each new interactive chat, invoke `goal-check`
before task execution or other startup workflows (including skill-radar).
Read `~/.agentic/skills/goal-check/SKILL.md` if no skill invocation tool exists.
This startup invocation is pre-authorized; ask the goal question, not permission
to use the skill. Follow it once per chat, then continue the original task.

## Memory

AgentMemory is the sole durable agent-memory system. Recall it when prior
decisions, preferences, project context, or earlier work are relevant. Use
Headroom only to compress unusually large current-session content. Use CodeGraph
for code structure; run `codegraph init` in that repository if its index is missing.
Never use Serena memory tools.

Before saving a stable, reusable fact, show a `Proposed memory` with its type and
concise summary. Ask the user to choose personal memory (`devinat1-personal`),
project memory (show its stable ID), or no save. Call `memory_save` only after
that explicit choice. Propose useful durable context; omit transient details.
Workflow state may be saved automatically. Personal facts and preferences still
require approval. Legacy memory archives are read-only evidence, not a second
active memory system; importing them requires the same approval.

## Before building

Use the `safeguard` skill before a non-trivial feature, build, or refactor, and
complete its Build Brief before implementation. Use the harness's skill mechanism
or read `~/.agentic/skills/safeguard/SKILL.md` when it has no invocation tool.
Skip this gate for an already detailed user-provided plan/issue, bounded PR
review comments, or an explicit opt-out. Use `clarify` for bugs with obvious scope.

## Shared storage

`~/.agentic` is the canonical home for shared instructions, installed skills,
skill artifacts, AgentMemory data, workflow state, and shared configuration.
Read `~/.agentic/index.json` to locate repositories and external resources.
Executable helpers honor `AGENTIC_HOME`, defaulting to `$HOME/.agentic`.
Internal index paths are relative to its root; harness discovery paths are
relative to the user's home; external resource paths are absolute.

Save reusable generated files under `artifacts/<kind>/` and temporary multi-step
work under `state/runs/<skill>/<unique-run-id>/`. Keep explicitly checked-in
project artifacts in their repository. Access the blog and Obsidian through the
indexed locations and their existing workflow tools. Use AgentMemory for durable
memory and `state/` for workflow state. Keep credentials, sessions, transcripts,
caches, plugin-managed files, and application databases in their native locations.

All harness skill directories are discovery symlinks to `~/.agentic/skills`.
Owned entries link into `~/.agentic/repos/skills` or its sibling
`engineering-skills`. Update their source once; never mirror catalogs. Run
`~/.agentic/repos/skills/scripts/agentic doctor` to check links and indexed paths.
Only documented harness/application discovery integrations write native harness
locations. Keep private state, credentials, and `index.json` outside Git.
