from typing import Optional, List
from .node import Node
from .connectable import Connectable
from .option import Option
from .helpers import load_entrypoints
import inspect


class Module(Node):
    def __init__(self,
                 name: Optional[str] = "Module",
                 description: Optional[str] = "A Master-Module",
                 inputs: Optional[List[Connectable]] = None,
                 outputs: Optional[List[Connectable]] = None,
                 options: Optional[List[Option]] = None,
                 nodes: Optional[Node] = None):
        super().__init__(name=name, description=description)

        self.registered = dict()
        self.update_registered()

        # add nodes
        if nodes is None:
            nodes = []
        self.nodes = []

        for node in nodes:
            if isinstance(node, Node):
                self.nodes.append(node)
            if type(node) == str:
                self.add_node_from_key(node)

        self.connections = []


    def update_registered(self):
        # register entrypoints
        entrypoints = load_entrypoints("msys.modules")
        if entrypoints:
            print("[Module]: " + str(entrypoints))
            for entry in entrypoints:
                try:
                    eclass = entry.load()
                except:
                    continue

                print("[Module] load entry: " + entry.value)
                obj = eclass

                meta = obj.to_dict()["meta"]

                infos = dict(launch="uvicorn " +entry.value + " --port {port}")#launch
                if "name" in meta.keys():
                    infos["name"] = meta["name"]
                else:
                    infos["name"] = entry.name

                if "description" in meta:
                    infos["description"] = meta["description"]

                self.registered.update({entry.name: infos})
        print("[Module]: registered " + str(self.registered))
        # register from file

    def get_node(self, id:str):
        if id == self.id:
            return self
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def add_node(self,
                 node: Node):
        self.nodes.append(node)

    def add_node_from_key(self,
                 key: str):
        if not key in self.registered.keys():
            return False
        self.add_node(Node(id=len(self.nodes), process=self.registered[key]["launch"])) # TODO remove id setter
        return True

    def find_input(self, parent_id: str, input_id: str):
        node = self.get_node(parent_id)
        if not node:
            return None
        if node is self:
            return node.get_output(input_id)
        return node.get_input(input_id)

    def find_output(self, parent_id: str, output_id: str):
        node = self.get_node(parent_id)
        if not node:
            return None
        if node is self:
            return node.get_input(output_id)
        return node.get_output(output_id)

    def connect(self, output: Connectable, input: Connectable):
        
        pass

    def disconnect(self, id):
        pass


