from fastapi import FastAPI
from typing import Optional
from ..core import Node, Metadata
from .nodes_router import NodesRouter
from .extension_router import ExtensionRouter
from .connectable_router import ConnectableRouter


class ModuleServer(FastAPI):
    def __init__(self,
                 module):
        super().__init__()
        self.module = module
        self.extensions = ExtensionRouter(self.module)
        self.nodes = NodesRouter(self.module)
        self.inputs = ConnectableRouter(self.module, "inputs")
        self.outputs = ConnectableRouter(self.module, "outputs")

        self.include_router(self.extensions)
        self.include_router(self.nodes)
        self.include_router(self.inputs)
        self.include_router(self.outputs)

        @self.put("/update")
        async def update():
            return self.module.update()

        @self.get("/inside")
        async def inside():
            return self.module.update()