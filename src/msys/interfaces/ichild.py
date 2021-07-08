from abc import ABC, abstractmethod


class IChild(ABC):
    @abstractmethod
    def set_parent(self, node:"node") -> None:
        pass

    def get_global_id(self) -> list:
        pass

    def get_local_id(self) -> str:
        pass