"""Record Serp's quest-event and multiplayer clarifications without new runtime claims."""
from workspace_paths import current_source_id
import json
from reconcile_trigger_clarifications import read, write, replace, paragraph


def main():
    receipt_path = 'reference/triggers/condition-clarifications.json'
    data = json.loads(read(receipt_path))
    if any(answer['id'] == 'T007' for answer in data['answers']):
        print('Later HowTo status answers recorded; do not reopen those questions.')
        return
    condition = 'gameplay/trigger-conditions.md'
    replace(condition, '| QuestSuccessfullyResolved + ContextData | Worked in a documented setup; QuestStarted did not. Explicit ActionStartQuest versus pool start/context may account for the difference. Do not interchange ContextData and ContextAsset without a native/example match. |', '| QuestSuccessfullyResolved + ContextData | Worked in a documented setup; QuestStarted did not. Serp clarification2026-10-03: pool start versus ActionStartQuest remains a **reasoned hypothesis, not further tested**. Do not treat pool start as a proven fix or interchange ContextData and ContextAsset without a native/example match. |')
    replace(condition, 'ConditionAttractiveness queries and ConditionCorporationDifficulty in MP have uncertain/failed test contexts.', 'ConditionAttractiveness queries remain uncertain; Serp clarified on 2026-10-03 that ConditionCorporationDifficulty **probably does not work in multiplayer**, with no further tests and no newly established Coop-versus-multiple-participant distinction.')
    mp = 'multiplayer/synchronization.md'
    text = read(mp)
    note = '**ForceBuild clarification from Serp (2026-10-03):** the comment describing this command as usable in multiplayer is conditional on **every client executing it in exactly the same game tick**. A command described elsewhere as multiplayer-incompatible can still be usable under that synchronized-execution premise; the label does not make arbitrary local calls safe. For this specific workflow, Serp considers a direct single ForceBuild call through ActionExecuteScript, repeated through separate script invocations, relatively practical without desync. This is an author assessment, not a newly supplied controlled test or a universal scheduling guarantee. Keep each direct invocation free of per-client waits/coroutine delays that could move it to different ticks. The once-per-tick build limit and all-client same-tick execution are distinct requirements. Follow identical effective participant/session/target data as well; the answer does not establish the behavior of SessionParticipants when clients are in different sessions. Original example: shared_PirateExtraSpawn/data/scripts_serp/forcebuild_harlow.lua:3–7; [walkthrough](../reference/trigger-mod-walkthroughs.md#1500003820--shared_pirateextraspawn).\n\n'
    if note not in text:
        write(mp, text.replace('## Local context and disconnected peers', note + '## Local context and disconnected peers', 1))
    api = 'lua/api-and-timing.md'
    replace(api, '| Trader ForceBuild | The documented successful access is through SessionParticipants, not Participants. It follows trader/pirate fleet definitions and is reported limited to one built ship per tick. |', '| Trader ForceBuild | The documented successful access is through SessionParticipants, not Participants. It follows trader/pirate fleet definitions and is reported limited to one built ship per tick. Serp considers direct ActionExecuteScript invocation practical in MP **if all clients execute in exactly the same tick**; see [conditional MP contract](../multiplayer/synchronization.md#command-specific-behavior). This is not proof for arbitrary waits or differing sessions. |')
    walk = 'reference/trigger-mod-walkthroughs.md'
    paragraph(walk, 'The deepest actions register', 'The deepest actions register a short-lived script-dispatch trigger rather than directly repeating ForceBuild within one Lua call. forcebuild_harlow.lua:3–7 reports one build per game tick. ActionExecuteScript still runs on all human clients. Serp clarified on 2026-10-03 that the claimed multiplayer usability requires every client to call ForceBuild in **exactly the same tick**: direct one-call scripts, repeated via separate ActionExecuteScript invocations, are relatively practical under that premise. This is an author assessment, not a newly supplied controlled MP test or general scheduling guarantee. Once-per-tick throttling alone does not prove same-tick execution across peers. The script uses SessionParticipants, not the XML counter\'s Global scope; its different-session behavior remains unestablished by this answer. See [multiplayer contract](../multiplayer/synchronization.md#command-specific-behavior).')
    replace('reference/personal-test-evidence.md', '| ConditionEvent QuestSuccessfullyResolved with ContextData works; QuestStarted did not in one setup | ActionStartQuest versus pool start may explain context; do not claim all quest events are interchangeable |', '| ConditionEvent QuestSuccessfullyResolved with ContextData works; QuestStarted did not in one setup | Serp clarification2026-10-03: ActionStartQuest versus pool start remains a reasoned hypothesis, not further tested |')
    disc = 'reference/discrepancies.md'
    replace(disc, 'Remaining concrete questions T004–T006 concern quest-start emission, ForceBuild peer/session scope and multiplayer difficulty checks; source-specific uncertainty is retained until answered.', 'T004–T006 were answered by Serp: QuestStarted pool/action distinction is a reasoned hypothesis, not further tested; ForceBuild usability is conditional on all clients executing in exactly the same tick, without a new different-session test claim; CorporationDifficulty probably fails in MP and was not further tested. Retain these certainty limits.')
    coverage = 'reference/coverage.md'
    replace(coverage, 'T004–T006 retain concrete further runtime questions;', 'T004–T006 answered: quest-start distinction remains a reasoned hypothesis, ForceBuild usability requires identical-tick execution on every client, and CorporationDifficulty probably fails in MP without further tests;')
    answers = {
        'T004': ('reasoned hypothesis, not further tested', 'QuestStarted pool-versus-ActionStartQuest distinction remains a reasoned hypothesis.'),
        'T005': ('conditional author assessment; no new controlled test supplied', 'ForceBuild can be practical through direct single ActionExecuteScript calls repeated separately if every client executes in exactly the same tick. Once-per-tick limitation does not itself prove peer tick alignment; different-session behavior was not established.'),
        'T006': ('probably fails in multiplayer, not further tested', 'ConditionCorporationDifficulty probably does not work in multiplayer; no further test or Coop-versus-participant scope supplied.')}
    for question in data['pending_questions']:
        ident = question['id']
        if ident not in answers:
            continue
        certainty, answer = answers[ident]
        data['answers'].append({'id': ident, 'topic': question['question'], 'certainty': certainty, 'answer': answer, 'sources': question['sources'], 'answer_source': 'Serp direct follow-up reply in this chat', 'date': '2026-10-03'})
    notebook = next(answer for answer in data['answers'] if answer['id'] == 'T004')['sources'][0]
    def notebook_source(first, last):
        return dict(notebook, line=first, end_line=last)
    data['pending_questions'] = [
        {'id': 'T007', 'question': 'Does ConditionAttractiveness/CountAllTypes sum attraction types or check individual types? Was the proposed Area PlayerCounter Attractiveness alternative actually tested?', 'sources': [notebook_source(1844, 1848)]},
        {'id': 'T008', 'question': 'Is the possible need for two full trigger executions when adding goods/items to third-party ships still current, or was its readiness/context cause resolved?', 'sources': [notebook_source(1857, 1857)]}]
    write(receipt_path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    section = '''## Q008: remaining attractiveness and third-party inventory questions

**Status: awaiting Serp clarification; original qualifications retained.**

- T007, HowTo.xml:1844–1848: ConditionAttractiveness/CountAllTypes did not trigger in the recorded test; summing types versus checking individual types is uncertain. PlayerCounter/Attractiveness is proposed for island totals, not marked as a successful matching test. Ask whether either interpretation or alternative was subsequently tested.
- T008, HowTo.xml:1857: adding goods/items to third-party ships may require two full trigger executions, explicitly not merely two actions. Ask whether this remains current or a readiness/context cause was established. The separately reported post-spawn-trigger workaround does not resolve this case by itself.

Exact source paths, lines and hashes: [condition clarification receipt](triggers/condition-clarifications.json). No mod defect or new runtime result is inferred from these open questions.

'''
    text = read(disc)
    if section not in text:
        assert '## Q008:' not in text
        write(disc, text.replace('## Historical and context differences', section + '## Historical and context differences', 1))
    # Existing scope/status and original evidence remain untouched.
    ledger_path = 'reference/review-ledger.json'
    ledger = json.loads(read(ledger_path))
    entry = ledger[next(key for key in ledger if current_source_id(key) ==
                        'workspace:SharedMods/shared_PirateExtraSpawn/data/config/export/main/asset/SpawnShipsIfWeak.include.xml')]
    entry['condition_clarification_receipt'] = 'reference/triggers/condition-clarifications.json'
    entry['forcebuild_mp_clarification'] = {'date': '2026-10-03', 'source': 'Serp direct user reply', 'certainty': answers['T005'][0], 'answer': answers['T005'][1]}
    for destination in ['multiplayer/synchronization.md', 'reference/trigger-mod-walkthroughs.md']:
        if destination not in entry.setdefault('documentation', []):
            entry['documentation'].append(destination)
    write(ledger_path, json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')
    print('Recorded QuestStarted, conditional ForceBuild MP use and CorporationDifficulty answers; original sources preserved.')


if __name__ == '__main__':
    main()
