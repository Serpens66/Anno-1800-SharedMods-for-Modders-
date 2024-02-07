
  -- use the lua variable 
    -- if g_Im_CoopLeader_LuaCoopHelper == true then
  -- in your lua scripts to check if the executing player is the Coop-Leader, to only execute code once per coop-team.
  -- It will also be true for every human if it is a singleplayer game or a MP game without any Coop players (as soon this script was executed).
  -- Will be false for every non-leader
  -- if it is nil, the user did not yet click the PopUp and you should wait
  
  -- ##
  
  -- IMPORTANT:
  -- IF your code may run within ~10 seconds after the game/savegame was loaded, you may need the following code to wait for the player to click the PopUp.
  -- use this code (copy paste it into your script) to wait until g_Im_CoopLeader_LuaCoopHelper is defined, before using it on every script call!
  -- define/rename MyFunc() to your liking
  
  -- local function WaitFor_g_Im_CoopLeader_LuaCoopHelper() then
    -- local stop = 0
    -- while g_Im_CoopLeader_LuaCoopHelper==nil then
      -- system.waitForGameTimeDelta(100)
      -- stop = stop + 1
      -- if stop > 1000 then -- in case it never happens (waited 100 seconds), just break
        -- break
      -- end
    -- end
    -- MyFunc() -- only after the waiting, within this coroutine, call you function that uses g_Im_CoopLeader_LuaCoopHelper. Still check if variable is nil, in case of a problem
  -- end
  -- if g_Im_CoopLeader_LuaCoopHelper==nil then -- wait for it and call your MyFunc() within the coroutine on the first time
    -- system.start(WaitFor_g_Im_CoopLeader_LuaCoopHelper)
  -- else
    -- MyFunc()
  -- end

-- ################################################################################################
-- ################################################################################################

-- using ts.Online.GetUsername(peer int) to find out if coop slots are used (0 to 3 are normal slots, all others are coop slots. should be enough to check 4 to 7, because these will be for sure occupied if higher slots are occupied too)
-- is not occupied it returns an empty string
-- Checking GetUsername does not help to count the current number of active coop players, because they are also returned if the game is loaded without them!
local function IsCoopTeam_serp()
  local PID = ts.Participants.GetGetCurrentParticipantID()
  if PID == 0 then -- first coop team
    if ts.Online.GetUsername(4)~="" or ts.Online.GetUsername(8)~="" or ts.Online.GetUsername(12)~="" then
      return true
    end
  elseif PID == 1 then
    if ts.Online.GetUsername(5)~="" or ts.Online.GetUsername(9)~="" or ts.Online.GetUsername(13)~="" then
      return true
    end
  elseif PID == 2 then
    if ts.Online.GetUsername(6)~="" or ts.Online.GetUsername(10)~="" or ts.Online.GetUsername(14)~="" then
      return true
    end
  elseif PID == 3 then
    if ts.Online.GetUsername(7)~="" or ts.Online.GetUsername(11)~="" or ts.Online.GetUsername(15)~="" then
      return true
    end
  end
  return false
end


-- using shared_LuaOnGameLoaded to make sure PopUp only triggers once per loading a savegame, not once every SessionEnter:
-- enter your ModID here for unqiue identifier. Change the content of "OnSaveGameLoad" to your liking.
local ModID = "shared_LuaCoopLeader_Serp"
local function OnSaveGameLoad()
  if ts.GameSetup.GetIsMultiPlayerGame() then
    local PID = ts.Participants.GetGetCurrentParticipantID() -- dont using fn IsCoopTeam_serp here, because we can only use global stuff here and I dont want to make it global. because other mods should use the same fn without needed to wait for lua load of another mod (by using a local version themself)
    if (PID == 0 and (ts.Online.GetUsername(4)~="" or ts.Online.GetUsername(8)~="" or ts.Online.GetUsername(12)~="")) or 
      (PID == 1 and (ts.Online.GetUsername(5)~="" or ts.Online.GetUsername(9)~="" or ts.Online.GetUsername(13)~="")) or
      (PID == 2 and (ts.Online.GetUsername(6)~="" or ts.Online.GetUsername(10)~="" or ts.Online.GetUsername(14)~="")) or 
      (PID == 3 and (ts.Online.GetUsername(7)~="" or ts.Online.GetUsername(11)~="" or ts.Online.GetUsername(15)~="")) then
      ts.Conditions.RegisterTriggerForCurrentParticipant(1500004529) -- start the PopUp
    else
      g_Im_CoopLeader_LuaCoopHelper = true
    end
  else
    g_Im_CoopLeader_LuaCoopHelper = true
  end
end
g_saveloaded_events_serp = g_saveloaded_events_serp or {} -- global table where mods can add their functions to (define it if it does not exist yet)
if g_saveloaded_events_serp~=nil and g_saveloaded_events_serp[ModID]==nil then -- do not change these lines, just copy paste
  g_saveloaded_events_serp[ModID] = OnSaveGameLoad
end


