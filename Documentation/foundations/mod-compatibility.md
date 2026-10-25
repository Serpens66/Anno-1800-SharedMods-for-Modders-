# Mod compatibility in Anno 1800

Compatibility means that combined mods retain the intended structure and behavior. Valid XML, an error-free patch log and different custom GUIDs are useful checks, but do not establish this on their own. This chapter concerns **interaction between mods**; [savegame snapshots](../gameplay/savegames.md) and [multiplayer synchronization](../multiplayer/synchronization.md) have additional contracts.

Evidence was reconciled on 2026-10-25. [Source excerpts, hashes and classifications](../reference/validation/mod-compatibility/sources.json) distinguish Serp's requirements/comments, historical notes, community recommendations, loader implementation and offline checks. Reading a source for this topic does not certify its whole mod.

## Ensure containers, then append entries

When extending a list whose serialized container may be absent, first merge its empty structure from a parent that exists. Then append the new entries to that container. This is Serp's explicit requirement and the working pattern in the merchant mods (S01, C09-C11).

For the Campaign reminder, the actual 1.023 patch is:

```xml
<ModOp Type="merge" GUID="151076" Path="/Values/Trigger">
  <SubTriggers />
</ModOp>
<ModOp Type="add" GUID="151076" Path="/Values/Trigger/SubTriggers">
  <Item>
    <SubTrigger>
      <Template>AutoCreateTrigger</Template>
      <Values>
        <Trigger>
          <TriggerCondition>
            <Template>ConditionTimer</Template>
            <Values>
              <Condition />
              <ConditionTimer>
                <TimeLimit>10000</TimeLimit>
              </ConditionTimer>
            </Values>
          </TriggerCondition>
        </Trigger>
      </Values>
    </SubTrigger>
  </Item>
</ModOp>
```

The empty merge creates `SubTriggers` if missing. If one already exists, its existing children remain. The add then appends one `Item` inside that list. Adding a complete `SubTriggers` element to `/Values/Trigger` would instead append a second container when another mod supplied one first. This follows the inspected loader and was reproduced in the actual GU17.1 evaluator.

The parent path must exist: merging into a nonexistent target does not create that target or its ancestors. For a deeper missing path, merge the required empty structure from an existing ancestor, as Serp's merchant example does from `/Values`. Also distinguish serialized XML from values inherited later by the game.

This pattern does **not**:

- Remove duplicate containers that already exist.
- Deduplicate `Item` entries; applying the add twice can append the same entry twice.
- Supply a missing Asset or repair an incompatible replacement by another mod.
- Make two changes to the same trigger's behavior compatible.

Two foreign-mod ordering fixtures retain both contributions in one container. They only test XML composition: an additional child can still change the trigger's completion requirements, timing or action order. The Campaign patch therefore preserves its existing signal, timer, native registration and cancellation without promising compatibility with arbitrary trigger rewrites.

## Choose the smallest suitable change

Change the property or keyed entry that implements the feature. Avoid replacing an entire asset or list to change one value. Serp's session-goods mod explicitly preserves native and other mods' production entries, accepting an author-reported performance cost (C11; no new benchmark).

Where an entry has a stable key, select it by that key, such as `Item[Good='...']`, instead of assuming `Item[1]` is still the desired entry. If it is absent, use a separate guarded add into the prepared container. Updating an existing entry and adding a missing entry are different operations (C04, C10).

A missing-entry condition must use the loader's supported node-selection context. Do not substitute scalar `Condition="true()"` or `count(...) > 0` for a verified 1800 node selection; see [Q001](../reference/discrepancies.md#q001-scalar-condition-expressions-in-anno-1800).

Explicit GUIDs are not automatically bad. In Story's detailed condition file, Serp intentionally targets reviewed Vanilla GUIDs and the expected condition shape instead of changing every foreign asset containing a similar condition (C13). Conversely, copying a fixed Vanilla list can omit later mod additions. Choose the scope from the intended integration contract rather than a rule that every query must be global or dynamic.

## Merge does not identify logical list keys

The inspected `RecursiveMerge` finds existing children by **name and occurrence**. With two payload `Item` nodes it merges into the first and second existing `Item`; it does not search for equal product GUIDs. Earlier additions or reordering can redirect such an update.

