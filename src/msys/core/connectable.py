from .interfaces import ConnectableInterface
from enum import Enum
import weakref
from .unit import UUnit


class ConnectableFlag(Enum):
    INPUT = 0
    OUTPUT = 1


class Connectable(UUnit, ConnectableInterface):
    def __init__(self, type, id=None):
        super().__init__(id)
        self.ctype = type
        self.input = None
        self.outputs = []
        self.flag = None

    def to_dict(self) -> dict:
        res = super().to_dict()
        res["type"] = self.ctype.to_dict()
        if self.input:
            res["ingoing"] = self.input().id
        if self.outputs:
            res["outpoing"] = [o().id for o in self.outputs]
        return res

    def from_dict(self, json: dict, safe=False) -> bool:
        pass

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
            from .connection import Connection
            return Connection.connect(output, self)
        return False

    def connect_outgoing(self, input) -> bool:
        if input:
            from .connection import Connection
            return Connection.connect(self, input)
        return False

    def connect_multiple_outgoing(self, inputs: list) -> bool:
        worked = True
        if inputs:
            for input in inputs:
                from .connection import Connection
                if not Connection.connect(self, input):
                    worked = False
        return worked

    def disconnect_ingoing(self) -> bool:
        if self.get_ingoing():
            from .connection import Connection
            return Connection.disconnect(self.get_ingoing(), self)
        return True

    def disconnect_outgoing(self) -> bool:
        success = True
        if self.get_outgoing():
            for input in self.get_outgoing():
                print(input)
                from .connection import Connection
                if not Connection.disconnect(self, input):
                    success = False
        return success

    def is_changed(self) -> bool:
        if self.get_ingoing():
            return self.get_ingoing().is_changed()
        return self.ctype.is_changed()

    def update(self) -> bool:
        result = self.is_changed()
        return result
