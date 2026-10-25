# Offline validation and its limits

Checks performed on 2026-10-03. No game or multiplayer session was started.

## Actual Anno 1800 XML evaluator

The installed Anno Modding Tools 2.3.1 extension contains `external/xmltest.exe`, reporting **GU17.1**. Its SHA-256, complete command arguments, fixtures, patched output and logs are retained in [the result record](validation/loader/results.json). The check is reproducible with [validate_loader.py](../tools/validate_loader.py).

All eight assertions passed:

| Case | Observed output |
| --- | --- |
| `Condition="true()"` | XPath error; operation skipped; original name retained |
| Node selection as Condition | Operation applied |
| Replace `Standard` with a `Name` payload | `Standard` removed; child payload occupies its position |
| Replace `Standard` with a complete `Standard` payload | Correct container retained |
| Merge an empty list container | Existing entries retained |
| Merge one repeated `Item` | First occurrence changed; second retained |
| Add one `Item` | Third entry appended |
| `Path="@1/Standard"` | Name changed, confirming Values-relative lookup |

This confirms the tested standalone evaluator's behavior and agrees with the inspected `stable/anno1800` implementation. It does not identify the integrated loader's exact binary revision or establish in-game behavior on every release.

The first execution inside the Windows sandbox ended with `0xC0000409` before logging. Repeating the same offline checks outside the sandbox succeeded. This was an execution-environment failure, not evidence that the XML cases were invalid.

## Correct command form

Use separate arguments, for example:

```powershell
& 'C:\Users\Serpens66\.vscode\extensions\jakobharder.anno-modding-tools-2.3.1\external\xmltest.exe' `
  -c patch -m '<absolute mod folder>' -o '<absolute output.xml>' `
  '<absolute vanilla.xml>' '<absolute patch.xml>'
```

The final two arguments are positional. `-p` means **prepatch mod directory**, not patch filename. Despite the usage text printing `-c=<command>` and similar forms, the inspected parser consumes the next separate argument. Use `-c patch`, `-m path` and `-o path`.

Inspect both the log and output. A successful process exit alone does not imply every ModOp matched or was applied; the scalar-condition case reports an error while the command itself returns zero.

## Other validation layers

The complete upstream XML fixture corpus was also read and 54 unchanged, well-formed cases passed in the same standalone evaluator. Seven cases have explicit non-execution reasons: six malformed original XML inputs and one supplied active-ModID context unavailable in the inspected CLI call. See [corpus results](validation/upstream-corpus/results.json) and [loader history and tests](loader-history-and-tests.md). This is not a rebuilt upstream Catch2 suite.

Both XML [starting recipes](../recipes/basic-workflows.md) also passed [exact-asset checks](validation/recipes/results.json), reproduced by [validate_recipes.py](../tools/validate_recipes.py). The full dataAlle assets file was traversed to verify one occurrence each of GUID 2001241 and anchor 130248. The actual evaluator then patched isolated copies of those exact assets: the radius changed 28 to 40 with every other asset field preserved; one new Trigger retained the original sibling and the intended condition/action/script/second-party fields. The fixture used private GUID 2001000000 only within documentation outputs. This does not verify all modded-data interactions or startup runtime behavior.

Well-formed XML does not prove a valid XPath. A valid XPath does not prove a matching target in a particular vanilla/modded data set. A matching target does not prove a correct game property. Offline Lua syntax does not prove the existence, calling convention or synchronization of a native game function. Record each layer separately.

Sources: pinned loader `cmd/xmltest/src/main.cc`, `parse_args.cc`, XML operation implementation; installed executable provenance in the result record.

## Trigger documentation examples

[Trigger results](validation/triggers/results.json) record eight complete recipe patches using the installed 1800 evaluator, complete preservation of the exact native anchor 130248, native template/property/enum checks, private fixture GUID bindings, tree placement and rejection of three invalid contracts. Reproduce with `Documentation/tools/validate_triggers.py` after running the extraction/reference/example generators documented in [trigger audit](trigger-audit.md). No conditions/actions, dependency loader, game-save lifecycle or multiplayer session were executed.
