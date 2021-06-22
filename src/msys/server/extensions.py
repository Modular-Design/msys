from fastapi import APIRouter, Body

def load_entrypoints(entry_name: str):
    # search in entry points
    import sys
    if sys.version_info < (3, 8):
        from importlib_metadata import entry_points
    else:
        from importlib.metadata import entry_points

    entrypoints = entry_points()
    if not entry_name in entrypoints.keys():
        return []
    return entrypoints[entry_name]

class Extensions(APIRouter):
    def __init__(self):
        super().__init__(prefix="/extensions", tags=["extensions"])
        self.extensions = []
        self.register_extensions()

        @self.get("")
        async def lists():
            """lists alls extensions"""
            return self.extensions

        @self.get("/update")
        async def update():
            """lists alls extensions"""
            self.register_extensions()
            return self.extensions

    def register_extensions(self):
        entries = load_entrypoints("msys.extensions")
        for entry in entries:
            eclass = entry.load()
            if eclass not in self.extensions:
                self.extensions.append(eclass)
                self.include_router(eclass())

