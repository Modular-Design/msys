from ..core.connection import StandardType
import numpy as np


class VectorType(StandardType):
    def __init__(self, default_value):
        super().__init__(np.array([0]))
        self.set_value(default_value)

    def is_same(self, value) -> bool:
        return list(self.value) == list(value)

    def set_value(self, value) -> bool:
        if isinstance(value, np.ndarray):
            return super().set_value(value)
        elif isinstance(value, list):
            return super().set_value(np.array(value))
        elif isinstance(value, int) or isinstance(value, float):
            return super().set_value(np.array([value]))
        return False