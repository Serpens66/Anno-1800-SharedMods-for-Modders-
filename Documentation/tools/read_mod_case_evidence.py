"""Read captured evidence without changing files; compact output retains every scalar."""
import json
import sys
from lxml import etree as ET
from inspect_mod_trigger_cases import OUT

def summary(n, prefix=''):
    if not isinstance(n.tag, str):
        if n.text:
            print(prefix+' COMMENT '+n.text.strip())
        return
    if len(n) == 0:
        print(prefix+'/'+n.tag+'='+str(n.text or '')+(' '+str(dict(n.attrib)) if n.attrib else ''))
        return
    for i,c in enumerate(n):
        summary(c, prefix+'/'+n.tag+('['+str(i)+']' if n.tag in {'Item', 'SubTriggers','TriggerActions','Actions'} else ''))

def main():
    native = json.loads((OUT/'native.json').read_text('utf-8'))
    mode, names = sys.argv[1], sys.argv[2:]
    if mode == 'case':
        for name in names:
            print('\nCASE '+name)
            summary(ET.parse(str(OUT/(name+'.xml'))).getroot())
    elif mode in {'properties','templates','datasets'}:
        for name in names:
            print('\n'+name)
            print(json.dumps(native[mode][name], ensure_ascii=False, indent=2))
    elif mode == 'assets':
        for name in names:
            print('\nASSET '+name)
            summary(ET.fromstring(native['assets'][name]['xml'].encode('utf-8')))
    elif mode == 'assetpath':
        n = ET.fromstring(native['assets'][names[0]]['xml'].encode('utf-8'))
        for path in names[1:]:
            print('\n'+names[0]+':'+path)
            for child in n.xpath(path):
                summary(child)
    elif mode == 'modassets':
        integration = json.loads((OUT/'integration.json').read_text('utf-8'))
        seen = set()
        for asset in integration['definitions']:
            if asset['guid'] in names and asset['guid'] not in seen:
                print('\n'+asset['source']+':'+str(asset['line']))
                summary(ET.fromstring(asset['xml'].encode('utf-8')))
                seen.add(asset['guid'])

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
