#!/usr/bin/env python3
"""Adopt new harness skills into the shared catalog without overwriting conflicts."""
import importlib.util
import json
import os
from pathlib import Path

spec = importlib.util.spec_from_file_location('migration', Path(__file__).with_name('migrate-agentic-home.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def plan(home, root):
    catalog = root / 'skills'
    if not catalog.is_dir() or not (root / 'index.json').is_file():
        raise ValueError('Initialize the shared home before running upkeep')
    groups, errors = {}, []
    visited = set()
    for base in [catalog, *(home / p for p in m.CATALOGS)]:
        if not base.exists():
            if base.is_symlink():
                errors.append(f'Broken catalog link: {base}')
            continue
        if base.resolve() in visited:
            continue
        visited.add(base.resolve())
        for p in sorted(base.iterdir()):
            if p.name.startswith('.') and p.name != '.system':
                continue
            if p.is_symlink() and not p.exists():
                errors.append(f'Broken skill link: {p}')
            elif (p / 'SKILL.md').is_file() or (p.name == '.system' and p.is_dir()):
                groups.setdefault(p.name, set()).add(p.resolve())
            elif p.name in m.BUCKETS and p.is_dir():
                for q in sorted(p.iterdir()):
                    if (q / 'SKILL.md').is_file():
                        groups.setdefault(q.name, set()).add(q.resolve())
    selected = {}
    for name, sources in sorted(groups.items()):
        sources = sorted(sources)
        manifests = [m.digest(p, normalize=True) for p in sources]
        if any(value != manifests[0] for value in manifests[1:]):
            errors.append(f'Content conflict for {name}: ' + ', '.join(map(str, sources)))
        existing = catalog / name
        if existing.exists() and not ((existing / 'SKILL.md').is_file() or (name == '.system' and existing.is_dir())):
            errors.append(f'Catalog destination is occupied by a non-skill: {existing}')
        selected[name] = str(existing.resolve() if existing.exists() else sources[0])
    if errors:
        raise ValueError('Upkeep aborted without changes:\n' + '\n'.join(errors))
    index = json.loads((root / 'index.json').read_text())
    adopt = []
    for name, source in selected.items():
        dest = catalog / name
        resolved = Path(source)
        # Owned repository sources remain links; all other skill content belongs
        # physically inside the catalog. External source repositories stay intact.
        if not m.exists(dest) or (dest.is_symlink() and not resolved.is_relative_to(root)):
            adopt.append(name)
    links = [str(home / p) for p in m.CATALOGS
             if not (home / p).is_symlink() or (home / p).resolve() != catalog.resolve()]
    entries = {name: 'skills/' + name for name in selected if name != '.system'}
    return {'skills': selected, 'adopt': adopt, 'restore_links': links,
            'index_entries': entries, 'refresh_index': index['skills'] != entries}


def run(home, root, apply=False):
    report = plan(home, root)
    summary = {key: report[key] for key in ('adopt', 'restore_links', 'refresh_index')}
    if not apply or not (report['adopt'] or report['restore_links'] or report['refresh_index']):
        return summary
    transaction = m.Transaction(home, root, {'kind': 'skill-upkeep', **summary})
    try:
        for name in report['adopt']:
            source = Path(report['skills'][name])
            target = root / 'skills' / name
            transaction.backup(target)
            if source.is_relative_to(root / 'repos'):
                transaction.link(target, source)
            else:
                transaction.copy(source, target)
        for path in report['restore_links']:
            transaction.link(Path(path), root / 'skills')
        index = json.loads((root / 'index.json').read_text())
        index['skills'] = report['index_entries']
        transaction.write(root / 'index.json', json.dumps(index, indent=2) + '\n')
        # Re-inventory proves adoption is idempotent before committing the journal.
        after = plan(home, root)
        if after['adopt'] or after['restore_links'] or after['refresh_index']:
            raise ValueError('Upkeep did not converge')
        transaction.data['status'] = 'applied'
        transaction.save()
        return {**summary, 'migration_id': transaction.id}
    except BaseException:
        transaction.rollback()
        raise
