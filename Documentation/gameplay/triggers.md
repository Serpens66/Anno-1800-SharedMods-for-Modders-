# Designing Anno 1800 triggers

Read this chapter together with [condition selection](trigger-conditions.md), the [complete native field lookup](trigger-condition-reference.md), [datasets](trigger-datasets.md), and the [source audit and remaining boundaries](../reference/trigger-audit.md). These chapters concern gameplay triggers. A ModOp `Condition="..."` instead controls XML patch application before gameplay; see [ModOps](../xml/modops.md).

Evidence labels follow the README. Native schema describes structure and intent; Serp's explicit tests provide observed runtime behavior under their stated conditions. Neither proves undocumented engine behavior in every context. The mandatory [feature audit](../foundations/vanilla-research.md) still applies to the actual objects, actions, reference chains and shared dependency versions used by a new mod.

## Start with the intended behavior

Before choosing XML, write down the processing participant, eligible humans/AIs, session/area/object target, conditions that must hold *now*, events that may be remembered, branch priority, action side effects, repeat interval, save migration and mod-removal guard. Include Coop peers separately from human participant slots.

1. Find a native Condition template whose properties express the check. Use the template index and field/dataset lookup; do not derive a property name from its template name.
2. Find an actual native or reviewed mod example in the same context. A quest objective or object selector is not automatically a top-level TriggerCondition.
3. Choose the tree from the timing requirement below. Put actions at the level whose completion should execute them. Keep context-producing conditions near their consuming actions.
4. Choose registration/reset and participant scope explicitly. Audit saved trigger identity before modifying or reusing a GUID.
5. Follow each referenced asset, pool, session, script and action filter. A correct condition does not establish the action's target or execution locality.

When replacing a local event, preserve the native condition's child-completion settings and cancellation paths. The historical Campaign 1.021 [comparison (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/campaign-trigger-comparison.json) shows a lost MutuallyExclusive becoming default Parallel, and a timer registration that revives a reminder after its native cancellation. These were offline source findings, not multiplayer reproductions. The [1.022 source correction and evaluator receipt (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/campaign-1.022-validation.json) retain the bounded fix verification.

## Native structure and effective defaults

The `Trigger` template combines `Standard`, `Trigger` and `TriggerSetup`. `AutoCreateTrigger` combines `Trigger` without a separate Standard/GUID. `FeatureUnlock` adds `Locked` and sets `AutoSelfUnlock=1`. `UnlockableAsset` combines Standard and Locked, without a trigger. Native contracts contain their complete XML and source lines.

| Location | Meaning / serialized shape |
| --- | --- |
| `Values/Trigger/TriggerCondition` | Embedded condition: `Template` plus `Values`, or an inherited embedded definition with `IsBaseAutoCreateAsset`. |
| `Values/Trigger/SubTriggers/Item/SubTrigger` | Embedded `AutoCreateTrigger`, containing its own `Values/Trigger`. Nest further SubTriggers here. |
| `Values/Trigger/TriggerActions/Item/TriggerAction` | Embedded action. Ordinary action templates generally combine `Action` with their specialized property; check each template. |
| `Values/Trigger/ResetTrigger` | Embedded `AutoCreateTrigger` or `EmptyAutoCreateValue`. This is not an action list or a numeric trigger GUID. |
| `TriggerCondition/Values/Condition` | Controls the **children of this condition**: SubConditionCompletionOrder, IsOptional, LinkAllActionsToQuest. |
| `TriggerCondition/Values/ConditionPropsNegatable` | Negation where the condition/template supports this property. Do not substitute a ModOp `!` here. |
| `Values/TriggerSetup` | AutoRegisterTrigger, AutoSelfUnlock, UsedBySecondParties. Applies to the owning asset, not each inline child. |

