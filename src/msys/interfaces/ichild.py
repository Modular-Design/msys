from abc import ABC, abstractmethod


class IChild(ABC):
    @abstractmethod
    def set_parent(self, module:"Module"):
        pass