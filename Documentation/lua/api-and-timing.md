# Lua access, identifiers and asynchronous changes

## Discovering an API contract

`ts` is the shortcut for `TextSources.TextSourceRoots`. The console's completion and the older `textsourcelist.json` reveal aliases, return types and arguments. Follow a member's ReturnType to the corresponding catalogue class. A textsource alias without arguments can have a getter form; setters/getters with arguments need an actual call. Do not systematically invent `Get`/`Set` forms for every alias.

The catalogue is incomplete and not every listed member is callable in Lua. Vector/list-returning members and `MetaObjects/SessionGameObject` are important examples requiring textembed access in Serp's tests. The supplied native catalogue also contains invalid JSON escapes inside comments; a strict JSON parse failure is a catalogue-format issue, not proof that its API entries are invalid. Preserve the source and record any in-memory repair used for analysis.

API evidence must distinguish: native script usage, a documented successful Serp test, a command catalogue entry, and an untested experiment. Console completion proves a spelling is exposed in that context; it does not establish multiplayer safety.

Sources: [Lua basics](https://github.com/anno-mods/modding-guide/blob/main/Scripting/basics.md), [command documentation](https://github.com/anno-mods/modding-guide/blob/main/Scripting/documentation.md), local notes and [runtime contracts](../reference/runtime-contracts.json).

## Identifiers are not interchangeable

| Identifier | Meaning |
| --- | --- |
| Asset GUID | Definition of a building, item, trigger, quest, pool or other asset. |
| Object ID / OID | Particular runtime object instance; use the verified conversion/accessor. |
| Participant ID | Participant enum position for relevant Lua APIs; not that participant's profile asset GUID. |
| Peer index | One client slot; multiple peers can share a participant in Coop. |
| Session GUID | Session definition. |
| Area ID | Runtime area/island context for APIs that expect it; not an island-file GUID. |
| Quest instance ID | A running/previous quest instance, not the quest definition GUID. |
| Dataset Id | Serialized enum ID, which can differ from the zero-based list position used by a Lua call. |
| Property ID | Engine property identifier; not a GUID or arbitrary order of properties in XML. |

Validate all conversions at their call boundary. Native `visitallmarkets.lua` contains an old hardcoded market property number, while current catalogues/helpers can have different IDs. A native sample is evidence of API usage, not a promise that every old constant is current.

## Object facades and userdata

`ts.Selection.Object` is selection-dependent. `session` points at the executing client's active session. Neither is a saved global object index. Coop can make participant-level selection include another peer's objects, so recheck the intended OID, owner, GUID and session before acting.

`session.getSelectedFactory()` returns selected userdata even when the object is not a factory, according to Serp's tests; for multiple selections its chosen object is not a reliable substitute for processing the explicit selection list. `session.getObjectGroupByProperty(...)` is reported to enumerate the local human's objects in the active session, not every participant and session.

`userdata:getOID()` returns a structured identifier in the observed API. Its `ObjectID` field alone is not the complete OID expected by the textsource accessor. The early guide extracts an OID from `userdata:getName()`. Current shared helpers have dedicated conversions; use and document their exact version instead of carrying the old string parser into a new mod without inspection.

Serp observed that an old `ts.Objects.GetObject(OID)` facade can produce incorrect subsequent values after a getter. Reacquire it before independent reads as the documented workaround. `ts.GetGameObject(OID)` provides broader cross-session reads in later notes, but support is member-specific and writes can fail to synchronize across sessions. Do not generalize a successful Name read to ItemContainer mutation.

Persist OIDs or your own data, not userdata or mutable textsource facades. Reacquire and validate the object after yielding, changing sessions, reloading a save, destroying an object or changing its GUID.

## Textembed bridge

`game.TextSourceManager.setDebugTextSource(expression)` evaluates a textsource expression but does not return the result directly to Lua in Serp's tests. Light's established workaround evaluates the desired expression and writes its result into a reserved Nameable helper, then reads that helper's name.

This is an integration with real resources, reserved helper participants and shared state. Do not use an arbitrary player's ship as a scratch register or independently claim Light's helper participants. Inputs must be formatted and escaped with the established helper functions. Strings containing quotes, backslashes, brackets or parentheses can break the composed expression.

The bridge permits operations through `MetaObjects SessionGameObject(OID)` across sessions, which is more reliable for the documented Nameable case than direct `ts.GetGameObject(...).Nameable.SetName(...)`. The bridge's API and locking rules belong in the shared-helper reference; not every bridged command becomes synchronized merely because it uses a textembed.

The early textembed guide says calls are unavailable. Native/user examples with argument-bearing textsource expressions and later helper implementations supersede that broad wording. Lua function calls and textsource commands remain different languages.

## Read after write

Do not treat a write followed by a getter in the same Lua invocation as proof of the new game state. Some commands submit work for a later tick. Yielding once is the guide's example, not a universal completion barrier.

A general scheduling pattern is:

```lua
-- Generic helper: submit/read/isDone are supplied by an audited feature.
local function waitForObservedChange(submit, read, isDone, maxYields)
    submit()
    for attempt = 1, maxYields do
        coroutine.yield()
        local value = read()
        if isDone(value) then
            return true, value
        end
    end
    return false, "change was not observed within the configured bound"
end
```

Run this inside a managed coroutine and define what success means for the particular operation. The bound is a caller-supplied feature decision, not a universal number of ticks. A local observed result does not establish that all peers have observed it at the same tick. Do not use this pattern alone to coordinate an unsynchronized command.

Serp's Nameable tests are particularly important: a local SetName can be immediately readable on that client, take roughly 3-10 ticks to reach other clients, and temporarily revert as queued changes arrive. A direct local read can therefore falsely certify cross-peer completion. The recorded range is an observation, not a guaranteed maximum.

## Useful command families and recorded limits

| Family | Recorded usage and limit |
| --- | --- |
| Profile counters | `ts.Participants.GetParticipant(pid).ProfileCounter.Stats.GetCounter(valueType, counter, context, scope, scopeContext)`. Numeric enums use zero-based dataset positions. ScopeContext can be a session GUID or Area ID. Direct PlayerCounterContextPool counting is reported unsupported. |
| Condition amount | `ts.Conditions.GetCurrentConditionAmount(triggerGuid)` is the documented workaround for an XML counter condition whose pool cannot be counted directly. Audit the trigger, owner and returned fields. |
| Unlocks | GetIsUnlocked reads state; SetUnlockNet/SetRelockNet submit network-aware changes. The non-Net unlock call is reported to desynchronize when invoked asymmetrically. |
| Trigger/quest invocation | RegisterTriggerForCurrentParticipant and StartQuestForCurrentPlayerNet act for the invoking human. ActionExecuteScript invokes the script on every client, which can multiply calls. Quest startup is reported to use the player's current session rather than simply QuestSessionDependencies. |
| Trader ForceBuild | The documented successful access is through SessionParticipants, not Participants. It follows trader/pirate fleet definitions and is reported limited to one built ship per tick. Serp considers direct ActionExecuteScript invocation practical in MP **if all clients execute in exactly the same tick**; see [conditional MP contract](../multiplayer/synchronization.md#command-specific-behavior). This is not proof for arbitrary waits or differing sessions. |
| Object upgrades | userdata addUpgrade/removeUpgrade persist buffs through saves/session transitions, but are reported unsynchronized. AllowStacking=0 does not remove repeated hidden applications; multiple applications need matching removals. |
| Skin changes | Serp reports SetChangeSkin synchronized in the tested setup. Do not infer this for every object mutation. |
| Sound | game.playSound is reported local to the peer; AudioText playback can also create notification UI. |
| Weather | Native scenario scripts use ForcePreset. Dataset position and client/session context matter. Enabling a scenario's Season UI does not establish that its entire feature is active in sandbox. |
| Ownership | Changing a kontor's owner can leave AI logic and storage UI active/broken. The notebook's upgrade workaround is a test observation, not a safe general island-transfer recipe. |

The table preserves existing observations; a task using one of these families still needs its full feature-specific vanilla/helper audit. Additional API catalogues and command-specific chapters remain subject to the [coverage register](../reference/coverage.md).
