from .inode import INode
from abc import ABC, abstractmethod

class IModule(ABC, INode):
    @abstractmethod
    def connect(self, output:"Connectable", input:"Connectable") -> bool:
        pass

    @abstractmethod
    def disconnect(self, cid:"Connection") -> bool:
        pass