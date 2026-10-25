"""Offline GU17.1 compatibility checks; never launches the game or repairs saves."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

from lxml import etree as ET

DOC = Path(__file__).resolve().parents[1]
ROOT = DOC.parent.parent
CAMPAIGN = ROOT / 'Anno-1800-Mods/YouKnowWhatYouDo-Mods/Campaign in Coop (Serp)'
STORY = CAMPAIGN.parent / 'Story Quests in Coop (Serp)'
HELPER = DOC.parent / 'shared_CheckSingleHuman'
PATCH = CAMPAIGN / 'data/config/export/main/asset/AntiDesync/ADLeaveUI.include.xml'
EXE = Path(r'C:\Users\Serpens66\.vscode\extensions\jakobharder.anno-modding-tools-2.3.1\external\xmltest.exe')
VANILLA = ROOT.parent / 'Anno1800 RDA unpacked/dataAlle/data/config/export/main/asset/assets.xml'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    path.write_bytes(text.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))


def normalized(node):
    parser = ET.XMLParser(remove_blank_text=True)
    return ET.tostring(ET.fromstring(ET.tostring(node), parser), method='c14n', with_comments=False)


def walk_assets(path):
    for _, node in ET.iterparse(str(path), events=('end',), tag='Asset', remove_blank_text=True):
        guid = node.findtext('Values/Standard/GUID')
        if not guid:
            continue
        yield guid, node
        node.clear()
        while node.getprevious() is not None:
            del node.getparent()[0]


def fingerprints(path):
    values = {}
    for guid, node in walk_assets(path):
        if guid in values:
            raise AssertionError('Duplicate asset GUID: ' + guid)
        values[guid] = hashlib.sha256(normalized(node)).hexdigest()
    return values


def document(*nodes):
    root = ET.Element('ModOps')
    for node in nodes:
        root.append(copy.deepcopy(node))
    return root


def foreign_item(delay):
    node = ET.fromstring('''<Item><SubTrigger><Template>AutoCreateTrigger</Template><Values><Trigger>
      <TriggerCondition><Template>ConditionTimer</Template><Values><Condition/><ConditionTimer>
      <TimeLimit>777</TimeLimit></ConditionTimer></Values></TriggerCondition>
      </Trigger></Values></SubTrigger></Item>''')
    node.find('.//TimeLimit').text = str(delay)
    return node


def run_patch(work, name, source, patch, mod):
    patchfile = work / (name + '-patch.xml')
    output = work / (name + '-output.xml')
    log = work / (name + '.log')
    write(patchfile, ET.tostring(patch, encoding='unicode'))
    args = [str(EXE), '-c', 'patch', '-v', '-m', str(mod), '-o', str(output), str(source), str(patchfile)]
    result = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
    write(log, result.stdout + result.stderr)
    diagnostics = [line for line in (result.stdout + result.stderr).splitlines()
                   if re.search(r'\[(?:error|warning)\]|No matching node', line, re.I)]
    assert result.returncode == 0 and output.is_file(), (name, result.returncode, diagnostics)
    assert not diagnostics, (name, diagnostics)
    receipt = {'name': name, 'exit_code': result.returncode, 'input_sha256': digest(source),
               'patch_sha256': digest(patchfile), 'output_sha256': digest(output),
               'log_sha256': digest(log), 'diagnostics': diagnostics}
    return output, receipt


def full_chain(work, baseline):
    stages = []
    source = VANILLA
    for index, mod in enumerate([HELPER, STORY, CAMPAIGN]):
        output = work / ('after-stage' + str(index) + '.xml')
        log = work / ('after-stage' + str(index) + '.log')
        args = [str(EXE), '-c', 'patch', '-v', '-m', str(mod), '-o', str(output), str(source),
                str(mod / 'data/config/export/main/asset/assets.xml')]
        run = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
        text = run.stdout + run.stderr
        write(log, text)
        assert run.returncode == 0 and output.is_file(), (index, run.returncode)
        diagnostics = [line for line in text.splitlines()
                       if re.search(r'\[(?:error|warning)\]|No matching node', line, re.I)]
        assert all('No matching node for Path' in line and
                   ('ResourceSetCondition' in line or 'RandomIsland' in line) for line in diagnostics), diagnostics
        stages.append({'stage': index, 'mod': mod.name, 'exit_code': run.returncode,
                       'input_sha256': digest(source), 'output_sha256': digest(output),
                       'log_sha256': digest(log), 'allowed_diagnostics': diagnostics})
        source = output
    before, after = fingerprints(baseline), fingerprints(source)
    assert before.keys() == after.keys(), 'Asset identities changed'
    changed = [guid for guid in before if before[guid] != after[guid]]
    assert not changed, changed
    return {'stages': stages, 'baseline_sha256': digest(baseline), 'assets_compared': len(before),
            'semantic_changes': changed, 'allowed_no_match_count': sum(len(s['allowed_diagnostics']) for s in stages)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True, help='Disposable output directory outside workspace')
    parser.add_argument('--baseline', type=Path, required=True, help='Full pre-change effective Campaign XML')
    parser.add_argument('--receipt', type=Path, default=DOC / 'reference/validation/mod-compatibility/results.json')
    args = parser.parse_args()
    assert args.baseline.is_file()
    work = args.work.resolve()
    assert not work.is_relative_to(ROOT.resolve()), 'Keep full vanilla-derived outputs outside workspace'
    assert args.baseline.resolve() not in {work / ('after-stage' + str(i) + '.xml') for i in range(3)}, 'Baseline must not be overwritten by this run'
    work.mkdir(parents=True, exist_ok=True)
    tree = ET.parse(str(PATCH))
    prep = tree.xpath('//ModOp[@GUID="151076" and @Type="merge" and @Path="/Values/Trigger"]')
    append = tree.xpath('//ModOp[@GUID="151076" and @Type="add" and @Path="/Values/Trigger/SubTriggers"]')
    assert len(prep) == len(append) == 1
    prep, append = prep[0], append[0]
    assert len(prep.find('SubTriggers')) == 0 and len(append.findall('Item')) == 1
    actual = document(prep, append)
    native = next(copy.deepcopy(n) for guid, n in walk_assets(VANILLA) if guid == '151076')
    assert native.find('Values/Trigger/SubTriggers') is None
    foreign_add = ET.Element('ModOp', Type='add', GUID='151076', Path='/Values/Trigger/SubTriggers')
    foreign_add.append(foreign_item(777))
    foreign = document(prep, foreign_add)
    old_add = ET.Element('ModOp', Type='add', GUID='151076', Path='/Values/Trigger')
    old_container = ET.SubElement(old_add, 'SubTriggers')
    old_container.append(copy.deepcopy(append.find('Item')))
    cases = []
    for kind in ['missing', 'empty', 'populated', 'foreign-before', 'foreign-after', 'merge-twice',
                 'repeat-add', 'positional-merge', 'legacy-duplicate', 'preexisting-duplicates']:
        fixture = ET.Element('Assets')
        fixture.append(copy.deepcopy(native))
        trigger = fixture.find('Asset/Values/Trigger')
        if kind not in ['missing', 'foreign-before', 'foreign-after']:
            container = ET.SubElement(trigger, 'SubTriggers')
            if kind in ['populated', 'merge-twice', 'positional-merge', 'legacy-duplicate', 'preexisting-duplicates']:
                container.append(foreign_item(777))
            if kind == 'positional-merge':
                container.append(foreign_item(888))
            if kind == 'preexisting-duplicates':
                ET.SubElement(trigger, 'SubTriggers').append(foreign_item(888))
        fixture_path = work / (kind + '-input.xml')
        write(fixture_path, ET.tostring(fixture, encoding='unicode'))
        sequence = [actual]
        if kind == 'foreign-before':
            sequence = [foreign, actual]
        elif kind == 'foreign-after':
            sequence = [actual, foreign]
        elif kind in ['merge-twice', 'preexisting-duplicates']:
            sequence = [document(prep, prep)]
        elif kind == 'repeat-add':
            sequence = [actual, actual]
        elif kind == 'legacy-duplicate':
            sequence = [document(old_add)]
        elif kind == 'positional-merge':
            merge = ET.Element('ModOp', Type='merge', GUID='151076', Path='/Values/Trigger/SubTriggers')
            merge.append(foreign_item(999))
            sequence = [document(merge)]
        output, runs = fixture_path, []
        for index, patch in enumerate(sequence):
            output, receipt = run_patch(work, kind + '-' + str(index), output, patch, work)
            runs.append(receipt)
        result = ET.parse(str(output))
        containers = result.findall('Asset/Values/Trigger/SubTriggers')
        delays = result.xpath('//SubTriggers/Item/SubTrigger/Values/Trigger/TriggerCondition/Values/ConditionTimer/TimeLimit/text()')
        expected = {'missing': ['10000'], 'empty': ['10000'], 'populated': ['777', '10000'],
                    'foreign-before': ['777', '10000'], 'foreign-after': ['10000', '777'],
                    'merge-twice': ['777'], 'repeat-add': ['10000', '10000'],
                    'positional-merge': ['999', '888'], 'legacy-duplicate': ['777', '10000'],
                    'preexisting-duplicates': ['777', '888']}[kind]
        assert delays == expected, (kind, delays)
        assert len(containers) == (2 if kind in ['legacy-duplicate', 'preexisting-duplicates'] else 1), kind
        if kind in ['merge-twice', 'preexisting-duplicates']:
            assert normalized(result.getroot()) == normalized(fixture), kind
        if kind in ['populated', 'foreign-before', 'foreign-after', 'legacy-duplicate']:
            original = foreign_item(777)
            kept = next(node for node in result.xpath('//SubTriggers/Item') if node.findtext('.//TimeLimit') == '777')
            assert normalized(kept) == normalized(original), kind
        cases.append({'case': kind, 'passed': True, 'container_count': len(containers), 'delays_ms': delays, 'runs': runs})
    receipt = {'date': '2026-10-25', 'scope': 'Offline XML composition; no game/save/MP execution',
               'tool': 'xmltest GU17.1 bundled with vscode-anno 2.3.1', 'tool_sha256': digest(EXE),
               'campaign_version': json.loads((CAMPAIGN / 'modinfo.json').read_text())['Version'],
               'cases': cases, 'full_chain': full_chain(work, args.baseline),
               'limits': ['Fixture foreign mods only append valid timer children; this does not certify gameplay semantics.',
                          'Repeated add and preexisting duplicate-container cases intentionally demonstrate unresolved limits.',
                          'Full proprietary asset outputs are disposable local files, not repository artifacts.']}
    write(args.receipt, receipt)
    print(json.dumps({'passed': len(cases), 'assets_compared': receipt['full_chain']['assets_compared'],
                      'semantic_changes': receipt['full_chain']['semantic_changes']}))


if __name__ == '__main__':
    main()
