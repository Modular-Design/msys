from fastapi import FastAPI, APIRouter, BackgroundTasks, Body, Path, HTTPException
from ..core import Module, Connectable, Type
from .routers import module
from ..registration import *
from typing import List, Optional, Set

class MSYSServer(FastAPI):
    def __init__(self, module_obj=None, changeable = False):
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
            return json

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
            return json

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

        """
        #####################
        Module specific API's
        #####################
        """

        @modules.get("/root")
        async def get_root_module():
            return self.module.to_dict()

        def find_module(module_id:str):
            import json
            module_id = module_id.replace("'","\"")
            module_id = json.loads(module_id)
            found = self.module.find(module_id)
            return found

        @modules.get("/{module_id}")
        async def get_module(
                module_id:str = Path(
                    ...,
                    example=str(self.module.identifier())
                ),):
            found = find_module(module_id)
            if isinstance(found, Module):
                return found.to_dict()
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.post("/{parent_id}")
        async def add_module(
                *,
                parent_id:str = Path(
                    ...,
                    example=str(self.module.identifier())
                ),
                module: dict= Body(
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
                parent = find_module(parent_id)
                if not isinstance(parent, Module):
                    raise HTTPException(status_code=404, detail="Parent not Found")
                parent.add_module(module)

            return module.to_dict()

        @modules.put("/{module_id}")
        async def update_module(
                module_id: str = Path(
                    ...,
                    example=str(self.module.identifier())
                ),
                body: dict= Body(
                    ...,
                    example={
                      "metadata": {"name": "ROOT",}
                    }
                ),
            ):
            found = find_module(module_id)
            if not isinstance(found, Module):
                raise HTTPException(status_code=404, detail="Module not Found")
            if not found.from_dict(body):
                raise HTTPException(status_code=404, detail="Body caused Exception!")
            return found.to_dict()


        @modules.delete("/{module_id}")
        async def delete_module(
                module_id: str= Path(
                    ...,
                    example=str(self.module.identifier())
                )):
            found = find_module(module_id)
            if not isinstance(found, Module):
                raise HTTPException(status_code=404, detail="Module not Found")
            del found
            return {"message": "Module deleted!"}

        @modules.get("/{module_id}/inputs")
        async def get_module_inputs(module_id:str):
            found = find_module(module_id)
            if isinstance(found, Module):
                return found["inputs"]
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.post("/{parent_id}/connect")
        async def connect(
                parent_id: str = Path(
                    ...,
                    example=str(self.module.identifier())
                ),
                body = Body(
                    ...,
                    examples={
                        "lazy":{
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
            parent = find_module(parent_id)
            if not isinstance(parent, Module):
                raise HTTPException(status_code=404, detail="Module not Found")
            obj_from = parent.find(body["from"])
            obj_to = parent.find(body["to"])
            if parent.connect(obj_from, obj_to):
                outgoing = obj_from.get_outgoing()
                if obj_to in outgoing:
                    return {"from": body["from"], "to": body["to"]}
                else:
                    return {"from": body["to"], "to": body["from"]}
            raise HTTPException(status_code=404, detail="Connection not Possible")


        @modules.put("/{module_id}/inputs/{id}")
        async def get_module_inputs(module_id: str):
            found = find_module(module_id)
            if isinstance(found, Module):
                return found["inputs"]
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.get("/{module_id}/ouputs")
        async def get_module_ouputs(module_id: str):
            found = find_module(module_id)
            if isinstance(found, Module):
                return found["ouputs"]
            raise HTTPException(status_code=404, detail="Module not Found")


        @modules.get("/{module_id}/modules")
        async def get_module_submodules():
            return {"message": "Hello World"}

        @modules.post("/{module_id}/inputs/")
        async def get_module_inputs(module_id: str):
            found = find_module(module_id)
            if isinstance(found, Module):
                return found["inputs"]
            raise HTTPException(status_code=404, detail="Module not Found")

        @modules.put("/{module_id}/inputs/{id}")
        async def get_module_inputs(module_id: str):
            found = find_module(module_id)
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
            found = find_module(module_id)
            if not isinstance(found, Module):
                raise HTTPException(status_code=404, detail="Module not Found")
            background_tasks.add_task(found.update)
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
            return json

        self.include_router(extensions)
        self.include_router(modules)
        self.include_router(types)