from fastapi import APIRouter, HTTPException, Body


class NodesRouter(APIRouter):
    def __init__(self,
                 module):
        super().__init__(prefix="/nodes", tags=["nodes"])
        self.module = module

        @self.get("/")
        async def get_all():
            res = []
            for node in self.module.nodes:
                res.append(node.to_dict())
            return res

        @self.get("/registered")
        async def get_registered():
            res = self.module.registered.copy()
            for key in res.keys():
                res[key]["launch"] = str(res[key]["launch"])
            return res

        @self.get("/{id}/config")
        async def get_config(id: str):
            node = self.module.get_node(id)
            if node is None:
                raise HTTPException(status_code=404, detail="Not Found")
            return node.to_dict()

        @self.post("/{id}/config")
        async def change_config(id: str,
                                body=Body(
                                    ...,
                                ),
                                ):
            node = self.module.get_node(id)
            if node is None:
                print("none")
                raise HTTPException(status_code=404, detail="Not Found")
            if not node.configure(body):
                print("configure")
                raise HTTPException(status_code=404, detail="Error")
            return node.to_dict()

        @self.put("/{id}/update")
        async def update(id: str):
            node = self.module.get_node(id)
            if node is None:
                raise HTTPException(status_code=404, detail="Not Found")
            return node.update()

        @self.get("/{id}/meta")
        async def get_meta(id: str):
            node = self.module.get_node(id)
            if node is None:
                raise HTTPException(status_code=404, detail="Not Found")
            return node.meta.to_dict()

        @self.post("/{id}/meta")
        async def change_meta(id: str,
                              body=Body(
                                  ...,
                              ),
                              ):
            node = self.module.get_node(id)
            if node is None:
                raise HTTPException(status_code=404, detail="Not Found")
            node.meta.load(body)
            return node.meta.to_dict()

        @self.get("/{id}/inputs")
        async def get_inputs(id: str):
            node = self.module.get_node(id)
            if node is None:
                raise HTTPException(status_code=404, detail="Not Found")
            res = []
            for c in node.inputs:
                res.append(c.to_dict())

        @self.get("/{n_id}/inputs/{c_id}")
        async def get_specific_input(n_id: str, c_id: str):
            node = self.module.get_node(n_id)
            if node is None:
                raise HTTPException(status_code=404, detail="Not Found")
            c = node.get_input(c_id)
            if c is None:
                raise HTTPException(status_code=404, detail="Not Found")
            return c.to_dict()

        @self.get("/{id}/outputs")
        async def get_outputs(id: str):
            node = self.module.get_node(id)
            if node is None:
                raise HTTPException(status_code=404, detail="Not Found")
            res = []
            for c in node.inputs_refs:
                res.append(c.to_dict())

        @self.post("/add/{access_id}")
        async def add_node(access_id: str):
            if self.module.add_node_from_key(access_id):
                return {"msg": "success"}
            raise HTTPException(status_code=404, detail="Not Found")

        @self.delete("/{id}/delete")
        async def delete(id: str):
            node = self.module.get_node(id)
            if node is None:
                raise HTTPException(status_code=404, detail="Not Found")
            self.module.nodes.remove(node)
            return len(self.module.nodes)



