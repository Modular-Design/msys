from .ichild import IChild
from .iupdatable import IUpdatable
from .iserializer import ISerializer
from abc import ABC, abstractmethod
from typing import List


class IConnectable(IChild, ISerializer, IUpdatable):
    @abstractmethod
    def get_data(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def set_data(self, data) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_output(self) -> "IConnectable":
        raise NotImplementedError

    @abstractmethod
    def set_ingoing(self, connection: "Connection"):
        """
        Set the Ingoing-Connection.
        There can be only one! Further calls will overite the current connection.

        Args:
            other: Connection to get value from

        """
        raise NotImplementedError

    @abstractmethod
    def get_inputs(self) -> List["IConnectable"]:
        raise NotImplementedError

    @abstractmethod
    def set_outgoing(self, connections: List["Connection"]) -> None:
        """

        Args:
            other:

        Returns:
            bool: True if successfully connected to.
        """
        raise NotImplementedError

    @abstractmethod
    def add_outgoing(self, connection: "Connection") -> None:
        """

        Args:
            other:

        Returns:
            bool: True if successfully connected to.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_outgoing(self, connection: "Connection") -> None:
        """

        Args:
            other:

        Returns:
            bool: True if successfully connected to.
        """
        raise NotImplementedError

    @abstractmethod
    def is_data_valid(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def is_connectable(self, output: "IConnectable"):
        raise NotImplementedError

    @abstractmethod
    def is_editable(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_connected(self) -> bool:
        raise NotImplementedError