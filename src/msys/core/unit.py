from .metadata import Metadata
from .interfaces import UnitInterface
from .serializer import Serializer


class Unit(Serializer, UnitInterface):
    def __init__(self, id, parent=None, metadata=None):
        super().__init__()
        if metadata is None:
            metadata = Metadata()
        self.id = id
        self.metadata = metadata
        self.parent = parent

    def own_id(self):
        return self.id

    def complete_id(self) -> []:
        identifiers = [self.own_id()]
        if self.parent:
            identifiers = self.parent.complete_id() + identifiers
        return identifiers

    def get_metadata(self) -> Metadata:
        return self.metadata

    def set_inverted(self, inverted: bool):
        self.metadata.inverted = bool

    def set_protected(self, protected: bool):
        super().set_protected(protected)
        for c in get_childs():
            set_protected(protected)

    def set_name(self, name: str):
        self.metadata.name = name

    def find(self, id: [], complete=True):
        if complete:
            length = len(id)

            def _find(elem: UnitInterface, index: int):
                tmp = elem.complete_id()
                if index >= 0:
                    if index < length:
                        if not id[index] == elem.own_id():
                            return None
                else:
                    if elem.own_id() in id:
                        index = id.index(elem.own_id())
                if index < 0:
                    return None
                if index == length - 1:
                    return elem
                if index < length - 1:
                    pos = index + 1
                    for child in elem.get_childs():
                        res = _find(child, pos)
                        if res:
                            return res
                return None

            return _find(self, -1)
        else:
            raise NotImplementedError

    def find_all(self, id: [], complete=True) -> []:
        result = []
        if complete:
            length = len(id)

            def _find(elem: UnitInterface, index: int):
                if index >= 0:
                    if index < length:
                        if not id[index] == elem.own_id():
                            return None
                else:
                    if elem.own_id() in id:
                        index = id.index(elem.own_id())
                if index < 0:
                    return None
                if index == length - 1:
                    result.append(elem)
                    return elem
                if index < length - 1:
                    pos = index + 1
                    for child in elem.get_childs():
                        _find(child, pos)
                return None

            _find(self, -1)
        else:
            raise NotImplementedError
        return result

    def get_childs(self) -> []:
        return []

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_parents(self) -> []:
        # if self.parent:
        #     parents = self.parent.get_parents()
        #     parents += [self.parent]
        #     return parents
        pass

    def update(self) -> bool:
        # changed = False
        # for child in self.get_childs():
        #     res = child.update()
        #     if res:
        #         changed = True
        # return changed
        pass

    def from_dict(self, json: dict, safe=False) -> bool:
        if not super().from_dict(json, safe):
            return False
        if "id" in json.keys():
            self.id = json["id"]

        if "metadata" in json.keys():
            if not self.metadata:
                self.metadata = Metadata()
            self.metadata.from_dict(json["metadata"])
        return True

    def to_dict(self) -> dict:
        res = super().to_dict()
        res["id"] = self.id
        res["identifier"] = self.complete_id()

        metadata = self.metadata.to_dict()
        if metadata:
            res["metadata"] =  metadata

        return res

import uuid

class UUnit(Unit):
    def __init__(self, id, parent = None, metadata = None):
        if id is None:
            id = str(uuid.uuid4())
        super().__init__(id, parent, metadata)