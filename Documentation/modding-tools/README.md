# Modding tools

This section describes external tools and practical workflows for Anno 1800. It is separate from the knowledge base's own [research and validation scripts](../tools/README.md). Start with the [setup](../setup.md); native feature audits and the project's allocation rules still apply before creating game-dependent changes.

## Anno Toolbox

For a code-backed answer about custom buttons, new widgets, existing UI edits and end-user requirements, read [UI editor capabilities](ui-editor.md).

[SunnyM00n/anno-toolbox](https://github.com/SunnyM00n/anno-toolbox) is a Python-based suite of editors, viewers and converters for several Anno games. **Review snapshot: 2026-11-16, package 0.1.2, commit `edb26301d79c7af1b497103ca5b5691451ad0946`** ([source snapshot](https://github.com/SunnyM00n/anno-toolbox/tree/edb26301d79c7af1b497103ca5b5691451ad0946)). The latest commit at cloning was the 2026-11-15 hotfix for ground visibility and animation while zooming in the 1800/2205 views.

Evidence here is **upstream guide plus bounded source review**, not an independent game test. Upstream [suite documentation](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/suite.md) explicitly says nothing the suite writes has been loaded by a game yet. Read the current upstream guide after updates; neither a successful build nor an internal check establishes that generated content works in Anno 1800. This review inventories tool capabilities, not native gameplay contracts, and changes no mod or save.

### Which tool helps with which task?

Select an app in the suite's left sidebar. The guides below are pinned to the reviewed revision.

| Tool | Useful for Anno 1800 modding | Starting workflow and limits |
| --- | --- | --- |
| [Viewer](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/viewer.md) | Inspect models, textures, animations, effects and sounds; locate source resources before editing. | Open the game tree or a file, inspect its preview and references, then use **File > Export**. A file with no discovered reference can still be loaded through a name constructed at runtime; do not delete it on that result alone. |
| [Assets](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/asset-editor.md) | Search assets and edit schema-generated forms; prepare ModOps for a new project. | Select game/project, search an asset, change fields, inspect the change set and build into a separate output. Importing an existing mod reconstructs effective changes and reports unsupported parts; it does not preserve every conditional design or the original XML structure. Keep hand-maintained complex mods intact. |
| [Texts](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/text-editor.md) | Translate mod texts with two languages side by side; find untranslated rows and placeholder/markup problems. | Open texts in the project, select the language pair, edit rows or exchange CSV/XLIFF/PO, inspect checks, save and build. Verify the generated 1800 text files and text IDs. |
| [UI](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/ui-editor.md) | Explore and edit supported 1800 Phoenix interface structures with a preview and bindings graph. | Open a supported UI document, inspect the widget tree and preview, edit a copied project document and build. Preview values and codec tests do not demonstrate runtime bindings. This is not a replacement for the [infotip binding audit](../ui-and-resources/infotips-and-text.md). |
| [Objects](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/object-builder.md) | Assemble a model config: parts, materials, effects, lights, sequences and info-file boxes. | Open a config, select parts in the tree/3D view, change their properties, then choose a new file, replacement or patch in the project. Inspect output paths and patches before applying them. |
| [Particles](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/particle-editor.md) | Inspect and edit supported baked 1800 particle data with playback. | Open an 1800 `.rdp` from a file or model, inspect its baked ticks and supported header/material/tint fields, preview, then save a replacement or a private copy. Older games' emitter-curve workflows do not apply to this format. Editor playback is not an in-game test. |
| [Sound](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/sound-editor.md) | Browse 1800 Wwise banks, events, containers and media; prepare supported clip replacements. | Open a bank, follow an event to its media, preview/export it, and use the supported replacement workflow in a separate project. Some audio conversions need ffmpeg or ww2ogg codebooks. |
| [Islands](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/island-editor.md) | Explore islands in 3D; prepare object, terrain, ground, river and forest edits or island ports. | Configure the 1800 install, open an island, save edits into a project and build separately. Upstream assumes path replacement for 1800 island loading; that assumption is not a demonstrated native contract. Cross-game/region conversion needs its own feature audit and game checks. |
| [Maps](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/map-editor.md) | Edit session/map templates, island slots, start positions, size and playable area. | Open the 1800 map, change placements/slots, inspect checks and growth reports, save and build. Keep map and island editing distinct, and preserve IDs needed by existing saves. |
| [Mod diff](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/mod-diff.md) | Compare versions and inspect likely asset/value changes or profile conflicts; export Markdown/CSV reports. | Choose game/mod or two versions, run comparison and inspect both values and file differences. Positional list matching, omitted list-only reorders and file-only treatment of binary infotips limit the report. Its evaluator is not the actual 1800 loader; see the discrepancy below. |
| [Mods](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/mod-manager.md) | Inspect installed mods, profiles, proposed load order, issues and the previous loader log. | Inspect first. Activating/installing/removing or applying a profile changes installed state. Upstream explicitly leaves 1800 activation/profile behavior unverified; retain an independent copy of the working setup. |
| [Saves](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/save-editor.md) | A candidate generic archive/tree inspection tool. | Upstream has no 1800 save sample in its stated coverage. Do not promise decoded 1800 summaries, money edits or safe write-back. Use the established [savegame workflow](../gameplay/savegames.md) and qualify any new decoder evidence. |
| [RDM/glTF](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/rdm-gltf.md) | Inspect/diff model records and exchange meshes with Blender through glTF. | Export, edit in Blender, export glTF with **Custom Properties**, import using the original as `--like`, then inspect the report and compare. Upstream's actual Blender round trip is untested; `validate`/`relayout` target 117 conventions, so they are not a general 1800 repair step. |
| [Batch export](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/exporting.md) | Extract stored resources plus converted textures, models, audio or tabular data for research. | Choose a file/folder and formats; inspect `index.json`/`index.csv` for `failed` or `tool-missing`, not merely process exit status. Converted JSON is a reading aid and can abbreviate binary fields; retain the stored originals. |

**Not an 1800 feature:** the optional engine-hooking [Live Link](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/live-link.md) helper is currently for Anno 117 only. The separate UI 2205 app is also outside this chapter's scope.

### Install and start from the clone

Use your own Python **3.12 or newer**, an OpenGL 3.3 driver and your own game installation. A clone contains source, not an installed application. Open PowerShell in the clone folder and run the following once (substitute your interpreter if `python` is not on PATH):

    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -e ".[gui]"
    .\.venv\Scripts\python.exe -m annotoolbox --app viewer

The virtual environment avoids changing a shared Python installation. `[gui]` installs PySide6, moderngl, numpy, scipy and Pillow. For command-line-only work use `pip install -e .`; add `pip install -e ".[textures]"` for decoded texture export. The package is not published on PyPI at the reviewed snapshot: use the clone, the root README's Git URL, or the upstream Windows MSI, rather than the abbreviated PyPI commands in some sub-guides.

1. Set game paths under **Islands > File > Games and folders**, and optionally choose German as the interface language. Settings are shared under `%LOCALAPPDATA%/anno-toolbox`.
2. Use **Project > New** with a separate empty project folder and **Anno 1800**. Keep edited files and build output separate from source archives and existing hand-maintained mods.
3. For Serp assets, use the [existing reserved range and live allocation check](../reference/serp-guid-usage.md). Do not accept an automatic project range as permission to bypass that register or to take someone else's reservation.
4. Switch to the relevant app, inspect/edit and save the project. **Build mod** writes `build/<mod id>/`; review its metadata, ModOps, file paths and IDs. **Build & install** additionally copies into the configured game mods folder and requires installation authorization.
5. Complete the native feature audit and actual 1800 loader checks for generated changes, then test the particular game/save scenario. Keep these results distinct from Toolbox previews and upstream synthetic tests.

To open only the standalone 1800 island editor:

    .\.venv\Scripts\python.exe -m annotoolbox --games anno1800

At this revision `--games` is passed to the standalone editor; the suite path selected with `--app` does not forward it. Select the project's game explicitly in the suite.

The GUI texture path uses **texconv**: obtain it from [Microsoft DirectXTex](https://github.com/microsoft/DirectXTex/releases), put it under the clone's `tools/` folder or on PATH, or set `ANNO_TEXCONV`. See the upstream [tool instructions](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/tools/README.md). ffmpeg and ww2ogg codebooks are optional for particular exports; read the export report to see which are missing. These dependencies were not installed as part of this review.

The upstream [Windows installer](https://github.com/SunnyM00n/anno-toolbox/releases/latest) is an alternative that bundles Python and GUI libraries. Installing it creates a separate application; updating the Git clone does not update that installation.

### Command-line examples

Run from the clone after installing into `.venv`; paths below are placeholders for your own copies and output folders.

    .\.venv\Scripts\python.exe -m annotoolbox --help
    .\.venv\Scripts\python.exe -m annotoolbox rdm inspect model_lod0.rdm --values
    .\.venv\Scripts\python.exe -m annotoolbox rdm export model_lod0.rdm -o exported/ --lods
    .\.venv\Scripts\python.exe -m annotoolbox rdm import edited.glb --like model_lod0.rdm -o imported/model_lod0.rdm
    .\.venv\Scripts\python.exe -m annotoolbox rdm diff model_lod0.rdm edited.glb --values
    .\.venv\Scripts\python.exe -m annotoolbox export textures/ -o exported-textures/ --format png,exr

The inspected [CLI dispatcher](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/src/annotoolbox/suite/toolbox.py) also exposes `rda`, `island`, `save`, `viewer-files` and `unreferenced`. Start with each group's `--help`; presence in the CLI is not proof of support for every game's files. The root README's list of only `rdm` and `export` is incomplete at this revision.

### Keep up with fixes

The locally added **`update.bat`** lives in the clone root. Double-click it, or run `& .\update.bat /nopause` from PowerShell. It locates Git for Windows, requires this upstream's `main` branch, rejects tracked modifications and local commits, fetches `origin` and applies only a fast-forward. On a network error, local edit or diverging history it stops; it does not reset, stash or resolve conflicts. Untracked files are retained; Git refuses a merge that would overwrite one. The helper itself is excluded only through `.git/info/exclude`, without changing upstream files.

Close running Toolbox windows before updating. An editable Python install uses the updated source; if dependencies/package metadata changed, rerun:

    .\.venv\Scripts\python.exe -m pip install -e ".[gui]"

The helper updates **source only**. It neither installs Python dependencies nor updates an MSI application, and it is not a scheduled task. After an update, read upstream changes and recheck the affected workflow. The installed MSI's **Help > Check for updates** handles published releases separately; unreleased fixes can already be on `main`.

For knowledge maintenance, record a new reviewed commit and changed capabilities here rather than silently treating this dated review as current. Preserve prior test qualifications and add actual 1800 results only when performed.

### Known documentation and validation gaps

- The [Mod diff guide](https://github.com/SunnyM00n/anno-toolbox/blob/edb26301d79c7af1b497103ca5b5691451ad0946/docs/mod-diff.md) groups 1800 with 117 for constructs including `ModItem`, `ModValue` and options, while admitting 1800 behavior is unknown. These are not established 1800 capabilities in this knowledge base. Use the supported legacy syntax and the [actual 1800 evaluator](../reference/offline-validation.md); a Toolbox lint/diff pass is supplementary.
- Some sub-guides show `pip install anno-toolbox` even though the root README says the package is not on PyPI. Use the installation above.
- Upstream documents 1800 island replacement as an assumption, 1800 mod profiles as unverified, and no 1800 save sample. Those workflows remain pending independent native/in-game validation.
- This review read the root README, packaging/CLI entry points and the linked app/export guides. It did not audit the entire implementation, execute the GUI, install dependencies, load generated output into a game, modify a save, or perform multiplayer tests. No native feature audit was required for this tool inventory; one is required before relying on generated game-dependent changes.

### Local checks on 2026-11-16

- `update.bat /nopause` completed a real fetch/fast-forward check against upstream; the clone was already current and remained clean. The dirty/divergent/error branches were source-reviewed, not exercised with fabricated repository states.
- Source CLI `--version` returned 0.1.2 and `--help` listed the documented command groups. This used the configured interpreter and checkout source path without installing dependencies or opening a GUI.
- The read-only documentation validator reported no findings across 423 text files, 3,241 internal links and 731 XML snippets; Git whitespace checks passed. These checks establish documentation structure, not tool output or game compatibility.

### Local source runtime and UI editor (2026-11-16)

The local checkout now has a dependency-only `.venv` based on the existing portable Python 3.12.8. The Toolbox package itself is **not installed**: the local runner adds the checkout's `src` to the Python import path. No MSI or global Python package installation is needed. This is an additional local setup after the initial review above; the dated upstream review and game-output limitations still apply.

| Local file | Purpose |
| --- | --- |
| `start-ui.bat` | Open the full suite directly on **UI**, with the configured Anno 1800 game and German menus on first start. |
| `start-toolbox.bat` | Open the same source suite on **Viewer**; switch to any other app in the sidebar. |
| `source-cli.bat` | Pass CLI arguments through the same environment, e.g. `source-cli.bat --help` or `source-cli.bat rdm inspect model.rdm`. |
| `refresh-environment.bat` | Read the current GUI requirements from `pyproject.toml` and install missing/changed requirements only in `.venv`; record versions in `environment-versions.txt`. It does not force upgrades of every already-satisfying library. |
| `local-runtime.json` | Personal game/tool paths and first-start language. Tool paths are applied to the launched process only; edit this file if an external tool moves. |
| `source-launcher.py` | Shared source path, tool environment and first-start settings initialization. |

Double-click `start-ui.bat`. The UI app automatically reads the configured Anno 1800 installation; the first start indexes its archives. Pick a scene or widget under **Files**, then inspect its elements, properties, preview, sample values and bindings. **F** fits the preview, the wheel zooms, and middle-drag pans. Browsing needs no new mod project. Saving edited UI content and building a mod are separate actions, subject to the feature audit and review workflow.

The runtime keeps its settings/cache under `.local-appdata/anno-toolbox` and its workspace under `.workspace` in the clone. `LOCALAPPDATA` is redirected only for the child Toolbox process; no persistent Windows environment variable is changed. The venv, runtime files and local launchers are ignored locally through `.git/info/exclude`; upstream tracked code is unchanged. They depend on the configured portable Python installation remaining available.

Existing ffmpeg and texconv were connected through `ANNO_FFMPEG` and `ANNO_TEXCONV`. Paths are kept in personal local configuration, not this chapter. The reviewed Wwise workspace contains ffmpeg/vgmstream helpers, but no matching ww2ogg codebook file was found there; `wwcodebooks` remains optional and unconfigured. This does not block the UI editor. The existing Wwise workflow was not changed.

After `update.bat`, restart the Toolbox. Source changes are used immediately at the next launch; run `refresh-environment.bat` when upstream requirements change. Keep the launchers and runtime folders when updating. An upstream API or dependency change can require rechecking this local setup.

Environment checks: GUI libraries import successfully and `pip check` reports no broken requirements. The UI window was constructed offscreen and opened the actual Anno 1800 archives, reporting **4,461 scenes and widget files**. This establishes startup/index access only; no UI file was edited, generated mod built, game runtime behavior established or save changed.

The final real update check fast-forwarded to `5e436bb0f1503cfb42ad3810ae1c4473505dbbc0`; the same source-launcher UI/Anno 1800 check passed again on that revision. This updates the local runtime receipt only, not the earlier complete tool-guide review scope. The checkout remains clean.
