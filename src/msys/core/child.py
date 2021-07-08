from ..interfaces import IChild, ISerializer
import uuid

class Child(IChild, ISerializer):
    def __init__(self,
                 parent: Optional["Child"] = None,
                 id: Optional[str] = None):
        self.parent = parent
        if id is None:
           id = str(uuid.uuid4())
        self.id = id

    def set_parent(self, node:"node") -> None:
        self.parent = None

    def get_local_id(self) -> str:
        return self.id

    def get_global_id(self) -> list:
        identifier = []
        if self.parent is not None:
            identifier = self.parent.get_global_id()
        return identifier + [self.id]

    def to_dict(self) -> dict:
        res = dict()
        res["id"] = self.id
        return res

    def load(self, json: dict) -> bool:
        if "id" in json.keys():
            self.id = json["id"]
        return True