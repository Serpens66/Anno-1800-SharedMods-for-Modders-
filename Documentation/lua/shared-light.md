# LuaLight: implementation contract and limitations

Source: workspace `SharedMods/shared_LuaLight/` [GitHub](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/tree/3aece64f299365309aaf1f7a57f28e2f6900f106/shared_LuaLight), ModID **shared_LuaTools_Light_Serp**, version **1.009**. Read its `modinfo.json`, `data/scripts_serp/lighttools.lua` [GitHub](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/blob/3aece64f299365309aaf1f7a57f28e2f6900f106/shared_LuaLight/data/scripts_serp/lighttools.lua) and XML integration together. Bundled copies must be compared by hash/version before assuming the same contract.

Light depends on **WhichPlayer_Serp** and deprecates **shared_LuaTools_Serp**. Its Lua global is **g_LTL_Serp**. Initialize only when nil:

```lua
if g_LTL_Serp == nil then
    console.startScript("data/scripts_serp/lighttools.lua")
end
```

Loading the script recreates its table and clears `logs/lualog.txt`; repeated initialization can discard callback registrations. It also loads `data/scripts_serp/h/bint.lua` [GitHub](https://github.com/Serpens66/Anno-1800-SharedMods-for-Modders-/blob/3aece64f299365309aaf1f7a57f28e2f6900f106/shared_LuaLight/data/scripts_serp/h/bint.lua) when `g_bint_Library051` is nil and constructs a 256-bit integer type. The script itself is not a per-save initialization service.

## General utility interface

| Export / arguments | Result and relevant behavior |
| --- | --- |
| replace_chars_for_Name(str) | String with commas removed, equals converted to hyphens, brackets/braces/parentheses replaced by stars and backslash by slash; destructive normalization |
| TableToFormattedString(var,sorted,indent) | Recursive debug display; not a persistence format; cyclic tables are not handled |
| deepcopy(orig,copies) | Copy with cycle preservation and recursively copied metatables |
| table_len(t) | Counts pairs, including sparse/map keys |
| table_contains_value(tbl,x) | First matching key, otherwise false; iteration order unspecified |
| mysplit(pString,pPattern) | Pattern-based splitting; special escapes only for `.`, `(` and `)`; empty pieces generally omitted |
| myreplace(source,repl,with) | string.gsub; pattern semantics, special escape only for dot |
| myround(num,idp) | floor(x+0.5) rounding; do not assume symmetric negative rounding |
| my_to_type(value,to_type) | string/number/boolean/integer/bint conversion; integer rejects fractional numbers; string `"false"` becomes false; `"0"` is truthy |
| to_bint(value) | Fixed-width large integer; supply large values as decimal strings |
| MergeMapsDeep(...) | New recursively merged map; later non-table values win; asserts when a key's value types differ |
| weighted_random_choices(choices,num_choices) | Array of chosen keys with replacement, weights are map values; local math.random and unordered pairs |
| random_choice(choices) | One sequence element via math.random(#choices) |
| tables_equal(o1,o2,ignore_mt) | Recursive equality, optionally honoring __eq; no cycle detection |
| myeval(str,as_table_pointer) | Evaluates `return ...`; on error logs and returns original string; pointer mode returns parent object and final key |
| SortFnBigToSmall(a,b) | Descending comparison |
| pairsByKeys(t,f) | Iterator over a snapshot of sorted keys |
| GetPairAtIndSortedKeys(t,i,f) | Key/value at one-based sorted position |
| comma_value(n,sep) | Digit grouping, default comma; assumes input matches its numeric string pattern |
| GetOS() | `win` for backslash package separator, otherwise `unix` |
| TableToHex(table), HexToTable(hex) | Custom table-to-Lua-literal encoding, then hexadecimal; see restrictions below |
| argstotext(sep,...) | Debug concatenation with trailing separator; `{...}` plus pairs does not preserve nil arguments or reliable order |

Random helpers do not synchronize their results. Broadcast one selected outcome through an established mechanism before it drives replicated state; do not let every peer draw separately.

The hex serializer handles tables with string/number keys and number/string/Boolean values. It logs unsupported value types as nil. It does not escape quotes in strings, preserve userdata/functions/threads or detect cycles. Hexadecimal transport does not repair an incorrectly generated Lua literal. Do not use arbitrary user-entered strings without checking round-trip correctness.

## Logging and coroutines

| Export / arguments | Behavior |
| --- | --- |
| modlog(text,ModID) | Appends date and optional identifier to game-relative `logs/lualog.txt`; silently skips if file cannot open |
| log_error(err) | xpcall handler with debug.traceback, logs and returns full error string |
| start_thread(threadname,ModID,fn,...) | system.start wrapper; xpcall logs errors; name is `ModID: threadname` |
| waitForTimeDelta(waittime) | Coroutine yield loop using os.clock()*1000; not save-persistent |
| StopAllThreads() | Removes **all** system.internal.coroutines entries except names containing NoStopGameLeft; collects garbage |
| WasNewGameJustStarted() | CorporationTime < 30000 heuristic, not a saved per-mod initialization marker |
| IsHuman(PID) | Tests PID<4 only; caller must supply a valid nonnegative participant |

Thread names containing `_random_` get a random suffix; an existing name is otherwise replaced after a warning. `_nodouble_` returns false when an existing coroutine has that name. These conventions are local scheduling, not multiplayer deduplication.

The wait function is described as realtime in its comment, but its implementation uses **os.clock**. Standard Lua defines that as CPU time; the game may customize it. What is established here is the actual loop and the comment's observations, not a guaranteed portable wall-clock timer. Coroutines advance on game ticks and pause in menus/pause. A long-lived wait may resume in a different save unless explicitly cleaned up.

`StopAllThreads` has a global side effect on other mods' threads. Use the shared game-leave lifecycle intentionally; do not call it casually to stop only your own work.

## Object and area IDs

| Export / arguments | Result |
| --- | --- |
| AreatableToAreaID(Areatable) | Packs AreaIndex<<13, IslandID<<6, SessionID into an integer |
| AreaIDToAreatable(AreaID) | Unpacks masks 0xE000, 0x1FC0 and 0xF |
| OIDtableToOID(OIDtable) | Packs ObjectID low 32 bits, AreaID bits 32–47, EditorChunkID from bit 50 and EditorFlag from bit 63; returns string for editor fields |
| OIDToOIDtable(OID) | Uses bint, returns ObjectID, nested AreaID, EditorChunkID and EditorFlag |
| get_OID(userdata,to_type) | Parses `oid ...` from getName(); default number; choose string for large editor IDs |

The exact masks, including the **four-bit SessionID decode**, are part of this implementation. Do not silently generalize to arbitrary session IDs or assert a complete native bit-field specification. Comments include known tested examples, including `9223413826886570355` for a prebuilt object. Keeping that as a decimal string avoids precision loss and signed-range problems.

Object IDs are not globally unique without area/session fields. Moving a ship between sessions can change its OID. `ts.Area.Current.ID` over water/world map can be unsuitable; derive an audited object's area instead. Store IDs, then reacquire facades/userdata for the required session and lifetime.

## Textembed bridge and reserved resources

The XML adds Nameable and discovery configuration to scenario participants. It uses `OverwriteNameWithTextAsset=11156` and modifies confirmation-popup asset **500115**, matching DestroyConfirmation's ConfirmPopup button. These are integration side effects, not merely utility functions.

| Reserved resource | Use |
| --- | --- |
| PID120, asset100939 | CompanyName return channel for DoForSessionGameObject |
| PID121, asset101507 | Function name / arguments for t_FnViaTextEmbed |
| PID122, asset101508 | Optional single evaluated textembed argument |
| 1500005600 | Function bridge lock/dispatch FeatureUnlock |
| 1500005606 | ObjectDummies readiness signal referenced by comments; not owned by Light itself |
| 1500001613–1500001616 | WhichPlayer dispatch prerequisites |

Do not reuse these channels for independent protocols. CompanyName is the local short-lived channel here; the Nameable property on a session participant is a different mechanism used for saved/shared data by Medium/Ultra.

`t_FnViaTextEmbed(PID)` reads PID121's CompanyName, restores the normal names, splits by `|`, resolves the global function/arguments with myeval, then starts a protected coroutine. With `usetextembed`, it substitutes PID122's evaluated CompanyName. Its caller must obey the 1500005600 availability check and lock/release protocol. Read the XML comments before constructing a notification command; the old underscore example is historical, whereas the implementation splits pipes.

`DoForSessionGameObject(ts_embed_string,doreturnstring,keepasstring)` runs `game.TextSourceManager.setDebugTextSource`. With a return requested it writes the expression into PID120's CompanyName, reads it, resets the name, and optionally evaluates the string. A reset/default name produces nil. It cannot safely return arbitrary object tables/pointers through a display name. Validate the expression and avoid concurrent use of its return channel.

## Game-specific public utilities

| Export / arguments | Result, context or limitation |
| --- | --- |
| ToTextembed(path) | Converts dots to spaces, removes initial Get/Set per component; convenience transformation, not a full grammar parser |
| SplitNumberFromName(name) | Splits underscores; returns concatenated nonnumeric parts and first number |
| AddToNameInvisible(origname,addstring,onlifnotaddedyet), GetNameInvisible(name) | Invisible-marker and `#` convention with reported 16-character display budget; substring checks use Lua patterns |
| GetFertilitiesOrLodesFromArea_CurrentSession(AreaID,kind) | GUID-keyed set through Count/At; kind Fertilities or Lodes; current-session restriction |
| GetVectorGuidsFromSessionObject(expression,InfoToInclude) | Zero-based result rows; default Guid string, Value number; expression must contain Count; replaces every Count substring |
| GetCoopPeersAtMarker(UIState,RefOid) | Set of other active Coop peers viewing the same marker; local peer excluded; not a complete active-peer census |
| GetItemOrBuffEffectTargets(GUID) | One-based GUID array through ToolOneHelper |
| GetAssetCosts(GUID) | ProductGUID-to-Amount map; duplicate product entries overwrite |
| GetGameObjectPath(OID,path) | Numeric OID uses dynamic ts.GetGameObject call; string OID uses textembed; invalid result may be zero or nil |
| GetActiveQuestInstances(DescriptionTextGUID,firstfound,startfromID,logloop,maxemptycount) | Quest instance IDs, filters IsActive and not HasEnded; starts at 2, stops after 20 consecutive empty entries by default; global instances do not identify owning participant |
| GetCurrentSessionObjectsFromLocaleByProperty(Property) | OID-keyed object records for local participant/current session; string property resolved with built-in ID table; excludes own buildings on foreign/unowned islands per comments |
| DestroyGUIDByLocal(PID,GUID,Property) | Finds local objects (default ShipMaintenance), waits for ownership change up to 100 yields, then SetAddDamagePercent(100,PID); specialized reaction protocol |
| EventOnObjectDeletionConfirmed | Register callbacks by unique ModID; confirmation-popup callback only, not every possible destruction |
| ChangeGUIStateIf(PID,allowedOwner,allowedselectedGUIDs,GUIState) | Intended conditional local UI toggle; see defect below |
| IsUserdataValid(userdata,OID) | Returns userdata if getName contains oid, else nil; does not defensively handle every nil/input type |
| HasProperty(userdata,Property,OID) | true/false/nil tri-state; pcall catches unsupported/missing property; native log may still show a caught exception |
| HasWalking, HasCommandQueue, HasAttacker, HasAttackable, HasBombarder(OID,userdata) | Property check plus heuristic value fallback; not authoritative absence detection |
| NeedsBuildPermit(OID,GUID) | ts.BuildPermits.GetNeedsBuildPermit, optionally resolves GUID |
| AffectedByStatusEffect(OID,StatusEffectGUID) | Attackable active status-effect chain only; not every item/global buff |
| GetModloaderlog(), GetActiveMods() | Windows USERPROFILE/Documents log reader and log parser; redirected Documents/Linux unsupported assumptions |

HasProperty's comments list unsupported properties even on a flagship: Standard, Object, Text, Drifting, MinimapToken, Cost, Craftable, Locked, ExpeditionAttribute, Stance, WorldMapSound and SoundEmitterCommandBarks. An exposed facade is not proof of native property presence. A fallback such as `nil ~= 0` can also give a misleading true result for an invalid object.

The export also supplies PIDs, ShipNameGUIDs, Languages, DiplomacyState, UITypeState and PropertiesStringToID. These are local observed catalogs. Property IDs, GUIType and UI event-state numbers must not be confused. UITypeState is explicitly incomplete. In particular, the returned UI event numbers are not promised to match dataset GUIType.

## Source defects: do not assume intended behavior

These are code-inspection findings, not new game tests. Existing mods remain unchanged.

- `play_random_sound(sounds)` calls `next(picks)` and assigns its first return (array key, usually 1) as the sound. The selected sound is the array **value**. The implementation does not implement its advertised selection correctly.
- `t_FnViaTextEmbed` compares TaskString to undefined `oldname` rather than the local oldname1. The intended default-name guard is not established by this condition.
- `GetEffectivities(GUID)` uses entire row tables as keys and values after GetVectorGuidsFromSessionObject; it does not extract the row's empty-string field as GetItemOrBuffEffectTargets does. Its advertised pool-to-percentage map is not produced as documented.
- `ChangeGUIStateIf` accesses `ts.Selection.Object.GUID.Owner`; GUID is otherwise used as a scalar. This owner-filter path must be corrected or independently verified before use.
- The export assigns `CallGlobalFnBlocked=CallGlobalFnBlocked`, but this file defines no such local function. In a clean environment that table field is absent. The actual blocker belongs to Medium.
- GetActiveMods recognizes only log entries beginning `Load [`; the nearby commented example includes an unbracketed `Load Cheat Mortar`. Its result is not an exhaustive list of active mods.
- The hex serializer does not escape apostrophes/backslashes inside generated Lua literals; round-trip support is narrower than arbitrary tables of arbitrary strings.

A future chat should verify the selected bundle's actual implementation before relying on these functions. Documentation is not permission to alter shared mods in this task.

## Trigger-side contract

[Trigger design](../gameplay/triggers.md#savegames-removal-and-extension-points) distinguishes the always-locked mod-presence guard from Light's initially-unlocked lock-to-start FeatureUnlock. Keep the existing availability, cooldown and peer execution contract when building a new consumer. [Condition pitfalls](../gameplay/trigger-conditions.md) also documents counter/pool and context handoff limits.
