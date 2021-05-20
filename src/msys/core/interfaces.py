from abc import ABC, ABCMeta, abstractmethod


def includes(array: [], elements: []) -> bool:
    for e in elements:
        if not e in array:
            return False
    return True


class SerializerInterface(ABC):# metaclass=ABCMeta
    @abstractmethod
    def from_dict(self, json: dict) -> bool:
        """Load class from dictionary."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Gerenate dict from class."""
        pass


class ConnectableInterface(ABC):# metaclass=ABCMeta
    @abstractmethod
    def get_value(self) -> []:
        pass

    @abstractmethod
    def set_value(self, value) -> bool:
        pass

    @abstractmethod
    def get_ingoing(self):
        pass

    @abstractmethod
    def get_outgoing(self) -> []:
        pass

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def connect_ingoing(self, output) -> bool:
        pass

    @abstractmethod
    def connect_outgoing(self, input) -> bool:
        pass

    @abstractmethod
    def disconnect_ingoing(self) -> bool:
        pass

    @abstractmethod
    def disconnect_outgoing(self) -> bool:
        pass

    @abstractmethod
    def is_changed(self) -> bool:
        pass

    @abstractmethod
    def update(self) -> bool:
        return True


class TypeInterface(SerializerInterface):
    """
    """

    def is_same(self, value) -> bool:
        pass

    def get_value(self):
        """
        Must return representative value for connectivity-checks
        """
        pass

    def set_value(self, value) -> bool:
        pass

    def is_changed(self) -> bool:
        """
        Returns True if value has changed.
        Important for optimisation, for deciding whether to ignore or process a recipe.
        """
        pass

    def is_connectable(self, other) -> bool:
        pass