"""Build a read-only source inventory; scanning is not semantic review."""
from pathlib import Path
import hashlib
import json
import re
from collections import Counter

from workspace_paths import DOC, ROOT, current_source_id

OUT = DOC / "reference"
CACHE = Path(r"C:\Users\Serpens66\AppData\Local\Temp\anno1800-documentation-research-20261003")
VANILLA = Path(r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Anno1800 RDA unpacked\dataAlle")
TEXT_EXTENSIONS = {".xml", ".lua", ".md", ".txt", ".json", ".jsonc", ".cfg", ".ifo", ".fc", ".prp", ".sln", ".py", ".cs", ".csproj", ".rs", ".gltf", ".toml", ".yaml", ".bat", ".cmd", ".cf7", ".ts", ".ts_", ".js", ".xsd", ".fx", ".hlsl", ".glsl", ".ini", ".def", ".svg", ".csv", ".html", ".css", ".cmake", ".vcxproj", ".props", ".targets"}
BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".dds", ".rdm", ".rdp", ".island", ".isd", ".pdf", ".blend"}
TEXT_EXTENSIONS.update({".a7te", ".bfg", ".wwu", ".wproj", ".wsettings", ".obj"})
BINARY_EXTENSIONS.update({".a7t", ".a7tinfo", ".glb", ".xcf", ".pdn", ".blend1", ".zip", ".bnk", ".wav", ".wem"})
URL_PATTERN = r"https?://[^\s<>\"'\[\]()`]+"

def decode(raw):
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16"), "utf-16-bom"
    try:
        return raw.decode("utf-8-sig"), "utf-8-bom" if raw.startswith(b"\xef\xbb\xbf") else "utf-8"
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace"), "cp1252-fallback"

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + "\n").replace("\n", "\r\n").encode("utf-8"))

def main():
    groups = [("workspace", ROOT), ("guide", CACHE / "modding-guide"),
              ("loader1800", CACHE / "anno-mod-loader"), ("loader-current", CACHE / "loader-current"),
              ("FileDBReader", CACHE / "FileDBReader"), ("Modinfo", CACHE / "Modinfo"),
              ("GuidRanges", CACHE / "GuidRanges"), ("shared-resources", CACHE / "shared-resources"),
              ("rdm4", CACHE / "rdm4"), ("blender-addon", CACHE / "blender-addon"),
              ("Blender-Anno-1800", CACHE / "Blender-Anno-1800"),
              ("FileDBReader-wiki", CACHE / "FileDBReader-wiki-readable"),
              ("AddCustomMusic", CACHE / "AddCustomMusic"),
              ("iModYourAnno-wiki", CACHE / "iModYourAnno-wiki"),
              ("vscode-anno", CACHE / "vscode-anno")]
    rows, links, local_links, modcards, hashes = [], [], [], [], {}
    for group, base in groups:
        for path in sorted(base.rglob("*")):
            if not path.is_file() or any(x in {".git", "Documentation", "third_party", "node_modules"} for x in path.relative_to(base).parts):
                continue
            stamp = not path.suffix and any(x.lower() in {"stamps", "stamps single buildings"} for x in path.relative_to(base).parts)
            if path.suffix.lower() not in TEXT_EXTENSIONS | BINARY_EXTENSIONS | {".hpp", ".cxx", ".cc", ".h", ".cpp", ".yml", ".json_"} and path.name not in {"BUILD", "CMakeLists.txt", ".gitattributes", ".gitignore"} and not stamp:
                continue
            raw = path.read_bytes()
            binary = path.suffix.lower() in BINARY_EXTENSIONS or stamp
            text, encoding = ('', 'binary') if binary else decode(raw)
            rel = path.relative_to(base).as_posix()
            digest = hashlib.sha256(raw).hexdigest()
            key = group + ":" + rel
            row = {"id": key, "path": str(path), "relative_path": rel, "group": group,
                   "bytes": len(raw), "lines": len(text.splitlines()), "sha256": digest,
                   "encoding": encoding, "crlf": raw.count(b"\r\n"), "lf": raw.count(b"\n"),
                   "status": "inventoried; semantic review pending"}
            hashes.setdefault(digest, []).append(key)
            row["headings"] = re.findall(r"^#{1,6}\s+(.+)$", text, re.M)
            row["modop_types"] = dict(Counter(re.findall(r'<ModOp\b[^>]*\bType="([^"]+)"', text, re.I)))
            row["templates"] = sorted(set(re.findall(r"<Template>([^<]+)</Template>", text)))
            if path.suffix.lower() == ".lua":
                row["functions"] = re.findall(r"(?:local\s+)?function\s+([\w.:]+)\s*\(([^\n]*)\)", text)
                row["api_calls"] = sorted(set(re.findall(r"\b(?:ts|game|system|session|event|condition|console)\.[\w.]+", text)))
            for line, line_text in enumerate(text.splitlines(), 1):
                for url in re.findall(URL_PATTERN, line_text):
                    links.append({"source": key, "line": line, "url": url.rstrip(").,;]`")})
                for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', line_text):
                    target = target.strip().split(' "', 1)[0].strip('<>')
                    if not re.match(r'[a-zA-Z]+:', target) and not target.startswith('#'):
                        local_links.append({'source': key, 'line': line, 'target': target,
                                            'resolved_path': str(path.parent / target.split('#')[0])})
            rows.append(row)
            if group == "workspace" and path.name.lower() == "modinfo.json":
                modcards.append({"source": key, "folder": str(path.parent), "raw_metadata": text})
    for path in [Path(r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\HowTo.xml"),
                 Path(r"D:\CDesktopLink\Unterlagen\Mods\Anno 1800\Python Modding\info.txt")]:
        raw = path.read_bytes()
        text, encoding = decode(raw)
        rows.append({"id": "notes:" + path.name, "path": str(path), "sha256": hashlib.sha256(raw).hexdigest(),
                     "bytes": len(raw), "lines": len(text.splitlines()), "encoding": encoding,
                     "status": "inventoried; semantic review pending"})
        for line, line_text in enumerate(text.splitlines(), 1):
            for url in re.findall(URL_PATTERN, line_text):
                links.append({"source": "notes:" + path.name, "line": line, "url": url.rstrip(").,;]`")})
    # Preserve explicit human review outcomes only for unchanged content.
    ledger_path = OUT / 'review-ledger.json'
    ledger = json.loads(ledger_path.read_text('utf-8')) if ledger_path.exists() else {}
    # Keep historical review IDs intact when new inventory paths use SharedMods.
    indexed_ledger = {current_source_id(key): (key, value) for key, value in ledger.items()}
    for row in rows:
        review_key, review = indexed_ledger.get(row['id'], (row['id'], None))
        if review:
            row['status'] = review['status'] if review['sha256'] == row['sha256'] else 'changed since reviewed revision; re-review required'
            row['review_record'] = 'review-ledger.json#' + review_key
    write_json(OUT / "source-inventory.json", rows)
    write_json(OUT / "link-inventory.json", links)
    write_json(OUT / "local-link-inventory.json", local_links)
    write_json(OUT / "duplicate-groups.json", [v for v in hashes.values() if len(v) > 1])
    write_json(OUT / "mod-inventory.json", modcards)
    print(json.dumps({"sources": len(rows), "mods": len(modcards), "links": len(links),
                      "groups": dict(Counter(r.get("group", "notes") for r in rows))}))

if __name__ == "__main__":
    main()
