# xml ModOp code snippets for various purposes

- [ActionExecuteActionByChance with fixed chance](#actionexecuteactionbychance-with-fixed-chance)
- [Delete all kontors from an AI (and therefore removing it from the game)](#delete-all-kontors-from-an-ai-and-therefore-removing-it-from-the-game)
- [Add text to existing strings (from vanilla or other mods)](#add-text-to-existing-strings-from-vanilla-or-other-mods)
- [Limit a building to "once per Island" without UniqueType property](#limit-a-building-to-once-per-island-without-uniquetype-property)

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
