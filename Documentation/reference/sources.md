# Sources and provenance

Research date: **2026-10-03**, Europe/Berlin.

## Primary upstream sources

| Source | Pinned revision / role |
| --- | --- |
| [Anno 1800 loader branch](https://github.com/jakobharder/anno-mod-loader/tree/stable/anno1800) | Branch name is `stable/anno1800`, not a directory within branch `stable`. Commit `8326b7c5a7648787c52f1252cd6e8ae60e593d1c`, dated 2025-07-07. |
| [Modloader Reference](https://jakobharder.github.io/anno-mod-loader/) | Current multi-game reference, inspected source commit `5a4464dc2da222844f439ac0463174d2da97b087`, dated2025-11-19. Source Markdown under `docs`; `a1800`, `a117`, `all` macros and tab labels distinguish games. |
| [Modding Guide](https://github.com/anno-mods/modding-guide) | Commit `9afc5adb6271e02282532931cf4291b9a5059268`, dated 2026-08-30. Read Anno 1800 material separately from `anno-117` and `Scripting/Anno_117_Lua_Tutorial.md`. |
| [XPath cheat sheet](https://devhints.io/xpath) | Fully read; XPath2 functions and malformed examples excluded, see discrepancy register. Supporting reference, not authoritative for loader extensions. |
| [FileDBReader](https://github.com/anno-mods/FileDBReader) | `349145a1c1f188d09beb61b675311ff52586e15f`, 2025-09-04. README and RDP definition read; wiki and remaining format/code audits pending. |
| [Modinfo](https://github.com/anno-mods/Modinfo) | `880b5a994dc3de1d65d1c714e6704b0d06192d3f`, 2024-02-20. README, complete format specification and relevant C# example models read. Models are historical/partial. |
| [GuidRanges](https://github.com/anno-mods/GuidRanges) | `093505292129985db9cb818468c15cee329dc354`, 2026-09-30. README, complete 1800 GUID and enum registries read; 117 allocations excluded. |
| [Shared resources](https://github.com/anno-mods/shared-resources) | `554da1cf86b07004a23576443affa5c022c47fd2`, 2026-10-02. Root README read; individual components and linked repositories still require review. |
| [FileDBReader wiki](https://github.com/anno-mods/FileDBReader/wiki) | `c1822d3bc661aea78da1b771e4d3a1a3f0565eed`, 2024-03-13. All nine accessible Markdown pages read. Windows-invalid colon filenames extracted through git show; temporary path-map.json preserves the original names. |
| [rdm4](https://github.com/lukts30/rdm4) | `a1d5970021b2332babb36edecfc80cc7e3ad2503`, 2026-08-30. README and CLI definition read; relevant converter branches inspected; remaining implementations, issues and linked videos tracked separately. |
| [Original Blender addon](https://github.com/xormenter/Blender-Anno-.cfg-Import-Addon) | `358cde764c8999bf59ef55a63af7f99e32f529fe`, 2025-11-15. Complete README read; discontinued and points to the separate 1800 successor. |
| [Blender Anno 1800 successor](https://github.com/anno-mods/Blender-Anno-1800) | `c790c97572edfa6b2ea5fcb229feaff0fc753185`, 2025-09-03. Complete README read; import/export implementation audits pending. Separate from Anno 117 addon. |
| [AddCustomMusic](https://github.com/anno-mods/AddCustomMusic) | `d4b5b3d66c22b7ba3c65f8c86d1f296841da378d`, 2026-09-06. All 11 Markdown/XML/Lua files read; native audio/session audit and linked video pending. |
| [iModYourAnno wiki](https://github.com/anno-mods/iModYourAnno/wiki) | `7c30b533f475d35cab35654888a3e076e8950378`, 2023-05-03. All three pages read; historical preprocessing/application implementation pending. |
| [Anno Modding Tools](https://github.com/anno-mods/vscode-anno) | `19cda8edc73d65a622c9c5c588953a0170c337c6`, 2026-09-24; package version 2.3.1. All 12 documentation Markdown pages and selected build/metadata/XML-test implementations read; remaining converter/linked-example review pending. |
| [Schwubbe modding blog](https://schwubbe.de/modding_blog.php) | Retrieved 2026-10-03; historical external loader and superseded claims separated. Entire page text/code read, linked files/forums remain separate tasks. |

Temporary research checkouts are located under `C:/Users/Serpens66/AppData/Local/Temp/anno1800-documentation-research-20261003/`. They are disposable caches, not the permanent documentation. Published claims must link to upstream sources or the original workspace sources, not depend on that temporary directory surviving.

## Local sources

| Source | Treatment |
| --- | --- |
| `D:/CDesktopLink/Unterlagen/Mods/Anno 1800/HowTo.xml` | All2862 lines read, including comments/corrections; key outcomes in personal-test-evidence and XML/UI chapters. Remaining gameplay feature audits are tracked separately. Notebook, not a deployable patch. |
| `D:/CDesktopLink/Unterlagen/Mods/Anno 1800/Python Modding/info.txt` | All867 lines read; Lua/runtime/MP outcomes recorded, historical Python separated. Q002 clarified by Serp; uncertainty retained. |
| Workspace mods | Includes own mods, shared components, duplicated bundles, WIP/retired code, community bugfixes, sound resources and third-party modpack components. |
| `D:/CDesktopLink/Unterlagen/Mods/Anno 1800/Anno1800 RDA unpacked/dataAlle/` | Preferred extracted vanilla source. Main asset/config files are under `data/config/export/main/asset/`; `export.xml` at the extraction root is the decoded infotip export. |
| `D:/CDesktopLink/Unterlagen/Mods/DST/_scripts/` | Historical backup only; not used to establish current Anno 1800 behavior. |

SHA-256 hashes and source paths are in the machine-readable inventory and vanilla-contract records. The available extraction is treated as the user's preferred data set; its exact originating game build has not been independently established.

## Serp repository links (verified 2026-10-25)

Keep local/evidence links and add a direct GitHub source link when the referenced content belongs to a verified Anno repository. Prefer the inspected published commit and exact file/line over a repository homepage. Resolve junctions and bundled copies to the actual source; do not guess from a repeated basename. Local reports, generated audit data, private notes/saves and extracted Vanilla are not automatically published repository content.

| Workspace folder | GitHub source | Verified published commit |
| --- | --- | --- |
| Anno-1800-Mods | [Repository](https://github.com/Serpens66/Anno-1800-Mods) | [Inspected tree](https://github.com/Serpens66/Anno-1800-Mods/tree/88821b04ee972424667178d35a5080a753a853d0) |
| SharedMods | [Repository](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-) | [Inspected tree](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/tree/3aece64f299365309aaf1f7a57f28e2f6900f106) |
| Anno1404SoundsTo1800 | [Repository](https://github.com/Serpens66/Anno1404SoundsTo1800) | [Inspected tree](https://github.com/Serpens66/Anno1404SoundsTo1800/tree/9d1d181b9d64a49013c7aa20a82af5a971d1d07c) |

Explicit workspace paths in the evidence tables now have accompanying GitHub links. [Link validation](validation/github-links/results.json) records repository trees, published branch equality, source-content checks and the scope of the mapping. This is link/provenance maintenance, not a new code or gameplay validation. The subsequent Campaign 1.022 fixes and Story 1.032 comments are local and uncommitted; these GitHub commits describe the earlier inspected source, with [current local hashes and checks (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/dlc-gates-validation.json) recorded separately.

## Key implementation entry points

Pinned loader commit links:

- [XML selection, conditions, operations and recursive merge](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/xml_operations.cc)
- [Loading order, duplicates and version comparison](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/mod_loading_order.cc)
- [File loading, patch dispatch and caches](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/external-file-loader/src/mod_manager.cc)
- [Binary FileDB serialization](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/xml_filedb_reader.cc)
- [Feedback conversion](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/xml_fc_reader.cc)

Published examples may contain mistakes. XML validity, path context and the selected game version must be checked even when an example has a 1800 label.

## Savegame source addition (2026-10-25)

- Local `Anno1800SavegameVisualizerv5.0/tools`: RDAConsole 1.1.0, FileDBReader 3.0.3/.NET 6, `unpack_savegame.py`, `a7s_hex.xml` and `a7s_all_serp.xml`. Exact binary/format/script hashes, named private-save hashes and selected anonymized observations are in [savegame-audit.json (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/savegame-audit.json). Account identifiers, complete saves/XML and signed redirect URLs are excluded.
- [Pinned V2 parser](https://github.com/anno-mods/FileDBReader/blob/349145a1c1f188d09beb61b675311ff52586e15f/FileDBSerializer/FileDBSerializer/IO/Parsing/Versions/BBStructureParser_V2.cs), [document parser](https://github.com/anno-mods/FileDBReader/blob/349145a1c1f188d09beb61b675311ff52586e15f/FileDBSerializer/FileDBSerializer/IO/Parsing/BBDocumentParser.cs), [version routing](https://github.com/anno-mods/FileDBReader/blob/349145a1c1f188d09beb61b675311ff52586e15f/FileDBSerializer/FileDBSerializer/IO/DependencyVersions.cs) and [reserved dictionary names](https://github.com/anno-mods/FileDBReader/blob/349145a1c1f188d09beb61b675311ff52586e15f/FileDBSerializer/FileDBSerializer/Document/TagSection.cs) establish the inspected structural reader contract. The local executable is fingerprinted separately; binary equivalence to the checkout is not claimed.
- [Campaign mod.io page](https://mod.io/g/anno-1800/m/campaign-in-coop-serp): visible release history, 1.021 dated 2025-10-18, release file 6857871. The downloaded package hash and normalized differences from workspace are retained. The [historical case evidence (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/savegame-audit.json) preserves the release comparison; the [active review (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/README.md) now contains only unresolved points.
- [Reading savegames](../gameplay/savegames.md) documents archive/outer compression/FileDB stages, field-specific decoding and peer/version uncertainty. These are offline observations; prior gameplay/Coop qualifications remain unchanged.

## External links to continue

The source graph includes FileDBReader and its format definitions, Modinfo, GuidRanges, shared-resources, Anno Modding Tools, iModYourAnno tweaking documentation, Pnski's Lua command documentation, graphics conversion tools, the map editor, custom-music documentation, the inheritance forum and Discord-linked tests/tutorials. Their individual status must be recorded before coverage is considered complete. Login-only Discord material, videos without a usable transcript and unavailable resources must be identified as such, not silently omitted.


## Mod-composition source addition (2026-10-25)

[The compatibility chapter](../foundations/mod-compatibility.md) links the merchant preparation/incremental-add examples, scoped Story predicates, SharedMods policy and LuaLight namespacing to their original published sources. Commit 9858f32602891e2b562a73a1b6c8b5890bfd1f68 in Anno-1800-Mods and 79f10e0cc8e53d909c44dd831689ddc8d4632c99 in SharedMods matched their remote branch refs before editing. New Campaign 1.023/chapter edits are local and are not represented as published by those baseline links.

[Selected source excerpts and hashes](validation/mod-compatibility/sources.json) distinguish Serp's own statements from the community compatibility guide and mixed-authorship Pnski/Serp log helper. The pinned 1800 loader is the implementation evidence for append/recursive merge; the current standalone GU17.1 executable is separately fingerprinted. Old add/replace advice and the invalid upstream duplicate-removal XPath are not promoted to working recipes. [Actual offline results](validation/mod-compatibility/results.json) and [reproducer](../tools/validate_mod_compatibility.py) retain their game/MP limits.
