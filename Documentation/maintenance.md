# Maintain this one knowledge base

Documentation is the maintained source for all readers. There is no parallel portable edition and no transfer to ModdingWithCodex. The old [KIT register](reference/kit-transfer.md) is historical; keep its IDs, original scope, exclusions and exact commit receipts.

## Record a finding once

1. Identify the existing topic, current source revisions and the prior statement being corrected. Read coverage/discrepancies before treating an indexed source as reviewed. Follow the mandatory feature audit before deriving a game-dependent implementation.
2. Update the relevant chapter directly. Retain useful comments, existing evidence IDs and the original conditions/certainty of reported tests. A correction links its predecessor and explains the changed conclusion; do not erase historical receipts or silently refresh old hashes.
3. Add durable provenance: source identity, public file/commit/line when available, source date/version/hash, relevant finding, evidence category, audit scope and remaining limitations. Use the [finding record](templates/finding.md) as a checklist, not as a second copy of the chapter.
4. If the original evidence is local/private, give a self-contained factual summary in the chapter or [local evidence summaries](reference/local-evidence.md). Identify unavailable originals and distinguish author reports from independently repeated checks. Keep personal configuration, saves and complete native databases out of tracked files. A local file link alone is insufficient for external readers.
5. Update coverage, discrepancies and the index when their scope actually changes. Pending observations can be documented immediately with their uncertainty; documentation does not make them confirmed facts.
6. Run [read-only documentation checks](tools/README.md) and any additional checks justified by the change. Keep source review, structural checks, offline loader results and game/save/MP tests distinct. Commit/push only when authorized; a local edit becomes available to external chats only after GitHub publication.

## When the chat cannot write

Return the target chapter, an exact proposed replacement/addition, source links/identities, evidence status and unresolved questions. Do not claim the repository was updated. Findings from another user's extraction include that user's source versions and test conditions; they do not silently supersede a different build's evidence.

## Historical artifacts and current checks

Dated JSON inventories, hashes, validation receipts and adaptation records describe their original inputs. Absolute paths in them are provenance, not setup instructions. Tools resolve configured identities or explicit historical aliases at read time. Re-running a tool does not certify a changed source against an earlier receipt.

Write new research/check outputs under ignored outputPath and deliberately review any promotion into documentation. Old one-time chapter generators and reconciliation scripts retain historical logic: do not use them as an automatic refresh pipeline. [The consolidation record](reference/consolidation.md) accounts for prior starter-only material and outstanding KIT topics.
