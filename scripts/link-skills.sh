#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd -P)"
AGENTIC_ROOT="${AGENTIC_HOME:-$HOME/.agentic}"
python3 "$REPO/scripts/generate-skill-metadata.py"
python3 - "$REPO" "$AGENTIC_ROOT" <<'PY'
import json
import os
from pathlib import Path
import sys
repo, root = map(Path, sys.argv[1:])
catalog = root / 'skills'
if not (root / 'index.json').is_file():
    raise SystemExit('Initialize the shared home with migrate-agentic-home.py first.')
candidates = []
for bucket in ('learning', 'productivity', 'writing', 'setup', 'engineering', 'interview'):
    for skill in sorted((repo / 'skills' / bucket).glob('*/SKILL.md')):
        source = skill.parent.resolve()
        target = catalog / source.name
        if target.exists() and not target.is_symlink():
            raise SystemExit(f'Refusing to replace a real catalog directory: {target}')
        if target.is_symlink() and target.resolve() != source and not target.resolve().is_relative_to(repo):
            raise SystemExit(f'Conflicting skill source: {target}')
        candidates.append((source, target))
index = json.loads((root / 'index.json').read_text())
for source, target in candidates:
    if not target.is_symlink() or target.resolve() != source:
        if target.is_symlink():
            target.unlink()
        target.symlink_to(os.path.relpath(source, target.parent))
    index['skills'][source.name] = 'skills/' + source.name
temporary = root / 'index.json.tmp'
temporary.write_text(json.dumps(index, indent=2) + '\n')
os.replace(temporary, root / 'index.json')
print(f'{len(candidates)} owned skills linked to {catalog}')
PY
