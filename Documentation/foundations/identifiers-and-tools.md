# Identifiers, registry coordination and binary-data tools

## Asset GUIDs and independent namespaces

An asset's `Values/Standard/GUID` identifies that asset. References, localization GUIDs, pool entries, unlocks and text embeds must resolve to the appropriate asset/text namespace; an arbitrary integer is not sufficient. An object's runtime OID, an area ID, a session index and a session GUID are different values. See [ObjectFinder](../lua/objectfinder-and-coopcount.md) for concrete signatures where confusing them silently changes scope.

The [Anno 1800 GUID registry](https://github.com/anno-mods/GuidRanges/blob/093505292129985db9cb818468c15cee329dc354/1800/guids.md) records the safe mod range as **1337471142–2147483647**. It coordinates reservations, not runtime allocation. Within that range, another modder may already own an interval. For this workspace, **Serp's Mods: 1500000000–1500010000** is the recorded reservation. Existing shared GUIDs inside it are already used; never assume an unused-looking number is free without searching all workspace mods and dependencies. The private-use interval is **2001000000–2001009999**; it is intended for unpublished personal mods, not independently published mods that may collide.

Some registered historical ranges are below the stated safe lower bound. Their presence in the registry does not make every lower number generally available. Preserve existing allocations; do not copy a tutorial's example GUID or take another author's interval. Keep the signed 32-bit upper bound explicit when writing asset IDs. Runtime object IDs have a different representation and can exceed it.

For a new public asset, record its purpose and allocation next to the mod's source, search the extracted vanilla and all active mods, reserve a suitable interval through the registry's process when needed, and validate every reference. A `BaseAssetGUID` clone needs a new Standard GUID; matching the source GUID replaces/duplicates identity rather than creating a separate asset. The actual inheritance contract is explained in [Inheritance](inheritance.md).

## Enum and internal-resource reservations

The [Anno 1800 enum registry](https://github.com/anno-mods/GuidRanges/blob/093505292129985db9cb818468c15cee329dc354/1800/enums.md) coordinates limited pre-existing enum slots and other scarce identifiers. It does not prove that arbitrary new enum names can be introduced into the executable. The current snapshot includes FreeAreaType, SessionType, ItemAllocation, Participant, SocketExclusive, Unique, difficulty categories, key bindings, internal model IDs and special popup constraints.

Relevant Serp reservations include `ParticipantMod10` for the Nature helper, `ParticipantMod11` for the Trader PirateMode helper, `ItemAllocationMod2` for sabotage and `UniqueMod4` for sabotage. Actual mods must also be checked: a registry reservation alone does not explain participant index, template compatibility, spawning or UI behavior. Do not confuse `ParticipantMod10` with numeric human participant ID 10 or with the runtime peer index.

The registry notes that `ModuleParentTypeModX` had failed tests, that festivals have no general Mod enum slots, and that difficulty categories likewise require reuse of existing entries. Its festival workaround rewires specific vanilla reward types; do not apply those patches without auditing the complete reward/festival chain. The documented PC popup reuse candidate `ResetConsoleOptionsConfirmation` is not a universal guarantee for all platforms, versions or other mods.

Internal graphics IDs are another finite namespace; the registry includes collisions and uncertain assignments. A GUID reservation does not reserve these IDs. Avoid taking an apparently empty slot without checking the current registry, vanilla assets and installed mods. Key bindings likewise require coordination; reusing a registered key/name can intercept another mod's action even when asset GUIDs differ.

The repository has separate Anno 117 and Anno 1800 directories. Use the **1800** registry only. Record the commit/date used because reservations continue to change.

## FileDBReader conversion pipeline

[FileDBReader](https://github.com/anno-mods/FileDBReader/tree/349145a1c1f188d09beb61b675311ff52586e15f) converts serialized/compressed game data to editable representations. Its README distinguishes `decompress`, `compress`, `interpret`, `toHex`, `check_fileversion`, `fctohex` and `hextofc`. An interpreter XML specifies the structure of a particular binary format. Decompression alone does not turn every format into human-readable game XML; interpreting and reconstructing bytes are separate steps.

The tool documents compression versions 1 (older files, up to GU12), 2 and 3 (newer or additional files), with automatic detection on decompression. Use `check_fileversion` and preserve the correct target format when compressing. Do not infer a file's version solely from its extension or from the tool repository's most recent commit.

The optional `-i` interpreter can combine conversion stages. A common workflow is binary → decompressed/interpreted XML → edit → reverse conversion/compression. Choose the matching **1800** format definition; the latest repository also contains 117 definitions. The README explicitly treats supplied definitions as incomplete in places. A converted file that parses is not proof that every field has been understood.

Feedback data can contain binary CDATA whose stored size needs repair. The loader's [FC patch chapter](../ui-and-resources/cfg-and-fc.md) describes the source-verified handling. Do not edit opaque bytes as if they were normal XML text or apply XML formatting tools indiscriminately to a binary payload. Preserve an original file and verify conversion before replacing a game resource.

FileDBReader's .NET library targets .NET 6 or later in the reviewed README. Its command-line help and wiki are separate documentation sources; the README alone does not establish all interpreter grammar or library APIs. Those remaining pages are tracked in the coverage register.

## Shared resources and development-tool dependencies

[Shared Mod Resources](https://github.com/anno-mods/shared-resources/tree/554da1cf86b07004a23576443affa5c022c47fd2) asks consumers to include shared resources unchanged. Its root README links pools/definitions, construction-menu helpers, hotel compatibility, one-step influence, other-residence influence text and merged UI tabs. A bundled copy should retain its ModID/version; modifying it under the same identity can affect other consumers through highest-version selection.

The manual dependency example uses `ModDependencies` with `"shared-pools-and-definitions"` and `LoadAfterIds` with that same ModID. Presence and ordering are separate concerns. The automatic VS Code Build and Deploy example instead puts a release ZIP URL in `ModDependencies`: **that URL is a development-tool download instruction**, not evidence that the game loader downloads arbitrary dependencies. Check the built/deployed metadata and included mod layout before launch.

The README's versioning policy increases major for new shared features/mods, minor for additions and patch for corrections; it is an upstream packaging policy, not an API-compatibility guarantee. Read each helper's own documentation and implementation. Linked external collections (Qurila, Taludas, lion053, Jakob, Serp and others) are additional sources, not automatically reviewed by reading this index.

## Modinfo specification and consumer differences

The [Modinfo specification](https://github.com/anno-mods/Modinfo/blob/880b5a994dc3de1d65d1c714e6704b0d06192d3f/modinfo-format.md) covers identity/version, dependency/order/conflict fields, localized display data, descriptions, known issues, DLC declarations, creator/contact, mod.io resource IDs and banners. See [Structure and loading](structure-and-loading.md) for implementation-backed loader behavior.

An English display string is the specification's fallback. ModID, ModName and Category use valid folder characters. Description rendering supports escaped newlines and documented Markdown/file references in consumers that implement them; the integrated loader itself is not a full mod-manager renderer. Deprecated base64 `Image` is replaced by adjacent `banner.jpg`/`banner.png` for supporting managers. `DLCDependencies` distinguishes `required`, `partly` and `atLeastOneRequired`; its DLC name list is dated and is not a complete current ownership API.

The C# example classes in that repository are **older partial models**, not a complete authoritative schema: `Modinfo.cs` uses `CreatorName` while the specification documents `Creator`, and omits newer loading/deprecation fields. They should not override the actual 1800 loader's parsing. The specification's alphabetical loading explanation is also historical; the inspected loader source and explicit dependency order take precedence. These differences are attributable to version/consumer scope, not an unresolved game test.