Serp's later notebook says merge can add missing children and that order is now irrelevant (C01). The first point agrees with implementation. The order statement must be limited: it does not make repeated names key-based. The positional-merge fixture changes the first timer entry while leaving the second untouched.

The earlier notebook recommendation to avoid add and prefer replace (C02) belongs to the older explanation before the later merge correction. It is historical context, not current advice to replace whole lists. Keep the original notes unchanged; use prepare-then-append for this extension problem. See [list handling and inheritance](../xml/content-and-lists.md).

## Keep anchors and template contracts

Removing an entry can remove another mod's insertion anchor. Avoid unnecessary removal or replacement of construction-menu entries and template members; apply the smallest supported change after auditing the actual feature. The community guide recommends preserving these anchors (C18).

Serp's attacker helper similarly avoids a wider tower/type change because foreign towers could be affected (C14). This is a scoped design decision, not proof that a generic template edit is safe.

Do not copy upstream examples uncritically. The community compatibility guide's duplicate-cleanup expression `position() &amp; last()` has an invalid XPath operator (C19). This chapter does not present that dummy/duplicate-asset recipe as valid. The existing [discrepancy register](../reference/discrepancies.md#editorial-defects-found-during-research) retains its provenance.

## Copy the effective data at the intended time

`Content` reads the XML state when its operation executes. Serp's proposed late copy of item-set buffs avoids manually freezing their values, but still uses explicit source/target mappings (C03). The preferred-goods mod also prepares missing containers before copying an effective source node (C12).

If the copy must include earlier mods' additions, establish that order. Do not assume `Condition="#other-mod"` means the other mod has already patched the XML. Use the appropriate dependency and phase rules; a small late submod can be preferable to moving all unrelated work late. Later mods can still replace the result. See [Content](../xml/content-and-lists.md#copy-timing-and-late-submods) and [loading order](structure-and-loading.md#loading-order-and-nested-helpers).

## Shared components, metadata and names

`ModDependencies` expresses required components; `LoadAfterIds` expresses ordering. A late-phase integration must respect the late phase as well as the named dependency. Keep stable ModIDs, check cycles and inspect the actual selected shared version. Highest-version selection is not an API guarantee; equal IDs/versions with different contents remain a packaging risk.

Serp's SharedMods README asks consumers to keep shared copies unchanged, propose general improvements upstream and make private adaptations from their own consuming mod loaded afterwards (C08). Preserve that contract when bundling helpers.

The virtual file overlay is not isolated by mod-folder name. Give custom scripts/resources distinct author-and-feature paths. Likewise, keep independent Lua globals, threads and callback registrations distinct. LuaLight prefixes thread names with the ModID and provides a ModID-keyed callback extension map (C15-C16). Add through that interface instead of replacing the entire map. A Lua function override also does not intercept every native/textembed consumer (C05).

See [resource paths and metadata](structure-and-loading.md), [identifier allocation](identifiers-and-tools.md) and [Lua lifecycle](../lua/execution-and-lifecycle.md). An illustrative ordering entry in the Python snippet collection (C07) does not establish new loader behavior or dependency-download support.

## Diagnose conflicts at the right layer

Declare known conflicts where appropriate, but do not treat `IncompatibleIds` as a compatibility repair. The popup helper reads incompatibility messages already written to the mod-loader log (C17); it does not discover every contradictory list, trigger or resource change.

Inspect the effective combined output, selected dependencies and load order. A useful compatibility check preserves another mod's sentinel contribution and tests both relevant orders. Investigate missing paths and unexpected warnings rather than hiding them. Existing game/MP observations keep their original scope; source composition tests do not certify save migration or multiplayer timing.

## Sources and evidence

The following are original sources, not claims that this new chapter or the local Campaign 1.023 edit is already published. Baseline links use commits verified against the remote on 2026-10-25. Private notebooks have hashes and selected excerpts in the source record, without an invented public URL.

