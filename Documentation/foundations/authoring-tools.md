# Authoring tools and generated deployment output

## Scope and evidence

These procedures describe tooling, not game API contracts. Primary source: [vscode-anno](https://github.com/anno-mods/vscode-anno/tree/19cda8edc73d65a622c9c5c588953a0170c337c6), retrieved 2026-10-03. All documentation Markdown pages and the metadata reader, builder, metadata/assets/static/texture converters, DDS wrapper, downloader, deployment command and xmltest wrapper have been read. Other converters and tests remain under review. The pinned repository's package version and the installed extension both say **2.3.1**; matching version numbers alone do not prove matching binaries or source commits.

## Configure Anno 1800 explicitly

Open a folder containing complete mods. The current setup page distinguishes Anno 1800's `Anno: Rda Folder` and `Anno: Mods Folder` from the separate Anno 117 game-path settings. For this workspace the extracted-data root is `D:/CDesktopLink/Unterlagen/Mods/Anno 1800/Anno1800 RDA unpacked/dataAlle`, containing `data/config/export/main/asset/assets.xml`.

The metadata reader defaults to Anno 1800 unless `Anno` is 8 or a valid metadata file without Anno has a `data/base/config` directory. That latter layout is the Anno 117 detection path. Do not copy 117 metadata/schema examples into an 1800 mod.

The documentation's live analysis is implemented as an **offline xmltest child process**. It patches extracted XML and parses diagnostics; it does not run a game simulation when a file is saved. GUI diagnosis and Show Diff are useful for selection/patch failures, not proof of effects, synchronization, save compatibility or native C API behavior.

The 1800 XML schema association applies to `{assets*,*.include}.xml`, with the Red Hat XML extension supplying XSD support. This is partial completion and validation. It does not supersede the checked loader implementation or a vanilla audit. GUID completion deliberately excludes some categories, notably Audio and Test; missing completion does not prove a GUID is invalid.

## Dependencies used by analysis

For Anno 1800, `getAllDependencies()` combines `ModDependencies`, `Development.Dependencies` (falling back to old OptionalDependencies) and `LoadAfterIds`, removing duplicates. Navigation can see vanilla, the current mod, dependencies and previously opened XML patches.

For Show Diff and `fetchIssues()`, the inspected xmltest wrapper obtains prepatches specifically from the **intersection of ModDependencies and LoadAfterIds**. The current analysis page describes the Anno 117 `Dependencies.Require/LoadAfter` form; use the actual 1800 fields above. The wrapper does not add Development.Dependencies in these inspected diff/diagnostic functions, although the documentation says development dependencies are pre-applied. Additional caller handling still requires review before declaring that discrepancy closed.

## Build and deploy are file mutations

The deploy command constructs a ModBuilder with the configured mods output and extracted-data directory. The CLI entry creates an `out` directory and resolves each input metadata glob, using a per-mod `.vanilla` folder for its source cache. Both run the same builder. No build or deployment was executed during this documentation research.

Default output is `${annoMods}/${modName}`, where modName is `[Category.English] ModName.English`. `Development.DeployPath` overrides it; old `out` is a fallback. Relative output paths resolve under the source mod. Always inspect the resolved target and generated output before distributing a mod.

The builder does not begin by deleting all old output. Copied files overwrite their existing paths, while unrelated stale files can survive. Bundled subfolders are renamed to ModID; when that target exists the code removes it before renaming. Do not use an output folder containing unrelated work.

### Default pipeline

| Input | Inspected behavior |
| --- | --- |
| Config, include patches, Lua, Markdown, banners | Selected by explicit glob patterns and copied; this is not a universal copy-every-file build |
| `*.cf7` | Feedback converter |
| `*.rdp.xml` | Particle converter |
| glTF except propsonly prefix | Model converter, default 5 LODs, rdm/anim output paths; converter details require their own review |
| `*.cfg.yaml` | Skin generation converter |
| Diff/norm/height/metal/mask/rga/r_a/r_a+b PNG suffixes | Texture converter, default 3 LODs under maps |
| `icon*.png` | PNG copy plus icon texture conversion |
| CFG, IFO, PRP, FC, RDM, DDS, RDP, BNK | Copied from data/products/shared trees |
| `assets_.xml` at the main asset path | Copied as `assets.xml`; generated assets_.xml is removed, a timestamp comment is appended to force cache refresh |
| modinfo | Generated JSON, with build-only fields removed |

A custom converter list replaces the default list and then receives an assets conversion entry. Therefore it can omit normal Lua/static/modinfo processing. Review the final converter list, not only the source-tree structure.

### Metadata output

The converter removes Development and legacy bundle/src/out/converter fields. Missing localized Category, ModName and Description values are filled from English. It sets a missing English description to `file::README.md`; the inspected converter does **not** inline README content there. Its `_readMarkdownWithoutImages()` helper is not invoked by `run()`. Thus the deploy page's blanket statement that README text is inserted is not established by this implementation.

`base64.jpg`, when present, becomes a JPEG data URI in Image. Optional `content_en` writes the current English description to content_en.txt. The converter strips carriage returns from description strings and writes JSON with LF formatting; this tool's output behavior is separate from this workspace's required UTF-8/CRLF authoring policy.

### Textures

The DDS wrapper runs annotex with automatically detected format and requested LOD count. `_rga.png` expects `_norm.dds`, while `_r_a.png` and `_r_a+b.png` expect `_metal.dds`. PNG filenames are source conventions, not identical deployed filenames.

Outside `data/ui`, icon handling requests only one converted level and copies that LOD0 to the other named LOD files to avoid blurry icons. Inside `data/ui`, special icon handling is disabled. The inspected converter stores that flag outside its file loop, so encountering a vanilla UI path can also disable special handling for later files in that batch. Inspect actual outputs when mixing paths. This is a source observation, not a game-rendering test.

The wrapper checks whether expected output exists and parses annotex's reported output names. Existing stale files can satisfy an existence check; use isolated outputs when validating a conversion.

## Bundles: unresolved documentation shortcut

`Development.Bundle` is the code-visible bundle list. Relative entries beginning with a dot are recursively built from local metadata; other entries are downloaded and extracted. Download caches use ZIP filename and a sanitized URL-parent version. A reused filename/version can reuse the cached archive.

The Deploy documentation additionally promises automatic URL handling in ModDependencies. The inspected builder, metadata reader and metadata converter show no such conversion; a full src search found no separate implementation. **Q003 was answered on 2026-10-03:** Serp has not tested the shortcut and directs this documentation to use the code finding. The documented source-derived authoring pattern is an explicit normal ModID in ModDependencies plus its download URL in Development.Bundle. The shortcut remains an unsupported documentation claim at this inspected revision. This is an external build step; the integrated game loader is not thereby an internet downloader.

The recursive local bundle builder's return value is not propagated, and `_buildBundle()` can return early after logging without failing the top-level build. Review logs and required bundled content even when the outer build reports success.

## Offline checks and limitations

The general test wrapper enumerates `**/*-input.xml`, compares against corresponding `*-expectation.xml`, and normalizes line whitespace. The inspected current `test()` always chooses xmltest2.exe, while `diff()` and `fetchIssues()` choose xmltest.exe for Anno 1800. The `show()` function also chooses xmltest2.exe. Do not assume every command uses the same 1800 evaluator.

This knowledge base's actual 1800 checks invoke the installed xmltest.exe directly and inspect both logs and patched structure; see [offline validation](../reference/offline-validation.md). A clean XSD check, empty filtered diagnostic list or build success is insufficient to establish in-game correctness.

## Graphics authoring conventions

The legacy glTF import page recommends the newer [Blender Anno 1800 addon](https://github.com/anno-mods/Blender-Anno-1800). Its older naming-based importer modifies transforms, not arbitrary mesh geometry: `prop_`, `particle_`, `file_`, `fc_`, `hitbox`, `dummy_`, `FeedbackBlocker`, `ground` and `UnevenBlocker` have distinct consumers. Ground's decal extents and IFO BuildBlocker dimensions are different outputs. Some missing objects are marked `_removed`; others are retained. Deleting an object in Blender therefore does not universally delete its original configuration node.

The reskin page defines `.cfg.yaml` with a variant source, XPath changes/removals and separate IFO changes. It supports modification of CFG/IFO, with same-basename feedback copied/generated. Its examples' property names belong to graphics configurations, not assets.xml ModOps. See [graphics toolchain](../ui-and-resources/graphics-toolchain.md) and [binary formats](../ui-and-resources/binary-formats.md); detailed converter and native graphics audits remain required.
