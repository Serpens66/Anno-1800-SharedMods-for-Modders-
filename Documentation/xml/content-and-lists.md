# Dynamic content and list handling

Evidence: pinned 1800 `XmlOperation::Apply`, `XmlLookup` and `RecursiveMerge`; loader 10/11 notes; the current [Dynamic Content](https://jakobharder.github.io/anno-mod-loader/modops/content/) and [Item Lists](https://jakobharder.github.io/anno-mod-loader/modops/lists/) references. Full test-case execution is pending.

## Copy existing nodes

`Content` selects source nodes from the XML state **at the time that operation runs**. Earlier mods and earlier operations can change that source. It is not an immutable copy of vanilla.

An empty ModOp with `Content` uses those selected nodes as its payload. Match the payload level to the operation: `replace` needs a replacement element; `add` appends inside the target; siblings are inserted alongside it. A scalar number or boolean result is not established 1800 `Content` syntax.

With payload markup, use `ModOpContent` as the insertion placeholder:

```xml
<!-- Schematic: CUSTOM_POOL_GUID must be replaced with a uniquely allocated GUID. -->
<ModOp Type="add" Path="@CUSTOM_POOL_GUID/AssetPool/AssetList"
       Content="@193666/ItemEffectTargetPool/EffectTargetGUIDs/Item/GUID/text()">
  <Item>
    <Asset><ModOpContent /></Asset>
  </Item>
</ModOp>
```

This converts source GUID text nodes into the different list structure of an `AssetPool`. It requires the destination asset and its serialized `AssetList` container to exist already. Vanilla `193666` is an `ItemEffectTargetPool`; its list uses `Item/GUID`, while `AssetPool` uses `Item/Asset`. Pool types are not interchangeable just because they both contain GUIDs.

The pinned implementation repeats the wrapper for each selected source node. Only the first located `ModOpContent` is replaced in that construction step. Do not use several placeholders to duplicate the same value without verifying the output; Serp's notes contain a two-operation merge technique for constructing differently named fields.

If source selection is empty, the operation warns and returns. A later `AllowNoMatch` target suppression does not turn empty source content into a valid payload. Source lookup context follows the same GUID-relative rules as conditions; an explicit `@sourceGUID/...` avoids accidental reference to the destination.

## Merge is positional for repeated names

For a payload with two `Item` nodes, recursive merge edits the first and second existing `Item` nodes. It does not search for a matching product. Another mod adding or reordering items can therefore redirect a positional merge.

Select the logical key explicitly before updating:

```xml
<ModOp Type="merge" GUID="100780"
       Path="/Values/Maintenance/Maintenances/Item[Product='1010017']">
  <Amount>500</Amount>
</ModOp>
```

This illustrative narrow operation is supported by the recorded oil-powerplant maintenance structure. It does not replace workforce or other maintenance entries. If the desired item is absent, merge cannot create the missing target: a separate guarded add to the list container is needed.

To append an entry once, check the list for its key first:

```xml
<!-- Schematic: NEW_PRODUCT_GUID is not an allocated number. -->
<ModOp Type="add" GUID="120055"
       Path="/Values/ProductStorageList/ProductList"
       Condition="!/Values/ProductStorageList/ProductList[Item/Product='NEW_PRODUCT_GUID']">
  <Item><Product>NEW_PRODUCT_GUID</Product></Item>
</ModOp>
```

Conditional insertion avoids a duplicate in this exact list. It does not prevent GUID collisions or deduplicate other mods' differently structured references.

## Copy timing and late submods

If a new pool must include other mods' additions to a source pool, perform the copy after those additions. A small late submod can use `LoadAfterIds` with `*` rather than moving the entire mod to the late phase. It still needs its own ModID, version and appropriate dependencies.

Copying an empty pool, a nonexistent inherited container, or a list of the wrong item shape does not become valid because the operation is late. Audit the final source shape and destination property definition.

## Two kinds of list behavior

Loader merge changes serialized XML. Game inheritance decides what a derived asset inherits. Their rules differ:

- Loader merge is recursive and occurrence-based; unspecified XML remains.
- A derived asset's explicitly supplied vanilla vector replaces its inherited vector according to Serp's tests, unless individual entries use `VectorElement/InheritedIndex`.
- An explicit empty vector clears inherited entries in those tested cases.

Do not use the loader's merge rules to predict how a new asset's inheritance behaves. Conversely, vector replacement at game load does not make a `merge` clear an existing XML list.

`ModItem`, `ModValue`, `SkipParent` and automatic keyed merges from Anno 117 are excluded from 1800 examples.


## Prepare containers before appending

Use an empty merge from an existing parent to create a missing list container, then add Item entries into the container. Adding a complete container with add can duplicate it when another mod supplied one first. This does not deduplicate entries or repair preexisting duplicate containers. See [Mod compatibility](../foundations/mod-compatibility.md#ensure-containers-then-append-entries) for the tested Campaign example, source history and scope limits.
