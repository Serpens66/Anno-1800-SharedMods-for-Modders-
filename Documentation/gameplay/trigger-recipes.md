# Worked trigger recipes and new-chat walkthroughs

Read [design](triggers.md), [condition pitfalls](trigger-conditions.md) and [audit boundaries](../reference/trigger-audit.md) first. The XML files below are complete ModOps **documentation examples**, not installed mods. Every uppercase GUID token is a required collision-free reserved integer substitution; tests bind them to private fixture IDs. No example is deployed or run in the game.

Each example introduces its own locked result/signal assets, preserving the native anchor 130248. Gates illustrate input signals; they are not population/session/object checks until replaced by an audited contract. Shared helper IDs in the final recipe are real dependencies, not fixture-defined native assets. In a new mod, also create the usual modinfo.json with your stable ModID and dependencies.

## Examples

### One execution after a timer

One trigger instance completes once. This is not an every-save-load callback.

[Complete XML](../reference/triggers/examples/once.xml).

Embedded Trigger body (inside Values of the owning Trigger asset):

```xml
<Trigger>
          <TriggerCondition>
            <Template>ConditionTimer</Template>
            <Values>
              <Condition/>
              <ConditionTimer>
                <TimeLimit>1000</TimeLimit>
              </ConditionTimer>
            </Values>
          </TriggerCondition>
          <TriggerActions>
            <Item>
              <TriggerAction>
                <Template>ActionUnlockAsset</Template>
                <Values>
                  <Action/>
                  <ActionUnlockAsset>
                    <UnlockAssets>
                      <Item>
                        <Asset>RESULT_GUID</Asset>
                      </Item>
                    </UnlockAssets>
                  </ActionUnlockAsset>
                </Values>
              </TriggerAction>
            </Item>
          </TriggerActions>
          <ResetTrigger>
            <Template>EmptyAutoCreateValue</Template>
            <Values>
              <EmptyAutoCreateValue/>
            </Values>
          </ResetTrigger>
        </Trigger>
```

### A repeated state pulse

Main completion unlocks the private result marker; the reset child waits 1000 ms, locks it and rearms the main trigger. The main wait is 10000 ms; the reset wait is additional. Substitute your audited action and repeat policy.

[Complete XML](../reference/triggers/examples/repeat.xml).

### Three state gates at the action

Actions belong to the deepest level. Gates are private assets initially locked; the consuming mod supplies the signals. Flattening them into Parallel siblings changes the reported timing contract.

[Complete XML](../reference/triggers/examples/simultaneous.xml).

Embedded Trigger body (inside Values of the owning Trigger asset):

```xml
<Trigger>
          <TriggerCondition>
            <Template>ConditionUnlocked</Template>
            <Values>
              <Condition/>
              <ConditionUnlocked>
                <UnlockNeeded>GATE_A_GUID</UnlockNeeded>
              </ConditionUnlocked>
            </Values>
          </TriggerCondition>
          <TriggerActions/>
          <SubTriggers>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionUnlocked</Template>
                      <Values>
                        <Condition/>
                        <ConditionUnlocked>
                          <UnlockNeeded>GATE_B_GUID</UnlockNeeded>
                        </ConditionUnlocked>
                      </Values>
                    </TriggerCondition>
                    <TriggerActions/>
                    <SubTriggers>
                      <Item>
                        <SubTrigger>
                          <Template>AutoCreateTrigger</Template>
                          <Values>
                            <Trigger>
                              <TriggerCondition>
                                <Template>ConditionUnlocked</Template>
                                <Values>
                                  <Condition/>
                                  <ConditionUnlocked>
                                    <UnlockNeeded>GATE_C_GUID</UnlockNeeded>
                                  </ConditionUnlocked>
                                </Values>
                              </TriggerCondition>
                              <TriggerActions>
                                <Item>
                                  <TriggerAction>
                                    <Template>ActionUnlockAsset</Template>
                                    <Values>
                                      <Action/>
                                      <ActionUnlockAsset>
                                        <UnlockAssets>
                                          <Item>
                                            <Asset>RESULT_GUID</Asset>
                                          </Item>
                                        </UnlockAssets>
                                      </ActionUnlockAsset>
                                    </Values>
                                  </TriggerAction>
                                </Item>
                              </TriggerActions>
                              <ResetTrigger>
                                <Template>EmptyAutoCreateValue</Template>
                                <Values>
                                  <EmptyAutoCreateValue/>
                                </Values>
                              </ResetTrigger>
                            </Trigger>
                          </Values>
                        </SubTrigger>
                      </Item>
                    </SubTriggers>
                    <ResetTrigger>
                      <Template>EmptyAutoCreateValue</Template>
                      <Values>
                        <EmptyAutoCreateValue/>
                      </Values>
                    </ResetTrigger>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
          </SubTriggers>
          <ResetTrigger>
            <Template>EmptyAutoCreateValue</Template>
            <Values>
              <EmptyAutoCreateValue/>
            </Values>
          </ResetTrigger>
        </Trigger>
```

