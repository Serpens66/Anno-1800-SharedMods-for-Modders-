# Mod structure, metadata and loading

## The file overlay

An Anno 1800 mod contributes files under paths relative to the game's virtual data root. A mod folder is a package boundary; it is not a namespace that isolates identically named game files. Two mods contributing `data/scripts/init.lua` compete for that same path. Give custom Lua, models, textures, icons and audio an author-and-feature-specific directory, for example `data/serp/my_feature/`.

Use this layout for a new 1800 XML mod:

```text
my-feature-author/
  modinfo.json
  README.md
  data/
    config/export/main/asset/assets.xml
    config/gui/texts_english.xml
    author/my_feature/...
```

`assets.xml` contains a `ModOps` document, not a complete replacement of the extracted assets database. Its location identifies the original game file to patch. `templates.xml`, `properties.xml` and language XML have their own corresponding paths. Do not put an asset patch into a language file or copy 117's `data/base/config/export/assets.xml` path into an 1800 mod.

For ordinary custom resources, preserve the resource's game-relative path in every XML reference. Slashes inside game paths should follow existing working examples. Serp's Lua notes report that script filenames must be lowercase. Avoid depending on case-insensitive Windows filesystem lookup to establish what the game's resource lookup accepts.

Sources: [1800 file structure](https://jakobharder.github.io/anno-mod-loader/file-structure/), [guide structure](https://github.com/anno-mods/modding-guide/blob/main/getting-started/structure-of-a-mod.md), local `HowTo.xml`, lines 337-344; `Python Modding/info.txt`, lowercase-script note.

## Metadata

Always supply valid JSON metadata for a new mod. JSON examples in upstream documentation sometimes contain comments or omitted fields for illustration; comments are not valid strict JSON.

```json
{
  "Anno": 7,
  "Version": "1.0.0",
  "ModID": "my-feature-author",
  "ModDependencies": [],
  "LoadAfterIds": [],
  "DeprecateIds": [],
  "IncompatibleIds": []
}
```

Replace the example ID with a unique, stable identity. Changing a folder name is not the same as changing `ModID`. `Anno: 7` identifies Anno 1800 for tools; `Anno: 8` belongs to Anno 117. The current reference describes `Anno` as optional for 1800. Legacy manually installed 1800 mods can fall back to their folder name without metadata, but mod.io mods and mods discovered in subfolders need metadata according to the installation reference.

| Field | Meaning and limit |
| --- | --- |
| `Version` | Three numeric components are recommended. Use a major version change for a release that recommends a new game, a minor for additions and a patch for fixes. This convention does not itself prove savegame safety. |
| `ModDependencies` | Required mod IDs. Missing dependencies are reported; do not assume this field downloads or installs them. |
| `LoadAfterIds` | Ordering dependencies. Absence of the named mod does not itself generate a required-dependency warning. |
| `OptionalDependencies` | Optional integrations; inspect the tool/version that consumes this field. Current tooling moves development-only dependency information into `Development.Dependencies`. |
| `DeprecateIds` | IDs superseded by this mod. Do not add an unrelated ID merely to suppress a duplicate. |
| `IncompatibleIds` | Declared incompatibilities. A declaration is not a repair for conflicting resources or patches. |
| `Development` | Tool-specific settings such as `DeployPath`, `Bundle` and `Dependencies`. These are not Lua lifecycle hooks. |

The 1800 version parser compares numeric components, not decimal fractions: a metadata version `1.009` is not a decimal quantity. Existing workspace helpers use such historical spellings. Preserve their IDs and versioning when documenting or making a targeted change; do not independently renumber them.

Source: [Modinfo reference](https://jakobharder.github.io/anno-mod-loader/modinfo/), [pinned 1800 metadata/order implementation](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/mod_loading_order.cc). Display/localization metadata and the separately linked Modinfo specification must be checked before publishing a distributable mod.

## Loading order and nested helpers

There are normal and late phases. `LoadAfterIds: ["*"]` places a mod in the late phase. A normal-phase mod cannot load after a late-phase mod by naming it alone. A late compatibility patch must also use `*` if its prerequisite is late:

```json
{
  "Anno": 7,
  "Version": "1.0.0",
  "ModID": "postprocessing-author",
  "LoadAfterIds": ["*", "other-late-mod"]
}
```

Within a phase, explicit dependency ordering takes priority over historical alphabetical behavior. Cycles have undefined meaningful order; removing a cycle is part of fixing the integration. Folder prefixes such as `zzz` are not a substitute for dependencies.

`Condition="#mod-id"` means the mod is active. It does not mean its XML has already executed. Add the appropriate `LoadAfterIds` if your `Content` expression must see that mod's changes.

A nested mod has its own metadata and loading order, independent of the parent's order. Its activation follows its parent. A collection folder containing several independent mods is different: the folder is not itself a mod and has no activation identity.

Shared nested copies with the same `ModID` are deduplicated by version. The highest version is selected. Equal-version but different-content copies are unsafe: the reference only promises that one is chosen. Compare actual hashes and integrations, not just version strings. This is especially relevant to bundled Light/Medium/Ultra helpers in this workspace.

Source: [loading order](https://jakobharder.github.io/anno-mod-loader/loading-order/), [nested/shared mods](https://jakobharder.github.io/anno-mod-loader/file-structure/).

## Installation, activation and diagnostics

The current 1800 reference lists the user's `Anno 1800/mods` folder and the installation's `mods` folder. This workspace is a development collection, not automatically the folder the running game reads. Inspect the user's chosen installation and deployment configuration before copying a finished mod.

Manual mods can be disabled with a leading `-` on their folder or ZIP name. The reference says this is unavailable for mod.io folders and discourages changing it while the game runs. Alternatively, `activation.json` in a manual mods folder contains:

```json
{
  "disabledIds": ["my-feature-author"]
}
```

This uses metadata IDs, with folder-name fallback for legacy mods. Anno 117's `active-profile.txt` is not an 1800 profile mechanism.

The reference supports ZIP-contained 1800 mods but warns about island files in ZIPs. For map/island work, use an unpacked installation when following the documented procedure. A game start creates a new loader log under the user's `Anno 1800/log/mod-loader.log`. Examine loading order, missing IDs, unmatched paths and parse errors before diagnosing game logic.

Source: [installation](https://jakobharder.github.io/anno-mod-loader/install/), [activation](https://jakobharder.github.io/anno-mod-loader/profiles/), [debugging](https://jakobharder.github.io/anno-mod-loader/debug/).

## Reloading and historical external-loader code

Serp's notebook records reload limitations: graphics do not refresh reliably through `mods.reload()`, changed keybinding commands can retain the old command, target matches can require a restart, and QuestPool cooldowns/limits can reset. Advanced Lua helper comments contain additional reload concerns. A reload is not equivalent to closing and restarting the game, or loading a newly created save.

The pinned repository contains older external-loader integration, including Python forwarding and a file watcher. Its `external-file-loader/src/mod_manager.cc` still recognizes `start_script.py`, scans only its historical folder arrangement and treats `.xml` as patchable. These remnants must not override current integrated-loader documentation about nested mods, binary patches or Lua. The reusable `xml-operations` implementation is the inspected source for ModOp semantics; provenance is recorded per component.

Do not install historical replacement Python DLLs as a step in a new integrated-loader workflow. Python remains useful outside the game for extraction, XML/XPath checks, generation and analysis.


For composition rules beyond metadata, see [Mod compatibility](mod-compatibility.md): prepare missing containers, retain foreign list entries and anchors, and distinguish declared ordering from compatible behavior.
