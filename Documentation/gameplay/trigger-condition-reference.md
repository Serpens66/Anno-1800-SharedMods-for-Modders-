# Native condition and trigger contract lookup

Generated from the local Anno 1800 dataAlle revision by `Documentation/tools/build_trigger_reference.py`. Read [trigger design](triggers.md), [condition selection and pitfalls](trigger-conditions.md), and the [audit outcome](../reference/trigger-audit.md) first.

**Evidence:** schema and serialized defaults, not engine implementation or a game test. The 91 entries below are templates with a direct `Condition` property. Related object selectors, quest objectives and schema-only properties are listed separately. Existence does not guarantee that a condition works in every trigger context.

Exact XML, authoring restrictions, complete datasets, SHA-256 hashes, example owners and base chains: [native contracts](../reference/triggers/vanilla.json). Missing explicit defaults stay unspecified here; do not interpret them as zero. Template overrides take precedence over property defaults. Container defaults describe list entries, not a request to insert that entry into an empty vector.

## Template index

Candidate intent below is summarized from native names, fields and sample contexts; it is not a guarantee of runtime support. See the selection chapter for tested exceptions.

| Template / candidate intent | Property blocks (exact names) | Explicit-template native examples (owner GUID, source line) |
| --- | --- | --- |
| `ConditionActiveRegion`: Presence in a session of a chosen region | [Condition](#condition), [ConditionActiveRegion](#conditionactiveregion) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionActiveSession`: Active-session presence / blacklist | [Condition](#condition), [ConditionActiveSession](#conditionactivesession) | 150746 (assets.xml:749853; Chapter000_Intro); 150810 (assets.xml:750145; CQ001_DynamiteFishingQuest) |
| `ConditionAlwaysFalse`: Never-satisfied gate | [Condition](#condition), [ConditionAlwaysFalse](#conditionalwaysfalse) | 150770 (assets.xml:759660; CQ172A_LockThemUp); 150621 (assets.xml:760286; CQ172B_OpenTheLetter) |
| `ConditionAlwaysTrue`: Unconditional gate | [Condition](#condition), [ConditionAlwaysTrue](#conditionalwaystrue) | 11468 (assets.xml:705276; TRIGGER Unlock ConstructionMenu Scene (Bugfix)); 150746 (assets.xml:749853; Chapter000_Intro) |
| `ConditionAreaClaimed`: Claimed status of a specified island | [Condition](#condition), [ConditionAreaClaimed](#conditionareaclaimed) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionAttractiveness`: Attractiveness type/value and scope | [Condition](#condition), [ConditionAttractiveness](#conditionattractiveness) | 114562 (assets.xml:2936511; DLC02 - Achievement06); 136971 (assets.xml:4174050; Player has NOT 1500Att Zoo Unlock) |
| `ConditionBuildingsInBlueprintmode`: Blueprint count for a building type | [Condition](#condition), [ConditionBuildingsInBlueprintmode](#conditionbuildingsinblueprintmode) | 7968 (assets.xml:845696; Blueprint FarmerResidence); 7970 (assets.xml:846065; Blueprint WarehouseLvl1) |
| `ConditionBurningObject`: Burning-object list | [Condition](#condition), [ConditionBurningObject](#conditionburningobject) | 400095 (assets.xml:2345790; Action_Achievement_What's That Smell) |
| `ConditionBusActivationNeedSaturation`: Need saturation across filtered objects | [Condition](#condition), [ObjectFilter](#objectfilter), [ConditionBusActivationNeedSaturation](#conditionbusactivationneedsaturation) | 132790 (assets.xml:4026724; Trigger Pre quest audio 2); 134573 (assets.xml:4027085; Trigger Pre quest audio 6) |
| `ConditionCameraMovement`: Tracked camera action/distance | [Condition](#condition), [ConditionCameraMovement](#conditioncameramovement) | 10000108 (assets.xml:2724296; SwitchAsset_Pan&Rotate_BeforeQuest) |
| `ConditionCorporationDifficulty`: Game-setup difficulty flags | [Condition](#condition), [ConditionCorporationDifficulty](#conditioncorporationdifficulty) | 151121 (assets.xml:801816; Fertilities); 151271 (assets.xml:802215; Island) |
| `ConditionDecision`: Player decision with an option list | [Condition](#condition), [ConditionDecision](#conditiondecision) | 119886 (assets.xml:3347446; LoLStory_FascinatingWest2); 119899 (assets.xml:3356261; LoLStory_TheOfficialMeeting) |
| `ConditionDecisionOption`: Decision option, actions, cost/unlock/UI behavior | [Condition](#condition), [ConditionDecisionOption](#conditiondecisionoption) | 119886 (assets.xml:3347446; LoLStory_FascinatingWest2); 119899 (assets.xml:3356261; LoLStory_TheOfficialMeeting) |
| `ConditionDiplomaticState`: Desired relationship state between participants | [Condition](#condition), [ConditionDiplomaticState](#conditiondiplomaticstate), [ConditionPropsNegatable](#conditionpropsnegatable) | 151441 (assets.xml:882161; TQ_WarDeclared); 152462 (assets.xml:925286; Making own moral - George Smith) |
| `ConditionDiplomaticStateChanged`: Diplomatic-state change / alliance count | [Condition](#condition), [ConditionDiplomaticStateChanged](#conditiondiplomaticstatechanged) | 400101 (assets.xml:2346008; Action_Achievement_World Peace) |
| `ConditionEvaluateTextSource`: Textsource evaluation (numeric runtime discrepancy) | [Condition](#condition), [ConditionEvaluateTextSource](#conditionevaluatetextsource), [ConditionPropsNegatable](#conditionpropsnegatable) | 103532 (assets.xml:4476686; CUT ---TutorialHint_DLC11_SB035_LoseTarget_DISABLED) |
| `ConditionEvent`: SimpleEventType listener with event-specific context | [Condition](#condition), [ConditionEvent](#conditionevent), [ConditionPropsNegatable](#conditionpropsnegatable) | 150810 (assets.xml:750145; CQ001_DynamiteFishingQuest); 8452 (assets.xml:750718; CQ001_DynamiteFishingQuest_CONSOLE) |
| `ConditionExpeditionFinished`: Finished expedition / morale comparison | [Condition](#condition), [ConditionExpeditionFinished](#conditionexpeditionfinished) | 400090 (assets.xml:2345744; Action_Achievement_On a Knife Edge) |
| `ConditionExportGoodsLeveled`: Docklands export level/count | [Condition](#condition), [ConditionExportGoodsLeveled](#conditionexportgoodsleveled) | 132391 (assets.xml:3954030; Trigger Pre quest audio 1); 132392 (assets.xml:3954126; Trigger Pre quest audio 2) |
| `ConditionFactoryProductivity`: Productivity of filtered factories | [Condition](#condition), [ConditionFactoryProductivity](#conditionfactoryproductivity), [ObjectFilter](#objectfilter) | 151274 (assets.xml:856139; Trees); 151247 (assets.xml:859522; Trade Routes) |
| `ConditionFestival`: Festival type and active/ended state | [Condition](#condition), [ConditionFestival](#conditionfestival) | 134255 (assets.xml:4060482; Trigger Queen Festival check end) |
| `ConditionFiniteResource`: Remaining finite-resource quantity/types | [Condition](#condition), [ConditionFiniteResource](#conditionfiniteresource) | 139176 (assets.xml:4960994; Trigger_Reaction_ResourceDepleted); 139175 (assets.xml:4961750; Trigger_Reaction_ResourceLow) |
| `ConditionFirstTimeEventHappened`: First-time event for an asset | [Condition](#condition), [ConditionFirstTimeEventHappened](#conditionfirsttimeeventhappened) | 400077 (assets.xml:2344837; Action_Achievement_Choo Choo) |
| `ConditionGUIEvent`: Local UI-state enter/leave listener | [Condition](#condition), [ConditionGUIEvent](#conditionguievent) | 10000135 (assets.xml:2724436; Trigger_QuickNavigationMapOpen); 10000136 (assets.xml:2724531; Trigger_QuickNavigationMapClose) |
| `ConditionGameEnded`: Win/lose state | [Condition](#condition), [ConditionGameEnded](#conditiongameended) | 400093 (assets.xml:2344772; Action_Achievement_Annoholic) |
| `ConditionGamePadAction`: Tracked gamepad action/count | [Condition](#condition), [ConditionGamePadAction](#conditiongamepadaction) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionHaciendaDecreesActive`: Selected active Hacienda decree flags | [Condition](#condition), [ConditionHaciendaDecreesActive](#conditionhaciendadecreesactive), [ObjectFilter](#objectfilter) | 26028 (assets.xml:4339383; DLC10Achievement04) |
| `ConditionHaciendaModuleCount`: Hacienda module count | [Condition](#condition), [ConditionHaciendaModuleCount](#conditionhaciendamodulecount) | 25851 (assets.xml:4339429; DLC10Achievement05) |
| `ConditionHappinessMood`: Population happiness mood for a participant | [Condition](#condition), [ConditionHappinessMood](#conditionhappinessmood) | 151041 (assets.xml:1169026; RQ_Farmers_FieldDig); 151042 (assets.xml:1169446; RQ_Farmers_ExtraGoods) |
| `ConditionInPalaceRange`: Any/all assets in palace range | [Condition](#condition), [ConditionInPalaceRange](#conditioninpalacerange) | 269322 (assets.xml:3125768; DLC04 Achievement02) |
| `ConditionInStorage`: Goods/items in filtered storage | [Condition](#condition), [ConditionInStorage](#conditioninstorage), [ObjectFilter](#objectfilter) | 124997 (assets.xml:3854898; Trigger LooseKontorORGoods FirstTime); 131058 (assets.xml:3855015; Trigger LooseKontorORGoods AllOtherTimes) |
| `ConditionIrrigatedModules`: Irrigated/non-irrigated farm modules | [Condition](#condition), [ConditionIrrigatedModules](#conditionirrigatedmodules), [ObjectFilter](#objectfilter) | 25486 (assets.xml:4289967; Trigger_Reaction_IrrigationMissingPaprika); 25595 (assets.xml:4290080; Trigger_Reaction_IrrigationMissingSugar) |
| `ConditionIrrigationCapacityExceeded`: Irrigation-capacity excess | [Condition](#condition), [ConditionIrrigationCapacityExceeded](#conditionirrigationcapacityexceeded) | 127909 (assets.xml:3859729; TutorialHint LoL 06 PumpOverCapacity 3DBuilding) |
| `ConditionIsBuffed`: Applied compatible buff count | [Condition](#condition), [ObjectFilter](#objectfilter), [ConditionIsBuffed](#conditionisbuffed), [ConditionPropsNegatable](#conditionpropsnegatable) | 269953 (assets.xml:3145155; TutorialTrigger BH Tractors Modules); 118946 (assets.xml:3145225; TutorialTrigger BH Tractors OilRunning1) |
| `ConditionIsCampaign`: Campaign mode | [ConditionPropsNegatable](#conditionpropsnegatable), [ConditionIsCampaign](#conditioniscampaign), [Condition](#condition) | 150559 (assets.xml:800519; InitCampaign); 151121 (assets.xml:801816; Fertilities) |
| `ConditionIsCraftingInProgress`: Crafting-in-progress state | [Condition](#condition), [ConditionIsCraftingInProgress](#conditioniscraftinginprogress) | 127940 (assets.xml:3863653; TutorialHint LoL 11 WorkforceSlider RCMenu) |
| `ConditionIsCreativeMode`: Creative mode | [ConditionPropsNegatable](#conditionpropsnegatable), [Condition](#condition), [ConditionIsCreativeMode](#conditioniscreativemode) | 140885 (assets.xml:705334; South America Discovery Expedition Unlock); 18585 (assets.xml:3849805; Trigger SessionSetup - Creative Mode) |
| `ConditionIsDLCActive`: Activation of listed DLC assets | [Condition](#condition), [ConditionIsDLCActive](#conditionisdlcactive), [ConditionPropsNegatable](#conditionpropsnegatable) | 130258 (assets.xml:669943; intermediate moderate 3.1.1 unhide pathways); 130259 (assets.xml:670082; intermediate moderate 3.2.1 unlock pathways) |
| `ConditionIsDiscovered`: Participant discovery through ParticipantRelation | [Condition](#condition), [ParticipantRelation](#participantrelation), [ConditionIsDiscovered](#conditionisdiscovered), [ConditionPropsNegatable](#conditionpropsnegatable) | 153231 (assets.xml:798628; AftermathComments_End_Trigger); 151276 (assets.xml:835214; Diplomacy Button LaFortune) |
| `ConditionIsDocklandsExportPyramidFull`: Docklands pyramid completion | [Condition](#condition), [ConditionIsDocklandsExportPyramidFull](#conditionisdocklandsexportpyramidfull) | 132122 (assets.xml:3960007; -- TutorialHint Docklands 16 Pyramid); 132196 (assets.xml:3962392; DLC07 Achievement03 (GoodPyramid)) |
| `ConditionIsGamepadMode`: Gamepad input mode | [Condition](#condition), [ConditionIsGamepadMode](#conditionisgamepadmode), [ConditionPropsNegatable](#conditionpropsnegatable) | 150810 (assets.xml:750145; CQ001_DynamiteFishingQuest); 8452 (assets.xml:750718; CQ001_DynamiteFishingQuest_CONSOLE) |
| `ConditionIsIndustrialized`: Industrialization amount/type or filtered objects | [Condition](#condition), [ConditionIsIndustrialized](#conditionisindustrialized), [ObjectFilter](#objectfilter) | 7738 (assets.xml:4886529; DLC12Achievement03) |
| `ConditionIsMultiplayer`: Multiplayer game mode, distinct from slot count | [Condition](#condition), [ConditionIsMultiplayer](#conditionismultiplayer), [ConditionPropsNegatable](#conditionpropsnegatable) | 10000108 (assets.xml:2724296; SwitchAsset_Pan&Rotate_BeforeQuest); 10000135 (assets.xml:2724436; Trigger_QuickNavigationMapOpen) |
| `ConditionIsParticipantInGame`: Participant selected in setup; not reliable live defeat detection | [Condition](#condition), [ConditionIsParticipantInGame](#conditionisparticipantingame), [ConditionPropsNegatable](#conditionpropsnegatable) | 151153 (assets.xml:1146747; Down with Anne Harlow 1 - Vicente); 137827 (assets.xml:1168785; FIX Trigger - Down with Anne Harlow (Da Silva) Cancel if no MoRE Anne is present) |
| `ConditionIsPaused`: Paused state of filtered buildings | [Condition](#condition), [ConditionIsPaused](#conditionispaused), [ObjectFilter](#objectfilter) | 105920 (assets.xml:4171230; DLC09_FixBarbecue_Quest); 136918 (assets.xml:4172087; Trigger Start Strike & Quest) |
| `ConditionIsTutorial`: Tutorial mode | [Condition](#condition), [ConditionIsTutorial](#conditionistutorial), [ConditionPropsNegatable](#conditionpropsnegatable) | 153287 (assets.xml:850439; Botanical Garden); 153288 (assets.xml:850943; Botanical Module) |
| `ConditionIslandsDiscovered`: Discovered-island count and scope | [Condition](#condition), [ConditionIslandsDiscovered](#conditionislandsdiscovered) | 10000050 (assets.xml:2722682; TSBConsole_QuickNavigationMap) |
| `ConditionIslandsWithFertility`: Owned-island count with a fertility / scope | [Condition](#condition), [ConditionIslandsWithFertility](#conditionislandswithfertility) | 133189 (assets.xml:880851; TQ_SettleNewIslandHops); 153303 (assets.xml:881313; TQ_SettleNewIslandPepper) |
| `ConditionMetagameLoaded`: Loaded metagame / human count | [Condition](#condition), [ConditionMetagameLoaded](#conditionmetagameloaded) | 400096 (assets.xml:2344730; Action_Achievement_Musketeers) |
| `ConditionModuleCount`: Absolute/percentage building-module amount | [Condition](#condition), [ObjectFilter](#objectfilter), [ConditionModuleCount](#conditionmodulecount) | 151176 (assets.xml:818517; Farmfields Potato); 151243 (assets.xml:818914; Enclosures Sheep) |
| `ConditionMonoCulture`: Monoculture delta comparison | [Condition](#condition), [ConditionMonoCulture](#conditionmonoculture) | 139555 (assets.xml:4961597; Trigger_Reaction_AgriAreaWarn); 139174 (assets.xml:4961673; Trigger_Reaction_Monoculture) |
| `ConditionMonumentEventActive`: Listed monument events active (property name is plural) | [Condition](#condition), [ConditionMonumentEventsActive](#conditionmonumenteventsactive) | 400089 (assets.xml:2345600; Action_Achievement_Party Like 1851); 400103 (assets.xml:2345652; Action_Achievement_Great Exhibitionist) |
| `ConditionMonumentProgress`: Filtered monument progress | [Condition](#condition), [ConditionMonumentProgress](#conditionmonumentprogress), [ObjectFilter](#objectfilter) | 136660 (assets.xml:4163830; Trigger Start Event 2); 136747 (assets.xml:4166694; Trigger Start Event 3) |
| `ConditionMoveVehicle`: Vehicle movement/distance, optional label | [Condition](#condition), [ConditionMoveVehicle](#conditionmovevehicle), [ConditionPropsSessionSettings](#conditionpropssessionsettings) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionMutualAreaInSubconditions`: Common area of specialized child conditions | [Condition](#condition), [ConditionMutualAreaInSubconditions](#conditionmutualareainsubconditions) | 152558 (assets.xml:1072784; Puzzle Sunken Poetry 2 - An Ancient Map - Pincess Qing DISABLED); 151041 (assets.xml:1169026; RQ_Farmers_FieldDig) |
| `ConditionNewspaperPossible`: Newspaper-possible state | [Condition](#condition), [ConditionNewspaperPossible](#conditionnewspaperpossible) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionNewspaperPublished`: Published newspaper / replaced-page amount | [Condition](#condition), [ConditionNewspaperPublished](#conditionnewspaperpublished) | 400091 (assets.xml:2344672; Action_Achievement_Fake News); 111797 (assets.xml:2778856; Trigger Propaganda Quests Increase Chance) |
| `ConditionObjHPCheck`: Target GUID/owner HP percentage | [Condition](#condition), [ConditionObjHPCheck](#conditionobjhpcheck) | 150936 (assets.xml:774269; CQ252_TakeRevenge_CombatDialog01); 150938 (assets.xml:774349; CQ252_TakeRevenge_CombatDialog02) |
| `ConditionObjectPosition`: Filtered objects near filtered targets | [Condition](#condition), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ConditionObjectPosition](#conditionobjectposition), [ObjectFilter](#objectfilter), [ObjectTargetFilter](#objecttargetfilter), [ConditionPropsNegatable](#conditionpropsnegatable) | 124965 (assets.xml:3366506; Trigger BiniamReachedPump1); 124963 (assets.xml:3366690; Trigger BiniamReachedPump2) |
| `ConditionObjectSelected`: Filtered-object selection / incident/ruin state | [Condition](#condition), [ConditionObjectSelected](#conditionobjectselected), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ObjectFilter](#objectfilter), [ConditionPropsNegatable](#conditionpropsnegatable) | 152289 (assets.xml:826985; RQ_Worker_DrillGift); 151357 (assets.xml:844386; SellShip Sandbox) |
| `ConditionOverlapsAABB`: Overlap of two asset bounds | [Condition](#condition), [ConditionOverlapsAABB](#conditionoverlapsaabb), [ConditionPropsNegatable](#conditionpropsnegatable) | 270144 (assets.xml:3147993; DLC05 Achievement03) |
| `ConditionPalaceItemEquipBonusActive`: Palace item/effect building and equipment counts | [Condition](#condition), [ConditionPalaceItemEquipBonusActive](#conditionpalaceitemequipbonusactive) | 269323 (assets.xml:3125843; DLC04 Achievement03) |
| `ConditionPalaceUnlocks`: Ministry/decree unlock flags | [Condition](#condition), [ConditionPalaceUnlocks](#conditionpalaceunlocks) | 269534 (assets.xml:3110714; TutorialHint Palace ParagonHint); 269321 (assets.xml:3125726; DLC04 Achievement01) |
| `ConditionPhotographyObject`: Photography framing/object settings (property PhotographObject) | [Condition](#condition), [ConditionPhotographObject](#conditionphotographobject) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionPlayerCounter`: Typed participant counter with context and scope | [Condition](#condition), [ConditionPlayerCounter](#conditionplayercounter) | 130249 (assets.xml:669195; intermediate moderate 1.1); 130250 (assets.xml:669256; intermediate moderate 1.2) |
| `ConditionProductCapacityReached`: Product storage capacity reached | [Condition](#condition), [ConditionProductCapacityReached](#conditionproductcapacityreached) | 139195 (assets.xml:4960112; Trigger_Reaction_FullWarehouse) |
| `ConditionProductivity`: Good production rate/productivity comparison | [Condition](#condition), [ConditionProductivity](#conditionproductivity) | 270147 (assets.xml:3148539; DLC05 Achievement06); 129692 (assets.xml:3926465; DLC06 Achievement04 (StewProduction)) |
| `ConditionQuestPoolQuestRunning`: Any/all listed quest pools running a quest | [Condition](#condition), [ConditionQuestPoolQuestRunning](#conditionquestpoolquestrunning), [ConditionPropsNegatable](#conditionpropsnegatable) | 131177 (assets.xml:3474802; Info Unlock Library); 132628 (assets.xml:3872019; LandOfLions SessionStorytelling UnlockLibrary) |
| `ConditionQuestResolveConfirmation`: Quest confirmation objective context | [ConditionQuestResolveConfirmation](#conditionquestresolveconfirmation), [Condition](#condition), [ConditionQuestObjective](#conditionquestobjective) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionQuestState`: Quest/quest-line state flags | [Condition](#condition), [ConditionQuestState](#conditionqueststate) | 269946 (assets.xml:704306; TRIGGER Unlock Great Eastern); 152031 (assets.xml:751336; CQ001_TravelBroker_HitDialog_Trigger) |
| `ConditionRecipeResearchCompleted`: Completed research recipes by research field | [Condition](#condition), [ConditionRecipeResearchCompleted](#conditionreciperesearchcompleted) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionReputation`: Directional participant reputation comparison | [Condition](#condition), [ConditionReputation](#conditionreputation), [ParticipantRelation](#participantrelation) | 152489 (assets.xml:895598; Gift Shared Treasure - Bente); 152490 (assets.xml:896049; Gift Missing Credits? - Bente) |
| `ConditionResearchPointLimitReached`: Research-point limit state | [Condition](#condition), [ConditionResearchPointLimitReached](#conditionresearchpointlimitreached) | 127937 (assets.xml:3863236; TutorialHint LoL 10 ResearchPointsLimit HUD) |
| `ConditionResidentsInBuilding`: Resident count in filtered buildings | [Condition](#condition), [ObjectFilter](#objectfilter), [ConditionResidentsInBuilding](#conditionresidentsinbuilding) | 136213 (assets.xml:4243604; DLC09 Achievement06 (PopulationSkylineTower)) |
| `ConditionSeason`: Season in specified/all sessions | [Condition](#condition), [ConditionSeason](#conditionseason) | 25207 (assets.xml:4287518; Trigger_Reaction_FirstRain); 25212 (assets.xml:4287596; Trigger_Reaction_FirstRainOver) |
| `ConditionSelectionHappinessDebuffActive`: Selection happiness-category debuff flags | [Condition](#condition), [ConditionSelectionHappinessDebuffActive](#conditionselectionhappinessdebuffactive) | 134424 (assets.xml:4089473; -- TutorialHint Tourists SB17 PickyNeedsA); 134425 (assets.xml:4089877; -- TutorialHint Tourists SB18 PickyNeedsB) |
| `ConditionSessionLoading`: Session-loading context | [Condition](#condition), [ConditionSessionLoading](#conditionsessionloading), [ConditionPropsSessionSettings](#conditionpropssessionsettings) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionShipsInRange`: Ship/target range check with ownership and session settings | [Condition](#condition), [ConditionShipsInRange](#conditionshipsinrange), [SessionFilter](#sessionfilter) | 151434 (assets.xml:781859; CQ320_Escape2_PyroSpawn_Trigger); 153171 (assets.xml:1079319; ShipBecomesGeneralEnemy) |
| `ConditionShipsOwnedInSession`: Ship/pool amount in a session | [Condition](#condition), [ConditionShipsOwnedInSession](#conditionshipsownedinsession) | 151073 (assets.xml:783430; CQ322_DefenseMeasures_Trigger); 151498 (assets.xml:1208763; RQ_Jornaleros_BytheShore) |
| `ConditionShipyardState`: Shipyard queue state and owner | [Condition](#condition), [ConditionShipyardState](#conditionshipyardstate) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionStarterObject`: Quest starter selection/movement/area setup | [Condition](#condition), [ConditionStarterObject](#conditionstarterobject), [ConditionQuestObjective](#conditionquestobjective), [ConditionPropsSessionSettings](#conditionpropssessionsettings) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionStaticResult`: Fixed ConditionResult token | [Condition](#condition), [ConditionStaticResult](#conditionstaticresult) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionTextPopupClosed`: Closed text-popup layout flags (not text GUID) | [Condition](#condition), [ConditionTextPopupClosed](#conditiontextpopupclosed) | 120247 (assets.xml:3370710; Trigger LoLStory CloseJournal); 120308 (assets.xml:3371625; Trigger LoLStory CloseAccounts) |
| `ConditionTextPopupPagesViewed`: Viewed pages by popup layout | [Condition](#condition), [ConditionTextPopupPagesViewed](#conditiontextpopuppagesviewed) | 400060 (assets.xml:2343888; Action_Achievement_Nosey Parker); 400086 (assets.xml:2344056; Action_Achievement_Bookworm) |
| `ConditionThreshold`: Textsource threshold/duration (serious recorded limitations) | [Condition](#condition), [ConditionThreshold](#conditionthreshold) | No explicit-Template sample captured; also search Values/property and inherited definitions. |
| `ConditionTimePassed`: Time-passed comparison | [Condition](#condition), [ConditionTimePassed](#conditiontimepassed) | 2287 (assets.xml:4503758; GoldTrigger) |
| `ConditionTimer`: Eligible-condition timer with ID/pause/unregister behavior | [Condition](#condition), [ConditionTimer](#conditiontimer) | 151119 (assets.xml:868153; TQ_FindStartingIsland); 151344 (assets.xml:868716; TQ_FirstSettlement) |
| `ConditionTradeRouteCount`: Filtered trade-route amount | [Condition](#condition), [ConditionTradeRouteCount](#conditiontraderoutecount) | 400073 (assets.xml:2345129; Action_Achievement_Charter Company); 2657 (assets.xml:4500339; DLC11Achievement03) |
| `ConditionTutorialInteraction`: Tutorial/UI interaction and hint context | [Condition](#condition), [ConditionTutorialInteraction](#conditiontutorialinteraction) | 151121 (assets.xml:801816; Fertilities); 151271 (assets.xml:802215; Island) |
| `ConditionUnlocked`: Current unlock state of an asset | [Condition](#condition), [ConditionUnlocked](#conditionunlocked), [ConditionPropsNegatable](#conditionpropsnegatable) | 141003 (assets.xml:703981; TRIGGER Unlock Schooner & Gunboat); 141007 (assets.xml:704167; TRIGGER Unlock Collier & Battle Cruiser) |
| `ConditionUnlockedList`: Unlock list with range operator (property ConditionUnlockList) | [Condition](#condition), [ConditionUnlockList](#conditionunlocklist) | 152564 (assets.xml:908539; Deliver New Year Celebrations 1 - Ticking Machines - Princess Qing); 152546 (assets.xml:1070819; Deliver Treasures Ship 3 - Old World Poetry - Princess Qing) |

## Related native templates: objectives and object selectors

These templates do not have a direct Condition property. They are not automatically interchangeable with a TriggerCondition. The field reference also includes schema-only properties without a same-named template (for example ConditionItemUsed).

| Template | Property blocks | Template source line |
| --- | --- | --- |
| `AirdropObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestAirdrop](#conditionquestairdrop) | 1741 |
| `BringVehicleToObjectObjective` | [ConditionQuestBringVehicleToObject](#conditionquestbringvehicletoobject), [ConditionQuestObjective](#conditionquestobjective), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 1769 |
| `BusActivationNeedSaturationObjective` | [ConditionQuestObjective](#conditionquestobjective), [ObjectFilter](#objectfilter), [ConditionQuestBusActivationNeedSaturation](#conditionquestbusactivationneedsaturation) | 1816 |
| `CameraMovementObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestCameraMovement](#conditionquestcameramovement) | 1849 |
| `ConditionObjectAnywhere` | [ConditionObjectAnywhere](#conditionobjectanywhere) | 727 |
| `ConditionObjectClientQuestObject` | [ConditionObjectClientQuestObject](#conditionobjectclientquestobject), [ConditionScanner](#conditionscanner), [ConditionObjectiveSignsAndFeedback](#conditionobjectivesignsandfeedback) | 733 |
| `ConditionObjectPlayerKontor` | [ConditionObjectPlayerKontor](#conditionobjectplayerkontor), [ConditionScanner](#conditionscanner), [ConditionObjectiveSignsAndFeedback](#conditionobjectivesignsandfeedback) | 753 |
| `ConditionObjectPrebuiltObject` | [ConditionObjectPrebuiltObject](#conditionobjectprebuiltobject), [ConditionScanner](#conditionscanner), [ConditionObjectiveSignsAndFeedback](#conditionobjectivesignsandfeedback) | 764 |
| `ConditionObjectSpawnedObject` | [ConditionObjectSpawnedObject](#conditionobjectspawnedobject), [ConditionScanner](#conditionscanner), [ConditionObjectiveSignsAndFeedback](#conditionobjectivesignsandfeedback) | 777 |
| `ConditionObjectStarterObject` | [ConditionScanner](#conditionscanner), [ConditionObjectStarterObject](#conditionobjectstarterobject), [ConditionObjectiveSignsAndFeedback](#conditionobjectivesignsandfeedback) | 795 |
| `ConditionObjectUseDefaultSettings` | [ConditionObjectUseDefaultSettings](#conditionobjectusedefaultsettings) | 806 |
| `ConditionObjectiveSignsAndFeedback` | [ConditionObjectiveSignsAndFeedback](#conditionobjectivesignsandfeedback) | 744 |
| `ConditionScanner` | [ConditionScanner](#conditionscanner) | 812 |
| `DecisionObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestDecision](#conditionquestdecision) | 1877 |
| `DeliveryObjective` | [ConditionQuestDelivery](#conditionquestdelivery), [ConditionQuestObjective](#conditionquestobjective), [ObjectiveScaling](#objectivescaling), [ConditionPropsSessionSettings](#conditionpropssessionsettings) | 1905 |
| `DestroyObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestDestroy](#conditionquestdestroy), [SpawnArea](#spawnarea), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 1967 |
| `DivingBellObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestDivingBell](#conditionquestdivingbell), [SpawnArea](#spawnarea), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2016 |
| `EscortObjective` | [ConditionQuestEscort](#conditionquestescort), [ConditionQuestObjective](#conditionquestobjective), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2055 |
| `ExpeditionObjective` | [ConditionQuestExpedition](#conditionquestexpedition), [ConditionQuestObjective](#conditionquestobjective), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2110 |
| `FactoryProductivityObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestFactoryProductivity](#conditionquestfactoryproductivity), [ObjectFilter](#objectfilter) | 2147 |
| `FakeQuestObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestFakeObjective](#conditionquestfakeobjective) | 2176 |
| `FollowShipObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestFollowShip](#conditionquestfollowship) | 2204 |
| `GamePadActionObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestGamePadAction](#conditionquestgamepadaction) | 2262 |
| `HitMovingTargetObjective` | [ConditionQuestHitMovingTarget](#conditionquesthitmovingtarget), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ConditionQuestObjective](#conditionquestobjective), [SpawnArea](#spawnarea), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2290 |
| `IslandsWithFertilityObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestIslandsWithFertility](#conditionquestislandswithfertility) | 2357 |
| `ItemUsageObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestItemUsed](#conditionquestitemused), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2387 |
| `ModuleBuildingEfficiencyObjective` | [ConditionQuestModuleBuildingEfficiency](#conditionquestmodulebuildingefficiency), [ConditionQuestObjective](#conditionquestobjective), [ConditionPropsNegatable](#conditionpropsnegatable), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2425 |
| `MonumentDestroyedObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestMonumentDestroyed](#conditionquestmonumentdestroyed) | 2466 |
| `ObjectFilterWithSignsAndFeedback` | [ObjectFilter](#objectfilter), [ConditionObjectiveSignsAndFeedback](#conditionobjectivesignsandfeedback) | 829 |
| `PhotographyObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestPhotography](#conditionquestphotography), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2494 |
| `PickupObjective` | [ConditionQuestPickup](#conditionquestpickup), [ConditionQuestObjective](#conditionquestobjective), [SpawnArea](#spawnarea), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings), [ConditionPropsSessionSettings](#conditionpropssessionsettings) | 2533 |
| `PicturePuzzleObjective` | [ConditionQuestPicturePuzzle](#conditionquestpicturepuzzle), [ConditionQuestObjective](#conditionquestobjective), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2582 |
| `QuestExecutionPlace` | [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 839 |
| `RecipeResearchCompletedObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestRecipeResearchCompleted](#conditionquestreciperesearchcompleted) | 2623 |
| `SelectObjectObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestSelectObject](#conditionquestselectobject), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2653 |
| `SellObjectToParticipantObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestSellObjectToParticipant](#conditionquestsellobjecttoparticipant) | 2693 |
| `SmugglerObjective` | [ConditionQuestSmuggler](#conditionquestsmuggler), [ConditionQuestObjective](#conditionquestobjective), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2721 |
| `StatusQuoObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionPlayerCounter](#conditionplayercounter), [ConditionQuestStatusQuo](#conditionqueststatusquo), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2773 |
| `SubQuestObjective` | [ConditionQuestSubQuest](#conditionquestsubquest), [ConditionQuestObjective](#conditionquestobjective) | 2810 |
| `SustainObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionPlayerCounter](#conditionplayercounter), [ConditionQuestSustain](#conditionquestsustain), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2838 |
| `TutorialObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionQuestTutorial](#conditionquesttutorial) | 2876 |
| `UseItemInAreaObjective` | [ConditionQuestObjective](#conditionquestobjective), [ConditionPropsSessionSettings](#conditionpropssessionsettings), [ConditionQuestUseItemInArea](#conditionquestuseiteminarea), [SpawnArea](#spawnarea), [ConditionPropsExecutionPlaceSettings](#conditionpropsexecutionplacesettings) | 2904 |

## Template overrides and related templates

For each indexed template, the exact template XML is retained in native contracts. The following nonempty overrides affect the effective condition; copy neither a property default nor a nearby template as a substitute.

### ActionDelayedActions overrides (templates.xml:96)

```xml
<ActionDelayedActions>
            <DelayedActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </DelayedActions>
          </ActionDelayedActions>
```

### AirdropObjective overrides (templates.xml:1741)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### AutoCreateTrigger overrides (templates.xml:3154)

```xml
<Trigger>
          <TriggerCondition>
            <Template>ConditionAlwaysTrue</Template>
            <Values>
              <Condition/>
              <ConditionAlwaysTrue/>
            </Values>
          </TriggerCondition>
          <ResetTrigger>
            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
            <Values>
              <EmptyAutoCreateValue/>
            </Values>
          </ResetTrigger>
        </Trigger>
```

### BringVehicleToObjectObjective overrides (templates.xml:1769)

```xml
<ConditionQuestBringVehicleToObject>
            <BringToObject>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </BringToObject>
            <VehicleDistance>20</VehicleDistance>
          </ConditionQuestBringVehicleToObject>
          
<ConditionQuestObjective>
            <TextCombinedContextValue>15268</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectAnywhere</Template>
              <Values>
                <ConditionObjectAnywhere/>
              </Values>
            </ExecutionPlace>
          </ConditionPropsExecutionPlaceSettings>
```

### BusActivationNeedSaturationObjective overrides (templates.xml:1816)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ObjectFilter>
            <ObjectGUID>601445</ObjectGUID>
            <CheckParticipantID>1</CheckParticipantID>
            <CheckProcessingParticipantID>1</CheckProcessingParticipantID>
          </ObjectFilter>
```

### CameraMovementObjective overrides (templates.xml:1849)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### ConditionAreaClaimed overrides (templates.xml:962)

```xml
<ConditionAreaClaimed>
            <Claimed>1</Claimed>
          </ConditionAreaClaimed>
```

### ConditionBusActivationNeedSaturation overrides (templates.xml:992)

```xml
<ObjectFilter>
            <ObjectGUID>601445</ObjectGUID>
            <CheckParticipantID>1</CheckParticipantID>
            <CheckProcessingParticipantID>1</CheckProcessingParticipantID>
          </ObjectFilter>
          
<ConditionBusActivationNeedSaturation>
            <NeedsRangeOP>All</NeedsRangeOP>
          </ConditionBusActivationNeedSaturation>
```

### ConditionCameraMovement overrides (templates.xml:1006)

```xml
<ConditionCameraMovement>
            <CameraMovementActionToTrack/>
          </ConditionCameraMovement>
```

### ConditionCorporationDifficulty overrides (templates.xml:1015)

```xml
<ConditionCorporationDifficulty>
            <Difficulty>Easy;Normal;Hard;Classic</Difficulty>
            <DifficultyConstructionCostRefund>Full;Half;None;PayCredits</DifficultyConstructionCostRefund>
            <DifficultyLossCondition>BailoutWithSlowLiquidation;BailoutWithFastLiquidation;Bankrupt</DifficultyLossCondition>
            <DifficultyOptionalQuestFrequency>Often;Normal;Rare</DifficultyOptionalQuestFrequency>
            <DifficultyOptionalQuestRewards>Plenty;Medium;Spare;PennyPinching</DifficultyOptionalQuestRewards>
            <DifficultyRelocateBuildings>On;Off;PayCredits</DifficultyRelocateBuildings>
            <DifficultyRevenue>Plenty;Medium;Spare</DifficultyRevenue>
            <DifficultyStartCredits>Plenty;Medium;Spare</DifficultyStartCredits>
            <DifficultyStartShips>None;OneShip;TradeFleet;WarFleet</DifficultyStartShips>
            <DifficultyStartWithKontor>Off;Standard;Full</DifficultyStartWithKontor>
          </ConditionCorporationDifficulty>
```

### ConditionDecisionOption overrides (templates.xml:1040)

```xml
<ConditionDecisionOption>
            <ActionList>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </ActionList>
            <DecisionNotification>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </DecisionNotification>
          </ConditionDecisionOption>
```

### ConditionEvent overrides (templates.xml:1085)

```xml
<ConditionEvent>
            <ContextAssetInfolayer>2001386</ContextAssetInfolayer>
            <EventCount>1</EventCount>
          </ConditionEvent>
```

### ConditionIslandsDiscovered overrides (templates.xml:1285)

```xml
<ConditionIslandsDiscovered>
            <IslandsDiscoveredScope>Global</IslandsDiscoveredScope>
          </ConditionIslandsDiscovered>
```

### ConditionIslandsWithFertility overrides (templates.xml:1294)

```xml
<ConditionIslandsWithFertility>
            <IslandScope>Global</IslandScope>
          </ConditionIslandsWithFertility>
```

### ConditionMoveVehicle overrides (templates.xml:1372)

```xml
<ConditionMoveVehicle>
            <MoveVehicleTargetDistance>20</MoveVehicleTargetDistance>
          </ConditionMoveVehicle>
```

### ConditionMutualAreaInSubconditions overrides (templates.xml:1383)

```xml
<ConditionMutualAreaInSubconditions>
            <UseParentValues>1</UseParentValues>
          </ConditionMutualAreaInSubconditions>
```

### ConditionObjectClientQuestObject overrides (templates.xml:733)

```xml
<ConditionObjectiveSignsAndFeedback>
            <Infolayer>500693</Infolayer>
            <MinimapToken>2001840</MinimapToken>
          </ConditionObjectiveSignsAndFeedback>
```

### ConditionObjectPlayerKontor overrides (templates.xml:753)

```xml
<ConditionObjectiveSignsAndFeedback>
            <Infolayer>500693</Infolayer>
            <MinimapToken>2001840</MinimapToken>
          </ConditionObjectiveSignsAndFeedback>
```

### ConditionObjectPosition overrides (templates.xml:1406)

```xml
<ConditionObjectPosition>
            <ExpectObjectExists>1</ExpectObjectExists>
            <ExpectTargetExists>1</ExpectTargetExists>
          </ConditionObjectPosition>
```

### ConditionObjectPrebuiltObject overrides (templates.xml:764)

```xml
<ConditionObjectPrebuiltObject>
            <PrebuiltObjectUseVisibilityAutomatism>1</PrebuiltObjectUseVisibilityAutomatism>
          </ConditionObjectPrebuiltObject>
          
<ConditionObjectiveSignsAndFeedback>
            <Infolayer>500693</Infolayer>
            <MinimapToken>2001840</MinimapToken>
          </ConditionObjectiveSignsAndFeedback>
```

### ConditionObjectSpawnedObject overrides (templates.xml:777)

```xml
<ConditionObjectSpawnedObject>
            <ObjectSpawnArea>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <SpawnArea/>
              </Values>
            </ObjectSpawnArea>
          </ConditionObjectSpawnedObject>
          
<ConditionObjectiveSignsAndFeedback>
            <Infolayer>500693</Infolayer>
            <MinimapToken>2001840</MinimapToken>
          </ConditionObjectiveSignsAndFeedback>
```

### ConditionObjectStarterObject overrides (templates.xml:795)

```xml
<ConditionObjectiveSignsAndFeedback>
            <Infolayer>500693</Infolayer>
            <MinimapToken>2001840</MinimapToken>
          </ConditionObjectiveSignsAndFeedback>
```

### ConditionObjectiveSignsAndFeedback overrides (templates.xml:744)

```xml
<ConditionObjectiveSignsAndFeedback>
            <Infolayer>500693</Infolayer>
            <MinimapToken>2001840</MinimapToken>
          </ConditionObjectiveSignsAndFeedback>
```

### ConditionQuestResolveConfirmation overrides (templates.xml:1496)

```xml
<ConditionQuestObjective>
            <TextCombinedContextValue>12763</TextCombinedContextValue>
          </ConditionQuestObjective>
```

### ConditionRecipeResearchCompleted overrides (templates.xml:1513)

```xml
<ConditionRecipeResearchCompleted>
            <ResearchRangeOp>Any</ResearchRangeOp>
          </ConditionRecipeResearchCompleted>
```

### ConditionShipsInRange overrides (templates.xml:1567)

```xml
<SessionFilter>
            <AllowParentConditionSession>0</AllowParentConditionSession>
            <AllowProcessingSession>1</AllowProcessingSession>
          </SessionFilter>
```

### ConditionStarterObject overrides (templates.xml:1592)

```xml
<ConditionStarterObject>
            <DockingPlaceDistance>20</DockingPlaceDistance>
            <StarterObjectObject>
              <Template>ConditionObjectClientQuestObject</Template>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </StarterObjectObject>
            <StarterObjectDockingPlace>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </StarterObjectDockingPlace>
          </ConditionStarterObject>
          
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <Template>ConditionObjectiveSignsAndFeedback</Template>
              <Values>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>500173</Infolayer>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### ConditionTutorialInteraction overrides (templates.xml:1692)

```xml
<ConditionTutorialInteraction>
            <AllowedInputTypes>MouseKeyboard;Gamepad</AllowedInputTypes>
            <ObjectFilter>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ObjectFilter/>
              </Values>
            </ObjectFilter>
          </ConditionTutorialInteraction>
```

### ConditionUnlockedList overrides (templates.xml:1715)

```xml
<ConditionUnlockList>
            <UnlockRangeOP>All</UnlockRangeOP>
          </ConditionUnlockList>
```

### DecisionObjective overrides (templates.xml:1877)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### DeliveryObjective overrides (templates.xml:1905)

```xml
<ConditionQuestDelivery>
            <DeliveryExecutionPlace>
              <Template>ConditionObjectClientQuestObject</Template>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </DeliveryExecutionPlace>
          </ConditionQuestDelivery>
          
<ConditionQuestObjective>
            <TextCombinedContextValue>12754</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ObjectiveScaling>
            <ScaleObjectives>1</ScaleObjectives>
            <ScaleFactors>
              <EarlyGame>
                <Factor>1</Factor>
              </EarlyGame>
              <EarlyMidGame>
                <Factor>1.2</Factor>
              </EarlyMidGame>
              <MidGame>
                <Factor>1.4</Factor>
              </MidGame>
              <LateMidGame>
                <Factor>1.6</Factor>
              </LateMidGame>
              <LateGame>
                <Factor>1.8</Factor>
              </LateGame>
              <EndGame>
                <Factor>2</Factor>
              </EndGame>
            </ScaleFactors>
          </ObjectiveScaling>
```

### DestroyObjective overrides (templates.xml:1967)

```xml
<ConditionQuestObjective>
            <TextCombinedContextValue>12756</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <Template>ConditionObjectiveSignsAndFeedback</Template>
              <Values>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>500335</Infolayer>
                  <MinimapToken>2001947</MinimapToken>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionQuestDestroy>
            <MoveAngleMin_cqd>45</MoveAngleMin_cqd>
            <MoveAngleMax_cqd>90</MoveAngleMax_cqd>
            <ObjectsBehaviour>Patrol</ObjectsBehaviour>
          </ConditionQuestDestroy>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectClientQuestObject</Template>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ExecutionPlace>
            <ExecutionPlaceText>14033</ExecutionPlaceText>
          </ConditionPropsExecutionPlaceSettings>
```

### DivingBellObjective overrides (templates.xml:2016)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionQuestDivingBell>
            <AdditionalObjectData>
              <AdditionalObjectList>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <ConditionScanner/>
                </Values>
              </AdditionalObjectList>
            </AdditionalObjectData>
          </ConditionQuestDivingBell>
```

### EscortObjective overrides (templates.xml:2055)

```xml
<ConditionQuestEscort>
            <SpawnArea>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <SpawnArea/>
              </Values>
            </SpawnArea>
            <DistMinBetweenAttacker>5</DistMinBetweenAttacker>
            <DistMaxBetweenAttacker>10</DistMaxBetweenAttacker>
            <StarterHeadlineText>15208</StarterHeadlineText>
            <StarterHeadlineTextWithoutShip>14999</StarterHeadlineTextWithoutShip>
            <TargetMapBorderText>20073</TargetMapBorderText>
          </ConditionQuestEscort>
          
<ConditionQuestObjective>
            <TextCombinedContextValue>12757</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <Template>ConditionObjectiveSignsAndFeedback</Template>
              <Values>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>500336</Infolayer>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectClientQuestObject</Template>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ExecutionPlace>
            <ExecutionPlaceText>12754</ExecutionPlaceText>
          </ConditionPropsExecutionPlaceSettings>
```

### ExpeditionObjective overrides (templates.xml:2110)

```xml
<ConditionQuestObjective>
            <TextCombinedContextValue>12762</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectAnywhere</Template>
              <Values>
                <ConditionObjectAnywhere/>
              </Values>
            </ExecutionPlace>
          </ConditionPropsExecutionPlaceSettings>
```

### FactoryProductivityObjective overrides (templates.xml:2147)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### FakeQuestObjective overrides (templates.xml:2176)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### FeatureUnlock overrides (templates.xml:10070)

```xml
<Trigger>
          <TriggerCondition>
            <Template>ConditionAlwaysTrue</Template>
            <Values>
              <Condition/>
              <ConditionAlwaysTrue/>
            </Values>
          </TriggerCondition>
          <ResetTrigger>
            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
            <Values>
              <EmptyAutoCreateValue/>
            </Values>
          </ResetTrigger>
        </Trigger>
        
<TriggerSetup>
          <AutoRegisterTrigger>1</AutoRegisterTrigger>
          <AutoSelfUnlock>1</AutoSelfUnlock>
          <UsedBySecondParties>1</UsedBySecondParties>
        </TriggerSetup>
```

### FollowShipObjective overrides (templates.xml:2204)

```xml
<ConditionQuestObjective>
            <QuestTrackerIcon>data/ui/2kimages/main/icons/icon_warning.png</QuestTrackerIcon>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionQuestFollowShip>
            <StartRangeObjectiveText>11976</StartRangeObjectiveText>
            <RangeWarningText>12106</RangeWarningText>
            <StartPosition>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionScanner/>
                <ConditionObjectStarterObject/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </StartPosition>
            <StartRange>25</StartRange>
            <TargetShip>
              <Template>ConditionObjectSpawnedObject</Template>
              <Values>
                <ConditionObjectSpawnedObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>501543</Infolayer>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </TargetShip>
            <MinRange>20</MinRange>
            <MaxRange>50</MaxRange>
            <MinRangeEffectPositive>500886</MinRangeEffectPositive>
            <MinRangeEffectNegative>500888</MinRangeEffectNegative>
            <MaxRangeEffectPositive>500886</MaxRangeEffectPositive>
            <MaxRangeEffectNegative>500888</MaxRangeEffectNegative>
            <RangeWarningTime>30000</RangeWarningTime>
          </ConditionQuestFollowShip>
```

### GamePadActionObjective overrides (templates.xml:2262)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### HitMovingTargetObjective overrides (templates.xml:2290)

```xml
<ConditionQuestHitMovingTarget>
            <HitTargetSignsAndFeedback>
              <Template>ConditionObjectiveSignsAndFeedback</Template>
              <Values>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>500482</Infolayer>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </HitTargetSignsAndFeedback>
            <WaypointAmount>5</WaypointAmount>
            <TargetPatrolRadius>20</TargetPatrolRadius>
            <ItemRetrievalPlace>
              <Template>ConditionObjectClientQuestObject</Template>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ItemRetrievalPlace>
            <ItemUsed>190585</ItemUsed>
          </ConditionQuestHitMovingTarget>
          
<ConditionQuestObjective>
            <TextCombinedContextValue>12764</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <Template>ConditionObjectiveSignsAndFeedback</Template>
              <Values>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>500482</Infolayer>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<SpawnArea>
            <SpawnContext>ClientKontor</SpawnContext>
            <SpawnAreaType>Water</SpawnAreaType>
          </SpawnArea>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectClientQuestObject</Template>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ExecutionPlace>
            <ExecutionPlaceText>12754</ExecutionPlaceText>
          </ConditionPropsExecutionPlaceSettings>
```

### IslandsWithFertilityObjective overrides (templates.xml:2357)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionQuestIslandsWithFertility>
            <QuestIslandScope>Global</QuestIslandScope>
          </ConditionQuestIslandsWithFertility>
```

### ItemUsageObjective overrides (templates.xml:2387)

```xml
<ConditionQuestObjective>
            <TextCombinedContextValue>12755</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectAnywhere</Template>
              <Values>
                <ConditionObjectAnywhere/>
              </Values>
            </ExecutionPlace>
          </ConditionPropsExecutionPlaceSettings>
```

### ModuleBuildingEfficiencyObjective overrides (templates.xml:2425)

```xml
<ConditionQuestModuleBuildingEfficiency>
            <Efficiency>1</Efficiency>
          </ConditionQuestModuleBuildingEfficiency>
          
<ConditionQuestObjective>
            <TextCombinedContextValue>12758</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectAnywhere</Template>
              <Values>
                <ConditionObjectAnywhere/>
              </Values>
            </ExecutionPlace>
          </ConditionPropsExecutionPlaceSettings>
```

### MonumentDestroyedObjective overrides (templates.xml:2466)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### ObjectFilterWithSignsAndFeedback overrides (templates.xml:829)

```xml
<ConditionObjectiveSignsAndFeedback>
            <Infolayer>500693</Infolayer>
            <MinimapToken>2001840</MinimapToken>
          </ConditionObjectiveSignsAndFeedback>
```

### PhotographyObjective overrides (templates.xml:2494)

```xml
<ConditionQuestObjective>
            <TextCombinedContextValue>12722</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <Template>ConditionObjectiveSignsAndFeedback</Template>
              <Values>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>501594</Infolayer>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectAnywhere</Template>
              <Values>
                <ConditionObjectAnywhere/>
              </Values>
            </ExecutionPlace>
          </ConditionPropsExecutionPlaceSettings>
```

### PickupObjective overrides (templates.xml:2533)

```xml
<ConditionQuestObjective>
            <TextCombinedContextValue>12731</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <Template>ConditionObjectiveSignsAndFeedback</Template>
              <Values>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>500334</Infolayer>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<SpawnArea>
            <MinObjectDistance>5</MinObjectDistance>
            <MaxObjectDistance>10</MaxObjectDistance>
            <DistanceToBorder>Mid</DistanceToBorder>
            <DistanceToIsland>Mid</DistanceToIsland>
          </SpawnArea>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectClientQuestObject</Template>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ExecutionPlace>
            <ExecutionPlaceText>14033</ExecutionPlaceText>
          </ConditionPropsExecutionPlaceSettings>
```

### PicturePuzzleObjective overrides (templates.xml:2582)

```xml
<ConditionQuestObjective>
            <TextCombinedContextValue>12760</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <Template>ConditionObjectiveSignsAndFeedback</Template>
              <Values>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>501016</Infolayer>
                  <ShowMinimapToken>0</ShowMinimapToken>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectAnywhere</Template>
              <Values>
                <ConditionObjectAnywhere/>
              </Values>
            </ExecutionPlace>
          </ConditionPropsExecutionPlaceSettings>
```

### Quest overrides (templates.xml:11746)

```xml
<Quest>
            <StarterMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </StarterMessage>
            <SuccessMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </SuccessMessage>
            <FailureMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </FailureMessage>
            <SelectionReminderMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </SelectionReminderMessage>
            <AbortedManuallyMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </AbortedManuallyMessage>
            <AbortedAutomaticallyMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </AbortedAutomaticallyMessage>
            <InvitationMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification>
                    <IsUnique>1</IsUnique>
                  </BaseNotification>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </InvitationMessage>
            <EscortShipSelectedMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </EscortShipSelectedMessage>
            <ReminderMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification>
                    <IsUnique>1</IsUnique>
                  </BaseNotification>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </ReminderMessage>
            <ResolveConfirmationMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification>
                    <IsUnique>1</IsUnique>
                  </BaseNotification>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </ResolveConfirmationMessage>
            <InvitationSmugglerQuestMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </InvitationSmugglerQuestMessage>
            <SmugglerQuestTradingStationReached>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </SmugglerQuestTradingStationReached>
            <StartInvitationGiveItemMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </StartInvitationGiveItemMessage>
            <StartFollowShipMessage>
              <Notification>
                <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </Notification>
            </StartFollowShipMessage>
            <OnQuestStart>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnQuestStart>
            <OnQuestDeclined>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnQuestDeclined>
            <OnQuestActive>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnQuestActive>
            <OnQuestAborted>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnQuestAborted>
            <OnQuestTimedOut>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnQuestTimedOut>
            <OnActiveQuestTimedOut>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnActiveQuestTimedOut>
            <OnQuestFailed>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnQuestFailed>
            <OnQuestDiscarded>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnQuestDiscarded>
            <OnQuestSucceeded>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnQuestSucceeded>
            <OnQuestEnd>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnQuestEnd>
            <OnPhotographySuccessNewspaperAction>
              <Template>ActionForceNewspaper</Template>
              <Values>
                <Action/>
                <ActionForceNewspaper>
                  <OpenNewspaperType>SpecialEdition</OpenNewspaperType>
                </ActionForceNewspaper>
              </Values>
            </OnPhotographySuccessNewspaperAction>
            <NeededProgressLevel>EarlyGame;EarlyMidGame;MidGame;LateMidGame;LateGame;EndGame</NeededProgressLevel>
            <ConfirmOnReachedCondition>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionQuestResolveConfirmation/>
                <Condition/>
                <ConditionQuestObjective/>
              </Values>
            </ConfirmOnReachedCondition>
            <QuestBookBackground>data/ui/2kimages/main/assets16/questbackground/bg_quest_smugglewithoutscanners_delivery_pickup.png</QuestBookBackground>
            <ReputationQuestFail>
              <ReputationFailList>
                <Item>
                  <ReputationAmount>-2</ReputationAmount>
                </Item>
              </ReputationFailList>
            </ReputationQuestFail>
            <HasStarterSpeechBubble>1</HasStarterSpeechBubble>
            <StarterSpeechBubble>
              <Template>ConditionTutorialInteraction</Template>
              <Values>
                <Condition/>
                <ConditionTutorialInteraction>
                  <HintType>Object</HintType>
                  <HintAnchor>BottomRight</HintAnchor>
                  <OnlyShowOnQuestObjects>1</OnlyShowOnQuestObjects>
                </ConditionTutorialInteraction>
              </Values>
            </StarterSpeechBubble>
            <SuccessSpeechBubble>
              <Template>ConditionTutorialInteraction</Template>
              <Values>
                <Condition/>
                <ConditionTutorialInteraction>
                  <HintType>Object</HintType>
                  <HintEndCondition>Time</HintEndCondition>
                  <HintDisplayTime>30000</HintDisplayTime>
                  <HintAnchor>BottomRight</HintAnchor>
                  <OnlyShowOnQuestObjects>1</OnlyShowOnQuestObjects>
                </ConditionTutorialInteraction>
              </Values>
            </SuccessSpeechBubble>
          </Quest>
          
<PreConditionList>
            <Condition>
              <Template>ConditionAlwaysTrue</Template>
              <Values>
                <Condition>
                  <SubConditionCompletionOrder>Linear</SubConditionCompletionOrder>
                </Condition>
                <ConditionAlwaysTrue/>
              </Values>
            </Condition>
          </PreConditionList>
          
<Reward>
            <RewardReputation>
              <Item>
                <ReputationAmount>3</ReputationAmount>
              </Item>
            </RewardReputation>
          </Reward>
          
<QuestOptional>
            <StarterObject>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <Condition/>
                <ConditionStarterObject/>
                <ConditionQuestObjective/>
                <ConditionPropsSessionSettings/>
              </Values>
            </StarterObject>
          </QuestOptional>
```

### RecipeResearchCompletedObjective overrides (templates.xml:2623)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionQuestRecipeResearchCompleted>
            <QuestResearchRangeOp>Any</QuestResearchRangeOp>
          </ConditionQuestRecipeResearchCompleted>
```

### SelectObjectObjective overrides (templates.xml:2653)

```xml
<ConditionQuestObjective>
            <TextCombinedContextValue>12733</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <Template>ConditionObjectiveSignsAndFeedback</Template>
              <Values>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>500482</Infolayer>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectAnywhere</Template>
              <Values>
                <ConditionObjectAnywhere/>
              </Values>
            </ExecutionPlace>
          </ConditionPropsExecutionPlaceSettings>
```

### SellObjectToParticipantObjective overrides (templates.xml:2693)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### SmugglerObjective overrides (templates.xml:2721)

```xml
<ConditionQuestSmuggler>
            <InitialTradingStation>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectAnywhere/>
              </Values>
            </InitialTradingStation>
            <EnforceStationOrder>1</EnforceStationOrder>
            <ShipInRangeForActivationText>15268</ShipInRangeForActivationText>
            <TextTradingStation_NoItem>15538</TextTradingStation_NoItem>
            <TextTradingStation>12759</TextTradingStation>
          </ConditionQuestSmuggler>
          
<ConditionQuestObjective>
            <TextCombinedContextValue>15638</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectClientQuestObject</Template>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ExecutionPlace>
            <ExecutionPlaceText>12754</ExecutionPlaceText>
          </ConditionPropsExecutionPlaceSettings>
```

### StatusQuoObjective overrides (templates.xml:2773)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectAnywhere</Template>
              <Values>
                <ConditionObjectAnywhere/>
              </Values>
            </ExecutionPlace>
          </ConditionPropsExecutionPlaceSettings>
```

### SubQuestObjective overrides (templates.xml:2810)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### SustainObjective overrides (templates.xml:2838)

```xml
<ConditionQuestObjective>
            <TextCombinedContextValue>12761</TextCombinedContextValue>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectAnywhere</Template>
              <Values>
                <ConditionObjectAnywhere/>
              </Values>
            </ExecutionPlace>
          </ConditionPropsExecutionPlaceSettings>
```

### Trigger overrides (templates.xml:3193)

```xml
<Trigger>
          <TriggerCondition>
            <Template>ConditionAlwaysTrue</Template>
            <Values>
              <Condition/>
              <ConditionAlwaysTrue/>
            </Values>
          </TriggerCondition>
          <ResetTrigger>
            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
            <Values>
              <EmptyAutoCreateValue/>
            </Values>
          </ResetTrigger>
        </Trigger>
        
<TriggerSetup>
          <AutoRegisterTrigger>1</AutoRegisterTrigger>
          <UsedBySecondParties>1</UsedBySecondParties>
        </TriggerSetup>
```

### TutorialObjective overrides (templates.xml:2876)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
```

### UseItemInAreaObjective overrides (templates.xml:2904)

```xml
<ConditionQuestObjective>
            <ObjectiveSignsAndFeedback>
              <Template>ConditionObjectiveSignsAndFeedback</Template>
              <Values>
                <ConditionObjectiveSignsAndFeedback>
                  <Infolayer>500482</Infolayer>
                </ConditionObjectiveSignsAndFeedback>
              </Values>
            </ObjectiveSignsAndFeedback>
            <ObjectiveSuccessMessage>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </ObjectiveSuccessMessage>
            <OnSuccessActions>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList/>
              </Values>
            </OnSuccessActions>
          </ConditionQuestObjective>
          
<ConditionQuestUseItemInArea>
            <StartPlace>
              <Template>ConditionObjectClientQuestObject</Template>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </StartPlace>
            <UseItemInAreaSignsAndFeedback>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </UseItemInAreaSignsAndFeedback>
          </ConditionQuestUseItemInArea>
          
<ConditionPropsExecutionPlaceSettings>
            <ExecutionPlace>
              <Template>ConditionObjectClientQuestObject</Template>
              <Values>
                <ConditionObjectClientQuestObject/>
                <ConditionScanner/>
                <ConditionObjectiveSignsAndFeedback/>
              </Values>
            </ExecutionPlace>
            <ExecutionPlaceText>12754</ExecutionPlaceText>
          </ConditionPropsExecutionPlaceSettings>
```

## Property field reference

Rows reproduce field types and descriptions. `{dataset key}` denotes Array entries; `Item` denotes Vector entries. AutoCreateAsset values contain embedded Template/Values definitions; their allowed properties/templates are in the Restrictions column and exact contract. Preserve spelling, including native typos.

### Action

Source: properties-toolone.xml:7987. Captured owning templates: `ActionDelayedActions`, `ActionExecuteScript`, `ActionLockAsset`, `ActionRegisterTrigger`, `ActionResetTrigger`, `ActionSpawnObjects`, `ActionStartQuest`, `ActionUnlockAsset`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<Action/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ActionDelayedActions

Source: properties-toolone.xml:6368. Captured owning templates: `ActionDelayedActions`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `UseVariableAsDelay` | Boolean |  |  |  |
| `DelayVariable` | Choice | [Variables](trigger-datasets.md#variables) |  |  |
| `ExecutionDelay` | Time |  |  |  |
| `DelayedActions` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= |  |

Explicit property defaults:

```xml
<ActionDelayedActions>
                  <DelayVariable>Mercier_ARQTriggerChance</DelayVariable>
                  <DelayedActions>
                    <Template>Actions</Template>
                    <Values>
                      <ActionList/>
                    </Values>
                  </DelayedActions>
                </ActionDelayedActions>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ActionExecuteScript

Source: properties-toolone.xml:6585. Captured owning templates: `ActionExecuteScript`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ScriptFileName` | FileName |  |  | The script file that should be executed |

Explicit property defaults:

```xml
<ActionExecuteScript/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ActionLink

Source: properties-toolone.xml:7990. Captured owning templates: `ActionLink`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Action` | Asset |  | NeededProperty=ActionList |  |

Explicit property defaults:

```xml
<ActionLink>
              <Action>0</Action>
            </ActionLink>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ActionList

Source: properties-toolone.xml:7998. Captured owning templates: `Actions`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Actions` | Vector |  |  |  |
| `Actions/Item/Action` | AutoCreateAsset |  | AllowedTemplates=ActionLink; AllowedProperties=Action |  |

Explicit property defaults:

```xml
<ActionList>
              <Actions/>
            </ActionList>
```

Container defaults (entry contents):

```xml
<ActionList>
              <Actions>
                <Action>
                  <Template>ActionLink</Template>
                  <Values>
                    <ActionLink/>
                  </Values>
                </Action>
              </Actions>
            </ActionList>
```

### ActionLockAsset

Source: properties-toolone.xml:6714. Captured owning templates: `ActionLockAsset`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `LockAssets` | Vector |  |  |  |
| `LockAssets/Item/Asset` | Asset |  |  |  |

Explicit property defaults:

```xml
<ActionLockAsset>
                  <LockAssets/>
                </ActionLockAsset>
```

Container defaults (entry contents):

```xml
<ActionLockAsset>
                  <LockAssets>
                    <Asset>0</Asset>
                  </LockAssets>
                </ActionLockAsset>
```

### ActionRegisterTrigger

Source: properties-toolone.xml:6903. Captured owning templates: `ActionRegisterTrigger`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TriggerAsset` | Asset |  | NeededProperty=Trigger |  |
| `UnregisterTrigger` | Boolean |  |  | If false, the trigger will be created. CAUTION: If it is already created it will be reset to its origin state. If true, the trigger will be unregistered instead of registered |
| `InheritArea` | Boolean |  |  | Set to true if you want the area by the paren Quest/Trigger to be passed on to the newly registered trigger |

Explicit property defaults:

```xml
<ActionRegisterTrigger>
                  <TriggerAsset>0</TriggerAsset>
                </ActionRegisterTrigger>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ActionResetTrigger

Source: properties-toolone.xml:6973. Captured owning templates: `ActionResetTrigger`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ActionResetTrigger/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ActionSpawnObjects

Source: properties-toolone.xml:7161. Captured owning templates: `ActionSpawnObjects`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `SpawnGUID` | Asset |  |  |  |
| `Amount` | Integer |  | Min=1 |  |
| `SpawnInfolayer` | Asset |  | NeededProperty=InfoLayerIcon | spawned objects will show this infolayer |
| `Highlight` | Boolean |  |  | Highlights the spawn assets with an outline |
| `SpawnContextObjectLabel` | String |  |  |  |
| `RandomRotation` | Boolean |  |  |  |
| `OwnerIsProcessingParticipant` | Boolean |  |  |  |
| `Owner` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  |  |
| `DoSetVisualSpawnOwner` | Boolean |  |  | If true, you will visually override the owner of the object, i.e. the object looks as if it belongs to a different player. If false, visual owner is the same as the real owner |
| `VisualSpawnOwner` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | Visually override the owner of the object, i.e. the object looks as if it belongs to a different player. If false, visual owner is the same as the real owner |
| `SpawnObjectGroupLabel` | String |  |  | If a text is given the spawned object will be added to a group with the text as label. If the group did not exist before, it will be created |

Explicit property defaults:

```xml
<ActionSpawnObjects>
                  <SpawnGUID>0</SpawnGUID>
                  <SpawnInfolayer>0</SpawnInfolayer>
                  <Owner>Human0</Owner>
                  <VisualSpawnOwner>Human0</VisualSpawnOwner>
                </ActionSpawnObjects>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ActionStartQuest

Source: properties-toolone.xml:7319. Captured owning templates: `ActionStartQuest`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Quest` | Quest |  | NeededProperty=Quest |  |
| `InheritQuestArea` | Boolean |  |  | Indicates whether the action should pass on the quest area of the the quest assigned to this action |
| `InheritQuestSession` | Boolean |  |  | Indicates whether the action should pass on the quest session of the the quest assigned to this action |
| `InheritQuestObjects` | Boolean |  |  | Inherits the list of all objects that were related to that quest, so they can be used by object actions |
| `UseCurrentSession` | Boolean |  |  | Indicates whether the quest should be spawned for the session where the current player is in |
| `QuestSession` | Asset |  | NeededProperty=Session;Region | The session where this quest should be started or a region(= list of sessions) where a session is randomly chosen from if the player entered that session already |
| `GetQuestSessionFromArea` | Boolean |  |  | If true the session is determined by the given area. Needs an area to be set and also InheritQuestArea needs to be set! |

Explicit property defaults:

```xml
<ActionStartQuest>
                  <Quest>0</Quest>
                  <QuestSession>0</QuestSession>
                </ActionStartQuest>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ActionUnlockAsset

Source: properties-toolone.xml:7487. Captured owning templates: `ActionUnlockAsset`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `UnlockAssets` | Vector |  |  | Assets get unlocked |
| `UnlockAssets/Item/Asset` | Asset |  | NeededProperty=Locked;AssetPool |  |
| `UnhideAssets` | Vector |  |  | Assets get visible |
| `UnhideAssets/Item/Asset` | Asset |  | NeededProperty=Locked;AssetPool |  |
| `UnlockGroups` | Vector |  |  | Assets in these groups get unlocked  |
| `UnlockGroups/Item/Group` | QuestGroup |  |  |  |
| `UnhideGroups` | Vector |  |  | Assets in these groups get visible |
| `UnhideGroups/Item/Group` | QuestGroup |  |  |  |

Explicit property defaults:

```xml
<ActionUnlockAsset>
                  <UnlockAssets/>
                  <UnhideAssets/>
                  <UnlockGroups/>
                  <UnhideGroups/>
                </ActionUnlockAsset>
```

Container defaults (entry contents):

```xml
<ActionUnlockAsset>
                  <UnlockAssets>
                    <Asset>0</Asset>
                  </UnlockAssets>
                  <UnhideAssets>
                    <Asset>0</Asset>
                  </UnhideAssets>
                </ActionUnlockAsset>
```

### Condition

Serp clarification (2026-10-03): the original descriptions below remain verbatim evidence. For construction, a parent condition gates subordinate execution even with MutuallyExclusive; choose the first matching complete branch from top to bottom. Serp assesses IsOptional on an owning main without a parent as ineffective and harmless. See [design rules and certainty](triggers.md#subtrigger-timing-and-actions).

Source: properties-toolone.xml:3682. Captured owning templates: `ConditionActiveRegion`, `ConditionActiveSession`, `ConditionAlwaysFalse`, `ConditionAlwaysTrue`, `ConditionAreaClaimed`, `ConditionAttractiveness`, `ConditionBuildingsInBlueprintmode`, `ConditionBurningObject`, `ConditionBusActivationNeedSaturation`, `ConditionCameraMovement`, `ConditionCorporationDifficulty`, `ConditionDecision`, `ConditionDecisionOption`, `ConditionDiplomaticState`, `ConditionDiplomaticStateChanged`, `ConditionEvaluateTextSource`, `ConditionEvent`, `ConditionExpeditionFinished`, `ConditionExportGoodsLeveled`, `ConditionFactoryProductivity`, `ConditionFestival`, `ConditionFiniteResource`, `ConditionFirstTimeEventHappened`, `ConditionGUIEvent`, `ConditionGameEnded`, `ConditionGamePadAction`, `ConditionHaciendaDecreesActive`, `ConditionHaciendaModuleCount`, `ConditionHappinessMood`, `ConditionInPalaceRange`, `ConditionInStorage`, `ConditionIrrigatedModules`, `ConditionIrrigationCapacityExceeded`, `ConditionIsBuffed`, `ConditionIsCampaign`, `ConditionIsCraftingInProgress`, `ConditionIsCreativeMode`, `ConditionIsDLCActive`, `ConditionIsDiscovered`, `ConditionIsDocklandsExportPyramidFull`, `ConditionIsGamepadMode`, `ConditionIsIndustrialized`, `ConditionIsMultiplayer`, `ConditionIsParticipantInGame`, `ConditionIsPaused`, `ConditionIsTutorial`, `ConditionIslandsDiscovered`, `ConditionIslandsWithFertility`, `ConditionMetagameLoaded`, `ConditionModuleCount`, `ConditionMonoCulture`, `ConditionMonumentEventActive`, `ConditionMonumentProgress`, `ConditionMoveVehicle`, `ConditionMutualAreaInSubconditions`, `ConditionNewspaperPossible`, `ConditionNewspaperPublished`, `ConditionObjHPCheck`, `ConditionObjectPosition`, `ConditionObjectSelected`, `ConditionOverlapsAABB`, `ConditionPalaceItemEquipBonusActive`, `ConditionPalaceUnlocks`, `ConditionPhotographyObject`, `ConditionPlayerCounter`, `ConditionProductCapacityReached`, `ConditionProductivity`, `ConditionQuestPoolQuestRunning`, `ConditionQuestResolveConfirmation`, `ConditionQuestState`, `ConditionRecipeResearchCompleted`, `ConditionReputation`, `ConditionResearchPointLimitReached`, `ConditionResidentsInBuilding`, `ConditionSeason`, `ConditionSelectionHappinessDebuffActive`, `ConditionSessionLoading`, `ConditionShipsInRange`, `ConditionShipsOwnedInSession`, `ConditionShipyardState`, `ConditionStarterObject`, `ConditionStaticResult`, `ConditionTextPopupClosed`, `ConditionTextPopupPagesViewed`, `ConditionThreshold`, `ConditionTimePassed`, `ConditionTimer`, `ConditionTradeRouteCount`, `ConditionTutorialInteraction`, `ConditionUnlocked`, `ConditionUnlockedList`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `SubConditionCompletionOrder` | Choice | [SubConditionCompletionOrder](trigger-datasets.md#subconditioncompletionorder) |  | Parallel: All sub conditions can be solved at any time. Linear: The sub conditions have to be completed in order. Mutually Exclusive: Only one sub condition has to be completed and the sub conditions are solvable before the main condition. |
| `IsOptional` | Boolean |  |  | Set to true, if it is not needed to satisfy this condition to satisfy the parent condition |
| `LinkAllActionsToQuest` | Boolean |  |  |  |

Explicit property defaults:

```xml
<Condition>
              <SubConditionCompletionOrder>Parallel</SubConditionCompletionOrder>
            </Condition>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionActiveRegion

Source: properties-toolone.xml:1382. Captured owning templates: `ConditionActiveRegion`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ActiveRegion` | Asset |  | NeededProperty=Region | The region from which a session has to be active. If no region is given then any active session triggers this condition. |

Explicit property defaults:

```xml
<ConditionActiveRegion>
                  <ActiveRegion>0</ActiveRegion>
                </ConditionActiveRegion>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionActiveSession

Source: properties-toolone.xml:1391. Captured owning templates: `ConditionActiveSession`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ActiveSession` | Asset |  | NeededProperty=Session;Sector | The session which has to be active. If no session is given then any session triggers this condition. |
| `ConditionActiveSessionUseActiveSession` | Boolean |  |  | Will override ActiveSession |
| `SessionBlacklist` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionActiveSession>
                  <ActiveSession>0</ActiveSession>
                </ConditionActiveSession>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionAlwaysFalse

Source: properties-toolone.xml:1410. Captured owning templates: `ConditionAlwaysFalse`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionAlwaysFalse/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionAlwaysTrue

Source: properties-toolone.xml:1413. Captured owning templates: `ConditionAlwaysTrue`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionAlwaysTrue/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionAreaClaimed

Source: properties-toolone.xml:1416. Captured owning templates: `ConditionAreaClaimed`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Island` | Asset |  | NeededProperty=Island | which construction area |
| `Claimed` | Boolean |  |  | Condition is valid if claimed status matches |

Explicit property defaults:

```xml
<ConditionAreaClaimed>
                  <Island>0</Island>
                </ConditionAreaClaimed>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionAttractiveness

Source: properties-toolone.xml:1430. Captured owning templates: `ConditionAttractiveness`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `AttractivenessNeed` | Integer |  |  |  |
| `AttractivenessComparisonOp` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `AttractivenessType` | Choice | [AttractivityType](trigger-datasets.md#attractivitytype) |  |  |
| `CountAllTypes` | Boolean |  |  |  |
| `AttractivenessSessionOrRegion` | Asset |  | NeededProperty=Session;Region |  |
| `AttractivenessCheckSpecificBuilding` | Boolean |  |  | If true, AttractivenessSpecificBuilding will be considered |
| `AttractivenessSpecificBuilding` | Asset |  |  | A specific building that is checked for its attractiveness |

Explicit property defaults:

```xml
<ConditionAttractiveness>
                  <AttractivenessComparisonOp>AtLeast</AttractivenessComparisonOp>
                  <AttractivenessType>Culture</AttractivenessType>
                  <AttractivenessSessionOrRegion>0</AttractivenessSessionOrRegion>
                  <AttractivenessSpecificBuilding>0</AttractivenessSpecificBuilding>
                </ConditionAttractiveness>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionBuildingsInBlueprintmode

Source: properties-toolone.xml:1466. Captured owning templates: `ConditionBuildingsInBlueprintmode`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `BuildingCount` | Integer |  |  |  |
| `BlueprintBuildingType` | Asset |  |  | If this is set to something other than Invalid GUID, it will only count the blueprints for that procided GUID |

Explicit property defaults:

```xml
<ConditionBuildingsInBlueprintmode/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionBurningObject

Source: properties-toolone.xml:1478. Captured owning templates: `ConditionBurningObject`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `BurningObjects` | Vector |  |  |  |
| `BurningObjects/Item/BurningObjectGUID` | Asset |  |  |  |

Explicit property defaults:

```xml
<ConditionBurningObject>
                  <BurningObjects/>
                </ConditionBurningObject>
```

Container defaults (entry contents):

```xml
<ConditionBurningObject>
                  <BurningObjects>
                    <BurningObjectGUID>0</BurningObjectGUID>
                  </BurningObjects>
                </ConditionBurningObject>
```

### ConditionBusActivationNeedSaturation

Source: properties-toolone.xml:1491. Captured owning templates: `ConditionBusActivationNeedSaturation`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ObjectAmountComparisonOP` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  | Comparison Operator for the Amount of Objects that fulfill the configured need |
| `ObjectAmountThreshold` | Integer |  | Min=0 | Amount of Objects to fulfill the overall condition |
| `NeedsToCheck` | Vector |  |  | The needs that needs to be fulfilled per object |
| `NeedsToCheck/Item/GUID` | Asset |  |  |  |
| `NeedsToCheck/Item/ComparisonOP` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `NeedsToCheck/Item/Threshold` | Integer |  | Min=0; Max=100 |  |
| `NeedsRangeOP` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  |  |

Explicit property defaults:

```xml
<ConditionBusActivationNeedSaturation>
                  <ObjectAmountComparisonOP>AtLeast</ObjectAmountComparisonOP>
                  <NeedsToCheck/>
                  <NeedsRangeOP>None</NeedsRangeOP>
                </ConditionBusActivationNeedSaturation>
```

Container defaults (entry contents):

```xml
<ConditionBusActivationNeedSaturation>
                  <NeedsToCheck>
                    <GUID>0</GUID>
                    <ComparisonOP>AtLeast</ComparisonOP>
                  </NeedsToCheck>
                </ConditionBusActivationNeedSaturation>
```

### ConditionCameraMovement

Source: properties-toolone.xml:1533. Captured owning templates: `ConditionCameraMovement`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `CameraMovementComparator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `CameraMovementActionToTrack` | Flags | [CameraMovementAction](trigger-datasets.md#cameramovementaction) |  |  |
| `CameraMovementDistance` | Float |  |  | Distance is in meters |
| `StartDistanceTrackingOnFirstEvaluation` | Boolean |  |  | Should the distance of the camera action be tracked when the condition was evaluated for the first time or when the tracking for this participant started. |

Explicit property defaults:

```xml
<ConditionCameraMovement>
                  <CameraMovementComparator>AtLeast</CameraMovementComparator>
                  <CameraMovementActionToTrack>Economy</CameraMovementActionToTrack>
                </ConditionCameraMovement>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionCorporationDifficulty

Source: properties-toolone.xml:1556. Captured owning templates: `ConditionCorporationDifficulty`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Difficulty` | Flags | [CorporationDifficulty](trigger-datasets.md#corporationdifficulty) |  |  |
| `DifficultyConstructionCostRefund` | Flags | [DCConstructionCostRefund](trigger-datasets.md#dcconstructioncostrefund) |  |  |
| `DifficultyLossCondition` | Flags | [DCLossCondition](trigger-datasets.md#dclosscondition) |  |  |
| `DifficultyOptionalQuestFrequency` | Flags | [DCOptionalQuestFrequency](trigger-datasets.md#dcoptionalquestfrequency) |  |  |
| `DifficultyOptionalQuestRewards` | Flags | [DCOptionalQuestRewards](trigger-datasets.md#dcoptionalquestrewards) |  |  |
| `DifficultyRelocateBuildings` | Flags | [DCRelocateBuildings](trigger-datasets.md#dcrelocatebuildings) |  |  |
| `DifficultyRevenue` | Flags | [DCRevenue](trigger-datasets.md#dcrevenue) |  |  |
| `DifficultyStartCredits` | Flags | [DCStartCredits](trigger-datasets.md#dcstartcredits) |  |  |
| `DifficultyStartShips` | Flags | [DCStartShips](trigger-datasets.md#dcstartships) |  |  |
| `DifficultyStartWithKontor` | Flags | [DCStartWithKontor](trigger-datasets.md#dcstartwithkontor) |  |  |

Explicit property defaults:

```xml
<ConditionCorporationDifficulty>
                  <Difficulty/>
                  <DifficultyConstructionCostRefund/>
                  <DifficultyLossCondition/>
                  <DifficultyOptionalQuestFrequency/>
                  <DifficultyOptionalQuestRewards/>
                  <DifficultyRelocateBuildings/>
                  <DifficultyRevenue/>
                  <DifficultyStartCredits/>
                  <DifficultyStartShips/>
                  <DifficultyStartWithKontor/>
                </ConditionCorporationDifficulty>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionDecision

Source: properties-toolone.xml:1609. Captured owning templates: `ConditionDecision`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `DecisionFluffText` | Text |  | NeededProperty=Text | The decision text displayed to the user to describe what decision to take |
| `DecisionPortrait` | Asset |  | NeededProperty=Portrait | The portrait that should be displayed in the decision popup |
| `DecisionOptionList` | Vector |  |  | The list of options to choose from |
| `DecisionOptionList/Item/DecisionOption` | AutoCreateAsset |  | AllowedTemplates=ConditionDecisionOption; AllowedProperties= |  |

Explicit property defaults:

```xml
<ConditionDecision>
                  <DecisionFluffText>0</DecisionFluffText>
                  <DecisionPortrait>0</DecisionPortrait>
                  <DecisionOptionList/>
                </ConditionDecision>
```

Container defaults (entry contents):

```xml
<ConditionDecision>
                  <DecisionOptionList>
                    <DecisionOption>
                      <Template>ConditionDecisionOption</Template>
                      <Values>
                        <Condition/>
                        <ConditionDecisionOption>
                          <ActionList>
                            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                            <Template>Actions</Template>
                            <Values>
                              <ActionList/>
                            </Values>
                          </ActionList>
                          <DecisionNotification>
                            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                            <Template>CharacterNotification</Template>
                            <Values>
                              <CharacterNotification/>
                              <BaseNotification/>
                              <NotificationSubtitle/>
                            </Values>
                          </DecisionNotification>
                        </ConditionDecisionOption>
                      </Values>
                    </DecisionOption>
                  </DecisionOptionList>
                </ConditionDecision>
```

### ConditionDecisionOption

Source: properties-toolone.xml:1637. Captured owning templates: `ConditionDecisionOption`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `DecisionOptionText` | Text |  | NeededProperty=Text | The text displayed on the decision button that describes the decision option |
| `DecisionOptionInfotip` | Text |  |  |  |
| `ActionList` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | A list of actions that should be executed when the user chose this option |
| `UnlockRequirements` | Vector |  |  | A list of assets that need to be unlocked to be able to choose this decision option |
| `UnlockRequirements/Item/RequiredUnlock` | Asset |  | NeededProperty=Locked |  |
| `UnlockInfotipDescription` | Text |  | NeededProperty=Text | Infotip text that is displayed when this option is locked |
| `HideDecisionPanelAfterChoice` | Boolean |  |  | Indicates whether the decision popup should close after this option was taken |
| `FollowUpDecisionList` | Vector |  |  | A list of follow up decisions that will be a result of this decision option |
| `FollowUpDecisionList/Item/FollowUpDecision` | AutoCreateAsset |  | AllowedTemplates=ConditionDecision; AllowedProperties= |  |
| `HasDecisionCostBehavior` | Boolean |  |  | If true, any ActionAddGoodsToItemContainer in the action list would be evaluated and following things happen: 1. Decision gets disabled if player could not pay the resources 2. Resource requirements will be shown in infotip |
| `HasNotification` | Boolean |  |  | If true, triggers the DecisionNotification when the decision option was chosen |
| `DecisionNotification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= | Will get triggered when this decision option was chosen and HasNotification is true |
| `ShowDecisionBuffs` | Boolean |  |  | If true, buff icons with infotip will be shown for each buff action in the action list |

Explicit property defaults:

```xml
<ConditionDecisionOption>
                  <DecisionOptionText>0</DecisionOptionText>
                  <DecisionOptionInfotip>0</DecisionOptionInfotip>
                  <ActionList>
                    <Template>Actions</Template>
                    <Values>
                      <ActionList/>
                    </Values>
                  </ActionList>
                  <UnlockRequirements/>
                  <UnlockInfotipDescription>0</UnlockInfotipDescription>
                  <FollowUpDecisionList/>
                  <DecisionNotification>
                    <Template>CharacterNotification</Template>
                    <Values>
                      <CharacterNotification/>
                      <BaseNotification/>
                      <NotificationSubtitle/>
                    </Values>
                  </DecisionNotification>
                  <ShowDecisionBuffs>1</ShowDecisionBuffs>
                </ConditionDecisionOption>
```

Container defaults (entry contents):

```xml
<ConditionDecisionOption>
                  <UnlockRequirements>
                    <RequiredUnlock>0</RequiredUnlock>
                  </UnlockRequirements>
                  <FollowUpDecisionList>
                    <FollowUpDecision>
                      <Template>ConditionDecision</Template>
                      <Values>
                        <Condition/>
                        <ConditionDecision/>
                      </Values>
                    </FollowUpDecision>
                  </FollowUpDecisionList>
                </ConditionDecisionOption>
```

### ConditionDiplomaticState

Source: properties-toolone.xml:1715. Captured owning templates: `ConditionDiplomaticState`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `SourceIsQuestOwner2` | Boolean |  |  | When true, the source participant is overriden by the quest owner |
| `SourceParticipant2` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  |  |
| `TargetIsQuestOwner2` | Boolean |  |  | When true, the target participant is overriden by the quest owner |
| `TargetParticipant2` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  |  |
| `DesiredState` | Choice | [DiplomacyState](trigger-datasets.md#diplomacystate) |  |  |
| `IgnoreTeamAlliance` | Boolean |  |  | Indicates whether an alliance state should be considered when the two participants started the game as a team (in multiplayer) |

Explicit property defaults:

```xml
<ConditionDiplomaticState>
                  <SourceParticipant2>Human0</SourceParticipant2>
                  <TargetParticipant2>Human0</TargetParticipant2>
                  <DesiredState>War</DesiredState>
                </ConditionDiplomaticState>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionDiplomaticStateChanged

Source: properties-toolone.xml:1748. Captured owning templates: `ConditionDiplomaticStateChanged`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `AllianceCount` | Integer |  |  |  |

Explicit property defaults:

```xml
<ConditionDiplomaticStateChanged/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionEvaluateTextSource

Source: properties-toolone.xml:1755. Captured owning templates: `ConditionEvaluateTextSource`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TextSourceString` | String |  |  | The textsource that should be evaluated for this condition |
| `ComparisonType` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  | [only used when textsource returns a number] Type of comparison you want to apply to the result |
| `ComparisonValue` | Float |  |  | [only used when textsource returns a number] The value you want to comparte the result to |

Explicit property defaults:

```xml
<ConditionEvaluateTextSource>
                  <ComparisonType>AtLeast</ComparisonType>
                </ConditionEvaluateTextSource>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionEvent

Source: properties-toolone.xml:1774. Captured owning templates: `ConditionEvent`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ConditionEvent` | Choice | [SimpleEventType](trigger-datasets.md#simpleeventtype) |  | The type of event that will be watched by this condition |
| `ContextData` | String |  |  | A context string that defines additional information about the event (e.g. the GUID of an asset if the event type is Object_Destroyed) |
| `ContextAsset` | Asset |  |  | A context GUID that defines additional information about the event |
| `ContextAssetInfolayer` | Asset |  |  |  |
| `EventCount` | Integer |  |  | The number of events of this type that should be called. Usually 1 |

Explicit property defaults:

```xml
<ConditionEvent>
                  <ConditionEvent>SessionLoad</ConditionEvent>
                  <ContextAsset>0</ContextAsset>
                  <ContextAssetInfolayer>0</ContextAssetInfolayer>
                </ConditionEvent>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionExpeditionFinished

Source: properties-toolone.xml:1804. Captured owning templates: `ConditionExpeditionFinished`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Morale` | Integer |  |  |  |
| `MoraleComparisonOperator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |

Explicit property defaults:

```xml
<ConditionExpeditionFinished>
                  <MoraleComparisonOperator>AtLeast</MoraleComparisonOperator>
                </ConditionExpeditionFinished>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionExportGoodsLeveled

Source: properties-toolone.xml:1816. Captured owning templates: `ConditionExportGoodsLeveled`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ExportLevelComparisonOp` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `ExportLevelDesiredAmount` | Integer |  |  |  |
| `UpgradesRelativeToQuestStart` | Boolean |  |  |  |
| `ExportLevelToCheck` | Choice | [ExportLevel](trigger-datasets.md#exportlevel) |  |  |

Explicit property defaults:

```xml
<ConditionExportGoodsLeveled>
                  <ExportLevelComparisonOp>AtLeast</ExportLevelComparisonOp>
                  <ExportLevelDesiredAmount>1</ExportLevelDesiredAmount>
                  <ExportLevelToCheck>Uncommon</ExportLevelToCheck>
                </ConditionExportGoodsLeveled>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionFactoryProductivity

Source: properties-toolone.xml:1837. Captured owning templates: `ConditionFactoryProductivity`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ProductivityComparison` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `ProductivityThreshold` | Integer |  | Min=0; Max=100 |  |

Explicit property defaults:

```xml
<ConditionFactoryProductivity>
                  <ProductivityComparison>AtLeast</ProductivityComparison>
                </ConditionFactoryProductivity>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionFestival

Source: properties-toolone.xml:1851. Captured owning templates: `ConditionFestival`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `CheckFestival` | Choice | [FestivalType](trigger-datasets.md#festivaltype) |  |  |
| `CheckForActive` | Boolean |  |  | Set to false to check if the festival has ended (is not active) |
| `IgnoreType` | Boolean |  |  | Don't care for the type of the festival, just check if any or none festival is active |

Explicit property defaults:

```xml
<ConditionFestival>
                  <CheckFestival>BeerFestival</CheckFestival>
                </ConditionFestival>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionFiniteResource

Source: properties-toolone.xml:1869. Captured owning templates: `ConditionFiniteResource`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `CheckResourceTypes` | Flags | [ResourceType](trigger-datasets.md#resourcetype) |  |  |
| `ResourceAmountComp` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `ResourceAmountRemaining` | Integer |  |  |  |

Explicit property defaults:

```xml
<ConditionFiniteResource>
                  <CheckResourceTypes/>
                  <ResourceAmountComp>AtLeast</ResourceAmountComp>
                </ConditionFiniteResource>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionFirstTimeEventHappened

Source: properties-toolone.xml:1887. Captured owning templates: `ConditionFirstTimeEventHappened`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `SpecificAsset` | Asset |  |  |  |

Explicit property defaults:

```xml
<ConditionFirstTimeEventHappened>
                  <SpecificAsset>0</SpecificAsset>
                </ConditionFirstTimeEventHappened>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionGUIEvent

Source: properties-toolone.xml:1939. Captured owning templates: `ConditionGUIEvent`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `UIEventType` | Choice | [GUIEventType](trigger-datasets.md#guieventtype) |  |  |
| `StateToCheck` | Choice | [GUIState](trigger-datasets.md#guistate) |  |  |

Explicit property defaults:

```xml
<ConditionGUIEvent>
                  <UIEventType>Enter</UIEventType>
                  <StateToCheck>Video</StateToCheck>
                </ConditionGUIEvent>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionGameEnded

Source: properties-toolone.xml:1894. Captured owning templates: `ConditionGameEnded`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `WinLoseState` | Choice | [WinLoseState](trigger-datasets.md#winlosestate) |  |  |

Explicit property defaults:

```xml
<ConditionGameEnded>
                  <WinLoseState>Win</WinLoseState>
                </ConditionGameEnded>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionGamePadAction

Source: properties-toolone.xml:1902. Captured owning templates: `ConditionGamePadAction`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `GamePadActionComparator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `GamePadActionToTrack` | Choice | [GamepadAction](trigger-datasets.md#gamepadaction) |  |  |
| `GamePadActionTriggeredAmount` | Integer |  |  |  |
| `StartAmountTrackingOnFirstEvaluation` | Boolean |  |  | Should the number of times the game pad action is pressed be tracked when the condition was evaluated for the first time or when the tracking for this participant started. |

Explicit property defaults:

```xml
<ConditionGamePadAction>
                  <GamePadActionComparator>AtLeast</GamePadActionComparator>
                  <GamePadActionToTrack>ChangeTabLeft</GamePadActionToTrack>
                </ConditionGamePadAction>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionGoodsInRange

Source: properties-toolone.xml:1924. Captured owning templates: none; schema-only in this template set. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `GoodsInRangeType` | Choice | [GoodsInRangeType](trigger-datasets.md#goodsinrangetype) |  | The type of goodsInRange check that should be performed. See Dataset entries for more information |
| `AllowKontors` | Boolean |  |  | True if ships and kontors are valid to bring goods in range, False if only ships can do so |

Explicit property defaults:

```xml
<ConditionGoodsInRange>
                  <GoodsInRangeType>TargetObject</GoodsInRangeType>
                </ConditionGoodsInRange>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionHaciendaDecreesActive

Source: properties-toolone.xml:1952. Captured owning templates: `ConditionHaciendaDecreesActive`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ActiveDecrees` | Flags | [MinistryDecreeTier](trigger-datasets.md#ministrydecreetier) |  |  |
| `DecreesRangeOp` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  |  |

Explicit property defaults:

```xml
<ConditionHaciendaDecreesActive>
                  <ActiveDecrees/>
                  <DecreesRangeOp>None</DecreesRangeOp>
                </ConditionHaciendaDecreesActive>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionHaciendaModuleCount

Source: properties-toolone.xml:1965. Captured owning templates: `ConditionHaciendaModuleCount`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `HaciendaModuleCount` | Integer |  |  |  |
| `HaciendaModuleOperator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |

Explicit property defaults:

```xml
<ConditionHaciendaModuleCount>
                  <HaciendaModuleOperator>AtLeast</HaciendaModuleOperator>
                </ConditionHaciendaModuleCount>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionHappinessMood

Source: properties-toolone.xml:1977. Captured owning templates: `ConditionHappinessMood`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `RequiredLevel` | Flags | [HappinessState](trigger-datasets.md#happinessstate) |  |  |
| `UseProcessingParticipant_chl` | Boolean |  |  | Indicates whether the participants should be chosen dynamically by the current context (e.g. quest asignee) |
| `Participant_chl` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  |  |
| `PopulationLevel` | Asset |  | NeededProperty=PopulationLevel7 |  |

Explicit property defaults:

```xml
<ConditionHappinessMood>
                  <RequiredLevel/>
                  <UseProcessingParticipant_chl>1</UseProcessingParticipant_chl>
                  <Participant_chl>Human0</Participant_chl>
                  <PopulationLevel>0</PopulationLevel>
                </ConditionHappinessMood>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionInPalaceRange

Source: properties-toolone.xml:2000. Captured owning templates: `ConditionInPalaceRange`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `InRangeList` | Vector |  |  | List of assets that should be checked to be in range |
| `InRangeList/Item/BuildingAsset` | Asset |  |  | The building or pool asset that should be checked to be in range. |
| `CheckAny` | Boolean |  |  | Indicates whether any or all elements in the InRangeList must be in palace range for this condition to be fulfilled |

Explicit property defaults:

```xml
<ConditionInPalaceRange>
                  <InRangeList/>
                </ConditionInPalaceRange>
```

Container defaults (entry contents):

```xml
<ConditionInPalaceRange>
                  <InRangeList>
                    <BuildingAsset>0</BuildingAsset>
                  </InRangeList>
                </ConditionInPalaceRange>
```

### ConditionInStorage

Source: properties-toolone.xml:2020. Captured owning templates: `ConditionInStorage`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `InStorageGoods` | Vector |  |  | List of goods that are checked by the condition |
| `InStorageGoods/Item/Product` | Asset |  | NeededProperty=Product;Item | The product that gets checked |
| `InStorageGoods/Item/Amount` | Integer |  | Min=0 | The amount of the product that needs to be reached |
| `InStorageCompareOp` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `CheckQuestAreaKontor` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionInStorage>
                  <InStorageGoods/>
                  <InStorageCompareOp>AtLeast</InStorageCompareOp>
                </ConditionInStorage>
```

Container defaults (entry contents):

```xml
<ConditionInStorage>
                  <InStorageGoods>
                    <Product>0</Product>
                  </InStorageGoods>
                </ConditionInStorage>
```

### ConditionIrrigatedModules

Source: properties-toolone.xml:2051. Captured owning templates: `ConditionIrrigatedModules`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `IrrigatedModulesRange` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  | Select range of modules which should be irrigated. CAUTION: Farms without any modules will be ignored in this condition |
| `CheckNonIrrigated` | Boolean |  |  | True, if you want to check the non-irrigated modules instead of the irrigated modules |

Explicit property defaults:

```xml
<ConditionIrrigatedModules>
                  <IrrigatedModulesRange>None</IrrigatedModulesRange>
                </ConditionIrrigatedModules>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIrrigationCapacityExceeded

Source: properties-toolone.xml:2065. Captured owning templates: `ConditionIrrigationCapacityExceeded`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionIrrigationCapacityExceeded/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsBuffed

Source: properties-toolone.xml:2068. Captured owning templates: `ConditionIsBuffed`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Buff` | Asset |  | NeededProperty=Buff |  |
| `RequiredAmount` | Integer |  | Min=1 | The amount of applied buffs required to fulfill this condition |
| `UseEffectHandler` | Boolean |  |  | Instead of checking if Buildings have the specific buff we check the EffectHandler (only used by BuffFactories, ForwardBuffs and AreaBuffs) for a specific buff and count the affected Buildings. This could increase performance when having a lot of potential affected Buildings. |

Explicit property defaults:

```xml
<ConditionIsBuffed>
                  <Buff>0</Buff>
                  <RequiredAmount>1</RequiredAmount>
                </ConditionIsBuffed>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsCampaign

Source: properties-toolone.xml:2088. Captured owning templates: `ConditionIsCampaign`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionIsCampaign/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsCraftingInProgress

Source: properties-toolone.xml:2091. Captured owning templates: `ConditionIsCraftingInProgress`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionIsCraftingInProgress/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsCreativeMode

Source: properties-toolone.xml:2094. Captured owning templates: `ConditionIsCreativeMode`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionIsCreativeMode/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsDLCActive

Source: properties-toolone.xml:2101. Captured owning templates: `ConditionIsDLCActive`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `DLCAssetList` | Vector |  |  | List of DLCs that should be checked for activation |
| `DLCAssetList/Item/DLCAsset` | Asset |  | NeededProperty=UplayProduct |  |

Explicit property defaults:

```xml
<ConditionIsDLCActive>
                  <DLCAssetList/>
                </ConditionIsDLCActive>
```

Container defaults (entry contents):

```xml
<ConditionIsDLCActive>
                  <DLCAssetList>
                    <DLCAsset>0</DLCAsset>
                  </DLCAssetList>
                </ConditionIsDLCActive>
```

### ConditionIsDiscovered

Source: properties-toolone.xml:2097. Captured owning templates: `ConditionIsDiscovered`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionIsDiscovered/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsDocklandsExportPyramidFull

Source: properties-toolone.xml:2116. Captured owning templates: `ConditionIsDocklandsExportPyramidFull`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionIsDocklandsExportPyramidFull/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsGamepadMode

Source: properties-toolone.xml:2119. Captured owning templates: `ConditionIsGamepadMode`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionIsGamepadMode/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsIndustrialized

Source: properties-toolone.xml:2122. Captured owning templates: `ConditionIsIndustrialized`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `IndustrializationDesiredValue` | Integer |  |  |  |
| `IndustrializationComparisonOperator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `CheckIndustrializationTypeInsteadOfObjectFilter` | Boolean |  |  | If true, all objects of a given type will be checked. Otherwise the object filter will be checked |
| `IndustrializationTypeChecked` | Choice | [IndustrializationType](trigger-datasets.md#industrializationtype) |  |  |

Explicit property defaults:

```xml
<ConditionIsIndustrialized>
                  <IndustrializationTypeChecked>Powerplant</IndustrializationTypeChecked>
                  <IndustrializationComparisonOperator>AtLeast</IndustrializationComparisonOperator>
                </ConditionIsIndustrialized>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsMultiplayer

Source: properties-toolone.xml:2211. Captured owning templates: `ConditionIsMultiplayer`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionIsMultiplayer/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsParticipantInGame

Source: properties-toolone.xml:2214. Captured owning templates: `ConditionIsParticipantInGame`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `InGameParticipant` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | Checks if a participant was selected in the game setup. |

Explicit property defaults:

```xml
<ConditionIsParticipantInGame>
                  <InGameParticipant>Human0</InGameParticipant>
                </ConditionIsParticipantInGame>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsPaused

Source: properties-toolone.xml:2223. Captured owning templates: `ConditionIsPaused`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `IsObjectPaused` | Boolean |  |  | True if you want to check for paused buildings, False otherwise |
| `IsPauseRangeOp` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  | Define which of the configured buildings need to match the paused state |

Explicit property defaults:

```xml
<ConditionIsPaused>
                  <IsPauseRangeOp>None</IsPauseRangeOp>
                </ConditionIsPaused>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIsTutorial

Source: properties-toolone.xml:2237. Captured owning templates: `ConditionIsTutorial`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionIsTutorial/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionIslandsDiscovered

Source: properties-toolone.xml:2144. Captured owning templates: `ConditionIslandsDiscovered`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `IslandsDiscoveredComparator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `IslandsDiscoveredAmount` | Integer |  |  |  |
| `IslandsDiscoveredScope` | Choice | [CounterScope](trigger-datasets.md#counterscope) |  |  |
| `IslandsDiscoveredCustomRegion` | Asset |  |  |  |
| `IslandsDiscoveredCustomSession` | Vector |  |  |  |
| `IslandsDiscoveredCustomSession/Item/GUID` | Asset |  |  |  |

Explicit property defaults:

```xml
<ConditionIslandsDiscovered>
                  <IslandsDiscoveredComparator>AtLeast</IslandsDiscoveredComparator>
                  <IslandsDiscoveredScope>Area</IslandsDiscoveredScope>
                  <IslandsDiscoveredCustomRegion>0</IslandsDiscoveredCustomRegion>
                  <IslandsDiscoveredCustomSession/>
                </ConditionIslandsDiscovered>
```

Container defaults (entry contents):

```xml
<ConditionIslandsDiscovered>
                  <IslandsDiscoveredCustomSession>
                    <GUID>0</GUID>
                  </IslandsDiscoveredCustomSession>
                </ConditionIslandsDiscovered>
```

### ConditionIslandsWithFertility

Source: properties-toolone.xml:2175. Captured owning templates: `ConditionIslandsWithFertility`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `IslandComparator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `IslandThreshold` | Integer |  | Min=0 |  |
| `FertilityContext` | Asset |  |  |  |
| `IslandScope` | Choice | [CounterScope](trigger-datasets.md#counterscope) |  |  |
| `CustomRegion` | Asset |  |  |  |
| `CustomSessions` | Vector |  |  |  |
| `CustomSessions/Item/GUID` | Asset |  |  |  |

Explicit property defaults:

```xml
<ConditionIslandsWithFertility>
                  <IslandComparator>AtLeast</IslandComparator>
                  <FertilityContext>0</FertilityContext>
                  <IslandScope>Area</IslandScope>
                  <CustomRegion>0</CustomRegion>
                  <CustomSessions/>
                </ConditionIslandsWithFertility>
```

Container defaults (entry contents):

```xml
<ConditionIslandsWithFertility>
                  <CustomSessions>
                    <GUID>0</GUID>
                  </CustomSessions>
                </ConditionIslandsWithFertility>
```

### ConditionItemActionCompleted

Source: properties-toolone.xml:2241. Captured owning templates: none; schema-only in this template set. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionItemActionCompleted/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionItemUsed

Source: properties-toolone.xml:2244. Captured owning templates: none; schema-only in this template set. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TargetItem` | Asset |  |  | Item the player has to activate or to socket |
| `ItemAmount` | Integer |  |  | Amount of items the player has to activate or to socket |
| `ItemTargetObject` | Asset |  |  | At which game objects the item(s) have to be activated/socketed. If nothing is setup here, then it's only checked whether the item(s) have been activated. |
| `ItemNeedsActivation` | Boolean |  |  | True, if the item nees to be equipped AND activated |

Explicit property defaults:

```xml
<ConditionItemUsed>
                  <TargetItem>0</TargetItem>
                  <ItemTargetObject>0</ItemTargetObject>
                </ConditionItemUsed>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionMetagameLoaded

Source: properties-toolone.xml:2267. Captured owning templates: `ConditionMetagameLoaded`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `HumanPlayerCount` | Integer |  |  |  |

Explicit property defaults:

```xml
<ConditionMetagameLoaded/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionModuleBuildingEfficiency

Source: properties-toolone.xml:2274. Captured owning templates: none; schema-only in this template set. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionModuleBuildingEfficiency/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionModuleCount

Source: properties-toolone.xml:2277. Captured owning templates: `ConditionModuleCount`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ModuleComparison` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  | The comparsion that should be used to compare the percentage of modules existing |
| `CheckAbsoluteCount` | Boolean |  |  | Indicates whether an absolute number of modules or a percentage of modules should be checked |
| `ModuleCount` | Integer |  |  |  |
| `RestrictToMandatoryModules` | Boolean |  |  | Indicates whether the absolute module count should be capped at the mandatory amount and ignore addional modules built for visuals |
| `ModulePercentage` | Float |  | Min=0; Max=1 | The percentage (0 = 0%, 1 = 100%) of modules that the current amount should be compared to |
| `RequiresIndustrialization` | Boolean |  |  |  |
| `RequiredIndustrialization` | Choice | [IndustrializationType](trigger-datasets.md#industrializationtype) |  |  |
| `CheckAdditionalModuleOnly` | Boolean |  |  |  |
| `CheckIrrigatedModulesOnly` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionModuleCount>
                  <ModuleComparison>AtLeast</ModuleComparison>
                  <RequiredIndustrialization>Powerplant</RequiredIndustrialization>
                </ConditionModuleCount>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionMonoCulture

Source: properties-toolone.xml:2325. Captured owning templates: `ConditionMonoCulture`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `MonocultureDeltaComp` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `MonocultureDelta` | Float |  |  |  |

Explicit property defaults:

```xml
<ConditionMonoCulture>
                  <MonocultureDeltaComp>AtLeast</MonocultureDeltaComp>
                </ConditionMonoCulture>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionMonumentEventsActive

Source: properties-toolone.xml:2337. Captured owning templates: `ConditionMonumentEventActive`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `MonumentEventsActive` | Vector |  |  |  |
| `MonumentEventsActive/Item/MonumentEventGUID` | Asset |  |  |  |

Explicit property defaults:

```xml
<ConditionMonumentEventsActive>
                  <MonumentEventsActive/>
                </ConditionMonumentEventsActive>
```

Container defaults (entry contents):

```xml
<ConditionMonumentEventsActive>
                  <MonumentEventsActive>
                    <MonumentEventGUID>0</MonumentEventGUID>
                  </MonumentEventsActive>
                </ConditionMonumentEventsActive>
```

### ConditionMonumentProgress

Source: properties-toolone.xml:2350. Captured owning templates: `ConditionMonumentProgress`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `MonumentComparisonOP` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `MonumentProgress` | Integer |  | Min=0; Max=100 |  |

Explicit property defaults:

```xml
<ConditionMonumentProgress>
                  <MonumentComparisonOP>AtLeast</MonumentComparisonOP>
                </ConditionMonumentProgress>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionMoveVehicle

Source: properties-toolone.xml:3995. Captured owning templates: `ConditionMoveVehicle`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `MoveVehicleTargetDistance` | Float |  |  |  |
| `VehicleLabel` | String |  |  | Which vehicle is moved? If left empty, the command vehicle needs to be moved by player command. |

Explicit property defaults:

```xml
<ConditionMoveVehicle/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionMutualAreaInSubconditions

Source: properties-toolone.xml:2364. Captured owning templates: `ConditionMutualAreaInSubconditions`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `UseParentValues` | Boolean |  |  |  |
| `AreaFlags` | Flags | [MutualAreaMask](trigger-datasets.md#mutualareamask) |  | Flags to filter only for certain types of islands |
| `SpecifySession` | Boolean |  |  | True, if the SessionAsset should be evaluated |
| `UseProcessingSession` | Boolean |  |  | True, if only areas of the processing session should be used |
| `SessionAsset` | Asset |  | NeededProperty=Session | If given and SpecifySession is true then only areas of this session are accepted |

Explicit property defaults:

```xml
<ConditionMutualAreaInSubconditions>
                  <AreaFlags/>
                  <SessionAsset>0</SessionAsset>
                </ConditionMutualAreaInSubconditions>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionNewspaperPossible

Source: properties-toolone.xml:2394. Captured owning templates: `ConditionNewspaperPossible`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionNewspaperPossible/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionNewspaperPublished

Source: properties-toolone.xml:2397. Captured owning templates: `ConditionNewspaperPublished`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `PagesReplaced` | Integer |  |  |  |

Explicit property defaults:

```xml
<ConditionNewspaperPublished/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjHPCheck

Source: properties-toolone.xml:2450. Captured owning templates: `ConditionObjHPCheck`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `HPTargetGUID` | Asset |  |  |  |
| `HPTargetOwner` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  |  |
| `HPPercentage` | Float |  | Min=0; Max=1 |  |
| `HPComparison` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `HPUnique` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionObjHPCheck>
                  <HPTargetGUID>0</HPTargetGUID>
                  <HPTargetOwner>Human0</HPTargetOwner>
                  <HPComparison>AtLeast</HPComparison>
                </ConditionObjHPCheck>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjectAnywhere

Source: properties-toolone.xml:1119. Captured owning templates: `ConditionObjectAnywhere`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionObjectAnywhere/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjectClientQuestObject

Source: properties-toolone.xml:1122. Captured owning templates: `ConditionObjectClientQuestObject`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionObjectClientQuestObject/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjectPlayerKontor

Source: properties-toolone.xml:1146. Captured owning templates: `ConditionObjectPlayerKontor`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `PlayerKontorUseQuestArea` | Boolean |  |  | If true, only the Kontor of the current quest area (if any) will be a valid target |

Explicit property defaults:

```xml
<ConditionObjectPlayerKontor/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjectPosition

Source: properties-toolone.xml:2404. Captured owning templates: `ConditionObjectPosition`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Radius` | Float |  |  | an object is considered as at a target if its distance is less than this radius |
| `AllObjects` | Boolean |  |  | is it sufficient to have one of the objects at one of the targets, or are all objects checked? |
| `OnlyOneTarget` | Boolean |  |  | when all objects are checked, do they need to be at the same target object? |
| `ExpectObjectExists` | Boolean |  |  | If existence is expected and the object does not exist, the quest will auto resolve. Otherwise it will wait until the object exists |
| `ExpectTargetExists` | Boolean |  |  | If existence is expected and the target does not exist, the quest will fail. Otherwise it will wait until the target exists |

Explicit property defaults:

```xml
<ConditionObjectPosition/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjectPrebuiltObject

Source: properties-toolone.xml:1154. Captured owning templates: `ConditionObjectPrebuiltObject`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `PrebuiltObject` | Asset |  |  |  |
| `PrebuiltObjectLabel` | String |  |  |  |
| `PrebuiltObjectCheckOwner` | Boolean |  |  | Use together with PrebuiltObject to filter results by owner |
| `PrebuiltUseProcessingParticipant` | Boolean |  |  | Indicates whether the owner should be resolved dynamically by code depending on the context of use |
| `PrebuiltObjectOwner` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | Use together with PrebuiltObject to filter results by owner |
| `PrebuiltObjectSpecifiySession` | Boolean |  |  | Indicates whether the session of the prebuilt object(s) should be specified |
| `PrebuiltObjectUseQuestArea` | Boolean |  |  | If true, only prebuilt objects of the current quest area (if any) will be a valid target |
| `PrebuiltObjectUseProcessingSession` | Boolean |  |  | Indicates that the processing session should be used as constraint for the prebuilt object(s). In quests this is the session where the quest is about to start. |
| `PrebuiltObjectSession` | Asset |  | NeededProperty=Session | Session guid that the prebuilt objects should be looked for in |
| `PrebuiltObjectUseVisibilityAutomatism` | Boolean |  |  | If true the quest will remember the initial object visibility on quest start and set the object to visible. When the quest ends it will restore the initial visibility again. If false, the object visibility is not touched |
| `PrebuiltObjectLimitToQuestObjects` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionObjectPrebuiltObject>
              <PrebuiltObject>0</PrebuiltObject>
              <PrebuiltObjectOwner>Human0</PrebuiltObjectOwner>
              <PrebuiltObjectSession>0</PrebuiltObjectSession>
            </ConditionObjectPrebuiltObject>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjectSelected

Source: properties-toolone.xml:2432. Captured owning templates: `ConditionObjectSelected`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `IgnoreSelectionBeforeActivation` | Boolean |  |  | If true, this condition needs the selection to happen _after_ it was activated (e.g. the parent condition was fulfilled). If false, previous selections also count |
| `UseRuinState` | Choice | [Tristate](trigger-datasets.md#tristate) |  |  |
| `IsInIncident` | Choice | [Tristate](trigger-datasets.md#tristate) |  |  |

Explicit property defaults:

```xml
<ConditionObjectSelected>
                  <UseRuinState>DontCare</UseRuinState>
                  <IsInIncident>DontCare</IsInIncident>
                </ConditionObjectSelected>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjectSpawnedObject

Source: properties-toolone.xml:1211. Captured owning templates: `ConditionObjectSpawnedObject`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ExecutionObject` | Asset |  |  | Accepts Assets and AssetPools |
| `ObjectSpawnArea` | AutoCreateAsset |  | AllowedTemplates=QuestSpawnArea; AllowedProperties= |  |
| `ObjectDespawn` | Choice | [QuestObjectDespawn](trigger-datasets.md#questobjectdespawn) |  |  |
| `ObjectDespawnDelay` | Time |  |  |  |
| `ObjectDamage` | Float |  |  |  |
| `ObjectOwner` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | The owner of the spawned object |
| `SpawnTiming` | Choice | [QuestSpawnTiming](trigger-datasets.md#questspawntiming) |  | Choose the time when these objects should be spawned during the quest |
| `DoSetVisualObjectOwner` | Boolean |  |  | If true, you will visually override the owner of the object, i.e. the object looks as if it belongs to a different player. If false, visual owner is the same as the real owner |
| `VisualObjectOwner` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | Visually override the owner of the object, i.e. the object looks as if it belongs to a different player. If false, visual owner is the same as the real owner |
| `ObjectGroupLabel` | String |  |  | If a text is given the spawned object will be added to a group with the text as label. If the group did not exist before, it will be created |

Explicit property defaults:

```xml
<ConditionObjectSpawnedObject>
              <ExecutionObject>0</ExecutionObject>
              <ObjectSpawnArea>
                <Template>QuestSpawnArea</Template>
                <Values>
                  <SpawnArea/>
                </Values>
              </ObjectSpawnArea>
              <ObjectDespawn>LeaveMap</ObjectDespawn>
              <ObjectOwner>Neutral</ObjectOwner>
              <SpawnTiming>OnQuestActivated</SpawnTiming>
              <VisualObjectOwner>Human0</VisualObjectOwner>
            </ConditionObjectSpawnedObject>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjectStarterObject

Source: properties-toolone.xml:1266. Captured owning templates: `ConditionObjectStarterObject`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionObjectStarterObject/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjectUseDefaultSettings

Source: properties-toolone.xml:1269. Captured owning templates: `ConditionObjectUseDefaultSettings`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionObjectUseDefaultSettings/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionObjectiveSignsAndFeedback

Source: properties-toolone.xml:1125. Captured owning templates: `ConditionObjectClientQuestObject`, `ConditionObjectPlayerKontor`, `ConditionObjectPrebuiltObject`, `ConditionObjectSpawnedObject`, `ConditionObjectStarterObject`, `ConditionObjectiveSignsAndFeedback`, `ObjectFilterWithSignsAndFeedback`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Infolayer` | Asset |  |  | the infolayer icon above the quest object |
| `MinimapToken` | Asset |  | NeededProperty=MinimapTokenSettings |  |
| `ShowMinimapToken` | Boolean |  |  |  |
| `ShowOutline` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionObjectiveSignsAndFeedback>
              <Infolayer>0</Infolayer>
              <MinimapToken>0</MinimapToken>
              <ShowMinimapToken>1</ShowMinimapToken>
            </ConditionObjectiveSignsAndFeedback>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionOverlapsAABB

Source: properties-toolone.xml:2477. Captured owning templates: `ConditionOverlapsAABB`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `AssetA` | Asset |  |  |  |
| `AssetB` | Asset |  |  |  |

Explicit property defaults:

```xml
<ConditionOverlapsAABB>
                  <AssetA>0</AssetA>
                  <AssetB>0</AssetB>
                </ConditionOverlapsAABB>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionPalaceItemEquipBonusActive

Source: properties-toolone.xml:2488. Captured owning templates: `ConditionPalaceItemEquipBonusActive`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `BuildingsWithEffectActive` | Vector |  |  |  |
| `BuildingsWithEffectActive/Item/Building` | Asset |  |  |  |
| `BuildingsWithEffectActive/Item/MinimalAmount` | Integer |  |  |  |
| `AffectedBuildingCount` | Integer |  |  |  |
| `AmountItemsEquipped` | Integer |  |  |  |

Explicit property defaults:

```xml
<ConditionPalaceItemEquipBonusActive>
                  <BuildingsWithEffectActive/>
                </ConditionPalaceItemEquipBonusActive>
```

Container defaults (entry contents):

```xml
<ConditionPalaceItemEquipBonusActive>
                  <BuildingsWithEffectActive>
                    <Building>0</Building>
                  </BuildingsWithEffectActive>
                </ConditionPalaceItemEquipBonusActive>
```

### ConditionPalaceUnlocks

Source: properties-toolone.xml:2513. Captured owning templates: `ConditionPalaceUnlocks`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `CheckMinistryUnlocks` | Flags | [PalaceMinistryType](trigger-datasets.md#palaceministrytype) |  |  |
| `CheckDecreeUnlocks` | Array | [PalaceMinistryType](trigger-datasets.md#palaceministrytype) |  |  |
| `CheckDecreeUnlocks/{dataset key}/DecreeUnlocks` | Flags | [MinistryDecreeTier](trigger-datasets.md#ministrydecreetier) |  |  |

Explicit property defaults:

```xml
<ConditionPalaceUnlocks>
                  <CheckMinistryUnlocks/>
                  <CheckDecreeUnlocks/>
                </ConditionPalaceUnlocks>
```

Container defaults (entry contents):

```xml
<ConditionPalaceUnlocks>
                  <CheckDecreeUnlocks>
                    <DecreeUnlocks/>
                  </CheckDecreeUnlocks>
                </ConditionPalaceUnlocks>
```

### ConditionPhotographObject

Source: properties-toolone.xml:2533. Captured owning templates: `ConditionPhotographyObject`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `StagedPhotography` | FileName |  |  | If set, this picture will be shown instead of the actual screenshot made by the player |
| `CircleAreaPercentage` | Float |  |  | The percentage of the area that the circle around the object has in relation to the total screen space. Toggle quest hint cheat during photography quest to see details |
| `ScreenBorderPercentage` | Float |  |  | The object has to be inside a smaller rectangle than the screen itself. This is the percentage of the area that is reduced from each border to define the inner rectangle |
| `AppearInNewspaperArticle` | Asset |  | NeededProperty=NewspaperArticle;NewspaperSpecialEditionArticle | If any article is selected, this picture will be shown in the given article |
| `ShowHintMarkerWhenOffscreen` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionPhotographObject>
                  <AppearInNewspaperArticle>0</AppearInNewspaperArticle>
                  <ShowHintMarkerWhenOffscreen>1</ShowHintMarkerWhenOffscreen>
                </ConditionPhotographObject>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionPlayerCounter

Source: properties-toolone.xml:2561. Captured owning templates: `ConditionPlayerCounter`, `StatusQuoObjective`, `SustainObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `PlayerCounter` | Choice | [PlayerCounter](trigger-datasets.md#playercounter) |  | The type of this player counter |
| `Context` | Asset |  |  | The context info for the player counter |
| `ContextAllowAny` | Boolean |  |  | If true, all counters will be summed up, ignoring the context |
| `ComparisonOp` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  | The comparison operator for counter value and desired value |
| `CounterAmount` | Int64 |  |  | The desired value the counter should match |
| `CounterScope` | Choice | [CounterScope](trigger-datasets.md#counterscope) |  | The scope of the counter |
| `CounterScopeUseCurrentContext` | Boolean |  |  | Use the processing scope for this counter |
| `CounterScopeUseActiveSession` | Boolean |  |  | Indicates whether the session that is taken as context is the active session of the player |
| `CounterScopeContext` | Asset |  |  | Context information for the counter scope, i.e. GUID of a region or session |
| `CounterScopeKeepFirstFound` | Boolean |  |  | If true, the first time this condition gets evaluated and a scope context was found it will be kept forever (e.g. You don't know in which session this coindition will be started, but once it was started it should keep looking in that session). Otherwise the scope context will be checked continuously (e.g. You want to keep checking in the given session, used for quest preconditions for example) |
| `RelativeToQuestStart` | Boolean |  |  | True: Counting from current condition start - False: Counting from 0. |
| `ShowAbsoluteValues` | Boolean |  |  | If RelativeToQuestStart is set, this value defines if absolute or relative values should be shown |
| `ShowInvertedValues` | Boolean |  |  | Indicates whether the player counter values shown in the questtracker should be inverted |
| `CounterValueType` | Choice | [CounterValueType](trigger-datasets.md#countervaluetype) |  | Defines if the MIN the MAX or the CURRENT value should be returned. |
| `CheckSpecificParticipant` | Boolean |  |  | If true, not the condition owner will be checked but the participant that is specified under &lt;CheckedParticipant&gt; |
| `CheckedParticipant` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | if &lt;CheckSpecificParticipant&gt; is true, then this defines the participant to check |

Explicit property defaults:

```xml
<ConditionPlayerCounter>
                  <PlayerCounter>ObjectBuilt</PlayerCounter>
                  <Context>0</Context>
                  <ComparisonOp>AtLeast</ComparisonOp>
                  <CounterScope>Global</CounterScope>
                  <CounterScopeUseCurrentContext>1</CounterScopeUseCurrentContext>
                  <CounterScopeContext>0</CounterScopeContext>
                  <CounterScopeKeepFirstFound>1</CounterScopeKeepFirstFound>
                  <CounterValueType>Current</CounterValueType>
                  <CheckedParticipant>Human0</CheckedParticipant>
                </ConditionPlayerCounter>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionProductCapacityReached

Source: properties-toolone.xml:2649. Captured owning templates: `ConditionProductCapacityReached`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `cpcr_ProductType` | Asset |  | NeededProperty=Product; |  |
| `cpcr_RangeOp` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  |  |

Explicit property defaults:

```xml
<ConditionProductCapacityReached>
                  <cpcr_ProductType>0</cpcr_ProductType>
                  <cpcr_RangeOp>None</cpcr_RangeOp>
                </ConditionProductCapacityReached>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionProductivity

Source: properties-toolone.xml:2662. Captured owning templates: `ConditionProductivity`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Good_CP` | Asset |  |  | The Good that should be checked |
| `ComparisonMode` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `CheckAbsoluteProduction` | Boolean |  |  |  |
| `ProductivityRequired` | Float |  | Min=0; Max=1 | The required percentage of productivity |
| `ProductionRequired` | Float |  |  | The amount of production per minute of the required good |

Explicit property defaults:

```xml
<ConditionProductivity>
                  <Good_CP>0</Good_CP>
                  <ComparisonMode>AtLeast</ComparisonMode>
                </ConditionProductivity>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionPropsExecutionPlaceSettings

Source: properties-toolone.xml:3702. Captured owning templates: `BringVehicleToObjectObjective`, `DestroyObjective`, `DivingBellObjective`, `EscortObjective`, `ExpeditionObjective`, `HitMovingTargetObjective`, `ItemUsageObjective`, `ModuleBuildingEfficiencyObjective`, `PhotographyObjective`, `PickupObjective`, `PicturePuzzleObjective`, `QuestExecutionPlace`, `SelectObjectObjective`, `SmugglerObjective`, `StatusQuoObjective`, `SustainObjective`, `UseItemInAreaObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ExecutionPlace` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectUseDefaultSettings;ConditionObjectAnywhere;ConditionObjectPlayerKontor;ConditionObjectClientQuestObject;ConditionObjectSpawnedObject;ConditionObjectPrebuiltObject;ObjectFilterWithSignsAndFeedback;ConditionObjectStarterObject; AllowedProperties= |  |
| `ExecutionPlaceText` | Text |  | NeededProperty=Text |  |
| `ExecutionPlaceConfirmOnReached` | Boolean |  |  | if true, triggers a message when goods are delivered that needs to be accepted to continue |
| `ExecutionPlaceAllowedDeliveryObjectLayers` | Flags | [QuestDeliveryObjectLayer](trigger-datasets.md#questdeliveryobjectlayer) |  |  |

Explicit property defaults:

```xml
<ConditionPropsExecutionPlaceSettings>
              <ExecutionPlace>
                <Template>ConditionObjectUseDefaultSettings</Template>
                <Values>
                  <ConditionObjectUseDefaultSettings/>
                </Values>
              </ExecutionPlace>
              <ExecutionPlaceText>0</ExecutionPlaceText>
              <ExecutionPlaceConfirmOnReached>1</ExecutionPlaceConfirmOnReached>
              <ExecutionPlaceAllowedDeliveryObjectLayers>Water;Air</ExecutionPlaceAllowedDeliveryObjectLayers>
            </ConditionPropsExecutionPlaceSettings>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionPropsNegatable

Source: properties-toolone.xml:3726. Captured owning templates: `ConditionDiplomaticState`, `ConditionEvaluateTextSource`, `ConditionEvent`, `ConditionIsBuffed`, `ConditionIsCampaign`, `ConditionIsCreativeMode`, `ConditionIsDLCActive`, `ConditionIsDiscovered`, `ConditionIsGamepadMode`, `ConditionIsMultiplayer`, `ConditionIsParticipantInGame`, `ConditionIsTutorial`, `ConditionObjectPosition`, `ConditionObjectSelected`, `ConditionOverlapsAABB`, `ConditionQuestPoolQuestRunning`, `ConditionUnlocked`, `ModuleBuildingEfficiencyObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `NegateCondition` | Boolean |  |  | Negate the result (success/still checking) of this condition |

Explicit property defaults:

```xml
<ConditionPropsNegatable/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionPropsSessionSettings

Source: properties-toolone.xml:3734. Captured owning templates: `ConditionMoveVehicle`, `ConditionObjectPosition`, `ConditionObjectSelected`, `ConditionSessionLoading`, `ConditionStarterObject`, `DeliveryObjective`, `DestroyObjective`, `EscortObjective`, `HitMovingTargetObjective`, `ItemUsageObjective`, `ModuleBuildingEfficiencyObjective`, `PickupObjective`, `PicturePuzzleObjective`, `SelectObjectObjective`, `SmugglerObjective`, `UseItemInAreaObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionPropsSessionSettings/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestAirdrop

Source: properties-toolone.xml:5406. Captured owning templates: `AirdropObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `DropOnObject` | AutoCreateAsset |  | AllowedTemplates=ObjectFilter | Objects that are checked if they are hit by an air drop action |
| `DropObjectRangeOp` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  | Defines what objects of the DropOnObject list are required for this condition |
| `DroppedProjectile` | Asset |  | NeededProperty=Projectile | The projectile that is required for this condition. Can be a projectile or a pool of projectiles. If left empty: any projectile is accepted |

Explicit property defaults:

```xml
<ConditionQuestAirdrop>
                  <DropObjectRangeOp>None</DropObjectRangeOp>
                </ConditionQuestAirdrop>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestBringVehicleToObject

Source: properties-toolone.xml:4017. Captured owning templates: `BringVehicleToObjectObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `BringToObject` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectClientQuestObject;ConditionObjectPlayerKontor;ConditionObjectPrebuiltObject;ConditionObjectSpawnedObject;ConditionObjectStarterObject; AllowedProperties= |  |
| `VehicleDistance` | Float |  |  | Needed distance between vehicle and context object. If 0 the interaction distance of both objects will be used |
| `ShowConfirmOnReach` | Boolean |  |  | Indicates whether a notification should be triggered once the player reached the target location |

Explicit property defaults:

```xml
<ConditionQuestBringVehicleToObject>
                  <BringToObject>
                    <Template>ConditionObjectClientQuestObject</Template>
                    <Values>
                      <ConditionObjectClientQuestObject/>
                      <ConditionScanner/>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </BringToObject>
                  <ShowConfirmOnReach>1</ShowConfirmOnReach>
                </ConditionQuestBringVehicleToObject>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestBusActivationNeedSaturation

Source: properties-toolone.xml:4036. Captured owning templates: `BusActivationNeedSaturationObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `QuestHotelComparisonOP` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `QuestHotelThreshold` | Integer |  | Min=0 |  |
| `QuestHotelNeed` | Asset |  |  |  |
| `QuestHotelNeedComparisonOP` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `QuestHotelNeedThreshold` | Integer |  | Min=0; Max=100 |  |

Explicit property defaults:

```xml
<ConditionQuestBusActivationNeedSaturation>
                  <QuestHotelComparisonOP>AtLeast</QuestHotelComparisonOP>
                  <QuestHotelNeed>0</QuestHotelNeed>
                  <QuestHotelNeedComparisonOP>AtLeast</QuestHotelNeedComparisonOP>
                </ConditionQuestBusActivationNeedSaturation>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestCameraMovement

Source: properties-toolone.xml:4064. Captured owning templates: `CameraMovementObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `QuestCameraMovementComparator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `QuestCameraMovementActionToTrack` | Flags | [CameraMovementAction](trigger-datasets.md#cameramovementaction) |  |  |
| `QuestCameraMovementDistance` | Float |  |  | Distance is in meters |
| `QuestStartDistanceTrackingOnFirstEvaluation` | Boolean |  |  | Should the distance of the camera action be tracked when the condition was evaluated for the first time or when the tracking for this participant started. |

Explicit property defaults:

```xml
<ConditionQuestCameraMovement>
                  <QuestCameraMovementComparator>AtLeast</QuestCameraMovementComparator>
                </ConditionQuestCameraMovement>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestDecision

Source: properties-toolone.xml:4087. Captured owning templates: `DecisionObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `DecisionBG` | FileName |  |  | The background shown in the decision popup UI |
| `DecisionList` | Vector |  |  | List of decisions to take until the objective is met |
| `DecisionList/Item/Decision` | AutoCreateAsset |  | AllowedTemplates=ConditionDecision; AllowedProperties= |  |
| `NarrativeBook` | Asset |  | NeededProperty=DecisionQuestNarrativeBook |  |
| `AutoAcceptLastDecisionOption` | Boolean |  |  | If true, the last of the current decision options will automatically be chosen when the quest times out or gets cancelled |
| `AutoShowDecisionScreen` | Boolean |  |  | If true, the decision screen will be forced to show when the quest gets active. Caution this might interfere with other menus at that point |
| `HideDecisionScreenCloseButton` | Boolean |  |  | Hides the close button from the decision screen to enforce a decision by the player |
| `SlowDownInDecisionScreen` | Boolean |  |  | If true, the game will slow down as long as the decision screen is opened and continue with normal gamespeed as soon as a decision was made. Does not work in multiplayer matches! |

Explicit property defaults:

```xml
<ConditionQuestDecision>
                  <DecisionList/>
                  <NarrativeBook>0</NarrativeBook>
                </ConditionQuestDecision>
```

Container defaults (entry contents):

```xml
<ConditionQuestDecision>
                  <DecisionList>
                    <Decision>
                      <Template>ConditionDecision</Template>
                      <Values>
                        <Condition/>
                        <ConditionDecision/>
                      </Values>
                    </Decision>
                  </DecisionList>
                </ConditionQuestDecision>
```

### ConditionQuestDelivery

Source: properties-toolone.xml:4133. Captured owning templates: `DeliveryObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `DeliveryObject_cqd` | Vector |  |  |  |
| `DeliveryObject_cqd/Item/ObjectGUID` | Asset |  | NeededProperty=Product;Item |  |
| `DeliveryObject_cqd/Item/Min` | Integer |  |  |  |
| `DeliveryObject_cqd/Item/Max` | Integer |  |  |  |
| `DeliveryType` | Choice | [GoodsInRangeType](trigger-datasets.md#goodsinrangetype) |  | The type of delivery for this quest. See the dataset for more information on the available options |
| `AllowKontorsToDeliver` | Boolean |  |  | True if ships and kontors of the player are valid objects to deliver wares, False if only ships can deliver |
| `AllowedDeliveryObjectLayers` | Flags | [QuestDeliveryObjectLayer](trigger-datasets.md#questdeliveryobjectlayer) |  |  |
| `DeliveryExecutionPlace` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectPlayerKontor;ConditionObjectClientQuestObject;ConditionObjectPrebuiltObject;ConditionObjectSpawnedObject;ConditionObjectStarterObject; AllowedProperties= | If DeliveryType == Ship then this will be the place where the goods need to be brought. In the other cases this object will only be used for the selection reminder message AND only if not starter object is configured |
| `UseQuestArea` | Boolean |  |  | Indicates whether the area should be dynamically choosen where the quest takes place (decided by precondition or starter object) |
| `DeliveryIsland` | Asset |  | NeededProperty=Island |  |
| `ConfirmOnReach` | Boolean |  |  | if true, triggers a message when goods are delivered that needs to be accepted to continue |

Explicit property defaults:

```xml
<ConditionQuestDelivery>
                  <DeliveryObject_cqd>
                    <Item/>
                  </DeliveryObject_cqd>
                  <DeliveryType>TargetObject</DeliveryType>
                  <AllowedDeliveryObjectLayers>Water;Air</AllowedDeliveryObjectLayers>
                  <DeliveryExecutionPlace>
                    <Template>ConditionObjectPlayerKontor</Template>
                    <Values>
                      <ConditionObjectPlayerKontor/>
                      <ConditionScanner/>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </DeliveryExecutionPlace>
                  <DeliveryIsland>0</DeliveryIsland>
                  <ConfirmOnReach>1</ConfirmOnReach>
                </ConditionQuestDelivery>
```

Container defaults (entry contents):

```xml
<ConditionQuestDelivery>
                  <DeliveryObject_cqd>
                    <ObjectGUID>0</ObjectGUID>
                    <Min>1</Min>
                    <Max>1</Max>
                  </DeliveryObject_cqd>
                </ConditionQuestDelivery>
```

### ConditionQuestDestroy

Source: properties-toolone.xml:4193. Captured owning templates: `DestroyObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `DestroyObjects` | Vector |  |  |  |
| `DestroyObjects/Item/DestroyObject` | AutoCreateAsset |  | AllowedTemplates=QuestObjectList; AllowedProperties= |  |
| `DestroyObjectsPrebuilt` | Vector |  |  | List of prebuilt objects that should be destroyed |
| `DestroyObjectsPrebuilt/Item/DestroyObject` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectPrebuiltObject; AllowedProperties= |  |
| `EscortShips` | Vector |  |  |  |
| `EscortShips/Item/EscortShip` | AutoCreateAsset |  | AllowedTemplates=QuestObjectList; AllowedProperties= |  |
| `MoveAngleMin_cqd` | Integer |  |  |  |
| `MoveAngleMax_cqd` | Integer |  |  |  |
| `DestroyFinishObjects` | Vector |  |  |  |
| `DestroyFinishObjects/Item/DestroyFinishObject` | AutoCreateAsset |  | AllowedTemplates=QuestObjectList; AllowedProperties= | Defines the object that will spawn right at the place where the last destroy ship sunk. The object should have an infolayer and should be unsinkable. |
| `ObjectsBehaviour` | Choice | [QuestDestroyTargetShipBehaviour](trigger-datasets.md#questdestroytargetshipbehaviour) |  |  |
| `AllowShipToCancelMovementToDefendItself` | Boolean |  |  | If set, the destroy object will cancel its movement commands when attacked and attack the attacker. If not, it will follow its movement command and onlty auto attack |

Explicit property defaults:

```xml
<ConditionQuestDestroy>
                  <DestroyObjects/>
                  <DestroyObjectsPrebuilt/>
                  <EscortShips/>
                  <MoveAngleMin_cqd>90</MoveAngleMin_cqd>
                  <MoveAngleMax_cqd>120</MoveAngleMax_cqd>
                  <DestroyFinishObjects/>
                  <ObjectsBehaviour>StandStill</ObjectsBehaviour>
                  <AllowShipToCancelMovementToDefendItself>1</AllowShipToCancelMovementToDefendItself>
                </ConditionQuestDestroy>
```

Container defaults (entry contents):

```xml
<ConditionQuestDestroy>
                  <DestroyObjects>
                    <DestroyObject>
                      <Template>QuestObjectList</Template>
                      <Values>
                        <ObjectList/>
                      </Values>
                    </DestroyObject>
                  </DestroyObjects>
                  <DestroyObjectsPrebuilt>
                    <DestroyObject>
                      <Template>ConditionObjectPrebuiltObject</Template>
                      <Values>
                        <ConditionObjectPrebuiltObject/>
                        <ConditionScanner/>
                        <ConditionObjectiveSignsAndFeedback/>
                      </Values>
                    </DestroyObject>
                  </DestroyObjectsPrebuilt>
                  <EscortShips>
                    <EscortShip>
                      <Template>QuestObjectList</Template>
                      <Values>
                        <ObjectList/>
                      </Values>
                    </EscortShip>
                  </EscortShips>
                  <DestroyFinishObjects>
                    <DestroyFinishObject>
                      <Template>QuestObjectList</Template>
                      <Values>
                        <ObjectList/>
                      </Values>
                    </DestroyFinishObject>
                  </DestroyFinishObjects>
                </ConditionQuestDestroy>
```

### ConditionQuestDivingBell

Source: properties-toolone.xml:4264. Captured owning templates: `DivingBellObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TreasureItem` | Asset |  | NeededProperty=Item | The specific Item that the player should receive. Either a real item or a treasure dummy item |
| `AddScrapToTreasure` | Boolean |  |  | Indicates whether there should be scrap as an additional reward for the treasure |
| `AdditionalScrapItem` | Asset |  | NeededProperty=Item | The reward pool to choose the scrap from |
| `AmountScrapSpots` | Integer |  |  | The amount of scrap spots spawned in the world besides the treasure |
| `ScrapDummyItem` | Asset |  | NeededProperty=Item | The item representing scrap that the player receives when searching a scrap spot |
| `SpawnedTreasureGround` | Asset |  | NeededProperty=DivingBellObject | The object spawned in the world to visualize a diving bell location and holding the items |
| `SpawnAdditionalObjects` | Boolean |  |  |  |
| `AdditionalObjectData` | Struct |  |  |  |
| `AdditionalObjectData/AdditionalObjectList` | AutoCreateAsset |  | AllowedTemplates=ConditionScanner; AllowedProperties= |  |
| `AdditionalObjectData/DistanceToTreasure` | Float |  |  |  |
| `ShowTreasureMapButton` | Boolean |  |  | Shows the treasure map button in the quest tracker UI |

Explicit property defaults:

```xml
<ConditionQuestDivingBell>
                  <TreasureItem>0</TreasureItem>
                  <AdditionalScrapItem>0</AdditionalScrapItem>
                  <ScrapDummyItem>0</ScrapDummyItem>
                  <SpawnedTreasureGround>0</SpawnedTreasureGround>
                  <AdditionalObjectData/>
                </ConditionQuestDivingBell>
```

Container defaults (entry contents):

```xml
<ConditionQuestDivingBell>
                  <AdditionalObjectData>
                    <AdditionalObjectList>
                      <Template>ConditionScanner</Template>
                      <Values>
                        <ConditionScanner/>
                      </Values>
                    </AdditionalObjectList>
                  </AdditionalObjectData>
                </ConditionQuestDivingBell>
```

### ConditionQuestEscort

Source: properties-toolone.xml:4328. Captured owning templates: `EscortObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `EscortObjects` | Vector |  |  |  |
| `EscortObjects/Item/EscortObject` | AutoCreateAsset |  | AllowedTemplates=QuestObjectList; AllowedProperties= | Which objects the player has to escort. Each List entry contains an exact amount of objects to escort. |
| `EscortObjectsPrebuilt` | Vector |  |  |  |
| `EscortObjectsPrebuilt/Item/EscortObject` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectPrebuiltObject;ObjectFilterWithSignsAndFeedback; AllowedProperties= |  |
| `MinSurvivors` | Integer |  | Min=1 | Defines the minimum amount of escorted ships that should survive, otherwise the Quest will fail. |
| `SpawnArea` | AutoCreateAsset |  | AllowedTemplates=QuestSpawnArea; AllowedProperties= |  |
| `Destinations` | Vector |  |  |  |
| `Destinations/Item/MoveDirection` | Choice | [QuestEscortMoveTarget](trigger-datasets.md#questescortmovetarget) |  | Defines the target where the escorted ships move to. |
| `Destinations/Item/TargetObject` | Asset |  |  | Defines the target object where the escorted objects should move to. |
| `Destinations/Item/TargetSpawnArea` | AutoCreateAsset |  | AllowedTemplates=QuestSpawnArea; AllowedProperties= |  |
| `Destinations/Item/TargetObjectDespawn` | Boolean |  |  |  |
| `Destinations/Item/TargetObjectDamage` | Float |  | Min=0; Max=1 | Initial damage of target ships in percent [0..1] |
| `Destinations/Item/PrebuiltObject` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectPrebuiltObject; AllowedProperties= |  |
| `EscortObjectDamage` | Float |  | Min=0; Max=1 | Initial damage of escort ships in percent [0..1] |
| `EscortBeginRadius` | Integer |  | Min=0 | The radius in what a player ship has to be to start the escort. In game, this is dynamic: 11 + colliderShipA + colliderShipB. It would be better if this was dynamically calculated, but we have not data about the colliders at the time of the check. So for now, a range of 32 should be sufficient for even the longest ships. Also note, that as of now, this value is never overwritten.  |
| `EscortObjectDespawn` | Choice | [QuestObjectDespawn](trigger-datasets.md#questobjectdespawn) |  | The way how the escort object should despawn after the quest ended |
| `EscortObjectDespawnDelay` | Time |  |  |  |
| `AttackerObjectDespawn` | Choice | [QuestObjectDespawn](trigger-datasets.md#questobjectdespawn) |  | The way how the attacker object should despawn after the quest ended |
| `AttackerObjectDespawnDelay` | Time |  |  |  |
| `AttackerObjects` | Vector |  |  |  |
| `AttackerObjects/Item/AttackerObject` | AutoCreateAsset |  | AllowedTemplates=QuestObjectList; AllowedProperties= | Defines which objects should spawn and attack the escorted ship(s). |
| `AttackerList` | Vector |  |  | At list of attacker settings that are spawned during the escort quest |
| `AttackerList/Item/SpawnTime` | Time |  |  | The time at which this attacker should spawn relativ to quest activation |
| `AttackerList/Item/AttackerObjectList` | Vector |  |  | List of attacker objects that should be spawned at this time interval |
| `AttackerList/Item/AttackerObjectList/Item/AttackerObject` | AutoCreateAsset |  | AllowedTemplates=QuestObjectList; AllowedProperties= |  |
| `HasEndlessAttacker` | Boolean |  |  | Indicates whether the escort will spawn attacker indefintely. This will be used after the last entry of the attacker list has been spawned |
| `AttackerEndlessSpawn` | Vector |  |  | The attacker objects that should be spawned as endless attacker |
| `AttackerEndlessSpawn/Item/AttackerObject` | AutoCreateAsset |  | AllowedTemplates=QuestObjectList; AllowedProperties= |  |
| `AttackerEndlessInterval` | Time |  |  | The time interval at which the endless attacker should be regularly spawned |
| `MinDistAttackerToObject` | Float |  |  | Defines the minimum distance from escorted ship where the attacker ships will spawn. |
| `MaxDistAttackerToObject` | Float |  |  | Defines the maximum distance from escorted ship where the attacker ships will spawn. |
| `DistMinBetweenAttacker` | Float |  |  | Minimum distance between multiple attackers when spawned |
| `DistMaxBetweenAttacker` | Float |  |  | Maximum distance between multiple attackers when spawned |
| `AttackerSpawnInterval` | Time |  |  | Defines the interval after which the first and all following attacker waves will spawn. Attacker waves spawn until the escorted ship is destroyed or leaves the map. |
| `NeedsShipInRange` | Boolean |  |  | Indicates whether there has to be a ship near the escort objects to be able to start the escort |
| `StarterHeadlineText` | Text |  | NeededProperty=Text |  |
| `StarterHeadlineTextWithoutShip` | Text |  | NeededProperty=Text | The objective text used when there does not have to a ship nearby |
| `TargetMapBorderText` | Text |  | NeededProperty=Text | The text that is used when the destination is the map border |
| `EscortFinishObjects` | Vector |  |  |  |
| `EscortFinishObjects/Item/EscortFinishObject` | AutoCreateAsset |  | AllowedTemplates=QuestObjectList; AllowedProperties= | Defines the objects that will spawn right at the place where the last escort ship reached it's destination. |
| `StartImmediately` | Boolean |  |  |  |
| `DespawnPrebuiltEscortObjects` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionQuestEscort>
                  <EscortObjects/>
                  <EscortObjectsPrebuilt/>
                  <SpawnArea>
                    <Template>QuestSpawnArea</Template>
                    <Values>
                      <SpawnArea/>
                    </Values>
                  </SpawnArea>
                  <Destinations/>
                  <EscortBeginRadius>32</EscortBeginRadius>
                  <EscortObjectDespawn>LeaveMap</EscortObjectDespawn>
                  <AttackerObjectDespawn>LeaveMap</AttackerObjectDespawn>
                  <AttackerObjects/>
                  <AttackerList/>
                  <AttackerEndlessSpawn/>
                  <NeedsShipInRange>1</NeedsShipInRange>
                  <StarterHeadlineText>0</StarterHeadlineText>
                  <StarterHeadlineTextWithoutShip>0</StarterHeadlineTextWithoutShip>
                  <TargetMapBorderText>0</TargetMapBorderText>
                  <EscortFinishObjects/>
                </ConditionQuestEscort>
```

Container defaults (entry contents):

```xml
<ConditionQuestEscort>
                  <EscortObjects>
                    <EscortObject>
                      <Template>QuestObjectList</Template>
                      <Values>
                        <ObjectList/>
                      </Values>
                    </EscortObject>
                  </EscortObjects>
                  <EscortObjectsPrebuilt>
                    <EscortObject>
                      <Template>ConditionObjectPrebuiltObject</Template>
                      <Values>
                        <ConditionObjectPrebuiltObject/>
                        <ConditionScanner/>
                        <ConditionObjectiveSignsAndFeedback/>
                      </Values>
                    </EscortObject>
                  </EscortObjectsPrebuilt>
                  <Destinations>
                    <MoveDirection>MapBorder</MoveDirection>
                    <TargetObject>0</TargetObject>
                    <TargetSpawnArea>
                      <Template>QuestSpawnArea</Template>
                      <Values>
                        <SpawnArea/>
                      </Values>
                    </TargetSpawnArea>
                    <PrebuiltObject>
                      <Template>ConditionObjectPrebuiltObject</Template>
                      <Values>
                        <ConditionObjectPrebuiltObject/>
                        <ConditionScanner/>
                        <ConditionObjectiveSignsAndFeedback/>
                      </Values>
                    </PrebuiltObject>
                  </Destinations>
                  <AttackerObjects>
                    <AttackerObject>
                      <Template>QuestObjectList</Template>
                      <Values>
                        <ObjectList/>
                      </Values>
                    </AttackerObject>
                  </AttackerObjects>
                  <AttackerList>
                    <ContainerValues>
                      <AttackerObjectList>
                        <AttackerObject>
                          <Template>QuestObjectList</Template>
                          <Values>
                            <ObjectList/>
                          </Values>
                        </AttackerObject>
                      </AttackerObjectList>
                    </ContainerValues>
                    <AttackerObjectList/>
                  </AttackerList>
                  <AttackerEndlessSpawn>
                    <AttackerObject>
                      <Template>QuestObjectList</Template>
                      <Values>
                        <ObjectList/>
                      </Values>
                    </AttackerObject>
                  </AttackerEndlessSpawn>
                  <EscortFinishObjects>
                    <EscortFinishObject>
                      <Template>QuestObjectList</Template>
                      <Values>
                        <ObjectList/>
                      </Values>
                    </EscortFinishObject>
                  </EscortFinishObjects>
                </ConditionQuestEscort>
```

### ConditionQuestExpedition

Source: properties-toolone.xml:4570. Captured owning templates: `ExpeditionObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `RequestedExpedition` | Asset |  | NeededProperty=Expedition | This expedition needs to be completed |
| `CheckedExpeditionStates` | Flags | [ExpeditionState](trigger-datasets.md#expeditionstate) |  |  |

Explicit property defaults:

```xml
<ConditionQuestExpedition>
                  <RequestedExpedition>0</RequestedExpedition>
                  <CheckedExpeditionStates>Ended</CheckedExpeditionStates>
                </ConditionQuestExpedition>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestFactoryProductivity

Source: properties-toolone.xml:4584. Captured owning templates: `FactoryProductivityObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `QuestProductivityComparison` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `QuestProductivityThreshold` | Integer |  | Min=0; Max=100 |  |

Explicit property defaults:

```xml
<ConditionQuestFactoryProductivity>
                  <QuestProductivityComparison>AtLeast</QuestProductivityComparison>
                </ConditionQuestFactoryProductivity>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestFakeObjective

Source: properties-toolone.xml:4598. Captured owning templates: `FakeQuestObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `QuestTrackerEntries` | Vector |  |  |  |
| `QuestTrackerEntries/Item/TextContent` | Text |  | NeededProperty=Text |  |
| `QuestTrackerEntries/Item/TextValue` | Text |  | NeededProperty=Text |  |
| `QuestTrackerEntries/Item/CombinedText` | Text |  | NeededProperty=Text |  |
| `QuestTrackerEntries/Item/QuestTrackerIcon` | FileName |  |  |  |

Explicit property defaults:

```xml
<ConditionQuestFakeObjective>
                  <QuestTrackerEntries/>
                </ConditionQuestFakeObjective>
```

Container defaults (entry contents):

```xml
<ConditionQuestFakeObjective>
                  <QuestTrackerEntries>
                    <TextContent>0</TextContent>
                    <TextValue>0</TextValue>
                    <CombinedText>0</CombinedText>
                  </QuestTrackerEntries>
                </ConditionQuestFakeObjective>
```

### ConditionQuestFollowShip

Source: properties-toolone.xml:4626. Captured owning templates: `FollowShipObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `StartRangeObjectiveText` | Text |  | NeededProperty=Text |  |
| `RangeWarningText` | Text |  | NeededProperty=Text | This text will be shown if the ship is too near or too far away from the target ship |
| `StartPosition` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectStarterObject;ConditionObjectPrebuiltObject; AllowedProperties= |  |
| `StartRange` | Integer |  | Min=0 |  |
| `TargetShip` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectSpawnedObject;ConditionObjectPrebuiltObject; AllowedProperties= |  |
| `MinRange` | Float |  |  | Distance of player ship and target ship must not fall below this value |
| `MaxRange` | Float |  |  | Distance of player ship and target ship must not exceed this value |
| `MinRangeEffectPositive` | Asset |  | NeededProperty=Mesh |  |
| `MinRangeEffectNegative` | Asset |  | NeededProperty=Mesh |  |
| `MaxRangeEffectPositive` | Asset |  | NeededProperty=Mesh |  |
| `MaxRangeEffectNegative` | Asset |  | NeededProperty=Mesh |  |
| `RangeWarningTime` | Time |  |  |  |
| `TargetPositions` | Vector |  |  |  |
| `TargetPositions/Item/Position` | AutoCreateAsset |  | AllowedTemplates=ObjectFilter; AllowedProperties= |  |
| `TargetPositions/Item/Range` | Float |  |  |  |

Explicit property defaults:

```xml
<ConditionQuestFollowShip>
                  <StartRangeObjectiveText>0</StartRangeObjectiveText>
                  <RangeWarningText>0</RangeWarningText>
                  <StartPosition>
                    <Template>ConditionObjectStarterObject</Template>
                    <Values>
                      <ConditionScanner/>
                      <ConditionObjectStarterObject/>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </StartPosition>
                  <TargetShip>
                    <Template>ConditionObjectSpawnedObject</Template>
                    <Values>
                      <ConditionObjectSpawnedObject/>
                      <ConditionScanner/>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </TargetShip>
                  <MinRangeEffectPositive>0</MinRangeEffectPositive>
                  <MinRangeEffectNegative>0</MinRangeEffectNegative>
                  <MaxRangeEffectPositive>0</MaxRangeEffectPositive>
                  <MaxRangeEffectNegative>0</MaxRangeEffectNegative>
                  <TargetPositions/>
                </ConditionQuestFollowShip>
```

Container defaults (entry contents):

```xml
<ConditionQuestFollowShip>
                  <TargetPositions>
                    <Position>
                      <Template>ObjectFilter</Template>
                      <Values>
                        <ObjectFilter/>
                      </Values>
                    </Position>
                    <Range>15</Range>
                  </TargetPositions>
                </ConditionQuestFollowShip>
```

### ConditionQuestGamePadAction

Source: properties-toolone.xml:4707. Captured owning templates: `GamePadActionObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `QuestGamePadActionComparator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `QuestGamePadActionToTrack` | Choice | [GamepadAction](trigger-datasets.md#gamepadaction) |  |  |
| `QuestGamePadActionTriggeredAmount` | Integer |  |  |  |
| `QuestStartAmountTrackingOnFirstEvaluation` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionQuestGamePadAction>
                  <QuestGamePadActionComparator>AtLeast</QuestGamePadActionComparator>
                  <QuestGamePadActionToTrack>ChangeTabLeft</QuestGamePadActionToTrack>
                </ConditionQuestGamePadAction>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestHitMovingTarget

Source: properties-toolone.xml:4728. Captured owning templates: `HitMovingTargetObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `HitTarget` | Asset |  | NeededProperty=Walking | The target object that should be destroyed |
| `HitTargetAmount` | Integer |  | Min=1 |  |
| `HitTargetSignsAndFeedback` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectiveSignsAndFeedback; AllowedProperties= |  |
| `WaypointAmount` | Integer |  |  | The amount of waypoints used to mark the radial track of the target |
| `TargetPatrolRadius` | Float |  |  | The radius in which the target object will patrol around its spawn position |
| `PickUp` | Asset |  |  |  |
| `PickUpAmount` | Integer |  |  |  |
| `ItemRetrievalPlace` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectPlayerKontor;ConditionObjectClientQuestObject;ConditionObjectPrebuiltObject;ConditionObjectSpawnedObject;ConditionObjectAnywhere; AllowedProperties= |  |
| `ItemUsed` | Asset |  |  |  |
| `CondInStorageCombinedText` | Text |  | NeededProperty=Text |  |
| `HitMovingTargetCombinedText` | Text |  | NeededProperty=Text |  |
| `SkipItemRetrievalPlaceConfirmation` | Boolean |  |  | If false, a confirmation message needs to be accepted to get the item, otherwise the player gets no notification |

Explicit property defaults:

```xml
<ConditionQuestHitMovingTarget>
                  <HitTarget>0</HitTarget>
                  <HitTargetAmount>1</HitTargetAmount>
                  <HitTargetSignsAndFeedback>
                    <Template>ConditionObjectiveSignsAndFeedback</Template>
                    <Values>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </HitTargetSignsAndFeedback>
                  <PickUp>0</PickUp>
                  <ItemRetrievalPlace>
                    <Template>ConditionObjectPlayerKontor</Template>
                    <Values>
                      <ConditionObjectPlayerKontor/>
                      <ConditionScanner/>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </ItemRetrievalPlace>
                  <ItemUsed>0</ItemUsed>
                  <CondInStorageCombinedText>0</CondInStorageCombinedText>
                  <HitMovingTargetCombinedText>0</HitMovingTargetCombinedText>
                </ConditionQuestHitMovingTarget>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestIslandsWithFertility

Source: properties-toolone.xml:4791. Captured owning templates: `IslandsWithFertilityObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `QuestIslandComparator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `QuestIslandThreshold` | Integer |  | Min=0 |  |
| `QuestFertilityContext` | Asset |  |  |  |
| `QuestIslandScope` | Choice | [CounterScope](trigger-datasets.md#counterscope) |  |  |
| `QuestCustomRegion` | Asset |  |  |  |
| `QuestCustomSessions` | Vector |  |  |  |
| `QuestCustomSessions/Item/GUID` | Asset |  |  |  |

Explicit property defaults:

```xml
<ConditionQuestIslandsWithFertility>
                  <QuestIslandComparator>AtLeast</QuestIslandComparator>
                  <QuestFertilityContext>0</QuestFertilityContext>
                  <QuestIslandScope>Area</QuestIslandScope>
                  <QuestCustomRegion>0</QuestCustomRegion>
                  <QuestCustomSessions/>
                </ConditionQuestIslandsWithFertility>
```

Container defaults (entry contents):

```xml
<ConditionQuestIslandsWithFertility>
                  <QuestCustomSessions>
                    <GUID>0</GUID>
                  </QuestCustomSessions>
                </ConditionQuestIslandsWithFertility>
```

### ConditionQuestItemUsed

Source: properties-toolone.xml:4827. Captured owning templates: `ItemUsageObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `UseItems` | Vector |  |  | Which Items the player has to activate/socket and how often |
| `UseItems/Item/Item` | Asset |  | NeededProperty=Item | Item the player has to activate or to socket |
| `UseItems/Item/Amount` | Integer |  |  | Amount of items the player has to activate or to socket |
| `UseItems/Item/TargetObject` | Asset |  |  | At which game objects the item(s) have to be activated/socketed. If nothing is setup here, then it's only checked whether the item(s) have been activated. |
| `UseItems/Item/NeedsActivation` | Boolean |  |  | True, if the item nees to be equipped AND activated |

Explicit property defaults:

```xml
<ConditionQuestItemUsed>
                  <UseItems/>
                </ConditionQuestItemUsed>
```

Container defaults (entry contents):

```xml
<ConditionQuestItemUsed>
                  <UseItems>
                    <Item>0</Item>
                    <TargetObject>0</TargetObject>
                  </UseItems>
                </ConditionQuestItemUsed>
```

### ConditionQuestModuleBuildingEfficiency

Source: properties-toolone.xml:4858. Captured owning templates: `ModuleBuildingEfficiencyObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ModuleBuildingAsset` | Asset |  |  | The module owner building that will be checked for the number of modules |
| `Efficiency` | Float |  |  | The efficiency that needs to be reached. Must be &gt;= 0 and &lt;= 1. The efficiency is calculated by (modules / max number of modules) |
| `Negate` | Boolean |  |  | Indicates whether the condiion should be negated |

Explicit property defaults:

```xml
<ConditionQuestModuleBuildingEfficiency>
                  <ModuleBuildingAsset>0</ModuleBuildingAsset>
                </ConditionQuestModuleBuildingEfficiency>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestMonumentDestroyed

Source: properties-toolone.xml:4876. Captured owning templates: `MonumentDestroyedObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `MonumentBaseGUID` | Asset |  |  |  |
| `MonumentCounterScope` | Choice | [CounterScope](trigger-datasets.md#counterscope) |  |  |
| `MonumentCustomContext` | Asset |  |  |  |
| `MonumentContextUseQuestArea` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionQuestMonumentDestroyed>
                  <MonumentBaseGUID>0</MonumentBaseGUID>
                  <MonumentCounterScope>Area</MonumentCounterScope>
                  <MonumentCustomContext>0</MonumentCustomContext>
                </ConditionQuestMonumentDestroyed>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestObjective

Source: properties-toolone.xml:6012. Captured owning templates: `AirdropObjective`, `BringVehicleToObjectObjective`, `BusActivationNeedSaturationObjective`, `CameraMovementObjective`, `ConditionQuestResolveConfirmation`, `ConditionStarterObject`, `DecisionObjective`, `DeliveryObjective`, `DestroyObjective`, `DivingBellObjective`, `EscortObjective`, `ExpeditionObjective`, `FactoryProductivityObjective`, `FakeQuestObjective`, `FollowShipObjective`, `GamePadActionObjective`, `HitMovingTargetObjective`, `IslandsWithFertilityObjective`, `ItemUsageObjective`, `ModuleBuildingEfficiencyObjective`, `MonumentDestroyedObjective`, `PhotographyObjective`, `PickupObjective`, `PicturePuzzleObjective`, `RecipeResearchCompletedObjective`, `SelectObjectObjective`, `SellObjectToParticipantObjective`, `SmugglerObjective`, `StatusQuoObjective`, `SubQuestObjective`, `SustainObjective`, `TutorialObjective`, `UseItemInAreaObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `IsVisibleInQuestTracker` | Boolean |  |  | true, if this condition should be shown in the quest tracker |
| `TextCombinedContextValue` | Text |  | NeededProperty=Text | this is the combined description text with a value text of a quest objetive (e.g. "Build houses 2 / 5") |
| `QuestTrackerIcon` | FileName |  |  |  |
| `ObjectiveSignsAndFeedback` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectiveSignsAndFeedback; AllowedProperties= |  |
| `FakeMinimapPings` | Struct |  |  | Mininmappings that are not related to the objective can be defined here |
| `FakeMinimapPings/Objects` | Vector |  |  |  |
| `FakeMinimapPings/Objects/Item/FakeMinimapObjects` | AutoCreateAsset |  | AllowedTemplates=ObjectFilter; AllowedProperties= |  |
| `FakeMinimapPings/Objects/Item/SignsAndFeedback` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectiveSignsAndFeedback; AllowedProperties= |  |
| `ObjectiveSuccessMessage` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `JumpToVisibility` | Choice | [QuestJumpToButtonVisibility](trigger-datasets.md#questjumptobuttonvisibility) |  | Defines the visibility of the jump-to button for this objective |
| `OnSuccessActions` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= |  |
| `LinkAllQuestActionsToQuest` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionQuestObjective>
              <IsVisibleInQuestTracker>1</IsVisibleInQuestTracker>
              <TextCombinedContextValue>0</TextCombinedContextValue>
              <ObjectiveSignsAndFeedback>
                <Template>ConditionObjectiveSignsAndFeedback</Template>
                <Values>
                  <ConditionObjectiveSignsAndFeedback/>
                </Values>
              </ObjectiveSignsAndFeedback>
              <FakeMinimapPings/>
              <ObjectiveSuccessMessage>
                <Template>CharacterNotification</Template>
                <Values>
                  <CharacterNotification/>
                  <BaseNotification/>
                  <NotificationSubtitle/>
                </Values>
              </ObjectiveSuccessMessage>
              <JumpToVisibility>Show</JumpToVisibility>
              <OnSuccessActions>
                <Template>Actions</Template>
                <Values>
                  <ActionList/>
                </Values>
              </OnSuccessActions>
            </ConditionQuestObjective>
```

Container defaults (entry contents):

```xml
<ConditionQuestObjective>
              <FakeMinimapPings>
                <ContainerValues>
                  <Objects>
                    <FakeMinimapObjects>
                      <Template>ObjectFilter</Template>
                      <Values>
                        <ObjectFilter/>
                      </Values>
                    </FakeMinimapObjects>
                    <SignsAndFeedback>
                      <Template>ConditionObjectiveSignsAndFeedback</Template>
                      <Values>
                        <ConditionObjectiveSignsAndFeedback/>
                      </Values>
                    </SignsAndFeedback>
                  </Objects>
                </ContainerValues>
                <Objects/>
              </FakeMinimapPings>
            </ConditionQuestObjective>
```

### ConditionQuestPhotography

Source: properties-toolone.xml:4896. Captured owning templates: `PhotographyObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `PhotographyObjectList` | Vector |  |  | Which objective needs to be photographed. After the quest is accepted, the palyer is able to enter a special photography view. While being in the photography view, the player needs to center the objective on the screen. He can take pictures anytime, by pressing a certain button on the interface, but when the objective is centered, he will get a special feedback that he took the right picture. |
| `PhotographyObjectList/Item/Entry` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectPrebuiltObject;ConditionObjectSpawnedObject; AllowedProperties= |  |
| `PhotographyObjectList/Item/StagedPhotography` | FileName |  |  | If set, this picture will be shown instead of the actual screenshot made by the player |
| `PhotographyObjectList/Item/CircleAreaPercentage` | Float |  |  | The percentage of the area that the circle around the object has in relation to the total screen space. Toggle quest hint cheat during photography quest to see details |
| `PhotographyObjectList/Item/ScreenBorderPercentage` | Float |  |  | The object has to be inside a smaller rectangle than the screen itself. This is the percentage of the area that is reduced from each border to define the inner rectangle |
| `PhotographyObjectList/Item/AppearInNewspaperArticle` | Asset |  | NeededProperty=NewspaperArticle;NewspaperSpecialEditionArticle | If any article is selected, this picture will be shown in the given article |
| `PhotographyObjectList/Item/ShowHintMarkerWhenOffscreen` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionQuestPhotography>
                  <PhotographyObjectList/>
                </ConditionQuestPhotography>
```

Container defaults (entry contents):

```xml
<ConditionQuestPhotography>
                  <PhotographyObjectList>
                    <Entry>
                      <Template>ConditionObjectPrebuiltObject</Template>
                      <Values>
                        <ConditionObjectPrebuiltObject/>
                        <ConditionScanner/>
                        <ConditionObjectiveSignsAndFeedback/>
                      </Values>
                    </Entry>
                    <CircleAreaPercentage>5</CircleAreaPercentage>
                    <ScreenBorderPercentage>10</ScreenBorderPercentage>
                    <AppearInNewspaperArticle>0</AppearInNewspaperArticle>
                  </PhotographyObjectList>
                </ConditionQuestPhotography>
```

### ConditionQuestPickup

Source: properties-toolone.xml:4937. Captured owning templates: `PickupObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `PickupObjects` | Vector |  |  |  |
| `PickupObjects/Item/PickupObject` | AutoCreateAsset |  | AllowedTemplates=QuestObjectList; AllowedProperties= |  |
| `PickupObjects/Item/IsOnlyDecoration` | Boolean |  |  | If true: These objects will not count towards the quest goal. They are only decoys. |
| `PickupObjects/Item/IsDecoy` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionQuestPickup>
                  <PickupObjects/>
                </ConditionQuestPickup>
```

Container defaults (entry contents):

```xml
<ConditionQuestPickup>
                  <PickupObjects>
                    <PickupObject>
                      <Template>QuestObjectList</Template>
                      <Values>
                        <ObjectList/>
                      </Values>
                    </PickupObject>
                  </PickupObjects>
                </ConditionQuestPickup>
```

### ConditionQuestPicturePuzzle

Source: properties-toolone.xml:4961. Captured owning templates: `PicturePuzzleObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `PicturePuzzleObjects` | Vector |  |  |  |
| `PicturePuzzleObjects/Item/Object` | Asset |  |  |  |
| `PicturePuzzleObjects/Item/Amount` | Integer |  |  |  |
| `PicturePuzzleObjects/Item/MinAmount` | Integer |  |  |  |
| `PicturePuzzleObjects/Item/MaxAmount` | Integer |  |  |  |
| `PicturePuzzleObjects/Item/AdditionalAmount` | Integer |  |  |  |
| `PicturePuzzleObjects/Item/Context` | Struct |  |  |  |
| `PicturePuzzleObjects/Item/Context/CargoAsset` | Asset |  |  |  |
| `PicturePuzzleObjects/Item/Context/SpawnArea` | AutoCreateAsset |  | AllowedTemplates=QuestSpawnArea; AllowedProperties= |  |
| `PicturePuzzleObjects/Item/Context/Behaviour` | Choice | [QuestPicturePuzzleObjectBehaviour](trigger-datasets.md#questpicturepuzzleobjectbehaviour) |  | Different behaviours of spawned objects. 'Static': Objects will be placed and stand still, 'Mob': Special behaviour for moving mobs. |
| `PicturePuzzleObjects/Item/Context/PathLabel` | String |  |  | Only used when Behaviour is set to 'Mob'. Use it if you have a predefined path that the mob should take |
| `PicturePuzzleObjects/Item/Context/PathIsland` | Asset |  | NeededProperty=Island | Only used when Behaviour is set to 'Mob'. Use to define on which island the mob should spawn on |
| `PicturePuzzleObjects/Item/Context/IsOnlyDecoy` | Boolean |  |  | If true: These objects will not count towards the quest goal. They are only decoys. |
| `PicturePuzzleObjects/Item/Context/MobTryStreetPath` | Boolean |  |  | If true, the mob tries to use only streets |
| `PicturePuzzleObjects/Item/Context/MobTargetUnitCount` | Integer |  |  |  |
| `PicturePuzzleObjects/Item/Context/MobFeedbackHideRadius` | Float |  |  |  |
| `PicturePuzzleObjects/Item/Context/MobForceSpawnUnitCount` | Integer |  |  |  |
| `PicturePuzzleObjects/Item/Context/MobForceSpaenUnitType` | Asset |  | NeededProperty=TrafficFeedbackClass |  |
| `PicturePuzzleObjects/Item/Context/MobGoHomeOnTearDown` | Boolean |  |  |  |
| `PicturePuzzleObjects/Item/Context/MobMoveSpeed` | Float |  |  |  |
| `PicturePuzzleObjects/Item/Context/MobOverwriteUnitType` | Asset |  | NeededProperty=TrafficFeedbackClass | The units spawned in houses to join the mob will all have this unit type. (If set to invalid the unit type of inhabitants of the spawning building are used) |
| `PicturePuzzleObjects/Item/Context/MobSequence` | Choice | [QuestPicturePuzzleMobSequence](trigger-datasets.md#questpicturepuzzlemobsequence) |  |  |

Explicit property defaults:

```xml
<ConditionQuestPicturePuzzle>
                  <PicturePuzzleObjects/>
                </ConditionQuestPicturePuzzle>
```

Container defaults (entry contents):

```xml
<ConditionQuestPicturePuzzle>
                  <PicturePuzzleObjects>
                    <ContainerValues>
                      <Context>
                        <CargoAsset>0</CargoAsset>
                        <SpawnArea>
                          <Template>QuestSpawnArea</Template>
                          <Values>
                            <SpawnArea/>
                          </Values>
                        </SpawnArea>
                        <Behaviour>Static</Behaviour>
                        <PathIsland>0</PathIsland>
                        <MobTryStreetPath>1</MobTryStreetPath>
                        <MobTargetUnitCount>100</MobTargetUnitCount>
                        <MobFeedbackHideRadius>11</MobFeedbackHideRadius>
                        <MobForceSpawnUnitCount>70</MobForceSpawnUnitCount>
                        <MobForceSpaenUnitType>0</MobForceSpaenUnitType>
                        <MobMoveSpeed>0.3</MobMoveSpeed>
                        <MobOverwriteUnitType>0</MobOverwriteUnitType>
                        <MobSequence>Protest</MobSequence>
                      </Context>
                    </ContainerValues>
                    <Object>0</Object>
                    <Context/>
                  </PicturePuzzleObjects>
                </ConditionQuestPicturePuzzle>
```

### ConditionQuestPoolQuestRunning

Source: properties-toolone.xml:2691. Captured owning templates: `ConditionQuestPoolQuestRunning`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `EveryPoolMustBeRunning` | Boolean |  |  | Indicates whether every pool of the vector list should be running a quest. If false, the condition will be true if ANY quest pool is running a quest. |
| `QuestPoolsToCheck` | Vector |  |  | The list of quest pools to check |
| `QuestPoolsToCheck/Item/QuestPool` | Asset |  | NeededProperty=QuestPool |  |

Explicit property defaults:

```xml
<ConditionQuestPoolQuestRunning>
                  <QuestPoolsToCheck/>
                </ConditionQuestPoolQuestRunning>
```

Container defaults (entry contents):

```xml
<ConditionQuestPoolQuestRunning>
                  <QuestPoolsToCheck>
                    <QuestPool>0</QuestPool>
                  </QuestPoolsToCheck>
                </ConditionQuestPoolQuestRunning>
```

### ConditionQuestRecipeResearchCompleted

Source: properties-toolone.xml:5069. Captured owning templates: `RecipeResearchCompletedObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `QuestCompletedResearchField` | Flags | [ResearchFields](trigger-datasets.md#researchfields) |  | All research fields that should be checked |
| `QuestResearchComparisonOp` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  | The operator to compare the completed research recipes and the desired amount |
| `QuestResearchDesiredAmount` | Integer |  | Min=0 | The desired amount of completed research recipes |
| `QuestResearchRangeOp` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  | Defines which research fields need to match the desired amount |
| `QuestResearchRelativeToQuestStart` | Boolean |  |  | True: Counting from current condition start - False: Counting from 0. |

Explicit property defaults:

```xml
<ConditionQuestRecipeResearchCompleted>
                  <QuestResearchComparisonOp>AtLeast</QuestResearchComparisonOp>
                  <QuestResearchRangeOp>None</QuestResearchRangeOp>
                </ConditionQuestRecipeResearchCompleted>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestResolveConfirmation

Source: properties-toolone.xml:5101. Captured owning templates: `ConditionQuestResolveConfirmation`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ResolveConfirmationMessage` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `AvoidShipInRangeCondition` | Boolean |  |  | Does not generate a condition to force a ship to be near a target object |

Explicit property defaults:

```xml
<ConditionQuestResolveConfirmation>
                  <ResolveConfirmationMessage>
                    <Template>CharacterNotification</Template>
                    <Values>
                      <CharacterNotification/>
                      <BaseNotification/>
                      <NotificationSubtitle/>
                    </Values>
                  </ResolveConfirmationMessage>
                </ConditionQuestResolveConfirmation>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestSelectObject

Source: properties-toolone.xml:5115. Captured owning templates: `SelectObjectObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `SelectObjects` | Vector |  |  |  |
| `SelectObjects/Item/Object` | AutoCreateAsset |  | AllowedTemplates=ObjectFilter;ConditionObjectPlayerKontor;ConditionObjectClientQuestObject;ConditionObjectPrebuiltObject;ConditionObjectSpawnedObject;ConditionObjectStarterObject; AllowedProperties= |  |
| `QuestUseRuinState` | Choice | [Tristate](trigger-datasets.md#tristate) |  |  |

Explicit property defaults:

```xml
<ConditionQuestSelectObject>
                  <SelectObjects/>
                  <QuestUseRuinState>DontCare</QuestUseRuinState>
                </ConditionQuestSelectObject>
```

Container defaults (entry contents):

```xml
<ConditionQuestSelectObject>
                  <SelectObjects>
                    <Object>
                      <Template>ObjectFilter</Template>
                      <Values>
                        <ObjectFilter/>
                      </Values>
                    </Object>
                  </SelectObjects>
                </ConditionQuestSelectObject>
```

### ConditionQuestSellObjectToParticipant

Source: properties-toolone.xml:5135. Captured owning templates: `SellObjectToParticipantObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `BuyerParticipant` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | The participant that the player has to sell an object to |
| `ObjectToSell` | Asset |  | NeededProperty=ShipMaintenance;Item;Product | The object that the player has to sell to the participant |
| `SellAmount` | Integer |  | Min=1 | The amount the player has to sell to the buying participant |

Explicit property defaults:

```xml
<ConditionQuestSellObjectToParticipant>
                  <BuyerParticipant>Human0</BuyerParticipant>
                  <ObjectToSell>0</ObjectToSell>
                  <SellAmount>1</SellAmount>
                </ConditionQuestSellObjectToParticipant>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestSmuggler

Source: properties-toolone.xml:5156. Captured owning templates: `SmugglerObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `InitialTradingStation` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectAnywhere;ConditionObjectPlayerKontor;ConditionObjectClientQuestObject;ConditionObjectSpawnedObject;ConditionObjectPrebuiltObject;ConditionObjectStarterObject; AllowedProperties= | The (optional) very first station where the player needs to go to start the quest. Setting this to "anywhere" means that no initial trading station is needed. |
| `RetrieveItemAtInitialTradingStation` | Asset |  | NeededProperty=Item;Product | If not null, player will receive this item upon activating the quest at the initial trading station |
| `InitialTradingStationLayerFlags` | Flags | [PathPlannerLayer](trigger-datasets.md#pathplannerlayer) |  |  |
| `SmugglerStations` | Vector |  |  |  |
| `SmugglerStations/Item/Station` | AutoCreateAsset |  | AllowedTemplates=QuestTradingStation; AllowedProperties= |  |
| `SmugglerStations/Item/AllowKontors` | Boolean |  |  | True if ships and kontors of the player are valid objects to give/receive wares, False if only ships can do so |
| `EnforceStationOrder` | Boolean |  |  | If true, all stations need to be visited in the given order |
| `FailObjectiveOnDetection` | Boolean |  | ReadOnly=1 | CURRENT DESIGN ENFORCES THIS TO TRUE! If true, the quest will be failed if any of your ships was detected by a scanner. If false, the scanner ships will only start attacking |
| `ShipInRangeForActivationText` | Text |  | NeededProperty=Text | Will be shown when the ship is in range of the starter object and ready to activate the smuggler quest |
| `TextTradingStation_NoItem` | Text |  | NeededProperty=Text | Objective text that will be shown for trading stations where no item is needed to be delivered |
| `TextTradingStation` | Text |  | NeededProperty=Text | Objective text that will be shown for trading stations where an item needs to be delivered |
| `AdditionalScannerUnits` | Vector |  |  |  |
| `AdditionalScannerUnits/Item/ScannerCenterObject` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectPrebuiltObject; AllowedProperties= | The object that the scanner units will move around |

Explicit property defaults:

```xml
<ConditionQuestSmuggler>
                  <InitialTradingStation>
                    <Template>ConditionObjectAnywhere</Template>
                    <Values>
                      <ConditionObjectAnywhere/>
                    </Values>
                  </InitialTradingStation>
                  <RetrieveItemAtInitialTradingStation>0</RetrieveItemAtInitialTradingStation>
                  <InitialTradingStationLayerFlags>Land;Water;Air</InitialTradingStationLayerFlags>
                  <SmugglerStations/>
                  <FailObjectiveOnDetection>1</FailObjectiveOnDetection>
                  <ShipInRangeForActivationText>0</ShipInRangeForActivationText>
                  <TextTradingStation_NoItem>0</TextTradingStation_NoItem>
                  <TextTradingStation>0</TextTradingStation>
                  <AdditionalScannerUnits/>
                </ConditionQuestSmuggler>
```

Container defaults (entry contents):

```xml
<ConditionQuestSmuggler>
                  <SmugglerStations>
                    <Station>
                      <Template>QuestTradingStation</Template>
                      <Values>
                        <TradingStation>
                          <TradingStationDestination>
                            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                            <Template>ConditionObjectPlayerKontor</Template>
                            <Values>
                              <ConditionObjectPlayerKontor/>
                              <ConditionScanner/>
                              <ConditionObjectiveSignsAndFeedback/>
                            </Values>
                          </TradingStationDestination>
                          <OnTradingStationVisited>
                            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                            <Template>Actions</Template>
                            <Values>
                              <ActionList/>
                            </Values>
                          </OnTradingStationVisited>
                          <TradingStationSignsAndFeedback>
                            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                            <Template>ConditionObjectiveSignsAndFeedback</Template>
                            <Values>
                              <ConditionObjectiveSignsAndFeedback/>
                            </Values>
                          </TradingStationSignsAndFeedback>
                          <TradingStationReachedNotification>
                            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                            <Template>CharacterNotification</Template>
                            <Values>
                              <CharacterNotification/>
                              <BaseNotification/>
                              <NotificationSubtitle/>
                            </Values>
                          </TradingStationReachedNotification>
                        </TradingStation>
                      </Values>
                    </Station>
                  </SmugglerStations>
                  <AdditionalScannerUnits>
                    <ScannerCenterObject>
                      <Template>ConditionObjectPrebuiltObject</Template>
                      <Values>
                        <ConditionObjectPrebuiltObject/>
                        <ConditionScanner/>
                        <ConditionObjectiveSignsAndFeedback/>
                      </Values>
                    </ScannerCenterObject>
                  </AdditionalScannerUnits>
                </ConditionQuestSmuggler>
```

### ConditionQuestState

Source: properties-toolone.xml:2711. Captured owning templates: `ConditionQuestState`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ConditionQuestStateStates` | Flags | [QuestState](trigger-datasets.md#queststate) |  | All the states that satisfy this condition. |
| `ConditionQuestStateIsBlacklist` | Boolean |  |  | Indicates whether the given state flags should be treated as a blacklist instead of a whitelist |
| `ConditionQuestStateQuestGUID` | Asset |  | NeededProperty=Quest;QuestLine | A quest or a quest line that should be checked |
| `ConditionQuestStateRangeOp` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  | If the ConditionQuestStateQuestGUID is a quest line, this operator checks for which quests the states need to match |

Explicit property defaults:

```xml
<ConditionQuestState>
                  <ConditionQuestStateStates/>
                  <ConditionQuestStateQuestGUID>0</ConditionQuestStateQuestGUID>
                  <ConditionQuestStateRangeOp>None</ConditionQuestStateRangeOp>
                </ConditionQuestState>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestStatusQuo

Source: properties-toolone.xml:5236. Captured owning templates: `StatusQuoObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `MaxObjectiveCount` | Integer |  | Min=0 | If there is a pool used as a context, this value can restrict the number of generated objectives. This value is only used when AutoSpawnConditionsPerObject is true. |
| `LimitToQuestArea_SQ` | Boolean |  |  | Indicates whether the player counter should only be checked on the current quest area. Note, that the player counter must match AREA in order to use this. |
| `CheckAnyPoolAsset` | Boolean |  |  | Indicates if the player counter should be checked for ANY or ALL assets from a given asset pool. Can be ignored if context guid is not an asset pool |
| `CombinePoolAssets` | Boolean |  |  | If TRUE, the sum of all context pool results will be added and compared. In that case &lt;CheckAnyPoolAsset&gt; has no effect. Can be ignored if context guid is not an asset pool |
| `ShowSignsAndFeedback` | Boolean |  |  | If true, the signs and feedback of the objective will be used for all objects matching the given Context. StatusQuo objectives do not show signs and feedback per default |
| `BestAreaIsHighestValue` | Boolean |  |  | If true the area with the highest counter among all areas will be returned. Otherwise the lowest |

Explicit property defaults:

```xml
<ConditionQuestStatusQuo>
                  <BestAreaIsHighestValue>1</BestAreaIsHighestValue>
                </ConditionQuestStatusQuo>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestSubQuest

Source: properties-toolone.xml:5270. Captured owning templates: `SubQuestObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Asset` | Asset |  | NeededProperty=Objectives |  |

Explicit property defaults:

```xml
<ConditionQuestSubQuest>
                  <Asset>0</Asset>
                </ConditionQuestSubQuest>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestSustain

Source: properties-toolone.xml:5278. Captured owning templates: `SustainObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `SustainTime` | Time |  |  | How long the Status should be sustained in order to solve the Quest |
| `ResetTimer` | Boolean |  |  | Should the timer be resetted to the initial value, in case the player counter is not be fulfilled anymore? |
| `SustainObjectiveText` | Text |  | NeededProperty=Text | Defines the headline text for the timer. If an icon is assigned to the text GUID, it is shown in the Quest Tracker. |
| `LimitToQuestArea_Sustain` | Boolean |  |  | Indicates whether the player counter should only be checked on the current quest area. Note, that the player counter must match AREA in order to use this. |
| `BestAreaIsHighestValueSustain` | Boolean |  |  | If true the area with the highest counter among all areas will be returned. Otherwise the lowest |

Explicit property defaults:

```xml
<ConditionQuestSustain>
                  <SustainObjectiveText>0</SustainObjectiveText>
                  <BestAreaIsHighestValueSustain>1</BestAreaIsHighestValueSustain>
                </ConditionQuestSustain>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionQuestTutorial

Source: properties-toolone.xml:5307. Captured owning templates: `TutorialObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `InteractionFlow` | Vector |  |  |  |
| `InteractionFlow/Item/TutorialInteraction` | AutoCreateAsset |  | AllowedTemplates=; AllowedProperties=ConditionTutorialInteraction |  |
| `InteractionFlowGamepad` | Vector |  |  | Is used when we are in gamepad mode and there are some interactions configured |
| `InteractionFlowGamepad/Item/TutorialInteraction` | AutoCreateAsset |  | AllowedTemplates=; AllowedProperties=ConditionTutorialInteraction | Is used when we are in gamepad mode and there are some interactions configured |

Explicit property defaults:

```xml
<ConditionQuestTutorial>
                  <InteractionFlow/>
                  <InteractionFlowGamepad/>
                </ConditionQuestTutorial>
```

Container defaults (entry contents):

```xml
<ConditionQuestTutorial>
                  <InteractionFlow>
                    <TutorialInteraction>
                      <Template>ConditionTutorialInteraction</Template>
                      <Values>
                        <Condition/>
                        <ConditionTutorialInteraction>
                          <ObjectFilter>
                            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                            <Template>ObjectFilter</Template>
                            <Values>
                              <ObjectFilter/>
                            </Values>
                          </ObjectFilter>
                        </ConditionTutorialInteraction>
                      </Values>
                    </TutorialInteraction>
                  </InteractionFlow>
                  <InteractionFlowGamepad>
                    <TutorialInteraction>
                      <Template>ConditionTutorialInteraction</Template>
                      <Values>
                        <Condition/>
                        <ConditionTutorialInteraction>
                          <ObjectFilter>
                            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                            <Template>ObjectFilter</Template>
                            <Values>
                              <ObjectFilter/>
                            </Values>
                          </ObjectFilter>
                        </ConditionTutorialInteraction>
                      </Values>
                    </TutorialInteraction>
                  </InteractionFlowGamepad>
                </ConditionQuestTutorial>
```

### ConditionQuestUseItemInArea

Source: properties-toolone.xml:5336. Captured owning templates: `UseItemInAreaObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TargetObject` | Asset |  |  |  |
| `ItemToUse` | Asset |  |  |  |
| `StartPlace` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectPlayerKontor;ConditionObjectClientQuestObject;ConditionObjectPrebuiltObject;ConditionObjectSpawnedObject;ConditionObjectAnywhere; AllowedProperties= |  |
| `TargetAmount` | Integer |  |  |  |
| `UseItemInAreaSignsAndFeedback` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectiveSignsAndFeedback; AllowedProperties= | these signs and feedback are used for the objects where the items should be used |

Explicit property defaults:

```xml
<ConditionQuestUseItemInArea>
                  <TargetObject>0</TargetObject>
                  <ItemToUse>0</ItemToUse>
                  <StartPlace>
                    <Template>ConditionObjectPlayerKontor</Template>
                    <Values>
                      <ConditionObjectPlayerKontor/>
                      <ConditionScanner/>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </StartPlace>
                  <UseItemInAreaSignsAndFeedback>
                    <Template>ConditionObjectiveSignsAndFeedback</Template>
                    <Values>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </UseItemInAreaSignsAndFeedback>
                </ConditionQuestUseItemInArea>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionRecipeResearchCompleted

Source: properties-toolone.xml:2737. Captured owning templates: `ConditionRecipeResearchCompleted`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `CompletedResearchField` | Flags | [ResearchFields](trigger-datasets.md#researchfields) |  | All research fields that should be checked |
| `ResearchComparisonOp` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  | The operator to compare the completed research recipes and the desired amount |
| `ResearchDesiredAmount` | Integer |  | Min=0 | The desired amount of completed research recipes |
| `ResearchRangeOp` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  | Defines which research fields need to match the desired amount |
| `ResearchRelativeToQuestStart` | Boolean |  |  | True: Counting from current condition start - False: Counting from 0. |

Explicit property defaults:

```xml
<ConditionRecipeResearchCompleted>
                  <CompletedResearchField/>
                  <ResearchComparisonOp>AtLeast</ResearchComparisonOp>
                  <ResearchRangeOp>None</ResearchRangeOp>
                </ConditionRecipeResearchCompleted>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionReminderMessage

Source: properties-toolone.xml:2769. Captured owning templates: none; schema-only in this template set. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionReminderMessage/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionReputation

Source: properties-toolone.xml:2772. Captured owning templates: `ConditionReputation`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Reputation` | Integer |  |  | [IngameValue] [ComparisonOperator] [Reputation] e.g. X &lt; 5 |
| `ComparisonOperator` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |

Explicit property defaults:

```xml
<ConditionReputation>
                  <ComparisonOperator>AtLeast</ComparisonOperator>
                </ConditionReputation>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionResearchPointLimitReached

Source: properties-toolone.xml:2785. Captured owning templates: `ConditionResearchPointLimitReached`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionResearchPointLimitReached/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionResidentsInBuilding

Source: properties-toolone.xml:2788. Captured owning templates: `ConditionResidentsInBuilding`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ResidentsComparisonOP` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `ResidentsAmount` | Integer |  |  |  |
| `ResidentsBuildingRangeOP` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  | All Found Buildings need to reach the amount, any, or none? |

Explicit property defaults:

```xml
<ConditionResidentsInBuilding>
                  <ResidentsComparisonOP>AtLeast</ResidentsComparisonOP>
                  <ResidentsBuildingRangeOP>All</ResidentsBuildingRangeOP>
                </ConditionResidentsInBuilding>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionScanner

Source: properties-toolone.xml:1272. Captured owning templates: `ConditionObjectClientQuestObject`, `ConditionObjectPlayerKontor`, `ConditionObjectPrebuiltObject`, `ConditionObjectSpawnedObject`, `ConditionObjectStarterObject`, `ConditionScanner`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `DEPRECATED_ScannerAmount` | Integer |  | ReadOnly=1; Min=0 |  |
| `DEPRECATED_ScannerPool` | Vector |  | ReadOnly=1 |  |
| `DEPRECATED_ScannerPool/Item/GUID` | Asset |  | ReadOnly=1; NeededProperty=Scanner;ObjectPool |  |
| `ScannerPoolAdvanced` | Vector |  |  |  |
| `ScannerPoolAdvanced/Item/Scanner` | AutoCreateAsset |  | AllowedTemplates=QuestObjectList; AllowedProperties= |  |

Explicit property defaults:

```xml
<ConditionScanner>
              <DEPRECATED_ScannerPool/>
              <ScannerPoolAdvanced/>
            </ConditionScanner>
```

Container defaults (entry contents):

```xml
<ConditionScanner>
              <DEPRECATED_ScannerPool>
                <GUID>0</GUID>
              </DEPRECATED_ScannerPool>
              <ScannerPoolAdvanced>
                <Scanner>
                  <Template>QuestObjectList</Template>
                  <Values>
                    <ObjectList/>
                  </Values>
                </Scanner>
              </ScannerPoolAdvanced>
            </ConditionScanner>
```

### ConditionSeason

Source: properties-toolone.xml:2806. Captured owning templates: `ConditionSeason`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `SeasonToCheck` | Asset |  | NeededProperty=Season |  |
| `SessionToCheck` | Asset |  | NeededProperty=Session | Session to check season for. If empty all sessions will be checked. |

Explicit property defaults:

```xml
<ConditionSeason>
                  <SeasonToCheck>0</SeasonToCheck>
                  <SessionToCheck>0</SessionToCheck>
                </ConditionSeason>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionSelectionHappinessDebuffActive

Source: properties-toolone.xml:2820. Captured owning templates: `ConditionSelectionHappinessDebuffActive`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `HapinessCategoriesToCheck` | Flags | [HappinessCategory](trigger-datasets.md#happinesscategory) |  |  |
| `HapinessCategoryRangeOP` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  |  |

Explicit property defaults:

```xml
<ConditionSelectionHappinessDebuffActive>
                  <HapinessCategoriesToCheck/>
                  <HapinessCategoryRangeOP>None</HapinessCategoryRangeOP>
                </ConditionSelectionHappinessDebuffActive>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionSessionLoading

Source: properties-toolone.xml:2833. Captured owning templates: `ConditionSessionLoading`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<ConditionSessionLoading/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionShipsInRange

Source: properties-toolone.xml:2836. Captured owning templates: `ConditionShipsInRange`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Range` | Integer |  | Min=0 | The range in which the ships can be detected |
| `TargetObject_sir` | Asset |  |  | The object that the ships should be near to |
| `CheckSpecificTargetOwner` | Boolean |  |  | Indicates whether the owner of the target object should be specified. |
| `UseProcessingParticipantAsTarget` | Boolean |  |  |  |
| `TargetOwnerParticipant` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | The owner of the target object |
| `CheckSpecificShipOwner` | Boolean |  |  | Indicates whether a specific owner of the ships should be checked |
| `UseProcessingParticipantAsShipOwner` | Boolean |  |  |  |
| `ShipOwnerParticipant` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | The particpant whose ships are checked to be near the target |
| `UseSpecificShipGuid` | Boolean |  |  | Indicates whether a specific ship needs to be close to the target. If empty, any ship will be able to fulfill the condition |
| `SpecifiedShipOrPool` | Asset |  |  | The guid of the ship or ship pool that should be near the target object(s) |
| `AllowKontorsInRange` | Boolean |  |  | True if ships and kontors are valid objects in range, False if only ships are |

Explicit property defaults:

```xml
<ConditionShipsInRange>
                  <TargetObject_sir>0</TargetObject_sir>
                  <TargetOwnerParticipant>Human0</TargetOwnerParticipant>
                  <ShipOwnerParticipant>Human0</ShipOwnerParticipant>
                  <SpecifiedShipOrPool>0</SpecifiedShipOrPool>
                </ConditionShipsInRange>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionShipsOwnedInSession

Source: properties-toolone.xml:2896. Captured owning templates: `ConditionShipsOwnedInSession`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ShipSession` | Asset |  | NeededProperty=Session | The session in which the ship amount is checked |
| `ShipTarget` | Asset |  |  | The target ship GUID that should be checked (also accepts asset pools) |
| `ShipComparison` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  | The type of comparision that should be use to check the ship amount |
| `ShipAmount` | Integer |  | Min=0 | The ship amount that should be checked |
| `ShipOwner` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | The owner of the ships |

Explicit property defaults:

```xml
<ConditionShipsOwnedInSession>
                  <ShipSession>0</ShipSession>
                  <ShipTarget>0</ShipTarget>
                  <ShipComparison>AtLeast</ShipComparison>
                  <ShipOwner>Human0</ShipOwner>
                </ConditionShipsOwnedInSession>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionShipyardState

Source: properties-toolone.xml:2929. Captured owning templates: `ConditionShipyardState`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ShipyardIsSomethingInQueue` | Boolean |  |  | true, if any object is currently in the construction queue of this shipyard |
| `ShipyardOwner` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  |  |

Explicit property defaults:

```xml
<ConditionShipyardState>
                  <ShipyardOwner>Human0</ShipyardOwner>
                </ConditionShipyardState>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionStarterObject

Source: properties-toolone.xml:5364. Captured owning templates: `ConditionStarterObject`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `MoveIntoSession` | Boolean |  |  | True, if the StarterObjectObject should move into the session to the docking place. False, if the StarterObjectObject should be selectable from the very beginning |
| `DockingPlaceDistance` | Float |  |  | If MoveIntoSession is true, then the StarterObjectObject tries to come near StarterObjectDockingPlace, respecting this distance |
| `StarterObjectObject` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectPlayerKontor;ConditionObjectClientQuestObject;ConditionObjectPrebuiltObject;ObjectFilterWithSignsAndFeedback;ConditionObjectSpawnedObject; AllowedProperties= | The object that needs to be selected to start the quest. If MoveIntoSession is true, this object (=ship) will need to move into position first |
| `StarterObjectDockingPlace` | AutoCreateAsset |  | AllowedTemplates=ConditionObjectClientQuestObject;ConditionObjectPlayerKontor;ConditionObjectPrebuiltObject; AllowedProperties= | The place where the StarterObjectObject tries to move to, when MoveIntoSession is true |
| `OverwriteExistingQuestArea` | Boolean |  |  | If true, the starter condition will not only set the area of the starter object as quest area when it is empty but also when is already set |

Explicit property defaults:

```xml
<ConditionStarterObject>
                  <StarterObjectObject>
                    <Template>ConditionObjectPlayerKontor</Template>
                    <Values>
                      <ConditionObjectPlayerKontor/>
                      <ConditionScanner/>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </StarterObjectObject>
                  <StarterObjectDockingPlace>
                    <Template>ConditionObjectClientQuestObject</Template>
                    <Values>
                      <ConditionObjectClientQuestObject/>
                      <ConditionScanner/>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </StarterObjectDockingPlace>
                </ConditionStarterObject>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionStaticResult

Source: properties-toolone.xml:2942. Captured owning templates: `ConditionStaticResult`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ConditionResult` | Choice | [ConditionResult](trigger-datasets.md#conditionresult) |  |  |
| `IsNotReached` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionStaticResult>
                  <ConditionResult>Success</ConditionResult>
                </ConditionStaticResult>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionTextPopupClosed

Source: properties-toolone.xml:2954. Captured owning templates: `ConditionTextPopupClosed`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TextPopupLayouts` | Flags | [TextPopupLayout](trigger-datasets.md#textpopuplayout) |  |  |

Explicit property defaults:

```xml
<ConditionTextPopupClosed>
                  <TextPopupLayouts/>
                </ConditionTextPopupClosed>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionTextPopupPagesViewed

Source: properties-toolone.xml:2962. Captured owning templates: `ConditionTextPopupPagesViewed`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `PagesViewed` | Array | [TextPopupLayout](trigger-datasets.md#textpopuplayout) |  |  |
| `PagesViewed/{dataset key}/ViewCount` | Integer |  |  |  |

Explicit property defaults:

```xml
<ConditionTextPopupPagesViewed>
                  <PagesViewed/>
                </ConditionTextPopupPagesViewed>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionThreshold

Source: properties-toolone.xml:2976. Captured owning templates: `ConditionThreshold`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `DataSource` | String |  |  |  |
| `LowerThreshold` | Float |  |  |  |
| `UpperThreshold` | Float |  |  |  |
| `ThresholdDuration` | Time |  |  |  |
| `IsAreaSpecific` | Boolean |  |  |  |

Explicit property defaults:

```xml
<ConditionThreshold/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionTimePassed

Source: properties-toolone.xml:2999. Captured owning templates: `ConditionTimePassed`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TimePassedComp` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  |  |
| `TimePassed` | Time |  |  |  |

Explicit property defaults:

```xml
<ConditionTimePassed>
                  <TimePassedComp>AtLeast</TimePassedComp>
                </ConditionTimePassed>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionTimer

Source: properties-toolone.xml:3011. Captured owning templates: `ConditionTimer`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TimeLimit` | Time |  |  | A time limit for the timer. |
| `IsPaused` | Boolean |  |  | True, when the timer is currently not ticking |
| `TimerID` | String |  |  | An ID by which the timer can be referenced from other conditions or actions. |
| `KeepTimerOnUnregister` | Boolean |  |  | timer value is not reset when condition is unregistered |

Explicit property defaults:

```xml
<ConditionTimer/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionTradeRouteCount

Source: properties-toolone.xml:3034. Captured owning templates: `ConditionTradeRouteCount`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TradeRouteCount` | Integer |  |  |  |
| `CountComparisonOp` | Choice | [ComparisonOperator](trigger-datasets.md#comparisonoperator) |  | Comparison operator the is used to check the current count, i.e. (CurrentGameValue) (ComparisonOPerator) (TradeRouteCount) |
| `FilterTradeRouteTransportationType` | Flags | [TradeRouteTransportationType](trigger-datasets.md#traderoutetransportationtype) |  | Only routes with the given transportation type will be counted. Will be skipped if no flag is set |
| `FilterAssignedTradeRouteObjectOrPool` | Asset |  |  | Only routes with the given assigned objects will be counted. Will be skipped if no asset or pool is set |
| `FilterTradeRoutesWithoutWarnings` | Boolean |  |  | If true, only trade routes without warnings will be counted |

Explicit property defaults:

```xml
<ConditionTradeRouteCount>
                  <CountComparisonOp>AtLeast</CountComparisonOp>
                </ConditionTradeRouteCount>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ConditionTutorialInteraction

Source: properties-toolone.xml:3063. Captured owning templates: `ConditionTutorialInteraction`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `HintType` | Choice | [TutorialUiHintType](trigger-datasets.md#tutorialuihinttype) |  | The type of hint that should be displayed |
| `AllowedInputTypes` | Flags | [InputMode](trigger-datasets.md#inputmode) |  | Condition will be skipped if the active input mode is not checked here |
| `ShowScrollHintWhenOffscreen` | Boolean |  |  | True = When the hinted object is offscreen, show a marked in that direction. False = Don't. |
| `TutorialConditionType` | Choice | [TutorialCondition](trigger-datasets.md#tutorialcondition) |  | The type of interaction that should be checked |
| `NegateTutorialConditionType` | Boolean |  |  | Indicates whether the tutorial condition type should be negated to succeed (NOT selected, NOT visible, etc.) |
| `HintEndCondition` | Choice | [TutorialUiHintEndCondition](trigger-datasets.md#tutorialuihintendcondition) |  | The condition that has to be fulfilled to hide the hint |
| `HintDisplayTime` | Time |  |  | The duration the hint should be displayed before it disappears automatically |
| `HintAnchor` | Choice | [TutorialUiHintAnchor](trigger-datasets.md#tutorialuihintanchor) |  | Describes the direction of the arrow pointing of to the tutorial element. The box will be positioned accordingly |
| `HintText` | Text |  | NeededProperty=Text | The text that should be displayed in the ui hint box |
| `TutorialUiCategory` | Choice | [TutorialUiCategory](trigger-datasets.md#tutorialuicategory) |  | The category of the tutorial that is used to reference phoenix objects |
| `RefGuid` | Integer |  |  | The RefGUID of the phoenix element that should be highlighted |
| `RefGuidGamepad` | Asset |  | NeededProperty=TutorialUiElement |  |
| `ContextObject` | Asset |  | ReadOnly=1; NeededProperty=Object |  |
| `OnlyShowOnQuestObjects` | Boolean |  |  |  |
| `ObjectFilter` | AutoCreateAsset |  | AllowedTemplates=ObjectFilter; AllowedProperties= |  |
| `HidePortrait` | Boolean |  |  | Indicates whether the speech bubble should have a portrait or not (false = show portrait) |
| `UseSpecificPortrait` | Boolean |  |  | Indicates whether a special portrait should be used for the hint. If false, the quest giver will be taken |
| `SpecificPortraitProfile` | Asset |  | NeededProperty=Profile | The profile asset of the portrait that should be displayed |
| `SpecifyHintColorType` | Boolean |  |  | Indicates whether there should be a specific color for the background of the hint |
| `HintColorType` | Choice | [TutorialUiHintColorType](trigger-datasets.md#tutorialuihintcolortype) |  | The specific (background) color of the hint  |
| `UseSmallPortrait` | Boolean |  |  |  |
| `DeselectObjectOnClose` | Boolean |  |  |  |
| `ScreenOpenConditionType` | Choice | [TutorialConditionScreenType](trigger-datasets.md#tutorialconditionscreentype) |  |  |
| `ScreenOpenConditionFlow` | Vector |  |  | Configure additional screens here that are also part of the flow. |
| `ScreenOpenConditionFlow/Item/Screen` | Choice | [TutorialConditionScreenType](trigger-datasets.md#tutorialconditionscreentype) |  |  |

Explicit property defaults:

```xml
<ConditionTutorialInteraction>
                  <HintType>None</HintType>
                  <ShowScrollHintWhenOffscreen>1</ShowScrollHintWhenOffscreen>
                  <TutorialConditionType>Click</TutorialConditionType>
                  <HintEndCondition>None</HintEndCondition>
                  <HintAnchor>Top</HintAnchor>
                  <HintText>0</HintText>
                  <TutorialUiCategory>ConstructionMenu</TutorialUiCategory>
                  <ContextObject>0</ContextObject>
                  <ObjectFilter>
                    <Template>ObjectFilter</Template>
                    <Values>
                      <ObjectFilter/>
                    </Values>
                  </ObjectFilter>
                  <SpecificPortraitProfile>0</SpecificPortraitProfile>
                  <HintColorType>Info</HintColorType>
                  <ScreenOpenConditionType>ConstructionMenu</ScreenOpenConditionType>
                  <ScreenOpenConditionFlow>ConstructionMenu</ScreenOpenConditionFlow>
                  <ScreenOpenConditionFlow>Economy</ScreenOpenConditionFlow>
                </ConditionTutorialInteraction>
```

Container defaults (entry contents):

```xml
<ConditionTutorialInteraction>
                  <ScreenOpenConditionFlow>
                    <Screen>ConstructionMenu</Screen>
                  </ScreenOpenConditionFlow>
                </ConditionTutorialInteraction>
```

### ConditionUnlockList

Source: properties-toolone.xml:3209. Captured owning templates: `ConditionUnlockedList`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `UnlockNeededList` | Vector |  |  |  |
| `UnlockNeededList/Item/UnlockNeeded` | Asset |  |  |  |
| `UnlockRangeOP` | Choice | [RangeOperator](trigger-datasets.md#rangeoperator) |  |  |

Explicit property defaults:

```xml
<ConditionUnlockList>
                  <UnlockNeededList/>
                  <UnlockRangeOP>None</UnlockRangeOP>
                </ConditionUnlockList>
```

Container defaults (entry contents):

```xml
<ConditionUnlockList>
                  <UnlockNeededList>
                    <UnlockNeeded>0</UnlockNeeded>
                  </UnlockNeededList>
                </ConditionUnlockList>
```

### ConditionUnlocked

Source: properties-toolone.xml:3202. Captured owning templates: `ConditionUnlocked`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `UnlockNeeded` | Asset |  |  |  |

Explicit property defaults:

```xml
<ConditionUnlocked>
                  <UnlockNeeded>0</UnlockNeeded>
                </ConditionUnlocked>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### EmptyAutoCreateValue

Source: properties-toolone.xml:8537. Captured owning templates: `EmptyAutoCreateValue`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| No declared ValueDefinition | | | | |

Explicit property defaults:

```xml
<EmptyAutoCreateValue/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### Locked

Source: properties-toolone.xml:28805. Captured owning templates: `FeatureUnlock`, `UnlockableAsset`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `DefaultLockedState` | Boolean |  |  |  |
| `Unpackable` | Boolean |  |  | Is the asset unpackable for the player and will need additional interaction |
| `DLCDependency` | Asset |  | NeededProperty=UplayProduct | Enter the DLC asset here, if this asset is only available with a DLC |
| `Scope` | Choice | [LockScope](trigger-datasets.md#lockscope) |  |  |
| `VisibleWhenLocked` | Boolean |  |  |  |

Explicit property defaults:

```xml
<Locked>
          <DefaultLockedState>1</DefaultLockedState>
          <DLCDependency>0</DLCDependency>
          <Scope>Participant</Scope>
        </Locked>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### ObjectFilter

Source: properties-toolone.xml:518. Captured owning templates: `BusActivationNeedSaturationObjective`, `ConditionBusActivationNeedSaturation`, `ConditionFactoryProductivity`, `ConditionHaciendaDecreesActive`, `ConditionInStorage`, `ConditionIrrigatedModules`, `ConditionIsBuffed`, `ConditionIsIndustrialized`, `ConditionIsPaused`, `ConditionModuleCount`, `ConditionMonumentProgress`, `ConditionObjectPosition`, `ConditionObjectSelected`, `ConditionResidentsInBuilding`, `FactoryProductivityObjective`, `ObjectFilterWithSignsAndFeedback`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ObjectLabel` | String |  |  | object label of a single object or group label for a group of objects |
| `ObjectGUID` | Asset |  | NeededProperty=Mesh | finds all objects with this GUID (performance critical!) which belong to ObjectParticipant |
| `CheckParticipantID` | Boolean |  |  | If true, ObjectParticipantID will be used to additionally check the owner of the objects |
| `CheckProcessingParticipantID` | Boolean |  |  |  |
| `ObjectParticipantID` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | use together with ObjectGUID |
| `ObjectUseParentConditionObjects` | Boolean |  |  | Only used in Actions! Uses the objects that the parent condition found during evaluation. This is not implemented for many conditions yet, please contact PRG before you use this value |
| `ObjectIslands` | Vector |  |  |  |
| `ObjectIslands/Item/Island` | Asset |  | NeededProperty=Island |  |
| `ObjectSession` | Asset |  | NeededProperty=Session | If provided, only objects from the given session are filtered |
| `CheckQuestStarterSession` | Boolean |  |  | If true and this action is fired from within a quest, the quest start session will be checked for objects |
| `CheckQuestArea` | Boolean |  |  | If true and this filter is used within a quest, then the current quest area (if any) will be used to filter objects |
| `ObjectivePrebuiltObjectUseVisibilityAutomatism` | Boolean |  |  | This flag is only used in quest objectives! If true the quest will remember the initial object visibility on quest start and set the object to visible. When the quest ends it will restore the initial visibility again. If false, the object visibility is not touched |
| `ObjectRestrictToQuestObjects` | Boolean |  |  | If true and this action is fired from within a quest, only objects that are used in the linked quest will be taken into account |
| `IncludePreviewObjects` | Boolean |  |  |  |
| `IncludeOnlyBlueprintObjects` | Boolean |  |  | If true, ONLY blueprint objects will be filtered for. All other include booleans will be ignored in this case. |
| `IncludeEditorObjects` | Boolean |  |  |  |
| `MaxObjectCount` | Integer |  | Min=0 | If &gt; 0 this will set an upper limit for the number of filtered objects. Objects will be chosen at random from the filtered object list |

Explicit property defaults:

```xml
<ObjectFilter>
              <ObjectGUID>0</ObjectGUID>
              <ObjectParticipantID>Human0</ObjectParticipantID>
              <ObjectIslands/>
              <ObjectSession>0</ObjectSession>
            </ObjectFilter>
```

Container defaults (entry contents):

```xml
<ObjectFilter>
              <ObjectIslands>
                <Island>0</Island>
              </ObjectIslands>
            </ObjectFilter>
```

### ObjectTargetFilter

Source: properties-toolone.xml:706. Captured owning templates: `ConditionObjectPosition`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TargetLabel` | String |  |  | object label of a single object or group label for a group of objects |
| `TargetGUID` | Asset |  |  | finds all objects with this GUID (performance critical!) which belong to TargetParticipant |
| `TargetCheckParticipantID` | Boolean |  |  | If true, ObjectParticipantID will be used to additionally check the owner of the objects |
| `TargetCheckProcessingParticipantID` | Boolean |  |  |  |
| `TargetParticipantID` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | use together with TargetGUID |
| `TargetUseParentConditionObjects` | Boolean |  |  | Only used in Actions! Uses the objects that the parent condition found during evaluation. This is not implemented for many conditions yet, please contact PRG before you use this value |
| `TargetObjectIslands` | Vector |  |  |  |
| `TargetObjectIslands/Item/Island` | Asset |  | NeededProperty=Island |  |
| `TargetObjectSession` | Asset |  | NeededProperty=Session | If provided, only objects from the given session are filtered |
| `TargetCheckQuestStarterSession` | Boolean |  |  | If true and this action is fired from within a quest, the quest start session will be checked for objects |
| `TargetCheckQuestArea` | Boolean |  |  | If true and this filter is used within a quest, then the current quest area (if any) will be used to filter objects |
| `TargetObjectivePrebuiltObjectUseVisibilityAutomatism` | Boolean |  |  | This flag is only used in quest objectives! If true the quest will remember the initial object visibility on quest start and set the object to visible. When the quest ends it will restore the initial visibility again. If false, the object visibility is not touched |
| `TargetObjectRestrictToQuestObjects` | Boolean |  |  | If true and this action is fired from within a quest, only objects that are used in the linked quest will be taken into account |
| `TargetIncludePreviewObjects` | Boolean |  |  |  |
| `TargetIncludeOnlyBlueprintObjects` | Boolean |  |  | If true, ONLY blueprint objects will be filtered for. All other include booleans will be ignored in this case. |
| `TargetIncludeEditorObjects` | Boolean |  |  |  |
| `TargetMaxObjectCount` | Integer |  | Min=0 | If &gt; 0 this will set an upper limit for the number of filtered objects. Objects will be chosen at random from the filtered object list |

Explicit property defaults:

```xml
<ObjectTargetFilter>
              <TargetGUID>0</TargetGUID>
              <TargetCheckParticipantID>1</TargetCheckParticipantID>
              <TargetParticipantID>Human0</TargetParticipantID>
              <TargetObjectIslands/>
              <TargetObjectSession>0</TargetObjectSession>
            </ObjectTargetFilter>
```

Container defaults (entry contents):

```xml
<ObjectTargetFilter>
              <TargetObjectIslands>
                <Island>0</Island>
              </TargetObjectIslands>
            </ObjectTargetFilter>
```

### ObjectiveScaling

Source: properties-toolone.xml:608. Captured owning templates: `DeliveryObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `ScaleObjectives` | Boolean |  |  |  |
| `ScaleFactors` | Array | [ProgressLevel](trigger-datasets.md#progresslevel) |  |  |
| `ScaleFactors/{dataset key}/Factor` | Float |  |  |  |

Explicit property defaults:

```xml
<ObjectiveScaling>
              <ScaleFactors/>
            </ObjectiveScaling>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### Objectives

Source: properties-toolone.xml:46472. Captured owning templates: `Quest`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `WinConditions` | Vector |  |  | The conditions that need to be fulfilled to successfully end this quest. |
| `WinConditions/Item/Objective` | AutoCreateAsset |  | AllowedTemplates=ItemUsageObjective;BringVehicleToObjectObjective;ConditionAlwaysFalse;ConditionAlwaysTrue;DeliveryObjective;DeliveryWithAttackerObjective;DestroyObjective;EscortObjective;ExpeditionObjective;FakeQuestObjective;FollowShipObjective;HitMovingTargetObjective;ModuleBuildingEfficiencyObjective;PhotographyObjective;PickupObjective;PicturePuzzleObjective;SelectObjectObjective;SellObjectToParticipantObjective;SmugglerObjective;StatusQuoObjective;SubQuestObjective;SustainObjective;TutorialObjective;UseItemInAreaObjective;DivingBellObjective;DecisionObjective;RecipeResearchCompletedObjective;FactoryProductivityObjective;IslandsWithFertilityObjective;BusActivationNeedSaturationObjective;MonumentDestroyedObjective;AirdropObjective;CameraMovementObjective;GamePadActionObjective; AllowedProperties= |  |
| `WinConditionCompletionOrder` | Choice | [SubConditionCompletionOrder](trigger-datasets.md#subconditioncompletionorder) |  |  |

Explicit property defaults:

```xml
<Objectives>
          <WinConditions/>
          <WinConditionCompletionOrder>Parallel</WinConditionCompletionOrder>
        </Objectives>
```

Container defaults (entry contents):

```xml
<Objectives>
          <WinConditions>
            <Objective>
              <Template>ItemUsageObjective</Template>
              <Values>
                <ConditionQuestObjective>
                  <ObjectiveSignsAndFeedback>
                    <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                    <Template>ConditionObjectiveSignsAndFeedback</Template>
                    <Values>
                      <ConditionObjectiveSignsAndFeedback/>
                    </Values>
                  </ObjectiveSignsAndFeedback>
                  <ObjectiveSuccessMessage>
                    <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                    <Template>CharacterNotification</Template>
                    <Values>
                      <CharacterNotification/>
                      <BaseNotification/>
                      <NotificationSubtitle/>
                    </Values>
                  </ObjectiveSuccessMessage>
                  <OnSuccessActions>
                    <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                    <Template>Actions</Template>
                    <Values>
                      <ActionList/>
                    </Values>
                  </OnSuccessActions>
                </ConditionQuestObjective>
                <ConditionQuestItemUsed/>
                <ConditionPropsSessionSettings/>
                <ConditionPropsExecutionPlaceSettings>
                  <ExecutionPlace>
                    <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                    <Template>ConditionObjectAnywhere</Template>
                    <Values>
                      <ConditionObjectAnywhere/>
                    </Values>
                  </ExecutionPlace>
                </ConditionPropsExecutionPlaceSettings>
              </Values>
            </Objective>
          </WinConditions>
        </Objectives>
```

### ParticipantRelation

Source: properties-toolone.xml:795. Captured owning templates: `ConditionIsDiscovered`, `ConditionReputation`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `SourceIsOwner` | Boolean |  |  | Indicates whether the source participant should be the owner of this condition (in quests this would be the quest receiver) |
| `SourceParticipant` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | The participant that is the source of the relation (its state is checked against or of target) |
| `TargetIsOwner` | Boolean |  |  | Indicates whether the target participant should be the owner of this condition (in quests this would be the quest receiver) |
| `TargetParticipant` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | The target participant of the relation |

Explicit property defaults:

```xml
<ParticipantRelation>
              <SourceParticipant>Human0</SourceParticipant>
              <TargetParticipant>Human0</TargetParticipant>
            </ParticipantRelation>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### PreConditionList

Source: properties-toolone.xml:3738. Captured owning templates: `Quest`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `Condition` | AutoCreateAsset |  | AllowedTemplates=; AllowedProperties=Condition |  |
| `SubConditions` | Vector |  |  |  |
| `SubConditions/Item/SubCondition` | AutoCreateAsset |  | AllowedTemplates=PreConditionList; AllowedProperties= |  |

Explicit property defaults:

```xml
<PreConditionList>
              <Condition>
                <Template>ConditionActiveRegion</Template>
                <Values>
                  <Condition/>
                  <ConditionActiveRegion/>
                </Values>
              </Condition>
              <SubConditions/>
            </PreConditionList>
```

Container defaults (entry contents):

```xml
<PreConditionList>
              <SubConditions>
                <SubCondition>
                  <Template>PreConditionList</Template>
                  <Values>
                    <PreConditionList>
                      <Condition>
                        <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                        <Template>ConditionAlwaysTrue</Template>
                        <Values>
                          <Condition/>
                          <ConditionAlwaysTrue/>
                        </Values>
                      </Condition>
                    </PreConditionList>
                  </Values>
                </SubCondition>
              </SubConditions>
            </PreConditionList>
```

### Quest

Source: properties-toolone.xml:46514. Captured owning templates: `Quest`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `StarterMessage` | Struct |  |  |  |
| `StarterMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `StarterMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `SuccessMessage` | Struct |  |  |  |
| `SuccessMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `SuccessMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `FailureMessage` | Struct |  |  |  |
| `FailureMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `FailureMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `SelectionReminderMessage` | Struct |  |  |  |
| `SelectionReminderMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `SelectionReminderMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `AbortedManuallyMessage` | Struct |  |  |  |
| `AbortedManuallyMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `AbortedManuallyMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `AbortedAutomaticallyMessage` | Struct |  |  |  |
| `AbortedAutomaticallyMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `AbortedAutomaticallyMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `InvitationMessage` | Struct |  |  |  |
| `InvitationMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `InvitationMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `EscortShipSelectedMessage` | Struct |  |  |  |
| `EscortShipSelectedMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `EscortShipSelectedMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `ReminderMessage` | Struct |  |  |  |
| `ReminderMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `ReminderMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `ResolveConfirmationMessage` | Struct |  |  |  |
| `ResolveConfirmationMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `ResolveConfirmationMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `InvitationSmugglerQuestMessage` | Struct |  |  |  |
| `InvitationSmugglerQuestMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `InvitationSmugglerQuestMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `SmugglerQuestTradingStationReached` | Struct |  |  |  |
| `SmugglerQuestTradingStationReached/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `SmugglerQuestTradingStationReached/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `StartInvitationGiveItemMessage` | Struct |  |  |  |
| `StartInvitationGiveItemMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `StartInvitationGiveItemMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `StartFollowShipMessage` | Struct |  |  |  |
| `StartFollowShipMessage/Notification` | AutoCreateAsset |  | AllowedTemplates=CharacterNotification; AllowedProperties= |  |
| `StartFollowShipMessage/SuppressMessage` | Boolean |  |  | Do not play any notification and do not fall back to PamSy configuration |
| `OnQuestStart` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | A list of actions that will be executed when this quest starts. |
| `OnQuestDeclined` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | A list of actions that will be executed when this quest declined. This will be executed before OnQuestEnd. |
| `OnQuestActive` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | A list of actions that will be executed when this quest becomes active. This is when the user actually started the quest. |
| `OnQuestAborted` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | A list of actions that will be executed when this quest is active and aborted by the player. This will be executed before OnQuestEnd. |
| `OnQuestTimedOut` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | A list of actions that will be executed when the pre activation timer of this quest ran out. This will be executed before OnQuestDiscarded and OnQuestEnd. |
| `OnActiveQuestTimedOut` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | A list of actions that will be executed when the active quest timer ran out. This will be executed before OnQuestFailed and OnQuestEnd. |
| `OnQuestFailed` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | A list of actions that will be executed when this quest fails. This will be executed before OnQuestEnd. |
| `OnQuestDiscarded` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | Callback when the quest has been automatically aborted by the system. Gets called before OnQuestEnd. |
| `OnQuestSucceeded` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | A list of actions that will be executed when this quest succeeds. This will be executed before OnQuestEnd. |
| `OnQuestEnd` | AutoCreateAsset |  | AllowedTemplates=Actions; AllowedProperties= | A list of actions that will be executed when this quest ends - independent from the success of the quest. This will be executed at last. |
| `OnPhotographySuccessNewspaperAction` | AutoCreateAsset |  | AllowedTemplates=ActionForceNewspaper; AllowedProperties= | This action will be triggered to show the newspaper for a photography quest. It has no effect if no photography objective is present or if all photography objectives set the flag to not show a newspaper on success. |
| `QuestGiver` | Asset |  | NeededProperty=Profile | This is the guys picture will be shown in the quest. |
| `StoryText` | Text |  | NeededProperty=Text | This is the fluff text of a quest. |
| `DescriptionText` | Asset |  |  | This is the description of a quest. |
| `IsEnabled` | Boolean |  |  | Only enabled quests will be used by the game |
| `MaxCallOut` | Integer |  |  | Maximum number that this quest can be triggered. &lt; 0 means infinite calls are possible |
| `MaxSolveCount` | Integer |  |  | Maximum number that this quest can be solved. &lt;= 0 means infinite calls are possible |
| `MaxAbortCount` | Integer |  |  | Maximum number that this quest can be aborted. &lt;= 0 means infinite calls are possible |
| `CountForQuestLimit` | Boolean |  |  | True if this quest counts for the global and the pool quest limits. |
| `PreActivationTimer` | Time |  |  | This timer cancelles a quest if the quest has not become active until the timer runs out. |
| `QuestTimeLimit` | Time |  |  | If a time limit is set, the quest will fail if it is not completed within this time |
| `QuestCategory` | Choice | [QuestCategory](trigger-datasets.md#questcategory) |  | The category of the quest defines the internal behaviour of the quest. See DDD for details. |
| `QuestActivation` | Choice | [QuestActivationTime](trigger-datasets.md#questactivationtime) |  | Defines at which point this quest changes its status to "Activated". Only activated quests are visible in the Quest Tracker. |
| `IsAbortable` | Boolean |  |  | If true, this quest can be aborted in the assignment center or the quest tracker |
| `NeededProgressLevel` | Flags | [ProgressLevel](trigger-datasets.md#progresslevel) |  | This quest can only be triggered if the player progress level matches these checked levels. |
| `LatencyTimer` | Time |  |  | Latency before a quest can start after all other preconditions are fulfilled. The latency starts again if a single precondition check fails during the countdown. This needs to be checked over the whole duration and is EXPENSIVE for game performance |
| `DelayTimer` | Time |  |  | Delay the quest after the preconditions were fulfilled once. The preconditions will be checked once again after the delay finished. This is a CHEAPER alternative to the latency timer in terms of performance |
| `QuestTrackerVisibility` | Choice | [QuestTrackerVisibility](trigger-datasets.md#questtrackervisibility) |  | Defines when this quest will be visible in the quest tracker. |
| `QuestBookVisibility` | Choice | [QuestBookVisibility](trigger-datasets.md#questbookvisibility) |  | Defines when this quest will be visible in the quest book. |
| `ConfirmOnReached` | Boolean |  |  | After solving the quest stays in quest tracker and needs to be confirmed by player |
| `CustomizeConfirmOnReachedCondition` | Boolean |  |  | If true, a custom confirmOnReached condition can be configured for this quest specifically |
| `ConfirmOnReachedCondition` | AutoCreateAsset |  | AllowedTemplates=ConditionQuestResolveConfirmation; AllowedProperties= | Use this to provide a custom configuration for the resolve confirmation for this quest |
| `HasExclusiveQuestGiver` | Boolean |  |  | Optional quests are only started if no other exclusive quest is already running with the same quest giver |
| `QuestBlackList` | Vector |  |  |  |
| `QuestBlackList/Item/QuestGUID` | Asset |  |  |  |
| `QuestSessionDependencies` | Vector |  |  | If not empty, the quest can only be triggered if one of the specified sessions is loaded |
| `QuestSessionDependencies/Item/SessionOrRegion` | Asset |  | NeededProperty=Session;Region | Session or region(= list of sessions) allowed here |
| `QuestBlockedSessions` | Vector |  |  | If not empty, the quest can not be triggered in one of the specified sessions |
| `QuestBlockedSessions/Item/SessionOrRegion` | Asset |  | NeededProperty=Session;Region | Session or region(= list of sessions) allowed |
| `AlternativeRewardTitle` | Text |  | NeededProperty=Text | An alternative headline for the rewards |
| `QuestDifficulty` | Choice | [QuestDifficulty](trigger-datasets.md#questdifficulty) |  | This is the balanced difficulty of this quest |
| `KeepCheckingPreconditionsWhenRunning` | Boolean |  |  | If true, the quest keeps checking the preconditions and will abort automatically if they are not met any longer |
| `CampaignChapter` | Choice | [QuestCampaignChapter](trigger-datasets.md#questcampaignchapter) |  | Defines to which chapter of the campaign this quest belongs. This is only useful when the questCategory is set to main quest and will be ignored otherwise |
| `QuestBookBackground` | FileName |  |  |  |
| `ReputationQuestFail` | Struct |  |  |  |
| `ReputationQuestFail/ReputationFailList` | Vector |  |  |  |
| `ReputationQuestFail/ReputationFailList/Item/ReputationParticipant` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | The participant that rewards reputation |
| `ReputationQuestFail/ReputationFailList/Item/ReputationAmount` | Integer |  |  | The amount of reputation that is rewarded. This number can be negative to create a reputation loss |
| `ReputationQuestDeclined` | Struct |  |  |  |
| `ReputationQuestDeclined/ReputationDeclinedList` | Vector |  |  |  |
| `ReputationQuestDeclined/ReputationDeclinedList/Item/ReputationParticipant` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | The participant that rewards reputation |
| `ReputationQuestDeclined/ReputationDeclinedList/Item/ReputationAmount` | Integer |  |  | The amount of reputation that is rewarded. This number can be negative to create a reputation loss |
| `QuestGiverIdleMessages` | Vector |  |  |  |
| `QuestGiverIdleMessages/Item/Subtitle` | Asset |  | NeededProperty=AudioText |  |
| `QuestGiverIdleMessageMinPause` | Time |  |  |  |
| `QuestGiverIdleMessageMaxPause` | Time |  |  |  |
| `ResetPreconditionsAfterQuestWasTriggered` | Boolean |  |  | If true, the interal state of all preconditions will be reset. This is especially important for ConditionEvent which otherwise endlessly remembers any received event |
| `RespectRelatedQuestSession` | Boolean |  |  | If true, this quest tries to spawn in the same session as another quest that is configured in the preconditions. We try to determine the correct quest out of all conditions given. An assert will be thrown if we don't manage to find a quest but this flag is set |
| `QuestHints` | Vector |  |  |  |
| `QuestHints/Item/Text` | Text |  | NeededProperty=Text |  |
| `HasStarterSpeechBubble` | Boolean |  |  |  |
| `StarterSpeechBubble` | AutoCreateAsset |  | AllowedTemplates=ConditionTutorialInteraction; AllowedProperties= |  |
| `HasSuccessSpeechBubble` | Boolean |  |  |  |
| `SuccessSpeechBubble` | AutoCreateAsset |  | AllowedTemplates=ConditionTutorialInteraction; AllowedProperties= |  |
| `CanBeActiveForMultipleParticipants` | Boolean |  |  | Only takes effect in quest pools. Checking this will stop preventing the quest from being called from the pool, while another player has this quest running |
| `HasReminderMessage` | Boolean |  |  | True, if this quest should trigger a reminder message when the starter object or another specified object was selected |

Explicit property defaults:

```xml
<Quest>
          <StarterMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </StarterMessage>
          <SuccessMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </SuccessMessage>
          <FailureMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </FailureMessage>
          <SelectionReminderMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </SelectionReminderMessage>
          <AbortedManuallyMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </AbortedManuallyMessage>
          <AbortedAutomaticallyMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </AbortedAutomaticallyMessage>
          <InvitationMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </InvitationMessage>
          <EscortShipSelectedMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </EscortShipSelectedMessage>
          <ReminderMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </ReminderMessage>
          <ResolveConfirmationMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </ResolveConfirmationMessage>
          <InvitationSmugglerQuestMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </InvitationSmugglerQuestMessage>
          <SmugglerQuestTradingStationReached>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </SmugglerQuestTradingStationReached>
          <StartInvitationGiveItemMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </StartInvitationGiveItemMessage>
          <StartFollowShipMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </StartFollowShipMessage>
          <OnQuestStart>
            <Template>Actions</Template>
            <Values>
              <ActionList/>
            </Values>
          </OnQuestStart>
          <OnQuestDeclined>
            <Template>Actions</Template>
            <Values>
              <ActionList/>
            </Values>
          </OnQuestDeclined>
          <OnQuestActive>
            <Template>Actions</Template>
            <Values>
              <ActionList/>
            </Values>
          </OnQuestActive>
          <OnQuestAborted>
            <Template>Actions</Template>
            <Values>
              <ActionList/>
            </Values>
          </OnQuestAborted>
          <OnQuestTimedOut>
            <Template>Actions</Template>
            <Values>
              <ActionList/>
            </Values>
          </OnQuestTimedOut>
          <OnActiveQuestTimedOut>
            <Template>Actions</Template>
            <Values>
              <ActionList/>
            </Values>
          </OnActiveQuestTimedOut>
          <OnQuestFailed>
            <Template>Actions</Template>
            <Values>
              <ActionList/>
            </Values>
          </OnQuestFailed>
          <OnQuestDiscarded>
            <Template>Actions</Template>
            <Values>
              <ActionList/>
            </Values>
          </OnQuestDiscarded>
          <OnQuestSucceeded>
            <Template>Actions</Template>
            <Values>
              <ActionList/>
            </Values>
          </OnQuestSucceeded>
          <OnQuestEnd>
            <Template>Actions</Template>
            <Values>
              <ActionList/>
            </Values>
          </OnQuestEnd>
          <OnPhotographySuccessNewspaperAction>
            <Template>ActionForceNewspaper</Template>
            <Values>
              <Action/>
              <ActionForceNewspaper/>
            </Values>
          </OnPhotographySuccessNewspaperAction>
          <QuestGiver>0</QuestGiver>
          <StoryText>0</StoryText>
          <DescriptionText>0</DescriptionText>
          <IsEnabled>1</IsEnabled>
          <MaxCallOut>-1</MaxCallOut>
          <MaxSolveCount>-1</MaxSolveCount>
          <MaxAbortCount>-1</MaxAbortCount>
          <CountForQuestLimit>1</CountForQuestLimit>
          <QuestTimeLimit>1800000</QuestTimeLimit>
          <QuestCategory>MainQuest</QuestCategory>
          <QuestActivation>QuestStart</QuestActivation>
          <NeededProgressLevel/>
          <QuestTrackerVisibility>Session</QuestTrackerVisibility>
          <QuestBookVisibility>SameAsQuestTracker</QuestBookVisibility>
          <ConfirmOnReachedCondition>
            <Template>ConditionQuestResolveConfirmation</Template>
            <Values>
              <ConditionQuestResolveConfirmation>
                <ResolveConfirmationMessage>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>CharacterNotification</Template>
                  <Values>
                    <CharacterNotification/>
                    <BaseNotification/>
                    <NotificationSubtitle/>
                  </Values>
                </ResolveConfirmationMessage>
              </ConditionQuestResolveConfirmation>
              <Condition/>
              <ConditionQuestObjective>
                <ObjectiveSignsAndFeedback>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>ConditionObjectiveSignsAndFeedback</Template>
                  <Values>
                    <ConditionObjectiveSignsAndFeedback/>
                  </Values>
                </ObjectiveSignsAndFeedback>
                <ObjectiveSuccessMessage>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>CharacterNotification</Template>
                  <Values>
                    <CharacterNotification/>
                    <BaseNotification/>
                    <NotificationSubtitle/>
                  </Values>
                </ObjectiveSuccessMessage>
                <OnSuccessActions>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>Actions</Template>
                  <Values>
                    <ActionList/>
                  </Values>
                </OnSuccessActions>
              </ConditionQuestObjective>
            </Values>
          </ConfirmOnReachedCondition>
          <HasExclusiveQuestGiver>1</HasExclusiveQuestGiver>
          <QuestBlackList/>
          <QuestSessionDependencies/>
          <QuestBlockedSessions/>
          <AlternativeRewardTitle>2653</AlternativeRewardTitle>
          <QuestDifficulty>Easy</QuestDifficulty>
          <CampaignChapter>Chapter1</CampaignChapter>
          <QuestBookBackground>data/ui/2kimages/main/assets16/questbook_bg/bg_quest_polar.png</QuestBookBackground>
          <ReputationQuestFail/>
          <ReputationQuestDeclined/>
          <QuestGiverIdleMessages/>
          <QuestGiverIdleMessageMinPause>20000</QuestGiverIdleMessageMinPause>
          <QuestGiverIdleMessageMaxPause>60000</QuestGiverIdleMessageMaxPause>
          <QuestHints/>
          <StarterSpeechBubble>
            <Template>ConditionTutorialInteraction</Template>
            <Values>
              <Condition/>
              <ConditionTutorialInteraction>
                <ObjectFilter>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>ObjectFilter</Template>
                  <Values>
                    <ObjectFilter/>
                  </Values>
                </ObjectFilter>
              </ConditionTutorialInteraction>
            </Values>
          </StarterSpeechBubble>
          <SuccessSpeechBubble>
            <Template>ConditionTutorialInteraction</Template>
            <Values>
              <Condition/>
              <ConditionTutorialInteraction>
                <ObjectFilter>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>ObjectFilter</Template>
                  <Values>
                    <ObjectFilter/>
                  </Values>
                </ObjectFilter>
              </ConditionTutorialInteraction>
            </Values>
          </SuccessSpeechBubble>
          <HasReminderMessage>1</HasReminderMessage>
        </Quest>
```

Container defaults (entry contents):

```xml
<Quest>
          <StarterMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </StarterMessage>
          <SuccessMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </SuccessMessage>
          <FailureMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </FailureMessage>
          <SelectionReminderMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </SelectionReminderMessage>
          <AbortedManuallyMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </AbortedManuallyMessage>
          <AbortedAutomaticallyMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </AbortedAutomaticallyMessage>
          <InvitationMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </InvitationMessage>
          <EscortShipSelectedMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </EscortShipSelectedMessage>
          <ReminderMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </ReminderMessage>
          <ResolveConfirmationMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </ResolveConfirmationMessage>
          <InvitationSmugglerQuestMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </InvitationSmugglerQuestMessage>
          <SmugglerQuestTradingStationReached>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </SmugglerQuestTradingStationReached>
          <StartInvitationGiveItemMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </StartInvitationGiveItemMessage>
          <StartFollowShipMessage>
            <Notification>
              <Template>CharacterNotification</Template>
              <Values>
                <CharacterNotification/>
                <BaseNotification/>
                <NotificationSubtitle/>
              </Values>
            </Notification>
          </StartFollowShipMessage>
          <QuestBlackList>
            <QuestGUID>0</QuestGUID>
          </QuestBlackList>
          <QuestSessionDependencies>
            <SessionOrRegion>0</SessionOrRegion>
          </QuestSessionDependencies>
          <QuestBlockedSessions>
            <SessionOrRegion>0</SessionOrRegion>
          </QuestBlockedSessions>
          <ReputationQuestFail>
            <ContainerValues>
              <ReputationFailList>
                <ReputationParticipant>Human0</ReputationParticipant>
              </ReputationFailList>
            </ContainerValues>
            <ReputationFailList/>
          </ReputationQuestFail>
          <ReputationQuestDeclined>
            <ContainerValues>
              <ReputationDeclinedList>
                <ReputationParticipant>Human0</ReputationParticipant>
              </ReputationDeclinedList>
            </ContainerValues>
            <ReputationDeclinedList/>
          </ReputationQuestDeclined>
          <QuestGiverIdleMessages>
            <Subtitle>0</Subtitle>
          </QuestGiverIdleMessages>
          <QuestHints>
            <Text>0</Text>
          </QuestHints>
        </Quest>
```

### QuestOptional

Source: properties-toolone.xml:47257. Captured owning templates: `Quest`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `HasStarterObject` | Choice | [QuestStarterObjectChoice](trigger-datasets.md#queststarterobjectchoice) |  |  |
| `StarterObject` | AutoCreateAsset |  | AllowedTemplates=ConditionStarterObject; AllowedProperties= |  |
| `StarterObjectCompletionOrder` | Choice | [SubConditionCompletionOrder](trigger-datasets.md#subconditioncompletionorder) |  | Defines the completion order between the starter object condition and the win conditions |
| `IsUniqueQuest` | Boolean |  | Export=0 | Only used for ToolOne filter possibility |

Explicit property defaults:

```xml
<QuestOptional>
          <HasStarterObject>None</HasStarterObject>
          <StarterObject>
            <Template>ConditionStarterObject</Template>
            <Values>
              <Condition/>
              <ConditionStarterObject>
                <StarterObjectObject>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>ConditionObjectClientQuestObject</Template>
                  <Values>
                    <ConditionObjectClientQuestObject/>
                    <ConditionScanner/>
                    <ConditionObjectiveSignsAndFeedback/>
                  </Values>
                </StarterObjectObject>
                <StarterObjectDockingPlace>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>ConditionObjectClientQuestObject</Template>
                  <Values>
                    <ConditionObjectClientQuestObject/>
                    <ConditionScanner/>
                    <ConditionObjectiveSignsAndFeedback/>
                  </Values>
                </StarterObjectDockingPlace>
              </ConditionStarterObject>
              <ConditionQuestObjective>
                <ObjectiveSignsAndFeedback>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>ConditionObjectiveSignsAndFeedback</Template>
                  <Values>
                    <ConditionObjectiveSignsAndFeedback/>
                  </Values>
                </ObjectiveSignsAndFeedback>
                <ObjectiveSuccessMessage>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>CharacterNotification</Template>
                  <Values>
                    <CharacterNotification/>
                    <BaseNotification/>
                    <NotificationSubtitle/>
                  </Values>
                </ObjectiveSuccessMessage>
                <OnSuccessActions>
                  <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                  <Template>Actions</Template>
                  <Values>
                    <ActionList/>
                  </Values>
                </OnSuccessActions>
              </ConditionQuestObjective>
              <ConditionPropsSessionSettings/>
            </Values>
          </StarterObject>
          <StarterObjectCompletionOrder>Linear</StarterObjectCompletionOrder>
        </QuestOptional>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### Reward

Source: properties-toolone.xml:47519. Captured owning templates: `Quest`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `RewardAssets` | Vector |  |  |  |
| `RewardAssets/Item/Reward` | Asset |  | NeededProperty=Product;Item;RewardPool;RegionRewardPool;ResourceRewardPool;Session;BuildPermit |  |
| `RewardAssets/Item/Amount` | Integer |  |  |  |
| `RewardAssets/Item/SentToQuestArea` | Boolean |  |  | Indicates if the reward should be sent to the kontor of the quest area |
| `RewardAssets/Item/IsHidden` | Boolean |  |  | Indicates whether this reward should not be shown as a reward preview upon quest invitation (i.e. Bonus Reward) |
| `RewardAssets/Item/IsDisguised` | Boolean |  |  | Indicates whether this (item) reward is disguised as visible, but unknown reward to not give away the actual item earned upon invitation |
| `RewardReputation` | Vector |  |  | List of reputation rewards distributed |
| `RewardReputation/Item/ReputationParticipant` | Choice | [ParticipantID](trigger-datasets.md#participantid) |  | The participant that rewards reputation |
| `RewardReputation/Item/ReputationAmount` | Integer |  |  | The amount of reputation that is rewarded. This number can be negative to create a reputation loss |
| `GenerateIgnoreUnlocks` | Boolean |  |  | do not check unlocks when generating rewards |
| `GenerateRewardsUnique` | Boolean |  |  | same Reward GUID is not chosen multiple times if a pool is listed as reward asset |
| `PenaltyList` | Vector |  |  |  |
| `PenaltyList/Item/Penalty` | Struct |  |  |  |
| `PenaltyList/Item/Penalty/Action` | AutoCreateAsset |  | AllowedTemplates=; AllowedProperties=Action |  |
| `PenaltyList/Item/Penalty/IsHidden` | Boolean |  |  |  |
| `PenaltyList/Item/Penalty/IsDisguised` | Boolean |  |  |  |
| `PenaltyList/Item/Penalty/Icon` | Asset |  |  |  |
| `PenaltyList/Item/Penalty/Infotip` | Text |  | NeededProperty=Text |  |

Explicit property defaults:

```xml
<Reward>
          <RewardAssets>
            <Item>
              <Reward>150038</Reward>
              <Amount>1</Amount>
            </Item>
            <Item>
              <Reward>190352</Reward>
              <Amount>1</Amount>
            </Item>
          </RewardAssets>
          <RewardReputation/>
          <PenaltyList/>
        </Reward>
```

Container defaults (entry contents):

```xml
<Reward>
          <RewardAssets>
            <Reward>0</Reward>
          </RewardAssets>
          <RewardReputation>
            <ReputationParticipant>Human0</ReputationParticipant>
          </RewardReputation>
          <PenaltyList>
            <ContainerValues>
              <Penalty>
                <Action>
                  <Template>ActionAddGoodsToItemContainer</Template>
                  <Values>
                    <Action/>
                    <ActionAddGoodsToItemContainer>
                      <ItemContainerObjects>
                        <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                        <Template>ObjectFilter</Template>
                        <Values>
                          <ObjectFilter/>
                        </Values>
                      </ItemContainerObjects>
                    </ActionAddGoodsToItemContainer>
                  </Values>
                </Action>
                <Icon>0</Icon>
                <Infotip>0</Infotip>
              </Penalty>
            </ContainerValues>
            <Penalty/>
          </PenaltyList>
        </Reward>
```

### SessionFilter

Source: properties-toolone.xml:821. Captured owning templates: `ActionSpawnObjects`, `ConditionShipsInRange`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `AllowParentConditionSession` | Boolean |  |  | Allow the session of the parent condition (if any) to be an allowed session for this action |
| `AllowActiveSession` | Boolean |  | ReadOnly=1 | THIS IS CURRENTLY NOT IMPLEMENTED! Ask programming if you really need it! Allows the currently active session to be allowed for this action. |
| `AllowProcessingSession` | Boolean |  |  | Allow the processing session to be an allowed session for this action |
| `Sessions` | Vector |  |  |  |
| `Sessions/Item/Session` | Asset |  | NeededProperty=Session |  |
| `AllowQuestSession` | Boolean |  |  |  |
| `AllowQuestArea` | Boolean |  |  |  |

Explicit property defaults:

```xml
<SessionFilter>
              <AllowParentConditionSession>1</AllowParentConditionSession>
              <Sessions/>
            </SessionFilter>
```

Container defaults (entry contents):

```xml
<SessionFilter>
              <Sessions>
                <Session>0</Session>
              </Sessions>
            </SessionFilter>
```

### SpawnArea

Source: properties-toolone.xml:859. Captured owning templates: `ActionSpawnObjects`, `DestroyObjective`, `DivingBellObjective`, `HitMovingTargetObjective`, `PickupObjective`, `UseItemInAreaObjective`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `SpawnContext` | Choice | [ObjectSpawnerContextType](trigger-datasets.md#objectspawnercontexttype) |  |  |
| `MatcherGUID` | Asset |  | NeededProperty=Matcher |  |
| `ContextGUID` | Asset |  |  | Accepts Assets and AssetPools |
| `ContextMarkerName` | String |  |  | The name of the marker inside the context object where the target object should be spawned |
| `ContextLabel` | String |  |  |  |
| `LimitToQuestArea` | Boolean |  |  |  |
| `SpawnAreaType` | Flags | [SpawnArea](trigger-datasets.md#spawnarea) |  |  |
| `SpreadObjects` | Boolean |  |  |  |
| `DistanceToContext` | Float |  |  |  |
| `MinObjectDistance` | Float |  | Min=0; Max=10000 |  |
| `MaxObjectDistance` | Float |  | Min=0; Max=10000 |  |
| `DistanceToBorder` | Flags | [SpawnBorderDistance](trigger-datasets.md#spawnborderdistance) |  |  |
| `DistanceToIsland` | Flags | [SpawnIslandDistance](trigger-datasets.md#spawnislanddistance) |  |  |

Explicit property defaults:

```xml
<SpawnArea>
              <SpawnContext>Random</SpawnContext>
              <MatcherGUID>0</MatcherGUID>
              <ContextGUID>0</ContextGUID>
              <SpawnAreaType/>
              <DistanceToBorder/>
              <DistanceToIsland/>
            </SpawnArea>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### Standard

Source: properties-toolone.xml:161. Captured owning templates: `FeatureUnlock`, `Quest`, `Trigger`, `UnlockableAsset`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `GUID` | Integer |  | ReadOnly=1 |  |
| `Name` | String |  |  | Internal name of the asset |
| `WikiPage` | String |  | Export=0 | Name of the page after https://wiki.related-designs.de/wiki/display/MMHO/ |
| `Creator` | String |  | Export=0; ReadOnly=1 | Creator of this profile |
| `CreationTime` | String |  | Export=0; ReadOnly=1 | time when this asset was created |
| `Comments` | Vector |  | Export=0; ReadOnly=1 | List of comments for this asset |
| `Comments/Item/Date` | String |  | Export=0 |  |
| `Comments/Item/User` | String |  | Export=0 |  |
| `Comments/Item/Comment` | String |  | Export=0 |  |
| `LastChangeUser` | String |  | Export=0; ReadOnly=1 | user who made the last change |
| `LastChangeTime` | String |  | Export=0; ReadOnly=1 | last time when this asset was changed |
| `IconFilename` | FileName |  |  |  |
| `ID` | String |  |  | ID used to identify this GUID. A constant int will be generated which can be used by programmers |
| `Comment` | String |  | Export=0 | Comment used to describe this asset |
| `InfoDescription` | Text |  | NeededProperty=Text | Description fluff of the object, used with [ToolOneHelper InfoDescription([RefGuid])] |
| `GraphViewConfig` | String |  | Export=0 | The GraphView config to use when opening this asset in the graph view |
| `InheritIconFromParent` | Boolean |  | Export=0 |  |
| `Version` | Choice | [VersionType](trigger-datasets.md#versiontype) | Export=0 |  |

Explicit property defaults:

```xml
<Standard>
          <Comments/>
          <InfoDescription>0</InfoDescription>
          <Version>main</Version>
        </Standard>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

### Text

Source: properties-toolone.xml:289. Captured owning templates: `Quest`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `MaxCharacters` | Integer |  | Export=0 | max characters this text may have. May be ignored when set to 0 |
| `LocaText` | Array | [EditLanguage](trigger-datasets.md#editlanguage) |  |  |
| `LocaText/{dataset key}/Text` | String |  |  |  |
| `LocaText/{dataset key}/LastFinalText` | String |  | Export=0 | Text als der Status auf Final gesetzt wurde |
| `LocaText/{dataset key}/Status` | Choice | [EditingStatus](trigger-datasets.md#editingstatus) |  | Aktueller Status dieses Textes |
| `LocaText/{dataset key}/ExportCount` | Integer |  | Export=0 | how many times this text was exported |
| `Localize` | Boolean |  | Export=0 | true when this text needs to be localized. When set to false the german text will be used for every language |
| `LineID` | Integer |  |  |  |
| `OasisComment` | String |  | Export=0 | Comment visible in Oasis for translation teams |
| `TextOverride` | Asset |  |  |  |

Explicit property defaults:

```xml
<Text>
          <LocaText/>
          <Localize>1</Localize>
          <TextOverride>0</TextOverride>
        </Text>
```

Container defaults (entry contents):

```xml
<Text>
          <LocaText>
            <Status>New</Status>
          </LocaText>
        </Text>
```

### Trigger

Source: properties-toolone.xml:3765. Captured owning templates: `AutoCreateTrigger`, `FeatureUnlock`, `Trigger`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `TriggerCondition` | AutoCreateAsset |  | AllowedTemplates=; AllowedProperties=Condition |  |
| `TriggerActions` | Vector |  |  |  |
| `TriggerActions/Item/TriggerAction` | AutoCreateAsset |  | AllowedTemplates=ActionLink; AllowedProperties=Action |  |
| `SubTriggers` | Vector |  |  |  |
| `SubTriggers/Item/SubTrigger` | AutoCreateAsset |  | AllowedTemplates=AutoCreateTrigger; AllowedProperties= |  |
| `ResetTrigger` | AutoCreateAsset |  | AllowedTemplates=EmptyAutoCreateValue;AutoCreateTrigger; AllowedProperties= |  |

Explicit property defaults:

```xml
<Trigger>
              <TriggerCondition>
                <Template>ConditionActiveRegion</Template>
                <Values>
                  <Condition/>
                  <ConditionActiveRegion/>
                </Values>
              </TriggerCondition>
              <TriggerActions/>
              <SubTriggers/>
              <ResetTrigger>
                <Template>EmptyAutoCreateValue</Template>
                <Values>
                  <EmptyAutoCreateValue/>
                </Values>
              </ResetTrigger>
            </Trigger>
```

Container defaults (entry contents):

```xml
<Trigger>
              <TriggerActions>
                <TriggerAction>
                  <Template>ActionLink</Template>
                  <Values>
                    <ActionLink/>
                  </Values>
                </TriggerAction>
              </TriggerActions>
              <SubTriggers>
                <SubTrigger>
                  <Template>AutoCreateTrigger</Template>
                  <Values>
                    <Trigger>
                      <TriggerCondition>
                        <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                        <Template>ConditionAlwaysTrue</Template>
                        <Values>
                          <Condition/>
                          <ConditionAlwaysTrue/>
                        </Values>
                      </TriggerCondition>
                      <ResetTrigger>
                        <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
                        <Template>EmptyAutoCreateValue</Template>
                        <Values>
                          <EmptyAutoCreateValue/>
                        </Values>
                      </ResetTrigger>
                    </Trigger>
                  </Values>
                </SubTrigger>
              </SubTriggers>
            </Trigger>
```

### TriggerSetup

Source: properties-toolone.xml:3828. Captured owning templates: `FeatureUnlock`, `Trigger`. Native owners and exact definitions are indexed in [native contracts](../reference/triggers/vanilla.json).

| Field path | Type | Dataset | Restrictions / bounds | Native description |
| --- | --- | --- | --- | --- |
| `AutoRegisterTrigger` | Boolean |  |  |  |
| `AutoSelfUnlock` | Boolean |  |  |  |
| `UsedBySecondParties` | Boolean |  |  | If true, this trigger will also be created for all second party players |

Explicit property defaults:

```xml
<TriggerSetup/>
```

Container defaults (entry contents):

No serialized block captured; inspect the original before drawing a runtime conclusion.

