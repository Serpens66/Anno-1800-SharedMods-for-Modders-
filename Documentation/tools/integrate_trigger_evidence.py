"""Attach trigger-scope evidence without promoting scans to complete whole-source reviews."""
from pathlib import Path
import json
import re
from audit_triggers import DEST, write
from inventory import OUT, write_json

DOC = Path(__file__).resolve().parents[1]

def destination(text, source):
    if re.search(r'IsOptional|MutuallyExclusive|SubCondition|Parallel|Linear|subtrigger', text, re.I):
        return 'gameplay/triggers.md#subtrigger-timing-and-actions', 'Composition / reported timing; retain tentative or conflicting wording.'
    if re.search(r'savegame|samegame|safe vorhanden|deactivat|disabled|removed assets|nicht existente|non.existen|already registered|old code|GUIDs.*free', text, re.I):
        return 'gameplay/triggers.md#savegames-removal-and-extension-points', 'Saved-state/removal observation or migration context, not automatic replay.'
    if re.search(r'QuestArea|InheritArea|SessionFilter|AllowProcessing|AllowQuest|LimitToQuest|CounterScope|parent.condition.object|ObjectUseParent', text, re.I):
        return 'gameplay/trigger-conditions.md#area-session-and-object-propagation', 'Context-dependent consumer or propagation observation; no generalization to arbitrary actions.'
    if re.search(r'Threshold|EvaluateTextSource|InStorage|IsBuffed|ItemUsed|ItemAction|IslandsWithFertility|Attractiveness', text, re.I):
        return 'gameplay/trigger-conditions.md#numeric-text-sources-storage-buffs-and-item-activation', 'Specialized condition; distinguish schema, explicit tests, failures and proposed checks.'
    if re.search(r'ConditionEvent|GUIEvent|MovieFinished|LeaveUI|EnterUI|NotificationRemoved|PreCondition|TextPopup|QuestState|QuestStarted|QuestResolved', text, re.I):
        return 'gameplay/trigger-conditions.md#events-ui-and-quests', 'Event/quest/local-UI context; preserve listener order, exact GUID and test limitations.'
    if re.search(r'RegisterTrigger|ResetTrigger|ConditionTimer|init|delay', text, re.I):
        return 'gameplay/triggers.md#registration-repeat-execution-and-initialization', 'Registration/reset/readiness example, not universal idempotence or timing proof.'
    if re.search(r'coop|desync|ActionExecuteScript|multiplayer|SessionEnter|SessionLoaded|game.loaded|session.*load', text, re.I):
        return 'gameplay/triggers.md#session-lifecycle-and-luacoop', 'Client/participant/lifecycle observation; do not infer MP safety.'
    if re.search(r'PlayerCounter|CheckedParticipant|WorkingConditions|RelativeToQuestStart|ProfileCounter', text, re.I):
        return 'gameplay/trigger-conditions.md#playercounter-contracts-and-pitfalls', 'Counter context/ownership/aggregation; distinguish suggestions from successful tests.'
    if re.search(r'processing|WhichPlayer|IsParticipant|IsAIPlayer|dead|defeat|second.part|human', text, re.I):
        return 'gameplay/triggers.md#participants-execution-multiplicity-and-context', 'Participant targeting/readiness/liveness context; not a peer selector.'
    if re.search(r'infotip|tooltip|Visibility|Condition=|ModOp|XPath', text, re.I) or 'exportbin_' in source:
        return 'gameplay/triggers.md', 'Separate XML patch/UI consumer or contextual application; consult linked ModOps/infotip chapters.'
    return 'gameplay/trigger-conditions.md#action-side-special-cases-that-affect-trigger-design', 'Contextual action/example, allocation or experiment; original wording is evidence, not a universal recipe.'

