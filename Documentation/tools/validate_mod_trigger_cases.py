"""Check the six source definitions and their scoped real caller/consumer patches."""
from workspace_paths import source_path
import copy
import hashlib
import json
import subprocess
import sys
from lxml import etree as ET
from inventory import DOC, ROOT, write_json, decode
from audit_triggers import write, xml
from inspect_mod_trigger_cases import OUT, CASES
from validate_triggers import canonical, validate_asset_structure, validate_definition
from validate_loader import EXE

VALIDATION = DOC/'reference/validation/mod-trigger-cases'

def tree(path):
    text, _ = decode(path.read_bytes())
    return ET.fromstring(text.encode('utf-8'), ET.XMLParser(huge_tree=True, remove_comments=True))

def main():
    native = json.loads((OUT/'native.json').read_text('utf-8'))
    integration = json.loads((OUT/'integration.json').read_text('utf-8'))
    for source in native['sources']+list(integration['sources'].values()):
        assert hashlib.sha256(open(source_path(source['path']), 'rb').read()).hexdigest() == source['sha256'], source['path']
    contracts = {'templates': native['templates'], 'properties': {n:{'xml':p['schema']} for n,p in native['properties'].items()}, 'datasets': native['datasets']}
    custom = ROOT/'SharedMods/shared_PirateExtraSpawn/shared_PirateDefeatHelpers/data/config/export/main/asset/templates.xml'
    n = tree(custom).xpath(".//Template[Name='Harlow_Currently_NOT_Defeated']")[0]
    contracts['templates'][n.findtext('Name')] = {'xml': xml(n)}
    datasets = {k:ET.fromstring(v['xml'].encode('utf-8')) for k,v in native['datasets'].items()}
    schemas = {k:ET.fromstring(v['schema'].encode('utf-8')) for k,v in native['properties'].items()}
    reports = []
    for guid in CASES:
        n = tree(OUT/(guid+'.xml'))
        validate_asset_structure(n, contracts)
        # Check Values inside IsBaseAutoCreateAsset definitions as well, not just explicit Template nodes.
        for values in n.iter('Values'):
            for prop in values:
                if isinstance(prop.tag, str):
                    assert prop.tag in schemas, prop.tag
                    validate_definition(prop, schemas[prop.tag], datasets)
        reports.append({'guid':guid, 'source_structure_passed':True})
    original = ET.Element('Assets')
    for a in native['assets'].values():
        original.append(ET.fromstring(a['xml'].encode('utf-8')))
    original_path = VALIDATION/'original.xml'
    write(original_path, xml(original))
    patches = []
    for guid, rel in CASES.items():
        source = tree(source_path(ROOT/rel))
        asset = source.xpath(".//Asset[Values/Standard/GUID='"+guid+"']")[0]
        op = ET.Element('ModOp', **dict(asset.getparent().attrib))
        op.append(copy.deepcopy(asset))
        patches.append(op)
    # Original sources and exact paths of the relevant additional mutations, in include order.
    bt = ROOT/'Anno-1800-Mods/Recommended-Mods/BT Passive Trading (Serp)/data/config/export/main/asset/assets.xml'
    cq = ROOT/'Anno-1800-Mods/YouKnowWhatYouDo-Mods/P PirateComebackFleetFix (Serp)/data/config/export/main/asset/ComebackFleet.include.xml'
    campaign = ROOT/'Anno-1800-Mods/YouKnowWhatYouDo-Mods/Campaign in Coop (Serp)/data/config/export/main/asset/AntiDesync'
    # Assets defining the selected ship/buff/signal identities are preserved exactly.
    wanted = {'1500000041','1500003001','1500003005','1500003009','1500003070','1500003071','1500003072',
              '1500004202','1500004234','1500004391'}
    for path in [bt, campaign/'MovieCopies.include.xml', campaign/'UnlockableAssets.include.xml', campaign/'MovieUnlocks.include.xml']:
        for a in tree(path).iter('Asset'):
            if a.findtext('Values/Standard/GUID') in wanted:
                op = ET.Element('ModOp', **dict(a.getparent().attrib))
                op.append(copy.deepcopy(a)); patches.append(op)
    relevant_ops = []
    for op in tree(cq).findall('ModOp'):
        if op.get('GUID') == '153262':
            relevant_ops.append(copy.deepcopy(op))
    for path in [campaign/'ADMovies.include.xml', campaign/'ADNotifications.include.xml']:
        for op in tree(path).findall('ModOp'):
            if op.get('GUID') in {'150721','150594,150836'}:
                relevant_ops.append(copy.deepcopy(op))
    patches += relevant_ops
    patch = ET.Element('ModOps')
    patch.extend(patches)
    mod = VALIDATION/'fixture'
    path = mod/'data/config/export/main/asset/assets.xml'
    write(path, xml(patch))
    output = VALIDATION/'patched.xml'
    args = [str(EXE),'-c','patch','-m',str(mod),'-o',str(output),str(original_path),str(path)]
    run = subprocess.run(args, capture_output=True, encoding='utf-8', errors='replace')
    log = run.stdout+run.stderr
    write(VALIDATION/'xmltest.log', log)
    assert run.returncode == 0 and '[error]' not in log, log
    result = ET.parse(str(output))
    for report in reports:
        matches = result.xpath("//Asset[Values/Standard/GUID='"+report['guid']+"']")
        assert len(matches)==1 and canonical(matches[0])==canonical(tree(OUT/(report['guid']+'.xml'))), report['guid']
        report['exact_payload_preserved'] = True
    for guid in ['130221','130248']:
        matches = result.xpath("//Asset[Values/Standard/GUID='"+guid+"']")
        assert len(matches)==1 and canonical(matches[0])==canonical(ET.fromstring(native['assets'][guid]['xml'].encode('utf-8')))
    quest = result.xpath("//Asset[Values/Standard/GUID='153262']")[0]
    assert quest.findtext('Values/Quest/OnQuestEnd/Values/ActionList/Actions/Item/Action/Values/ActionRegisterTrigger/UnregisterTrigger') == '1'
    assert quest.xpath("Values/Quest/OnQuestEnd//ActionDelayedActions[ExecutionDelay='1000']//TriggerAsset[text()='1500001103']")
    movie_consumer = result.xpath("//Asset[Values/Standard/GUID='150721']")[0]
    assert movie_consumer.findtext('Values/Trigger/TriggerCondition/Values/ConditionEvent/ConditionEvent') == 'GUIDLocked'
    assert movie_consumer.findtext('Values/Trigger/TriggerCondition/Values/ConditionEvent/ContextAsset') == '1500004234'
    assert movie_consumer.xpath("Values/Trigger/TriggerActions//ActionDelayedActions[ExecutionDelay='1000']//TargetSession[text()='180023']")
    banner = result.xpath("//Asset[Values/Standard/GUID='150594']")[0]
    assert banner.findtext('Values/Trigger/TriggerCondition/Values/ConditionEvent/ContextAsset')=='1500004302'
    assert banner.xpath('Values/Trigger/TriggerActions//ActionUnloadSession')
    # File presence and provider semantics are checked separately from game API execution.
    script = ROOT/'Anno-1800-Mods/YouKnowWhatYouDo-Mods/Campaign in Coop (Serp)/Story Quests in Coop (Serp)/data'
    for name in ['gamespeed_slow_serp.lua','gamespeed_normal_serp.lua']:
        text, _ = decode((script/name).read_bytes())
        assert all(not line.strip() or line.lstrip().startswith('--') for line in text.splitlines())
    report = {'date':'2026-10-03', 'cases':reports, 'source_hashes_verified':len(native['sources'])+len(integration['sources']),
              'evaluator_sha256':hashlib.sha256(EXE.read_bytes()).hexdigest(), 'command':args,
              'caller_consumer_assertions':['Quest OnQuestEnd preserves native unregister and adds delayed 1500001103 registration',
                                            '150721 listens to 1500004234 and enters session after 1000 ms',
                                            '150594 listens to 1500004302 and retains ActionUnloadSession',
                                            'both insertion anchors unchanged', 'Story dependency provides comment-only game-speed scripts'],
              'limits':'Scoped real-source fixture only; no complete mod/dependency load, inheritance serialization, timing, saved-state, Lua C-function or MP execution. Three questions remain unanswered.'}
    write_json(VALIDATION/'results.json', report)
    print('PASS: six real definitions, exact inserted payloads, two native anchors and quest/movie caller-consumer patches. Runtime questions remain open.')

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
