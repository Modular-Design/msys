from ..interfaces import IUpdatable
from .child import Child
from .helpers import encrypt
from typing import Optional
from .metadata import Metadata
import requests


class ConnectableFlag(Enum):
    INPUT = 0
    OUTPUT = 1

class Connectable(Child, IUpdatable):
    def __init__(self,
                 parent: Optional[str] = None,,
                 id: Optional[str] = None,,

                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 default_value: Optional[dict] = None,
                 removable: Optional[bool] = False,
                 flag: Optional[ConnectableFlag] = ConnectableFlag.INPUT,
                 ):
        super().__init__(parent, id)
        self.flag = flag
        self.meta = Metadata(name, description)
        self.data = default_value
        self.last_hash = encrypt(self.data)
        self.removable = removable

        self.input = None
        self.outputs = []

    def get_local(self):
        if self.flag is None:
            return self.flag
        if self.flag.name == "INPUT":
            return ConnectableFlag.OUTPUT
        else:
            return ConnectableFlag.INPUT

    def get_global(self):
        return self.flag

    def get_ingoing(self):
        if self.input:
            return self.input()
        return None

    def get_outgoing(self) -> []:
        res = []
        for out in self.outputs:
            obj = out()
            if obj:
                res.append(obj)
        return res

    def get_data(self):
        if self.get_ingoing():
            self.ctype.set_value(self.get_ingoing().get_value())
        return self.ctype.get_value()

    def set_data(self, value) -> bool:
        if not self.get_ingoing():
            self.ctype.set_value(value)

        return True

    def to_dict(self) -> dict:
        res = Child.to_dict(self)

        res["removable"] = self.removable
        res["data"] = self.data

        res["meta"] = self.meta.to_dict()

        return res

    def load(self, json: dict) -> bool:
        Child.load(self, json)

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



    def set_ingoing(self, outpu: "Connectable") -> bool:
        if not self.is_connectable(con):
            print("[Connectable]: [ERROR] wrong format")
            return False
        if con.input == self.input:
            print("[Connectable]: [ERROR] same type")
            return False

        self.ingoing = dict(parent_id=con.parent.id, connectable_id=con.id)