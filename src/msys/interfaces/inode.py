from .ichild import IChild
from .iupdatable import IUpdatable
from .iserializer import ISerializer
from abc import ABC, abstractmethod

class INode(ABC, IChild, ISerializer, IUpdatable):
    @abstractmethod
    def get_childs(self) -> list:
        pass

    @abstractmethod
    def get_inputs(self) -> list:
        pass

    @abstractmethod
    def get_outputs(self) -> list:
        pass

    @abstractmethod
    def get_options(self) -> list:
        pass

    @abstractmethod
    def add_input(self) -> bool:
        pass

    @abstractmethod
    def remove_input(self, id) -> bool:
        pass

    @abstractmethod
    def add_output(self) -> bool:
        pass

    @abstractmethod
    def remove_output(self, id) -> bool:
        pass