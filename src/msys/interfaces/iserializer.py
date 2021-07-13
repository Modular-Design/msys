from abc import ABC, abstractmethod


class ISerializer(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def load(self, json: dict) -> bool:
        raise NotImplementedError

