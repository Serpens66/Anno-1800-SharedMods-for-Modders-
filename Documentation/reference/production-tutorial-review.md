# Production tutorial: complete text/code review

## Scope and provenance

All 2,959 lines of Tutorial 3's README, including every progressive/final XML fragment, have been read at modding-guide commit `9afc5adb6271e02282532931cf4291b9a5059268`. Its linked images, video, external asset browser and packaged mod are separate sources; reading the README does not certify those sources or the entire production feature audit.

Source: [Making a new production chain](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/hier0nimus-tutorials/03-making-new-production-chain/readme.md). The following inventory of responsibilities retains the author's example identities for source navigation. All `17420088xx` identities belong to that author; new mods must allocate their own identities.

## The complete dependency structure illustrated

The tutorial creates a Product (8803), description (8804), ProductionChain (8805), chain description (8806), FactoryBuilding7 (8807), building description (8808), unhide Trigger (8809) and unlock Trigger (8810). It supplies localization and a product icon, reuses the marquetry workshop model and later redirects two diffuse textures to mod-specific resources.

It also patches these consumers, which are independent of defining a Product:

| Consumer | Tutorial reference and selection | Purpose claimed by the tutorial |
| --- | --- | --- |
| Storage lists | 120055,120057; Values/ProductStorageList/ProductList | Register product for standard storage and Moderate marketplace |
| Product lists | 501997,502019,502006,7398,501995,501996,501992; Values/ProductList/List | Consumption, workforce, unlock and luxury list membership |
| Item target pools | 190914,6000018,193875,193856,25599; Values/ItemEffectTargetPool/EffectTargetGUIDs | Let existing specialist effects target the new building |
| Construction categories | 25000191,500945; BuildingList/Item[Building='500008'] | Show the chain after canned food in tier/function menus |
| Population input lists | 15000000,15000001,15000002,5403 | Create the actual Farmers/Workers/Artisans/Artistas need |
| Workforce menu | 25000087; Values/WorkforceMenu/BoostableFactories | Register adjustable working conditions |
| Trigger group insertion | Anchor 130248 | Unhide at one Artisan, unlock at 500 Artisans |

The tutorial correctly distinguishes ProductList membership from the actual PopulationInputs configuration. Native ProductList's Product field can reference either Product or ProductList; therefore nested aggregate lists exist. Every consumer still needs verification against the chosen data revision and already-patched document. A list name is not a complete proof of its consumers.

Sibling insertion selects an existing Item, not its enclosing list. An absent anchor prevents insertion. For example, selecting Item[Product='1010216'] after proving that schnapps occurs in both storage lists is structurally different from adding a sibling to ProductList itself. The latter would put Item at the wrong level.

## Property findings verified in dataAlle

The complete native FactoryBase, Factory7, Maintenance, Product, Transporter7, LogisticNode, Industrializable, Electrifiable, ProductStorageList, ProductList, ProductionChain, Locked and PopulationLevel7 schemas were read, together with their relevant defaults, the corresponding templates and selected native reference assets. This is a property-level review; pending consumer/feature audits below must still be completed before treating the entire tutorial as a certified new-mod recipe.

- FactoryBase uses input/output vectors. Each entry identifies a product, a per-cycle Amount and a StorageAmount. CycleTime is measured in seconds. The schema describes storage separately from goods currently inside the production cycle. These values are not the island's total storage capacity.
- The native FactoryBuilding7 template has no BaseAssetGUID inheritance chain. It supplies a Factory building type, Production selection UI, ConsumerPriority 1, manual pause capability and other property overrides. Creating a sibling after marquetry workshop 1010320 does **not** inherit that workshop's contents: the tutorial explicitly writes the chosen values into a separate full asset.
- LogisticNode defaults to FactoryTransporter 1010104, one transporter, ten parallel queue slots, loading/unloading modifiers 1 and Street path layer. Transporter 1010104 uses Transporter7 defaults. Electric factory/warehouse transporters 120028/120027 explicitly set loading/unloading times 2, speed 1.4 and their electric feedback types. TrainTransporter 120025 uses capacity 200, speed 2.5 and a wagon threshold of 20. These are distinct configuration contracts.
- Electrifiable's supplied ElectricityBoost is 1, with zero described as neutral. Industrializable defaults to BoostedByIndustrialization 1 and receiving type Powerplant, referencing the electric transporters. Empty property tags retain defaults; they are not literal Boolean values of 1 by themselves.
- The native Region dataset also includes Meta, Mod1, Mod2 and Mod3. The tutorial's four familiar regions are a useful example subset, not the full dataset.
- The native StorageLevel dataset includes Meta as well as Area and Building. ProductCategory is a Text field, not a named ProductCategory dataset. The example's 11705 is a text reference.
- ProductionChain contains its root Building and nested Tier1/Tier2/Tier3 vectors. These four levels describe the UI chain; they do not create FactoryInputs or simulate a new supply relationship.
- Locked's general default is DefaultLockedState 1 and Participant scope, but templates can override it. ResidenceBuilding, for example, supplies DefaultLockedState 0; engineer residence 1010346 explicitly overrides it to 1. Never generalize the tutorial's locked examples to all templates.
- AdditionalGlobalUnlockRequirement's native description says the selected population threshold must be reached globally once and is not revoked merely by later population decline. It is separate from a need's local NoWeightPopulationCount and from unlocking the Product GUID.
- The native engineer population 15000003 references DefaultResidence 1010346, which references that population and has ResidentMax 40. Bonus-needs, floor requirements and excluded population are explicitly present; their calculations must not be flattened into one unchecked resident formula.

