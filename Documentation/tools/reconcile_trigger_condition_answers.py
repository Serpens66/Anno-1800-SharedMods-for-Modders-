"""Apply Serp's condition clarifications, preserving tentative original findings."""
import hashlib
import json
from pathlib import Path
from reconcile_trigger_clarifications import DOC, read, write, replace, paragraph


def main():
    receipt_path = DOC/'reference/triggers/condition-clarifications.json'
    if receipt_path.exists():
        previous = json.loads(receipt_path.read_text('utf-8'))
        if any(answer['id'] == 'T004' for answer in previous.get('answers', [])):
            print('Later quest/MP answers already recorded; do not replay earlier pending questions.')
            return
    condition = 'gameplay/trigger-conditions.md'
    replace(condition, 'The author explicitly doubts whether both flags are needed.', 'Serp explicitly confirmed on 2026-10-03 that it remains **unclear whether both flags are required or one suffices**. The observed combined setup does not establish either flag individually as sufficient.')
    replace(condition, 'CodeSnippets say it appears to require simultaneous subconditions in this special arrangement, unlike ordinary remembered Parallel completion.', 'Serp assessed the original simultaneous-subconditions comment on 2026-10-03 as **very likely correct, not absolutely certain**: this special arrangement requires simultaneous subconditions rather than ordinary remembered Parallel completion.')
    replace(condition, 'Keep "appears" for the timing exception.', 'Retain the very-likely qualification for the timing exception; no new game test was performed.')
    paragraph(condition, '**ConditionThreshold:**', '**ConditionThreshold:** Serp explicitly reaffirmed on 2026-10-03 that **all comments in CodeSnippets.md:702–710 remain current**, with their original certainty. Actions executed **23 times** in the recorded intended-single-execution test; ResetTrigger appeared never true, and placing Threshold in a SubTrigger hung new-game/save loading. Meta-storage usage appeared usable, area building counts required IsAreaSpecific=1, and the ProfileCounter text-source setup appeared not to work. ThresholdDuration=0 appeared usable; positive durations working and milliseconds as the unit remain **probable, not confirmed**. Do not silently promote any original "seems"/"likely" finding into certainty or universalize the exact 23 count to every context. Do not use Threshold as a drop-in fix for EvaluateTextSource. Prefer native counters for supported quantities, or an established Lua/lock bridge; keep an isolated Threshold workaround\'s limits beside its example. No new game test was performed.')
    replace('gameplay/triggers.md', 'ConditionMutualAreaInSubconditions retains its separately documented specialized timing observations.', 'ConditionMutualAreaInSubconditions retains its specialized timing observation: Serp considers simultaneous subconditions **very likely required, not absolutely certain** in the tested main-condition arrangement.')
    replace('reference/personal-test-evidence.md', '| ConditionMutualAreaInSubconditions only works reliably in tested main-condition context | Not a general constraint that can be moved anywhere in a condition tree |', '| ConditionMutualAreaInSubconditions only works reliably in tested main-condition context | Serp clarification2026-10-03: simultaneous subconditions very likely required, not absolutely certain; do not move the condition arbitrarily within the tree |')
    replace('reference/personal-test-evidence.md', '| ConditionThreshold works in some storage contexts; mass repetition/subtrigger hangs reported | Preserve context and performance limits |', '| ConditionThreshold works in some storage contexts; mass repetition/subtrigger hangs reported | Serp reaffirmed all CodeSnippets comments2026-10-03; original seems/likely qualifiers remain. Positive durations and milliseconds remain probable, not confirmed |')
    audit = 'reference/trigger-audit.md'
    replace(audit, 'Threshold units beyond tested zero, MutualArea simultaneous behavior,', 'Threshold units/positive durations (still probable), MutualArea simultaneous behavior (very likely, not certain),')
    disc = 'reference/discrepancies.md'
    section = '''## Q007: MutualArea, quest linking and Threshold follow-up

**Status: answered by Serp on 2026-10-03 with explicit certainty differences. No new game test.**

- ConditionMutualAreaInSubconditions simultaneous subconditions: **very likely correct, not absolutely certain**, according to Serp. Original comment: Outdated_shared_AreaBuffsHelper (Serp)/data/config/export/main/asset/assets.xml:50–53; HowTo.xml:859. The tested main-condition/same-level arrangement remains the scope.
- Quest-linked object flags: **still unclear** whether LinkAllQuestActionsToQuest and LinkAllActionsToQuest are both required or one is sufficient (HowTo.xml:1142–1143). The combined example is evidence of that combination only.
- ConditionThreshold: Serp reaffirmed all CodeSnippets.md:702–710 comments. Preserve their exact qualifications: reported 23-fold execution, reset/subtrigger failures and text-source contexts; positive ThresholdDuration values working and milliseconds as the unit remain **probable, not confirmed**.

Exact original paths, lines, hashes and direct-user-answer certainty: [condition clarification receipt](triggers/condition-clarifications.json). Guidance: [condition selection](../gameplay/trigger-conditions.md). Remaining concrete questions T004–T006 concern quest-start emission, ForceBuild peer/session scope and multiplayer difficulty checks; source-specific uncertainty is retained until answered. Known failed experiments are not automatically treated as new mod defects.

'''
    text = read(disc)
    if section not in text:
        assert '## Q007:' not in text
        write(disc, text.replace('## Historical and context differences', section + '## Historical and context differences', 1))
    coverage = 'reference/coverage.md'
    text = read(coverage)
    note = '- Q007 records Serp condition follow-up2026-10-03: MutualArea simultaneous subconditions very likely, quest-linking minimum flags still unclear, all Threshold comments reaffirmed with original probability qualifiers. T004–T006 retain concrete further runtime questions; see [condition clarification receipt](triggers/condition-clarifications.json).\n'
    if note not in text:
        write(coverage, text.replace('## Six real trigger cases', note + '\n## Six real trigger cases', 1))
    root = DOC.parent.parent
    notebook = Path('D:/CDesktopLink/Unterlagen/Mods/Anno 1800/HowTo.xml')
    helper = root/'SharedMods/Outdated_shared_AreaBuffsHelper (Serp)/data/config/export/main/asset/assets.xml'
    snippets = root/'SharedMods/CodeSnippets.md'
    forcebuild = root/'SharedMods/shared_PirateExtraSpawn/data/scripts_serp/forcebuild_harlow.lua'
    def source(path, first, last):
        return {'path': str(path), 'line': first, 'end_line': last, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    receipt = {'date': '2026-10-03', 'answer_source': 'Serp direct user reply in this chat', 'new_game_or_mp_tests': False, 'mod_source_changes': False,
        'answers': [
            {'id': 'T001', 'topic': 'MutualArea simultaneous subconditions', 'certainty': 'very likely, not absolutely certain', 'answer': 'Serp thinks the original comment is correct.', 'sources': [source(helper, 50, 53), source(notebook, 859, 859)]},
            {'id': 'T002', 'topic': 'Quest-linking minimum flags', 'certainty': 'unresolved', 'answer': 'Still unclear whether both flags are required or one suffices.', 'sources': [source(notebook, 1142, 1143)]},
            {'id': 'T003', 'topic': 'Threshold comments', 'certainty': 'original certainty retained; likely remains probable', 'answer': 'All CodeSnippets comments remain current, including the likely statements.', 'sources': [source(snippets, 702, 710)]}],
        'pending_questions': [
            {'id': 'T004', 'question': 'Has the hypothesis that QuestStarted only works for pool-started quests, rather than ActionStartQuest, been tested?', 'sources': [source(notebook, 1659, 1660)]},
            {'id': 'T005', 'question': 'Was one ForceBuild ship per script invocation observed in Coop/multiplayer, including peers in different sessions, or is this inferred from once-per-tick behavior?', 'sources': [source(forcebuild, 3, 7)]},
            {'id': 'T006', 'question': 'Does ConditionCorporationDifficulty still appear not to work in multiplayer; is there a more precise tested scope?', 'sources': [source(notebook, 2616, 2616)]}]}
    write('reference/triggers/condition-clarifications.json', json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    ledger_path = 'reference/review-ledger.json'
    ledger = json.loads(read(ledger_path))
    for key in ['notes:HowTo.xml', 'workspace:' + str(helper.relative_to(root)).replace('\\', '/'), 'workspace:' + str(snippets.relative_to(root)).replace('\\', '/')]:
        assert key in ledger, key
        ledger[key]['condition_clarification_receipt'] = 'reference/triggers/condition-clarifications.json'
        destinations = ledger[key].setdefault('documentation', [])
        if 'gameplay/trigger-conditions.md' not in destinations:
            destinations.append('gameplay/trigger-conditions.md')
    write(ledger_path, json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')
    print('Recorded three condition answers and three remaining questions with original source hashes; no source mods changed.')


if __name__ == '__main__':
    main()
