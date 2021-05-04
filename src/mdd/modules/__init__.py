from .math import Math


def get_modules():
    modules = {}

    # search in modules namespace
    # Problem of finding right classes!
    """
    import importlib
    import pkgutil
    def iter_namespace(ns_pkg):
        # Specifying the second argument (prefix) to iter_modules makes the
        # returned name an absolute name instead of a relative one. This allows
        # import_module to work without having to do additional modification to
        # the name.
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    import mdd.modules
    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in iter_namespace(mdd.modules)
    }
    # """

    # search in entry points
    from importlib.metadata import entry_points

    discovered_modules = entry_points()['mdd.modules']
    print(discovered_modules)


    for module in discovered_modules:
        modules[module.name] = module.load()

    return modules