def main():
    w = json.loads((DEST/'workspace.json').read_text('utf-8'))
    lines = ['# Traceable trigger-source comment evidence', '',
             'This register preserves original source quotations, including German and failed/TODO experiments. English destinations/treatments explain where to read the governing contract. Read [audit scope](../trigger-audit.md) before treating an excerpt as tested behavior. Hashes, encodings, full origins and byte-identical source groups are in [workspace extraction](workspace.json).', '',
             'Each E-number is the stable zero-based comment index in workspace.json for this extraction. XML-only comment lines remain in that JSON; the prose table does not substitute for their surrounding complete XML definition. A documentation destination is a topic association, not a claim that every contextual mod application is a validated recipe.', '',
             '| Evidence | First source and line | Source quotation | Documentation / treatment |', '| --- | --- | --- | --- |']
    associations = []
    origins = {}
    pattern = re.compile(r'trigger|condition|processing|checkedparticipant|inheritarea|questarea|sessionfilter', re.I)
    for i, c in enumerate(w['comments']):
        xml_only = re.fullmatch(r'<[^>]+>.*?</[^>]+>|<[^>]+>', c['text'], re.S)
        if not pattern.search(c['text']) or xml_only:
            continue
        first = c['sources'][0]
        target, treatment = destination(c['text'], first['id'])
        association = {'evidence': 'E'+str(i), 'origins': c['sources'], 'documentation': target, 'treatment': treatment,
                       'status': 'source quotation and topic association; no new runtime verification'}
        associations.append(association)
        for s in c['sources']:
            origins.setdefault(s['id'], set()).add(target)
        quoted = c['text'].replace('|', '\\|').replace('<', '&lt;').replace('>', '&gt;').replace('[', '&#91;').replace(']', '&#93;')
        if len(quoted) > 2500:
            quoted = 'Long mixed ModOps/notebook source block; exact text is retained in workspace.json at this evidence index. Trigger-specific later notebook comments are individually indexed below.'
        status = 'WIP/retired source; ' if re.search(r'WorkInProgress|Outdated|will not work|OLD solution', first['id']+' '+c['text'], re.I) else ''
        lines.append(f"| E{i} | `{first['id']}:{first['line']}` | {quoted} | [{target}]({ '../../'+target }); {status}{treatment} |")
    write(DEST/'prose-evidence.md', '\n'.join(lines)+'\n')
    write_json(DEST/'evidence-associations.json', associations)
    # Append a topic-scoped review to existing records; never overwrite their review status/outcome.
    ledger_path = OUT/'review-ledger.json'
    raw = ledger_path.read_bytes()
    assert not raw.startswith(b'\xef\xbb\xbf'), 'Preserve existing BOM/encoding deliberately'
    ledger = json.loads(raw.decode('utf-8'))
    lookup = {s['id']: s for s in w['sources']}
    for ident, docs in origins.items():
        s = lookup[ident]
        if ident not in ledger:
            ledger[ident] = {'sha256': s['sha256'], 'reviewed_on': '2026-10-03',
                             'status': 'trigger-topic comments reconciled; complete source/integration review pending',
                             'documentation': sorted({x.split('#')[0] for x in docs}),
                             'outcome': 'Trigger-relevant source quotations reconciled with topic guidance; no complete whole-file or runtime certification.'}
        ledger[ident]['trigger_review'] = {'sha256': s['sha256'], 'reviewed_on': '2026-10-03',
                                          'scope': 'trigger-specific comment evidence and structural lookups, not complete whole-mod integration',
                                          'documentation': sorted(docs), 'evidence': 'triggers/evidence-associations.json'}
    write_json(ledger_path, ledger)
    # Preserve inventory counts and statuses; a topic-scoped association is additional evidence only.
    path = OUT/'source-inventory.json'
    raw = path.read_bytes()
    assert not raw.startswith(b'\xef\xbb\xbf')
    rows = json.loads(raw.decode('utf-8'))
    for row in rows:
        if row['id'] in origins:
            row['trigger_review_record'] = 'review-ledger.json#'+row['id']
    write_json(path, rows)
    # Remove only the transient extraction pages made by audit_triggers in this task.
    for number in range(1, 20):
        path = DEST/f'comments-{number:02}.md'
        if path.exists():
            path.unlink()
    print(json.dumps({'prose_evidence_rows': len(associations), 'sources_with_topic_evidence': len(origins),
                      'review_ledger_records': len(ledger)}))

if __name__ == '__main__':
    main()
