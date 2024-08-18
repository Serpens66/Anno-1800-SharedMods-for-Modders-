


-- if SearchModLog_Pnski==nil then
  console.startScript("data/scripts/search_modlog_pnski.lua")
-- end


local incompatible_string = ""
-- in mod-loader.log eg. "[2024-08-15 22:35:39.877] [error] [Gameplay] testmod is incompatible with: shared_IncompatibleModsPopUp"
-- mod1 is a ModName, while mod2 is a ModID
local inc_mods_list = listIncompatible_Pnski()
local inc_mods_count = #inc_mods_list
for _,modpair in pairs(inc_mods_list) do
  if inc_mods_count<=8 then -- we can only display roughly 33 rows in the popoup (~40 in total, but we already use some lines)
    incompatible_string = incompatible_string..modpair[1].."\n!/!\n"..modpair[2].."\n\n"
  elseif inc_mods_count<=15 then
    incompatible_string = incompatible_string..modpair[1].."  !/!  "..modpair[2].."\n\n"
  else
    incompatible_string = incompatible_string.."- "..modpair[1].."  !/!  "..modpair[2].."\n"
  end
end

-- invalid signs/zeichen in strings (to save it into nameable): " \ , [ ] and () if both used. and better do not use - because it might hurt gsub?
local function replace_chars(str) -- string should not contain these characters
  str = str:gsub("%[", "*")
  str = str:gsub("%]", "*")
  str = str:gsub("%,", "*")
  str = str:gsub("%(", "*")
  str = str:gsub("%)", "*") -- as soon as this bracket closes, the rest is not shown anymore for whatever reason
  str = str:gsub("%\\", "*")
  str = str:gsub("%\"", "*")
  return str
end

-- print(incompatible_string)
incompatible_string = replace_chars(incompatible_string)
-- print(incompatible_string)

if incompatible_string ~="" then
  -- abuse the CompanyName of the Neutral Participant which exists in every session, to bring our text to an ingame object to display it as text (best workaround I found to display the text we found in lua :D )
  -- the name is reverted back to "Neutral" in the PopUp Commands
  ts.Participants.GetParticipant(8).Profile.SetCompanyName(incompatible_string)
  ts.Conditions.RegisterTriggerForCurrentParticipant(1500005500)
end
