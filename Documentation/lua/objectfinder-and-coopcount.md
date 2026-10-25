# ObjectFinder and CoopCount: actual WIP interfaces

## Source and evidence boundary

This chapter reviews the complete `objectfinder.lua` (1086 lines) and `coopcount.lua` in `Anno-1800-Mods/WorkInProgress-Mods/shared_LuaMedium/data/scripts_serp/` [GitHub](https://github.com/Serpens66/Anno-1800-Mods/tree/88821b04ee972424667178d35a5080a753a853d0/WorkInProgress-Mods/shared_LuaMedium/data/scripts_serp). It describes their implementation and the tests written in their comments, not a newly validated game API. Use [Medium and Ultra](shared-medium-and-ultra.md), [LuaLight](shared-light.md), and the [multiplayer rules](../multiplayer/synchronization.md) alongside it. XML spawning, participant and trigger integration still require their feature-specific audits.

Both scripts use `g_LuaScriptBlockers[ModID]`, which must already exist. ObjectFinder starts Light if needed; its cache initialization waits for Medium. Calling its exported methods before `g_LTM_Serp.Shared_Cache[ModID]` exists can fail even after `g_ObjectFinderSerp` becomes non-nil. Initialization and readiness are different states. Game-leave cleanup clears `g_ObjectFinderSerp` and its native session callbacks; the blocker is released after a 1000-unit helper delay.

## ObjectFinder exports

| Export | Arguments and result | Scope and restrictions |
| --- | --- | --- |
| `GetCurrentSessionObjectsFromLocaleByProperty` | `Property, ...`; delegates to Light | Local participant, local active session; not a global object enumeration. |
| `IsLoadedSessionByID` | `SessionID, dontusecache`; session GUID or nil | Searches object indices 1–10 in water area for the neutral participant. Excludes fake helper session 1500005538. A bounded heuristic, not native authoritative session enumeration. |
| `GetLoadedSessions` | `FromSessionID, ToSessionID, dontusecache`; map `[SessionID]=SessionGuid` | Defaults 1–20; cached data may survive a session unload unless explicitly bypassed. |
| `GetAllLoadedSessionsParticipants` | `PIDs, sSessionGuid, sSessionID`; map `[SessionID][PID]=record` | Searches indices 1–100 or copies the cache. `PIDs` is a dense array; `sSessionGuid="First"` returns the first matching session encountered. The cache copy can contain participants beyond the requested PIDs. |
| `GetFirst100LoadedSessionsGameObjects` | `sSessionGuid, sSessionID`; map `[SessionID][OID]=record` | Diagnostic scan of indices 1–100; same `"First"` convention. |
| `GetAnyValidKontorOIDFrom` | `PID`; OID or nil | Searches cached trading posts and rechecks GUID/owner; `pairs` order gives no deterministic choice among several valid posts. |
| `GetHighestObIDsLocalPlayerCurrentSessionByProperty` | `Property`; no explicit return | Updates low/high indices from the local property group. Its delayed high-index reset has a scope defect described below. |
| `GetAnyObjectsFromAnyone` | one options table; map `[OID]=record` | Expensive bounded search; cached foreign islands, editor-object limitations and early-exit behavior matter. |
| `AreasCurrentSessionLooper` | `executionfunc`; no explicit return | Current session, settled island areas; callback receives ten arguments below. |
| `SpawnMaxObjIdHelpers` | `kind`; boolean | `kind=="Area"` selects island helper; any other value selects walkable helper. Relocks the spawn unlock if currently unlocked; true means requested, not that every helper has appeared. |
| `DoesMaxObjIdHelperExists` | `AreaID, AreaOwner, MaxObjIdWalkableHelperGuid, MaxObjIdAreaHelperGuid`; boolean | Uses profile counters for owner on islands or humans 0–3 on water. Optional GUID overrides replace defaults. |
| `_OnSessionLoaded`, `_OnIslandSettledSessionEnter` | `PID` | Internal event adapters; guard against the local participant ID and start cache-update coroutines. |

Constants: `PID_Neutral=8`, `l_MaxSessionID=20`, `l_MaxIslandID=80`, `MaxObjIdAreaHelper={Guid=1500005548,Unlock=1500005549}`, `MaxObjIdWalkableHelper={Guid=1500005550,Unlock=1500005552}`. These bounds and reserved GUIDs belong to this helper implementation, not universal vanilla maxima. Do not reuse them for unrelated assets.

Participant/diagnostic records contain `OID, PID, GUID, SessionGuid, ObjectID, AreaID, SessionID`. Search results instead contain `GUID, ParticipantID, userdata, SessionGuid, SessionID, IslandID, AreaIndex, ObjectID, AreaOwner, Kontor_OID`, keyed by OID. Do not confuse `PID` with `ParticipantID` or expect a result's `AreaID` field; reconstruct it from the supplied components when necessary.

## Search configuration and callback contract

`GetAnyObjectsFromAnyone(myargs)` recognizes `ObjectFilter`, `SessionFilter`, `FromSessionID`, `ToSessionID`, `FromIslandID`, `ToIslandID`, `FromAreaIndex`, `ToAreaIndex`, `FromObjectID`, `ToObjectID`, `withyield`, and `waitforhelper`.

Defaults are sessions 1–20, islands 0–80, area indices 0–1 and object indices starting at 1. Island 0 requires area index 0; nonzero islands require nonzero area indices. Shared islands with index 2 require an explicit expanded range. The active code's default upper object index is **1,000,000**, despite an earlier comment saying 100,000. With a detected maximum-index helper it becomes **100,000,000**, stopping when that helper is encountered. Explicit bounds override these choices; otherwise cached low/high indices can narrow the scan.

`SessionFilter(SessionID, SessionGuid)` must return a truthy value to search a session. The commented/example filter which only returns false for other sessions implicitly returns nil for the wanted session, so it rejects every session. Use an explicit boolean expression.

`ObjectFilter(OID, GUID, userdata, SessionGuid, ParticipantID, AreaID, SessionID, IslandID, AreaIndex, ObjectID, AreaOwner, Kontor_OID)` may return a table:

- `addthis=true`: add this valid object to the result.
- `done=true`: stop the search after processing this object.
- `next_AreaID=true`: leave the current object's area loop.
- `next_SessionID=true`: intended to leave the current session, but the actual outer loop also breaks. In this revision it terminates the whole search, like `done`, rather than advancing to the next session.

A nil/non-table result does not add anything. The complex illustrative `my_ObjectFilter` computes `adden` but never returns it in its matching branch; it is an unfinished example. `AreaOwner` and object `ParticipantID` can differ, especially in mods. The callback's userdata is only requested when the scanned session equals the local active session and may still be nil. Reacquire native facade values as explained in [API and timing](api-and-timing.md).

`AreasCurrentSessionLooper` calls `executionfunc(SessionGuid, ParticipantID, AreaID, SessionID, IslandID, AreaIndex, AreaOwner, Kontor_OID, GUID, OID)`. A truthy callback result requests an early stop. It obtains an area callback through the first valid scanned object, not through a native list of every island. Unsettled/invalid areas are not equivalent to a missing result for a settled island.

## Cache, performance and side effects

Cache namespace: `g_LTM_Serp.Shared_Cache[ModID]`, initially `{ObIDs={}, LoadedSessionsParticipants={}, LoadedSessions={}, Kontor_OIDs={}, Loaded=nil, Changed=nil, SyncChanged=nil}`. Methods mutate these maps and sometimes set `Changed`. This is not inherently persistent or synchronized; Ultra's saving/synchronization limitations still apply.

For a foreign session, island searches need previously cached `AreaOwner`, `AreaOwnerName` and trading-post information. Missing foreign-area metadata causes the area-index loop to break; the function does not guarantee that every foreign island is searched. Current-session area information refreshes the trading-post cache. A trading-post index is used as the lower bound under the author's assumption that it is the first building; that assumption can omit lower-index exceptional objects. A preplaced editor trading post which cannot be resolved by the constructed non-editor OID marks an area invalid as `"EditorObject"`.

All constructed scan OIDs have `EditorFlag=0, EditorChunkID=0`. Consequently this algorithm does not enumerate preplaced editor objects even where Light can encode their IDs through strings/big integers. Ships receive new object IDs on session transfer according to the author's comments; high bounds and saved OIDs cannot be assumed permanently current.

With `withyield=true`, the search yields per area and every 10,000 tested object indices. It must run inside a coroutine. `waitforhelper=true` adds an unbounded wait until helper counters report availability; it also needs a coroutine even when `withyield` is false. A missing helper, unloaded session, changed XML setup or insufficient progress can stall it indefinitely. Choose explicit narrow bounds and a terminating filter; an unconstrained scan can freeze the game or take very long. No new performance test was performed.

`GetHighestObIDsLocalPlayerCurrentSessionByProperty` declares `CacheObIDsSessionID` inside its per-object loop, then references that name from a later delayed callback outside its scope. In ordinary Lua lexical scope that callback reads a global nil, so the intended reset fails. It also cannot reset each encountered session through that inaccessible local. This is a source defect, not evidence that high-index expiry works.

Several methods assign `OID`, `CheckingSessionGuid` or `done` without `local`, polluting globals. Do not rely on those names staying private between threads. `pairs` choices and object discovery order are not a peer-election mechanism.

## Existing author observations and inactive experiments

The opening comments record facade reuse problems, delayed cross-peer writes, company names being local, cross-session Nameable access through text embeds, and competing rename commands. A two-player rename test ended with the client's value; the author explicitly did not establish a general host/peer priority rule. Local `SetName` can be read immediately while replication arrives later and can temporarily overwrite successive local writes. A local read-back is therefore not a remote acknowledgement.

The comments also describe long or irregular yield delays in the statistics menu at slowed game speed, continued old threads after loading another game, and loading-screen crashes observed with several different mod combinations, eventually including no mods. They do **not** isolate ObjectFinder as the cause. Preserve that uncertainty; no crash was reproduced in this documentation task.

`_RegisterEvents` is implemented but its call is commented out. Active integration uses XML-trigger adapters. The author's event experiments include protected calls and still report crashes; do not present the inactive registration function as the current startup path. Cache refresh requests Ultra synchronization only when applicable cached trading-post information changed; this remains subject to the save receiver defect in the [Ultra chapter](shared-medium-and-ultra.md).

## CoopCount interface and actual algorithm

Global `g_CoopCountResSerp` exports `MakeNewCount()` and `ContinueWithTotalChanceCoop(totalchance)`, plus `LocalCount`, `TotalCount`, `CountPerPID`, `IsPIDActive`, `Finished`. Initialization sets counts to zero and `Finished=nil`; use values only after **`Finished==true`**, not after the table merely exists. `MakeNewCount` queues the coroutine under `g_CoopCountResSerp_MakeNewCount` through Medium's local queue.

In multiplayer every executing client reads humans 0–3's global `MetaStorage` profile counter for resource **1500004521**, submits one local `MetaStorage.AddAmount(...,1)`, waits 2000 helper time units, and derives each participant's count from the difference. This intentionally exploits multiple peer executions contributing to a synchronized resource. It requires coordinated execution on all clients and no unrelated writer to the reserved resource. The delay is an author-chosen heuristic, not an acknowledgement protocol. Late arrivals/leavers or replication timing can distort differences. A new game test is outside this task.

For its own participant, if the new resource amount exceeds 99990 it subtracts 100000, then waits 1000 units. In Coop, multiple peers can each submit this reset; resulting saturation and future baselines need runtime verification. In single player it directly sets the local human's count to one, all others to zero and total to one.

**Repeated multiplayer counts have an implementation defect:** `TotalCount` is incremented by every newly observed count, without resetting it at the beginning of `t_DoMakeNewCount`. `CountPerPID` is replaced but `TotalCount` accumulates across calls. Consumers must not assume the second recount reports the current total correctly. The game-leave callback clears `g_SaveLuaStuff_Serp` rather than `g_CoopCountResSerp`; this appears to be a copied cleanup error and can affect Ultra while retaining the CoopCount global. The script releases its blocker after 1000 units, so subsequent script invocations can initialize a new table.

`ContinueWithTotalChanceCoop` returns false for zero, true for values at least one, nil when not ready, otherwise compares local `math.random()` to `1-(1-totalchance)^(1/LocalCount)`. This formula models at least one success across **independent** executions. It does not synchronize random streams or guarantee exactly one execution; two or more peers may succeed. Negative probabilities and zero/invalid local counts are not validated. Do not use it to select the sole writer for an operation that must run exactly once.

## Validation boundary

The source-level scope, accumulation and filter-return findings follow Lua syntax/control flow. They require no guessed vanilla behavior. Asset placement, helper lifetime, counter replication, multiplayer safety and current game compatibility are not established by syntax checking. Before deploying a consumer, audit the matching included XML, active dependency versions and native contracts; preserve the WIP distinction.
