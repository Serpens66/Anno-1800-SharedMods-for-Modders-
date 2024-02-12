
g_SessionEnter_Done_serp = g_SessionEnter_Done_serp or {}

-- should also work fine in multiplayer/coop because unlock is not a problem and even if the players are in different sessions, reappling a buff works on all sessions loaded.
 -- but in multiplayer the unlock will be done once per session and per human player (but again: still better than on every SessionEnter)


if event.OnSessionEnter["shared_OncePerSession_Serp"] == nil then -- only add it once
  
  -- better define the function here (after the if) to prevent problems (because the script is called on SessionEnter and it calls with the lua event on SessionEnter. If these both happen at the same time, the function that is currently called gets overwritten)
  local function OnSessionEnter_serp()
    local S_ID = session.getSessionGUID()
    S_ID = tostring(S_ID)
    if S_ID~=nil and S_ID~="" and S_ID~="nil" and S_ID~="180039" then -- 180039 is the worldmap
      if g_SessionEnter_Done_serp[S_ID] == nil then
        g_SessionEnter_Done_serp[S_ID] = true
        ts.Unlock.SetUnlockNet(1500004530)
      end
    end
  end
  
  event.OnSessionEnter["shared_OncePerSession_Serp"] = OnSessionEnter_serp
  
end


-- helper from shared_LuaOnGameLoaded
local ModID = "shared_OncePerSession_Serp"
local function OnSaveGameLoad()
  g_SessionEnter_Done_serp = {} -- empty this on every savegame load, because we don't know anything about the new savegame
  -- first time executing we already entered a session without having the event OnSessionEnter registered, so unlock it here
  local S_ID = session.getSessionGUID()
  S_ID = tostring(S_ID)
  if S_ID~=nil and S_ID~="" and S_ID~="nil" and S_ID~="180039" then -- 180039 is the worldmap
    if g_SessionEnter_Done_serp[S_ID] == nil then
      g_SessionEnter_Done_serp[S_ID] = true
      ts.Unlock.SetUnlockNet(1500004530)
    end
  end
end
g_saveloaded_events_serp = g_saveloaded_events_serp or {} -- global table where mods can add their functions to (define it if it does not exist yet)
if g_saveloaded_events_serp~=nil and g_saveloaded_events_serp[ModID]==nil then -- do not change these lines, just copy paste
  g_saveloaded_events_serp[ModID] = OnSaveGameLoad
end