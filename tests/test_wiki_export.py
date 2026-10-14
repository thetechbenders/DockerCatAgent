"""Credential-free tests for the pinned-source GitHub Wiki export."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'scripts' / 'export-wiki.py'
spec = importlib.util.spec_from_file_location('dockercat_wiki_export', MODULE)
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class WikiExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='dockercat-wiki-fixture-')
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo'
        self.repo.mkdir()
        (self.repo / 'wiki').mkdir()
        (self.repo / 'docs').mkdir()
        (self.repo / 'docs' / 'guide.md').write_text('# Guide\n## Chapter\n')
        (self.repo / 'wiki' / 'Home.md').write_text(
            '# Home\n[Guide](../docs/guide.md#chapter) [Development](Development.md)\n')
        (self.repo / 'wiki' / 'Development.md').write_text('[Home](Home.md)\n')
        (self.repo / 'wiki' / '_Sidebar.md').write_text('[Home](Home.md)\n')
        self.git('init', '-q')
        self.sha = self.commit()

    def git(self, *args):
        env = {**os.environ, 'GIT_AUTHOR_NAME': 'Fixture',
               'GIT_AUTHOR_EMAIL': 'fixture@example.invalid',
               'GIT_COMMITTER_NAME': 'Fixture',
               'GIT_COMMITTER_EMAIL': 'fixture@example.invalid'}
        return subprocess.run(['git', '-C', str(self.repo), *args],
                              env=env, check=True, capture_output=True, text=True).stdout.strip()

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'Fixture content')
        return self.git('rev-parse', 'HEAD')

    def test_exports_pinned_canonical_and_wiki_links(self):
        out = self.repo / 'publish'
        sha, count = exporter.export(self.repo, self.sha, out)
        self.assertEqual(sha, self.sha)
        self.assertEqual(count, 3)
        page = (out / 'Home.md').read_text()
        self.assertIn(f'/blob/{self.sha}/docs/guide.md#chapter', page)
        self.assertIn('/wiki/Development', page)
        self.assertNotIn('](../', page)
        manifest = json.loads((out / 'manifest.json').read_text())
        self.assertEqual(manifest['source_sha'], self.sha)
        self.assertEqual(manifest['pages']['Home.md'],
                         hashlib.sha256(page.encode()).hexdigest())
        with self.assertRaisesRegex(ValueError, 'Refusing to overwrite'):
            exporter.export(self.repo, self.sha, out)

    def test_broken_links_fail_without_partial_output(self):
        (self.repo / 'wiki' / 'Home.md').write_text('[Missing](Nothing.md)\n')
        bad_ref = self.commit()
        out = self.repo / 'failed'
        with self.assertRaisesRegex(ValueError, 'does not exist'):
            exporter.export(self.repo, bad_ref, out)
        self.assertFalse(out.exists())

    def test_invalid_ref_fails_before_file_creation(self):
        out = self.repo / 'invalid'
        with self.assertRaisesRegex(ValueError, '40-character'):
            exporter.export(self.repo, 'main', out)
        self.assertFalse(out.exists())

    def test_export_reads_commit_not_changed_working_tree(self):
        (self.repo / 'wiki' / 'Home.md').write_text('[Broken](Nope.md)\n')
        out = self.repo / 'pinned'
        exporter.export(self.repo, self.sha, out)
        self.assertIn('Guide', (out / 'Home.md').read_text())


if __name__ == '__main__':
    unittest.main()
