# Anno Toolbox UI editor: capabilities and distribution

Reviewed 2026-11-16 at Toolbox commit `5e436bb0f1503cfb42ad3810ae1c4473505dbbc0`. This is a source review plus a bounded native scene/widget audit, not a successful generated-mod game test. See the [tool overview and local launchers](README.md) and [native inspection receipt](../reference/ui-editor-audit.json).

## Practical answers

| Question | Supported conclusion |
| --- | --- |
| Change an existing UI? | Yes: open an existing scene or widget, change supported fields/elements/bindings and save binary output. Runtime correctness of the particular edit still needs a game test. |
| Make a new UI? | New **widget files** can be created and placed through a container in an existing UI. There is no demonstrated automatic registration of an arbitrary new independent game scene/window. |
| Add buttons and interaction? | Reuse existing game widgets/components and their supported event/action bindings. An arbitrary new button callback or arbitrary Lua function is not implemented by this editor alone. |
| Distribute normally? | The build copies the saved binaries into a mod folder at their game paths and writes metadata. A plain UI-resource mod needs the game's normal mod support, not the editor, Python or conversion tools on the recipient's computer. Its particular files must still be accepted in a real 1800 test. |

## What is actually editable

The [UI app](https://github.com/SunnyM00n/anno-toolbox/blob/5e436bb0f1503cfb42ad3810ae1c4473505dbbc0/src/annotoolbox/uiedit/uiwindow.py) and [document mutations](https://github.com/SunnyM00n/anno-toolbox/blob/5e436bb0f1503cfb42ad3810ae1c4473505dbbc0/src/annotoolbox/uiedit/uidoc.py) implement editing of existing scene (`SC`) and widget (`WI`) files. This includes stored properties, position/scale/colour, supported image and text references, component/effect values, element duplication/removal, custom properties, binding changes and animation keys/tween parameters. Values controlled by bindings/animations can override static edits; the context must be inspected for the particular file.

The directly creatable visual primitives are **container, image, label and video**. Existing template/component behavior supplies higher-level controls. The editor can add declared library components/effects when their descriptions are available. Not every advertised library feature is available for every game: this native 1800 extraction has no `data/ui/pwl/` directory or `data/script/types/generated/rdui/gameobjects/` stubs. Names and descriptions may therefore be missing; the editor can show numeric IDs/hashes instead. The game object's older `gameobjectsstructure.json` contains malformed unescaped quotes in a description and was not treated as valid complete JSON evidence.

**File > New widget file** creates a binary `WI` document with a deterministic UUID based on the project ModID/name (`uiwindow.py:714-727`, `uidoc.py:339-348`). A container's `Template` references that widget. A new widget file by itself is not an instruction for the engine to display it: some loaded scene/widget must reference it. There is no equivalent new-scene-and-register workflow in the inspected menu/code. Do not confuse these UUID resource names with gameplay asset GUID reservations.

## Buttons, events, actions and scripts

[Binding dialogs](https://github.com/SunnyM00n/anno-toolbox/blob/5e436bb0f1503cfb42ad3810ae1c4473505dbbc0/src/annotoolbox/uiedit/bindingdialogs.py) can declare custom **Event** and **Action** properties and connect sources through an operator to targets. This provides UI interface/dataflow declarations; it does not implement a new engine function. A declared action with a chosen name does not make the game execute that name as Lua.

The new-binding picker exposes the document's custom properties, element builtins and source constants, with event/action direction filtering for builtins. It does not provide a universal **OnClick -> arbitrary Lua function** workflow or enumerate all custom component event paths. The builtin table contains lifecycle, image-loading, video and animation events/actions, not a general button callback wizard. Existing button/widget wiring remains important when creating a control.

The **States and events** panel displays declarations/existing bindings and animation controls; it is not a general handler-code editor. **Load a script list** reads JSON function metadata, and **Add readout** creates a custom UI property (`uiwindow.py:459-475`). These operations do not generate a Lua implementation or establish a new 1800 script-to-UI bridge.

Therefore distinguish three tasks: constructing a control's appearance, wiring a supported UI event, and performing a particular game operation. Each additional game operation or script bridge requires its own feature-specific audit. Arbitrary new engine actions, a custom window-opening API and arbitrary Lua callbacks remain **unestablished**, rather than proven impossible.

## Native composition evidence

The audit read complete binary trees for `confirmationmenuscene`, `pausemenuscene` and their complete **container-template** closure: 16 files / 85,546 bytes. It followed actual references rather than treating a file-name hit as the native contract. This closure covers document composition/interfaces, not all image/font/component resources or engine action implementations.

- `confirmationmenuscene` places `ConfirmPopup` -> `0b645fc8-92f4-41ef-994c-86753c8a336e` -> `GeneralPopupButtonList` -> `e40c85e3-5da8-49b9-afa8-cc3d64e76f83` -> `TextButton_48` -> `467338cc-e409-4500-aad1-b4929557b95b`.
- `pausemenuscene` places `PauseMenu` -> `1d45b9de-2072-4380-bec4-2907113e42e2`. The latter declares events `ResumeButtonReleased`, `TitleButtonReleased`, `OptionsButtonReleased`, `QuitButtonReleased`, `LoadButtonReleased` and `SaveButtonReleased`.
- The pause scene has 22 bindings, including child event paths assigned to its `GameContext` paths. The event declarations and stored connections are structural evidence; interpreting every hashed destination as an arbitrary mod-defined action is not justified.

The receipt records hashes, complete-decoding status, re-encoding comparisons, native element references and custom-property declarations. No gameplay-asset/default/dataset contract was substituted: these particular declarations are binary UI documents, and no gameplay action implementation is proposed. Engine-backed destination semantics remain explicitly unknown where not traced.

## Build and end-user requirements

[UI project output](https://github.com/SunnyM00n/anno-toolbox/blob/5e436bb0f1503cfb42ad3810ae1c4473505dbbc0/src/annotoolbox/uiedit/projectpart.py) saves changed/new UI files under `ui-edits/<game>/<game path>`. The shared [project builder](https://github.com/SunnyM00n/anno-toolbox/blob/5e436bb0f1503cfb42ad3810ae1c4473505dbbc0/src/annotoolbox/suite/project.py) copies them into `build/<mod id>/` and writes `modinfo.json`. A resulting UI file can be distributed at:

    <mod folder>/modinfo.json
    <mod folder>/data/ui/studio/generated/<existing scene name or widget UUID>

New widget references, resources and metadata must all be included. Follow the [ordinary 1800 overlay/loading rules](../foundations/structure-and-loading.md); the reviewed historical 1800 external-file loader also reads unpatched resource replacements from their mod disk paths. This establishes the intended packaging route, not an independently verified runtime acceptance of every newly encoded Phoenix file.

The recipient of a **plain UI-resource mod** needs Anno 1800 with its normal mod support and any dependencies explicitly shipped/declared by that mod. They do not need Toolbox, Python, `.venv`, ffmpeg, texconv or a development hook DLL. A separate mod feature that introduces a genuine runtime dependency must document it separately. Toolbox's optional Live Link/game-dump integration is for **Anno 117**, not a prerequisite for a normal 1800 UI mod.

UI output is a **whole binary file replacement**, not an XML merge patch for individual UI elements. Independent mods replacing the same file can conflict; load order alone cannot combine their edits. Editing a widely shared button widget can also affect many places using it; a private cloned widget still needs its parent reference changed.

## Verification limits

`UiDoc` checks its decoder/writer against the original bytes and warns about nonexact files. The upstream guide reports only about **93% of 1800 files** round-trip byte-identically; this is an author report, not a local full-game scan. An unedited document retains original bytes; an edited document uses the binary writer.

The native audit and successful earlier startup/indexing of 4,461 scenes/widgets do not establish edited-file loading, appearance, click behavior, save safety or multiplayer behavior. Upstream explicitly says UI-editor changes have not been loaded by a game; its separate codec experiment is not that test. Before distributing a particular UI, inspect its consumers/references and test the built mod in game.

## Replacement granularity and possible editor improvements

Follow-up review on 2026-11-16 confirms that **the visual scope of an edit and the file scope of its deployment differ**. The native pause scene references `PauseMenu` widget `1d45b9de-2072-4380-bec4-2907113e42e2`. In that parent, `btnResume`, `btnOptions`, `btnSave`, `btnLoad`, `btnTitle` and `btnSaveExit` all reference shared button widget `467338cc-e409-4500-aad1-b4929557b95b`.

| Intended change | Actual output scope |
| --- | --- |
| Move/restyle supported instance properties of only `btnResume` | Replace the complete parent PauseMenu widget binary; the separate `pausemenuscene` need not change. |
| Edit the shared button widget itself | Replace that widget binary; every scene/control referencing it may inherit the edit. |
| Give only `btnResume` different internal widget content | Create a private widget copy and change that instance's template reference. Output includes the private new widget plus the complete changed parent binary. This is a proposed assisted workflow, not an existing automatic clone button in the editor. |

Two mods changing different buttons in the same parent still replace one identical game path. Their small semantic scopes do not make the deployed binaries compose.

At the reviewed historical [1800 loader revision](https://github.com/jakobharder/anno-mod-loader/tree/8326b7c5a7648787c52f1252cd6e8ae60e593d1c), `libs/external-file-loader/src/mod_manager.cc` (`IsPatchableFile`, lines 660-666) distinguishes patchable `.xml` from whole-file resource replacements. `libs/xml-operations/src/xml_auto_serializer.cc` (lines 26-36, 58-72) has FileDB/FC/XML handlers, with no Phoenix scene/widget handler. The historical source is not a claim about byte-identical current integrated engine internals, but it supplies no basis for advertising Phoenix ModOps patches. Appending `.xml` to an opaque binary patch does not add a missing serializer.

Possible **editor improvements**, not implemented or authorized as a source rewrite in this review:

- Show every consumer before editing a shared widget and offer a private copy for one selected instance, preserving its properties/events and remapping the parent reference.
- Record semantic changes by instance UUID plus field/property path, with source hashes/original-value preconditions and conflict detection.
- Combine several compatible change sets during a build, then encode one shared output binary. This can help a combined project or compatibility mod.

An editor-side change-set format alone cannot make separately installed ordinary binary-replacement mods merge on an end user's machine. That needs a common composition/build step or a Phoenix-aware loader extension. A binary diff also needs an applicator. No loader extension or editor implementation was made here.

## Button behavior and multiplayer boundary

The editor's event/data-binding vocabulary includes assigning supported properties, event-to-Boolean conversions and supported animation/video actions. Native pause/confirmation widget inspection found `EventToTrue`, `EventToFalse`, conditional assignments, Boolean inversion and existing menu event wiring. This supports inspecting/reusing existing UI control behavior; it does not establish every possible new binding's runtime validity or a universal callable game API.

**The earlier Lua limitation is specific to arbitrary newly authored Phoenix controls.** Existing asset-configured popup and notification command hooks must not be ruled out by that statement. They are distinct integration mechanisms, and a custom Phoenix button does not gain them merely by declaring an Action or a property named Command.

A click is not automatically a broadcast of the same UI event to every client. Distinguish the local UI event, its handler and any game command that handler submits. The [existing multiplayer evidence](../multiplayer/synchronization.md) and Serp's [command-hook observations](https://github.com/anno-mods/modding-guide/blob/main/Scripting/Lua_Probleme.md) report client-local button-command entry points, synchronized game commands, and commands requiring synchronized execution separately. Those are author observations under their stated conditions, not new multiplayer tests of Toolbox output.

Serp's notebook (HowTo.xml:2619-2652; summarized in [personal evidence](../reference/personal-test-evidence.md)) specifically reports ConditionGUIEvent firing for the invoking client and a tested Coop unlock flow desyncing. Thus detecting a UI event through a trigger is not a generally safe synchronization bridge either.

Pure visual/local menu work does not by itself establish shared simulation changes. For a gameplay button, inspect the exact command's synchronization, participant/peer scope, target/session context, repeated submission behavior and trigger lifecycle. Identical mod files on both clients are not proof that the callback executes consistently. No general MP-safe claim, new synchronization wrapper, generated-UI game test or multiplayer test is supplied by this review.

### Existing native command hooks: completed bounded audit

The current native XML audit read asset **500115** (`GenericPopupConfig`, template `GenericPopup`, no base), its template membership (`Standard` + `GenericPopup`), corresponding complete property definition/defaults and `GenericPopup` dataset. `GenericPopup/Popups` is a dataset-bound Array; its button list is a Vector with `Text`, `Command` String and embedded `Actions` (AutoCreateAsset restricted to template `Actions`). Defaults include `Actions/Values/ActionList`. The fixed popup dataset does not establish arbitrary new popup enum registration.

- `Popups/Quit/Buttons/Item/Command` contains `GameManager.fastQuit(2)`: a concrete existing Lua command hook, not a Phoenix-editor-generated callback.
- `Popups/CampaignReadLetter` has a button action `ActionTriggerTextPopup` with `PopupText=10521`; `TutorialHappiness` uses `ActionNotification`. These are native embedded-action structures, not proof that every game action or every MP context is supported.
- The public Serp popup helper (`Anno-1800-Mods/WorkInProgress-Mods/shared_PopUp/data/config/export/main/asset/assets.xml`) locally inspected at lines 96-136 replaces `ResetConsoleOptionsConfirmation` and uses `pcall(g_shared_PopUp_Serp.ButtonHit,1)` through `3`. This is a WIP reuse of an existing popup type with its own queue/Coop limitations; do not present it as a completed generic callback framework.

For notification hooks, the audit read the `CharacterNotification/ThirdpartyNotificationButtons` definition: `Command` String, and `ActiveCallback` explicitly a Boolean Textsource statement. Native reporter assets **91** (`Profile_Virtual_NeverOwnsObjects`, no base) and **162** (`PaMSy_Archetype_Editor`, base 121 -> `PaMSy_MASTER_Template_Archetype` / `PaMSy_Base`) contain a `CharacterNotification` under `ParticipantMessages/MessageTriggers/NewspaperCreated/Reactions`. Its button command is `[Newspaper ShowLatestNewspaperUI()]`. This is a concrete existing non-Lua UI operation. The existing author reports distinguish these Textsource commands from popup Lua commands and qualify selection-context restrictions.

Source locations: native `properties-toolone.xml` around 40485-40590 for GenericPopup and 30496 onward for notification buttons, plus owning assets/templates/defaults/dataset as above. The parser/schema evidence establishes hook shapes; the [author's locality/synchronization observations](https://github.com/anno-mods/modding-guide/blob/main/Scripting/Lua_Probleme.md) establish the reported test context. No new action implementation, popup allocation, PHX callback bridge, in-game or MP test is claimed.
