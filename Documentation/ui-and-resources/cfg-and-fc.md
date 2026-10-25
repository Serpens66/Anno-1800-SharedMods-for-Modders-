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
