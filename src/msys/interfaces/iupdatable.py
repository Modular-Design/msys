from abc import ABC, abstractmethod


class IUpdatable(ABC):
    @abstractmethod
    def update(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_changed(self) -> bool:
        raise NotImplementedError
