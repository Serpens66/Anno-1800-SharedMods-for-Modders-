# Lua execution and lifecycle

## Runtime and entry points

Anno 1800 exposes a modified Lua 5.3 environment. A Lua 5.3 syntax check is useful, but it cannot prove the availability, arguments or synchronization of a game-provided C function. The language runtime and game API are different contracts.

The game uses Lua for UI/game communication and native scenario/benchmark scripts. Ordinary mod scripts need an entry point; simply placing `init.lua` in a mod does not establish an automatic startup hook. The 117 `modinfo.json` script module/lifecycle mechanism must not be used for 1800.

| Entry | Execution context | Important limit |
| --- | --- | --- |
| XML `ActionExecuteScript` | All active human clients, including each Coop peer. | The trigger's processing participant does not restrict which clients run the Lua file. |
| `GUIConfig/KeyBindings/Item/Command` | The client that presses the key. | A command may still submit a synchronized game action. Local invocation and local effect are different. |
| Console/script manager | The invoking client. | Useful for investigation; not a self-starting distributable mod. |
| Existing generic popup command | The client clicking the button. | Serp reports at most three visible buttons and reuse of existing enum-backed popup types. |
| CharacterNotification button/default command | Textsource evaluation. | Not a general Lua evaluator; a raw `console.startScript(...)` is not interchangeable with a textembed. |