The full Production Output Goods InfoTip 25000208 was read from export.xml. It distinguishes selected-object Logistic storage from selected-area Economy storage, evaluates FreeSpace, and checks TeleportsProducedGoodsDirectlyIntoAreaStorage/NoWarehouseInRange for a warning. Its RefGuid means the product being displayed, not automatically the selected building's GUID. This explains why a visible stock number is not necessarily factory storage; the actual branch/context matters.

## Corrections and limits in the example

1. **Consumption/income units:** use **MoneyValue as income per 100 inhabitants per minute**, following Serp's explicit decision and the guide's resident-based calculation. Serp explains that the property-comment authors are German non-native English speakers and is very confident that "residences" was used for inhabitants here. This is user-provided language context and an interpretation decision, not an independently verified engine calculation or game test. Retain the original property wording for traceability. For Amount, Serp considers the guide's explanation correct; the conflicting full-house wording and remaining runtime calculation boundary stay visible. See [decision register](discrepancies.md#q004-population-consumption-and-income-units).
2. **Storage numbers change between fragments:** explanatory text uses six input tons and ten output tons; some progressive/final fragments use six for both, while another uses ten for both. These are different example settings, not engine-derived constants.
3. **Hit points differ:** prose chooses 3000, while the progressive/final XML writes MaximumHitPoints 3500. The actual supplied XML determines the example's value.
4. **Path typo:** the ItemEffectTargetPool prose writes `/Value/...`; its actual ModOp correctly uses `/Values/...`. Use the latter after checking the asset's real structure.
5. **Output limit:** the guide says output is limited to one product. FactoryOutputs is nevertheless a vector in the native schema; the current top-level asset scan found no asset with more than one explicitly serialized FactoryOutputs/Item. That absence does not prove multi-output runtime support or disprove the limit. Use a single ordinary output in this tutorial; separately configured FactoryUpgrade/AdditionalOutput is a different mechanism.
6. **Warehouse range:** the guide links reachability to CycleTime and StorageAmount. No exact numeric formula or universal example range has been established from engine code. Do not claim that a particular storage/cycle ratio guarantees a number of tiles.
7. **Docklands:** the source describes IsMainFactory as the factory selected for export-value calculation and lists possible inputs to that calculation. The precise native balancing contract and relevant export references are still pending. Do not present the guide's prose as a verified complete formula.
8. **Graphics explanations:** the tutorial calls the normal map smoothness/gloss and describes metallic/mask behavior broadly. Channel and shader-specific behavior must be reconciled with the dedicated graphics guides, converter implementation and native materials; these simplified descriptions are not selected as authoritative material contracts.
9. **Metadata:** its JSON examples are fenced as XML and use historical CreatorName. They are metadata examples, not valid XML snippets; use the reviewed current metadata/tool contract instead.
10. **Archives and software:** data2.rda/data8.rda are historical extraction examples. Use the current merged dataAlle paths and verify actual file availability. Do not promise Windows 3D Viewer is preinstalled on every machine.

The complete building example retains incident/sound/feedback/culture/quest/ecosystem properties copied from the chosen workshop. Their presence is not proof that a shortened building asset with only FactoryBase is a usable replacement. Likewise, deleting copied resources is safe only after every retained CFG/FC/IFO reference is traced; keeping original model paths can intentionally reuse vanilla resources.

## Remaining feature audit and validation tasks

Complete native storage/list consumers, construction-category variants, production-chain roots, population modifiers/defaults, working-conditions balancing, item-pool references, unlock trigger group/setup/default scope and the complete workshop CFG/IFO/FC/resource chain. Read the packaged tutorial mod and images and compare its final implementation with the README. Resolve the dedicated graphics discrepancies from primary material/tool evidence, then ask Serp if a true conflict remains.

Offline validation must check each consumer XPath against the current native and patched state; validate selected list anchors in every target, detect duplicate identities/list entries and retain the intended locked/unhidden states. An XML parse alone cannot validate production, consumption, logistics, DLC availability or save/MP effects. No game tests are performed as part of this documentation work.
