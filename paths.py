import pathlib
import re

from exception import FilterException
import util

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

    # (%f) export format (png, webp, jpx, etc.)
    if code == 'f':
        return format

    # (%s) the emoji's shortcode
    if code == 's':
        if 'code' not in emoji:
            raise ValueError('Cannot resolve %s - no shortcode')
        return emoji['code']

    # (%u) the emoji's unicode codepoint
    if code == 'u':
        if 'unicode' not in emoji:
            raise ValueError('Cannot resolve %u - no unicode codepoint defined')
        if '!' in emoji['unicode']:
            raise FilterException('Cannot resolve %u (unicode codepoint is explicitly undefined )')
        return util.uni_to_hex_filename(emoji['unicode'])

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
    elif format.startswith('png-'):
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
        repl = format_resolve(fcode, emoji, FilterException)
        res = res.replace(match, repl)

    return res
