# Feature-specific vanilla research

## Required audit

Before proposing a game-dependent implementation, complete the audit required by AGENTS.md. A GUID search or a syntactically valid patch does not establish the game's contract. The audit must explain the exact feature you will change, its inherited values, the supported data types and its relevant consumers.

The current extracted source root is:

```text
D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Anno1800 RDA unpacked\dataAlle
```

| Source | Purpose |
| --- | --- |
| `data/config/export/main/asset/assets.xml` | Asset instances, explicit values, base references and inline conditions/actions. |
| `data/config/export/main/asset/templates.xml` | Properties assigned by each template and template-specific overrides. |
| `data/config/export/main/asset/properties-toolone.xml` | Authoring schema: types, vector layout, datasets, restrictions, descriptions and implementation hints. |
| `data/config/export/main/asset/properties.xml` | Exported default values. |
| `data/config/export/main/asset/datasets.xml` | Enum names, serialization IDs and list ordering. |
| `data/config/gui/texts_english.xml` and other languages | Display text and embedded textsource expressions. |
| Root `export.xml` | Decoded infotip data available in this extraction; the mod patches the corresponding game `export.bin` through `export.bin.xml`. |
| Native `*.lua`, graphics and map files | Existing API usage and resource consumers for the feature. |
| `textsourcelist.json` | An older API/textsource catalogue; useful evidence, not a complete current Lua API. |

`assets.xml` is about 289 MB in this extraction. Use `rg` for targeted discovery and an XML parser for structural extraction. There are also leaf elements named `Asset` inside pools. A top-level asset record is identified by `Values/Standard/GUID`; do not treat every `<Asset>` element as a full definition.

## Reading properties-toolone.xml and datasets.xml

**Evidence and scope:** the basic reading model below was inspected in the local dataAlle files and explicitly confirmed by Serp on 2026-10-03. That confirmation concerns understanding the schema, not a new game test or certification of every specialized data type. These two files are central references for available properties, their field structures, compatible references and declared values. They must be read together with templates, defaults and concrete assets.

### From a definition to an asset field

In properties-toolone.xml, find a `Property` by its direct `Name` child, for example `FactoryBase`. Its `ValueDefinition` children describe fields inside the corresponding `Values/FactoryBase` block of an asset. The surrounding schema `Groups/Group` hierarchy organizes definitions; do not reproduce that hierarchy in the asset.

| Definition entry | How to read it |
| --- | --- |
| `Name` | Actual XML field name at this nesting level. A name can recur in other properties or nested entries; retain its complete owning path. |
| `DataType` | Type and structural interpretation: for example Integer, Float, Boolean, String, Text, FileName, Asset, Choice, Flags, Struct, Vector, Array or AutoCreateAsset. |
| `Description` | Intended meaning, units, conditions and usage notes. Preserve qualifications and reconcile ambiguous wording with the feature's other evidence. |
| `Items` | Definitions of nested fields or entry contents, interpreted according to the containing DataType. |
| `Min` / `Max` | Declared bounds where supplied. Missing bounds do not prove that every numeric value is meaningful. |
| `DataSet` | Name of the dataset supplying choices, flag members or array keys; resolve it in datasets.xml. |
| `NeededProperty` | Property requirement on the referenced asset, where supplied; see reference fields below. |
| `AllowedTemplates` / `AllowedProperties` | Declared restrictions on embedded AutoCreateAsset definitions. |
| `Category`, `Browsable`, `ReadOnly`, `Export`, `ExportPlatforms`, `ExcludedVersions` and similar entries | Authoring/editor/export metadata. Distinguish presentation and export settings from the runtime meaning of the field. |

Do not copy `ValueDefinition`, `DataType`, `NeededProperty` or the other schema metadata into the asset as values. For example, Standard/GUID is marked ReadOnly in the authoring schema; that describes editor behavior and does not prohibit a mod from supplying its new asset's GUID. Likewise, an editor-hidden field is not automatically unsupported, and an Export=0 field is not evidence of an exported gameplay effect. A declared schema field, Min/Max bound or implementation marker does not by itself prove how every game build enforces it.

### Struct, Vector and Array nesting

