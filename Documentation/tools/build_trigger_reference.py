"""Render structural lookups from the extracted native contracts; no runtime certification."""
import json
import re
from pathlib import Path
from lxml import etree as ET
from audit_triggers import DEST, write

DOC = Path(__file__).resolve().parents[1]

# Candidate intent follows native names/fields; this is not runtime certification.
PURPOSES = {
    'ActiveRegion': 'Presence in a session of a chosen region', 'ActiveSession': 'Active-session presence / blacklist',
    'AlwaysFalse': 'Never-satisfied gate', 'AlwaysTrue': 'Unconditional gate', 'AreaClaimed': 'Claimed status of a specified island',
    'Attractiveness': 'Attractiveness type/value and scope', 'BuildingsInBlueprintmode': 'Blueprint count for a building type',
    'BurningObject': 'Burning-object list', 'BusActivationNeedSaturation': 'Need saturation across filtered objects',
    'CameraMovement': 'Tracked camera action/distance', 'CorporationDifficulty': 'Game-setup difficulty flags',
    'Decision': 'Player decision with an option list', 'DecisionOption': 'Decision option, actions, cost/unlock/UI behavior',
    'DiplomaticState': 'Desired relationship state between participants', 'DiplomaticStateChanged': 'Diplomatic-state change / alliance count',
    'EvaluateTextSource': 'Textsource evaluation (numeric runtime discrepancy)', 'Event': 'SimpleEventType listener with event-specific context',
    'ExpeditionFinished': 'Finished expedition / morale comparison', 'ExportGoodsLeveled': 'Docklands export level/count',
    'FactoryProductivity': 'Productivity of filtered factories', 'Festival': 'Festival type and active/ended state',
    'FiniteResource': 'Remaining finite-resource quantity/types', 'FirstTimeEventHappened': 'First-time event for an asset',
    'GUIEvent': 'Local UI-state enter/leave listener', 'GameEnded': 'Win/lose state', 'GamePadAction': 'Tracked gamepad action/count',
    'HaciendaDecreesActive': 'Selected active Hacienda decree flags', 'HaciendaModuleCount': 'Hacienda module count',
    'HappinessMood': 'Population happiness mood for a participant', 'InPalaceRange': 'Any/all assets in palace range',
    'InStorage': 'Goods/items in filtered storage', 'IrrigatedModules': 'Irrigated/non-irrigated farm modules',
    'IrrigationCapacityExceeded': 'Irrigation-capacity excess', 'IsBuffed': 'Applied compatible buff count',
    'IsCampaign': 'Campaign mode', 'IsCraftingInProgress': 'Crafting-in-progress state', 'IsCreativeMode': 'Creative mode',
    'IsDLCActive': 'Activation of listed DLC assets', 'IsDiscovered': 'Participant discovery through ParticipantRelation',
    'IsDocklandsExportPyramidFull': 'Docklands pyramid completion', 'IsGamepadMode': 'Gamepad input mode',
    'IsIndustrialized': 'Industrialization amount/type or filtered objects', 'IsMultiplayer': 'Multiplayer game mode, distinct from slot count',
    'IsParticipantInGame': 'Participant selected in setup; not reliable live defeat detection', 'IsPaused': 'Paused state of filtered buildings',
    'IsTutorial': 'Tutorial mode', 'IslandsDiscovered': 'Discovered-island count and scope',
    'IslandsWithFertility': 'Owned-island count with a fertility / scope', 'MetagameLoaded': 'Loaded metagame / human count',
    'ModuleCount': 'Absolute/percentage building-module amount', 'MonoCulture': 'Monoculture delta comparison',
    'MonumentEventActive': 'Listed monument events active (property name is plural)', 'MonumentProgress': 'Filtered monument progress',
    'MoveVehicle': 'Vehicle movement/distance, optional label', 'MutualAreaInSubconditions': 'Common area of specialized child conditions',
    'NewspaperPossible': 'Newspaper-possible state', 'NewspaperPublished': 'Published newspaper / replaced-page amount',
    'ObjHPCheck': 'Target GUID/owner HP percentage', 'ObjectPosition': 'Filtered objects near filtered targets',
    'ObjectSelected': 'Filtered-object selection / incident/ruin state', 'OverlapsAABB': 'Overlap of two asset bounds',
    'PalaceItemEquipBonusActive': 'Palace item/effect building and equipment counts', 'PalaceUnlocks': 'Ministry/decree unlock flags',
    'PhotographyObject': 'Photography framing/object settings (property PhotographObject)', 'PlayerCounter': 'Typed participant counter with context and scope',
    'ProductCapacityReached': 'Product storage capacity reached', 'Productivity': 'Good production rate/productivity comparison',
    'QuestPoolQuestRunning': 'Any/all listed quest pools running a quest', 'QuestResolveConfirmation': 'Quest confirmation objective context',
    'QuestState': 'Quest/quest-line state flags', 'RecipeResearchCompleted': 'Completed research recipes by research field',
    'Reputation': 'Directional participant reputation comparison', 'ResearchPointLimitReached': 'Research-point limit state',
    'ResidentsInBuilding': 'Resident count in filtered buildings', 'Season': 'Season in specified/all sessions',
    'SelectionHappinessDebuffActive': 'Selection happiness-category debuff flags', 'SessionLoading': 'Session-loading context',
    'ShipsInRange': 'Ship/target range check with ownership and session settings', 'ShipsOwnedInSession': 'Ship/pool amount in a session',
    'ShipyardState': 'Shipyard queue state and owner', 'StarterObject': 'Quest starter selection/movement/area setup',
    'StaticResult': 'Fixed ConditionResult token', 'TextPopupClosed': 'Closed text-popup layout flags (not text GUID)',
    'TextPopupPagesViewed': 'Viewed pages by popup layout', 'Threshold': 'Textsource threshold/duration (serious recorded limitations)',
    'TimePassed': 'Time-passed comparison', 'Timer': 'Eligible-condition timer with ID/pause/unregister behavior',
    'TradeRouteCount': 'Filtered trade-route amount', 'TutorialInteraction': 'Tutorial/UI interaction and hint context',
    'Unlocked': 'Current unlock state of an asset', 'UnlockedList': 'Unlock list with range operator (property ConditionUnlockList)',
}

