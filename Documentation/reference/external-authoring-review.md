# External authoring sources: findings and limits

This register separates a completed reading of source files from the native feature audit required before adopting their game behavior. It is not an executable recipe.

## AddCustomMusic

Original: [anno-mods/AddCustomMusic](https://github.com/anno-mods/AddCustomMusic), commit `d4b5b3d66c22b7ba3c65f8c86d1f296841da378d`, dated 2026-09-06; retrieved 2026-10-03. All Markdown, XML and Lua files have been read, including the complete soundbank catalog.

The repository contains fragments from Return to the Orient, rather than a packaged standalone mod. Its own session GUID, asset GUIDs, script paths and Wwise event IDs are examples belonging to that integration. Allocate replacements and audit the actual target session before reuse.

The source expresses these connections:

| Component | Source connection |
| --- | --- |
| Bank asset `1404000853` | Wwise bank ID `626769978`; added to RequiredSoundBanks of four named GUIDs and optionally `133700001` |
| Start audio `1404000854` | Wwise event `65769146` |
| Stop audio `1404000857` | Wwise event `467769552` |
| Enter trigger `1404000856` | Executes `data/script/music/region_check.lua` on SessionEnter and resets itself |
| Leave trigger `1404000855` | Plays stop audio on SessionLeave and resets itself |
| Explicit start trigger `1404000858` | Active-session condition `1404000000`; AutoRegisterTrigger is zero |
| Gate `1404000859` | Separate UnlockableAsset; region_check requires it to be unlocked before registering the start trigger |
| Startup trigger `1404000860` | Installs exit-to-menu Lua event handler |

Two integration gaps are directly visible without making assumptions about the game:

- `XML/assets__index.xml` includes audio, soundbanks and the gate, but **does not include `assets_music_triggers.xml`**. A containing mod must include those triggers separately; this repository does not demonstrate that containing entry point.
- The supplied files contain no action unlocking gate `1404000859`. Its effective default and the containing mod's unlock path require inspection before deciding when music begins.

The exit handler checks `event.OnLeaveUIState["ReturntoOrient"]`, but writes `event.OnLeaveUIState[ModID]` with `ModID="test"`. These are different keys. The guard therefore does not test whether its own handler is installed; reuse also risks overwriting another handler using `test`. The callback is wrapped in `pcall`, consistent with Serp's documented event-callback error handling. UI IDs 63, 170 and 171 are comments from this example, not a complete native lifecycle contract.

The catalog numbers describe **Wwise IDs**, not GUID allocations for new Standard/GUID assets. Several exceed signed 32-bit asset ranges. Do not apply the asset GUID allocator to this different namespace. Catalog descriptions are author summaries; event-name lists do not prove every event is appropriate in every game context.

The README links a Wwise video tutorial. That video has not yet been evaluated. Bank generation/version compatibility, exact session-local sound execution, all relevant native templates/defaults, RequiredSoundBanks reference chains and main-menu lifetime remain separate audit tasks. No audio or multiplayer run has been performed.

## Historical iModYourAnno authoring workflow

Original: [iModYourAnno wiki](https://github.com/anno-mods/iModYourAnno/wiki), commit `7c30b533f475d35cab35654888a3e076e8950378`, dated 2023-05-03; retrieved 2026-10-03. All three wiki pages have been read. These are tool-level instructions, not proof that the integrated loader implements every Imya-prefixed attribute.

The tweaking page explains a preprocessing workflow: selected ModOps are copied into `<filename>.imyatweak.include.xml`, edited there, and the original operation is skipped while an Include is appended. Saved tweaks are described as residing under `.imya/tweaks`. Therefore inspect the generated patch and its new ordering, rather than assuming the exposed original operation executes at its original position.

| Authoring feature | Meaning in the wiki |
| --- | --- |
| ModOp ID | Associates operations belonging to a tweak |
| Expose ID | Stable setting identifier across updates; preserve uniqueness |
| ImyaExposePath | XPath relative to the operation payload, including examples using `self::Text/Text` and `self::Amount` |
| Description | Explanation displayed by the authoring tool |
| Enum | Fixed values offered as choices |
| Slider | Default, minimum, maximum and stepping |
| Toggle | Original XML versus alternate XML; alternate payload still needs game validation |
| ImyaTweaksTitle | Tool-facing title |

Its arbitrary toggle tags illustrate replacement behavior and are not valid game properties merely because they appear in the wiki. The application implementation and generated-file compatibility have not yet been reviewed; do not offer this historical workflow as a verified current tool recommendation.

The GitHub integration page describes a package as repository owner, repository name and a download regex. It selects the first matching ZIP release asset from the latest release. Package publication is described in [anno-mods/Packages](https://github.com/anno-mods/Packages); that linked registry remains to be evaluated. This release download mechanism belongs to the external application and must not be attributed to the integrated game loader.

## First-mod tutorial

The complete text and XML/JSON examples of [Tutorial 1](https://github.com/anno-mods/modding-guide/tree/main/hier0nimus-tutorials/01-my-first-mod) have been read at the guide revision in [sources](sources.md). Screenshot review and its linked asset-browser implementation remain separate.

Its central patch replaces the existing Feras productivity Value at GUID `192450`, `/Values/FactoryUpgrade/ProductivityUpgrade/Value`, from 50 to 420. This is a whole selected-node replacement; the enclosing Percental flag is retained by that narrow selection. This tutorial is not yet an audited item recipe in this knowledge base: target-pool and upgrade contracts must be completed first.

Editorial/version cautions: the displayed metadata is JSON despite an XML code-fence label; `CreatorName` belongs to the older metadata examples and differs from later `Creator` consumers; the archive list and archive number are dated rather than universal. The distinction between extracted research files and the game's loaded archives is sound. A statement that extracted archive content can never be repacked is too broad; the documented mod workflow uses loader patches, while archive tooling is a separate subject.

## New-specialist tutorial

The complete 1,823-line text and every embedded XML/JSON example of [Tutorial 2](https://github.com/anno-mods/modding-guide/tree/main/hier0nimus-tutorials/02-making-new-specialists) have been read. Images, associated packaged mod files and the full native item/upgrade/acquisition audit remain separate tasks.

The example builds Maria Lopez as a GuildhouseItem, gives it a separate description text, targets gold mine `101311`, adds productivity and periodic iron output, expedition attributes, increased workforce, two pool entries and a population-counter unlock trigger. The tutorial also surveys residence, maintenance, culture, heating, irrigation, powerplant, incidents and trading-post upgrades. These surveys contain context-sensitive claims; they must not become validated recipes merely through transcription.

Source-specific cautions:

- The prose initially chooses **1,000 Obreros**, later prose and the final trigger choose **500**. This is an editorial design change; the final displayed CounterAmount is 500. Preserve that fact instead of claiming a universal progression threshold.
- One intermediate pool patch switches from `192737,193089` to six different GUIDs; the final combined patch returns to two. Review the actual packaged version and all pool consumers before assigning acquisition channels. A pool name alone does not prove a research/visitor/quest route.
- The final new-item example says it will lock the item, but contains **no Locked property override**. Whether the effective default implements that intention requires template/default inspection.
- A statement that self-closing properties do nothing conflicts with the general role of defaults and inheritance. Empty XML spelling alone is not a runtime no-op guarantee; see [inheritance](../foundations/inheritance.md).
- A statement that item-provided industrialization powers everything within the trade-union radius leaves out its explicit ItemEffect target filter. Resolve the full native effect contract before explaining coverage.
- One text example changes the intended name to `Item Template`; do not copy that placeholder as the specialist's fallback label.
- The powerplant range example omits Percental while its explanation calls the increase a percentage. Inspect the UpgradeValue default and native examples before choosing units.
- ResidentsUpgrade is described with explicit uncertainty. Its presence in a schema does not establish that a current consumer applies it.
- The tutorial gives several nested-pool and effect-pool examples. Duplicate inclusion is a graph issue; do not flatten or duplicate entries without following the actual chain and weighting.

These issues are recorded as source findings, not new game test results. Complete the native audits before deciding any unresolved semantic disagreement or asking Serp to choose between supported alternatives.

## Original-source access status

The original Pnski/Anno1800ModDoku GitHub page can be read through the web tool, but two direct Git clone attempts returned Repository not found. This does **not** justify excluding the API catalog as unavailable: continue through readable original GitHub file pages or original raw content. A cached page's age must remain visible when newer revision provenance cannot be established.

The current [vscode-anno repository](https://github.com/anno-mods/vscode-anno) was retrieved at `19cda8edc73d65a622c9c5c588953a0170c337c6` (2026-09-24). All 12 documentation Markdown pages have been read; implementation, screenshots and recursive example links remain under review. Its Anno 117 and 1800 instructions must be separated. The installed extension used for offline tests is version 2.3.1 and must not silently inherit every capability of this newer repository.

## Tutorial 0: snippet catalog

All 1,012 lines of [the tutorial's documentation catalog](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/hier0nimus-tutorials/00-documentation/readme.md) were read: archives, languages, ModOp names, item templates/settings/upgrades, expedition attributes, DLC references, asset pools, building settings, participant portraits, sounds, costs, maintenance and industrialization. This is a catalog of snippets and example subsets, not a complete specification. Its unfinished Building templates and RewardPool sections explicitly contain ellipses.

Source-specific findings:

- Archive listings end at data28; this is a historical subset, not a complete current extraction order. Later examples elsewhere use newer data archives.
- The language list omits filenames present in other examples, including Brazilian and Portuguese. Verify the actual target localization files rather than treating this list as exhaustive.
- ItemType lists only Specialist and Normal; the audited native ItemType dataset also includes Animal and None. Likewise, Allocation/ExclusiveGroup/region/participant lists are examples to cross-check against their actual named datasets.
- The catalog calls MaxStackSize's standard value 1. The native Item schema says 0 means unlimited while ItemContainer's limit still applies; properties.xml's Item default entry does not explicitly serialize MaxStackSize, and the inspected GuildhouseItem/TownhallItem/VehicleItem templates do not override it. These findings do not expose an implicit engine default. Document the distinction and inspect native examples/consumer behavior before promising either an omitted value of 1 or unlimited stacking.
- The catalog describes ScenarioFilter 650 as the only value for Eden Burning. The native schema defines an asset reference requiring ScenarioMetaInfo, and the explicit property default is 0. Treat 650 as that example's scenario reference, not an enum with only one permitted nonzero value.
- Native GuildhouseItem supplies Allocation GuildHouse, ItemAction SelfRadius, CanEndItemAction 0 and ExpeditionAttribute BaseMorale 5; TownhallItem supplies corresponding TownHall allocation/action values; VehicleItem supplies Ship allocation and BaseMorale 5. Item's general Allocation default is RadiusBuilding. These template overrides matter when shortening a new item.
- GuildhouseItem includes Locked in its property composition. Consequently, Tutorial 2's missing explicit Locked element cannot by itself establish an unlocked item: its effective defaults must be resolved. General Locked defaults are recorded in the inheritance audit.
- The snippet catalog demonstrates flat and Percental upgrade shapes, periodic outputs, input replacement, target lists, residence need substitution/consumption, incident effects, population benefit modifiers, trade protections/generation, heating, powerplant and irrigation. The presence of an XML field is not proof of an active runtime consumer. Each subsystem's target filters, defaults and units remain subject to its native audit.
- A final industrialization snippet sets BoostedByIndustrialization 1 and describes a 100% boost. Native Industrializable defines eligibility and transporter/type settings; Electrifiable separately provides ElectricityBoost. Do not infer an arbitrary boost amount from that Boolean alone.

The complete portrait list includes duplicate entries (for example Africa_Blake and Third_enemy_01_Grant). It is a useful search aid; duplicated lines do not create different participant identities. Separate the configured selection archetype from the owner participant, local peer or Coop role.

The catalog does not provide complete assets, acquisition consumers, list registration, trigger setup or graphics dependencies for every snippet. Its data-backed settings will be transferred into the relevant gameplay chapters only after the feature audits, with source labels preserved.

## Historical Schwubbe blog

The [blog](https://schwubbe.de/modding_blog.php) was read through its final Substance Painter section on 2026-10-03. It covers historical installation, asset research, properties, inheritance, factories, triggers and graphics. Installation-era external-loader/Python instructions are historical. Claims that 1800 lacks datasets and that converters cannot handle animations are superseded by the locally inspected data and newer tools. Its early factory examples use FactoryBuilding while their explanation and final example use FactoryBuilding7; its trigger skeleton has mismatched closing tags. These examples need correction and native audits before reuse. Linked forums, downloadable shader/templates and converter details remain separate sources. Its coordinate-conversion advice must be checked against the actual converter; manually swapping axes after an automatic conversion can apply the transformation twice.
