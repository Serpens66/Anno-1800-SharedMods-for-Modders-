# Creating Reward Pools in Anno 1800

## 1. Structure and creation

A reward pool is an asset containing candidate rewards. Creating it does not automatically add rewards to traders, quests or expeditions: a consumer must reference its GUID, directly or through another pool.

`RewardPool` and `RewardItemPool` are **template names**. Both provide the **property** `RewardPool`, with entries under `Values/RewardPool/ItemsPool/Item`. The former additionally supplies `Text`; both override `Locked/DefaultLockedState` to `0`. The name `RewardItemPool` does not establish an items-only restriction: both use the same property schema.

Place this example in your mod's `data/config/export/main/asset/assets.xml`. Replace every `NEW_POOL_GUID` with one unused GUID from your mod's allocated range. The placeholder is not deployable. Grain (`1010192`) and beef (`1010193`) are verified vanilla Product assets.

```xml
<ModOps>
  <ModOp Type="addNextSibling" GUID="112574">
    <Asset>
      <Template>RewardPool</Template>
      <Values>
        <Standard>
          <GUID>NEW_POOL_GUID</GUID>
          <Name>My Goods Reward Pool</Name>
        </Standard>
        <RewardPool>
          <ItemsPool>
            <Item>
              <ItemLink>1010192</ItemLink>
              <MinAmount>5</MinAmount>
              <MaxAmount>5</MaxAmount>
              <Weight>3</Weight>
            </Item>
            <Item>
              <ItemLink>1010193</ItemLink>
              <MinAmount>2</MinAmount>
              <MaxAmount>2</MaxAmount>
              <Weight>1</Weight>
            </Item>
          </ItemsPool>
        </RewardPool>
        <Locked />
        <Text />
      </Values>
    </Asset>
  </ModOp>
</ModOps>
```

`112574` is only an insertion anchor, not a base asset or reward source. Insertion location matters because vanilla groups can themselves be referenced by pools; avoid arbitrary placement inside reward-bearing groups.

## 2. Linking pools and consumers

To include your pool in an existing parent, append an entry to the parent's existing `ItemsPool`. Replace `PARENT_POOL_GUID` and `NEW_POOL_GUID`; execute this after creating the new asset, inside your `ModOps` root:

```xml
<ModOp Type="add" GUID="PARENT_POOL_GUID"
       Path="/Values/RewardPool/ItemsPool">
  <Item>
    <ItemLink>NEW_POOL_GUID</ItemLink>
    <Weight>1</Weight>
  </Item>
</ModOp>
```

Confirm that the selected container exists explicitly: loader XPath sees serialized XML before game inheritance. `add` appends; repeated execution or overlapping mods can create duplicate entries.

A concrete vanilla chain is quest `151562` -> reward pool `151049` -> goods pool `151062` -> Product assets. The quest references its pool through `Values/Reward/RewardAssets/Item/Reward`, with `Amount=1`. Changing a shared child pool affects consumers that reach it through their parent pools.

`ItemGroup` instead references a **group ID**, not an asset GUID. Vanilla pool `151049`, for example, references group `902574339`. The schema says this folder is used only when `ItemLink` is empty, and all items in the folder receive the same weight. Group IDs can be negative; do not substitute item GUIDs or invent folder identifiers.

## 3. Weight and amount

`Weight` is an integer relative selection weight, not a percentage or reward quantity. Its entry default is `1`; weights need not total 100. For ordinary flat weighted selection among eligible candidates, the model is `chance = weight / sum of weights`: weights 3 and 1 give 75% and 25%. This example assumes both candidates are eligible and no consumer-specific filtering changes the draw.

For groups, the schema assigns weight to each contained item; do not treat a whole folder as one equally weighted candidate. Membership changes can therefore change the distribution.

Nested links are supported, but the inspected XML does not prove the engine's precise nested normalization, flattening or duplicate-handling algorithm. Do not promise exact final percentages by multiplying parent and child fractions. Repeated paths to the same reward also require care, particularly with uniqueness settings.

`MinAmount` and `MaxAmount` are integers, both defaulting to `1`. Set them equal for a fixed quantity. **Both are ignored when `ItemLink` references a pool**; specify quantities on the eventual reward entries. Use positive weights and sensible positive amounts; zero/negative-weight behavior, numeric limits and cyclic-pool handling are not established here.

## 4. Allowed references and related pools

Restrictions below concern the target asset's effective **properties**, including template/base inheritance, rather than its name or GUID range.

| Reference field | Schema-declared target properties |
| --- | --- |
| `RewardPool/ItemsPool/Item/ItemLink` | `Product`, `Item`, `RewardPool`, `RegionRewardPool`, `BuildPermit` |
| `Reward/RewardAssets/Item/Reward` | The above, plus `ResourceRewardPool` and `Session` |
| `ResourceRewardPool/PossibleRewards/Item/Resource` | `Product` |
| `RegionRewardPool/RewardPools/<Region>/RewardPool` | `RewardPool` |

These lists identify declared compatible categories, not permission to reward arbitrary buildings, ships or triggers. In particular, the broader quest-reward list must not be copied to `ItemLink`.

Template `ResourcePool` supplies `ResourceRewardPool`: its `PossibleRewards` entries contain `Resource`, integer `Amount` and integer `Weight` (default 1, declared minimum 1). Amount is modified by `ResourcePoolModifier`. Vanilla `150038` is a money pool referencing Product `1010017`.

`RegionRewardPool` provides a region-keyed array, not an `Item` vector. Dataset keys are `Meta`, `Moderate`, `Colony01`, `Arctic`, `Africa`, `Mod1`, `Mod2`, `Mod3`. This structure is schema-backed; no concrete instance was found in the inspected main asset set, so missing-region fallback is unverified.

## 5. Additional controls and evidence

- `IgnoreUnlocks` permits locked rewards. The consumer's separate `Reward/GenerateIgnoreUnlocks` controls unlock checks during reward generation; do not assume undocumented precedence.
- `GenerateUniqueRewards` defaults to `1`; its description prevents repeated ItemLink rewards within a generation and resets afterward. Consumers also have `Reward/GenerateRewardsUnique`.
- `DivingScrapAmountLevelNeeded` gates weight use by an upgrade level. `RewardDescription` is a localized-text reference.

Checked against current extracted `assets.xml`, `templates.xml`, `properties-toolone.xml`, `properties.xml` and `datasets.xml` on 2026-10-05. These establish data contracts, not engine implementation or an in-game probability test. Validate the patched XML, then test the intended consumer in-game.
