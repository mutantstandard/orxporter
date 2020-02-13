import os
import pathlib
import re

from exception import FilterException
import util
import log

def format_resolve(code, emoji, format):
    """
    Takes an instance of %whatever in a file path, and returns the actual intended value.
    """

    # %(param)
    if code[0] == '(':
        inside = code[1:-1]
        if inside not in emoji:
            raise ValueError('Missing property: ' + inside)
        return emoji[inside]

    # (%c) colormap
    if code == 'c':
        if 'color' not in emoji:
            raise ValueError('Cannot resolve %c - no colormap')
        return emoji['color']

    # (%d) replicating the directory structure to the image file as given in the input folder.
    if code == 'd':
        if 'src' not in emoji:
            raise ValueError('Cannot resolve %d - no emoji source file defined')
        return str(pathlib.Path(emoji['src']).parent)




    # (%f) export format (png-64, webp-128, etc.)
    if code == 'f':
        return format

    # (%z) export size (64, 128, 512, etc.)
    # will return 0 (as a string) if it's SVG.
    if code == 'z':
        if format.split("-")[0] in ["svg", "svgo"]: # if there's no size...
            return "0"
        else:
            return format.split("-")[1]

    # (%i) image format, without size (png, webp, avif, etc.)
    if code == 'i':
        return format.split("-")[0]




    # (%s) the emoji's shortcode
    if code == 's':
        if 'short' not in emoji:
            raise ValueError('Cannot resolve %s - no shortcode')
        return emoji['short']

    # (%u) the emoji's unicode codepoint
    if code == 'u':
        if 'code' not in emoji:
            raise ValueError('Cannot resolve %u - no unicode codepoint defined')
        if '!' in emoji['code']:
            raise FilterException('Cannot resolve %u (unicode codepoint is explicitly undefined )')
        return util.uni_to_hex_filename(emoji['code'])


    raise ValueError('Cannot resolve format code: ' + code)



def format_path(path, emoji, format):
    """
    Takes the requested output format and creates
    an actual usable path with it.
    """

    res = path

    # add file extensions to the path
    # (also acts as a format check)
    if format == 'svg':
        res = res + '.svg'
    elif format == 'svgo':
        res = res + '.svg'
    elif format.startswith('png-'):
        res = res + '.png'
    elif format.startswith('pngc-'):
        res = res + '.png'
    elif format.startswith('flif-'):
        res = res + '.flif'
    elif format.startswith('webp-'):
        res = res + '.webp'
    elif format.startswith('avif-'):
        res = res + '.avif'
    else:
        raise ValueError('Invalid export format: ' + FilterException)

    # - catch instances of % in the output file path
    # - uses format_resolve() to figure out what it is
    # - replaces what it found
    for match, fcode in set(re.findall(r'(%(\(.*\)|.))', res)):
        repl = format_resolve(fcode, emoji, format)
        res = res.replace(match, repl)

    return res

def make_dir_structure_for_file(path):
    try:
        dirname = os.path.dirname(path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
    except IOError:
        raise Exception('Could not create directory: ' + dirname)
