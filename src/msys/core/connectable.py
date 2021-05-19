from .interfaces import ConnectableInterface
from enum import Enum
import weakref
from .unit import Unit
import uuid


class ConnectableFlag(Enum):
    INPUT = 0
    OUTPUT = 1


class Connectable(Unit, ConnectableInterface):
    def __init__(self, type, id=None):
        if id is None:
            id = str(uuid.uuid4())
        super().__init__(id)
        self.ctype = type
        self.input = None
        self.outputs = []
        self.flag = None

    def set_global(self, flag: ConnectableFlag):
        self.flag = flag

    def get_local(self):
        if self.flag is None:
            return self.flag
        if self.flag.name == "INPUT":
            return ConnectableFlag.OUTPUT
        else:
            return ConnectableFlag.INPUT

    def get_global(self):
        return self.flag

    def get_value(self):
        if self.get_ingoing():
            self.ctype.set_value(self.get_ingoing().get_value())
        return self.ctype.get_value()

    def set_value(self, value) -> bool:
        if not self.get_ingoing():
            return self.ctype.set_value(value)
        return False

    def get_type(self):
        return self.ctype

    def get_ingoing(self):
        if self.input:
            return self.input()
        return None

    def get_outgoing(self) -> []:
        res = []
        for out in self.outputs:
            obj = out()
            if obj:
                res.append(obj)
        return res

    def connect_ingoing(self, output) -> bool:
        if output:
            return Connectable.connect(self, output)
        return False

    def connect_outgoing(self, input) -> bool:
        if input:
            return Connectable.connect(input, self)
        return False

    def connect_multiple_outgoing(self, inputs: list) -> bool:
        worked = True
        if inputs:
            for input in inputs:
                if not Connectable.connect(input, self):
                    worked = False
        return worked

    def disconnect_ingoing(self) -> bool:
        if self.get_ingoing():
            return Connectable.disconnect(self, self.get_ingoing())
        return True

    def disconnect_outgoing(self) -> bool:
        success = True
        if self.get_outgoing():
            for input in self.get_outgoing():
                print(input)
                if not Connectable.disconnect(input, self):
                    success = False
        return success

    def is_changed(self) -> bool:
        if self.get_ingoing():
            return self.get_ingoing().is_changed()
        return self.ctype.is_changed()

    def update(self) -> bool:
        result = self.is_changed()
        return result

    @staticmethod
    def connect(input: ConnectableInterface, output: ConnectableInterface) -> bool:
        if not (issubclass(input.__class__, ConnectableInterface) and issubclass(output.__class__,
                                                                                 ConnectableInterface)):
            return False

        if not input.get_type().is_connectable(output.get_type()):
            return False

        ingoing = input.get_ingoing()
        if ingoing:
            if not input.disconnect_ingoing():
                return False
        input.input = weakref.ref(output)

        outgoing = output.get_outgoing()
        if not input in outgoing:
            output.outputs.append(weakref.ref(input))
        return True

    @staticmethod
    def disconnect(input: ConnectableInterface, output: ConnectableInterface) -> bool:
        if not (issubclass(Connectable, input.__class__) and issubclass(Connectable, output.__class__)):
            return False

        if not input in output.get_outgoing():
            return False
        input.input = None
        index = output.get_outgoing().index(input)
        output.outputs.pop(index)
        return True
