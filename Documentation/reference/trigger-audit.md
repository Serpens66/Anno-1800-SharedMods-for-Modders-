# Trigger documentation audit and evidence boundaries

Date: 2026-10-03. Entry points: [design and lifecycle](../gameplay/triggers.md), [condition selection](../gameplay/trigger-conditions.md), [native fields](../gameplay/trigger-condition-reference.md), [datasets](../gameplay/trigger-datasets.md), [worked recipes](../gameplay/trigger-recipes.md).

## What was examined

The documentation previously had a one-shot startup recipe and notebook outcome tables, but no combined trigger-design chapter. This pass reconciles the trigger-specific notebook observations and corrections, shared-helper usage comments, CodeSnippets and workspace trigger comments into the chapters above. [Original source-comment evidence](triggers/prose-evidence.md) preserves individual excerpts, locations and their documentation destinations, including contextual, WIP and rejected approaches. Original-language quotations are retained; explanatory prose is English.

[Workspace extraction](triggers/workspace.json) stores paths, SHA-256, encodings, byte-identical source groups, comment origins, and a trigger-shape index. [Extraction summary](triggers/extraction-summary.json) distinguishes discovery counts from semantic review. The scan includes every applicable current source-inventory row in the workspace and both notebooks, plus a live filesystem check for new supported source files. It is not limited to the named examples. Comments without trigger keywords are retained in the machine record to preserve surrounding context. Non-identical bundles remain separate groups. This record does not certify complete whole-mod integration, every action consumer or unrelated feature code.

[Native contracts](triggers/vanilla.json) contain the exact five primary source revisions, 91 templates with a direct Condition property, related templates, 141 Condition-prefixed property definitions plus supporting/action contracts, corresponding property and container defaults, datasets, explicit-template native example owners and their captured base chains. Schema-only conditions and quest/object-specific properties are deliberately kept even when no same-named native Condition template exists. The generator scans the complete main assets.xml for representative explicit-template occurrences. An empty sample list is **not proof of no native use**: IsBaseAutoCreateAsset and inherited/inline Values may omit Template.

The completed native audit for the **core structure and documentation recipes** covers Trigger/AutoCreateTrigger/FeatureUnlock/UnlockableAsset, Condition/negation, Timer/AlwaysTrue/Event/Unlocked/ActiveSession, TriggerSetup, register/reset/unlock/lock actions, their template overrides, property/container defaults and enums. The new examples use mod-owned locked signals/results; no existing gameplay asset is changed. Anchor 130248 is an independent Trigger whose complete original owning record is retained for preservation checks. Session 180023 is explicitly SessionModerate with no BaseAssetGUID; Human0 signal 1500001613 is a **WhichPlayer_Serp helper**, not a native asset.

The catalogue is a structural lookup for other features, not a completed gameplay audit of every achievement, tutorial, spawning, graphics or quest system represented by its sample owners. Before a new consumer changes those systems, follow its exact relevant reference chain, inherited values and action resources. No native game-engine implementation for the disputed runtime algorithms was supplied by the extraction. Source-file descriptions are never labelled engine-code proof.

The sole standalone XML parse diagnostic is in `notes:HowTo.xml`: a double hyphen inside a notebook comment at line 29. The original notebook is retained as prose evidence, not treated as loadable mod XML, and has not been repaired. All other selected unique XML source groups parsed structurally; this does not execute includes, inheritance or gameplay.

## Reconciled source families

Paths below are workspace-relative unless explicitly marked external. Source hashes and exact per-comment lines are in the linked records.

