def get_class_info(rclass):
    import re
    patern = r"<class '(.*?)'>"
    string = str(rclass)
    id, = re.findall(patern, string)
    res = id.split(".")
    if len(res) > 1:
        return dict(package=res[0], name=res[-1])
    else:
        return dict(package=[], name=res[0])

def set_class_info(rclass, info) -> bool:
    from msys.core.registrable import Registrable
    if not issubclass(rclass, Registrable):
        return False
    rclass.registered_name = info["name"]
    rclass.registered_package = info["package"]
    return True

def get_registered(entry_name: str):
    registered = []

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
        eclass= entry.load()
        info = get_class_info(eclass)
        if set_class_info(eclass, info):
            info["class"] = eclass
            registered.append(info)

    return registered

def get_modules():
    return get_registered('msys.modules')

def get_types():
    return get_registered('msys.types')

def get_extensions():
    return get_registered('msys.extensions')

def filter_package(package, entries) -> []:
    def fun(variable):
        return variable.get("package") == package
    return list(filter(fun, entries))

def filter_name(name, entries) -> []:
    def fun(variable):
        return variable.get("name") == name
    return list(filter(fun, entries))