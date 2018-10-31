def uni_to_hex_hash(uni):
    return ' '.join(map(lambda x: '#' + hex(x)[2:], uni))

def uni_to_hex_filename(uni):
    return '-'.join(map(lambda x: hex(x)[2:], uni))
