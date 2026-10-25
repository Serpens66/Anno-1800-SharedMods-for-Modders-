# Personal notebook evidence and unresolved runtime limits

Both original notebooks were read completely on 2026-10-03: `D:/CDesktopLink/Unterlagen/Mods/Anno 1800/HowTo.xml` (2862 lines) and `D:/CDesktopLink/Unterlagen/Mods/Anno 1800/Python Modding/info.txt` (867 lines). Their hashes are in the source inventory. This register preserves important observations while the remaining feature audits and gameplay chapters are completed.

**Evidence policy:** an explicit Serp test is accepted unless contradicted; tentative wording remains tentative. A quoted schema description is a source contract, not proof of runtime behavior. A TODO, rejected attempt or proposed workaround is not a successful test. This register is not a blanket implementation recipe for unreviewed systems.

## XML/loader and development history

| Notebook finding | Treatment |
| --- | --- |
| Reserved GUID range1500000000–1500010000 and a historical “6150 free” note | Historical allocation notes; check actual current collisions/reservations before use |
| External loader/Python DLL installation, integrated loader from2023, loader11/mod.io dates | Historical; current integrated-loader packaging is documented separately |
| Merge on repeated-name lists initially unsupported | Superseded by GU17.1 occurrence merge; never interpreted as key-based merge |
| Empty merge payload did not clear list | Confirmed by inspected implementation and offline evaluator |
| Exact GUID/path lookup much faster than broad speculative traversal in one measured case | Preserve example-specific measurement; do not promise universal timings |
| Content copy with per-target GUID versus arbitrary global multiselection | Selection context matters; use tested lookup forms, not imagined per-target relative Content |
| Marker-based intersection, temporary number tables, pool conversion | Loader techniques; cleanup and exact node shapes required; see XML content/list chapter |
| Condition grouping can test once globally and prevent insertion for later entries | Use per-entry predicates when appropriate; do not treat an operation Condition as a per-result predicate |
| PreferLocalFiles experiment later found ineffective | Rejected solution; do not recommend as a required mod setting |
| mods.reload stale matching/quest cooldown behavior | Context-specific reload limitations; Medium/Ultra additionally report crashes |

## Trigger, condition and save lifecycle observations

| Observation in HowTo.xml | Preserved scope / implication |
| --- | --- |
| Trigger registration/fired state saved; changing XML does not necessarily replay old triggers | Serp confirms registration snapshots current code; fresh registration reads new code. XML registration is a no-op while registered, possible again after full completion; Lua can register concurrent copies. Replay/migration still needs explicit guards |
| Missing unlock asset treated as unlocked | Saved trigger can fire after mod removal; Light's inverted lock guard is an established mitigation with its specific contract |
| ActionExecuteScript executes all human clients, not only processing participant | Confirmed in later Lua notes and helpers; Coop multiplicity remains |
| Dead AI and disconnected humans differ in which actions run | Do not generalize human/AI lifecycle behavior from one trigger |
| Parallel subconditions can retain earlier completion | Do not assume all predicates are reevaluated simultaneously at main completion |
| Linear/MutuallyExclusive define order/first completed branch | Not equivalent to source order selecting first true-looking XML node |
| IsOptional nesting claim is followed by a later test contradicting it (lines852–856) | Serp follow-up2026-10-03: later test very likely correct, not absolutely certain; optional level-two branches exempt non-optional level-three descendants from blocking main completion |
| ConditionMutualAreaInSubconditions only works reliably in tested main-condition context | Serp clarification2026-10-03: simultaneous subconditions very likely required, not absolutely certain; do not move the condition arbitrarily within the tree |
| Reset timing can count deletion/changes toward next relative baseline | Notebook suggests roughly one-second delayed reset for the tested case, not a universal fixed delay |
| ConditionEvent QuestSuccessfullyResolved with ContextData works; QuestStarted did not in one setup | Serp clarification2026-10-03: ActionStartQuest versus pool start remains a reasoned hypothesis, not further tested |
| ConditionEvaluateTextSource numeric comparisons gave inconsistent results | Do not use as an established arbitrary numeric expression evaluator |
| ConditionThreshold works in some storage contexts; mass repetition/subtrigger hangs reported | Serp reaffirmed all CodeSnippets comments2026-10-03; original seems/likely qualifiers remain. Positive durations and milliseconds remain probable, not confirmed |
| ConditionIsParticipantInGame for pirates has initialization/session issues and destroyed pirates can remain true | Notebook's later re-registration/session observations narrow the earlier unconditional failure claim |
| ConditionGUIEvent more reliable than generic GUI events but causes Coop divergence for tested unlock flow | Local UI activity is not a replicated gameplay trigger |

