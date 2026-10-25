# Loader components, history and upstream tests

## Do not equate all repository components with the integrated loader

Evidence is pinned to `stable/anno1800`, commit `8326b7c5a7648787c52f1252cd6e8ae60e593d1c`. The repository contains both reusable XML libraries and the old external Python DLL implementation. Its current README explicitly states that Anno 1800 includes the loader from GU17 onward.

The inspected `libs/external-file-loader` is wired to `libs/python35` through its BUILD dependencies and the Python DLL entry point. It hooks Windows/game file loading and detects game addresses. Its scanner accepts a single mods directory, prioritizes Documents if it exists, skips only dash-prefixed mod folders and `.cache`, and sorts by folder name. **These are historical component facts.** They must not override the integrated-loader README and the inspected ModLoadingOrder class, which describe both mods locations, activation by ModID, version selection and explicit ordering.

All mod_manager.cc, external-file-loader.cc, mod.cc, their relevant public headers and BUILD file have been read. cache.cc and cache.h are empty; cache logic is actually inside mod_manager.cc. Embedded third-party hash/UTF-8 libraries are not additional authoring APIs; their internal algorithms have not been audited as game behavior.

## Historical file dispatch and caches

The old Mod maps every regular file recursively to its mod-relative game path. Its PathMap normalizes path syntax and compares uppercase Windows paths; this does not establish case-insensitive XML tags or XPath names.

For that external implementation:

- XML files are patchable; ordinary non-XML files replace the game-path file. Multiple non-patchable contributions overwrite the map entry during collection, so the last collected file wins.
- `start_script.py` is collected as a Python console startup command rather than an ordinary replacement file.
- Assets, templates and properties paths under `data/config/game/asset` are aliased to export/main/asset equivalents.
- Files are patched after a readiness point in archive loading. Modded file reads wait for the patching thread; output resides in memory or in a disk replacement file.
- Layer metadata stores input hash, patch hash, output hash, output filename and mod name, with patch-operation version `1.17`. A version mismatch excludes those cache entries.
- A cache hit requires the current input hash and patch-file hash. Cached output is Zstandard-compressed. An invalidated layer truncates later layers; the metadata writer removes obsolete generated layer files.
- The inspected patch hash is calculated for the main patch file, not recursively for its Include inputs. **Source inference:** include-only edits can leave an old external cache reusable. This is not proof of the integrated game's cache implementation.
- The watcher rebuilds/reloads data after mod-file changes and ignores cache paths/start_script.py notifications. Its presence is not evidence that the integrated game can safely hot-reload every feature, save contract or Lua lifetime.

Do not instruct users to install these external DLL hooks, alter game addresses or rely on their side effects as current mod prerequisites. The historical hook also overrides warning-time/credits behavior; those changes are unrelated to an authored mod's XML semantics.

## Historical Python startup versus development Python

The complete `libs/python35/src/python.cc` wrapper has been read. It calls the real PyRun_StringFlags first, then uses a process-static `scripts_done` flag to execute collected start-script commands once on the first intercepted call. This is old external Python integration, not a modern modinfo scripting lifecycle or an XML ActionExecuteScript Lua contract.

Serp's folder named `Python Modding` contains valuable later Lua notes. The folder name does not make its Lua tests Python behavior. Python used to inspect XML, create documentation inventories or validate files is an offline development tool; it does not require restoring game-side Python integration.

## Feature history read from actual diffs

The relevant history was fetched and concrete implementation/test diffs read. Commit dates differ from author dates for some changes; the table records commit dates and does not invent a game release date.

| Commit | Commit date | Verified change |
| --- | --- | --- |
| `3128ffe7d782b6f2eb2ef989707fbb6f7ac1aad8` | 2023-05-23 | Recursive merge adds a per-name occurrence index for ordered repeated nodes; old legacy wrapper form remains |
| `b6f417ab2c66616fff0cabfa5f618997dcad54a3` | 2023-05-23 | A single leading slash on Condition/Content inherits GUID/template context without requiring `~`; document-wide forms remain separate |
| `e96bc927ef7d512971c2d32f513293bc3f48a7a9` | 2023-05-23 | `@GUID` recognizes Values-container context |
| `e7d77e756859147b9be38d30488e73f996fb39c2` | 2023-06-17 | `#ModID` conditions use a supplied active-ID set; nested groups propagate that set |
| `1d5c15a5f4e027a74f6d5292cebaa0a4c4b6095e` | 2023-06-18 | FileDB writer repairs ChildCount from the greater InfoElement/VisibilityElement count |
| `ab03f369dd81260247fb142d9cc5eeebdf4f782d` | 2023-06-18 | FC writer maps repeated `$auto(n)` tokens to the same allocated ID |

Remaining history searches are tracked separately; this table is a reviewed feature timeline, not a claim that every repository commit has been semantically audited.

## Complete XML fixture reading and actual offline execution

All files in `tests/xml` have been read: inputs, patches, includes, all 61 active JSON specifications, one disabled `.json_` specification, generator, runner and BUILD rules. The generator selects only `*.json`; the disabled nested-merge experiment is not an active supported-feature test.

The upstream runner tests XPath existence/nonexistence and whether warning/error text appears. It does not compare complete XML documents, validate game templates or prove runtime behavior. It calls `load_file()` without checking its parse result, so malformed inputs must not be treated as trustworthy validation fixtures merely because they are in the repository.

The installed GU17.1 xmltest.exe was then used directly outside the sandbox to evaluate unchanged well-formed fixtures. [Results](validation/upstream-corpus/results.json) preserve commands, expected paths, individual assertions and logs; [validate_upstream_corpus.py](../tools/validate_upstream_corpus.py) reproduces the checks.

- **54 cases passed**, including relative and absolute Includes, include order, conditions and negation, groups, Skip, AllowNoMatch, @GUID context, content copying/wrapping, ordinary merge/replace/add/remove and sibling ordering.
- **Six cases were not executed** because their original inputs have mismatched Group/Groups closing tags. They are retained as source findings. The documentation's independent well-formed synthetic list/empty-merge checks already provide separate evidence for those tested operations.
- **One ModID case was not executed** because the upstream C++ runner supplies an active ModID set, while the inspected CLI Apply calls use the default empty set. Pretending that CLI execution recreates the supplied-ID context would give misleading results.
- The disabled `.json_` case expects recursive lookup that skips a parent level. Its suffix and actual merge implementation prevent treating it as supported syntax.

The test named include_order uses `Cat['2']`, a nonempty string predicate, rather than `Cat[text()='2']`. It demonstrates sequencing for its one-node fixture; it does not prove value filtering by that predicate. Likewise, synthetic templates and fields in the fixtures are XML structure tests, not vanilla-compatible asset recipes.

No compiled upstream Catch2 run or game/MP test is claimed. Executable identity and the two exact-vanilla recipe assertions are separately recorded in [offline validation](offline-validation.md).

Sources: [external component](https://github.com/jakobharder/anno-mod-loader/tree/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/external-file-loader), [Python wrapper](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/python35/src/python.cc), [XML corpus](https://github.com/jakobharder/anno-mod-loader/tree/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/tests/xml).
