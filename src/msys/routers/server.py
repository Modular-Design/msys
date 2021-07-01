from fastapi import FastAPI
from typing import Optional
from ..core import Node, Metadata
from .nodes_router import NodesRouter
from .extension_router import ExtensionRouter
from .connectable_router import ConnectableRouter


class Server(FastAPI):
    def __init__(self,
                 blueprint):
        super().__init__()
        if type(blueprint) == type: # is class
            self.default = blueprint()
        else:
            self.default = blueprint


        title = self.default.meta.name
        if title:
            self.title = title


        description = self.default.meta.description
        if description:
            self.description = description

        if self.default.nodes is not None:
            self.extensions = ExtensionRouter(self.default)
            self.nodes = NodesRouter(self.default)
            self.inputs = ConnectableRouter(self.default, "inputs")
            self.outputs = ConnectableRouter(self.default, "outputs")

            self.include_router(self.extensions)
            self.include_router(self.nodes)
            self.include_router(self.inputs)
            self.include_router(self.outputs)

            @self.get("/structure", tags=["blueprint"])
            async def get_structure():
                """interacts with blueprint"""
                return self.default.update()

            @self.post("/structure", tags=["blueprint"])
            async def restructure(
                body=Body(
                    ...,
                )):
                """interacts with blueprint"""

                if not self.default.load(body):
                    return
                return self.default.to_dict()

        @self.get("/config")
        async def get_configuration():
            """runs on copy\n
            returns "outer"-layer
            """
            json = self.default.to_dict()
            if "nodes" in json.keys():
                json.pop("nodes")
            return json

        @self.post("/config")
        async def configure(
                body=Body(
                    ...,
                )):
            """runs on copy"""
            instance = self.default.__class__()
            instance.load(self.default.to_dict())
            if not instance.load(body):
                raise HTTPException(status_code=404, detail="Not Connectable")
            return instance.to_dict()

        @self.put("/update")
        async def update(
                body=Body(
                    ...,
                )):
            """runs on copy"""
            instance = self.default.__class__()
            instance.load(self.default.to_dict())
            if not instance.load(body):
                raise HTTPException(status_code=404, detail="Not Connectable")
            instance.update()
            return instance.to_dict()
