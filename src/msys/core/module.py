from typing import Optional, List
from .node import Node
from .connectable import Connectable
from .option import Option
from .helpers import load_entrypoints


class Module(Node):
    def __init__(self,
                 name: Optional[str] = "Module",
                 description: Optional[str] = "A Master-Module",
                 inputs: Optional[List[Connectable]] = None,
                 outputs: Optional[List[Connectable]] = None,
                 options: Optional[List[Option]] = None,
                 nodes: Optional[Node] = None):
        super().__init__(name=name, description=description)
        if nodes is None:
            nodes = []
        self.nodes = nodes
        self.connections = []
        self.registered = dict()
        self.update_registered()

    def update_registered(self):
        # register entrypoints
        entrypoints = load_entrypoints("msys.modules")
        if entrypoints:
            print("[Module]: " + str(entrypoints))
            for entry in entrypoints:
                eclass = entry.load()

                strclass = str(entry.value)
                if type(eclass) == type: # is class
                    obj = eclass()
                    pos0 = strclass.find("'") + 1
                    pos1 = strclass.find("'", pos0)
                    strclass = strclass[pos0: pos1]
                else:
                    obj = eclass

                meta = obj.to_dict()["meta"]

                infos = dict(pyclass=eclass)#launch
                if "name" in meta.keys():
                    infos["name"] = meta["name"]
                else:
                    infos["name"] = entry.name

                if "description" in meta:
                    infos["description"] = meta["description"]

                self.registered.update({entry.name: infos})
        print(self.registered)
        # register from file

    def get_node(self, id:str):
        for node in self.nodes:
            if node.id == id:
                return node

    def add_node(self,
                 node: Node):
        self.nodes.append(node)

    def connect(self, output, input):
        pass

    def disconnect(self, id):
        pass