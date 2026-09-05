#!/usr/bin/env python3
"""Relocate shared agent files with a persistent, reversible operation journal.

Dry runs never write. Duplicate manifests ignore only filesystem caches and the
installation timestamp in agent-native-skill.json. --prefer requires an explicit
source choice; every discarded duplicate remains in the rollback snapshot.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone

CATALOGS = ('.claude/skills', '.codex/skills', '.cursor/skills', '.agents/skills', '.pi/agent/skills')
BUCKETS = ('learning', 'productivity', 'writing', 'setup', 'engineering', 'interview')
ARTIFACTS = ('exams', 'illustrations', 'labs', 'momtest-scorecards', 'plans', 'process-exercises', 'recaps')
CACHES = {'.git', '__pycache__', '.DS_Store', '.codegraph'}


def exists(path):
    return path.exists() or path.is_symlink()


def git(repo, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    return subprocess.check_output(['git', '-C', str(repo), *args], env=env)


def digest(path, normalize=False):
    """Hash an entire tree, including symlink text and executable bits."""
    path = Path(path)
    def entry(p):
        if p.is_symlink():
            return ['link', os.readlink(p)]
        if p.is_dir():
            return ['dir']
        raw = p.read_bytes()
        if normalize and p.name == 'agent-native-skill.json':
            obj = json.loads(raw)
            obj.pop('installedAt', None)
            raw = json.dumps(obj, sort_keys=True).encode()
        return ['file', hashlib.sha256(raw).hexdigest(), p.stat().st_mode & 0o111]
    if not path.is_dir() or path.is_symlink():
        return {'.': entry(path)}
    result = {}
    for directory, dirs, files in os.walk(path, followlinks=False):
        if normalize:
            dirs[:] = [d for d in dirs if d not in CACHES]
            files = [f for f in files if f not in CACHES]
        for name in sorted(dirs + files):
            p = Path(directory) / name
            result[str(p.relative_to(path))] = entry(p)
    return result


def git_state(repo):
    for marker in ('MERGE_HEAD', 'rebase-merge', 'rebase-apply', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'index.lock'):
        p = Path(git(repo, 'rev-parse', '--git-path', marker).decode().strip())
        if not p.is_absolute():
            p = repo / p
        if p.exists():
            raise ValueError(f'Git operation in progress: {p}')
    worktrees = git(repo, 'worktree', 'list', '--porcelain').decode()
    if worktrees.count('worktree ') != 1:
        raise ValueError(f'Additional worktrees: {repo}')
    keys = {
        'head': ('rev-parse', 'HEAD'),
        'refs': ('show-ref',),
        'remotes': ('remote', '-v'),
        'status': ('status', '--porcelain=v1', '-uall'),
        'unstaged': ('diff', '--binary'),
        'staged': ('diff', '--cached', '--binary'),
    }
    return {key: hashlib.sha256(git(repo, *args)).hexdigest() for key, args in keys.items()}


def inventory(home, root, preferences):
    if exists(root):
        raise ValueError(f'Destination occupied: {root}')
    repos = [home / '.claude', home / '.claude/repos/engineering-skills']
    states = {str(p): git_state(p) for p in repos}
    home_instructions = home / 'AGENTS.md'
    if home_instructions.exists() and (not (home / '.claude/AGENTS.md').exists() or home_instructions.read_bytes() != (home / '.claude/AGENTS.md').read_bytes()):
        raise ValueError(f'Merge distinct home instructions into shared config before migration: {home_instructions}')
    groups = {}
    for catalog in CATALOGS:
        base = home / catalog
        if not base.exists():
            continue
        for p in base.iterdir():
            if p.name.startswith('.'):
                continue
            if (p / 'SKILL.md').is_file():
                groups.setdefault(p.name, set()).add(p.resolve())
            elif p.name in BUCKETS and p.is_dir():
                for q in p.iterdir():
                    if (q / 'SKILL.md').is_file():
                        groups.setdefault(q.name, set()).add(q.resolve())
    chosen, conflicts = {}, []
    for name, sources in sorted(groups.items()):
        sources = sorted(sources)
        manifests = [digest(p, normalize=True) for p in sources]
        preference = preferences.get(name)
        if preference:
            source = Path(preference).expanduser().resolve()
            if source not in sources:
                raise ValueError(f'Invalid preferred source for {name}: {source}')
        else:
            source = sources[0]
            if any(m != manifests[0] for m in manifests[1:]):
                keys = set().union(*(set(m) for m in manifests))
                conflicts.append({'name': name, 'sources': list(map(str, sources)),
                                  'files': sorted(k for k in keys if any(m.get(k) != manifests[0].get(k) for m in manifests[1:]))})
        chosen[name] = str(source)
    if conflicts:
        raise ValueError('Skill conflicts; no files moved:\n' + json.dumps(conflicts, indent=2))
    for relative in ('.codex/AGENTS.override.md', '.pi/agent/AGENTS.override.md'):
        p = home / relative
        if p.exists() and p.stat().st_size:
            raise ValueError(f'Global instructions would be shadowed: {p}')
    return {'repositories': states, 'skills': chosen, 'preferences': preferences,
            'retire_duplicate_home_instructions': home_instructions.exists(),
            'artifacts': [str(home / '.claude' / name) for name in ARTIFACTS if exists(home / '.claude' / name)],
            'catalogs': [str(home / c) for c in CATALOGS if exists(home / c)]}


class Transaction:
    def __init__(self, home, root, report, fail_after=0):
        self.home, self.root = home, root
        self.id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:8]
        self.folder = root / 'state/migrations' / self.id
        self.folder.mkdir(parents=True, mode=0o700)
        self.data = {'id': self.id, 'home': str(home), 'root': str(root), 'status': 'applying',
                     'inventory': report, 'operations': []}
        self.fail_after = fail_after
        self.save()

    def save(self):
        path = self.folder / 'manifest.json'
        temporary = path.with_suffix('.tmp')
        with temporary.open('w') as f:
            json.dump(self.data, f, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)

    def operation(self, kind, path, **details):
        op = {'kind': kind, 'path': str(path), **details}
        self.data['operations'].append(op)
        self.save()  # write-ahead journal: a killed process can be rolled back
        if self.fail_after and len(self.data['operations']) == self.fail_after:
            raise RuntimeError('Injected apply failure')
        return op

    def mkdir(self, path):
        if path.exists():
            return
        self.mkdir(path.parent)
        self.operation('create', path)
        path.mkdir()

    def backup(self, path):
        if not exists(path):
            return None
        target = self.folder / 'rollback' / path.relative_to(self.home)
        target.parent.mkdir(parents=True, exist_ok=True)
        self.operation('move', path, backup=str(target), checksum=digest(path))
        path.rename(target)
        return target

    def copy(self, source, target):
        if exists(target):
            raise ValueError(f'Refusing to overwrite {target}')
        self.mkdir(target.parent)
        self.operation('create', target)
        if source.is_symlink():
            target.symlink_to(os.readlink(source))
        elif source.is_dir():
            shutil.copytree(source, target, symlinks=True)
        else:
            shutil.copy2(source, target)
        if digest(source) != digest(target):
            raise ValueError(f'Copy checksum mismatch: {source} -> {target}')

    def write(self, path, content):
        self.backup(path)
        self.mkdir(path.parent)
        self.operation('create', path)
        path.write_text(content)

    def link(self, path, target):
        if path.is_symlink() and path.resolve() == target.resolve():
            return
        self.backup(path)
        self.mkdir(path.parent)
        self.operation('create', path)
        path.symlink_to(os.path.relpath(target, path.parent))

    def rollback(self):
        rollback(self.folder)


def rollback(folder):
    folder = folder.resolve()
    path = folder / 'manifest.json'
    data = json.loads(path.read_text())
    if data['status'] == 'rolled-back':
        return
    # Retain post-migration files instead of deleting potentially newer user work.
    for i, op in reversed(list(enumerate(data['operations']))):
        if op.get('rolled_back'):
            continue
        target = Path(op['path'])
        if op['kind'] == 'create' and exists(target):
            retained = folder / 'reverted-content' / str(i)
            retained.parent.mkdir(parents=True, exist_ok=True)
            target.rename(retained)
        elif op['kind'] == 'move' and exists(Path(op['backup'])):
            if exists(target):
                raise ValueError(f'Rollback conflict at {target}; original retained in {op["backup"]}')
            if digest(Path(op['backup'])) != op['checksum']:
                raise ValueError(f'Rollback snapshot changed: {op["backup"]}')
            target.parent.mkdir(parents=True, exist_ok=True)
            Path(op['backup']).rename(target)
        op['rolled_back'] = True
        path.write_text(json.dumps(data, indent=2) + '\n')
    # Optional overlay records edits made while preparing this migration. Restore
    # their original bytes too, retaining prepared versions beside the snapshot.
    for i, edit in enumerate(data.get('before_edits', [])):
        if edit.get('restored'):
            continue
        target = Path(edit['path'])
        original_bytes = None
        if edit.get('git_blob'):
            blob = edit['git_blob']
            original_bytes = git(Path(blob['repository']), 'show', blob['revision'] + ':' + blob['relative'])
            if hashlib.sha256(original_bytes).hexdigest() != blob['sha256']:
                raise ValueError(f'Original Git content changed: {target}')
        if exists(target):
            if digest(target) != edit['prepared_checksum']:
                raise ValueError(f'Pre-edit restoration conflict: {target}')
            retained = folder / 'prepared-content' / str(i)
            retained.parent.mkdir(parents=True, exist_ok=True)
            target.rename(retained)
        if original_bytes is not None:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(original_bytes)
            target.chmod(edit['mode'])
        elif edit.get('original'):
            original = Path(edit['original'])
            if digest(original) != edit['original_checksum']:
                raise ValueError(f'Pre-edit snapshot changed: {original}')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original, target)
            target.chmod(edit['mode'])
        edit['restored'] = True
        path.write_text(json.dumps(data, indent=2) + '\n')
    data['status'] = 'rolled-back'
    path.write_text(json.dumps(data, indent=2) + '\n')


def apply(home, root, report, fail_after=0):
    t = Transaction(home, root, report, fail_after)
    try:
        main = home / '.claude'
        engineering = main / 'repos/engineering-skills'
        new_main = root / 'repos/skills'
        new_engineering = root / 'repos/engineering-skills'
        # Relocate exact Git databases, not clones: staged/unstaged state survives.
        files = git(main, 'ls-files', '-z', '--cached', '--others', '--exclude-standard').decode().split('\0')
        t.mkdir(new_main)
        for relative in sorted(set(files) - {''}):
            source = main / relative
            if exists(source):
                t.copy(source, new_main / relative)
        eng_backup = t.backup(engineering)
        t.copy(eng_backup, new_engineering)
        git_backup = t.backup(main / '.git')
        t.copy(git_backup, new_main / '.git')
        for old, new in ((main, new_main), (engineering, new_engineering)):
            if git_state(new) != report['repositories'][str(old)]:
                raise ValueError(f'Git state changed during relocation: {old}')
        t.data['git_preserved'] = True
        t.save()

        for repo, buckets in ((new_main, 'learning, productivity, writing, and setup'),
                              (new_engineering, 'engineering, interview, and learning')):
            t.write(repo / 'AGENTS.md', '# Repository maintenance\n\n'
                    f'Owned skills live in the {buckets} buckets under `skills/`.\n'
                    'Every owned skill must appear in the top-level README, its bucket README,\n'
                    'and `.claude-plugin/plugin.json`. Run `./scripts/link-skills.sh` after\n'
                    'adding or moving skills to regenerate metadata and refresh the central catalog.\n'
                    'The shared catalog is `~/.agentic/skills`; local discovery links are ignored.\n'
                    'Keep personal state and credentials out of Git. `settings.json`, when present,\n'
                    'is an installation example; active harness settings remain harness-owned.\n')
            t.link(repo / 'CLAUDE.md', repo / 'AGENTS.md')

        # The catalog also contains managed .system skills and pre-existing broken
        # discovery entries. Preserve them; doctor reports broken entries explicitly.
        t.mkdir(root / 'skills')
        for name, source_text in report['skills'].items():
            source = Path(source_text)
            destination = root / 'skills' / name
            if source.is_relative_to(engineering):
                t.link(destination, new_engineering / source.relative_to(engineering))
            elif source.is_relative_to(main / 'skills') and source.relative_to(main / 'skills').parts[0] in BUCKETS:
                t.link(destination, new_main / source.relative_to(main))
            else:
                t.copy(source, destination)
        for catalog in CATALOGS:
            base = home / catalog
            if not base.exists():
                continue
            for p in base.iterdir():
                target = root / 'skills' / p.name
                if not exists(target) and p.name == '.system' and p.is_dir():
                    t.copy(p, target)

        # Capture old catalogs only after all their shared targets have been read.
        for catalog in CATALOGS:
            t.backup(home / catalog)
        for name in ARTIFACTS:
            old = main / name
            if exists(old):
                saved = t.backup(old)
                t.copy(saved, root / 'artifacts' / name)
            else:
                t.mkdir(root / 'artifacts' / name)
        for old, new in ((home / '.agentmemory', root / 'memory/agentmemory'),
                         (home / '.codex/accountability-beeminder.json', root / 'state/accountability-beeminder.json')):
            if exists(old):
                t.copy(t.backup(old), new)
            elif new.suffix == '.json':
                t.write(new, '{"version": 1, "commitments": []}\n')
            else:
                t.mkdir(new)
        t.mkdir(root / 'state/runs')
        old_workflow = home / '.local/state/dunning-krueger-analysis'
        if exists(old_workflow):
            t.copy(t.backup(old_workflow), root / 'state/dunning-krueger-analysis')
        t.mkdir(root / 'memory/legacy/claude-auto')
        for old in sorted((main / 'projects').glob('*/memory')):
            t.copy(t.backup(old), root / 'memory/legacy/claude-auto' / old.parent.name)

        # Remove only repository-owned top-level paths; native runtime stays put.
        top_levels = {p.split('/')[0] for p in files if p}
        for name in sorted(top_levels - {'skills', 'settings.json', 'repos'}):
            t.backup(main / name)
        t.backup(main / 'AGENTS.md')
        if report.get('retire_duplicate_home_instructions'):
            t.backup(home / 'AGENTS.md')
        config = new_main / 'config/agentic'
        t.link(root / 'config', config)
        t.link(root / 'AGENTS.md', root / 'config/AGENTS.md')
        for relative in ('.claude/CLAUDE.md', '.codex/AGENTS.md', '.pi/agent/AGENTS.md'):
            t.link(home / relative, root / 'AGENTS.md')
        t.link(home / '.cursor/rules/agentic.mdc', root / 'config/harnesses/cursor/agentic.mdc')
        for catalog in CATALOGS:
            t.link(home / catalog, root / 'skills')
        t.link(home / '.local/bin/agentic', new_main / 'scripts/agentic')
        t.link(home / '.agentmemory', root / 'memory/agentmemory')
        # Claude's legacy global gate is a discovery link to a conditional adapter.
        t.link(main / 'rules/safeguard-gate.md', root / 'config/harnesses/claude/rules/safeguard-gate.md')
        settings_path = main / 'settings.json'
        settings = json.loads(settings_path.read_text()) if settings_path.exists() else {}
        settings['autoMemoryEnabled'] = False
        t.write(settings_path, json.dumps(settings, indent=2) + '\n')
        index = make_index(home, root, report, t.id)
        t.write(root / 'index.json', json.dumps(index, indent=2) + '\n')
        verify(home, root)
        t.data['status'] = 'applied'
        t.save()
        return t.id
    except BaseException:
        t.rollback()
        raise


def make_index(home, root, report, migration_id):
    return {
        'schema_version': 1, 'root': str(root),
        'paths': {'instructions': 'AGENTS.md', 'config': 'config', 'skills': 'skills',
                  'artifacts': 'artifacts', 'memory': 'memory/agentmemory', 'runs': 'state/runs',
                  'accountability': 'state/accountability-beeminder.json'},
        'harnesses': {name: {'skills': rel, 'instructions': instructions} for name, rel, instructions in (
            ('claude', '.claude/skills', '.claude/CLAUDE.md'), ('codex', '.codex/skills', '.codex/AGENTS.md'),
            ('cursor', '.cursor/skills', '.cursor/rules/agentic.mdc'), ('agents', '.agents/skills', None),
            ('pi', '.pi/agent/skills', '.pi/agent/AGENTS.md'))},
        'repositories': {'skills': {'path': 'repos/skills', 'origin': git(root / 'repos/skills', 'remote', 'get-url', 'origin').decode().strip()},
                         'engineering-skills': {'path': 'repos/engineering-skills', 'origin': git(root / 'repos/engineering-skills', 'remote', 'get-url', 'origin').decode().strip()}},
        'skills': {name: 'skills/' + name for name in report['skills']},
        'external_resources': {
            'blog': str(home / 'Desktop/blog'), 'blog_content': str(home / 'Desktop/blog/content'),
            'obsidian_state': str(home / 'Documents/State'), 'obsidian_church': str(home / 'Documents/Church'),
            'leetcode_note': str(home / 'Documents/State/Notes/CP/LeetCode Weekly Plan.md'),
            'cold_email_skills': str(home / 'cold-email-ai-skills')},
        'migration': {'id': migration_id, 'manifest': f'state/migrations/{migration_id}/manifest.json'},
    }


def verify(home, root):
    index = json.loads((root / 'index.json').read_text())
    errors, warnings = [], []
    for p, target in ((root / 'AGENTS.md', root / 'config/AGENTS.md'),
                      (root / 'config', root / 'repos/skills/config/agentic'),
                      (home / '.cursor/rules/agentic.mdc', root / 'config/harnesses/cursor/agentic.mdc')):
        if not p.is_symlink() or not p.exists() or p.resolve() != target.resolve():
            errors.append(f'Shared configuration link: {p}')
    for relative in ('.codex/AGENTS.override.md', '.pi/agent/AGENTS.override.md'):
        p = home / relative
        if p.exists() and p.stat().st_size:
            errors.append(f'Global instructions shadowed by {p}')
    schema_path = root / 'config/index.schema.json'
    if schema_path.exists():
        try:
            import jsonschema
            jsonschema.validate(index, json.loads(schema_path.read_text()))
        except ImportError:
            warnings.append('Install jsonschema to validate the index schema')
    for catalog in CATALOGS:
        p = home / catalog
        if not p.is_symlink() or p.resolve() != (root / 'skills').resolve():
            errors.append(f'Catalog link: {p}')
    for relative in ('.claude/CLAUDE.md', '.codex/AGENTS.md', '.pi/agent/AGENTS.md'):
        p = home / relative
        if not p.is_symlink() or p.resolve() != (root / 'AGENTS.md').resolve():
            errors.append(f'Instruction link: {p}')
    for name, relative in index['paths'].items():
        if not (root / relative).exists():
            errors.append(f'Missing indexed path: {name}: {relative}')
    for name, relative in index['skills'].items():
        if not (root / relative / 'SKILL.md').is_file():
            errors.append(f'Missing skill: {name}')
    for name, path in index['external_resources'].items():
        if not Path(path).exists():
            warnings.append(f'External resource unavailable: {name}: {path}')
    for p in (root / 'skills').iterdir():
        if p.is_symlink() and not p.exists():
            warnings.append(f'Pre-existing broken discovery entry: {p.name}')
    if not (home / '.agentmemory').is_symlink() or (home / '.agentmemory').resolve() != (root / 'memory/agentmemory').resolve():
        errors.append('AgentMemory discovery link is incorrect')
    if json.loads((home / '.claude/settings.json').read_text()).get('autoMemoryEnabled') is not False:
        errors.append('Claude auto-memory is enabled')
    for name in ARTIFACTS:
        if exists(home / '.claude' / name):
            errors.append(f'Old artifact path still exists: {name}')
    for name, repo in index['repositories'].items():
        p = root / repo['path']
        if not (p / 'CLAUDE.md').is_symlink() or (p / 'CLAUDE.md').resolve() != (p / 'AGENTS.md').resolve():
            errors.append(f'Repository instruction link: {p}')
        if git(p, 'remote', 'get-url', 'origin').decode().strip() != repo['origin']:
            errors.append(f'Remote changed: {name}')
        subprocess.run(['git', '-C', str(p), 'fsck', '--no-progress'], check=True, stdout=subprocess.DEVNULL)
    print(json.dumps({'errors': errors, 'warnings': warnings, 'skills': len(index['skills'])}, indent=2))
    if errors:
        raise ValueError('Verification failed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--dry-run', action='store_true')
    modes.add_argument('--apply', action='store_true')
    modes.add_argument('--verify', action='store_true')
    modes.add_argument('--rollback', metavar='MIGRATION_ID')
    parser.add_argument('--home', type=Path, default=Path.home(), help='Isolated fixture home for tests')
    parser.add_argument('--prefer', action='append', default=[], metavar='NAME=SOURCE')
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    root = Path(os.environ.get('AGENTIC_HOME', str(home / '.agentic'))).expanduser().absolute()
    if not root.is_relative_to(home) or root == home:
        parser.error('AGENTIC_HOME must be a directory inside the selected home')
    if args.rollback:
        if Path(args.rollback).name != args.rollback or args.rollback in ('.', '..'):
            parser.error('Invalid migration ID')
        rollback(root / 'state/migrations' / args.rollback)
    elif args.verify or (args.apply and (root / 'index.json').exists()):
        verify(home, root)
    else:
        report = inventory(home, root, dict(p.split('=', 1) for p in args.prefer))
        if args.dry_run:
            print(json.dumps(report, indent=2))
        else:
            print('Migration:', apply(home, root, report))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f'error: {error}', file=sys.stderr)
        sys.exit(1)
