class TypeInterface:
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

    @staticmethod
    def is_compatible(output_type, input_types: list) -> int:
        for i, t in enumerate(input_types):
            if t.is_connectable(output_type):
                return i
        return -1


class StandardType(TypeInterface):
    def __init__(self, default_value):
        self.changed = True
        self.value = default_value

    def is_same(self, value) -> bool:
        return self.value == value

    def get_value(self):
        return self.value

    def set_value(self, value) -> bool:
        self.changed = not self.is_same(value)
        if self.changed:
            self.value = value
        return self.changed

    def is_changed(self) -> bool:
        return self.changed

    def is_connectable(self, other) -> bool:
        if not issubclass(other.__class__, self.__class__):
            return False
        return True