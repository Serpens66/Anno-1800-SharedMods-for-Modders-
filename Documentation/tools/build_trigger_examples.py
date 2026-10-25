"""Build complete isolated documentation examples with explicit placeholder bindings."""
from pathlib import Path
from lxml import etree as ET
from audit_triggers import write
from inventory import write_json

DOC = Path(__file__).resolve().parents[1]
DEST = DOC/'reference/triggers/examples'

def element(name, text=None):
    n = ET.Element(name)
    if text is not None:
        n.text = str(text)
    return n

def block(name, values=None):
    n = element(name)
    for key, value in (values or {}).items():
        n.append(element(key, value))
    return n

def condition(template, values=None, mode=None, optional=False, negate=False):
    n = element('TriggerCondition')
    n.append(element('Template', template))
    v = ET.SubElement(n, 'Values')
    c = ET.SubElement(v, 'Condition')
    if mode:
        c.append(element('SubConditionCompletionOrder', mode))
    if optional:
        c.append(element('IsOptional', 1))
    prop = 'ConditionUnlockList' if template == 'ConditionUnlockedList' else template
    v.append(block(prop, values))
    if negate:
        v.append(block('ConditionPropsNegatable', {'NegateCondition': 1}))
    return n

def actions(target, lock=False):
    n = element('TriggerActions')
    action = ET.SubElement(ET.SubElement(n, 'Item'), 'TriggerAction')
    name = 'ActionLockAsset' if lock else 'ActionUnlockAsset'
    action.append(element('Template', name))
    v = ET.SubElement(action, 'Values')
    ET.SubElement(v, 'Action')
    p = ET.SubElement(v, name)
    lst = ET.SubElement(p, 'LockAssets' if lock else 'UnlockAssets')
    ET.SubElement(ET.SubElement(lst, 'Item'), 'Asset').text = target
    return n

def trigger(c, target=None, children=(), reset=None, lock=False):
    t = element('Trigger')
    t.append(c)
    if target:
        t.append(actions(target, lock))
    else:
        ET.SubElement(t, 'TriggerActions')
    if children:
        subs = ET.SubElement(t, 'SubTriggers')
        for child in children:
            a = ET.SubElement(ET.SubElement(subs, 'Item'), 'SubTrigger')
            a.append(element('Template', 'AutoCreateTrigger'))
            ET.SubElement(a, 'Values').append(child)
    if reset is not None:
        r = ET.SubElement(t, 'ResetTrigger')
        r.append(element('Template', 'AutoCreateTrigger'))
        ET.SubElement(r, 'Values').append(reset)
    else:
        r = ET.SubElement(t, 'ResetTrigger')
        r.append(element('Template', 'EmptyAutoCreateValue'))
        v = ET.SubElement(r, 'Values')
        ET.SubElement(v, 'EmptyAutoCreateValue')
    return t

def unlock(name, optional=False):
    return condition('ConditionUnlocked', {'UnlockNeeded': name}, optional=optional)

def asset(guid, template, t=None):
    a = element('Asset')
    a.append(element('Template', template))
    v = ET.SubElement(a, 'Values')
    s = ET.SubElement(v, 'Standard')
    s.append(element('GUID', guid))
    s.append(element('Name', 'Documentation example ' + guid))
    if template == 'UnlockableAsset':
        v.append(block('Locked', {'DefaultLockedState': 1}))
    else:
        v.append(t)
        v.append(block('TriggerSetup', {'AutoRegisterTrigger': 1, 'UsedBySecondParties': 0}))
    return a

