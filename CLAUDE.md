Don't be sycopanthic. At the end of each response, give me a one paragraph tldr of what happened devoid of jargon. Tell me how to test it briefly, rather than telling me you "finished it".

Skills are organized into bucket folders under `skills/`:

- `learning/` — learning loop (diagnose, lab, grade, break-it)
- `engineering/` — code review and repo tooling
- `interview/` — mock interview practice
- `productivity/` — workflow tools (Todoist, Granola, clarification)
- `writing/` — blog workflow
- `setup/` — one-time per-repo configuration

Flat symlinks at `skills/<name>` (e.g. `skills/tdd`) are **local-only** third-party skills installed via skills.sh — they are gitignored and must not be committed.

Every skill in the bucket folders above must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.

After moving or adding owned skills, run `./scripts/link-skills.sh` to refresh flat symlinks in `~/.claude/skills/` for Claude Code.
