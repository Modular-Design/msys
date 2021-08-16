from pymsys import INode

import time


class Priority:
    def __init__(self, node: INode):
        self.node = node
        self.inputs = 0
        self.time = 0
        self.changes = 0
        self.outputs = 0

        self.dt = 0

    def __lt__(self, other):
        # priority by:
        # lower connected inputs
        if self.inputs != other.inputs:
            return self.inputs < other.inputs

        # then lower time score
        if self.time != other.time:
            return self.time < other.time

        # then lowest change counter: connected inputs - input changes
        if self.inputs - self.changes != other.inputs - other.changes:
            return self.inputs - self.changes < other.inputs - other.changes

        # then highest changes
        if self.changes != other.changes:
            return self.changes > other.changes

        # then highest output connections
        if self.outputs != other.outputs:
            return self.outputs < other.outputs

        return 1

    def update_numbers(self):
        self.inputs = 0
        self.changes = 0
        for input in self.node.get_inputs():
            if input.is_changed():
                self.changes += 1
            if input.is_connected():
                self.inputs += 1

        self.outputs = 0
        for output in self.node.get_outputs():
            if input.is_connected():
                self.outputs += 1

        if self.dt <= 1:
            self.dt = 1
        import math
        self.time = round(math.log10(self.dt))

    def update(self) -> bool:
        start = time.time()
        res = self.node.update()
        self.dt = time.time() - start

        self.update_numbers()
        return res