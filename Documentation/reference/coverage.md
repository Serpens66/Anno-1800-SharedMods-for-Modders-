# Coverage and continuation ledger

## Current state

This is a working knowledge base, **not yet the fully completed documentation requested by Serp**. Counts describe inventory/extraction, not complete semantic understanding.

- Inventory pass regenerated with additional authoring sources, BUILD files and disabled `.json_` tests: 11,136 sources; 583 metadata files; 3,104 URL occurrences. These are inventory counts, not review counts. The explicit review ledger currently contains 994 source-specific records (including narrowly scoped trigger-topic records); partial-review statuses are retained.
- Vanilla extraction: 96,102 top-level GUID-bearing asset records; 27 selected assets, 23 template contracts and 71 property contracts. Selected defaults, datasets, localization and infotip examples are also recorded.
- Loader `stable/anno1800`: all seven `doc/*.md`, XML operations/loading order, automatic/binary serializers, historical external-file-loader/mod-manager/cache, Python startup wrapper and all XML fixtures/runner/generator/BUILD files have been read. Six concrete feature-history diffs were read. See loader-history-and-tests.md for boundaries; remaining relevant history/linked-resource checks are still tracked.
- Current website source: all17 Markdown chapters read, including Basic Types in a complete reread. Source commit recorded; game labels and defective examples reconciled. Recursive linked-resource review and chapter-specific coverage cross-check remain. Anno117-only features are excluded.
- Guide: inheritance, compatibility, GU16/GU17 updates, AI, variations, initial mod structure/tooling, Lua execution/read-after-write/problems and infotips have been reviewed. Large command catalogues, tutorials, graphics guides and external linked sources are not complete.
- Personal notes: all2862 XML-notebook and867 Lua-notebook lines read completely. Outcome register now records tests, corrections and speculation; remaining gameplay contracts/topic transfer remain separate from reading completion.
- Workspace mods: inventory entries byte-scanned; LuaLight, Medium, Ultra startup/save, complete ObjectFinder, CoopCount and peer implementations reviewed. Light XML partly reviewed; helper lifecycle XML/dependencies and differing bundles still need full integration review. This is **not** a completed semantic review of all mods.
- Q001 answered on 2026-10-03: Serp has not tested scalar conditions and prefers implementation evidence. The inspected 1800 evaluator requires node sets; the discrepancy register records the source-based conclusion and its runtime/version limits.
- Eight synthetic offline assertions passed in installed GU17.1 xmltest outside the Windows sandbox, including scalar rejection, container replacement, merge/add lists and @GUID context. No game/MP tests. See offline-validation.md.
- Q002 answered2026-10-03: latest socket result is **probably no desync**, still uncertain; exact conditions unspecified.
- Q003 answered2026-10-03: Serp has not tested authoring-tool ModDependencies URLs and requests the code finding. Document ordinary dependency IDs plus Development.Bundle URLs; do not promise the conflicting shortcut.
- Q004 updated2026-10-03: Serp explicitly selects MoneyValue as income per 100 inhabitants per minute, matching the guide. Serp attributes the contrary "residences" wording to German non-native English comment authors; this context is user-provided. Amount retains Serp's assessment that the guide is correct and the unresolved runtime calculation boundary. The decision is not recorded as a game test or engine-code proof.
- All FileDBReader wiki pages, original/successor Blender READMEs, graphics-guide text/code, AddCustomMusic files, iModYourAnno wiki pages, first two tutorial text/code examples and all 12 vscode-anno documentation pages read. Source-specific outcomes and implementation corrections have been added; images, linked resources, remaining tutorials and relevant native contracts remain separate unfinished tasks.
- Two recipes were additionally checked against exact vanilla asset copies in the installed 1800 XML evaluator: radius replacement preserves the remaining asset and new trigger insertion preserves its anchor. These are offline patch assertions, not game/save/MP tests.
- Missing README destinations have been supplied: foundations, Lua lifecycle/API, multiplayer, infotips/text, CFG/FC and basic recipes. Shared helper implementation chapters and personal-test register are also present.
- AGENTS.md received only the authorized short entry-point hint, appended without re-encoding existing bytes.

## Trigger-topic addition (2026-10-03)

- Added design/lifecycle, condition selection, native field/dataset lookup and complete recipe chapters; see [trigger audit](trigger-audit.md).
- Native lookup covers 91 direct-Condition templates, related objectives/selectors, 141 Condition-prefixed property definitions plus supporting contracts. Exact revision counts and hashes are in [extraction summary](triggers/extraction-summary.json) and [native contracts](triggers/vanilla.json).
- Current inventory search reached 3,885 source rows / 879 distinct byte groups with trigger-related text, including both notebooks. The [prose evidence register](triggers/prose-evidence.md) maps 1,354 distinct trigger-relevant quotations to topic guidance; duplicates and non-identical bundles remain distinguishable. These are discovery/topic-evidence counts, not complete integration-review counts.
- Eight complete documentation XML recipes were checked against native structures and the installed XML evaluator; see [results](validation/triggers/results.json). No game/MP execution, independent new-chat agent test or dependency-loading test was performed.
- Q005 updated from Serp follow-up2026-10-03: XML registration is a no-op while active and possible again after full completion; Lua may register concurrent copies; fresh registration snapshots current code. Optional branches exempting non-optional descendants is very likely, not absolutely certain. Direct self-registration remains possible but unconfirmed. Parent gating is confirmed; timer restart remains probable and owning-main optionality an author assessment.
- Existing whole-source review statuses were retained; new source records expressly describe trigger-topic evidence only. Remaining helper/action/quest/system integration work below is not silently marked complete.

