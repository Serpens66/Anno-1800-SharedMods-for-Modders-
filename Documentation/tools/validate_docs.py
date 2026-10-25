"""Check documentation links/snippets and normalize only UTF-8 documentation."""
from pathlib import Path
import json
import re
from lxml import etree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reference/validation'

def main():
    findings, lua_files, xml_count, link_count = [], [], 0, 0
    for path in sorted(ROOT.rglob('*.md')):
        text = path.read_text('utf-8-sig')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            target = target.strip('<>').split('#', 1)[0]
            if not target or re.match(r'^[a-z]+:', target, re.I):
                continue
            link_count += 1
            if not (path.parent / target).exists():
                findings.append({'file': str(path), 'error': 'missing link target', 'target': target})
        for number, (language, source) in enumerate(re.findall(r'^```(\w+)\s*\n(.*?)^```\s*$', text, re.M | re.S), 1):
            if language.lower() == 'xml':
                xml_count += 1
                try:
                    ET.fromstring(('<Snippet>' + source + '</Snippet>').encode('utf-8'))
                except ET.XMLSyntaxError as exc:
                    findings.append({'file': str(path), 'block': number, 'error': str(exc)})
            if language.lower() == 'lua':
                target = OUT / 'lua' / (path.stem + '-' + str(number) + '.lua')
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))
                lua_files.append(str(target))
    # All documentation source files in this task use UTF-8. Never normalize mods/AGENTS/game files.
    normalized = 0
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix in {'.md', '.py', '.json', '.xml', '.lua', '.log', '.txt'}:
            raw = path.read_bytes()
            source = raw.decode('utf-8')
            fixed = source.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8')
            if raw != fixed:
                path.write_bytes(fixed); normalized += 1
    report = {'date': '2026-10-03', 'xml_blocks_checked': xml_count,
              'local_links_checked': link_count, 'lua_snippets': lua_files,
              'findings': findings, 'crlf_normalized_files': normalized,
              'limits': 'XML well-formedness and file links only; no runtime/API/MP claim; Lua compiler separately required.'}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'documentation.json').write_bytes((json.dumps(report, indent=2) + '\n').replace('\n', '\r\n').encode('utf-8'))
    print(json.dumps({'xml_blocks': xml_count, 'links': link_count, 'lua': len(lua_files), 'findings': findings, 'normalized': normalized}))
    if findings:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
