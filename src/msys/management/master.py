from fastapi import FastAPI, Body, Header
from ..core import Registration
from .factory import Factory
from typing import Optional

class Master(FastAPI):
    def __init__(self):
        super().__init__()
        self.registration = Registration()
        self.factory = Factory(self.registration)
        self.include_router(self.factory)

        @self.get("/resources")
        async def get_resources(host: Optional[str] = Header(None)):
            res = dict()
            resources = self.registration.get_registered()
            for key in resources.keys():
                own = dict()
                resource = resources[key]

                if "name" in resource.keys():
                    own["name"] = resource["name"]

                if "description" in resource.keys():
                    own["description"] = resource["description"]

                if "config" in resource.keys() or "location" in resource.keys():
                    own["remote"] = host + "/" + key
                elif "remote" in resource.keys():
                    own["remote"] = resource["remote"]

                res[key] = own
            return res

        @self.get("/{id}/config")
        async def get_config(
                id:str,
                ):
            print("[Master]: ID: " + id)
            node = self.registration.launch(rid=id)
            print("[Master]: Node: " + str(node))
            return node.to_dict()

        @self.post("/{id}/config")
        def change_config(
                id: str,
                body=Body(
                    ...,
                )):
            node = self.registration.launch(id)
            node.load(body)
            return node.to_dict()

        @self.put("/{id}/update")
        def update_config(
                id: str,
                body=Body(
                    ...,
                )):
            node = self.registration.launch(id)
            node.load(body)
            node.update()
            return node.to_dict()


