"""Read-only verification of trigger sources, documentation anchors and CRLF."""
from workspace_paths import source_path
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import unicodedata

DOC = Path(__file__).resolve().parents[1]
RECORD = DOC/'reference/triggers'


def anchors(path):
    text = path.read_text('utf-8-sig')
    seen, result = Counter(), set()
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', text, re.M):
        title = re.sub(r'<[^>]+>', '', title).lower()
        title = ''.join(c for c in title if c in '_- ' or unicodedata.category(c)[0] in 'LN')
        title = title.replace(' ', '-')
        base = title
        if seen[base]:
            title += '-'+str(seen[base])
        seen[base] += 1
        result.add(title)
    result.update(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)', text))
    return result


def main():
    findings, hashes, fragments = [], 0, 0
    workspace = json.loads((RECORD/'workspace.json').read_text('utf-8'))
    native = json.loads((RECORD/'vanilla.json').read_text('utf-8'))
    for source in workspace['sources']+native['sources']:
        path = source_path(source['path'])
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes += 1
        if digest != source['sha256']:
            findings.append({'source': str(path), 'error': 'source hash changed since extraction'})
    pages = list((DOC/'gameplay').glob('trigger*.md'))
    pages += [DOC/'reference/trigger-audit.md', DOC/'reference/trigger-mod-walkthroughs.md', RECORD/'prose-evidence.md']
    cache = {}
    for page in pages:
        for target in re.findall(r'\]\(([^)]+)\)', page.read_text('utf-8-sig')):
            if '#' not in target or re.match(r'^[a-z]+:', target, re.I):
                continue
            file, fragment = target.strip('<>').split('#', 1)
            path = (page.parent/file).resolve() if file else page
            if path.suffix != '.md' or not path.exists():
                continue
            if path not in cache:
                cache[path] = anchors(path)
            fragments += 1
            if fragment not in cache[path]:
                findings.append({'file': str(page), 'error': 'missing heading fragment', 'target': target})
    checked = 0
    for path in DOC.rglob('*'):
        if not path.is_file() or path.suffix not in {'.md', '.py', '.json', '.xml', '.lua', '.log', '.txt'}:
            continue
        raw = path.read_bytes()
        checked += 1
        try:
            raw.decode('utf-8')
        except UnicodeDecodeError:
            findings.append({'file': str(path), 'error': 'not UTF-8; preserve original and inspect'})
        if b'\n' in raw.replace(b'\r\n', b'') or b'\r' in raw.replace(b'\r\n', b''):
            findings.append({'file': str(path), 'error': 'not CRLF'})
    report = {'date': '2026-10-03', 'source_hashes_checked': hashes,
              'linked_heading_fragments_checked': fragments, 'utf8_crlf_files_checked': checked,
              'findings': findings, 'limitations': 'No game, Lua C-function, dependency-loader or MP execution; source preservation is measured against this extraction.'}
    output = DOC/'reference/validation/triggers/documentation-integrity.json'
    # The report itself is the only file written by this verifier.
    output.write_bytes((json.dumps(report, indent=2)+'\n').replace('\n', '\r\n').encode('utf-8'))
    print(json.dumps(report))
    if findings:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
