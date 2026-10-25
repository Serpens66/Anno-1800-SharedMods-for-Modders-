"""Check trigger examples against native schemas and actual offline XML patch output."""
from workspace_paths import source_path
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess
from lxml import etree as ET
from inventory import VANILLA, write_json
from audit_triggers import DEST, write
from validate_loader import EXE

DOC = Path(__file__).resolve().parents[1]
OUT = DOC/'reference/validation/triggers'

def canonical(node):
    return (node.tag, tuple(sorted(node.attrib.items())), (node.text or '').strip(), tuple(canonical(x) for x in node if isinstance(x.tag, str)))

def validate_definition(node, definitions, datasets):
    by_name = {x.findtext('Name'): x for x in definitions.findall('ValueDefinition')}
    for child in node:
        if not isinstance(child.tag, str):
            continue
        assert child.tag in by_name, 'Undeclared field: '+child.tag+' in '+node.tag
        f = by_name[child.tag]
        kind = f.findtext('DataType')
        if kind in {'Vector', 'Array', 'Struct'}:
            items = f.find('Items')
            if kind == 'Vector':
                assert all(x.tag == 'Item' for x in child), 'Vector requires Item: '+child.tag
                for item in child:
                    validate_definition(item, items, datasets)
            elif kind == 'Struct':
                validate_definition(child, items, datasets)
        elif kind in {'Choice', 'Flags'}:
            ds = f.findtext('DataSet')
            if ds and child.text:
                allowed = {x.findtext('Name') for x in datasets[ds].findall('Items/Item')}
                for token in child.text.split(';'):
                    assert token in allowed, 'Invalid enum '+ds+': '+token
        elif kind == 'AutoCreateAsset':
            assert child.find('Template') is not None or child.find('IsBaseAutoCreateAsset') is not None, 'Missing embedded identity'
        elif kind == 'Boolean':
            assert child.text in {None, '0', '1'}, 'Invalid Boolean in example'
        elif kind in {'Integer', 'Int64', 'Time', 'Asset', 'Text'} and child.text:
            int(child.text)

def validate_asset_structure(root, contracts):
    templates = {n: ET.fromstring(x['xml'].encode('utf-8')) for n, x in contracts['templates'].items()}
    schema = {n: ET.fromstring(x['xml'].encode('utf-8')) for n, x in contracts['properties'].items()}
    datasets = {n: ET.fromstring(x['xml'].encode('utf-8')) for n, x in contracts['datasets'].items()}
    for ident in root.iter('Template'):
        name = ident.text
        assert name in templates, 'Uncaptured template '+str(name)
        values = ident.getparent().find('Values')
        assert values is not None, 'Missing Values'
        allowed = {x.tag for x in templates[name].findall('Properties/*')}
        for prop in values:
            assert prop.tag in allowed, 'Property '+prop.tag+' does not belong to template '+name
            validate_definition(prop, schema[prop.tag], datasets)

