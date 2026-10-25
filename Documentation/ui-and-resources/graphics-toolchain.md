# Graphics conversion and Blender authoring sources

## Scope and prerequisites

This chapter documents the reviewed converter/addon interfaces and the graphics guides' procedures and qualifications. It is not a completed vanilla audit for every model, animation, blocker, particle or material. Before applying the workflow to a particular asset, follow its Object variations, CFG/subfiles, IFO, feedback, shaders, sequences and material/texture references together. That feature-specific audit is required by AGENTS.md; successful conversion alone cannot waive it.

Primary sources are [rdm4](https://github.com/lukts30/rdm4/tree/a1d5970021b2332babb36edecfc80cc7e3ad2503), the [original Blender addon](https://github.com/xormenter/Blender-Anno-.cfg-Import-Addon/tree/358cde764c8999bf59ef55a63af7f99e32f529fe) and its explicitly linked [Anno 1800 successor](https://github.com/anno-mods/Blender-Anno-1800/tree/c790c97572edfa6b2ea5fcb229feaff0fc753185). The original addon is discontinued. The separate Blender-Anno-117 repository is not this game's addon.

The reviewed addon README targets Blender 3/3.2 and lists rdm4, Microsoft DirectXTex `texconv`, Jakob's AnnoFCConverter, optional A.N.T. Landscape for island previews, and RDA extraction. These are the source's version requirements, not a claim that every later Blender version is supported. Configure the extraction root to the folder **containing `data`**, and configure the actual converter executable paths. A scene's mod folder allows resources to be found in the mod as well as the extraction.

## rdm4 command-line contract

The reviewed README advertises `0.11.2-alpha.1`; it was reconciled with `src/main.rs`. `-i/--input` requires an existing file; `-o/--outdst` sets output; `-n/--in-is-out-filename` uses the input filename and requires an output directory when combined with `-o`. `--force` permits overwrites, so work on copied resources. Explorer context-menu integrations do not expose the animation workflow.

RDM → glTF uses `-s/--skeleton` for joints and `-a/--animation` for animation, with an external animation file specified by `-m/--rdanimation`. Animation requires skeleton; an external animation file requires both. glTF → RDM requires `-g/--gltf` with the destination vertex format. `--gltf-mesh-index` defaults to zero; a multi-mesh glTF must select the intended mesh, rather than assuming all meshes are exported as one RDM.

`--no_transform` suppresses glTF node transforms and is documented for animation workflows. `--negative-x-and-v0v2v1` mirrors X and reverses triangle winding; **the current CLI prohibits combining it with skeleton/animation**. Therefore a static-model mirroring command is not interchangeable with an animated conversion. The crane guide prepares the mirrored model before animation instead.

`--overide-mesh-idx` is the CLI's actual spelling (one r in `overide`). It overrides material/mesh-instance indices; the inspected converter requires one override per primitive. `-u/--gltf-node-joint-name-src` selects `UniqueName` (default) or `UnstableIndex`. Older guide references to `--unstableIndex` do not match this current interface. Unique bone/node names are preferable when preserving references; index-derived names may change after scene edits.

RDM → glTF output formats are `glb`, `gltf`, `gltfmin`, default `glb`; `-t/--diffusetexture` supplies diffuse texture files. A glTF container format does not solve missing normals, tangents, UVs, joint weights or vertex color data.

## Destination vertex formats

| Converter format | Documented use and required data |
| --- | --- |
| `P4h_N4b_G4b_B4b_T2h` | Ordinary static model with positions, normals, tangents and UVs. |
| `P4h_N4b_G4b_B4b_T2h_I4b` | Joint indices without stored weights; the crane guide uses rigid bone assignment and CFG NumBonesPerVertex=1. |
| `P4h_N4b_G4b_B4b_T2h_I4b_W4b` | Joint indices and weights, e.g. portraits; requires the corresponding glTF attributes. |
| `P3f_N3f_G3f_B3f_T2f_C4b` | Cloth, with vertex colors. |
| `P4h_N4b_G4b_B4b_T2h_C4b_C4b` | Plants, with two color channels; the README notes a Blender 4.2 exporter issue. |
| `P4h_T2h_C4b` | Decal detail, with color controlling luminosity variation; guide neutral gray 0.5. |

The current CLI help text lists only three formats, but its `TargetVertexFormat` handling and README describe six; do not treat the shortened help summary as exhaustive. The inspected glTF reader handles the cloth/plant/decal variants explicitly.

Missing normals/tangents trigger errors and fallback values in the inspected converter, which can still leave a generated file. Missing joint/weight data with skeleton export can panic. Check converter logs, exported attributes and reimported geometry, not just whether an RDM filename exists. For animated glTF the reader also reads weights even when the chosen destination omits stored weights; do not deliberately strip weight data from the source based only on `_I4b`.

The animation guide's suggestion that the engine permits only one bone per vertex is explicitly a guess for its example. Weighted converter support is separate evidence and does not justify a universal one-bone limit or guarantee every weighted format in every material context.

## Blender scene and material structure

The addon uses `MAIN_FILE_*` as the main parent, with model/prop/particle/decal/subfile children corresponding to CFG hierarchy and special `IFOFILE`/`CF7FILE` children. Parent hierarchy determines export membership; displayed object prefixes help humans but do not themselves define ConfigType.

Export edited meshes as RDM before exporting the main CFG. Resources must reside below the configured extraction/mod root so paths can become game-relative. Duplicate an imported Anno material when creating another material: an ordinary Blender material lacks the required XML properties and shader-node names. Cloth and model materials are incompatible. A PNG preview is not a packaged DDS texture; verify the actual referenced game texture and mip variants.

IFO cuboids use object position, scale and rotation; editing their mesh vertices does not define their intended extents. IFO planes depend on vertex positions. The IFO guide explicitly warns against applying all transforms to its cuboid objects, while the generic addon advice recommends applying transforms to **exported model meshes**. These instructions concern different object types and are not a blanket contradiction.

Asset-browser collections initially instantiate a scene. `Instanced Collection To FILE_` produces a reference which cannot be directly edited/animated; `Make Instances Real` with hierarchy preserved produces editable objects. Imported props require a PropContainer parent. Missing parents can make the result disappear from the exported CFG despite looking correct in Blender.

The addon can import/export parts of island gamedata and RD3D; its coarse heightmap is preview-only, with uncertain vertical scale in the README. It is not a complete island editor. See [binary formats](binary-formats.md) for island files and the remaining terrain audit.

## Animation guide: creation and edited native rigs

[Create RDM animations](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/guides/rdm_animations.md) uses a crane, rigid vertex groups and matching bone names. Every material applied to that example uses the animated vertex format and NumBonesPerVertex=1, including unanimated pieces of the same model. Parent child bones with keep-offset where movement should inherit; group/bone names must match. Mesh names must differ from joint names to avoid the converter's name-resolution collision.

Use pose-mode keys with explicit held/rest positions. Add intermediate keys for large rotations rather than expecting a single 360-degree key to produce a full turn: quaternion interpolation chooses the shorter route. Translation and rotation are supported; animation scale channels and morph-target weights are documented as unsupported by this converter. Sample animation consistently; the README requires compatible timestamps and recommends Blender's Always Sample Animations.

The inspected export-settings image shows selected objects, +Y Up, UVs/normals/tangents/colors enabled, Apply Modifiers disabled, animations enabled, playback-range limiting, sampling rate 1 and Always Sample Animations. It also enables NLA grouping, export of all armature actions and reset pose between actions. These are example settings, not a promise that exporting unrelated armature actions is always desired.

The guide's frame-to-time formula assumes **24 fps**: `milliseconds = frames * 1000 / fps`. Its “249 frames = 10.375 ms” statement is a units/editorial error: at 24 fps this is **10375 ms**, or 10.375 seconds. Use the scene's actual fps and converter's duration, not that mistaken unit. Animation CFG Scale greater than one is described by the guide as slower playback; that runtime claim remains tied to the documented example, not a new game test.

[Edit existing animations](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/guides/rdm_animations_edit.md) addresses an extra exported armature node causing bone-index problems. It moves the intended armatures/mesh out of the imported MAIN_FILE, selects the intended Armature modifier and reparents newly added bones appropriately. Its illustrated export uses embedded glTF text to allow manual node editing.

Deleting a glTF node shifts indices: scene roots, child lists, skin joint/skeleton references and animation target references must remain coherent. The tutorial's local indices are example-specific; changing only its demonstrated scene entry is not a proven repair for arbitrary models. Validate the complete reference graph and converter output. The tutorial expressly limits confidence across all models. No modified animation was deployed or tested here.

## Related guide findings awaiting native feature audits

[Cloth](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/guides/clothes.md) uses white vertex color for fixed regions, black for maximum simulated deflection and intermediate values proportionally; preserve normals and UVs and export colors. Its RDM cloth format differs from the cloth shader's CFG `VertexFormat` label; those are distinct representations. An inspected native `airport_flag_02.cfg` indeed has a `Clothes/Config` with CLOTH material, `P3f_N3b,T2f`, WindStrength 0.5, Gravity 0.01 and a separate orientation transform. Its complete asset/variant/material audit is not yet closed.

[Particles](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/guides/particles.md) explains RDP interpreted arrays: UInt16 start/end, Byte material index, signed Int16 relative positions, Byte rotations/scales/colors. Position is relative to center and scaled by extents; colors are BGRA in the original representation. The VS Code simplified representation presents named vector/color fields and derives end from tick count. A converter-specific audit is still required for exact wrap/rotation-axis behavior.

[Mesh height maps](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/guides/Mesh-Height-Maps.md) describes IFO sampling coordinates and pre-existing Blender grid vertices. Its example width 65 and height 33 describes **2145** samples, not the stated 2048: 64×32 counts the intervals/cells. Preserve vertex-sample dimensions and verify the exporter before creating a new map. The suggested base height and coordinate assumptions remain example-specific until the corresponding native IFO and placement behavior are audited.

The [IFO reference](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/documentation/ifo-file.md) covers blockers, dummies, connection points, feedback, hit/selection boxes and sequences, and explicitly marks several functions unknown. Those unknowns must not become guaranteed runtime instructions. A complete IFO topic and native reference audit remains in the coverage queue.
