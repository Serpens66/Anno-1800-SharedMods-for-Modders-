# Four traceable starting workflows

These workflows use reviewed contracts and separate offline checks from runtime evidence. They are starting recipes for small XML/Lua mods; they do not replace the mandatory feature audit when extending them to other game systems.

## 1. Change an existing asset scalar

Goal: change the standard harbour-construction radius in asset2001241. Its template BuildingBaseTiles has Standard and BuildingBaseTiles properties; the latter declares HarbourConstructionAreaRadius as an Integer. The native explicit value is28; the separate creative value is56. The property defaults concern render/street heights and do not override this explicit radius.

The source has no BaseAssetGUID and the scalar has no data-reference dependency. Preserve its other fields, texture references and creative radius. The audit and provenance are in [vanilla contracts](../reference/vanilla-contracts.json), asset2001241 and matching template/property/default entries.

Create a mod folder with `modinfo.json`, a unique stable ModID and a version, then add `data/config/export/main/asset/assets.xml`:

```xml
<ModOps>
  <ModOp Type="merge" GUID="2001241" Path="/Values/BuildingBaseTiles">
    <!-- Merge preserves the other heights, colors and creative-mode radius. -->
    <HarbourConstructionAreaRadius>40</HarbourConstructionAreaRadius>
  </ModOp>
</ModOps>
```

Check there is one asset and one target property; assert the resulting radius is40 and the other children remain. Do not replace BuildingBaseTiles with only a radius child. See [offline validation](../reference/offline-validation.md) for the actual tested container behavior.

This verifies a changed configuration value. It does not promise that every placement restriction disappears: height, beach, edge and other placement systems are separate constraints. No game-placement test was performed.

## 2. Create a new asset with a real script entry point

Goal: add a new automatically registered Trigger that logs startup once when its always-true condition fires. The new asset is independent of a BaseAssetGUID. Its templates are Trigger, ConditionAlwaysTrue and ActionExecuteScript, all inspected in [runtime contracts](../reference/runtime-contracts.json). Trigger's native template defaults AutoRegisterTrigger=1 and UsedBySecondParties=1; this recipe explicitly disables second-party creation.

First allocate a collision-free GUID in the project's current reservation. **`CUSTOM_TRIGGER_GUID` below requires replacement with a valid reserved integer**; it is not deployable syntax. Do not use a notebook's old “next free GUID” without checking workspace/current upstream allocations. Audit save compatibility before reusing a formerly deployed trigger GUID.

```xml
<ModOps>
  <ModOp Type="AddNextSibling" GUID="130248">
    <Asset>
      <Template>Trigger</Template>
      <Values>
        <Standard>
          <GUID>CUSTOM_TRIGGER_GUID</GUID>
          <Name>Example author startup trigger</Name>
        </Standard>
        <Trigger>
          <TriggerCondition>
            <Template>ConditionAlwaysTrue</Template>
            <Values><Condition /><ConditionAlwaysTrue /></Values>
          </TriggerCondition>
          <TriggerActions>
            <Item>
              <TriggerAction>
                <Template>ActionExecuteScript</Template>
                <Values>
                  <Action />
                  <ActionExecuteScript>
                    <ScriptFileName>data/example_author/startup.lua</ScriptFileName>
                  </ActionExecuteScript>
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
</ModOps>
```

Anchor130248 is present in the audited data and the local Light integration uses the same sibling anchor. Verify its current group context and that the inserted Trigger is not unintentionally included in a group-based pool. New identity, template membership, trigger registration and script dispatch are separate requirements; this complete payload supplies each relevant one.

An always-true auto-registered Trigger is not a guaranteed every-save-load callback. Registered/fired triggers persist in saves. Use the established lifecycle integration when that behavior is required, rather than adding credit/spawn actions to this startup example.

## 3. Start and guard Lua

Place the following at `data/example_author/startup.lua` in the same mod. This deliberately logs and reads context, without submitting gameplay mutations:

```lua
ExampleAuthor = ExampleAuthor or {}

function ExampleAuthor.logStartup()
    local file = io.open("logs/example_author.txt", "a")
    if file then
        file:write("startup PID=", tostring(ts.Participants.GetGetCurrentParticipantID()),
                   " session=", tostring(session.getSessionGUID()), "\n")
        file:close()
    end
end

local ok, err = pcall(ExampleAuthor.logStartup)
if not ok then
    print("ExampleAuthor startup failed: " .. tostring(err))
end
```

Use a unique author/mod prefix for globals and files. Relative logging requires the game's logs directory to exist and be writable. Read-only session/current-participant calls are documented in the inspected guide and personal notes; syntax checking does not certify those native functions in every game build.

For library callbacks, see the guarded registration in [execution and lifecycle](../lua/execution-and-lifecycle.md). A persistent process-global flag prevents duplicate callback registration, but cannot establish per-save initialization. Do not install 117 script-lifecycle metadata into an1800 mod.

Offline validation: replace the GUID placeholder, parse the XML, assert the anchor exists, inspect the resulting new Asset and template/property structure, then run Lua5.3 syntax checking on the standalone file. No game execution is required for those checks.

## 4. Assess a Coop action before implementing it

Start from the exact entry point. ActionExecuteScript invokes all human clients, even if one participant's trigger fired. A PID check can restrict participants but still leaves each Coop peer. A local button/selection has a different invoking-client set.

For the preceding logging recipe, each client's local log entry is intended. No peer election is necessary for that local effect. If replacing the log with AddAmount, BuyNet, an ownership change or item manipulation, reclassify the command individually using the [synchronization chapter](../multiplayer/synchronization.md) and original tests.

Write down the target participant, full OID and session; whether the command itself replicates; harmless or harmful repetition; submitting peer; readiness and completion; persistence and failure cleanup. A synchronized additive command submitted by two Coop peers adds twice. An unsynchronized change performed only by one can diverge. Neither is solved by a PID check alone.

Do not treat `ContinueCoopCalled()` as a Boolean: `AllCoop` is truthy. [Medium/Ultra](../lua/shared-medium-and-ultra.md) explains its current interface and WIP limits, including the shared-cache receiver defect. A documented helper limitation is a reason to design within its established contract or request a separately scoped fix, not to invent a replacement peer protocol.

Where the available test is uncertain, keep that uncertainty. Serp's latest socket result is “probably no desync”; it is not a general ItemContainer synchronization guarantee. The review can finish as a **documented unsupported/uncertain design**, with precise runtime test instructions, rather than falsely declaring it MP-safe.

## Package checklist for these examples

Use UTF-8/CRLF, correct relative resource paths, a unique ModID/GUID/global prefix, required metadata/dependencies and explicit load ordering where needed. Inspect log matches and modified output. These files belong to the documentation until separately deployed; the task has not installed a new mod or changed an existing one.

## Complex trigger workflows

The startup recipe above is deliberately small. For nested gates, Linear event chains, MutuallyExclusive complete-branch priority, optional actions, reset pulses and participant/session gating, read [trigger design](../gameplay/triggers.md), [condition selection](../gameplay/trigger-conditions.md) and the [complete trigger recipes](../gameplay/trigger-recipes.md). Their offline validation proves structure/patching only; saved-state and Coop design still require the documented contracts.