### Two events in order

Arm before emitting A. B must occur after the second listener becomes eligible; a B event that happened earlier is not a substitute for the later event. For live state use ConditionUnlocked instead, with different semantics.

[Complete XML](../reference/triggers/examples/sequence.xml).

### First complete alternative wins

A is first, but it must finish its descendant timer before that branch is complete. B may win while A is incomplete. Keep consequential actions at branch completion. Priority does not reserve the result merely because A first became true.

[Complete XML](../reference/triggers/examples/priority.xml).

Embedded Trigger body (inside Values of the owning Trigger asset):

```xml
<Trigger>
          <TriggerCondition>
            <Template>ConditionAlwaysTrue</Template>
            <Values>
              <Condition>
                <SubConditionCompletionOrder>MutuallyExclusive</SubConditionCompletionOrder>
              </Condition>
              <ConditionAlwaysTrue/>
            </Values>
          </TriggerCondition>
          <TriggerActions/>
          <SubTriggers>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionUnlocked</Template>
                      <Values>
                        <Condition/>
                        <ConditionUnlocked>
                          <UnlockNeeded>GATE_A_GUID</UnlockNeeded>
                        </ConditionUnlocked>
                      </Values>
                    </TriggerCondition>
                    <TriggerActions/>
                    <SubTriggers>
                      <Item>
                        <SubTrigger>
                          <Template>AutoCreateTrigger</Template>
                          <Values>
                            <Trigger>
                              <TriggerCondition>
                                <Template>ConditionTimer</Template>
                                <Values>
                                  <Condition/>
                                  <ConditionTimer>
                                    <TimeLimit>1000</TimeLimit>
                                  </ConditionTimer>
                                </Values>
                              </TriggerCondition>
                              <TriggerActions>
                                <Item>
                                  <TriggerAction>
                                    <Template>ActionUnlockAsset</Template>
                                    <Values>
                                      <Action/>
                                      <ActionUnlockAsset>
                                        <UnlockAssets>
                                          <Item>
                                            <Asset>RESULT_GUID</Asset>
                                          </Item>
                                        </UnlockAssets>
                                      </ActionUnlockAsset>
                                    </Values>
                                  </TriggerAction>
                                </Item>
                              </TriggerActions>
                              <ResetTrigger>
                                <Template>EmptyAutoCreateValue</Template>
                                <Values>
                                  <EmptyAutoCreateValue/>
                                </Values>
                              </ResetTrigger>
                            </Trigger>
                          </Values>
                        </SubTrigger>
                      </Item>
                    </SubTriggers>
                    <ResetTrigger>
                      <Template>EmptyAutoCreateValue</Template>
                      <Values>
                        <EmptyAutoCreateValue/>
                      </Values>
                    </ResetTrigger>
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
                        <Condition/>
                        <ConditionUnlocked>
                          <UnlockNeeded>GATE_B_GUID</UnlockNeeded>
                        </ConditionUnlocked>
                      </Values>
                    </TriggerCondition>
                    <TriggerActions>
                      <Item>
                        <TriggerAction>
                          <Template>ActionUnlockAsset</Template>
                          <Values>
                            <Action/>
                            <ActionUnlockAsset>
                              <UnlockAssets>
                                <Item>
                                  <Asset>ALTERNATE_RESULT_GUID</Asset>
                                </Item>
                              </UnlockAssets>
                            </ActionUnlockAsset>
                          </Values>
                        </TriggerAction>
                      </Item>
                    </TriggerActions>
                    <ResetTrigger>
                      <Template>EmptyAutoCreateValue</Template>
                      <Values>
                        <EmptyAutoCreateValue/>
                      </Values>
                    </ResetTrigger>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
          </SubTriggers>
          <ResetTrigger>
            <Template>EmptyAutoCreateValue</Template>
            <Values>
              <EmptyAutoCreateValue/>
            </Values>
          </ResetTrigger>
        </Trigger>
```