def main():
    cases = [
        ('once', 'One execution after a timer', [], trigger(condition('ConditionTimer', {'TimeLimit': 1000}), 'RESULT_GUID'),
         'One trigger instance completes once. This is not an every-save-load callback.'),
        ('repeat', 'A repeated state pulse', [], trigger(condition('ConditionTimer', {'TimeLimit': 10000}), 'RESULT_GUID',
         reset=trigger(condition('ConditionTimer', {'TimeLimit': 1000}), 'RESULT_GUID', lock=True)),
         'Main completion unlocks the private result marker; the reset child waits 1000 ms, locks it and rearms the main trigger. The main wait is 10000 ms; the reset wait is additional. Substitute your audited action and repeat policy.'),
        ('simultaneous', 'Three state gates at the action', ['GATE_A_GUID', 'GATE_B_GUID', 'GATE_C_GUID'],
         trigger(unlock('GATE_A_GUID'), children=[trigger(unlock('GATE_B_GUID'), children=[trigger(unlock('GATE_C_GUID'), 'RESULT_GUID')])]),
         'Actions belong to the deepest level. Gates are private assets initially locked; the consuming mod supplies the signals. Flattening them into Parallel siblings changes the reported timing contract.'),
        ('sequence', 'Two events in order', ['GATE_A_GUID', 'GATE_B_GUID'],
         trigger(condition('ConditionAlwaysTrue', mode='Linear'), 'RESULT_GUID', children=[
             trigger(condition('ConditionEvent', {'ConditionEvent': 'GUIDUnlocked', 'ContextAsset': 'GATE_A_GUID'})),
             trigger(condition('ConditionEvent', {'ConditionEvent': 'GUIDUnlocked', 'ContextAsset': 'GATE_B_GUID'}))]),
         'Arm before emitting A. B must occur after the second listener becomes eligible; a B event that happened earlier is not a substitute for the later event. For live state use ConditionUnlocked instead, with different semantics.'),
        ('priority', 'First complete alternative wins', ['GATE_A_GUID', 'GATE_B_GUID', 'ALTERNATE_RESULT_GUID'],
         trigger(condition('ConditionAlwaysTrue', mode='MutuallyExclusive'), children=[
             trigger(unlock('GATE_A_GUID'), children=[trigger(condition('ConditionTimer', {'TimeLimit': 1000}), 'RESULT_GUID')]),
             trigger(unlock('GATE_B_GUID'), 'ALTERNATE_RESULT_GUID')]),
         'A is first, but it must finish its descendant timer before that branch is complete. B may win while A is incomplete. Keep consequential actions at branch completion. Priority does not reserve the result merely because A first became true.'),
        ('optional', 'Optional side action without blocking', ['GATE_A_GUID', 'OPTIONAL_RESULT_GUID'],
         trigger(condition('ConditionTimer', {'TimeLimit': 1000}), 'RESULT_GUID', children=[trigger(unlock('GATE_A_GUID', optional=True), 'OPTIONAL_RESULT_GUID')]),
         'The root can complete without the side gate. A side action is conditional, not guaranteed. This leaf example avoids the unresolved minimal IsOptional marking of nested descendants.'),
        ('removal-safe', 'A locked-presence guard for saved triggers', ['PRESENCE_GUID'],
         trigger(condition('ConditionUnlocked', {'UnlockNeeded': 'PRESENCE_GUID'}, negate=True), children=[
             trigger(condition('ConditionTimer', {'TimeLimit': 1000}), 'RESULT_GUID')]),
         'PRESENCE_GUID is a private UnlockableAsset with DefaultLockedState=1 which must never be unlocked. The saved trigger checks that it is still locked before its child/actions can run. When the mod asset disappears, the reported missing-GUID-as-unlocked behavior makes the negated guard false. This demonstrates the presence guard, not a new in-game removal test or a lock-to-start bridge.'),
        ('human-session', 'Positive participant and session gates', [],
         trigger(unlock('1500001613'), children=[trigger(condition('ConditionActiveSession', {'ActiveSession': 180023}), children=[
             trigger(condition('ConditionTimer', {'TimeLimit': 1000}), 'RESULT_GUID')])]),
         'Requires ModDependencies containing WhichPlayer_Serp (which depends on IsAIPlayer_Serp), plus its actual initialization scripts. Positive 1500001613 identifies processing Human0 after readiness; 180023 is the audited Moderate session. Any Coop peer may satisfy ActiveSession. This does not select one Lua peer or establish an action session/area.'),
    ]
    lines = ['# Worked trigger recipes and new-chat walkthroughs', '',
             'Read [design](triggers.md), [condition pitfalls](trigger-conditions.md) and [audit boundaries](../reference/trigger-audit.md) first. The XML files below are complete ModOps **documentation examples**, not installed mods. Every uppercase GUID token is a required collision-free reserved integer substitution; tests bind them to private fixture IDs. No example is deployed or run in the game.', '',
             'Each example introduces its own locked result/signal assets, preserving the native anchor 130248. Gates illustrate input signals; they are not population/session/object checks until replaced by an audited contract. Shared helper IDs in the final recipe are real dependencies, not fixture-defined native assets. In a new mod, also create the usual modinfo.json with your stable ModID and dependencies.', '',
             '## Examples', '']
    manifest = []
    for name, title, gates, t, explanation in cases:
        root = element('ModOps')
        op = ET.SubElement(root, 'ModOp', Type='AddNextSibling', GUID='130248')
        for guid in ['RESULT_GUID'] + gates:
            op.append(asset(guid, 'UnlockableAsset'))
        op.append(asset('CUSTOM_TRIGGER_GUID', 'Trigger', t))
        ET.indent(root, space='  ')
        source = ET.tostring(root, encoding='unicode')+'\n'
        path = DEST/(name+'.xml')
        write(path, source)
        manifest.append({'case': name, 'path': str(path), 'tokens': sorted(set(['RESULT_GUID', 'CUSTOM_TRIGGER_GUID']+gates)),
                         'external': ['WhichPlayer_Serp', '1500001613', '180023'] if name=='human-session' else [],
                         'runtime_evidence': 'Source-based design, not a newly executed runtime test'})
        lines.extend([f'### {title}', '', explanation, '', f'[Complete XML](../reference/triggers/examples/{name}.xml).', ''])
        if name in {'once', 'simultaneous', 'priority', 'optional', 'removal-safe'}:
            # Show the readable trigger body here; complete files include all assets and setup.
            lines.extend(['Embedded Trigger body (inside Values of the owning Trigger asset):', '', '```xml', ET.tostring(t, encoding='unicode').strip(), '```', ''])
    lines.extend(['## Walk through a design using only this documentation', '',
                  '| Task | Expected design / reason |', '| --- | --- |',
                  '| Complex A, B, C live-state requirement | Nested one-child gates with actions at C; explain why Parallel remembers earlier successes. Check optional/MutualArea exceptions before substituting them. |',
                  '| Ordered event chain | Linear children, with each event emitted after its listener becomes eligible; a persistent unlock is a different state check. |',
                  '| Prioritized alternatives | MutuallyExclusive, highest-priority complete branch first; incomplete first branches do not yet exclude later complete branches. Avoid irreversible actions in speculative partial branches. |',
                  '| Repeated execution | Embedded ResetTrigger with a deliberate wait; include its wait in the cycle and account for actions changing the original condition. |',
                  '| Save-compatible extension | Preserve historical GUID state; a separately guarded migration or the documented reset extension point supplies new actions. Explain why appending a reset to a completed GUID is insufficient. |',
                  '| Coop-sensitive Lua action | Identify processing participant separately from executing peers. Use the reviewed lock/cooldown or peer mechanism; Human0 alone does not deduplicate clients. |',
                  '| Multiple checks on one island | Use the specialized main MutualArea plus same-level Area-producing checks and the correct action/quest context. Session agreement alone is insufficient. |', '',
                  'Offline checks parse all eight complete examples, bind placeholders, verify native template/property membership, inspect the exact subtrigger/reset trees, and apply each ModOp with the actual Anno 1800 XML evaluator to the exact vanilla anchor. The checks do not execute conditions/actions, settle the unresolved timing contracts or prove multiplayer safety. See [validation results](../reference/validation/triggers/results.json).', ''])
    write(DOC/'gameplay/trigger-recipes.md', '\n'.join(lines)+'\n')
    write_json(DEST/'manifest.json', manifest)
    print('Built eight complete XML examples and the recipe chapter.')

if __name__ == '__main__':
    main()
