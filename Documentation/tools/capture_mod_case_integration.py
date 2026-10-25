"""Record selected package/include/helper integration and source preservation hashes."""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import re
import sys
from lxml import etree as ET
from inventory import ROOT, decode, write_json
from audit_triggers import stamp, write, xml
from inspect_mod_trigger_cases import OUT, CASES

PACKAGES = [
 'Anno-1800-Mods/Recommended-Mods/BT Passive Trading (Serp)',
 'SharedMods/shared_PirateExtraSpawn',
 'Anno-1800-Mods/YouKnowWhatYouDo-Mods/P PirateComebackFleetFix (Serp)',
 'Anno-1800-Mods/YouKnowWhatYouDo-Mods/Campaign in Coop (Serp)',
 'Anno-1800-Mods/YouKnowWhatYouDo-Mods/Story Quests in Coop (Serp)',
 'SharedMods/shared_PirateDefeatHelpers',
 'SharedMods/shared_WhichPlayer_Condition',
]
REFERENCES = set(CASES) | {'1500000041', '1500003001', '1500003005', '1500003009', '1500003070', '1500003071', '1500003072',
             '1500001145', '1500001147', '1500001613', '1500004202', '1500004234', '1500004391', '1500004300', '1500004385'}

def main():
    sources, metadata, includes, definitions, references = {}, [], [], [], []
    groups = defaultdict(list)
    for package in PACKAGES:
        root = ROOT/package
        for path in sorted(root.rglob('*')):
            if not path.is_file() or path.suffix.lower() not in {'.xml', '.lua', '.json', '.txt'}:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel in sources:
                continue
            raw = path.read_bytes()
            text, enc = decode(raw)
            sources[rel] = {**stamp(path), 'encoding': enc}
            if path.name == 'modinfo.json':
                meta = json.loads(text)
                item = {'path': rel, **{k: meta.get(k) for k in ['ModID', 'Version', 'ModDependencies', 'LoadAfterIds', 'IncompatibleIds']}}
                files = sorted(p for p in path.parent.rglob('*') if p.is_file() and not any(s in {'.git', '.vscode'} for s in p.parts))
                bundle_hash = hashlib.sha256()
                for p in files:
                    bundle_hash.update(p.relative_to(path.parent).as_posix().encode('utf-8')+b'\0'+p.read_bytes())
                item['complete_package_hash'] = bundle_hash.hexdigest()
                groups[(meta.get('ModID'), meta.get('Version'), item['complete_package_hash'])].append(rel)
                metadata.append(item)
            if path.suffix.lower() == '.xml':
                tree = ET.fromstring(text.encode('utf-8'), ET.XMLParser(huge_tree=True))
                for inc in tree.iter('Include'):
                    name = inc.get('File')
                    # The nearest metadata owner is the virtual package root.
                    owner = path.parent
                    while not (owner/'modinfo.json').exists() and owner != ROOT:
                        owner = owner.parent
                    target = owner/name.lstrip('/') if name.startswith('/') else path.parent/name
                    includes.append({'source': rel, 'line': inc.sourceline, 'file': name, 'resolved': str(target.resolve()), 'exists': target.exists()})
                for asset in tree.iter('Asset'):
                    guid = asset.findtext('Values/Standard/GUID')
                    if guid in REFERENCES:
                        definitions.append({'guid': guid, 'source': rel, 'line': asset.sourceline, 'base': asset.findtext('BaseAssetGUID'), 'template': asset.findtext('Template'), 'xml': xml(asset)})
                for node in tree.iter():
                    if isinstance(node.tag, str) and node.text and node.text.strip() in REFERENCES:
                        references.append({'guid': node.text.strip(), 'source': rel, 'line': node.sourceline, 'element': node.tag, 'xml_path': tree.getroottree().getpath(node)})
    write_json(OUT/'integration.json', {'scope': 'Workspace package/include/resource inspection; not installed active-mod selection or dependency-loader execution.',
                                      'sources': sources, 'metadata': metadata, 'includes': includes, 'definitions': definitions,
                                      'references': references, 'byte_identical_package_groups': [{'mod_id': k[0], 'version': k[1], 'sha256': k[2], 'copies': v} for k,v in groups.items()]})
    print(json.dumps({'source_files': len(sources), 'metadata': [{k:v for k,v in m.items() if k != 'complete_package_hash'} for m in metadata],
                      'missing_includes': [x for x in includes if not x['exists']], 'definitions': len(definitions),
                      'package_groups': [{ 'mod_id': k[0], 'version': k[1], 'copies': len(v)} for k,v in groups.items()]}, indent=2))

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