### Optional side action without blocking

The root can complete without the side gate. A side action is conditional, not guaranteed. This is a leaf example. Serp considers it very likely that optional children also exempt their non-optional descendants from blocking the parent; see the qualified nested example in [trigger design](triggers.md#subtrigger-timing-and-actions).

[Complete XML](../reference/triggers/examples/optional.xml).

Embedded Trigger body (inside Values of the owning Trigger asset):

```xml
<Trigger>
          <TriggerCondition>
            <Template>ConditionTimer</Template>
            <Values>
              <Condition/>
              <ConditionTimer>
                <TimeLimit>1000</TimeLimit>
              </ConditionTimer>
            </Values>
          </TriggerCondition>
          <TriggerActions>
            <Item>
              <TriggerAction>
                <Template>ActionUnlockAsset</Template>
                <Values>
                  <Action/>
                  <ActionUnlockAsset>
                    <UnlockAssets>
                      <Item>
                        <Asset>RESULT_GUID</Asset>
                      </Item>
                    </UnlockAssets>
                  </ActionUnlockAsset>
                </Values>
              </TriggerAction>
            </Item>
          </TriggerActions>
          <SubTriggers>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionUnlocked</Template>
                      <Values>
                        <Condition>
                          <IsOptional>1</IsOptional>
                        </Condition>
                        <ConditionUnlocked>
                          <UnlockNeeded>GATE_A_GUID</UnlockNeeded>
                        </ConditionUnlocked>
                      </Values>
                    </TriggerCondition>
                    <TriggerActions>
                      <Item>
                        <TriggerAction>
                          <Template>ActionUnlockAsset</Template>
                          <Values>
                            <Action/>
                            <ActionUnlockAsset>
                              <UnlockAssets>
                                <Item>
                                  <Asset>OPTIONAL_RESULT_GUID</Asset>
                                </Item>
                              </UnlockAssets>
                            </ActionUnlockAsset>
                          </Values>
                        </TriggerAction>
                      </Item>
                    </TriggerActions>
                    <ResetTrigger>
                      <Template>EmptyAutoCreateValue</Template>
                      <Values>
                        <EmptyAutoCreateValue/>
                      </Values>
                    </ResetTrigger>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
          </SubTriggers>
          <ResetTrigger>
            <Template>EmptyAutoCreateValue</Template>
            <Values>
              <EmptyAutoCreateValue/>
            </Values>
          </ResetTrigger>
        </Trigger>
```

### A locked-presence guard for saved triggers

PRESENCE_GUID is a private UnlockableAsset with DefaultLockedState=1 which must never be unlocked. The saved trigger checks that it is still locked before its child/actions can run. When the mod asset disappears, the reported missing-GUID-as-unlocked behavior makes the negated guard false. This demonstrates the presence guard, not a new in-game removal test or a lock-to-start bridge.

[Complete XML](../reference/triggers/examples/removal-safe.xml).

Embedded Trigger body (inside Values of the owning Trigger asset):

```xml
<Trigger>
          <TriggerCondition>
            <Template>ConditionUnlocked</Template>
            <Values>
              <Condition/>
              <ConditionUnlocked>
                <UnlockNeeded>PRESENCE_GUID</UnlockNeeded>
              </ConditionUnlocked>
              <ConditionPropsNegatable>
                <NegateCondition>1</NegateCondition>
              </ConditionPropsNegatable>
            </Values>
          </TriggerCondition>
          <TriggerActions/>
          <SubTriggers>
            <Item>
              <SubTrigger>
                <Template>AutoCreateTrigger</Template>
                <Values>
                  <Trigger>
                    <TriggerCondition>
                      <Template>ConditionTimer</Template>
                      <Values>
                        <Condition/>
                        <ConditionTimer>
                          <TimeLimit>1000</TimeLimit>
                        </ConditionTimer>
                      </Values>
                    </TriggerCondition>
                    <TriggerActions>
                      <Item>
                        <TriggerAction>
                          <Template>ActionUnlockAsset</Template>
                          <Values>
                            <Action/>
                            <ActionUnlockAsset>
                              <UnlockAssets>
                                <Item>
                                  <Asset>RESULT_GUID</Asset>
                                </Item>
                              </UnlockAssets>
                            </ActionUnlockAsset>
                          </Values>
                        </TriggerAction>
                      </Item>
                    </TriggerActions>
                    <ResetTrigger>
                      <Template>EmptyAutoCreateValue</Template>
                      <Values>
                        <EmptyAutoCreateValue/>
                      </Values>
                    </ResetTrigger>
                  </Trigger>
                </Values>
              </SubTrigger>
            </Item>
          </SubTriggers>
          <ResetTrigger>
            <Template>EmptyAutoCreateValue</Template>
            <Values>
              <EmptyAutoCreateValue/>
            </Values>
          </ResetTrigger>
        </Trigger>
```

### Positive participant and session gates

Requires ModDependencies containing WhichPlayer_Serp (which depends on IsAIPlayer_Serp), plus its actual initialization scripts. Positive 1500001613 identifies processing Human0 after readiness; 180023 is the audited Moderate session. Any Coop peer may satisfy ActiveSession. This does not select one Lua peer or establish an action session/area.

[Complete XML](../reference/triggers/examples/human-session.xml).

## Walk through a design using only this documentation

| Task | Expected design / reason |
| --- | --- |
| Complex A, B, C live-state requirement | Nested one-child gates with actions at C; explain why Parallel remembers earlier successes. Check optional/MutualArea exceptions before substituting them. |
| Ordered event chain | Linear children, with each event emitted after its listener becomes eligible; a persistent unlock is a different state check. |
| Prioritized alternatives | MutuallyExclusive, highest-priority complete branch first; incomplete first branches do not yet exclude later complete branches. Avoid irreversible actions in speculative partial branches. |
| Repeated execution | Embedded ResetTrigger with a deliberate wait; include its wait in the cycle and account for actions changing the original condition. |
| Save-compatible extension | Preserve historical GUID state; a separately guarded migration or the documented reset extension point supplies new actions. Explain why appending a reset to a completed GUID is insufficient. |
| Coop-sensitive Lua action | Identify processing participant separately from executing peers. Use the reviewed lock/cooldown or peer mechanism; Human0 alone does not deduplicate clients. |
| Multiple checks on one island | Use the specialized main MutualArea plus same-level Area-producing checks and the correct action/quest context. Session agreement alone is insufficient. |

Offline checks parse all eight complete examples, bind placeholders, verify native template/property membership, inspect the exact subtrigger/reset trees, and apply each ModOp with the actual Anno 1800 XML evaluator to the exact vanilla anchor. The checks do not execute conditions/actions, settle the unresolved timing contracts or prove multiplayer safety. See [validation results](../reference/validation/triggers/results.json).

