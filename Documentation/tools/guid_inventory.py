"""Conservative, read-only Serp GUID scan; --write explicitly refreshes the register."""
import argparse
from bisect import bisect_right
from datetime import date
import hashlib
import itertools
import json
import os
from pathlib import Path
import re

from workspace_paths import DOC, configured_path

LOW, HIGH = 1500000000, 1500010000
NUMBER = re.compile(r'(?<!\d)15000\d{5}(?!\d)')
SKIP = {'.git', '.svn', '__pycache__', 'node_modules', '.cache'}
TEXT = {'.xml', '.lua', '.json', '.jsonc', '.cfg', '.fc', '.ifo', '.md', '.txt',
        '.py', '.ps1', '.include', '.yaml', '.yml', '.csv', '.tsv', '.log'}


def decode(raw):
    if raw.startswith((b'\xff\xfe', b'\xfe\xff')):
        return raw.decode('utf-16')
    if b'\0' in raw:
        return None
    try:
        return raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        return raw.decode('cp1252', errors='replace')


def scan(root):
    sources, records, metadata, warnings = {}, {}, {}, []
    scanned = 0
    for directory, dirs, names in os.walk(root, followlinks=False):
        base = Path(directory)
        dirs[:] = sorted(d for d in dirs if d not in SKIP
                         and (base / d).resolve() != DOC.resolve()
                         and not (base / d).is_symlink())
        for name in sorted(names):
            path = base / name
            # Include disabled sources such as assets.xml_ and modinfo.json_.
            if Path(name.rstrip('_~')).suffix.lower() not in TEXT:
                continue
            raw = path.read_bytes()
            content = decode(raw)
            if content is None:
                continue
            scanned += 1
            identity = path.relative_to(root).as_posix()
            if name.lower() == 'modinfo.json':
                try:
                    info = json.loads(content)
                    metadata[base] = {'path': identity, 'mod_id': info.get('ModID'),
                                      'incompatible_ids': info.get('IncompatibleIds') or []}
                except ValueError:
                    # Never silently treat unreadable conflict declarations as absent.
                    match = re.search(r'"ModID"\s*:\s*"([^"]+)"', content)
                    metadata[base] = {'path': identity, 'mod_id': match[1] if match else None,
                                      'incompatible_ids': [], 'unparsed': True}
                    warnings.append(identity + ': metadata is not strict JSON; inspect manually')
            matches = [m for m in NUMBER.finditer(content) if LOW <= int(m[0]) <= HIGH]
            if not matches:
                continue
            sources[identity] = hashlib.sha256(raw).hexdigest()
            # Mask comments without moving offsets or line numbers. Definitions are
            # lexical evidence, not evaluated ModOps or proof of simultaneous loading.
            active = re.sub(r'<!--.*?-->', lambda m: re.sub(r'[^\r\n]', ' ', m[0]), content, flags=re.S)
            definitions = {}
            for block in re.finditer(r'<Standard\b[^>]*>.*?</Standard>', active, re.S):
                for m in re.finditer(r'<GUID>\s*(15000\d{5})\s*</GUID>', block[0]):
                    definitions[block.start() + m.start(1)] = 'asset-definition'
            for m in re.finditer(r'<Text\b[^>]*>\s*<GUID>\s*(15000\d{5})\s*</GUID>', active):
                definitions[m.start(1)] = 'text-definition'
            newlines = [m.start() for m in re.finditer('\n', content)]
            for m in matches:
                guid = int(m[0])
                row = {'path': identity, 'line': bisect_right(newlines, m.start()) + 1,
                       'kind': definitions.get(m.start(), 'reference-or-comment')}
                if row not in records.setdefault(guid, []):
                    records[guid].append(row)
    for rows in records.values():
        for row in rows:
            parent = (root / row['path']).parent
            while parent != root and parent not in metadata:
                parent = parent.parent
            row['mod'] = metadata[parent]['path'] if parent in metadata else None
    mods = {v['path']: v for v in metadata.values()}
    pairs = []
    for guid, rows in sorted(records.items()):
        owners = sorted({r['mod'] for r in rows if r['kind'] == 'asset-definition' and r['mod']})
        for left, right in itertools.combinations(owners, 2):
            a, b = mods[left], mods[right]
            if a['mod_id'] and a['mod_id'] == b['mod_id']:
                status = 'same-ModID'
            elif (b['mod_id'] in a['incompatible_ids'] or a['mod_id'] in b['incompatible_ids']):
                status = 'declared-incompatible'
            else:
                status = 'review-required'
            pairs.append({'guid': guid, 'left': left, 'right': right, 'status': status})
    return {'date': date.today().isoformat(), 'range': [LOW, HIGH], 'scanned_text_files': scanned,
            'source_sha256': sources, 'mods': mods, 'warnings': warnings,
            'guids': {str(g): rows for g, rows in sorted(records.items())}, 'definition_pairs': pairs}


