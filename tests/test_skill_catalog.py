import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('catalog', Path(__file__).resolve().parents[1] / 'scripts/skill-catalog.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class UpkeepTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name).resolve()
        self.root = self.home / '.agentic'
        (self.root / 'skills').mkdir(parents=True)
        (self.root / 'index.json').write_text('{"skills": {}}\n')
        for rel in c.m.CATALOGS:
            p = self.home / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.symlink_to(self.root / 'skills')

    def tearDown(self):
        self.temp.cleanup()

    def skill(self, directory, content='same'):
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'SKILL.md').write_text('---\nname: demo\ndescription: demo\n---\n')
        (directory / 'helper.py').write_text(content)

    def test_new_skill_through_shared_link_only_refreshes_index(self):
        self.skill(self.home / '.pi/agent/skills/demo')
        before = c.m.digest(self.home)
        report = c.run(self.home, self.root)
        self.assertEqual(before, c.m.digest(self.home))
        self.assertEqual(report['adopt'], [])
        self.assertTrue(report['refresh_index'])
        c.run(self.home, self.root, apply=True)
        self.assertFalse(c.run(self.home, self.root)['refresh_index'])

    def test_replaced_harness_directory_is_adopted_and_relinked(self):
        p = self.home / '.cursor/skills'
        p.unlink()
        self.skill(p / 'demo')
        before = c.m.digest(self.home)
        result = c.run(self.home, self.root, apply=True)
        self.assertEqual((self.root / 'skills/demo/helper.py').read_text(), 'same')
        self.assertTrue(p.is_symlink())
        self.assertEqual(p.resolve(), self.root / 'skills')
        self.assertEqual(c.run(self.home, self.root, apply=True)['adopt'], [])
        c.m.rollback(self.root / 'state/migrations' / result['migration_id'])
        after = {k: v for k, v in c.m.digest(self.home).items() if not k.startswith('.agentic/state')}
        self.assertEqual(before, after)

    def test_conflicting_helper_preserves_both(self):
        self.skill(self.root / 'skills/demo', 'central')
        p = self.home / '.codex/skills'
        p.unlink()
        self.skill(p / 'demo', 'newer')
        before = c.m.digest(self.home)
        with self.assertRaisesRegex(ValueError, 'Content conflict'):
            c.run(self.home, self.root, apply=True)
        self.assertEqual(before, c.m.digest(self.home))

    def test_external_skill_link_is_centralized(self):
        source = self.home / 'external/demo'
        self.skill(source)
        (self.root / 'skills/demo').symlink_to(source)
        c.run(self.home, self.root, apply=True)
        self.assertFalse((self.root / 'skills/demo').is_symlink())
        self.assertTrue((source / 'SKILL.md').exists())


if __name__ == '__main__':
    unittest.main()
