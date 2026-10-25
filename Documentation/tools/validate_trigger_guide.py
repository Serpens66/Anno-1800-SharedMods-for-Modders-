"""Validate the standalone guide and execute its complete ModOps offline."""
import copy
import hashlib
import json
import re
import subprocess
from workspace_paths import source_path
from pathlib import Path
from lxml import etree as ET
from inventory import write_json
from validate_loader import EXE, write as loader_write
from validate_triggers import canonical, validate_asset_structure
from verify_trigger_documentation import anchors

DOC = Path(__file__).resolve().parents[1]
GUIDE = DOC.parent/'Trigger_Guide.md'
OUT = DOC/'reference/validation/trigger-guide'


def write(path, text):
    # Embedded fences are read from a CRLF Markdown file; the older fixture
    # writer expects LF input before adding CRLF itself.
    loader_write(path, text.replace('\r\n', '\n'))


def main():
    raw = GUIDE.read_bytes()
    text = raw.decode('utf-8')
    assert b'\n' not in raw.replace(b'\r\n', b'') and b'\r' not in raw.replace(b'\r\n',b''), 'Guide must be CRLF'
    assert '{{' not in text, 'Unexpanded guide marker'
    contracts = json.loads((DOC/'reference/triggers/vanilla.json').read_text('utf-8'))
    audit = json.loads((OUT/'native-audit.json').read_text('utf-8'))
    for source in audit['sources']:
        assert hashlib.sha256(source_path(source['path']).read_bytes()).hexdigest() == source['sha256'], source['path']
    html_anchors = re.findall(r'<a id="([^"]+)"></a>', text)
    assert len(html_anchors) == len(set(html_anchors)), 'Duplicate explicit anchor'
    guide_anchors = anchors(GUIDE)
    links, fragments, public_links = 0, 0, []
    assert 'Documentation/' not in text and 'Documentation\\' not in text, 'Private documentation path in reader guide'
    allowed_repositories = {'https://github.com/Serpens66/Anno-1800-Mods', 'https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-'}
    code_links = json.loads((OUT/'public-code-links.json').read_text('utf-8'))['records']
    assert {row['guid'] for row in code_links} == {'1500003013', '1500003820', '1500003835', '1500001103', '1500004302', '1500004332'}
    for row in code_links:
        for key, line_key in [('url', 'asset_line'), ('guid_url', 'guid_line')]:
            url = row[key]
            assert any(url.startswith(repo+'/blob/') for repo in allowed_repositories)
            assert url.endswith('#L'+str(row[line_key]))
            assert text.count('](<'+url+'>)') == 1, ('Missing or duplicate public source link', row['guid'], key)
    allowed_public_links = allowed_repositories | {row[key] for row in code_links for key in ['url', 'guid_url']}
    for target in re.findall(r'\]\((<[^>]+>|[^)]+)\)', text):
        target = target.strip('<>')
        if re.match(r'^[a-z]+://', target, re.I):
            assert target in allowed_public_links, ('Unapproved external link', target)
            public_links.append(target)
            continue
        assert target.startswith('#'), ('Reader depends on another local file', target)
        file, _, fragment = target.partition('#')
        path = (GUIDE.parent/file).resolve() if file else GUIDE
        # This report is written at the end of this run.
        assert path.exists() or path == OUT/'results.json', ('Broken link', target)
        links += 1
        if fragment and path.suffix == '.md':
            assert fragment in (guide_anchors if path == GUIDE else anchors(path)), ('Broken anchor', target)
            fragments += 1
    # Ensure every code fence is inside a details block, including default snapshots.
    depth, fenced = 0, False
    for line in text.splitlines():
        if line.startswith('<details>'):
            depth += 1
        if line.startswith('```'):
            assert depth > 0, 'Code outside collapsible block'
            fenced = not fenced
        if line == '</details>':
            assert depth > 0 and not fenced
            depth -= 1
    assert depth == 0 and not fenced
    native_templates = {name for name, row in contracts['templates'].items() if ET.fromstring(row['xml'].encode()).find('Properties/Condition') is not None}
    catalogue = text.split('## 17.',1)[1].split('### Common property',1)[0]
    found = re.findall(r'^\| `(Condition\w+)`:', catalogue, re.M)
    assert len(found) == 91 and set(found) == native_templates, 'Catalogue coverage differs'
    standalone = json.loads((OUT/'standalone-reference.json').read_text('utf-8'))
    assert set(standalone['condition_templates']) == native_templates
    reference_checks = {'properties':0, 'templates':0, 'datasets':0}
    for name, record in standalone['properties'].items():
        marker = '<a id="property-'+name.lower()+'"></a>'
        assert text.count(marker) == 1, ('Missing or duplicate property',name)
        section = text.split(marker,1)[1].split('<a id=',1)[0]
        actual = [ET.fromstring(block.strip().encode()) for block in re.findall(r'```xml\s*\n(.*?)\n```',section,re.S)]
        expected = [ET.fromstring(source.encode()) for source in record.values() if source]
        assert [canonical(n) for n in actual] == [canonical(n) for n in expected], ('Property schema/default drift',name)
        reference_checks['properties'] += 1
    for group, prefix in [('templates','template'),('datasets','dataset')]:
        for name, source in standalone[group].items():
            marker = '<a id="'+prefix+'-'+name.lower()+'"></a>'
            assert text.count(marker) == 1, ('Missing or duplicate reference',name)
            section = text.split(marker,1)[1].split('<a id=',1)[0]
            blocks = re.findall(r'```xml\s*\n(.*?)\n```',section,re.S)
            assert len(blocks) == 1 and canonical(ET.fromstring(blocks[0].strip().encode())) == canonical(ET.fromstring(source.encode())), ('Reference drift',name)
            reference_checks[group] += 1
    property_names = set(standalone['properties'])
    dataset_names = set(standalone['datasets'])
    for source in standalone['templates'].values():
        assert {n.tag for n in ET.fromstring(source.encode()).findall('Properties/*')} <= property_names, 'Template missing in-file property'
    for record in standalone['properties'].values():
        assert {n.text for n in ET.fromstring(record['schema'].encode()).iter('DataSet') if n.text} <= dataset_names, 'Property missing in-file dataset'
    manifest = json.loads((OUT/'examples.json').read_text('utf-8'))
    blocks = re.findall(r'```xml\s*\n(.*?)\n```', text, re.S)
    complete, parsed, real_assets = [], [], []
    for block in blocks:
        block = block.strip()
        tokens = sorted(set(re.findall(r'\b[A-Z_]+_GUID\b', block)))
        bound = block
        for index, token in enumerate(tokens):
            bound = bound.replace(token, str(2001000100+index))
        root = ET.fromstring(bound.encode('utf-8'))
        parsed.append(root.tag)
        if root.tag == 'ModOps':
            complete.append((block, root))
        elif root.tag == 'Asset':
            real_assets.append(root)
        elif root.tag in {'TriggerCondition', 'TriggerAction', 'SubTrigger', 'Trigger'}:
            validate_asset_structure(root, contracts)
    assert len(complete) == len(manifest) == 9
    assert len(real_assets) == 7, 'Opening native asset plus six reviewed cases'
    for case, (block, _) in zip(manifest, complete):
        assert hashlib.sha256(block.strip().replace('\r\n','\n').encode()).hexdigest() == case['sha256'], ('Example changed', case['id'])
    anchor = ET.fromstring(audit['assets']['130248']['xml'].encode())
    fixture = ET.Element('Assets')
    fixture.append(copy.deepcopy(anchor))
    original = OUT/'original.xml'
    write(original, ET.tostring(fixture, encoding='unicode', pretty_print=True))
    all_guids = {str(row['guid']) for row in json.loads((DOC/'reference/vanilla-asset-index.json').read_text('utf-8'))}
    reports, trees = [], {}
    for number, (case, (block, _)) in enumerate(zip(manifest, complete)):
        tokens = sorted(set(re.findall(r'\b[A-Z_]+_GUID\b', block)))
        bindings = {token: str(2001000100+number*20+index) for index, token in enumerate(tokens)}
        assert not set(bindings.values()) & all_guids, 'Native collision in fixture'
        for token, value in bindings.items():
            block = block.replace(token, value)
        root = ET.fromstring(block.encode())
        validate_asset_structure(root, contracts)
        assets = root.findall('ModOp/Asset')
        by_guid = {a.findtext('Values/Standard/GUID'): a for a in assets}
        assert len(by_guid) == len(assets)
        for ref in root.xpath('//ActionUnlockAsset/UnlockAssets/Item/Asset | //ActionLockAsset/LockAssets/Item/Asset'):
            assert ref.text in by_guid and by_guid[ref.text].find('Values/Locked') is not None
        folder = OUT/case['id']
        patch = folder/'data/config/export/main/asset/assets.xml'
        output = folder/'patched.xml'
        write(patch, block)
        args = [str(EXE), '-c', 'patch', '-m', str(folder), '-o', str(output), str(original), str(patch)]
        run = subprocess.run(args, capture_output=True, encoding='utf-8', errors='replace')
        log = run.stdout+run.stderr
        write(folder/'xmltest.log', log)
        assert run.returncode == 0 and '[error]' not in log, log
        result = ET.parse(str(output))
        originals = result.xpath('//Asset[Values/Standard/GUID="130248"]')
        assert len(originals) == 1 and canonical(originals[0]) == canonical(anchor), 'Anchor changed'
        for guid, asset in by_guid.items():
            actual = result.xpath('//Asset[Values/Standard/GUID="'+guid+'"]')
            assert len(actual) == 1 and canonical(actual[0]) == canonical(asset), ('Payload altered',guid)
        trees[case['id']] = assets[-1].find('Values/Trigger')
        reports.append({'case':case['id'], 'passed':True, 'bindings':bindings, 'command':args,
            'assertions':['native schema and enum membership','all result action references resolve to Locked assets','unique fixture identities','complete anchor and insertion payload preserved'], 'external':case.get('external',[])})
    # Four reader scenarios: verify the meaningful structural choices, not runtime claims.
    tree = trees['simultaneous']
    for _ in range(2):
        assert len(tree.findall('SubTriggers/Item')) == 1 and not tree.findall('TriggerActions/Item')
        tree = tree.find('SubTriggers/Item/SubTrigger/Values/Trigger')
    assert len(tree.findall('TriggerActions/Item')) == 1
    assert trees['priority'].findtext('TriggerCondition/Values/Condition/SubConditionCompletionOrder') == 'MutuallyExclusive'
    assert len(trees['priority'].findall('SubTriggers/Item')) == 2
    assert trees['repeat'].findtext('TriggerCondition/Values/ConditionTimer/TimeLimit') == '10000'
    assert trees['repeat'].findtext('ResetTrigger/Values/Trigger/TriggerCondition/Values/ConditionTimer/TimeLimit') == '1000'
    assert trees['removal-safe'].findtext('TriggerCondition/Values/ConditionPropsNegatable/NegateCondition') == '1'
    assert not trees['removal-safe'].findall('TriggerActions/Item')
    assert 'one GUID does not guarantee one active instance' in text or 'multiple concurrent registrations' in text
    assert 'exactly the same tick' in text and 'fresh' in text and 'snapshot' in text
    # Real mod presentation may change only comments, indentation and the display Name.
    for asset in real_assets:
        guid = asset.findtext('Values/Standard/GUID')
        if guid == '130221':
            expected = ET.fromstring(audit['assets'][guid]['xml'].encode())
        else:
            expected = ET.parse(str(DOC/'reference/triggers/mod-cases'/(guid+'.xml')), ET.XMLParser(remove_comments=True)).getroot()
            expected.find('Values/Standard/Name').text = 'Reviewed trigger '+guid
        assert canonical(asset) == canonical(expected), ('Real case presentation changes behavior', guid)
    report = {'date':'2026-10-03','guide':str(GUIDE),'guide_sha256':hashlib.sha256(raw).hexdigest(),
        'utf8_crlf':True,'xml_blocks_checked':len(parsed),'collapsible_sections':text.count('<details>'),
        'local_links_checked':links,'heading_fragments_checked':fragments,'catalogue_templates':len(found),
        'standalone_reference_checks':reference_checks,'optional_public_repository_links':public_links,'other_file_links':0,
        'cases':reports,'reader_scenarios':['nested complex live-state combination','prioritized complete alternatives','main timer plus reset timer','presence guard and documented save/Coop workflow'],
        'real_asset_presentations_checked':len(real_assets),'findings':[],
        'evaluator_sha256':hashlib.sha256(EXE.read_bytes()).hexdigest(),
        'limits':'Offline XML/schema/patch and source-preservation checks; authored reader walkthroughs, not an independent agent test; no game, Lua API, save migration, dependency selector or MP timing test.'}
    write_json(OUT/'results.json',report)
    print(json.dumps({k:report[k] for k in ['xml_blocks_checked','local_links_checked','heading_fragments_checked','catalogue_templates','collapsible_sections','findings']}))


if __name__ == '__main__':
    main()
