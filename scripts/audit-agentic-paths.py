#!/usr/bin/env python3
"""Audit installed skills for obsolete shared-state paths (read-only)."""
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(os.environ.get('AGENTIC_HOME', Path.home() / '.agentic')).expanduser()
STALE = re.compile(r'(?:~|\$\{?HOME\}?|/Users/[^/\s]+)/(?:\.claude|\.codex|\.cursor|\.pi|\.agents)/|/tmp/[A-Za-z][\w-]*(?:/|\.)')
SKIP = {'.git', '__pycache__', '.codegraph', 'node_modules'}
TEXT = {'.md', '.py', '.sh', '.js', '.ts', '.mjs'}


def audit():
    seen, findings, count, managed = set(), [], 0, 0
    for directory, dirs, files in os.walk(ROOT / 'skills', followlinks=True):
        path = Path(directory)
        real = path.resolve()
        if real in seen:
            dirs[:] = []
            continue
        seen.add(real)
        dirs[:] = [name for name in dirs if name not in SKIP]
        if '.system' in path.relative_to(ROOT / 'skills').parts:
            # Codex-managed installers/config helpers must address native discovery.
            managed += sum(Path(name).suffix in TEXT for name in files)
            continue
        for name in files:
            p = path / name
            if p.suffix not in TEXT:
                continue
            count += 1
            for number, line in enumerate(p.read_text(errors='replace').splitlines(), 1):
                if STALE.search(line):
                    findings.append({'path': str(p), 'line': number, 'text': line.strip()})
    return {'files_checked': count, 'managed_integration_files_exempt': managed, 'findings': findings}


if __name__ == '__main__':
    result = audit()
    print(json.dumps(result, indent=2))
    sys.exit(bool(result['findings']))
