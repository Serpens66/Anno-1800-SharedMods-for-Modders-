"""Extract exact vanilla contracts. Extraction alone does not establish runtime behavior."""
from pathlib import Path
import hashlib
import json
import re
from lxml import etree as ET
from inventory import VANILLA, OUT, write_json

ASSET_DIR = VANILLA / "data/config/export/main/asset"
TARGETS = {"5244", "2001241", "100780", "1010372", "120055", "120057", "193666", "119965", "191455", "2001271", "500094", "1010516", "1010560", "100939", "101507", "101508"}
TEMPLATES = {"Skin", "FactoryBuilding7", "Product", "AssetPool", "ItemEffectTargetPool", "PlayerCounterContextPool", "FeatureUnlock", "Trigger", "Quest", "QuestPool", "ActionExecuteScript", "ConditionActiveSession", "ConditionUnlockNeeded", "ActionSpawnObject", "ConditionEvent", "ConditionTimer", "RewardPool", "Ship"}
PROPERTIES = {"Standard", "Skin", "Text", "Locked", "Unlockable", "VectorElement", "InheritanceMapV2", "FactoryBase", "Factory7", "Product", "Maintenance", "ConstructionCategory", "Building", "BuildingBaseTiles", "ActionExecuteScript", "ActionSpawnObject", "ConditionActiveSession", "ConditionUnlockNeeded", "ConditionEvent", "ConditionPropsNegatable", "Trigger", "TriggerSetup", "FeatureUnlock", "Quest", "QuestPool", "Nameable", "AssetPool", "ItemEffectTargetPool", "PlayerCounterContextPool", "KeyBindings"}

def xml(node):
    return ET.tostring(node, encoding="unicode", pretty_print=True)

