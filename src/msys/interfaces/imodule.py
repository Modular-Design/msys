from .inode import INode
from abc import ABC, abstractmethod
from typing import List

class IModule(INode):
    @abstractmethod
    def get_nodes(self) -> List[INode]:
        raise NotImplementedError

    @abstractmethod
    def connect(self, output: "Connectable", input: "Connectable") -> bool:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, cid: List[str]) -> bool:
        raise NotImplementedError