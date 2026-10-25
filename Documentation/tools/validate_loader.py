"""Run synthetic offline loader checks. No game or multiplayer execution."""
from pathlib import Path
import hashlib
import json
import subprocess
from lxml import etree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reference' / 'validation' / 'loader'
EXE = Path(r'C:\Users\Serpens66\.vscode\extensions\jakobharder.anno-modding-tools-2.3.1\external\xmltest.exe')

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))

def main():
    target = OUT / 'original.xml'
    write(target, '<Assets><Asset><Template>Example</Template><Values><Standard><GUID>1</GUID><Name>old</Name></Standard><List><Item><A>1</A></Item><Item><A>2</A></Item></List></Values></Asset></Assets>\n')
    cases = [
        ('scalar-condition', '<ModOp Type="merge" GUID="1" Path="/Values/Standard" Condition="true()"><Name>new</Name></ModOp>', 'string(//Standard/Name)', 'old', True),
        ('nodes-condition', '<ModOp Type="merge" GUID="1" Path="/Values/Standard" Condition="//Asset[Values/Standard/GUID=\'1\']"><Name>new</Name></ModOp>', 'string(//Standard/Name)', 'new', False),
        ('replace-container-with-child', '<ModOp Type="replace" GUID="1" Path="/Values/Standard"><Name>new</Name></ModOp>', 'count(//Standard)', 0.0, False),
        ('replace-container-correct', '<ModOp Type="replace" GUID="1" Path="/Values/Standard"><Standard><GUID>1</GUID><Name>new</Name></Standard></ModOp>', 'string(//Standard/Name)', 'new', False),
        ('merge-empty-does-not-clear', '<ModOp Type="merge" GUID="1" Path="/Values"><List/></ModOp>', 'count(//List/Item)', 2.0, False),
        ('merge-occurrence', '<ModOp Type="merge" GUID="1" Path="/Values/List"><Item><A>9</A></Item></ModOp>', 'string(//List/Item[2]/A)', '2', False),
        ('add-appends', '<ModOp Type="add" GUID="1" Path="/Values/List"><Item><A>9</A></Item></ModOp>', 'count(//List/Item)', 3.0, False),
        ('at-values-context', '<ModOp Type="merge" Path="@1/Standard"><Name>new</Name></ModOp>', 'string(//Standard/Name)', 'new', False),
    ]
    results = []
    for name, operation, xpath, expected, error_expected in cases:
        mod = OUT / name
        patch = mod / 'data/config/export/main/asset/assets.xml'
        write(patch, '<ModOps>' + operation + '</ModOps>\n')
        output = mod / 'patched.xml'
        args = [str(EXE), '-c', 'patch', '-m', str(mod), '-o', str(output), str(target), str(patch)]
        run = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
        log = run.stdout + run.stderr
        write(mod / 'xmltest.log', log)
        actual = ET.parse(str(output)).xpath(xpath) if output.exists() else None
        passed = run.returncode == 0 and actual == expected and (('[error]' in log) == error_expected)
        results.append({'case': name, 'command': args, 'exit_code': run.returncode, 'assertion': xpath,
                        'expected': expected, 'actual': actual, 'expected_error': error_expected, 'passed': passed})
    report = {'date': '2026-10-03', 'scope': 'Synthetic offline XML; not an in-game or multiplayer test',
              'executable': str(EXE), 'sha256': hashlib.sha256(EXE.read_bytes()).hexdigest(),
              'reported_build': 'GU17.1', 'cases': results}
    write(OUT / 'results.json', json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    for item in results:
        print(item['case'], 'PASS' if item['passed'] else 'FAIL', repr(item['actual']))
    if not all(x['passed'] for x in results):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
