class FilterException(Exception):
    """
    An exception that signals when an emoji has been filtered out of an export process.

    This also applies to implicit scenarios. ie. when the user is exporting a codepoint-named
    set and an emoji doesn't have a set codepoint.
    """
    def __init__(self, s=''):
        self.s = s

    def __str__(self):
        return self.s
