from fastapi import FastAPI
from typing import Optional, List
from .node import Node
from .connectable import Connectable
from .option import Option
from .metadata import Metadata


class Module(Node):
    def __init__(self,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 inputs: Optional[List[Connectable]] = None,
                 outputs: Optional[List[Connectable]] = None,
                 options: Optional[List[Option]] = None,
                 nodes: Optional[Node] = None):
        super().__init__(name=name, description=description)
        if nodes is None:
            nodes = []
        self.nodes = nodes
        self.connections = []

    def get_node(self, id:str):
        for node in self.nodes:
            if node.id == id:
                return node

    def connect(self, output, input):
        pass

    def disconnect(self, id):
        pass