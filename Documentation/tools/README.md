# Tools and checks

Read [setup](../setup.md), [workflow](../workflow.md) and [maintenance](../maintenance.md) first. All commands below are relative to the Documentation folder. Substitute your interpreter's absolute path when it is not on PATH.

## Routine read-only checks

    python tools/validate_docs.py
    python -m unittest discover -s tests -v
    & .\tools\check-setup.ps1

`validate_docs.py` checks internal links/anchors, text encoding/CRLF, active personal-path leakage and XML snippet well-formedness without changing files or writing a receipt. It needs only Python's standard library. It does not execute Lua or evaluate ModOps. Tests cover configuration/source resolution, isolated use and setup error cases; fake game files in setup tests establish presence handling only.

The Windows setup check is read-only and accepts `-ConfigPath`. Python source tools accept the `ANNO_DOCUMENTATION_CONFIG` environment variable. All configured relative paths are based on that JSON file's location. No check installs tools or extracts game data.

## Source research and offline evaluator tools

The existing `inventory.py`, `vanilla_audit.py`, `runtime_audit.py`, trigger audits and offline evaluator scripts are specialist maintainer tools. They require configured sources, and many require `lxml`; evaluator scripts additionally require tools.xmltest. They are not prerequisites for reading the knowledge base. Configure the relevant checkout in sources or researchPath; never rely on Serp's temporary research folder surviving.

Fresh extraction/check outputs go to ignored outputPath. The dated artifacts under reference remain historical inputs; new output is not automatically promoted over them. Existing generators may read those historical inputs, so they are not a general current-game build pipeline. Source IDs/hashes must still be checked and interpreted for the feature.

Run evaluator scripts only after the relevant feature audit. Anno 1800's actual xmltest.exe is required; do not substitute xmltest2.exe. Inspect logs, match counts, output files and preservation assertions. Missing tools/sources mean checks are unavailable, never passed. Run Git/Lua outside the Windows sandbox; use the documented permission retry for infrastructure startup failures.

The `build_*`, `complete_*`, `finalize_*`, `integrate_*`, `link_*`, `make_*`, `record_*`, `review_ledger.py` and `reconcile_*` scripts are historical authoring utilities. Some intentionally rewrite chapters/ledgers and contain dated user-answer logic. Do not run them as validation or automatic maintenance; review their entire intended diff before deliberate use. In particular, a recorded test result must not be regenerated from a script's constant claim.

For XML/trigger/Lua reader scenarios and the one-time migration checks, see [consolidation](../reference/consolidation.md). Those checks are not game, save or multiplayer tests. Existing offline results remain in [offline validation](../reference/offline-validation.md).