## Quests and pools

| Observation | Scope |
| --- | --- |
| RelativeToQuestStart begins when quest is offered, not only after acceptance (line2292) | Baselines may already change while star is visible |
| QuestLimit caps simultaneous quests; pool cooldown still applies | Raising limit does not remove cooldown |
| PoolCooldown is after choosing/calling a quest | Parent and child pools independently affect cadence |
| CooldownOnQuestStart/End start a cooldown only if none is running | End does not necessarily extend an already running timer; notebook wording remains qualified |
| QuestCooldown applies to quests, not a pool containing only subpools | Do not use it as an interchangeable subpool cooldown |
| AffectedByCooldownFactor scales by quest-frequency setting | Schema wording and notebook interpretation |
| Pool preconditions checked for each new grant | Quest's own KeepCheckingPreconditionsWhenRunning needed for cancel-on-invalid behavior |
| ActionStartQuest ignores normal preconditions at start; KeepChecking... still checks during running | Distinguish pool scheduling from explicit action start |
| ResetPreconditionsAfterQuestWasTriggered resets event-like preconditions | Does not turn MetaGameLoaded into a repeatable every-load event |
| QuestSessionDependencies is OR among loaded sessions | Cannot express “all listed sessions loaded”; explicit action context can differ |
| War can cancel only one outstanding quest in observed setup | Add explicit quest preconditions/cancel design where needed; do not assume all are removed |
| Participant world departure canceled quests, but destroyed pirate could still get new quests | Availability guard needed for that tested pool design |
| ManualActivation versus QuestStart distinction marked uncertain | Do not upgrade it to a confirmed workflow |
| Quest instance IsActive remains true after completion; use not HasEnded too | Lua helper uses both; global instance index does not establish ownership |
| StateReachable corresponds to ready reward/confirmation stage; StateReached can persist across later instances | Not a generic live spatial check |
| Same QuestDecision GUID can propagate choices between active copies in MP | Use one active instance or audited participant-specific identities |
| A malformed/failed OnQuestStart spawn can prevent whole quest | Validate prerequisites before blaming pool scheduling |
| DeliveryObjective under MutuallyExclusive can display OR between required goods | Reported UI defect, not proof that delivery requirements changed |
| PlayerCounterContextPool supports TargetObject delivery while Area delivery failed | Context-specific pool support |
| Groups with GUIDs can be referenced by research/quest pools | Sibling insertion position can create unintended membership |

## Object spawning, filtering and ownership

| Observation | Scope |
| --- | --- |
| AllowProcessingSession fails in OnQuestEnd; worked in other tested trigger/quest contexts | Action context is part of spawn contract |
| Quest/client/kontor/context/inherited area modes differ | Follow each native reference chain; no single default context rule |
| ForceContextPosition ignores distance constraints in tested setup | Not a guarantee of valid building placement |
| Spawning outside ConstructionArea can make BuffFactory area buffs and area counters fail | Object existence does not imply valid area registration |
| ActionSpawnObjects AssetPool random choice and ConditionObjectSpawnedObject ExecutionObject pool caused MP desync | Do not offer MP-safe pool spawning recipe |
| Probability ignored in tested spawn-pool usage; duplicate entries provide weighting | Not a universal RewardPool/AssetPool probability rule |
| ObjectFilter with one-entry pools can fail, including narrower counter-pool context | Never simplify a multi-entry working filter to one entry without evidence |
| ItemEffectTargetPool and PlayerCounterContextPool work in some ObjectFilters; MatcherCriterionGUID needs plain AssetPool in tested usage | Pool shapes are consumer-specific |
| CheckedParticipant changes ownership target, not necessarily searched islands | Avoid conflating processing, target and search scope |
| Projectile SpawnImpactObject does not trigger ObjectBuilt event | Use appropriate tested counter/event rather than assuming normal construction |
| Fast projectiles can disappear before counter update | Counter-based detection may miss them |
| Lifetime did not expire some spawned flotsam as expected | Not a proven arbitrary object cleanup timer |
| GUID change clears labels; only compatible property sets safe | Some schooner-to-gunboat change crashed, while another ship conversion worked |
| Ship cargo/routes can persist through a compatible GUID change; maintenance/UI refresh delayed | Expedition/world-map objects and Upgradable conversions are separate failure cases |
| ActionDeleteObjects LeaveMap affected by movement/ownership order; internal WarFleet entry may remain | Delete/leave-map not equivalent to all AI bookkeeping cleanup |
| ActionChangeParticipant with MaxCount1 crashed in one filter setup | Preserve original context rather than generalize all owner changes |
| ActionAddGoodsToItemContainer divides across targets, may overflow to flotsam, can auto-equip | Require exact targeted container and slot/socket expectations |
| NPC trading-station insertion failed; NPC ship insertion needed separate post-spawn trigger | A delay inside the original action list did not establish the same context |
| ActionDeleteItem is global in tested usage; ActionReplaceItem not random reward generation | Do not invent ObjectFilter behavior for these actions |
| ConditionInStorage checks slots rather than sockets; absent object amount zero can satisfy comparison | Zero-valued query can mask missing target |

