# LuaMedium and LuaUltra: reviewed interfaces and WIP boundaries

Sources are under `Anno-1800-Mods/WorkInProgress-Mods/shared_LuaMedium/` [GitHub](https://github.com/Serpens66/Anno-1800-Mods/tree/88821b04ee972424667178d35a5080a753a853d0/WorkInProgress-Mods/shared_LuaMedium) and `shared_LuaUltra/`. Their location, TODOs and metadata issues matter: these are development implementations. An interface being present does not certify that all its protocols work. ObjectFinder, peer detection and XML integration require their separate complete reviews before publishing a ready-to-use full integration recipe.

## Versions, dependencies and startup

Medium: **shared_LuaTools_Medium_Serp 1.002**, depends on Light, **shared_NatureParticipant_Serp**, **shared_Matchers_Serp**, **ObjectDummies_Serp**; deprecates the older UltimateHelpers, EventOnGameLoaded and LuaCoopCounterRes IDs.

Ultra: **shared_LuaTools_Ultra_Serp 1.00**, depends on Light and Medium and loads after Medium. Deprecates UltimateHelpers and LuaPeers. Its metadata describes a **5–15 second initialization** on every multiplayer load, with a notification. This is a documented approximate cost, not a bounded completion guarantee.

Both startup scripts require `g_LuaScriptBlockers` to exist. The EventOnGameLoaded integration starts them after its own save-load initialization, via unlock 1500004636 as described in comments. Do not call either startup script in a clean Lua environment before that prerequisite.

Medium loads Light if necessary, then ObjectFinder and CoopCount. It seeds the process-wide math.random generator with os.time, which is unsuitable as a cross-peer deterministic seed. Global **g_LTM_Serp** contains the exports below. It registers a game-leave callback that clears the global, then unblocks its startup name after a one-second local wait.

Ultra loads Light if needed, then `check_peers.lua` and `savetablestuff.lua`. Global **g_LTU_Serp** exposes `PeersInfo=g_PeersInfo_Serp` and `SaveLuaStuff=g_SaveLuaStuff_Serp`; its game-leave callback clears the wrapper global. Startup alone does not mean peer identification or saved cache loading has completed.

Both metadata files report crash/corrupted-save problems with `mods.reload()`. Medium's comments include contradictory reproductions and finally suspect Medium or its combination with other scripts; a trivial coroutine alone did not reproduce it. The cause is unproven. Do not prescribe hot reload as a safe validation procedure for these WIP helpers. No such test was run here.

## Medium's implemented public table

| Function / field | Contract from inspected implementation |
| --- | --- |
| ObjectFinder | Alias to g_ObjectFinderSerp |
| CoopCountRes | Alias to g_CoopCountResSerp |
| CallGlobalFnBlocked(fn_name,blocknameadd,blocktime,...) | Resolves a global function name, local cooldown; default 1000ms; name includes function plus caller suffix |
| CallFnBlocked(fn,blocknameadd,blocktime,...) | Local cooldown keyed only by caller suffix; default 1000ms; can collide if callers reuse suffix |
| AddToQueue(ID,fn,...) | Per-ID FIFO of protected coroutine tasks; errors logged; local queue, not a multiplayer mutex |
| IsThirdPartyTrader(PID,PID_OID) | true/false/nil; locates a session participant, tests Trader through HasProperty, falls back to nonempty Trader/RerollCosts |
| ContinueCoopCalled() | `IsFirst`, `AllCoop`, or false; **not a Boolean** |
| t_ChangeOwnerOIDToPID(OID,To_PID,ignoreowner,notifyonfail,forbidpiratenewowner,CallerModID) | Coroutine operation using Sellable BuyNet and optional intermediate owner; success Boolean and event callback |
| EventOnObjectOwnerChanged | Callback map keyed by unique ModID |
| SimpleExecuteForEveryone(PID,funcname,...) | Local participant gate; direct singleplayer call or queued Nameable transport to all clients |
| _DoExectionForEveryone() | Internal reader/dispatcher; spelling Exection is the actual API |
| NatureParticipantPID | 158, mod participant asset1500004528, intended universal trade-rights intermediary |
| Shared_Cache | ModID-keyed map; process-local until an audited persistence mechanism saves it |

`ContinueCoopCalled()` returns `IsFirst` when the peer helper elects the executing peer, false otherwise. Without usable Ultra election it returns `AllCoop`; if CoopCount reports local count one it changes that to `IsFirst`. A caller using `if ContinueCoopCalled() then` also executes for **AllCoop**. Require `=="IsFirst"` for a once-only operation, and establish readiness first. The implementation checks some Finished fields for non-nil rather than strictly true, so false can still enter a branch; inspect the actual readiness protocol.

Blocker functions protect only the executing client's repeated calls. Queue tasks may yield, but the queue does not serialize different clients. A task error does not persist progress across save/load. Varargs packed into ordinary tables do not preserve trailing nils.

## Ownership-transfer protocol

The function requires a Sellable object, valid GUID/OID, suitable trade rights or the Nature intermediary, and valid trading-station OIDs when crediting a different human. Default recipient is the local participant; default owner validation rejects an object owned by somebody else unless ignoreowner is set. Influence product1010190 is deliberately excluded from compensation.

Its advertised multiplayer advantage comes from BuyNet, not from making userdata changeOwner synchronized. Human buy costs are credited before the sale; former human-owner prices are compensated afterward, with local waits. Multiple Coop submissions can therefore duplicate financial compensation even if the ownership change itself does not repeat. **One submitting peer is a prerequisite**, not provided by the function itself.

The normal branch uses Walking DebugStop around the transfer, except for third-party traders whose leave-map command must remain. The comments report that not all existing ship tasks/routes are reliably canceled and that a trader purchase can make the ship leave the map. It also removes the NOSELL marker from the object name.

For supported vanilla ships given to PID17/18 pirates, the special branch buys through a scenario helper then registers 1500005617/1500005618; corresponding XML converts ship GUIDs and ownership. `_supportedShipsOwnerToPirate` covers player and sale versions of schooner/gunboat/frigate/ship-of-the-line-type mappings recorded in code; new mappings require matching XML changes, not just an added Lua entry. Comments disagree on the helper identity: the header says GUID100132/PID118, but the active branch reads `PIDs.Scenario3_Archie.PID`, which Light maps to **GUID103131/PID138**. Treat the active lookup as the implementation, and audit the matching XML before claiming successful integration.

The callback receives `success,Local_PID,Owner,GUID,OID,To_PID,ignoreowner,notifyonfail,forbidpiratenewowner,with_middleman,CallerModID`. Success is set after commands are submitted; it is not an independently checked final-owner acknowledgment. Failure notifications are partly TODOs and one branch references optional Sellable notification1500005611.

## Medium's all-client dispatch

SimpleExecuteForEveryone uses PID139/asset4387 **Nameable** in the first located loaded session. It writes a hex table `{funcname=...,args=...}`, waits 3000ms, relocks **1500005607**, then waits another1500ms before releasing its local queue. Every client executes the internal reader through the XML script entry point.

The contract assumes one initiating participant, identical arguments among any initiating Coop peers, compatible first-session choice and serializable data. Independent participants can overwrite the shared channel. The helpers do not restore the original name because each write is delayed. Fixed waits are observations, not a network acknowledgment. Use it only within its reviewed integration limits; it is not a general concurrent RPC service.

## Ultra save interface, completely inspected save script

`savetablestuff.lua` exposes **g_SaveLuaStuff_Serp**:

| Function / field | Behavior |
| --- | --- |
| t_SyncSharedCacheToEveryone(sModID,waitforfinish,skip_equalcheck) | Coroutine; waits for Medium and CoopFinished==true; broadcasts whole cache or one key through peer dispatcher |
| SyncAndSaveSharedCache() | Starts asynchronous save if not already saving; returns true for started, false for busy |
| t_LoadSharedCache() | Coroutine; waits for peers/ObjectFinder/cache readiness, reads helper name and merges saved data with current cache |
| LoadingDone | True after loading attempt, including an unsuccessful decode; not proof that data was recovered |
| PIDToSaveData | PID130 / asset101523, Scenario3_Queen |
| _CurrentlySaving | Internal local operation flag |
| _ExecutingSyncSharedCache(sModID,OtherCache,skip_equalcheck) | Internal merge receiver; defect below |

Persistence uses the **Nameable of a session participant**, not CompanyName. The first active peer writes TableToHex(Shared_Cache), followed by a five-second wait. SyncAndSave calls a peer synchronization operation then waits six seconds; its comment admits that dispatch can take from four seconds to an unbounded time and assumes later saves will catch up. Lua globals and in-progress saves do not become save-persistent just because this function returned true.

Loading distinguishes the default name via text11156, decodes with pcall, then calls MergeMapsDeep(saved,current), so current values override saved non-table values. MergeMapsDeep rejects type changes and has no deletion/tombstone protocol. Do not expect removal of a key on one peer to remove it from all peers or future saved merges.

**Implementation defect:** `_ExecutingSyncSharedCache` assigns the merged table to a local variable `Cache`. It never writes it back to `g_LTM_Serp.Shared_Cache` or `Shared_Cache[sModID]`; MergeMapsDeep returns a new table. Consequently this receiver does not update the shared cache as its name/comment promise. Documented use of this WIP interface cannot establish reliable cross-peer cache synchronization without addressing this defect in a separately authorized mod change.

The serialization limits in [LuaLight](shared-light.md) apply. Use unique ModID keys, plain serializable data, explicit migration/version fields, and OIDs rather than userdata/facades. Peer election/detection and the XML save-event integration remain necessary contracts, not optional details.

## Ultra peer implementation: full source review

Both `check_peers.lua` (591 lines) and `h/peer_tricks.lua` [GitHub](https://github.com/Serpens66/Anno-1800-Mods/blob/88821b04ee972424667178d35a5080a753a853d0/WorkInProgress-Mods/shared_LuaUltra/data/scripts_serp/h/peer_tricks.lua) (366 lines) were read completely, together with their small island-settled/save-tick/peer0 entry scripts. **The following describes the implemented/intended protocol and its defects, not a currently certified working multiplayer API.** Complete helper-session XML and native consumer audits remain outstanding.

The public object is **g_PeersInfo_Serp**, exposed as `g_LTU_Serp.PeersInfo`. Each startup recreates it. PID is the local participant; PeerInt and Username initially nil. CoopFinished is intended to certify local-team identity/election; FullFinished also covers all-team active/inactive maps. Merely having the table is insufficient.

| Public member | Implemented meaning |
| --- | --- |
| GetCoopCount() | Number of entries in ActiveCoopPeers |
| AmIFirstActiveCoopPeer() | Compares the first pairs iteration entry with PeerInt; no numeric sorting |
| IsAnyActiveCoopInSession(sessionGUID) | First matching local-team peer via its active-session getter, else false |
| AmIFirstActiveCoopPeerInSession(sessionGUID) | Whether preceding result equals local PeerInt |
| AmIFirstActivePeer() | Prioritizes participant0, then1/2/3 if earlier teams have no active peers; uses CoopCount; may return string `error` before readiness |
| IsAnyActiveInSession(sessionGUID), AmIFirstActivePeerInSession(sessionGUID) | Equivalent lookup/election using ActivePeers |
| t_ExecuteFnWithArgsForPeers(funcname,waittime,returnafterfinish,ForPeers,...) | Sends serializable function/arguments through helper Nameable channel and dispatch unlocks |
| t_ShareLuaInfo(infostring,waittime,DoneVariableString) | Internal queue-based channel writer; waits for readiness, not network acknowledgment |
| GetSharedLuaInfo(FromPeerInt) | Reads corresponding session-participant Nameable |
| ActiveCoopPeers/InactiveCoopPeers/ActivePeers/InactivePeers | PeerInt-to-Username maps |
| Everactive_Usernames | Nonempty usernames observed in slots0–15; includes potentially disconnected peers |
| NeverActivePeers | Intended never-used slot set; actual marking defects below |
| PeerToPID | Slots PID, PID+4, PID+8, PID+12 belong to the same participant |

The intended initialization avoids relying on stale usernames/session values: it obtains the separately measured Coop counts, opens statistics UI state176 to find **other** active Coop peers at marker0, and, when necessary, forces all active clients to change session. Slots whose active session changed are considered present. Combining that with the UI marker set identifies the executing client as the one remaining active local-team slot.

If all ever-active peers still match TotalCount, the session-change phase is skipped. Otherwise it uses another already visited loaded session (Max IslandSettled counter) or loads helper session **1500005538**. It switches back afterward and locks that session. Unloading is postponed until an IslandSettled event indicates every relevant participant has an alternative destination; repeated load/unload would increase maximum runtime SessionID and make ObjectFinder loops expensive.

Side effects include setting game speed to3, opening statistics, closing menus through session switching, loading a helper session, and displaying start/done notifications. DoHideUI is false in this version because hiding UI also hides notifications/movies. It does not restore the previous game speed. Failure paths after bounded UI/session waits call **GameManager.OnlineManager.leaveSession()**. Removing the mod while its helper session remains loaded is explicitly unresolved in its TODO.

Reserved resources include PIDs117–129 and136–138 (16 helper channels), per-peer unlocks **1500004620–1500004635**, helper session1500005538 and control/notification resources1500005540–1500005544. These reservations must be coordinated with Light's overlapping scenario participants; Nameable and CompanyName are different channels, but shared ownership/integration still matters.

### Actual dispatcher contract

ForPeers accepts a list of peer numbers or strings `Everyone`, `FirstActivePeer`, `FirstActiveCoopPeer`, `Human0`–`Human3`, `Human0_FirstPeer`–`Human3_FirstPeer`, optionally suffixed `_Session_<sessionGUID>`. Nil also selects everyone. **Invalid selectors log an error and default to everyone**, which is unsafe for a consequential once-only action.

The single-active-client shortcut does not fully check string selectors; its own comment acknowledges this. A table selector is checked by value. In multi-client mode it serializes `{funcname,args,ForPeers}`, queues a per-client helper-channel write, waits for `_ExecuteDone` to equal that serialized text, then unlocks the submitting peer's dispatcher resource and waits500ms. The result is not a general returned remote function value or confirmed completion from every recipient.

The per-client share channel is chosen by **sorted helper PID position PeerInt+1**. No other mod may reuse a reserved channel independently. Serialization and wait constraints from Light apply; each channel is occupied for roughly4 seconds according to comments. Static all-client calls can avoid argument transport by using an audited XML ActionExecuteScript path.

### Defects found in this WIP revision

- `_Start` tests `not table_len(Everactive_Usernames)==1`. Lua parses this as `(not number)==1`, which is always false. Thus this revision's multiplayer initialization branch is unreachable, and it enters OnlyOnePeer even in a multi-client game. Intended UI/session detection cannot be claimed operational from this file.
- OnlyOnePeer takes `next(Everactive_Usernames)`, which cannot establish the actual local client in a multi-client game. Setting Finished flags afterward does not make that identity correct.
- AmIFirstActiveCoopPeer and session lookup functions use pairs iteration despite comments promising “first” numerical order. That order is not guaranteed by Lua.
- AmIFirstActivePeer's fallback calls `ipairs(0,4,8,...)` instead of ipairs on a table, and checks ActivePeers values (usernames) for a numeric peer number. The fallback does not implement its intended election.
- Several dispatcher branches test undefined `SessionGUID` instead of the local **SessionGuid**. Their session-qualified first-peer selection does not follow the requested session filter in a clean environment.
- The channel-freeing loops initialize `local i=1` but never increment it; all helper-channel flags depend on the same NeverActivePeers[1]. Slot0 is also excluded by the marking loop1–15. Do not reuse a channel just because this code marks it false.
- `t_Unload_EmptySession` calls DoWeNeedHelpSession before that later local function is in lexical scope; the call resolves a global with that name. This needs a forward local binding to refer to the intended helper.
- Completion waits in dispatch may be unbounded, and invalid ForPeers defaults to all clients. A fixed delay in the save helper does not repair either issue.

These findings concern the exact current WIP sources, not every historical Ultra version. They prevent describing the wrappers as a reliable drop-in solution for new multiplayer mods. Source correction and game/MP verification would be a separate mod-development task; neither was performed here.
