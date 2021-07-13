from .ichild import IChild
from .iupdatable import IUpdatable
from .iserializer import ISerializer
from .iconnectable import IConnectable

from typing import List
from abc import ABC, abstractmethod

class INode(IChild, ISerializer, IUpdatable):
    @abstractmethod
    def find_child(self, cid: List[str], local=False) -> IChild:
        raise NotImplementedError

    @abstractmethod
    def get_inputs(self, local=False) -> List[IConnectable]:
        raise NotImplementedError

    @abstractmethod
    def get_outputs(self, local=False) -> List[IConnectable]:
        raise NotImplementedError

    @abstractmethod
    def get_options(self) -> List["Option"]:
        raise NotImplementedError

    @abstractmethod
    def get_input(self, id: str, local=False):
        raise NotImplementedError

    @abstractmethod
    def get_output(self, id: str, local=False):
        raise NotImplementedError

    @abstractmethod
    def are_inputs_removable(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def are_outputs_removable(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_removable_inputs(self) -> List[IConnectable]:
        raise NotImplementedError

    @abstractmethod
    def get_removable_outputs(self) -> List[IConnectable]:
        raise NotImplementedError

    @abstractmethod
    def add_input(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove_input(self, id) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_output(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove_output(self, id) -> bool:
        raise NotImplementedError