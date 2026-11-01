"""Resolve user-owned sources without changing dated provenance or downloading files."""
import json
import os
import re
from pathlib import Path

DOC = Path(__file__).resolve().parents[1]
REPOSITORY = DOC.parent
CONFIG_PATH = Path(os.environ.get('ANNO_DOCUMENTATION_CONFIG', DOC / 'local.json')).resolve()
LEGACY_SHARED = 'Anno-1800-SharedMods (for Modders)'


class ConfigurationError(SystemExit):
    """An inaccessible source is a prerequisite, not a game-code failure."""


def configuration():
    if not CONFIG_PATH.is_file():
        return {}
    try:
        value = json.loads(CONFIG_PATH.read_text('utf-8-sig'))
    except (ValueError, OSError) as error:
        raise ConfigurationError(f'Invalid configuration {CONFIG_PATH}: {error}') from error
    if not isinstance(value, dict) or type(value.get('configVersion')) is not int or value['configVersion'] != 1:
        raise ConfigurationError(f'{CONFIG_PATH}: configVersion must be integer 1; see setup.md.')
    for key in ('tools', 'sources', 'pathAliases'):
        item = value.get(key, {})
        if not isinstance(item, dict) or any(not isinstance(v, str) for v in item.values()):
            raise ConfigurationError(f'{CONFIG_PATH}: {key} must map names to path strings.')
    for key in ('gamePath', 'vanillaPath', 'modsPath', 'workPath', 'outputPath', 'workspacePath', 'researchPath'):
        if key in value and not isinstance(value[key], str):
            raise ConfigurationError(f'{CONFIG_PATH}: {key} must be a path string.')
    return value


CONFIG = configuration()


def local_path(value):
    path = Path(value)
    return path.resolve() if path.is_absolute() else (CONFIG_PATH.parent / path).resolve()


def configured_path(name, required=True):
    value = CONFIG
    for part in name.split('.', 1):
        value = value.get(part, {}) if isinstance(value, dict) else {}
    if not isinstance(value, str) or not value.strip():
        if not required:
            return None
        raise ConfigurationError(f'Missing {name} in {CONFIG_PATH}. Copy local.example.json to local.json and follow setup.md; provide your own sources/tools.')
    path = local_path(value)
    if required and not path.exists():
        raise ConfigurationError(f'{name} does not exist: {path}. Check local configuration; see setup.md.')
    if name == 'tools.xmltest' and path.name.lower() != 'xmltest.exe':
        raise ConfigurationError('Select Anno 1800 xmltest.exe, not xmltest2.exe; see setup.md.')
    return path


ROOT = configured_path('workspacePath', required=False) or DOC


def output_path(relative=''):
    """Keep fresh outputs away from maintained and native source files."""
    base = configured_path('outputPath', required=False) or DOC / 'out'
    protected = [(DOC, True)]
    protected += [(configured_path(k, required=False), False) for k in ('gamePath', 'vanillaPath', 'modsPath', 'researchPath', 'workPath')]
    protected += [(configured_path('workspacePath', required=False), True)]
    protected += [(local_path(v), True) for v in CONFIG.get('sources', {}).values() if v]
    for root, allow_documentation_output in protected:
        if root is None:
            continue
        if allow_documentation_output and base == DOC / 'out' and (root == DOC or DOC.is_relative_to(root)):
            continue
        if base == root or base.is_relative_to(root) or root.is_relative_to(base):
            raise ConfigurationError(f'outputPath overlaps maintained/source directory {root}; see setup.md.')
    result = (base / relative).resolve()
    if not result.is_relative_to(base.resolve()):
        raise ConfigurationError('Output must remain within configured outputPath.')
    return result


def source_roots():
    roots = {k: local_path(v) for k, v in CONFIG.get('sources', {}).items() if v}
    roots.setdefault('SharedMods', REPOSITORY)
    return roots


def source_path(value):
    """Resolve old identities at read time; never rewrite an old receipt."""
    raw = str(value).replace('\\', '/')
    if raw.startswith('workspace:'):
        raw = raw[len('workspace:'):]
    for old, new in sorted(CONFIG.get('pathAliases', {}).items(), key=lambda x: len(x[0]), reverse=True):
        prefix = old.replace('\\', '/').rstrip('/')
        if raw.casefold() == prefix.casefold() or raw.casefold().startswith(prefix.casefold() + '/'):
            return local_path(new).joinpath(raw[len(prefix):].lstrip('/'))
    path = Path(raw)
    if path.is_absolute() or re.match(r'^[a-z]:/', raw, re.I):
        try:
            raw = path.relative_to(ROOT).as_posix()
        except ValueError:
            parts = raw.split('/')
            if 'dataAlle' in parts:
                return configured_path('vanillaPath').joinpath(*parts[parts.index('dataAlle') + 1:])
            cache = next((i for i, p in enumerate(parts) if p.startswith('anno1800-documentation-research-')), None)
            if cache is not None:
                return configured_path('researchPath').joinpath(*parts[cache + 1:])
            if 'mods bei github' in parts:
                raw = '/'.join(parts[parts.index('mods bei github') + 1:])
            elif path.name in {'HowTo.xml', 'info.txt'}:
                return configured_path('sources.notes:' + path.name)
            elif path.exists():
                return path
            else:
                raise ConfigurationError(f'Unavailable historical source {value}; configure sources/pathAliases or provide the file (setup.md).')
    raw = raw.replace(LEGACY_SHARED + '/', 'SharedMods/', 1)
    if raw in {'Trigger_Guide.md', 'Guide_RewardPools.md'}:
        return DOC / raw
    if raw.startswith('Documentation/'):
        return DOC / raw[len('Documentation/'):]
    if raw.startswith('SharedMods/Documentation/'):
        return DOC / raw[len('SharedMods/Documentation/'):]
    if raw in {'SharedMods/Trigger_Guide.md', 'SharedMods/Guide_RewardPools.md'}:
        return DOC / raw.split('/', 1)[1]
    roots = source_roots()
    for name in sorted(roots, key=len, reverse=True):
        if raw == name or raw.startswith(name + '/'):
            return roots[name].joinpath(raw[len(name):].lstrip('/'))
    if raw.startswith('notes:'):
        return configured_path('sources.' + raw)
    if ROOT == DOC:
        raise ConfigurationError(f'Unconfigured source {raw}; set sources or workspacePath in {CONFIG_PATH} (setup.md).')
    return ROOT / raw


def source_relative(path):
    path = Path(path).resolve()
    if path.is_relative_to(DOC):
        return Path('SharedMods/Documentation') / path.relative_to(DOC)
    for name, root in source_roots().items():
        if path.is_relative_to(root):
            return Path(name) / path.relative_to(root)
    if path.is_relative_to(ROOT):
        return path.relative_to(ROOT)
    raise ConfigurationError(f'No source identity for {path}; configure a sources entry.')


def current_source_id(value):
    if not value.startswith('workspace:'):
        return value
    raw = value[len('workspace:'):]
    if raw.startswith(LEGACY_SHARED + '/'):
        raw = 'SharedMods/' + raw[len(LEGACY_SHARED) + 1:]
    elif raw.startswith('Documentation/'):
        raw = 'SharedMods/' + raw
    return 'workspace:' + raw
