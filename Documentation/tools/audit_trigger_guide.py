"""Audit the guide's native opening example and reused recipe contracts."""
import copy
import hashlib
import json
from workspace_paths import source_path
from pathlib import Path
from lxml import etree as ET
from inventory import write_json

DOC = Path(__file__).resolve().parents[1]
OUT = DOC/'reference/validation/trigger-guide'


def main():
    captured = json.loads((DOC/'reference/triggers/vanilla.json').read_text('utf-8'))
    for source in captured['sources']:
        assert hashlib.sha256(source_path(source['path']).read_bytes()).hexdigest() == source['sha256'], source['path']
    directory = source_path(captured['sources'][0]['path']).parent
    needed = {'130221', '130248', '15000003'}
    original = ET.fromstring((DOC/'reference/triggers/mod-cases/native-assets/130221.xml').read_bytes())
    needed.update(x.text for x in original.xpath('Values/Trigger/TriggerActions/Item/TriggerAction/Values/ActionUnlockAsset/UnlockAssets/Item/Asset | Values/Trigger/TriggerActions/Item/TriggerAction/Values/ActionUnlockAsset/UnhideAssets/Item/Asset'))
    assets, references = {}, []
    while needed:
        found = set()
        for _, node in ET.iterparse(str(directory/'assets.xml'), events=('end',), tag='Asset', huge_tree=True):
            guid = node.findtext('Values/Standard/GUID')
            if guid:
                if guid in needed:
                    assets[guid] = {'line': node.sourceline, 'template': node.findtext('Template'),
                        'base': node.findtext('BaseAssetGUID'), 'name': node.findtext('Values/Standard/Name'),
                        'xml': ET.tostring(node, encoding='unicode')}
                    found.add(guid)
                if guid != '130221':
                    for ref in node.iter():
                        if ref.text and ref.text.strip() == '130221':
                            receipt = {'owner': guid, 'owner_template': node.findtext('Template'), 'line': ref.sourceline, 'field': ref.tag}
                            if receipt not in references:
                                references.append(receipt)
                node.clear()
                while node.getprevious() is not None:
                    del node.getparent()[0]
        assert needed <= found, ('missing native asset', needed-found)
        needed = {a['base'] for a in assets.values() if a['base']} - assets.keys()
    assert ET.tostring(ET.fromstring(assets['130221']['xml'].encode())).strip() == ET.tostring(original).strip(), 'Opening example differs from current native source'
    parser = ET.XMLParser(huge_tree=True)
    templates = {n.findtext('Name'): n for n in ET.parse(str(directory/'templates.xml'), parser).xpath('//Template[Name]')}
    properties = {n.findtext('Name'): n for n in ET.parse(str(directory/'properties-toolone.xml'), parser).xpath('//Property[Name]')}
    defaults = ET.parse(str(directory/'properties.xml'), parser)
    datasets = {n.findtext('Name'): n for n in ET.parse(str(directory/'datasets.xml'), parser).xpath('//DataSet[Name]')}
    names = {'Trigger', 'AutoCreateTrigger', 'FeatureUnlock', 'UnlockableAsset', 'EmptyAutoCreateValue', 'ActionResetTrigger', 'ActionRegisterTrigger'}
    names.update(x.text for a in assets.values() for x in ET.fromstring(a['xml'].encode()).iter('Template') if x.text in templates)
    for manifest in json.loads((DOC/'reference/triggers/examples/manifest.json').read_text('utf-8')):
        names.update(x.text for x in ET.parse(manifest['path']).iter('Template'))
    props = {x.tag for name in names for x in templates[name].findall('Properties/*')}
    ds_names = {x.text for name in props for x in properties[name].iter('DataSet') if x.text}
    def xml(node):
        return ET.tostring(node, encoding='unicode') if node is not None else None
    result = {'scope': 'Opening native trigger, its counter context, all unlock/unhide targets, their full base chains, relevant template/schema/default/dataset contracts and native references to 130221. Reused recipe consumer audits remain in the linked existing records; not game-engine proof.',
        'sources': captured['sources'], 'assets': assets, 'native_references_to_130221': references,
        'templates': {name: {'line': templates[name].sourceline, 'xml': xml(templates[name])} for name in sorted(names)},
        'properties': {name: {'line': properties[name].sourceline, 'schema': xml(properties[name]),
            'default': xml(defaults.find('.//DefaultValues/'+name)), 'container_default': xml(defaults.find('.//DefaultContainerValues/'+name))} for name in sorted(props)},
        'datasets': {name: {'line': datasets[name].sourceline, 'xml': xml(datasets[name])} for name in sorted(ds_names)},
        'prior_audits': ['reference/trigger-audit.md', 'reference/triggers/mod-cases/native.json', 'reference/triggers/mod-cases/integration.json'],
        'new_game_or_mp_tests': False}
    write_json(OUT/'native-audit.json', result)
    print(json.dumps({'assets': len(assets), 'templates': len(names), 'properties': len(props), 'datasets': len(ds_names), 'references': len(references), 'source_hashes_verified': len(captured['sources'])}))


if __name__ == '__main__':
    main()
