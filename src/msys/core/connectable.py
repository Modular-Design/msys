from ..interfaces import IConnectable
from .child import Child
from .helpers import encrypt
from typing import Optional, List
from .metadata import Metadata
import requests
import weakref
from enum import Enum


class ConnectableFlag(Enum):
    INPUT = 0
    OUTPUT = 1

class Connectable(Child, IConnectable):
    def __init__(self,
                 # Child
                 parent: Optional["INode"] = None,
                 id: Optional[str] = None,

                 # Metadata
                 name: Optional[str] = None,
                 description: Optional[str] = None,

                 # new
                 default_value: Optional[dict] = None,
                 removable: Optional[bool] = False,
                 flag: Optional[ConnectableFlag] = ConnectableFlag.INPUT,
                 ):
        super().__init__(parent, id)
        self.flag = flag
        self.meta = Metadata(name, description)
        self.data = default_value
        self.removable = removable

        self.in_ref = None
        self.out_refs = []
        # important that get_data is called at the end
        self.last_hash = encrypt(self.get_data())

    def get_local(self):
        if self.flag is None:
            return self.flag
        if self.flag.name == "INPUT":
            return ConnectableFlag.OUTPUT
        else:
            return ConnectableFlag.INPUT

    def get_global(self):
        return self.flag

    def get_output(self) -> IConnectable:
        if not self.in_ref:
            return None
        connection = self.in_ref()
        if not connection:
            return None
        return connection.get_output()

    def get_inputs(self) -> List[IConnectable]:
        res = []
        for i in range(len(self.out_refs)):
            connection = self.out_refs[i]()
            if not connection:
                del self.out_refs[i]
            input = connection.get_input()
            if input:
                res.append(input)
        return res

    def get_data(self):
        output = self.get_output()
        if output:
            output.get_data()
        return self.data

    def is_data_valid(self, data) -> bool:
        if parent is None:
            return True

        res = self.parent.get_configuration()
        config = self.to_dict()
        config["data"] = data
        if self.output_ref:
            res["inputs"]["elements"].append(config)
        else:
            res["outputs"]["elements"].append(config)

        from .node import Node
        if isinstance(parent, Node):
            if self.parent.get_processor().change_config(config):
                return False
        else:
            for outgoing in self.get_inputs():# TODO: Think about a better solution of type validation
                if not outgoing.is_data_valid(data):
                    return False
        return True

    def set_data(self, data) -> bool:
        if self.is_data_valid(data):
            self.data = data
        return False

    def to_dict(self) -> dict:
        res = Child.to_dict(self)

        res["removable"] = self.removable
        res["data"] = self.get_data()
        res["meta"] = self.meta.to_dict()
        res["connected"] = self.is_connected()

        return res

    def load(self, json: dict) -> bool:
        Child.load(self, json)

        if "meta" in json.keys():
            self.meta.load(json["meta"])
        if "data" in json.keys():
            self.data = json["data"]
        if "removable" in json.keys():
            self.removable = json["removable"]
        return True

    def update(self) -> bool:
        hash = encrypt(self.get_data())
        res = hash == self.last_hash
        self.last_hash = hash
        return res

    def is_changed(self) -> bool:
        return encrypt(self.get_data()) == self.last_hash

    def is_connectable(self, output: IConnectable) -> bool:
        return self.is_data_valid(other.data)

    def set_ingoing(self, connection: "Connection"):
        if self.in_ref:
            conn = self.in_ref()
            if conn is not connection:
                conn.disconnect()
        self.in_ref = weakref.ref(connection)

    def set_outgoing(self, connections: List["Connection"]):
        for i in range(len(self.out_refs)):
            conn = self.out_refs[i]()
            if conn not in connections:
                conn.disconnect()

        self.out_refs = []
        for conn in connections:
            self.add_outgoing(conn)

    def add_outgoing(self, connection: "Connection"):
        found = False
        for i in range(len(self.out_refs)):
            conn_ref = self.out_refs[i]
            if conn_ref() is connection:
                found = True
                break

        if not found:
            self.outgoing.append(weakref.ref(connection))

    def remove_outgoing(self, connection: "Connection"):
        for i in range(len(self.out_refs)):
            conn_ref = self.out_refs[i]
            if conn_ref() is connection:
                del self.out_refs[i]

    def is_removable(self) -> bool:
        return self.removable

    def is_connected(self) -> bool:
        if self.get_global() == ConnectableFlag.INPUT:
            if self.get_output():
                return True
        elif self.get_global() == ConnectableFlag.OUTPUT:
            if self.get_inputs():
                return True
        return False