---
name: update-blog-on-leetcode
description: Sync LeetCode notes from the State Obsidian vault to the public Quartz blog and deploy. Use when the user says "update blog on leetcode", "publish leetcode notes", or wants coding writeups from Notes/CP live on mydevin.com/blog/coding/.
---

Publish LeetCode problem writeups from the State vault to the Quartz blog.

Some agent-managed notes live under `Agentic/` in both the State and Church vaults. This publishing workflow remains State-only: check `~/Documents/State/Agentic/` before treating a named source note as missing, use any existing moved match in place, and never recreate it under `Notes/CP/` or create a duplicate. Do not publish from the Church vault unless the user explicitly expands the scope.

## Paths

| | Path |
|---|---|
| Source vault | `~/Documents/State/Notes/CP/` |
| Filter | Frontmatter `platform: Leetcode` (~318 files) |
| Destination | `~/Desktop/blog/content/coding/` |
| Migration script | `~/Desktop/blog/scripts/migrate-leetcode.py` |
| Blog repo | `~/Desktop/blog` (branch `v4`) |
| Live site | `mydevin.com/blog/coding/` |

**Excluded:** HackerRank/Codesignal notes, MOC pages, and LeetCode notes outside `Notes/CP/`. Source vault is copy-only — never edit it.

## What the migration script does

For each note with `platform: Leetcode`:

1. Sets `draft: "false"` in frontmatter
2. Strips `![[...excalidraw]]` embeds (Quartz can't render them)
3. Copies to `content/coding/<same-filename>.md`

## Workflow

Run from any directory:

```bash
python3 ~/Desktop/blog/scripts/migrate-leetcode.py
cd ~/Desktop/blog
node ./quartz/bootstrap-cli.mjs sync
```

1. **Migrate** — run the script; note how many files copied and excalidraw lines removed
2. **Review output** — if migration errors, fix source notes and retry
3. **Sync** — `node ./quartz/bootstrap-cli.mjs sync` commits changes, builds, and pushes to `origin/v4`
4. **Report** — tell the user what changed (file count, notable updates) and the live URL pattern (`/coding/<Problem-Name>`)

If migration produces no git changes, sync still runs but will report "Everything up-to-date."

## Section structure

- Landing page: `content/coding/index.md`
- Homepage links to `[[coding/]]` in `content/index.md`
- Quartz auto-generates browsable listings under `/coding/`

## Troubleshooting

- **Script fails on YAML:** fix frontmatter in the source note under `Notes/CP/`
- **Sync conflicts:** resolve in `~/Desktop/blog`, then re-run `node ./quartz/bootstrap-cli.mjs sync`
- **New note not appearing:** confirm `platform: Leetcode` in frontmatter and re-run migration
