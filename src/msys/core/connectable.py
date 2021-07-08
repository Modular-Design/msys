from ..interfaces import ISerializer, IChild, IUpdatable
from .helpers import encrypt
from typing import Optional
from .metadata import Metadata
import requests


class Connectable(ISerializer, IChild, IUpdatable):
    def __init__(self,
                 id: Optional[object] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 default_value: Optional[dict] = None,
                 removable: Optional[bool] = False,
                 input=True,
                 parent = None):
        super().__init__()
        self.id = id
        self.parent = parent
        self.input = input
        self.meta = Metadata(name, description)
        self.data = default_value
        self.last_hash = encrypt(self.data)
        self.removable = removable

        self.ingoing = None

    def set_parent(self, node):
        self.parent = node

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

    def is_connectable(self, con:"Connectable") -> bool:
        res = self.parent.get_configuration()
        config = self.to_dict()
        config["data"] = con.data
        if self.input:
            res["inputs"]["elements"].append(config)
        else:
            res["outputs"]["elements"].append(config)

        response = requests.post(self.url + "/config", res)
        if response.status_code != 200:
            return False
        return True

    def set_ingoing(self, con: "Connectable") -> bool:
        if not self.is_connectable(con):
            print("[Connectable]: [ERROR] wrong format")
            return False
        if con.input == self.input:
            print("[Connectable]: [ERROR] same type")
            return False

        self.ingoing = dict(parent_id=con.parent.id, connectable_id=con.id)