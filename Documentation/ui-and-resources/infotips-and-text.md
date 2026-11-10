# Infotips, localization and text expressions

Evidence: [the infotip guide](https://github.com/anno-mods/modding-guide/blob/main/documentation/infotips.md) ([previously pinned revision](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/documentation/infotips.md)), [textembeds](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/Scripting/textembeds.md), Serp's `HowTo.xml` final sections, and the vanilla and workspace sources below. Runtime observations retain the guide/notebook's qualifications.

## The three separate data layers

1. Asset properties such as `Standard/Name` identify an asset internally. Display text can be supplied by the asset's `Text` property, aliases, or system-specific text references.
2. Localization files such as `data/config/gui/texts_english.xml` contain `<TextExport><Texts><Text><GUID>...</GUID><Text>...</Text></Text></Texts></TextExport>`. Patch them using their own root; they are not assets with `Values/Standard/GUID`.
3. Tooltip layouts are binary `data/infotips/export.bin`. The corresponding mod patch is **`data/infotips/export.bin.xml`** containing ModOps, not a replacement binary export.

The extracted `dataAlle/export.xml` is a research copy of the decoded export. Its name at the extraction root is not the game's resource path. For another build, copy that build's `data/infotips/export.bin` into a scratch directory and decode the copy with [FileDBReader](https://github.com/anno-mods/FileDBReader/releases), using the 1800 infotip format definition. The guide's CLI form is:

    FileDBReader.exe decompress -i "FileFormats/infotip.xml" -f "scratch/export.bin" -y

Use the resulting XML as research input. The [current loader reference](https://jakobharder.github.io/anno-mod-loader/infotips/) supplies the 1800 legacy selector; its compact 117 element attributes and Oasis text IDs do not apply.

Anno 1800's authoring schema already contains `Text/LineID` and an Oasis category. That does **not** establish support for Anno 117's different exported localization syntax or loader features. Use the 1800 text-file structure.

## Find the layout for a specific UI area

Keep these identifiers separate even when the same number appears in more than one place:

| Identifier | Where to resolve it |
| --- | --- |
| Layout GUID | `/Content/InfoTipData/Guid` in the decoded export; look for the same number at `Asset/Values/Standard/GUID` in `assets.xml`. A matching `Template=InfoTip` gives an internal name; the actual display rows live in the export. |
| Consumer | The scene, button, notification, object menu or other field that supplies the layout GUID. Identify its owning asset and full field path. A same-number hit in an unrelated numeric field is not a consumer. |
| Text GUID | `TextGUID` inside text, headline, subtext or similar wrappers; resolve it in the matching language's `texts_*.xml`. One text can occur in multiple layouts. |
| Layout template GUID | `TemplateGUID` points to another `InfoTipData` with `IsTemplate=True`. It is distinct from an asset's template in `templates.xml`. Trace it in both directions before patching shared rows. |
| Context IDs | The asset under the pointer, selected asset, live object (`[RefOid]`), list index or a literal in a condition belongs to the expression. It does not identify the outer layout. |

1. Describe the exact widget and state: construction menu versus selected building, shipyard button versus world map icon, normal versus disabled, keyboard/mouse versus controller, and region/DLC. Take a distinctive visible phrase (preferably two) or the relevant UI configuration name.
2. For a phrase, find its GUID in the right language file and search the export for `TextGUID` at any depth, including `SubText`. For a named area, search internal `Standard/Name` values of `InfoTip` assets and UI scene assets, then join the GUIDs against the export. A text expression can derive the label from the hovered asset instead of a fixed `TextGUID`; use a neighboring label, a distinctive `Condition`/`Source` expression or the consumer in that case.
3. Reverse-search the layout GUID in `assets.xml`, `templates.xml`, `properties.xml` and relevant UI/scenario files. Check the actual owner and path; inspect `properties-toolone.xml` for the field shape and `BaseAssetGUID`/template/defaults for the effective value. Some legacy fields declared as Text still contain IDs that join to layouts, e.g. `ConstructionMenu/BuildButtonInfotip`; a field name or authoring type alone does not identify the runtime binding.
4. Open the complete candidate layout, including visibility branches and any `TemplateGUID` it includes. Verify that its expression inputs exist in that widget. If only the internal name and display text match, report the candidate and the unverified binding instead of claiming the engine selects it.

The read-only [lookup tool](../tools/find_infotips.py) uses the configured `vanillaPath`. From Documentation:

    python -B tools/find_infotips.py --query "Island Population"
    python -B tools/find_infotips.py --text-guid 23861 --references
    python -B tools/find_infotips.py --guid 500683 --references
    python -B tools/find_infotips.py --contains "BuildCostForShip"

Use `--language german` for German labels or `--export` to select another decoded export (a relative path is resolved from the local configuration directory). The tool lists names, direct text hits and layout template links. `--references` lists **candidates** from the main asset, template and default files; it does not resolve inheritance, walk scenarios or UI resources, evaluate expressions or prove an in-game binding. For manual lookup, from the extracted main asset directory run `rg -n -F '>500460<' assets.xml templates.xml properties.xml`; use an XML parser to get each complete owner and field path.

### Verified starting points

| UI area | Layout GUID and name | Evidence in the inspected extraction |
| --- | --- | --- |
| Alternative grass color option | `373` — `UseAlternativeGrassColor_InfoTip` | `SettingsMenu` asset `501073` contains `OptionToggle/ToggleInfotip=373` beside the alternative grass color textsource, in both containers. Layout uses `TextGUID=23861`. |
| Construction menu: building / production chain / subcategory | `25000020` / `500038` / `501001` | `ConstructionMenu` asset `25000035`, fields `BuildButtonInfotip`, `ProductionChainButtonInfotip`, `SubCategoryInfotip`. Also inspect `500132` for pinned/right-click building buttons; the controller radial scene `817` has its own fields. |
| Module construction | `500683` — `Production Build Module InfoTip` | Default `ModuleOwner/BlueprintModuleOption/ModuleButtonInfotip` in `properties.xml`; the schema declares an Asset reference with `NeededProperty=Infotip`. Check effective overrides per building. |
| World map ship / trade route ship list | `500460` — `StrategicViewShip` / `500503` — `ShipButtonInfoTip` | `WorldMapConfig` asset `500475`, `WorldMapConfig/Infotips/ShipInfotip`; `SessionTradeRoutesScene` asset `500344`, `ShipListInfoTip`. `500460` is also referenced by minimap token settings and the ship radial menu. |
| Shipyard build button | `500057` — `ShipContructionButtonInfoTip` | Internal name, localized cargo and lock labels, native `[Selection Object Shipyard BuildCostForShip([RefGuid]) ...]` branches and both shipyard mods agree. No explicit binding was located in the inspected main asset/template/default XML. |
| Influence in resource bar / island population | `500880` — `InfluenceInfoTipSimple` / `501255` — `IslandPopulationInfoTip` | `ResourceBarScene` asset `25000122` explicitly sets `InfluenceInfotip=500880`. For `501255`, labels `15602`/`15601` and the population fixes identify the candidate; no explicit main XML consumer was located. |
| Item socket / expedition item or goods | `25000084` — `ItemSocketInfotip` / `500933` — `ExpeditionItemGoodsInfoTip` | Socket layout has explicit references such as `SessionTradeRoutesScene/GoodsInfotip` and `CraftingPopup/SelectedItemInfotip`. The expedition layout is identified by its name, expedition labels and expressions. Both use shared layout templates; do not assume every item hover uses these GUIDs. |

### A fully traced simple vanilla tooltip

The decoded export begins with `InfoTipData/Guid=373` at line 4. It has one type-3 InfoElement and `Text/TextGUID=23861`. The English text for 23861 is recorded alongside it in [vanilla-contracts.json](../reference/vanilla-contracts.json). The visibility wrapper is an element-type-2 container with empty `OperatorType`; the element has empty style/value/warning/background fields. There are no template, icon or dynamic-value references in this simple example.

This is a suitable starting point for tracing text layout. It is not a generic guarantee that a new tooltip GUID is automatically used by a newly created gameplay asset; the consuming asset/UI reference also needs an audit.

### Factory input and output goods

The selected factory's goods slots use different infotips. The native input layout `25000206` (asset ID `ProductionInputInfotip`) tests `[ProductAssetData([RefGuid]) IsAbstract]` and has a dedicated abstract-product branch that renders the referenced product's icon and name. Vanilla `FakeInputMineralResource` (`1591`) is abstract and is listed in the Coal Mine's `FactoryBase/FactoryInputs`. `FakeProductWater` (`917`) is another abstract factory input.

The factory property `FactoryBase/ProductionOutputInfotip` defaults to `25000208` in `properties.xml`. That layout has an unconditional localized Output Storage heading (`100371`) and a product row that reads storage from the selected object's logistics using `[RefGuid]`. It has no equivalent abstract-product branch. The Cyanide Leacher (`24844`) explicitly sets `ProductionOutputInfotip=0` while listing the abstract `FakeProductWaste` (`25073`) in `FactoryOutputs`. This is an asset-side override of the default layout GUID. It does not establish an engine-wide rule for all abstract outputs.

When a modded output shows no tooltip, first resolve the building's effective `ProductionOutputInfotip` and identify the actual hover slot. If the binding is valid, compare the same slot with an ordinary product and a known visible static heading to isolate whether the widget invokes the layout for each product. A visibility condition inside the layout can only affect rows once the widget invokes it. Product flags and the precise slot are separate checks. This comparison is a diagnostic procedure, with no new runtime result recorded.

Evidence: main `assets.xml` near lines 665174 (fake input), 2363959 (input layout asset), 4254095 (Cyanide Leacher output), and 4260899 (waste product), `properties.xml:13309` (default), `properties-toolone.xml:57368` (Asset field), and `export.xml:130794` / `132068` (layouts) in the extraction identified below.

## Layout structure and counts

`InfoTipData` entries use **`Guid`**, not uppercase `GUID`. They contain ordered `InfoElement` children and may contain `Variables`. Layout order follows sibling order. Within an element, `VisibilityElement` controls its branch; nested elements form conditional containers. The decoded 1800 shape uses `VisibilityElement/ElementType/ElementType=1` for condition entries and `=2` for grouping wrappers in this extraction. `InfoElement/ElementType` is a different, direct scalar.

The inspected export contains 993 regular layouts and four template layouts, all as direct `Content/InfoTipData` siblings. The templates `319435862`, `454144439`, `1022171025` and `1563783317` have `IsTemplate=True` and no matching main asset definition. Of the regular layouts, 992 have a matching main `InfoTip` asset; `600338` does not. Missing a main asset hit therefore does not by itself invalidate a layout. Editing `454144439`, for instance, affects callers such as `25000083`; editing the latter alone does not change every caller of that template.

The export represents enum-like fields with nested names, for example:

```xml
<ResultType><ResultType>1</ResultType></ResultType>
<CompareOperator><CompareOperator>5</CompareOperator></CompareOperator>
<ExpectedValueInt>0</ExpectedValueInt>
<Condition>[Selection Object Upgradability Reasons COUNT]</Condition>
```

This shape is present in vanilla tooltip 500934. Do not flatten nested wrappers just because a field name repeats.

The loader's FileDB serializer updates **existing** `ChildCount` nodes and export counts. It does not create a missing count. The guide reports types 7 and 8 require one; preserve a count from a traced native container when adding children. The serializer uses the maximum of the applicable sibling InfoElement/VisibilityElement counts, not a recursive descendant total.

The native layout `132172` also contains `WarningType/WarningType=1` once; the other nonempty warnings in this export use 2. The guide reports red highlighting for 2. The visual meaning of 1 was not verified.

## Observed value comparisons

| Field | Guide / notebook interpretation |
| --- | --- |
| CompareOperator 0 | Equal |
| 1 | Not equal |
| 2 | Less than |
| 3 | Less than or equal |
| 4 | Greater than or equal |
| 5 | Greater than |
| ResultType 0 | Boolean; omitted expected Boolean is reported as true |
| ResultType 1 | Integer; omitted expected integer is zero |
| ResultType 2 | Float; use decimal dot |
| OperatorType 0 | AND between sibling visibility entries |
| OperatorType 1 | OR between sibling visibility entries |

These meanings are reverse-engineered observations, not an official complete UI specification. `ExpectedValueInt` is a typed literal: the loader writes an integer. Putting another `[expression]` there is not a supported comparison of two dynamic values. Serp explicitly tested this restriction. `ExpectedValueFloat` and `ExpectedValueBool` likewise have typed binary serialization.

## Observed InfoElement types

| Type | Reported purpose / restriction |
| --- | --- |
| 1 | Bright bold header, wrapping; vertically centered icon |
| 2 | Header with extra lower spacing and possible SubText |
| 3 | Bright wrapping text/value; no icon |
| 4 | Icon/text/value attribute row; does not wrap long text |
| 5 | Dark grey descriptive text; no icon/value |
| 6 | Separator, optionally text; intermittent rendering reported |
| 7 | Container with same-level Source, iteration contexts |
| 8 | Container with Sources on child levels |
| 9 | Single-line UI/infolayer hint; no icon |
| 10 | Cost-row container with Source/Columns; guide reports Columns always renders two |
| 11 | Cost/material/permit/upgrade row |
| 12, 13 | Containers; purpose incompletely known |
| 14 | Medium-grey action help; does not grow tooltip to fit |
| 15 | No established behavior |
| 16 | Category tooltip, requires Headline in the guide |
| 17 | Dark descriptive text without automatic size adaptation |
| 18 | Italic item/buff flavor text |
| 19 | Template inclusion / effect listing via TemplateGUID |

For types with unknown behavior, copy and audit a matching native use instead of inventing semantics. The remaining template/reference chains of complex tooltip 500934 are not yet a complete feature audit; this chapter supplies its structural observations, not a ready-to-deploy rewrite of that tooltip.

## Context is part of the expression

`[RefGuid]` identifies the referenced asset in a tooltip context. `[Selection Object ...]` reads the current selection; it may show information about a previously selected building while hovering a menu icon. `[Selection Picked ...]` is reported to follow a hovered object. `[StaticData ...]` can serve asset/menu contexts, with a narrower API.

Do not substitute `[MetaObjects SessionGameObject([RefOid]) ...]` for Selection without checking the receiving context. The guide reports that checking the bare Walking property through SessionGameObject always fails, whereas a deeper value such as `Walking BaseSpeedWithUpgrades` can work.

A bare property expression is not a normally invertible Boolean. In Serp's tests, `[Selection Object Hacienda]` is true when the property exists and false when absent **regardless of the expected Boolean**. Missing properties can also make deeper comparisons fail rather than evaluate as zero. A complementary branch needs a different positively established check.

`TextGUID` can pass tooltip variables to a localized text; replacing it with `Text` containing `[AssetData(GUID) Text]` may lose variables such as `{ItemGuid}`. `#index0#` is a loop context; its source and parent container must exist. A literal item GUID, reference asset GUID, runtime object ID and iterator index are different inputs.

## Text formatting and reuse

XML must escape markup intended for the text renderer:

```xml
<Text>&lt;b&gt;Example&lt;/b&gt;&lt;br/&gt;Second line</Text>
```

Serp records bold/italic/font-size/color/image/custom-entity experiments. Their availability depends on the receiving widget; asset expressions do not render everywhere (research UI, recipe text and MainNotification limitations are noted). Do not infer unrestricted HTML support. Greyed text can transform supplied colors; `overrideTextColor` is not a universal correction.

The vanilla `Text` property defaults to empty LocaText, Localize=1 and TextOverride=0. `TextOverride` can reuse another text asset. The schema says Localize=0 uses German everywhere, but Serp reports this did not work for modded display text. **Interpretation:** an authoring/export flag is not a reliable runtime localization recipe; write the required language files instead.

Asset 100274 supplies existing styles such as `storagegood`, `percentage`, `knots`, `maintenance`, `float` and `time`. `knots` applies multiply(2) then one decimal; `maintenance` applies sign, zero decimals and invert. Serp reports adding entirely new style names did not work. The schema permitting a Styles vector is not proof that the renderer accepts arbitrary newly introduced styles.

`ValueAssetMap` maps value ranges, in ascending order, to assets. Serp observed loss of integer precision for large ValidFrom values, with examples around 32–36 million and larger GUID-sized values. This is not a proven exact maximum. Do not use it as a lossless GUID dictionary.

## Compatibility and troubleshooting

For an existing layout, put legacy ModOps under `<ModOps>` in the mod's `data/infotips/export.bin.xml`. Use `Path="//InfoTipData[Guid='…']/..."` to select it; the 117 infotip `GUID` shortcut is not established for 1800. The actual selector from `shared_ItemsetTooltip` is:

    //InfoTipData[Guid='501233']/InfoElement[SubText/TextGUID='15782']

It selects one native row. `AddNextSibling` on that row inserts after it; `add` on the row would append inside it. The mod inserts a type-8 container copied in shape from native layouts, with its own visibility and child counts. Match the row in the target extraction and in the real load order. A broad expression match may deliberately select several contexts; verify each owner and the expected count. Use a scoped leaf replacement when changing only a leaf, and keep predicates that depend on editable text or conditions as narrow as the feature allows.

For a separate, new layout, the workspace's `DiploActions_Serp` illustrates three coordinated changes: insert new `InfoTipData` records as siblings under `Content`; add corresponding `Template=InfoTip` assets with the same `Standard/GUID` and an `InfoTip` property; and point the notification buttons' `CharacterNotification/ThirdpartyNotificationButtons/Item/Infotip` at those GUIDs in their asset templates. Add localization separately if using new text IDs. Audit the receiving field and allocate fresh GUIDs; copying a layout by itself will not bind it to a widget. The WIP `Disasters` moving-storm tooltip follows the same pattern through its minimap `Tooltip` field.

Find a semantic selector using Guid, text/condition markers and the audited ancestor context. Replacing a layout branch changes selectors other mods may depend on. Adding a sibling generally disturbs fewer existing anchors; insertion still requires valid context and counts.

The infotip guide deliberately recommends keeping mismatch errors visible for required compatibility anchors. Do not hide all errors with AllowNoMatch/Condition. Package a reusable tooltip fix as a separate shared mod; a specialized fix should also remain separable so a later general solution can supersede it.

Failure checklist: correct resource path; correct Guid spelling; selector still matches after dependencies; counts present where required; correct nested enum shape; typed expected values; existing reference/template/variable; correct hovered/selected object context; text renderer support for that widget.

### Workspace examples by purpose

These are source examples, including WIP mods. Read the active `Include` chain and `modinfo.json` of the actual copy before borrowing an operation. A copied include may be byte-identical even when its entrypoint or load order differs.

| Workspace source | What to look for |
| --- | --- |
| `Anno-1800-Mods/Recommended-Mods/MoreInfoTooltips (Serp)` | Includes for build menu `25000020`, ship costs `500057`, ship stats `500230/500460/500503`, storage and permit context. Ship stats includes a second file with separate layout records and asset-side consumers. Metadata orders it after the tooltip bug fixes and shipyard helper. The Diplomacy Sabotage copy has different build-menu/storage includes despite the same entrypoint. |
| `SharedMods/shared_TooltipBugFixes` | Included fixes for building warnings and permit costs/source, ship permits, population, research, tourist hotspots, buff targets, exclusive items, production outputs, plus/minus signs and newspaper. Some selectors target rows introduced by other mods: the four permit source IDs `2100119815`, `2100119818`, `2100119816`, `2100119829` have no hit on clean Vanilla. Check intent and load order before treating a zero hit as a bug. |
| `shared_TT_MenuInputOutputAmounts`, `shared_TT_MultipleInputAmountUpgrade` | Menu/module input-output rows on `25000020/500683` versus iterator logic in shared template `454144439`. The multiple-input patch and the production-output bug fix both touch this template; inspect their affected branches together. |
| `shared_ShipyardForBuffsTooltip`, `shared_ShowBuffTargetsTooltip`, `shared_ShowIndirectItemEffects`, `shared_ItemsetTooltip` | Four separate data paths: dummy ship effect targets, target visibility on `25000102`, indirect item effects through a Costs convention, and an unfinished item set using a different reference context from the completed set. Read the corresponding asset patches and comments before reusing their data conventions. |
| `shared_TT_ModPalaceMinistryHacienda` | Generalizes hardcoded cases around policy/decree effect targets in `269559`. Its condition replacements can match multiple native branches. Check both positive and complementary branches. |
| `shared_FertilityBuffs/[Shared] Pools and Definitions`; Community Bugfixes copies | The production-chain description patch on `500038` reads the asset's `Standard.InfoDescription`. Community examples also include custom tourist buildings and residence branches, storage trend `25000205`, and influence `500880`. |
| `Anno-1800-Mods/WorkInProgress-Mods` | `shared_Honor` extends population, profile/resource and attractiveness UI through includes; `Limited Preferred Profits (Serp)` adds an item-socket row; `Disasters (Serp)` and `Diplomacy Sabotage (Serp)/DiploActions_Serp` add layouts and consumers. The separate Sabotage tooltip file is a stub with no active ModOp. |

### Source and verification scope

2026-11-10 structural audit: the supplied `infotips_export_data30.xml` and configured extraction's `export.xml` are byte-identical, SHA-256 `3ab707e64bf59b3ff7415d56f1371b525ed3f3e5105833240250bc789a61f5d6`. The accompanying extracted `data/infotips/export.bin` hash is `b88fc4f9388f83fe621522b16d20bb7196cbeebcba9fe1a53608be9fe5b0f52e`; the XML was compared to the existing decode, without a fresh re-extraction from the installed game. Main `assets.xml`: `08b6cc7023aa1d834f2e6c2042848a3b3e2f13fcc44735a6248f6b6622d42c6a`; English texts: `e86ed2baec84581974dced4e5bfb8f1c5eed79df085d14494ed85b5fece08ace`. Inspected the relevant defaults and schema alongside the assets and layouts. The count repair above is from the [pinned 1800 serializer](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/xml_filedb_reader.cc).

The workspace sweep inspected 184 XML files directly under `data/infotips` across 57 mod directories (including ignored/bundled copies); 49 distinct file contents by SHA-256. ModOps, includes, new GUIDs and standalone XPath matches against clean Vanilla were inspected. Individual matches are structural evidence, not a simulation of mod order. For example, the WIP `shared_Honor/attractivness_info.include.xml` selector has a trailing slash that standard XPath rejects; it is not a pattern to copy. For a concrete patch, run the [1800 offline loader checks](../tools/README.md) on the actual dependency order and inspect logs and the resulting nodes.

No new rendering tests were performed. Remaining runtime-only cases require inspecting the intended widget with different selection/hover states, languages and lock states; multiplayer-local UI actions need the separate synchronization review.
