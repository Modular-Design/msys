from ..interfaces import IChild, ISerializer
import uuid
from typing import Optional

class Child(IChild, ISerializer):
    def __init__(self,
                 parent: Optional["Child"] = None,
                 id: Optional[str] = None):
        self.parent = parent
        self.id = id

    def set_parent(self, parent) -> None:
        self.parent = parent

    def get_parent(self):
        return self.parent

    def set_local_id(self, id: Optional[str] = None):
        if not id:
            id = str(uuid.uuid4())
        self.id = id

    def get_local_id(self) -> str:
        return self.id

    def get_global_id(self) -> list:
        identifier = []
        if self.parent is not None:
            identifier = self.parent.get_global_id()
        return identifier + [self.id]

    def to_dict(self) -> dict:
        res = dict()
        if self.id:
            res["id"] = self.id
        return res

    def load(self, json: dict) -> bool:
        if "id" in json.keys():
            self.id = json["id"]
        return True