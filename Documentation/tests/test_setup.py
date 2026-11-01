"""MIT: portable structural and read-only setup checks; no game simulation."""
from pathlib import Path
import argparse, copy, hashlib, json, os, re, shutil, subprocess, tempfile, unittest
from urllib.parse import unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PARSER = argparse.ArgumentParser()
PARSER.add_argument('--powershell', default=shutil.which('powershell') or shutil.which('pwsh'))
OPTIONS, UNIT_ARGS = PARSER.parse_known_args()
FILES = ['assets.xml','templates.xml','properties-toolone.xml','properties.xml','datasets.xml']

class Setup(unittest.TestCase):
    def setUp(self):
        if not OPTIONS.powershell: self.fail('PowerShell is required for setup tests.')
        self.temp=tempfile.TemporaryDirectory(prefix='anno kit tests ')
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.config=json.loads((ROOT/'local.example.json').read_text('utf-8'))
        self.config.update(gamePath='game installation',vanillaPath='extracted data',modsPath='',workPath='my mods',outputPath='my results')
        for relative in ['game installation/Bin/Win64/Anno1800.exe']+['extracted data/data/config/export/main/asset/'+n for n in FILES]:
            p=self.base/relative; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b'fixture')
        self.path=self.base/'local.json'

    def run_check(self, value=None, raw=None, missing=False, default_path=False):
        if not missing:
            self.path.write_text(raw if raw is not None else json.dumps(value if value is not None else self.config),encoding='utf-8')
        script=ROOT/'tools/check-setup.ps1'
        arguments=['-ConfigPath',str(self.path)]
        if default_path:
            script=self.base/'tools/check-setup.ps1'
            script.parent.mkdir()
            shutil.copyfile(ROOT/'tools/check-setup.ps1',script)
            arguments=[]
        before={p.relative_to(self.base).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in self.base.rglob('*') if p.is_file()}
        result=subprocess.run([OPTIONS.powershell,'-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(script)]+arguments,capture_output=True,text=True,encoding='utf-8',errors='replace')
        after={p.relative_to(self.base).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in self.base.rglob('*') if p.is_file()}
        self.assertEqual(before,after,'Setup check mutated fixture files')
        self.assertFalse((self.base/'my mods').exists()); self.assertFalse((self.base/'my results').exists())
        return result

    def test_missing_config(self):
        r=self.run_check(missing=True); self.assertEqual(r.returncode,1); self.assertIn('configuration is missing',r.stdout)

    def test_default_configuration_location(self):
        self.config.update(workPath='work', outputPath='out')
        r=self.run_check(default_path=True); self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertFalse((self.base/'work').exists()); self.assertFalse((self.base/'out').exists())

    def test_malformed_json(self):
        r=self.run_check(raw='{broken'); self.assertEqual(r.returncode,1); self.assertIn('strict JSON',r.stdout)

    def test_jsonc_rejected(self):
        for raw in ('{"configVersion":1,}', '{/* comment */ "configVersion":1}'):
            with self.subTest(raw=raw): self.assertEqual(self.run_check(raw=raw).returncode,1)

    def test_wrong_types(self):
        for key,val in [('gamePath',123),('tools',[]),('configVersion','1'),('configVersion',True),('workPath','')]:
            with self.subTest(key=key,val=val):
                c=copy.deepcopy(self.config); c[key]=val
                r=self.run_check(c); self.assertEqual(r.returncode,1); self.assertIn('[ERROR]',r.stdout)

    def test_valid_spaces_without_optional_tools(self):
        r=self.run_check(); self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('Offline loader validation is unavailable',r.stdout)
        self.assertIn('file-presence checks passed',r.stdout)

    def test_valid_optional_evaluator_not_executed(self):
        (self.base/'xmltest.exe').write_bytes(b'not an executable')
        self.config['tools']['xmltest']='xmltest.exe'
        r=self.run_check(); self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertNotIn('Offline loader validation is unavailable',r.stdout)

    def test_unicode_and_bracket_paths(self):
        folder='extracted [data] '+chr(252)
        (self.base/'extracted data').rename(self.base/folder)
        self.config['vanillaPath']=folder
        r=self.run_check(); self.assertEqual(r.returncode,0,r.stdout+r.stderr)

    def test_wrong_evaluator(self):
        self.config['tools']['xmltest']='xmltest2.exe'
        r=self.run_check(); self.assertEqual(r.returncode,1); self.assertIn('Anno 1800 xmltest.exe',r.stdout)

    def test_missing_and_empty_vanilla(self):
        p=self.base/'extracted data/data/config/export/main/asset/assets.xml'
        p.unlink(); r=self.run_check(); self.assertEqual(r.returncode,1); self.assertIn('Missing vanilla assets.xml',r.stdout)
        p.write_bytes(b''); r=self.run_check(); self.assertEqual(r.returncode,1); self.assertIn('assets.xml is empty',r.stdout)

    def test_unsafe_output_overlap(self):
        for key,value in [('workPath','game installation/mods'),('outputPath','extracted data/results'),('workPath','.'),('outputPath','my mods/results')]:
            with self.subTest(key=key,value=value):
                c=copy.deepcopy(self.config); c[key]=value
                r=self.run_check(c); self.assertEqual(r.returncode,1); self.assertIn('overlap',r.stdout)

    def test_optional_source_maps_and_overlap(self):
        self.config['sources']={'a-mod': 'another checkout'}
        r=self.run_check(); self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('source is unavailable',r.stdout)
        self.config['outputPath']='another checkout/results'
        r=self.run_check(); self.assertEqual(r.returncode,1); self.assertIn('overlaps',r.stdout)

    def test_malformed_optional_configuration(self):
        for key,val in [('workspacePath',3),('sources',[]),('pathAliases',{'old':True})]:
            with self.subTest(key=key):
                c=copy.deepcopy(self.config); c[key]=val
                r=self.run_check(c); self.assertEqual(r.returncode,1); self.assertIn('[ERROR]',r.stdout)

if __name__=='__main__':
    unittest.main(argv=['test_setup.py']+UNIT_ARGS)
