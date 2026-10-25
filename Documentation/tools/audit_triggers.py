"""Extract traceable trigger evidence. Extraction never marks a semantic review complete."""
from workspace_paths import source_path
from pathlib import Path
from collections import defaultdict, Counter
import copy
import hashlib
import json
import re
from lxml import etree as ET
from inventory import ROOT, OUT, VANILLA, decode, write_json

DEST = OUT / 'triggers'
ASSET = VANILLA / 'data/config/export/main/asset'
PATTERN = re.compile(r'trigger|condition|registertrigger|resettrigger|unlock|processing|checkedparticipant|sessionfilter|inheritarea|questarea|secondpart', re.I)

def stamp(path):
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def xml(node):
    return ET.tostring(node, encoding='unicode', pretty_print=True)

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))

def main():
    DEST.mkdir(parents=True, exist_ok=True)
    parser = ET.XMLParser(huge_tree=True)
    templates = {n.findtext('Name'): n for n in ET.parse(str(ASSET/'templates.xml'), parser).xpath('//Template[Name]')}
    schema = {n.findtext('Name'): n for n in ET.parse(str(ASSET/'properties-toolone.xml'), parser).xpath('//Property[Name]')}
    defaults_tree = ET.parse(str(ASSET/'properties.xml'), parser)
    defaults = {n.tag: n for n in defaults_tree.xpath('//DefaultValues/*')}
    container_defaults = {n.tag: n for n in defaults_tree.xpath('//DefaultContainerValues/*')}
    datasets = {n.findtext('Name'): n for n in ET.parse(str(ASSET/'datasets.xml'), parser).xpath('//DataSet[Name]')}
    condition_names = sorted(n for n, t in templates.items() if t.find('Properties/Condition') is not None)
    common = {'Trigger', 'AutoCreateTrigger', 'FeatureUnlock', 'UnlockableAsset', 'ActionRegisterTrigger',
              'ActionResetTrigger', 'ActionExecuteScript', 'ActionStartQuest', 'ActionSpawnObjects', 'Quest', 'ActionLink',
              'ActionUnlockAsset', 'ActionLockAsset', 'ActionDelayedActions', 'Actions', 'EmptyAutoCreateValue'}
    selected_templates = set(condition_names) | common
    selected_templates.update(n for n, t in templates.items() if any(x.tag.startswith('Condition') for x in t.findall('Properties/*')))
    prop_names = {'Trigger', 'TriggerSetup', 'Condition', 'ConditionPropsNegatable', 'Locked', 'Unlockable', 'Action', 'SessionFilter', 'ObjectFilter'}
    prop_names.update(n for n in schema if n.startswith('Condition'))
    for name in selected_templates:
        if name in templates:
            prop_names.update(n.tag for n in templates[name].findall('Properties/*'))
    ds_names = set()
    for name in prop_names:
        if name in schema:
            ds_names.update(n.text for n in schema[name].iter('DataSet') if n.text)
    examples, uses, assets = defaultdict(list), Counter(), {}
    wanted_ids = {'130248', '15000003', '1010346', '700055', '180023', '15000000', '15000002', '15000001'}
    # Retain whole owning records, including embedded definitions, before clearing.
    for _, node in ET.iterparse(str(ASSET/'assets.xml'), events=('end',), tag='Asset', huge_tree=True):
        guid = node.findtext('Values/Standard/GUID')
        if not guid:
            continue
        names = set(n.text for n in node.iter('Template') if n.text)
        retain = guid in wanted_ids
        for name in names & selected_templates:
            uses[name] += 1
            if len(examples[name]) < 2:
                retain = True
                snippets = [xml(n.getparent()) for n in node.iter('Template') if n.text == name]
                examples[name].append({'guid': guid, 'name': node.findtext('Values/Standard/Name'),
                                       'line': node.sourceline, 'base': node.findtext('BaseAssetGUID'), 'definitions': snippets})
        if retain:
            assets[guid] = {'guid': guid, 'line': node.sourceline, 'template': node.findtext('Template'),
                            'base': node.findtext('BaseAssetGUID'), 'xml': xml(node)}
        node.clear()
        while node.getprevious() is not None:
            del node.getparent()[0]
    needed = {a['base'] for a in assets.values() if a['base']} - assets.keys()
    while needed:
        found = set()
        for _, node in ET.iterparse(str(ASSET/'assets.xml'), events=('end',), tag='Asset', huge_tree=True):
            guid = node.findtext('Values/Standard/GUID')
            if guid in needed:
                assets[guid] = {'guid': guid, 'line': node.sourceline, 'template': node.findtext('Template'),
                                'base': node.findtext('BaseAssetGUID'), 'xml': xml(node)}
                found.add(guid)
            if guid:
                node.clear()
                while node.getprevious() is not None:
                    del node.getparent()[0]
        if needed - found:
            raise RuntimeError('Missing bases: ' + repr(needed-found))
        needed = {a['base'] for a in assets.values() if a['base']} - assets.keys()
    # Store exact source definitions, not guessed field/default summaries.
    contracts = {'status': 'extracted; source definitions and examples require semantic review',
                 'sources': [stamp(ASSET/n) for n in ['assets.xml', 'templates.xml', 'properties-toolone.xml', 'properties.xml', 'datasets.xml']],
                 'templates': {n: {'line': templates[n].sourceline, 'xml': xml(templates[n])} for n in sorted(selected_templates) if n in templates},
                 'properties': {n: {'line': schema[n].sourceline, 'xml': xml(schema[n]),
                                    'defaults_xml': xml(defaults[n]) if n in defaults else None,
                                    'container_defaults_xml': xml(container_defaults[n]) if n in container_defaults else None} for n in sorted(prop_names) if n in schema},
                 'datasets': {n: {'line': datasets[n].sourceline, 'xml': xml(datasets[n])} for n in sorted(ds_names) if n in datasets},
                 'examples': dict(examples), 'native_owning_asset_counts': dict(uses), 'assets': assets}
    write_json(DEST/'vanilla.json', contracts)
    rows = json.loads((OUT/'source-inventory.json').read_text('utf-8'))
    # Check the live workspace as well: an older inventory can omit newly added mod files.
    known_paths = {str(source_path(r['path']).resolve()).casefold() for r in rows}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in {'.xml', '.lua', '.md', '.txt', '.json', '.jsonc'}:
            continue
        if any(p in {'Documentation', '.git', '.codex', '.agents', 'node_modules', 'third_party'} for p in path.relative_to(ROOT).parts):
            continue
        if str(path.resolve()).casefold() not in known_paths:
            rel = path.relative_to(ROOT).as_posix()
            rows.append({'id': 'workspace:'+rel, 'group': 'workspace', 'path': str(path)})
    sources, comments, shapes = [], {}, {}
    parse_errors = []
    groups = defaultdict(list)
    for row in rows:
        if row.get('group') != 'workspace' and not row['id'].startswith('notes:'):
            continue
        path = source_path(row['path'])
        if path.suffix.lower() not in {'.xml', '.lua', '.md', '.txt', '.json', '.jsonc'}:
            continue
        raw = path.read_bytes()
        text, encoding = decode(raw)
        if not PATTERN.search(text):
            continue
        # Exclude merely general prose with no gameplay condition/trigger reference.
        if not re.search(r'<(?:Template>Condition|Trigger|Condition)|[Ss]ub[Tt]rigger|[Rr]egister[Tt]rigger|[Rr]eset[Tt]rigger|[Tt]rigger', text):
            continue
        digest = hashlib.sha256(raw).hexdigest()
        sources.append({'id': row['id'], **stamp(path), 'encoding': encoding,
                        'status': 'extracted; trigger-scope review pending'})
        groups[digest].append(row['id'])
        if len(groups[digest]) > 1:
            continue
        blocks = []
        if path.suffix.lower() == '.xml':
            for m in re.finditer(r'<!--(.*?)-->', text, re.S):
                body = m.group(1).strip()
                if body:
                    blocks.append((text.count('\n', 0, m.start())+1, body))
        elif path.suffix.lower() == '.lua':
            for i, line in enumerate(text.splitlines(), 1):
                if '--' in line:
                    blocks.append((i, line.split('--', 1)[1].strip()))
        else:
            blocks = [(i, line.strip()) for i, line in enumerate(text.splitlines(), 1) if line.strip() and not line.strip().startswith('<')]
        for line, body in blocks:
            # XML comments adjacent to conditions often omit their names; retain all comments of these files.
            normalized = re.sub(r'\s+', ' ', body)
            key = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
            entry = comments.setdefault(key, {'text': normalized, 'sources': []})
            entry['sources'].append({'id': row['id'], 'line': line})
        # Native-layout XML can be read structurally even when a mod mixes includes/patch fragments.
        try:
            # Decode for inspection without changing original bytes; a UTF-16 declaration
            # must not be left on a re-encoded UTF-8 parsing buffer.
            parse_text = re.sub(r'<\?xml[^?]*\?>', '', text, count=1)
            tree = ET.fromstring(parse_text.encode('utf-8'), ET.XMLParser(huge_tree=True, recover=False))
            for n in tree.iter('Trigger'):
                shape = re.sub(r'\s+', ' ', xml(n)).strip()
                key = hashlib.sha256(shape.encode('utf-8')).hexdigest()
                entry = shapes.setdefault(key, {'xml': shape, 'sources': []})
                entry['sources'].append({'source': row['id'], 'line': n.sourceline})
        except (ET.XMLSyntaxError, ValueError) as exc:
            if path.suffix.lower() == '.xml':
                parse_errors.append({'source': row['id'], 'error': str(exc),
                                     'treatment': 'Original text/comments retained; standalone parse cannot certify this source. No mod source repaired.'})
    shape_index = {k: {'sources': v['sources'], 'templates': sorted(set(re.findall(r'<Template>([^<]+)</Template>', v['xml']))),
                       'fields': sorted(set(re.findall(r'<([A-Za-z][A-Za-z0-9_]*)[ >]', v['xml']))),
                       'completion_orders': re.findall(r'<SubConditionCompletionOrder>([^<]+)</SubConditionCompletionOrder>', v['xml'])} for k, v in shapes.items()}
    write_json(DEST/'workspace.json', {'status': 'extracted; see review outcomes for completed scope',
                                      'sources': sources, 'duplicate_groups': list(groups.values()),
                                      'comments': list(comments.values()), 'trigger_shape_index': shape_index,
                                      'standalone_xml_parse_diagnostics': parse_errors})
    relevant = [c for c in comments.values() if PATTERN.search(c['text'])]
    for start in range(0, len(relevant), 100):
        lines = ['# Trigger source comments: extraction, not review', '']
        for i, c in enumerate(relevant[start:start+100], start+1):
            origins = '; '.join(f"{s['id']}:{s['line']}" for s in c['sources'][:3])
            lines.extend([f"## C{i}: {origins}", c['text'], ''])
        write(DEST/f'comments-{start//100+1:02}.md', '\n'.join(lines)+'\n')
    write_json(DEST/'extraction-summary.json', {'condition_templates': len(condition_names), 'property_contracts': len(contracts['properties']),
                                               'datasets': len(contracts['datasets']), 'owning_assets_and_bases': len(assets),
                                               'workspace_sources': len(sources), 'unique_source_groups': len(groups),
                                               'unique_comments': len(comments), 'keyword_comments': len(relevant), 'trigger_shapes': len(shapes),
                                               'standalone_xml_parse_diagnostics': len(parse_errors)})
    print(json.dumps(json.loads((DEST/'extraction-summary.json').read_text('utf-8'))))

if __name__ == '__main__':
    main()
