from src.mdd.core.unit import UniqueUnit
from .connectable import ConnectableInterface

class Output(UniqueUnit, ConnectableInterface):
    def __init__(self, default_value=[0.0], inputs=[], optimized=False):
        super().__init__()
        self.return_value = default_value
        self.inputs = inputs
        self.optimized = optimized

    def value(self):
        return self.return_value

    def is_optimized(self) -> bool:
        return self.optimized

    def set_optimized(self, optimized: bool) -> bool:
        self.optimized = optimized
        return self.is_optimized()

    def connect(self, connectable, both=True) -> bool:
        from .input import Input
        if not isinstance(connectable, Input):
            return False
        for i in self.inputs:
            if i.getid() == connectable.getid():
                return False
        if both:
            if not connectable.connect(self, False):
                return False

        self.inputs.append(connectable)
        return True

    def connectAll(self, connectables: [], both=True) -> bool:
        result = True
        for c in connectables:
            if not self.connect(c, both):
                result = False
        return result

    def disconnect(self, connectable=None, both=True) -> bool:
        for i in range(len(self.inputs)):
            input = self.inputs[i]
            if connectable:
                if connectable.getid() != input.getid():
                    continue
            if both:
                if not input.disconnect(self, False):
                    return False
            self.inputs.remove(input)
            if connectable:
                if connectable.getid() == input.getid():
                    return True
        return True