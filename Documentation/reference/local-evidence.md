# Summaries of historical local evidence

These summaries preserve reusable findings previously linked only to Serp's local CodeReview folder. They are **reported historical source/offline findings**, not newly repeated audits or game/MP tests. Original reports are not included or assumed available. [Consolidation source records](consolidation-sources.json) identify the inspected original snapshots by hash. Users audit their own current Vanilla and mod files before implementation.

## Savegame audit

Original: `CodeReview/Campaign-in-Coop-Serp/evidence/savegame-audit.json`, 2026-10-25. Eight extracted saves and three complete condition-key/GUID cross-checks informed the bounded [read-only workflow](../gameplay/savegames.md) and [Q009](discrepancies.md#q009-interpreting-savegame-code-revisions-fields-and-peer-counts).

- Current mod metadata, a release package, current source XML and definitions stored in a save are different identities. Equal version labels do not prove equal contents. Mixed historical trigger snapshots were observed in the inspected saves.
- A converter's exit code is insufficient: the inspected FileDBReader could return zero after a file-in-use diagnostic without usable output. Validate actual files and parsing results. Guessed field types and invalid XML character references do not prove save corruption or a safe write-back format; retain raw bytes.
- Historical peer/session entries do not establish the currently connected peer count. Different test branches cannot be combined into a continuous execution trace. Unknown repair commands or remembered choices must remain unknown.

No saves, account identifiers, general save editor or repair certification are supplied here. Fresh registration versus existing saved definitions retains the qualifications in [Q005](discrepancies.md#q005-trigger-composition-and-registration-boundaries).

## Trigger comparison

Original: `CodeReview/Campaign-in-Coop-Serp/evidence/campaign-trigger-comparison.json`, 2026-10-25. Relevant contracts and complete native/effective assets were recorded for the Campaign review.

A replacement event must preserve the owning condition's other relevant settings and native cancellation/progression semantics. The historical review found a lost MutuallyExclusive setting and a source-supported lifecycle counterexample involving moved registration/timers. A valid XPath match alone cannot establish equivalent gameplay. The earlier report is unavailable here; this summary does not promote it into a universal timer rule or a new runtime reproduction. See [trigger design](../gameplay/triggers.md) and historical KIT018.

## Campaign validation

Original: `CodeReview/Campaign-in-Coop-Serp/evidence/campaign-1.022-validation.json`, 2026-10-25. Bounded current-source corrections were checked with the full offline evaluator in helper -> Story -> Campaign order. The historical check retained all 96,272 asset identities. [Q009](discrepancies.md#q009-interpreting-savegame-code-revisions-fields-and-peer-counts) retains the release-versus-snapshot distinction.

That receipt describes its captured local revision, not the later state of a GitHub branch or existing saves. Retroactive save repairs were excluded. No new game/Coop test was performed.

## DLC gates

Original: `CodeReview/Campaign-in-Coop-Serp/evidence/dlc-gates-validation.json`, 2026-10-25. The audit followed native ownership/reference chains, state definitions/examples and relevant defaults; its follow-up evaluator comparison found four additional DLC-filter changes while preserving other compared data.

A gate intended to remain open after an optional quest starts must account for relevant completed/aborted states, rather than assuming a transient Active state is retained. Pre-active Triggered is separate. Preserve native DLC/population/timer prerequisites and inspect late consumers; this is a feature-specific lesson, not a universal flag recipe. Consult the user's actual native definitions before implementing it.

The report also retained Serp's recollection that a prior movie experiment may have left ordinary background simulation speed unchanged. This is recollection, not a verified command guarantee. Historical KIT020 records both scopes; no game/MP attribution was established.

## Movie speed

Original: `CodeReview/Campaign-in-Coop-Serp/evidence/movie-speed-callers.json`, 2026-10-25. Caller/history inspection found 18 play-trigger callers, existing author timing/MP warnings and speed scripts containing comments only since their first Git revision. Disabled files do not establish the effect of a working speed command or justify reactivating it. The original intended experiment was not recovered.

The source-specific risk concerns coroutine timing, local sessions and multiplayer exits. Keep the disabled-script observation separate from API behavior and the later recollection above. See [reviewed mod walkthroughs](trigger-mod-walkthroughs.md).

## Open review

Original: `CodeReview/Campaign-in-Coop-Serp/README.md`, inspected local snapshot dated 2026-10-25, Campaign 1.023 / Story 1.032. C005 identified diary-open listener 150862 using EnterUIState / TextPopup as a reachable synchronization risk. No desync was reproduced in that workflow; the same-tick opening premise remained untested. Pending runtime work included fresh progression, New World Play/Skip and actual multi-client tests.

This is a dated review snapshot, not a live issue list or certification of the public release. The [published baseline comment](https://github.com/Serpens66/Anno-1800-Mods/blob/88821b04ee972424667178d35a5080a753a853d0/YouKnowWhatYouDo-Mods/Campaign%20in%20Coop%20%28Serp%29/data/config/export/main/asset/AntiDesync/ADLeaveUI.include.xml#L8) supplies public context. [Composition results](validation/mod-compatibility/results.json) remain structural evidence only.
