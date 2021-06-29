from fastapi import APIRouter

class ConnectableRouter(APIRouter):
    def __init__(self,
                 module, type:str):
        super().__init__(prefix="/"+type, tags=[type])
