# Starter-kit transfer register

This workspace retains detailed research; the starter kit receives selected, portable adaptations. Record kit-relevant new or corrected findings here so transfer decisions are not lost between chats. This register tracks adoption, not semantic review or runtime certification.

## Status and history rules

- `open`: a transfer decision or update is outstanding. It may still need research; open does not mean ready to publish.
- `adopted`: the stated scope was adapted, checked and committed to the kit. Preserve evidence qualifications and the exact destination/date/commit.
- `excluded`: consciously outside the current kit scope, with a reason. Exclusion is reversible and is not a claim that the topic is incorrect or fully researched.
- Give each new finding a stable unused KIT number. Keep previous IDs and adoption receipts. For a later correction, create a new `open` entry linked to the prior ID; do not erase its historical commit or imply it includes the correction.
- Before changing a status to adopted, compare relevant evidence, update the kit deliberately and run appropriate checks. Hash differences alone establish change, not the content or urgency of a finding.

## Initial adopted scope

Research baseline: 2026-10-03; adaptation date: 2026-10-04. All twelve entries below are **partial curated adaptations**, not complete chapter exports. Their source hashes are retained in the [original kit adaptation manifest](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/reference/adaptations.json). Baseline commit: [1a2f3f6](https://github.com/Serpens66/ModdingWithCodex/commit/1a2f3f68eabf3172967a4388de473b181aae6257).

| ID | Adopted finding / scope | Research evidence | Kit destination at baseline | Status | Adoption receipt |
| --- | --- | --- | --- | --- | --- |
| KIT001 | Feature-specific audit, source roles and unknown-contract handling; not the complete extracted reference database. | [Source](../foundations/vanilla-research.md); baseline SHA-256 in adaptation manifest | [Documentation/foundations/vanilla-research.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/foundations/vanilla-research.md) | adopted | 2026-10-04; baseline commit |
| KIT002 | Selected scalar/vector inheritance rules with Serp-test and historical qualifications; detailed native examples omitted. | [Source](../foundations/inheritance.md); baseline SHA-256 in adaptation manifest | [Documentation/foundations/inheritance.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/foundations/inheritance.md) | adopted | 2026-10-04; baseline commit |
| KIT003 | Selected layout, metadata, dependency/order and installation boundaries; not every loader-history case. | [Source](../foundations/structure-and-loading.md); baseline SHA-256 in adaptation manifest | [Documentation/foundations/structure-and-loading.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/foundations/structure-and-loading.md) | adopted | 2026-10-04; baseline commit |
| KIT004 | Identifier namespaces, reservation cautions and selected tool boundaries; no complete enum/resource catalogue. | [Source](../foundations/identifiers-and-tools.md); baseline SHA-256 in adaptation manifest | [Documentation/foundations/identifiers-and-tools.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/foundations/identifiers-and-tools.md) | adopted | 2026-10-04; baseline commit |
| KIT005 | 1800 setup/evaluator selection and selected authoring-tool discrepancies; not the full build/converter review. | [Source](../foundations/authoring-tools.md); baseline SHA-256 in adaptation manifest | [Documentation/setup.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/setup.md) | adopted | 2026-10-04; baseline commit |
| KIT006 | Selected legacy operations, lookup contexts, conditions, includes and warning semantics; executable gameplay examples omitted. | [Source](../xml/modops.md); baseline SHA-256 in adaptation manifest | [Documentation/xml/modops.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/xml/modops.md) | adopted | 2026-10-04; baseline commit |
| KIT007 | Selected XPath/node-selection patterns and inheritance/version boundaries; no complete XPath manual. | [Source](../xml/xpath.md); baseline SHA-256 in adaptation manifest | [Documentation/xml/xpath.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/xml/xpath.md) | adopted | 2026-10-04; baseline commit |
| KIT008 | Selected Content timing, repeated-name merge and list-shape cautions; full production recipes omitted. | [Source](../xml/content-and-lists.md); baseline SHA-256 in adaptation manifest | [Documentation/xml/content-and-lists.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/xml/content-and-lists.md) | adopted | 2026-10-04; baseline commit |
| KIT009 | Evidence categories and abbreviated coverage/exclusion boundaries; original inventory counts and full continuation ledger omitted. | [Source](coverage.md); baseline SHA-256 in adaptation manifest | [Documentation/reference/coverage.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/reference/coverage.md) | adopted | 2026-10-04; baseline commit |
| KIT010 | Q001/Q003, tool differences and inherited-wording cautions; advanced unresolved topics only summarized. | [Source](discrepancies.md); baseline SHA-256 in adaptation manifest | [Documentation/reference/discrepancies.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/reference/discrepancies.md) | adopted | 2026-10-04; baseline commit |
| KIT011 | Validation layers, actual evaluator invocation and historical-test limits; private fixtures/logs not distributed. | [Source](offline-validation.md); baseline SHA-256 in adaptation manifest | [Documentation/reference/validation.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/reference/validation.md) | adopted | 2026-10-04; baseline commit |
| KIT012 | Bounded scalar-edit research and offline evidence, plus the audit-first workflow; Lua/trigger recipes not adopted. | [Source](../recipes/basic-workflows.md); baseline SHA-256 in adaptation manifest | [Documentation/reference/radius-audit.md](https://github.com/Serpens66/ModdingWithCodex/blob/1a2f3f68eabf3172967a4388de473b181aae6257/Documentation/reference/radius-audit.md) | adopted | 2026-10-04; baseline commit |

## Current exclusions

| ID | Topic / evidence | Kit topic | Status | Reason |
| --- | --- | --- | --- | --- |
| KIT013 | [Lua execution](../lua/execution-and-lifecycle.md), [shared helpers](../lua/shared-light.md), [multiplayer](../multiplayer/synchronization.md) | Complete Lua/shared-helper guidance | excluded | The first draft focuses on small XML mods; no complete helper stack or synchronization certification is shipped. |
| KIT014 | [Trigger design](../gameplay/triggers.md), [recipes](../gameplay/trigger-recipes.md), [trigger audit](trigger-audit.md) | Complete trigger/quest guidance | excluded | Specialist workflow is outside the first draft; selected cautions do not constitute adoption of the full guide. |
| KIT015 | [Graphics](../ui-and-resources/graphics-toolchain.md), [binary formats](../ui-and-resources/binary-formats.md), [audio example](https://github.com/Serpens66/Anno1404SoundsTo1800) | Complete graphics/audio guidance | excluded | Requires separate tools and feature contracts; public repository links are optional reading, not a bundled workflow. |

## Open transfers

No additional research transfer was identified when initializing this register on 2026-10-04. Add concrete new/corrected findings with ID, evidence, destination, status and any blocker. The documentation-maintenance changes below introduce no new gameplay finding or runtime evidence.

### KIT016: Reward-pool data contracts (2026-10-05)

- Status: `adopted` for the bounded reward-pool guide and portable audit. Initial entry was `open` on 2026-10-05; that initial state involved no kit adoption or synchronization.
- Evidence: [English guide](../../Guide_RewardPools.md) and [native audit, source hashes and structural checks](reward-pools-audit.json).
- Findings: distinguish RewardPool/RewardItemPool templates from their shared property; separate ItemLink target restrictions from the broader quest RewardAssets field; preserve entry defaults, group-ID semantics, ignored quantities on pool links and uniqueness controls.
- Boundaries: nested sampling probabilities and runtime edge cases remain unverified; regional pools are schema-only in the inspected main asset set. XML parsing/reference checks are not a loader or game test.
- Relationship: extends the small-XML scope of KIT012; does not change KIT014's exclusion of complete quest guidance.
- Adoption receipt: 2026-10-05, exact local kit commit `5382e3974c39cfa93e7434b932ae2ff7a15dafc9`. Destinations: `Documentation/gameplay/reward-pools.md` and `Documentation/reference/reward-pools-audit.json`, linked from the kit index, coverage and research-state page. Original guide retained; private audit paths adapted to extraction-relative paths.
- Checks: unchanged native-source hashes; all five existing Structure tests passed (JSON/template, links, portable content, skills, UTF-8/CRLF); Git whitespace check passed with CRLF-aware settings. No new loader/game/save/MP test. Local commit only; no push/publication performed.

### KIT017: Read-only savegame inspection and revision diagnosis (2026-10-25)

- Status: `open`; no kit files changed, no adoption receipt, publication or synchronization.
- Evidence: [savegame workflow](../gameplay/savegames.md), [Campaign New World case (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/README.md) and [anonymized source/check record (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/savegame-audit.json).
- Candidate portable scope: separate RDA extraction, outer zlib and FileDB interpretation; preserve unknown raw types; validate actual outputs; distinguish active mod identity, release package, workspace XML and saved definition snapshots. Preserve the limits of saved peer/account/session records.
- Relationship: linked to KIT014 (complete trigger/quest guidance excluded) and KIT015 (complete binary/graphics tooling excluded). This entry does not reverse those exclusions or declare a general save editor suitable for the starter kit.
- Pending decision: deliberately adapt a bounded read-only recipe and its evidence qualifications, or record a specific exclusion reason. Keep private saves/account identifiers out of a portable kit. Do not mark adopted before appropriate kit checks and an exact dated kit commit are recorded.
- Validation boundary: eight extracted saves, three full condition-key/GUID cross-checks and bounded structural example checks; no new game/Coop test, repacking or repair certification.

### KIT018: Preserve native condition and cancellation semantics (2026-10-25)

- Status: open; no kit adaptation, publication or synchronization.
- Evidence: [Campaign vanilla comparison (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/campaign-trigger-comparison.json) and [native/effective excerpts and source hashes (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/campaign-trigger-comparison.json).
- Candidate portable finding: replacing an unsafe local event must preserve owning Condition settings such as MutuallyExclusive; moving registration to support a timer must retain native cancellation and progress semantics. A correct XPath match does not prove equivalent behavior.
- Relationship: extends KIT014's trigger topic and KIT017's distinction between current and saved definitions. It does not reverse KIT014's exclusion or provide a tested save migration.
- Boundaries: one confirmed lost setting and one source-supported lifecycle counterexample; no new game/MP reproduction. Decide deliberately whether a bounded caution belongs in the kit; retain an exact dated commit and checks before adoption.

### KIT020: Persistent post-story gates and qualified speed recollection (2026-10-25)

- Status: open; no kit adaptation, publication or synchronization.
- Evidence: [DLC native-chain/state/validation record (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/dlc-gates-validation.json); current [open review (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/README.md).
- Relationship: follows KIT019 and KIT018; the complete trigger/Lua topics remain bounded by KIT014/KIT013. Retain previous IDs and receipts.
- Candidate portable lesson: a milestone gate intended to stay open after an optional quest starts must not accept only transient Active; include the relevant completion/abort states while excluding pre-active Triggered. Parent prerequisites and late quest-pool evaluation prevent assuming that every listener remembered Active. Preserve native DLC/population/timer requirements.
- Boundaries: state names/flags checked against native contracts/examples, actual whole-asset XML patch and exact four-asset follow-up diff verified. No game/MP test or attribution to the recalled user report. Serp's belief that a prior movie experiment left background simulation speed unchanged is recorded as recollection; it is not a new verified command guarantee.

## Maintenance receipt

- 2026-10-04: initialized this register and the portable kit research-state page. The initial research-source hashes remain historical and unchanged.
- Kit documentation-maintenance commit: [8f4ebfa](https://github.com/Serpens66/ModdingWithCodex/commit/8f4ebfa6d37a3e7544045889a0b775f878686618).
- Checks: local evidence/target/ID mapping, links and preserved text format; existing kit structural checks. No game/save/multiplayer checks were performed for this documentation change.
