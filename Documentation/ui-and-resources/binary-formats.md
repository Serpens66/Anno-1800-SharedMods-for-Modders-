# Binary formats, interpreters and island containers

## Evidence and version

This chapter explains the reviewed FileDBReader format/writing wiki and library entry points. It does not establish map-generation, session or terrain gameplay behavior. The wiki revision is `c1822d3bc661aea78da1b771e4d3a1a3f0565eed` (2024-03-13); the code/format repository is `349145a1c1f188d09beb61b675311ff52586e15f` (2025-09-04). A wiki example can use an older API name. See [identifiers and tools](../foundations/identifiers-and-tools.md) for conversion stages and [FC patches](cfg-and-fc.md) for loader-specific conversion.

## FileDB tree representation

The [compression 2/3 specification](https://github.com/anno-mods/FileDBReader/wiki/Anno-Fileformats:-compression-version-2-&-3) distinguishes structural **Tags** from data-bearing **Attribs**. These are binary-document node classes; an Attrib is not necessarily an XML attribute such as `Type="merge"`. A document can contain multiple roots. Node names are represented by IDs and stored in dictionaries at the end.

Version 2 layout: content section, tag dictionary, attribute dictionary, followed by four-byte offsets to those two dictionaries and eight magic bytes. Relative footer offsets are −16 for the tag offset, −12 for the attribute offset and −8 for magic. Magic is little-endian Int32 pair `(8,-2)`: `08 00 00 00 FE FF FF FF`.

Attribute nodes contain Int32 byte size, Int32 name ID and payload, padded to eight-byte blocks. Padding is excluded from the attribute's declared payload byte size. Tags contain Int32 byte size (zero in the inspected V2/V3 reader contract), Int32 ID, child nodes and an eight-zero-byte node terminator. An extra terminator ends the content section. The dictionary stores an Int32 count, UInt16 IDs, zero-terminated names (ASCII in the inspected saves) and eight-byte alignment padding. The inspected reader obtains name characters through BinaryReader.ReadChar. Consequently the dictionaries have a 16-bit ID restriction despite wider IDs in the content nodes. Reserved tag ID 1 and attribute ID 32768 both mean None without a dictionary entry. These IDs belong to the file dictionary, not asset GUIDs. The [savegame audit (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/savegame-audit.json) records the exact parser/TagSection source hashes and the selected actual-save cross-checks.

Version 3 retains that layout with magic `(8,-3)` (`08 00 00 00 FD FF FF FF`) and an additional footer: eight unknown zero bytes at −32 and eight-byte total node count at −24, before the dictionary offsets. A valid edit must update sizes/counts/offsets consistently; rely on the appropriate serializer rather than manually changing isolated byte spans.

The wiki links [RDAExplorer's older file.db specification](https://github.com/lysannschlegel/RDAExplorer/wiki/file.db-format) for version 1. That linked specification remains a separate research source; the preceding version 2/3 description does not substitute for reading it.

## Interpreter grammar

For `.a7s` archives, use the separate [read-only savegame workflow](../gameplay/savegames.md): RDA extraction, outer zlib decompression and FileDB interpretation are distinct stages. It documents the installed tools, a minimal structural reader and a real interpreter defect where guessed string types generated invalid XML character references. A readable/recovered XML view is not a verified write-back format.

The [interpreter-writing page](https://github.com/anno-mods/FileDBReader/wiki/FileDBReader:-Writing-Interpreters) describes a root `Converts`, optional `Default`, an `InternalCompression` list and a nested `Converts` list of `Convert` rules. Rules select XML nodes through `Path`; they assign primitive `Type`, optional string `Encoding`, `Structure` and optional enum mappings. Structure is `Default`, `List` or `Cdata`. `Default` can also carry type/encoding/structure.

Each enum `Entry` maps a unique numeric `Value` to a unique `Name`; duplicate names or values make reverse conversion ambiguous. A string's encoding is a format contract, not a choice based on whether it currently contains only ASCII. Primitive type names follow the tool's .NET conversions.

`InternalCompression/Element` names a nested file-data path and its `CompressionVersion`. A neighboring `ByteCount`, when present in the documented `None/ByteCount,Data` structure, is recalculated. `ReplaceTagNames/Entry` maps otherwise unsuitable names to XML-friendly names and back; original and replacement names must each be unique.

The published sample incorrectly opens a second `<Element>` where `</Element>` is required. Correct the closing tag before parsing; this is an XML editorial defect, not a second nested-compression rule. Do not copy the malformed sample as a working interpreter.

The reviewed `FileFormats/tmc.xml` sets Int32 default, `FileName` as String, `PositionsXZ` as a Single list, `RotationsY` and `Coverages` as Byte lists, `UsedMaterialBits` as Int32, and `Indices`/`Vertices` as Int16 lists. Its comment says CTT despite its filename; use the actual definition and relevant original file. `ctt.xml` converts `Downsampled/map` to a UInt16 list, `Data/map` to a Byte list and `ScaleFactor` to Single. An interpreter's decoded values alone do not explain all geometric scales or buffer packing.

## Island and map containers

The [island format page](https://github.com/anno-mods/FileDBReader/wiki/Anno-Fileformats:-Island-Files) identifies these related files:

| File | Documented contents | Consequence |
| --- | --- | --- |
| `.a7m` | RDA v2.2 archive containing `gamedata.data` and `rd3d.data`, both FileDB-compressed | Archive extraction and FileDB conversion are separate operations. |
| `gamedata.data` | Logic and interaction data | Requires its appropriate Gamedata interpreter; changing render props does not automatically change gameplay placement. |
| `rd3d.data` | General chunk data and individual terrain-prop locations | Has its own RD3D interpreter. |
| `.tmc` | FileDB-compressed island mesh chunks containing vertex/index buffers | Every chunk must preserve its binary representation and references. |
| `.a7minfo` | FileDB-compressed metadata | Not interchangeable with plain editor XML. |
| `.a7me` | XML editor data | Separate from the runtime archive and meshes. |
| `.ctt` | Multiple-resolution detail height maps | Additional outer compression and runtime reconstruction are involved. |

Map templates similarly contain an RDA v2.2 archive with `gamedata.data`, plain `.a7te` XML and FileDB-compressed `.a7tinfo`. These are source-format statements, not a complete new-session recipe.

CTT begins with eight magic bytes `5F 42 54 54 4D B8 05 00`, followed by a documented zlib-compressed block and then a FileDB document. The wiki describes a downsampled image plus quantized mip levels, each with ScaleFactor and QuantBits. It points to native `data/shaders/fx/terrain_compress.fx` for runtime dequantization and tangent-space normal-map generation. That shader's feature audit is still required before specifying an actual terrain-editing algorithm. Do not equate the decoded quantized bytes with a ready-to-use height image or assume Blender's coarse-heightmap preview can export it.

## TMC patch tutorial: complete code review and limits

[Edit Island Meshes](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/guides/Edit-Island-Meshes.md) has a short narrative, a decompression/patch-generation batch block and a 3061-line recompression block. The latter consists of the same four commands repeated for all **576 coordinates, 0–23 × 0–23**, without content-dependent variation. That repeated structure was compared across the entire block; it is not 576 distinct mesh algorithms.

The generator replaces the five `flowers_moderate_01..05.prp` paths under `//GroundObjects/None/FileName`: variants 1–4 map to jungle 1–4; moderate 5 maps to jungle 1. This is reference replacement inside a decoded TMC, not remeshing. The code includes a stray `[text() = 'hello']` batch line. Its recursive XML loop also needs care on a second invocation because already generated patch/output XML may be included.

The recompression block invokes old-form xmltest, renames `patched.xml`, compresses with version 2 and then overwrites the original `.tmc` with `MOVE /Y`. It does not check failures before consuming the output. Missing source tiles are expected by the author, but a failed command followed by stale `patched.xml` or `.tmc` can corrupt the next result. Therefore the original batch file is **not an approved general-purpose automation**. Work on a dedicated copy, enumerate existing input tiles, write separate unique outputs, check command success and content, then deliberately replace the intended copied resource. This documentation task did not run the batch or alter islands.

The installed xmltest CLI used in this task has explicit `-c patch`, mod root and output arguments; see [offline validation](../reference/offline-validation.md). Do not assume a tutorial's old command-line form matches the installed binary. Compression version 2 in the sample is a sample-specific choice, not proof that all current island chunks should be rewritten as V2.

## .NET BBDom entry points and historical wiki drift

[Basics](https://github.com/anno-mods/FileDBReader/wiki/AnnoMods.BBDom:-Basics), [Lookups](https://github.com/anno-mods/FileDBReader/wiki/AnnoMods.BBDom:-LookUps) and [Serialization](https://github.com/anno-mods/FileDBReader/wiki/AnnoMods.BBDom:-Serialization) cover direct DOM access and object serialization. `BBDocument.LoadStream` reads a stream; `WriteToStream(stream, version)` writes one. The inspected `BBDocument.cs` default write version is **V3**. In contrast, constructing the inspected `BBSerializerOptions` defaults its `Version` to **V1**. Set the intended version explicitly rather than conflating the two defaults.

`CreateTag`, `CreateAttrib`, `AddChildren` and `AddRoot` build the tree. Direct DOM lookup paths are plain slash-separated node names starting at the receiver, with **no leading slash**, wildcard, regex or XPath predicates. `SelectNodes` returns matching nodes; `SelectSingleNode` returns the first; overloads can take a node-filter delegate. These lookups are distinct from loader XPath and interpreter XPath.

The inspected `AnnoMods.BBDom.ObjectSerializer.BBConvert` exposes `SerializeObject` (new or supplied stream), `SerializeObjectToDocument`, `DeserializeObject` and `DeserializeObjectFromDocument`, using `BBSerializerOptions` and generic `class,new()` constraints. The older serialization page alternates `FileDBConvert`, `FileDBSerializerOptions` and older version-enum names; use the pinned library signatures when compiling new tooling.

The wiki describes public get/set properties rather than fields, arrays as its supported enumerable shape, `FlatArray` for repeated unwrapped entries, nullable-value handling, and encoding-aware string wrappers. Options in inspected code include `DefaultEncoding=UTF8`, `IgnoreMissingProperties=false`, `SkipDefaultedValues=false`, and three null-skipping defaults true (`SkipSimpleNullValues`, `SkipListNullValues`, `SkipReferenceArrayNullValues`). Missing-property suppression can conceal schema mismatches; do not use it as proof of a complete round trip.

The wiki's `OnSerialized` statement describes a callback after deserialization. The complete inspected `BBDocumentDeserializer.GetObjectStructureFromBBDocument` constructs the object, assigns properties and returns it without such a callback; a search of the pinned library finds no `OnSerialized`/`OnDeserialized` implementation. Consequently this callback is **not an established capability of the pinned code**, regardless of the older wiki statement. No callback example is supplied as validated code.

The complete lookup implementation also limits the wiki's filter claim: `SelectSingleNode` applies its delegate at the final node, but traverses only the first matching intermediate tag and does not backtrack into later matching branches. `SelectNodes` tests the condition while descending the first path segment, drops it in recursive calls, and does not apply it in its final-node branch. Thus a delegate passed to `SelectNodes` is **not a reliable final-result filter** in this pinned implementation. Filter the returned enumerable explicitly when writing tooling. A name-only lookup and a condition-aware single lookup are different contracts.

The available wiki is not a compiled test suite. Any C# tool based on it must validate its exact library version, actual file fixture, encoding and round-trip output independently. These source-level corrections have not involved running third-party library code.

## Remaining source boundaries

The nine accessible wiki Markdown pages were read. Windows-invalid colon filenames were recovered through `git show`; the temporary cache mapping retains original page names. Linked RDA format documentation, .NET primitive/encoding definitions, the Anno 2205 terrain presentation and native terrain shaders remain separate sources. Anno 2205 renderer material is context, not proof of Anno 1800's exact shader contract. Complete island/session gameplay instructions remain pending their larger audits.