| Source family | Findings transferred / classification |
| --- | --- |
| External `HowTo.xml`, especially 816–959, 968–1015, 1020–1175 and later trigger/counter/event sections | Saved/fired identities, remembered subcompletion, completion modes, optional-depth reversal, MutualArea exception, dynamic context corrections, item/event/counter and MP tests. Tests retain their original qualifications; superseded experiments are not promoted to recipes. |
| External `Python Modding/info.txt` | ActionExecuteScript multiplicity, trigger/Lua handoff, local context, counters/pools, GUI/notification/movie tests, same-process save-loading limits. Existing Q002 uncertainty remains unchanged. |
| `SharedMods/CodeSnippets.md` [GitHub](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/blob/3aece64f299365309aaf1f7a57f28e2f6900f106/CodeSnippets.md) | Chance branches; Threshold failures and exact 23-execution observation; smallest-unlock-trigger-GUID display; human AreaBuff quest design; AI marker limitations; MutualArea placement and qualified timing. Current and OLD solution sections remain distinguished. |
| `shared_IsAIPlayer_Condition`, `shared_WhichPlayer_Condition`, `shared_WhichModPlayer`, `shared_CheckSingleHuman` | Positive identity signals, readiness before negation, unsupported identities, initialization and count/Coop distinctions. ModID, metadata and template dependencies must accompany the example. Different bundled versions are not treated as interchangeable. |
| `shared_PlayerKnownAndInGameCheck/IMPORANT.txt` [GitHub](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/blob/3aece64f299365309aaf1f7a57f28e2f6900f106/shared_PlayerKnownAndInGameCheck/IMPORANT.txt) and assets | Dead/nonexistent CheckedParticipant counter always false; persistent AI flags cannot update after defeat; processing-human loss and owned-object alternatives. Its warning overrides a naive use of the helper's name. |
| `shared_PirateDefeatHelpers`, `shared_PirateExtraSpawn`, PirateComebackFleetFix | LaFortune/IsParticipantInGame failures; state-based specialized consumers; saved-helper extension migration; optional branches, participant coordinator and re-registration caveats. Explicit source corrections retained. |
| `shared_TickActions`, `shared_EventOnGameLoaded`, `shared_OncePerSession_xml`, `shared_OncePerSessionPerSaveLoad` | Timer intervals/readiness; reset extension points; once-ever versus once-per-save-load; prior consumers on an existing save; global-buff session visitation; Medium replacement/load-order boundary. These are established helper workflows, not newly tested in-game here. |
| `shared_LuaLight`, Medium/Ultra, their templates, scripts and bundled copies | Lock-to-start bridge versus locked-presence guard, script dispatch, callback readiness, synchronized handoff, local state and Coop registration duplication. Existing integration-pending statuses are preserved. |
| BT Passive Trading / MoreTradeForHumans / speed-buff files / BT Quests Instead Preferred | Delayed GUID change to allow completion/reset; periodic reapplication instead of IsBuffed; ProfileCounter on third parties; pool sum; quest-local running-precondition cancellation replaces old trigger cancellation. |
| Campaign in Coop / Story Quests in Coop, AntiDesync and Conditions files | Local-event/state divergence; registration timing; event versus persistent state; timer/lock replacements at audited show/open points; preserving SubConditionCompletionOrder when changing condition type; separate save-fix identities. GUID-specific fixes are examples, not universal GUI rewrites. |
| Diplomacy Sabotage, Specialised Islands, shared PopUp and Outdated_AreaBuffsHelper | Extensive context/spawn/inventory/optional-marker observations. WIP/outdated identity, failed branches, comments saying TODO/test, and subsequent simpler solutions remain explicit. Do not silently adopt the obsolete whole workflow. |
| Pirates Flak Trigger / Towing Ships (will not work) | ShipsInRange target/pool/registration issues, ObjectPosition alternative, ObjectAttached versus ObjectDropped observation. Towing is explicitly unsuccessful. |
| Other indexed workspace trigger/comment applications | Retained in the source-comment register with source-specific wording and destination. Infotip VisibilityElement, ModOp Conditions, Diplomacy SpecialTrigger/Reactions and generic "trigger" references are separate consumers or contextual applications, not independent gameplay-trigger contracts. |

## Known unresolved contracts