def source(path):
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def main():
    records, asset_summary = {}, []
    representative = set()
    # End-of-Asset traversal retains inline auto-created assets until their owning asset is handled.
    for _, node in ET.iterparse(str(ASSET_DIR / "assets.xml"), events=("end",), tag="Asset", huge_tree=True):
        guid = node.findtext("Values/Standard/GUID")
        if guid:
            templ = node.findtext("Template")
            base = node.findtext("BaseAssetGUID")
            values = node.find("Values")
            props = [x.tag for x in values if isinstance(x.tag, str)] if values is not None else []
            record = {"guid": guid, "name": node.findtext("Values/Standard/Name"), "template": templ,
                      "base": base, "line": node.sourceline, "properties": props}
            asset_summary.append(record)
            records[guid] = record
            if guid in TARGETS or templ in TEMPLATES and templ not in representative:
                record["xml"] = xml(node)
                representative.add(templ)
            if base:
                # Preserve every base asset node so target chains can be resolved without assumptions.
                record["base_candidate_xml"] = xml(node)
            node.clear()
            while node.getprevious() is not None:
                del node.getparent()[0]
    template_tree = ET.parse(str(ASSET_DIR / "templates.xml"), ET.XMLParser(huge_tree=True))
    templates = {n.findtext("Name"): n for n in template_tree.xpath("//Template[Name]")}
    property_tree = ET.parse(str(ASSET_DIR / "properties-toolone.xml"), ET.XMLParser(huge_tree=True))
    properties = {n.findtext("Name"): n for n in property_tree.xpath("//Property[Name]")}
    chosen = {k: v for k, v in records.items() if "xml" in v}
    pending = list(chosen)
    missing = []
    while pending:
        current = chosen[pending.pop()]
        base = current["base"]
        if base and base not in chosen:
            if base not in records:
                missing.append(base)
            else:
                # The base may be a template-root asset not captured as a base candidate.
                chosen[base] = records[base]
                pending.append(base)
    need_xml = {k for k, v in chosen.items() if "xml" not in v}
    if need_xml:
        for _, node in ET.iterparse(str(ASSET_DIR / "assets.xml"), events=("end",), tag="Asset", huge_tree=True):
            guid = node.findtext("Values/Standard/GUID")
            if guid in need_xml:
                chosen[guid]["xml"] = xml(node)
            if guid:
                node.clear()
                while node.getprevious() is not None:
                    del node.getparent()[0]
    for v in chosen.values():
        v.pop("base_candidate_xml", None)
    used_templates = TEMPLATES | {v["template"] for v in chosen.values() if v["template"]}
    used_properties = PROPERTIES | {p for v in chosen.values() for p in v["properties"]}
    for name in used_templates:
        if name in templates:
            used_properties.update(x.tag for x in templates[name].find("Properties") if isinstance(x.tag, str))
    default_tree = ET.parse(str(ASSET_DIR / "properties.xml"), ET.XMLParser(huge_tree=True))
    dataset_tree = ET.parse(str(ASSET_DIR / "datasets.xml"), ET.XMLParser(huge_tree=True))
    datasets = {}
    for node in dataset_tree.xpath("//DataSet[Name]"):
        name = node.findtext("Name")
        if name in {"ParticipantID", "CounterScope", "CounterValueType", "PlayerCounter", "SimpleEventType", "LockScope", "FeedbackSequenceType"}:
            datasets[name] = {"line": node.sourceline, "items": [{"position": i, "name": n.findtext("Name"), "id": n.findtext("Id")} for i, n in enumerate(node.findall("Items/Item"))]}
    defaults = {}
    for name in used_properties:
        nodes = default_tree.xpath("//DefaultValues/" + name)
        if nodes:
            defaults[name] = [{"line": n.sourceline, "xml": xml(n)} for n in nodes]
    structure_nodes = property_tree.xpath("//*[Name='VectorElement' or Name='InheritanceMapV2']")
    export_path = VANILLA / "export.xml"
    export_tree = ET.parse(str(export_path), ET.XMLParser(huge_tree=True))
    info_examples = {}
    for guid in ["373", "500934"]:
        found = export_tree.xpath("//InfoTipData[Guid='" + guid + "']")
        if found:
            info_examples[guid] = {"line": found[0].sourceline, "xml": xml(found[0])}
    text_path = VANILLA / "data/config/gui/texts_english.xml"
    text_tree = ET.parse(str(text_path), ET.XMLParser(huge_tree=True))
    texts = {}
    for guid in ["5244", "5246", "5247", "5753", "23861"]:
        found = text_tree.xpath("/TextExport/Texts/Text[GUID='" + guid + "']")
        if found:
            texts[guid] = {"line": found[0].sourceline, "xml": xml(found[0])}
    result = {"status": "extracted; feature-specific interpretation and reference review required",
              "sources": [source(ASSET_DIR / n) for n in ["assets.xml", "templates.xml", "properties-toolone.xml", "datasets.xml", "properties.xml"]],
              "assets": chosen, "templates": {k: {"line": templates[k].sourceline, "xml": xml(templates[k])} for k in sorted(used_templates) if k in templates},
              "properties": {k: {"line": properties[k].sourceline, "xml": xml(properties[k])} for k in sorted(used_properties) if k in properties},
              "structures": [{"line": n.sourceline, "xml": xml(n)} for n in structure_nodes],
              "defaults": defaults, "datasets": datasets, "infotips": info_examples, "texts": texts,
              "additional_sources": [source(export_path), source(text_path)], "missing_bases": missing}
    write_json(OUT / "vanilla-contracts.json", result)
    # A compact GUID index supports traceable searches without copying all proprietary game assets.
    write_json(OUT / "vanilla-asset-index.json", [{k: v for k, v in r.items() if k not in {"xml", "base_candidate_xml"}} for r in asset_summary])
    print(json.dumps({"assets_indexed": len(asset_summary), "assets_extracted": len(chosen), "templates": len(result["templates"]), "properties": len(result["properties"]), "missing_bases": missing}))

if __name__ == "__main__":
    main()
