# CFG and FC patching

This chapter establishes the loader's file/serialization contract and identifies the feedback guide's terminology. A new graphical object also needs the feature audit of its assets, native graphics and every referenced resource; a patchable file is not by itself a usable model.

## Loader contract for Anno 1800

Place a ModOps patch at the **same relative game path**, adding `.xml` to the resource extension:

| Game resource | Mod patch |
| --- | --- |
| `.../world_map_01.cfg` | `.../world_map_01.cfg.xml` |
| `.../world_map_01.fc` | `.../world_map_01.fc.xml` |

A full file at the original path is a replacement; `.cfg.xml` or `.fc.xml` is a patch applied to the resolved original. The current 1800 reference notes patching is more expensive than replacement. Compatibility may still justify a targeted patch when several mods need to extend one file; replacing a complete shared world-map resource can erase other changes.

CFG is XML and uses ordinary XPath against its actual root/structure, not Asset GUID helpers. `//Models` or `/Config/...` is only correct if that particular CFG has those nodes. Multiple Config sections can exist; constrain the selector by ConfigType, Name or a verified path as appropriate.

FC is a binary feedback format. The loader decodes it to a FileDBReader-compatible XML tree, applies XML operations, fixes automatic IDs and serializes it back. Do not manually paste decoded XML into a binary `.fc` file. The game's CFG/FC/IFO/model relationship must be traced from the native asset's Object variations.

