from .inode import INode
from abc import ABC, abstractmethod

class IModule(ABC, INode):
    @abstractmethod
    def find_child(self, id:str, local_context=True) -> IChild:
        raise NotImplementedError

    @abstractmethod
    def connect(self, output:"Connectable", input:"Connectable") -> bool:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, cid:"Connection") -> bool:
        raise NotImplementedError