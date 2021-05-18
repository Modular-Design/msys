from ..unit import UniqueUnit
from .connectable import ConnectableInterface
from .type import TypeInterface


class Input(UniqueUnit, ConnectableInterface):
    """A class to connect to one Output.

       Inputs can have multiple Types to be very flexible when trying to connect to an Output.
       On Input can only be connected to one Output but one Output can have multiple connected Inputs.

       Attributes:
           types (list): a list of types with which the input tries to parse the type of the output
           type_id (int): the index of the type, with which a successfull connection was made
           connection (Output): the connected output
    """
    def __init__(self, types: list, output=None, optimized=False, generator=None):
        """Input Constructor

        Note:
            Do not include the `self` parameter in the ``Args`` section
        Args:
            types (:obj:`list`, optional): Description of `param1`.
            connection (:obj:`Output`, optional): Description of `param2`.
        """
        super().__init__()
        self.generator = generator
        self.types = types
        self.type_id = 0
        self.output = output
        self.optimized = optimized

    def get_value(self):
        """
        Returns the value of the connectable type.

        Returns:
            value: Type specific value
        """
        if self.output:
            return self.output.get_value()
        return self.types[self.type_id].get_value()

    def set_value(self, value) -> bool:
        """
        Sets the default value.
        Args:
            value (): the new default value

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.output:
            return False
        else:
            return self.types[self.type_id].set_value(value)

    def is_optimized(self) -> bool:
        if self.output:
            return False
        return self.optimized

    def set_optimized(self, optimized: bool) -> bool:
        self.optimized = optimized
        return self.is_optimized()

    def is_changed(self) -> bool:
        if self.output:
            return self.output.is_changed()
        return self.types[self.type_id].is_changed()

    def is_connected(self) -> bool:
        if self.output:
            return True
        return False

    def connect(self, connectable, both=True) -> bool:
        """Use to connect to Output.
        One Input can only connect to one Output,
        but one Output can be connected to multiple Inputs.
        If the Input is already connected it gets disconnected and then tries to connect to the new Output.

        Args:
            connectable (Connectable): accepts all kind of objects, but only outputs have a chance to succeed.
            both (:obj:`bool`, optional): bool, optional
            is used if both Input and Output should know from each other.
            Default ``True``.

        Returns:
            bool: True if successful, False otherwise.
        """
        from .output import Output
        if not isinstance(connectable, Output):
            return False
        if self.output:
            if not self.disconnect():
                return False
        i = TypeInterface.is_compatible(connectable.type, self.types)
        if i < 0:
            return False
        if both:
            if not connectable.connect(self, False):
                return False
        self.type_id = i
        self.output = connectable
        return True

    def disconnect(self, connectable=None, both=True) -> bool:
        if not self.output:
            return False

        if both:
            if not self.output.disconnect(self, False):
                return False
        self.output = None
        return True

    def update(self) -> bool:
        result = self.is_changed()
        return result

