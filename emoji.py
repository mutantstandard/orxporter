def match(emoji, export_filter):
    for k, v in export_filter:
        if k not in emoji:
            if '!' not in v:
                return False
        elif '*' not in v and emoji.get(k) not in v:
            return False
    return True
