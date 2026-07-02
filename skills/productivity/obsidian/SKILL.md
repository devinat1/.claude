---
name: obsidian
description: Navigate and write to the State Obsidian vault via CLI for Zettelkasten workflows. Use when the user wants to capture ideas, find notes, read vault context, or mentions Obsidian, State vault, zettels, or MOCs.
---

# Obsidian

Teach agents **when** and **how** to work with the State vault through the Obsidian CLI — not the filesystem.

## Bootstrap

On every session involving vault work:

1. Read [CONFIG.md](CONFIG.md).
2. Use MCP `user-obsidian` → `obsidian_cli` for all vault reads/writes.
3. If CLI calls fail, tell the user Obsidian may not be open with the State vault — do not silently fall back to `Read`/`Write`/`Grep` on `~/Documents/State/`.

CLI syntax and navigation patterns: [REFERENCE.md](REFERENCE.md).

<HARD-GATE>
**Out of scope — use other skills instead:**

- Blog publishing / Quartz sync → `update-blog-on-leetcode`
- Periodic/daily/weekly/monthly notes (`#periodic`, `Periodic/`)
- Literature / Zotero notes (`#literature`, `Literature/`)
- Excalidraw embeds (`![[...excalidraw]]`)
- Running Templater scripts (`<%* ... %>`) or QuickAdd macros
- Editing MOC bodies to list zettels — Dataview handles that in Obsidian UI

**Never** use raw filesystem tools on vault paths when Obsidian CLI is available.
</HARD-GATE>

## When to use Obsidian

| Use Obsidian | Use something else |
|--------------|-------------------|
| Capture an idea, insight, or link as a zettel | Todoist task → `focus` / `ramble` |
| Read existing notes for context on a topic | Meeting analysis → Granola / `meeting-feedback` |
| Find what's already written before building | Prior-art search → `literature-review` |
| Persist knowledge that should live in the graph | Session diagnostics → `experience` |

Trigger when the user mentions Obsidian, State vault, zettels, MOCs, or asks to save/find notes.

## Note-type judgment

No folder-level rules — decide by note type:

| Type | Tag | Agent behavior |
|------|-----|----------------|
| Atomic zettel | `idea` | Create/edit in `Notes/` with full frontmatter |
| Map of Content | `MOC` | Read and navigate; link **to** it from new zettels; don't edit MOC for listing |
| Literature | `literature` | Out of scope |
| Periodic | `periodic` | Out of scope |
| Draft / clipping / file | varies | Read for context if useful; don't apply zettel rules unless asked |

## Workflows

### 1. Read for context

Before answering or building on a topic:

1. `search query="<topic>" path=Notes limit=20`
2. Read promising hits with `read file=<name>`
3. If a MOC exists, `read file=<MOC>` then `backlinks file=<MOC> counts` to find linked zettels
4. Summarize what the vault already says; cite note titles

Ignore Dataview code blocks when reading — they won't execute via CLI.

### 2. Navigate a MOC graph

Dataview on MOC pages is UI-only. Approximate with:

1. Find MOC: search by topic keyword or `#MOC`
2. `backlinks file="<MOC Name>" counts` — zettels linking to this MOC
3. `links file=<zettel>` — outgoing connections
4. `property:read name=related file=<zettel>` — explicit graph edges

See [REFERENCE.md](REFERENCE.md) for full command cheat sheet.

### 3. Create a zettel

Strict template match ([CONFIG.md](CONFIG.md), [REFERENCE.md](REFERENCE.md)):

1. Confirm topic and target MOC (search if unclear; ask one question if ambiguous)
2. `create name="<Title>" path=Notes/ content=<full note with frontmatter>`
3. Set `tags: [idea]`, today's date, `related:` with wikilink to MOC
4. Body content, then `---` and `## References` section
5. **Do not edit the MOC** — linking from the zettel's `related:` is enough; Dataview lists it in Obsidian

Title = filename. One atomic idea per note.

### 4. Edit a zettel

1. `read file=<name>` first — never blind-write
2. Prefer surgical edits: `append`, `prepend`, or `property:set`
3. Preserve existing frontmatter schema and References section
4. When adding a new MOC link, update `related:` on the zettel only

### 5. Capture from conversation

When the user shares an insight worth keeping:

1. Propose a zettel title and MOC placement
2. Show draft frontmatter + body for approval if the edit is substantial
3. Create via CLI after approval (or immediately if user said "save this to Obsidian")

## Rules

- One question at a time when MOC placement or title is ambiguous.
- Search before create — avoid duplicate zettels on the same idea.
- Wikilinks in `related:` use `[[Note Name]]` syntax matching existing vault names.
- Status emoji (🟥🟨🟩) is optional; leave blank if unknown.
- Do not set `publish:` unless the user asks.
