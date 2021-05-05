def includes(array: [], elements: []) -> bool:
    for e in elements:
        if not e in array:
            return False
    return True


class SerializerInterface:
    def from_dict(self, json: dict) -> bool:
        """Load class from dictionary."""
        pass

    def to_dict(self) -> dict:
        """Gerenate dict from class."""
        pass


class SerializableList(SerializerInterface):
    def __init__(self, elems: [], generator=None):
        self.elems = elems
        self.generator = generator
        self.changeable = True
        if self.generator is None:
            self.changeable = False

    def from_dict(self, json: dict) -> bool:
        if not includes(json.keys(), ["elements", "size"]):
            return False
        elements = json["elements"]
        size = json["size"]
        if size !=len(self.elems) and self.changeable:
            diff = size - len(self.elems)
            if diff < 0:
                # remove:
                for i in range(abs(diff)):
                    self.elems.pop()
            else:
                for i in range(diff):
                    self.elems.append(self.generator(len(self.elems)))
        else:
            return False

        for new_e in elements:
            if not "id" in new_e:
                break
            for old_e in self.elems:
                if new_e["id"] == old_e.id:
                    old_e.from_dict(new_e)
                    break
        return True

    def to_dict(self) -> dict:
        return dict(elements=self.elems, size=len(self.elems), changeable=self.changeable)

    def update(self) -> bool:
        changed = False
        for e in self.elems:
            if e.update():
                changed = True
        return changed

    def __setitem__(self, elemno, elem):
        self.elems[elemno] = elem

    def __getitem__(self, elemno):
        return self.elems[elemno]

    def __len__(self):
        return len(self.elems)

