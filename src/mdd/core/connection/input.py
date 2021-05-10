from ..unit import UniqueUnit
from .connectable import ConnectableInterface
from .type import TypeInterface


class Input(UniqueUnit, ConnectableInterface):
    def __init__(self, types: list, output=None, optimized=False, generator=None):
        super().__init__()
        self.generator = generator
        self.types = types
        self.type_id = 0
        self.output = output
        self.optimized = optimized

    def get_value(self):
        if self.output:
            return self.output.get_value()
        return self.types[self.type_id].get_value()

    def set_value(self, value) -> bool:
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

    def connect(self, connectable, both=True) -> bool:
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

