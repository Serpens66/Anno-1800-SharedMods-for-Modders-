"""Apply Serp's 2026-10-03 clarification; never modify original mod/native evidence."""
import json
from pathlib import Path

DOC = Path(__file__).resolve().parents[1]


def read(relative):
    raw = (DOC / relative).read_bytes()
    assert raw.count(b'\n') == raw.count(b'\r\n'), relative
    return raw.decode('utf-8').replace('\r\n', '\n')


def write(relative, text):
    (DOC / relative).write_bytes(text.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))


def replace(relative, old, new):
    text = read(relative)
    if new in text:
        return
    assert text.count(old) == 1, (relative, old)
    write(relative, text.replace(old, new, 1))


def paragraph(relative, prefix, new):
    text = read(relative)
    if new in text:
        return
    start = text.index(prefix)
    end = text.index('\n\n', start)
    write(relative, text[:start] + new + text[end:])


def main():
    receipt = json.loads(read('reference/triggers/mod-cases/review-outcomes.json'))
    if 'lifecycle_followup' in receipt:
        print('Later lifecycle answers already recorded; do not replay the earlier clarification over them.')
        return
    design = 'gameplay/triggers.md'
    paragraph(design, '**Important boundaries:**', '**Parent gating — central design rule (Serp clarification, 2026-10-03):** no subordinate SubTrigger executes before its parent condition is satisfied. This also applies when the parent sets SubConditionCompletionOrder=MutuallyExclusive: that mode selects only the first matching complete child branch, from top to bottom; it does not bypass the parent gate. Serp confirms that 1500003013 therefore changes ship GUIDs only after its ConditionObjectPosition radius check succeeds. Preserve the native comment about children being "solvable before the main condition" as original wording, but do not use it to recommend early child execution against this clarification. Parent gating does not erase the separately reported remembered completion of previously satisfied siblings. ConditionMutualAreaInSubconditions retains its separately documented specialized timing observations.\n\n**Optionality and timers:** IsOptional describes whether a child is required for its parent completion. Serp thinks it has no effect on an owning main condition without a parent and is harmless there; this is an author assessment, not a new controlled test. Do not claim it consumes a false owning main. HowTo.xml:854–856 still reverses the claim that every optional descendant must be marked; the minimal required marking remains unresolved. When an ancestor becomes false during a nested timer, Serp considers a full restart on renewed eligibility **probable, not confirmed** (1500003820). Do not promise either accumulated elapsed time or an uninterrupted full interval from that assessment. See [remaining boundaries](../reference/discrepancies.md#q005-trigger-composition-and-registration-boundaries).')
    replace(design, 'Their exclusive-main, interrupted-timer and optional-owning-main questions remain open; passing offline patches does not resolve them.', 'Serp confirmed parent gating and branch priority, considers timer restart probable but unconfirmed, and assesses owning-main IsOptional as ineffective without a parent. Re-registration and nested optional-depth boundaries remain open; passing offline patches does not resolve them.')
    walk = 'reference/trigger-mod-walkthroughs.md'
    replace(walk, 'Three runtime explanations have been submitted to Serp for clarification and remain open below.', 'Serp supplied three clarifications on 2026-10-03, recorded below with their respective certainty; remaining runtime boundaries stay explicit.')
    replace(walk, '**Classification: structurally explainable; specific MutuallyExclusive gating remains an open runtime question.**', '**Classification: explainable; parent gating and exclusive branch priority confirmed by Serp.**')
    paragraph(walk, '**Question M001:**', '**M001 answered by Serp, 2026-10-03:** ConditionObjectPosition is the parent gate. No subordinate trigger executes before it is true. MutuallyExclusive selects only the first matching complete branch from top to bottom; it does not bypass that gate. Serp explicitly confirms the GUID changes occur only within Radius=115. This resolves the documented recommendation despite the contrary native description retained in the field reference. It is an author-confirmed observation/rule, not a newly performed game test.')
    paragraph(walk, '**Question M002:**', '**M002 answered with uncertainty by Serp, 2026-10-03:** a full timer restart is **probable, not confirmed** if a preceding condition becomes false in the meantime. Applied here, exceeding three pirate ships probably discards the elapsed hour and starts a fresh 3600000 ms when the preceding gates become true again. Pause/resume is not established either. The source comment about aborting and KeepTimerOnUnregister do not prove the exact interruption contract. No new test was performed.')
    replace(walk, '**Classification: optional dispatch intent is clear; top-level completion/re-registration behavior needs clarification.**', '**Classification: dispatch structure explainable; owning-main optionality assessed by Serp, re-registration behavior remains open.**')
    paragraph(walk, '**Question M003:**', '**M003 clarified by Serp, 2026-10-03:** Serp thinks IsOptional matters only when a parent condition exists, matching the property description. On this owning ConditionIsDiscovered it therefore has no effect and is harmless. This is an author assessment, not a controlled test. Discovery remains the parent gate; its optional not-defeated child does not need to block completion, but its Lua action still requires a satisfied child. In particular, top-level IsOptional is not evidence that failed discovery consumes the trigger. The original line 437 comment is preserved but this broader consumption interpretation is not recommended. The fresh/repeated-registration question is separate and remains subject to [Q005](discrepancies.md#q005-trigger-composition-and-registration-boundaries).')
    replace(walk, '| M001: exclusive children before proximity main | Open Q005 application; requested Serp clarification. |', '| M001: exclusive children before proximity main | Resolved by Serp: parent gate applies; first matching complete branch wins in source order. |')
    replace(walk, '| M002: restart versus pause below a false parent | Documentation gap/open runtime question; requested Serp clarification. |', '| M002: restart versus pause below a false parent | Serp considers full restart probable, not confirmed; runtime uncertainty retained. |')
    replace(walk, '| M003: IsOptional on the owning main condition | Documentation gap/open runtime question; requested Serp clarification. |', '| M003: IsOptional on the owning main condition | Serp assesses it as ineffective and harmless without a parent; failed-main consumption is not established. |')
    replace(walk, 'M001–M003 prevent an unqualified sign-off. Pending answers must not be silently converted into tested recipes.', 'M002 remains uncertain and M003 is an assessment; neither may be silently converted into a tested recipe.')
    disc = 'reference/discrepancies.md'
    replace(disc, '- The native Condition/SubConditionCompletionOrder description says MutuallyExclusive subconditions are solvable before the main condition. HowTo.xml:830 describes broad main-condition gating without resolving this exception. Do not extend that gating claim to every exclusive tree. The complete-branch/first-eligible-branch observations and priority remain separately documented.', '- Resolved for documentation by Serp on 2026-10-03: a parent condition gates subordinate execution, also with MutuallyExclusive. The mode chooses the first matching complete child branch from top to bottom. Serp confirms proximity gating in 1500003013. Preserve the native description about children being solvable before the main as contrary original wording, not as a bypass rule. No new game test or engine-code proof.')
    text = read(disc)
    start = text.index('**Status: awaiting Serp clarification;', text.index('## Q006:'))
    end = text.index('## Historical and context differences', start)
    replacement = '**Status: answered by Serp on 2026-10-03 with explicit certainty differences; remaining runtime questions retained.**\n\n- M001, 1500003013: confirmed parent gating and top-to-bottom MutuallyExclusive priority. This resolves the conflicting construction advice in Q005.\n- M002, 1500003820: full timer restart after an ancestor becomes false is **probable, not confirmed** according to Serp. Restart/pause behavior remains a runtime uncertainty.\n- M003, 1500003835: Serp thinks IsOptional is ineffective and harmless on an owning main without a parent. Do not infer failed-main consumption from this flag. Re-registration lifetime is a separate unresolved Q005 boundary.\n\nRemaining questions relevant to these trigger patterns: minimal IsOptional marking across nested descendants; registering already-running/completed instances in XML versus Lua; and refreshing saved registered code. Existing source-specific ForceBuild peer/session and movie/session timing qualifications also remain. These are not newly detected mod defects. Full source positions and certainty are in [six mod walkthroughs](trigger-mod-walkthroughs.md) and [case outcomes](triggers/mod-cases/review-outcomes.json).\n\n'
    write(disc, text[:start] + replacement + text[end:])
    replace('reference/coverage.md', '- Q005 records unresolved IsOptional-depth, MutuallyExclusive-gating and register/reset-context boundaries. Existing uncertain condition/action tests remain qualified beside the relevant guidance.', '- Q005 retains unresolved IsOptional-depth and register/reset-context boundaries. Serp resolved MutuallyExclusive parent gating on 2026-10-03; timer restart remains probable, not confirmed, and owning-main optionality is an author assessment. Existing uncertain tests remain qualified.')
    replace('reference/coverage.md', 'M001–M003 remain pending Serp clarification (exclusive/main gating, interrupted timer, optional owning main).', 'M001–M003 received Serp clarification: parent gating confirmed, timer restart probable but unconfirmed, owning-main optionality assessed as ineffective without a parent. Remaining registration/optional-depth and saved-code boundaries are retained.')
    replace('reference/trigger-audit.md', 'M001–M003 pending user clarification and retained runtime limitations.', 'M001–M003 author clarifications (confirmed gating, probable timer restart, assessed owning-main optionality) and retained runtime limitations.')
    # Keep verbatim native descriptions intact; add interpretation beside the source table.
    ref = 'gameplay/trigger-condition-reference.md'
    text = read(ref)
    marker = '### Condition\n'
    note = '\nSerp clarification (2026-10-03): the original descriptions below remain verbatim evidence. For construction, a parent condition gates subordinate execution even with MutuallyExclusive; choose the first matching complete branch from top to bottom. Serp assesses IsOptional on an owning main without a parent as ineffective and harmless. See [design rules and certainty](triggers.md#subtrigger-timing-and-actions).\n'
    if note not in text:
        assert text.count(marker) == 1
        write(ref, text.replace(marker, marker + note, 1))
    path = 'reference/triggers/mod-cases/review-outcomes.json'
    data = json.loads(read(path))
    answers = {
        '1500003013': ('M001', 'confirmed by Serp', 'Parent gates all subordinate execution; MutuallyExclusive chooses the first matching complete child branch from top to bottom. Radius 115 gates the GUID change.'),
        '1500003820': ('M002', 'probable, not confirmed', 'Serp expects a full timer restart when an ancestor becomes false; no certain restart/pause contract.'),
        '1500003835': ('M003', 'author assessment, not a controlled test', 'Serp thinks IsOptional has no effect and is harmless without a parent; this does not establish failed-main consumption or fresh registration.')}
    for case in data['cases']:
        if case['guid'] in answers:
            ident, certainty, answer = answers[case['guid']]
            case['questions'] = []
            case['clarification'] = {'id': ident, 'date': '2026-10-03', 'source': 'Serp direct user reply in this chat', 'certainty': certainty, 'answer': answer}
            case['classification'] = {'M001': 'explainable; parent gating confirmed by Serp', 'M002': 'explainable registration chain; timer restart probable, not confirmed', 'M003': 'dispatch explainable; owning-main optionality author-assessed, registration lifetime unresolved'}[ident]
    data['pending_user_clarifications'] = []
    data['remaining_runtime_uncertainties'] = ['M002 timer restart versus pause', 'M003 owning-main optionality assessment and registration lifetime', 'Q005 optional descendant depth and running/completed registration', 'saved registered-code refresh and source-qualified peer/session timing']
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    ledger_path = 'reference/review-ledger.json'
    ledger = json.loads(read(ledger_path))
    for case in data['cases']:
        entry = ledger['workspace:' + case['source']]
        entry['trigger_case_reviews'][case['guid']] = case
        if 'clarification' in case:
            entry['status'] = 'selected trigger definitions/integration reviewed; author clarifications recorded with remaining runtime limitations'
    write(ledger_path, json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')
    print('Recorded Serp clarifications in guidance, walkthroughs, discrepancy/coverage and review registers; original evidence untouched.')


if __name__ == '__main__':
    main()
