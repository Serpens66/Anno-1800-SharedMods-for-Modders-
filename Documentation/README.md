# Anno 1800 modding knowledge base

This is the single maintained knowledge base for creating and editing **Anno 1800 PC mods**, for local assistants and chats reading GitHub. All prose is English; assistants answer in the user's language. Read the self-contained [chat instructions](AGENTS.md). No access to Serp's PC or surrounding workspace is required.

Public mod sources are linked on GitHub. Each user supplies their **own current extracted Vanilla files** for feature audits. Historical excerpts, inventories and examples do not replace that audit.

**Research is in progress.** An inventory is not a completed review. Read [coverage and next steps](reference/coverage.md) before treating this as an exhaustive reference. Unresolved statements are listed in [questions and discrepancies](reference/discrepancies.md). Existing tests documented by Serp are accepted unless contradictory; no new in-game or multiplayer tests have been performed.

## Start a new chat

Give the chat this README and ask:

> Read README.md, AGENTS.md, reference/coverage.md and reference/discrepancies.md from this Documentation folder. Use the relevant chapters and linked public sources for my task. Before game-dependent decisions, audit my own extracted Vanilla files. Ask for files you cannot access. Preserve evidence qualifications, and record reusable findings through maintenance.md.

1. For explanation/research, begin with the topic index; no local setup is required.
2. For mod work, follow [setup](setup.md) and the [workflow](workflow.md). A path grants access only if the chat has a file tool that can read it; otherwise upload the necessary files or use a local assistant.
3. Identify the mod, dependencies, feature and save/session context. Complete the [feature audit](foundations/vanilla-research.md) before choosing an implementation.
4. Read referenced source content and compare versions/hashes where applicable. Missing essential sources block dependent decisions, not unrelated explanation.
5. Preserve encoding, CRLF, structure and useful comments. Update this same knowledge base using [knowledge maintenance](maintenance.md); without write access, return a concrete proposed edit.

Local users may copy [local.example.json](local.example.json) to ignored `local.json`. [Practical tools](tools/README.md), [audit template](templates/audit.md) and [empty XML mod template](templates/xml-mod/README.md) are included. No subscription, globally installed skill, complete game database or executable is bundled.

## Topic index

For a progressive, human-readable introduction with collapsible code examples and a condition catalogue in one file, read the [standalone Trigger Guide](Trigger_Guide.md).

