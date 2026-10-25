"""Expand authored guide markers with audited XML and native condition lookups."""
import copy
import hashlib
import json
import re
from workspace_paths import ROOT, source_path
from pathlib import Path
from lxml import etree as ET
from build_trigger_reference import fields, cell
from build_trigger_examples import condition, trigger, unlock, actions
from inventory import write_json

DOC = Path(__file__).resolve().parents[1]
GUIDE = DOC.parent/'Trigger_Guide.md'
OUT = DOC/'reference/validation/trigger-guide'


def pretty(node):
    n = copy.deepcopy(node)
    for x in n.iter():
        if x.text and not x.text.strip():
            x.text = None
        x.tail = None
    ET.indent(n, space='  ')
    return ET.tostring(n, encoding='unicode').strip()


def code(summary, text):
    return '<details>\n<summary>'+summary+'</summary>\n\n```xml\n'+text.strip()+'\n```\n\n</details>'


def main():
    original = GUIDE.read_text('utf-8')
    if '{{NATIVE_EXAMPLE}}' not in original:
        print('Guide already expanded; edit authored prose directly, do not overwrite it.')
        return
    contracts = json.loads((DOC/'reference/triggers/vanilla.json').read_text('utf-8'))
    audit = json.loads((OUT/'native-audit.json').read_text('utf-8'))
    manifest = json.loads((DOC/'reference/triggers/examples/manifest.json').read_text('utf-8'))
    cases = json.loads((DOC/'reference/triggers/mod-cases/cases.json').read_text('utf-8'))
    replacements, records = {}, []
    native = ET.fromstring(audit['assets']['130221']['xml'].encode())
    replacements['NATIVE_EXAMPLE'] = code('Original vanilla asset 130221 — complete Asset, not a ModOps file', pretty(native))
    custom = ET.parse(str(DOC/'reference/triggers/examples/once.xml')).getroot()
    c = custom.find('.//TriggerCondition')
    c.clear()
    c.append(ET.Element('Template'))
    c[0].text = 'ConditionPlayerCounter'
    values = ET.SubElement(c, 'Values')
    ET.SubElement(values, 'Condition')
    props = ET.SubElement(values, 'ConditionPlayerCounter')
    for name, value in [('PlayerCounter','PopulationByLevel'),('Context','15000003'),('ComparisonOp','AtLeast'),('CounterAmount','1'),('CounterScope','Global'),('CounterValueType','Current')]:
        ET.SubElement(props, name).text = value
    custom_text = pretty(custom)
    replacements['CUSTOM_EXAMPLE'] = code('First custom population trigger — complete ModOps; replace GUID tokens', custom_text)
    records.append({'id': 'custom-population', 'kind': 'complete-modops', 'sha256': hashlib.sha256(custom_text.encode()).hexdigest(), 'source': 'Native 130221 counter and audited once recipe', 'tokens': sorted(set(re.findall(r'\b[A-Z_]+_GUID\b', custom_text)))})
    replacements['NEGATE_FRAGMENT'] = code('Negated unlocked condition — fragment for Trigger/TriggerCondition', pretty(condition('ConditionUnlocked', {'UnlockNeeded':'PRESENCE_GUID'}, negate=True)))
    replacements['MODE_FRAGMENT'] = code('Parent A with Parallel children B and C — embedded Trigger fragment', pretty(trigger(condition('ConditionUnlocked', {'UnlockNeeded':'GATE_A_GUID'}, mode='Parallel'), 'RESULT_GUID', children=[trigger(unlock('GATE_B_GUID')), trigger(unlock('GATE_C_GUID'))])))
    replacements['OPTIONAL_FRAGMENT'] = code('Optional child and its action — fragment for SubTriggers/Item/SubTrigger', '<SubTrigger>\n  <Template>AutoCreateTrigger</Template>\n  <Values>\n'+pretty(trigger(unlock('GATE_A_GUID', optional=True), 'OPTIONAL_RESULT_GUID'))+'\n  </Values>\n</SubTrigger>')
    register = ET.fromstring(b'<TriggerAction><Template>ActionRegisterTrigger</Template><Values><Action/><ActionRegisterTrigger><TriggerAsset>TARGET_TRIGGER_GUID</TriggerAsset></ActionRegisterTrigger></Values></TriggerAction>')
    replacements['REGISTER_FRAGMENT'] = code('Manual registration action — fragment for TriggerActions/Item', pretty(register))
    lua = ET.fromstring(b'<TriggerAction><Template>ActionExecuteScript</Template><Values><Action/><ActionExecuteScript><ScriptFileName>data/scripts/my_trigger.lua</ScriptFileName></ActionExecuteScript></Values></TriggerAction>')
    replacements['LUA_FRAGMENT'] = code('Script action — fragment; supply this example script path in your mod', pretty(lua))
    for example in manifest:
        text = source_path(example['path']).read_text('utf-8').strip()
        ident = example['case']
        replacements['RECIPE_'+ident.upper().replace('-', '_')] = code(example_title(ident)+' — complete ModOps; replace GUID tokens', text)
        records.append({'id': ident, 'kind': 'complete-modops', 'sha256': hashlib.sha256(text.encode()).hexdigest(), 'source': str(source_path(example['path']).relative_to(ROOT)), 'tokens': example['tokens'], 'external': example['external']})
    for marker, guids in [('SOURCE_BT',['1500003013']), ('SOURCE_PIRATES',['1500003820','1500003835']), ('SOURCE_COMEBACK',['1500001103']), ('SOURCE_CAMPAIGN',['1500004302','1500004332'])]:
        parts = []
        for guid in guids:
            case = cases[guid]
            source = source_path(ROOT/case['source'])
            assert hashlib.sha256(source.read_bytes()).hexdigest() == case['sha256'], case['source']
            asset = ET.parse(str(DOC/'reference/triggers/mod-cases'/(guid+'.xml')), ET.XMLParser(remove_comments=True)).getroot()
            asset.find('Values/Standard/Name').text = 'Reviewed trigger '+guid
            parts.append('[Original source, owning Asset at line '+str(case['line'])+'](<'+case['source']+'>). The presentation below removes original comments and uses an English display Name; gameplay fields are retained. It depends on the original mod integration and is not a standalone recipe.\n\n'+code('Reviewed trigger '+guid+' — complete owning Asset', pretty(asset)))
        replacements[marker] = '\n\n'.join(parts)
    ref = (DOC/'gameplay/trigger-condition-reference.md').read_text('utf-8')
    section = ref.split('## Native Condition templates',1)[1] if '## Native Condition templates' in ref else ref
    rows = [line for line in section.splitlines() if line.startswith('| `Condition')]
    rows = rows[:91]
    assert len(rows) == 91 and len({re.search(r'`(Condition\w+)`', row)[1] for row in rows}) == 91
    # Preserve the source catalogue's audited purposes; suppress native display Names.
    catalogue = ['| Template and candidate purpose | Property contracts | Captured native owners |','| --- | --- | --- |']
    for row in rows:
        row = re.sub(r'\]\(#([^)]+)\)', r'](Documentation/gameplay/trigger-condition-reference.md#\1)', row)
        row = re.sub(r'(\d+) \(assets.xml:(\d+); [^)]*\)', r'GUID \1 (assets.xml:\2)', row)
        catalogue.append(row)
    replacements['CATALOGUE'] = '\n'.join(catalogue)
    common = ['Condition','TriggerSetup','ConditionPlayerCounter','ConditionTimer','ConditionUnlocked','ConditionUnlockList','ConditionEvent','ConditionPropsNegatable','ConditionPropsSessionSettings','ConditionActiveSession','ConditionIsDiscovered','ParticipantRelation','ConditionObjectPosition','ObjectFilter','ObjectTargetFilter','ConditionInStorage','ConditionIsBuffed','ConditionQuestState','ConditionMutualAreaInSubconditions','ConditionEvaluateTextSource','ConditionThreshold','ActionRegisterTrigger','ActionResetTrigger','ActionExecuteScript']
    blocks = []
    for name in common:
        record = contracts['properties'][name]
        schema = ET.fromstring(record['xml'].encode())
        lines = ['<details>', '<summary>'+name+' — fields, dataset references and defaults</summary>', '',
                 'Source: properties-toolone.xml:'+str(record['line'])+'.', '',
                 '| Field path | Type | Dataset | Schema description |', '| --- | --- | --- |']
        for path, field in fields(schema):
            ds = field.findtext('DataSet')
            ds_link = '['+ds+'](Documentation/gameplay/trigger-datasets.md#'+ds.lower()+')' if ds else ''
            lines.append('| `'+path+'` | '+cell(field.findtext('DataType'))+' | '+ds_link+' | '+cell(field.findtext('Description'))+' |')
        lines.extend(['', 'Explicit property defaults:', ''])
        if record['defaults_xml']:
            lines.extend(['```xml', pretty(ET.fromstring(record['defaults_xml'].encode())), '```'])
        else:
            lines.append('Not explicitly captured; consult the effective template and source contract.')
        if record['container_defaults_xml']:
            lines.extend(['', 'Container-entry defaults:', '', '```xml', pretty(ET.fromstring(record['container_defaults_xml'].encode())), '```'])
        lines.extend(['', '</details>'])
        blocks.append('\n'.join(lines))
    # Frequently needed dataset tokens stay in this file, including the complete counter list.
    for name in ['SubConditionCompletionOrder','CounterScope','CounterValueType','ComparisonOp','PlayerCounter','SimpleEventType','UnlockRangeOP']:
        if name not in contracts['datasets']:
            continue
        ds = ET.fromstring(contracts['datasets'][name]['xml'].encode())
        tokens = [x.findtext('Name') for x in ds.findall('Items/Item')]
        blocks.append('<details>\n<summary>'+name+' — native dataset tokens</summary>\n\n'+', '.join('`'+x+'`' for x in tokens)+'\n\nThese are serialization tokens; support depends on the consumer.\n\n</details>')
    replacements['COMMON_FIELDS'] = '\n\n'.join(blocks)
    for key, content in replacements.items():
        marker = '{{'+key+'}}'
        assert original.count(marker) == 1, key
        original = original.replace(marker, content, 1)
    assert '{{' not in original
    GUIDE.write_bytes(original.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
    write_json(OUT/'examples.json', records)
    print(json.dumps({'complete_examples': len(records), 'catalogue_templates':len(rows), 'common_property_blocks':len(common), 'guide_lines':len(original.splitlines())}))


def example_title(ident):
    return {'once':'Single execution', 'repeat':'Repeating timer and reset', 'simultaneous':'Three nested live-state gates', 'sequence':'Ordered event chain', 'priority':'Prioritized alternatives', 'optional':'Optional side action', 'removal-safe':'Mod presence guard', 'human-session':'Human0 and session guards'}[ident]


if __name__ == '__main__':
    main()
