"""Extract source contracts for Lua entry points and the inheritance example."""
from pathlib import Path
import hashlib
import json
import re
from lxml import etree as ET
from inventory import VANILLA, OUT, write_json

ASSET_DIR = VANILLA / 'data/config/export/main/asset'

def excerpt(node):
    return {'line': node.sourceline, 'xml': ET.tostring(node, encoding='unicode', pretty_print=True)}

def provenance(path):
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def main():
    selected = {}
    vector_example = False
    for _, node in ET.iterparse(str(ASSET_DIR / 'assets.xml'), events=('end',), tag='Asset', huge_tree=True):
        guid = node.findtext('Values/Standard/GUID')
        if not guid:
            continue
        scripts = node.findall('.//ScriptFileName')
        vector = (not vector_example and node.find('.//InheritedIndex') is not None
                  and len(ET.tostring(node)) < 6000)
        if guid in {'24965', '2001386', '100274'} or scripts or vector:
            selected[guid] = {**excerpt(node), 'name': node.findtext('Values/Standard/Name'),
                              'template': node.findtext('Template'), 'base': node.findtext('BaseAssetGUID'),
                              'script_files': [x.text for x in scripts], 'vector_example': vector}
            if vector:
                vector_example = True
        node.clear()
        while node.getprevious() is not None:
            del node.getparent()[0]
    # Follow the BaseAssetGUID chain for every selected asset, without modifying the source.
    missing = {x['base'] for x in selected.values() if x['base'] and x['base'] not in selected}
    while missing:
        found = set()
        for _, node in ET.iterparse(str(ASSET_DIR / 'assets.xml'), events=('end',), tag='Asset', huge_tree=True):
            guid = node.findtext('Values/Standard/GUID')
            if guid in missing:
                selected[guid] = {**excerpt(node), 'name': node.findtext('Values/Standard/Name'),
                                  'template': node.findtext('Template'), 'base': node.findtext('BaseAssetGUID')}
                found.add(guid)
            if guid:
                node.clear()
                while node.getprevious() is not None:
                    del node.getparent()[0]
        if missing - found:
            raise ValueError('Unresolved bases: ' + str(missing - found))
        missing = {x['base'] for x in selected.values() if x['base'] and x['base'] not in selected}
    templates = ET.parse(str(ASSET_DIR / 'templates.xml'), ET.XMLParser(huge_tree=True))
    wanted = {x['template'] for x in selected.values() if x['template']} | {
        'ActionExecuteScript', 'ConditionEvent', 'ConditionAlwaysTrue', 'ActionResetTrigger', 'Trigger', 'FeatureUnlock'}
    # Inline template names are part of the entry-point contract as well.
    for value in selected.values():
        wanted.update(re.findall(r'<Template>([^<]+)</Template>', value['xml']))
    chosen_templates = {n.findtext('Name'): excerpt(n) for n in templates.xpath('//Template[Name]') if n.findtext('Name') in wanted}
    props = {'Standard', 'Text', 'Skin', 'Locked', 'Trigger', 'TriggerSetup', 'ActionExecuteScript',
             'ConditionEvent', 'Condition', 'Action', 'Nameable', 'ConditionPropsNegatable'}
    for value in chosen_templates.values():
        node = ET.fromstring(value['xml'])
        props.update(n.tag for n in node.find('Properties') if isinstance(n.tag, str))
    properties = ET.parse(str(ASSET_DIR / 'properties-toolone.xml'), ET.XMLParser(huge_tree=True))
    chosen_properties = {n.findtext('Name'): excerpt(n) for n in properties.xpath('//Property[Name]') if n.findtext('Name') in props}
    wanted_datasets = {'ParticipantID', 'SimpleEventType', 'LockScope', 'PlayerCounter', 'CounterScope', 'CounterValueType'}
    for value in chosen_properties.values():
        wanted_datasets.update(re.findall(r'<DataSet>([^<]+)</DataSet>', value['xml']))
    datasets = ET.parse(str(ASSET_DIR / 'datasets.xml'), ET.XMLParser(huge_tree=True))
    defaults = ET.parse(str(ASSET_DIR / 'properties.xml'), ET.XMLParser(huge_tree=True))
    native_scripts = []
    for path in sorted(VANILLA.rglob('*.lua')):
        if path.name == 'json.lua':
            continue
        native_scripts.append({**provenance(path), 'text': path.read_text(encoding='utf-8-sig')})
    write_json(OUT / 'runtime-contracts.json', {
        'status': 'extracted; review the full excerpts before relying on a feature contract',
        'sources': [provenance(ASSET_DIR / n) for n in ('assets.xml','templates.xml','properties-toolone.xml','properties.xml','datasets.xml')],
        'assets': selected, 'templates': chosen_templates, 'properties': chosen_properties,
        'datasets': {n.findtext('Name'): excerpt(n) for n in datasets.xpath('//DataSet[Name]') if n.findtext('Name') in wanted_datasets},
        'defaults': {n.tag: excerpt(n) for n in defaults.xpath('//DefaultValues/*') if n.tag in props},
        'native_scripts': native_scripts})
    print(json.dumps({'assets': len(selected), 'templates': len(chosen_templates), 'properties': len(chosen_properties), 'native_scripts': len(native_scripts)}))

if __name__ == '__main__':
    main()
