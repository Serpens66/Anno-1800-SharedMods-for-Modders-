"""Targeted byte-preserving additions to existing UTF-8/CRLF documentation."""
from pathlib import Path
import json

DOC = Path(__file__).resolve().parents[1]

def encoded(text):
    return text.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8')

def add(path, text, anchor=None):
    p = DOC/path
    raw = p.read_bytes()
    raw.decode('utf-8')
    assert raw.count(b'\n') == raw.count(b'\r\n'), 'Preserve non-CRLF source deliberately: '+str(p)
    new = encoded(text)
    if new in raw:
        return
    if anchor:
        key = encoded(anchor)
        assert raw.count(key) == 1, (path, anchor)
        raw = raw.replace(key, new+key, 1)
    else:
        raw += new
    p.write_bytes(raw)

def main():
    add('README.md', '| Build gameplay triggers, combine subtriggers and handle saved state | [Trigger design](gameplay/triggers.md), [condition selection](gameplay/trigger-conditions.md), [complete fields](gameplay/trigger-condition-reference.md), [datasets](gameplay/trigger-datasets.md) and [recipes](gameplay/trigger-recipes.md) |\n',
        '| Understand Lua entry points and lifetime |')
    add('README.md', '\n[Trigger audit](reference/trigger-audit.md) records the topic-specific review and its limits. [Native trigger contracts](reference/triggers/vanilla.json), [workspace trigger evidence](reference/triggers/workspace.json) and [source-comment destinations](reference/triggers/prose-evidence.md) support the trigger chapters; extraction is not complete whole-mod integration or runtime certification.\n')
    add('reference/coverage.md', '## Trigger-topic addition (2026-10-03)\n\n- Added design/lifecycle, condition selection, native field/dataset lookup and complete recipe chapters; see [trigger audit](trigger-audit.md).\n- Native lookup covers 91 direct-Condition templates, related objectives/selectors, 141 Condition-prefixed property definitions plus supporting contracts. Exact revision counts and hashes are in [extraction summary](triggers/extraction-summary.json) and [native contracts](triggers/vanilla.json).\n- Current inventory search reached 3,885 source rows / 879 distinct byte groups with trigger-related text, including both notebooks. The [prose evidence register](triggers/prose-evidence.md) maps 1,354 distinct trigger-relevant quotations to topic guidance; duplicates and non-identical bundles remain distinguishable. These are discovery/topic-evidence counts, not complete integration-review counts.\n- Eight complete documentation XML recipes were checked against native structures and the installed XML evaluator; see [results](validation/triggers/results.json). No game/MP execution, independent new-chat agent test or dependency-loading test was performed.\n- Q005 records unresolved IsOptional-depth, MutuallyExclusive-gating and register/reset-context boundaries. Existing uncertain condition/action tests remain qualified beside the relevant guidance.\n- Existing whole-source review statuses were retained; new source records expressly describe trigger-topic evidence only. Remaining helper/action/quest/system integration work below is not silently marked complete.\n\n', '## Next steps, in order')
    p = DOC/'reference/coverage.md'
    raw = p.read_bytes()
    count = len(json.loads((DOC/'reference/review-ledger.json').read_text('utf-8')))
    # Original prose used 334; replace that exact fact without re-encoding the rest.
    raw = raw.replace(b'334 source-specific records', str(count).encode()+b' source-specific records (including narrowly scoped trigger-topic records)')
    p.write_bytes(raw)
    add('reference/discrepancies.md', '## Q005: trigger composition and registration boundaries\n\n**Status: unresolved runtime details; documentation uses narrow source-supported patterns. No new game test.**\n\n- HowTo.xml:854-856 first says every optional descendant must carry IsOptional, then reports a test where unmarked lower descendants did not block completion. Workspace nested optional examples mark multiple levels. Neither establishes the minimal universally required marking. Use explicit optional levels where the whole branch must be optional and keep the contradictory test visible.\n- The native Condition/SubConditionCompletionOrder description says MutuallyExclusive subconditions are solvable before the main condition. HowTo.xml:830 describes broad main-condition gating without resolving this exception. Do not extend that gating claim to every exclusive tree. The complete-branch/first-eligible-branch observations and priority remain separately documented.\n- Native ActionRegisterTrigger says an existing trigger resets to its origin state. Popup helper comments say registration does nothing when already registered, while notebook/Lua tests report duplicate registrations, uncertain completed-trigger restart and failed circular re-registration. Call site, XML versus Lua, participant and running/completed state differ. Treat registration as context-sensitive; prefer the reviewed embedded ResetTrigger pattern for ordinary repetition and preserve defeated-participant caveats.\n\nExact source hashes, original wording and destinations: [trigger audit](trigger-audit.md), [source evidence](triggers/prose-evidence.md), [native contracts](triggers/vanilla.json). These findings do not supersede explicit earlier test conditions or invent an engine-code resolution.\n\n', '## Historical and context differences')
    additions = {
        'lua/execution-and-lifecycle.md': '\n## Gameplay trigger design\n\nUse [trigger design](../gameplay/triggers.md) for registration, ResetTrigger, saved instances, mod-removal guards and the difference between state and events. [Condition selection](../gameplay/trigger-conditions.md) preserves the inconsistent MetaGameLoaded/ProfileLoaded tests and session/readiness limits; [recipes](../gameplay/trigger-recipes.md) provide complete XML structures. A startup trigger does not establish an every-save-load callback.\n',
        'lua/shared-light.md': '\n## Trigger-side contract\n\n[Trigger design](../gameplay/triggers.md#savegames-removal-and-extension-points) distinguishes the always-locked mod-presence guard from Light\'s initially-unlocked lock-to-start FeatureUnlock. Keep the existing availability, cooldown and peer execution contract when building a new consumer. [Condition pitfalls](../gameplay/trigger-conditions.md) also documents counter/pool and context handoff limits.\n',
        'multiplayer/synchronization.md': '\n## Trigger composition and local events\n\n[Trigger design](../gameplay/triggers.md) separates participant selection from peer multiplicity and explains saved subcondition completion. [Condition selection](../gameplay/trigger-conditions.md#events-ui-and-quests) preserves GUID-specific UI/movie/notification observations: even firing a saved trigger without consequential actions can diverge client state. Native declared pool support is not MP-safety evidence. See the complete source register in [trigger audit](../reference/trigger-audit.md).\n',
        'reference/personal-test-evidence.md': '\n## Trigger-topic transfer\n\nThe observations above now have detailed guidance in [trigger design](../gameplay/triggers.md), [condition selection](../gameplay/trigger-conditions.md) and [recipes](../gameplay/trigger-recipes.md). [Native fields](../gameplay/trigger-condition-reference.md) and [datasets](../gameplay/trigger-datasets.md) support condition discovery. Original corrections and unsuccessful/WIP examples are traceable through [source evidence](triggers/prose-evidence.md); Q005 keeps unresolved runtime details visible. This does not mark unrelated gameplay-topic transfer complete.\n',
        'recipes/basic-workflows.md': '\n## Complex trigger workflows\n\nThe startup recipe above is deliberately small. For nested gates, Linear event chains, MutuallyExclusive complete-branch priority, optional actions, reset pulses and participant/session gating, read [trigger design](../gameplay/triggers.md), [condition selection](../gameplay/trigger-conditions.md) and the [complete trigger recipes](../gameplay/trigger-recipes.md). Their offline validation proves structure/patching only; saved-state and Coop design still require the documented contracts.\n',
        'reference/offline-validation.md': '\n## Trigger documentation examples\n\n[Trigger results](validation/triggers/results.json) record eight complete recipe patches using the installed 1800 evaluator, complete preservation of the exact native anchor 130248, native template/property/enum checks, private fixture GUID bindings, tree placement and rejection of three invalid contracts. Reproduce with `Documentation/tools/validate_triggers.py` after running the extraction/reference/example generators documented in [trigger audit](trigger-audit.md). No conditions/actions, dependency loader, game-save lifecycle or multiplayer session were executed.\n',
    }
    for path, text in additions.items():
        add(path, text)
    print('Linked trigger chapters and updated scoped coverage/discrepancy records; original encodings and bytes outside additions retained.')

if __name__ == '__main__':
    main()
