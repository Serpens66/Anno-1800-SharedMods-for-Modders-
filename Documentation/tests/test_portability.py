"""Exercise independent source locations and a Documentation-only, read-only copy."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

DOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DOC / 'tools'))
from validate_docs import validate


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}


def load_paths(config):
    with patch.dict(os.environ, {'ANNO_DOCUMENTATION_CONFIG': str(config)}):
        spec = importlib.util.spec_from_file_location('configured_documentation_paths', DOC / 'tools/workspace_paths.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


class SourceResolution(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='anno sources [test] ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.config = self.root / 'configuration/local.json'
        self.config.parent.mkdir()
        self.native = self.root / 'user extraction'
        self.native.mkdir()
        self.mods = self.root / 'independent mod checkout'
        self.mods.mkdir()
        self.notes = self.root / 'personal notebook.xml'
        self.notes.write_text('test fixture', encoding='utf-8')
        self.value = {'configVersion': 1, 'vanillaPath': '../user extraction',
                      'outputPath': '../results', 'sources': {'Anno-1800-Mods': '../independent mod checkout',
                      'notes:HowTo.xml': '../personal notebook.xml'},
                      'pathAliases': {'Z:/historical/project': '../independent mod checkout'}}

    def module(self):
        self.config.write_text(json.dumps(self.value), encoding='utf-8')
        return load_paths(self.config)

    def test_relative_paths_use_configuration_directory(self):
        m = self.module()
        self.assertEqual(m.configured_path('vanillaPath'), self.native)
        self.assertEqual(m.source_path('workspace:Anno-1800-Mods/example.xml'), self.mods / 'example.xml')
        self.assertEqual(m.source_relative(self.mods / 'example.xml').as_posix(), 'Anno-1800-Mods/example.xml')
        self.assertEqual(m.source_path('notes:HowTo.xml'), self.notes)

    def test_historical_source_paths_and_identity_preservation(self):
        m = self.module()
        self.assertEqual(m.source_path('Z:/old/dataAlle/data/config/example.xml'), self.native / 'data/config/example.xml')
        self.assertEqual(m.source_path('Z:/old/mods bei github/Anno-1800-Mods/example.xml'), self.mods / 'example.xml')
        self.assertEqual(m.source_path('Z:/historical/project/example.xml'), self.mods / 'example.xml')
        self.assertEqual(m.source_path('workspace:Documentation/README.md'), DOC / 'README.md')
        old = 'workspace:Anno-1800-SharedMods (for Modders)/shared/example.lua'
        self.assertEqual(m.current_source_id(old), 'workspace:SharedMods/shared/example.lua')
        self.assertEqual(m.source_path('Trigger_Guide.md'), DOC / 'Trigger_Guide.md')

    def test_missing_sources_are_explicit(self):
        m = load_paths(self.root / 'absent.json')
        with self.assertRaisesRegex(m.ConfigurationError, 'Missing vanillaPath'):
            m.configured_path('vanillaPath')
        with self.assertRaisesRegex(m.ConfigurationError, 'Unconfigured source'):
            m.source_path('UnavailableMod/data/file.xml')

    def test_malformed_configuration_and_wrong_game_tool(self):
        self.config.write_text('{broken', encoding='utf-8')
        with self.assertRaisesRegex(SystemExit, 'Invalid configuration'):
            load_paths(self.config)
        self.value['tools'] = []
        with self.assertRaisesRegex(SystemExit, 'tools must map'):
            self.module()
        self.value['tools'] = {'xmltest': '../xmltest2.exe'}
        (self.root / 'xmltest2.exe').write_bytes(b'fixture, never executed')
        m = self.module()
        with self.assertRaisesRegex(m.ConfigurationError, 'Anno 1800 xmltest.exe'):
            m.configured_path('tools.xmltest')

    def test_outputs_cannot_overwrite_sources_or_escape(self):
        m = self.module()
        self.assertEqual(m.output_path('check/results.json'), self.root / 'results/check/results.json')
        with self.assertRaisesRegex(m.ConfigurationError, 'remain within'):
            m.output_path('../source.xml')
        self.value['outputPath'] = '../user extraction/results'
        m = self.module()
        with self.assertRaisesRegex(m.ConfigurationError, 'overlaps'):
            m.output_path()
        self.value['outputPath'] = str(DOC / 'out')
        self.value['gamePath'] = str(DOC.parent)
        m = self.module()
        with self.assertRaisesRegex(m.ConfigurationError, 'overlaps'):
            m.output_path()


class StandaloneDocumentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='standalone Documentation ')
        cls.root = Path(cls.temp.name) / 'Documentation'
        shutil.copytree(DOC, cls.root, ignore=shutil.ignore_patterns('local.json', 'local.*.json', 'out', 'work', '__pycache__'))
        shutil.copyfile(DOC / 'local.example.json', cls.root / 'local.example.json')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_all_links_and_snippets_in_isolation(self):
        report = validate(self.root)
        self.assertEqual(report['findings'], [], json.dumps(report, indent=2))

    def test_validator_cli_never_changes_files(self):
        before = snapshot(self.root)
        env = dict(os.environ)
        env.pop('ANNO_DOCUMENTATION_CONFIG', None)
        run = subprocess.run([sys.executable, str(self.root / 'tools/validate_docs.py')],
                             cwd=self.root.parent, env=env, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(before, snapshot(self.root))

    def test_xml_trigger_lua_navigation_and_missing_audit_sources(self):
        scenarios = json.loads((self.root / 'tests/reader-scenarios.json').read_text('utf-8'))
        index = (self.root / 'README.md').read_text('utf-8')
        instructions = (self.root / 'AGENTS.md').read_text('utf-8')
        setup = (self.root / 'setup.md').read_text('utf-8')
        self.assertIn("user's own current extracted sources", instructions)
        self.assertIn('stop dependent implementation decisions', setup)
        for scenario in scenarios['scenarios']:
            with self.subTest(task=scenario['task']):
                for chapter in scenario['chapters']:
                    self.assertTrue((self.root / chapter).is_file(), chapter)
                    self.assertIn(chapter, index)
                self.assertIn('assets.xml', scenario['native_files'])
        # Public Lua source is actually named; private reports are not prerequisites.
        self.assertIn('https://github.com/', (self.root / 'lua/shared-light.md').read_text('utf-8'))

    def test_knowledge_correction_has_one_destination(self):
        destination = self.root / 'xml/xpath.md'
        original = destination.read_bytes()
        try:
            before = snapshot(self.root)
            addition = b'\r\nTemporary reader check: Pending; source unavailable; no runtime result.\r\n'
            destination.write_bytes(original + addition)
            after = snapshot(self.root)
            self.assertEqual([p for p in before if before[p] != after[p]], ['xml/xpath.md'])
            self.assertEqual(validate(self.root)['findings'], [])
            maintenance = (self.root / 'maintenance.md').read_text('utf-8')
            self.assertIn('Update the relevant chapter directly', maintenance)
            self.assertIn('Without', (self.root / 'workflow.md').read_text('utf-8'))
        finally:
            destination.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
