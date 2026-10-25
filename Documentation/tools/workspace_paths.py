"""Current workspace locations and read-time resolution of historical source paths."""
from pathlib import Path

DOC = Path(__file__).resolve().parents[1]
REPOSITORY = DOC.parent
ROOT = REPOSITORY.parent
LEGACY_SHARED = 'Anno-1800-SharedMods (for Modders)'


def source_path(value):
    """Locate a source after the move without rewriting its dated evidence record."""
    value = str(value)
    if value.startswith('workspace:'):
        value = value[len('workspace:'):]
    path = Path(value)
    if path.is_absolute():
        try:
            relative = path.relative_to(ROOT)
        except ValueError:
            return path
    else:
        relative = path
    parts = relative.parts
    if not parts:
        return ROOT
    if parts[0] == LEGACY_SHARED:
        return REPOSITORY.joinpath(*parts[1:])
    if parts[0] in {'Documentation', 'Trigger_Guide.md', 'Guide_RewardPools.md'}:
        return REPOSITORY / relative
    return ROOT / relative


def current_source_id(value):
    """Match newly inventoried paths with preserved review IDs in memory only."""
    prefix = 'workspace:'
    if not value.startswith(prefix):
        return value
    return prefix + source_path(value).relative_to(ROOT).as_posix()
