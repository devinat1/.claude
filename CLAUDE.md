Don't be sycopanthic.

Skills are organized into bucket folders under `skills/`:

- `learning/` — learning loop (diagnose, lab, grade, break-it)
- `engineering/` — code review and repo tooling
- `interview/` — mock interview practice
- `productivity/` — workflow tools (Todoist, Granola, clarification)
- `writing/` — blog workflow
- `setup/` — one-time per-repo configuration

Flat symlinks at `skills/<name>` (e.g. `skills/tdd`) are **local-only** third-party skills installed via skills.sh — they are gitignored and must not be committed.

User-level gate: `rules/safeguard-gate.md` applies in every Claude Code session (projects may add their own copy too).

Every skill in the bucket folders above must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.

After moving or adding owned skills, run `./scripts/link-skills.sh` to refresh flat symlinks in `~/.claude/skills/` for Claude Code.

@RTK.md

## Memory routing

AgentMemory is the sole durable agent-memory system. Recall it only when prior decisions, preferences, known-project context, or earlier work is relevant. Save only stable, reusable facts. Never use Serena memory tools. Use Headroom only to compress unusually large current-session content. Use CodeGraph for codebase structure; if it reports a missing or uninitialized index, run `codegraph init` in that repository before retrying.