## Production, items, buffs and AI

| Observation | Scope |
| --- | --- |
| BuffFactory plus FactoryOutput duplicates statistics entries | UI side effect, even if production works |
| BuffFactory ignores NeededFertility in later Kurila correction | Reject earlier proposed fertility detector based on a buff-only factory |
| Non-unit input/output Amount experiments inconsistent with cart delivery | Do not recommend universal non-unit amount scaling; intermediate/additional-output designs need their own audits |
| Larger transporter storage affected range with reported clamp near67 | One observed case, not a schema-wide cap |
| ReapplyEffects did not fully update old/new buff targets on saved games | Modifying an asset does not guarantee existing effects migrate |
| AllowStacking0 does not prevent all repeated upgrade bookkeeping | Repeated removeUpgrade may be necessary even when UI does not show stacking |
| MetaBuffHandler needed for some third-party/global buffs | Session/object upgrades are distinct |
| ConditionIsBuffed did not detect passive socketed/global effects; native use targets activated ActiveBuff | Presence of an effect is not always detectable through this condition |
| ItemTypeSpecialist could combine passive buff and active action; Normal limited in tested usage | Item type matters |
| ItemWithUI activation works in cargo slot but not ordinary socketed guildhouse context | GUIType changes did not establish an arbitrary button panel |
| Godlike items could overwrite native godlike behavior | Rejected rarity/cost trick, preserve compatibility caution |
| Common research items need CommonRecipesBlacklist exclusion; other rarities need relevant research pools | Research pool membership, including nested groups, is separate from ordinary reward probability |
| Probability0 did not remove an item from research availability | Consumer-specific probability interpretation |
| New AI production alternatives can stall despite normal unlock progression | SecondPartyRelevant, IsConsideredByAI and GUID-specific native exceptions must be audited |
| Coal mine/kiln behavior ceased when GUIDs changed in tests | Not proof that duplicating their XML gives a general alternative-production AI selector |
| Unarmed ships can act as AI trade ships without WarFleet; armed ones need military integration | Spawned/gifted military ships still behaved inconsistently; self-built variants worked in tested setup |
| Shipyard AI needs matching CrafterConfiguration/build-menu/unique craftable ship integration | Terrain and placement exceptions remain uncertain |
| New arbitrary AI PlacementScore values are not established | Use actual existing balancing/contracts |
| AI replacements and UnlockReferenceAssets exist in native profiles | These are concrete research anchors, not proof every replacement is automatically supported |

## Lua API and multiplayer notebook outcomes