A `Struct` groups its defined fields directly under its named element. A `Vector` describes a variable sequence of `Item` entries; each Item contains the fields declared in the Vector's `Items`. A dataset-bound `Array` instead has entries keyed by dataset names, with each key holding the defined entry fields. Do not substitute a Vector's Item layout for an Array's named keys. Read nested definitions recursively and check the actual serialized layout in vanilla assets/defaults before writing a specialized or unfamiliar type.

FactoryBase/FactoryInputs is a Vector whose entry fields are Product (Asset requiring Product), Amount (Integer, consumed per cycle) and StorageAmount (Integer, maximum stored amount excluding goods in the current cycle). Its translation into asset values is:

```xml
<FactoryBase>
  <FactoryInputs>
    <Item>
      <!-- Replace with the GUID of an audited Product asset. -->
      <Product>PRODUCT_GUID</Product>
      <Amount>1</Amount>
      <StorageAmount>4</StorageAmount>
    </Item>
  </FactoryInputs>
</FactoryBase>
```

This is a property fragment, not a complete asset or ModOps file. `PRODUCT_GUID` is a required substitution and is not valid deployable GUID syntax. The values 1 and 4 illustrate the structure, not a recommended balance or a verified standalone factory. Defining inputs alone does not establish the factory's output, logistics, unlocks or menus.

### Dataset lookup and the different kinds of identifiers

Item/Allocation has DataType Choice and DataSet ItemAllocation. Locate `DataSet[Name='ItemAllocation']` in datasets.xml and read its Items. `Ship` is one of the named entries, so an asset can serialize that choice as:

```xml
<Item>
  <Allocation>Ship</Allocation>
</Item>
```

Here Item is the property name, not a Vector entry. The definition's nesting determines which meaning applies.

Each dataset has its own Name and Id; each entry has its own Name and Id as well. Keep four facts separate: dataset Id, entry Id, entry Name and entry position in the file. They are not interchangeable, and none is automatically an asset GUID. Positions and IDs can differ: Region's Mod1 follows Africa in the list but has Id 9. Item names used in asset XML must match the relevant dataset; translate a displayed label only through the proper localization mechanism, not by renaming the enum token.

| Use of a dataset | Interpretation |
| --- | --- |
| Choice | Select one named entry, as in Item/Allocation=Ship. |
| Flags | Select a combination of supported members. This differs from a single Choice. Verify the field's actual serialized combination syntax in native examples rather than assuming separators or deriving bit masks from entry position. |
| Array | Dataset entries provide the named keys for the array's structured values; the Items definitions describe what belongs under each key. |
| Lua arguments | Determine whether that particular API expects an enum ID, an index, a string or another representation. Do not automatically pass a dataset's printed Id or its list position. |

A dataset exposes declared vocabulary, not a promise that a new arbitrary member can acquire new engine behavior. Do not add enum members or infer Lua numeric constants merely because the XML is editable.

### Reference fields and embedded assets

For FactoryInputs/Product, DataType Asset together with NeededProperty Product means the value references an asset expected to possess the Product property. Resolve its GUID and inspect its effective property membership through the asset/template/base chain. **NeededProperty constrains the referenced target; it does not instruct you to add Product to the referring factory.** Text and FileName fields also need their own reference/resource interpretation; an Integer is not automatically an asset reference just because its value resembles a GUID.

AutoCreateAsset describes an embedded asset definition, rather than an ordinary numeric Asset reference. Read AllowedTemplates and AllowedProperties together with the candidate template and an existing native example, including nested Values and any applicable inheritance markers. Do not improvise an embedded definition from the property name alone.

**Unresolved specialized rules:** the general interpretation above does not establish the exact AND/OR/filter semantics of every semicolon-separated NeededProperty or AllowedProperties list, nor every special case of Upgrade, InnerDataSet or implicit defaults of built-in data types. Inspect each relevant contract before using those cases. An empty restriction element must not be given a universal meaning without evidence.

### Combining properties and resolving effective values

The schema supplies field shapes and many compatibility/meaning constraints, but it does not establish that any arbitrary collection of property blocks produces a working object. Read templates.xml to identify the properties combined by the selected Template and its overrides; read properties.xml for exported property defaults; then inspect assets.xml and every BaseAssetGUID in the chosen chain for concrete values and combinations. Follow consumers and resources as required by the feature audit below. A missing explicit field is not automatically zero, false or disabled.

