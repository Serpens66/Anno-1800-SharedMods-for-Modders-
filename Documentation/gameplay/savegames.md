# Reading Anno 1800 savegames

## Scope and evidence

This is a **read-only Anno 1800 PC** workflow, checked on 2026-10-25. It explains how to inspect an existing save without launching the game or repacking it. The [historical Campaign evidence record (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/evidence/savegame-audit.json) distinguishes observed data, source contracts and inferences. It does not certify a repaired save or multiplayer execution. The [active review (local workspace only)](../../../CodeReview/Campaign-in-Coop-Serp/README.md) now lists only unresolved points; retroactive save repairs are outside the requested scope.

Follow the [feature-specific vanilla audit](../foundations/vanilla-research.md) before interpreting a gameplay field or proposing a repair. An archive converter makes bytes readable; it does not establish their gameplay meaning.

## Tools and conversion stages

The installed tools used here are under:

```text
D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Anno1800SavegameVisualizerv5.0\tools
  RDAConsole.exe                         version 1.1.0
  FileDBReader\FileDBReader.exe          version 3.0.3
  FileDBReader\FileFormats\a7s_hex.xml
  FileDBReader\FileFormats\a7s_all_serp.xml
  FileDBReader\unpack_savegame.py
```

The portable interpreter is `D:\CDesktopLink\Portable\Python\WinPy64\python\python.exe`; the installed FileDBReader declares .NET 6.0. Binary and interpreter-file hashes are recorded in the evidence JSON. Inspected library source is separately pinned there: a source checkout is not proof that a local binary was built from that exact revision.

| Stage | Input | Result |
| --- | --- | --- |
| Archive extraction | Original `.a7s` save | `header.a7s`, `gamesetup.a7s`, `meta.a7s`, `data.a7s` |
| Outer decompression | Each extracted component | zlib-decompressed FileDB bytes, conventionally named `.bin` |
| Structural decoding | FileDB bytes | Named XML elements with raw hexadecimal data |
| Selected interpretation | Raw field bytes plus a verified interpreter rule | A string, integer, enum or other established value |

Do not pass the original archive directly to `zlib.decompress` or treat an extracted component as already decoded XML. The inspected local unpacking script uses the same archive/zlib/FileDB separation. In the twelve components checked here, the final four bytes of each compressed component equal the decompressed byte length; zlib also accepts the trailing data. This observation is not a general write-back specification.

### Extract into a fresh analysis directory

This PowerShell example asks for the source path, creates a unique temporary output directory, and never deletes an existing directory. Existing sandbox/approval rules still apply; do not change the input file to overcome an execution restriction.

```powershell
$saveFile = Read-Host 'Absolute path of the original .a7s save'
if (-not [System.IO.Path]::IsPathRooted($saveFile) -or
    -not (Test-Path -LiteralPath $saveFile -PathType Leaf)) {
    throw 'Supply an existing absolute savegame path.'
}
$toolDir = 'D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Anno1800SavegameVisualizerv5.0\tools'
$analysisDir = Join-Path ([System.IO.Path]::GetTempPath()) ('anno-save-read-' + [guid]::NewGuid())
$unpackedDir = Join-Path $analysisDir 'components'
New-Item -ItemType Directory -Path $unpackedDir | Out-Null
$sourceHash = (Get-FileHash -LiteralPath $saveFile -Algorithm SHA256).Hash
& (Join-Path $toolDir 'RDAConsole.exe') extract -f $saveFile -o $unpackedDir -y -n
if ($LASTEXITCODE -ne 0) { throw 'Archive extraction failed.' }
foreach ($component in @('header', 'gamesetup', 'meta', 'data')) {
    $componentPath = Join-Path $unpackedDir ($component + '.a7s')
    if (-not (Test-Path -LiteralPath $componentPath -PathType Leaf) -or
        (Get-Item -LiteralPath $componentPath).Length -eq 0) {
        throw "Missing or empty component: $component"
    }
}
if ((Get-FileHash -LiteralPath $saveFile -Algorithm SHA256).Hash -ne $sourceHash) {
    throw 'The original save changed during inspection.'
}
```

RDAConsole's `-y` operates on the newly created analysis output. It is not permission to overwrite an original save. Avoid running the complete `unpack_savegame.py` driver for this task: its unpack route deletes its selected output folder, and the same script also implements packing, multiplayer conversion and scenario conversion.

### Decompress the components

Continue in the same PowerShell session. The quoted here-string prevents PowerShell from interpreting Python code. `xb` refuses to replace an existing `.bin` output.

```powershell
@'
from pathlib import Path
import sys, zlib

folder = Path(sys.argv[1])
for name in ('header', 'gamesetup', 'meta', 'data'):
    source = folder / (name + '.a7s')
    payload = zlib.decompress(source.read_bytes())
    if not payload:
        raise ValueError('Empty decompressed component: ' + name)
    target = source.with_suffix('.bin')
    with target.open('xb') as stream:
        stream.write(payload)
    print(name, len(payload), 'bytes')
'@ | & 'D:\CDesktopLink\Portable\Python\WinPy64\python\python.exe' - $unpackedDir
if ($LASTEXITCODE -ne 0) { throw 'Component decompression failed.' }
```

### Decode a component with FileDBReader

Start with the small header. FileDBReader writes XML next to the input `.bin`; use distinct copies for raw and interpreted output. The following raw conversion uses the installed minimal interpreter.

```powershell
$fdbDir = Join-Path $toolDir 'FileDBReader'
$rawBin = Join-Path $unpackedDir 'header.hex.bin'
Copy-Item -LiteralPath (Join-Path $unpackedDir 'header.bin') -Destination $rawBin
& (Join-Path $fdbDir 'FileDBReader.exe') decompress -f $rawBin -i (Join-Path $fdbDir 'FileFormats\a7s_hex.xml') -y
if ($LASTEXITCODE -ne 0) { throw 'FileDBReader failed.' }
$rawXml = Join-Path $unpackedDir 'header.hex.xml'
if (-not (Test-Path -LiteralPath $rawXml -PathType Leaf) -or
    (Get-Item -LiteralPath $rawXml).Length -eq 0) {
    throw 'FileDBReader did not produce a nonempty XML file.'
}
```

For a separate interpreted copy, repeat with `header.typed.bin` and `a7s_all_serp.xml`. For condition/quest inspection, select `data.bin` instead. Validate the resulting XML before making conclusions. A zero exit code alone is insufficient: this FileDBReader returned zero while reporting that an output file was in use. Complete interpretation of the large data component can take minutes and produce hundreds of megabytes; do not start another writer against its output while it is running.

## Interpreter limits and hexadecimal values

`a7s_all_serp.xml` explicitly says it was partly generated by guessing types from payload length. Its own header warns that it cannot distinguish floats from integers reliably. For example, it interpreted `PinnedResources` bytes as a string, producing references such as `&#x14;` and `&#x0;`, which are invalid XML 1.0 characters. The source save is not thereby shown corrupt.

Keep the original field bytes. A strict parser failure, a plausible-looking decimal or readable text is not proof of the correct interpretation. A recovery parser or replacement of invalid character references can help examine unrelated fields, but that is a lossy analysis view. It must not become a write-back input or evidence that all fields decoded correctly. The direct reader below avoids guessed payload types. The minimal `a7s_hex.xml` also contains nested-session expansion and tag-renaming rules; its XML is not a byte-identical representation of every nested blob.

| Inspected field | Interpretation used in this investigation |
| --- | --- |
| `ConditionKey`, entries of `SubConditionKeys`, `EventDataString` | UTF-8 text from their raw payloads |
| `AssetGUID`, `TriggerAsset`, `Quest`, lowercase `questGUID`, `QuestID` | Little-endian integers, after checking their field/context |
| Saved action `ScriptFileName` and notification `Callback` | UTF-16LE in the inspected snapshots |
| `EventType/id` and `QuestState/id` | Little-endian enum values, resolved against the matching vanilla dataset |
| `ConditionQuestStateStates` | A serialized flag string in these snapshots; not an arbitrary integer |

An integer-shaped payload can instead be a float, a list or a packed structure. Do not select a decoder solely from length. Preserve absence versus an empty element; do not universally turn both into Boolean false or enum zero. In particular, native `ConditionResult` has `Success=0` and `Failed=1`: zero is not a general "still waiting" indicator.

## Minimal structural reader for selected managers

The inspected FileDB reader uses eight-byte node headers. Tags have no attribute payload; closing tags are terminators. Attribute payloads occupy `ceil(size / 8) * 8` bytes, with padding excluded from the declared size. The last 16 bytes contain dictionary offsets followed by magic `(8, -2)` or `(8, -3)`. V3 additionally has footer fields before those offsets. Dictionaries contain an Int32 count, UInt16 IDs and zero-terminated names. Reserved tag ID `1` and attribute ID `32768` mean `None` and need no dictionary entry. These IDs are document names, not asset GUIDs. See also [binary format contracts](../ui-and-resources/binary-formats.md).

This example reads a decompressed component, retains raw hexadecimal payloads only inside selected managers, and skips all other payloads. It does not expand session `BinaryData`, infer field types, edit or serialize a save. It requires `lxml`, which is available in the inspected portable Python. Unknown IDs and malformed/truncated structures cause an error instead of silently inventing names.

```python
from pathlib import Path
import struct
from lxml import etree as ET

def selected_managers(path, targets):
    data = Path(path).read_bytes()
    if len(data) < 32 or struct.unpack_from('<ii', data, len(data) - 8) not in ((8, -2), (8, -3)):
        raise ValueError('Expected a FileDB V2/V3 component')
    tags_at, attrs_at = struct.unpack_from('<ii', data, len(data) - 16)
    if not 0 < tags_at < attrs_at < len(data) - 16:
        raise ValueError('Invalid dictionary offsets')

    def dictionary(offset, end):
        count = struct.unpack_from('<i', data, offset)[0]
        if count < 0 or offset + 4 + count * 2 > end:
            raise ValueError('Invalid dictionary count')
        ids = struct.unpack_from('<' + 'H' * count, data, offset + 4)
        position = offset + 4 + count * 2
        result = {}
        for ident in ids:
            stop = data.index(b'\0', position, end)
            if ident in result:
                raise ValueError('Duplicate dictionary ID')
            result[ident] = data[position:stop].decode('utf-8')
            position = stop + 1
        return result

    tags = dictionary(tags_at, attrs_at)
    attrs = dictionary(attrs_at, len(data) - 16)
    position, stack, current, roots = 0, [], None, []
    terminated = False
    while position + 8 <= tags_at:
        size, raw_id = struct.unpack_from('<iI', data, position)
        ident = raw_id & 0xffff
        position += 8
        if size < 0:
            raise ValueError('Negative node size')
        if ident == 0:
            if size != 0:
                raise ValueError('Invalid terminator')
            if not stack:
                terminated = True
                break
            if current is not None:
                current = current.getparent()
            stack.pop()
        elif ident < 32768:
            if size != 0:
                raise ValueError('Unexpected tag payload')
            name = 'None' if ident == 1 else tags[ident]
            stack.append(name)
            if current is not None:
                current = ET.SubElement(current, name)
            elif name in targets:
                current = ET.Element(name, binary_path='/'.join(stack))
                roots.append(current)
        else:
            name = 'None' if ident == 32768 else attrs[ident]
            stop = position + ((size + 7) // 8) * 8
            if stop > tags_at:
                raise ValueError('Truncated attribute payload')
            if current is not None:
                ET.SubElement(current, name).text = data[position:position + size].hex()
            position = stop
    if not terminated or stack:
        raise ValueError('Unterminated FileDB document')
    return roots

# Use an analysis copy produced by the preceding decompression step.
# managers = selected_managers(r'C:\analysis\data.bin', {'ConditionManager', 'QuestManager'})
```

This is a bounded inspection example, not a replacement for the official library or an approved save editor. Its targeted condition-key/GUID output was compared with FileDBReader on three actual saves; that comparison does not verify every payload, nested session or future save format.

## Inspecting saved conditions and actions

The inspected global component contains `MetaGameManager/ConditionManager/Conditions/None`. Each condition stores its own `ConditionKey` and an owning `AssetGUID`. One asset can have a main condition and several descendants, or multiple registered copies. Follow each `SubConditionKeys/None` string to the corresponding `ConditionKey`; the XML order and a shared owning GUID do not establish parentage.

`participantID/value/id` is the processing participant. Inspect `EventType/id`, `EventDataString`, `CallAmountCurrent`, `ConditionFulfilled`, `IsResolved`, `IsActive` and the saved `Actions` together. Their observed combinations describe a snapshot, not a complete execution log. For example, New World listener `153242` can have a fulfilled film event while its banner child remains pending. Absence from the active condition list alone does not distinguish completed, unregistered and never-created instances.

Resolve enum IDs against the correct dataset: `SimpleEventType` has `SessionLoaded=9` and `GUIDLocked=129`. A saved GUID event's `EventDataString` was UTF-8 digits such as `1500004306`. Do not confuse these event IDs with a GUID, or assume the internal saved `conditionTypeEnum` is the same enum. Saved actions may contain their original callback and registration targets even when the current mod file has changed.

Registration snapshots and migration follow the existing [trigger lifecycle contract](triggers.md#savegames-removal-and-extension-points). Fresh registration reads current code; an active saved instance retains its old definition. XML and Lua registration have different previously documented behavior. This investigation did not re-test that distinction. One-off migration triggers are not automatically replayed because the contents of their XML changed. Updating a definition does not replay missed edges, restore quest progression or make repeated rewards safe.

## Quest and peer interpretation

`MetaGameManager/QuestManager` contains `RunningQuests` and `QuestHistory` in these saves. Use lowercase `questGUID`, instance `QuestID`, assignee and `QuestState/id` together. Vanilla `QuestState` identifies `Active=2` and `Reached=4`. Two running records with the same quest GUID and different instance IDs are evidence of two instances; they do not by themselves identify the code or person that created them.

The header's `CorporationProfile/GameSetup/Peers/Peer` records configured peers, including human account assignment and team membership. Do not publish their account identifiers. The examined setup contains 16 peer entries, including AI/closed entries, so `PeerCount` or a vector count of 16 is not a human headcount. Coop humans can share the same company/team. Compare whether account fields are populated and corroborate with other saved state, rather than counting every historical human configuration as currently connected.

`PeerToSessionMap` retained three entries in saves whose header assigned only one human account. Its last/current session fields therefore are not a reliable connected-peer list. Construction-AI `ThreadStateOfEachPeer` provided a corroborating difference in this case, but is not established as a universal online-human API. The resulting solo-versus-Coop assessment remains an inference, not a reconstructed network log. See [multiplayer execution](../multiplayer/synchronization.md).

## Establishing which code was active

Use three separate evidence layers:

1. **Save metadata:** active mod.io IDs/local ModIDs establish recorded mod identity. The examined headers have no concrete mod-version field.
2. **Release history and package:** a save date plus the user's assumption of the latest release gives a likely version. Retain release file ID, archive hash and actual package contents; timestamps alone are insufficient.
3. **Saved code:** compare exact callbacks, actions and condition trees with both the release and workspace. Several snapshots can coexist from different code revisions.

The New World case demonstrates why a matching `modinfo.json` version is insufficient: release 1.021 and the workspace both report 1.021, but only the workspace fixes the incorrect Skip callback. Do not infer the exact historical release for every active instance from the date of the enclosing save. Record remaining uncertainties and use a fresh game separately from pre-transition, in-transition and already-blocked saves when planning future tests.

Original mod example: [Campaign callback source on GitHub](https://github.com/Serpens66/Anno-1800-Mods/blob/88821b04ee972424667178d35a5080a753a853d0/YouKnowWhatYouDo-Mods/Campaign%20in%20Coop%20%28Serp%29/data/config/export/main/asset/AntiDesync/ADMovies.include.xml#L583-L588). The linked CodeReview report and generated save excerpts are local artifacts.
