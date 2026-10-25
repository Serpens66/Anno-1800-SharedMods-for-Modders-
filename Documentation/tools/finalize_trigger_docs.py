"""Finish targeted trigger audit prose without changing existing text encodings."""
from pathlib import Path

DOC = Path(__file__).resolve().parents[1]


def replace(path, old, new):
    target = DOC/path
    raw = target.read_bytes()
    raw.decode('utf-8')
    def encoded(value):
        return value.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8')
    before, after = encoded(old), encoded(new)
    if after in raw:
        return
    if before in raw:
        assert raw.count(before) == 1, path
        target.write_bytes(raw.replace(before, after, 1))
    else:
        assert after in raw, (path, old)


def main():
    for path, old, new in [
        ('reference/trigger-audit.md', 'record seven complete XML recipes', 'record eight complete XML recipes'),
        ('reference/offline-validation.md', 'record seven complete recipe patches', 'record eight complete recipe patches'),
        ('reference/coverage.md', 'Seven complete documentation XML recipes', 'Eight complete documentation XML recipes'),
        ('tools/link_trigger_chapters.py', 'record seven complete recipe patches', 'record eight complete recipe patches'),
        ('tools/link_trigger_chapters.py', 'Seven complete documentation XML recipes', 'Eight complete documentation XML recipes'),
    ]:
        replace(path, old, new)
    replace('reference/trigger-audit.md',
        'The scan includes every applicable current source-inventory row in the workspace and both notebooks, not just the named examples.',
        'The scan includes every applicable current source-inventory row in the workspace and both notebooks, plus a live filesystem check for new supported source files. It is not limited to the named examples.')
    replace('reference/trigger-audit.md', '## Reconciled source families',
        'The sole standalone XML parse diagnostic is in `notes:HowTo.xml`: a double hyphen inside a notebook comment at line 29. The original notebook is retained as prose evidence, not treated as loadable mod XML, and has not been repaired. All other selected unique XML source groups parsed structurally; this does not execute includes, inheritance or gameplay.\n\n## Reconciled source families')
    target = DOC/'reference/trigger-audit.md'
    raw = target.read_bytes()
    if b'## Reproducing the documentation checks' not in raw:
        extra = '''
## Reproducing the documentation checks

Run the tools with the configured Python runtime and lxml available, from the workspace root:

1. `Documentation/tools/audit_triggers.py` captures native revisions and workspace evidence. Extraction does not certify semantic review.
2. `Documentation/tools/build_trigger_reference.py` and `Documentation/tools/build_trigger_examples.py` rebuild the condition lookup, datasets and complete examples.
3. `Documentation/tools/integrate_trigger_evidence.py` rebuilds original quotations/destinations and adds scoped records without replacing overall review outcomes.
4. `Documentation/tools/validate_triggers.py` checks native contracts and invokes the configured local 1800 XML evaluator. Its private GUID bindings are fixture values, not deployed mod allocations.
5. `Documentation/tools/validate_docs.py` checks file links/XML snippets and normalizes UTF-8 Documentation files to CRLF. `Documentation/tools/verify_trigger_documentation.py` checks linked heading fragments, source hash preservation and documentation encoding/line endings.

`link_trigger_chapters.py` and `finalize_trigger_docs.py` are idempotent integration helpers for the existing entry points/register prose. If source revisions change, repeat the relevant semantic audit and update the scoped prose/counts; regenerating JSON alone does not renew a review.
'''
        target.write_bytes(raw+extra.replace('\n', '\r\n').encode('utf-8'))


if __name__ == '__main__':
    main()
