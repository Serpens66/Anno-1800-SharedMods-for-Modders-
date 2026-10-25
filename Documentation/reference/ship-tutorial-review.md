# Ship tutorial: complete text/code review

## Reading scope

All 1,533 lines of [Tutorial 4](https://github.com/anno-mods/modding-guide/blob/9afc5adb6271e02282532931cf4291b9a5059268/hier0nimus-tutorials/04-making-new-ship/readme.md) were read, including the complete original and final XML, progressive changes and late Blender corrections. Screenshots, linked tools/videos and native TradeShip/shipyard/graphics contracts have separate review status. This is an evidence map for that audit, not a certified ship recipe.

The source uses cargo ship 1010062, named internally Collier (Trade), as the copied example. It inserts a separate TradeShip before it, using author-owned identities 1742008813 (ship), 8814 (description) and 8815 (trigger). Sibling position does not provide asset inheritance. The first copied skeleton still contains the original GUID; that intermediate fragment must not be deployed before replacing its identity.

## Connections that must be reviewed together

| Part | Exact source configuration | Audit purpose |
| --- | --- | --- |
| TradeShip | New Standard identity; Object/Variations/Item/Filename | Bind gameplay asset to its new CFG |
| Walking | Water planner, dimensions, speed, turn, cargo/wind factors | Match navigation behavior to model size |
| Mesh | OnWaterSlope | Retained placement behavior |
| CommandQueue | FormationPriority 1, TradeShipPoints 2, PriorityShipList 2 | Preserve distinct command-list meanings; do not infer their units |
| Attackable | 1500 HP, self-heal 1.2, pause 30000 | Verify damage/heal time units and conditions |
| ItemContainer | One socket, two slots, Ship;SteamShip;Tradeship allocation | Separate item sockets from cargo slots and per-slot capacity |
| Cost | Timber/beams/motors five each; TradeShip influence point 1 | Materials and influence are distinct requirements |
| Craftable | CraftingTime 180000 | Source claims milliseconds, unlike FactoryBase's seconds |
| ExpeditionAttribute | BaseMorale 35, Navigation 10, trade/steam perks 1 | Retain expedition-facing properties |
| ShipMaintenance | Maintenance 125 | Separate running upkeep from build cost |
| Sellable | Baseprice Item inherits template index 0, Amount 125000 | Resolve native vector inheritance and currency identity |
| Steam shipyard | 1010521; AssemblyOptions/Item[Vehicle='1010062'] | Add new Vehicle before the cargo ship option |
| Item target pool | 193982, all tradeships NEW | Register specialist targeting; this is not all ship logic |
| Trigger | ConditionPlayerCounter, PopulationByLevel, context 15000003, amount 500 | Unhide and unlock the new ship |

The original example also carries minimap/strategic tokens, sounds, command barks, selection actions, drifting, TradeRouteVehicle, Nameable, MetaPersistent, Stance, Rentable, WorldMapSound, Pausable and ShipIncident. The guide mostly retains them without explaining their effective contracts. A shorter new-ship recipe must explicitly audit any omitted property or changed template.

## Important distinctions and corrections

- The guide's shipyard and target-pool patches use different Item fields: Vehicle for AssemblyOptions, GUID for EffectTargetGUIDs. They cannot be interchanged because both containers happen to use Item.
- ItemEffectTargetPool membership establishes an effect-target reference. The guide describes this as inclusion in trade-ship logic broadly; it does not prove registration in every trade route, AI, expedition, ship-name, statistics or session-transfer consumer.
- The trigger is unhide **and** unlock in one action. Its claim of matching steam-shipyard availability at 500 Engineers still requires the complete native shipyard unlock contract, other gates and the insertion group/setup audit.
- `Type="addnextSibling"` appears in the guide. The inspected 1800 Type parser uses `stricmp`, so the different capitalization of that operation name is accepted there. This does **not** make XPath element names, game property names or every XML attribute case-insensitive. Documentation examples use the canonical `addNextSibling` spelling.
- A progressive Text snippet is `<Text>Small Cargo Ship</Text>`; the final asset uses Text/LocaText/English/Text with status and a retained LineID 14859. These are not equivalent asset-property payloads. Audit localization and choose deliberately whether to keep a vanilla LineID; a custom identity alone does not justify blindly copying it.
- The five-second construction setting (`5000`) and original collier CFG/icon are temporary troubleshooting substitutions. The final example restores CraftingTime 180000 and the custom paths. Do not leave the temporary time in a balanced release.
- The source mentions a cargo-slot UI limit but does not identify a verified numeric maximum. It does not establish that every ItemContainer with extra slots has corresponding UI support or capacity behavior.
- CraftingTime, SelfHealPausedTimeIfAttacked, Walking speed and ship upkeep must each be checked in their own native schema. A number with the same magnitude or a time-like name is not a shared unit contract.
- The tutorial's GUID sequence says the previous example ended at 8812, although Tutorial 3's listed identities end at 8810. This is author allocation history, not permission to reuse supposedly skipped identities.

## Model, texture and export procedure described

The source uses rdm4, texconv, AnnoFCConverter and the old xormenter Blender CFG add-on. It configures a merged extracted-data root and executable paths, imports collier.cfg, edits MODEL objects and exports the model separately from MAIN_FILE. The old add-on is now discontinued; current tool instructions must identify the actual add-on/version, not mix its panel names with the successor's UI.

The two export stages have different responsibilities. Exporting the MODEL writes geometry; MAIN_FILE export writes CFG and associated resource references. The source explicitly checks the exported RDM FileName in the Anno Object panel. Renaming the Blender object is not by itself proof that the CFG now references a packaged new RDM.

The source shortens geometry, removes lifeboats/flag posts, retargets diffuse textures and repositions lamps, smoke, waves, damage/fire dummies and bounds. It distinguishes BoundingBox, MeshBoundingBox and IntersectBox. Those are separate boxes; changing navigation reservation dimensions alone does not update their exported graphics data.

It supplies diffuse variants at 1280,640,320,160,80 square pixels. These are the example's five texture levels, not universal image-size requirements. It retains original metallic/normal/mask textures. UV changes and remaining original maps must be checked for visible mismatches; changing the diffuse color does not automatically regenerate normal or metallic information.

## Late corrections must override the intermediate instructions

The guide first deletes one PROPCONTAINER and later discovers that both original state containers are needed. Its final correction restores the original containers, moves new cargo into the normal visibility container and keeps floating boards for the destroyed state. The VISIBILITY_TRANSFORM/state configuration matters; a generic newly created prop container does not necessarily reproduce it.

The author reports that changing each added ship prop's Flags from 1 to 0 made cargo visible, while explicitly saying the underlying height/relative-coordinate logic is unknown. Preserve this as an **author observation for this example**, not a general Flags bit definition or a universal instruction for building props. Native CFG, converter/add-on implementation and the relevant flags must be inspected before generalizing.

The guide also changes its destruction-model plan: it initially reuses the original destruct model, then ultimately deletes it and accepts explosion/smoke visuals. These are alternative final design choices. Keeping an original unshortened destruction model can visibly disagree with the new hull; deleting it still requires checking animation/model references.

## Remaining audit tasks

Read and trace native cargo ship 1010062, TradeShip template/defaults, Walking, ItemContainer, Craftable, ShipMaintenance, Sellable, Cost, Attackable, CommandQueue and all changed fields. Audit the complete shipyard 1010521 and its effective assembly/unlock rules, target pool 193982 and item consumers, trigger group/defaults, current collier CFG/IFO/FC/RDM/material/prop/animation resources and converter/add-on coordinate/flag/export behavior. Inspect all source screenshots and any packaged example or record a specific access limitation.

Check all selections and identities offline after the audit. Lua syntax/XML structure checks cannot establish navigability, cargo UI, expedition suitability, session transfer, destruction visuals, multiplayer synchronization or save behavior. No new game or multiplayer tests are performed for this documentation.