The Trigger and AutoCreateTrigger **template overrides** choose ConditionAlwaysTrue and an empty inherited ResetTrigger. The generic Trigger **property defaults** instead contain ConditionActiveRegion and EmptyAutoCreateValue. The Condition default is `SubConditionCompletionOrder=Parallel`. Trigger's template sets AutoRegisterTrigger=1 and UsedBySecondParties=1; FeatureUnlock additionally sets AutoSelfUnlock=1. Do not mistake an empty explicit TriggerSetup for disabling these template values. Missing serialized Boolean fields have no explicit value in this lookup; consult their effective contract rather than treating omissions as intentional overrides.

Use an explicit Template when changing an embedded condition's kind. `IsBaseAutoCreateAsset` preserves the inherited embedded template; adding another property need not replace an inherited AlwaysTrue/AlwaysFalse condition. Serp highlights this for Quest PreConditionList and DummyQuest. [Inheritance](../foundations/inheritance.md) also governs nested defaults, empty scalar tags and vector overrides.

## Subtrigger timing and actions

The central trap is **remembered completion**. Serp's HowTo.xml:828–859 reports that completed sibling subconditions retain their completion, including when the main condition temporarily becomes false. Their actions can already have run while a different sibling is still pending. A flat collection of siblings is therefore not a live Boolean AND.

| Desired behavior | Tree / mode | Consequence from the reported tests |
| --- | --- | --- |
| All sibling requirements may happen at different times | Parallel, the native default | Eligible children are checked without waiting for preceding siblings; main completion waits for all required children. Earlier successes remain remembered. |
| Requirements must be completed in sequence | Linear | Later siblings become eligible after preceding siblings complete. Earlier successes are not continuously retested. |
| Choose one complete alternative | MutuallyExclusive | First **complete** eligible branch wins; sibling order gives priority. A true first condition with a false descendant does not yet exclude a later complete branch. |
| Several state checks must hold together at the action | One child per level, actions on the deepest node | Serp's tested nesting pattern keeps the ancestor conditions as gates. Do not flatten it into Parallel siblings. This is a reported pattern, not an arbitrary Boolean-expression evaluator. |
| Side action may run but must not block parent completion | Child condition with IsOptional=1, action on that child | Parent need not wait for that child. The side action still requires its condition/tree to be satisfied. |
| Multiple checks must refer to the same island | ConditionMutualAreaInSubconditions at the main level, area-producing siblings | Separate specialized contract; see condition selection. Do not replace the siblings with the ordinary nested-AND pattern. |

A two-child Parallel example can complete after A was true yesterday and B becomes true today. Linear adds ordering, not simultaneous truth. For nested A → B → C, place the guarded action under C, not under A or B. Keep the chain free of earlier side actions if it is meant to be a pure gate.

A child action executes at that child's completion; it does not wait for every sibling or the main action list. Root actions execute at root completion. MutuallyExclusive can therefore have already-started work in incomplete alternatives; do not design speculative child actions as if the mode were an atomic transaction with rollback.

Keep the intended order of `TriggerActions/Item` entries, but distinguish invoking an action from its effect becoming visible to later checks. A spawn, counter update, GUID change or delayed action is not a general completion barrier for another action. Arm event listeners before emitting their event, and use the reviewed separate post-spawn trigger where item insertion needs an existing object. `Linear` orders sibling **condition completion**, not asynchronous completion of all side effects in an action list. No universal synchronous action-order contract was established by this audit.

**Parent gating — central design rule (Serp clarification, 2026-10-03):** no subordinate SubTrigger executes before its parent condition is satisfied. This also applies when the parent sets SubConditionCompletionOrder=MutuallyExclusive: that mode selects only the first matching complete child branch, from top to bottom; it does not bypass the parent gate. Serp confirms that 1500003013 therefore changes ship GUIDs only after its ConditionObjectPosition radius check succeeds. Preserve the native comment about children being "solvable before the main condition" as original wording, but do not use it to recommend early child execution against this clarification. Parent gating does not erase the separately reported remembered completion of previously satisfied siblings. ConditionMutualAreaInSubconditions retains its specialized timing observation: Serp considers simultaneous subconditions **very likely required, not absolutely certain** in the tested main-condition arrangement.

