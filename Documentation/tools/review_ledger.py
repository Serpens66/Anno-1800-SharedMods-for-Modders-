"""Apply explicit reviewed-source outcomes; do not infer review from scanning."""
from workspace_paths import current_source_id
from pathlib import Path
import json
from inventory import OUT, write_json

def main():
    rows = json.loads((OUT / 'source-inventory.json').read_text('utf-8'))
    ledger_path = OUT / 'review-ledger.json'
    ledger = json.loads(ledger_path.read_text('utf-8')) if ledger_path.exists() else {}
    def record(row, chapters, outcome, state='reviewed and documented'):
        ledger[row['id']] = {'sha256': row['sha256'], 'reviewed_on': '2026-10-03',
                             'status': state, 'documentation': chapters, 'outcome': outcome}
    guide = {
        'guides/Inheritance.md': ('foundations/inheritance.md', 'Scalar, vector and mixed inheritance; malformed example excluded.'),
        'documentation/infotips.md': ('ui-and-resources/infotips-and-text.md', 'Layout, typed literals, contexts, enum observations and compatibility; complex consumer audits remain feature-specific.'),
        'Scripting/textembeds.md': ('ui-and-resources/infotips-and-text.md', 'Textsource translation and restricted context, not arbitrary Lua execution.'),
        'Scripting/ExecutingScripts.md': ('lua/execution-and-lifecycle.md', '1800 script entry points and multiplayer multiplicity.'),
        'Scripting/ReadAfterWrite.md': ('lua/api-and-timing.md', 'Native writes are asynchronous; yield and reacquire.'),
        'Scripting/Lua_Probleme.md': ('lua/api-and-timing.md', 'Native C API/facade limits and invalid object behavior.'),
    }
    loader_files = {'xml_operations.cc': ('xml/modops.md', 'Complete operation, lookup, content, condition and recursive-merge implementation.'),
                    'mod_loading_order.cc': ('foundations/structure-and-loading.md', 'Dependencies, late phase and version selection.'),
                    'xml_filedb_reader.cc': ('ui-and-resources/infotips-and-text.md', 'Typed infotip serialization and existing count repair.'),
                    'parse_args.cc': ('reference/offline-validation.md', 'Separate CLI arguments; patch positional, -p prepatch.'),
                    'main.cc': ('reference/offline-validation.md', 'Only cmd/xmltest entry used; return status not enough for match validation.')}
    for row in rows:
        ident, rel = row['id'], row.get('relative_path', '')
        if row.get('group') == 'guide' and rel in guide:
            chapter, result = guide[rel]; record(row, [chapter], result)
        if row.get('group') == 'loader1800':
            if rel.startswith('tests/xml/'):
                record(row, ['reference/loader-history-and-tests.md', 'reference/validation/upstream-corpus/results.json'],
                       'Entire XML corpus read, including inputs, patches, includes, specifications, disabled experiment, runner and generator. 54 offline cases passed; six malformed fixtures and one CLI-context mismatch explicitly excluded from execution.')
            if rel.startswith('libs/external-file-loader/') and Path(rel).name in {'mod_manager.cc', 'external-file-loader.cc', 'mod.cc', 'cache.cc', 'cache.h', 'mod_manager.h', 'mod.h', 'fs.h', 'external-file-loader.h', 'BUILD'}:
                record(row, ['reference/loader-history-and-tests.md'],
                       'Complete historical implementation/header/build review; scanner, file dispatch, Python dependency and cache limits distinguished from integrated loader behavior.')
            if rel == 'libs/python35/src/python.cc':
                record(row, ['reference/loader-history-and-tests.md'], 'Full historical startup wrapper read: first intercepted call executes collected Python commands once per process; no modern Lua lifecycle inference.')
            name = Path(rel).name
            if name in loader_files and (name != 'main.cc' or rel == 'cmd/xmltest/src/main.cc'):
                chapter, result = loader_files[name]; record(row, [chapter], result)
            if rel.startswith('doc/') and rel.endswith('.md'):
                record(row, ['xml/modops.md', 'foundations/structure-and-loading.md', 'reference/discrepancies.md'],
                       'Full historical loader documentation read; distinguish release milestones, proposals and external Python integration.')
        if row.get('group') == 'loader-current' and rel.startswith('docs/') and rel.endswith('.md'):
            record(row, ['reference/discrepancies.md', 'xml/modops.md', 'foundations/structure-and-loading.md',
                         'ui-and-resources/infotips-and-text.md'],
                   'Full chapter read with game macros; 117-only features excluded; source-verified corrections and examples recorded.',
                   'read and reconciled; chapter-specific coverage cross-check pending')
        if ident.startswith('notes:'):
            record(row, ['lua/api-and-timing.md', 'lua/execution-and-lifecycle.md', 'multiplayer/synchronization.md',
                         'ui-and-resources/infotips-and-text.md', 'reference/discrepancies.md'],
                   'Entire file read in bounded chunks, including experiments and corrections. Q002 answered by Serp. Gameplay test outcomes still require complete topic transfer.',
                   'fully read; documentation transfer in progress')
        if current_source_id(ident) == 'workspace:SharedMods/shared_LuaLight/data/scripts_serp/lighttools.lua':
            record(row, ['lua/shared-light.md'], 'Full helper algorithm/interface review; catalog table indexed, native IDs still need full schema comparison. Defects explicitly documented.',
                   'implementation reviewed; integration audit in progress')
        if ident.endswith('WorkInProgress-Mods/shared_LuaMedium/data/scripts_serp/mediumtools.lua'):
            record(row, ['lua/shared-medium-and-ultra.md'], 'Public exports, synchronization channels, ownership transfer and WIP boundaries reviewed.',
                   'implementation reviewed; dependencies/integration audit in progress')
        if ident.endswith('WorkInProgress-Mods/shared_LuaUltra/data/scripts_serp/ultratools.lua') or ident.endswith('WorkInProgress-Mods/shared_LuaUltra/data/scripts_serp/savetablestuff.lua'):
            record(row, ['lua/shared-medium-and-ultra.md'], 'Startup and complete save script reviewed; cache receiver local-assignment defect identified.',
                   'implementation reviewed; peer/integration audit in progress')
    for row in rows:
        review = ledger.get(row['id'])
        if review:
            if review['sha256'] == row['sha256']:
                row['status'] = review['status']; row['review_record'] = 'review-ledger.json#' + row['id']
            else:
                row['status'] = 'changed since reviewed revision; re-review required'
    write_json(ledger_path, ledger)
    write_json(OUT / 'source-inventory.json', rows)
    print('Explicit source outcomes:', len(ledger))

if __name__ == '__main__':
    main()
