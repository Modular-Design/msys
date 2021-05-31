from fastapi import FastAPI, APIRouter, BackgroundTasks, Body, Path, HTTPException, status

from ..core import Module, Connectable, Type
from ..registration import *
from typing import List, Optional, Set
from enum import Enum

import zmq
import json


class Topics(Enum):
    ADD = "add"
    CONNECT = "connect"
    CHANGE = "change"
    DELETE = "delete"
    STATUS = "status"


class MSYSServer(FastAPI):
    def __init__(self, module_obj=None, changeable=False, port=5557):
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

        def find_object(module_id: str):
            import json
            module_id = module_id.replace("'", "\"")
            module_id = json.loads(module_id)
            found = self.module.find(module_id)
            return found

        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%d" % port)

        # from fastapi_websocket_pubsub import PubSubEndpoint
        # endpoint = PubSubEndpoint()
        # endpoint.register_route(self, "/pubsub")

        async def publish(status: Topics, address: list, content: dict):
            # await endpoint.publish([status.value], content)
            self.socket.send_string(status.value)
            self.socket.send_string(json.dumps(address))
            self.socket.send_string(json.dumps(content))

        async def publish_parent_status(parent_id):
            found = find_object(parent_id)
            if found:
                await publish(Topics.STATUS, found.identifier(), found.to_dict())

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
                    example=str(self.module.identifier())
                ), ):
            found = find_object(module_id)
            if isinstance(found, Module):
                return found.to_dict()
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.post("/{parent_id}", status_code=status.HTTP_201_CREATED)
        async def add_module(
                background_tasks: BackgroundTasks,
                parent_id: str = Path(
                    ...,
                    example=str(self.module.identifier())
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
            background_tasks.add_task(publish_parent_status, parent_id)
            return {"message": "Module created!"}

        @modules.put("/{module_id}", status_code=status.HTTP_202_ACCEPTED)
        async def update_module(
                background_tasks: BackgroundTasks,
                module_id: str = Path(
                    ...,
                    example=str(self.module.identifier())
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
            background_tasks.add_task(publish_parent_status, module_id)

            return {"message": "Module updated!"}

        @modules.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
        async def delete_module(
                background_tasks: BackgroundTasks,
                module_id: str = Path(
                    ...,
                    example=str(self.module.identifier())
                )):
            found = find_object(module_id)

            if not isinstance(found, Module):
                raise HTTPException(status_code=404, detail="Module not Found")

            msg = found.to_dict()
            parent_id = str(found.parent.identifier())
            del found
            background_tasks.add_task(publish, Topics.DELETE, json.loads(parent_id), msg)
            background_tasks.add_task(publish_parent_status, parent_id)
            return {"message": "Module deleted!"}

        @modules.get("/{module_id}/inputs")
        async def get_module_inputs(module_id: str):
            found = find_object(module_id)
            if isinstance(found, Module):
                return found["inputs"]
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.post("/{parent_id}/connect", status_code=status.HTTP_202_ACCEPTED)
        async def connect(
                background_tasks: BackgroundTasks,
                parent_id: str = Path(
                    ...,
                    example=str(self.module.identifier())
                ),
                body=Body(
                    ...,
                    examples={
                        "lazy": {
                            "summary": "A lazy example",
                            "description": "A **lazy** connection works does not care about right direction.",
                            "value": {
                                "from": self.module.inputs[0].identifier(),
                                "to": self.module.outputs[0].identifier(),
                            },
                        },
                        "normal": {
                            "summary": "A normal example",
                            "description": "A **normal** connection works from output to input.",
                            "value": {
                                "from": self.module.outputs[0].identifier(),
                                "to": self.module.inputs[0].identifier(),
                            },
                        },
                    }
                )
        ):
            parent = find_object(parent_id)
            if not isinstance(parent, Module):
                raise HTTPException(status_code=404, detail="Module not Found")
            obj_from = parent.find(body["from"])
            obj_to = parent.find(body["to"])
            if parent.connect(obj_from, obj_to):
                outgoing = obj_from.get_outgoing()
                msg = {}
                if obj_to in outgoing:
                    msg = {"from": body["from"], "to": body["to"]}
                else:
                    msg = {"from": body["to"], "to": body["from"]}
                background_tasks.add_task(publish, Topics.CONNECT, json.loads(parent_id), msg)
                background_tasks.add_task(publish_parent_status, parent_id)
            raise HTTPException(status_code=404, detail="Connection not Possible")

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

        @modules.put("/{module_id}/update")
        async def update_module(
                background_tasks: BackgroundTasks,
                module_id: str = Path(
                    ...,
                    example=str(self.module.identifier())
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
