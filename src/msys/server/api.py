from fastapi import FastAPI, APIRouter, BackgroundTasks, Body, Path, HTTPException, status

from ..core import Module, Type, Connection
from ..registration import *
from typing import List, Optional, Set
from enum import Enum

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json


class Topics(Enum):
    ADD = "add"
    CONNECT = "connect"
    CHANGE = "change"
    DELETE = "delete"
    STATUS = "status"


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


class MSYSServer(FastAPI):
    def __init__(self, module_obj=None, changeable=False):
        super().__init__()
        if module_obj is None:
            self.module = Module(inputs=[Type(0)], outputs=[Type(1)])

        """
        #######################
        POST: to create data.
        GET: to read data.
        PUT: to update data.
        DELETE: to delete data.
        #######################
        """

        def find_object(module_id):
            if isinstance(module_id, str):
                print("str")
                import json
                module_id = module_id.replace("'", "\"")
                module_id = json.loads(module_id)

            print(module_id)
            if isinstance(module_id, list):
                print("list")
                module_id = self.module.find(module_id)

            return module_id

        self.manager = ConnectionManager()

        # from fastapi_websocket_pubsub import PubSubEndpoint
        # endpoint = PubSubEndpoint()
        # endpoint.register_route(self, "/pubsub")

        async def publish(status: Topics, address: list, content: dict):
            # await endpoint.publish([status.value], content)
            msg = dict(topic=status.value, receiver=address, content=content)
            # print(msg)
            print("[API]: " + json.dumps(msg))
            await self.manager.broadcast(json.dumps(msg))

        async def publish_parent_status(parent_id):
            found = find_object(parent_id)
            if found:
                await publish(Topics.STATUS, found.complete_id(), found.to_dict())

        @self.websocket("/pubsub")
        async def websocket_endpoint(websocket: WebSocket):
            # await websocket.accept()
            print("Connected")
            await self.manager.connect(websocket)
            try:
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                self.manager.disconnect(websocket)
                await self.manager.broadcast(f"Client left the Projekt")
                print("DISCONNECTED")

        """
        ########################
        Extension specific API's
        ########################
        """
        extensions = APIRouter(
            prefix="/extensions",
            tags=["extensions"],
            dependencies=[],
            responses={404: {"description": "Not found"}},
        )

        @extensions.get("/")
        async def available_extensions():
            json = get_extensions()
            for j in json:
                del j["class"]
            return dict(extensions=json)

        """
        #####################
        Module specific API's
        #####################
        """
        modules = APIRouter(
            prefix="/modules",
            tags=["modules"],
            dependencies=[],
            responses={404: {"description": "Not found"}},
        )

        @modules.get("/")
        async def available_modules():
            json = get_modules()
            for j in json:
                del j["class"]
            return dict(modules=json)

        @modules.get("/all")
        async def all_modules():
            res = [self.module.to_dict()]

            def get_modules(module):
                for m in module.modules:
                    res.append(m.to_dict())
                    if m.modules:
                        get_modules(m)

            get_modules(self.module)
            return res

        @modules.get("/root")
        async def get_root_module():
            return self.module.to_dict()

        @modules.get("/{module_id}")
        async def get_module(
                module_id: str = Path(
                    ...,
                    example=str(self.module.complete_id())
                ), ):
            found = find_object(module_id)
            if isinstance(found, Module):
                return found.to_dict()
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.post("/connect", status_code=status.HTTP_202_ACCEPTED)
        async def connect(
                background_tasks: BackgroundTasks,
                body=Body(
                    ...,
                    examples={
                        "lazy": {
                            "summary": "A lazy example",
                            "description": "A **lazy** connection works does not care about right direction.",
                            "value": {
                                "from": self.module.inputs[0].complete_id(),
                                "to": self.module.outputs[0].complete_id(),
                            },
                        },
                        "normal": {
                            "summary": "A normal example",
                            "description": "A **normal** connection works from output to input.",
                            "value": {
                                "from": self.module.outputs[0].complete_id(),
                                "to": self.module.inputs[0].complete_id(),
                            },
                        },
                    }
                )
        ):
            print("found "+ str(body))
            res = Connection.find_connection(self.module, body["from"], body["to"])
            if len(res) != 3:
                raise HTTPException(status_code=404, detail="Not Connectable")
            parent = res[2]

            if not isinstance(parent, Module):
                raise HTTPException(status_code=404, detail="Module not Found")
            input = res[1]
            output = res[0]

            print("Connect")

            if Connection.connect( output, input, parent):
                msg = {"from": output.complete_id(), "to": input.complete_id()}

                background_tasks.add_task(publish, Topics.CONNECT, json.dumps(parent.complete_id()), msg)
                background_tasks.add_task(publish_parent_status, parent)
                return {"message": "Successfull Connection!"}
            raise HTTPException(status_code=404, detail="Connection not Possible")

        @modules.delete("/disconnect", status_code=status.HTTP_202_ACCEPTED)
        async def connect(
                background_tasks: BackgroundTasks,
                body=Body(
                    ...,
                    examples={
                        "lazy": {
                            "summary": "A lazy example",
                            "description": "A **lazy** connection works does not care about right direction.",
                            "value": {
                                "from": self.module.inputs[0].complete_id(),
                                "to": self.module.outputs[0].complete_id(),
                            },
                        },
                        "normal": {
                            "summary": "A normal example",
                            "description": "A **normal** connection works from output to input.",
                            "value": {
                                "from": self.module.outputs[0].complete_id(),
                                "to": self.module.inputs[0].complete_id(),
                            },
                        },
                    }
                )
        ):
            print("found " + str(body))
            res = self.module.find_pair(body["from"], body["to"])
            if len(res) != 3:
                raise HTTPException(status_code=404, detail="Not Connectable")
            parent = res[2]

            if not isinstance(parent, Module):
                raise HTTPException(status_code=404, detail="Module not Found")
            input = res[2]
            output = res[1]



            if Connection.disconnect(output, input, parent):
                msg = {"from": output.complete_id(), "to": input.complete_id()}

                background_tasks.add_task(publish, Topics.DELETE, json.dumps(parent.complete_id()), msg)
                # background_tasks.add_task(publish_parent_status, parent)
                return {"message": "Successfull Connection!"}
            raise HTTPException(status_code=404, detail="Connection not Possible")

        @modules.post("/{parent_id}", status_code=status.HTTP_201_CREATED)
        async def add_module(
                background_tasks: BackgroundTasks,
                parent_id: str = Path(
                    ...,
                    example=str(self.module.complete_id())
                ),
                module: dict = Body(
                    ...,
                    example={
                        "package": "msys",
                        "name": "NetworkModule",
                    }
                ),
        ):
            res = filter_package(module["package"], filter_name(module["name"], get_modules()))
            if not res:
                raise HTTPException(status_code=404, detail="Format not found.")

            module = res[0]["class"]()

            if parent_id == "[]":
                self.module = module
            else:
                parent = find_object(parent_id)
                if not isinstance(parent, Module):
                    raise HTTPException(status_code=404, detail="Parent not Found")
                parent.add_module(module)

            background_tasks.add_task(publish, Topics.ADD, json.loads(parent_id), module.to_dict())
            # background_tasks.add_task(publish_parent_status, parent_id)
            return {"message": "Module created!"}

        @modules.put("/{module_id}", status_code=status.HTTP_202_ACCEPTED)
        async def update_module(
                background_tasks: BackgroundTasks,
                module_id: str = Path(
                    ...,
                    example=str(self.module.complete_id())
                ),
                body: dict = Body(
                    ...,
                    example={
                        "metadata": {"name": "ROOT", }
                    }
                ),
        ):
            found = find_object(module_id)
            if not isinstance(found, Module):
                raise HTTPException(status_code=404, detail="Module not Found")
            if not found.from_dict(body):
                raise HTTPException(status_code=400, detail="Body caused Exception!")

            background_tasks.add_task(publish, Topics.CHANGE, json.loads(module_id), found.to_dict())
            # background_tasks.add_task(publish_parent_status, module_id)

            return {"message": "Module updated!"}

        @modules.delete("/delete/{module_id}", status_code=status.HTTP_202_ACCEPTED)
        async def delete_module(
                background_tasks: BackgroundTasks,
                module_id: str = Path(
                    ...,
                    example=str(self.module.complete_id())
                )):
            found = find_object(module_id)

            if not isinstance(found, Module):
                raise HTTPException(status_code=404, detail="Module not Found")

            msg = found.to_dict()
            parent_id = str(found.parent.complete_id())
            found.delete()
            # background_tasks.add_task(publish, Topics.DELETE, json.loads(parent_id), msg)
            background_tasks.add_task(publish_parent_status, parent_id)
            return {"message": "Module deleted!"}

        @modules.get("/{module_id}/inputs")
        async def get_module_inputs(module_id: str):
            found = find_object(module_id)
            if isinstance(found, Module):
                return found["inputs"]
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.put("/{module_id}/inputs/{id}")
        async def get_module_inputs(module_id: str):
            found = find_object(module_id)
            if isinstance(found, Module):
                return found["inputs"]
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.get("/{module_id}/ouputs")
        async def get_module_ouputs(module_id: str):
            found = find_object(module_id)
            if isinstance(found, Module):
                return found["ouputs"]
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.get("/{module_id}/modules")
        async def get_module_submodules():
            return {"message": "Hello World"}

        @modules.post("/{module_id}/inputs/")
        async def get_module_inputs(module_id: str):
            found = find_object(module_id)
            if isinstance(found, Module):
                return found["inputs"]
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.put("/{module_id}/inputs/{id}")
        async def get_module_inputs(module_id: str):
            found = find_object(module_id)
            if isinstance(found, Module):
                return found["inputs"]
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.put("/update/{module_id}")
        async def update_module(
                background_tasks: BackgroundTasks,
                module_id: str = Path(
                    ...,
                    example=str(self.module.complete_id())
                )):
            found = find_object(module_id)
            if not isinstance(found, Module):
                raise HTTPException(status_code=404, detail="Module not Found")
            background_tasks.add_task(found.update, json.loads(module_id), found)
            background_tasks.add_task(publish_parent_status, module_id)
            return {"message": "Process is updating in the background!"}

        """
        #####################
        Types specific API's
        #####################
        """
        types = APIRouter(
            prefix="/types",
            tags=["types"],
            dependencies=[],
            responses={404: {"description": "Not found"}},
        )

        @types.get("/")
        async def available_types():
            json = get_types()
            for j in json:
                del j["class"]
            return dict(types=json)

        self.include_router(extensions)
        self.include_router(modules)
        self.include_router(types)
