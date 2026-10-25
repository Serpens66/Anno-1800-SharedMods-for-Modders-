# Infotips, localization and text expressions

Evidence: [the infotip guide](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/documentation/infotips.md), [textembeds](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/Scripting/textembeds.md), Serp's `HowTo.xml` final sections, and the selected vanilla contracts below. Runtime observations retain the guide/notebook's qualifications.

## The three separate data layers

1. Asset properties such as `Standard/Name` identify an asset internally. Display text can be supplied by the asset's `Text` property, aliases, or system-specific text references.
2. Localization files such as `data/config/gui/texts_english.xml` contain `<TextExport><Texts><Text><GUID>...</GUID><Text>...</Text></Text></Texts></TextExport>`. Patch them using their own root; they are not assets with `Values/Standard/GUID`.
3. Tooltip layouts are binary `data/infotips/export.bin`. The corresponding mod patch is **`data/infotips/export.bin.xml`** containing ModOps, not a replacement binary export.

The extracted `dataAlle/export.xml` is a research copy of the decoded export. Its name at the extraction root is not the game's resource path. FileDBReader can decode the binary with its infotip format definition; preserve the distinction between a decoded source and the patch deployed to the game.

Anno 1800's authoring schema already contains `Text/LineID` and an Oasis category. That does **not** establish support for Anno 117's different exported localization syntax or loader features. Use the 1800 text-file structure.

## A fully traced simple vanilla tooltip

The decoded export begins with `InfoTipData/Guid=373` at line 4. It has one type-3 InfoElement and `Text/TextGUID=23861`. The English text for 23861 is recorded alongside it in [vanilla-contracts.json](../reference/vanilla-contracts.json). The visibility wrapper is an element-type-2 container with empty `OperatorType`; the element has empty style/value/warning/background fields. There are no template, icon or dynamic-value references in this simple example.

This is a suitable starting point for tracing text layout. It is not a generic guarantee that a new tooltip GUID is automatically used by a newly created gameplay asset; the consuming asset/UI reference also needs an audit.

## Layout structure and counts

`InfoTipData` entries use **`Guid`**, not uppercase `GUID`. They contain ordered `InfoElement` children and may contain `Variables`. Layout order follows sibling order. Within an element, `VisibilityElement` controls its branch; nested elements form conditional containers.

The export represents enum-like fields with nested names, for example:

```xml
<ResultType><ResultType>1</ResultType></ResultType>
<CompareOperator><CompareOperator>5</CompareOperator></CompareOperator>
<ExpectedValueInt>0</ExpectedValueInt>
<Condition>[Selection Object Upgradability Reasons COUNT]</Condition>
```

This shape is present in vanilla tooltip 500934. Do not flatten nested wrappers just because a field name repeats.

The loader's FileDB serializer updates **existing** `ChildCount` nodes and export counts. It does not create a missing count. The guide reports types 7 and 8 require one; preserve a count from a traced native container when adding children. The serializer uses the maximum of the applicable sibling InfoElement/VisibilityElement counts, not a recursive descendant total.

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

Find a semantic selector using Guid, text/condition markers and the audited ancestor context. Replacing a layout branch changes selectors other mods may depend on. Adding a sibling generally disturbs fewer existing anchors; insertion still requires valid context and counts.

The infotip guide deliberately recommends keeping mismatch errors visible for required compatibility anchors. Do not hide all errors with AllowNoMatch/Condition. Package a reusable tooltip fix as a separate shared mod; a specialized fix should also remain separable so a later general solution can supersede it.

Failure checklist: correct resource path; correct Guid spelling; selector still matches after dependencies; counts present where required; correct nested enum shape; typed expected values; existing reference/template/variable; correct hovered/selected object context; text renderer support for that widget.

No new rendering tests were performed. Remaining runtime-only cases require inspecting the intended widget with different selection/hover states, languages and lock states; multiplayer-local UI actions need the separate synchronization review.