| Observation in info.txt | Treatment |
| --- | --- |
| Process globals persist across saves until game restart | Separate library registration from per-save state |
| Event callback error can crash; coroutine error can disappear | Protect/log boundaries, not silent pcall |
| Read-after-write can remain stale for more than one yield | Query specific completion, not universal tick count |
| Userdata valid only in local session; cached facades can break after use | Reacquire via full OID, distinguish numeric/string editor IDs |
| Nameable direct cross-session write not properly shared; SessionGameObject textembed workaround | Exact channel/path/timing required |
| Local selected object/group APIs have context limitations | Never broadcast a selection-based action without explicit target |
| getProperty works only for some properties and own/current-session objects | Failure not always absence |
| changeOwner/AddUpgrade/RemoveUpgrade not normally synchronized | All-peers same target/time workaround remains command-specific |
| SetChangeSkin observed synchronized; game.playSound local | Do not infer other APIs from method prefix |
| ProfileCounter Lua query cannot handle pools | XML condition amount workaround uses a predefined audited pool/trigger |
| ForceBuild through SessionParticipants for pirates/traders worked in MP in tested usage | One object per tick and exact participant/object context matter |
| AI credits are not ordinary human money; owning a kontor differs from control logic | Ownership changes do not replace native AI initialization |
| Kontor owner change caused persistent storage/control anomalies across subsequent new games | Upgrade workaround limited to original test, not general migration |
| GameSetup difficulty values reflect initial setup; scenario features not loaded merely by a UI flag | Do not advertise sandbox seasons from a menu setting |
| CheatAddBuildingPermits adds all rather than one | Need appropriate XML contract for targeted permits |
| SetCheatItemInSocket latest result: **probably no desync** | Serp clarification2026-10-03, Q002; still uncertain |
| SetClearSlot separately reported desync; EquipSlot/UnequipSocket swap tests differed | Do not merge these distinct functions into one synchronization rule |
| Factory.ToggleCheatFertility adds required fertility and can persist; existing factories may need move/rebuild | MP outcome unconfirmed; not equivalent to regeneration of FertilitySet |
| RewardPoolCheatItemInSlot earlier failure followed by later “works” note | Later observation supersedes blanket unsupported claim; precise context remains unspecified |
| Selection-group storage overwrites user groups and a ship can belong to only one | Avoid using reserved user controls as invisible temporary storage |
| SetAddDamagePercent versus userdata Kill differ in MP and ruin/island ownership effects | Destruction procedure is not interchangeable |
| WeatherForcePreset indices reference dataset positions; native examples establish (2,1) rain and (0,1) sunny | Do not guess meaning of every enum/index from its displayed Id |
| Nameable rejects some characters; hex transport helper introduced later | Serializer itself has escaping/round-trip limits |
| Amount maximum100000 “seems” with money exception | Unconfirmed cap, not a universally enforced limit |
| Replacing a Lua global API wrapper affects Lua callers but not native/textembed calls | Reject attempted universal interception |

## Local GUI, notifications and movies

NotificationRemoved, GUI events and movie completion can be client-local while changing saved trigger state. The notebook contains successful and unsuccessful movie tests depending on GUID, trigger kind, start timing and action. Preserve these differences; “money did not desync” does not prove every action is safe or that money is outside desync checking.

CharacterNotification ThirdpartyDefaultCommand is the reported workaround for some dismissal handling; it does not run when a predefined choice button handled the notification and cannot be blindly added to other notification types. Commands accept textsource expressions, not unrestricted Lua. Selection access failed in those contexts even when it worked in debug textsource.

The bridge using helper CompanyName and a script trigger is documented in LuaLight. Its callback/locking and delayed execution limitations still apply. Multiple Coop choices need the established availability guard; a local choice alone must not trigger conflicting replicated operations.

## Runtime-only verification instructions

For an unresolved claim, retain the original notebook snippet, exact asset/trigger GUID, data version, entry point, owner/processing participant, session/area, initial object/quest/buff state and whether it is a new game or loaded save. Compare the narrow alternatives independently. In MP record each peer's presence, active session, invocation count and OID. Include pause, disconnect and same-process save reload only when relevant to the feature. No tests are requested or performed by this documentation task.

## Trigger-topic transfer

The observations above now have detailed guidance in [trigger design](../gameplay/triggers.md), [condition selection](../gameplay/trigger-conditions.md) and [recipes](../gameplay/trigger-recipes.md). [Native fields](../gameplay/trigger-condition-reference.md) and [datasets](../gameplay/trigger-datasets.md) support condition discovery. Original corrections and unsuccessful/WIP examples are traceable through [source evidence](triggers/prose-evidence.md); Q005 keeps unresolved runtime details visible. This does not mark unrelated gameplay-topic transfer complete.


## Movie-speed recollection (2026-10-25)

Serp believes he previously tested the commented movie-speed command and found that background simulation still ran at normal speed during the movie. He explicitly presents ineffectiveness as a possibility. Record this as an uncertain historical recollection, not a newly repeated test or proof that all GameClock speed changes are ineffective. Both movie scripts remain commented and now contain the risks/recollection. [Source/change evidence (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/dlc-gates-validation.json); [original caller audit (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/movie-speed-callers.json).
