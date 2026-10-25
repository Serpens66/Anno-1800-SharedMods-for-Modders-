"""Capture feature-scoped native contracts and owning asset/base chains for six cases."""
from pathlib import Path
import json
import sys
from lxml import etree as ET
from inventory import VANILLA, write_json
from audit_triggers import xml, stamp, write
from inspect_mod_trigger_cases import OUT

ASSET = VANILLA/'data/config/export/main/asset'
SEEDS = {'130221', '130248', '141003', '193897', '100681', '100707', '700138',
         '153262', '153266', '150721', '150810', '8452', '600170', '180023', '142310', '150594', '150836',
         '100438', '45', '73', '2001386', '116915', '137108'}

def main():
    cases = json.loads((OUT/'cases.json').read_text('utf-8'))
    parser = ET.XMLParser(huge_tree=True)
    templates = {n.findtext('Name'): n for n in ET.parse(str(ASSET/'templates.xml'), parser).xpath('//Template[Name]')}
    schema = {n.findtext('Name'): n for n in ET.parse(str(ASSET/'properties-toolone.xml'), parser).xpath('//Property[Name]')}
    d = ET.parse(str(ASSET/'properties.xml'), parser)
    defaults = {n.tag: n for n in d.xpath('//DefaultValues/*')}
    containers = {n.tag: n for n in d.xpath('//DefaultContainerValues/*')}
    datasets = {n.findtext('Name'): n for n in ET.parse(str(ASSET/'datasets.xml'), parser).xpath('//DataSet[Name]')}
    assets, needed = {}, set(SEEDS)
    while needed:
        found = set()
        for _, n in ET.iterparse(str(ASSET/'assets.xml'), events=('end',), tag='Asset', huge_tree=True):
            guid = n.findtext('Values/Standard/GUID')
            if guid in needed:
                assets[guid] = {'line': n.sourceline, 'template': n.findtext('Template'),
                                'base': n.findtext('BaseAssetGUID'), 'name': n.findtext('Values/Standard/Name'), 'xml': xml(n)}
                found.add(guid)
            if guid:
                n.clear()
                while n.getprevious() is not None:
                    del n.getparent()[0]
        assert needed <= found, 'Native seed/base missing: '+str(needed-found)
        needed = {n['base'] for n in assets.values() if n['base']} - assets.keys()
        # Resolve the actual pool members; a pool name alone cannot establish its targets.
        for asset in assets.values():
            n = ET.fromstring(asset['xml'].encode('utf-8'))
            members = n.xpath('Values/ItemEffectTargetPool/EffectTargetGUIDs/Item/GUID | Values/PlayerCounterContextPool/Contexts/Item/Asset | Values/AssetPool/Assets/Item/Asset')
            needed.update(x.text for x in members if x.text and x.text != '0' and x.text not in assets)
    names = {t for c in cases.values() for t in c['templates'] if t in templates}
    names.update({'Actions', 'EmptyAutoCreateValue', 'ActionEnterSession', 'ActionUnlockAsset',
                  'ActionSetObjectVisibility', 'ActionNotification'})
    props = {p for c in cases.values() for p in c['properties']}
    props.update({'SessionFilter', 'Quest', 'PreConditionList', 'Movie', 'ProfileCounter', 'ConditionPropsNegatable'})
    for a in assets.values():
        n = ET.fromstring(a['xml'].encode('utf-8'))
        names.update(t.text for t in n.iter('Template') if t.text in templates)
        props.update(p.tag for v in n.iter('Values') for p in v if isinstance(p.tag, str))
    for name in names:
        if name in templates:
            props.update(n.tag for n in templates[name].findall('Properties/*'))
    used_ds = {n.text for p in props if p in schema for n in schema[p].iter('DataSet') if n.text}
    record = {'scope': 'Six selected mod cases; source/schema/default/example/base evidence, not native engine-algorithm proof.',
              'sources': [stamp(ASSET/n) for n in ['templates.xml','properties-toolone.xml','properties.xml','datasets.xml','assets.xml']],
              'templates': {name: {'line': templates[name].sourceline, 'xml': xml(templates[name])} for name in sorted(names) if name in templates},
              'properties': {name: {'line': schema[name].sourceline, 'schema': xml(schema[name]),
                                   'default': xml(defaults[name]) if name in defaults else None,
                                   'container_default': xml(containers[name]) if name in containers else None} for name in sorted(props) if name in schema},
              'datasets': {name: {'line': datasets[name].sourceline, 'xml': xml(datasets[name])} for name in sorted(used_ds) if name in datasets},
              'assets': assets}
    write_json(OUT/'native.json', record)
    for guid, asset in assets.items():
        write(OUT/'native-assets'/(guid+'.xml'), asset['xml'])
    print(json.dumps({'templates': len(record['templates']), 'properties': len(record['properties']),
                      'datasets': len(record['datasets']), 'assets': {g: {'line': a['line'], 'template': a['template'], 'base': a['base'], 'name': a['name']} for g,a in assets.items()}}, indent=2))

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
