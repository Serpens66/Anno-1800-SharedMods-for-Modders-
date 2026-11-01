# One-time knowledge consolidation

Date: **2026-11-01**. Documentation is now the only maintained knowledge base. ModdingWithCodex was read as a historical starter draft; it was not edited, deleted, archived or published by this change. There is no automatic synchronization, commit or push.

## Reconciliation and provenance

[Source records](consolidation-sources.json) retain hashes and destinations for every starter Documentation file and the local report snapshots consulted. Overlapping foundations/XML chapters were selected adaptations of the existing full chapters: retain the full chapters and qualifications, rather than maintaining the shortened edition alongside them.

- Setup, guided workflow, path checks and the empty mod/audit templates were adapted into this folder. Former skill instructions are expressed directly through AGENTS.md, setup.md and workflow.md; no skill installation/discovery is required.
- The starter's bounded full-database scalar-edit audit adds [its historical result](radius-audit.md), including original hashes and limits. It has not been rerun by this migration.
- Original adaptation hashes and starter validation results are retained under reference/history/starter-kit. They remain earlier checks, not current migration results.
- The reward-pool starter chapter was a bounded adaptation of the complete [guide](../Guide_RewardPools.md) and [audit](reward-pools-audit.json), which remain canonical. Its portable source identities do not supersede original audit hashes.
- Both complete guides were relocated byte-for-byte into Documentation. Their old locations are pointers.

No new gameplay contract is inferred by consolidation. The full documentation still has incomplete coverage, reported tests and unresolved runtime questions; read [coverage](coverage.md) and [discrepancies](discrepancies.md).

## Historical transfer entries

Preserve [KIT001-KIT021 and their existing receipts](kit-transfer.md), including gaps in the numbering. Original adopted/excluded/open statuses describe the earlier kit and are not rewritten as adoption into a new kit.

| Historical scope | Current destination / treatment |
| --- | --- |
| KIT001-KIT012 | Full foundations/XML chapters, setup/workflow, evidence registers and radius audit |
| KIT013-KIT015 | Existing full Lua/trigger/graphics/MP chapters remain available; a complete specialist wizard or runtime certification is not implied |
| KIT016 | Full reward-pool guide and original bounded audit |
| KIT017 | Read-only savegame chapter and local-evidence summary; no save editor or retroactive repair |
| KIT018 | Trigger chapter and local-evidence summary retain cancellation/settings cautions |
| KIT020 | Local-evidence summary retains post-story gate lesson and qualified speed recollection |
| KIT021 | Existing compatibility chapter, source record and offline composition results |

The historical KIT020 relationship names KIT019, but no KIT019 entry was present in the inspected register. Do not invent or reuse that ID; the original relationship remains historical provenance.

## Verification boundary

Current checks cover isolated Documentation-only use, links/anchors, JSON/template shape, text format, configuration resolution with different source locations, read-only validation, setup error cases and authored XML/trigger/Lua reader scenarios. Scenarios check available references and missing-source handling; they do not independently prove gameplay semantics or simulate a new chat.

See [the migration receipt](validation/consolidation/results.json) for actual commands/results. No new game, save, multiplayer or offline loader execution is claimed. Dated evidence files were preserved; guide content hashes were preserved across relocation. New knowledge follows [maintenance](../maintenance.md) directly.

Nine historical patched XML outputs already contained mixed line endings. Their exact bytes are preserved rather than normalizing old evidence. The read-only checker accepts only the original hashes listed in [format exceptions](history/format-exceptions.json); changed files do not inherit that exception. New authored text uses CRLF.

## Attribution

Starter-derived setup/workflow, instructions, template prose and the radius audit originate with Serpens66 / Anno 1800 Modding Starter Kit, https://github.com/Serpens66/ModdingWithCodex, and were adapted here. Their prose license is [CC BY 4.0](licenses/starter-prose.md); imported executable scripts/tests/template code retain [MIT](licenses/starter-code.txt). These notices apply to imported material, not a new blanket license for this repository, other mods, upstreams or game resources.
