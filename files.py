import os

def try_write(data, out_path, obj_name):
    """
    Tries to write a file out. Creates an exception if it fails.

    'obj_name' is a name to give the thing you're trying to export so that
    if it fails, the error message that's given is more specific.
    """

    try:
        f = open(out_path, 'w')
        f.write(data)
        f.close()

    except IOError as e:
        raise Exception(f"Could not write {obj_name} to path '{out_path}'. More info: {e}")