| Task | Read |
| --- | --- |
| Find the real data, defaults and references | [Vanilla research](foundations/vanilla-research.md) |
| Read property definitions, nested types and dataset values | [Properties and datasets](foundations/vanilla-research.md#reading-properties-toolonexml-and-datasetsxml) |
| Understand assets, templates and BaseAssetGUID | [Inheritance](foundations/inheritance.md) |
| Package and order mods or shared dependencies | [Structure and metadata](foundations/structure-and-loading.md) |
| Make mods compose safely | [Mod compatibility](foundations/mod-compatibility.md) |
| Allocate identifiers and convert binary formats | [Identifiers and tools](foundations/identifiers-and-tools.md) |
| Configure authoring tools and inspect generated deployment | [Authoring tools](foundations/authoring-tools.md) |
| Write an XML patch | [ModOps](xml/modops.md) and [XPath](xml/xpath.md) |
| Copy nodes or construct lists | [Dynamic content](xml/content-and-lists.md) |
| Create and connect reward pools; understand weights and allowed targets | [Reward Pool Guide](Guide_RewardPools.md), [native audit and limits](reference/reward-pools-audit.json) |
| Build gameplay triggers, combine subtriggers and handle saved state | [Trigger design](gameplay/triggers.md), [condition selection](gameplay/trigger-conditions.md), [complete fields](gameplay/trigger-condition-reference.md), [datasets](gameplay/trigger-datasets.md) [recipes](gameplay/trigger-recipes.md) and [real mod walkthroughs](reference/trigger-mod-walkthroughs.md) |
| Unpack saves, inspect stored triggers/quests and distinguish code revisions | [Reading savegames](gameplay/savegames.md), [historical Campaign evidence (historical local evidence; summary available)](reference/local-evidence.md#savegame-audit) and [open Campaign review (historical local evidence; summary available)](reference/local-evidence.md#open-review) |
| Understand Lua entry points and lifetime | [Lua execution](lua/execution-and-lifecycle.md) |
| Avoid synchronous-read and object-access mistakes | [Lua API and timing](lua/api-and-timing.md) |
| Understand peer execution and synchronization | [Multiplayer and Coop](multiplayer/synchronization.md) |
| Use or assess the actual shared Lua interfaces | [LuaLight](lua/shared-light.md), [Medium and Ultra](lua/shared-medium-and-ultra.md) |
| Search objects or count executing Coop peers | [ObjectFinder and CoopCount](lua/objectfinder-and-coopcount.md) |
| Change tooltip XML and text expressions | [Infotips and text](ui-and-resources/infotips-and-text.md) |
| Patch model and feedback files | [CFG and FC patches](ui-and-resources/cfg-and-fc.md) |
| Decode binary resources and island containers | [Binary formats](ui-and-resources/binary-formats.md) |
| Understand converters and Blender source procedures | [Graphics toolchain](ui-and-resources/graphics-toolchain.md) |
| Build a small, reviewable example | [Recipes](recipes/basic-workflows.md) |
| Find source versions and review status | [Sources](reference/sources.md), [coverage](reference/coverage.md) |
| Check external tutorial defects and integration gaps | [External authoring review](reference/external-authoring-review.md) |
| Follow complete production/ship tutorial findings and pending native consumers | [Production tutorial review](reference/production-tutorial-review.md), [ship tutorial review](reference/ship-tutorial-review.md) |
| Trace existing notebook tests and corrections | [Personal test evidence](reference/personal-test-evidence.md) |
| See actual offline evaluator checks | [Offline validation](reference/offline-validation.md) |
| Separate external loader remnants and reviewed feature history | [Loader history and tests](reference/loader-history-and-tests.md) |

Additional gameplay, graphical-resource and shared-helper chapters will be added as their audits are completed. A missing topic must be researched, rather than inferred from a nearby example.

## Evidence labels

- **Loader source:** implementation inspected at the recorded Anno 1800 commit. This is not a claim that every released game build is byte-identical to that commit.
- **Vanilla data:** fields, defaults, examples or references found in `dataAlle`; extraction proves structure, not undocumented runtime semantics.
- **Serp test:** an observation explicitly documented in Serp's notes, guides or comments. Preserve its original conditions and qualifications.
- **Guide:** a published procedure; its version and any historical limitations matter.
- **Inference:** a conclusion derived from the preceding evidence; distinguish it from a test.
- **Pending:** not yet reviewed, contradictory, unavailable, or awaiting a runtime-only verification.

## Version boundary

The current Modloader Reference covers both Anno 117 and Anno 1800. Use the legacy `Type="..." Path="..."` form for 1800. Short attributes such as `Merge="..."`, standalone `<Asset>` operations, `ModItem`, `ModValue`, `MaxRepeat`, `Property` lookups, script lifecycle entries in `modinfo.json`, `active-options.jsonc`, and Anno 117's LineID/Oasis localization are **not Anno 1800 capabilities** established by this research.

The important exception is the `@GUID` lookup: it already exists in the 1800 implementation when used in the supported legacy attributes. It starts at the asset's **Values** container, while the `GUID` attribute starts at the **Asset**.

## Machine-readable research records

[Source inventory](reference/source-inventory.json) contains exact paths, SHA-256 hashes, detected encodings, line counts, headings, ModOp types and Lua signatures. [Duplicate groups](reference/duplicate-groups.json) identifies byte-identical copies. [Mod inventory](reference/mod-inventory.json) records each metadata file. [Link inventory](reference/link-inventory.json) preserves discovered URLs and their originating lines; discovery does not mean those URLs have been read.

[Vanilla contracts](reference/vanilla-contracts.json) stores selected source excerpts and provenance. [Vanilla GUID index](reference/vanilla-asset-index.json) is a structural lookup aid. Neither file is a replacement for the feature audit.

[Runtime contracts](reference/runtime-contracts.json) preserves script-entry templates, properties and native Lua examples. [Review ledger](reference/review-ledger.json) distinguishes sources that were read/reconciled from inventory-only entries and records documentation destinations. A partial integration audit is explicitly identified even when the Lua algorithm itself was read completely.

[Trigger audit](reference/trigger-audit.md) records the topic-specific review and its limits. [Native trigger contracts](reference/triggers/vanilla.json), [workspace trigger evidence](reference/triggers/workspace.json) and [source-comment destinations](reference/triggers/prose-evidence.md) support the trigger chapters; extraction is not complete whole-mod integration or runtime certification.

[Savegame evidence (historical local evidence; summary available)](reference/local-evidence.md#savegame-audit) records inspected save hashes, tool/source identities, anonymized condition/quest/peer excerpts and bounded decoder checks. The evidence separates historical releases and saved definitions; the [active review (historical local evidence; summary available)](reference/local-evidence.md#open-review) lists only unresolved questions/risks. No complete save or account identifier is included.

## One knowledge base and historical evidence

Read [knowledge maintenance](maintenance.md) for new or corrected findings. The [kit transfer register](reference/kit-transfer.md) is retained as history; no further transfer to ModdingWithCodex is required. [Consolidation provenance](reference/consolidation.md) records the one-time reconciliation, original IDs and starter-only additions.

[Sources](reference/sources.md) links public repositories and pinned revisions. [Local evidence summaries](reference/local-evidence.md) make reusable conclusions understandable without private reports. Original local reports, notes and saves are optional additional evidence, explicitly identified as unavailable in this download. Their summaries do not claim that the originals were published.

Dated JSON inventories, source hashes and validation receipts retain their historical contents. Absolute paths inside them identify historical inputs; they are not setup requirements. New runs resolve configured sources through `tools/workspace_paths.py` and write disposable research/check outputs under ignored `out/`. Old chapter generators are historical authoring utilities, not the normal update workflow; review them before deliberate use.

Earlier [relocation](reference/validation/relocation/results.json), source-review and kit receipts remain evidence for their stated versions only. Publishing this folder is separate from editing it; local changes reach other users only after an authorized GitHub publication.