| Source / claim | Workspace source | Published baseline |
| --- | --- | --- |
| Merchant path preparation (C09) | [Local file](../../../Anno-1800-Mods/Recommended-Mods/BT%20Merchants%20Offering%20More%20Goods%20%28Serp%29/data/config/export/main/asset/assets.xml) | [GitHub](https://github.com/Serpens66/Anno-1800-Mods/blob/9858f32602891e2b562a73a1b6c8b5890bfd1f68/Recommended-Mods/BT%20Merchants%20Offering%20More%20Goods%20%28Serp%29/data/config/export/main/asset/assets.xml#L44-L55) |
| Preserve other mods' goods (C11) | [Local file](../../../Anno-1800-Mods/Recommended-Mods/BT%20Merchants%20Produce%20Session%20Goods%20%28Serp%29/data/config/export/main/asset/assets.xml) | [GitHub](https://github.com/Serpens66/Anno-1800-Mods/blob/9858f32602891e2b562a73a1b6c8b5890bfd1f68/Recommended-Mods/BT%20Merchants%20Produce%20Session%20Goods%20%28Serp%29/data/config/export/main/asset/assets.xml#L33-L36) |
| Effective-data copy (C12) | [Local file](../../../Anno-1800-Mods/Recommended-Mods/BT%20Display%20Offered-Preferred%20Always%20%28Serp%29/data/config/export/main/asset/assets.xml) | [GitHub](https://github.com/Serpens66/Anno-1800-Mods/blob/9858f32602891e2b562a73a1b6c8b5890bfd1f68/Recommended-Mods/BT%20Display%20Offered-Preferred%20Always%20%28Serp%29/data/config/export/main/asset/assets.xml#L34-L38) |
| Scope to reviewed Vanilla assets (C13) | [Local file](../../../Anno-1800-Mods/YouKnowWhatYouDo-Mods/Story%20Quests%20in%20Coop%20%28Serp%29/data/config/export/main/asset/Conditions_detailed.include.xml) | [GitHub](https://github.com/Serpens66/Anno-1800-Mods/blob/9858f32602891e2b562a73a1b6c8b5890bfd1f68/YouKnowWhatYouDo-Mods/Story%20Quests%20in%20Coop%20%28Serp%29/data/config/export/main/asset/Conditions_detailed.include.xml#L3-L8) |
| Shared-component policy (C08) | [Local file](../../README.md) | [GitHub](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/blob/79f10e0cc8e53d909c44dd831689ddc8d4632c99/README.md#L24-L24) |
| Qualified list-extension advice (C06) | [Local file](../../CodeSnippets.md) | [GitHub](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/blob/79f10e0cc8e53d909c44dd831689ddc8d4632c99/CodeSnippets.md#L2527-L2529) |
| ModID-keyed Lua extension (C16) | [Local file](../../shared_LuaLight/data/scripts_serp/lighttools.lua) | [GitHub](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/blob/79f10e0cc8e53d909c44dd831689ddc8d4632c99/shared_LuaLight/data/scripts_serp/lighttools.lua#L1244-L1253) |
| Community guidance (C18) | Local extraction/cache | [GitHub](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/guides/mod-compatibility.md#L13-L18) |
| Loader append/merge implementation (C21) | Local extraction/cache | [GitHub](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/xml_operations.cc#L831-L849) |
| Shared version and phase handling (C22) | Local extraction/cache | [GitHub](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/mod_loading_order.cc#L158-L169) |

The source record contains the complete selected claim register, including the notebooks, Python snippets and mixed-authorship log helper. It explicitly separates negative/limited findings from positive guidance. The original merchant mods, notebooks and old receipts are not rewritten.

## Offline validation and limits

[The validation receipt](../reference/validation/mod-compatibility/results.json) records ten actual GU17.1 fixtures: missing/empty/populated containers, foreign additions in both orders, repeated empty merge, repeated add, occurrence-based merge, the legacy duplicate-container failure and preexisting duplicates.

The full `shared_CheckSingleHuman -> Story -> Campaign` application retains all **96,272** asset identities and has **zero semantic asset changes** against the captured 1.022 baseline. The comparison ignores formatting/comments, not property values or child order. Story stays 1.032; Campaign becomes 1.023. Seven previously understood optional resource/island no-match diagnostics remain; unexpected errors/warnings are rejected.

Reproduce with [the dedicated validator](../tools/validate_mod_compatibility.py), passing a full pre-change effective XML as `--baseline` and a disposable directory outside the repository as `--work`. The earlier baseline must not be replaced by a post-change output. Full Vanilla-derived outputs remain temporary; only bounded receipts, hashes and authored test code are retained.

No new game, save repair, multiplayer session, publication or starter-kit synchronization was performed. [KIT021](../reference/kit-transfer.md#kit021-mod-composition-and-empty-container-preparation-2026-10-25) remains open for deliberate later adaptation.
