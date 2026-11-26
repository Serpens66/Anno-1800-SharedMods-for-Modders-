# Anno Mod-Corner research for Anno 1800

- [Graphics](graphics.md) covers models, textures, materials, animation and graphical resources.
- [Code and XML](code-and-xml.md) covers asset patching, scripting and gameplay-related investigation.

Use the [topic index](../README.md) for maintained instructions. This section records selected useful results from community discussions, source comparisons and open questions. Each case identifies its evidence. A **community report** is an account from the discussion with its stated test conditions. **Pending** marks a claim that needs independent confirmation. **Vanilla data** describes the inspected asset or file structure. **Tool source** describes the pinned tool implementation. Game, save and multiplayer behavior each require their own evidence.

## Export scope

| Channel | HTML files | Unique message IDs | UTC date range | Local replies resolved |
| --- | ---: | ---: | --- | ---: |
| [#graphics](https://discord.com/channels/578443209940926465/1080167315452203040) | 3 | 11,654 | 2023-02-28 to 2026-11-26 | 2,460 |
| [#1800-code](https://discord.com/channels/578443209940926465/578443576552325143) | 21 | 103,642 | 2019-05-16 to 2026-11-24 | 17,873 |

The corpus pass compared HTML message-container IDs with parsed records on every page, then indexed text, code blocks, reply pointers, URLs and attachment references. Links from Graphics resolved to 13 distinct exported Code messages. Links from Code resolved to 11 distinct exported Graphics messages. Technical selection combines topic searches across all 24 pages with contextual reading of relevant threads, replies and selected attachments. See the [coverage ledger](../reference/coverage.md#discord-community-research-2026-11-26) for the review boundaries. Discord permalinks may require server membership. The local exports and all source copies used in this review are separate from the knowledge base.

## PC game and tool dates

| Release | Why it matters when reading older advice |
| --- | --- |
| [GU17, 2023-04-04](https://www.anno-union.com/updates/anno-1800-pc-game-update-17/) | Ubisoft confirmed the integrated PC loader shipped in April 2023. Instructions for the external loader's replacement Python DLLs belong to the earlier workflow. [Ubisoft's follow-up](https://www.anno-union.com/union-update-news-patch-plans-and-a-community-spotlight/) |
| [GU17.1, 2023-05-23](https://www.anno-union.com/updates/anno-1800-pc-game-update-17-1/) | Fixed high memory usage while loading with mods and a case where zoo animals and other feedback units failed to spawn after a save load. The [existing offline evaluator receipts](../reference/offline-validation.md) identify the GU17.1 test executable used there. |
| [GU18, 2023-08-22](https://www.anno-union.com/updates/anno-1800-pc-game-update-18/) | Added the mod.io browser and documented extending mod-presence conditions to any patch. |
| [GU18.1, 2023-11-14](https://www.anno-union.com/updates/anno-1800-pc-game-update-18-1/) | Fixed the loader's failure to follow load order for identical files. Inspect the relevant files, loading phase and build before reusing reports of this symptom. |
| [GU18.2, 2024-05-14](https://www.anno-union.com/updates/anno-1800-pc-game-update-18-2/) | Added modding support for shaders and sound banks. |
| [GU18.3, 2024-09-19](https://www.anno-union.com/updates/anno-1800-pc-game-update-18-3/) | Fixed a regression affecting ambient-setting mods and a startup mod-initialization issue. |
| [GU18.4, 2024-12-05](https://www.anno-union.com/updates/anno-1800-pc-game-update-18-4/) | Latest officially documented Anno 1800 PC game update located as of 2026-11-26. Its graphics fix concerns a specific DLC asset at low and medium settings. Ubisoft subsequently described the end of the post-launch phase. [Ubisoft's December retrospective](https://www.anno-union.com/union-update-the-anno-1800-saga/) |

Compare these dates with the affected feature. A message may cite an older build, and Blender, converters and the editor extension can change independently of the game. In mixed threads, check the game named by the participants, the resources involved and the exact tool branch. Anno 117 had a [public PC demo from 2025-09-02](https://www.anno-union.com/everything-to-know-about-the-anno-117-pax-romana-demo/) and [launched on 2025-11-13](https://www.anno-union.com/games/anno-117-pax-romana/). Earlier dates can therefore still refer to Anno 117. Treat ambiguous cases as pending until Anno 1800 support is established independently.

## Historical texture reference

Judekw's eight-page *ANNO Texture 101* (2019-12-30, p. 7 for Anno 1800 and 2205, SHA-256 `ebc0c695446b4afe6f29ef03f5edc5314c17722bde645986e3501c5896106cb9`) reports gloss in normal-map alpha, reflectivity and reflection tint in metal-map RGB, ambient occlusion in metal-map alpha and player-color coverage in a grayscale dye mask. It expressly presents the proposed timing of the colored day/night window mask as untested. Treat channel meanings as historical author evidence for the materials described there. The section about Judekw's mod for Anno 2070 describes that mod's own pipeline. Original attachment available in the local export. [2019 attachment post](https://discord.com/channels/578443209940926465/578443576552325143/661336817617993744)