Keep source categories distinct: schema metadata, supplied defaults, actual asset values, engine implementation and reported tests are different evidence. In particular, Serp explains that the property-comment authors are German non-native English speakers and words can be confused. For MoneyValue, Serp explicitly selects income per 100 inhabitants per minute despite the comment's word "residences"; see [Q004](../reference/discrepancies.md#q004-population-consumption-and-income-units). This specific decision does not authorize silently replacing every occurrence of residence or citizen elsewhere.

Local source anchors: properties-toolone.xml `//Property[Name='FactoryBase']`, `//Property[Name='Item']`, `//Property[Name='Standard']` and the nested DevTestProp structural examples; datasets.xml `//DataSet[Name='ItemAllocation']` and `//DataSet[Name='Region']`. These are structural lookup paths into the source files listed above, not loader ModOp selections. See [inheritance](inheritance.md) for omission, empty values and native vector inheritance.

## Audit procedure

1. Identify the asset and every relevant consumer: construction menus, needs, upgrade targets, pools, triggers, quest actions, scripts, UI and resources as applicable. Record the feature boundaries.
2. Read the complete owning asset, follow every `BaseAssetGUID` until its root, and inspect the effective template. Check ordering requirements when introducing a derived asset.
3. Read every involved property definition and its corresponding defaults. Record whether a field is a scalar, Vector, Array, Choice, Asset, Text, FileName or AutoCreateAsset. A field name alone does not establish its scope or list semantics.
4. Follow relevant references to their actual definitions. For example, a text number may identify localized text; a participant enum is not an asset GUID; an OID identifies an instance rather than a type of object.
5. Inspect relevant dataset entries, native scripts, infotip expressions and exported text. For Lua enum arguments, compare list position with the printed `Id` rather than assuming equality.
6. Read the existing workspace implementation and its comments, tests, dependency metadata and savegame behavior. Inspect every non-identical shared helper version used by the mod.
7. Write an audit outcome: explicit data, inherited data, source-tested behavior, unsupported assumptions, remaining questions, and the smallest proposed patch. Only then implement or run dependent checks.

There is no requirement to read unrelated game systems for a small change. There is a requirement to follow every relevant part of the selected feature's contract; expand the audit when the proposed change introduces another system.

## Two different times at which data is combined

ModOps operate on serialized XML before the game resolves template/default/base inheritance. XPath therefore sees explicit nodes in the patched document. A value may exist in the effective game asset while being absent from that asset's XML. A `replace` targeting that absent node cannot change it; merge into an existing suitable parent to introduce an override.

This does not make ModOp merge equivalent to inheritance. Repeated list nodes are matched positionally by loader merge, while native vector inheritance uses explicit `VectorElement/InheritedIndex` where requested. See [inheritance](inheritance.md) and [lists](../xml/content-and-lists.md).

Sources: [inheritance guide](https://github.com/anno-mods/modding-guide/blob/main/guides/Inheritance.md), [loader discussion of pre-inheritance patching](https://github.com/xforce/anno1800-mod-loader/issues/192), inspected 1800 operation implementation.

## Research artifacts and their limits

[Vanilla contracts](../reference/vanilla-contracts.json) contains selected exact excerpts and hashes. [Runtime contracts](../reference/runtime-contracts.json) adds Lua-entry, vector and native-script evidence. [GUID index](../reference/vanilla-asset-index.json) locates 96,102 GUID-bearing records.

These are extraction aids. Their extraction status is deliberately not called an audit completion. Before reusing an example, read the actual excerpts and follow its feature-specific reference chain. Temporary research checkouts are also not durable dependencies of a finished mod.

Older scripts in the supplied DST backup path are secondary historical evidence. Use them only to explain a version difference or recover a missing original; do not replace a current contract with an older API merely because the old example is easier to understand.

## Audit record to retain

For a future mod task, retain: source version/hash, GUID and template chain, relevant fields/defaults/datasets, input/output references, execution context, savegame and multiplayer implications, original test conditions, intended XML selections, and validation results. Distinguish a structural check from a runtime observation. When a native contract remains unknown, record it as unknown instead of filling it with a plausible default.
