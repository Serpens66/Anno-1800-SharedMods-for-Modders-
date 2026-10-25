# ModOps in Anno 1800

Evidence: complete inspection of [XML operations at the pinned 1800 commit](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/xml_operations.cc), its seven documentation files and the current [Modloader Reference](https://jakobharder.github.io/anno-mod-loader/). These are data-load patches, not commands executed each time a player performs an action.

## File and operation structure

Use an XML file with one `ModOps` root. Keep operations in execution order. A patch for the main asset file belongs at `data/config/export/main/asset/assets.xml` within the mod. Included feature files are loaded where their `Include` appears.

```xml
<ModOps>
  <ModOp Type="merge" GUID="2001241" Path="/Values/BuildingBaseTiles">
    <HarbourConstructionAreaRadius>40</HarbourConstructionAreaRadius>
  </ModOp>
</ModOps>
```

This demonstrates patch syntax, not a balancing recommendation. Vanilla GUID `2001241` has `HarbourConstructionAreaRadius=28` in the recorded extraction, and a separate `HarbourConstructionAreaRadiusCreativeMode=56`. Changing one does not imply changing the other. See the [audit records](../reference/vanilla-contracts.json).

In the inspected 1800 code, the operation type is matched case-insensitively; XML field/property names and XPath names still require their exact spelling. Prefer a consistent spelling and do not infer that arbitrary attribute names are case-insensitive.

## Selection context

| Form | Starting node | Example |
| --- | --- | --- |
| `GUID="2001241"` | Matching `Asset` | `Path="/Values/BuildingBaseTiles"` |
| `Path="@2001241/BuildingBaseTiles"` | Matching asset's `Values` | No extra `/Values` after `@GUID` |
| No helper, absolute XPath | Whole XML document | `Path="//Asset[Values/Standard/GUID='2001241']/Values/BuildingBaseTiles"` |
| `Template="Skin"` | Named `Template` in `templates.xml` | `Path="/Properties/Locked"` |

`GUID` and `Template` must not both be supplied. A comma-separated GUID attribute expands the operation for each GUID. Avoid whitespace in that list: the pinned splitter does not trim it. An omitted or empty path with a GUID selects the asset itself, not `Values`.

The optimizer attempts GUID/template selection and may fall back to the full XPath for ordinary targets. Complex unions and missing matches deserve inspection of the resulting patch/log, not an assumption that a helper is pure textual XPath substitution. Conditions use strict selection. The first matching asset is used by optimized GUID lookup; duplicate assets are not a safe way to intentionally select multiple definitions.

## All supported operation types

| Type | Effect | Payload |
| --- | --- | --- |
| `add` | Append payload children inside each selected node. | New child nodes. It does not deduplicate existing entries. |
| `addNextSibling` | Insert payload after each selected node. | Sibling nodes, including new `Asset` definitions. Payload order is preserved. |
| `addPrevSibling` | Insert payload before each selected node. | Sibling nodes. Payload order is preserved. |
| `remove` | Remove selected nodes entirely. | No payload; source content is not used. |
| `replace` | Insert payload siblings and remove selected nodes. | Include the replacement node's own tag. An empty payload removes the target. |
| `merge` | Recursively update existing children/attributes and append missing ones. | Child nodes, or the single matching outer container described below. |

A target path may select several nodes; the operation applies to each. The distinction between *adding inside a node* and *adding next to it* is essential. Adding a new `Asset` inside an existing `Asset` is not the same as inserting a sibling.

### Replace

```xml
<ModOp Type="replace" GUID="2001241"
       Path="/Values/BuildingBaseTiles/HarbourConstructionAreaRadius">
  <HarbourConstructionAreaRadius>40</HarbourConstructionAreaRadius>
</ModOp>
```

Replacing the entire `BuildingBaseTiles` container with only this field would remove the other explicitly serialized fields. Omitted values might then inherit defaults, but that is a different change and can overwrite other mods. Prefer a narrow target or merge.

An explicit empty container such as `<Cost />` replaces the old container with an empty one. A completely empty ModOp removes the selected node. Runtime inheritance may further interpret an empty container; loader replacement and game inheritance are distinct layers.

The pinned implementation inserts each replacement after the original target without moving its insertion cursor. **Inference from code:** several replacement siblings can therefore appear in reverse payload order. Use a single replacement node where order matters, or validate the exact output with the appropriate xmltest. Do not transfer `addNextSibling`'s order guarantee to `replace`.

### Merge

Merge identifies sibling nodes by name and occurrence number, recurses into their children, updates supplied attributes, and appends missing nodes. It does not remove unspecified children. `<Building />` is not a request to clear the building property.

These two forms normally have the same effect:

```xml
<ModOp Type="merge" GUID="2001241" Path="/Values/BuildingBaseTiles">
  <HarbourConstructionAreaRadius>40</HarbourConstructionAreaRadius>
</ModOp>
```

```xml
<ModOp Type="merge" GUID="2001241" Path="/Values/BuildingBaseTiles">
  <BuildingBaseTiles>
    <HarbourConstructionAreaRadius>40</HarbourConstructionAreaRadius>
  </BuildingBaseTiles>
</ModOp>
```

The legacy outer-container interpretation applies only when the payload consists of **exactly one top-level node** whose name matches the selected node. Do not mix a matching container with additional top-level children and expect implicit path correction. Repeated parent/child names, especially localized `Text`, require careful selection and explicit structure.

Sibling order is not required to match for differently named fields. Repeated same-name fields are matched by their occurrence index, however. `Item` entries are not matched by `Product`, `GUID` or another logical key. See [lists](content-and-lists.md).

## Conditions

Use `Condition` to check the current patched XML before applying an operation. In the verified 1800 implementation, a condition matches when its selected node set is non-empty. A leading `!` negates that existence test.

```xml
<!-- Preserve a radius that another mod already raised to at least 40. -->
<ModOp Type="merge" GUID="2001241" Path="/Values/BuildingBaseTiles"
       Condition="!/Values/BuildingBaseTiles[HarbourConstructionAreaRadius &gt;= 40]">
  <HarbourConstructionAreaRadius>40</HarbourConstructionAreaRadius>
</ModOp>
```

With a GUID helper, a single leading `/` on `Condition` is relative to the asset (GU17.1 behavior). `//` denotes document-wide selection. The older explicit `~` relative prefix remains supported, but its path must still include the correct container. `@GUID` begins at `Values`.

A negative duplicate check is useful because a missing target can still produce a warning. A positive condition may silently skip when a prerequisite has disappeared. Choose deliberately: expected absence may justify a positive guard; unexpected structural incompatibility should remain visible.

**Q001, source-based resolution:** the current website mentions scalar `true()` conditions, but the inspected 1800 implementation uses `select_nodes()` and rejects scalar results. Do not use `Condition="true()"` or `Condition="count(//Asset)&gt;0"`. Serp has not tested them in-game. See the [exact website statement, implementation and limits](../reference/discrepancies.md#q001-scalar-condition-expressions-in-anno-1800). XPath comparisons *inside predicates selecting nodes* are supported and are a different case.

### ModID conditions

`Condition="#mod-id"` checks whether the ModID is active; `Condition="!#mod-id"` checks absence. This is an active-mod check, not evidence that the other mod's XML has already been applied. Use `LoadAfterIds` when its data is needed.

For 1800, nest groups to require two ModIDs or to combine presence and absence. The pinned implementation treats everything after `#` as one ID. It does not implement the 117 expression `#mod-a and not(#mod-b)`.

```xml
<Group Condition="#first-mod">
  <Group Condition="!#conflicting-mod">
    <!-- Compatible patch operations go here. -->
  </Group>
</Group>
```

## Groups, includes and skipping

```xml
<ModOps>
  <Group Condition="@2001241">
    <Include File="feature.include.xml" />
  </Group>
</ModOps>
```

- A `Group` applies its children in order after evaluating its condition. It is not a transaction or an inheritance container.
- A relative include path is relative to the including file. A path beginning `/` is relative to the mod root, not the game root or disk root.
- Use `*.include.xml` to distinguish included files from ordinary patch entrypoints. The included file needs its own `ModOps` root.
- Includes can nest. Missing or invalid include files produce parse/load errors.
- In the inspected implementation include files are opened while operations are constructed, before the group's runtime condition is applied. **Inference:** a false include condition must not be used as a guarantee that a nonexistent include will never be opened. A present `Skip` prevents construction of that node.
- `Skip` works by attribute presence. `Skip="0"` still skips. Remove the attribute to activate the operation.
- `MaxRepeat` is a 117 capability; a normal 1800 group is not a loop.

## Warnings and validation

`AllowNoMatch` suppresses target-not-found warnings; in the pinned code it too is enabled by attribute presence. It does not make invalid XPath valid or make an absent target appear. An empty `Content` match has its own warning. Use suppression only when absence is expected and understood.

Check well-formed XML, the exact target context, match counts, output structure, operation order and dependency order. Inspect `mod-loader.log`, then check behavior in the correct game/save/session context. The guide's historical fallback/dummy-asset techniques should not replace the simpler supported conditions without a concrete reason.
