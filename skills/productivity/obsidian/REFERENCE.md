# Obsidian CLI reference — State vault

All commands go through MCP `obsidian_cli` with the command string **without** the `obsidian` prefix.

**Prerequisite:** Obsidian must be running with the State vault open.

## Core commands

| Action | Command | Notes |
|--------|---------|-------|
| Read note | `read file=<name>` | Resolves by wikilink-style name |
| Read by path | `read path=Notes/My Note.md` | Exact path |
| Search text | `search query=<text> path=Notes limit=20` | Full-text; no tag operator syntax |
| Search with context | `search:context query=<text> path=Notes limit=10` | Matching lines |
| List folder | `files folder=Notes` | All files in folder |
| Create note | `create name=<title> path=Notes/ content=<text>` | Use `\n` for newlines in content |
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
search query="#MOC" path=Notes limit=20
search query="<topic keyword>" path=Notes limit=20
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
search query="#idea" path=Notes limit=30
tags name=idea counts sort=count
```

Combine with topic keyword in `search query="<keyword>" path=Notes`.

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
create name="My New Idea" path=Notes/ content="---\ntags:\n  - idea\naliases:\ndate: 2026-06-21\nstatus:\npublish:\nrelated:\n  - \"[[Topic MOC]]\"\n---\n\nNote body here.\n\n---\n## References\n- "
```

Prefer `property:set` to patch frontmatter on existing notes instead of rewriting whole files.
