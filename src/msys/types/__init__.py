def get_types():
    types = {}

    # search in entry points
    import sys
    if sys.version_info < (3, 8):
        from importlib_metadata import entry_points
    else:
        from importlib.metadata import entry_points

    discovered_types = entry_points()['msys.types']

    for type in discovered_types:
        types[type.name] = type.load()

    return types
