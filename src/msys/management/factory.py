from fastapi import APIRouter, HTTPException, Body, WebSocket, WebSocketDisconnect
from typing import Optional, List
from .instance import Instance
from ..core import Module
import json


class Factory(APIRouter):
    def __init__(self, registration):
        super().__init__(prefix="/factory", tags=["factory"])
        self.registration = registration
        self.instances= dict()

        @self.get("/all")
        async def get_all_instances():
            return self.get_instances()

        @self.get("/active")
        async def get_active_instances():
            return self.get_instances(False)

        @self.get("/create")
        async def create_instance():
            id = self.create_instance()
            if not id:
                raise HTTPException(status_code=404, detail="Could not create instance!")
            return id

        @self.get("/create/{instance_id}")
        async def create_custom_instance(instance_id:str):
            id = self.create_instance(None, instance_id)
            if not id:
                raise HTTPException(status_code=404, detail="Could not create instance!")
            return id

        @self.get("/{instance_id}/open/{source}")
        async def create_new_instance_from(
                instance_id: str,
                source: str,
        ):
            id = self.create_instance(instance_id)
            if not id:
                raise HTTPException(status_code=404, detail="Source not found!")
            return id

        @self.get("/open/{source}")
        async def open_instance(
                source:str,
        ):
            id = self.create_instance(source, source)
            if not id:
                raise HTTPException(status_code=404, detail="Source not found!")
            return id

        @self.get("/{instance_id}/config")
        async def get_instance(instance: str):
            instance = self.instances.get(instance_id)
            if not instance:
                raise HTTPException(status_code=404, detail="Instance not found!")
            return instance.module.to_dict()

        @self.websocket("/{instance_id}/pubsub")
        async def websocket_endpoint(instance_id:str, websocket: WebSocket):
            # await websocket.accept()
            instance = self.instances.get(instance_id)
            if not instance:
                raise HTTPException(status_code=404, detail="Instance not found!")
            print("Connected")
            await instance.connect(websocket)
            try:
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                instance.disconnect(websocket)
                await instance.connections.broadcast(f"Client left the Projekt")
                print("DISCONNECTED")
                if instance.nof_connections() == 0:
                    self.save_instance(instance_id)
                    self.close_instance(instance_id)


        @self.put("/{instance_id}/config")
        async def change_instance(instance_id: str):
            pass

        @self.post("/{instance_id}/update")
        async def update_instance(instance_id: str):
            pass

        @self.get("/{instance_id}/save")
        async def save_instance(instance_id: str):
            if self.save_instance(instance_id):
                return {"msg": "saved"}
            raise HTTPException(status_code=404, detail="Instance not found!")

        @self.delete("/{instance_id}/close")
        async def close_instance(instance_id: str):
            if self.close_instance(instance_id):
                return {"msg": "closed"}
            raise HTTPException(status_code=404, detail="Instance not found!")

        @self.delete("/{instance_id}/delete")
        async def remove_related_entry(instance_id: str):
            if self.remove_instance(instance_id):
                return {"msg": "closed"}
            raise HTTPException(status_code=404, detail="Resource not found!")


    def get_instances(self, all=True):
        res = []
        if all:
            res = list(self.registration.get_registered(exclude=["location", "remote"]).keys())
        for key in self.instances.keys():
            if key not in res:
                res.append(key)
        return res

    def create_instance(self, load_id: Optional[str] = None, publish_id: Optional[str] = None) -> str:
        instance = None
        if load_id:
            node = self.registration.launch(load_id)
            if not node:
                return ""
            if not isinstance(node, Module):
                return ""
            instance = Instance(id=publish_id, module=node)
        else:
            instance = Instance(id=publish_id)

        publish_id = instance.id
        self.instances[publish_id] = instance
        return publish_id

    def change_instance(self, name: str, change: dict):
        pass

    def save_instance(self, name: str):
        instance = self.instances.get(name)
        if not instance:
            return False
        self.registration.store(instance.id, instance.module)
        return True

    def close_instance(self, name: str):
        if name in self.instances.keys():
            self.instances.pop(name)
            print("[Factory]: closed instance: " + name)
            return True
        return False

    def remove_instance(self, name: str):
        instance = self.instances.get(name)
        if instance:
            name = instance.id
            self.instances.pop(name)
        if self.registration.remove(name):
            return True
        return False