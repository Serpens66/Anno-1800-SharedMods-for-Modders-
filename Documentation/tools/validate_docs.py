"""Read-only standalone link/text/snippet checks. Never normalizes or writes files."""
import ast
import html
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {'out', 'work', '__pycache__', '.cache', '.git'}
TEXT = {'.md', '.py', '.ps1', '.json', '.xml', '.lua', '.log', '.txt'}


def files(root):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and not (set(p.relative_to(root).parts) & EXCLUDED)
                  and (not p.name.startswith('local.') or p.name == 'local.example.json'))


def anchors(text):
    result = set(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)', text, re.I))
    counts = {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        heading = re.sub(r'<[^>]*>', '', html.unescape(heading))
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        count = counts.get(slug, 0)
        result.add(slug + (f'-{count}' if count else ''))
        counts[slug] = count + 1
    return result


def validate(root=ROOT):
    findings = []
    links = blocks = checked = 0
    historical_pages = {'reference/sources.md', 'reference/kit-transfer.md'}
    exception_file = root / 'reference/history/format-exceptions.json'
    exceptions = json.loads(exception_file.read_text('utf-8')) if exception_file.is_file() else {}
    for path in files(root):
        relative = path.relative_to(root).as_posix()
        if path.suffix not in TEXT and path.name != '.gitignore':
            continue
        raw = path.read_bytes()
        checked += 1
        try:
            text = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            findings.append({'file': relative, 'error': 'not UTF-8; preserve original encoding and inspect'})
            continue
        if b'\n' in raw.replace(b'\r\n', b'') or b'\r' in raw.replace(b'\r\n', b''):
            if exceptions.get(relative, {}).get('sha256') != hashlib.sha256(raw).hexdigest():
                findings.append({'file': relative, 'error': 'not CRLF'})
        if path.suffix == '.py':
            try:
                ast.parse(text, filename=relative)
            except SyntaxError as error:
                findings.append({'file': relative, 'error': str(error)})
        if path.suffix == '.json':
            try:
                json.loads(text)
            except ValueError as error:
                findings.append({'file': relative, 'error': str(error)})
        active = (path.suffix in {'.md', '.py', '.ps1'} and relative not in historical_pages
                  and not relative.startswith(('reference/history/', 'reference/validation/')))
        if active and re.search(r'(?i)[a-z]:[/\\](?:Users[/\\]|CDesktopLink[/\\])', text):
            findings.append({'file': relative, 'error': 'personal path in active instructions/code'})
        if path.suffix != '.md':
            continue
        for target in re.findall(r'\]\(([^)]+)\)', text):
            target = target.strip('<>')
            if re.match(r'^[a-z][a-z0-9+.-]*:', target, re.I):
                continue
            links += 1
            filename, _, fragment = unquote(target).partition('#')
            resolved = (path.parent / filename).resolve() if filename else path.resolve()
            if not resolved.is_relative_to(root.resolve()):
                findings.append({'file': relative, 'error': 'link escapes Documentation', 'target': target})
            elif not resolved.is_file():
                findings.append({'file': relative, 'error': 'missing file', 'target': target})
            elif fragment and resolved.suffix == '.md' and fragment not in anchors(resolved.read_text('utf-8-sig')):
                findings.append({'file': relative, 'error': 'missing heading fragment', 'target': target})
        for language, source in re.findall(r'^```(\w+)\s*\n(.*?)^```\s*$', text, re.M | re.S):
            if language.lower() != 'xml':
                continue
            blocks += 1
            try:
                ET.fromstring('<Snippet>' + source + '</Snippet>')
            except ET.ParseError as error:
                findings.append({'file': relative, 'error': 'XML snippet: ' + str(error)})
    return {'text_files_checked': checked, 'internal_links_checked': links,
            'xml_blocks_checked': blocks, 'findings': findings,
            'limits': 'Read-only structure/text checks; no source audit, loader, Lua, game/save/MP execution.'}


def main():
    report = validate()
    print(json.dumps(report, ensure_ascii=False))
    return 1 if report['findings'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
