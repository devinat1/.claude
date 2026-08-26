# Obsidian CLI reference — State and Church vaults

All commands go through MCP `obsidian_cli` with the command string **without** the `obsidian` prefix.

**Prerequisite:** Obsidian must be running and able to access the requested vault. Pass `vault=State` or `vault=Church` explicitly.

## Agentic folder rule

Some agent-managed notes live under `Agentic/` in both vaults. Search `path=Agentic` in the relevant vault before treating a named note as missing. If no vault is specified, search both vaults. Update existing matches in place and never recreate a moved note at its former path or create a duplicate.

## Core commands

| Action | Command | Notes |
|--------|---------|-------|
| Read note | `read file=<name>` | Resolves by wikilink-style name |
| Read by path | `read vault=<State-or-Church> path=Agentic/My Note.md` | Exact Agentic path |
| Search text | `search query=<text> vault=<State-or-Church> path=Agentic limit=20` | Search Agentic first; then other folders as needed |
| Search with context | `search:context query=<text> vault=<State-or-Church> path=Agentic limit=10` | Matching lines |
| List folder | `files vault=<State-or-Church> folder=Agentic` | Agent-managed files in the folder |
| Create note | `create name=<title> vault=<State-or-Church> path=Agentic/ content=<text>` | Use `\n` for newlines in content |
| Append | `append file=<name> content=<text>` | Add to end |
| Prepend | `prepend file=<name> content=<text>` | Add to start |
| Set property | `property:set name=related value="[[MOC Name]]" type=list file=<name>` | YAML frontmatter |
| Read property | `property:read name=tags file=<name>` | Single property |
| Outgoing links | `links file=<name>` | Wikilinks from note |
| Backlinks | `backlinks file=<name> counts` | Notes linking here — key for MOC navigation |
| Tag stats | `tags counts sort=count` | Vault-wide tag counts |
| Tag on file | `tags file=<name>` | Tags for one note |
| File info | `file file=<name>` | Path, dates |
| Delete | `delete file=<name>` | Sends to trash unless `permanent` |
| Help | `help` or `help <command>` | Full command list |

Quote values with spaces: `file="My Note Title"`.

## Navigating Zettelkasten without Dataview

Dataview blocks in MOCs are **human/Obsidian-UI only**. Approximate them with CLI:

### Find MOCs on a topic

```
search query="#MOC" vault=<State-or-Church> path=Agentic limit=20
search query="<topic keyword>" vault=<State-or-Church> path=Agentic limit=20
```

Then `read file=<name>` and check `property:read name=tags` confirms `MOC`.

### List zettels under a MOC

Dataview uses `FROM [[]] AND -#MOC` on the MOC page. CLI equivalent:

```
backlinks file="<MOC Name>" counts
```

Each backlink is a note that wikilinks to the MOC (usually via `related:` frontmatter).

### Find zettels by tag

```
search query="#idea" vault=<State-or-Church> path=Agentic limit=30
tags name=idea counts sort=count
```

Combine with a topic keyword in `search query="<keyword>" vault=<State-or-Church> path=Agentic`; search `path=Notes` afterward only for legacy or explicitly non-Agentic notes.

### Explore a note's graph

```
read file=<name>
links file=<name>
backlinks file=<name>
property:read name=related file=<name>
```

### Avoid broken search queries

- Do **not** use `tags:` operator syntax — Obsidian CLI search rejects it.
- Bracket wikilinks in search (`[[Note]]`) may error — prefer `backlinks` instead.

## Zettel frontmatter template

```yaml
---
tags:
  - idea
aliases:
date: YYYY-MM-DD
status:
publish:
related:
  - "[[Topic MOC]]"
---
```

Body, then:

```markdown
---
## References
- [Source title](url)
```

## Create example (single MCP call)

```
create name="My New Idea" vault=State path=Agentic/ content="---\ntags:\n  - idea\naliases:\ndate: 2026-06-21\nstatus:\npublish:\nrelated:\n  - \"[[Topic MOC]]\"\n---\n\nNote body here.\n\n---\n## References\n- "
```

Prefer `property:set` to patch frontmatter on existing notes instead of rewriting whole files.
