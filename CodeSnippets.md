# xml ModOp code snippets for various purposes

- [ActionExecuteActionByChance with fixed chance](#actionexecuteactionbychance-with-fixed-chance)
- [Delete all kontors from an AI (and therefore removing it from the game)](#delete-all-kontors-from-an-ai-and-therefore-removing-it-from-the-game)
- [Add text to existing strings (from vanilla or other mods)](#add-text-to-existing-strings-from-vanilla-or-other-mods)
- [Limit a building to "once per Island" without UniqueType property](#limit-a-building-to-once-per-island-without-uniquetype-property)
- [Global Buffs](#global-buffs)
- [Area wide Buff based on Area ConditionPlayerCounter conditions](#area-wide-buff-based-on-area-conditionplayercounter-conditions)
- [Add product to Tooltip Arctic Flue Chance](#Add-product-to-tooltip-arctic-flue-chance)

###  ActionExecuteActionByChance with fixed chance
- Usage of ActionExecuteActionByChance without a variable (vanilla xml always uses a variable for this, but we can not add custom variables. So being able to use it with a fixed value is important, but vanilla code has no example of it). 50:50 chance example:

  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```xml
  <TriggerAction>
    <Template>ActionExecuteActionByChance</Template>
    <Values>
      <Action />
      <ActionExecuteActionByChance>
        <ChanceValue>
          <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
          <Values>
            <VariableValue>
              <FloatValue>50</FloatValue>
            </VariableValue>
          </Values>
        </ChanceValue>
        <ActionListChanceSuccess>
          <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
          <Values>
            <ActionList>
              <Actions>
                [...]
              </Actions>
            </ActionList>
          </Values>
        </ActionListChanceSuccess>
        <ActionListChanceFailure>
          <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
          <Values>
            <ActionList>
              <Actions>
                [...]
              </Actions>
            </ActionList>
          </Values>
        </ActionListChanceFailure>
      </ActionExecuteActionByChance>
    </Values>
  </TriggerAction>

  ```
  </details>
If you want sth to happen with different chances based on circumstance, you may try a Trigger with multiple SubTriggers checking for your custom unlocks.
I mean eg. you do 11 "UnlockableAsset" and call them 0%, 10%, 20% up to 100%. Then in the trigger you check for these unlocks with MutuallyExclusive. And eg. if the 10%-unlock is unlocked, the action will be a ActionExecuteActionByChance with FloatValue 10 and your action in success (and nothing in fail). This way you can lock/unlock your UnlockableAssets however you like, to control hat what chance your actions will be executed.

###  Delete all kontors from an AI (and therefore removing it from the game) 
  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```xml
  <ModOp GUID="130248" Type="AddNextSibling">
    <Asset>
      <Template>Trigger</Template>
      <Values>
        <Standard>
          <GUID>1500001161</GUID>
          <Name>Delete Kontors from AI mentioned below</Name>
        </Standard>
        <Trigger>
          <TriggerCondition>
            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
            <Values>
              <Condition />
              <ConditionAlwaysTrue />
            </Values>
          </TriggerCondition>
          <TriggerActions>
            <Item>
              <TriggerAction>
                <Template>ActionDeleteObjects</Template>
                <Values>
                  <Action />
                  <ActionDeleteObjects />
                  <ObjectFilter>
                    <ObjectGUID>700000</ObjectGUID>
                    <CheckParticipantID>1</CheckParticipantID>
                    <ObjectParticipantID>Second_ai_11_Mercier</ObjectParticipantID>
                  </ObjectFilter>
                </Values>
              </TriggerAction>
            </Item>
          </TriggerActions>
        </Trigger>
        <TriggerSetup>
          <AutoRegisterTrigger>1</AutoRegisterTrigger>
          <UsedBySecondParties>0</UsedBySecondParties>
        </TriggerSetup>
      </Values>
    </Asset>
  </ModOp>
  ```
  </details>

###  Add text to existing strings (from vanilla or other mods) 
  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```xml
  <!-- add something to a vanilla text (one can not use [AssetData(10595) Text] within Text 10595, it causes endless loop). here we add " (0%)" after the string. -->
  <ModOp Type="replace" Path="/TextExport/Texts/Text[GUID = '10595']/Text[not(contains(.,' (0%)'))]"
    Content="/TextExport/Texts/Text[GUID = '10595']/Text/text()">
    <Text><ModOpContent /> (0%)</Text>
  </ModOp>
  ```
  </details>

###  Limit a building to "once per Island" without UniqueType property
  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```xml
  <!-- With the following code you can limit your building to only be built once per island, without the need of one of the "UniqueType" Enums, which are only available in limited number (only 20 are available, while many are already in use from other mods) -->
  
  <!-- Copy the whole following code. -->
  <!-- Replace YOUR_BUILDING_GUID with the GUID of your building you want to limit to once per building. -->
  <!-- Replace YOUR_PRODUCT_GUID with a new GUID for the product that will be used as build material for one of your buildings to limit it to "once per island". You need one product per building you want to limit. -->
    <!-- add the product to the "Cost/Costs" property of your building and Ingredient with Amount 1. -->
  <!-- Replace YOUR_QUESTPOOL_GUID with a new GUID for the helper Questpool. One Pool for all your helper Quests is enough. -->
  <!-- Replace YOUR_QUEST_GUID with a new GUID for the helper Quest. You need one helper Quest per building you want to limit. -->
  
  <!-- You also need my shared mod shared_ObjectDummies https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/blob/main/shared_ObjectDummies/data/config/export/main/asset/templates.xml -->
   <!-- to be able to use my template "A7_QuestDummyQuest". Alternatively use A7_QuestStatusQuo and copy paste all properties from my A7_QuestDummyQuest into your Quest and replace them with the new values from here (but better simply use my shared mod) -->
   <!-- You use a shared mod by downloading the whole mod and placing the whole mod folder next to the "data" folder of your mod. Done. -->
    <!-- (This way the shared mod will automatically be loaded when your mod is active and allows you to use eg. my template) -->
  
  
  <!-- Create a new product, one per building you want to limit to "once per island". You can use the very same code like below with your own GUID --> 
  <ModOp Type="addNextSibling" GUID="1010196">
    <Asset>
      <Template>Product</Template>
      <Values>
        <Standard>
          <GUID>YOUR_PRODUCT_GUID</GUID>
          <Name>Once Per Island Build Material</Name>
          <IconFilename>data/ui/2kimages/main/icons/roman_numerals/icon_roman_numerals_1.png</IconFilename>
          <InfoDescription>2359</InfoDescription>
        </Standard>
        <Locked>
          <DefaultLockedState>0</DefaultLockedState>
        </Locked>
        <Text />
        <Product>
          <HideInUI>1</HideInUI>
          <StorageLevel>Building</StorageLevel>
          <ProductCategory>11707</ProductCategory>
          <BasePrice>1</BasePrice>
          <CivLevel>1</CivLevel>
          <AssociatedRegion>Moderate;Colony01;Arctic;Africa</AssociatedRegion>
          <ProductionRegions>
            <Item>
              <RegionType>Moderate</RegionType>
            </Item>
            <Item>
              <RegionType>Colony01</RegionType>
            </Item>
            <Item>
              <RegionType>Arctic</RegionType>
              <RequiredDLCs>
                <Item>
                  <RequiredDLC>410042</RequiredDLC>
                </Item>
              </RequiredDLCs>
            </Item>
            <Item>
              <RegionType>Africa</RegionType>
              <RequiredDLCs>
                <Item>
                  <RequiredDLC>410071</RequiredDLC>
                </Item>
              </RequiredDLCs>
            </Item>
          </ProductionRegions>
        </Product>
        <ExpeditionAttribute />
      </Values>
    </Asset>
  </ModOp>

  <!-- For ActionAddGoodsToItemContainer to work, the product has to be part of this StandardProductStorageList GUID 120055 -->
   <!-- we do not add it to more lists, eg 502004,502017,501957, because we do not want it to be displayed in any list ingame -->
  <ModOp Type="add" GUID='120055' Path="/Values/ProductStorageList/ProductList">
    <Item>
      <Product>YOUR_PRODUCT_GUID</Product>
    </Item>
  </ModOp>


  <!-- we need a helper Quest to be able to use UseQuestAreaKontor, to credit the new product once to every island that does not have neither the product nor the building -->
   <!-- we use DelayTimer to make sure the condition is at least 1 second fullfilled (because when building sth: for 100ms you neither have the product nor the building anymore) -->
  <!-- You can copy paste the whole code and simply exchange the GUID-placeholders with yours -->
  <!-- This is just a help-construct, it will not be visible to anyone as Quest -->
  <ModOp Type="AddNextSibling" GUID="152264">
    <Asset>
      <Template>A7_QuestDummyQuest</Template>
      <Values>
        <Standard>
          <GUID>YOUR_QUEST_GUID</GUID>
          <Name>Add 1 Product to Built once</Name>
        </Standard>
        <Quest>
          <OnQuestSucceeded>
            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
            <Values>
              <ActionList>
                <Actions>
                  <Item>
                    <Action>
                      <Template>ActionAddGoodsToItemContainer</Template>
                      <Values>
                        <Action />
                        <ActionAddGoodsToItemContainer>
                          <Goods>
                            <Item>
                              <Good>YOUR_PRODUCT_GUID</Good>
                              <Amount>1</Amount>
                            </Item>
                          </Goods>
                          <UseQuestAreaKontor>1</UseQuestAreaKontor>
                        </ActionAddGoodsToItemContainer>
                      </Values>
                    </Action>
                  </Item>
                </Actions>
              </ActionList>
            </Values>
          </OnQuestSucceeded>
          <DelayTimer>1000</DelayTimer>
        </Quest>
        <PreConditionList>
          <Condition>
            <Template>ConditionMutualAreaInSubconditions</Template>
            <Values>
              <Condition />
              <ConditionMutualAreaInSubconditions />
            </Values>
          </Condition>
          <SubConditions>
            <Item>
              <SubCondition>
                <Template>PreConditionList</Template>
                <Values>
                  <PreConditionList>
                    <Condition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>YOUR_BUILDING_GUID</Context>
                          <CounterAmount>1</CounterAmount>
                          <ComparisonOp>LessThan</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </Condition>
                  </PreConditionList>
                </Values>
              </SubCondition>
            </Item>
            <Item>
              <SubCondition>
                <Template>PreConditionList</Template>
                <Values>
                  <PreConditionList>
                    <Condition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <PlayerCounter>GoodsInStock</PlayerCounter>
                          <Context>YOUR_PRODUCT_GUID</Context>
                          <CounterAmount>1</CounterAmount>
                          <ComparisonOp>LessThan</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </Condition>
                  </PreConditionList>
                </Values>
              </SubCondition>
            </Item>
          </SubConditions>
        </PreConditionList>
      </Values>
    </Asset>
    
  </ModOp>
  
  <!-- This Pool will frequently check if the PreConditionList of any included Quest is true and start the Quest -->
  <ModOp Type="addNextSibling" GUID="150725">
    <Asset>
      <Template>QuestPool</Template>
      <Values>
        <Standard>
          <GUID>YOUR_QUESTPOOL_GUID</GUID>
          <Name>alwaystrue-QuestPool</Name>
        </Standard>
        <QuestPool>
          <Quests>
            <!-- add your helper quest-GUIDs here, it can be multiple ones if you want to limit multiple buildings. no need to change anything else from this code -->
            <Item>
              <Quest>YOUR_QUEST_GUID</Quest>
            </Item>
          </Quests>
          <PoolCooldown>0</PoolCooldown>
          <QuestCooldown>0</QuestCooldown>
          <CooldownOnQuestStart>1</CooldownOnQuestStart>
          <CooldownOnQuestEnd>0</CooldownOnQuestEnd>
          <AffectedByCooldownFactor>0</AffectedByCooldownFactor>
          <IsMainStoryPool>0</IsMainStoryPool>
          <IsTopLevel>1</IsTopLevel>
          <QuestLimit>1</QuestLimit>
        </QuestPool>
      </Values>
    </Asset>
  </ModOp>


  ```
  </details>

###  Global Buffs
- Adding Global Buffs to human/AIs and make sure thay also work on new entered sessions:

  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```xml
  <!-- Example uses personal GUID range 2001000000 -	2001009999, replace them with your own GUIDs. -->
  <!-- In this example GUID 2001000000 and 2001000001 will be the Buffs you want to apply globally -->
   <!-- They can be InfluenceTitleBuff, GuildhouseBuff, HarbourOfficeBuff, TownhallBuff and any combination of buff properties (usually ending on "..Upgrade", like "ResidenceUpgrade") -->

  <!-- Global Buffs added via "ActionBuff" are only applied to sessions that were already visited by the player/AI (by camera or by ship) at the time of action.  -->
  <!-- That means we need to reapply the buff everytime we enter a new session for the first time -->
  <!-- This can either be done by hardcoding each session GUID in your code and use ConditionActiveSession. But this then only works on Sessions we know. It won't work for mod-session if we did not add their GUIDs as well to our code. -->
   <!-- So the best alternative found your would be the ConditionEvent "SessionEnter". This fires everytime the human player enters any session (switches camera to the session). -->
   <!-- It means it fires too often, but there is not really an alternative that catches all sessions without hardcoding GUIDs. -->
    <!-- So when using "SessionEnter", we will remove and add the global buff again, to reapply it, so it affects all currently visited sessions. -->
  <!-- Unfortunately there is no way to check if a buff is already active for a player in a session, so all we can do is to remove and add the buff again on each SessionEnter -->
  
    <!-- I made alot of helper-shared-mods you can find here: -->
     <!-- https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders- -->
    <!-- two of them will be used in the following code exmaples: shared_IsAIPlayer_Condition and shared_OncePerSessionPerSaveLoad -->

  
  
  <!-- ########################### -->


  <!-- Only for humans -->
   <!-- (using ConditionTimer before resetting the trigger just to not trigger it too often when switching sessions back and forth) -->
  <ModOp GUID="153271" Type="AddNextSibling">
    <Asset>
      <Template>Trigger</Template>
      <Values>
        <Standard>
          <GUID>2001000002</GUID>
          <Name>Apply and reapply Buff 2001000000 to Human</Name>
        </Standard>
        <Trigger>
          <TriggerCondition>
            <Template>ConditionEvent</Template>
            <Values>
              <Condition />
              <ConditionEvent>
                <ConditionEvent>SessionEnter</ConditionEvent>
              </ConditionEvent>
              <ConditionPropsNegatable />
            </Values>
          </TriggerCondition>
          <TriggerActions>
            <Item>
              <TriggerAction>
                <Template>ActionBuff</Template>
                <Values>
                  <Action />
                  <ActionBuff>
                    <BuffAsset>2001000000</BuffAsset>
                    <AddBuff>0</AddBuff>
                    <BuffProcessingParticipant>1</BuffProcessingParticipant>
                  </ActionBuff>
                </Values>
              </TriggerAction>
            </Item>
            <Item>
              <TriggerAction>
                <Template>ActionBuff</Template>
                <Values>
                  <Action />
                  <ActionBuff>
                    <BuffAsset>2001000000</BuffAsset>
                    <AddBuff>1</AddBuff>
                    <BuffProcessingParticipant>1</BuffProcessingParticipant>
                  </ActionBuff>
                </Values>
              </TriggerAction>
            </Item>
          </TriggerActions>
          <ResetTrigger>
            <Template>AutoCreateTrigger</Template>
            <Values>
              <Trigger>
                <TriggerCondition>
                  <Template>ConditionTimer</Template>
                  <Values>
                    <Condition />
                    <ConditionTimer>
                      <TimeLimit>30000</TimeLimit>
                    </ConditionTimer>
                  </Values>
                </TriggerCondition>
              </Trigger>
            </Values>
          </ResetTrigger>
        </Trigger>
        <TriggerSetup>
          <AutoRegisterTrigger>1</AutoRegisterTrigger>
          <UsedBySecondParties>0</UsedBySecondParties>
        </TriggerSetup>
      </Values>
    </Asset>


  <!-- ########################### -->
  <!-- humans and/or AIs -->

  <!-- It will renew the buffs for AI everytime the AI settles any Island, to make sure it is active in every session (since SessionEnter does not work for AI) -->
  <!-- GUID 1500001601 is from my "shared_IsAIPlayer_Condition" shared mod to make sure sth is only executed for AI (and 1500001600 only for human) -->
  <ModOp GUID="153271" Type="AddNextSibling">
    <Asset>
      <Template>Trigger</Template>
      <Values>
        <Standard>
          <GUID>2001000003</GUID>
          <Name>Apply and reapply Buff 2001000000 to Human and Buff 2001000001 to AI</Name>
        </Standard>
        <Trigger>
          <TriggerCondition>
            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
            <Values>
              <Condition>
                <SubConditionCompletionOrder>MutuallyExclusive</SubConditionCompletionOrder>
              </Condition>
              <ConditionAlwaysTrue />
            </Values>
          </TriggerCondition>
          <SubTriggers>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionUnlocked</Template>
                      <Values>
                        <Condition />
                        <ConditionUnlocked>
                          <UnlockNeeded>1500001600</UnlockNeeded>
                        </ConditionUnlocked>
                        <ConditionPropsNegatable />
                      </Values>
                    </TriggerCondition>
                    <SubTriggers>
                      <Item>
                        <SubTrigger>
                          <Template>AutoCreateTrigger</Template>
                          <Values>
                            <Trigger>
                              <TriggerCondition>
                                <Template>ConditionEvent</Template>
                                <Values>
                                  <Condition />
                                  <ConditionEvent>
                                    <ConditionEvent>SessionEnter</ConditionEvent>
                                  </ConditionEvent>
                                  <ConditionPropsNegatable />
                                </Values>
                              </TriggerCondition>
                              <TriggerActions>
                                <Item>
                                  <TriggerAction>
                                    <Template>ActionBuff</Template>
                                    <Values>
                                      <Action />
                                      <ActionBuff>
                                        <BuffAsset>2001000000</BuffAsset>
                                        <AddBuff>0</AddBuff>
                                        <BuffProcessingParticipant>1</BuffProcessingParticipant>
                                      </ActionBuff>
                                    </Values>
                                  </TriggerAction>
                                </Item>
                                <Item>
                                  <TriggerAction>
                                    <Template>ActionBuff</Template>
                                    <Values>
                                      <Action />
                                      <ActionBuff>
                                        <BuffAsset>2001000000</BuffAsset>
                                        <AddBuff>1</AddBuff>
                                        <BuffProcessingParticipant>1</BuffProcessingParticipant>
                                      </ActionBuff>
                                    </Values>
                                  </TriggerAction>
                                </Item>
                              </TriggerActions>
                            </Trigger>
                          </Values>
                        </SubTrigger>
                      </Item>
                    </SubTriggers>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionUnlocked</Template>
                      <Values>
                        <Condition />
                        <ConditionUnlocked>
                          <UnlockNeeded>1500001601</UnlockNeeded>
                        </ConditionUnlocked>
                        <ConditionPropsNegatable />
                      </Values>
                    </TriggerCondition>
                    <SubTriggers>
                      <Item>
                        <SubTrigger>
                          <Template>AutoCreateTrigger</Template>
                          <Values>
                            <Trigger>
                              <TriggerCondition>
                                <Template>ConditionEvent</Template>
                                <Values>
                                  <Condition />
                                  <ConditionEvent>
                                    <ConditionEvent>IslandSettled</ConditionEvent>
                                  </ConditionEvent>
                                  <ConditionPropsNegatable />
                                </Values>
                              </TriggerCondition>
                              <TriggerActions>
                                <Item>
                                  <TriggerAction>
                                    <Template>ActionBuff</Template>
                                    <Values>
                                      <Action />
                                      <ActionBuff>
                                        <BuffAsset>2001000001</BuffAsset>
                                        <AddBuff>0</AddBuff>
                                        <BuffProcessingParticipant>1</BuffProcessingParticipant>
                                      </ActionBuff>
                                    </Values>
                                  </TriggerAction>
                                </Item>
                                <Item>
                                  <TriggerAction>
                                    <Template>ActionBuff</Template>
                                    <Values>
                                      <Action />
                                      <ActionBuff>
                                        <BuffAsset>2001000001</BuffAsset>
                                        <AddBuff>1</AddBuff>
                                        <BuffProcessingParticipant>1</BuffProcessingParticipant>
                                      </ActionBuff>
                                    </Values>
                                  </TriggerAction>
                                </Item>
                              </TriggerActions>
                            </Trigger>
                          </Values>
                        </SubTrigger>
                      </Item>
                    </SubTriggers>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
          </SubTriggers>
          <ResetTrigger>
            <Template>AutoCreateTrigger</Template>
            <Values>
              <Trigger>
                <TriggerCondition>
                  <Template>ConditionTimer</Template>
                  <Values>
                    <Condition />
                    <ConditionTimer>
                      <TimeLimit>30000</TimeLimit>
                    </ConditionTimer>
                  </Values>
                </TriggerCondition>
              </Trigger>
            </Values>
          </ResetTrigger>
        </Trigger>
        <TriggerSetup>
          <AutoRegisterTrigger>1</AutoRegisterTrigger>
          <UsedBySecondParties>1</UsedBySecondParties>
        </TriggerSetup>
      </Values>
    </Asset>
    <!-- For AI: starting a savegame with already settled islands does not count for IslandSettled, so we have to add the buff once after the mod was newly added to enable the buff first time -->
    <Asset>
      <Template>Trigger</Template>
      <Values>
        <Standard>
          <GUID>2001000004</GUID>
        </Standard>
        <Trigger>
          <TriggerCondition>
            <Template>ConditionUnlocked</Template>
            <Values>
              <Condition />
              <ConditionUnlocked>
                <UnlockNeeded>1500001601</UnlockNeeded>
              </ConditionUnlocked>
              <ConditionPropsNegatable />
            </Values>
          </TriggerCondition>
          <TriggerActions />
        </Trigger>
        <TriggerSetup>
          <AutoRegisterTrigger>1</AutoRegisterTrigger>
          <UsedBySecondParties>1</UsedBySecondParties>
        </TriggerSetup>
      </Values>
    </Asset>
    
  </ModOp>
  
  <!-- ########################################################## -->
  
  <!-- Advanced: -->
  <!-- Use the following for humans, if your code might cause lag, eg. because your buff affects alot of targets: -->
   <!-- Use my shared mod: shared_OncePerSessionPerSaveLoad. This adds a new FeatureUnlock you can simply add your actions to, you want to execute everytime the human enters a session for the first time (since loading a savegame) -->
   <!-- That means your buffs are only once per session per gameload renewed, which might cause lag as usual first, but not all the time on every single session-switching. -->
  <ModOp Type="add" GUID="1500004530" Path="Values/Trigger/ResetTrigger/Values/Trigger/TriggerActions">
    <Item>
      <TriggerAction>
        <Template>ActionBuff</Template>
        <Values>
          <Action />
          <ActionBuff>
            <BuffAsset>2001000000</BuffAsset>
            <AddBuff>0</AddBuff>
            <BuffProcessingParticipant>1</BuffProcessingParticipant>
          </ActionBuff>
        </Values>
      </TriggerAction>
    </Item>
    <Item>
      <TriggerAction>
        <Template>ActionBuff</Template>
        <Values>
          <Action />
          <ActionBuff>
            <BuffAsset>2001000000</BuffAsset>
            <AddBuff>1</AddBuff>
            <BuffProcessingParticipant>1</BuffProcessingParticipant>
          </ActionBuff>
        </Values>
      </TriggerAction>
    </Item>
  </ModOp>

  ```
  </details>

###  Area wide Buff based on Area ConditionPlayerCounter conditions
- **WARNING:**
  this code is currently incomplete and not optimal! I will improve it within few days.  
- improved code from previous shared_AreaBuffsHelper, this share mod was removed, because its better as Code Snippet  
- enable/disable Island specifc and islandwide Buffs based on ConditionPlayerCounter-Area-Scope Conditions
- It works by spawning invisible BuffFactories on the island you want which buff all targets on the island. 
- You can spawn/delete them as you please, eg. spawn a debuff as soon as someone reached an amount GoodsInStock and remove again when it goes below.
- use "OwnerChangeTarget" to make the BuffFactories stay when Island was lost/changed owner, to bind the buff permanently to the island.
- below the "ConditionMutualAreaInSubconditions" Condition yo can add any SubTrigger ConditionPlayerCounter condition with Area-Scope you want, current code spawns one per settled island, regardless of any other conditions
- the code requires my shared mods: shared_CopyPools_AP_Kontors, shared_IsAIPlayer_Condition and shared_ObjectDummies (1.08 and higher)
- You find usage of this in my mod Specialised islands (name may change, not released yet)

  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```xml
  WARNING:
  this code is currently incomplete and not optimal! I will improve it within some days.  


  <ModOp Type="AddNextSibling" GUID='132370'>
    
    <!-- ############################################################## -->
    <!-- BuffFactories -->
    
    <!-- These BuffBuildings get OwnerChangeTarget, so they are not destroyed when island is lost/changes owner, which basically means the buffs are from now on tied to the island -->
    <!-- you can of course remove it, if you want the buildings to get destryoed on island loss/owner change -->
    <Asset>
      <Template>BuffFactoryDummy_WithOwner</Template>
      <Values>
        <Standard>
          <GUID>1500004685</GUID>
          <Name>BuffBuilding</Name>
        </Standard>
        <Building>
          <OwnerChangeTarget>1500004685</OwnerChangeTarget>
        </Building>
        <BuffFactory>
          <BaseBuff>1500004686</BaseBuff>
          <BaseBuffScope>Area</BaseBuffScope>
        </BuffFactory>
        <LogisticNode />
        <Pausable />
      </Values>
    </Asset>
    
    <!-- Spawn Helper only required for spawning on AI islands -->
    <Asset>
      <Template>BuildingDummy_WithOwner</Template>
      <Values>
        <Standard>
          <GUID>1500004684</GUID>
          <Name>BuffBuilding - Spawn Helper</Name>
        </Standard>
      </Values>
    </Asset>
    
  </ModOp>
  

  <!-- ##############################################################################   -->
  <!-- Buffs -->
  <ModOp Type="AddNextSibling" GUID='190093'>
    <Asset>
      <Template>GuildhouseBuff</Template>
      <Values>
        <Standard>
          <GUID>1500004686</GUID>
          <Name>Buff Island</Name>
          <IconFilename>data/ui/2kimages/main/3dicons/specialists/systemic/icon_pearl_diver_102.png</IconFilename>
          <InfoDescription>12513</InfoDescription>
        </Standard>
        <FactoryUpgrade>
          <ProductivityUpgrade>
            <Value>15</Value>
            <Percental>1</Percental>
          </ProductivityUpgrade>
        </FactoryUpgrade>
        <Buff>
          <ShouldBeShownInForeignObjectMenu>1</ShouldBeShownInForeignObjectMenu>
        </Buff>
        <ItemEffect>
          <EffectTargets>
            <Item>
              <GUID>6000018</GUID>
            </Item>
          </EffectTargets>
        </ItemEffect>
      </Values>
    </Asset>
    
  </ModOp>
  
  
  <!-- ############################## -->
  <!-- Triggers -->
  
  <!-- Initial first Trigger to check if Human (1500001600) or AI (1500001601) -->
  <ModOp Type="AddNextSibling" GUID="130248">
    <!-- most likely we can not put the human/AI check into the same Condition like ConditionMutualAreaInSubconditions (ConditionMutualAreaInSubconditions must be main condition) -->
     <!-- so we put this extra trigger in front of it to check it first -->
    <Asset>
      <Template>Trigger</Template>
      <Values>
        <Standard>
          <GUID>1500004676</GUID>
          <Name>Check Human or AI</Name>
        </Standard>
        <Trigger>
          <!-- small initial delay to make sure game is loaded -->
          <TriggerCondition>
            <Template>ConditionTimer</Template>
            <Values>
              <Condition>
                <SubConditionCompletionOrder>MutuallyExclusive</SubConditionCompletionOrder>
              </Condition>
              <ConditionTimer>
                <TimeLimit>1000</TimeLimit>
              </ConditionTimer>
            </Values>
          </TriggerCondition>
          <SubTriggers>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionUnlocked</Template>
                      <Values>
                        <Condition />
                        <ConditionUnlocked>
                          <UnlockNeeded>1500001600</UnlockNeeded>
                        </ConditionUnlocked>
                        <ConditionPropsNegatable />
                      </Values>
                    </TriggerCondition>
                    <TriggerActions>
                      <Item>
                        <TriggerAction>
                          <Template>ActionRegisterTrigger</Template>
                          <Values>
                            <Action />
                            <ActionRegisterTrigger>
                              <TriggerAsset>1500004677</TriggerAsset>
                            </ActionRegisterTrigger>
                          </Values>
                        </TriggerAction>
                      </Item>
                    </TriggerActions>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionUnlocked</Template>
                      <Values>
                        <Condition />
                        <ConditionUnlocked>
                          <UnlockNeeded>1500001601</UnlockNeeded>
                        </ConditionUnlocked>
                        <ConditionPropsNegatable />
                      </Values>
                    </TriggerCondition>
                    <TriggerActions>
                      <Item>
                        <TriggerAction>
                          <Template>ActionRegisterTrigger</Template>
                          <Values>
                            <Action />
                            <ActionRegisterTrigger>
                              <TriggerAsset>1500004678</TriggerAsset>
                            </ActionRegisterTrigger>
                          </Values>
                        </TriggerAction>
                      </Item>
                      <Item>
                        <TriggerAction>
                          <Template>ActionRegisterTrigger</Template>
                          <Values>
                            <Action />
                            <ActionRegisterTrigger>
                              <TriggerAsset>1500004679</TriggerAsset>
                            </ActionRegisterTrigger>
                          </Values>
                        </TriggerAction>
                      </Item>
                      <Item>
                        <TriggerAction>
                          <Template>ActionRegisterTrigger</Template>
                          <Values>
                            <Action />
                            <ActionRegisterTrigger>
                              <TriggerAsset>1500004680</TriggerAsset>
                            </ActionRegisterTrigger>
                          </Values>
                        </TriggerAction>
                      </Item>
                    </TriggerActions>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
          </SubTriggers>
        </Trigger>
        <TriggerSetup>
          <AutoRegisterTrigger>1</AutoRegisterTrigger>
          <UsedBySecondParties>1</UsedBySecondParties>
        </TriggerSetup>
      </Values>
    </Asset>
    
  </ModOp>
  
  <!-- Trigger Human -->
  <!-- initial registering Trigger 1500004676 is in assets.xml -->
  
  <ModOp Type="AddNextSibling" GUID="130248">
    <!-- Buff Display Building -->
    <Asset>
      <Template>Trigger</Template>
      <Values>
        <Standard>
          <GUID>1500004677</GUID>
          <Name>Human check buildings and start spawn</Name>
        </Standard>
        <Trigger>
          <TriggerCondition>
            <Template>ConditionMutualAreaInSubconditions</Template>
            <Values>
              <Condition />
              <ConditionMutualAreaInSubconditions />
            </Values>
          </TriggerCondition>
          <SubTriggers>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>700000</Context>
                          <CounterAmount>1</CounterAmount>
                          <ComparisonOp>AtLeast</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>1500004685</Context>
                          <CounterAmount>0</CounterAmount>
                          <ComparisonOp>AtMost</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
          </SubTriggers>
          <TriggerActions> 
            <Item>
              <TriggerAction>
                <Template>ActionStartQuest</Template>
                <Values>
                  <Action />
                  <ActionStartQuest>
                    <Quest>1500004681</Quest>
                    <InheritQuestArea>1</InheritQuestArea>
                    <InheritQuestSession>1</InheritQuestSession>
                  </ActionStartQuest>
                </Values>
              </TriggerAction>
            </Item>
          </TriggerActions>
          <ResetTrigger>
            <Template>AutoCreateTrigger</Template>
            <Values>
              <Trigger>
                <TriggerCondition>
                  <Template>ConditionTimer</Template>
                  <Values>
                    <Condition />
                    <ConditionTimer>
                      <TimeLimit>200</TimeLimit>
                    </ConditionTimer>
                  </Values>
                </TriggerCondition>
              </Trigger>
            </Values>
          </ResetTrigger>
        </Trigger>
        <TriggerSetup>
          <AutoRegisterTrigger>0</AutoRegisterTrigger>
          <UsedBySecondParties>0</UsedBySecondParties>
        </TriggerSetup>
      </Values>
    </Asset>
  </ModOp>
  
  <!-- only within Quests LimitToQuestArea works -->
  <ModOp Type="AddNextSibling" GUID="152264">
    <Asset>
      <Template>A7_QuestDummyQuest</Template>
      <Values>
        <Standard>
          <GUID>1500004681</GUID>
          <Name>Spawn Display Building at Kontor</Name>
        </Standard>
        <Quest>
          <OnQuestStart>
            <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
            <Values>
              <ActionList>
                <Actions>
                  <Item>
                    <Action>
                      <Template>ActionSpawnObjects</Template>
                      <Values>
                        <Action />
                        <ActionSpawnObjects>
                          <SpawnGUID>1500004685</SpawnGUID>
                          <Amount>1</Amount>
                          <OwnerIsProcessingParticipant>1</OwnerIsProcessingParticipant>
                        </ActionSpawnObjects>
                        <SpawnArea>
                          <SpawnContext>ForceContextPosition</SpawnContext>
                          <MatcherGUID>1500004687</MatcherGUID>
                          <LimitToQuestArea>1</LimitToQuestArea>
                        </SpawnArea>
                        <SessionFilter>
                          <AllowProcessingSession>0</AllowProcessingSession>
                          <AllowParentConditionSession>0</AllowParentConditionSession>
                          <AllowQuestSession>1</AllowQuestSession>
                          <AllowQuestArea>1</AllowQuestArea>
                        </SessionFilter>
                      </Values>
                    </Action>
                  </Item>
                </Actions>
              </ActionList>
            </Values>
          </OnQuestStart>
        </Quest>
      </Values>
    </Asset>
  </ModOp>
  
  <!-- ############# -->
  <!-- AI Triggers -->
  
  <ModOp Type="AddNextSibling" GUID="130248">
   
    <!-- AI can not use Quests and therefore can not use LimitToQuestArea. So we need a kind of Bruteforce to spawn the buildings once for each of their islands -->
    <!-- we will spawn a unique helper building first. then check if this was by chance spawned at correct island -->
     <!-- if it is, fine then we will spawn at this unique location the final building. -->
     <!-- if it is not (so at this island already is a final building), remove the helper building and try spawn randomly again, until we got the correct island -->
     
     <!-- CheckQuestArea (in ActionDeleteObjects) does not work in Trigger, but AllowQuestSession+AllowQuestArea does work in a way that the Session is correctly chosen for spawning, which is also important -->
     
     <!-- eine ActionRegister-Schleife mit den drei Triggern 78,79 und 80 zu erstellen hat irgednwie nicht funktioniert, -->
      <!-- die trigger wurden nach erstem loop einfach nicht erneut registered.. oder klappt ActionRegisterTrigger nur einmal pro Trigger?! -->
      <!-- Deswegen jetzt nur einmal registeren und danach ResetTrigger, das funktioniert. -->
        
    <Asset>
      <Template>Trigger</Template>
      <Values>
        <Standard>
          <GUID>1500004678</GUID>
          <Name>AI check buildings and spawn helper</Name>
        </Standard>
        <Trigger>
          <TriggerCondition>
            <Template>ConditionMutualAreaInSubconditions</Template>
            <Values>
              <Condition />
              <ConditionMutualAreaInSubconditions />
            </Values>
          </TriggerCondition>
          <SubTriggers>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>700000</Context>
                          <CounterAmount>1</CounterAmount>
                          <ComparisonOp>AtLeast</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>1500004685</Context>
                          <CounterAmount>0</CounterAmount>
                          <ComparisonOp>AtMost</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>1500004684</Context>
                          <CounterAmount>0</CounterAmount>
                          <ComparisonOp>AtMost</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
          </SubTriggers>
          <TriggerActions> 
            <Item>
              <TriggerAction>
                <Template>ActionSpawnObjects</Template>
                <Values>
                  <Action />
                  <ActionSpawnObjects>
                    <SpawnGUID>1500004684</SpawnGUID>
                    <Amount>1</Amount>
                    <OwnerIsProcessingParticipant>1</OwnerIsProcessingParticipant>
                  </ActionSpawnObjects>
                  <SpawnArea>
                    <SpawnContext>ForceContextPosition</SpawnContext>
                    <MatcherGUID>1500004687</MatcherGUID>
                    <LimitToQuestArea>1</LimitToQuestArea>
                  </SpawnArea>
                  <SessionFilter>
                    <AllowProcessingSession>0</AllowProcessingSession>
                    <AllowParentConditionSession>0</AllowParentConditionSession>
                    <AllowQuestSession>1</AllowQuestSession>
                    <AllowQuestArea>1</AllowQuestArea>
                  </SessionFilter>
                </Values>
              </TriggerAction>
            </Item>
          </TriggerActions>
          <ResetTrigger>
            <Template>AutoCreateTrigger</Template>
            <Values>
              <Trigger>
                <TriggerCondition>
                  <Template>ConditionTimer</Template>
                  <Values>
                    <Condition />
                    <ConditionTimer>
                      <TimeLimit>200</TimeLimit>
                    </ConditionTimer>
                  </Values>
                </TriggerCondition>
              </Trigger>
            </Values>
          </ResetTrigger>
        </Trigger>
        <TriggerSetup>
          <AutoRegisterTrigger>0</AutoRegisterTrigger>
          <UsedBySecondParties>1</UsedBySecondParties>
        </TriggerSetup>
      </Values>
    </Asset>
    
    <Asset>
      <Template>Trigger</Template>
      <Values>
        <Standard>
          <GUID>1500004679</GUID>
          <Name>AI check spawn: failed and repeat</Name>
        </Standard>
        <Trigger>
          <TriggerCondition>
            <Template>ConditionMutualAreaInSubconditions</Template>
            <Values>
              <Condition />
              <ConditionMutualAreaInSubconditions />
            </Values>
          </TriggerCondition>
          <SubTriggers>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>700000</Context>
                          <CounterAmount>1</CounterAmount>
                          <ComparisonOp>AtLeast</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>1500004684</Context>
                          <CounterAmount>1</CounterAmount>
                          <ComparisonOp>AtLeast</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>1500004685</Context>
                          <CounterAmount>1</CounterAmount>
                          <ComparisonOp>AtLeast</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
          </SubTriggers>
          <TriggerActions>
            <Item>
              <TriggerAction>
                <Template>ActionDeleteObjects</Template>
                <Values>
                  <Action />
                  <ActionDeleteObjects />
                  <ObjectFilter>
                    <ObjectGUID>1500004684</ObjectGUID>
                    <CheckParticipantID>1</CheckParticipantID>
                    <CheckProcessingParticipantID>1</CheckProcessingParticipantID>
                  </ObjectFilter>
                </Values>
              </TriggerAction>
            </Item>
          </TriggerActions>
          <ResetTrigger>
            <Template>AutoCreateTrigger</Template>
            <Values>
              <Trigger>
                <TriggerCondition>
                  <Template>ConditionTimer</Template>
                  <Values>
                    <Condition />
                    <ConditionTimer>
                      <TimeLimit>200</TimeLimit>
                    </ConditionTimer>
                  </Values>
                </TriggerCondition>
              </Trigger>
            </Values>
          </ResetTrigger>
        </Trigger>
        <TriggerSetup>
          <AutoRegisterTrigger>0</AutoRegisterTrigger>
          <UsedBySecondParties>1</UsedBySecondParties>
        </TriggerSetup>
      </Values>
    </Asset>
    
    <Asset>
      <Template>Trigger</Template>
      <Values>
        <Standard>
          <GUID>1500004680</GUID>
          <Name>AI check spawn: success</Name>
        </Standard>
        <Trigger>
          <TriggerCondition>
            <Template>ConditionMutualAreaInSubconditions</Template>
            <Values>
              <Condition />
              <ConditionMutualAreaInSubconditions />
            </Values>
          </TriggerCondition>
          <SubTriggers>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>700000</Context>
                          <CounterAmount>1</CounterAmount>
                          <ComparisonOp>AtLeast</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>1500004685</Context>
                          <CounterAmount>0</CounterAmount>
                          <ComparisonOp>AtMost</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionPlayerCounter</Template>
                      <Values>
                        <Condition />
                        <ConditionPlayerCounter>
                          <Context>1500004684</Context>
                          <CounterAmount>1</CounterAmount>
                          <ComparisonOp>AtLeast</ComparisonOp>
                          <CounterScope>Area</CounterScope>
                          <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                        </ConditionPlayerCounter>
                      </Values>
                    </TriggerCondition>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
          </SubTriggers>
          <TriggerActions> 
            <!-- spawn the final object at the helpers position -->
            <Item>
              <TriggerAction>
                <Template>ActionSpawnObjects</Template>
                <Values>
                  <Action />
                  <ActionSpawnObjects>
                    <SpawnGUID>1500004685</SpawnGUID>
                    <Amount>1</Amount>
                    <OwnerIsProcessingParticipant>1</OwnerIsProcessingParticipant>
                  </ActionSpawnObjects>
                  <SpawnArea>
                    <SpawnContext>ForceContextPosition</SpawnContext>
                    <MatcherGUID>1500004688</MatcherGUID>
                    <LimitToQuestArea>1</LimitToQuestArea>
                  </SpawnArea>
                  <SessionFilter>
                    <AllowProcessingSession>0</AllowProcessingSession>
                    <AllowParentConditionSession>0</AllowParentConditionSession>
                    <AllowQuestSession>1</AllowQuestSession>
                    <AllowQuestArea>1</AllowQuestArea>
                  </SessionFilter>
                </Values>
              </TriggerAction>
            </Item>
            <!-- delete the helper -->
            <Item>
              <TriggerAction>
                <Template>ActionDeleteObjects</Template>
                <Values>
                  <Action />
                  <ActionDeleteObjects />
                  <ObjectFilter>
                    <ObjectGUID>1500004684</ObjectGUID>
                    <CheckParticipantID>1</CheckParticipantID>
                    <CheckProcessingParticipantID>1</CheckProcessingParticipantID>
                  </ObjectFilter>
                </Values>
              </TriggerAction>
            </Item>
          </TriggerActions>
          <ResetTrigger>
            <Template>AutoCreateTrigger</Template>
            <Values>
              <Trigger>
                <TriggerCondition>
                  <Template>ConditionTimer</Template>
                  <Values>
                    <Condition />
                    <ConditionTimer>
                      <TimeLimit>200</TimeLimit>
                    </ConditionTimer>
                  </Values>
                </TriggerCondition>
              </Trigger>
            </Values>
          </ResetTrigger>
        </Trigger>
        <TriggerSetup>
          <AutoRegisterTrigger>0</AutoRegisterTrigger>
          <UsedBySecondParties>1</UsedBySecondParties>
        </TriggerSetup>
      </Values>
    </Asset>
  </ModOp>
  

  ```
  </details>


###  Add product to Tooltip Arctic Flue Chance
- Adding mod-heat-providing product to the "Arctic Flue Chance" Tooltip (see also [here](https://github.com/anno-mods/modding-guide/blob/main/documentation/infotips.md) for modding info about tooltips). Unfortunately I see no way to make the game automatically fetch this.. but adding sth to a list is most of the time fully compatible to other mods also adding to the list, so I think its ok to add mod products to this list.  
   Using the same list-entry structure like vanilla, although I wonder why they use as diplay-condition "if the product is not locked" instead of "if the product is unlocked" :D
- Put the following code in your mod into data/infotips/export.bin.xml and replace "YOUR_GUID" with your GUID of the product that provides heat. The code will add your product in the list below the vanilla heat provider "114890" (Cantine)
  <details>
  <summary>(CLICK) CODE</summary>  
  
  ```xml
  <ModOps>
  
  <!-- Adding mod-heat-providing product to the "Arctic Flue Chance" Tooltip. Unfortunately I see no way to make the game automatically fetch this.. but adding sth to a list is most of the time fully compatible to other mods also adding to the list, so I think its ok to add mod products to this list. -->
   <!-- Using the same list-entry structure like vanilla, although I wonder why they use as diplay-condition "if the product is not locked" instead of "if the product is unlocked" :D -->
  <!-- Replace "YOUR_GUID" with your GUID of the product that provides heat. The code will add your product in the list below the vanilla heat provider "114890" (Cantine) -->
   <ModOp Type="AddNextSibling" Path="//InfoTipData[Guid='116020']/InfoElement[Value/Text='[Selection Object Residence CurrentHeatForGood(114890) &gt;&gt; happiness]']">
    <InfoElement>
      <ElementType>4</ElementType>
      <VisibilityElement>
        <ElementType>
          <ElementType>2</ElementType>
        </ElementType>
        <ChildCount>1</ChildCount>
        <VisibilityElement>
          <ElementType>
            <ElementType>1</ElementType>
          </ElementType>
          <CompareOperator />
          <ResultType />
          <ExpectedValueBool>False</ExpectedValueBool>
          <Condition>[Selection Object Area Economy NeedLocked([Selection Object Residence PopulationLevel Guid], YOUR_GUID)]</Condition>
        </VisibilityElement>
        <OperatorType />
      </VisibilityElement>
      <Icon>
        <IconGUID>YOUR_GUID</IconGUID>
        <Style />
      </Icon>
      <Text>
        <TextGUID>YOUR_GUID</TextGUID>
        <Style />
      </Text>
      <Value>
        <Text>[Selection Object Residence CurrentHeatForGood(YOUR_GUID) &gt;&gt; happiness]</Text>
        <Style />
      </Value>
      <WarningType />
      <BackgroundType />
    </InfoElement>
    
    
  </ModOp>
    
    
  </ModOps>  

  ```
  </details>
