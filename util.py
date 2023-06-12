def uni_to_hex_hash(uni):
    return ' '.join(map(lambda x: '#' + hex(x)[2:], uni))

def uni_to_hex_filename(uni):
    return '-'.join(map(lambda x: hex(x)[2:], uni))

def get_color_palettes(emoji, manifest):
    """Get the source and destination colour palettes for the given emoji."""
    if 'color' not in emoji:
        return None

    cmap = manifest.colormaps[emoji['color']]
    pfrom = manifest.palettes[cmap['src']]
    pto = manifest.palettes[cmap['dst']]

    return (pfrom, pto)

"""Mapping of the license type, keyed by export format."""
_license_format_map = {
    'svg': 'svg',
    'png': 'exif',
    'pngc': 'exif',
}

def get_license_type_for_format(f):
    """Gets the license type for a given export format, or None if not set."""

    return _license_format_map.get(f.split('-')[0])

def get_formats_for_license_type(t):
    """Get the export formats for a given license type."""
    return tuple(f for f, ft in _license_format_map.items() if ft == t)