See [Q005](discrepancies.md#q005-trigger-composition-and-registration-boundaries): Serp confirms parent gating, XML no-op registration while active, fresh registration after full completion, Lua concurrent copies and current-code snapshots on fresh registration. Optional level-two branches exempting non-optional level-three descendants is very likely, not absolutely certain. Direct self-registration during its own actions is possible but unconfirmed. These are author clarifications, not newly performed game tests or inspected engine-code proof.

Other uncertain observations remain next to the affected condition/action: Threshold units/positive durations (still probable), MutualArea simultaneous behavior (very likely, not certain), timer/context transfer, numeric EvaluateTextSource comparisons, pirate/session refresh, Attractiveness/Fertility/MP-difficulty tests, popup and local movie tests, item/socket detection and quest-linked object filters. An asset/schema's existence does not waive those limitations.

## Validation and acceptance

The root [Trigger Guide](../../Trigger_Guide.md) presents the reviewed knowledge as a self-contained progressive English tutorial. The in-file appendix embeds the full schema/default and dataset reference needed by the catalogue; only the two user-approved optional public repo links leave the guide. Its [native opening audit](validation/trigger-guide/native-audit.json) adds complete target/base coverage for 130221. Its [guide-specific checks](validation/trigger-guide/results.json) cover exact embedded reference completeness, complete ModOps, source-preserving real-case presentations, catalogue, collapsible blocks, links/anchors and authored reader scenarios. These remain offline checks; the guide does not upgrade uncertain findings or expand this audit into every condition consumer.

[Offline results](validation/triggers/results.json) record eight complete XML recipes patched with the installed Anno 1800 evaluator, native template/property/dataset checks, complete-anchor preservation and source hashes. [Recipe walkthroughs](../gameplay/trigger-recipes.md#walk-through-a-design-using-only-this-documentation) state the expected design and failure modes for representative new-chat tasks. They are reasoning checks against the documentation, not independently executed game simulations or a new-chat agent test.

The acceptance boundary is a usable, traceable design chapter, condition lookup and known-exception register. Discovery counts, indexed original comments and rare native sample owners do not imply that every mod or every represented secondary subsystem received a complete integration/runtime review. Coverage remains explicit rather than silently upgraded. No mod code, source comments, AGENTS.md or vanilla file is changed by this task.

## Reproducing the documentation checks

Run the tools with the configured Python runtime and lxml available, from the workspace root:

1. `Documentation/tools/audit_triggers.py` captures native revisions and workspace evidence. Extraction does not certify semantic review.
2. `Documentation/tools/build_trigger_reference.py` and `Documentation/tools/build_trigger_examples.py` rebuild the condition lookup, datasets and complete examples.
3. `Documentation/tools/integrate_trigger_evidence.py` rebuilds original quotations/destinations and adds scoped records without replacing overall review outcomes.
4. `Documentation/tools/validate_triggers.py` checks native contracts and invokes the configured local 1800 XML evaluator. Its private GUID bindings are fixture values, not deployed mod allocations.
5. `Documentation/tools/validate_docs.py` checks file links/XML snippets and normalizes UTF-8 Documentation files to CRLF. `Documentation/tools/verify_trigger_documentation.py` checks linked heading fragments, source hash preservation and documentation encoding/line endings.

`link_trigger_chapters.py` and `finalize_trigger_docs.py` are idempotent integration helpers for the existing entry points/register prose. If source revisions change, repeat the relevant semantic audit and update the scoped prose/counts; regenerating JSON alone does not renew a review.

## Follow-up: six real mod cases

[Six real walkthroughs](trigger-mod-walkthroughs.md) extend this catalogue-based pass with relevant selected-mod integration and caller/consumer audits. [Case outcomes](triggers/mod-cases/review-outcomes.json) and [offline results](validation/mod-trigger-cases/results.json) distinguish explained source structure from M001–M003 author clarifications (confirmed gating, probable timer restart, assessed owning-main optionality) and retained runtime limitations. They do not upgrade the broad workspace extraction to a whole-mod certification.
