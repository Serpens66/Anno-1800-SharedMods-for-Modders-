"""Record that the two remaining HowTo cases have no newer test result."""
import json
from reconcile_trigger_clarifications import read, write, replace


def main():
    receipt_path = 'reference/triggers/condition-clarifications.json'
    data = json.loads(read(receipt_path))
    if any(answer['id'] == 'T007' for answer in data['answers']):
        print('Latest-known HowTo status already recorded.')
        return
    for question in data['pending_questions']:
        assert question['id'] in {'T007', 'T008'}
        data['answers'].append({'id': question['id'], 'topic': question['question'],
            'certainty': 'unresolved; original HowTo qualifications retained',
            'answer': 'Serp has no newer findings; the HowTo text remains the latest known state. This is not confirmation of the tentative mechanism or proposed alternative.',
            'sources': question['sources'], 'date': '2026-10-03',
            'answer_source': 'Serp direct reply in this chat'})
    data['pending_questions'] = []
    data['clarification_status'] = 'All eight submitted condition questions answered; qualified runtime uncertainties remain. No further clarification required for these scoped findings.'
    write(receipt_path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    condition = 'gameplay/trigger-conditions.md'
    replace(condition, 'ConditionAttractiveness queries remain uncertain;', 'Serp confirmed on 2026-10-03 that HowTo.xml:1844–1848 is the latest known state: ConditionAttractiveness/CountAllTypes interpretation remains uncertain and the suggested PlayerCounter/Attractiveness alternative is not newly confirmed;')
    replace(condition, 'Third-party ship tests sometimes needed two executions;', 'HowTo.xml:1857 says third-party ships may need **two full trigger executions**, not merely two actions. Serp confirmed on 2026-10-03 that this is the latest known state, with no newer findings; the need/cause remains tentative rather than a guaranteed two-pass fix. For those recorded cases,')
    disc = 'reference/discrepancies.md'
    replace(disc, '**Status: awaiting Serp clarification; original qualifications retained.**', '**Status: answered by Serp on 2026-10-03: no newer findings; HowTo is the latest known state. Runtime uncertainty and original qualifications remain.**')
    replace(disc, 'Ask whether either interpretation or alternative was subsequently tested.', 'Serp has no newer findings; neither the interpretation nor the proposed alternative is newly confirmed.')
    replace(disc, 'Ask whether this remains current or a readiness/context cause was established.', 'Serp has no newer findings; the tentative two-execution observation remains current and its cause is still unknown.')
    replace(disc, 'No mod defect or new runtime result is inferred from these open questions.', 'Both clarification requests are answered. No mod defect or new runtime result is inferred; no new answer is required to retain the documented uncertainty.')
    coverage = 'reference/coverage.md'
    text = read(coverage)
    note = '- Q008 answered2026-10-03: Serp has no newer attractiveness or third-party inventory findings; HowTo remains the latest state with original qualifications. All eight submitted condition questions are answered; remaining uncertainty is not a pending clarification or runtime certification.\n'
    if note not in text:
        write(coverage, text.replace('## Six real trigger cases', note + '\n## Six real trigger cases', 1))
    ledger_path = 'reference/review-ledger.json'
    ledger = json.loads(read(ledger_path))
    ledger['notes:HowTo.xml']['latest_trigger_condition_followup'] = {
        'date': '2026-10-03', 'source': 'Serp direct user reply', 'cases': ['T007', 'T008'],
        'answer': 'No newer findings; original HowTo uncertainties remain latest known state.',
        'receipt': 'reference/triggers/condition-clarifications.json'}
    write(ledger_path, json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')
    print('Recorded latest-known status for both HowTo cases; all submitted clarification questions answered, runtime uncertainty retained.')


if __name__ == '__main__':
    main()
