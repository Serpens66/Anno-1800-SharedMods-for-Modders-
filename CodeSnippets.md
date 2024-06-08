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
  <ModOp Type="add" Path="/TextExport/Texts/Text[GUID = '10595']/Text"> (0%)</ModOp>

  <!-- You can also make use of "Content" to copy the text from another GUID if you want. and you can use a "contain" check to make sure sth is not already part of a string -->
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
  <!-- With this code it only properly works to limit it to 1 per island (not multiple ones) unfortunately. -->
  <!-- And I tried to adjust the tooltips, to not display "missing buildmaterials" but instead "Limited to once per island", but this failed, because there are SO many locations one have to edit it, and the tooltips itself are buggy .. if you are interested in my attempt, contact me and ask for my "shared_BuildCountPerIsland" code... -->
  
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
    <!-- For AI: starting a savegame with already settled islands does not count for IslandSettled, so we have to add the buff once after the mod was newly added to enable the buff first time (add your custom condition of course via SubTrigger, if you dont want the buff to be active from the start) -->
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
          <TriggerActions>
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
- improved code from previous shared_AreaBuffsHelper, this share mod was removed, because its better as Code Snippet  
- enable/disable Island specifc and islandwide Buffs based on ConditionPlayerCounter-Area-Scope Conditions
- It works by spawning invisible BuffFactories on the island you want which buff all targets on the island. 
- You can spawn/delete them as you please, eg. spawn a debuff as soon as someone reached an amount GoodsInStock and remove again when it goes below.
- the code for Human players requires my shared mods: shared_Matchers (v1.0 and higher) and shared_ObjectDummies (1.08 and higher)
- for AI the code is much more complicated (for now this is only code to ADD one buffbuilding to every AI island, not to remove it again), since AIs can not use Quests, which we need to be able to use "LimitToQuestArea". CheckQuestArea is needed for removing the buff buildings again in ActionDeleteObjects. But this also does not work in Triggers (only Quests). so we need another complex workaround to delete the buff building at the correct island again and since its unlikely one wants this for AI anyways, I did not think about how this could be done. If you have a nice worakaround, let me know and I will add it.

  <details>
  <summary>(CLICK) CODE for HUMAN players</summary>  
  
  ```xml
  <!-- Used shared mods from https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders- : -->
  <!-- - shared_Matchers (v1.0 and newer): GUID 1500004905, a matcher to spawn sth. at a DistributionCenter (Kontor) building from the processing player -->
  <!-- - shared_ObjectDummies (v1.08 and newer): for the templates "BuffFactoryDummy_WithOwner" and "A7_QuestDummyQuest" -->
  
  
  <!-- Carefully check your conditions! Add for testing an action like  -->
  <!-- <Item> -->
    <!-- <Action> -->
      <!-- <Template>ActionAddResource</Template> -->
      <!-- <Values> -->
        <!-- <Action /> -->
        <!-- <ActionAddResource> -->
          <!-- <Resource>1010017</Resource> -->
          <!-- <ResourceAmount>100000</ResourceAmount> -->
        <!-- </ActionAddResource> -->
      <!-- </Values> -->
    <!-- </Action> -->
  <!-- </Item> -->
  <!-- to your helper Quests, to make sure your conditions are not endlessly triggered, but only when you want them to trigger! -->
  
  
    <ModOp Type="AddNextSibling" GUID='132370'>
  
      <!-- Hint: add -->
        <!-- <Building> -->
          <!-- <OwnerChangeTarget>2001000003</OwnerChangeTarget> -->
        <!-- </Building> -->
       <!-- to your BuffFactory IF you want that buff to be bound PERMANENTLY to this island (without it, the BuffFactory is removed on owner change of the island) -->
      
      <Asset>
        <Template>BuffFactoryDummy_WithOwner</Template>
        <Values>
          <Standard>
            <GUID>2001000003</GUID>
            <Name>Example Invisible BuffFactory</Name>
          </Standard>
          <BuffFactory>
            <BaseBuff>2001000004</BaseBuff>
            <BaseBuffScope>Area</BaseBuffScope>
          </BuffFactory>
          <LogisticNode />
          <Pausable />
        </Values>
      </Asset>    
    </ModOp>
  
    <!-- just an example buff for testing, that gives +15% productivity to all production buildings, you can use whatever buff you want of course -->
     <!-- ShouldBeShownInForeignObjectMenu was set so I could test if it works with AI, you dont need it in your buffs (Quests wont work with AI, so different code is needed for them) -->
    <ModOp Type="AddNextSibling" GUID='190093'>
      <Asset>
        <Template>GuildhouseBuff</Template>
        <Values>
          <Standard>
            <GUID>2001000004</GUID>
            <Name>Example Buff Island</Name>
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
  
  
  
    <!-- Add your Helper Quests to this pool, can be as many as you want -->
    <!--  (since Quests will be instantly solved, so the next PreCondition can be checked nearly all the time, but make sure that the conditions are properly written, to not firely endlessly!) -->
    <!--  You may add a PreConditionList to this pool, if you want all Helper Quest from it to only be checked if that condition is fullfilled. For more detailed conditions, use PreConditionList from the Quests instead -->
    <!-- (Instead of a QuestPool, one can also start the Helper Quest within a Trigger, but I think a QuestPool is more straightforward) -->
    <ModOp Type="addNextSibling" GUID="150725">
      <Asset>
        <Template>QuestPool</Template>
        <Values>
          <Standard>
            <GUID>2001000000</GUID>
            <Name>AlwaysTrue-Pool</Name>
          </Standard>
          <QuestPool>
            <Quests>
              <Item>
                <Quest>2001000001</Quest>
              </Item>
              <Item>
                <Quest>2001000002</Quest>
              </Item>
            </Quests>
            <PoolCooldown>0</PoolCooldown>
            <QuestCooldown>0</QuestCooldown>
            <CooldownOnQuestStart>1</CooldownOnQuestStart>
            <CooldownOnQuestEnd>1</CooldownOnQuestEnd>
            <AffectedByCooldownFactor>0</AffectedByCooldownFactor>
            <IsMainStoryPool>0</IsMainStoryPool>
            <IsTopLevel>1</IsTopLevel>
            <QuestLimit>1</QuestLimit>
          </QuestPool>
          <Locked>
            <DefaultLockedState>0</DefaultLockedState>
          </Locked>
        </Values>
      </Asset>
    </ModOp>
    
    <!-- only within Quests "LimitToQuestArea" works -->
    <!-- its best to use AddNextSibling with GUID 152264 here, because vanilla uses Groups for Quests (and Items), so it matters where you add your assets. 152264 should be in no vanilla group so save to use I would say (otherwise you might accidently add this Quest to an AI Questpool or so) (for items its save to add your items next to GUID 112574) -->
    <ModOp Type="AddNextSibling" GUID="152264">
      <Asset>
        <Template>A7_QuestDummyQuest</Template>
        <Values>
          <Standard>
            <GUID>2001000001</GUID>
            <Name>Spawn invisible Buff Building at Kontor, when having at least 40 Timber in stock at an island</Name>
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
                            <SpawnGUID>2001000003</SpawnGUID>
                            <Amount>1</Amount>
                            <OwnerIsProcessingParticipant>1</OwnerIsProcessingParticipant>
                          </ActionSpawnObjects>
                          <SpawnArea>
                            <SpawnContext>ForceContextPosition</SpawnContext>
                            <MatcherGUID>1500004905</MatcherGUID>
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
          <PreConditionList>
            <Condition>
              <Template>ConditionMutualAreaInSubconditions</Template>
              <Values>
                <Condition />
                <ConditionMutualAreaInSubconditions />
              </Values>
            </Condition>
            <SubConditions>
              <!-- first making sure the island does not have our bufffactory already -->
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
                            <Context>2001000003</Context>
                            <CounterAmount>0</CounterAmount>
                            <ComparisonOp>AtMost</ComparisonOp>
                            <CounterScope>Area</CounterScope>
                            <CounterScopeUseCurrentContext>0</CounterScopeUseCurrentContext>
                          </ConditionPlayerCounter>
                        </Values>
                      </Condition>
                    </PreConditionList>
                  </Values>
                </SubCondition>
              </Item>
              <!-- then checking for any ConditionPlayerCounter you want to check for the island, in this example if having at least 40t of Timber in stock -->
               <!-- you can add more SubCondition, all of them must be true at the same time -->
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
                            <Context>1010196</Context>
                            <ComparisonOp>AtLeast</ComparisonOp>
                            <CounterAmount>40</CounterAmount>
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
      
      <!-- And now the code to remove the BuffFactory again, if having less than 40 timber and island has a BuffFactory, basically the opposite conditions from the spawn Quest. -->
      <Asset>
        <Template>A7_QuestDummyQuest</Template>
        <Values>
          <Standard>
            <GUID>2001000002</GUID>
            <Name>Delete invisible Buff Building at Kontor, when having less than 40 timber in stock</Name>
          </Standard>
          <Quest>
            <OnQuestStart>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <ActionList>
                  <Actions>
                    <Item>
                      <Action>
                        <Template>ActionDeleteObjects</Template>
                        <Values>
                          <Action />
                          <ActionDeleteObjects />
                          <ObjectFilter>
                            <ObjectGUID>2001000003</ObjectGUID>
                            <CheckParticipantID>1</CheckParticipantID>
                            <CheckProcessingParticipantID>1</CheckProcessingParticipantID>
                            <CheckQuestArea>1</CheckQuestArea>
                          </ObjectFilter>
                        </Values>
                      </Action>
                    </Item>
                  </Actions>
                </ActionList>
              </Values>
            </OnQuestStart>
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
                            <Context>2001000003</Context>
                            <CounterAmount>1</CounterAmount>
                            <ComparisonOp>AtLeast</ComparisonOp>
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
                            <Context>1010196</Context>
                            <ComparisonOp>LessThan</ComparisonOp>
                            <CounterAmount>40</CounterAmount>
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
  
  ```
  </details>
  <details>
  <summary>(CLICK) CODE for AI players (only adding, not removing!)</summary>  
  
  ```xml
  
    <!-- # Add the Example BuffFactory 2001000003 and Example Buff 2001000004 from the top of the code for Humans -->
    
    <!-- Used shared mods from https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders- : -->
    <!-- - shared_Matchers (v1.0 and newer): GUID 1500004905, a matcher to spawn sth. at a DistributionCenter (Kontor) building from the processing player -->
    <!-- - shared_ObjectDummies (v1.08 and newer): for the templates "BuffFactoryDummy_WithOwner", "BuildingDummy_WithOwner" and "A7_QuestDummyQuest" -->
    <!-- - shared_IsAIPlayer_Condition (v1.01 and newer): for GUID 1500001601 to check if the processing player is AI -->
    
    
    <!-- AI can not use Quests and therefore can not use LimitToQuestArea (still added it in belows code, but its not functional). So we need a kind of Bruteforce to spawn the buildings once for each of their islands -->
      <!-- we will spawn a unique helper building first. then check if this was by chance spawned at correct island -->
       <!-- if it is, fine then we will spawn at this unique location the final building. -->
       <!-- if it is not (so at this island already is a final building), remove the helper building and try spawn randomly again, until we got the correct island -->
       
       <!-- CheckQuestArea (in ActionDeleteObjects) does not work in Trigger, but AllowQuestSession+AllowQuestArea does work in a way that the Session is correctly chosen for spawning, which is also important -->
     
     
     <!-- ################################# -->
     
     <!-- IMPORTANT: -->
      <!-- CheckQuestArea is needed for removing the buff buildings again in ActionDeleteObjects. But this also does not work in Triggers (only Quests) -->
       <!-- so we need another complex workaround to delete the buff building at the correct island again... -->
      <!-- Since its unlikely one wants this for AI anyways, I did not think about how this could be done. -->
       <!-- If you have a nice solution, let me know and I will add it. -->
      
      <!-- So for now this is only code to ADD one buffbuilding to every AI island, not to remove it again. -->
      
      <!-- ################################# -->
    
    

    
    
    <ModOp Type="AddNextSibling" GUID='132370'>

      <!-- Spawn Helper only required for spawning on AI islands -->
      <Asset>
        <Template>BuildingDummy_WithOwner</Template>
        <Values>
          <Standard>
            <GUID>2001000005</GUID>
            <Name>BuffBuilding - Spawn Helper</Name>
          </Standard>
        </Values>
      </Asset>  
      
    </ModOp>
    
    <ModOp Type="addNextSibling" GUID="153189">
      <Asset>
        <Template>Matcher</Template>
        <Values>
          <Standard>
            <GUID>2001000009</GUID>
            <Name>Matcher to spawn at Spawn-Helper position</Name>
          </Standard>
          <Matcher>
            <Criterion>
              <IsBaseAutoCreateAsset>1</IsBaseAutoCreateAsset>
              <Values>
                <MatcherCriterion />
                <MatcherCriterionAnd>
                  <CriterionOperandListAnd>
                    <Item>
                      <CriterionOperand>
                        <Template>MatcherCriterionOwner</Template>
                        <Values>
                          <MatcherCriterion />
                          <MatcherCriterionOwner>
                            <UseProcessingParticipant>1</UseProcessingParticipant>
                          </MatcherCriterionOwner>
                        </Values>
                      </CriterionOperand>
                    </Item>
                    <Item>
                      <CriterionOperand>
                        <Template>MatcherCriterionGUID</Template>
                        <Values>
                          <MatcherCriterion />
                          <MatcherCriterionGUID>
                            <ObjectMatched>2001000005</ObjectMatched>
                          </MatcherCriterionGUID>
                        </Values>
                      </CriterionOperand>
                    </Item>
                  </CriterionOperandListAnd>
                </MatcherCriterionAnd>
              </Values>
            </Criterion>
          </Matcher>
        </Values>
      </Asset>
    
    </ModOp>
    

    <!-- ############# -->
    <!-- AI Triggers -->
    
    <ModOp Type="AddNextSibling" GUID="130248">
     
       <!-- eine ActionRegister-Schleife mit den drei Triggern Spawn-fail-success zu erstellen hat irgendwie nicht funktioniert, -->
        <!-- die trigger wurden nach erstem loop einfach nicht erneut registered..  -->
        <!-- Deswegen jetzt so, nur einmal registeren und danach ResetTrigger, das funktioniert. -->
      
      <!-- ########## -->
          
      <!-- Initial first Trigger to check if Human (1500001600) or AI (1500001601) -->
      <!-- most likely we can not put the AI check into the same Trigger like ConditionMutualAreaInSubconditions (ConditionMutualAreaInSubconditions must be main condition) -->
       <!-- so we put this extra trigger in front of it to check it first and only then register the other triggers -->
      <Asset>
        <Template>Trigger</Template>
        <Values>
          <Standard>
            <GUID>1500004676</GUID>
            <Name>Check if AI</Name>
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
            <TriggerActions>
              <Item>
                <TriggerAction>
                  <Template>ActionRegisterTrigger</Template>
                  <Values>
                    <Action />
                    <ActionRegisterTrigger>
                      <TriggerAsset>2001000006</TriggerAsset>
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
                      <TriggerAsset>2001000007</TriggerAsset>
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
                      <TriggerAsset>2001000008</TriggerAsset>
                    </ActionRegisterTrigger>
                  </Values>
                </TriggerAction>
              </Item>
            </TriggerActions>
          </Trigger>
          <TriggerSetup>
            <AutoRegisterTrigger>1</AutoRegisterTrigger>
            <UsedBySecondParties>1</UsedBySecondParties>
          </TriggerSetup>
        </Values>
      </Asset>
          
      <Asset>
        <Template>Trigger</Template>
        <Values>
          <Standard>
            <GUID>2001000006</GUID>
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
                            <Context>2001000003</Context>
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
                            <Context>2001000005</Context>
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
                      <SpawnGUID>2001000005</SpawnGUID>
                      <Amount>1</Amount>
                      <OwnerIsProcessingParticipant>1</OwnerIsProcessingParticipant>
                    </ActionSpawnObjects>
                    <SpawnArea>
                      <SpawnContext>ForceContextPosition</SpawnContext>
                      <MatcherGUID>1500004905</MatcherGUID>
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
            <GUID>2001000007</GUID>
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
                            <Context>2001000005</Context>
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
                            <Context>2001000003</Context>
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
                      <ObjectGUID>2001000005</ObjectGUID>
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
            <GUID>2001000008</GUID>
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
                            <Context>2001000003</Context>
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
                            <Context>2001000005</Context>
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
              <!-- spawn the final object at the unique location of the Spawn-Helper -->
              <Item>
                <TriggerAction>
                  <Template>ActionSpawnObjects</Template>
                  <Values>
                    <Action />
                    <ActionSpawnObjects>
                      <SpawnGUID>2001000003</SpawnGUID>
                      <Amount>1</Amount>
                      <OwnerIsProcessingParticipant>1</OwnerIsProcessingParticipant>
                    </ActionSpawnObjects>
                    <SpawnArea>
                      <SpawnContext>ForceContextPosition</SpawnContext>
                      <MatcherGUID>2001000009</MatcherGUID>
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
                      <ObjectGUID>2001000005</ObjectGUID>
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
