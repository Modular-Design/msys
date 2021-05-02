def get_processors():
    from importlib.metadata import entry_points

    discovered_modules = entry_points()['mdd.processors']
    print(discovered_modules)
    modules = {}
    for module in discovered_modules:
        modules[module.name] = module.load()

    return modules