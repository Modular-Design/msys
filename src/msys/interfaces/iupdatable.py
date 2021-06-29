from abc import ABC, abstractmethod


class IUpdatable(ABC):
    @abstractmethod
    def update(self) -> bool:
        pass

    @abstractmethod
    def is_changed(self) -> bool:
        pass
