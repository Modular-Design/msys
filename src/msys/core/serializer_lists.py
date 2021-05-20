from .interfaces import SerializerInterface
from .connectable import ConnectableFlag, ConnectableInterface
from .unit import UnitInterface


class SerializableList(SerializerInterface):
    def __init__(self, parent,  elems: [], flag: ConnectableFlag):
        self.parent = parent
        self.flag = flag
        self.elems = []
        self.changed = True
        for e in elems:
            self.add(e)

    def add(self, connectable: UnitInterface):
        connectable.parent = self.parent
        self.elems.append(connectable)
        return True

    def from_dict(self, json: dict) -> bool:
        success = True
        for i in range(len(json)):
            if not self.elems[i].from_dict(json[i]):
                success = False
        return success

    def to_dict(self) -> dict:
        res = []
        for e in self.elems:
            res.append(e.to_dict())
        return res

    def update(self) -> bool:
        changed = False
        for e in self.elems:
            if e.update():
                changed = True
        res = self.changed
        self.changed = changed
        return res

    def __setitem__(self, elemno, elem):
        self.elems[elemno] = elem

    def __getitem__(self, elemno):
        return self.elems[elemno]

    def __len__(self):
        return len(self.elems)



class ConnectableList(SerializableList):
    def __init__(self, parent, elems: [], flag):
        self.connections = 0
        self.length = 0
        self.changed_count = 0
        super().__init__(parent, elems, flag)
        self.update_numbers()

    def add(self, connectable: ConnectableInterface) -> bool:
        connectable.set_global(self.flag)
        return super().add(connectable)

    def get_no_connected(self) -> int:
        return self.connections

    def get_no_elems(self) -> int:
        return self.length

    def get_no_changed(self) -> int:
        return self.changed_count

    def update_numbers(self) -> bool:
        self.length = len(self.elems)
        self.connections = 0
        self.changed_count = 0
        for e in self.elems:
            if self.flag == ConnectableFlag.INPUT:
                if e.get_ingoing():
                    self.connections += 1
            else:
                if e.get_outgoing():
                    self.connections += 1
            if e.is_changed():
                self.changed_count += 1

    def update(self) -> bool:
        res = super().update()
        self.update_numbers()
        return res