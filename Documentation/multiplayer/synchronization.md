# Multiplayer and Coop execution

## Separate participant, client and command

A participant is a game company. A peer is a running client. Coop peers share a participant but have local cameras, sessions, selections and Lua variables. Restricting work to Human0 does not restrict it to one client of Human0.

Saved setup counts are not a replacement for a live peer helper. In the [2026-10-25 savegame case evidence (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/savegame-audit.json), a 16-entry setup included AI/closed positions, while PeerToSessionMap retained historical peers even when only one human account was assigned. Account assignment plus corroborating thread state supported a solo-test inference; no definitive connection log was recovered. See [savegame peer interpretation](../gameplay/savegames.md#quest-and-peer-interpretation).

XML ActionExecuteScript runs on every active human client. A synchronized command submitted by each of three Coop peers can credit the shared participant three times. WhichPlayer's unlock check restricts the participant; it does not solve peer duplication. A keybinding runs Lua on the invoking client, but the invoked game command may still broadcast a synchronized action.

Sources: [Lua basics](https://github.com/anno-mods/modding-guide/blob/main/Scripting/basics.md), [multiplayer guide](https://github.com/anno-mods/modding-guide/blob/main/guides/Multiplayer_Compatibility.md), [Serp's detailed notes](https://github.com/anno-mods/modding-guide/blob/main/Scripting/Lua_Probleme.md), local `Python Modding/info.txt`.

## Command-specific behavior

| Behavior | Required reasoning |
| --- | --- |
| Automatically synchronized game mutation | Decide which client submits it. Multiple submissions can multiply effects even without a desync. |
| Local-only display/audio action | Usually execute for the intended client; verify it does not also alter simulated state. |
| Unsynchronized simulated mutation | Every active client must apply the same mutation to the same target on the same game tick, according to the documented tests. |
| Unknown synchronization | Withhold an MP-safe claim and supply a precise future test; do not infer safety from a `Net` suffix or unrelated command. |

Serp reports participant reputation changes, selected-object ownership changes and userdata buff changes in the unsynchronized category. Selection-changing work is especially difficult because all peers must target the same object and have access to its session. A loop that waits until each client's local state is ready can finish on different ticks, making that loop insufficient synchronization.

For ordinary deterministic decisions, a Lua-to-XML unlock/trigger handoff can avoid repeated consequential actions: all eligible peers evaluate the same decision, set the same unlock, and an XML trigger performs the action. This needs an audited idempotent trigger/unlock lifecycle, participant scope and reset mechanism. It is not a solution for peers independently choosing different random outcomes.

**ForceBuild clarification from Serp (2026-10-03):** the comment describing this command as usable in multiplayer is conditional on **every client executing it in exactly the same game tick**. A command described elsewhere as multiplayer-incompatible can still be usable under that synchronized-execution premise; the label does not make arbitrary local calls safe. For this specific workflow, Serp considers a direct single ForceBuild call through ActionExecuteScript, repeated through separate script invocations, relatively practical without desync. This is an author assessment, not a newly supplied controlled test or a universal scheduling guarantee. Keep each direct invocation free of per-client waits/coroutine delays that could move it to different ticks. The once-per-tick build limit and all-client same-tick execution are distinct requirements. Follow identical effective participant/session/target data as well; the answer does not establish the behavior of SessionParticipants when clients are in different sessions. Original example: shared_PirateExtraSpawn/data/scripts_serp/forcebuild_harlow.lua:3–7; [walkthrough](../reference/trigger-mod-walkthroughs.md#1500003820--shared_pirateextraspawn).

## Local context and disconnected peers

Serp's tests show peer slots can have holes. The initial mapping observes participant slots 0-3 and additional Coop slots such as 4 and 8 for Human0. Do not assume a particular slot is active just because it has a stored name or session.

GetUsername/GetPlayerName and GetActiveSessionGUIDOfPeerInt can retain data after a peer disconnects. Those getters do not establish current presence. A presumed Coop leader might not be present when another peer resumes a save alone, so simply selecting the historical leader can prevent the mod from doing anything.

GetCoopPeersAtMarker excludes the local peer in the reported behavior. It is available through textembed access rather than directly through the tested Lua interface. An empty result does not establish that there are no Coop peers in the game.

The later Ultra helper combines a forced session change, inactive-peer detection and shared UI markers to identify clients. This changes users' session/UI state and has initialization cost. It must be documented and integrated through the actual helper version; it is not equivalent to a newly available native `isHost()` getter.

## Session and selection conditions

Serp reports that XML ConditionActiveSession can match when any Coop peer is in the target session, while several CurrentSession/UseActiveSession context mechanisms use the leader's session. Lua `session.getSessionGUID()` describes the executing client. These are different observations about different APIs, not interchangeable definitions of “current”.

An object facade or userdata obtained before a yield/session transition can become unusable. A selected-object action needs an explicit target and validation. Do not assume participant-level selection uniquely identifies the client that clicked an item.

Cross-session Nameable writes provide another trap: a direct ts.GetGameObject write is reported visible locally without reaching all other peers. The SessionGameObject textembed path is the established workaround for that case; completion still requires the helper's handling of delayed propagation.

## Randomness

Local `math.random()` sequences can differ between peers. Serp's earlier examples succeed when the chosen result is submitted as a synchronized action; this does not make independently generated Lua decisions deterministic.

For a synchronized mutation, select one authorized submitting peer or use an established synchronized XML mechanism. For unsynchronized mutations, do not use per-peer random results. Do not seed from local wall-clock time or assume the observed GameSetup.RandomSeed equals the visible seed and is synchronized.

The notebook reports that choosing an AssetPool member as ActionSpawnObjects SpawnGUID or ConditionObjectSpawnedObject ExecutionObject causes desync in the tested multiplayer cases. Do not promote those examples into MP-safe random spawning recipes.

## Save/load and buff accounting

Serp clarified on 2026-10-03 that the newest result for `ItemContainer.SetCheatItemInSocket(192168,1)` is **probably no desync**, still uncertain. Earlier contradictory notebook annotations do not establish its current synchronization category. Do not generalize this to SetClearSlot (separately reported desync) or other item-container commands. See Q002 in the discrepancy register.

Track persistent state through an audited shared save helper or game-owned mechanism, not a process-global table. Changing the active peer count between applying and removing an effect can break multiplicity-based bookkeeping.

In particular, AllowStacking=0 hides/prevents the ordinary visible stacking effect but Serp's tests still require multiple removeUpgrade calls after repeated applications. Dividing a resource amount by Coop count may solve a very particular additive command; it does not solve arbitrary object upgrades, ownership changes or delayed coordination.

## Review a proposed Coop feature

For each entry point and each consequential command, record: invoking clients, target participant/OID/session, synchronization category, whether repeated invocation is harmless, which peer submits, readiness/completion evidence, behavior when peers disconnect or load another save, and cleanup after failure.

A design is only supported to the extent of its recorded command-specific tests. This documentation performs no new MP tests. A future test should use two participants plus two peers in one participant, different active sessions/selections, a disconnected historical peer, and save reload within the same game process. Record command counts and target OIDs before/after; a successful syntax check is not an MP test.

## Trigger composition and local events

[Trigger design](../gameplay/triggers.md) separates participant selection from peer multiplicity and explains saved subcondition completion. [Condition selection](../gameplay/trigger-conditions.md#events-ui-and-quests) preserves GUID-specific UI/movie/notification observations: even firing a saved trigger without consequential actions can diverge client state. Native declared pool support is not MP-safety evidence. See the complete source register in [trigger audit](../reference/trigger-audit.md).