def compact(data):
    """Store repeated source identities and owner pairs once, retaining all lines."""
    result = {k: v for k, v in data.items() if k not in {'guids', 'definition_pairs'}}
    result['guids'] = {}
    for guid, rows in data['guids'].items():
        grouped = {}
        for row in rows:
            entry = grouped.setdefault(row['path'], {'mod': row['mod']})
            entry.setdefault(row['kind'], []).append(row['line'])
        result['guids'][guid] = grouped
    grouped = {}
    for pair in data['definition_pairs']:
        key = (pair['left'], pair['right'], pair['status'])
        grouped.setdefault(key, []).append(pair['guid'])
    result['definition_pairs'] = [dict(left=a, right=b, status=s, guids=ids)
                                  for (a, b, s), ids in sorted(grouped.items())]
    return result


def intervals(ids):
    runs = []
    for _, group in itertools.groupby(enumerate(sorted(set(ids))), lambda x: x[1] - x[0]):
        values = [x[1] for x in group]
        runs.append(str(values[0]) if len(values) == 1 else f'{values[0]}-{values[-1]}')
    return ', '.join(runs)


def markdown(data):
    counts = {s: sum(p['status'] == s for p in data['definition_pairs'])
              for s in ('same-ModID', 'declared-incompatible', 'review-required')}
    lines = ['# Serp workspace GUID register', '',
             f"Snapshot: {data['date']}. Reserved interval: **{LOW}-{HIGH}, inclusive** (10,001 IDs).", '',
             'Source: Serp\'s explicit allocation instruction and a structural scan of the local workspace. '
             'Evidence: source inventory only; no game, loader or Vanilla semantic audit. '
             'Allocate from this reservation only when the current user is Serp. Other users should follow the '
             '[allocation rules](../foundations/identifiers-and-tools.md#asset-guids-and-independent-namespaces) '
             'for their own registered range.', '',
             f"Scanned {data['scanned_text_files']} text files; **{len(data['guids'])} distinct IDs conservatively blocked**. "
             f"Asset-definition owner pairs: {counts['same-ModID']} same ModID, "
             f"{counts['declared-incompatible']} declared incompatible, {counts['review-required']} require review.", '',
             '## Allocation workflow', '',
             'Before assigning a new GUID, run `python -B tools/guid_inventory.py --check NUMBER` '
             'from Documentation with `workspacePath` configured in ignored `local.json`, or pass `--workspace PATH`. '
             'Exit 0 means no literal occurrence in the scanned scope; exit 1 means occupied, '
             'and exit 2 means invalid input or an incomplete metadata check. '
             'After allocation, refresh with `python -B tools/guid_inventory.py --write` and review the result. '
             'The default command only reports counts and never writes. Check Vanilla and relevant external '
             'dependencies separately as required by the normal feature audit.', '',
             'All occurrences block fresh allocation, including references, comments, disabled files, WIP and old variants. '
             'A reference alone is not evidence of an asset definition. Do not recycle such IDs without tracing their ownership. '
             'The scanner includes hidden/ignored text sources and bundled copies; it excludes Documentation itself, '
             'Git/SVN/cache directories, node_modules, directory symlinks, binary files and archives. '
             'Only literal decimal IDs are detected; range comments block their literal endpoints only. Inspect declared subranges, generated/calculated IDs and unextracted archives manually. '
             'File-read errors abort the scan. Text extensions and definition heuristics are explicit in the scanner source.', '',
             'Same-ModID copies and explicitly incompatible pairs are classified separately, following Serp\'s '
             'instruction. Neither classification releases the GUID for a new unrelated asset. Metadata describes '
             'possible alternatives, not which version is installed. Other pairs are review candidates, not confirmed '
             'runtime collisions: conditional ModOps, intentional patches, inactive branches and alternative packages '
             'can explain them. Lexical Standard/GUID definitions can also be replacements. '
             'Only the nearest enclosing modinfo.json owns a source; nested mods are kept separate. '
             'Local text GUIDs are classified separately from Standard asset GUIDs.', '',
             'The [machine-readable register](serp-guid-usage.json) contains every GUID, workspace-relative file/line, '
             'definition/reference classification, nearest mod metadata, metadata declarations, source hashes and '
             'all cross-folder asset-definition pairs. No existing allocation was changed.', '',
             '## Metadata warnings', '']
    lines += ['- ' + w for w in data['warnings']] or ['None.']
    lines += ['', '## Definition pairs requiring review', '',
              'Grouped by ModID here; exact folder pairs remain in the JSON. These are review candidates, '
              'not findings of broken mods. Same-ModID and declared-incompatible pairs are excluded from this table.', '',
              '| ModIDs | GUIDs |', '| --- | --- |']
    review = {}
    for pair in data['definition_pairs']:
        if pair['status'] == 'review-required':
            key = tuple(sorted(str(data['mods'][pair[k]]['mod_id']) for k in ('left', 'right')))
            review.setdefault(key, []).append(pair['guid'])
    lines += [f"| {' / '.join(pair).replace('|', '/')} | {intervals(ids)} |"
              for pair, ids in sorted(review.items())]
    lines += ['', '## Occupied IDs', '',
              'Every row is blocked for fresh allocation. Owners below are ModIDs; `unassigned` means no enclosing metadata. '
              'Exact per-file evidence and pair classifications are in the JSON register.', '',
              '| GUID | Literal definitions (asset / text) | ModIDs of definitions, or mentions when no definition |',
              '| --- | --- | --- |']
    for guid, rows in data['guids'].items():
        defs = [r for r in rows if r['kind'] != 'reference-or-comment']
        owners = sorted({str(data['mods'][r['mod']]['mod_id']) if r['mod'] else 'unassigned'
                         for r in (defs or rows)})
        label = ', '.join(owners).replace('|', '\\|')
        lines.append(f"| {guid} | {sum(r['kind'] == 'asset-definition' for r in rows)} / "
                     f"{sum(r['kind'] == 'text-definition' for r in rows)} | {label} |")
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path)
    parser.add_argument('--check', type=int)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    root = (args.workspace or configured_path('workspacePath')).resolve()
    if not root.is_dir() or not any(root.iterdir()):
        parser.error('workspace must be an existing, nonempty directory')
    if args.check is not None and not LOW <= args.check <= HIGH:
        parser.error('GUID is outside Serp\'s reserved interval')
    data = scan(root)
    print(json.dumps({'guids': len(data['guids']), 'files': data['scanned_text_files'],
                      'warnings': data['warnings'], 'definition_pairs': {
                          s: sum(p['status'] == s for p in data['definition_pairs'])
                          for s in ('same-ModID', 'declared-incompatible', 'review-required')}}, indent=2))
    if args.write:
        for name, content in [('serp-guid-usage.json', json.dumps(compact(data), ensure_ascii=False, indent=2) + '\n'),
                              ('serp-guid-usage.md', markdown(data))]:
            (DOC / 'reference' / name).write_bytes(content.replace('\n', '\r\n').encode('utf-8'))
    if args.check is not None:
        hits = data['guids'].get(str(args.check), [])
        print(json.dumps(hits, ensure_ascii=False, indent=2))
        return 1 if hits else (2 if data['warnings'] else 0)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
