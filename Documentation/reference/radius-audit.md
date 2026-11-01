# Bounded scalar-edit validation example

Audit completed on 2026-10-04 before creating the example patch. Boundary: change one serialized normal-mode integer configuration field; no claim that every harbor placement restriction disappears.

- Full owner 2001241 has Template BuildingBaseTiles, no BaseAssetGUID, and one exact identity match in the complete source.
- Its complete template supplies Standard and BuildingBaseTiles. The owning definition declares HarbourConstructionAreaRadius as Integer, with no dataset reference or declared bound for this field. Relevant defaults supply render/street data, not a radius override.
- Explicit normal radius is 28, creative-mode radius is separately 56. No derived assets or other scalar references to owner 2001241 were found among complete asset records.
- Targeted native text searches located main/PC XML copies and no exposed Lua/config consumer. Absence of a textual consumer does not establish engine behavior. Main extracted files are the selected input; originating game build remains unknown.
- Existing icon/texture references and every other property are preserved. No new asset identity, localization or resource is introduced. Runtime placement, save and multiplayer implications remain unverified.
- Pinned 1800 XML lookup/merge implementation was reviewed; GUID starts at Asset and the path selects the serialized owning container.

After this audit the actual 1800 evaluator applied an authored merge changing radius 28 to 40 to the **full local assets database**. Output assertions confirmed one target, creative radius 56 and canonical preservation of all **96,102 full asset records**, after normalizing only the edited radius. No mod was installed or published.

| Local source identity | SHA-256 |
| --- | --- |
| assets.xml | `08b6cc7023aa1d834f2e6c2042848a3b3e2f13fcc44735a6248f6b6622d42c6a` |
| templates.xml | `099e887c72f97e3a443944e90d45ea544a3d83dd3dd440bf1e420ed709a187f8` |
| properties-toolone.xml | `bf8b81d19a54ab1e7086bc7d47e0239857335422cec6e299b527ef77d462593b` |
| properties.xml | `a9d10e0c450908ab8f7fb15d29852996a912eea536ccda7855f175cfd972c200` |

Evaluator SHA-256: `d977d9ad3ee1f2a446f3d62f5126e52811458552d4e8a63aefaa301fa51d751f`. Reviewed tool installation: Anno Modding Tools 2.3.1 / 1800 evaluator GU17.1. Local logs, audit and patched database remain in ignored work/out directories, not this distribution.

For a new user's feature, re-audit their current files before creating a patch. This example is evidence of a bounded offline check, not a general game/save/MP certification. Sources: [pinned implementation](https://github.com/jakobharder/anno-mod-loader/blob/8326b7c5a7648787c52f1252cd6e8ae60e593d1c/libs/xml-operations/src/xml_operations.cc), local source identities above, original workspace recipe research.