def cell(text):
    return re.sub(r'\s+', ' ', str(text or '')).replace('|', '\\|').replace('<', '&lt;').replace('>', '&gt;')

def fields(node, prefix=''):
    for value in node.findall('ValueDefinition'):
        name = prefix + value.findtext('Name', '?')
        yield name, value
        items = value.find('Items')
        if items is not None:
            kind = value.findtext('DataType')
            suffix = '/Item/' if kind == 'Vector' else '/{dataset key}/' if kind == 'Array' else '/'
            yield from fields(items, name + suffix)

def main():
    d = json.loads((DEST/'vanilla.json').read_text('utf-8'))
    lines = ['# Native condition and trigger contract lookup', '',
             'Generated from the local Anno 1800 dataAlle revision by `Documentation/tools/build_trigger_reference.py`. Read [trigger design](triggers.md), [condition selection and pitfalls](trigger-conditions.md), and the [audit outcome](../reference/trigger-audit.md) first.', '',
             '**Evidence:** schema and serialized defaults, not engine implementation or a game test. The 91 entries below are templates with a direct `Condition` property. Related object selectors, quest objectives and schema-only properties are listed separately. Existence does not guarantee that a condition works in every trigger context.', '',
             'Exact XML, authoring restrictions, complete datasets, SHA-256 hashes, example owners and base chains: [native contracts](../reference/triggers/vanilla.json). Missing explicit defaults stay unspecified here; do not interpret them as zero. Template overrides take precedence over property defaults. Container defaults describe list entries, not a request to insert that entry into an empty vector.', '',
             '## Template index', '', 'Candidate intent below is summarized from native names, fields and sample contexts; it is not a guarantee of runtime support. See the selection chapter for tested exceptions.', '',
             '| Template / candidate intent | Property blocks (exact names) | Explicit-template native examples (owner GUID, source line) |', '| --- | --- | --- |']
    for name, value in d['templates'].items():
        node = ET.fromstring(value['xml'].encode('utf-8'))
        if node.find('Properties/Condition') is None:
            continue
        props = [n.tag for n in node.findall('Properties/*')]
        samples = '; '.join(f"{x['guid']} (assets.xml:{x['line']}; {cell(x['name'])})" for x in d['examples'].get(name, []))
        assert name.removeprefix('Condition') in PURPOSES, name
        lines.append(f"| `{name}`: {PURPOSES[name.removeprefix('Condition')]} | " + ', '.join(f'[{p}](#{p.lower()})' for p in props) + f" | {samples or 'No explicit-Template sample captured; also search Values/property and inherited definitions.'} |")
    lines.extend(['', '## Related native templates: objectives and object selectors', '',
                  'These templates do not have a direct Condition property. They are not automatically interchangeable with a TriggerCondition. The field reference also includes schema-only properties without a same-named template (for example ConditionItemUsed).', '',
                  '| Template | Property blocks | Template source line |', '| --- | --- | --- |'])
    for name, record in d['templates'].items():
        n = ET.fromstring(record['xml'].encode('utf-8'))
        ps = [x.tag for x in n.findall('Properties/*')]
        if 'Condition' not in ps and any(x.startswith('Condition') for x in ps):
            lines.append(f"| `{name}` | " + ', '.join(f'[{p}](#{p.lower()})' for p in ps) + f" | {record['line']} |")
    lines.extend(['', '## Template overrides and related templates', '',
                  'For each indexed template, the exact template XML is retained in native contracts. The following nonempty overrides affect the effective condition; copy neither a property default nor a nearby template as a substitute.', ''])
    for name, record in d['templates'].items():
        n = ET.fromstring(record['xml'].encode('utf-8'))
        overrides = [x for x in n.findall('Properties/*') if len(x)]
        if overrides:
            lines.append(f"### {name} overrides (templates.xml:{record['line']})")
            lines.extend(['', '```xml', ''.join(ET.tostring(x, encoding='unicode', pretty_print=True) for x in overrides).strip(), '```', ''])
    lines.extend(['## Property field reference', '',
                  'Rows reproduce field types and descriptions. `{dataset key}` denotes Array entries; `Item` denotes Vector entries. AutoCreateAsset values contain embedded Template/Values definitions; their allowed properties/templates are in the Restrictions column and exact contract. Preserve spelling, including native typos.', ''])
    for name, record in d['properties'].items():
        n = ET.fromstring(record['xml'].encode('utf-8'))
        owners = [t for t, v in d['templates'].items() if ET.fromstring(v['xml'].encode('utf-8')).find('Properties/'+name) is not None]
        lines.extend([f'### {name}', '', f"Source: properties-toolone.xml:{record['line']}. Captured owning templates: " + (', '.join('`'+t+'`' for t in owners) or 'none; schema-only in this template set') + '. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).', '',
                      '| Field path | Type | Dataset | Restrictions / bounds | Native description |', '| --- | --- | --- | --- | --- |'])
        rows = list(fields(n))
        for path, f in rows:
            dataset = f.findtext('DataSet', '')
            restrictions = '; '.join(x.tag+'='+cell(x.text) for x in f if x.tag in {'NeededProperty', 'AllowedProperties', 'AllowedTemplates', 'Min', 'Max', 'ReadOnly', 'Export'})
            lines.append(f"| `{path}` | {cell(f.findtext('DataType'))} | " + (f'[{dataset}](trigger-datasets.md#{dataset.lower()})' if dataset else '') + f" | {restrictions} | {cell(f.findtext('Description'))} |")
        if not rows:
            lines.append('| No declared ValueDefinition | | | | |')
        for label, key in [('Explicit property defaults', 'defaults_xml'), ('Container defaults (entry contents)', 'container_defaults_xml')]:
            lines.extend(['', label + ':', ''])
            if record.get(key):
                lines.extend(['```xml', record[key].strip(), '```'])
            else:
                lines.append('No serialized block captured; inspect the original before drawing a runtime conclusion.')
        lines.append('')
    write(DOC/'gameplay/trigger-condition-reference.md', '\n'.join(lines)+'\n')
    lines = ['# Datasets used by condition and trigger contracts', '',
             'Generated from dataAlle datasets.xml. Names are XML serialization tokens; IDs and positions are different identifiers. A dataset entry is not proof that its consumer works in a given runtime context. Exact source hashes and full XML: [native contracts](../reference/triggers/vanilla.json).', '',
             'Return to [condition fields](trigger-condition-reference.md) or [design guidance](trigger-conditions.md).', '']
    for name, record in d['datasets'].items():
        n = ET.fromstring(record['xml'].encode('utf-8'))
        lines.extend([f'## {name}', '', f"Source: datasets.xml:{record['line']}; dataset Id={n.findtext('Id')}. Entries retain source order.", '', '| Entry | Id | Native description |', '| --- | --- | --- |'])
        for item in n.findall('Items/Item'):
            lines.append(f"| `{item.findtext('Name')}` | {item.findtext('Id', '')} | {cell(item.findtext('Description'))} |")
        lines.append('')
    write(DOC/'gameplay/trigger-datasets.md', '\n'.join(lines)+'\n')
    print('Rendered 91 native Condition templates, ' + str(len(d['properties'])) + ' property contracts and ' + str(len(d['datasets'])) + ' datasets.')

if __name__ == '__main__':
    main()
