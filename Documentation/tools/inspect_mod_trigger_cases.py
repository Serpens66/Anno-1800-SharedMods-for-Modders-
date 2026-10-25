"""Capture six existing mod trigger definitions for scoped documentation review."""
from workspace_paths import source_path
from pathlib import Path
import hashlib
import json
import sys
from lxml import etree as ET
from inventory import DOC, ROOT, VANILLA, decode, write_json
from audit_triggers import write, xml

OUT = DOC/'reference/triggers/mod-cases'
CASES = {
 '1500003013': 'Anno-1800-Mods/Recommended-Mods/BT Passive Trading (Serp)/data/config/export/main/asset/MoreTradeForHumansArchi.include.xml',
 '1500003820': 'SharedMods/shared_PirateExtraSpawn/data/config/export/main/asset/SpawnShipsIfWeak.include.xml',
 '1500003835': 'SharedMods/shared_PirateExtraSpawn/data/config/export/main/asset/SpawnShipsIfWeak.include.xml',
 '1500001103': 'Anno-1800-Mods/YouKnowWhatYouDo-Mods/P PirateComebackFleetFix (Serp)/data/config/export/main/asset/ComebackFleet.include.xml',
 '1500004302': 'Anno-1800-Mods/YouKnowWhatYouDo-Mods/Campaign in Coop (Serp)/data/config/export/main/asset/AntiDesync/MovieUnlocks.include.xml',
 '1500004332': 'Anno-1800-Mods/YouKnowWhatYouDo-Mods/Campaign in Coop (Serp)/data/config/export/main/asset/AntiDesync/MovieUnlocks.include.xml',
}

def main():
    result = {}
    for guid, rel in CASES.items():
        path = source_path(ROOT/rel)
        raw = path.read_bytes()
        text, encoding = decode(raw)
        tree = ET.fromstring(text.encode('utf-8'), ET.XMLParser(huge_tree=True))
        nodes = tree.xpath(".//Asset[Values/Standard/GUID='"+guid+"']")
        assert len(nodes) == 1, guid
        node = nodes[0]
        preceding = node.getprevious()
        comments = []
        while preceding is not None and isinstance(preceding, ET._Comment):
            comments.insert(0, {'line': preceding.sourceline, 'text': preceding.text})
            preceding = preceding.getprevious()
        payload = xml(node)
        write(OUT/(guid+'.xml'), payload)
        op = node.getparent()
        result[guid] = {'source': rel, 'sha256': hashlib.sha256(raw).hexdigest(), 'encoding': encoding,
                        'line': node.sourceline, 'name': node.findtext('Values/Standard/Name'),
                        'modop': dict(op.attrib), 'comments': comments,
                        'templates': sorted(set(n.text for n in node.iter('Template') if n.text)),
                        'properties': sorted(set(c.tag for v in node.iter('Values') for c in v if isinstance(c.tag, str))),
                        'numeric_references_to_inspect': sorted(set(n.text for n in node.iter() if n.text and n.text.strip().isdigit() and len(n.text.strip()) >= 5))}
    write_json(OUT/'cases.json', result)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
