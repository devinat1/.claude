"""Behavioral migration tests use disposable homes and real dirty Git repos."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('migration', Path(__file__).resolve().parents[1] / 'scripts/migrate-agentic-home.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name).resolve()
        self.root = self.home / '.agentic'
        self.main = self.home / '.claude'
        self.eng = self.main / 'repos/engineering-skills'
        for repo, name in ((self.main, 'skills'), (self.eng, 'engineering-skills')):
            repo.mkdir(parents=True, exist_ok=True)
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            m.git(repo, 'config', 'user.email', 'test@example.invalid')
            m.git(repo, 'config', 'user.name', 'Test')
            m.git(repo, 'remote', 'add', 'origin', f'git@github.com:devinat1/{name}.git')
            (repo / '.gitignore').write_text('repos/\n')
            (repo / 'tracked.txt').write_text('base\n')
            (repo / 'CLAUDE.md').write_text('old repo instructions\n')
            m.git(repo, 'add', '.')
            m.git(repo, 'commit', '-qm', 'initial')
            (repo / 'tracked.txt').write_text('staged\n')
            m.git(repo, 'add', 'tracked.txt')
            (repo / 'tracked.txt').write_text('unstaged\n')
            (repo / 'untracked.txt').write_text('keep me\n')
        config = self.main / 'config/agentic'
        config.mkdir(parents=True)
        (config / 'AGENTS.md').write_text('global\n')
        for p in ('harnesses/cursor/agentic.mdc', 'harnesses/claude/rules/safeguard-gate.md'):
            path = config / p
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('adapter\n')
        self.skill = self.main / 'skills/learning/demo'
        self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('demo\n')
        (self.skill / 'helper.py').write_text('print(1)\n')
        (self.main / 'skills/demo').symlink_to(self.skill)
        duplicate = self.home / '.codex/skills/demo'
        duplicate.mkdir(parents=True)
        for name in ('SKILL.md', 'helper.py'):
            (duplicate / name).write_text((self.skill / name).read_text())
        (self.main / 'exams').mkdir()
        (self.main / 'exams/a.md').write_text('artifact\n')
        (self.main / 'settings.json').write_text('{"effortLevel":"high"}\n')
        memory = self.home / '.agentmemory'
        memory.mkdir()
        (memory / 'standalone.json').write_text('{"keep":"private"}\n')

    def tearDown(self):
        self.temp.cleanup()

    def test_clean_duplicate_dirty_and_idempotent_verification(self):
        report = m.inventory(self.home, self.root, {})
        before = m.digest(self.home)
        self.assertEqual(before, m.digest(self.home))
        migration_id = m.apply(self.home, self.root, report)
        for cat in m.CATALOGS:
            self.assertEqual((self.home / cat).resolve(), self.root / 'skills')
        self.assertEqual((self.root / 'artifacts/exams/a.md').read_text(), 'artifact\n')
        self.assertEqual((self.root / 'repos/skills/untracked.txt').read_text(), 'keep me\n')
        self.assertEqual(m.git(self.root / 'repos/skills', 'diff', '--cached', '--', 'tracked.txt'),
                         b'diff --git a/tracked.txt b/tracked.txt\nindex df967b9..19d9cc8 100644\n--- a/tracked.txt\n+++ b/tracked.txt\n@@ -1 +1 @@\n-base\n+staged\n')
        m.verify(self.home, self.root)
        self.assertTrue(json.loads((self.root / 'state/migrations' / migration_id / 'manifest.json').read_text())['git_preserved'])
        m.rollback(self.root / 'state/migrations' / migration_id)
        after = m.digest(self.home)
        after = {k: v for k, v in after.items() if k != '.agentic' and not k.startswith('.agentic/')}
        self.assertEqual(before, after)

    def test_conflicting_helper_aborts_without_writes(self):
        (self.home / '.codex/skills/demo/helper.py').write_text('print(2)\n')
        before = m.digest(self.home)
        with self.assertRaisesRegex(ValueError, 'helper.py'):
            m.inventory(self.home, self.root, {})
        self.assertEqual(before, m.digest(self.home))

    def test_explicit_preference_resolves_conflict(self):
        (self.home / '.codex/skills/demo/helper.py').write_text('print(2)\n')
        report = m.inventory(self.home, self.root, {'demo': str(self.skill)})
        self.assertEqual(report['skills']['demo'], str(self.skill))

    def test_interrupted_apply_restores_originals(self):
        before = m.digest(self.home)
        report = m.inventory(self.home, self.root, {})
        with self.assertRaisesRegex(RuntimeError, 'Injected'):
            m.apply(self.home, self.root, report, fail_after=24)
        after = {k: v for k, v in m.digest(self.home).items() if k != '.agentic' and not k.startswith('.agentic/')}
        self.assertEqual(before, after)

    def test_occupied_destination_aborts(self):
        self.root.mkdir()
        with self.assertRaisesRegex(ValueError, 'occupied'):
            m.inventory(self.home, self.root, {})

    def test_second_apply_is_read_only(self):
        report = m.inventory(self.home, self.root, {})
        m.apply(self.home, self.root, report)
        before = m.digest(self.home)
        subprocess.run(['python3', str(Path(m.__file__)), '--apply', '--home', str(self.home)], check=True, capture_output=True)
        self.assertEqual(before, m.digest(self.home))

    def test_preparation_overlay_restores_original_git_bytes(self):
        report = m.inventory(self.home, self.root, {})
        migration_id = m.apply(self.home, self.root, report)
        folder = self.root / 'state/migrations' / migration_id
        path = folder / 'manifest.json'
        data = json.loads(path.read_text())
        saved = folder / 'rollback/.claude/tracked.txt'
        data['before_edits'] = [{'path': str(self.main / 'tracked.txt'),
            'prepared_checksum': m.digest(saved), 'mode': 0o644,
            'git_blob': {'repository': str(self.main), 'revision': m.git(self.root / 'repos/skills', 'rev-parse', 'HEAD').decode().strip(),
                         'relative': 'tracked.txt', 'sha256': m.hashlib.sha256(b'base\n').hexdigest()}}]
        path.write_text(json.dumps(data))
        m.rollback(folder)
        self.assertEqual((self.main / 'tracked.txt').read_text(), 'base\n')

    def test_timestamp_normalization_preserves_real_conflicts(self):
        first = self.skill / 'agent-native-skill.json'
        second = self.home / '.codex/skills/demo/agent-native-skill.json'
        first.write_text('{"installedAt":"earlier","version":1}')
        second.write_text('{"installedAt":"later","version":1}')
        m.inventory(self.home, self.root, {})
        second.write_text('{"installedAt":"later","version":2}')
        with self.assertRaisesRegex(ValueError, 'agent-native-skill.json'):
            m.inventory(self.home, self.root, {})

    def test_late_failure_restores_moved_catalogs(self):
        before = m.digest(self.home)
        report = m.inventory(self.home, self.root, {})
        original = m.verify
        def fail(*args):
            raise RuntimeError('late verification failure')
        m.verify = fail
        try:
            with self.assertRaisesRegex(RuntimeError, 'late verification'):
                m.apply(self.home, self.root, report)
        finally:
            m.verify = original
        after = {k: v for k, v in m.digest(self.home).items() if k != '.agentic' and not k.startswith('.agentic/')}
        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