- Q007 records Serp condition follow-up2026-10-03: MutualArea simultaneous subconditions very likely, quest-linking minimum flags still unclear, all Threshold comments reaffirmed with original probability qualifiers. T004–T006 answered: quest-start distinction remains a reasoned hypothesis, ForceBuild usability requires identical-tick execution on every client, and CorporationDifficulty probably fails in MP without further tests; see [condition clarification receipt](triggers/condition-clarifications.json).

- Q008 answered2026-10-03: Serp has no newer attractiveness or third-party inventory findings; HowTo remains the latest state with original qualifications. All eight submitted condition questions are answered; remaining uncertainty is not a pending clarification or runtime certification.

## Six real trigger cases (2026-10-03)

[Six mod walkthroughs](trigger-mod-walkthroughs.md) follow 1500003013, 1500003820, 1500003835, 1500001103, 1500004302 and 1500004332 through their relevant definitions, bundled versions, native contracts and caller/consumer patches. All six source payloads and the selected real ModOps passed [offline checks](validation/mod-trigger-cases/results.json). Integration evidence records 178 source hashes and resolved includes; it does not mark every whole mod reviewed. M001–M003 received Serp clarification: parent gating confirmed, timer restart probable but unconfirmed, owning-main optionality assessed as ineffective without a parent. Follow-up clarifies registration entry points and saved code refresh; optional-depth is very likely resolved, with direct self-registration and source-specific runtime qualifications retained. No runtime sign-off, source changes or new game/MP tests.

## Reward-pool topic addition (2026-10-05)

- [Standalone Reward Pool Guide](../../Guide_RewardPools.md) covers pool creation, linking, group references, weights, amounts, target-property restrictions and related pool types.
- [Native audit](reward-pools-audit.json) records source hashes, defaults and the quest 151562 -> pool 151049 -> pool 151062 -> Product chain. XML examples passed parsing/reference/target checks; no loader executable or game/save/multiplayer test was performed.
- Nested sampling, duplicate handling, nonpositive weights, cycles, unlock precedence and missing-region fallback remain unverified. The flat probability example is a qualified relative-weight model; RegionRewardPool has schema evidence but no instance in the inspected main asset set.
- KIT016 tracks deliberate adaptation into the starter kit; this addition does not broaden unrelated source-review statuses.

## Next steps, in order

