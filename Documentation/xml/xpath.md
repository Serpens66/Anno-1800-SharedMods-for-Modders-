# XPath and loader-specific lookups

The Anno 1800 loader uses pugixml XPath selection. Its `GUID`, `Template`, `@GUID`, `~` and `#ModID` handling are loader extensions, not generic XPath. See [the inspected implementation](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/xml_operations.cc) and the external [XPath cheat sheet](https://devhints.io/xpath). The cheat sheet still needs a complete compatibility review.

## Essential patterns

| Pattern | Meaning |
| --- | --- |
| `/TextExport/Texts` | Follow children from the document root. |
| `//Asset` | Find matching descendants anywhere. Broad searches can be expensive. |
| `Item[Product='1010017']` | Select list entries by a child value. |
| `Item[Product='1010017']/Amount` | Select that entry's amount field. |
| `..` | Parent of the current context node. |
| `text()` | Text-node selection, useful for copying leaf values with `Content`. |
| `A | B` | Union of node selections; not boolean OR. |
| `[A and B]`, `[A or B]` | Boolean predicates on a selected node. |
| `[not(Item/Product='123')]` | Select a container without the specified descendant value. |
| `[position() &lt; last()]` | All but the final node in that particular predicate context. |

XPath positions start at **1**. Vanilla vector inheritance indices and many Lua enum positions start at **0**. These are different index systems.

Predicate placement changes meaning. `//Item[1]` can select the first child item of each matching parent; `(//Item)[1]` selects the first item of the full resulting set. Do not use a positional selector without deciding which list/context it belongs to.

XML attributes require `<` to be escaped as `&lt;`. Use `&gt;` for `>` in these examples as well. An XPath reading text containing an apostrophe needs a suitable quoted string rather than broken XML quoting. Literal XML escaping and XPath quoting are separate steps.

## GUID shortcuts

```xml
<!-- Both select the radius field; the container context differs. -->
<ModOp Type="replace" GUID="2001241"
       Path="/Values/BuildingBaseTiles/HarbourConstructionAreaRadius">
  <HarbourConstructionAreaRadius>40</HarbourConstructionAreaRadius>
</ModOp>
<ModOp Type="replace" Path="@2001241/BuildingBaseTiles/HarbourConstructionAreaRadius">
  <HarbourConstructionAreaRadius>40</HarbourConstructionAreaRadius>
</ModOp>
```

`@GUID` is recognized at the start of a lookup. Do not insert it arbitrarily inside an XPath expression and expect the loader to expand it. Use explicit full XPath for more complex predicates or unions when needed.

## Serialized data versus inherited data

XPath sees the XML being patched. It does not automatically expand a base asset/template into every derived asset. `//FactoryBase[IsMainFactory='1']` will not find an asset whose value is only inherited. Determine whether to patch its base/template, materialize an override, or select explicit derived assets. See [inheritance](../foundations/inheritance.md).

## Unsupported transfers from Anno 117

Do not assume XPath 2.0 support, `.[predicate]` rewriting, scalar calculated `Content`, option variables, inline `ModValue`, or boolean combinations of `#ModID` work in 1800. XPath arithmetic inside a predicate selecting existing nodes is different from asking `Content` to insert an arithmetic result.

Test the XPath on the exact target file and inspect the match count. An XML parser accepting an attribute says nothing about the XPath expression's validity or the loader's special context rewriting.
