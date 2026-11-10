"""Search an Anno 1800 extraction without changing any source files."""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

from workspace_paths import configured_path, local_path


def asset_records(path):
    stack = []
    for event, node in ET.iterparse(path, events=("start", "end")):
        if event == "start":
            stack.append(node)
            continue
        if node.tag == "Asset" and node.find("Values/Standard/GUID") is not None:
            yield node
            stack[-2].remove(node)
        stack.pop()


def leaves(node, prefix=""):
    for child in node:
        if len(child):
            yield from leaves(child, prefix + child.tag + "/")
        elif child.text and child.text.strip():
            yield prefix + child.tag, child.text.strip()


def references(assets, matches):
    for asset in asset_records(assets / "assets.xml"):
        values = asset.find("Values")
        owner = values.findtext("Standard/GUID")
        name = values.findtext("Standard/Name") or ""
        for field, value in leaves(asset):
            if value in matches and field != "Values/Standard/GUID":
                yield value, "assets.xml", f"{owner} {name}", field

    for template in ET.parse(assets / "templates.xml").iter("Template"):
        props = template.find("Properties")
        if props is not None:
            for field, value in leaves(props, "Properties/"):
                if value in matches:
                    yield value, "templates.xml", template.findtext("Name", ""), field

    defaults = ET.parse(assets / "properties.xml").getroot()
    for field, value in leaves(defaults):
        if value in matches:
            yield value, "properties.xml", "", field


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    query = parser.add_mutually_exclusive_group(required=True)
    query.add_argument("--guid", help="exact InfoTipData/Guid")
    query.add_argument("--text-guid", help="exact TextGUID anywhere in the layout")
    query.add_argument("--query", help="substring of asset name or localized layout text")
    query.add_argument("--contains", help="substring of a serialized layout value, e.g. a Condition")
    parser.add_argument("--export", help="decoded XML override (default: vanillaPath/export.xml)")
    parser.add_argument("--language", default="english", help="suffix of texts_<language>.xml")
    parser.add_argument("--references", action="store_true", help="list exact numeric matches in asset fields, templates and defaults")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-zA-Z_]+", args.language):
        parser.error("--language must be a language suffix, such as german")
    for value in (args.guid, args.text_guid):
        if value is not None and not re.fullmatch(r"[0-9]+", value):
            parser.error("GUIDs must be decimal numbers")

    vanilla = configured_path("vanillaPath")
    assets = vanilla / "data/config/export/main/asset"
    export = local_path(args.export) if args.export else vanilla / "export.xml"
    root = ET.parse(export).getroot()
    if root.tag != "Content" or not root.findall("InfoTipData"):
        parser.error(f"{export} is not a decoded Anno 1800 infotip export")
    tips = {tip.findtext("Guid"): tip for tip in root.findall("InfoTipData")}
    includes = {
        guid: list(dict.fromkeys(n.text for n in tip.iter("TemplateGUID") if n.text))
        for guid, tip in tips.items()
    }
    included_by = defaultdict(list)
    for guid, dependencies in includes.items():
        for dependency in dependencies:
            included_by[dependency].append(guid)

    labels = {}
    texts = vanilla / "data/config/gui" / f"texts_{args.language}.xml"
    for row in ET.parse(texts).findall("./Texts/Text"):
        labels[row.findtext("GUID")] = row.findtext("Text", "")

    names = {}
    for asset in asset_records(assets / "assets.xml"):
        guid = asset.findtext("Values/Standard/GUID")
        if guid in tips:
            names[guid] = (asset.findtext("Values/Standard/Name", ""), asset.findtext("Template", ""))

    matched = set()
    for guid, tip in tips.items():
        name, template = names.get(guid, ("", ""))
        text_ids = list(dict.fromkeys(n.text for n in tip.iter("TextGUID") if n.text))
        localized = [(key, labels.get(key, "")) for key in text_ids]
        fields = list(leaves(tip))
        inline_text = [
            value for path, value in fields
            if path.endswith(("/Text/Text", "/HeadlineText", "/SublineText", "/ValueText"))
        ]
        if args.guid is not None and args.guid != guid:
            continue
        if args.text_guid is not None and args.text_guid not in text_ids:
            continue
        if args.query is not None and not any(
            args.query.casefold() in value.casefold()
            for value in [name, *inline_text, *(label for _, label in localized)]
        ):
            continue
        if args.contains is not None and not any(
            args.contains.casefold() in value.casefold() for _, value in fields
        ):
            continue
        matched.add(guid)
        kind = "layout template" if tip.findtext("IsTemplate") == "True" else "infotip"
        print(f"{guid}  {kind}  {name or '(no matching asset definition)'}  {template}")
        for key, label in localized:
            if args.text_guid is not None and key != args.text_guid:
                continue
            print(f"  TextGUID {key}: {' '.join(label.split()) or '(no localized text found)'}")
        if args.contains is not None:
            for field, value in fields:
                if args.contains.casefold() in value.casefold():
                    print(f"  {field}: {value}")
        for key in includes[guid]:
            print(f"  includes layout template {key}")
        parents = included_by[guid]
        if parents:
            print(f"  included by: {', '.join(parents)}")

    if args.references and matched:
        print("Exact numeric matches (verify field semantics and effective inheritance):")
        for guid, source, owner, field in references(assets, matched):
            print(f"  {guid}  {source}  {owner}  {field}")
    if not matched:
        print("No matching layout. Check the language, extraction, and UI/asset references.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ET.ParseError) as error:
        sys.exit(str(error))
