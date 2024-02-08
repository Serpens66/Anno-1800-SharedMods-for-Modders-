# Anno-1800-SharedMods--for-Modders-
 Anno 1800 shared mods for modders, helpful utility-like mods

How to Download  
-
Click on the green "Code" button on the top right and hit "download zip" to download the complete collection. Of course you can delete the mods you don't want after download (I know no way to only download a single folder from github).

Usage  
-
All shared mods are intended to not be changed from other modders except the author/s. So you copy paste the desired shared mod into your mod folder, which will automatically enable the shared mod together with your mod. If you want to make iprovements to any shared mod, do a PR to this repository. If you want to change things/texts that are not suited for everyone, do this within your own mod instead, by loading your mod after my shared mod and then do ModOp changes like usual to it.

[Shared] WhichPlayer Condition
-
Condition to check if processing player is any AI or specific AI or specific Human.

If you only need the "Is any AI" Condition and not the advanced ones, you can also use the 
<br>**"IsAIPlayer Condition"**<br>
mod instead.

USAGE: 
  Put the whole mod folder into your mod (next to your data folder) and use the GUID from list below for the player you want to check and use this condition in your code:
  ```
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
  ```
  The GUIDs to use from this mod are:
  - 1500001600 - Is any Human
  - 1500001601 - Is any AI
  - 1500001602 - Second_ai_01_Jorgensen
  - 1500001603 - Second_ai_02_Qing
  - 1500001604 - Second_ai_03_Wibblesock
  - 1500001605 - Second_ai_04_Smith
  - 1500001606 - Second_ai_05_OMara
  - 1500001607 - Second_ai_06_Gasparov
  - 1500001608 - Second_ai_07_von_Malching
  - 1500001609 - Second_ai_08_Gravez
  - 1500001610 - Second_ai_09_Silva
  - 1500001611 - Second_ai_10_Hunt
  - 1500001612 - Second_ai_11_Mercier
  - 1500001613 - Human0
  - 1500001614 - Human1
  - 1500001615 - Human2
  - 1500001616 - Human3

With **WhichModPlayer** shared mod you can also use the following for Participants added by mods:
  - 1500001617 - Mod1
  - 1500001618 - Mod2
  - 1500001619 - Mod3
  - 1500001620 - Mod4
  - 1500001621 - Mod5 
  - 1500001622 - Mod6 
  - 1500001623 - Mod7 
  - 1500001624 - Mod8 
  - 1500001625 - Mod9 
  - 1500001626 - Mod10
  - 1500001627 - Mod11
  - 1500001628 - Mod12
  - 1500001629 - Mod13
  - 1500001630 - Mod14
  - 1500001631 - Mod15
  - 1500001632 - Mod16
  - 1500001633 - Mod17
  - 1500001634 - Mod18
  - 1500001635 - Mod19
  - 1500001636 - Mod20
  - Human4 to Human7 are unused by vanilla, so might be used by modders for AI players
  - 1500001637 - Human4
  - 1500001638 - Human5
  - 1500001639 - Human6
  - 1500001640 - Human7
