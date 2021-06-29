from fastapi import FastAPI
from typing import Optional
from .node import Node
from .metadata import Metadata


class Module(Node):
    def __init__(self,
                 nodes: Optional[Node] = None):
        super().__init__()
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