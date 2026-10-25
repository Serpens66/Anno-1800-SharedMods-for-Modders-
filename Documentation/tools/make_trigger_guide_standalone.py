"""Inline native references into the guide; leave gameplay examples unchanged."""
import hashlib
import json
import re
from workspace_paths import source_path
from pathlib import Path
from lxml import etree as ET
from build_trigger_reference import fields, cell
from complete_trigger_guide import pretty
from inventory import write_json

DOC = Path(__file__).resolve().parents[1]
GUIDE = DOC.parent/'Trigger_Guide.md'
OUT = DOC/'reference/validation/trigger-guide'


def details(summary, content, ident=None):
    return ('<a id="'+ident+'"></a>\n' if ident else '')+'<details>\n<summary>'+summary+'</summary>\n\n'+content+'\n\n</details>'


def xml_block(source):
    return '```xml\n'+pretty(ET.fromstring(source.encode()))+'\n```'


def main():
    text = GUIDE.read_text('utf-8')
    if '<a id="native-template-overrides"></a>' in text:
        print('Standalone guide already built; preserve subsequent authored edits.')
        return
    contracts = json.loads((DOC/'reference/triggers/vanilla.json').read_text('utf-8'))
    for record in contracts['sources']:
        assert hashlib.sha256(source_path(record['path']).read_bytes()).hexdigest() == record['sha256'], record['path']
    native_dir = source_path(contracts['sources'][0]['path']).parent
    parser = ET.XMLParser(huge_tree=True)
    schemas = {n.findtext('Name'): n for n in ET.parse(str(native_dir/'properties-toolone.xml'),parser).xpath('//Property[Name]')}
    templates = {n.findtext('Name'): n for n in ET.parse(str(native_dir/'templates.xml'),parser).xpath('//Template[Name]')}
    defaults = ET.parse(str(native_dir/'properties.xml'),parser)
    datasets = {n.findtext('Name'): n for n in ET.parse(str(native_dir/'datasets.xml'),parser).xpath('//DataSet[Name]')}
    conditions = {name for name, n in templates.items() if n.find('Properties/Condition') is not None}
    assert len(conditions) == 91
    # Cover every former property destination and every native template shown in code.
    former = set(re.findall(r'Documentation/gameplay/trigger-condition-reference.md#([a-z0-9]+)',text))
    by_lower = {name.lower():name for name in schemas}
    props = {by_lower[name] for name in former}
    names = set(conditions)
    for block in re.findall(r'```xml\s*\n(.*?)\n```',text,re.S):
        root = ET.fromstring(block.strip().encode())
        names.update(n.text for n in root.iter('Template') if n.text in templates)
    names.update({'FeatureUnlock','UnlockableAsset','AutoCreateTrigger','Trigger','ActionResetTrigger','ActionRegisterTrigger'})
    props.update(n.tag for name in names for n in templates[name].findall('Properties/*'))
    # Retain useful schema-only fields discussed in the tutorial.
    props.update({'ConditionItemUsed','ConditionPropsSessionSettings','ParticipantRelation','ObjectFilter','ObjectTargetFilter'})
    assert props <= schemas.keys()
    ds_names = {n.text for name in props for n in schemas[name].iter('DataSet') if n.text}
    assert ds_names <= datasets.keys()
    for match in re.findall(r'Documentation/gameplay/trigger-datasets.md#([a-z0-9]+)',text):
        ds_names.add(next(name for name in datasets if name.lower() == match))
    def replace(old,new):
        nonlocal text
        assert text.count(old) == 1, old
        text = text.replace(old,new,1)
    replace('[Native audit receipt](Documentation/reference/validation/trigger-guide/native-audit.json).', 'The audit covered the current assets.xml, templates.xml, properties-toolone.xml, properties.xml and datasets.xml exports; [the audit procedure is explained below](#vanilla-audit).')
    replace('The original wording is preserved in the technical source reference, but is not a reason to run ship changes outside the parent\'s radius check.', 'The original wording is retained in [the Condition schema below](#property-condition), alongside its source context. It is not a reason to run ship changes outside the parent\'s radius check.')
    text = re.sub(r'\[Original source, owning Asset at line (\d+)\]\(<[^>]+>\)',r'Original owning Asset begins at source line \1',text)
    replace('Full caller/consumer, helper-version and native audit details: [six-case walkthrough](Documentation/reference/trigger-mod-walkthroughs.md).', '''### Integration details needed to read these cases

The selected PirateExtraSpawn and PirateComebackFleetFix bundles use PirateDefeatHelpers 1.041; the inspected copies were byte-identical. The checked WhichPlayer 1.091 and IsAIPlayer 1.02 bundles match their standalone counterparts. Campaign in Coop 1.021 uses StoryQuestsInCoop 1.031 and its CheckSingleHuman 1.02 bundle. An installed higher-version shared mod can change the effective dependency; those versions are the reviewed scope, not universal requirements for all future versions.

The positive Harlow-not-defeated helper maps its custom condition to unlock 1500001145. This signal checks lighthouse 100707 with RuinCount at most zero in session 180023, then self-unlocks. The paired defeated signal 1500001147 checks ruin state and each side resets/relocks through the opposite signal. Both start locked, so absence of the positive signal during initialization is not itself a confirmed defeat. Native Harlow profile 73 has ProfileCounter; pirate pool 700138 contains ship types 102429–102432.

The positive Human0 marker 1500001613 is initially locked. WhichPlayer initializer 1500001672 invokes its human-identification script and maps human ParticipantIDs 0–3 to synchronized marker unlocks. That is why waiting for the positive marker matters. It selects a company, not one Coop peer.

For the Campaign movie path, local play submits RelockNet(1500004300) and RelockNet(1500004391); skip/default submits RelockNet(1500004300) and RelockNet(1500004332). The shared availability identity is 1500004300. Play/skip both emit transition signal 1500004234. Patched native trigger 150721 listens for that edge, enters session 180023 after 1000 ms, unlocks PrologueCompleted 142310 and restores selected object visibility. The completion relock on 1500004302 is consumed by patched 150594/150836; 150594 unloads session 180014. Save migration 1500004385 unregisters and, after 1000 ms, re-registers relevant listeners. Fresh registration refreshes code; correct progress guards and listener ordering are still needed.

The movie copy derives from native Video 600170. Both named game-speed scripts in the reviewed dependency contain only comments. Availability checking does not prove an atomic resolution of two peers choosing conflicting buttons; preserve the original single-decision/host caveat.

The Harlow dispatch script's effective direct call is shown here. It needs the correct participant/session and all-client tick alignment explained earlier; it is not a new guarantee for clients in different sessions.

<details>
<summary>Harlow ForceBuild dispatch — effective Lua call</summary>

```lua
local Pirate_PID = 17 -- Harlow
ts.SessionParticipants.GetParticipant(Pirate_PID).Trader.ForceBuild()
```

</details>''')
    replace('The catalogue links to exact property reference sections and lists captured native owners for further inspection.', 'The catalogue links to property sections in this same file and lists native owners as provenance for inspection in your own vanilla assets.xml.')
    text = re.sub(r'\]\(Documentation/gameplay/trigger-condition-reference.md#([a-z0-9]+)\)',r'](#property-\1)',text)
    # Regenerate the appendix once, deduplicating formerly common and uncommon properties.
    start = text.index('### Common property layouts and serialized defaults')
    end = text.index('<a id="sources"></a>',start)
    appendix = ['### Common property layouts and serialized defaults','',
        'All property links above now lead to this file. Frequently used blocks appear first; the remaining catalogue properties follow alphabetically. Each shared property is listed once. Descriptions and defaults below are vanilla data, not proof of undocumented runtime behavior. The parent-gating clarification and other runtime qualifications in the learning chapters remain authoritative for the reviewed designs.','',
        '**Read defaults in this order:** concrete asset overrides, BaseAssetGUID inheritance where applicable, concrete template property overrides, then generic property/container defaults. An absent serialized default is not an invented zero. Consult the template section as well as the property table.','',
        '[Template overrides](#native-template-overrides) · [Property index](#native-property-index) · [Dataset index](#native-dataset-index)','']
    frequent = ['Condition','Trigger','TriggerSetup','ConditionPlayerCounter','ConditionTimer','ConditionUnlocked','ConditionUnlockList','ConditionEvent','ConditionPropsNegatable','ConditionPropsSessionSettings','ConditionActiveSession','ConditionIsDiscovered','ParticipantRelation','ConditionObjectPosition','ObjectFilter','ObjectTargetFilter','ConditionInStorage','ConditionIsBuffed','ConditionQuestState','ConditionMutualAreaInSubconditions','ConditionEvaluateTextSource','ConditionThreshold','ActionRegisterTrigger','ActionResetTrigger','ActionExecuteScript']
    order = [name for name in frequent if name in props]+sorted(props-set(frequent))
    appendix.extend(['<a id="native-property-index"></a>', '### Property index','',', '.join('['+name+'](#property-'+name.lower()+')' for name in order),''])
    def xml(node):
        return ET.tostring(node,encoding='unicode') if node is not None else None
    property_records = {}
    for name in order:
        schema = schemas[name]
        default = defaults.find('.//DefaultValues/'+name)
        container = defaults.find('.//DefaultContainerValues/'+name)
        lines = ['Source: properties-toolone.xml:'+str(schema.sourceline)+'.','',
            '| Field path | Type | Dataset | Restrictions and metadata | Native description |','| --- | --- | --- | --- | --- |']
        for path, field in fields(schema):
            ds = field.findtext('DataSet')
            link = '['+ds+'](#dataset-'+ds.lower()+')' if ds else ''
            metadata = '; '.join(n.tag+'='+cell(n.text) for n in field if n.tag not in {'Name','DataType','DataSet','Description','Items'})
            lines.append('| `'+path+'` | '+cell(field.findtext('DataType'))+' | '+link+' | '+metadata+' | '+cell(field.findtext('Description'))+' |')
        # Include exact schema shape as well: nested arrays/auto-create restrictions cannot
        # be fully reconstructed from field paths alone.
        lines.extend(['','<details>','<summary>Exact native property schema</summary>','',xml_block(xml(schema)),'','</details>','', 'Explicit property defaults:',''])
        lines.append(xml_block(xml(default)) if default is not None else 'No explicit serialized property default; check the concrete template and inherited asset.')
        lines.extend(['','Container-entry defaults:','',xml_block(xml(container)) if container is not None else 'No explicit serialized container-entry default.'])
        appendix.append(details(name+' — full structure, defaults and dataset links','\n'.join(lines),'property-'+name.lower()))
        appendix.append('')
        property_records[name] = {'schema':xml(schema),'default':xml(default),'container_default':xml(container)}
    appendix.extend(['<a id="native-template-overrides"></a>', '### Native template overrides','',
        'These are the full exported template definitions for the 91 catalogue entries and the native trigger/action templates displayed in the learning examples. Nested IsBaseAutoCreateAsset uses the inherited embedded definition. Template names with no direct Condition property belong to their own owning/action/objective role. Custom mod conditions, such as the Harlow helper, are explained in the real-case section and are not silently presented as native templates.',''])
    for name in sorted(names):
        node = templates[name]
        linked = ', '.join('['+n.tag+'](#property-'+n.tag.lower()+')' for n in node.findall('Properties/*'))
        appendix.append(details(name+' — exact template property overrides','Source: templates.xml:'+str(node.sourceline)+'. Property blocks: '+linked+'.\n\n'+xml_block(xml(node)),'template-'+name.lower()))
        appendix.append('')
    appendix.extend(['<a id="native-dataset-index"></a>','### Native dataset index','',
        'All datasets referenced by the property appendix are included below. Entry names are XML tokens; their numeric IDs and source order are distinct. A token being present does not establish that its consumer works in every runtime context.','',
        ', '.join('['+name+'](#dataset-'+name.lower()+')' for name in sorted(ds_names)),''])
    for name in sorted(ds_names):
        node = datasets[name]
        lines = ['Source: datasets.xml:'+str(node.sourceline)+'. Dataset Id='+node.findtext('Id','')+'.','',
            '| Token | Id | Native description |','| --- | --- | --- |']
        for item in node.findall('Items/Item'):
            lines.append('| `'+item.findtext('Name','')+'` | '+item.findtext('Id','')+' | '+cell(item.findtext('Description'))+' |')
        # Preserve non-description metadata and complete dataset layout too.
        lines.extend(['','<details>','<summary>Exact native dataset definition</summary>','',xml_block(xml(node)),'','</details>'])
        appendix.append(details(name+' — all tokens, IDs and native metadata','\n'.join(lines),'dataset-'+name.lower()))
        appendix.append('')
    text = text[:start]+'\n'.join(appendix)+'\n'+text[end:]
    start = text.index('## 18. Sources, uncertainty and validation')
    end = text.index('### What remains uncertain',start)
    source_intro = '''## 18. Sources, uncertainty and validation

This guide combines local vanilla exports, Serp's original notes and mod comments, the six source integrations described above, and direct author clarifications on 2026-10-03. Everything needed to read the guide is included here; the original mods are examples with their own runtime dependencies, not standalone installable recipes. Original mod code and helpful comments were not changed.

### Evidence and provenance

Optional public sources for the original examples and shared helpers: [Serpens66 / Anno-1800-Mods](https://github.com/Serpens66/Anno-1800-Mods) and [Serpens66 / Anno-1800-SharedMods-for-Modders-](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-). You do not need to open either repository to follow this guide; their current contents can differ from the reviewed versions stated here.

Vanilla templates establish property membership and embedded defaults. Property definitions establish field types, nested shape, allowed references and datasets. Concrete assets establish real identities, overrides and base chains. They do not expose every engine algorithm. Author observations and clarifications are identified separately, with probable or unresolved claims kept qualified.

The opening example is native asset 130221. Its population context 15000003, every unlock/unhide target, their base chains and trigger contracts were checked against the current exports. The later native catalogue preserves source lines and sample owner GUIDs; those lines are specific to the captured revision. The six mod examples describe their helper versions and callers/consumers in section 15.

<a id="vanilla-audit"></a>
### How to audit a new trigger feature

1. In assets.xml, find an actual asset using the desired condition/action. Read the whole owning tree, not just a matching property name.
2. In templates.xml, resolve its owning and embedded templates. Record their property membership and overrides, including IsBaseAutoCreateAsset.
3. In properties-toolone.xml, inspect every relevant field's type, nested Items, allowed template/property/asset targets, datasets and descriptions. Schema text is intent, not runtime proof.
4. In properties.xml, inspect property and container defaults. Apply concrete asset/base overrides and concrete template overrides before drawing conclusions from generic defaults.
5. In datasets.xml, verify serialized token spelling and IDs. Do not invent a similar-sounding event or comparison token.
6. Follow BaseAssetGUID chains, counter context GUIDs, pool members, participant/session identities and action resources. Check the actual downstream consumers or caller that registers the trigger.
7. If names or UI expressions matter, verify export.xml and the relevant texts files rather than guessing from a GUID. For scripts/helpers, verify the loaded package version, script contents, initialization and command synchronization category.
8. Separate structural evidence, tested observations and inference. Keep any unknown runtime boundary visible and do not silently substitute an assumption.

The 91-condition appendix is a structural reference. It does not complete the gameplay audit for every achievement, quest, spawning, graphics or object system represented by its native examples. Repeat the relevant audit when a new design uses another consumer or a changed source revision.

### Captured vanilla revisions

These hashes identify the exports used for the source checks; they are provenance, not a claim about all installed game builds.

| Vanilla file | SHA-256 |
| --- | --- |
'''
    for source in contracts['sources']:
        source_intro += '| '+source_path(source['path']).name+' | `'+source['sha256']+'` |\n'
    text = text[:start]+source_intro+'\n'+text[end:]
    # No external link survives, including mod source file links.
    assert 'Documentation/' not in text and 'Documentation\\' not in text
    permitted = {'https://github.com/Serpens66/Anno-1800-Mods', 'https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-'}
    public_code_receipt = OUT/'public-code-links.json'
    if public_code_receipt.exists():
        permitted |= {row[key] for row in json.loads(public_code_receipt.read_text('utf-8'))['records'] for key in ['url', 'guid_url']}
    for target in re.findall(r'\]\((<[^>]+>|[^)]+)\)',text):
        assert target.startswith('#') or target in permitted, target
    GUIDE.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
    write_json(OUT/'standalone-reference.json', {'source_hashes':contracts['sources'], 'condition_templates':sorted(conditions),
        'templates':{name:xml(templates[name]) for name in sorted(names)}, 'properties':property_records,
        'datasets':{name:xml(datasets[name]) for name in sorted(ds_names)}, 'external_reader_files_required':False,
        'limits':'Reference coverage for this guide; no new game/MP or full gameplay-consumer audit.'})
    print(json.dumps({'condition_templates':len(conditions),'template_definitions':len(names),'properties':len(props),'datasets':len(ds_names),'lines':len(text.splitlines()),'external_links':0}))


if __name__ == '__main__':
    main()
