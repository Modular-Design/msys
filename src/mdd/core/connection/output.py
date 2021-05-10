from ..unit import UniqueUnit
from .connectable import ConnectableInterface
from .type import TypeInterface


class Output(UniqueUnit, ConnectableInterface):
    def __init__(self, type, inputs=None, optimized=False):
        super().__init__()
        self.type = type
        self.inputs = inputs
        if self.inputs is None:
            self.inputs = []
        self.optimized = optimized

    def get_value(self):
        return self.type.get_value()

    def set_value(self, value) -> bool:
        return self.type.set_value(value)

    def is_optimized(self) -> bool:
        return self.optimized

    def set_optimized(self, optimized: bool) -> bool:
        self.optimized = optimized
        return self.is_optimized()

    def is_changed(self) -> bool:
        return self.type.is_changed()

    def is_connected(self) -> bool:
        if self.inputs:
            return True
        return False

    def connect(self, connectable, both=True) -> bool:
        from .input import Input
        if not isinstance(connectable, Input):
            return False
        for i in self.inputs:
            if i.get_id() == connectable.get_id():
                return False
        if both:
            if not connectable.connect(self, False):
                return False

        self.inputs.append(connectable)
        return True

    def connect_all(self, connectables: [], both=True) -> bool:
        result = True
        for c in connectables:
            if not self.connect(c, both):
                result = False
        return result

    def disconnect(self, connectable=None, both=True) -> bool:
        if not self.inputs:
            return False
        for i in range(len(self.inputs)):
            input = self.inputs[i]
            if connectable:
                if connectable.get_id() != input.get_id():
                    continue
            if both:
                if not input.disconnect(self, False):
                    return False
            self.inputs.remove(input)
            if connectable:
                if connectable.get_id() == input.get_id():
                    return True
        return True

    def update(self) -> bool:
        return self.is_changed()