Sources: [1800 patch reference](https://jakobharder.github.io/anno-mod-loader/cfg-fc-patches/), pinned1800 `xml_auto_serializer.cc`, `xml_fc_reader.cc`, and [feedback guide](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/guides/fc-files-guide.md).

## Automatic feedback IDs

The inspected FC fix pass selects Id elements starting with `$auto` and allocates successive IDs from the root IdCounter.

- `$auto` allocates a new ID for that occurrence.
- `$auto(0)`, `$auto(1)` and similar labels reuse one allocated ID when that label occurs again in the same fix pass.
- The number in parentheses is a label, **not the final numerical ID**.
- IdCounter is updated after allocation. Do not assume a fixed output ID when another patch also adds feedback elements.

Use the labeled form when an added definition and its references must share an ID. Do not replace references with a guessed integer. Existing IDs and paths still require their own validity checks.

The FC reader represents binary integer-array CDATA as space-separated int32 values for editing; the writer converts these values back to binary and adjusts length. Thus a displayed GUID/variation pair list is a special serialized field, not arbitrary readable text.

## Terms that must remain distinct

The guide distinguishes a **CFG sequence** from an **FC object sequence**, an **actor sequence** and an **action**. They are different layers, even when their names or numeric values happen to coincide.

| Term | Guide meaning |
| --- | --- |
| Dummy | Fixed position and rotation |
| DummyGroup | Dummies and nested groups |
| Actor / Feedback Definition | Unit with supported behaviors and instances |
| Spline | 3D curve |
| Object sequence | Whole-object state selecting actor behavior |
| Actor sequence | Intro, running and outro behavior |
| Action | Individual movement/fade/animation step |

`FeedbackLoops` stores index-paired k/v lists: k is a FeedbackSequenceType dataset value, v is a zero-based actor SequenceDefinitions position. Interleaving k/v pairs is not required if both sequences preserve the corresponding order. `ValidSequenceIDs` declares supported states; the guide reports Default is supported even if not listed.

The extracted vanilla FeedbackSequenceType dataset contains **nine** entries, Default0, Work1, LowProductivity2, Cheer3, Boosted4, Riot5 and RiotSpecial01/02/03 at6/7/8. The guide's introductory “8” count is inconsistent with its own nine-entry example; retain the actual dataset. It reports Default is idle and Work follows positive factory productivity. That runtime behavior is guide evidence, not a new test here.

## CFG render conditions and sequence tracks

### Quick lookup by desired condition

For a single named condition, use its **CFG number** from the table. To combine several distinct entries, select them in the [CFG Condition Converter](../tools/cfg-condition-converter.html) or add their CFG numbers once each. For example, selecting `Common02` (64) and `Common09` (8192) produces `8256`. These are the two slots used in the projectile example below. The result encodes the selected entries. The specific transform determines how it acts on them.

| What you want to reference | CFG number | Vanilla name |
| --- | ---: | --- |
| No conditions selected | 0 | â€” |
| Color transform state | 1 | `ColorTransform` |
| Physics transform state | 2 | `PhysicsTransform` |
| Destruction transform state | 4 | `DestructionTransform` |
| Selected | 8 | `Selected` |
| Unselected | 16 | `Unselected` |
| Common slot 1 | 32 | `Common01` |
| Common slot 2 | 64 | `Common02` |
| Common slot 3 | 128 | `Common03` |
| Common slot 4 | 256 | `Common04` |
| Common slot 5 | 512 | `Common05` |
| Common slot 6 | 1024 | `Common06` |
| Common slot 7 | 2048 | `Common07` |
| Common slot 8 | 4096 | `Common08` |
| Common slot 9 | 8192 | `Common09` |
| Common slot 10 | 16384 | `Common10` |
| Common slot 11 | 32768 | `Common11` |
| Daytime sky | 65536 | `SkyDay` |
| Shield effect | 131072 | `EffectShield` |
| Repair effect | 262144 | `EffectRepair` |
| Stun effect | 524288 | `EffectStun` |
| Burn effect | 1048576 | `EffectBurn` |
| Warning lights | 2097152 | `ShowWarningLights` |
| Riot | 4194304 | `Riot` |
| Special riot state | 8388608 | `RiotSpecial01` |
| No inhabitants | 16777216 | `NoInhabitants` |
| Ruin | 33554432 | `Ruin` |
| Irrigated | 67108864 | `Irrigated` |
| Default ground decal | 134217728 | `GroundDecalDefault` |
| Ground decal variation | 268435456 | `GroundDecalVariation` |
| Electricity | 536870912 | `Electricity` |

For a named state such as **Electricity**, look up `536870912`. Vanilla uses this value on electric-lamp subfiles. For an effect driven by a **Common slot**, start from the matching sequence and look for the number shared by its track and the target transform. For example, the brass smelter uses `64` for steam during work, while the clipper also uses `64` in its idle sequence. Use the number from the example that matches the object and resource you are editing.

### Source and sequence examples

**Vanilla data.** `properties-toolone.xml` describes `GlobalConfig/RenderConditionIDs` as IDs for communication with the render engine when modifying CFG states. Its declared type is an array keyed by the `RenderCondition` dataset. The defaults in `properties.xml` contain 30 named renderer IDs, also present in the authoring defaults. Asset 2001270 (`GlobalBalancing`, template `GlobalConfig`, no base asset) supplies its own `SequenceIDs` and has no `RenderConditionIDs` override. The dataset item IDs identify the named entries. For example, `Irrigated` has dataset ID 27 and renderer ID 27, while `Common01` has dataset ID 5 and renderer ID 6. Using the dataset ID as a general conversion rule would shift many entries. [Inspected Vanilla source identities](../reference/vanilla-contracts.json).

The derived CFG values use `1 << (renderer ID - 1)`. Zero has no named entry in the renderer ID array. Native examples corroborate this interpretation.

- `Sequences/Config/Track/TrackElement/Condition` occurs on sequence tracks. The singular field can carry multiple bits. In `projectile_cannon_area_very_large_01.cfg`, sequence 2411 (`missland` in asset 2001270) has a Type 2 track with `Condition=8256` (64 + 8192). The file uses 64 on a prop-container visibility transform and 8192 on a light visibility transform. Sequence 2410 (`misswater`) has a track with 8192 alone. The adjacent Type 1 particle tracks use `ParticleID` as a separate field.
- `Transformer/Config/Conditions` occurs on the consuming transform. A color transform in the same projectile CFG has `Conditions=2080` (32 + 2048) and two child `State/Condition` entries, 32 and 2048, with different alpha values. This is direct structural evidence for a combined transform mask and distinct per-state values. It does not establish a universal AND/OR rule for every transform type.
- The same generic bit can occur under different sequences. `clipper.cfg` uses 64 in sequence 1000 (`idle01`) and 96 (32 + 64) in sequence 2000 (`walk01`). `heavy_09.cfg` uses 32 in 1000 and 64 in 3000 (`work01`), including a 64 visibility transform on a steam particle.
- For named engine states, `irrigation_channel_short_01.cfg` uses 67108864 (`Irrigated`) on irrigation plants and waterfall particles. `multifactory_02_03.cfg` uses 536870912 (`Electricity`) on subfiles referencing `electric_lamp_01.cfg`. These are corroborating native consumers. Engine activation of every named state and the interpretation of `RenderPropertyFlags` were not tested.

The extraction examined on 2026-11-26 contains 7,928 CFG files under `data`. The XML scan inspected numeric `Condition` and `Conditions` elements by parent type. It found 60 distinct values in sequence `TrackElement/Condition` entries, including zero and combinations. The projectile CFG is at `data/graphics/effects/military/projectiles/projectile_cannon_area_very_large_01.cfg`, SHA-256 `946543f64c142bd5af9c6efdb7f50cac6277b208ab39fc793959719a7ef3e9a6`. These are structural observations. A specific graphics change still needs its asset and resource audit. [Original question](https://discord.com/channels/578443209940926465/1080167315452203040/1241206857704407051), [context-dependent advice](https://discord.com/channels/578443209940926465/578443576552325143/1078196953424334888), [mask discussion](https://discord.com/channels/578443209940926465/1080167315452203040/1365752662707933295).

## Feedback guide findings to audit when authoring

The full guide was read. It reports these constraints:

- Dummy names inside an enumerated group must be consecutive; a gap can cause later units to lose positions and spawn at object center.
- RotationY is radians, Orientation is a quaternion, HeightAdaptationMode1 adapts to terrain and0 does not.
- Special names include FireDummy, feedback_door and bird_land. Dynamic feedback groups use `feedback_...` names and require the relevant FeedbackBuildingGroup registration; multiple memberships add spawn counts.
- AssetVariationList/GuidVariationList contains GUID/variation pairs; -1 means random variation, other indices start at0.
- Only one actor should be MainObject. It can affect CFG sequence behavior through dummy0.
- ActorCount, MaxActorCount, MultiplyActorByDummyCount and ApplyScaleToMovementSpeed govern instances/scaled movement.
- Loop0 is intro, Loop1 running and Loop2 outro. Intro/outro are optional; state such as scale carries between loops until despawn. A state transition need not interrupt the currently running walk/play count immediately.
- DefaultState sets initial loop state; ElementContainer actions run in their listed order.

These observations are a checklist for a matching native graphics audit, not a license to attach arbitrary groups to an unrelated object. The detailed modeling/island/animation guides and concrete native graphics chains still need their documented completion records.

## Failures and verification

Check the exact resource spelling/path and case, patch versus replacement extension, actual root, target match counts, ID references, corresponding CFG/IFO/model files and variation index bounds. A valid XML patch can produce an invalid graphical definition. Offline xmltest can check application/conversion, while displayed placement, animation, fire/hit dummies and state transitions remain runtime questions.

No graphical or game test was performed. A future runtime-only test should enumerate intended object states, each variation, rotation, terrain/height placement and graphics settings, and record both asset GUID and selected resource paths.
