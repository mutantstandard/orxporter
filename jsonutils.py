import json

import log

def write_emoji(emoji, json_out):
    log.out('Converting to JSON...', indent=4)
    j = json.dumps(emoji, sort_keys=True, indent=4)
    log.out('Exporting to file: ' + json_out, indent=4)
    f = open(json_out, 'w')
    f.write(j)
    f.close()

def write_web(emoji, web_out):
    cats = {}
    roots = {}
    out = {'cats': cats, 'roots': roots}
    log.out('Exporting metadata for MutStd website...', 36)
    log.out('Processing emoji...', indent=4)
    for e in emoji:
        if 'root' not in e:
            raise ValueError('no root defined for emoji: ' +str(e))
        if 'cat' not in e:
            raise ValueError('no category defined for emoji: ' + str(e))
        if e['cat'] not in cats:
            cats[e['cat']] = []
        if e['root'] not in cats[e['cat']]:
            cats[e['cat']].append(e['root'])
            roots[e['root']] = None
        if 'morph' in e or 'color' in e:
            morph = e.get('morph', '')
            color = e.get('color', '')
            suffix = morph + '_' + color if morph and color else morph + color
            if roots[e['root']] is None:
                roots[e['root']] = []
            roots[e['root']].append(suffix)
    log.out('Converting to JSON...', indent=4)
    j = json.dumps(out, sort_keys=True, indent=4)
    log.out('Exporting to file: ' + web_out, indent=4)
    f = open(web_out, 'w')
    f.write(j)
    f.close()
