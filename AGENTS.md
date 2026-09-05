# Repository maintenance

Owned skills live in the learning, productivity, writing, and setup buckets under `skills/`.
Every owned skill must appear in the top-level README, its bucket README,
and `.claude-plugin/plugin.json`. Run `./scripts/link-skills.sh` after
adding or moving skills to regenerate metadata and refresh the central catalog.
The shared catalog is `~/.agentic/skills`; local discovery links are ignored.
Keep personal state and credentials out of Git. `settings.json`, when present,
is an installation example; active harness settings remain harness-owned.
