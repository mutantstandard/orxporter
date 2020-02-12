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
