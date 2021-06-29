from ..interfaces import ISerializer, IChild, IUpdatable
from .helpers import encrypt
from typing import Optional
from .metadata import Metadata

class Connectable(ISerializer, IChild, IUpdatable):
    def __init__(self,
                 id: Optional[object] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 default_value: Optional[dict] = None,
                 removable: Optional[bool] = False):
        super().__init__()
        self.id = id
        self.parent = None
        self.meta = Metadata(name, description)
        self.data = default_value
        self.last_hash = encrypt(self.data)
        self.removable = removable

    def set_parent(self, module):
        self.parent = module

    def to_dict(self) -> dict:
        res = dict()

        res["id"] = self.id
        res["removable"] = self.removable
        res["data"] = self.data

        res["meta"] = self.meta.to_dict()

        return res

    def load(self, json: dict) -> bool:
        if "id" in json.keys():
            self.id = json["id"]
        if "meta" in json.keys():
            self.meta.load(json["meta"])
        if "data" in json.keys():
            self.data = "data"
        if "removable" in json.keys():
            self.removable = "removable"
        return True

    def update(self) -> bool:
        hash = encrypt(self.data)
        res = hash == self.last_hash
        self.last_hash = hash
        return res

    def is_changed(self) -> bool:
        return encrypt(self.data) == self.last_hash

