from .interfaces import SerializerInterface
from .metadata import Metadata


class UnitInterface(SerializerInterface):
    def get_id(self):
        pass

    def identifier(self) -> []:
        pass

    def get_metadata(self) -> Metadata:
        pass

    def find(self, id: [], complete=True):
        """
        Returns the first element if it can find the element based on the identifier.
        If the identifier is complete (i.e. generated by the identifier()) the algorithm will be use a
        """
        pass

    def find_all(self, id: [], complete=True) -> []:
        """
        Returns the elements if it can find the element based on the identifier.

        """
        pass

    def get_childs(self) -> []:
        pass

    def get_parent(self):
        pass

    def get_parents(self) -> []:
        pass

    def update(self) -> bool:
        pass


class Unit(UnitInterface):
    def __init__(self, id, parent=None, metadata=None):
        if metadata is None:
            metadata = Metadata()
        self.id = id
        self.metadata = metadata
        self.parent = parent

    def get_id(self):
        return self.id

    def identifier(self) -> []:
        identifiers = [self.get_id()]
        if self.parent:
            identifiers = self.parent.identifier() + identifiers
        return identifiers

    def get_metadata(self) -> Metadata:
        return self.metadata

    def find(self, id: [], complete=True):
        if complete:
            length = len(id)

            def _find(elem: UnitInterface, index: int):
                tmp = elem.identifier()
                if index >= 0:
                    if index < length:
                        if not id[index] == elem.get_id():
                            return None
                else:
                    if elem.get_id() in id:
                        index = id.index(elem.get_id())
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
                        if not id[index] == elem.get_id():
                            return None
                else:
                    if elem.get_id() in id:
                        index = id.index(elem.get_id())
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

    def from_dict(self, json: dict) -> bool:
        found = False
        if "id" in json.keys():
            self.id = json["id"]
            found = True

        if "metadata" in json.keys():
            if not self.metadata:
                self.metadata = Metadata()
            self.metadata.from_dict(json["metadata"])
            found = True
        return found

    def to_dict(self) -> dict:
        res = dict(id=self.id)

        if self.metadata:
            res.update({"metadata": self.metadata.to_dict()})

        return res
