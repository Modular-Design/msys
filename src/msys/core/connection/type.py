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


class StandardType(TypeInterface):
    def __init__(self, default_value="", type_name="standard"):
        self.type_name = type_name
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

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "value": self.value,
        }

    def from_dict(self, json: dict) -> bool:
        try:
            self.value = json["value"]
        except Exception:
            return False
        return True