**Optionality and timers:** IsOptional describes whether a child is required for its parent completion. Serp thinks it has no effect on an owning main condition without a parent and is harmless there; this is an author assessment, not a new controlled test. Do not claim it consumes a false owning main. On 2026-10-03 Serp assessed the later HowTo.xml:856 test as **very likely correct, not absolutely certain**: with one main condition, two optional children at level two, and non-optional descendants at level three, the main condition suffices for completion. The optional level-two branches and their descendants need not complete; recursively marking all descendants optional is not required in that assessed pattern. Optional actions still require their own conditions to be satisfied. Keep the earlier contradictory notebook wording as historical evidence. When an ancestor becomes false during a nested timer, Serp considers a full restart on renewed eligibility **probable, not confirmed** (1500003820). Do not promise either accumulated elapsed time or an uninterrupted full interval from that assessment. See [certainty and remaining boundaries](../reference/discrepancies.md#q005-trigger-composition-and-registration-boundaries).

## Registration, repeat execution and initialization

AutoRegisterTrigger arms the trigger without a separate action. Manual XML registration uses ActionRegisterTrigger/TriggerAsset, whose target must have Trigger. UnregisterTrigger=1 unregisters it; InheritArea=1 requests area transfer from the parent trigger/quest. ActionResetTrigger has no TriggerAsset field: it is a distinct action, not ActionRegisterTrigger with another spelling. Preserve the native description that an already-created trigger resets to its origin state as original schema wording; use the state/entry-point distinction confirmed by Serp below for construction.

For normal repetition, use the embedded **ResetTrigger** pattern in [recipes](trigger-recipes.md). Serp reports that it becomes registered when the main trigger completes and that its completion resets the parent. Directly unlocking a FeatureUnlock does not itself register that reset. Do not use an immediately true main/reset pair for expensive work; choose a meaningful timer or wait for state to change.

**Registration state and entry point (Serp confirmation, 2026-10-03):** XML ActionRegisterTrigger does nothing if the trigger is already registered. Once the full trigger has completed, it is no longer registered and can be registered again. Lua registration can instead register the same trigger multiple times concurrently; one GUID does not guarantee one active instance. Serp considers self-registration directly from the trigger's own action **possible but unconfirmed**; use ActionResetTrigger or the embedded ResetTrigger for that repetition. Do not infer the completion boundary during an executing action list from the ability to register after full completion. Earlier circular-registration failures retain their exact test context.

Serp reports explicit ActionRegisterTrigger/ActionResetTrigger can permit execution for already-defeated participants that ordinary ResetTrigger would avoid for AI. Humans present at game start can continue executing saved triggers after defeat/disconnection, including ordinary resets. Decide whether you want those executions; a human still owning a ship/kontor is not a reliable "has not lost" test.

Initialization is asynchronous. WhichPlayer/IsAI shared checks acquire their markers/unlocks after settlement and a short delay; immediately negating a still-false identity check misclassifies the player. Their comments recommend a kontor/settlement check followed by roughly two seconds before negation. Prefer positive identity checks. For frequent repetition, separate the initial readiness gate from the repeat trigger so the initialization delay is not paid each cycle. ActionExecuteDiplomaticAction has a reported roughly ten-second initial readiness delay. These times belong to those examples, not all conditions.

Actions can invalidate the condition that allowed them. BT Passive Trading's MoreTradeForHumans files delay ActionSetObjectGUID by 1000 ms because changing the matching object's GUID too soon prevented completion/reset. RelativeToQuestStart counters may see deletion in the following cycle unless a reset delay lets counters update. ModSettings notes report about 200 ms between ObjectBuilt events and ProfileCounter updates. Keep the source-specific timing and measure only when a new context requires it.

## Participants, execution multiplicity and context

UsedBySecondParties controls creation for second-party AI in addition to humans. It does not make a pirate or merchant the processing participant. The WhichPlayer sources explain that ordinary triggers run for humans, or humans plus AI, and that third parties cannot directly run them. Third-party objects can still be targets or CheckedParticipant where the relevant counter/filter supports them. AI cannot run the human quest-helper workflows described in CodeSnippets.

Use shared_WhichPlayer_Condition's positive identities (`1500001600` any human, `1500001601` AI, `1500001613`–`1500001616` Human0–Human3) only with its real dependency and initialization contract. Its templates and non-identical bundled versions must be inspected. PirateDefeatHelpers provides specialized positive current/not-defeated conditions; inspect its current version instead of reconstructing pirate liveness from ConditionIsParticipantInGame.

| Context | Required distinction |
| --- | --- |
| Processing/owner | The participant whose trigger/quest is being evaluated. Does not imply Lua runs only on that client's machine. |
| CheckedParticipant | Only used when its enabling field is set. In PlayerCounter Area tests it changes the searched owner, not the set of islands traversed. |
| ActiveSession | Current presence, not "session is loaded" or "session is unlocked". Serp reports any Coop peer can satisfy ConditionActiveSession. |
| Processing/parent/quest session | Registration, parent evaluation or quest-derived context. Do not substitute the executing Lua client's session for these. |
| QuestArea | Carries quest-specific context beyond selecting a session. Matching the same session does not restrict actions to one island. |
| Object GUID / OID / pool | Asset type, individual instance, or a collection. A filter by GUID does not uniquely identify the object that satisfied a condition. |

ObjectFilter's `ObjectParticipantID` is not an owner filter without its enabling checks. Serp's ObjectPosition/action examples explicitly require CheckParticipantID=1, including cases with CheckProcessingParticipantID=1. ObjectTargetFilter has its own fields; inspect both source definitions. MaxObjectCount is documented as a randomly chosen subset, not a stable first-object selector.

Area/session propagation, counter scope, object existence and action targeting have a dedicated treatment in [condition selection](trigger-conditions.md#area-session-and-object-propagation).

## Savegames, removal and extension points

For a read-only examination of actual saved definitions, follow [Reading savegames](savegames.md). The [Campaign New World case (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/README.md) demonstrates that release, current XML and multiple saved trigger revisions can differ despite the same ModID/version. Follow saved ConditionKey/SubConditionKeys links rather than grouping every condition with one owning GUID into a single instance. The case is offline evidence, not a new registration or multiplayer runtime test.

**Code snapshot on registration (Serp confirmation, 2026-10-03):** registration captures the code present at that moment as the trigger's saved definition. An already-registered instance retains that snapshot; editing XML does not update it in place. A later fresh registration captures the current code, including changed conditions/actions. XML ActionRegisterTrigger on an already-registered instance does nothing, so it does not refresh that snapshot: an unregister/re-register workflow must actually reach a fresh registration. This confirms the previously open saved-code-refresh mechanism, without promising replay or migration of completed rewards, missed events or already-applied effects. Adding a ResetTrigger to an already-completed GUID does not retroactively execute it. A new GUID may still be useful for an explicitly guarded migration. Do not reuse a historical GUID merely because it is now "free" or used as text.

Saved registered triggers may fire after the mod's assets are removed. **Missing UnlockNeeded GUIDs are treated as unlocked** in Serp's tests. A sole positive unlock condition can therefore start the removed trigger. Use the established **still-locked presence guard**: a mod-owned UnlockableAsset with DefaultLockedState=1 which remains locked, and a main ConditionUnlocked with NegateCondition=1 checking it. When the asset disappears the check becomes false. This is different from an intentional lock-to-start FeatureUnlock: that helper starts unlocked (DefaultLockedState=0), disables AutoSelfUnlock, and is relocked to signal execution. See LuaLight for its cooldown/rearm and Coop contract; do not mix these two lock conventions.

HowTo.xml also reports removal/save/re-enable can clear completed identities in one scenario. Treat that as an observation, not a universal migration or cleanup mechanism. Removing a ModOp, disabling auto-registration, or editing an old definition does not unregister every previously saved instance.

Shared_EventOnGameLoaded and OncePerSessionPerSaveLoad intentionally expose **ResetTrigger/Values/Trigger/TriggerActions** as an extension point so newly added actions are read when the reset is registered. Follow their metadata/load order, including Medium replacing EventOnGameLoaded. For semantic subscriptions, create your own trigger against the shared signal rather than attaching permanently saved custom actions to an unrelated helper. PirateDefeatHelpers explicitly changed its usage to separate consumer triggers for this reason.

## Session lifecycle and Lua/Coop

| Requirement | Existing workflow / limitation |
| --- | --- |
| Every session entry, including unknown mod sessions | ConditionEvent SessionEnter with an appropriate reset; it also occurs on loading a game in the established helpers. |
| First visit per session over the save | shared_OncePerSession_xml, GUIDUnlocked signal 1500004527. It may already have fired before a newly added consumer mod. For global buffs also apply immediately to previously visited sessions, or use consumer-owned identities when necessary. |
| First visit per session per save load | shared_OncePerSessionPerSaveLoad, signal 1500004530 and its Lua dependency; attach at the documented reset extension point. |
| Every save load | shared_EventOnGameLoaded, 1500004636 with its Lua/save detector, or the actual Medium replacement. Native MetaGameLoaded/ProfileLoaded experiments were inconsistent and are not a replacement. |

SessionLoaded is not the same as a human having visited/unlocked the session. The global-buff notes report that AddBuff requires prior visitation or an owned object, so a loaded-session event is too early in that workflow. Hardcoded ActiveSession triggers support only their enumerated sessions. For AI, IslandSettled is a reported useful signal and includes acquisitions; it can occur while a human's client is in another session.

ActionExecuteScript is reported to execute on **all human clients**, irrespective of the trigger's processing participant. Coop peers can each call RegisterTriggerForCurrentParticipant, leading to repeated registrations. Filtering the XML to Human0 does not by itself make the Lua call single-peer. Use the reviewed [LuaLight](../lua/shared-light.md) lock signal/cooldown or appropriate [peer helpers](../lua/shared-medium-and-ultra.md), preserving their dependencies. Syncing an unlock does not make arbitrary local GUI conditions safe.

Local UI/movie/notification conditions can diverge **saved trigger state even with no gameplay action**. Campaign/Story Coop mods replace specific flows with timers or synchronized lock signals at their actual registration points; these are context-specific alternatives. Do not start all event listeners at game start or blindly replace every ConditionEvent with a persistent unlock. Read [multiplayer](../multiplayer/synchronization.md) and [UI pitfalls](trigger-conditions.md#events-ui-and-quests).

## Review a completed design

Use the [worked recipes and walkthroughs](trigger-recipes.md). Trace initial registration, each child becoming eligible, remembered completion, action context, condition changes caused by actions, reset, reload, removal, and each executing participant/peer. Check nested modes and inherited templates after patching. Offline XML success establishes patch/structure only; it cannot validate timing, game C-functions, UI context or MP synchronization.

## Real mod walkthroughs

[Six existing mod trigger walkthroughs](../reference/trigger-mod-walkthroughs.md) trace complete definitions and relevant callers/consumers. They show the single-ship invariant behind a broad GUID filter, positive pirate-state helpers, optional quest cleanup and synchronized movie start/completion. Serp confirmed parent gating and branch priority, considers timer restart probable but unconfirmed, and assesses owning-main IsOptional as ineffective without a parent. Serp also confirms XML-versus-Lua registration and code snapshots; nested optional-depth is very likely clarified, while direct self-registration remains unconfirmed. Passing offline patches adds no runtime proof.


## Compose trigger extensions with other mods

Prepare a potentially missing SubTriggers list with an empty merge, then append the new Item. Preserve existing children, native registration/cancellation and condition settings. A shared container does not make arbitrary extra children semantically compatible: completion modes, timing and action order still need review. See [Mod compatibility](../foundations/mod-compatibility.md#ensure-containers-then-append-entries).
