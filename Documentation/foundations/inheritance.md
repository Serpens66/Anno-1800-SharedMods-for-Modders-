# Assets, properties and native inheritance

## Resolution sources

A normal full asset stores its identity in `Values/Standard/GUID`, with a developer-facing `Name`. Its `Template` determines its property composition. A `BaseAssetGUID` derives from another asset instead. Missing effective values can come from the base, its template and property defaults. Follow the complete chain before deciding a field is absent.

The game resolves this after ModOps. Loader XPath works on the serialized document, not a materialized table of every inherited field. Changing the template may alter much more than the visible XML fragment: the new property composition and defaults must be audited.

Source: [Serp's inheritance guide](https://github.com/anno-mods/modding-guide/blob/main/guides/Inheritance.md), native contracts linked below.

## Audited small example: Skin 5244

The extracted asset `5244` is `CDLC09 Residence Tier02`. It explicitly defines Standard, Skin, Locked and Text. The `Skin` template provides those same properties and overrides `Locked/Scope` to `Account`; the general Locked default is `Participant`. Therefore omitting a scope in this Skin asset does not select the general Participant default.

The Skin schema defines `SkinName`, `SkinDescription`, the `SkinVariations` vector of `Item/FileName`, and `SkinCategoryDescription`. Asset 5244 sets name text 5246, description text 5247, category text 5753, four CFG variations and DLC dependency 24965. The dependency resolves to the Old Town cosmetic DLC asset, which includes 5244 in its unlock list. A derived copy will retain this dependency unless a separately audited override changes it.

The default Skin entry explicitly provides name 0, description 0 and an empty variations vector. Do not infer every unspecified property's default is zero merely from that example. `properties-toolone.xml` can define authoring behavior, while `properties.xml` and templates show actual supplied defaults.

Provenance: [vanilla-contracts.json](../reference/vanilla-contracts.json), asset 5244 at assets line 215094, Skin template at templates line 7954, Skin schema at property-definition line 12830, Locked schema at line 28805, defaults and text entries. [runtime-contracts.json](../reference/runtime-contracts.json) includes DLC asset 24965.

## Omission, empty scalars and vectors

Serp's later tests in the inheritance guide report that omitting a scalar or writing its empty tag retains the inherited scalar value. An empty property container such as `<Locked />` also does not discard all values supplied by the base. The local notebook preserves an earlier explanation that suggested resetting empty scalars to defaults; that earlier explanation is not the selected current rule. The original 2020 forum remains a separate source-access/reconciliation task in the coverage register.

Vectors behave differently:

| Derived asset XML | Result reported by the guide |
| --- | --- |
| Omit `SkinVariations` | Inherit the base's complete vector. |
| Provide a populated `SkinVariations` | Use that vector; omitted base entries are not automatically appended. |
| Provide `<SkinVariations />` | Override the vector with an empty vector. |
| Provide `Item/VectorElement/InheritedIndex` | Inherit the explicitly referenced base/template vector entry, optionally overriding its fields. |

Native `InheritedIndex` is **zero-based**. XPath item positions are **one-based**. Confusing them selects the wrong entry even if both XML and XPath parse.

```xml
<SkinVariations>
  <Item>
    <VectorElement><InheritedIndex>0</InheritedIndex></VectorElement>
  </Item>
  <Item>
    <!-- Keep the third inherited variation. -->
    <VectorElement><InheritedIndex>2</InheritedIndex></VectorElement>
  </Item>
</SkinVariations>
```

This is a property fragment for a derived Skin asset, not a standalone ModOps document. The guide's original mixed-vector example has a missing `Item` boundary; do not copy that malformed example. The native ornamental asset 5187 also demonstrates indices 0-5 in its Costs vector and an Amount override on index 0. Its XML and the OrnamentalBuilding template are preserved in the runtime contracts.

The guide reports that `InheritanceMapV2` is unnecessary according to Taube. Native exports still contain it. Treat the reported lack of effect as guide evidence, not proof that every serialized occurrence is meaningless in every game build; simple documented inheritance examples use `InheritedIndex`.

## Adding a derived asset

Use an 1800 `ModOp Type="addNextSibling"` targeting the base to place the derived asset after it. Give the new asset its own allocated GUID. Do not reuse the guide's illustrative `1111111111111`: it is not a suitable signed 32-bit mod GUID. Do not treat the last free-GUID note in `HowTo.xml` as a current allocation ledger without checking the workspace and the reserved range.

```xml
<ModOps>
  <ModOp Type="addNextSibling" GUID="5244">
    <Asset>
      <BaseAssetGUID>5244</BaseAssetGUID>
      <Values>
        <Standard>
          <GUID>CUSTOM_SKIN_GUID</GUID>
          <Name>My derived Old Town skin</Name>
        </Standard>
        <Skin>
          <SkinVariations>
            <Item>
              <VectorElement><InheritedIndex>0</InheritedIndex></VectorElement>
            </Item>
          </SkinVariations>
        </Skin>
      </Values>
    </Asset>
  </ModOp>
</ModOps>
```

`CUSTOM_SKIN_GUID` is a required substitution, not deployable integer syntax. This example defines a derived asset retaining one existing variation. It does not by itself add the Skin to a building's skin-selection list, allocate a new translation or satisfy account/DLC unlocks for the new GUID. Those are separate consumers to audit before calling it a usable new skin mod.

`Text/TextOverride` can reuse another asset's display text where appropriate, as the guide demonstrates. Text references do not allocate a new identity, and a developer `Standard/Name` is not a localized display string.

## Property membership is not an API capability test

Do not conclude that an object has a runtime property because a Lua textsource facade lets you spell its getter. Serp's notes report calls remain addressable even for objects without the property. Conversely, infotip property-existence checks have special semantics. Use the actual asset/template contracts and the verified helper property-check procedure for the task.
