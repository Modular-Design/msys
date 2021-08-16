from fastapi import APIRouter

class ExtensionRouter(APIRouter):
    def __init__(self,
                 module):
        super().__init__(prefix="/extensions", tags=["extensions"])
        self.extensions = []

        for e in self.extensions:
            self.include_router(e)