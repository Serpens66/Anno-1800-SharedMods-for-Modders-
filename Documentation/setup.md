# Set up your own sources and tools

For explanation and research, read the topic chapters and their public links directly. No local configuration or access to Serp's computer is required. For creating or changing a mod, provide the current sources needed for its feature audit.

## Give the chat access

With a local assistant, open the downloaded Documentation folder and the relevant mod/source folders, or provide readable absolute paths. Explicitly ask it to read [AGENTS.md](AGENTS.md) when Documentation is not its working directory; do not assume instructions in a neighbouring folder are discovered automatically.

For a chat reading GitHub, start with the public [README](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/blob/main/Documentation/README.md). It links the same chapters, public mod examples and evidence summaries. A GitHub link does not load every linked file automatically: ask the chat to open the relevant sources and report inaccessible ones.

A path on your computer does not grant a web chat file access. Upload the required source files or relevant complete owning definitions and their dependencies, or use a local assistant. If the available files cannot support a complete feature audit, stop dependent implementation decisions and request the missing sources. Never substitute Serp's historical extraction for the user's current game data.

## Extract your game data

Use [RDAExplorer](https://github.com/lysannschlegel/RDAExplorer) and the [reviewed community extraction guide](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/getting-started/tools-you-need.md). Extract to a separate directory. Follow the guide's lower-to-higher archive order, with newer copies replacing older ones; inspect installed update archives and the tool's current instructions. A stale or mixed extraction is not current Vanilla. Record the game/extraction version when known.

Under the extracted root, provide:

    data/config/export/main/asset/assets.xml
    data/config/export/main/asset/templates.xml
    data/config/export/main/asset/properties-toolone.xml
    data/config/export/main/asset/properties.xml
    data/config/export/main/asset/datasets.xml

Localized text, decoded infotip export, native Lua, graphics and other resources are additional feature-specific inputs. The [audit procedure](foundations/vanilla-research.md) determines what is needed. This folder bundles no extraction tool, executable or complete game database.

## Local configuration

Copy [local.example.json](local.example.json) to ignored `local.json` in this folder. Use strict JSON, with no comments or trailing commas. Windows paths may use `/`; JSON backslashes must be doubled. Relative paths resolve against the configuration file's directory, not the current shell directory.

| Field | Meaning |
| --- | --- |
| configVersion | Integer 1 |
| gamePath | Installation root containing Bin/Win64/Anno1800.exe |
| vanillaPath | Your extracted root containing the five files above |
| modsPath | Optional installed-mod folder; may remain blank |
| workPath / outputPath | Separate generated-mod and audit/output directories; defaults work and out |
| tools.xmltest | Optional actual Anno 1800 xmltest.exe |
| tools.lua / tools.python | Optional interpreter paths |
| workspacePath | Optional root for research scans and historical workspace-relative identities |
| researchPath | Optional directory containing explicitly obtained upstream research checkouts |
| sources | Optional map from source identity to local file/directory, e.g. Anno-1800-Mods, SharedMods, notes:HowTo.xml, notes:info.txt, savegameTools |
| pathAliases | Optional map from a historical absolute directory prefix to its current local replacement |

Use `sources` for independently located checkouts. The historical shared-repository identity `Anno-1800-SharedMods (for Modders)` is recognized as `SharedMods`. Source resolution never downloads anything. Configure only material you actually have; notes and historical reports are not required for ordinary mod work. `ANNO_DOCUMENTATION_CONFIG` can select an alternative configuration file for Python tools.

Keep work/output separate from each other, installation, extracted data, installed mods and configured source directories. Keep them outside the maintained Documentation files except for its ignored work/out folders. For custom generated locations inside another repository, add ignore rules before writing.

From this folder, run the read-only Windows setup check:

    & .\tools\check-setup.ps1
    & .\tools\check-setup.ps1 -ConfigPath 'C:/my sources/local.json'

Use an approved local PowerShell execution route; no machine-wide execution-policy change is required. Exit 0 means required presence/type/path checks passed; exit 1 means errors. WARN identifies unavailable optional checks. The check does not launch tools, create files, establish freshness or prove game compatibility.

## Optional offline evaluator

[Anno Modding Tools](https://github.com/anno-mods/vscode-anno/tree/19cda8edc73d65a622c9c5c588953a0170c337c6) includes an evaluator. Select its actual `external/xmltest.exe` for Anno 1800, not Anno 117's `xmltest2.exe`. Version 2.3.1 was the historical reviewed installation; verify the version/provenance of your own executable. VS Code is optional. Missing xmltest leaves actual loader checks unavailable; it does not block reading the documentation.
