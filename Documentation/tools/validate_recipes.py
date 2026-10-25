"""Validate recipe selections against dataAlle, then patch isolated exact assets."""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess
from lxml import etree as ET
from validate_loader import EXE, write
from inventory import VANILLA

DOC = Path(__file__).resolve().parents[1]
OUT = DOC / 'reference/validation/recipes'
SOURCE = VANILLA / 'data/config/export/main/asset/assets.xml'

def main():
    selected, counts = {}, {'2001241': 0, '130248': 0}
    guid_in_use = False
    # The private-use GUID is only used in a documentation fixture, never deployed.
    example_guid = '2001000000'
    for _, node in ET.iterparse(str(SOURCE), events=('end',), tag='Asset', huge_tree=True):
        guid = node.findtext('Values/Standard/GUID')
        if guid in counts:
            counts[guid] += 1
            selected[guid] = copy.deepcopy(node)
        if guid == example_guid:
            guid_in_use = True
        if guid:
            node.clear()
            while node.getprevious() is not None:
                del node.getparent()[0]
    assert counts == {'2001241': 1, '130248': 1}, counts
    assert not guid_in_use, 'Example identity collides with extracted vanilla'
    assert selected['2001241'].findtext('Values/BuildingBaseTiles/HarbourConstructionAreaRadius') == '28'
    assert selected['130248'].findtext('Template') == 'Trigger'
    blocks = re.findall(r'```xml\s*\n(.*?)```', (DOC/'recipes/basic-workflows.md').read_text('utf-8'), re.S)
    reports = []
    for index, block in enumerate(blocks):
        case = OUT / ('change-radius' if index == 0 else 'new-trigger')
        target = case/'original.xml'
        root = ET.Element('Assets')
        root.append(copy.deepcopy(selected['2001241' if index == 0 else '130248']))
        write(target, ET.tostring(root, encoding='unicode', pretty_print=True))
        patch = case/'data/config/export/main/asset/assets.xml'
        write(patch, block.replace('CUSTOM_TRIGGER_GUID', example_guid))
        output = case/'patched.xml'
        args = [str(EXE), '-c', 'patch', '-m', str(case), '-o', str(output), str(target), str(patch)]
        run = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
        log = run.stdout + run.stderr
        write(case/'xmltest.log', log)
        assert run.returncode == 0 and '[error]' not in log, log
        tree = ET.parse(str(output))
        if index == 0:
            patched = tree.xpath('//Asset[Values/Standard/GUID="2001241"]')[0]
            assert patched.findtext('Values/BuildingBaseTiles/HarbourConstructionAreaRadius') == '40'
            before, after = copy.deepcopy(selected['2001241']), copy.deepcopy(patched)
            after.find('Values/BuildingBaseTiles/HarbourConstructionAreaRadius').text = '28'
            # Ignore whitespace; compare the complete preserved asset structure.
            def canonical(node):
                return (node.tag, tuple(sorted(node.attrib.items())), (node.text or '').strip(), tuple(canonical(n) for n in node))
            assert canonical(before) == canonical(after)
            assertion = 'Radius 28 -> 40; all other original asset nodes and attributes retained'
        else:
            new = tree.xpath('//Asset[Values/Standard/GUID="'+example_guid+'"]')
            assert len(new) == 1 and len(tree.xpath('//Asset[Values/Standard/GUID="130248"]')) == 1
            assert new[0].findtext('Template') == 'Trigger'
            assert new[0].findtext('Values/Trigger/TriggerCondition/Template') == 'ConditionAlwaysTrue'
            assert new[0].findtext('Values/Trigger/TriggerActions/Item/TriggerAction/Values/ActionExecuteScript/ScriptFileName') == 'data/example_author/startup.lua'
            assert new[0].findtext('Values/TriggerSetup/UsedBySecondParties') == '0'
            assertion = 'One new Trigger; original sibling preserved; inline condition/action and second-party override intact'
        reports.append({'case':case.name, 'command':args, 'assertion':assertion, 'passed':True})
    write(OUT/'results.json', json.dumps({'date':'2026-10-03', 'source':str(SOURCE),
          'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(), 'full_source_guid_matches':counts,
          'fixture_guid':example_guid, 'scope':'Full-source selection check; isolated exact-asset offline patch, no deployment or runtime test',
          'cases':reports}, indent=2)+'\n')
    print('PASS: full vanilla GUID selections and both exact-asset XML recipe patches')

if __name__ == '__main__':
    main()
