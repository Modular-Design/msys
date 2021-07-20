from abc import ABC, abstractmethod
from typing import Optional

class IChild(ABC):
    @abstractmethod
    def set_parent(self, node: "Node") -> None:
        raise NotImplementedError

    @abstractmethod
    def set_local_id(self, id: Optional[str] = None):
        raise NotImplementedError

    @abstractmethod
    def get_global_id(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_local_id(self) -> str:
        raise NotImplementedError
