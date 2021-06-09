from .interfaces import TypeInterface
from .registrable import Registrable, get_class_info


class Type(Registrable, TypeInterface):
    def __init__(self, default_value=""):
        super().__init__()
        self.changed = True
        self.value = default_value
        self.mro = []
        parents = self.__class__.__mro__
        for parent in parents:
            res = get_class_info(parent)
            if res["package"]:
                self.mro.append(res)

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
        if not issubclass(other.__class__, Type):
            return False
        if get_class_info(self.__class__) not in other.mro:
            return False
        return True

    def to_dict(self) -> dict:
        res = super().to_dict()
        res["value"] = self.value
        if self.mro:
            res["mro"] = self.mro
        return res

    def from_dict(self, json: dict) -> bool:
        found = super().from_dict(json)
        if "mro" in json.keys():
            self.mro = json["mro"]
        if "value" not in json.keys():
            return False
        self.value = json["value"]
        return True