def main():
    source = VANILLA/'data/config/export/main/asset/assets.xml'
    contracts = json.loads((DEST/'vanilla.json').read_text('utf-8'))
    assert hashlib.sha256(source.read_bytes()).hexdigest() == contracts['sources'][0]['sha256'], 'Source changed since audit'
    anchor, counts, guids = None, 0, set()
    for _, node in ET.iterparse(str(source), events=('end',), tag='Asset', huge_tree=True):
        guid = node.findtext('Values/Standard/GUID')
        if guid:
            guids.add(guid)
            if guid == '130248':
                counts += 1
                anchor = copy.deepcopy(node)
            node.clear()
            while node.getprevious() is not None:
                del node.getparent()[0]
    assert counts == 1 and anchor.findtext('Template') == 'Trigger'
    cases = json.loads((DEST/'examples/manifest.json').read_text('utf-8'))
    original = ET.Element('Assets')
    original.append(anchor)
    original_path = OUT/'original.xml'
    write(original_path, ET.tostring(original, encoding='unicode', pretty_print=True))
    reports, bound_roots = [], {}
    for number, case in enumerate(cases):
        text = source_path(case['path']).read_text('utf-8')
        bindings = {token: str(2001000100+number*10+i) for i, token in enumerate(case['tokens'])}
        assert not set(bindings.values()) & guids, 'Vanilla fixture GUID collision'
        for token, value in bindings.items():
            text = text.replace(token, value)
        assert not re.search(r'\b[A-Z_]+_GUID\b', text), 'Unbound placeholder'
        root = ET.fromstring(text.encode('utf-8'))
        validate_asset_structure(root, contracts)
        all_new = root.findall('ModOp/Asset')
        assert len({a.findtext('Values/Standard/GUID') for a in all_new}) == len(all_new)
        by_guid = {a.findtext('Values/Standard/GUID'): a for a in all_new}
        for reference in root.xpath('//ActionUnlockAsset/UnlockAssets/Item/Asset | //ActionLockAsset/LockAssets/Item/Asset'):
            assert reference.text in by_guid and by_guid[reference.text].find('Values/Locked') is not None
        bound_roots[case['case']] = root
        mod = OUT/case['case']
        patch = mod/'data/config/export/main/asset/assets.xml'
        output = mod/'patched.xml'
        write(patch, text)
        args = [str(EXE), '-c', 'patch', '-m', str(mod), '-o', str(output), str(original_path), str(patch)]
        run = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
        log = run.stdout+run.stderr
        write(mod/'xmltest.log', log)
        assert run.returncode == 0 and '[error]' not in log, log
        result = ET.parse(str(output))
        remaining = result.xpath('//Asset[Values/Standard/GUID="130248"]')
        assert len(remaining) == 1 and canonical(remaining[0]) == canonical(anchor), 'Original anchor changed'
        for asset in all_new:
            matches = result.xpath('//Asset[Values/Standard/GUID="'+asset.findtext('Values/Standard/GUID')+'"]')
            assert len(matches)==1 and canonical(matches[0])==canonical(asset), 'Payload altered or missing'
        reports.append({'case': case['case'], 'passed': True, 'bindings': bindings, 'command': args,
                        'assertions': ['native template/property/field and enum contracts', 'action targets have Locked',
                                       'unique private identities', 'exact full anchor preservation', 'complete insertion payload retained'],
                        'external_contracts_not_executed': case['external']})
    # Structural intent checks are useful independently of the XML evaluator's syntax acceptance.
    t = bound_roots['simultaneous'].findall('ModOp/Asset')[-1].find('Values/Trigger')
    assert not t.findall('TriggerActions/Item')
    for _ in range(2):
        assert len(t.findall('SubTriggers/Item')) == 1
        t = t.find('SubTriggers/Item/SubTrigger/Values/Trigger')
    assert len(t.findall('TriggerActions/Item')) == 1
    root = bound_roots['sequence'].findall('ModOp/Asset')[-1]
    assert root.findtext('Values/Trigger/TriggerCondition/Values/Condition/SubConditionCompletionOrder') == 'Linear'
    assert len(root.findall('Values/Trigger/SubTriggers/Item')) == 2
    root = bound_roots['priority'].findall('ModOp/Asset')[-1]
    assert root.findtext('Values/Trigger/TriggerCondition/Values/Condition/SubConditionCompletionOrder') == 'MutuallyExclusive'
    root = bound_roots['optional'].findall('ModOp/Asset')[-1]
    assert root.findtext('Values/Trigger/SubTriggers/Item/SubTrigger/Values/Trigger/TriggerCondition/Values/Condition/IsOptional') == '1'
    root = bound_roots['repeat'].findall('ModOp/Asset')[-1]
    assert root.findtext('Values/Trigger/ResetTrigger/Values/Trigger/TriggerCondition/Values/ConditionTimer/TimeLimit') == '1000'
    root = bound_roots['removal-safe'].findall('ModOp/Asset')[-1]
    assert root.findtext('Values/Trigger/TriggerCondition/Values/ConditionPropsNegatable/NegateCondition') == '1'
    assert not root.findall('Values/Trigger/TriggerActions/Item'), 'Actions must remain behind the presence gate'
    negatives = []
    for name, mutate in [
        ('misplaced-completion-mode', lambda r: r.find('.//Trigger').append(ET.fromstring(b'<SubConditionCompletionOrder>Linear</SubConditionCompletionOrder>'))),
        ('invalid-event-token', lambda r: setattr(r.find('.//ConditionEvent/ConditionEvent'), 'text', 'SessionEntered')),
        ('template-property-name-confusion', lambda r: setattr(r.find('.//TriggerCondition/Template'), 'text', 'ConditionUnlockedList')),
    ]:
        r = copy.deepcopy(bound_roots['sequence'])
        mutate(r)
        try:
            validate_asset_structure(r, contracts)
        except AssertionError:
            negatives.append({'case': name, 'rejected': True})
        else:
            raise AssertionError('Checker failed to reject '+name)
    write_json(OUT/'results.json', {'date': '2026-10-03', 'scope': 'Offline source/structure/patch assertions; no gameplay, timing, dependency loading or MP execution',
                                  'vanilla_sha256': contracts['sources'][0]['sha256'], 'evaluator_sha256': hashlib.sha256(EXE.read_bytes()).hexdigest(),
                                  'anchor_matches_in_full_vanilla': counts, 'cases': reports, 'negative_contract_cases': negatives,
                                  'intent_structure_checks_passed': True})
    print('PASS: eight complete recipes, exact vanilla anchor preservation, tree intent and three rejected invalid contracts.')

if __name__ == '__main__':
    main()
