from abc import ABC, abstractmethod


class IChild(ABC):
    @abstractmethod
    def set_parent(self, node: "Node") -> None:
        raise NotImplementedError

    @abstractmethod
    def get_global_id(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_local_id(self) -> str:
        raise NotImplementedError
