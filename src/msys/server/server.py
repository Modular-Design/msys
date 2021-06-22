from .websocket_manager import *
from .registration import *
from .extensions import *
from .resources import *

class MSYSServer(FastAPI):
    def __init__(self):
        super().__init__()
        self.registration = Registration()
        self.extensions = Extensions()
        self.resources = Resources()
        self.include_router(self.registration)
        self.include_router(self.extensions)
        self.include_router(self.resources)

        self.include_router(self.module_endpoints())
        self.include_router(self.connections_endpoints())
        self.include_router(self.input_endpoints())
        self.include_router(self.output_endpoints())

        self.childs = []

        @self.get("")
        async def status():
            pass



    def module_endpoints(self):
        modules = APIRouter(
            prefix="/modules",
            tags=["modules"],
        )

        @modules.get("")
        async def get():
            pass

        @modules.post("")
        async def add():
            pass

        @modules.put("")
        async def change():
            pass

        @modules.delete("")
        async def remove():
            pass

        return modules

    def connectable_endpoints(self, type:str):
        connectable = APIRouter(
            prefix="/"+type,
            tags=[type],
        )

        @connectable.get("")
        async def get():
            pass

        @connectable.post("")
        async def add():
            pass

        @connectable.put("")
        async def change():
            pass

        @connectable.delete("")
        async def remove():
            pass

        return connectable

    def connections_endpoints(self):
        connections = APIRouter(
            prefix="/connections",
            tags=["connections"],
        )
        @connections.get("")
        async def get():
            pass

        @connections.post("")
        async def add():
            pass

        @connections.delete("")
        async def remove():
            pass

        return connections

    def input_endpoints(self):
        return self.connectable_endpoints("inputs")

    def output_endpoints(self):
        return self.connectable_endpoints("ouputs")
