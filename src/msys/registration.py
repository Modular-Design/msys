def get_registered(entry_name: str):
    registered = {}

    # search in entry points
    import sys
    if sys.version_info < (3, 8):
        from importlib_metadata import entry_points
    else:
        from importlib.metadata import entry_points

    entrypoints = entry_points()
    if not entry_name in entrypoints.keys():
        return None

    for entry in entrypoints[entry_name]:
        registered[entry.name] = entry.load()

    return registered

def get_modules():
    return get_registered('msys.modules')

def get_types():
    return get_registered('msys.types')

def get_extensions():
    return get_registered('msys.extensions')