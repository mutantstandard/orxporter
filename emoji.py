

def match(emoji, export_filter):
    """
    Provides a match based on filters (provided through the flag -e).
    """
    for k, v in export_filter:
        if k not in emoji:
            if '!' not in v:
                return False
        elif '*' not in v and emoji.get(k) not in v:
            return False
    return True
