"""Integrate scoped review receipts; preserve previous review outcomes and encodings."""
import json
import re
from pathlib import Path
from inventory import ROOT, write_json
from inspect_mod_trigger_cases import OUT

DOC = Path(__file__).resolve().parents[1]

def encoded(text):
    return text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8')

def add(path, text, before=None):
    p = DOC/path
    raw = p.read_bytes()
    raw.decode('utf-8')
    assert raw.count(b'\n')==raw.count(b'\r\n'), path
    data = encoded(text)
    if data in raw:
        return
    if before:
        key = encoded(before)
        assert raw.count(key)==1, path
        raw = raw.replace(key, data+key, 1)
    else:
        raw += data
    p.write_bytes(raw)

def main():
    receipt = OUT/'review-outcomes.json'
    if receipt.exists():
        previous = json.loads(receipt.read_text('utf-8'))
        if any('clarification' in case for case in previous.get('cases', [])):
            print('Author clarifications already recorded; preserve them. Re-audit changed sources and reconcile outcomes explicitly before regenerating this initial review receipt.')
            return
    cases = json.loads((OUT/'cases.json').read_text('utf-8'))
    statuses = {
        '1500003013': ('structurally explainable; MutuallyExclusive main gating pending', ['M001']),
        '1500003820': ('registration chain explainable; continuous timer contract pending', ['M002']),
        '1500003835': ('dispatch structure explainable; optional owning-main completion pending', ['M003']),
        '1500001103': ('conditional quest-end cleanup explainable; Q005 register lifetime limitation retained', []),
        '1500004302': ('synchronized play/completion protocol explainable; source timing/save/MP limits retained', []),
        '1500004332': ('synchronized skip/completion protocol explainable; source timing/save/MP limits retained', []),
    }
    outcomes = []
    for guid,c in cases.items():
        outcomes.append({'guid':guid,'source':c['source'],'line':c['line'],'sha256':c['sha256'],
                         'classification':statuses[guid][0], 'questions':statuses[guid][1],
                         'documentation':'reference/trigger-mod-walkthroughs.md#'+guid+'--'+{
                             '1500003013':'bt-passive-trading', '1500003820':'shared_pirateextraspawn',
                             '1500003835':'shared_pirateextraspawn', '1500001103':'piratecomebackfleetfix',
                             '1500004302':'campaign-in-coop','1500004332':'campaign-in-coop'}[guid],
                         'scope':'Complete selected definition, relevant includes/own templates/helper references/callers/consumers, native field/default/base/pool audit and scoped evaluator patch; not game/MP verification.'})
    write_json(OUT/'review-outcomes.json', {'date':'2026-10-03', 'cases':outcomes,
                                          'pending_user_clarifications':['M001','M002','M003'],
                                          'mod_source_changes':False, 'new_game_or_mp_tests':False})
    ledger_path = DOC/'reference/review-ledger.json'
    ledger = json.loads(ledger_path.read_text('utf-8'))
    for outcome in outcomes:
        key = 'workspace:'+outcome['source']
        if key not in ledger:
            ledger[key] = {'sha256':outcome['sha256'], 'reviewed_on':'2026-10-03',
                           'status':'selected trigger definitions/integration reviewed; listed runtime questions pending',
                           'documentation':['reference/trigger-mod-walkthroughs.md'],
                           'outcome':'Selected GUIDs and relevant reference chains only; not a whole-file/whole-mod or runtime certification.'}
        # The general and original trigger-topic review statuses remain untouched.
        ledger[key].setdefault('trigger_case_reviews', {})[outcome['guid']] = outcome
    write_json(ledger_path, ledger)
    p = DOC/'reference/coverage.md'
    raw = p.read_bytes()
    raw, count = re.subn(rb'ledger currently contains \d+ source-specific records',
                        b'ledger currently contains '+str(len(ledger)).encode()+b' source-specific records', raw)
    assert count == 1
    p.write_bytes(raw)
    add('reference/coverage.md', '## Six real trigger cases (2026-10-03)\n\n[Six mod walkthroughs](trigger-mod-walkthroughs.md) follow 1500003013, 1500003820, 1500003835, 1500001103, 1500004302 and 1500004332 through their relevant definitions, bundled versions, native contracts and caller/consumer patches. All six source payloads and the selected real ModOps passed [offline checks](validation/mod-trigger-cases/results.json). Integration evidence records 178 source hashes and resolved includes; it does not mark every whole mod reviewed. M001–M003 remain pending Serp clarification (exclusive/main gating, interrupted timer, optional owning main). No runtime sign-off, source changes or new game/MP tests.\n\n', '## Next steps, in order')
    add('reference/discrepancies.md', '## Q006: six-trigger walkthrough questions\n\n**Status: awaiting Serp clarification; no inference accepted as a runtime answer.**\n\n- M001, BT Passive Trading 1500003013: proximity main with MutuallyExclusive children. Do GUID-change actions remain gated by proximity despite the native wording about children being solvable before the main? This is a concrete application of Q005.\n- M002, PirateExtraSpawn 1500003820: does its 3600000 ms nested timer restart or pause when the ship count exceeds three? Source comments report aborting, but current docs do not establish the precise interruption contract.\n- M003, PirateExtraSpawn 1500003835: can IsOptional on the owning main plus its child consume a failed dispatch without Lua and permit a fresh later manual registration? The schema describes parent completion; an owning main has no enclosing SubTrigger parent. Do not equate this with the already-documented optional leaf or silently settle Q005\'s registration lifetime.\n\nFull source positions, expected flows, audit and offline boundaries are in [six mod walkthroughs](trigger-mod-walkthroughs.md) and [case outcomes](triggers/mod-cases/review-outcomes.json). Questions were submitted directly to Serp; unanswered cases remain partial.\n\n', '## Historical and context differences')
    add('gameplay/triggers.md', '\n## Real mod walkthroughs\n\n[Six existing mod trigger walkthroughs](../reference/trigger-mod-walkthroughs.md) trace complete definitions and relevant callers/consumers. They show the single-ship invariant behind a broad GUID filter, positive pirate-state helpers, optional quest cleanup and synchronized movie start/completion. Their exclusive-main, interrupted-timer and optional-owning-main questions remain open; passing offline patches does not resolve them.\n')
    add('reference/trigger-audit.md', '\n## Follow-up: six real mod cases\n\n[Six real walkthroughs](trigger-mod-walkthroughs.md) extend this catalogue-based pass with relevant selected-mod integration and caller/consumer audits. [Case outcomes](triggers/mod-cases/review-outcomes.json) and [offline results](validation/mod-trigger-cases/results.json) distinguish explained source structure from M001–M003 pending user clarification and retained runtime limitations. They do not upgrade the broad workspace extraction to a whole-mod certification.\n')
    p = DOC/'README.md'
    raw = p.read_bytes()
    old = b'and [recipes](gameplay/trigger-recipes.md) |'
    new = b'[recipes](gameplay/trigger-recipes.md) and [real mod walkthroughs](reference/trigger-mod-walkthroughs.md) |'
    if new not in raw:
        assert raw.count(old)==1
        p.write_bytes(raw.replace(old, new, 1))
    print('Recorded six scoped outcomes and three pending questions; existing general review statuses preserved.')

if __name__ == '__main__':
    main()
