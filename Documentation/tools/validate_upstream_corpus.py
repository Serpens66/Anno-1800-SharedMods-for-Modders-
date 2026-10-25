"""Evaluate unchanged upstream XML fixtures offline; preserve invalid/skipped cases."""
from pathlib import Path
import json
import subprocess
from lxml import etree as ET
from validate_loader import EXE, write

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r'C:\Users\Serpens66\AppData\Local\Temp\anno1800-documentation-research-20261003\anno-mod-loader\tests\xml')
OUT = ROOT / 'reference/validation/upstream-corpus'

def main():
    results = []
    for spec in sorted(SOURCE.glob('*/*.json')):
        data = json.loads(spec.read_text('utf-8-sig'))
        case = spec.relative_to(SOURCE).as_posix()
        folder = spec.parent / data.get('folder', '')
        original = folder / (spec.stem + '_input.xml')
        patch = folder / (spec.stem + '_patch.xml')
        result = {'case': case, 'name': data['name'], 'source_spec': str(spec),
                  'source_input': str(original), 'source_patch': str(patch),
                  'expected_paths': data['expected']}
        if data.get('modIds'):
            result.update(status='not executed', reason='Upstream runner supplies an active ModID set; inspected CLI Apply call does not. Do not treat a different context as this test.')
        else:
            try:
                ET.parse(str(original))
                ET.parse(str(patch))
            except (ET.XMLSyntaxError, OSError) as exc:
                result.update(status='not executed', reason='Original fixture is missing or not well-formed XML', detail=str(exc))
            else:
                target = OUT / spec.parent.name / spec.stem
                target.mkdir(parents=True, exist_ok=True)
                output = target / 'patched.xml'
                if output.exists():
                    output.unlink()  # exact generated file, never a source/mod/game path
                args = [str(EXE), '-c', 'patch', '-v', '-m', str(spec.parent), '-o', str(output), str(original), str(patch)]
                run = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
                log = run.stdout + run.stderr
                write(target / 'xmltest.log', log)
                checks = []
                if output.exists():
                    tree = ET.parse(str(output))
                    for expression in data['expected']:
                        negative = expression.startswith('!')
                        xpath = expression[1:] if negative else expression
                        exists = bool(tree.xpath(xpath))
                        checks.append({'expression': expression, 'passed': exists != negative})
                issues = '[warning]' in log or '[error]' in log
                expected_issues = data.get('issuesExpected', '0') == '1'
                passed = (run.returncode == 0 and output.exists()
                          and all(c['passed'] for c in checks) and issues == expected_issues)
                result.update(status='passed' if passed else 'failed; review required', command=args,
                              exit_code=run.returncode, assertions=checks, issues=issues,
                              expected_issues=expected_issues, log=str(target / 'xmltest.log'))
        results.append(result)
    report = {'date':'2026-10-03', 'source_commit':'8326b7c5a7648787c52f1252cd6e8ae60e593d1c',
              'executable':str(EXE), 'scope':'Offline installed GU17.1 evaluator; not compiled upstream Catch2 suite, game or multiplayer',
              'disabled_specs':[str(p) for p in SOURCE.rglob('*.json_')], 'cases':results}
    write(OUT / 'results.json', json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    from collections import Counter
    print(dict(Counter(c['status'] for c in results)))
    for c in results:
        if c['status'] != 'passed':
            print(c['case'], c['status'], c.get('reason', ''), [a for a in c.get('assertions',[]) if not a['passed']])

if __name__ == '__main__':
    main()
