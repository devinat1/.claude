#!/usr/bin/env bash
# Sync ~/.agents/skills from ~/.claude/skills (source of truth).
# Usage: sync-agents-skills-from-claude.sh [--dry-run]
set -euo pipefail

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
fi

CLAUDE="${HOME}/.claude/skills"
AGENTS="${HOME}/.agents/skills"
PRESERVE_POSTIZ=1

python3 - "$CLAUDE" "$AGENTS" "$DRY_RUN" "$PRESERVE_POSTIZ" <<'PY'
import os, sys, shutil
from pathlib import Path
from collections import Counter

CLAUDE = Path(sys.argv[1])
AGENTS = Path(sys.argv[2])
DRY_RUN = sys.argv[3] == "1"
PRESERVE = {"postiz"} if sys.argv[4] == "1" else set()

def entry_kind(path: Path):
    if path.is_symlink():
        return "symlink", os.readlink(path)
    if path.is_dir():
        return "dir", None
    if path.exists():
        return "file", None
    return "missing", None

def resolves_into(path: Path, root: Path) -> bool:
    try:
        rp = path.resolve()
        rr = root.resolve()
        return rp == rr or str(rp).startswith(str(rr) + os.sep)
    except Exception:
        return False

actions = []
claude_names = {p.name for p in CLAUDE.iterdir() if not p.name.startswith(".")}
agents_names = {p.name for p in AGENTS.iterdir() if not p.name.startswith(".")}

for name in sorted(agents_names - claude_names):
    if name in PRESERVE:
        actions.append(("SKIP_PRESERVE", name, "orphan preserved"))
    else:
        actions.append(("DELETE", name, "not in claude"))

for name in sorted(claude_names):
    src = CLAUDE / name
    dst = AGENTS / name
    sk, st = entry_kind(src)
    dk, dt = entry_kind(dst)

    if name in PRESERVE:
        actions.append(("SKIP_PRESERVE", name, "keep real dir (claude points here)"))
        continue

    if sk == "symlink" and resolves_into(src, AGENTS):
        actions.append(("SKIP_EXTERNAL", name, f"claude -> agents; keep agents {dk}"))
        continue

    if sk == "symlink":
        desired = st
        if dk == "symlink" and dt == desired:
            actions.append(("OK", name, f"symlink -> {desired}"))
        else:
            actions.append(("REPLACE_WITH_SYMLINK", name, desired))
    elif sk == "dir":
        desired = str(src.resolve())
        if dk == "symlink":
            try:
                if Path(dst).resolve() == src.resolve():
                    actions.append(("OK", name, f"symlink -> {os.readlink(dst)}"))
                    continue
            except Exception:
                pass
        actions.append(("REPLACE_WITH_SYMLINK", name, desired))
    else:
        actions.append(("COPY_FILE", name, str(src)))

pending = [a for a in actions if a[0] not in ("OK", "SKIP_EXTERNAL", "SKIP_PRESERVE")]
print("=== {} ===".format("DRY-RUN" if DRY_RUN else "APPLY"))
for k, v in sorted(Counter(a[0] for a in actions).items()):
    print(f"  {k}: {v}")
if pending:
    print("Pending:")
    for op, name, detail in pending:
        print(f"  {op:22} {name:40} {detail}")
else:
    preserve_only = [a for a in actions if a[0] == "SKIP_PRESERVE"]
    print("No pending differences.")
    if preserve_only:
        print("Intentionally preserved:")
        for op, name, detail in preserve_only:
            print(f"  {name}: {detail}")

if DRY_RUN:
    sys.exit(0)

AGENTS.mkdir(parents=True, exist_ok=True)
changed = []
for op, name, detail in actions:
    dst = AGENTS / name
    if op == "DELETE":
        if dst.is_symlink() or dst.is_file():
            dst.unlink()
        elif dst.is_dir():
            shutil.rmtree(dst)
        changed.append(f"deleted {name}")
    elif op == "REPLACE_WITH_SYMLINK":
        if dst.is_symlink() or dst.is_file():
            dst.unlink()
        elif dst.exists():
            shutil.rmtree(dst)
        os.symlink(detail, dst)
        changed.append(f"symlink {name} -> {detail}")
    elif op == "COPY_FILE":
        if dst.exists() or dst.is_symlink():
            if dst.is_dir() and not dst.is_symlink():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        shutil.copy2(detail, dst)
        changed.append(f"copied {name}")

print(f"Applied {len(changed)} changes.")
for c in changed:
    print(f"  {c}")
PY
