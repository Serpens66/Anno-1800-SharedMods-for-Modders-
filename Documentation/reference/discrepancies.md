# Discrepancies, questions and historical boundaries

## Q001: scalar Condition expressions in Anno 1800

**Status: answered on 2026-10-03; documentation policy resolved from source and subsequently confirmed in the standalone GU17.1 XML evaluator. No in-game test exists.**

Serp has not tested scalar conditions and agrees that the actual Anno 1800 loader implementation is the stronger source for behavior. This answer does not itself establish an in-game result.

The current [Groups and Conditions reference, Condition section](https://jakobharder.github.io/anno-mod-loader/modops/control/#condition), under the label **117 & 1800**, says:

> ModOps are only applied when their `Condition` attribute matches to a non-empty list or to `true()`.

The inspected Anno 1800 implementation [selects nodes](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/xml_operations.cc#L226) and [tests whether that node set is non-empty](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/xml_operations.cc#L865). It does not evaluate an XPath boolean result. The [pugixml manual, section 8.2](https://pugixml.org/docs/manual.html#xpath_select) documents that `select_nodes()` rejects expressions returning a type other than a node set. The loader catches `pugi::xpath_exception`, logs the path error, and returns an empty result at lines 227-232.

**Source-based conclusion:** `Condition="true()"` and `Condition="count(//Asset)&gt;0"` are unsupported scalar conditions in the inspected 1800 code. Use node-selection conditions or the separately implemented `!`/`#ModID` forms. Boolean expressions within a predicate, such as `//Asset[Values/Standard/GUID='123']`, still return a node set and are a different case; the asset schema and selection context must remain correct.

Error handling is not an alternative condition syntax: a leading `!` can invert an empty result even when that result followed a selection error. Never rely on an invalid expression to control a patch.

**Boundary:** the website statement is broader than the verified 1800 implementation. This finding is pinned to commit `8326b7c5a7648787c52f1252cd6e8ae60e593d1c`; it is not a binary comparison with Serp's installed game or an in-game test, and it makes no claim about Anno 117's evaluator.

## Q002: SetCheatItemInSocket multiplayer result

**Status: answered by Serp on 2026-10-03.** `Python Modding/info.txt` lines 738–743 contains both a desync observation and an uncertain later reversal. Serp clarified: the newest state is **probably no desync**; the result remains uncertain. Record this wording, rather than describing the function as definitely synchronized or definitely desynchronizing. Exact peer/session/test conditions were not supplied. No new test was performed.

## Q003: URLs in authoring-tool ModDependencies

**Status: answered by Serp on 2026-10-03; documentation policy resolved from code.** Serp has not tested the URL shortcut and requests that the code finding be used.

At vscode-anno commit `19cda8edc73d65a622c9c5c588953a0170c337c6`, [Deploy documentation](https://github.com/anno-mods/vscode-anno/blob/19cda8edc73d65a622c9c5c588953a0170c337c6/docs/tools/deploy.md) claims ModDependencies URLs are automatically bundled and replaced with ZIP-derived dependency IDs. The inspected [builder](https://github.com/anno-mods/vscode-anno/blob/19cda8edc73d65a622c9c5c588953a0170c337c6/src/builder/index.ts), [metadata reader](https://github.com/anno-mods/vscode-anno/blob/19cda8edc73d65a622c9c5c588953a0170c337c6/src/anno/modInfo.ts) and [metadata converter](https://github.com/anno-mods/vscode-anno/blob/19cda8edc73d65a622c9c5c588953a0170c337c6/src/builder/converter/modinfo.ts) process Development.Bundle as the download list and leave ModDependencies unchanged. No separate shortcut implementation was found by searching all src files.

Document normal ModIDs in ModDependencies and URLs separately in Development.Bundle. Do not promise shortcut support from the contrary prose. No build/download execution test was performed. Other tool documentation issues (README inlining, development prepatches and XML-test evaluator selection) are recorded in [authoring tools](../foundations/authoring-tools.md), with their unresolved caller/version boundaries explicit.

## Q004: population consumption and income units

**Status: MoneyValue interpretation decided by Serp on 2026-10-03; remaining consumption/calculation boundaries retained.** Serp initially preferred properties-toolone.xml provisionally, then clarified that MoneyValue should be understood as **income per 100 inhabitants per minute**, as in the guide, rather than per 100 residential buildings. Use this interpretation in this documentation. This is an explicit user decision, not a reported controlled game test or an engine-code finding.

**Language context supplied by Serp:** the authors of the properties-toolone.xml comments are German and are not native English speakers. Consequently, words can be confused in those comments. Serp is very confident that the MoneyValue comment's "residences" means inhabitants in this case. This author/language context is recorded as information provided by Serp, not as independently verified biographical evidence. Do not automatically apply this correction to every occurrence of residence, resident or citizen; interpret each property in its own context.

The [production tutorial, Amount and MoneyValue sections](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/hier0nimus-tutorials/03-making-new-production-chain/readme.md#amount) describes consumption per resident per second and multiplies the engineer coffee value by 40 residents. It also calculates MoneyValue using residents rather than houses. The complete native PopulationLevel7 schema instead describes Amount as consumption by each full house per second, and MoneyValue as income from 100 residences per minute. Native population asset 15000003 contains coffee Product 120032 with Amount 0.000784314 and MoneyValue 40; its DefaultResidence 1010346 has ResidentMax 40. These identity matches establish that the comparison concerns the same example; they do not resolve the conflicting units by themselves.

The wording still differs: **citizens** are residents/inhabitants, whereas **residences** are houses. Dividing both by 100 does not make those different units equivalent. For one 40-resident house and MoneyValue 40, the guide's stated formula gives 16; the literal property description gives 0.4 per minute. With coffee Amount 0.000784314, the guide gives 1.8823536 tons per house/minute; the literal property description gives 0.04705884. These are comparisons of the stated formulas, not measured rates. **The selected MoneyValue interpretation is the guide's resident-based formula**: MoneyValue 40 with 40 inhabitants gives 16 per minute before any additional modifiers. The house-based result is retained only to explain the wording discrepancy and must not be used as the recommended interpretation.

The previous choice to prefer the native **comments** must not be confused with a comparison against actual engine **code**, as in Q001. PopulationLevel7/DefaultResidence and Residence7/ResidentMax both explicitly participate in consumption calculation, but their descriptions do not expose the complete calculation. Native exported UI expressions call engine-side production/consumption statistics rather than defining that calculation. Therefore source inspection alone has not proved these runtime calculations. The MoneyValue wording discrepancy is resolved for documentation purposes by Serp's decision above; preserve the original comment and provenance rather than silently rewriting the source. Amount remains documented with Serp's assessment that the guide is correct and the remaining evidence boundary; do not label the guide's formulas definitively wrong. Exact occupancy, bonus-needs and modifier calculations remain part of the feature audit. See [complete tutorial review](production-tutorial-review.md).

## Q005: trigger composition and registration boundaries

**Status: clarified by Serp on 2026-10-03 with certainty differences. No new game test.**

- HowTo.xml:854-856 preserves an earlier claim that every optional descendant must be marked, followed by a contrary test. Serp considers the later test **very likely correct, not absolutely certain**: a true main plus two optional level-two branches can complete despite non-optional, unfulfilled level-three descendants. Do not present recursive optional marking as a universal requirement.
- Serp confirms parent gating, including MutuallyExclusive. Only the first matching complete child branch executes, from top to bottom. Proximity gates the GUID changes in 1500003013. Preserve the contrary native description as original wording, not as a bypass rule.
- Serp confirms XML ActionRegisterTrigger is a no-op while registered. After full completion the trigger is no longer registered and can be registered again. Lua can register concurrent copies. Direct self-registration from its own actions is possible but unconfirmed; prefer ActionResetTrigger or ResetTrigger. The native reset-to-origin description and older circular-registration failures remain original, context-specific evidence.
- Serp confirms registration captures the current code as a saved snapshot; a later fresh registration uses new code. The Campaign savegamebugfixed.include.xml:3–7 TODO is resolved at the mechanism level. In-place edits or no-op registrations do not refresh an existing instance; refresh does not automatically reconstruct missed events or migrate past effects.

Exact original hashes, wording and destinations: [trigger audit](trigger-audit.md), [source evidence](triggers/prose-evidence.md), [native contracts](triggers/vanilla.json). Direct user clarifications are recorded in [case outcomes](triggers/mod-cases/review-outcomes.json). They are not engine-code proof.

## Q006: six-trigger walkthrough questions

**Status: answered by Serp on 2026-10-03 with explicit certainty differences; remaining runtime questions retained.**

- M001, 1500003013: confirmed parent gating and top-to-bottom MutuallyExclusive priority. This resolves the conflicting construction advice in Q005.
- M002, 1500003820: full timer restart after an ancestor becomes false is **probable, not confirmed** according to Serp. Restart/pause behavior remains a runtime uncertainty.
- M003, 1500003835: Serp thinks IsOptional is ineffective and harmless on an owning main without a parent. Do not infer failed-main consumption from this flag. Q005 now distinguishes a no-op XML registration while active from fresh registration after full completion; Lua concurrent registration is separate.

Serp's follow-up resolves XML/Lua registration and saved code refresh and assesses nested optionality as very likely. Remaining uncertainties are the interrupted timer (M002), owning-main optionality assessment (M003), direct self-registration during its own action list, and source-specific ForceBuild/movie/session timing. These are not newly detected mod defects. Full source positions and certainty are in [six mod walkthroughs](trigger-mod-walkthroughs.md) and [case outcomes](triggers/mod-cases/review-outcomes.json).

## Q007: MutualArea, quest linking and Threshold follow-up

**Status: answered by Serp on 2026-10-03 with explicit certainty differences. No new game test.**

- ConditionMutualAreaInSubconditions simultaneous subconditions: **very likely correct, not absolutely certain**, according to Serp. Original comment: Outdated_shared_AreaBuffsHelper (Serp)/data/config/export/main/asset/assets.xml:50–53; HowTo.xml:859. The tested main-condition/same-level arrangement remains the scope.
- Quest-linked object flags: **still unclear** whether LinkAllQuestActionsToQuest and LinkAllActionsToQuest are both required or one is sufficient (HowTo.xml:1142–1143). The combined example is evidence of that combination only.
- ConditionThreshold: Serp reaffirmed all CodeSnippets.md:702–710 comments. Preserve their exact qualifications: reported 23-fold execution, reset/subtrigger failures and text-source contexts; positive ThresholdDuration values working and milliseconds as the unit remain **probable, not confirmed**.

Exact original paths, lines, hashes and direct-user-answer certainty: [condition clarification receipt](triggers/condition-clarifications.json). Guidance: [condition selection](../gameplay/trigger-conditions.md). T004–T006 were answered by Serp: QuestStarted pool/action distinction is a reasoned hypothesis, not further tested; ForceBuild usability is conditional on all clients executing in exactly the same tick, without a new different-session test claim; CorporationDifficulty probably fails in MP and was not further tested. Retain these certainty limits. Known failed experiments are not automatically treated as new mod defects.

## Q008: remaining attractiveness and third-party inventory questions

**Status: answered by Serp on 2026-10-03: no newer findings; HowTo is the latest known state. Runtime uncertainty and original qualifications remain.**

- T007, HowTo.xml:1844–1848: ConditionAttractiveness/CountAllTypes did not trigger in the recorded test; summing types versus checking individual types is uncertain. PlayerCounter/Attractiveness is proposed for island totals, not marked as a successful matching test. Serp has no newer findings; neither the interpretation nor the proposed alternative is newly confirmed.
- T008, HowTo.xml:1857: adding goods/items to third-party ships may require two full trigger executions, explicitly not merely two actions. Serp has no newer findings; the tentative two-execution observation remains current and its cause is still unknown. The separately reported post-spawn-trigger workaround does not resolve this case by itself.

Exact source paths, lines and hashes: [condition clarification receipt](triggers/condition-clarifications.json). Both clarification requests are answered. No mod defect or new runtime result is inferred; no new answer is required to retain the documented uncertainty.

## Historical and context differences

| Statements | Interpretation and evidence |
| --- | --- |
| Loader 10 says repeated-name merge nodes are unsupported; later docs permit list merges. | A dated change: GU17.1 restored occurrence-based list merging. The pinned recursive merge has an index per node name. This still does not provide key-based list merging. |
| Early Lua guide says Coop duplication cannot be prevented; newer helpers offer peer identification. | The early statement predates the advanced helper solution. Ultra adds an intrusive peer-initialization procedure, rather than a newly discovered ordinary native host/peer getter. Full helper review remains pending. |
| Loader 11 document calls its features proposals. | Do not use that wording alone as release evidence. Compare the stable implementation, current 1800-labelled reference and deployed workspace examples for each capability. |
| GU17 update guide reports broken key bindings and startup UI changes. | A historical update warning. It does not establish that they remain broken in every subsequent game build. Preserve the caveat until the relevant local test/example is reviewed. |
| Inheritance guide mentions a different 2020 description of empty scalar tags. | Serp reports later tests showing inheritance for empty scalar tags. The older forum must still be read before claiming the historical disagreement is completely resolved. Vector/list clearing is a separate behavior. |

## Editorial defects found during research

These are not alternate supported APIs; never copy the defective example unchanged.

- The current InfoTips reference has unmatched `ElementType` tags in its 1800 example. Compare the decoded vanilla XML rather than reproducing those tags.
- The inheritance guide's mixed-vector example contains an unmatched `Item` boundary. Its illustrated GUID `1111111111111` is also an explanatory placeholder, not a suitable 32-bit mod GUID.
- A compatibility-guide duplicate-removal example contains `position() &amp; last()`, which decodes to an invalid XPath operator. Supported comparison syntax must be taken from a valid example and checked independently.
- Several current-reference examples carry 1800 labels while still using short attributes, or contain a malformed XPath step such as `//ModuleOwner/[...]`. Check the actual legacy form and XPath grammar against the pinned implementation.
- The Basic Types reference's 1800 Replace examples select a container (`/Values/Standard` or `/Values/BuildingBaseTiles`) but supply only its child. This replaces the container with that child. Use a complete matching container or select the leaf; see [offline assertions](offline-validation.md).
- The XPath cheat sheet includes XPath 2.0 `ends-with()` and malformed omitted-node-test steps such as `//[@id=...]`. These are not authoritative syntax for the loader's XPath 1.0 evaluator. Use `//*[@id=...]`, and establish relative versus document-wide predicates explicitly.

Additional discrepancies will be added as complete source review proceeds. No unreviewed topic is implicitly certified by this register.

## Q009: interpreting savegame code revisions, fields and peer counts

**Status: bounded offline findings recorded on 2026-10-25; causal/runtime questions remain open.** See [reading workflow](../gameplay/savegames.md), [historical Campaign case evidence (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/savegame-audit.json) and [source/excerpt evidence (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/savegame-audit.json).

- Release 1.021 (2025-10-18) and current workspace metadata both say 1.021, but the published package still has the incorrect New World Skip/default target 1500004391; workspace uses 1500004336. The inspected headers record mod identity without a concrete mod version. Release-date attribution assumes the user's latest-release premise, while saved callbacks prove only the actual code stored in each instance.
- Mixed saved definitions are directly observed: 150784 retains old callbacks while 150695 still contains a registration of 153242 removed in the workspace. The current one-off refresh of 150784 does not refresh the whole chain or recreate missed events. This reinforces the snapshot warning in Q005; it is not a new test contradicting Serp's XML/Lua registration distinction.
- `a7s_all_serp.xml` explicitly guesses some types from byte size. Its PinnedResources string conversion emitted XML 1.0-invalid character references. Retain raw bytes; do not label the save corrupt or certify a write-back format from a recovered XML parse. FileDBReader can also return zero with a file-in-use diagnostic and no usable output.
- Three configured human account assignments in Autosave 59 contrast with one in later test saves. PeerToSessionMap retains all three historical entries. Solo testing is a corroborated inference, not a definitive recovered online count. Serp said corrections were probably attempted alone; exact repair commands and their responsibility for duplicate instances remain unknown.
- New World movie choice/banner display were not remembered. Autosave 73 contains duplicate active quest instances, while Autosave 78 lacks the first quest and has an armed film listener. Different test branches must not be interpreted as one continuous execution trace. A clean current-code Play/Skip test and a progress-aware blocked-save repair remain unperformed.


Q009 follow-up, 2026-10-25: Campaign 1.022 includes the bounded current-source corrections verified by [the full offline evaluator receipt (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/campaign-1.022-validation.json). Serp excludes retroactive save repairs. Historical release/saved-code observations above remain evidence for their original snapshots; they are not the active review backlog. Comment-only speed scripts remain disabled after [caller/history inspection (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/movie-speed-callers.json); the exact original intent was not recovered. No new game/Coop test.