The [savegame reading addition](#savegame-reading-addition-2026-10-25) below extends offline coverage only; the outstanding whole-mod and runtime reviews remain open.

The [standalone English Trigger Guide](../../Trigger_Guide.md) provides a progressive 18-chapter learning path, nine complete ModOps examples, six reviewed source cases and all 91 captured Condition templates. It now embeds 115 property references with full schema/defaults, 105 native template definitions and all 52 referenced datasets. It has no private documentation references or other-file links; only internal anchors and the two user-approved optional public repository links remain. [Its native audit](validation/trigger-guide/native-audit.json) verifies the opening 130221 counter, every unlock/unhide target and base chain, and relevant templates/properties/defaults/datasets against current source hashes. [Guide validation](validation/trigger-guide/results.json) checks exact in-file reference completeness, actual offline evaluator results, source-preserving case presentations, collapsible XML, links/anchors and four authored design walkthroughs. No game, MP, dependency-loader or independent new-agent test; existing uncertainty remains qualified.

1. Q001 is resolved for documentation purposes from implementation evidence; retain the distinction between this conclusion and an in-game test. Continue recording any new discrepancies separately.
2. Retain review-ledger statuses when regenerating inventory; complete workspace revision and external-source provenance.
3. Loader external/cache/test inspection is recorded. Reconcile remaining loader history and linked implementation coverage. In addition to eight synthetic assertions, 54 unchanged well-formed upstream cases passed offline; seven cases were excluded with concrete reasons.
4. Complete personal-note gameplay transfer and helper XML integration. Algorithm/interface chapters exist for ObjectFinder/CoopCount and Medium/Ultra; verify every resource consumer and distinct bundled version.
5. Read every Anno 1800 guide/tutorial and recursive technical link. Record inaccessible material and source-specific review outcomes.
6. Review unique workspace sources per mod, compare non-identical bundled shared copies, classify WIP/retired examples and document all relevant patterns.
7. Complete feature-specific vanilla audits and gameplay/resource chapters. Expand recipes only after their reference chains are reviewed.
8. Validate links, snippets, CRLF/encoding, examples and representative new-chat workflows. Reconcile the coverage register with every inventory row.

## What counts as complete

A source is not complete merely because it was downloaded, searched, parsed, hashed, indexed or summarized mechanically. A complete review has a source-specific outcome, records applicable game/version/context, reconciles its claims with relevant tests/contracts, and links useful findings to an explanatory chapter or explicitly justifies exclusion.

For duplicated files, a completed review of one identical SHA-256 content group can cover the other copies, while the mod integration and metadata still require review. Different versions of the same shared ModID are not automatically equivalent.

For runtime behavior, preserve the original test's limits. Offline XML/Lua checks cannot establish multiplayer synchronization, UI context or game-specific C-function availability.

## Savegame reading addition (2026-10-25)

- Added [read-only savegame reading](../gameplay/savegames.md), the [Campaign New World case (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/README.md) and [anonymized evidence (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/savegame-audit.json). Eight source saves were extracted; selected managers were read structurally. Three saves also received FileDBReader conversion and exact agreement of all condition-key/owning-GUID pairs (11100, 11116 and 12404 rows).
- Inspected RDAConsole 1.1.0, FileDBReader 3.0.3, local interpreter files/unpack driver, and pinned V2/V3 parser/dictionary implementation. The generated interpreter has guessed types and can produce invalid XML 1.0 character references. This addition does not certify every interpreter rule, nested session or save format.
- Actual release 1.021 retains the wrong New World Skip/default callback, already corrected in workspace XML under the same version. Actual saved definitions retain old callbacks and an older late registration. Current one-off migration does not reconstruct missing progression. Remaining diary/DLC risks and a misplaced TriggerSetup are classified separately in the case report.
- Saved account assignment supports solo repair-test inferences for later saves; PeerToSessionMap is not a reliable connected-peer count. Duplicated quests/listeners do not establish normal Coop duplication or confirm which manual commands were used.
- Source/tool/save hashes, excerpts and decoder validation are retained without complete saves or account identifiers. No mod/save edits, game launch, repacking, repair or new multiplayer test. Full semantic review of every Campaign/Story quest remains open. KIT017 tracks possible portable adoption and is open.


## Campaign vanilla comparison follow-up (2026-10-25)

- Compared explicit-GUID condition replacements with 364 native condition matches, including 150 event matches. The [case report (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/campaign-trigger-comparison.json) and [selected definitions/hashes (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/campaign-trigger-comparison.json) record the scope and two concrete source regressions: lost MutuallyExclusive on 151434 and revival of cancelled 151076 through 150931.
- Traced their native owners, kontor upgrade/base chains, registration/cancellation callers, event sources, resulting actions and applicable templates/defaults/property contracts. Native schema reset wording remains distinct from Q005's runtime clarification. The diary-open source comment is now explicitly retained as a qualification.
- Documentation/evidence only. No mod or save changed, no clean-game/Coop reproduction, no runtime certification of every quest. KIT018 is open; prior KIT017 evidence and adoption/exclusion history remain intact.


## Campaign 1.022 correction follow-up (2026-10-25)

- Campaign 1.022 corrects the lost native child-completion mode, preserves the newspaper reminder's native InitCampaign/quest-cancellation lifecycle using an event-gated timer, and places worker TriggerSetup under Values. Story remains 1.031; no saved-instance migration was added at Serp's request.
- The complete dependency chain passed the actual GU17.1 evaluator. A normalized comparison of all 96,272 resulting assets found exactly five expected changed trigger GUIDs and no added/lost identities. Original range/spawn actions and the native cancellation caller remain intact. [Current source hashes and validation (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/campaign-1.022-validation.json).
- C004 caller investigation found 18 play triggers / 36 script call sites. Both scripts were disabled in their earliest Git revision. Author notes document slow-speed coroutine delays and a separate speed mod's multiplayer-exit guard. Comment-only bodies are not themselves a confirmed bug; no speed change was enabled. [Caller evidence (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/movie-speed-callers.json).
- [CodeReview (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/README.md) now lists only unresolved questions/risks. Existing evidence and past validation receipts are historical snapshots. No new game/MP test or publication. KIT019 is open.


## Persistent DLC milestone follow-up (2026-10-25)

- C006 is corrected in Campaign 1.022: all four final-campaign DLC gates accept Active and later terminal states of optional rebuild quest 153232, including manual/automatic abort. Triggered alone remains excluded. Native state-flag examples and the exact dataset support these names; no new persistent asset or save migration was added.
- The Cape chain 112116 -> 113430 -> 111842 depends on 113818 (700 artisans). A late evaluation after rebuild completion/abort no longer fails solely because Active expired. Existing DLC activation, population/timer and Coop/story-pool requirements remain unchanged. This is a demonstrated source-state defect, not a reconstruction of the recalled external user's specific save.
- A new complete GU17.1 pass preserves all 96,272 assets. Exactly four further gate assets differ from the preceding 1.022 output; the helper/Story XML outputs are identical. [Audit, state membership and validation (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/dlc-gates-validation.json).
- Both speed Lua scripts now document risks and Serp's uncertain recollection that movie-time slowdown left background speed normal. They remain entirely commented; Lua 5.3 syntax passed without executing scripts. Story metadata is 1.032 for this comment update. No new runtime test, save repair or publication. The active review now contains only C005; KIT020 is open.