Sources: [execution guide](https://github.com/anno-mods/modding-guide/blob/main/Scripting/ExecutingScripts.md), [Serp's Lua problems](https://github.com/anno-mods/modding-guide/blob/main/Scripting/Lua_Probleme.md), fully read local `Python Modding/info.txt`.

## XML action shape

Inside a Trigger's `TriggerActions`, use `Item/TriggerAction`, not the `Item/Action` layout used by an ActionList:

```xml
<TriggerActions>
  <Item>
    <TriggerAction>
      <Template>ActionExecuteScript</Template>
      <Values>
        <Action />
        <ActionExecuteScript>
          <ScriptFileName>data/author/my_feature/init.lua</ScriptFileName>
        </ActionExecuteScript>
      </Values>
    </TriggerAction>
  </Item>
</TriggerActions>
```

This is an inline action fragment, not a complete mod. The audited schema makes `ScriptFileName` a FileName field. The ActionExecuteScript template provides Action and ActionExecuteScript. Native asset 100128, `S03 Start Trigger`, contains this shape and invokes the supplied scenario script; the script itself uses scenario-specific commands. Do not copy its scenario targets into a sandbox mod.

Audit evidence: [runtime contracts](../reference/runtime-contracts.json), ActionExecuteScript template/schema, Trigger/TriggerQuest contracts, asset 100128 and its referenced `scenario_03_start.lua`; [vanilla contracts](../reference/vanilla-contracts.json).

## Repeated initialization

The early guide initializes on `ConditionEvent=SessionEnter` and resets the trigger so subsequent entries reload the function library. This is a workaround for startup/lifetime limitations, not an assertion that each SessionEnter is a new savegame. Initialization must be idempotent: replacing functions can be harmless; registering another event callback or crediting resources every time is not.

The native Trigger template auto-registers and is used by second parties by default. FeatureUnlock also auto-self-unlocks by default. Override those explicitly where the audited feature requires different behavior. A blank `<TriggerSetup />` does not negate template settings.

Serp's notes establish that Lua variables belong to the running game process: loading another save without exiting the game can retain variables from the previous save. A full game restart resets them. This means a global `initialized` boolean alone cannot establish that the current save has received the required initialization. Shared helpers provide additional lifecycle handling; read their actual version before adopting that integration.

Keep per-save data separate from function-library registration. Store durable state in an audited game mechanism or the established save helper. Do not assume a Lua table or coroutine is serialized into the savegame.

## Native events

Native scripts use `table.insert(event.OnSessionEnter, callback)`, `OnSessionLoad`, `OnSessionLoaded`, `OnCameraSequenceEnd` and `OnLeaveUIState`. These are callback containers, not a complete mapping from the XML SimpleEventType dataset. Serp tested many other `event.On...` names and found them nil.

The native benchmark examples show different argument shapes: OnSessionLoaded receives a structure with `sessionGUID`; OnCameraSequenceEnd receives a structure with `cameraSequenceID`. Do not interchange OnSessionLoad and OnSessionLoaded or assume a GUID argument on every event.

Serp reports that an error escaping a native-event callback can crash the game without recording the Lua error. Guard callbacks, and prevent duplicate registration:

```lua
-- Keep registration stable when the function library is reloaded.
MyFeature = MyFeature or {}

function MyFeature.onSessionEnter()
    -- Re-evaluate current session state here; no gameplay action in this example.
end

if not MyFeature.sessionEnterCallback then
    MyFeature.sessionEnterCallback = function(...)
        local ok, err = pcall(MyFeature.onSessionEnter, ...)
        if not ok then
            local file = io.open("logs/my_feature_errors.txt", "a")
            if file then
                file:write(tostring(err), "\n")
                file:close()
            end
        end
    end
    table.insert(event.OnSessionEnter, MyFeature.sessionEnterCallback)
end
```

The guard prevents repeated registration during library reload. It does not detect a new save or remove the callback when a mod is disabled. Callback removal must identify your own function; do not copy vanilla's `table.remove(event.OnLeaveUIState)` without an index, because it removes the last callback and could remove another mod's handler.

Native evidence: `data/script/benchmark/{benchmark,bench}.lua` and `data/dlc12/scenario04/.../outro_sequence_00.lua`, preserved with hashes in runtime contracts.

## Coroutines and delayed operations

`system.start(function, label)` schedules a coroutine resumed by game ticks. The native `visitallmarkets.lua` uses it with `system.waitForGameTimeDelta(20000)`. Execution runs until return or yield; a loop without yielding can block the game.

Use `coroutine.yield()` inside a managed coroutine when waiting for game progress. Calling it from an ordinary non-yieldable entry is not an equivalent scheduling mechanism. Waiting in real milliseconds outside the game cannot make a blocked game tick advance.

Some writes are deferred. The guide's AddAmount example becomes visible after a tick in that example, while Serp's later tests show that one tick does not reliably suffice for every property or save. Observe the specific result where possible, bound the wait, and handle failure. See [API and timing](api-and-timing.md).

Long-running coroutines are not persistent scheduled game actions. Serp's notes describe waits retained during some save reloads within the same process but lost after restart or after the old wait already finished. For a long-lived saved timer, investigate the XML ConditionTimer/Trigger lifecycle rather than promising that a coroutine survives loading.

## Logging and failures

`print` writes to the console. Use a checked `io.open` and the returned file handle for a dedicated log. Avoid the guide's global `file` variable and `io.output`, which change shared Lua state. Relative log paths are reported to resolve beneath the game installation; the directory must exist and be writable.

An error inside `system.start` can terminate work without the obvious report expected from direct execution, according to Serp's notes. Record the start, relevant arguments, completion and failure in important helper calls. An error containing `no matching overload found` often indicates a wrong type or argument count; it is not evidence that an arbitrary alternative argument is valid.

Do not wrap all failures in a silent `pcall`. Catch the error at the boundary, log it, clean up your own temporary state and stop the failed operation. Never change native global APIs to intercept all game behavior: Serp's experiment replacing `ts.Economy.MetaStorage.AddAmount` only affected Lua callers using that wrapper, not native/textembed consumers.

## Gameplay trigger design

Use [trigger design](../gameplay/triggers.md) for registration, ResetTrigger, saved instances, mod-removal guards and the difference between state and events. [Condition selection](../gameplay/trigger-conditions.md) preserves the inconsistent MetaGameLoaded/ProfileLoaded tests and session/readiness limits; [recipes](../gameplay/trigger-recipes.md) provide complete XML structures. A startup trigger does not establish an every-save-load callback.
