from abc import ABC, ABCMeta, abstractmethod

def includes(array: [], elements: []) -> bool:
    for e in elements:
        if not e in array:
            return False
    return True

class SerializerInterface(ABC):

    @abstractmethod
    def from_dict(self, json: dict, safe=False) -> bool:
        """Load class from dictionary."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Gerenate dict from class."""
        pass

class Serializer(SerializerInterface):
    def __init__(self, protected = False):
        self.protected = False;

    def from_dict(self, json: dict, safe=False) -> bool:
        if safe:
            if self.protected:
                return False

        if "protected" in json.keys():
            self.protected = json["protected"]
        return True

    def to_dict(self) -> dict:
        res = dict()
        if self.protected:
            res["protected"] = self.protected
        return res


    def set_protected(self, protected:bool):
        self.protected = protected

    def is_protected(self) -> bool:
        return self.protected

